#!/usr/bin/env python3
# fig11.4（第11章）: 平行配線の寄生成分。
# (a) 往復電流のつくる磁場 → 寄生インダクタンス L'
# (b) 導体上の電荷のつくる電場 → 寄生キャパシタンス C'
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
GY = "#b8b8b8"
BLUE = "#2a5db0"
RED = "#c0392b"
GRN = "#1e8449"
MAG = "#c2399b"

yT, yB = 2.0, 0.6
x0, x1 = 0.3, 4.6


def wires(ax):
    for yy in (yT, yB):
        ax.add_patch(Rectangle((x0, yy - 0.09), x1 - x0, 0.18,
                               fc=GY, ec="#777", lw=0.6, zorder=1))


def arrow(ax, x, y, dx, dy, c, lw=1.1, ms=8):
    ax.annotate("", xy=(x + dx, y + dy), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", lw=lw, color=c,
                                mutation_scale=ms), zorder=4)


def coil_h(ax, xa, xb, y, c=BK, n=4):
    dx = (xb - xa) / n
    r = dx / 2
    t = np.linspace(0, np.pi, 30)
    for k in range(n):
        xc = xa + dx * (k + 0.5)
        ax.plot(xc - r * np.cos(t), y + 0.9 * r * np.sin(t), color=c, lw=1.0)


def cap_v(ax, x, y1, y2, c=BK):
    yc = 0.5 * (y1 + y2)
    g, w = 0.10, 0.30
    ax.plot([x, x], [y1, yc + g], color=c, lw=1.0)
    ax.plot([x, x], [yc - g, y2], color=c, lw=1.0)
    ax.plot([x - w, x + w], [yc + g, yc + g], color=c, lw=1.2)
    ax.plot([x - w, x + w], [yc - g, yc - g], color=c, lw=1.2)


fig, axes = plt.subplots(1, 2, figsize=(4.25, 2.15))

# ---- (a) 磁場 → L' ----
ax = axes[0]
wires(ax)
for xx in np.linspace(0.8, 4.1, 3):
    arrow(ax, xx - 0.25, yT, 0.5, 0, RED)
    arrow(ax, xx + 0.25, yB, -0.5, 0, BLUE)
for xx in np.linspace(0.75, 4.15, 5):
    for yy in (1.5, 1.1):
        ax.text(xx, yy, r"$\otimes$", ha="center", va="center",
                fontsize=7.5, color=GRN)
ax.text(4.75, yT, "$+I$", ha="left", va="center", fontsize=8, color=RED)
ax.text(4.75, yB, "$-I$", ha="left", va="center", fontsize=8, color=BLUE)
ax.text(2.45, 1.30, "$B$", ha="center", va="center", fontsize=8, color=GRN,
        bbox=dict(fc="white", ec="none", pad=0.5))
# 等価回路
yE = -0.75
ax.plot([x0, 1.7], [yE, yE], color=BK, lw=1.0)
coil_h(ax, 1.7, 3.1, yE)
ax.plot([3.1, x1], [yE, yE], color=BK, lw=1.0)
ax.text(3.35, yE + 0.34, r"$L'$ [H/m]", ha="left", fontsize=7.5)
arrow(ax, 2.4, 0.18, 0, -0.55, BK, lw=0.8, ms=7)
ax.set_xlim(-0.3, 5.8)
ax.set_ylim(-2.05, 2.6)
ax.set_aspect("equal")
ax.axis("off")
ax.text(2.45, -1.95, "(a) 電流→磁場→寄生インダクタンス", ha="center",
        fontsize=6.6, fontproperties=JP, color="#555")

# ---- (b) 電場 → C' ----
ax = axes[1]
wires(ax)
for xx in np.linspace(0.8, 4.1, 4):
    ax.add_patch(Circle((xx, yT), 0.13, fc="white", ec=RED, lw=0.9, zorder=3))
    ax.text(xx, yT, "$+$", ha="center", va="center", fontsize=6, color=RED, zorder=4)
    ax.add_patch(Circle((xx, yB), 0.13, fc="white", ec=BLUE, lw=0.9, zorder=3))
    ax.text(xx, yB, "$-$", ha="center", va="center", fontsize=6, color=BLUE, zorder=4)
    arrow(ax, xx, yT - 0.26, 0, -(yT - yB - 0.62), MAG, lw=0.9, ms=6)
ax.text(4.75, yT, "$+q$", ha="left", va="center", fontsize=8, color=RED)
ax.text(4.75, yB, "$-q$", ha="left", va="center", fontsize=8, color=BLUE)
ax.text(2.45, 1.30, "$E$", ha="center", va="center", fontsize=8, color=MAG,
        bbox=dict(fc="white", ec="none", pad=0.5))
# 等価回路
yE1, yE2 = -0.35, -1.15
ax.plot([x0, x1], [yE1, yE1], color=BK, lw=1.0)
ax.plot([x0, x1], [yE2, yE2], color=BK, lw=1.0)
cap_v(ax, 2.4, yE1, yE2)
ax.text(2.85, 0.5 * (yE1 + yE2), r"$C'$ [F/m]", ha="left", fontsize=7.5)
arrow(ax, 2.4, 0.18, 0, -0.35, BK, lw=0.8, ms=7)
ax.set_xlim(-0.3, 5.8)
ax.set_ylim(-2.05, 2.6)
ax.set_aspect("equal")
ax.axis("off")
ax.text(2.45, -1.95, "(b) 電荷→電場→寄生キャパシタンス", ha="center",
        fontsize=6.6, fontproperties=JP, color="#555")

fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig11.4.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
