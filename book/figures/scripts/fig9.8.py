#!/usr/bin/env python3
# fig9.8（第9章）: ハイサイド駆動のためのブートストラップ回路。
# 下アームQ2がオンの間にVccからD_bootを通してC_bootを充電し（赤の経路），
# その電荷でハイサイドQ1のゲート電源（浮いた基準VS上のVB）をまかなう。
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


def wire(ax, pts, c=BK, lw=1.0):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=c, lw=lw,
            solid_capstyle="round", zorder=1)


def dot(ax, x, y, c=BK):
    ax.plot([x], [y], "o", ms=2.8, color=c, zorder=4)


def mosfet(ax, x, y1, y2, name, c=BK):
    yc = 0.5 * (y1 + y2)
    w, h = 0.6, 0.9
    wire(ax, [(x, y1), (x, yc - h / 2)], c)
    wire(ax, [(x, yc + h / 2), (x, y2)], c)
    ax.add_patch(Rectangle((x - w / 2, yc - h / 2), w, h, fc="white", ec=c,
                           lw=1.0, zorder=2))
    ax.text(x, yc, name, ha="center", va="center", fontsize=7.6, color=c)


def diode_r(ax, x1, x2, y, c=BK, lw=1.7):
    xc = 0.5 * (x1 + x2)
    s = 0.17
    wire(ax, [(x1, y), (xc - s, y)], c, lw)
    wire(ax, [(xc + s, y), (x2, y)], c, lw)
    ax.add_patch(Polygon([(xc - s, y - s), (xc - s, y + s), (xc + s, y)],
                         closed=True, fc="white", ec=c, lw=1.0, zorder=2))
    ax.plot([xc + s, xc + s], [y - s, y + s], color=c, lw=1.5, zorder=2)


def cap_v(ax, x, y1, y2, c=BK, lw=1.7):
    yc = 0.5 * (y1 + y2)
    g = 0.13
    wire(ax, [(x, y1), (x, yc + g)], c, lw)
    wire(ax, [(x, yc - g), (x, y2)], c, lw)
    ax.plot([x - 0.24, x + 0.24], [yc + g] * 2, color=c, lw=1.6, zorder=2)
    ax.plot([x - 0.24, x + 0.24], [yc - g] * 2, color=c, lw=1.6, zorder=2)


fig, ax = plt.subplots(figsize=(4.1, 2.5))

# ---- レグ（右） ----
yT, yB, yVS = 3.5, 0.5, 2.0
xLeg = 6.2
wire(ax, [(xLeg, yT), (xLeg + 0.7, yT)])
wire(ax, [(xLeg, yB), (xLeg + 0.7, yB)])
ax.text(xLeg + 0.75, yT, r"$+E$", ha="left", va="center", fontsize=7.2)
ax.text(xLeg + 0.75, yB, "GND", ha="left", va="center", fontsize=6.6)
mosfet(ax, xLeg, yVS, yT, r"$\mathrm{Q}_1$")
mosfet(ax, xLeg, yB, yVS, r"$\mathrm{Q}_2$")
dot(ax, xLeg, yVS)
wire(ax, [(xLeg, yVS), (xLeg + 1.1, yVS)])
ax.text(xLeg + 1.15, yVS, "負荷へ", ha="left", va="center", fontsize=6.4,
        fontproperties=JP)

# ---- ドライバIC ----
xIC = 1.6
ax.add_patch(Rectangle((xIC - 0.85, 1.15), 1.7, 2.0, fc="#f2f2f2", ec=BK, lw=1.0))
ax.text(xIC, 2.95, "ドライバ", ha="center", fontsize=6.8, fontproperties=JP)
pins = {"VB": 2.55, "HO": 2.15, "VS": 1.75, "LO": 1.4}
for nm, yy in pins.items():
    ax.text(xIC + 0.78, yy, nm, ha="right", va="center", fontsize=5.8, color="#555")
# VCCピン（左）
ax.text(xIC - 0.78, 2.55, "VCC", ha="left", va="center", fontsize=5.8, color="#555")

# ---- Vcc電源 ----
xVcc = 0.0
wire(ax, [(xVcc, 2.55), (xIC - 0.85, 2.55)])
ax.text(xVcc - 0.05, 2.55, r"$V_{cc}$", ha="right", va="center", fontsize=7.2)
dot(ax, 0.55, 2.55)
# GND
wire(ax, [(xVcc, 1.55), (xVcc, 0.15), (xLeg + 0.7, 0.15), (xLeg + 0.7, yB)])
ax.text(xVcc - 0.05, 1.55, "GND", ha="right", va="center", fontsize=6.0)
wire(ax, [(xVcc, 1.55), (xIC - 0.85, 1.55)])

# ---- ブートストラップ回路（中央の柱：xBoot） ----
xBoot = 4.3
yTop = 3.35
# Vcc → 上へ → Dboot（右向き）→ VBノード
wire(ax, [(0.55, 2.55), (0.55, yTop)], RED, 1.9)
wire(ax, [(0.55, yTop), (xBoot - 0.6, yTop)], RED, 1.9)
diode_r(ax, xBoot - 0.6, xBoot, yTop, RED, 1.9)
ax.text(xBoot - 0.3, yTop + 0.2, r"$\mathrm{D}_{boot}$", ha="center",
        fontsize=6.4, color=RED)
# VB柱（上側，Cbootの上まで）とVS柱（下側，Cbootの下から）
wire(ax, [(xBoot, yTop), (xBoot, 2.85)], RED, 1.9)
wire(ax, [(xBoot, 1.9), (xBoot, 1.4)], RED, 1.9)
dot(ax, xBoot, yTop, RED)
# Cboot（VB柱とVS帰線の間）
cap_v(ax, xBoot, 2.85, 1.9, RED, 1.9)
ax.text(xBoot + 0.28, 2.35, r"$C_{boot}$", ha="left", va="center",
        fontsize=6.6, color=RED)
# VBを駆動ICのVBピンへ
wire(ax, [(xBoot, yTop), (xBoot + 0.0, yTop)])
wire(ax, [(xIC + 0.85, 2.55), (xBoot, 2.55)])
dot(ax, xBoot, 2.55)
# VSノード（下側の横線）：Cboot下端→VSピン→レグ中点
yVSline = 1.4
wire(ax, [(xBoot, yVSline), (xLeg, yVSline)], RED, 1.9)
wire(ax, [(xLeg, yVSline), (xLeg, yVS)], RED, 1.9)
dot(ax, xLeg, yVS, RED)
wire(ax, [(xIC + 0.85, 1.75), (xBoot - 0.9, 1.75), (xBoot - 0.9, yVSline),
          (xBoot, yVSline)])
dot(ax, xBoot, yVSline, RED)

# ゲート配線（HO→Q1, LO→Q2）短いスタブ
wire(ax, [(xIC + 0.85, 2.15), (2.9, 2.15), (2.9, 2.75)])
ax.text(2.95, 2.78, "→$\\mathrm{Q}_1$", ha="left", va="center", fontsize=5.8)
wire(ax, [(xIC + 0.85, 1.4), (2.6, 1.4), (2.6, 0.9)])
ax.text(2.65, 0.85, "→$\\mathrm{Q}_2$", ha="left", va="center", fontsize=5.8)

# 充電経路の説明矢印
ax.annotate("", xy=(xBoot - 0.6, yTop), xytext=(xBoot - 1.4, yTop),
            arrowprops=dict(arrowstyle="-|>", lw=1.4, color=RED, mutation_scale=9))
ax.text(xBoot, 0.55, r"赤：$\mathrm{Q}_2$オン時の充電経路", ha="center",
        fontsize=6.2, fontproperties=JP, color=RED)

ax.set_xlim(-0.9, 8.0)
ax.set_ylim(0.0, 3.8)
ax.set_aspect("equal")
ax.axis("off")

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig9.8.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
