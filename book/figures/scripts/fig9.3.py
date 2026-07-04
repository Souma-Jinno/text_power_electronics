#!/usr/bin/env python3
# fig9.3（第9章）: デッドタイムと還流ダイオード。
# (a)上下アームのゲート信号とデッドタイム（両方オフの期間），
# (b)デッドタイム中に誘導性負荷の電流が還流ダイオードを通る経路。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BK = "#222222"
RED = "#c0392b"
BLUE = "#2a5db0"
GY = "#b8b8b8"
ORG = "#e08a1e"


def wire(ax, pts, c=BK, lw=1.0):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=c, lw=lw,
            solid_capstyle="round", zorder=1)


def dot(ax, x, y, c=BK):
    ax.plot([x], [y], "o", ms=2.6, color=c, zorder=3)


fig = plt.figure(figsize=(4.3, 2.2))
gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.0], wspace=0.15)

# ---- (a) ゲート信号とデッドタイム ----
ax = fig.add_subplot(gs[0, 0])
td = 0.06
# S1（上アーム）: onを 0.05..0.5-td, 0.55..1.0-td ...（周期0.5で交互）
def gate(ax, y0, on_intervals, c=BK, label=""):
    ax.plot([-0.02, 1.05], [y0, y0], color=BK, lw=0.7)
    ax.text(-0.05, y0 + 0.18, label, ha="right", va="center", fontsize=7, color=c)
    for (a, b) in on_intervals:
        ax.plot([a, a], [y0, y0 + 0.36], color=c, lw=1.3)
        ax.plot([a, b], [y0 + 0.36, y0 + 0.36], color=c, lw=1.3)
        ax.plot([b, b], [y0 + 0.36, y0], color=c, lw=1.3)

s1 = [(0.02, 0.5 - td), (0.52 + td, 1.0)]
s2 = [(0.5 + td, 1.0 - td)]
gate(ax, 0.9, s1, RED, r"$\mathrm{S}_1$")
gate(ax, 0.1, s2, BLUE, r"$\mathrm{S}_2$")
# デッドタイム帯
for x in [0.5 - td, 0.5, 1.0 - td, 1.0]:
    pass
for a in [0.5 - td, 1.0 - td]:
    ax.add_patch(Rectangle((a, -0.05), 2 * td, 1.4, fc="#fbe3c0", ec="none",
                           zorder=0))
ax.annotate("", xy=(0.5 + td, 1.38), xytext=(0.5 - td, 1.38),
            arrowprops=dict(arrowstyle="<->", lw=0.8, color=BK, mutation_scale=6))
ax.text(0.5, 1.52, r"デッドタイム $t_d$", ha="center", fontsize=6.4,
        fontproperties=JP, color="#333")
ax.text(0.5, -0.28, "両アームがオフ", ha="center", fontsize=6.0,
        fontproperties=JP, color="#a0630a")
ax.set_xlim(-0.15, 1.1)
ax.set_ylim(-0.4, 1.7)
ax.axis("off")
ax.text(0.5, -0.55, "(a) ゲート信号", ha="center", fontsize=7.0,
        fontproperties=JP, color="#555")

# ---- (b) 還流経路（1レグ） ----
ax = fig.add_subplot(gs[0, 1])
yT, yB, yM = 3.0, 0.4, 1.7
xL, xLoad = 1.4, 3.0


def swbox(ax, x, y1, y2, name, c=BK):
    yc = 0.5 * (y1 + y2)
    w, h = 0.42, 0.62
    wire(ax, [(x, y1), (x, yc - h / 2)], c)
    wire(ax, [(x, yc + h / 2), (x, y2)], c)
    ax.add_patch(Rectangle((x - w / 2, yc - h / 2), w, h, fc="white", ec=c,
                           lw=1.0, zorder=2))
    ax.text(x, yc, name, ha="center", va="center", fontsize=6.6, color=c)


def diode(ax, x, y1, y2, c=BK, hot=False):
    # アノード下→カソード上（上向き導通）。逆並列ダイオード
    yc = 0.5 * (y1 + y2)
    s, a = 0.20, 0.20
    cc = RED if hot else c
    wire(ax, [(x, y1), (x, yc - a)], cc, lw=1.6 if hot else 1.0)
    wire(ax, [(x, yc + a), (x, y2)], cc, lw=1.6 if hot else 1.0)
    ax.add_patch(Polygon([(x - s, yc - a), (x + s, yc - a), (x, yc + a)],
                         closed=True, fc="white", ec=cc, lw=1.0, zorder=2))
    ax.plot([x - s, x + s], [yc + a] * 2, color=cc, lw=1.4, zorder=2)


wire(ax, [(xL - 0.6, yT), (xL + 0.6, yT)])
wire(ax, [(xL - 0.6, yB), (xL + 0.6, yB)])
ax.text(xL - 0.6, yT + 0.16, "$+$", ha="center", fontsize=6.4)
ax.text(xL - 0.6, yB - 0.20, "$-$", ha="center", fontsize=6.4)
# スイッチ（グレー＝オフ）と逆並列ダイオード
swbox(ax, xL, yM, yT, r"$\mathrm{S}_1$", GY)
swbox(ax, xL, yB, yM, r"$\mathrm{S}_2$", GY)
diode(ax, xL + 0.5, yM, yT, BK, hot=False)
diode(ax, xL + 0.5, yB, yM, BK, hot=True)   # D2が還流
wire(ax, [(xL, yT), (xL + 0.5, yT)])
wire(ax, [(xL, yB), (xL + 0.5, yB)])
wire(ax, [(xL, yM), (xL + 0.5, yM)])
dot(ax, xL, yM)
dot(ax, xL + 0.5, yM)
# 負荷（誘導性）へ
wire(ax, [(xL + 0.5, yM), (xLoad, yM)])
ax.text(xLoad + 0.05, yM, "誘導性\n負荷へ", ha="left", va="center", fontsize=5.8,
        fontproperties=JP)
# 還流電流の矢印（赤）: 負荷→ノード→D2→下レール
ax.annotate("", xy=(xL + 0.5, yM - 0.02), xytext=(xLoad - 0.3, yM - 0.02),
            arrowprops=dict(arrowstyle="-|>", lw=1.3, color=RED, mutation_scale=8))
ax.annotate("", xy=(xL + 0.5, yB + 0.35), xytext=(xL + 0.5, yM - 0.35),
            arrowprops=dict(arrowstyle="-|>", lw=1.3, color=RED, mutation_scale=8))
ax.text(xL + 0.5, 1.02, r"$\mathrm{D}_2$", ha="left", va="center", fontsize=6.4,
        color=RED)
ax.set_xlim(0.5, 4.0)
ax.set_ylim(-0.2, 3.5)
ax.set_aspect("equal")
ax.axis("off")
ax.text(2.1, -0.55, "(b) デッドタイム中の還流", ha="center", fontsize=7.0,
        fontproperties=JP, color="#555")

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig9.3.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
