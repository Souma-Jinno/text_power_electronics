#!/usr/bin/env python3
# fig7.4（第7章）: オペアンプの負帰還。非反転入力に基準電圧V_ref，出力V_outを
# 抵抗R1・R2で分圧して反転入力へ戻す。仮想短絡でV_fb=V_refとなり，
# V_out=V_ref(1+R1/R2)に落ち着く。誤差を自動で打ち消すのが負帰還である。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BK = "#222222"
BLUE = "#2a5db0"
RED = "#c0392b"


def wire(ax, pts, c=BK):
    ax.plot([p[0] for p in pts], [p[1] for p in pts],
            color=c, lw=1.0, solid_capstyle="round", zorder=1)


def dot(ax, x, y, c=BK):
    ax.plot([x], [y], "o", ms=2.4, color=c, zorder=3)


def opamp(ax, xl, xr, yc, hh=0.85):
    # 左に底辺，右に頂点の三角形
    ax.add_patch(Polygon([(xl, yc + hh), (xl, yc - hh), (xr, yc)],
                         closed=True, fc="white", ec=BK, lw=1.1, zorder=2))
    ax.text(xl + 0.22, yc + 0.40, "$-$", ha="center", va="center", fontsize=9)
    ax.text(xl + 0.22, yc - 0.40, "$+$", ha="center", va="center", fontsize=9)


def res_v(ax, x, y1, y2, c=BK):
    yc = 0.5 * (y1 + y2)
    w, h = 0.34, 0.8
    wire(ax, [(x, y1), (x, yc + h / 2)], c)
    wire(ax, [(x, yc - h / 2), (x, y2)], c)
    ax.add_patch(Rectangle((x - w / 2, yc - h / 2), w, h,
                           fc="white", ec=c, lw=1.0, zorder=2))


def gnd(ax, x, y):
    wire(ax, [(x, y), (x, y - 0.2)])
    for i, wd in enumerate([0.34, 0.20, 0.08]):
        yy = y - 0.2 - i * 0.1
        ax.plot([x - wd / 2, x + wd / 2], [yy, yy], color=BK, lw=1.0)


fig, ax = plt.subplots(figsize=(4.0, 2.5))

# オペアンプ
xl, xr, yc = 3.0, 4.7, 2.3
opamp(ax, xl, xr, yc)
yp = yc - 0.42   # + 入力
ym = yc + 0.42   # - 入力

# + 入力：基準電圧
wire(ax, [(1.0, yp), (xl, yp)])
ax.plot([1.0], [yp], "o", ms=2.4, color=BK)
ax.text(0.8, yp, r"$V_{\mathrm{ref}}$", ha="right", va="center", fontsize=9, color=RED)

# 出力
xo = 6.2
wire(ax, [(xr, yc), (xo, yc)])
dot(ax, xo, yc)
ax.text(xo + 0.15, yc + 0.35, r"$V_{\mathrm{out}}$", ha="left", va="center", fontsize=9)

# 分圧抵抗（出力から下へ R1, R2）
ymid = 0.9
ybot = -0.4
res_v(ax, xo, yc, ymid)
ax.text(xo + 0.3, 0.5 * (yc + ymid), "$R_1$", ha="left", va="center", fontsize=8.5)
dot(ax, xo, ymid)
res_v(ax, xo, ymid, ybot)
ax.text(xo + 0.3, 0.5 * (ymid + ybot), "$R_2$", ha="left", va="center", fontsize=8.5)
gnd(ax, xo, ybot)

# フィードバック（分圧タップ→ - 入力）
wire(ax, [(xo, ymid), (2.2, ymid), (2.2, ym), (xl, ym)])
ax.text(xo - 1.4, ymid + 0.28, r"$V_{\mathrm{fb}}$", ha="center", fontsize=8.5, color=BLUE)
dot(ax, 2.2, ym)

ax.set_xlim(-0.2, 7.6)
ax.set_ylim(-1.1, 3.6)
ax.set_aspect("equal")
ax.axis("off")

fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig7.4.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
