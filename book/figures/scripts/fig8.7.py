#!/usr/bin/env python3
# fig8.7（第8章）: 昇圧型PFCの構成と入力電流整形。
# ダイオードブリッジ＋昇圧チョッパ（5章の再利用）で，入力電流を
# 整流電圧に相似な正弦半波に整形し，力率を1に近づける。
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
SHADE = "#eef3fb"


def wire(ax, pts, c=BK):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=c, lw=1.0,
            solid_capstyle="round", zorder=1)


def dot(ax, x, y, c=BK):
    ax.plot([x], [y], "o", ms=2.3, color=c, zorder=3)


def ind_h(ax, x1, x2, y, c=BK, n=4):
    dx = (x2 - x1) / n
    r = dx / 2
    th = np.linspace(0, np.pi, 30)
    for k in range(n):
        xc = x1 + dx * (k + 0.5)
        ax.plot(xc - r * np.cos(th), y + 0.8 * r * np.sin(th), color=c, lw=1.0, zorder=2)


def dio_v(ax, x, y1, y2, c=BK):
    yc = 0.5 * (y1 + y2)
    s = 0.24
    a = 0.66 * s
    wire(ax, [(x, y1), (x, yc - a)], c)
    wire(ax, [(x, yc + a), (x, y2)], c)
    ax.add_patch(Polygon([(x - s, yc - a), (x + s, yc - a), (x, yc + a)],
                         closed=True, fc="white", ec=c, lw=1.0, zorder=2))
    ax.plot([x - s, x + s], [yc + a, yc + a], color=c, lw=1.2, zorder=2)


def sw(ax, x, y1, y2, c=BK):
    yc = 0.5 * (y1 + y2)
    w, h = 0.5, 0.5
    wire(ax, [(x, y1), (x, yc - h / 2)], c)
    wire(ax, [(x, yc + h / 2), (x, y2)], c)
    ax.add_patch(Rectangle((x - w / 2, yc - h / 2), w, h, fc="white", ec=c, lw=1.0, zorder=2))
    ax.text(x, yc, "S", ha="center", va="center", fontsize=7, color=c)


def cap_v(ax, x, y1, y2, c=BK):
    yc = 0.5 * (y1 + y2)
    g, w = 0.10, 0.28
    wire(ax, [(x, y1), (x, yc + g)], c)
    wire(ax, [(x, yc - g), (x, y2)], c)
    ax.plot([x - w, x + w], [yc + g, yc + g], color=c, lw=1.2, zorder=2)
    ax.plot([x - w, x + w], [yc - g, yc - g], color=c, lw=1.2, zorder=2)


def res_v(ax, x, y1, y2, c=BK):
    yc = 0.5 * (y1 + y2)
    w, h = 0.32, 0.8
    wire(ax, [(x, y1), (x, yc + h / 2)], c)
    wire(ax, [(x, yc - h / 2), (x, y2)], c)
    ax.add_patch(Rectangle((x - w / 2, yc - h / 2), w, h, fc="white", ec=c, lw=1.0, zorder=2))


fig = plt.figure(figsize=(4.25, 3.05))
gs = fig.add_gridspec(2, 1, height_ratios=[1.25, 1.0], hspace=0.32)

# --- (a) 回路
ax = fig.add_subplot(gs[0])
yT, yB = 2.6, 0.6
# 交流＋ブリッジ（箱で表現）
xac = 0.55
wire(ax, [(xac, yB + 0.4), (xac, yT - 0.4)])
ax.add_patch(Circle((xac, 0.5 * (yB + yT)), 0.40, fc="white", ec=BK, lw=1.0, zorder=2))
s = np.linspace(-0.2, 0.2, 30)
ax.plot(xac + s, 0.5 * (yB + yT) + 0.13 * np.sin(s / 0.2 * np.pi), color=BK, lw=0.9, zorder=3)
ax.text(xac, yB - 0.05, "交流", ha="center", fontsize=6.4, fontproperties=JP, color="#555")
xbr = 1.55
ax.add_patch(Rectangle((xbr - 0.3, yB + 0.3), 0.6, yT - yB - 0.6,
                       fc="white", ec=BK, lw=1.0, zorder=2))
ax.plot([xbr - 0.3, xbr + 0.3], [yB + 0.3, yT - 0.3], color=BK, lw=0.8, zorder=3)
ax.text(xbr, yT + 0.12, "整流", ha="center", fontsize=6.2, fontproperties=JP, color="#555")
wire(ax, [(xac, yT - 0.4), (xac, yT), (xbr - 0.3, yT)])
wire(ax, [(xac, yB + 0.4), (xac, yB), (xbr - 0.3, yB)])
# ブリッジ出力→L→ノードA→D→出力
xL0, xL1 = 2.15, 3.35
xA = 3.9
xC = 4.9
xR = 6.1
wire(ax, [(xbr + 0.3, yT), (xL0, yT)])
ind_h(ax, xL0, xL1, yT)
wire(ax, [(xL1, yT), (xA, yT)])
dot(ax, xA, yT)
# D は A の右，横向き→ 出力へ
a = 0.24
wire(ax, [(xA, yT), (xA + 0.32, yT)])
ax.add_patch(Polygon([(xA + 0.32, yT - a), (xA + 0.32, yT + a), (xA + 0.32 + 0.36, yT)],
                     closed=True, fc="white", ec=BK, lw=1.0, zorder=2))
ax.plot([xA + 0.32 + 0.36, xA + 0.32 + 0.36], [yT - a, yT + a], color=BK, lw=1.2, zorder=2)
wire(ax, [(xA + 0.32 + 0.36, yT), (xC, yT)])
ax.text(xA + 0.5, yT + 0.28, "D", ha="center", fontsize=7)
dot(ax, xC, yT)
wire(ax, [(xC, yT), (xR, yT)])
# S: A から下へ
sw(ax, xA, yB, yT)
# 下側
wire(ax, [(xbr + 0.3, yB), (xR, yB)])
dot(ax, xA, yB)
cap_v(ax, xC, yT, yB)
ax.text(xC + 0.28, 0.5 * (yB + yT), "$C$", ha="left", va="center", fontsize=7)
res_v(ax, xR, yT, yB)
ax.text(xR + 0.28, 0.5 * (yB + yT), "負荷", ha="left", va="center", fontsize=6.4,
        fontproperties=JP)
ax.text(0.5 * (xL0 + xL1), yT + 0.30, "$L$", ha="center", fontsize=7.5)
# 制御の吹き出し
ax.text(xA + 0.15, yB - 0.55, "電流が正弦波になるよう S を制御", ha="center",
        fontsize=6.0, fontproperties=JP, color=RED)
ax.set_xlim(0, 6.7)
ax.set_ylim(-1.0, 3.7)
ax.set_aspect("equal")
ax.axis("off")
ax.text(3.3, 3.55, "(a) 昇圧型PFC（整流＋昇圧チョッパ）", ha="center", fontsize=6.8,
        fontproperties=JP, color="#555")

# --- (b) 入力電流整形
ax = fig.add_subplot(gs[1])
t = np.linspace(0, 2, 1000)
vs = np.sin(2 * np.pi * t)
ax.axhline(0, color=BK, lw=0.8)
ax.plot(t, vs, color="#9aa7bd", lw=1.1, ls="--", zorder=2)
# 入力電流: 電圧と同位相の正弦（細かいスイッチングリプルを重畳）
ig = 0.8 * vs + 0.03 * np.sin(2 * np.pi * 40 * t) * np.sign(vs)
ax.plot(t, ig, color=BLUE, lw=1.4, zorder=3)
ax.text(0.02, 1.02, r"$v_S$", fontsize=7.5, color="#888")
ax.text(0.30, 0.55, r"$i_S$（正弦波に整形）", fontsize=7, color=BLUE, fontproperties=JP)
for x in [0.5, 1.0, 1.5, 2.0]:
    ax.plot([x, x], [-0.05, 0.05], color=BK, lw=0.8)
ax.text(2.07, -0.02, r"$\omega t$", ha="left", va="top", fontsize=7)
ax.set_xlim(0, 2.2)
ax.set_ylim(-1.55, 1.25)
ax.axis("off")
ax.text(1.1, -1.35, "(b) 入力電流を電圧と同じ形にそろえる（力率$\\approx$1）",
        ha="center", fontsize=6.6, fontproperties=JP, color="#555")

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig8.7.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
