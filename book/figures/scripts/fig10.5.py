#!/usr/bin/env python3
# fig10.5（第10章）: マトリックスコンバータの構成。3相入力と3相出力の
# 交点に双方向スイッチを9個並べた行列配置と，双方向スイッチの内部構成。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyBboxPatch
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BK = "#222222"
BLUE = "#2a5db0"
RED = "#c0392b"
GY = "#999999"

fig, ax = plt.subplots(figsize=(4.25, 2.5))
ax.set_xlim(-1.6, 11.0)
ax.set_ylim(-1.3, 5.6)
ax.set_aspect("equal")
ax.axis("off")


def wire(pts, c=BK, lw=1.0, ls="-"):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=c, lw=lw,
            ls=ls, solid_capstyle="round", zorder=1)


def dot(x, y):
    ax.plot([x], [y], "o", ms=2.2, color=BK, zorder=3)


# --- 入力3線（横）と出力3線（縦）
YIN = [4.4, 3.2, 2.0]          # u, v, w
XOUT = [1.6, 3.4, 5.2]         # U, V, W
for y, name in zip(YIN, ["u", "v", "w"]):
    wire([(-0.9, y), (6.0, y)])
    ax.text(-1.1, y, name, ha="right", va="center", fontsize=8)
for x, name in zip(XOUT, ["U", "V", "W"]):
    wire([(x, 5.0), (x, -0.6)])
    ax.text(x, -0.9, name, ha="center", va="top", fontsize=8)

# --- 交点の双方向スイッチ（斜めのスイッチ記号）
S = 0.34
for x in XOUT:
    for y in YIN:
        dot(x, y)
        # スイッチ枝（点線の枠 + 斜めレバー）
        ax.add_patch(Rectangle((x - S - 0.14, y - S - 0.14),
                               2 * (S + 0.14), 2 * (S + 0.14),
                               fc="none", ec=RED, lw=0.6, ls=":",
                               zorder=2))
        ax.plot([x - S, x + S * 0.75], [y - S, y + S * 0.75], color=BK,
                lw=1.1, zorder=3)
        ax.plot([x - S], [y - S], "o", ms=2.0, mfc="white", mec=BK,
                zorder=4)

ax.text(3.4, 5.35, "双方向スイッチ×9", ha="center", fontsize=6.8,
        fontproperties=JP, color=RED)
ax.text(-0.6, 5.15, "3相入力", ha="left", fontsize=6.8, fontproperties=JP)
ax.text(5.9, -0.9, "3相出力", ha="left", va="top", fontsize=6.8,
        fontproperties=JP)

# ============ 右: 双方向スイッチの内部構成 ============
bx, by = 7.4, 1.7   # 左下基準
BW, BH = 3.3, 2.3
ax.add_patch(Rectangle((bx, by), BW, BH, fc="#f7f7f7", ec=GY, lw=0.7,
                       zorder=1))
ax.text(bx + BW / 2, by + BH + 0.22, "双方向スイッチの構成",
        ha="center", fontsize=6.6, fontproperties=JP)

ya, yb2 = by + BH - 0.62, by + 0.62   # 上枝・下枝
xa, xb = bx + 0.25, bx + BW - 0.25


def diode(x1, x2, y, direction=1):
    xc = 0.5 * (x1 + x2)
    s = 0.20
    wire([(x1, y), (xc - s * direction, y)])
    wire([(xc + s * direction, y), (x2, y)])
    ax.add_patch(Polygon([(xc - s * direction, y + s),
                          (xc - s * direction, y - s),
                          (xc + s * direction, y)], closed=True, fc=BK,
                         ec=BK, zorder=2))
    ax.plot([xc + s * direction] * 2, [y - s, y + s], color=BK, lw=1.2,
            zorder=2)


def swbox(x1, x2, y):
    xc = 0.5 * (x1 + x2)
    w, h = 0.52, 0.4
    wire([(x1, y), (xc - w / 2, y)])
    wire([(xc + w / 2, y), (x2, y)])
    ax.add_patch(Rectangle((xc - w / 2, y - h / 2), w, h, fc="white",
                           ec=BK, lw=1.0, zorder=2))
    ax.text(xc, y, "S", ha="center", va="center", fontsize=6.6)


xm = bx + BW / 2
# 上枝: 左→右に導通（スイッチ+ダイオード）
wire([(xa, ya), (xa, yb2)])
wire([(xb, ya), (xb, yb2)])
swbox(xa, xm, ya)
diode(xm, xb, ya, direction=1)
# 下枝: 右→左に導通
diode(xm, xb, yb2, direction=-1)
swbox(xa, xm, yb2)
# 端子
wire([(xa - 0.22, (ya + yb2) / 2), (xa, (ya + yb2) / 2)])
wire([(xa, ya), (xa, yb2)])
wire([(xb, (ya + yb2) / 2), (xb + 0.22, (ya + yb2) / 2)])
ax.plot([xa - 0.22], [(ya + yb2) / 2], "o", ms=2.4, mfc="white", mec=BK)
ax.plot([xb + 0.22], [(ya + yb2) / 2], "o", ms=2.4, mfc="white", mec=BK)

# 対応線（行列の1つのスイッチ → 内部構成）
wire([(XOUT[2] + S + 0.16, YIN[1]), (bx - 0.05, by + BH / 2)], c=GY,
     lw=0.5, ls=":")

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig10.5.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
