#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
net2asc.py -- deterministic ngspice .cir  ->  LTspice .asc generator (v2).

THREE LAYOUTS
-------------
    --layout grid   v1, preserved byte-for-byte: no routing at all, every pin
                    gets a stub + FLAG.  Correct, unreadable.
    --layout flow   v2: half-bridge topologies.  The power path is drawn with
                    REAL orthogonal wires around a vertical switching leg.
    --layout spine  v2b: GENERAL wired layout for everything else.  The main
                    signal/power path becomes a horizontal SPINE and every
                    remaining chain hangs off it as a vertical branch, each
                    with its own ground symbol.  See section 5B of NET2ASC.md.
    --layout auto   (default) flow, then spine, then grid.

v2c (2026-08-28) adds three things to the spine layout, all described in
section 5C of NET2ASC.md:

  1. ISLAND PACKING.  Islands used to stack in one column, which made an
     8000-unit ribbon out of an LLC deck.  They are now drawn stacked (so each
     one's placement validator only sees finished geometry) and afterwards
     moved as rigid bodies onto SHELVES, with the shelf width searched for the
     most page-shaped result.  Deterministic; connectivity untouched.
  2. ONE STRUCTURAL TEMPLATE -- the 4-switch bridge feeding a K-coupled
     inductor.  Detected the way find_leg() detects a half-bridge, from the
     electrical definition and never from names: two legs across a common rail
     and a common return, two midpoints, and a path of ordinary two-terminal
     elements between the midpoints that carries an inductor named by a K card.
     Drawn rail-on-top / return-at-the-bottom / legs as vertical columns /
     primary across the middle.  If it does not match, nothing happens and the
     ordinary spine layout runs; the template is never a reason to fail.
  3. TEXT in the collision checker.  Attribute text (InstName / Value) and net
     labels get ESTIMATED bounding boxes using asc2svg.py's own advance-width
     metric, so the checker and the renderer agree.  A text overlap is a
     placement failure that triggers the existing rollback-and-retry; if every
     candidate collides, the placement is ACCEPTED ANYWAY and the overlap is
     counted and reported.  Connectivity is never traded for typography.

v2b in one paragraph: the chain graph is searched for the simple path that
maximises (elements on the path) - (star penalty on its interior nets), tied
on element count and then on how HOMOGENEOUS the path is -- which is what
makes a Dickson pump's six series diodes win over five diodes plus a pump
capacitor.  Ground may only END a spine, so parts of a circuit that touch only
through ground become separate ISLANDS, each with its own spine, stacked in
their own band.  Branches are placed speculatively and validated against
everything already on the sheet (wire/wire contact between different nets, a
pin or FLAG on a foreign wire, overlapping symbol bodies); a branch that fails
is rolled back and retried one column over or one row up, and only if every
candidate fails does that one chain fall back to a net label.  Connectivity is
never traded for looks.

v2 in one paragraph: two-terminal elements (and a MOSFET's drain-source) are
contracted into SERIES CHAINS at every net that carries exactly two power
terminals; a HALF-BRIDGE LEG is then found graph-theoretically (two chains
sharing a net, the upper presenting a MOSFET source to it and the lower a
MOSFET drain).  The leg is drawn vertically, the chain feeding the high-side
drain becomes the top rail (left to right), the chain leaving the switch node
becomes the output run, chains ending on ground drop to a ground flag, and gate
drive / anything unroutable goes to a labelled band underneath.  Symbol
orientation is solved from the .asy pin coordinates, not from a lookup table.
Before anything is written, a geometric self-check replays LTspice's contact
semantics over the emitted figure and refuses any accidental short.  See
NET2ASC.md section 5.

DESIGN DECISION (v1 / --layout grid): NO WIRE ROUTING AT ALL.
------------------------------------------------------------
Automatic schematic routing is hard and, done badly, silently produces WRONG
connectivity.  This generator therefore refuses to route.  Instead:

  1. every drawable element is dropped on a COARSE GRID at a fixed pitch that
     is arithmetically guaranteed to be larger than the widest possible
     per-element coordinate footprint, so two different elements can NEVER
     produce a coincident pin / stub / flag coordinate (see CELL_W / CELL_H
     and the assertion in `_check_pitch()`);
  2. from every pin ONE short stub WIRE is drawn (STUB = 32 units, i.e. two
     LTspice grid steps), pointing away from the symbol body;
  3. at the far end of that stub a `FLAG <x> <y> <netname>` is placed.

LTspice joins same-named FLAGs into one net with no wire in between, so the
connectivity of the emitted schematic is EXACTLY the connectivity of the input
netlist -- it is correct BY CONSTRUCTION, not by routing luck.  Routing has
been reduced to labelling.

*** READABILITY IS KNOWINGLY SACRIFICED IN THE GRID LAYOUT. ***
The result is a "net-label soup": a rectangular field of unconnected-looking
components, each surrounded by little labelled whiskers.  It is electrically
exact and machine-checkable, but it does not look like a hand-drawn power
converter.  Making it readable (real wiring for the power path, template
placement for known topologies) is explicitly deferred to v2.  See NET2ASC.md.

Elements with no symbol in ltsym/ (B-sources, E/G/F/H, X subcircuit calls that
are not 3-terminal `d g s` MOSFET wrappers, ...) are NOT drawn.  They are emitted verbatim as `TEXT x y Left 2 !<line>` SPICE
directives, exactly the way the hand-built dist_asc_s6/improved_s6.asc already
carries its Bgsr*/Dsr*/Rsnb*/Csnb* cards.  Same for .param/.model/.options/
.tran/.ic/.include and K coupling statements.

A `.control ... .endc` block is DROPPED (LTspice has no equivalent; it would
be meaningless inside a .asc).  A `* dropped .control block` note is written
into the .asc as a plain comment TEXT record.

Symbol mapping
--------------
    R -> res      C -> cap      L -> ind (ind2 if named by a K statement,
    D -> diode    V -> voltage       so the phasing dot is explicit)
    S -> sw   (4 terminals: A, B, NC+, NC-)
    X -> nmos (3 terminals D, G, S) when the subckt is SIC_650 / SR_80 or is
              defined as `.subckt NAME d g s` in an .include'd file

Pin order is `PINATTR SpiceOrder` of the `PIN` records in the .asy (read since
2026-09-04; the PIN file order is used only for a symbol that states no
SpiceOrder, and that fallback is printed as a NOTE).  Same loader, and
therefore the same convention, as asc2ngspice.py.

Verification (on by default, --no-verify to skip)
-------------------------------------------------
    input.cir --[net2asc]--> out.asc --[asc2ngspice]--> out_rt.cir
then the TOPOLOGY of input.cir and out_rt.cir is compared: element names must
match one-to-one, and there must exist a BIJECTION between the two decks' net
names that makes every element's terminal-ordered net tuple identical.  Net
names may therefore be renamed; what must match is which element terminals
share which nets.  Any mismatch is printed and the process exits non-zero.

Round-trip re-extractor: asc2ngspice.py (NOT tools_ascnet_check.py).  See
NET2ASC.md and ascnet_check2.py for why.  It is a re-extractor, NOT an
"authority": the 2026-08-27 audit showed that calling it the authority made
its blind spots the blind spots of the whole verification.  --check now runs
three independent checks (contact analysis on the .asc geometry, the round
trip, duplicate element names); see NET2ASC.md 3.5 for what they do and do
not catch.

Usage
-----
    python3 net2asc.py input.cir [-o out.asc]
                       [--layout auto|flow|spine|grid] [--v1] [--spine]
                       [--no-verify] [--keep-rt] [--symdir DIR] [--cols N]
                       [--stub N] [--quiet]
    python3 net2asc.py input.cir --check existing.asc      # re-verify only
"""

import sys, os, re, argparse, importlib.util
from collections import OrderedDict, defaultdict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LIBDIR = os.path.join(HERE, 'ltsym')


def _load_module(name, path):
    # Byte-compiling asc2ngspice.py drops a tools/__pycache__/ into the
    # package the first time anything is run from it.  The self-test is
    # supposed to leave the package exactly as it was unpacked
    # (2026-09-04 audit C3), so bytecode writing is suppressed for this one
    # import and the interpreter's own setting is restored afterwards.
    old = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        sys.dont_write_bytecode = old
    return mod


# reuse the project's .asy loader + orientation table rather than reinventing
_A2N = _load_module('_a2n_for_net2asc', os.path.join(HERE, 'asc2ngspice.py'))
load_asy = _A2N.load_asy
ORI = _A2N.ORI


# ===========================================================================
# 1. netlist (.cir) parsing
# ===========================================================================

# how many leading tokens after the element name are NODES, per type letter.
# (Only used for topology extraction / comparison, and for the drawable set.)
NODE_COUNT = {
    'R': 2, 'C': 2, 'L': 2, 'D': 2, 'V': 2, 'I': 2, 'B': 2,
    'S': 4, 'W': 2, 'E': 4, 'G': 4, 'F': 2, 'H': 2,
    'Q': 3, 'J': 3, 'Z': 3, 'M': 4, 'T': 4, 'O': 4, 'U': 2,
}
# element letters we can draw with an ltsym symbol
DRAWABLE = {'R': 'res', 'C': 'cap', 'L': 'ind', 'D': 'diode', 'V': 'voltage', 'S': 'sw'}

DIRECTIVE_KEEP = ('.param', '.model', '.options', '.option', '.tran', '.ac', '.dc',
                  '.op', '.four', '.ic', '.nodeset', '.func', '.include', '.inc',
                  '.lib', '.save', '.meas', '.measure', '.step', '.global', '.temp')


class Element(object):
    __slots__ = ('name', 'letter', 'nodes', 'value', 'raw', 'lineno', 'params')

    def __init__(self, name, letter, nodes, value, raw, lineno, params=''):
        self.name = name
        self.letter = letter
        self.nodes = nodes
        self.value = value
        self.raw = raw
        self.lineno = lineno
        self.params = params

    def __repr__(self):
        return 'Element(%s,%s,%s)' % (self.name, self.letter, self.nodes)


class Deck(object):
    def __init__(self):
        self.elements = []        # Element, drawable or not
        self.directives = []      # verbatim '.xxx' cards (strings)
        self.couplings = []       # K statements (strings)
        self.comments = []        # '*' comment text (strings)
        self.dropped_control = []  # lines of the .control block
        self.title = ''
        # net-name case folding (see parse_cir): lower(name) -> sorted list of
        # the DISTINCT spellings the deck used for that one node.  Only entries
        # with >1 spelling are interesting; convert()/check_only() print them.
        self.net_case_merges = OrderedDict()


_INLINE_COMMENT = re.compile(r'\s+[\$;].*$')


def _strip_inline_comment(ln):
    """ngspice in-line comments ' $ ...' / ' ; ...' on an ELEMENT card.

    v1 carried them into SYMATTR Value, where they became unreadable blobs of
    prose next to every symbol.  They are not part of the topology, and the
    round-trip deck (which never re-emits them) is compared against an input
    parsed by this same function, so removing them is topology-neutral."""
    return _INLINE_COMMENT.sub('', ln).rstrip()


def _logical_lines(text):
    """join '+' continuations; strip comments; yield (lineno, text)."""
    out = []
    for i, raw in enumerate(text.replace('\r\n', '\n').replace('\r', '\n').split('\n')):
        ln = raw.rstrip()
        if not ln.strip():
            continue
        if ln.lstrip().startswith('+') and out:
            out[-1] = (out[-1][0], out[-1][1] + ' ' + ln.lstrip()[1:].strip())
        else:
            out.append((i + 1, ln.strip()))
    return out


def parse_cir(path):
    """Parse an ngspice deck into a Deck().  First line is the SPICE title.

    Node names are folded CASE-INSENSITIVELY, because ngspice's are: a deck
    that writes `N1` on one card and `n1` on the next is talking about ONE
    node, and ngspice will happily simulate it that way.  Until the 2026-08-27
    audit this parser was case-SENSITIVE, so such a deck was drawn as two
    disconnected islands and still reported VERIFY: PASS
    (audit_fable/case_test.cir is the proof).

    Folding is done by rewriting every occurrence to the spelling of the FIRST
    occurrence, which fixes identity without lowercasing the drawing: the FLAG
    text, labels and .asc keep the author's own capitalisation.  Every name
    that really had to be merged is recorded in deck.net_case_merges so the
    caller can say so out loud -- a human should know that two spellings in
    their deck were the same node."""
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    lines = _logical_lines(text)
    deck = Deck()
    _canon = {}          # lower(name) -> first-seen spelling (the DISPLAY form)
    _seen = OrderedDict()  # lower(name) -> set of spellings

    def canon_net(n):
        k = n.lower()
        if k not in _canon:
            _canon[k] = n
            _seen[k] = set()
        _seen[k].add(n)
        return _canon[k]

    in_control = False
    first = True
    for lineno, ln in lines:
        low = ln.lower()
        if in_control:
            deck.dropped_control.append(ln)
            if low.startswith('.endc'):
                in_control = False
            continue
        if low.startswith('.control'):
            in_control = True
            deck.dropped_control.append(ln)
            continue
        if ln.startswith('*') or ln.startswith(';'):
            if first and not deck.title:
                deck.title = ln.lstrip('*; ').strip()
            deck.comments.append(ln.lstrip('*; ').rstrip())
            first = False
            continue
        first = False
        if low.startswith('.end') and low.strip() in ('.end', '.ends'):
            continue
        if ln.startswith('.'):
            deck.directives.append(ln)
            continue
        ln = _strip_inline_comment(ln)
        tok = ln.split()
        if not tok:
            continue
        name = tok[0]
        letter = name[0].upper()
        if letter == 'K':
            deck.couplings.append(ln)
            continue
        if letter == 'X':
            nodes, sub, params = split_xcall(tok)
            nodes = [canon_net(n) for n in nodes]
            deck.elements.append(Element(name, 'X', nodes, sub, ln, lineno, params))
            continue
        nc = NODE_COUNT.get(letter)
        if nc is None or len(tok) < 1 + nc:
            # unknown / malformed -> carry verbatim, no nodes claimed
            deck.elements.append(Element(name, letter, [], '', ln, lineno))
            continue
        nodes = [canon_net(n) for n in tok[1:1 + nc]]
        value = ' '.join(tok[1 + nc:])
        deck.elements.append(Element(name, letter, nodes, value, ln, lineno))
    for k, spellings in _seen.items():
        if len(spellings) > 1:
            deck.net_case_merges[_canon[k]] = sorted(spellings)
    return deck


def split_xcall(tok):
    """`Xname n1 .. nk SUBCKT [p=v ...]` -> (nodes, subckt, paramstring).

    v1 used `tok[1:-1]` as the node list, which for a call carrying instance
    parameters swallowed the subckt name AND every `p=v` token into the node
    list.  That still round-tripped (both sides were parsed the same way) but
    it made the X call undrawable and produced bogus 'net names'.  Here the
    subckt name is the token right before the first `p=v` token, or the last
    token when there are none."""
    rest = tok[1:]
    ieq = next((i for i, t in enumerate(rest) if '=' in t), None)
    if ieq is not None and ieq >= 1:
        return rest[:ieq - 1], rest[ieq - 1], ' '.join(rest[ieq:])
    if not rest:
        return [], '', ''
    return rest[:-1], rest[-1], ''


SUBCKT_3T = re.compile(r'^\s*\.subckt\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s*$', re.I)
MOSFET_SUBCKT_PORTS = (('d', 'g', 's'), ('drain', 'gate', 'source'))
MOSFET_SUBCKT_NAMES = {'SIC_650', 'SR_80'}


def find_mosfet_subckts(cirpath, deck):
    """Names of 3-terminal `d g s` subcircuits reachable from this deck.

    Only `.subckt NAME d g s` (exactly three ports, named drain/gate/source)
    qualifies, plus the two device wrappers this project already ships.  Any
    other X call keeps the v1 TEXT-directive fallback."""
    names = set(MOSFET_SUBCKT_NAMES)
    base = os.path.dirname(os.path.abspath(cirpath))
    seen = set()
    for d in deck.directives:
        m = re.match(r'\.(?:include|inc|lib)\s+(.+)$', d, re.I)
        if not m:
            continue
        p = m.group(1).strip().strip('"').split()[0]
        if not os.path.isabs(p):
            p = os.path.join(base, p)
        p = os.path.abspath(p)
        if p in seen or not os.path.isfile(p):
            continue
        seen.add(p)
        try:
            with open(p, 'r', encoding='utf-8', errors='replace') as f:
                for ln in f:
                    mm = SUBCKT_3T.match(ln)
                    if mm and tuple(x.lower() for x in mm.groups()[1:]) in MOSFET_SUBCKT_PORTS:
                        names.add(mm.group(1).upper())
        except OSError:
            pass
    return names


def mosfet_map(deck, mosnames):
    """element name (upper) -> 'nmos' for every drawable X subcircuit call."""
    out = {}
    for e in deck.elements:
        if e.letter == 'X' and len(e.nodes) == 3 and e.value.upper() in mosnames:
            out[e.name.upper()] = 'nmos'
    return out


def symbol_for(e, pins, mosmap, coupled):
    """ltsym symbol name for an element, or None -> TEXT-directive fallback."""
    if e.letter == 'X':
        return mosmap.get(e.name.upper())
    sym = DRAWABLE.get(e.letter)
    if sym is None:
        return None
    if len(pins.get(sym, [])) != len(e.nodes):
        return None
    if sym == 'ind' and e.name.lower() in coupled:
        sym = 'ind2'
    return sym


def coupled_inductors(deck):
    coupled = set()
    for k in deck.couplings:
        for t in k.split()[1:]:
            if re.match(r'^[A-Za-z]', t):
                coupled.add(t.lower())
    return coupled


# ===========================================================================
# 2. .asc emission
# ===========================================================================

GRID = 16
STUB_DEFAULT = 32

# Coarse-grid pitch.  Must exceed the per-element coordinate footprint so that
# no two elements can ever share a pin / stub-end / flag coordinate.
CELL_W = 320
CELL_H = 384

# largest |offset| of any pin in the symbols we place
#   x = -48 : sw control pins NC+/NC-      x = +48 : nmos/pmos D and S pins
_MAX_PIN_DX_NEG = 48
_MAX_PIN_DX_POS = 48
_MAX_PIN_DY = 96


def _check_pitch(stub):
    """Arithmetic non-collision guarantee (cf. gen_cd_2phase.py's DY proof)."""
    # per-cell coordinate footprint, relative to the cell origin:
    x_lo = -(_MAX_PIN_DX_NEG + stub)
    x_hi = _MAX_PIN_DX_POS + stub
    y_lo = -stub
    y_hi = _MAX_PIN_DY + stub
    assert CELL_W > (x_hi - x_lo), 'CELL_W too small: %d <= %d' % (CELL_W, x_hi - x_lo)
    assert CELL_H > (y_hi - y_lo), 'CELL_H too small: %d <= %d' % (CELL_H, y_hi - y_lo)
    # neighbouring cells' footprints must be strictly disjoint
    assert CELL_W + x_lo > x_hi, 'CELL_W overlap'
    assert CELL_H + y_lo > y_hi, 'CELL_H overlap'
    assert CELL_W % GRID == 0 and CELL_H % GRID == 0 and stub % GRID == 0
    return (x_lo, x_hi, y_lo, y_hi)


NETNAME_OK = re.compile(r'^[A-Za-z0-9_]+$')


def sanitise_netnames(deck):
    """asc2ngspice maps FLAG text through re.sub(r'[^A-Za-z0-9_]','_').  If any
    net name would be altered by that, the TEXT-passthrough cards (which carry
    the ORIGINAL spelling verbatim) would no longer agree with the FLAGs.  We
    therefore refuse to silently mangle: return the list of offending names."""
    bad = set()
    for e in deck.elements:
        for n in e.nodes:
            if not NETNAME_OK.match(n):
                bad.add(n)
    return sorted(bad)


def _to_braces(s):
    """ngspice '<expr>' quoting -> LTspice {<expr>} so the .asc is usable in
    LTspice.  Applied to .param cards only.  Topology-neutral."""
    return re.sub(r"'([^']*)'", r'{\1}', s)


def build_asc(deck, pins, stub=STUB_DEFAULT, cols=None, symdir_note=True,
              mosmap=None):
    """Return (asc_lines, info) where info records the layout decisions."""
    foot = _check_pitch(stub)

    coupled = coupled_inductors(deck)
    mosmap = mosmap or {}

    drawn, text_fallback = [], []
    for e in deck.elements:
        sym = symbol_for(e, pins, mosmap, coupled)
        if sym is None:
            text_fallback.append(e)
            continue
        drawn.append((e, sym))

    n = len(drawn)
    if cols is None:
        cols = max(1, int(round(n ** 0.5)) or 1)
        while cols * cols < n:
            cols += 1
    rows = (n + cols - 1) // cols if n else 0

    wires, flags, symbols = [], [], []
    for idx, (e, sym) in enumerate(drawn):
        r, c = divmod(idx, cols)
        ox, oy = c * CELL_W, r * CELL_H
        pl = pins[sym]
        symbols.append('SYMBOL %s %d %d R0' % (sym, ox, oy))
        symbols.append('SYMATTR InstName %s' % e.name)
        if e.value:
            symbols.append('SYMATTR Value %s' % e.value)
        if e.params:
            symbols.append('SYMATTR SpiceLine %s' % e.params)
        for k, (px, py) in enumerate(pl):
            ax, ay = ox + px, oy + py
            # stub direction: vertical pins go out top/bottom, the sw control
            # pins (negative x) go out to the left.
            if px < 0:
                bx, by = ax - stub, ay
            elif py <= _MAX_PIN_DY // 2:
                bx, by = ax, ay - stub
            else:
                bx, by = ax, ay + stub
            assert bx % GRID == 0 and by % GRID == 0
            wires.append('WIRE %d %d %d %d' % (ax, ay, bx, by))
            flags.append('FLAG %d %d %s' % (bx, by, e.nodes[k]))

    # ---- SPICE directive TEXT records --------------------------------------
    tx = 0
    ty = rows * CELL_H + CELL_H // 2
    ty = ((ty + GRID - 1) // GRID) * GRID
    texts = []

    def put(body):
        nonlocal ty
        texts.append('TEXT %d %d Left 2 %s' % (tx, ty, body))
        ty += 32

    put(';--- generated by net2asc.py : FLAG-based connectivity, no routing ---')
    if deck.title:
        put(';%s' % deck.title.replace('\n', ' '))
    for d in deck.directives:
        put('!%s' % _to_braces(d) if d.lower().startswith('.param') else '!%s' % d)
    for k in deck.couplings:
        put('!%s' % k)
    for e in text_fallback:
        put('!%s' % e.raw)
    if deck.dropped_control:
        put(';.control ... .endc block dropped (%d lines): LTspice has no '
            'equivalent; re-add it in the ngspice deck.' % len(deck.dropped_control))
    und = undefined_params(deck)
    if und:
        put(';=== UNDEFINED PARAMETERS -- THIS SCHEMATIC WILL NOT RUN AS-IS ===')
        put(';%d {PLACEHOLDER}s have no .param card.  net2asc.py does NOT invent '
            'values.  Supply your own and delete the leading ";" below.' % len(und))
        for n in und:
            put(';!.param %s=<SUPPLY A VALUE>' % n)

    # ---- sheet ------------------------------------------------------------
    xs, ys = [0], [0]
    for w in wires:
        t = w.split()
        xs += [int(t[1]), int(t[3])]
        ys += [int(t[2]), int(t[4])]
    for f in flags + symbols + texts:
        t = f.split()
        if t[0] in ('FLAG', 'TEXT'):
            xs.append(int(t[1])); ys.append(int(t[2]))
        elif t[0] == 'SYMBOL':
            xs.append(int(t[2])); ys.append(int(t[3]))
    W = max(880, max(xs) + 400)
    H = max(680, max(ys) + 200)

    out = ['Version 4', 'SHEET 1 %d %d' % (W, H)]
    out += wires
    out += flags
    out += symbols
    out += texts

    info = {
        'drawn': [(e.name, sym) for e, sym in drawn],
        'text_fallback': [e.name for e in text_fallback],
        'text_fallback_raw': [e.raw for e in text_fallback],
        'cols': cols, 'rows': rows, 'stub': stub, 'footprint': foot,
        'n_wire': len(wires), 'n_flag': len(flags), 'n_symbol': len(drawn),
        'n_text': len(texts), 'sheet': (W, H),
        'dropped_control': len(deck.dropped_control),
    }
    return out, info


# ===========================================================================
# 2b. v2 "flow" layout -- real orthogonal wiring for the conduction path
# ===========================================================================
#
# v1 drew nothing but stubs+FLAGs.  v2 keeps the FLAG guarantee for everything
# it cannot place sensibly, but draws the power path as actual wires:
#
#   * two-terminal elements are contracted into SERIES CHAINS (a chain is a
#     maximal run of elements joined at nets that carry exactly two power
#     terminals), so a chain is drawn as one straight run of symbols;
#   * a HALF-BRIDGE LEG is recognised graph-theoretically: two chains sharing
#     one net, each containing exactly one MOSFET, with the upper chain's
#     MOSFET presenting its SOURCE to the shared net and the lower chain's
#     MOSFET presenting its DRAIN to it.  That shared net is the switch node.
#   * the leg is drawn vertically (high side above low side); the chain that
#     feeds the high-side drain becomes the top rail running left->right; the
#     chain leaving the switch node becomes the output run running left->right;
#     chains that end on ground drop straight down to a ground flag.
#   * gate nets, and any chain the placer cannot route, stay on FLAG labels in
#     a clearly separated band under the drawing.
#
# If the leg cannot be identified the caller falls back to the v1 grid.

LEAD = 48            # lead wire between a junction and the first pin of a run
LEAD_H = 96          # ... horizontally: the value text sits UNDER the symbol,
LEAD_V = 64          #     so a horizontal run needs a wider pitch than a
#                          vertical one (where the text sits beside it)
BRANCH_DX = 256      # column pitch for vertical branches hanging off a rail
RAIL_UP = 96         # distance from the top rail down to the HS drain
SW_STUB = 160        # switch-node label stub, keeps the net label off the FET
PARALLEL_DY = 192    # offset of a re-routed parallel chain from its rail
AUX_GAP = 256        # gap between the drawing and the auxiliary band
AUX_ROW_DY = 256
AUX_COL_GAP = 256
DROP_LEAD = 96       # extra drop before a branch hanging under a rail, so its
#                      InstName clears the rail's Value text
TEXT_DY = 32         # line pitch of the SPICE-directive block
TEXT_COL_ROWS = 27   # lines per directive column before starting a new one
AUX_LEAD = 256       # auxiliary runs are spread out: their Value strings are
#                      whole PULSE(...) argument lists
BODY_PAD = 16        # keep-out margin around a symbol's pin bounding box, used
#                      by the spine layout's placement validator
SPINE_COL_DX = 192   # column pitch when a branch has to step sideways
SPINE_ROW_MIN = 512  # minimum vertical pitch between the spine and a rail
COUPLE_DY = 256      # vertical gap between two K-coupled inductors
BAND_GAP = 512       # gap between two islands (parts of the circuit that touch
#                      only through ground, e.g. a transformer's two windings)

DIRV = {'R': (1, 0), 'L': (-1, 0), 'D': (0, 1), 'U': (0, -1)}
_ORI_ORDER = ('R0', 'R90', 'R180', 'R270', 'M0', 'M90', 'M180', 'M270')
_ORI_INV = {'R0': 'R0', 'R90': 'R270', 'R180': 'R180', 'R270': 'R90',
            'M0': 'M0', 'M90': 'M90', 'M180': 'M180', 'M270': 'M270'}


def lead_for(d):
    return LEAD_H if d in ('L', 'R') else LEAD_V


class LayoutError(Exception):
    pass


# ---------------------------------------------------------------------------
# TEXT extents.  The renderer is asc2svg.py, so its own advance-width metric is
# reused verbatim -- the checker and the picture must agree about how wide a
# string is.  If asc2svg.py cannot be imported the same formula is inlined.
# ---------------------------------------------------------------------------
try:
    _A2S = _load_module('_a2s_for_net2asc', os.path.join(HERE, 'asc2svg.py'))
    text_width = _A2S.text_width           # (string, font-size-in-units) -> units
    _FSIZE = _A2S.fsize                    # LTspice size index -> units
    BASE_FONT = _A2S.BASE_FONT
except Exception:                          # pragma: no cover - fallback only
    import unicodedata as _ud
    BASE_FONT = 24.0
    _FM = {0: 0.625, 1: 0.75, 2: 1.0, 3: 1.25, 4: 1.5, 5: 2.0, 6: 2.5, 7: 3.5}
    _EAW = {'W': 1.0, 'F': 1.0, 'A': 0.62, 'H': 0.5, 'Na': 0.58, 'N': 0.58}

    def text_width(s, size):
        return sum(_EAW.get(_ud.east_asian_width(c), 0.58) for c in s) * size

    def _FSIZE(idx, default=2):
        try:
            idx = int(idx)
        except (TypeError, ValueError):
            idx = default
        return BASE_FONT * _FM.get(idx, 1.0)

FLAG_FONT = BASE_FONT * 0.85       # asc2svg draws net labels at 0.85 * base
# Which orientations make asc2svg.py swap the axes / flip the text handedness.
# These are DERIVED from the same rule the renderer uses (asc2svg.Xf: swap when
# the image of the unit x vector is vertical, xflip when its x component is
# negative) instead of being spelled out by hand.  They were spelled out by
# hand until 2026-09-05, and the hand-written list was wrong in both
# directions: it missed R180 (a pure 180-degree rotation DOES flip the
# handedness: ORI['R180'](1,0) = (-1,0)) and it wrongly included M180 (a flip
# about the x axis leaves the handedness alone: ORI['M180'](1,0) = (1,0)).
# The consequence was silent: the overlap CHECKER put an R180 symbol's
# attribute text on the wrong side of its anchor, so it reported "0 overlaps"
# for a drawing in which two labels were printed exactly on top of each other
# (found by looking at the rendered PNG of an active-clamp forward converter,
# where DSR2's InstName landed on CO's).  The generator (windows_for) and the
# renderer had agreed all along; only the estimator disagreed with both.
_SWAP_ORI = tuple(o for o in ORI if ORI[o](1, 0)[0] == 0)
_XFLIP_ORI = tuple(o for o in ORI
                   if ORI[o](1, 0)[0] < 0 or (o in _SWAP_ORI
                                              and ORI[o](0, 1)[0] < 0))


def _attr_text_boxes(ori, origin, inst, value, windows):
    """ESTIMATED bounding boxes of a symbol's InstName / Value strings.

    `windows` are (wid, lx, ly, just, size) in the SYMBOL's own frame, exactly
    as they will be written out; asc2svg.py maps them through ORI[ori] and
    draws the baseline at y + 0.35*size with the justification as the anchor.
    Vertical (swapped) orientations make LTspice centre the string, and the
    mirrored codes flip Left <-> Right; both are reproduced here."""
    out = []
    body_of = {0: inst, 3: ('' if value is None else str(value))}
    for (wid, lx, ly, just, size) in windows:
        body = body_of.get(wid)
        if not body or size == 0:
            continue
        gx, gy = ORI[ori](lx, ly)
        gx += origin[0]
        gy += origin[1]
        sz = _FSIZE(size)
        w = text_width(body, sz)
        if ori in _SWAP_ORI:
            anchor = 'middle'
        elif ori in _XFLIP_ORI:
            anchor = {'Left': 'Right', 'Right': 'Left'}.get(just, just)
        else:
            anchor = just
        if anchor in ('middle', 'Center'):
            x0, x1 = gx - w / 2.0, gx + w / 2.0
        elif anchor == 'Right':
            x0, x1 = gx - w, gx
        else:
            x0, x1 = gx, gx + w
        out.append((x0, gy - 0.5 * sz, x1, gy + 0.5 * sz,
                    inst, 'attr%d' % wid))
    return out


def _pin_offs(pins, sym, ori):
    t = ORI[ori]
    return [t(px, py) for (px, py) in pins[sym]]


def _choose_ori(pins, sym, i0, i1, d):
    """orientation putting pin i0 first and pin i1 last along direction d.

    Returns (ori, span).  Non-mirrored orientations are tried first so the
    symbol graphics keep their normal handedness."""
    dx, dy = DIRV[d]
    for ori in _ORI_ORDER:
        o = _pin_offs(pins, sym, ori)
        ax, ay = o[i0]
        bx, by = o[i1]
        vx, vy = bx - ax, by - ay
        span = abs(vx) + abs(vy)
        if span and (vx, vy) == (dx * span, dy * span):
            return ori, span
    raise LayoutError('no orientation of %r puts pin %d before pin %d along %s'
                      % (sym, i0, i1, d))


def _span(pins, sym, i0, i1, d):
    return _choose_ori(pins, sym, i0, i1, d)[1]


class Sheet(object):
    """Accumulates .asc records and, in parallel, the DESIGNED net of every
    coordinate it emits, so an accidental geometric contact can be detected."""

    def __init__(self, pins):
        self.pins = pins
        self.wires = []          # (p, q, net)
        self.flags = []          # (p, name)
        self.syms = []           # dicts
        self.texts = []          # (x, y, body)
        self.pinpts = []         # (inst, k, coord, net-or-None)
        self.boxes = []          # (x0, y0, x1, y1, frozenset(nets), inst)
        self.tboxes = []         # (x0, y0, x1, y1, owner, kind) -- ESTIMATED
        #                          extents of attribute / net-label TEXT, using
        #                          asc2svg.py's own metric so the checker and
        #                          the renderer agree.  See `_text_box()`.
        self.junction = {}       # net -> a coordinate that is a WIRE ENDPOINT
        #                          (asc2ngspice only honours a FLAG that sits on
        #                          a wire endpoint or a pin, never mid-segment)
        # ---- island bookkeeping: every record remembers WHICH island drew it,
        # so the islands can be repacked side by side once they are all drawn.
        self.gid = 0
        self.autostagger = False
        self.wgrp = []; self.fgrp = []; self.sgrp = []; self.tgrp = []
        self.pgrp = []; self.bgrp = []; self.tbgrp = []
        self.jgrp = {}

    # -- speculative placement ---------------------------------------------
    def mark(self):
        """Checkpoint, so a branch that cannot be routed can be undone."""
        return (len(self.wires), len(self.flags), len(self.syms),
                len(self.texts), len(self.pinpts), len(self.boxes),
                dict(self.junction), len(self.tboxes), dict(self.jgrp))

    def rollback(self, m):
        del self.wires[m[0]:]; del self.wgrp[m[0]:]
        del self.flags[m[1]:]; del self.fgrp[m[1]:]
        del self.syms[m[2]:];  del self.sgrp[m[2]:]
        del self.texts[m[3]:]; del self.tgrp[m[3]:]
        del self.pinpts[m[4]:]; del self.pgrp[m[4]:]
        del self.boxes[m[5]:]; del self.bgrp[m[5]:]
        self.junction = m[6]
        del self.tboxes[m[7]:]; del self.tbgrp[m[7]:]
        self.jgrp = m[8]

    # -- primitives ---------------------------------------------------------
    def wire(self, p, q, net):
        p = (int(p[0]), int(p[1]))
        q = (int(q[0]), int(q[1]))
        if p == q:
            return
        if p[0] != q[0] and p[1] != q[1]:
            raise LayoutError('diagonal wire %s -> %s' % (p, q))
        for c in (p[0], p[1], q[0], q[1]):
            if c % GRID:
                raise LayoutError('off-grid wire coordinate %s %s' % (p, q))
        self.wires.append((p, q, net))
        self.wgrp.append(self.gid)

    def poly(self, pts, net):
        for a, b in zip(pts, pts[1:]):
            self.wire(a, b, net)

    def flag(self, p, name):
        p = (int(p[0]), int(p[1]))
        self.flags.append((p, name))
        self.fgrp.append(self.gid)
        if name != '0':
            # a net label is drawn beside the flag point; which side depends on
            # which way the wires leave it, which is not known yet, so the
            # estimate is centred on the point.  ESTIMATE -- see NET2ASC.md 5B.9.
            w = text_width(name, FLAG_FONT)
            self.tboxes.append((p[0] - w / 2.0, p[1] - 10 - FLAG_FONT,
                                p[0] + w / 2.0, p[1] + 10 + FLAG_FONT,
                                'FLAG:' + name, 'flag'))
            self.tbgrp.append(self.gid)

    def place(self, sym, ori, origin, inst, value=None, spiceline=None,
              nets=None, windows=None):
        ox, oy = int(origin[0]), int(origin[1])
        if ox % GRID or oy % GRID:
            raise LayoutError('off-grid symbol origin %s %s' % (inst, origin))
        self.syms.append(dict(sym=sym, ori=ori, x=ox, y=oy, inst=inst,
                              value=value, spiceline=spiceline,
                              windows=windows or []))
        self.sgrp.append(self.gid)
        coords = [(ox + dx, oy + dy) for dx, dy in _pin_offs(self.pins, sym, ori)]
        for k, c in enumerate(coords):
            self.pinpts.append((inst, k, c, (nets or {}).get(k)))
            self.pgrp.append(self.gid)
        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]
        # fields 0..3 are the pin bbox inflated by BODY_PAD (the WIRE keep-out);
        # fields 6..9 are the RAW pin bbox, which is what a text string has to
        # stay off -- a net label riding 10 units above a horizontal lead is
        # normal schematic practice and must not count as a collision.
        self.boxes.append((min(xs) - BODY_PAD, min(ys) - BODY_PAD,
                           max(xs) + BODY_PAD, max(ys) + BODY_PAD,
                           frozenset(v for v in (nets or {}).values() if v), inst,
                           min(xs), min(ys), max(xs), max(ys)))
        self.bgrp.append(self.gid)
        for b in _attr_text_boxes(ori, (ox, oy), inst, value, windows or []):
            self.tboxes.append(b)
            self.tbgrp.append(self.gid)
        return coords

    def text(self, x, y, body):
        self.texts.append((int(x), int(y), body))
        self.tgrp.append(self.gid)

    def set_junction(self, net, pt):
        if net not in self.junction:
            self.junction[net] = (int(pt[0]), int(pt[1]))
            self.jgrp[net] = self.gid

    # -- island repacking ---------------------------------------------------
    def translate_group(self, gid, dx, dy):
        """Move every record drawn by island `gid` by (dx, dy)."""
        dx, dy = int(dx), int(dy)
        if not dx and not dy:
            return
        for i, g in enumerate(self.wgrp):
            if g == gid:
                (p, q, n) = self.wires[i]
                self.wires[i] = ((p[0] + dx, p[1] + dy),
                                 (q[0] + dx, q[1] + dy), n)
        for i, g in enumerate(self.fgrp):
            if g == gid:
                (p, n) = self.flags[i]
                self.flags[i] = ((p[0] + dx, p[1] + dy), n)
        for i, g in enumerate(self.sgrp):
            if g == gid:
                self.syms[i]['x'] += dx
                self.syms[i]['y'] += dy
        for i, g in enumerate(self.tgrp):
            if g == gid:
                (x, y, b) = self.texts[i]
                self.texts[i] = (x + dx, y + dy, b)
        for i, g in enumerate(self.pgrp):
            if g == gid:
                (inst, k, c, n) = self.pinpts[i]
                self.pinpts[i] = (inst, k, (c[0] + dx, c[1] + dy), n)
        for i, g in enumerate(self.bgrp):
            if g == gid:
                b = self.boxes[i]
                self.boxes[i] = (b[0] + dx, b[1] + dy, b[2] + dx, b[3] + dy,
                                 b[4], b[5],
                                 b[6] + dx, b[7] + dy, b[8] + dx, b[9] + dy)
        for i, g in enumerate(self.tbgrp):
            if g == gid:
                b = self.tboxes[i]
                self.tboxes[i] = (b[0] + dx, b[1] + dy, b[2] + dx, b[3] + dy,
                                  b[4], b[5])
        for n, g in self.jgrp.items():
            if g == gid and n in self.junction:
                c = self.junction[n]
                self.junction[n] = (c[0] + dx, c[1] + dy)

    def group_bbox(self, gid):
        xs, ys = [], []
        for i, g in enumerate(self.wgrp):
            if g == gid:
                p, q, _ = self.wires[i]
                xs += [p[0], q[0]]; ys += [p[1], q[1]]
        for i, g in enumerate(self.bgrp):
            if g == gid:
                b = self.boxes[i]
                xs += [b[0], b[2]]; ys += [b[1], b[3]]
        for i, g in enumerate(self.tbgrp):
            if g == gid:
                b = self.tboxes[i]
                xs += [b[0], b[2]]; ys += [b[1], b[3]]
        for i, g in enumerate(self.tgrp):
            if g == gid:
                x, y, body = self.texts[i]
                xs += [x, x + int(len(body) * 15)]; ys += [y, y + 32]
        if not xs:
            return None
        return (min(xs), min(ys), max(xs), max(ys))

    # -- attribute text placement ------------------------------------------
    def windows_for(self, sym, ori, origin, pin_a, pin_b, d, value, drop=0):
        """WINDOW overrides so InstName / Value never land on the wire.

        Horizontal runs get the name above and the value below the body;
        vertical runs get both stacked to the right of it.  The coordinates in
        a WINDOW record live in the symbol's OWN frame, so the desired global
        offset is pushed through the inverse of the placement rotation."""
        ox, oy = origin
        offs = _pin_offs(self.pins, sym, ori)
        side = max(abs(dx) for dx, _ in offs)
        if d in ('L', 'R'):
            mx = (pin_a[0] + pin_b[0]) // 2 - ox
            my = pin_a[1] - oy
            g = [(0, mx, my - 56, 'Center'), (3, mx, my + 64 + drop, 'Center')]
        else:
            mx = max(side, 32) + 32
            my = (pin_a[1] + pin_b[1]) // 2 - oy
            # R180 (and the mirrored codes) flip the text's handedness, so a
            # 'Left'-justified window would run BACK OVER the symbol body.
            ax, ay = ORI[ori](1, 0)
            just = 'Right' if ax < 0 else 'Left'
            g = [(0, mx, my - 24, just), (3, mx, my + 24, just)]
        inv = ORI[_ORI_INV[ori]]
        out = []
        for wid, gx, gy, just in g:
            lx, ly = inv(gx, gy)
            size = 2
            if wid == 3 and (value is None or str(value).strip() == '0'):
                size = 0        # bare ammeter: keep the attribute, hide the text
            out.append((wid, int(lx), int(ly), just, size))
        return out

    # -- a run of series elements ------------------------------------------
    def run(self, start, d, items, net_of_step, lead=None, stagger=False):
        """items: [(elem, sym, i0, i1)] placed one after another along d.

        `net_of_step[i]` is the net entering item i; the net leaving item i is
        `net_of_step[i+1]`.  Returns the coordinate of the far end."""
        lead = lead_for(d) if lead is None else lead
        dx, dy = DIRV[d]
        if (self.autostagger and not stagger and d in ('L', 'R')
                and len(items) > 1):
            # a PULSE(...) argument list is far wider than the element pitch,
            # so on a horizontal run the Value strings of neighbouring symbols
            # would sit on top of each other.  Dropping every other one by one
            # line separates them without moving a single wire.
            for (e, sym, i0, i1) in items:
                if e.value and text_width(str(e.value), _FSIZE(2)) > \
                        lead + _span(self.pins, sym, i0, i1, d):
                    stagger = True
                    break
        cur = (int(start[0]), int(start[1]))
        for i, (e, sym, i0, i1) in enumerate(items):
            ori, span = _choose_ori(self.pins, sym, i0, i1, d)
            p0 = (cur[0] + dx * lead, cur[1] + dy * lead)
            p1 = (p0[0] + dx * span, p0[1] + dy * span)
            offs = _pin_offs(self.pins, sym, ori)
            origin = (p0[0] - offs[i0][0], p0[1] - offs[i0][1])
            nets = {i0: net_of_step[i], i1: net_of_step[i + 1]}
            if len(e.nodes) == len(self.pins[sym]):
                # pin k always carries e.nodes[k] (same convention v1 uses for
                # its stub FLAGs), so record EVERY terminal, not just the two
                # the chain runs through -- a `sw` has two control pins as well.
                nets = dict((k, n) for k, n in enumerate(e.nodes))
            elif sym in ('nmos', 'pmos'):
                nets[1] = e.nodes[1]
            self.place(sym, ori, origin, e.name, e.value or None,
                       e.params or None, nets,
                       self.windows_for(sym, ori, origin, p0, p1, d, e.value,
                                        drop=(56 if (stagger and i % 2) else 0)))
            self.wire(cur, p0, net_of_step[i])
            self.set_junction(net_of_step[i], cur)
            self.set_junction(net_of_step[i + 1], p1)
            cur = p1
        return cur

    def run_len(self, items, d, lead=None):
        lead = lead_for(d) if lead is None else lead
        return sum(lead + _span(self.pins, sym, i0, i1, d)
                   for (e, sym, i0, i1) in items)

    # -- gate stubs ---------------------------------------------------------
    def gate_stub(self, inst, sym, ori, origin, net):
        """short whisker from the MOSFET gate pin, ending in a FLAG."""
        offs = _pin_offs(self.pins, sym, ori)
        gx, gy = offs[1]
        dxs, dys = offs[0]                       # drain pin, i.e. the channel side
        vx = 0 if gx == dxs else (-1 if gx < dxs else 1)
        vy = 0 if gy == dys else (-1 if gy < dys else 1)
        if vx and vy:                            # gate is diagonal to the drain
            vy = 0
        p = (origin[0] + gx, origin[1] + gy)
        q = (p[0] + vx * LEAD, p[1] + vy * LEAD)
        self.wire(p, q, net)
        self.flag(q, net)

    def aux_pin_stubs(self, sym, ori, origin, nodes, power, lead=LEAD):
        """stub + FLAG on every terminal that is NOT one of the two the chain
        runs through (a MOSFET gate, a `sw`'s NC+/NC- control pair).

        Without this the pin would be left floating and the round trip would
        invent a fresh node name for it."""
        offs = _pin_offs(self.pins, sym, ori)
        if len(nodes) != len(offs):
            return
        cx = sum(offs[i][0] for i in power) / float(len(power))
        cy = sum(offs[i][1] for i in power) / float(len(power))
        for k, (gx, gy) in enumerate(offs):
            if k in power:
                continue
            vx, vy = gx - cx, gy - cy
            if abs(vx) >= abs(vy):
                v = (1 if vx > 0 else -1, 0)
            else:
                v = (0, 1 if vy > 0 else -1)
            p = (origin[0] + gx, origin[1] + gy)
            q = (p[0] + v[0] * lead, p[1] + v[1] * lead)
            self.wire(p, q, nodes[k])
            self.flag(q, nodes[k])

    # -- output -------------------------------------------------------------
    def bbox(self):
        xs, ys = [], []
        for p, q, _ in self.wires:
            xs += [p[0], q[0]]
            ys += [p[1], q[1]]
        for p, _ in self.flags:
            xs.append(p[0]); ys.append(p[1])
        for s in self.syms:
            for dx, dy in _pin_offs(self.pins, s['sym'], s['ori']):
                xs.append(s['x'] + dx); ys.append(s['y'] + dy)
            xs += [s['x'] - 64, s['x'] + 160]     # rough graphics/label margin
            ys += [s['y'] - 64, s['y'] + 128]
        for x, y, body in self.texts:
            xs += [x, x + int(len(body) * 15)]     # ~15 units/char at size 2
            ys += [y, y + 32]
        if not xs:
            return (0, 0, 0, 0)
        return (min(xs), min(ys), max(xs), max(ys))

    def emit(self, margin=64):
        x0, y0, x1, y1 = self.bbox()
        ox = -x0 + margin
        oy = -y0 + margin
        ox -= ox % GRID
        oy -= oy % GRID
        W = ((x1 - x0) + 2 * margin + 160)
        H = ((y1 - y0) + 2 * margin + 96)
        W = int(((W + GRID - 1) // GRID) * GRID)
        H = int(((H + GRID - 1) // GRID) * GRID)
        out = ['Version 4', 'SHEET 1 %d %d' % (W, H)]
        for p, q, _ in self.wires:
            out.append('WIRE %d %d %d %d' % (p[0] + ox, p[1] + oy,
                                             q[0] + ox, q[1] + oy))
        for p, nm in self.flags:
            out.append('FLAG %d %d %s' % (p[0] + ox, p[1] + oy, nm))
        for s in self.syms:
            out.append('SYMBOL %s %d %d %s' % (s['sym'], s['x'] + ox,
                                               s['y'] + oy, s['ori']))
            for wid, wx, wy, just, size in s.get('windows') or []:
                out.append('WINDOW %d %d %d %s %d' % (wid, wx, wy, just, size))
            out.append('SYMATTR InstName %s' % s['inst'])
            if s['value']:
                out.append('SYMATTR Value %s' % s['value'])
            if s['spiceline']:
                out.append('SYMATTR SpiceLine %s' % s['spiceline'])
        for x, y, body in self.texts:
            out.append('TEXT %d %d Left 2 %s' % (x + ox, y + oy, body))
        return out, (W, H)


# --------------------------------------------------------------------------
# series-chain contraction
# --------------------------------------------------------------------------

class Chain(object):
    __slots__ = ('steps', 'nets', 'placed')

    def __init__(self, steps, nets):
        self.steps = steps        # [(edge_index, pin_at_prev_net, pin_at_next_net)]
        self.nets = nets          # len(steps)+1 net names
        self.placed = False

    @property
    def a(self):
        return self.nets[0]

    @property
    def b(self):
        return self.nets[-1]

    def reversed_(self):
        st = [(i, pe, ps) for (i, ps, pe) in reversed(self.steps)]
        return Chain(st, list(reversed(self.nets)))

    def oriented(self, first_net):
        if self.nets[0] == first_net:
            return self
        if self.nets[-1] == first_net:
            return self.reversed_()
        raise LayoutError('chain does not touch %r' % first_net)

    def __len__(self):
        return len(self.steps)


def control_nets(edges, gate_of):
    """Nets that are DRIVE, not power: a MOSFET gate, or a controlled switch's
    sense terminal that appears on no power terminal anywhere in the deck.

    A `sw`'s NC- pin is very often tied to ground or to the switch node itself.
    Treating those as drive nets would banish the whole power stage to the
    label band, so a control net that is ALSO a power terminal stays power."""
    power, mos, ctrl = set(), set(), set()
    for (e, sym, na, nb, pa, pb) in edges:
        power.add(na)
        power.add(nb)
        if sym in ('nmos', 'pmos'):
            mos.add(e.nodes[1])
    for v in gate_of.values():
        ctrl.update(v)
    return (mos | (ctrl - power)) - {'0'}


def build_chains(deck, pins, mosmap, coupled, must_flag):
    """-> (edges, chains, gate_of, text_fallback)

    edges[i] = (element, symbol, netA, netB, pinA, pinB) where for a MOSFET
    netA/pinA is the DRAIN (SpiceOrder 1) and netB/pinB the SOURCE
    (SpiceOrder 3); the GATE (SpiceOrder 2) is not a chain terminal.

    gate_of[i] is the TUPLE of control terminals of edge i -- a MOSFET's gate,
    a voltage-controlled switch's NC+/NC- pair.  They are never chain terminals
    and a chain may not be contracted THROUGH one, otherwise the control net
    would end up unlabelled and the round trip would rename it."""
    edges, gate_of, text_fallback = [], {}, []
    for e in deck.elements:
        sym = symbol_for(e, pins, mosmap, coupled)
        if sym is None:
            text_fallback.append(e)
            continue
        if sym in ('nmos', 'pmos'):
            edges.append((e, sym, e.nodes[0], e.nodes[2], 0, 2))
            gate_of[len(edges) - 1] = (e.nodes[1],)
        else:
            edges.append((e, sym, e.nodes[0], e.nodes[1], 0, 1))
            if len(pins[sym]) > 2 and len(e.nodes) == len(pins[sym]):
                gate_of[len(edges) - 1] = tuple(e.nodes[2:])

    adj = defaultdict(list)
    for i, (e, sym, na, nb, pa, pb) in enumerate(edges):
        adj[na].append((i, pa))
        adj[nb].append((i, pb))
    # A control terminal must never end up in the MIDDLE of a contracted chain:
    # it has to stay a chain endpoint so that it gets a FLAG of its own.  The
    # matching stub FLAG on the device pin is what joins the two, and a net that
    # is present in two unconnected wire components must be named in BOTH.
    gate_nets = set(n for v in gate_of.values() for n in v)

    def internal(net):
        return (net != '0' and len(adj[net]) == 2 and net not in gate_nets
                and net not in must_flag)

    used = [False] * len(edges)
    chains = []
    for i0 in range(len(edges)):
        if used[i0]:
            continue
        e, sym, na, nb, pa, pb = edges[i0]
        used[i0] = True
        steps = [(i0, pa, pb)]
        nets = [na, nb]
        while internal(nets[-1]):
            cand = [(j, p) for (j, p) in adj[nets[-1]] if not used[j]]
            if not cand:
                break
            j, p = cand[0]
            _, _, naj, nbj, paj, pbj = edges[j]
            used[j] = True
            if p == paj and naj == nets[-1]:
                steps.append((j, paj, pbj)); nets.append(nbj)
            else:
                steps.append((j, pbj, paj)); nets.append(naj)
        while internal(nets[0]):
            cand = [(j, p) for (j, p) in adj[nets[0]] if not used[j]]
            if not cand:
                break
            j, p = cand[0]
            _, _, naj, nbj, paj, pbj = edges[j]
            used[j] = True
            if p == pbj and nbj == nets[0]:
                steps.insert(0, (j, paj, pbj)); nets.insert(0, naj)
            else:
                steps.insert(0, (j, pbj, paj)); nets.insert(0, nbj)
        chains.append(Chain(steps, nets))
    return edges, chains, gate_of, text_fallback


SWITCH_SYMS = ('sw', 'nmos', 'pmos')
MOS_SYMS = ('nmos', 'pmos')


def sw_steps(ch, edges, syms=SWITCH_SYMS):
    """the steps of `ch` that are switching devices (a `sw`, or a MOSFET)."""
    return [s for s in ch.steps if edges[s[0]][1] in syms]


def leg_orientation_ok(hi, lo, edges):
    """The half-bridge test `find_leg()` has always used, factored out so the
    bridge template can apply exactly the same electrical definition.

    `hi` is oriented rail -> midpoint, `lo` midpoint -> return.  A MOSFET must
    present its SOURCE to the midpoint from above and its DRAIN to it from
    below.  A voltage-controlled switch (`sw`) is symmetric between its two
    power terminals, so no orientation can be demanded of it."""
    hs = sw_steps(hi, edges, MOS_SYMS)
    ls = sw_steps(lo, edges, MOS_SYMS)
    if hs and hs[0][2] != 2:
        return False
    if ls and ls[0][1] != 0:
        return False
    return True


def find_leg(edges, chains):
    """-> (chainH, chainL, swnet, ntop, nbot) or None.

    chainH is returned oriented ntop -> swnet, chainL oriented swnet -> nbot."""
    def mos_steps(ch):
        return [s for s in ch.steps if edges[s[0]][1] in ('nmos', 'pmos')]

    cands = [c for c in chains if len(mos_steps(c)) == 1]
    best = None
    for ch in cands:
        for cl in cands:
            if ch is cl:
                continue
            for swnet in (set([ch.a, ch.b]) & set([cl.a, cl.b])):
                h = ch.oriented(ch.a if ch.b == swnet else ch.b)
                l = cl.oriented(swnet)
                if h.nets[-1] != swnet:
                    continue
                # high side must present its SOURCE to the switch node
                if mos_steps(h)[0][2] != 2:
                    continue
                # low side must present its DRAIN to the switch node
                if mos_steps(l)[0][1] != 0:
                    continue
                if h.nets[0] == '0':
                    continue
                score = (len(h) + len(l), -abs(len(h) - len(l)))
                if best is None or score > best[0]:
                    best = (score, h, l, swnet, h.nets[0], l.nets[-1])
    if best is None:
        return None
    return best[1], best[2], best[3], best[4], best[5]


_VREF = re.compile(r'\bv\s*\(\s*([A-Za-z0-9_]+)\s*(?:,\s*([A-Za-z0-9_]+)\s*)?\)',
                   re.I)


def expr_nets(deck, text_fallback):
    """net names referenced as v(<net>) by cards that are carried as TEXT."""
    out = set()
    for src in [e.raw for e in text_fallback] + list(deck.directives):
        for m in _VREF.finditer(src):
            out.add(m.group(1))
            if m.group(2):
                out.add(m.group(2))
    return out


def flow_build(deck, pins, mosmap, cirpath=None):
    """v2 layout.  Raises LayoutError when the topology is not recognised."""
    coupled = coupled_inductors(deck)

    # nets a TEXT-fallback card names must keep an explicit FLAG, otherwise the
    # round trip would invent a fresh node name for the drawn side
    drawn_nets, text_nets = set(), set()
    for e in deck.elements:
        sym = symbol_for(e, pins, mosmap, coupled)
        (drawn_nets if sym else text_nets).update(e.nodes)
    must_flag = (drawn_nets & text_nets) - {'0'}

    edges, chains, gate_of, text_fallback = build_chains(
        deck, pins, mosmap, coupled, must_flag)
    # a chain that terminates on a MOSFET GATE is drive circuitry, not power
    # flow: it always goes to the auxiliary band and connects by net label.
    gate_nets = control_nets(edges, gate_of)
    aux_only = set(id(c) for c in chains if gate_nets & {c.a, c.b})
    leg = find_leg(edges, chains)
    if leg is None:
        raise LayoutError('no half-bridge leg found (need two chains sharing a '
                          'net, one presenting a MOSFET source and one a '
                          'MOSFET drain)')
    chH, chL, SW, NTOP, NBOT = leg

    sh = Sheet(pins)
    hub = {}                       # net -> anchor point
    down_taps = defaultdict(int)   # hub -> vertical branches already hanging
    right_edge = {}                # hub -> x already consumed to its right
    left_edge = {}

    def stub(pt, d, net, n=LEAD_H):
        """short tail past the last symbol of a run.

        The net label goes on the tail's far end: put it on the symbol pin
        itself and asc2svg (and LTspice) would print it on top of the symbol."""
        dx, dy = DIRV[d]
        q = (pt[0] + dx * n, pt[1] + dy * n)
        sh.wire(pt, q, net)
        return q

    def items_of(ch):
        return [(edges[i][0], edges[i][1], ps, pe) for (i, ps, pe) in ch.steps]

    def mos_index(ch):
        for k, (i, ps, pe) in enumerate(ch.steps):
            if edges[i][1] in ('nmos', 'pmos'):
                return k
        return None

    def sub(ch, lo, hi):
        return Chain(ch.steps[lo:hi], ch.nets[lo:hi + 1])

    # ---------------- 1. the leg -------------------------------------------
    XLEG, YSW = 0, 0
    mk = mos_index(chH)
    pre = sub(chH, 0, mk)                     # feed elements, drawn on the top rail
    post = sub(chH, mk + 1, len(chH))         # anything between HS source and SW
    post_items = items_of(post)
    post_len = sh.run_len(post_items, 'D') + (LEAD_V if post_items else 0)
    mos_e, mos_sym, mps, mpe = items_of(chH)[mk]
    ori, span = _choose_ori(pins, mos_sym, mps, mpe, 'D')
    yd = YSW - post_len - span
    offs = _pin_offs(pins, mos_sym, ori)
    origin = (XLEG - offs[mps][0], yd - offs[mps][1])
    sh.place(mos_sym, ori, origin, mos_e.name, mos_e.value or None,
             mos_e.params or None,
             {mps: chH.nets[mk], mpe: chH.nets[mk + 1], 1: mos_e.nodes[1]},
             sh.windows_for(mos_sym, ori, origin, (XLEG, yd),
                            (XLEG, yd + span), 'D', mos_e.value))
    sh.gate_stub(mos_e.name, mos_sym, ori, origin, mos_e.nodes[1])
    if post_items:
        end = sh.run((XLEG, yd + span), 'D', post_items, post.nets)
        sh.wire(end, (XLEG, YSW), SW)
    YTOP = yd - RAIL_UP
    sh.wire((XLEG, YTOP), (XLEG, yd), chH.nets[mk])

    pre_r = pre.reversed_()
    ntop_pt = sh.run((XLEG, YTOP), 'L', items_of(pre_r), pre_r.nets)
    hub[NTOP] = stub(ntop_pt, 'L', NTOP)
    # the switch-node label hangs on a short stub to the right of the leg so it
    # does not sit on top of the high-side device's InstName/Value text
    sh.wire((XLEG, YSW), (XLEG + SW_STUB, YSW), SW)
    hub[SW] = (XLEG + SW_STUB, YSW)
    chH.placed = True

    mkL = mos_index(chL)
    mosL = items_of(chL)[mkL]
    # Shunt chains that bridge the switch node to the bottom of the leg (an RC
    # snubber, a bootstrap return, ...) are drawn as vertical branches beside
    # the leg and have to end level with it.  Stretch the leg if they are
    # longer, so the return wire never has to double back up the branch.
    legs_len = sh.run_len(items_of(chL), 'D')
    shunt_len = [DROP_LEAD + sh.run_len(items_of(c), 'D') for c in chains
                 if not c.placed and id(c) not in aux_only
                 and set([c.a, c.b]) == set([SW, NBOT])]
    pad = max(0, (max(shunt_len) if shunt_len else 0) - legs_len)
    pad += (-pad) % GRID
    sh.wire((XLEG, YSW), (XLEG, YSW + pad), SW)
    end = sh.run((XLEG, YSW + pad), 'D', items_of(chL), chL.nets)
    # same trick as the switch node: hang the bottom-of-leg label on a stub so
    # it does not print over the low-side device
    hub[NBOT] = stub(end, 'R', NBOT, SW_STUB)
    chL.placed = True
    # gate whisker of the low-side device
    for s in sh.syms:
        if s['inst'] == mosL[0].name:
            sh.gate_stub(s['inst'], s['sym'], s['ori'], (s['x'], s['y']),
                         mosL[0].nodes[1])
            break
    # the low-side leg hangs off the switch node at XLEG, i.e. LEFT of the
    # label stub, so every branch column to the right of hub[SW] is still free

    for n in (NTOP, SW, NBOT):
        sh.flag(hub[n], n)

    # ---------------- 2. branches off the placed hubs ----------------------
    def chains_at(net):
        return [c for c in chains
                if not c.placed and id(c) not in aux_only and net in (c.a, c.b)]

    def drop_to_ground(net, ch, x):
        """vertical branch from the rail of `net` at column x down to gnd."""
        c = ch.oriented(net)
        hx, hy = hub[net]
        sh.poly([(hx, hy), (x, hy), (x, hy + DROP_LEAD)], net)
        end = sh.run((x, hy + DROP_LEAD), 'D', items_of(c), c.nets)
        gnd = (end[0], end[1] + LEAD_V)
        sh.wire(end, gnd, c.nets[-1])
        sh.flag(gnd, '0')

    def parallel_vertical(net_top, net_bot, ch, x):
        """chain between two hubs that sit on different rows: an L-shaped
        branch down column x, closed by a horizontal wire at the bottom."""
        c = ch.oriented(net_top)
        tx, ty = hub[net_top]
        bx, by = hub[net_bot]
        sh.poly([(tx, ty), (x, ty), (x, ty + DROP_LEAD)], net_top)
        end = sh.run((x, ty + DROP_LEAD), 'D', items_of(c), c.nets)
        if end[1] > by:
            raise LayoutError('branch %s..%s overshoots its lower rail'
                              % (net_top, net_bot))
        sh.poly([end, (x, by), (bx, by)], c.nets[-1])

    def parallel_horizontal(net_l, net_r, ch, dy):
        """chain between two hubs that sit on the same horizontal rail."""
        c = ch.oriented(net_l)
        lx, ly = hub[net_l]
        rx, ry = hub[net_r]
        y2 = ly + dy
        sh.wire((lx, ly), (lx, y2), net_l)
        if lx + sh.run_len(items_of(c), 'R') > rx:
            raise LayoutError('parallel chain %s..%s does not fit' % (net_l, net_r))
        end = sh.run((lx, y2), 'R', items_of(c), c.nets)
        sh.poly([end, (rx, y2), (rx, ry)], c.nets[-1])

    def expand(net, grow):
        """place every remaining chain touching hub `net`.

        `grow` ('L' or 'R') is the direction the rail is allowed to extend for
        chains that lead to a NEW hub.  Chains that end on ground hang down."""
        hx, hy = hub[net]
        sgn = 1 if grow == 'R' else -1
        todo = chains_at(net)
        gnd = [c for c in todo if '0' in (c.a, c.b)]
        onward, para = [], []
        for c in todo:
            if c in gnd:
                continue
            other = c.b if c.a == net else c.a
            (para if other in hub else onward).append((c, other))
        rail = [(hx, hy)]
        for c in gnd:
            k = down_taps[net]
            down_taps[net] = k + 1
            x = hx + sgn * BRANCH_DX * k
            drop_to_ground(net, c, x)
            c.placed = True
            if (x, hy) != (hx, hy):
                rail.append((x, hy))
        # chains that reach a hub already placed on a DIFFERENT row: hang them
        # as an L-shaped vertical branch (this is how an RC snubber across the
        # low-side device, or any shunt element, gets drawn)
        for c, other in list(para):
            ox_, oy_ = hub[other]
            if oy_ > hy:
                k = down_taps[net]
                down_taps[net] = k + 1
                x = hx + sgn * BRANCH_DX * k
                top, bot = (net, other) if hy < oy_ else (other, net)
                try:
                    parallel_vertical(top, bot, c, x)
                    c.placed = True
                    rail.append((x, hy))
                except LayoutError:
                    down_taps[net] = k
                para.remove((c, other))
        nlevel = 0
        for c, other in list(para):
            ox_, oy_ = hub[other]
            if oy_ == hy:
                l, r = (net, other) if hx < ox_ else (other, net)
                nlevel += 1
                try:
                    parallel_horizontal(l, r, c, -PARALLEL_DY * nlevel)
                    c.placed = True
                except LayoutError:
                    nlevel -= 1         # leave it for the auxiliary band
                para.remove((c, other))
        # rail waypoints so the taps share endpoints with the trunk
        rail = sorted(set(rail), key=lambda p: sgn * p[0])
        sh.poly(rail, net)
        cur = rail[-1]
        newhubs = []
        if onward:
            # all chains heading for the SAME next hub form a parallel group;
            # the longest one is drawn on the rail so the others can be routed
            # beside it and still reach.
            target = onward[0][1]
            group = [c for (c, o) in onward if o == target]
            group.sort(key=lambda c: sh.run_len(items_of(c), grow), reverse=True)
            co = group[0].oriented(net)
            end = stub(sh.run(cur, grow, items_of(co), co.nets), grow, target)
            hub[target] = end
            sh.flag(end, target)
            group[0].placed = True
            newhubs.append(target)
            for (i, ps, pe) in co.steps:
                if edges[i][1] in ('nmos', 'pmos'):
                    for s in sh.syms:
                        if s['inst'] == edges[i][0].name:
                            sh.gate_stub(s['inst'], s['sym'], s['ori'],
                                         (s['x'], s['y']), edges[i][0].nodes[1])
            for k, c in enumerate(group[1:]):
                l, r = (net, target) if hx < end[0] else (target, net)
                try:
                    parallel_horizontal(l, r, c, -PARALLEL_DY * (nlevel + k + 1))
                    c.placed = True
                except LayoutError:
                    pass
        for nh in newhubs:
            expand(nh, grow)

    expand(SW, 'R')
    expand(NBOT, 'R')
    expand(NTOP, 'L')
    for n in list(hub):
        if chains_at(n):
            expand(n, 'L' if n in (NTOP,) else 'R')

    # ---------------- 3. auxiliary band ------------------------------------
    bx0, by0, bx1, by1 = sh.bbox()
    ay = by1 + AUX_GAP
    aux = [c for c in chains if not c.placed]
    aux.sort(key=lambda c: (c.a, c.b))
    ax = bx0
    for c in aux:
        items = items_of(c)
        sh.flag((ax, ay), c.a)
        end = sh.run((ax, ay), 'R', items, c.nets, lead=AUX_LEAD)
        sh.wire(end, (end[0] + LEAD_H, end[1]), c.nets[-1])
        sh.flag((end[0] + LEAD_H, end[1]), c.b)
        c.placed = True
        ay += AUX_ROW_DY            # one auxiliary chain per row: their Value
        #                             strings (PULSE(...)) are far too wide to
        #                             put two of them side by side
    if aux:
        sh.text(bx0, by1 + AUX_GAP - 112,
                ';--- gate drive / auxiliary: joined to the power stage by NET '
                'LABELS, not by wires ---')

    # Nets that only a TEXT card refers to -- directly as a terminal, or inside
    # a v(...) expression of a B source / .meas card -- must still carry a
    # visible name, otherwise the schematic silently renames them and those
    # cards would point at nodes that no longer exist.  Chain-internal nets are
    # named in place, at the wire junction between two symbols, which keeps the
    # chain (and its wiring) intact.
    labelled = set(nm for _, nm in sh.flags)
    wanted = ((must_flag | (expr_nets(deck, text_fallback) & drawn_nets))
              - labelled - {'0'})
    for n in sorted(wanted):
        if n in sh.junction:
            sh.flag(sh.junction[n], n)
            labelled.add(n)
    for n in sorted(must_flag - labelled):
        raise LayoutError('net %r is shared with a TEXT card but never labelled' % n)

    for c in chains:
        if not c.placed:
            raise LayoutError('chain %s..%s was never placed' % (c.a, c.b))

    info = {
        'chains': len(chains),
        'aux_chains': len(aux),
        'leg': (chH.nets[mk], SW, NBOT),
        'ntop': NTOP,
    }
    return sh, text_fallback, info


# ===========================================================================
# 2c. v2b "spine + branches" layout -- the general wired fallback
# ===========================================================================
#
# The v2 flow layout above can only draw a circuit that HAS a half-bridge leg.
# Everything else used to drop to the v1 label soup.  This layout replaces that
# fallback and draws real wires for any topology:
#
#   1. SPINE.  The chain graph (nodes = nets, edges = series chains) is searched
#      for the simple path that best represents the main signal/power path.  The
#      score is (elements on the path) - (sum over INTERIOR nets of deg-2): a
#      long path is good, threading the path through a star-shaped rail net is
#      bad, because that net wants to be drawn as a rail, not as a waypoint.
#      Ground may only be an END of the spine, never an interior node.
#      The spine is drawn as one horizontal run, left to right.
#   2. BRANCHES.  Every remaining chain hangs off the hub nets:
#        * chain to ground        -> vertical drop, its OWN ground symbol at the
#                                    foot (no shared ground bus);
#        * chain to a NEW net     -> vertical branch UP to a rail one row above
#                                    the spine, which then grows horizontally;
#        * chain to a PLACED net  -> a tap: vertical when the two hubs are on
#                                    different rows (this is what draws a Dickson
#                                    pump capacitor from the input rail down to
#                                    its stage node), horizontal-above when they
#                                    share a row (parallel R/C branches).
#      Branch columns are the attachment point's own x, so repeated motifs come
#      out as one column per repetition, ordered left to right by their spine
#      attachment.  (No motif *recognition* is done -- see NET2ASC.md.)
#   3. K-COUPLED INDUCTORS.  A closed loop chain (both ends on ground) that
#      contains an inductor named by a K card is placed as its own horizontal
#      run, x-aligned with and directly above its coupling partner, so the pair
#      reads as a transformer.
#   4. Anything that still cannot be routed goes to the auxiliary label band,
#      exactly as the flow layout already does.
#
# Every branch is placed SPECULATIVELY: the sheet is checkpointed, the branch is
# drawn, and a validator re-checks the new geometry against everything already
# on the sheet (wire/wire contact between different nets, a pin or FLAG landing
# on a foreign wire, a symbol body overlapping another).  A branch that fails is
# rolled back and retried at the next candidate column / row; if every candidate
# fails it falls back to the label band.  Connectivity is therefore never traded
# for looks: the FLAG guarantee still covers whatever could not be wired.


def _rng_ov(a0, a1, b0, b1):
    return min(a1, b1) >= max(a0, b0)


def _sbox(p, q):
    return (min(p[0], q[0]), min(p[1], q[1]), max(p[0], q[0]), max(p[1], q[1]))


def _pt_on(c, p, q):
    if p[0] == q[0] == c[0] and min(p[1], q[1]) <= c[1] <= max(p[1], q[1]):
        return True
    if p[1] == q[1] == c[1] and min(p[0], q[0]) <= c[0] <= max(p[0], q[0]):
        return True
    return False


def _wire_in_box(p, q, box):
    """wire p-q passes through the OPEN rectangle `box`."""
    x0, y0, x1, y1 = box[:4]
    if p[1] == q[1]:
        return (y0 < p[1] < y1 and
                max(min(p[0], q[0]), x0) < min(max(p[0], q[0]), x1))
    return (x0 < p[0] < x1 and
            max(min(p[1], q[1]), y0) < min(max(p[1], q[1]), y1))


def _box_ov(a, b, shrink=1.0):
    """strict overlap of two rectangles (mere touching is not an overlap)."""
    return (min(a[2], b[2]) - max(a[0], b[0]) > shrink and
            min(a[3], b[3]) - max(a[1], b[1]) > shrink)


def text_clashes(sh, m):
    """-> list of (new_box, old_box) pairs of TEXT that visually collide.

    Checked: attribute text vs attribute text, attribute/label text vs a
    SYMBOL BODY, net label vs net label.  NOT checked: text over a wire (LTspice
    schematics do that constantly and it reads fine), and the free TEXT
    directive block, which is emitted last, below everything else."""
    ntb, nb = m[7], m[5]
    out = []
    for nbx in sh.tboxes[ntb:]:
        for obx in sh.tboxes[:ntb]:
            if nbx[4] == obx[4]:
                continue                 # same symbol's own name/value pair
            if _box_ov(nbx, obx):
                out.append((nbx, obx))
        for obx in sh.boxes[:nb]:
            if nbx[4] == obx[5]:
                continue                 # a symbol may label itself
            if _box_ov(nbx, obx[6:10]):
                out.append((nbx, (obx[6], obx[7], obx[8], obx[9], obx[5], 'body')))
    for nbx in sh.boxes[nb:]:
        box = (nbx[6], nbx[7], nbx[8], nbx[9], nbx[5], 'body')
        for obx in sh.tboxes[:ntb]:
            if obx[4] == nbx[5]:
                continue
            if _box_ov(box, obx):
                out.append((box, obx))
    return out


def validate_new(sh, m, text_check=True):
    """Re-check everything added since checkpoint `m`.  Raises LayoutError."""
    nw, nf, _ns, _nt, npp, nb = m[0], m[1], m[2], m[3], m[4], m[5]
    old_w, new_w = sh.wires[:nw], sh.wires[nw:]
    if not new_w and len(sh.boxes) == nb:
        return
    for (p, q, net) in new_w:
        b = _sbox(p, q)
        for (r, s, net2) in old_w:
            if net2 == net:
                continue
            b2 = _sbox(r, s)
            if _rng_ov(b[0], b[2], b2[0], b2[2]) and _rng_ov(b[1], b[3], b2[1], b2[3]):
                raise LayoutError('wire %s-%s (net %s) would touch wire %s-%s '
                                  '(net %s)' % (p, q, net, r, s, net2))
        for (inst, k, c, n2) in sh.pinpts[:npp]:
            if n2 is not None and n2 != net and _pt_on(c, p, q):
                raise LayoutError('wire (net %s) would touch %s.pin%d (net %s)'
                                  % (net, inst, k + 1, n2))
        for (c, nm) in sh.flags[:nf]:
            if nm != net and _pt_on(c, p, q):
                raise LayoutError('wire (net %s) would touch FLAG %s' % (net, nm))
        for box in sh.boxes[:nb]:
            if net not in box[4] and _wire_in_box(p, q, box):
                raise LayoutError('wire (net %s) would cross the body of %s'
                                  % (net, box[5]))
    for (inst, k, c, n) in sh.pinpts[npp:]:
        if n is None:
            continue
        for (p, q, net) in old_w:
            if net != n and _pt_on(c, p, q):
                raise LayoutError('%s.pin%d (net %s) would land on a net-%s wire'
                                  % (inst, k + 1, n, net))
    for (c, nm) in sh.flags[nf:]:
        for (p, q, net) in old_w:
            if net != nm and _pt_on(c, p, q):
                raise LayoutError('FLAG %s would land on a net-%s wire' % (nm, net))
    for box in sh.boxes[nb:]:
        for (p, q, net) in old_w:
            if net not in box[4] and _wire_in_box(p, q, box):
                raise LayoutError('body of %s would cross a net-%s wire'
                                  % (box[5], net))
        for ob in sh.boxes[:nb]:
            if (_rng_ov(box[0] + 1, box[2] - 1, ob[0] + 1, ob[2] - 1) and
                    _rng_ov(box[1] + 1, box[3] - 1, ob[1] + 1, ob[3] - 1)):
                raise LayoutError('symbol %s would overlap %s' % (box[5], ob[5]))
    if text_check:
        cl = text_clashes(sh, m)
        if cl:
            a, b = cl[0]
            raise LayoutError('text %r would overlap %r (%d clash%s)'
                              % (a[4], b[4], len(cl),
                                 '' if len(cl) == 1 else 'es'))


def chain_graph(chains, aux_only):
    adj = defaultdict(list)
    for c in chains:
        if id(c) in aux_only or c.a == c.b:
            continue
        adj[c.a].append((c, c.b))
        adj[c.b].append((c, c.a))
    return adj


def pick_spine(chains, aux_only, edges=None, budget=200000):
    """Longest / least-star-crossing simple path through the chain graph.

    Returns (chains_on_path, nets_on_path) or None.  Deterministic: candidate
    edges are visited in chain-declaration order, never in id() order.

    Ranking key, in order:
      1. elements on the path MINUS a star penalty.  deg 3 is a perfectly good
         waypoint (in, out, and one branch hanging off it -- a Dickson stage
         node, a filter tap).  Only a genuine STAR (deg >= 4: a rail feeding
         many branches) is a bad net to thread a spine through, because it
         wants to be drawn as a rail of its own.  Ground is exempt: it is a
         star in every circuit and it is drawn as local ground symbols anyway.
      2. raw element count.
      3. HOMOGENEITY -- the fraction of the path made of one element type.  A
         repeated motif (a diode ladder, an LC ladder) is exactly what a human
         puts on the main axis, and this is the tie-break that picks the six
         series diodes of a Dickson pump over five diodes plus a capacitor."""
    adj = chain_graph(chains, aux_only)
    if not adj:
        return None
    cidx = dict((id(c), i) for i, c in enumerate(chains))
    deg = dict((n, len(v)) for n, v in adj.items())
    budget = [budget]
    best = [None]

    def score(path_nets, path_chains):
        nel = sum(len(c) for c in path_chains)
        pen = sum(max(0, deg[n] - 3) for n in path_nets if n != '0')
        hom = 0.0
        if edges is not None and nel:
            cnt = defaultdict(int)
            for c in path_chains:
                for (i, _, _) in c.steps:
                    cnt[edges[i][0].letter] += 1
            hom = max(cnt.values()) / float(nel)
        return (nel - pen, nel, hom, len(path_chains))

    def dfs(cur, path_nets, path_chains, visited):
        if budget[0] <= 0:
            return
        budget[0] -= 1
        if path_chains:
            s = score(path_nets, path_chains)
            if best[0] is None or s > best[0][0]:
                best[0] = (s, list(path_chains), list(path_nets))
        if cur == '0' and path_chains:
            return                       # ground is an END, never a waypoint
        for c, o in sorted(adj[cur], key=lambda t: (cidx[id(t[0])], t[1])):
            if o in visited:
                continue
            visited.add(o)
            path_nets.append(o)
            path_chains.append(c)
            dfs(o, path_nets, path_chains, visited)
            visited.discard(o)
            path_nets.pop()
            path_chains.pop()

    for s0 in sorted(adj):
        dfs(s0, [s0], [], set([s0]))
    if best[0] is None:
        return None
    pc, pn = best[0][1], best[0][2]
    # Reading direction: the busier end of the spine goes on the LEFT.  An
    # input rail / return node fans out to many branches; a load terminates a
    # single one.  (Ties broken on the net name so the output is stable.)
    ka = (deg.get(pn[0], 0), pn[0])
    kb = (deg.get(pn[-1], 0), pn[-1])
    if kb > ka:
        pc = list(reversed(pc))
        pn = list(reversed(pn))
    return pc, pn


def _k_partners(deck):
    """inductor name (lower) -> set of inductor names it is K-coupled to."""
    out = defaultdict(set)
    for k in deck.couplings:
        names = [t.lower() for t in k.split()[1:] if re.match(r'^[A-Za-z]', t)]
        for a in names:
            for b in names:
                if a != b:
                    out[a].add(b)
    return out


# ===========================================================================
# v2c -- the ONE structural template: 4-switch bridge + coupled-inductor pair
# ===========================================================================
# Detected from the ELECTRICAL definition, exactly the way find_leg() detects a
# half-bridge, never from element names:
#
#   * four switching devices (`sw` symbols, or 3-terminal MOSFET subckt calls)
#     arranged as TWO LEGS across one common supply rail and one common return,
#     giving TWO distinct midpoints.  A MOSFET must face the midpoint the way
#     leg_orientation_ok() requires; a `sw` is symmetric and is not constrained.
#   * the two midpoints are joined by a path of ordinary two-terminal elements
#     that contains at least one inductor named by a `K` card -- i.e. the
#     transformer / resonant-tank primary.  The path may not run through the
#     rail, the return or ground.
#
# If any part of that fails, find_bridge() returns None and the caller uses the
# ordinary spine layout.  The template never becomes a reason to fail.

BRIDGE_MIN_DX = 1216     # minimum distance between the two leg columns, so the
#                          body diode / Coss columns beside each leg still fit
BRIDGE_TOP = 128         # rail -> first high-side pin
BRIDGE_MIDGAP = 160      # midpoint -> first low-side pin
CTRL_STUB = 96           # stub on a switch's control terminals in the spine
#                          layout: long enough that the control net's label
#                          clears the symbol's own InstName / Value text
BRIDGE_MID_STUB = 192    # outward stub carrying the midpoint's net label,
#                          long enough to clear the switch's control pins
ISLAND_GAP_X = 448       # gap between two islands packed side by side
ISLAND_GAP_Y = 384
PAGE_ASPECT = 1.5        # target width : height of the packed island block


def _bridge_link(chains, used, aux_only, mid1, mid2, forbid, kinds, edges,
                 cidx, limit=6):
    """Shortest chain path mid1 -> mid2 that carries a K-coupled inductor.

    Returns (chains_on_path, nets_on_path) or None.  Deterministic: neighbours
    are visited in chain-declaration order."""
    adj = defaultdict(list)
    for c in chains:
        if c.placed or id(c) in used or id(c) in aux_only or c.a == c.b:
            continue
        adj[c.a].append((c, c.b))
        adj[c.b].append((c, c.a))
    best = [None]

    def dfs(cur, pc, pn, seen):
        if len(pc) > limit:
            return
        if cur == mid2 and pc:
            if not any(edges[i][0].name.lower() in kinds
                       for c in pc for (i, _, _) in c.steps):
                return
            key = (len(pc), tuple(cidx[id(c)] for c in pc))
            if best[0] is None or key < best[0][0]:
                best[0] = (key, list(pc), list(pn))
            return
        for c, o in sorted(adj[cur], key=lambda t: (cidx[id(t[0])], t[1])):
            if o in seen or (o != mid2 and o in forbid):
                continue
            seen.add(o); pn.append(o); pc.append(c)
            dfs(o, pc, pn, seen)
            pc.pop(); pn.pop(); seen.discard(o)

    dfs(mid1, [], [mid1], set([mid1]))
    return None if best[0] is None else (best[0][1], best[0][2])


def find_bridge(edges, chains, kpart, aux_only):
    """-> spec dict for the 4-switch bridge template, or None."""
    if not kpart:
        return None
    cidx = dict((id(c), i) for i, c in enumerate(chains))
    swc = [c for c in chains
           if len(sw_steps(c, edges)) == 1 and c.a != c.b]
    if len(swc) < 4:
        return None
    # every (rail, mid, ret) leg the deck contains
    legs = []
    for hi in swc:
        for lo in swc:
            if hi is lo:
                continue
            for mid in sorted(set([hi.a, hi.b]) & set([lo.a, lo.b])):
                if mid == '0':
                    continue
                h = hi.oriented(hi.a if hi.b == mid else hi.b)
                l = lo.oriented(mid)
                rail, ret = h.nets[0], l.nets[-1]
                if rail == ret or rail == mid or ret == mid:
                    continue
                if not leg_orientation_ok(h, l, edges):
                    continue
                legs.append((rail, ret, mid, h, l, hi, lo))
    # two legs across the SAME rail and return, with different midpoints
    best = None
    for i, (r1, e1, m1, h1, l1, oh1, ol1) in enumerate(legs):
        for (r2, e2, m2, h2, l2, oh2, ol2) in legs[i + 1:]:
            if (r1, e1) != (r2, e2) or m1 == m2:
                continue
            used = set(id(c) for c in (oh1, ol1, oh2, ol2))
            if len(used) != 4:
                continue
            link = _bridge_link(chains, used, aux_only, m1, m2,
                                set([r1, e1, '0']), set(kpart), edges, cidx)
            if link is None:
                continue
            lchains, lnets = link
            # a ground return reads as the bottom of the picture; prefer it.
            key = (0 if e1 == '0' else 1, len(lchains),
                   tuple(sorted(cidx[id(c)] for c in (oh1, ol1, oh2, ol2))))
            if best is None or key < best[0]:
                best = (key, dict(rail=r1, ret=e1, mid1=m1, mid2=m2,
                                  u1=h1, l1=l1, u2=h2, l2=l2,
                                  ord1=cidx[id(oh1)], ord2=cidx[id(oh2)],
                                  link=lchains, link_nets=lnets,
                                  chains=[oh1, ol1, oh2, ol2] + list(lchains),
                                  coils=[edges[i2][0].name
                                         for c in lchains
                                         for (i2, _, _) in c.steps
                                         if edges[i2][0].name.lower() in kpart]))
    if best is None:
        return None
    # orient the pair so the leg drawn on the left is the one declared first
    b = best[1]
    if b['ord2'] < b['ord1']:
        b['mid1'], b['mid2'] = b['mid2'], b['mid1']
        b['u1'], b['u2'] = b['u2'], b['u1']
        b['l1'], b['l2'] = b['l2'], b['l1']
        b['link'] = list(reversed(b['link']))
        b['link_nets'] = list(reversed(b['link_nets']))
    return b


def _mid_label(sh, x, sgn, y, net):
    """Outward stub carrying a bridge midpoint's net label.

    The midpoint itself is a four-way junction, so a label dropped straight on
    it lands on the switch symbols.  The stub length is chosen adaptively: the
    switches' own control-terminal labels stick out on whichever side their
    orientation puts them, so the first length whose label does not collide
    with anything already drawn wins."""
    for k in (0, 1, 2, -1, 3):
        m = sh.mark()
        pt = (x + sgn * (BRIDGE_MID_STUB + 96 * k), y)
        sh.wire((x, y), pt, net)
        sh.flag(pt, net)
        if not text_clashes(sh, m):
            return pt
        sh.rollback(m)
    pt = (x + sgn * BRIDGE_MID_STUB, y)
    sh.wire((x, y), pt, net)
    sh.flag(pt, net)
    return pt


def place_bridge(sh, br, edges, hub, on_spine, bandx, items_of, extra_pins,
                 band_y):
    """Draw the bridge the way a human draws it.

        rail  ────────────┬──────────────────────┬────────────
                       [u1]                   [u2]
        mid1  ────────────┼──[ primary / tank ]──┼──────  mid2
                       [l1]                   [l2]
        ret   ────────────┴──────────────────────┴────────────

    Everything else in the deck (body diodes, Coss, snubbers, gate drive, the
    supply, the secondary) is left to the ordinary branch machinery, which now
    finds the four bridge nets already hubbed."""
    rail, ret = br['rail'], br['ret']
    m1, m2 = br['mid1'], br['mid2']
    u1 = br['u1'].oriented(rail)
    u2 = br['u2'].oriented(rail)
    l1 = br['l1'].oriented(m1)
    l2 = br['l2'].oriented(m2)

    lu1 = sh.run_len(items_of(u1), 'D')
    lu2 = sh.run_len(items_of(u2), 'D')
    ll1 = sh.run_len(items_of(l1), 'D')
    ll2 = sh.run_len(items_of(l2), 'D')
    rail_y = band_y
    mid_y = rail_y + BRIDGE_TOP + max(lu1, lu2)
    ret_y = mid_y + BRIDGE_MIDGAP + max(ll1, ll2)
    mid_y += (-mid_y) % GRID
    ret_y += (-ret_y) % GRID

    # width: enough for the whole primary run between the two midpoints
    lchains, cur_net = [], m1
    for c in br['link']:
        co = c.oriented(cur_net)
        lchains.append(co)
        cur_net = co.nets[-1]
    prim = sum(sh.run_len(items_of(c), 'R') + LEAD_H for c in lchains)
    x1 = 0
    pad = max(0, BRIDGE_MIN_DX - prim)
    pad += (-pad) % GRID
    x2 = x1 + pad + prim
    x2 += (-x2) % GRID

    def leg(x, up, lo, mid):
        s = (x, mid_y - sh.run_len(items_of(up), 'D'))
        sh.wire((x, rail_y), s, rail)
        e = sh.run(s, 'D', items_of(up), up.nets)
        extra_pins(up)
        sh.wire(e, (x, mid_y), mid)
        e2 = sh.run((x, mid_y), 'D', items_of(lo), lo.nets)
        extra_pins(lo)
        sh.wire(e2, (x, ret_y), ret)

    leg(x1, u1, l1, m1)
    leg(x2, u2, l2, m2)

    # supply rail on top, return at the bottom
    sh.wire((x1, rail_y), (x2, rail_y), rail)
    sh.wire((x1, ret_y), (x2, ret_y), ret)
    xm = (x1 + x2) // 2
    xm -= xm % GRID
    hub[rail] = (x1, rail_y)
    sh.flag((x1, rail_y), rail)
    sh.set_junction(rail, (x1, rail_y))
    if ret == '0':
        g = (xm, ret_y + LEAD_V)
        sh.wire((xm, ret_y), g, '0')
        sh.flag(g, '0')
    else:
        hub[ret] = (xm, ret_y)
        sh.flag((xm, ret_y), ret)
        sh.set_junction(ret, (xm, ret_y))

    # the primary between the two midpoints
    pt = (x1 + pad, mid_y)
    sh.wire((x1, mid_y), pt, m1)
    hub[m1] = (x1, mid_y)
    # the midpoint label goes on a short OUTWARD stub: the midpoint itself is a
    # four-way junction (both switches, the primary, the snubber column) and a
    # label dropped on it lands on top of the switch symbols.
    lm = _mid_label(sh, x1, -1, mid_y, m1)
    sh.set_junction(m1, lm)
    for c in lchains:
        end = sh.run(pt, 'R', items_of(c), c.nets)
        extra_pins(c)
        tail = (end[0] + LEAD_H, end[1])
        sh.wire(end, tail, c.nets[-1])
        sh.set_junction(c.nets[-1], tail)
        pt = tail
        if c.nets[-1] != m2:
            hub[c.nets[-1]] = tail
            sh.flag(tail, c.nets[-1])
    hub[m2] = (x2, mid_y)
    rm = _mid_label(sh, x2, 1, mid_y, m2)
    sh.set_junction(m2, rm)

    seeds = [rail, m1, m2] + [c.nets[-1] for c in lchains if c.nets[-1] != m2]
    if ret != '0':
        seeds.append(ret)
    for n in seeds:
        on_spine.add(n)
        bandx[n] = (x1, x2)
    ok, problems = geometric_check(sh)
    if not ok:
        raise LayoutError('bridge template: ' + problems[0])
    # `u1`/`l1`/... are ORIENTED COPIES; the originals are the objects the rest
    # of the placer tracks, so they are the ones that must be marked placed.
    for c in br['chains']:
        c.placed = True
    return seeds


# ---------------------------------------------------------------------------
# island packing: 2-D shelves instead of one 8000-unit column
# ---------------------------------------------------------------------------
def _pack_order(n, bridge, sh, kpart):
    """Island order for the shelf packer.  Declaration order, except that the
    island holding the bridge transformer's SECONDARY is pulled up next to the
    bridge so the two sit side by side."""
    order = list(range(n))
    if not bridge or n < 3:
        return order
    partners = set()
    for nm in bridge.get('coils', ()):
        partners |= set(kpart.get(nm.lower(), ()))
    tgt = None
    for si, s in enumerate(sh.syms):
        if s['inst'].lower() in partners:
            g = sh.sgrp[si]
            if g > 0 and (tgt is None or g < tgt):
                tgt = g
    if tgt is None or tgt == 1:
        return order
    order.remove(tgt)
    order.insert(1, tgt)
    return order


def pack_islands(sh, n, order):
    """Shelf-pack the islands so the sheet is page-shaped, not a ribbon.

    Islands are drawn stacked in one column (so each one's placement validator
    only ever looks at finished geometry) and moved here as rigid bodies.  The
    move is by whole multiples of GRID and the shelves are separated by
    ISLAND_GAP_*, so no island can come into contact with another one and the
    connectivity of the drawing is untouched."""
    import math
    bb = {}
    for g in range(n):
        b = sh.group_bbox(g)
        if b is not None:
            bb[g] = b
    if len(bb) < 2:
        return []
    seq = [(g, bb[g][2] - bb[g][0], bb[g][3] - bb[g][1])
           for g in order if g in bb]
    widest = max(w for _, w, _ in seq)
    total = sum(w for _, w, _ in seq) + ISLAND_GAP_X * (len(seq) - 1)

    def shelves(target):
        """-> [(gid, x, y, w, h)], keeping the reading order of `seq`."""
        out, cx, cy, sh_h = [], 0, 0, 0
        for (g, w, h) in seq:
            if cx > 0 and cx + w > target:
                cy += sh_h + ISLAND_GAP_Y
                cx = sh_h = 0
            out.append((g, cx, cy, w, h))
            cx += w + ISLAND_GAP_X
            sh_h = max(sh_h, h)
        return out

    # The target width is SEARCHED rather than guessed: shelf packing with a
    # handful of large, very unequal boxes is nowhere near the ideal
    # sqrt(area * aspect), so every candidate width is simulated and the one
    # whose resulting page comes closest to PAGE_ASPECT wins.  Deterministic.
    best = None
    cands = sorted(set([widest] +
                       [widest + (total - widest) * i // 48 for i in range(49)]))
    for t in cands:
        pl = shelves(t)
        W = max(x + w for (_, x, _, w, _) in pl)
        H = max(y + h for (_, _, y, _, h) in pl)
        key = (round(abs(math.log((float(W) / max(H, 1)) / PAGE_ASPECT)), 6),
               W * H, t)
        if best is None or key < best[0]:
            best = (key, pl)
    placed = []
    for (g, x, y, w, h) in best[1]:
        b = bb[g]
        dx = int(math.floor(x - b[0]))
        dy = int(math.floor(y - b[1]))
        dx -= dx % GRID
        dy -= dy % GRID
        sh.translate_group(g, dx, dy)
        placed.append((g, int(w), int(h)))
    return placed


def refresh_flag_boxes(sh):
    """Recompute the net-label text boxes once the drawing is FINISHED.

    During placement a label's box has to be guessed conservatively (which side
    of the flag point the string ends up on depends on wires that do not exist
    yet).  Here the whole wire set is known, so asc2svg.py's own `free_side`
    rule is replayed and the boxes become the ones the renderer will really
    use.  The reported residual overlap count is based on these."""
    occ = defaultdict(set)
    for (p, q, _) in sh.wires:
        if p == q:
            continue
        if p[0] == q[0]:
            occ[p].add('D' if q[1] > p[1] else 'U')
            occ[q].add('D' if p[1] > q[1] else 'U')
        elif p[1] == q[1]:
            occ[p].add('R' if q[0] > p[0] else 'L')
            occ[q].add('R' if p[0] > q[0] else 'L')
    kept = [(b, g) for b, g in zip(sh.tboxes, sh.tbgrp) if b[5] != 'flag']
    seen = defaultdict(int)
    sz = FLAG_FONT
    lh = 1.15 * sz
    for i, (p, nm) in enumerate(sh.flags):
        if nm == '0':
            continue
        n = seen[p]
        seen[p] += 1
        w = text_width(nm, sz)
        side = 'U'
        for d in ('U', 'D', 'R', 'L'):
            if d not in occ.get(p, ()):
                side = d
                break
        if side == 'U':
            tx, ty, anc = p[0], p[1] - 10 - n * lh, 'C'
        elif side == 'D':
            tx, ty, anc = p[0], p[1] + 10 + 0.8 * sz + n * lh, 'C'
        elif side == 'R':
            tx, ty, anc = p[0] + 10, p[1] + 0.35 * sz + n * lh, 'S'
        else:
            tx, ty, anc = p[0] - 10, p[1] + 0.35 * sz + n * lh, 'E'
        if anc == 'C':
            x0, x1 = tx - w / 2.0, tx + w / 2.0
        elif anc == 'S':
            x0, x1 = tx, tx + w
        else:
            x0, x1 = tx - w, tx
        kept.append(((x0, ty - 0.8 * sz, x1, ty + 0.2 * sz,
                      'FLAG:' + nm, 'flag'), sh.fgrp[i]))
    sh.tboxes[:] = [b for b, _ in kept]
    sh.tbgrp[:] = [g for _, g in kept]


def count_all_text_clashes(sh):
    """Total number of ESTIMATED text/text and text/symbol-body overlaps left in
    the finished drawing.  Reported, not fatal.  See NET2ASC.md 5B.9."""
    n = 0
    tb = sh.tboxes
    for i in range(len(tb)):
        for j in range(i + 1, len(tb)):
            if tb[i][4] != tb[j][4] and _box_ov(tb[i], tb[j]):
                n += 1
    for t in tb:
        for b in sh.boxes:
            if t[4] != b[5] and _box_ov(t, b[6:10]):
                n += 1
    return n


def spine_build(deck, pins, mosmap, cirpath=None):
    """v2b layout.  Raises LayoutError when no usable spine exists."""
    coupled = coupled_inductors(deck)
    kpart = _k_partners(deck)

    drawn_nets, text_nets = set(), set()
    for e in deck.elements:
        sym = symbol_for(e, pins, mosmap, coupled)
        (drawn_nets if sym else text_nets).update(e.nodes)
    must_flag = (drawn_nets & text_nets) - {'0'}

    # asc2ngspice.py names an unlabelled junction 'n<k>' and does not check that
    # against the FLAG names already in use.  A deck that itself has nets called
    # n1/n2/... can therefore have a real node and a reconstructed one collapse
    # onto the same name -- which is a genuine wrong-netlist hazard, not just a
    # cosmetic one.  When such a name exists we label EVERY drawn net, so no
    # auto-generated name is ever produced.  (Chains are still contracted, so
    # this costs labels, not wires.)
    name_clash_risk = any(re.match(r'^[nN]\d+$', n) for n in drawn_nets)

    edges, chains, gate_of, text_fallback = build_chains(
        deck, pins, mosmap, coupled, must_flag)
    gate_nets = control_nets(edges, gate_of)
    aux_only = set(id(c) for c in chains if gate_nets & {c.a, c.b})

    sh = Sheet(pins)
    sh.autostagger = True
    hub = {}                 # net -> anchor coordinate
    on_spine = set()         # nets drawn on a spine row (as opposed to a rail)
    bandx = {}               # net -> (x0, x1) of the spine of ITS island

    def items_of(ch):
        return [(edges[i][0], edges[i][1], ps, pe) for (i, ps, pe) in ch.steps]

    def extra_pins(ch):
        """stub+FLAG the gate / control terminals of everything just placed."""
        for (i, ps, pe) in ch.steps:
            e, sym = edges[i][0], edges[i][1]
            if len(pins[sym]) <= 2:
                continue
            for s in sh.syms:
                if s['inst'] == e.name:
                    sh.aux_pin_stubs(sym, s['ori'], (s['x'], s['y']),
                                     e.nodes, (ps, pe), lead=CTRL_STUB)
                    break

    # vertical pitch: every branch must fit between two rows
    vlen = [sh.run_len(items_of(c), 'D') for c in chains if id(c) not in aux_only]
    ROW = max(SPINE_ROW_MIN, (max(vlen) if vlen else 0) + DROP_LEAD + 2 * LEAD_V)
    ROW += (-ROW) % GRID

    # ---------------- 1. one spine per island ------------------------------
    # Two parts of a circuit that touch only through ground (an isolated
    # converter's primary and secondary, a bridge and its rectifier) are
    # separate components of the chain graph, because ground is drawn as local
    # ground symbols and is never a hub to expand through.  Each such island
    # gets its own spine, stacked in its own horizontal band.
    def place_spine(sp_chains, sp_nets, band_y):
        pt = (0, band_y)
        cur_net = sp_nets[0]
        if cur_net == '0':
            g = (pt[0], pt[1] + LEAD_V)
            sh.wire(pt, g, '0')
            sh.flag(g, '0')
        else:
            hub[cur_net] = pt
            on_spine.add(cur_net)
            sh.flag(pt, cur_net)
        for c in sp_chains:
            co = c.oriented(cur_net)
            end = sh.run(pt, 'R', items_of(co), co.nets)
            extra_pins(co)
            tail = (end[0] + LEAD_H, end[1])
            sh.wire(end, tail, co.nets[-1])
            sh.set_junction(co.nets[-1], tail)
            cur_net = co.nets[-1]
            c.placed = True
            if cur_net == '0':
                g = (tail[0], tail[1] + LEAD_V)
                sh.wire(tail, g, '0')
                sh.flag(g, '0')
            else:
                hub[cur_net] = tail
                on_spine.add(cur_net)
                sh.flag(tail, cur_net)
            pt = tail
        span = (0, pt[0])
        for n in sp_nets:
            if n != '0':
                bandx[n] = span
        return [n for n in sp_nets if n in hub]

    # ---------------- 2. branches ------------------------------------------
    def unplaced_at(net):
        return [c for c in chains
                if not c.placed and id(c) not in aux_only and c.a != c.b
                and net in (c.a, c.b)]

    def drop_gnd(net, ch, col, jog):
        c = ch.oriented(net)
        hx, hy = hub[net]
        pts = [(hx, hy), (hx, hy + jog)]
        if col != hx:
            pts.append((col, hy + jog))
        sh.poly(pts, net)
        end = sh.run(pts[-1], 'D', items_of(c), c.nets)
        extra_pins(c)
        g = (end[0], end[1] + LEAD_V)
        sh.wire(end, g, c.nets[-1])
        sh.flag(g, '0')

    def branch_up(net, ch, off=0):
        """vertical branch from a spine hub up to a new rail one row above.

        `off` shifts the riser sideways along the hub's own row, which is what
        lets a branch leave a BRIDGE midpoint: the midpoint's own column is
        taken by the two switches of its leg."""
        c = ch.oriented(net)
        hx, hy = hub[net]
        if off:
            sh.wire((hx, hy), (hx + off, hy), net)
            hx += off
        end = sh.run((hx, hy), 'U', items_of(c), c.nets)
        extra_pins(c)
        top = (hx, hy - ROW)
        if end[1] <= top[1]:
            raise LayoutError('branch %s..%s is taller than the row pitch'
                              % (c.a, c.b))
        sh.wire(end, top, c.nets[-1])
        hub[c.nets[-1]] = top
        bandx[c.nets[-1]] = bandx.get(net, (0, 0))
        sh.flag(top, c.nets[-1])
        sh.set_junction(c.nets[-1], top)
        return c.nets[-1]

    def grow_side(net, ch, d):
        """rail growing sideways to a brand-new hub."""
        c = ch.oriented(net)
        hx, hy = hub[net]
        end = sh.run((hx, hy), d, items_of(c), c.nets)
        extra_pins(c)
        dx, dy = DIRV[d]
        tail = (end[0] + dx * LEAD_H, end[1] + dy * LEAD_H)
        sh.wire(end, tail, c.nets[-1])
        hub[c.nets[-1]] = tail
        bandx[c.nets[-1]] = bandx.get(net, (0, 0))
        if net in on_spine:
            on_spine.add(c.nets[-1])
        sh.flag(tail, c.nets[-1])
        sh.set_junction(c.nets[-1], tail)
        return c.nets[-1]

    def vtap(top, bot, ch, col):
        """chain between two hubs on different rows, drawn vertically."""
        c = ch.oriented(top)
        tx, ty = hub[top]
        bx, by = hub[bot]
        pts = [(tx, ty)]
        if col != tx:
            pts.append((col, ty))
        pts.append((col, ty + DROP_LEAD))
        sh.poly(pts, top)
        end = sh.run((col, ty + DROP_LEAD), 'D', items_of(c), c.nets)
        extra_pins(c)
        if end[1] > by:
            raise LayoutError('tap %s..%s overshoots its lower rail' % (top, bot))
        sh.poly([end, (col, by), (bx, by)], c.nets[-1])

    couple_bands = []            # (ylo, yhi): keep this gap clear so the two
    #                              halves of a K-coupled pair stay adjacent

    def htap(l, r, ch, dy, off=0):
        """chain between two hubs on the same row, drawn above it.

        `off` moves the riser away from the left hub's own column, which a
        bridge midpoint needs: its column is occupied by the leg itself."""
        c = ch.oriented(l)
        lx, ly = hub[l]
        rx, ry = hub[r]
        y2 = ly + dy
        if any(lo < y2 < hi for lo, hi in couple_bands):
            raise LayoutError('row %d is reserved for a K-coupled pair' % y2)
        if off:
            sh.wire((lx, ly), (lx + off, ly), l)
            lx += off
        if lx + sh.run_len(items_of(c), 'R') > rx:
            raise LayoutError('parallel chain %s..%s does not fit' % (l, r))
        sh.wire((lx, ly), (lx, y2), l)
        end = sh.run((lx, y2), 'R', items_of(c), c.nets)
        extra_pins(c)
        sh.poly([end, (rx, y2), (rx, ry)], c.nets[-1])

    text_overlaps = [0]

    def attempt(fn, cands):
        """Speculative placement: draw, validate, keep or undo.

        Two passes.  The first insists that nothing new collides -- INCLUDING
        attribute / net-label TEXT.  If every candidate fails that, the second
        pass drops only the TEXT condition and takes the first candidate that
        is electrically and geometrically sound, COUNTING the residual text
        overlaps rather than banishing the chain to the label band.  Wire,
        pin, FLAG and symbol-body contact is never traded away.

        hub bookkeeping is snapshotted too -- branch_up/grow_side register a
        new hub BEFORE the geometry can be validated."""
        for strict in (True, False):
            for a in cands:
                m = sh.mark()
                hb, rw, os_ = dict(hub), dict(bandx), set(on_spine)
                try:
                    out = fn(*a)
                    validate_new(sh, m, text_check=strict)
                    if not strict:
                        text_overlaps[0] += len(text_clashes(sh, m))
                    return out, True
                except LayoutError:
                    sh.rollback(m)
                    hub.clear(); hub.update(hb)
                    bandx.clear(); bandx.update(rw)
                    on_spine.clear(); on_spine.update(os_)
        return None, False

    def gnd_cands(net):
        hx, hy = hub[net]
        out = []
        sx0, sx1 = bandx.get(net, (0, 0))
        if net in on_spine:
            out.append((hx, DROP_LEAD))
            for k in range(1, 8):
                out.append((hx + SPINE_COL_DX * k, DROP_LEAD))
                out.append((hx - SPINE_COL_DX * k, DROP_LEAD))
        else:
            # a rail above the spine must not drop THROUGH the spine
            if hx < sx0 - GRID or hx > sx1 + GRID:
                out += [(hx, 0), (hx, DROP_LEAD)]
            for k in range(1, 10):
                out.append((sx1 + SPINE_COL_DX * k, 0))
                out.append((sx0 - SPINE_COL_DX * k, 0))
        return [((c - c % GRID), j) for c, j in out]

    # ---- K-coupled closed loops -------------------------------------------
    # A chain whose two ends are the SAME net (a source driving an isolated
    # loop back to ground) has no hub to hang off.  When it contains an
    # inductor named by a K card it is placed as its own horizontal run,
    # x-aligned with and directly above its coupling partner, so the pair reads
    # as a transformer.  This runs as soon as the partner has been drawn, and
    # the gap it opens is reserved (couple_bands) so a later parallel branch
    # cannot be routed between the two coils.
    def _sym_centre(s):
        offs = _pin_offs(pins, s['sym'], s['ori'])
        xs = [s['x'] + dx for dx, _ in offs]
        ys = [s['y'] + dy for _, dy in offs]
        return ((min(xs) + max(xs)) // 2, (min(ys) + max(ys)) // 2)

    def place_loop(ch, target, cx_t, cy_t, lead=LEAD_H):
        """horizontal run with a ground symbol at each end.

        `target` names an element inside the run whose PIN CENTRE must land on
        (cx_t, cy_t).  Matching the pin centre, not the symbol origin, is what
        actually stacks the two coils: a run drawn left-to-right and one drawn
        right-to-left use mirrored orientations, whose bodies sit on opposite
        sides of the same origin."""
        items = items_of(ch)
        pre, x0, y0 = 0, 0, 0
        for (ee, sym, i0, i1) in items:
            ori, span = _choose_ori(pins, sym, i0, i1, 'R')
            offs = _pin_offs(pins, sym, ori)
            p0 = pre + lead
            org = p0 - offs[i0][0]
            cx = org + (min(o[0] for o in offs) + max(o[0] for o in offs)) // 2
            cy = -offs[i0][1] + (min(o[1] for o in offs) + max(o[1] for o in offs)) // 2
            if ee.name == target:
                x0, y0 = cx_t - cx, cy_t - cy
                break
            pre += lead + span
        x0 -= x0 % GRID
        y0 -= y0 % GRID
        start = (x0, y0)
        head = (x0 - LEAD_H, y0)
        sh.wire(head, start, ch.nets[0])
        sh.flag(head, ch.nets[0])
        end = sh.run(start, 'R', items, ch.nets, lead=lead, stagger=True)
        extra_pins(ch)
        tail = (end[0] + LEAD_H, end[1])
        sh.wire(end, tail, ch.nets[-1])
        sh.flag(tail, ch.nets[-1])

    coupled_placed = []

    def place_pending_loops():
        did = False
        for c in chains:
            if c.placed or id(c) in aux_only or c.a != c.b:
                continue
            align = None
            pgid = sh.gid
            for (i, ps, pe) in c.steps:
                e = edges[i][0]
                for partner in sorted(kpart.get(e.name.lower(), ())):
                    for si, s in enumerate(sh.syms):
                        if s['inst'].lower() == partner:
                            px, py = _sym_centre(s)
                            align = (e.name, px, py)
                            pgid = sh.sgrp[si]
                            break
                    if align:
                        break
                if align:
                    break
            if align is None:
                continue
            cands = []
            for k in range(1, 5):                # above the partner first
                cands.append((align[0], align[1], align[2] - COUPLE_DY * k))
            for k in range(1, 5):                # then below it
                cands.append((align[0], align[1], align[2] + COUPLE_DY * k))
            # the loop must travel with its coupling partner when the islands
            # are repacked, so it is booked to the PARTNER's island, not to
            # whichever island happens to be under construction.
            keep_gid, sh.gid = sh.gid, pgid
            try:
                got, ok = attempt(
                    lambda t, cx, cy: (place_loop(c, t, cx, cy), cy)[1], cands)
            finally:
                sh.gid = keep_gid
            if ok:
                c.placed = True
                coupled_placed.append(c)
                couple_bands.append((min(align[2], got), max(align[2], got)))
                did = True
        return did

    queue = []
    cpos = dict((id(c), i) for i, c in enumerate(chains))

    def place_one(net, c):
        """route ONE chain hanging off hub `net`.  Returns True on success."""
        other = c.b if c.a == net else c.a
        if other == '0':
            _, ok = attempt(lambda cl, jg: drop_gnd(net, c, cl, jg),
                            gnd_cands(net))
            return ok
        if other in hub:
            if hub[other][1] == hub[net][1]:
                l, r = (net, other) if hub[net][0] < hub[other][0] else (other, net)
                cands = [(-PARALLEL_DY * k, 0) for k in range(1, 8)]
                cands += [(-PARALLEL_DY * k, o)
                          for o in (SPINE_COL_DX // 2, SPINE_COL_DX,
                                    SPINE_COL_DX * 2)
                          for k in range(1, 8)]
                _, ok = attempt(lambda dyv, o: htap(l, r, c, dyv, o), cands)
            else:
                top, bot = ((net, other) if hub[net][1] < hub[other][1]
                            else (other, net))
                cols = [hub[bot][0], hub[top][0]]
                cols += [hub[bot][0] + SPINE_COL_DX * k for k in range(1, 6)]
                cols += [hub[bot][0] - SPINE_COL_DX * k for k in range(1, 6)]
                _, ok = attempt(lambda cl: vtap(top, bot, c, cl),
                                [((cl - cl % GRID),) for cl in cols])
            return ok
        up_cands = [(0,)] + [(s2 * SPINE_COL_DX * k,)
                             for k in (1, 2, 3) for s2 in (1, -1)]
        if net in on_spine:
            nn, ok = attempt(lambda o: branch_up(net, c, o), up_cands)
            if not ok:
                # a bridge midpoint has its own column occupied by the leg, so
                # the only remaining direction is sideways
                nn, ok = attempt(lambda dd: grow_side(net, c, dd),
                                 [('L',), ('R',)])
        else:
            nn, ok = attempt(lambda dd: grow_side(net, c, dd), [('L',), ('R',)])
            if not ok:
                nn, ok = attempt(lambda o: branch_up(net, c, o), up_cands)
        if ok:
            queue.append(nn)
        return ok

    def rank(net, c):
        """taps to an existing hub first, then new hubs, then ground drops."""
        other = c.b if c.a == net else c.a
        k = 2 if other == '0' else (0 if other in hub else 1)
        return (k, cpos[id(c)])

    seen = set()

    def expand_queue():
        rounds = 0
        while queue and rounds < 4 * len(chains) + 64:
            rounds += 1
            net = queue.pop(0)
            if net in seen:
                continue
            seen.add(net)
            expand_hub(net)

    def expand_hub(net):
        stuck = set()
        while True:
            # RE-classify before every single placement: two chains leading to
            # the same new net must not both try to create its hub -- the first
            # one creates it, the second becomes a tap onto it.
            todo = [c for c in unplaced_at(net) if id(c) not in stuck]
            if not todo:
                break
            todo.sort(key=lambda c: rank(net, c))
            c = todo[0]
            if place_one(net, c):
                c.placed = True
            else:
                stuck.add(id(c))
        if unplaced_at(net):
            # a chain here could not be routed yet -- it may become routable
            # once the hub at its other end exists, so try again later
            queue.append(net)
            seen.discard(net)

    # ---------------- island driver ----------------------------------------
    # Islands are DRAWN one under the other (each island's placement validator
    # only has to look at what is already on the sheet, and a fresh band below
    # everything is always free), then REPACKED side by side afterwards -- see
    # `pack_islands` below.
    islands = []
    band_y = 0
    binfo = None
    bridge = find_bridge(edges, chains, kpart, aux_only)
    if bridge is None:
        binfo = ('no 4-switch bridge across a common rail and return whose two '
                 'midpoints are joined by a K-coupled inductor')
    else:
        sh.gid = 0
        m0 = sh.mark()
        try:
            seeds = place_bridge(sh, bridge, edges, hub, on_spine, bandx,
                                 items_of, extra_pins, band_y)
        except LayoutError as ex:
            for c in bridge['chains']:
                c.placed = False
            sh.rollback(m0)
            hub.clear(); on_spine.clear(); bandx.clear()
            binfo = 'bridge template rejected: %s' % ex
            bridge = None
        if bridge is not None:
            queue.extend(seeds)
            islands.append(([bridge['rail'], bridge['mid1'], bridge['mid2'],
                             bridge['ret']],
                            [edges[i][0].name for c in bridge['chains']
                             for (i, _, _) in c.steps]))
            expand_queue()
            for _ in range(len(chains) + 1):
                if not place_pending_loops():
                    break
            band_y = sh.bbox()[3] + BAND_GAP
            band_y += (-band_y) % GRID

    while True:
        rest = [c for c in chains
                if not c.placed and id(c) not in aux_only and c.a != c.b]
        if not rest:
            break
        picked = pick_spine(rest, aux_only, edges)
        if picked is None:
            break
        sp_chains, sp_nets = picked
        if sum(len(c) for c in sp_chains) < (2 if not islands else 1):
            break
        sh.gid = len(islands)
        queue.extend(place_spine(sp_chains, sp_nets, band_y))
        islands.append((sp_nets, [edges[i][0].name
                                  for c in sp_chains for (i, _, _) in c.steps]))
        expand_queue()
        for _ in range(len(chains) + 1):
            if not place_pending_loops():
                break
        band_y = sh.bbox()[3] + BAND_GAP
        band_y += (-band_y) % GRID
    if not islands:
        raise LayoutError('no chain-graph path carries two or more elements; '
                          'nothing worth calling a spine')

    # ---------------- 3. leftovers ------------------------------------------
    for _ in range(len(chains) + 1):
        if not place_pending_loops():
            break

    # ---------------- 3b. repack the islands into a page shape --------------
    pack_order = _pack_order(len(islands), bridge, sh, kpart)
    pack_geom = pack_islands(sh, len(islands), pack_order)

    # ---------------- 4. auxiliary label band ------------------------------
    sh.gid = len(islands)
    bx0, by0, bx1, by1 = sh.bbox()
    ay = by1 + AUX_GAP
    aux = [c for c in chains if not c.placed]
    aux.sort(key=lambda c: (c.a, c.b))
    for c in aux:
        items = items_of(c)
        sh.flag((bx0, ay), c.a)
        end = sh.run((bx0, ay), 'R', items, c.nets, lead=AUX_LEAD)
        extra_pins(c)
        sh.wire(end, (end[0] + LEAD_H, end[1]), c.nets[-1])
        sh.flag((end[0] + LEAD_H, end[1]), c.b)
        c.placed = True
        ay += AUX_ROW_DY
    if aux:
        sh.text(bx0, by1 + AUX_GAP - 112,
                ';--- not routed by the spine layout: joined to the drawing by '
                'NET LABELS, not by wires ---')

    labelled = set(nm for _, nm in sh.flags)
    wanted = (must_flag | (expr_nets(deck, text_fallback) & drawn_nets))
    if name_clash_risk:
        wanted |= drawn_nets
    wanted -= (labelled | {'0'})
    for n in sorted(wanted):
        if n in sh.junction:
            sh.flag(sh.junction[n], n)
            labelled.add(n)
    for n in sorted(must_flag - labelled):
        raise LayoutError('net %r is shared with a TEXT card but never labelled' % n)
    if name_clash_risk:
        miss = sorted((drawn_nets - labelled) - {'0'})
        if miss:
            raise LayoutError('deck has auto-name-shaped net names (n<k>), so '
                              'every drawn net must be labelled, but these were '
                              'not: %s' % ', '.join(miss))
    for c in chains:
        if not c.placed:
            raise LayoutError('chain %s..%s was never placed' % (c.a, c.b))

    info = {
        'chains': len(chains),
        'aux_chains': len(aux),
        'islands': islands,
        'spine_nets': islands[0][0],
        'spine_elems': islands[0][1],
        'rails': sorted(n for n in hub if n not in on_spine),
        'coupled_loops': [c.steps and edges[c.steps[0][0]][0].name for c in coupled_placed],
        'row_pitch': ROW,
        'bridge': (None if bridge is None else
                   dict(rail=bridge['rail'], ret=bridge['ret'],
                        mid1=bridge['mid1'], mid2=bridge['mid2'],
                        switches=[edges[i][0].name
                                  for c in (bridge['u1'], bridge['l1'],
                                            bridge['u2'], bridge['l2'])
                                  for (i, _, _) in sw_steps(c, edges)],
                        primary=[edges[i][0].name for c in bridge['link']
                                 for (i, _, _) in c.steps],
                        coils=bridge['coils'])),
        'bridge_note': binfo,
        'text_relaxed': text_overlaps[0],
        'text_overlaps': (refresh_flag_boxes(sh), count_all_text_clashes(sh))[1],
        'pack': pack_geom,
    }
    return sh, text_fallback, info


def build_asc_spine(deck, pins, mosmap, cirpath=None):
    sh, text_fallback, linfo = spine_build(deck, pins, mosmap, cirpath)

    ok, problems = geometric_check(sh)
    if not ok:
        raise LayoutError('geometric self-check failed:\n  ' + '\n  '.join(problems))

    x0, y0, x1, y1 = sh.bbox()
    body = _directive_text(deck, text_fallback)
    ty0 = y1 + AUX_GAP
    sh.text(x0, ty0 - 64,
            ';--- SPICE directives carried through by net2asc.py (v2b spine '
            'layout): spine + branches wired, leftovers on labels ---')
    _text_columns(sh, body, x0, ty0)

    lines, sheet = sh.emit()
    info = {
        'drawn': [(s['inst'], s['sym']) for s in sh.syms],
        'text_fallback': [e.name for e in text_fallback],
        'text_fallback_raw': [e.raw for e in text_fallback],
        'n_wire': len(sh.wires), 'n_flag': len(sh.flags),
        'n_symbol': len(sh.syms), 'n_text': len(sh.texts),
        'sheet': sheet, 'layout': 'spine',
        'dropped_control': len(deck.dropped_control),
        'geometric_check': 'PASS',
    }
    info.update(linfo)
    return lines, info


def _directive_text(deck, text_fallback):
    body = []
    if deck.title:
        body.append(';%s' % deck.title.replace('\n', ' '))
    for d in deck.directives:
        body.append('!%s' % _to_braces(d) if d.lower().startswith('.param')
                    else '!%s' % d)
    for k in deck.couplings:
        body.append('!%s' % k)
    for e in text_fallback:
        body.append('!%s' % _strip_inline_comment(e.raw))
    if deck.dropped_control:
        body.append(';.control ... .endc block dropped (%d lines): LTspice has '
                    'no equivalent; re-add it in the ngspice deck.'
                    % len(deck.dropped_control))
    und = undefined_params(deck)
    if und:
        body.append(';=== UNDEFINED PARAMETERS -- THIS SCHEMATIC WILL NOT RUN '
                    'AS-IS ===')
        body.append(';The source netlist uses %d {PLACEHOLDER}s that no .param '
                    'card defines' % len(und))
        body.append(';(a runner script substitutes them before ngspice sees the '
                    'deck).  LTspice has')
        body.append(';no such step and will report "Unknown parameter".  '
                    'net2asc.py does NOT invent')
        body.append(';values.  Supply your own, then UNCOMMENT the matching '
                    'line below by')
        body.append(';deleting its leading ";" so the record becomes a "!" '
                    'SPICE directive:')
        for n in und:
            body.append(';!.param %s=<SUPPLY A VALUE>' % n)
        body.append(';=== end of undefined-parameter note ===')
    return body


def _text_columns(sh, body, x0, ty0):
    cx = x0
    i = 0
    while i < len(body):
        col = body[i:i + TEXT_COL_ROWS]
        for j, ln in enumerate(col):
            sh.text(cx, ty0 + j * TEXT_DY, ln)
        wide = max(len(ln) for ln in col)
        cx += int(wide * 15) + 96
        cx += (-cx) % GRID
        i += TEXT_COL_ROWS


def undefined_params(deck):
    """`{NAME}` placeholders used by an element/directive but never defined.

    A runner script substitutes these before ngspice sees the deck; LTspice has
    no such step and would error out.  We do not invent values -- the caller
    emits a commented .param template instead."""
    defined = set()
    for d in deck.directives:
        for m in re.finditer(r'\.param\s+(.*)$', d, re.I):
            for mm in re.finditer(r'([A-Za-z_][A-Za-z0-9_]*)\s*=', m.group(1)):
                defined.add(mm.group(1).lower())
    used = OrderedDict()
    src = [e.raw for e in deck.elements] + list(deck.directives) + list(deck.couplings)
    for s in src:
        for m in re.finditer(r'\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}', s):
            if m.group(1).lower() not in defined:
                used.setdefault(m.group(1), None)
    return list(used)


def geometric_check(sh):
    """LTspice-semantics contact analysis over what we just emitted.

    Unions: wire endpoints; a wire endpoint lying on another wire's segment
    (a T junction -- LTspice honours these, asc2ngspice.py does NOT, so this
    check is strictly stronger there); a symbol pin or a FLAG lying on a wire.
    Every resulting component must carry exactly one DESIGNED net name."""
    parent = {}

    def find(a):
        parent.setdefault(a, a)
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        parent.setdefault(a, a); parent.setdefault(b, b)
        parent[find(a)] = find(b)

    def on_seg(p, a, b):
        if a[0] == b[0] == p[0] and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]):
            return True
        if a[1] == b[1] == p[1] and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]):
            return True
        return False

    segs = [(p, q) for p, q, _ in sh.wires]
    for p, q in segs:
        union(p, q)
    pts = set()
    for p, q in segs:
        pts.add(p); pts.add(q)
    for _, _, c, _ in sh.pinpts:
        pts.add(c)
    for c, _ in sh.flags:
        pts.add(c)
    for c in pts:
        for a, b in segs:
            if on_seg(c, a, b):
                union(c, a)

    claim = {}
    problems = []

    def claim_net(c, net, who):
        if net is None:
            return
        r = find(c)
        if r in claim and claim[r][0] != net:
            problems.append('ACCIDENTAL CONTACT: %s (net %r) touches %s (net %r)'
                            % (who, net, claim[r][1], claim[r][0]))
        else:
            claim[r] = (net, who)

    for p, q, net in sh.wires:
        claim_net(p, net, 'wire %s-%s' % (p, q))
        claim_net(q, net, 'wire %s-%s' % (p, q))
    for inst, k, c, net in sh.pinpts:
        claim_net(c, net, '%s.pin%d' % (inst, k + 1))
    for c, nm in sh.flags:
        claim_net(c, nm, 'FLAG %s@%s' % (nm, c))
    return (len(problems) == 0), problems


def build_asc_flow(deck, pins, mosmap, cirpath=None):
    sh, text_fallback, linfo = flow_build(deck, pins, mosmap, cirpath)

    ok, problems = geometric_check(sh)
    if not ok:
        raise LayoutError('geometric self-check failed:\n  ' + '\n  '.join(problems))

    x0, y0, x1, y1 = sh.bbox()
    body = _directive_text(deck, text_fallback)

    # The directive block is reference material, not the drawing.  v1 stacked
    # it in ONE column, which made it three times taller than the schematic and
    # shrank the circuit to nothing on screen.  Break it into columns instead.
    ty0 = y1 + AUX_GAP
    sh.text(x0, ty0 - 64,
            ';--- SPICE directives carried through by net2asc.py (v2 flow '
            'layout): power path wired, auxiliary nets on labels ---')
    _text_columns(sh, body, x0, ty0)

    lines, sheet = sh.emit()
    info = {
        'drawn': [(s['inst'], s['sym']) for s in sh.syms],
        'text_fallback': [e.name for e in text_fallback],
        'text_fallback_raw': [e.raw for e in text_fallback],
        'n_wire': len(sh.wires), 'n_flag': len(sh.flags),
        'n_symbol': len(sh.syms), 'n_text': len(sh.texts),
        'sheet': sheet, 'layout': 'flow',
        'dropped_control': len(deck.dropped_control),
        'geometric_check': 'PASS',
        # measured and REPORTED for the flow layout, never enforced: flow's
        # placement is not speculative, so there is nothing to roll back to.
        'text_overlaps': (refresh_flag_boxes(sh), count_all_text_clashes(sh))[1],
    }
    info.update(linfo)
    return lines, info


def write_asc(path, lines):
    """UTF-16LE, NO BOM, LF line endings, first line exactly 'Version 4'."""
    assert lines[0] == 'Version 4'
    txt = '\n'.join(lines) + '\n'
    d = os.path.dirname(os.path.abspath(path))
    if d and not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)
    with open(path, 'wb') as f:
        f.write(txt.encode('utf-16-le'))     # .encode() adds no BOM
    return len(txt.encode('utf-16-le'))


def check_encoding(path):
    """Independent re-read: UTF-16LE / no BOM / LF only / 'Version 4' first."""
    raw = open(path, 'rb').read()
    res = OrderedDict()
    res['no_bom'] = not (raw[:2] in (b'\xff\xfe', b'\xfe\xff'))
    try:
        txt = raw.decode('utf-16-le')
        res['utf16le_decodes'] = True
    except Exception:
        res['utf16le_decodes'] = False
        txt = ''
    res['lf_only'] = ('\r' not in txt)
    res['first_line_Version_4'] = txt.split('\n')[0] == 'Version 4'
    res['second_line_SHEET'] = txt.split('\n')[1].startswith('SHEET ') if txt.count('\n') else False
    # grid check
    off = []
    for ln in txt.split('\n'):
        t = ln.split()
        if not t:
            continue
        if t[0] == 'WIRE':
            nums = [int(v) for v in t[1:5]]
        elif t[0] == 'FLAG':
            nums = [int(t[1]), int(t[2])]
        elif t[0] == 'SYMBOL':
            nums = [int(t[2]), int(t[3])]
        else:
            continue
        if any(v % GRID for v in nums):
            off.append(ln)
    res['all_coords_on_16_grid'] = (len(off) == 0)
    res['off_grid_lines'] = off[:5]
    res['ok'] = all(v for k, v in res.items()
                    if k not in ('off_grid_lines',) and isinstance(v, bool))
    return res


# ===========================================================================
# 3. topology extraction + round-trip comparison
# ===========================================================================

# values the netlister INVENTS when a symbol carries no SYMATTR Value at all
# (asc2ngspice.emit_devices: `model = val if val else 'D'` etc).  Comparing a
# blank input value against one of these is not a real discrepancy, so it is
# reported as a NOTE instead of a MISMATCH.  This is the ONE value-comparison
# exclusion; everything else is compared.
_INVENTED_DEFAULTS = {'D', 'SW', 'NMOS', 'PMOS'}

_SQUOTE = re.compile(r"'([^']*)'")


def normalise_value(value, params=''):
    """Canonical form of an element's value string for round-trip comparison.

    The round trip is not byte-preserving, so a naive string compare would
    produce false failures.  Exactly these normalisations are applied, and
    nothing else:

      1. value and X-call instance parameters are concatenated (parse_cir
         splits them; asc2ngspice re-emits them as one tail);
      2. runs of whitespace collapse to a single space, and the string is
         stripped -- decks in this repo column-align their cards
         (`D1      0     N1   DRBE01VYM6A`);
      3. whitespace around '=' is removed (`Rser = 6.24m` == `Rser=6.24m`),
         because SpiceLine attributes are re-quoted by the .asc round trip;
      4. ngspice's `'expr'` expression quoting is rewritten to LTspice's
         `{expr}` -- the same rewrite _to_braces() already performs on .param
         cards, and the two spellings mean the same thing to ngspice.

    NOT applied: no case folding (a model name is not a node name), no numeric
    re-formatting (`1e9` is NOT made equal to `1G`), no unit stripping."""
    s = '%s %s' % (value or '', params or '')
    s = _SQUOTE.sub(r'{\1}', s)
    s = re.sub(r'\s*=\s*', '=', s)
    return ' '.join(s.split())


def k_parts(card):
    """`K1 L_conv L_ant {K_VALUE}` -> ('K1', ('L_CONV','L_ANT'), '{K_VALUE}').

    2026-09-04 audit, hole B2.  This used to be written inline in topology() as
    `kmap[t[0]] = t[1:-1]`, i.e. the coupling COEFFICIENT -- the last token --
    was deliberately thrown away and only the coupled partners were compared.
    Changing `{K_VALUE}` to `0.001` in a generated .asc therefore gave
    `VERIFY: PASS`, exit 0, while the schematic modelled an all-but-uncoupled
    transformer.  The coefficient is an element value in every sense that
    matters, so it is now compared like one (through normalise_value()).

    A braced coefficient may legally contain spaces (`{k * 2}`), so when a '{'
    is present everything from it on is the coefficient; otherwise the last
    token is, which is exactly the old partner split (no partner regression)."""
    t = card.split()
    if not t:
        return '', (), ''
    i = card.find('{')
    if i >= 0:
        head = card[:i].split()
        return t[0], tuple(x.upper() for x in head[1:]), card[i:].strip()
    if len(t) >= 4:
        return t[0], tuple(x.upper() for x in t[1:-1]), t[-1]
    return t[0], tuple(x.upper() for x in t[1:]), ''


def topology(path):
    """name -> (letter, tuple(nets), normalised value).  Plus K couplings.

    The K map is name -> (partners, normalised coefficient); both halves are
    compared by compare_topology()."""
    deck = parse_cir(path)
    topo = OrderedDict()
    dup = []
    for e in deck.elements:
        key = e.name.upper()
        if key in topo:
            dup.append(e.name)
        topo[key] = (e.letter, tuple(e.nodes), normalise_value(e.value, e.params))
    # directives may carry element cards too?  no: parse_cir already split them.
    kmap = OrderedDict()
    for k in deck.couplings:
        name, partners, coeff = k_parts(k)
        kmap[name.upper()] = (partners, normalise_value(coeff))
    return topo, kmap, dup


def compare_topology(topo_a, topo_b, kmap_a=None, kmap_b=None):
    """Graph/partition isomorphism keyed by element name.

    Element names are preserved by the round trip, so we require:
      * identical element-name sets, identical type letter, identical arity
      * a BIJECTION f : nets(A) -> nets(B) with f(net of A.pin_i) == net of
        B.pin_i for every element and every terminal index i.
      * identical element VALUES after normalise_value() (2026-08-27 audit
        fix: until then the round trip compared only wiring, so
        audit_fable/corrupt_C_value.asc -- L1 changed from {L} to a 1 GH
        inductor -- passed).
    Returns (ok, list_of_message_strings, netmap).  Value differences that are
    only 'input said nothing, the netlister invented a default model name' are
    appended to `notes`, not to the failure list."""
    msgs = []
    notes = []
    na, nb = set(topo_a), set(topo_b)
    missing = sorted(na - nb)
    extra = sorted(nb - na)
    if missing:
        msgs.append('elements MISSING from round-trip deck (%d): %s'
                    % (len(missing), ', '.join(missing)))
    if extra:
        msgs.append('elements EXTRA in round-trip deck (%d): %s'
                    % (len(extra), ', '.join(extra)))
    fwd, rev = {}, {}
    # ground must map to ground
    fwd['0'] = '0'
    rev['0'] = '0'
    for name in sorted(na & nb):
        la, va, xa = topo_a[name]
        lb, vb, xb = topo_b[name]
        if la != lb:
            msgs.append('%s: type letter %s -> %s' % (name, la, lb))
            continue
        if xa != xb:
            if not xa and xb in _INVENTED_DEFAULTS:
                notes.append('%s: input card carries no value; the round trip '
                             'shows the netlister\'s invented default %r '
                             '(not compared)' % (name, xb))
            else:
                msgs.append('%s: VALUE %r -> %r' % (name, xa, xb))
        if len(va) != len(vb):
            msgs.append('%s: terminal count %d -> %d  (%s vs %s)'
                        % (name, len(va), len(vb), list(va), list(vb)))
            continue
        for i, (a, b) in enumerate(zip(va, vb)):
            if a in fwd and fwd[a] != b:
                msgs.append('%s.pin%d: net %r already mapped to %r but here it is %r'
                            % (name, i + 1, a, fwd[a], b))
            elif b in rev and rev[b] != a:
                msgs.append('%s.pin%d: round-trip net %r already claimed by %r, '
                            'here it comes from %r' % (name, i + 1, b, rev[b], a))
            else:
                fwd[a] = b
                rev[b] = a
    if kmap_a is not None and kmap_b is not None:
        ka, kb = set(kmap_a), set(kmap_b)
        if ka != kb:
            msgs.append('K statements differ: only-in-input=%s only-in-rt=%s'
                        % (sorted(ka - kb), sorted(kb - ka)))
        for k in sorted(ka & kb):
            pa, ca = kmap_a[k]
            pb, cb = kmap_b[k]
            if pa != pb:
                msgs.append('K %s couples %s -> %s' % (k, list(pa), list(pb)))
            if ca != cb:
                # 2026-09-04 audit hole B2: the coefficient was not compared at
                # all, so `{K_VALUE}` -> `0.001` passed.
                msgs.append('K %s COUPLING COEFFICIENT %r -> %r' % (k, ca, cb))
    return (len(msgs) == 0), msgs, fwd, notes


# ===========================================================================
# 4. driver
# ===========================================================================

def convert(cirpath, ascpath, libdir=DEFAULT_LIBDIR, stub=STUB_DEFAULT,
            cols=None, verify=True, rtpath=None, keep_rt=False, quiet=False,
            layout='auto'):
    asymsgs = []
    pins = load_asy(libdir, asymsgs)
    for need in ('res', 'cap', 'ind', 'ind2', 'diode', 'voltage', 'sw', 'nmos'):
        if not pins.get(need):
            raise SystemExit('FATAL: no PIN data for symbol %r in %s' % (need, libdir))
    for m in asymsgs:
        print(m)

    deck = parse_cir(cirpath)
    for keep, spellings in deck.net_case_merges.items():
        print('NOTE: net-name spellings %s are ONE node in ngspice '
              '(node names are case-insensitive); drawing them as a single '
              'net labelled %r (the first spelling in the deck)'
              % (spellings, keep))
    bad = sanitise_netnames(deck)
    if bad:
        print('WARNING: net names contain characters LTspice/asc2ngspice will '
              'rewrite; connectivity may be reported as mismatched: %s' % bad)

    mosnames = find_mosfet_subckts(cirpath, deck)
    mosmap = mosfet_map(deck, mosnames)

    lines = info = None
    if layout in ('auto', 'flow'):
        try:
            lines, info = build_asc_flow(deck, pins, mosmap, cirpath)
        except LayoutError as ex:
            if layout == 'flow':
                raise SystemExit('FATAL: --layout flow failed: %s' % ex)
            if not quiet:
                print('  note: v2 flow (half-bridge) layout not applicable '
                      '(%s); trying the v2b spine layout.'
                      % str(ex).split('\n')[0])
    if lines is None and layout in ('auto', 'spine'):
        try:
            lines, info = build_asc_spine(deck, pins, mosmap, cirpath)
        except LayoutError as ex:
            if layout == 'spine':
                raise SystemExit('FATAL: --layout spine failed: %s' % ex)
            if not quiet:
                print('  note: v2b spine layout not applicable (%s); '
                      'falling back to the v1 grid.' % str(ex).split('\n')[0])
    if lines is None:
        lines, info = build_asc(deck, pins, stub=stub, cols=cols, mosmap=mosmap)
        info['layout'] = 'grid'
    nbytes = write_asc(ascpath, lines)
    enc = check_encoding(ascpath)

    if not quiet:
        print('%s -> %s  (%d bytes utf-16-le)' % (cirpath, ascpath, nbytes))
        if info['layout'] == 'grid':
            print('  layout : v1 GRID -- %d symbols in %dx%d cells '
                  '(pitch %dx%d, stub %d)'
                  % (info['n_symbol'], info['rows'], info['cols'],
                     CELL_W, CELL_H, stub))
        elif info['layout'] == 'spine':
            print('  layout : v2b SPINE -- %d symbols, %d series chains '
                  '(%d on labels)' % (info['n_symbol'], info['chains'],
                                      info['aux_chains']))
            if info.get('bridge'):
                b = info['bridge']
                print('  BRIDGE TEMPLATE: fired -- rail %s, return %s, '
                      'midpoints %s / %s' % (b['rail'], b['ret'],
                                             b['mid1'], b['mid2']))
                print('    switches (left leg hi/lo, right leg hi/lo): %s'
                      % ', '.join(b['switches']))
                print('    primary between the midpoints: %s   (K-coupled: %s)'
                      % (', '.join(b['primary']), ', '.join(b['coils'])))
            elif info.get('bridge_note'):
                print('  bridge template: NOT fired -- %s' % info['bridge_note'])
            for k, (snets, selems) in enumerate(info['islands']):
                lbl = 'bridge' if (k == 0 and info.get('bridge')) else 'spine '
                print('  %s %d: %s' % (lbl, k + 1, ' - '.join(snets)))
                print('           elements left to right: %s'
                      % ', '.join(selems))
            if info.get('pack'):
                print('  islands packed on shelves: %s'
                      % ', '.join('#%d %dx%d' % (g + 1, w, h)
                                  for (g, w, h) in info['pack']))
            print('  text overlaps (estimated extents): %d left in the drawing, '
                  '%d placement(s) accepted with one'
                  % (info['text_overlaps'], info['text_relaxed']))
            if info['rails']:
                print('  rails hung off the spine: %s' % ', '.join(info['rails']))
            if info['coupled_loops']:
                print('  K-coupled loops placed beside their partner: %s'
                      % ', '.join(str(x) for x in info['coupled_loops']))
            print('  geometric self-check (LTspice contact semantics): %s'
                  % info['geometric_check'])
        else:
            print('  layout : v2 FLOW -- %d symbols, %d series chains '
                  '(%d on labels), leg %s/%s/%s, top rail from %s'
                  % (info['n_symbol'], info['chains'], info['aux_chains'],
                     info['leg'][0], info['leg'][1], info['leg'][2],
                     info['ntop']))
            print('  text overlaps (estimated extents, reported only): %d'
                  % info.get('text_overlaps', 0))
            print('  geometric self-check (LTspice contact semantics): %s'
                  % info['geometric_check'])
        if mosmap:
            print('  MOSFET subckt calls drawn with the nmos symbol '
                  '(PIN order D,G,S): %s' % ', '.join(sorted(mosmap)))
        print('  records: WIRE=%d FLAG=%d SYMBOL=%d TEXT=%d  SHEET %d %d'
              % (info['n_wire'], info['n_flag'], info['n_symbol'], info['n_text'],
                 info['sheet'][0], info['sheet'][1]))
        if info['text_fallback']:
            print('  TEXT-directive fallback (%d elements, NOT drawn): %s'
                  % (len(info['text_fallback']), ', '.join(info['text_fallback'])))
        if info['dropped_control']:
            print('  dropped .control block (%d lines)' % info['dropped_control'])
        und = undefined_params(deck)
        if und:
            # 2026-09-04 (audit D1): this used to exist ONLY as a TEXT block
            # inside the generated .asc, so an agent reading stdout never saw
            # it and reported a schematic that LTspice refuses to open.
            print('  undefined params: %s (LTspice will NOT open this as-is; '
                  'the .asc carries a commented .param template -- supply values '
                  'and delete the leading ";")' % ', '.join(und))
        print('  encoding: ' + ' '.join('%s=%s' % (k, v) for k, v in enc.items()
                                        if k != 'off_grid_lines'))

    ok = True
    if verify:
        rtpath = rtpath or (os.path.splitext(ascpath)[0] + '_rt.cir')
        a2nmsgs = []
        deckstr = _A2N.emit(ascpath, libdir, messages=a2nmsgs)
        with open(rtpath, 'w', encoding='utf-8') as f:
            f.write(deckstr)
        ta, ka, dupa = topology(cirpath)
        tb, kb, dupb = topology(rtpath)
        ok, msgs, fwd, notes = compare_topology(ta, tb, ka, kb)
        cok, cmsgs = asc_contact_check(ascpath, cirpath, libdir)
        rok, rmsgs = directive_ref_check(rtpath, cirpath)
        sok, smsgs = directive_set_check(ascpath, cirpath, libdir, rtpath)
        eerr = _extractor_errors(a2nmsgs)
        # a2nmsgs also repeats whatever load_asy() said; those were printed at
        # the top of convert() already, so only the new ones are shown here.
        cmsgs = (_dup_msgs(dupa, dupb) + cmsgs + rmsgs + smsgs
                 + [m for m in a2nmsgs if m not in asymsgs])
        ok = (ok and cok and rok and sok and not eerr
              and not dupa and not dupb)
        if not quiet:
            print('  round trip: %s -> %s (re-extractor: asc2ngspice.py)'
                  % (os.path.basename(ascpath), os.path.basename(rtpath)))
            print('  compared %d input elements vs %d round-trip elements, '
                  '%d nets mapped' % (len(ta), len(tb), len(fwd)))
            print('  VERIFY: %s' % ('PASS' if ok else 'FAIL'))
            for m in cmsgs:
                print('    %s' % m)
            for m in msgs:
                print('    MISMATCH: %s' % m)
            for m in notes:
                print('    NOTE: %s' % m)
        if not keep_rt and ok:
            pass  # keep it anyway: it is evidence
    return ok, info


def _dup_msgs(dupa, dupb):
    """Duplicate element names are a FAILURE, not a note (changed 2026-08-27).

    Until the audit these produced only 'NOTE: duplicate element names ...'
    and exit 0.  Two reasons that was wrong:
      * ngspice refuses such a deck outright -- `ngspice -b` on a deck with two
        R1 cards prints 'device already exists, bail out' and runs nothing, so
        the input is not a netlist anybody can simulate;
      * topology() keys elements by name, so the second card OVERWRITES the
        first and one element silently drops out of the comparison.  A NOTE
        next to 'VERIFY: PASS' therefore claimed coverage that did not exist.
    No deck in this repo has duplicates, so this is strictly stronger."""
    out = []
    if dupa:
        out.append('DUPLICATE: element names repeated in input deck: %s -- ngspice would '
                   'reject this deck, and the comparison can only see one card '
                   'per name' % ', '.join(sorted(set(dupa))))
    if dupb:
        out.append('DUPLICATE: element names repeated in round-trip deck: %s'
                   % ', '.join(sorted(set(dupb))))
    return out


def asc_contact_check(ascpath, cirpath, libdir=DEFAULT_LIBDIR):
    """Direct LTspice-contact-semantics check ON THE .asc GEOMETRY.

    Added 2026-08-27.  The round trip alone used to be the whole of --check,
    and it inherited every blind spot of the netlister that produced the
    round-trip deck.  This runs the contact analysis over the .asc itself and
    fails when one connected component carries two different net labels --
    the fingerprint of a mid-wire FLAG or a T junction that shorted two nets
    (audit_fable/corrupt_A_midflag.asc, corrupt_B_tjunction.asc).

    An alias group whose names are two DISTINCT nets of the input deck is a
    SHORT and fails.  An alias group involving a label the input deck never
    uses is only a NOTE: it cannot change the input's topology, and refusing
    it would be inventing a rule the deck never stated.

    Returns (ok, messages)."""
    groups = _A2N.contact_report(ascpath, libdir)
    if not groups:
        return True, []
    deck = parse_cir(cirpath)
    nets = set()
    for e in deck.elements:
        for n in e.nodes:
            nets.add(n.lower())
    ok = True
    msgs = []
    for grp in groups:
        real = sorted({n for n in grp if n.lower() in nets},
                      key=lambda s: s.lower())
        if len(real) > 1:
            ok = False
            msgs.append('SHORT: nets %s are ONE connected component in the '
                        '.asc but are distinct nets in %s'
                        % (', '.join(repr(n) for n in real),
                           os.path.basename(cirpath)))
        else:
            msgs.append('NOTE: one component carries several labels %s; only '
                        '%s names a net of the input deck, so the topology is '
                        'unchanged'
                        % (', '.join(repr(n) for n in grp),
                           repr(real[0]) if real else 'no label'))
    return ok, msgs


_IREF = re.compile(r'\bi\s*\(\s*([A-Za-z0-9_#]+)\s*\)', re.I)
_ATREF = re.compile(r'@\s*([A-Za-z0-9_]+)\s*\[')


def _name_refs(deck):
    """(node names, element names) referenced BY NAME inside a deck's cards.

    Sources are every element card's raw text (this is where a TEXT-fallback
    B/E/G/F/H source lives once it has been carried through a .asc), every
    directive and every K statement.  Returns two dicts ref -> example card."""
    nodes, elems = OrderedDict(), OrderedDict()
    for src in ([e.raw for e in deck.elements] + list(deck.directives)
                + list(deck.couplings)):
        for m in _VREF.finditer(src):
            for g in (m.group(1), m.group(2)):
                if g:
                    nodes.setdefault(g.lower(), (g, src))
        for m in _IREF.finditer(src):
            elems.setdefault(m.group(1).lower(), (m.group(1), src))
        for m in _ATREF.finditer(src):
            elems.setdefault(m.group(1).lower(), (m.group(1), src))
    return nodes, elems


def _dangling(deck):
    """refs of _name_refs() that name nothing this deck actually defines."""
    have_n = {'0'}
    have_e = set()
    for e in deck.elements:
        have_e.add(e.name.lower())
        for n in e.nodes:
            have_n.add(n.lower())
    nrefs, erefs = _name_refs(deck)
    dn = OrderedDict((k, v) for k, v in nrefs.items() if k not in have_n)
    de = OrderedDict((k, v) for k, v in erefs.items() if k not in have_e)
    return dn, de


def directive_ref_check(rtpath, cirpath):
    """Cross-check names used INSIDE cards against the nets the drawing has.

    Added 2026-09-04 (audit hole A1).  The round-trip comparison is a
    BIJECTION on net names, so a *consistent* rename of a net is -- correctly
    -- not a mismatch.  But a schematic is not only its geometry: elements
    without a symbol (B/E/G/F/H sources) are carried as TEXT '!' directives and
    they name their nets **as literal text**, e.g.

        Bihs nihs 0 V = ((v(ghd)-v(sw)) > {VGMID}) ? i(vlsense) : 0

    Renaming the FLAGs of net `sw` to `swzz` on BOTH of its flags therefore
    left a perfectly bijective drawing whose TEXT card still asks for v(sw) --
    a node that no longer exists.  ngspice would create a fresh floating node
    and the monitor would read 0.  --check said PASS, exit 0.

    So: every `v(node)` / `i(element)` / `@element[..]` reference appearing in
    a card of the ROUND-TRIP deck must resolve against that same deck.  A
    reference that is dangling in the round trip but resolved in the INPUT deck
    is a FAILURE -- the conversion (or the hand-edit) broke it.  A reference
    dangling in BOTH is a pre-existing property of the user's own netlist and
    is reported as a NOTE, because refusing it would be this tool inventing a
    rule about a deck it was only asked to draw.

    Returns (ok, messages)."""
    rt = parse_cir(rtpath)
    src = parse_cir(cirpath)
    rt_n, rt_e = _dangling(rt)
    src_n, src_e = _dangling(src)
    ok = True
    msgs = []
    for key, (name, card) in rt_n.items():
        if key in src_n:
            msgs.append('NOTE: v(%s) is referenced by a card but no element of '
                        'the INPUT deck connects to a net of that name either; '
                        'pre-existing in %s, not introduced by the drawing'
                        % (name, os.path.basename(cirpath)))
            continue
        ok = False
        msgs.append('DANGLING NET REFERENCE: a card carried into the .asc names '
                    'net %r by text, but no net of that name exists in the '
                    'drawing (it does exist in %s).  The card is: %s'
                    % (name, os.path.basename(cirpath), card.strip()))
    for key, (name, card) in rt_e.items():
        if key in src_e:
            msgs.append('NOTE: i(%s)/@%s[..] names an element the INPUT deck '
                        'does not define either; pre-existing in %s'
                        % (name, name, os.path.basename(cirpath)))
            continue
        ok = False
        msgs.append('DANGLING ELEMENT REFERENCE: a card carried into the .asc '
                    'names element %r by text, but the drawing contains no such '
                    'element (the input deck does).  The card is: %s'
                    % (name, card.strip()))
    return ok, msgs


_DIR_HEAD = re.compile(r'^(\.\w+)(.*)$', re.S)


def _dir_key(card):
    """Comparison key for one directive card.

    The body goes through normalise_value() -- the same normalisation element
    values get -- and the leading `.keyword` is additionally folded to lower
    case.  SPICE directive keywords ARE case-insensitive (`.TRAN` and `.tran`
    are the same card, and asc2ngspice.py re-emits `.tran` in lower case after
    translating it), so not folding them would report a difference that does
    not exist.  Nothing else is folded: a model name is not a keyword."""
    m = _DIR_HEAD.match(card.strip())
    if not m:
        return normalise_value(card)
    return normalise_value(m.group(1).lower() + m.group(2))


_A2N_STAMP = re.compile(r'^\*.*generated by asc2ngspice\.py', re.I)


def deck_is_a2n_generated(cirpath):
    """True when this .cir is itself an asc2ngspice.py output.

    Added 2026-09-05 (audit_fable4).  asc2ngspice.py writes a provenance line
    into the deck header -- `* generated by asc2ngspice.py from <path>` -- and
    that line is the only reliable marker: the rewrites it performs (see
    directive_set_check) leave no trace in the cards themselves.  Only the
    leading comment block is scanned; a `*` line further down is deck body,
    not a header stamp."""
    try:
        with open(cirpath, encoding='utf-8', errors='replace') as f:
            for ln in f:
                t = ln.strip()
                if not t:
                    continue
                if not t.startswith('*'):
                    return False        # past the header comment block
                if _A2N_STAMP.match(t):
                    return True
    except OSError:
        return False
    return False


def directive_set_check(ascpath, cirpath, libdir=DEFAULT_LIBDIR, rtpath=None):
    """Every SPICE directive of the input deck must still be in the .asc.

    Added 2026-09-04 (audit hole B3).  Until then the *presence* of a
    directive was never compared against the input deck: deleting the `.tran`
    card, or an `.ic v(mid)=2`, from a generated .asc gave `VERIFY: PASS`,
    exit 0.  The documented exclusion was "the CONTENTS of
    `.model`/`.param`/`.options` are not compared"; in practice the tool
    behaved as if it read "directives are not compared at all", which is a far
    bigger hole -- a deck that lost its `.tran` card does not run, and a deck
    that lost its `.ic` starts from a different state.

    WHAT IS COMPARED HERE, AND WHY THAT SPLIT
      * every `.xxx` card, BY CONTENT, through normalise_value() -- the same
        normalisation element values get.  net2asc.py copies directives into
        the .asc verbatim; the ONLY rewrite is `_to_braces()` on `.param`, and
        normalise_value() performs exactly that `'expr'`->`{expr}` rewrite on
        both sides, so the comparison here is exact rather than approximate.
        Measured on the five reference decks (37 / 39 / 42 / 46 / 3 cards):
        multiset-equal.  This means `.model` / `.param` / `.options` CONTENTS
        are compared on THIS path.  The round-trip *deck* still cannot compare
        them -- asc2ngspice.py re-orders `.param` topologically and injects
        `.options` convergence aids -- which is why the old exclusion existed
        and why the check had to be made against the .asc, not the rt deck.
      * `K` cards are deliberately NOT compared here.  They are not dot cards,
        and compare_topology() already compares both their partners and (since
        2026-09-04) their coupling coefficient.  Comparing them twice would
        only produce two messages for one fault.
      * element cards with no symbol (`B`/`E`/`G`/`F`/`H`) that ride in the
        .asc as `!` TEXT are NOT compared here: topology() compares them as
        elements, values included, and already fails on deletion or edit.
      * `;` TEXT records -- the title, the notes, the commented-out `.param`
        template printed for undefined parameters -- are not directives and
        have no effect on a simulation, so they are not compared.


    WHEN THE INPUT DECK IS ITSELF AN asc2ngspice.py OUTPUT (2026-09-05,
    audit_fable4 false-FAIL)
      Everything above assumes the input deck is the hand-written source and
      the .asc is the drawing net2asc.py made from it -- the direction in
      which directives are copied VERBATIM, so an exact multiset comparison is
      right.  Checking an .asc against a deck asc2ngspice.py produced FROM that
      .asc is the other direction, and there they are not verbatim: emit()
      splits `.param a=1 b=2` into one card per assignment, transliterates the
      Greek eta to `eta`, rewrites `.tran ... startup` to `.tran ... uic`,
      injects `.param pi=...` and injects `.options` convergence aids.
      Measured on the three t_cl decks that produced 30 false messages on
      drawings whose topology compared clean (52 elements, 32 nets, no
      mismatch) -- a FAIL a reader would take to mean the drawing was wrong.
      In that direction the two sides are made comparable by putting BOTH
      through the same translator: the round-trip deck (already written by the
      caller) against the input deck, dot cards, multiset, same key.  The
      rewrites then apply to both sides and cancel; ordering does not matter to
      a multiset; and the check keeps its teeth -- a directive deleted from or
      added to the .asc still moves only one side of the comparison.  A deck
      generated by a DIFFERENT asc2ngspice.py version (a different aid set,
      say) legitimately reports a difference: the two decks then really do
      describe different simulations.
      This path is taken ONLY when the deck carries asc2ngspice.py's provenance
      stamp AND a round-trip deck is available; the verbatim comparison above
      is untouched for every hand-written input deck.

    Comparison is on a MULTISET, so deleting one of two identical cards is
    caught.  Both directions fail: a card missing from the .asc is a deletion,
    a card the input deck never had is an addition.  Returns (ok, messages)."""
    src = [d for d in parse_cir(cirpath).directives if d.startswith('.')]
    if rtpath and os.path.exists(rtpath) and deck_is_a2n_generated(cirpath):
        # both sides through the same translator -- see the docstring
        asc = [d for d in parse_cir(rtpath).directives if d.startswith('.')]
    else:
        asc = [d for d in _A2N.directive_report(ascpath, libdir)
               if d.startswith('.')]
    shown = {}
    for d in src + asc:
        shown.setdefault(_dir_key(d), d.strip())
    ca = Counter(_dir_key(d) for d in src)
    cb = Counter(_dir_key(d) for d in asc)
    msgs = []
    for key in sorted(ca - cb):
        n = (ca - cb)[key]
        msgs.append('DIRECTIVE MISSING FROM .asc (%d card(s)): %s -- the input '
                    'deck %s carries it; the drawing does not, so the '
                    'simulation the .asc describes is not the one the netlist '
                    'describes'
                    % (n, shown[key], os.path.basename(cirpath)))
    for key in sorted(cb - ca):
        n = (cb - ca)[key]
        msgs.append('DIRECTIVE ADDED TO .asc (%d card(s)): %s -- no such card '
                    'is in the input deck %s'
                    % (n, shown[key], os.path.basename(cirpath)))
    return (not msgs), msgs


def _extractor_errors(msgs):
    """Messages asc2ngspice.py raised that make its extraction untrustworthy.

    An `ERROR:` from the extractor means it met something in the .asc it could
    not carry into the netlist (an unknown `SYMATTR`, for instance).  The
    round-trip comparison downstream would then be comparing a deck that is
    silently missing part of the schematic, so `--check` must fail rather than
    report a PASS it cannot support (2026-09-04, hole B1)."""
    return [m for m in msgs if m.startswith('ERROR:')]


def check_only(cirpath, ascpath, libdir=DEFAULT_LIBDIR, rtpath=None,
               quiet=False):
    """Re-verify an EXISTING .asc against the netlist it should represent.

    Independent checks, ALL must pass:
      1. LTspice contact semantics run directly on the .asc geometry
         (asc_contact_check);
      2. the round trip .asc -> .cir -> topology comparison, values and K
         coupling coefficients included;
      3. names used inside cards (v(net), i(elem), @elem[..]) must still
         resolve in the drawing (directive_ref_check, 2026-09-04);
      4. the SET of SPICE directives carried into the .asc must equal the
         input deck's (directive_set_check, 2026-09-04);
      5. the extractor must not have met anything it could not carry into the
         netlist (_extractor_errors, 2026-09-04).
    Returns True on PASS."""
    rtpath = rtpath or (os.path.splitext(ascpath)[0] + '_rt.cir')
    asymsgs = []
    deckstr = _A2N.emit(ascpath, libdir, messages=asymsgs)
    with open(rtpath, 'w', encoding='utf-8') as f:
        f.write(deckstr)
    ta, ka, dupa = topology(cirpath)
    tb, kb, dupb = topology(rtpath)
    ok, msgs, fwd, notes = compare_topology(ta, tb, ka, kb)
    cok, cmsgs = asc_contact_check(ascpath, cirpath, libdir)
    rok, rmsgs = directive_ref_check(rtpath, cirpath)
    sok, smsgs = directive_set_check(ascpath, cirpath, libdir, rtpath)
    eerr = _extractor_errors(asymsgs)   # already printed above, out of asymsgs
    cmsgs = _dup_msgs(dupa, dupb) + cmsgs + rmsgs + smsgs
    ok = (ok and cok and rok and sok and not eerr
          and not dupa and not dupb)
    merges = parse_cir(cirpath).net_case_merges
    if not quiet:
        print('CHECK %s  against  %s' % (ascpath, cirpath))
        for m in asymsgs:
            print('  %s' % m)
        print('  round trip via asc2ngspice.py -> %s' % rtpath)
        print('  compared %d input elements vs %d round-trip elements, '
              '%d nets mapped' % (len(ta), len(tb), len(fwd)))
        for keep, spellings in merges.items():
            print('  NOTE: net-name spellings %s are ONE node in ngspice '
                  '(case-insensitive); using %r' % (spellings, keep))
        print('  VERIFY: %s' % ('PASS' if ok else 'FAIL'))
        for m in cmsgs:
            print('    %s' % m)
        for m in msgs:
            print('    MISMATCH: %s' % m)
        for m in notes:
            print('    NOTE: %s' % m)
    return ok


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('input', help='ngspice netlist (.cir)')
    ap.add_argument('-o', '--output', help='output .asc (default: <input>.asc)')
    ap.add_argument('--rt', help='where to write the round-trip .cir')
    ap.add_argument('--symdir', default=DEFAULT_LIBDIR)
    ap.add_argument('--stub', type=int, default=STUB_DEFAULT)
    ap.add_argument('--cols', type=int, default=None)
    ap.add_argument('--layout', choices=('auto', 'flow', 'spine', 'grid'),
                    default='auto',
                    help='auto (default): try the v2 half-bridge FLOW layout, '
                         'then the v2b SPINE layout, then the v1 grid; '
                         'flow: half-bridge only, fail if not applicable; '
                         'spine: spine+branches only, fail if not applicable; '
                         'grid: v1 behaviour (label soup, no routing)')
    ap.add_argument('--spine', dest='layout', action='store_const', const='spine',
                    help='alias for --layout spine')
    ap.add_argument('--v1', dest='layout', action='store_const', const='grid',
                    help='alias for --layout grid')
    ap.add_argument('--no-verify', dest='verify', action='store_false')
    ap.add_argument('--keep-rt', action='store_true', default=True)
    ap.add_argument('-q', '--quiet', action='store_true')
    ap.add_argument('--check', metavar='ASC',
                    help='do not generate: verify an existing .asc against '
                         'INPUT and exit 0/1')
    a = ap.parse_args(argv)

    if a.check:
        return 0 if check_only(a.input, a.check, libdir=a.symdir, rtpath=a.rt,
                               quiet=a.quiet) else 1

    out = a.output or (os.path.splitext(os.path.basename(a.input))[0] + '.asc')
    ok, info = convert(a.input, out, libdir=a.symdir, stub=a.stub, cols=a.cols,
                       verify=a.verify, rtpath=a.rt, keep_rt=a.keep_rt,
                       quiet=a.quiet, layout=a.layout)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
