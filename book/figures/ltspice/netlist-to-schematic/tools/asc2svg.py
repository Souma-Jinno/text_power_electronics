#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
asc2svg.py -- LTspice .asc schematic  ->  readable SVG (and optional PNG).

Pure-Python, no mandatory third-party dependency: the SVG XML is emitted by
string formatting.  PNG export is optional and uses cairosvg (preferred) or
matplotlib+cairosvg if either happens to be installed; if neither is present
the PNG step is skipped with a clear message (nothing is ever installed).

Usage
-----
    python asc2svg.py <input.asc> [-o out.svg] [--png out.png]
                      [--symdir DIR]... [--spiceline] [--margin N]

Default output is the input basename with a .svg extension, in the CWD.

Geometry conventions
--------------------
LTspice's Y axis points DOWN, which is also the SVG convention, so schematic
coordinates are emitted verbatim into the SVG user space and the viewBox is
computed from the content bounding box.  Nothing is flipped anywhere, so .asy
symbol primitives keep the orientation LTspice draws them with.

Symbol instance placement uses exactly the ORI table from asc2ngspice.py /
tools_ascnet_check.py, so a pin drawn by this renderer lands on the same
coordinate the netlister assigns it to.

Records understood
------------------
  .asc : Version, SHEET, WIRE, FLAG, IOPIN, SYMBOL, WINDOW, SYMATTR, TEXT,
         LINE, RECTANGLE, CIRCLE, ARC, DATAFLAG (ignored)
  .asy : LINE, RECTANGLE, CIRCLE, ARC, WINDOW, PIN, PINATTR, SYMATTR
"""

import sys, os, glob, math, unicodedata
from collections import defaultdict

# --------------------------------------------------------------------------
# orientation table -- MUST stay identical to asc2ngspice.py / tools_ascnet_check.py
# --------------------------------------------------------------------------
ORI = {'R0':   lambda x, y: (x, y),
       'R90':  lambda x, y: (-y, x),
       'R180': lambda x, y: (-x, -y),
       'R270': lambda x, y: (y, -x),
       'M0':   lambda x, y: (-x, y),
       'M90':  lambda x, y: (y, x),
       'M180': lambda x, y: (x, -y),
       'M270': lambda x, y: (-y, -x)}

# Resolved relative to THIS file so the tool works wherever the package is
# unpacked.  (Was an absolute path; that broke as soon as the tools were copied.)
DEFAULT_SYMDIRS = [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ltsym')]

GRID = 16.0                      # LTspice grid pitch
BASE_FONT = 1.5 * GRID           # 24 px == LTspice text "size 2"
# LTspice font size index -> multiplier of BASE_FONT
FONT_MULT = {0: 0.625, 1: 0.75, 2: 1.0, 3: 1.25, 4: 1.5,
             5: 2.0, 6: 2.5, 7: 3.5}

W_WIRE = 2.0                     # wire / symbol stroke width
W_SHAPE = 2.0
DOT_R = 4.0                      # junction dot radius

# LTspice line-style index -> SVG stroke-dasharray
DASH = {0: None, 1: '16,8', 2: '4,6', 3: '16,6,4,6', 4: '16,6,4,6,4,6'}


def fsize(idx, default=2):
    try:
        idx = int(idx)
    except (TypeError, ValueError):
        idx = default
    return BASE_FONT * FONT_MULT.get(idx, 1.0)


# --------------------------------------------------------------------------
# text decoding: .asc/.asy are either UTF-16LE (LTspice default) or plain ASCII
# --------------------------------------------------------------------------
def read_text(path):
    raw = open(path, 'rb').read()
    for enc in ('utf-16', 'utf-16-le', 'utf-8', 'latin-1'):
        try:
            t = raw.decode(enc)
        except (UnicodeError, UnicodeDecodeError):
            continue
        # heuristic: a good decode of a schematic starts with "Version"
        if t.lstrip('﻿').startswith('Version'):
            return t.lstrip('﻿').replace('\r\n', '\n')
    return raw.decode('latin-1').replace('\r\n', '\n')


def xesc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;'))


def _ints(parts, n, off=1):
    return [int(float(parts[off + i])) for i in range(n)]


# advance width per character, in em, used only for the bounding box.
# CJK ideographs / kana are full-width, halfwidth katakana is ~0.5 em.
_EAW_EM = {'W': 1.0, 'F': 1.0, 'A': 0.62, 'H': 0.5, 'Na': 0.58, 'N': 0.58}


def text_width(s, size):
    em = 0.0
    for ch in s:
        em += _EAW_EM.get(unicodedata.east_asian_width(ch), 0.58)
    return em * size


# --------------------------------------------------------------------------
# .asy symbol library
# --------------------------------------------------------------------------
def parse_asy(path):
    """-> dict(lines, rects, circles, arcs, windows, pins, name)"""
    sym = {'lines': [], 'rects': [], 'circles': [], 'arcs': [],
           'windows': {}, 'pins': [], 'attrs': {}}
    txt = read_text(path)
    for ln in txt.split('\n'):
        p = ln.split()
        if not p:
            continue
        h = p[0]
        try:
            if h == 'LINE':                      # LINE Normal x1 y1 x2 y2 [style]
                x1, y1, x2, y2 = _ints(p, 4, 2)
                sym['lines'].append((x1, y1, x2, y2, int(p[6]) if len(p) > 6 else 0))
            elif h == 'RECTANGLE':
                x1, y1, x2, y2 = _ints(p, 4, 2)
                sym['rects'].append((x1, y1, x2, y2, int(p[6]) if len(p) > 6 else 0))
            elif h == 'CIRCLE':
                x1, y1, x2, y2 = _ints(p, 4, 2)
                sym['circles'].append((x1, y1, x2, y2, int(p[6]) if len(p) > 6 else 0))
            elif h == 'ARC':   # ARC Normal bx1 by1 bx2 by2 sx sy ex ey [style]
                v = _ints(p, 8, 2)
                sym['arcs'].append(tuple(v) + (int(p[10]) if len(p) > 10 else 0,))
            elif h == 'WINDOW':                  # WINDOW id x y just size
                wid = int(p[1]); x, y = int(p[2]), int(p[3])
                sym['windows'][wid] = (x, y, p[4], int(p[5]) if len(p) > 5 else 2)
            elif h == 'PIN':                     # PIN x y NONE 0
                sym['pins'].append([int(p[1]), int(p[2]), None])
            elif h == 'PINATTR' and sym['pins']:
                if p[1] == 'PinName':
                    sym['pins'][-1][2] = ln.split(None, 2)[2]
            elif h == 'SYMATTR' and len(p) >= 2:
                parts = ln.split(None, 2)
                sym['attrs'][parts[1]] = parts[2] if len(parts) > 2 else ''
        except (ValueError, IndexError):
            continue
    sym['pins'] = [tuple(q) for q in sym['pins']]
    return sym


def symkey(raw):
    """normalise a SYMBOL name to an .asy library key (same rule as asc2ngspice)."""
    k = raw.lower().replace('\\\\', '\\')
    if 'jumper' in k:
        return 'jumper'
    if '\\' in k:
        k = k.split('\\')[-1]
    if '/' in k:
        k = k.split('/')[-1]
    return k


def load_symlib(dirs):
    lib = {}
    for d in dirs:
        if not d or not os.path.isdir(d):
            continue
        files = sorted(set(glob.glob(os.path.join(d, '**', '*.asy'), recursive=True) +
                           glob.glob(os.path.join(d, '*.asy'))))
        for f in files:
            key = symkey(os.path.splitext(os.path.basename(f))[0])
            if key in lib:
                continue                     # earlier dirs win
            try:
                lib[key] = parse_asy(f)
            except Exception:
                pass
    return lib


# --------------------------------------------------------------------------
# .asc schematic
# --------------------------------------------------------------------------
def parse_asc(path):
    sch = {'wires': [], 'flags': [], 'syms': [], 'texts': [],
           'lines': [], 'rects': [], 'circles': [], 'arcs': [], 'sheet': None}
    cur = None

    def flush():
        nonlocal cur
        if cur is not None:
            sch['syms'].append(cur)
        cur = None

    for ln in read_text(path).split('\n'):
        p = ln.split()
        if not p:
            continue
        h = p[0]
        try:
            if h == 'SYMBOL':                # SYMBOL name x y ORI
                flush()
                cur = {'raw': p[1], 'key': symkey(p[1]),
                       'x': int(p[2]), 'y': int(p[3]),
                       'ori': p[4] if len(p) > 4 else 'R0',
                       'windows': {}, 'attrs': {}}
                continue
            if h == 'WINDOW' and cur is not None:
                wid = int(p[1])
                cur['windows'][wid] = (int(p[2]), int(p[3]), p[4],
                                       int(p[5]) if len(p) > 5 else 2)
                continue
            if h == 'SYMATTR' and cur is not None:
                parts = ln.split(None, 2)
                if len(parts) >= 2:
                    cur['attrs'][parts[1]] = parts[2] if len(parts) > 2 else ''
                continue
            # any other record terminates the symbol block
            flush()
            if h == 'WIRE':
                x1, y1, x2, y2 = _ints(p, 4)
                sch['wires'].append(((x1, y1), (x2, y2)))
            elif h in ('FLAG', 'IOPIN'):
                name = ln.split(' ', 3)[3].strip() if len(ln.split(' ', 3)) > 3 else ''
                sch['flags'].append(((int(p[1]), int(p[2])), name, h))
            elif h == 'TEXT':                # TEXT x y Just Size body
                parts = ln.split(None, 5)
                if len(parts) >= 5:
                    body = parts[5] if len(parts) >= 6 else ''
                    sch['texts'].append({'x': int(parts[1]), 'y': int(parts[2]),
                                         'just': parts[3], 'size': int(parts[4]),
                                         'body': body})
            elif h == 'LINE':
                x1, y1, x2, y2 = _ints(p, 4, 2)
                sch['lines'].append((x1, y1, x2, y2, int(p[6]) if len(p) > 6 else 0))
            elif h == 'RECTANGLE':
                x1, y1, x2, y2 = _ints(p, 4, 2)
                sch['rects'].append((x1, y1, x2, y2, int(p[6]) if len(p) > 6 else 0))
            elif h == 'CIRCLE':
                x1, y1, x2, y2 = _ints(p, 4, 2)
                sch['circles'].append((x1, y1, x2, y2, int(p[6]) if len(p) > 6 else 0))
            elif h == 'ARC':
                v = _ints(p, 8, 2)
                sch['arcs'].append(tuple(v) + (int(p[10]) if len(p) > 10 else 0,))
            elif h == 'SHEET':
                sch['sheet'] = (int(p[2]), int(p[3])) if len(p) > 3 else None
        except (ValueError, IndexError):
            continue
    flush()
    return sch


# --------------------------------------------------------------------------
# transform helpers
# --------------------------------------------------------------------------
class Xf(object):
    """symbol instance placement: local .asy coords -> global schematic coords."""

    def __init__(self, x, y, ori):
        self.ox, self.oy, self.ori = x, y, ori
        self.t = ORI.get(ori, ORI['R0'])
        # unit images tell us about axis swap and handedness
        ax, ay = self.t(1, 0)
        bx, by = self.t(0, 1)
        self.swap = (ax == 0)                        # local x maps to a vertical dir
        self.det = ax * by - ay * bx                 # -1 for the mirrored codes
        self.xflip = (ax < 0) or (bx < 0 and self.swap)

    def __call__(self, x, y):
        dx, dy = self.t(x, y)
        return (self.ox + dx, self.oy + dy)


def pin_coords(sym_inst, lib):
    """global coords of a symbol instance's pins, in .asy PIN file order.

    Order is irrelevant here -- these coordinates are only used to draw the pin
    dots.  The SPICE terminal order (PINATTR SpiceOrder) is resolved in
    asc2ngspice.load_asy(), which is what the netlisting side uses."""
    xf = Xf(sym_inst['x'], sym_inst['y'], sym_inst['ori'])
    s = lib.get(sym_inst['key'])
    if not s:
        return []
    return [xf(px, py) for px, py, _ in s['pins']]


# --------------------------------------------------------------------------
# SVG element emission
# --------------------------------------------------------------------------
class Canvas(object):
    def __init__(self):
        self.body = []
        # text is emitted in two later layers so that no label's white halo
        # can ever paint over another label's glyphs
        self.halos = []
        self.glyphs = []
        self.minx = self.miny = 1e18
        self.maxx = self.maxy = -1e18
        self.counts = defaultdict(int)

    def grow(self, x, y):
        self.minx = min(self.minx, x); self.maxx = max(self.maxx, x)
        self.miny = min(self.miny, y); self.maxy = max(self.maxy, y)

    def add(self, kind, s):
        self.counts[kind] += 1
        self.body.append(s)

    # -- primitives ------------------------------------------------------
    def line(self, x1, y1, x2, y2, kind='wire', width=W_WIRE, style=0, color='black'):
        self.grow(x1, y1); self.grow(x2, y2)
        d = DASH.get(style)
        extra = ' stroke-dasharray="%s"' % d if d else ''
        self.add(kind, '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                       'stroke-width="%g" stroke-linecap="round"%s/>'
                       % (x1, y1, x2, y2, color, width, extra))

    def rect(self, x1, y1, x2, y2, kind='shape', width=W_SHAPE, style=0,
             fill='none', color='black'):
        x, y = min(x1, x2), min(y1, y2)
        w, h = abs(x2 - x1), abs(y2 - y1)
        self.grow(x, y); self.grow(x + w, y + h)
        d = DASH.get(style)
        extra = ' stroke-dasharray="%s"' % d if d else ''
        self.add(kind, '<rect x="%g" y="%g" width="%g" height="%g" fill="%s" '
                       'stroke="%s" stroke-width="%g"%s/>'
                       % (x, y, w, h, fill, color, width, extra))

    def ellipse(self, x1, y1, x2, y2, kind='shape', width=W_SHAPE, style=0,
                fill='none', color='black'):
        cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        rx, ry = abs(x2 - x1) / 2.0, abs(y2 - y1) / 2.0
        self.grow(cx - rx, cy - ry); self.grow(cx + rx, cy + ry)
        d = DASH.get(style)
        extra = ' stroke-dasharray="%s"' % d if d else ''
        self.add(kind, '<ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="%s" '
                       'stroke="%s" stroke-width="%g"%s/>'
                       % (cx, cy, rx, ry, fill, color, width, extra))

    def dot(self, x, y, r=DOT_R, color='black'):
        self.grow(x - r, y - r); self.grow(x + r, y + r)
        self.add('dot', '<circle cx="%g" cy="%g" r="%g" fill="%s"/>' % (x, y, r, color))

    def path(self, d, kind='shape', width=W_SHAPE, style=0, color='black'):
        ds = DASH.get(style)
        extra = ' stroke-dasharray="%s"' % ds if ds else ''
        self.add(kind, '<path d="%s" fill="none" stroke="%s" stroke-width="%g" '
                       'stroke-linecap="round"%s/>' % (d, color, width, extra))

    def text(self, x, y, s, size=BASE_FONT, anchor='start', kind='text',
             color='black', family=None, weight=None, style=None, halo=0.0):
        if s == '':
            return
        family = family or FONT_SANS
        w = text_width(s, size)
        if anchor == 'middle':
            self.grow(x - w / 2, y - size); self.grow(x + w / 2, y + 0.3 * size)
        elif anchor == 'end':
            self.grow(x - w, y - size); self.grow(x, y + 0.3 * size)
        else:
            self.grow(x, y - size); self.grow(x + w, y + 0.3 * size)
        a = ['x="%g"' % x, 'y="%g"' % y,
             'font-family="%s"' % family, 'font-size="%gpx"' % size]
        if anchor != 'start':
            a.append('text-anchor="%s"' % anchor)
        if weight:
            a.append('font-weight="%s"' % weight)
        if style:
            a.append('font-style="%s"' % style)
        attrs = ' '.join(a)
        body = xesc(s)
        # NOTE: paint-order="stroke" is not honoured by every renderer
        # (cairosvg ignores it and the white stroke then erases the glyph),
        # so the halo is a separate copy drawn underneath.
        if halo:
            self.halos.append('<text %s fill="none" stroke="#ffffff" '
                              'stroke-width="%g" stroke-linejoin="round">%s</text>'
                              % (attrs, halo, body))
        self.counts[kind] += 1
        self.glyphs.append('<text %s fill="%s">%s</text>' % (attrs, color, body))


FONT_SANS = ('Noto Sans CJK JP, Noto Sans JP, DejaVu Sans, '
             'Helvetica, Arial, sans-serif')
FONT_MONO = ('Noto Sans Mono CJK JP, DejaVu Sans Mono, '
             'Consolas, Menlo, monospace')


# --------------------------------------------------------------------------
# arc rendering: exact, no flattening.
# All ORI transforms are axis-aligned, so the ellipse stays axis-aligned; we
# only have to swap rx/ry on the axis-swapping codes and flip the SVG sweep
# flag on the mirroring ones.
# --------------------------------------------------------------------------
def arc_svg_path(a, xf):
    bx1, by1, bx2, by2, sx, sy, ex, ey = a[:8]
    cx, cy = (bx1 + bx2) / 2.0, (by1 + by2) / 2.0
    rx, ry = abs(bx2 - bx1) / 2.0, abs(by2 - by1) / 2.0
    if rx < 1e-9 or ry < 1e-9:
        p0 = xf(bx1, by1); p1 = xf(bx2, by2)
        return 'M %g %g L %g %g' % (p0[0], p0[1], p1[0], p1[1]), None
    # the endpoint records are rays from the centre, not necessarily on the curve
    t0 = math.atan2((sy - cy) / ry, (sx - cx) / rx)
    t1 = math.atan2((ey - cy) / ry, (ex - cx) / rx)
    # LTspice sweeps from start to end in the direction of DECREASING angle
    # in this y-down space (verified against ind.asy coils and Misc\jumper).
    delta = t0 - t1
    while delta <= 1e-9:
        delta += 2 * math.pi
    large = 1 if delta > math.pi else 0
    p0 = xf(cx + rx * math.cos(t0), cy + ry * math.sin(t0))
    p1 = xf(cx + rx * math.cos(t1), cy + ry * math.sin(t1))
    if xf.swap:
        rx, ry = ry, rx
    sweep = 1 if xf.det < 0 else 0          # mirroring reverses the sweep
    bbox = (xf(cx - abs(bx2 - bx1) / 2.0, cy - abs(by2 - by1) / 2.0),
            xf(cx + abs(bx2 - bx1) / 2.0, cy + abs(by2 - by1) / 2.0))
    return ('M %g %g A %g %g 0 %d %d %g %g'
            % (p0[0], p0[1], rx, ry, large, sweep, p1[0], p1[1])), bbox


# --------------------------------------------------------------------------
# junction dots
# --------------------------------------------------------------------------
def on_seg_strict(p, a, b):
    """p lies on segment a-b but is not an endpoint (axis-aligned segments)."""
    (px, py), (ax, ay), (bx, by) = p, a, b
    if p == a or p == b:
        return False
    if ax == bx == px and min(ay, by) < py < max(ay, by):
        return True
    if ay == by == py and min(ax, bx) < px < max(ax, bx):
        return True
    return False


def junctions(wires, pinset):
    endcount = defaultdict(int)
    for a, b in wires:
        if a == b:
            continue
        endcount[a] += 1
        endcount[b] += 1
    dots = set()
    for c, n in endcount.items():
        if n >= 3:
            dots.add(c)
    # T-junctions: an endpoint (or a symbol pin) sitting inside another wire
    cands = set(endcount) | set(pinset)
    for c in cands:
        if c in dots:
            continue
        for a, b in wires:
            if on_seg_strict(c, a, b):
                dots.add(c)
                break
    return dots


# --------------------------------------------------------------------------
# ground symbol + net-label placement
# --------------------------------------------------------------------------
def draw_ground(cv, x, y):
    cv.line(x, y, x, y + 8, kind='flag')
    cv.line(x - 16, y + 8, x + 16, y + 8, kind='flag')
    cv.line(x - 16, y + 8, x, y + 24, kind='flag')
    cv.line(x + 16, y + 8, x, y + 24, kind='flag')


def free_side(pt, wire_dirs):
    """pick a side of `pt` that no wire occupies; order of preference U,D,R,L."""
    occ = wire_dirs.get(pt, set())
    for d in ('U', 'D', 'R', 'L'):
        if d not in occ:
            return d
    return 'U'


def build_wire_dirs(wires):
    wd = defaultdict(set)
    for (x1, y1), (x2, y2) in wires:
        if (x1, y1) == (x2, y2):
            continue
        if x1 == x2:
            wd[(x1, y1)].add('D' if y2 > y1 else 'U')
            wd[(x2, y2)].add('D' if y1 > y2 else 'U')
        elif y1 == y2:
            wd[(x1, y1)].add('R' if x2 > x1 else 'L')
            wd[(x2, y2)].add('R' if x1 > x2 else 'L')
        else:                                    # diagonal: block both
            wd[(x1, y1)].update('UDLR')
            wd[(x2, y2)].update('UDLR')
    return wd


# --------------------------------------------------------------------------
# main render
# --------------------------------------------------------------------------
JUST_ANCHOR = {'Left': 'start', 'Right': 'end', 'Center': 'middle',
               'Top': 'middle', 'Bottom': 'middle',
               'VTop': 'middle', 'VBottom': 'middle',
               'VLeft': 'middle', 'VRight': 'middle'}


def render(ascpath, symdirs, margin=48, show_spiceline=False):
    sch = parse_asc(ascpath)
    lib = load_symlib(symdirs)
    cv = Canvas()
    missing = set()

    # ---------------- wires ----------------
    for (x1, y1), (x2, y2) in sch['wires']:
        cv.line(x1, y1, x2, y2, kind='wire')

    # ---------------- free-standing drawing objects ----------------
    ident = Xf(0, 0, 'R0')
    for x1, y1, x2, y2, st in sch['lines']:
        cv.line(x1, y1, x2, y2, kind='shape', style=st)
    for x1, y1, x2, y2, st in sch['rects']:
        cv.rect(x1, y1, x2, y2, style=st)
    for x1, y1, x2, y2, st in sch['circles']:
        cv.ellipse(x1, y1, x2, y2, style=st)
    for a in sch['arcs']:
        d, bbox = arc_svg_path(a, ident)
        if bbox:
            cv.grow(*bbox[0]); cv.grow(*bbox[1])
        cv.path(d, style=a[8] if len(a) > 8 else 0)

    # ---------------- symbols ----------------
    all_pins = []                       # (inst, key, order, coord)
    for si in sch['syms']:
        s = lib.get(si['key'])
        xf = Xf(si['x'], si['y'], si['ori'])
        inst = si['attrs'].get('InstName', '')
        if not s:
            missing.add(si['raw'])
            # placeholder so nothing silently disappears
            p = xf(0, 0)
            cv.rect(p[0] - 16, p[1] - 16, p[0] + 16, p[1] + 16,
                    kind='symbol', style=2)
            cv.text(p[0], p[1] - 22, si['raw'], size=BASE_FONT * 0.7,
                    anchor='middle', kind='symtext', halo=3.0)
            continue

        for x1, y1, x2, y2, st in s['lines']:
            a = xf(x1, y1); b = xf(x2, y2)
            cv.line(a[0], a[1], b[0], b[1], kind='symbol', style=st)
        for x1, y1, x2, y2, st in s['rects']:
            a = xf(x1, y1); b = xf(x2, y2)
            cv.rect(a[0], a[1], b[0], b[1], kind='symbol', style=st)
        for x1, y1, x2, y2, st in s['circles']:
            a = xf(x1, y1); b = xf(x2, y2)
            cv.ellipse(a[0], a[1], b[0], b[1], kind='symbol', style=st)
        for a in s['arcs']:
            d, bbox = arc_svg_path(a, xf)
            if bbox:
                cv.grow(*bbox[0]); cv.grow(*bbox[1])
            cv.path(d, kind='symbol', style=a[8] if len(a) > 8 else 0)

        for k, (px, py, pname) in enumerate(s['pins']):
            c = xf(px, py)
            cv.grow(c[0], c[1])
            all_pins.append((inst, si['key'], k, c))

        # ---- attribute text (InstName = window 0, Value = window 3,
        #      SpiceLine = window 39) --------------------------------------
        items = [(0, inst, 1.0)]
        val = si['attrs'].get('Value', '')
        if val:
            items.append((3, val, 1.0))
        if show_spiceline and si['attrs'].get('SpiceLine'):
            items.append((39, si['attrs']['SpiceLine'], 0.8))
        for wid, body, scale in items:
            if not body:
                continue
            if wid in si['windows']:
                wx, wy, just, wsz = si['windows'][wid]
                if wsz == 0:
                    continue            # size 0 in an .asc override == hidden
            elif wid in s['windows']:
                wx, wy, just, wsz = s['windows'][wid]
                if wsz == 0:
                    wsz = 2             # size 0 in an .asy == "default size"
            else:
                continue                # attribute has no place to go
            gx, gy = xf(wx, wy)
            anchor = JUST_ANCHOR.get(just, 'start')
            if xf.swap:
                anchor = 'middle'       # LTspice would set this text vertical
            elif xf.xflip:
                anchor = {'start': 'end', 'end': 'start'}.get(anchor, anchor)
            sz = fsize(wsz) * scale
            cv.text(gx, gy + 0.35 * sz, body, size=sz, anchor=anchor,
                    kind='symtext', halo=3.5)

    # ---------------- junction dots ----------------
    pinset = set(c for _, _, _, c in all_pins)
    for (jx, jy) in sorted(junctions(sch['wires'], pinset)):
        cv.dot(jx, jy)

    # ---------------- flags / net labels ----------------
    wd = build_wire_dirs(sch['wires'])
    seen_at = defaultdict(int)          # several FLAGs may share one coordinate
    for (fx, fy), name, kind in sch['flags']:
        if name == '0':
            draw_ground(cv, fx, fy)
            continue
        sz = BASE_FONT * 0.85
        lh = 1.15 * sz
        n = seen_at[(fx, fy)]
        seen_at[(fx, fy)] += 1
        side = free_side((fx, fy), wd)
        if side == 'U':
            tx, ty, anc = fx, fy - 10 - n * lh, 'middle'
        elif side == 'D':
            tx, ty, anc = fx, fy + 10 + 0.8 * sz + n * lh, 'middle'
        elif side == 'R':
            tx, ty, anc = fx + 10, fy + 0.35 * sz + n * lh, 'start'
        else:
            tx, ty, anc = fx - 10, fy + 0.35 * sz + n * lh, 'end'
        if n == 0:
            cv.dot(fx, fy, r=3.0)
        cv.text(tx, ty, name, size=sz, anchor=anc, kind='netlabel',
                weight='bold', halo=4.0)

    # ---------------- free text: comments and SPICE directives ----------
    for t in sch['texts']:
        body = t['body']
        if not body:
            continue
        directive = body.startswith('!')
        comment = body.startswith(';')
        raw = body[1:] if (directive or comment) else body
        lines = [ln for ln in raw.split('\\n')]
        sz = fsize(t['size'])
        fam = FONT_MONO if directive else FONT_SANS
        col = '#000000' if not comment else '#333333'
        sty = 'italic' if comment else None
        anchor = JUST_ANCHOR.get(t['just'], 'start')
        lh = 1.25 * sz
        y0 = t['y'] - (len(lines) - 1) * lh / 2.0 + 0.35 * sz
        for i, ln in enumerate(lines):
            cv.text(t['x'], y0 + i * lh, ln, size=sz, anchor=anchor,
                    kind='directive' if directive else 'comment',
                    color=col, family=fam, style=sty, halo=3.5)

    # ---------------- assemble ----------------
    if cv.maxx < cv.minx:               # completely empty schematic
        cv.minx = cv.miny = 0; cv.maxx = cv.maxy = 100
    vx = cv.minx - margin
    vy = cv.miny - margin
    vw = (cv.maxx - cv.minx) + 2 * margin
    vh = (cv.maxy - cv.miny) + 2 * margin

    title = os.path.basename(ascpath)
    out = []
    out.append('<?xml version="1.0" encoding="UTF-8"?>')
    out.append('<svg xmlns="http://www.w3.org/2000/svg" '
               'xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" '
               'width="%g" height="%g" viewBox="%g %g %g %g">'
               % (vw, vh, vx, vy, vw, vh))
    out.append('<title>%s</title>' % xesc(title))
    out.append('<desc>Rendered from %s by asc2svg.py</desc>' % xesc(os.path.abspath(ascpath)))
    out.append('<rect x="%g" y="%g" width="%g" height="%g" fill="#ffffff"/>'
               % (vx, vy, vw, vh))
    out.append('<g id="graphics">')
    out.extend(cv.body)
    out.append('</g>')
    out.append('<g id="text-halo">')
    out.extend(cv.halos)
    out.append('</g>')
    out.append('<g id="text">')
    out.extend(cv.glyphs)
    out.append('</g>')
    out.append('</svg>')

    stats = dict(cv.counts)
    stats['_bbox'] = (cv.minx, cv.miny, cv.maxx, cv.maxy)
    stats['_viewbox'] = (vx, vy, vw, vh)
    stats['_pins'] = all_pins
    stats['_missing'] = sorted(missing)
    stats['_records'] = {'WIRE': len(sch['wires']), 'SYMBOL': len(sch['syms']),
                         'FLAG': len(sch['flags']), 'TEXT': len(sch['texts'])}
    return '\n'.join(out) + '\n', stats


# --------------------------------------------------------------------------
# optional PNG
# --------------------------------------------------------------------------
def write_png(svg_text, png_path, scale=1.0):
    """-> (ok, message). Never installs anything."""
    try:
        import cairosvg
    except ImportError:
        return False, ('PNG skipped: cairosvg is not importable in this '
                       'interpreter (%s). Install it or use the SVG.'
                       % sys.executable)
    try:
        cairosvg.svg2png(bytestring=svg_text.encode('utf-8'),
                         write_to=png_path, scale=scale,
                         background_color='white')
        return True, 'PNG written via cairosvg -> %s' % png_path
    except Exception as e:
        return False, 'PNG failed (cairosvg): %s' % e


# --------------------------------------------------------------------------
def main(argv):
    import argparse
    ap = argparse.ArgumentParser(
        description='Render an LTspice .asc schematic to SVG (and optionally PNG).')
    ap.add_argument('input', help='input .asc file')
    ap.add_argument('-o', '--output', help='output .svg (default: <basename>.svg)')
    ap.add_argument('--png', help='also write a PNG here (needs cairosvg)')
    ap.add_argument('--png-scale', type=float, default=1.0,
                    help='PNG scale factor (default 1.0)')
    ap.add_argument('--symdir', action='append', default=[],
                    help='extra directory of .asy symbols (repeatable)')
    ap.add_argument('--margin', type=float, default=48.0,
                    help='blank margin around the content, in LTspice units')
    ap.add_argument('--spiceline', action='store_true',
                    help='also draw the SYMATTR SpiceLine text (Rser=... etc.)')
    ap.add_argument('-q', '--quiet', action='store_true')
    a = ap.parse_args(argv)

    symdirs = list(a.symdir)
    symdirs.append(os.path.dirname(os.path.abspath(a.input)))   # sidecar .asy
    symdirs.extend(DEFAULT_SYMDIRS)
    symdirs.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ltsym'))

    svg, st = render(a.input, symdirs, margin=a.margin,
                     show_spiceline=a.spiceline)
    out = a.output or (os.path.splitext(os.path.basename(a.input))[0] + '.svg')
    d = os.path.dirname(os.path.abspath(out))
    if d and not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(svg)

    if not a.quiet:
        r = st['_records']
        print('%s -> %s' % (a.input, out))
        print('  records : WIRE=%d SYMBOL=%d FLAG=%d TEXT=%d'
              % (r['WIRE'], r['SYMBOL'], r['FLAG'], r['TEXT']))
        print('  drawn   : ' + ' '.join(
            '%s=%d' % (k, v) for k, v in sorted(st.items()) if not k.startswith('_')))
        print('  viewBox : %g %g %g %g' % st['_viewbox'])
        if st['_missing']:
            print('  WARNING: no .asy found for: %s' % ', '.join(st['_missing']))

    if a.png:
        ok, msg = write_png(svg, a.png, scale=a.png_scale)
        if not a.quiet:
            print('  ' + msg)
        if not ok:
            return 0        # SVG still succeeded
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
