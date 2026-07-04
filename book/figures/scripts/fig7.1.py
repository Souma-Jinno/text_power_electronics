#!/usr/bin/env python3
# fig7.1（第7章）: リニアレギュレータの原理。入力電源V0と負荷RLの間に
# 直列に可変抵抗Rxを入れ，Rxで余分な電圧を落として出力Voutを作る。
# 落とした電圧×電流がそのままRxでの発熱（損失）になる。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
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


def source(ax, x, ybot, ytop, c=BK):
    r = 0.34
    yc = 0.5 * (ybot + ytop)
    wire(ax, [(x, ybot), (x, yc - r)], c)
    wire(ax, [(x, yc + r), (x, ytop)], c)
    ax.add_patch(Circle((x, yc), r, fc="white", ec=c, lw=1.0, zorder=2))
    ax.text(x, yc + 0.14, "$+$", ha="center", va="center", fontsize=6, color=c)
    ax.text(x, yc - 0.15, "$-$", ha="center", va="center", fontsize=6, color=c)


def varres_h(ax, x1, x2, y, c=BK):
    # 可変抵抗（横向き）：矩形に斜め矢印を貫かせる
    xc = 0.5 * (x1 + x2)
    w, h = 1.1, 0.46
    wire(ax, [(x1, y), (xc - w / 2, y)], c)
    wire(ax, [(xc + w / 2, y), (x2, y)], c)
    ax.add_patch(Rectangle((xc - w / 2, y - h / 2), w, h,
                           fc="white", ec=c, lw=1.0, zorder=2))
    ax.annotate("", xy=(xc + 0.45, y + 0.5), xytext=(xc - 0.45, y - 0.5),
                arrowprops=dict(arrowstyle="-|>", lw=1.1, color=c,
                                mutation_scale=9), zorder=4)


def res_v(ax, x, y1, y2, c=BK):
    yc = 0.5 * (y1 + y2)
    w, h = 0.36, 0.95
    wire(ax, [(x, y1), (x, yc + h / 2)], c)
    wire(ax, [(x, yc - h / 2), (x, y2)], c)
    ax.add_patch(Rectangle((x - w / 2, yc - h / 2), w, h,
                           fc="white", ec=c, lw=1.0, zorder=2))


def iarr(ax, x, y, dx, dy, c=RED):
    ax.annotate("", xy=(x + dx, y + dy), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", lw=1.1, color=c,
                                mutation_scale=8), zorder=4)


fig, ax = plt.subplots(figsize=(3.9, 2.15))

yT, yB = 2.9, 0.6
xV = 0.7
xRx0, xRx1 = 1.7, 4.4
xN = 5.2          # 出力ノード
xR = 6.6          # 負荷

# 上側の配線
wire(ax, [(xV, yT), (xRx0, yT)])
varres_h(ax, xRx0, xRx1, yT)
wire(ax, [(xRx1, yT), (xR, yT)])
dot(ax, xN, yT)
# 下側の配線
wire(ax, [(xV, yB), (xR, yB)])
dot(ax, xN, yB)

# 素子
source(ax, xV, yB, yT)
ax.text(xV - 0.5, 0.5 * (yB + yT), r"$V_0$", ha="right", va="center", fontsize=9)
res_v(ax, xR, yT, yB)
ax.text(xR - 0.34, 0.5 * (yB + yT), r"$R_L$", ha="right", va="center", fontsize=9)

# ラベル
ax.text(0.5 * (xRx0 + xRx1), yT + 0.62, r"$R_x$", ha="center", fontsize=9, color=RED)
ax.text(0.5 * (xRx0 + xRx1), yT - 0.66, r"$V_0-V_{\mathrm{out}}$",
        ha="center", fontsize=7.5, color=RED)
# 出力電圧の表示（負荷の右）
xvo = xR + 1.05
ax.text(xvo, yT - 0.42, "$+$", ha="center", fontsize=7)
ax.text(xvo, 0.5 * (yB + yT), r"$V_{\mathrm{out}}$",
        ha="center", va="center", fontsize=9)
ax.text(xvo, yB + 0.42, "$-$", ha="center", fontsize=7)
# 電流
iarr(ax, 4.7, yT, 0.35, 0, c=BLUE)
ax.text(4.9, yT + 0.26, "$I$", ha="center", fontsize=8, color=BLUE)

ax.set_xlim(-1.0, 8.5)
ax.set_ylim(-0.2, 3.9)
ax.set_aspect("equal")
ax.axis("off")

fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig7.1.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
