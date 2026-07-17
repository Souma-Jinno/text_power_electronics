#!/usr/bin/env python3
"""
asc_to_net.py -- .asc (LTspice schematic) -> SPICE netlist (.net) + connectivity check.

Fallback tool used because this machine has no wine/LTspice installed
(task 20260717_ltspice_asc_svg_pipeline_pwreletron.md, Phase 0 permits a
self-implemented .asc -> netlist parser when the real environment is unavailable).

Only supports the small custom symbol set in ../tools/symbols/ (voltage, current, res,
diode, zener, npn, pnp, nmos, ind, cap, sw, opamp) authored for this pipeline --
SYMBOL_PINS below must have an entry for every symbol type used in a schematic. Extend
it when new chapters introduce new symbols.

"opamp" is a special case (added chapter07): it has no real SPICE primitive of its own,
so build_netlist() emits it as an ideal E-element (voltage-controlled voltage source)
line "E<name> <out> 0 <in+> <in-> <gain>" instead of the generic "<inst> <nets> <value>"
line every other symbol gets -- see the isinstance check near the bottom of
build_netlist(). This approximates LTspice's UniversalOpamp2 macro model as a single
high-gain VCVS with no output saturation/GB-limit; document that simplification in the
chapter's VERIFICATION_NOTES.md wherever it's used.

Symbol type names match real LTspice's own library part names (verified 2026-07-17/18
against book/figures/ltspice/corpus/, a set of real .asc files -- 13 LTspice-bundled
examples + 16 of the author's own past circuits -- committed by the professor directly to
this repo for few-shot .asc authoring). This machine still has no wine/real LTspice, so the
*pin geometry* below remains this pipeline's own internally-consistent invention, not
verified against the real .asy library; only the symbol *names* were aligned to the corpus.
"""
import argparse
import math
import sys
from pathlib import Path

# Local pin coordinates (x, y) at rotation R0, before mirror/rotate/translate.
# Order matches the physical pin role documented in each .asy file, and also
# matches the SPICE node order expected for that element's card (e.g. Q: C B E,
# M: D G S B).
SYMBOL_PINS = {
    "voltage":  [(0, 0), (0, 96)],   # + , -
    "current":  [(0, 0), (0, 96)],   # + , -  (I<name> n+ n- value)
    "res":      [(0, 0), (0, 96)],   # 1 , 2
    "ind":      [(0, 0), (0, 96)],   # 1 , 2 (same 2-pin pattern as res)
    "cap":      [(0, 0), (0, 96)],   # 1 , 2 (same 2-pin pattern as res)
    "diode":    [(0, 0), (0, 96)],   # anode (A) , cathode (K)
    "zener":    [(0, 0), (0, 96)],   # anode (A) , cathode (K) -- same footprint as
                                      # diode, distinct .asy artwork (kinked cathode
                                      # bar) and a D-model with BV/IBV for breakdown
    # in+ (non-inverting), in- (inverting), out -- ideal op-amp, see module docstring
    "opamp":    [(0, 16), (0, 80), (64, 48)],
    "npn":      [(32, 0), (0, 48), (32, 96)],   # collector, base, emitter
    "pnp":      [(32, 0), (0, 48), (32, 96)],   # collector, base, emitter
    # drain, gate, source, body -- body pin coordinate is deliberately the same
    # point as the source pin so the union-find node merge (exact-coordinate
    # match) ties B=S automatically without any special-case code.
    "nmos":     [(32, 0), (0, 48), (32, 96), (32, 96)],
    # N+ , N- , NC+ , NC-  (ngspice/SPICE "S" voltage-controlled switch element,
    # matches the "sw" part the professor's own corpus/prof_00_boost.asc uses
    # for the chopper switch, driven by a PULSE control source into NC+/NC-
    # via matching net-name FLAGs, not a direct wire -- see named_groups above)
    "sw":       [(32, 0), (32, 96), (0, 32), (0, 64)],
}

SYMBOL_PREFIX = {
    "voltage": "V",
    "current": "I",
    "res": "R",
    "ind": "L",
    "cap": "C",
    "diode": "D",
    "zener": "D",
    "npn": "Q",
    "pnp": "Q",
    "nmos": "M",
    "sw": "S",
    "opamp": "E",
}


def transform_pin(local_xy, sym_x, sym_y, rotation):
    x, y = local_xy
    mirrored = rotation[0] == "M"
    angle = int(rotation[1:])
    if mirrored:
        x = -x
    theta = math.radians(angle)
    xr = x * math.cos(theta) - y * math.sin(theta)
    yr = x * math.sin(theta) + y * math.cos(theta)
    xr = round(xr)
    yr = round(yr)
    return (xr + sym_x, yr + sym_y)


class DSU:
    def __init__(self):
        self.parent = {}

    def find(self, a):
        self.parent.setdefault(a, a)
        while self.parent[a] != a:
            self.parent[a] = self.parent[self.parent[a]]
            a = self.parent[a]
        return a

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb


def parse_asc(path):
    wires = []
    symbols = []
    flags = []
    spice_lines = []
    cur = None
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        head = parts[0]
        if head == "WIRE":
            x1, y1, x2, y2 = map(int, parts[1:5])
            wires.append(((x1, y1), (x2, y2)))
        elif head == "SYMBOL":
            name = parts[1]
            x, y = int(parts[2]), int(parts[3])
            rotation = parts[4] if len(parts) > 4 else "R0"
            cur = {"symbol_name": name, "x": x, "y": y, "rotation": rotation,
                   "inst_name": None, "value": None}
            symbols.append(cur)
        elif head == "SYMATTR" and cur is not None:
            if parts[1] == "InstName":
                cur["inst_name"] = " ".join(parts[2:])
            elif parts[1] == "Value":
                cur["value"] = " ".join(parts[2:])
        elif head == "FLAG":
            x, y = int(parts[1]), int(parts[2])
            net_name = " ".join(parts[3:])
            flags.append({"x": x, "y": y, "net_name": net_name})
        elif head == "TEXT":
            if "!" in line:
                _, content = line.split("!", 1)
                spice_lines.append(content.strip())
    return wires, symbols, flags, spice_lines


def build_netlist(asc_path):
    wires, symbols, flags, spice_lines = parse_asc(asc_path)

    dsu = DSU()
    for (p1, p2) in wires:
        dsu.union(p1, p2)

    # SPICE convention: every GND flag (net_name "0") is the same global node,
    # even when no wire physically links the separate flag points.
    gnd_points = [(f["x"], f["y"]) for f in flags if f["net_name"] == "0"]
    for p in gnd_points[1:]:
        dsu.union(gnd_points[0], p)

    # Same convention applies to any *named* net label, not just "0": in real
    # LTspice, two FLAGs sharing a non-ground name (e.g. two "Vsw" labels) are
    # the same electrical node even with no wire between them -- this is how
    # the professor's own corpus (prof_00_boost.asc etc.) hops the switch
    # gate-drive pulse across the sheet without a long physical wire. Union
    # every group of same-named non-ground flags so our own connectivity
    # checker (node_member_count below) doesn't false-flag them as dangling.
    named_groups = {}
    for f in flags:
        if f["net_name"] != "0":
            named_groups.setdefault(f["net_name"], []).append((f["x"], f["y"]))
    for pts in named_groups.values():
        for p in pts[1:]:
            dsu.union(pts[0], p)

    # Register every symbol pin and every flag point as a node (union-find
    # merges points that share exact coordinates automatically via dict key).
    symbol_pin_abs = []  # (symbol, [abs pin coords])
    errors = []
    for sym in symbols:
        stype = sym["symbol_name"]
        if stype not in SYMBOL_PINS:
            errors.append(f"未知のシンボル種別 '{stype}' (SYMBOL_PINSに未登録)")
            continue
        pins_abs = [transform_pin(p, sym["x"], sym["y"], sym["rotation"])
                    for p in SYMBOL_PINS[stype]]
        for p in pins_abs:
            dsu.find(p)  # register node even if isolated
        symbol_pin_abs.append((sym, pins_abs))

    for f in flags:
        dsu.find((f["x"], f["y"]))

    # Assign net names per connected component (root -> name)
    root_name = {}
    # 1) ground first (net_name == "0")
    for f in flags:
        if f["net_name"] == "0":
            root_name[dsu.find((f["x"], f["y"]))] = "0"
    # 2) explicit non-ground net labels
    for f in flags:
        if f["net_name"] != "0":
            r = dsu.find((f["x"], f["y"]))
            root_name.setdefault(r, f["net_name"])
    # 3) auto-numbered nets for anything left
    counter = 1
    for sym, pins_abs in symbol_pin_abs:
        for p in pins_abs:
            r = dsu.find(p)
            if r not in root_name:
                root_name[r] = f"N{counter:03d}"
                counter += 1

    # Connectivity check: every pin must be part of some net that has >=2
    # distinct members overall (other pin or a FLAG) -- a dangling pin with
    # no wire, no other component, and no flag is an error. The ground net
    # ("0") is exempt from the >=2 rule: a single flag legitimately grounds
    # one branch.
    node_member_count = {}
    for sym, pins_abs in symbol_pin_abs:
        for p in pins_abs:
            r = dsu.find(p)
            node_member_count[r] = node_member_count.get(r, 0) + 1
    for f in flags:
        r = dsu.find((f["x"], f["y"]))
        node_member_count[r] = node_member_count.get(r, 0) + 1
    for sym, pins_abs in symbol_pin_abs:
        for i, p in enumerate(pins_abs):
            r = dsu.find(p)
            net = root_name.get(r, "?")
            if node_member_count[r] < 2 and net != "0":
                errors.append(
                    f"未接続ピン: {sym['inst_name']} pin{i+1} at {p} "
                    f"(net={net}, 他のピン/配線/FLAGと接続されていない)"
                )

    has_ground = any(f["net_name"] == "0" for f in flags)
    if not has_ground:
        errors.append("回路にGND(FLAG ... 0)が存在しない")

    # Build SPICE element lines
    elem_lines = []
    for sym, pins_abs in symbol_pin_abs:
        stype = sym["symbol_name"]
        nets = [root_name[dsu.find(p)] for p in pins_abs]
        inst = sym["inst_name"] or f"{SYMBOL_PREFIX.get(stype,'X')}?"
        value = sym["value"] or ""
        if stype == "opamp":
            # SYMBOL_PINS["opamp"] pin order is (in+, in-, out); ngspice has no
            # built-in opamp element, so emit it as an ideal E-source instead:
            # E<name> <out+> <out-(gnd)> <in+> <in-> <gain>. See module docstring.
            in_plus, in_minus, out = nets
            elem_lines.append(f"{inst} {out} 0 {in_plus} {in_minus} {value or '1e5'}")
        else:
            elem_lines.append(f"{inst} {' '.join(nets)} {value}".rstrip())

    return elem_lines, spice_lines, errors, root_name


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("asc_file")
    ap.add_argument("-o", "--output", help="output .net path (default: alongside .asc)")
    args = ap.parse_args()

    asc_path = Path(args.asc_file)
    out_path = Path(args.output) if args.output else asc_path.with_suffix(".net")

    elem_lines, spice_lines, errors, root_name = build_netlist(asc_path)

    header = f"* netlist auto-generated by asc_to_net.py from {asc_path.name}"
    body = [header] + elem_lines + spice_lines + [".end"]
    out_path.write_text("\n".join(body) + "\n", encoding="utf-8")

    print(f"netlist written: {out_path} ({len(elem_lines)} elements, {len(spice_lines)} directive lines)")
    if errors:
        print("接続チェック NG:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("接続チェック OK: 未接続ピンなし、GNDあり")


if __name__ == "__main__":
    main()
