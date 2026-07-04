#!/usr/bin/env python3
# fig8.1（第8章）: 半波整流回路と動作波形。
# 交流電源+ダイオード+抵抗負荷。正の半周期だけが負荷に現れる。
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
    ax.plot([x], [y], "o", ms=2.4, color=c, zorder=3)


def acsource(ax, x, ybot, ytop, c=BK):
    r = 0.42
    yc = 0.5 * (ybot + ytop)
    wire(ax, [(x, ybot), (x, yc - r)], c)
    wire(ax, [(x, yc + r), (x, ytop)], c)
    ax.add_patch(Circle((x, yc), r, fc="white", ec=c, lw=1.0, zorder=2))
    s = np.linspace(-0.22, 0.22, 40)
    ax.plot(x + s, yc + 0.14 * np.sin(s / 0.22 * np.pi), color=c, lw=0.9, zorder=3)


def dio_h(ax, x1, x2, y, c=BK):
    xc = 0.5 * (x1 + x2)
    s = 0.26
    a = 0.7 * s
    wire(ax, [(x1, y), (xc - a, y)], c)
    wire(ax, [(xc + a, y), (x2, y)], c)
    ax.add_patch(Polygon([(xc - a, y - s), (xc - a, y + s), (xc + a, y)],
                         closed=True, fc="white", ec=c, lw=1.0, zorder=2))
    ax.plot([xc + a, xc + a], [y - s, y + s], color=c, lw=1.2, zorder=2)


def res_v(ax, x, y1, y2, c=BK):
    yc = 0.5 * (y1 + y2)
    w, h = 0.36, 0.95
    wire(ax, [(x, y1), (x, yc + h / 2)], c)
    wire(ax, [(x, yc - h / 2), (x, y2)], c)
    ax.add_patch(Rectangle((x - w / 2, yc - h / 2), w, h,
                           fc="white", ec=c, lw=1.0, zorder=2))


fig = plt.figure(figsize=(4.2, 2.55))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.25], wspace=0.05)

# --- (a) 回路
ax = fig.add_subplot(gs[0, 0])
yT, yB = 2.7, 0.5
xS, xD0, xD1, xR = 0.7, 1.7, 2.7, 3.5
wire(ax, [(xS, yT), (xD0, yT)])
dio_h(ax, xD0, xD1, yT)
wire(ax, [(xD1, yT), (xR, yT)])
wire(ax, [(xS, yB), (xR, yB)])
acsource(ax, xS, yB, yT)
ax.text(xS - 0.55, 0.5 * (yB + yT), r"$v_S$", ha="right", va="center", fontsize=8)
res_v(ax, xR, yT, yB)
ax.text(xR - 0.30, 0.5 * (yB + yT), "$R$", ha="right", va="center", fontsize=8)
ax.text(xR + 0.72, yT - 0.35, "$+$", ha="center", fontsize=7)
ax.text(xR + 0.72, 0.5 * (yB + yT), r"$v_R$", ha="center", va="center", fontsize=8)
ax.text(xR + 0.72, yB + 0.35, "$-$", ha="center", fontsize=7)
ax.text(0.5 * (xD0 + xD1), yT + 0.34, "D", ha="center", fontsize=8)
ax.set_xlim(-0.7, 4.6)
ax.set_ylim(-0.2, 3.5)
ax.set_aspect("equal")
ax.axis("off")
ax.text(1.9, -0.15, "(a) 回路", ha="center", fontsize=7.0,
        fontproperties=JP, color="#555")

# --- (b) 波形
ax = fig.add_subplot(gs[0, 1])
t = np.linspace(0, 2, 1000)
vs = np.sin(2 * np.pi * t)
vr = np.where(vs > 0, vs, 0)
ax.axhline(0, color=BK, lw=0.8)
ax.plot(t, vs, color="#9aa7bd", lw=1.0, ls="--", zorder=2)
ax.fill_between(t, 0, vr, color=SHADE, zorder=1)
ax.plot(t, vr, color=BLUE, lw=1.5, zorder=3)
ax.text(0.25, 1.13, r"$v_S=V_m\sin\omega t$", ha="left", fontsize=7, color="#666")
ax.text(1.30, 0.72, r"$v_R$", ha="left", fontsize=8, color=BLUE)
for x in [0.5, 1.0, 1.5, 2.0]:
    ax.plot([x, x], [-0.05, 0.05], color=BK, lw=0.8)
ax.text(1.0, -0.20, r"$\pi$", ha="center", va="top", fontsize=7)
ax.text(2.0, -0.20, r"$2\pi$", ha="center", va="top", fontsize=7)
ax.text(2.08, -0.02, r"$\omega t$", ha="left", va="top", fontsize=7)
ax.set_xlim(0, 2.2)
ax.set_ylim(-1.25, 1.35)
ax.axis("off")
ax.text(1.1, -0.55, "(b) 電圧波形", ha="center", fontsize=7.0,
        fontproperties=JP, color="#555")

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig8.1.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
