#!/usr/bin/env python3
# fig9.1（第9章）: ハーフブリッジ回路とフルブリッジ回路の構成。
# 上下アーム（レグ）とスイッチの配置，負荷のつなぎ方を示す。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BK = "#222222"
RED = "#c0392b"
BLUE = "#2a5db0"


def wire(ax, pts, c=BK, lw=1.0):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=c, lw=lw,
            solid_capstyle="round", zorder=1)


def dot(ax, x, y, c=BK):
    ax.plot([x], [y], "o", ms=2.6, color=c, zorder=3)


def sw(ax, x, y1, y2, name, c=BK, fs=7.2):
    # 縦のスイッチ（箱）。y1下端，y2上端
    yc = 0.5 * (y1 + y2)
    w, h = 0.44, 0.70
    wire(ax, [(x, y1), (x, yc - h / 2)], c)
    wire(ax, [(x, yc + h / 2), (x, y2)], c)
    ax.add_patch(Rectangle((x - w / 2, yc - h / 2), w, h, fc="white",
                           ec=c, lw=1.0, zorder=2))
    ax.text(x, yc, name, ha="center", va="center", fontsize=fs, color=c)


def battery(ax, x, y1, y2, c=BK):
    yc = 0.5 * (y1 + y2)
    wire(ax, [(x, y1), (x, yc - 0.16)], c)
    wire(ax, [(x, yc + 0.16), (x, y2)], c)
    ax.plot([x - 0.28, x + 0.28], [yc + 0.16] * 2, color=c, lw=2.0, zorder=2)
    ax.plot([x - 0.15, x + 0.15], [yc - 0.16] * 2, color=c, lw=1.0, zorder=2)


def cap(ax, x, y1, y2, c=BK):
    yc = 0.5 * (y1 + y2)
    g = 0.10
    wire(ax, [(x, y1), (x, yc + g)], c)
    wire(ax, [(x, yc - g), (x, y2)], c)
    ax.plot([x - 0.26, x + 0.26], [yc + g] * 2, color=c, lw=1.6, zorder=2)
    ax.plot([x - 0.26, x + 0.26], [yc - g] * 2, color=c, lw=1.6, zorder=2)


def res_h(ax, x1, x2, y, c=BK):
    xc = 0.5 * (x1 + x2)
    w, h = 0.80, 0.34
    wire(ax, [(x1, y), (xc - w / 2, y)], c)
    wire(ax, [(xc + w / 2, y), (x2, y)], c)
    ax.add_patch(Rectangle((xc - w / 2, y - h / 2), w, h, fc="white",
                           ec=c, lw=1.0, zorder=2))


fig = plt.figure(figsize=(4.3, 2.4))
gs = fig.add_gridspec(1, 2, wspace=0.05)

# ---- (a) ハーフブリッジ ----
ax = fig.add_subplot(gs[0, 0])
yT, yB, yM = 3.2, 0.4, 1.8
xrail0, xrail1 = 0.8, 2.4
# レール
wire(ax, [(xrail0, yT), (xrail1, yT)])
wire(ax, [(xrail0, yB), (xrail1, yB)])
# 分割コンデンサ（左）
cap(ax, xrail0, yT, yM)
cap(ax, xrail0, yM, yB)
dot(ax, xrail0, yM)
ax.text(xrail0 - 0.34, 0.5 * (yT + yM), r"$\frac{E}{2}$", ha="right",
        va="center", fontsize=7.2)
ax.text(xrail0 - 0.34, 0.5 * (yM + yB), r"$\frac{E}{2}$", ha="right",
        va="center", fontsize=7.2)
# レグ（右）
sw(ax, xrail1, yM, yT, r"$\mathrm{S}_1$")
sw(ax, xrail1, yB, yM, r"$\mathrm{S}_2$")
dot(ax, xrail1, yM)
# 負荷
res_h(ax, xrail0, xrail1, yM)
ax.text(0.5 * (xrail0 + xrail1), yM + 0.28, "$R$", ha="center", fontsize=7.2)
ax.annotate("", xy=(0.5 * (xrail0 + xrail1) + 0.5, yM - 0.30),
            xytext=(0.5 * (xrail0 + xrail1) - 0.5, yM - 0.30),
            arrowprops=dict(arrowstyle="-|>", lw=1.0, color=RED, mutation_scale=8))
ax.text(0.5 * (xrail0 + xrail1), yM - 0.52, "$v_R$", ha="center",
        fontsize=7.0, color=RED)
ax.set_xlim(-0.2, 2.9)
ax.set_ylim(-0.4, 3.7)
ax.set_aspect("equal")
ax.axis("off")
ax.text(1.1, -0.35, "(a) ハーフブリッジ", ha="center", fontsize=7.2,
        fontproperties=JP, color="#555")

# ---- (b) フルブリッジ ----
ax = fig.add_subplot(gs[0, 1])
xS, xLegA, xLegB = 0.5, 1.9, 3.6
wire(ax, [(xS, yT), (xLegB, yT)])
wire(ax, [(xS, yB), (xLegB, yB)])
battery(ax, xS, yB, yT)
ax.text(xS - 0.42, yM, "$E$", ha="right", va="center", fontsize=7.4)
# レグA
sw(ax, xLegA, yM, yT, r"$\mathrm{S}_1$")
sw(ax, xLegA, yB, yM, r"$\mathrm{S}_2$")
dot(ax, xLegA, yM)
dot(ax, xLegA, yT)
dot(ax, xLegA, yB)
# レグB
sw(ax, xLegB, yM, yT, r"$\mathrm{S}_3$")
sw(ax, xLegB, yB, yM, r"$\mathrm{S}_4$")
dot(ax, xLegB, yM)
# 負荷
res_h(ax, xLegA, xLegB, yM)
ax.text(0.5 * (xLegA + xLegB), yM + 0.28, "$R$", ha="center", fontsize=7.2)
ax.annotate("", xy=(0.5 * (xLegA + xLegB) + 0.55, yM - 0.30),
            xytext=(0.5 * (xLegA + xLegB) - 0.55, yM - 0.30),
            arrowprops=dict(arrowstyle="-|>", lw=1.0, color=RED, mutation_scale=8))
ax.text(0.5 * (xLegA + xLegB), yM - 0.52, "$v_R$", ha="center",
        fontsize=7.0, color=RED)
ax.set_xlim(-0.3, 4.1)
ax.set_ylim(-0.4, 3.7)
ax.set_aspect("equal")
ax.axis("off")
ax.text(1.9, -0.35, "(b) フルブリッジ", ha="center", fontsize=7.2,
        fontproperties=JP, color="#555")

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig9.1.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
