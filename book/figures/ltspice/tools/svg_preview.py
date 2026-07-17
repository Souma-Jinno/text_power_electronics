"""
Minimal SVG->PNG previewer for visually auditing the figures this pipeline produces
(no cairosvg/rsvg/wine available on this machine -- see tools/README.md). Handles only
the small subset of SVG this pipeline's own renderer (ltspice_to_svg + fix_viewbox.py)
actually emits: <line>, <rect>, <ellipse>, <text>, and <g transform="translate(x,y)
rotate(r)">. Not a general SVG renderer -- do not use on arbitrary SVG.
"""
import math
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse


def parse_transform(g_tag):
    m = re.search(r'transform="translate\(([-\d.]+),([-\d.]+)\)(?:\s*rotate\(([-\d.]+)\))?"', g_tag)
    if not m:
        return 0.0, 0.0, 0.0
    tx, ty = float(m.group(1)), float(m.group(2))
    rot = float(m.group(3)) if m.group(3) else 0.0
    return tx, ty, rot


def rotate_pt(x, y, rot_deg):
    # SVG "translate(tx,ty) rotate(r)" applies rotate first (around the local
    # origin) and translate second -- rotate the local point before adding tx,ty.
    if not rot_deg:
        return x, y
    theta = math.radians(rot_deg)
    return (x * math.cos(theta) - y * math.sin(theta),
            x * math.sin(theta) + y * math.cos(theta))


def render(svg_path, png_path):
    svg = open(svg_path, encoding="utf-8").read()
    vb = re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+)"', svg)
    x0, y0, w, h = map(float, vb.groups())

    fig, ax = plt.subplots(figsize=(w / 60, h / 60), dpi=110)

    # Walk top-level <g ...>...</g> blocks and bare <line>/<text> at document level.
    # Track current translate+rotate by regex-splitting on group boundaries (good
    # enough for this pipeline's flat, non-nested-transform output). Rotation is
    # accumulated too (not just translation) -- a symbol placed with e.g. R180/R270
    # in the .asc (rendered by ltspice_to_svg as "translate(tx,ty) rotate(r)") must
    # have its local line/rect/ellipse coordinates rotated before the translate is
    # applied, or the preview draws the shape in the wrong place while the real SVG
    # (which a real SVG viewer rotates correctly) is fine -- caught 2026-07-18 on
    # chapter05's diode symbols (R180), see figure audit README in this directory.
    tx, ty, rot = 0.0, 0.0, 0.0
    depth_stack = []
    tag_iter = re.finditer(r'<(/?)(g|line|rect|ellipse)\b([^>]*)(/?)>', svg)
    for m in tag_iter:
        closing, tag, attrs, selfclose = m.group(1), m.group(2), m.group(3), m.group(4)
        if tag == "g":
            if closing:
                if depth_stack:
                    tx, ty, rot = depth_stack.pop()
            else:
                depth_stack.append((tx, ty, rot))
                dtx, dty, drot = parse_transform("<g " + attrs + ">")
                # dtx,dty are in the *parent* (pre-rotation) frame for this pipeline's
                # flat "translate(x,y) rotate(r)" symbol groups (rotation pivots on
                # the symbol's own local origin, not the parent's), so just add them.
                tx, ty, rot = tx + dtx, ty + dty, rot + drot
            continue
        if tag == "line":
            g = lambda k: float(re.search(k + r'="([-\d.]+)"', attrs).group(1))
            x1, x2, y1, y2 = g("x1"), g("x2"), g("y1"), g("y2")
            rx1, ry1 = rotate_pt(x1, y1, rot)
            rx2, ry2 = rotate_pt(x2, y2, rot)
            ax.plot([tx + rx1, tx + rx2], [ty + ry1, ty + ry2], color="black", linewidth=1.2)
        elif tag == "rect":
            g = lambda k: float(re.search(k + r'="([-\d.]+)"', attrs).group(1))
            x, y, rw, rh = g("x"), g("y"), g("width"), g("height")
            rx, ry = rotate_pt(x, y, rot)
            ax.add_patch(Rectangle((tx + rx, ty + ry), rw, rh, angle=rot, fill=False, edgecolor="black", linewidth=1.2))
        elif tag == "ellipse":
            g = lambda k: float(re.search(k + r'="([-\d.]+)"', attrs).group(1))
            cx, cy, rx, ry = g("cx"), g("cy"), g("rx"), g("ry")
            rcx, rcy = rotate_pt(cx, cy, rot)
            ax.add_patch(Ellipse((tx + rcx, ty + rcy), 2 * rx, 2 * ry, fill=False, edgecolor="black", linewidth=1.2))

    # Second pass: walk again tracking only g-translate, drawing text at each <text> tag
    # (kept separate from the shape pass above since interleaving both in one regex pass
    # made the group-depth bookkeeping error-prone).
    running_tx, running_ty, running_rot = 0.0, 0.0, 0.0
    stack = []
    for gm in re.finditer(r'<(/?)g\b([^>]*)>|<text\b([^>]*)>([^<]*)</text>', svg):
        if gm.group(0).startswith("</g"):
            if stack:
                running_tx, running_ty, running_rot = stack.pop()
        elif gm.group(0).startswith("<g"):
            stack.append((running_tx, running_ty, running_rot))
            dtx, dty, drot = parse_transform(gm.group(0))
            running_tx += dtx
            running_ty += dty
            running_rot += drot
        else:
            attrs, content = gm.group(3), gm.group(4)
            xx = float(re.search(r'\bx="([-\d.]+)"', attrs).group(1))
            yy = float(re.search(r'\by="([-\d.]+)"', attrs).group(1))
            fsm = re.search(r'font-size="([\d.]+)', attrs)
            fs = float(fsm.group(1)) if fsm else 24.0
            rxx, ryy = rotate_pt(xx, yy - fs * 0.7, running_rot)
            ax.text(running_tx + rxx, running_ty + ryy, content, fontsize=fs * 0.5,
                     family="sans-serif", va="bottom", ha="left")

    ax.set_xlim(x0, x0 + w)
    ax.set_ylim(y0 + h, y0)  # SVG y grows downward
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout(pad=0.3)
    fig.savefig(png_path, facecolor="white")
    plt.close(fig)
    print("wrote", png_path)


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
