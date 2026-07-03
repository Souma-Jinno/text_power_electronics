#!/usr/bin/env python3
# fig10.2（第10章）: 交流位相調整回路。逆並列サイリスタ（トライアック）の
# 回路構成と，点弧角αによる負荷電圧波形の切り出し。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BK = "#222222"
BLUE = "#2a5db0"
RED = "#c0392b"
GY = "#999999"

fig = plt.figure(figsize=(4.25, 2.15))
gs = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.45], hspace=0.15,
                      wspace=0.06)

# ============ 左: 回路図 ============
axc = fig.add_subplot(gs[:, 0])
axc.set_xlim(-0.4, 5.4)
axc.set_ylim(-0.6, 5.2)
axc.set_aspect("equal")
axc.axis("off")


def wire(ax, pts, c=BK, lw=1.0):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=c, lw=lw,
            solid_capstyle="round", zorder=1)


def thyristor(ax, x1, x2, y, direction=1, gate_dy=0.32, label=None):
    """x1→x2 の横向きサイリスタ。direction=+1で右向き導通"""
    xc = 0.5 * (x1 + x2)
    s = 0.30
    wire(ax, [(x1, y), (xc - s * direction, y)])
    wire(ax, [(xc + s * direction, y), (x2, y)])
    tri = Polygon([(xc - s * direction, y + s), (xc - s * direction, y - s),
                   (xc + s * direction, y)], closed=True, fc=BK, ec=BK,
                  zorder=2)
    ax.add_patch(tri)
    ax.plot([xc + s * direction] * 2, [y - s, y + s], color=BK, lw=1.4,
            zorder=2)
    # ゲート
    gx = xc + s * direction
    ax.plot([gx, gx + 0.30 * direction],
            [y + (s + 0.02) * np.sign(gate_dy),
             y + (s + 0.30) * np.sign(gate_dy)], color=BK, lw=0.9, zorder=2)
    if label:
        ax.text(xc, y + (0.62 if gate_dy > 0 else -0.66), label,
                ha="center", va="center", fontsize=7)


# 電源（左）
xs, yb, yt = 0.35, 0.55, 4.15
r = 0.34
yc = 2.35
wire(axc, [(xs, yb), (xs, yc - r)])
wire(axc, [(xs, yc + r), (xs, yt)])
axc.add_patch(Circle((xs, yc), r, fc="white", ec=BK, lw=1.0, zorder=2))
th = np.linspace(0, 2 * np.pi, 80)
axc.plot(xs - 0.18 + 0.36 * th / (2 * np.pi), yc + 0.11 * np.sin(2 * th),
         color=BK, lw=0.8, zorder=3)
axc.text(xs - 0.28, yc, r"$v_S$", ha="right", va="center", fontsize=8)

# 上辺: 逆並列サイリスタ（2本の横枝）
x1, x2 = 1.15, 3.65
wire(axc, [(xs, yt), (x1, yt)])
wire(axc, [(x1, yt), (x1, yt + 0.45)])
wire(axc, [(x1, yt), (x1, yt - 0.45)])
thyristor(axc, x1, x2, yt + 0.45, direction=1, gate_dy=0.32,
          label=r"$\mathrm{T}_1$")
thyristor(axc, x1, x2, yt - 0.45, direction=-1, gate_dy=-0.32,
          label=r"$\mathrm{T}_2$")
wire(axc, [(x2, yt + 0.45), (x2, yt)])
wire(axc, [(x2, yt - 0.45), (x2, yt)])
x3 = 4.6
wire(axc, [(x2, yt), (x3, yt)])

# 負荷R（右）
wire(axc, [(x3, yt), (x3, yc + 0.55)])
axc.add_patch(Rectangle((x3 - 0.24, yc - 0.55), 0.48, 1.1, fc="white",
                        ec=BK, lw=1.0, zorder=2))
axc.text(x3 + 0.34, yc, r"$R$", ha="left", va="center", fontsize=8)
axc.text(x3 - 0.36, yc, r"$v_R$", ha="right", va="center", fontsize=8,
         color=BLUE)
wire(axc, [(x3, yc - 0.55), (x3, yb)])
wire(axc, [(xs, yb), (x3, yb)])
axc.text(2.4, -0.35, "トライアック", ha="center", va="center", fontsize=6.6,
         fontproperties=JP, color="#555")

# ============ 右: 波形 ============
V0 = 1.0
alpha = np.pi / 3
tt = np.linspace(0, 4 * np.pi, 2000)
vs = V0 * np.sin(tt)
vr = np.where(np.mod(tt, np.pi) >= alpha, vs, 0.0)


def wax(ax, label):
    ax.annotate("", xy=(4 * np.pi + 1.0, 0), xytext=(-0.4, 0),
                arrowprops=dict(arrowstyle="-|>", lw=0.8, color=BK,
                                mutation_scale=8))
    ax.plot([0, 0], [-1.25, 1.25], color=BK, lw=0.8)
    for x in [np.pi, 2 * np.pi, 3 * np.pi, 4 * np.pi]:
        ax.plot([x, x], [-1.15, 1.15], color=GY, lw=0.5, ls=":")
    ax.text(-0.5, 1.15, label, ha="right", va="center", fontsize=8,
            color=BK)
    ax.text(4 * np.pi + 1.1, -0.35, r"$\theta$", fontsize=7.5)
    ax.set_xlim(-2.3, 4 * np.pi + 1.6)
    ax.set_ylim(-1.75, 1.55)
    ax.axis("off")


ax1 = fig.add_subplot(gs[0, 1])
wax(ax1, r"$v_S$")
ax1.plot(tt, vs, color=BK, lw=1.1)
ax1.text(2 * np.pi, 1.45, r"$v_S = V_0 \sin\theta$", ha="center",
         fontsize=7)
ax1.text(np.pi, -1.55, r"$\pi$", ha="center", fontsize=6.6)
ax1.text(2 * np.pi, -1.55, r"$2\pi$", ha="center", fontsize=6.6)

ax2 = fig.add_subplot(gs[1, 1])
wax(ax2, r"$v_R$")
ax2.plot(tt, vr, color=BLUE, lw=1.2, zorder=3)
ax2.plot(tt, vs, color=GY, lw=0.6, ls="--", zorder=2)
# 点弧角の表示
for k in range(4):
    x0 = k * np.pi
    ax2.annotate("", xy=(x0 + alpha, -1.38), xytext=(x0, -1.38),
                 arrowprops=dict(arrowstyle="-|>", lw=0.8, color=RED,
                                 mutation_scale=7))
ax2.text(alpha / 2, -1.72, r"$\alpha$", ha="center", fontsize=7.5,
         color=RED)
ax2.text(np.pi + alpha / 2, -1.72, r"$\pi+\alpha$", ha="center",
         fontsize=6.6, color=RED)

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig10.2.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
