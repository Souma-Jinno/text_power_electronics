"""
Minimal SVG->PNG previewer for visually auditing the figures this pipeline produces
(no cairosvg/rsvg/wine available on this machine -- see tools/README.md). Handles only
the small subset of SVG this pipeline's own renderer (ltspice_to_svg + fix_viewbox.py)
actually emits: <line>, <rect>, <ellipse>, <text>, and <g transform="translate(x,y)
rotate(r)">. Not a general SVG renderer -- do not use on arbitrary SVG.
"""
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


def render(svg_path, png_path):
    svg = open(svg_path, encoding="utf-8").read()
    vb = re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+)"', svg)
    x0, y0, w, h = map(float, vb.groups())

    fig, ax = plt.subplots(figsize=(w / 60, h / 60), dpi=110)

    # Walk top-level <g ...>...</g> blocks and bare <line>/<text> at document level.
    # Track current translate offset by regex-splitting on group boundaries (good
    # enough for this pipeline's flat, non-nested-transform output).
    tx, ty = 0.0, 0.0
    depth_stack = []
    tag_iter = re.finditer(r'<(/?)(g|line|rect|ellipse)\b([^>]*)(/?)>', svg)
    for m in tag_iter:
        closing, tag, attrs, selfclose = m.group(1), m.group(2), m.group(3), m.group(4)
        if tag == "g":
            if closing:
                if depth_stack:
                    tx, ty = depth_stack.pop()
            else:
                depth_stack.append((tx, ty))
                dtx, dty, rot = parse_transform("<g " + attrs + ">")
                tx, ty = tx + dtx, ty + dty
            continue
        if tag == "line":
            g = lambda k: float(re.search(k + r'="([-\d.]+)"', attrs).group(1))
            x1, x2, y1, y2 = g("x1"), g("x2"), g("y1"), g("y2")
            ax.plot([tx + x1, tx + x2], [ty + y1, ty + y2], color="black", linewidth=1.2)
        elif tag == "rect":
            g = lambda k: float(re.search(k + r'="([-\d.]+)"', attrs).group(1))
            x, y, rw, rh = g("x"), g("y"), g("width"), g("height")
            ax.add_patch(Rectangle((tx + x, ty + y), rw, rh, fill=False, edgecolor="black", linewidth=1.2))
        elif tag == "ellipse":
            g = lambda k: float(re.search(k + r'="([-\d.]+)"', attrs).group(1))
            cx, cy, rx, ry = g("cx"), g("cy"), g("rx"), g("ry")
            ax.add_patch(Ellipse((tx + cx, ty + cy), 2 * rx, 2 * ry, fill=False, edgecolor="black", linewidth=1.2))

    # Second pass: walk again tracking only g-translate, drawing text at each <text> tag
    # (kept separate from the shape pass above since interleaving both in one regex pass
    # made the group-depth bookkeeping error-prone).
    running_tx, running_ty = 0.0, 0.0
    stack = []
    for gm in re.finditer(r'<(/?)g\b([^>]*)>|<text\b([^>]*)>([^<]*)</text>', svg):
        if gm.group(0).startswith("</g"):
            if stack:
                running_tx, running_ty = stack.pop()
        elif gm.group(0).startswith("<g"):
            stack.append((running_tx, running_ty))
            dtx, dty, rot = parse_transform(gm.group(0))
            running_tx += dtx
            running_ty += dty
        else:
            attrs, content = gm.group(3), gm.group(4)
            xx = float(re.search(r'\bx="([-\d.]+)"', attrs).group(1))
            yy = float(re.search(r'\by="([-\d.]+)"', attrs).group(1))
            fsm = re.search(r'font-size="([\d.]+)', attrs)
            fs = float(fsm.group(1)) if fsm else 24.0
            ax.text(running_tx + xx, running_ty + yy - fs * 0.7, content, fontsize=fs * 0.5,
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
