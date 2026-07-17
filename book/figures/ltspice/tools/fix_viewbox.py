#!/usr/bin/env python3
"""
fix_viewbox.py -- widen an ltspice_to_svg-generated SVG's viewBox so that
long <text> annotations (added as LTspice comment TEXT lines in the .asc)
are not clipped.

Why this is needed: ltspice_to_svg's ViewboxCalculator
(site-packages/src/renderers/viewbox_calculator.py) computes the viewBox
from wires/shapes/symbols/flags only -- it never measures <text> content,
so a comment line placed at a fixed x that is longer than the schematic's
own wire/symbol extent silently renders past the right edge of the viewBox
and gets clipped by the SVG's default overflow:hidden. This was found
during the chapter02 figure audit (FLEET.md 図監査規約) when BJT/MOSFET/
IGBT/thyristor circuits used longer Japanese documentation comments than
chapter01's short one-liners.

Fix: re-parse the emitted SVG, estimate each <text> element's rendered
width from its content and font-size (ASCII glyph advance ~= 0.55*em,
full-width/CJK glyph advance ~= 1.0*em -- a conservative Arial estimate,
not exact metrics), and grow the viewBox's right/bottom edge to cover the
widest/lowest text runs found, with the same 10% margin convention the
original calculator uses.
"""
import re
import sys
from pathlib import Path

CJK_RANGES = (
    (0x3000, 0x30FF),   # CJK punctuation, hiragana, katakana
    (0x3400, 0x4DBF),   # CJK extension A
    (0x4E00, 0x9FFF),   # CJK unified ideographs
    (0xFF00, 0xFFEF),   # full-width forms
)


def is_cjk(ch):
    cp = ord(ch)
    return any(lo <= cp <= hi for lo, hi in CJK_RANGES)


def estimate_text_width(content, font_size):
    width = 0.0
    for ch in content:
        width += font_size * (1.0 if is_cjk(ch) else 0.55)
    return width


TEXT_RE = re.compile(
    r'<text\b[^>]*\bfont-size="([\d.]+)px"[^>]*\bx="(-?[\d.]+)"[^>]*\by="(-?[\d.]+)"[^>]*>(.*?)</text>',
    re.DOTALL,
)
VIEWBOX_RE = re.compile(r'viewBox="(-?[\d.]+) (-?[\d.]+) (-?[\d.]+) (-?[\d.]+)"')


def fix(svg_path: Path) -> bool:
    svg = svg_path.read_text(encoding="utf-8")
    m = VIEWBOX_RE.search(svg)
    if not m:
        print(f"  skip (no viewBox found): {svg_path}")
        return False
    min_x, min_y, width, height = (float(v) for v in m.groups())
    max_x, max_y = min_x + width, min_y + height

    text_max_x = max_x
    text_max_y = max_y
    for fsize, x, y, content in TEXT_RE.findall(svg):
        fsize = float(fsize)
        x = float(x)
        y = float(y)
        right_edge = x + estimate_text_width(content, fsize)
        text_max_x = max(text_max_x, right_edge)
        text_max_y = max(text_max_y, y + fsize * 0.3)

    if text_max_x <= max_x and text_max_y <= max_y:
        print(f"  ok, no overflow detected: {svg_path.name}")
        return False

    new_max_x = text_max_x + width * 0.03
    new_max_y = text_max_y + height * 0.03
    new_width = new_max_x - min_x
    new_height = new_max_y - min_y

    new_viewbox = f'viewBox="{min_x} {min_y} {new_width} {new_height}"'
    svg = VIEWBOX_RE.sub(new_viewbox, svg, count=1)
    svg_path.write_text(svg, encoding="utf-8")
    print(f"  fixed: {svg_path.name}  viewBox width {width:.1f}->{new_width:.1f}, "
          f"height {height:.1f}->{new_height:.1f}")
    return True


def main():
    if len(sys.argv) < 2:
        print("usage: fix_viewbox.py <svg_file> [<svg_file> ...]")
        sys.exit(1)
    any_fixed = False
    for arg in sys.argv[1:]:
        p = Path(arg)
        if fix(p):
            any_fixed = True
    sys.exit(0)


if __name__ == "__main__":
    main()
