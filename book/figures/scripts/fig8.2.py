#!/usr/bin/env python3
# fig8.2（第8章）: ダイオードブリッジ全波整流回路と出力波形。
# 4個のダイオードで交流の両半周期を同じ向きに整流する。
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


def dio(ax, x, y, ang, c=BK):
    # アノード→カソードが角度 ang(度) 方向。中心(x,y)。
    s = 0.24
    a = 0.62 * s
    th = np.radians(ang)
    ux, uy = np.cos(th), np.sin(th)
    px, py = -uy, ux
    tip = (x + a * ux, y + a * uy)
    b1 = (x - a * ux + s * px, y - a * uy + s * py)
    b2 = (x - a * ux - s * px, y - a * uy - s * py)
    ax.add_patch(Polygon([b1, b2, tip], closed=True, fc="white", ec=c, lw=1.0, zorder=2))
    ax.plot([tip[0] + s * px, tip[0] - s * px], [tip[1] + s * py, tip[1] - s * py],
            color=c, lw=1.2, zorder=2)


def res_v(ax, x, y1, y2, c=BK):
    yc = 0.5 * (y1 + y2)
    w, h = 0.34, 0.9
    wire(ax, [(x, y1), (x, yc + h / 2)], c)
    wire(ax, [(x, yc - h / 2), (x, y2)], c)
    ax.add_patch(Rectangle((x - w / 2, yc - h / 2), w, h,
                           fc="white", ec=c, lw=1.0, zorder=2))


fig = plt.figure(figsize=(4.2, 2.5))
gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.1], wspace=0.08)

# --- (a) ブリッジ回路（ひし形）
ax = fig.add_subplot(gs[0, 0])
cx, cy, d = 2.2, 1.7, 1.05          # ひし形中心と半対角
L, R = cx - d, cx + d               # 左・右ノード（交流入力）
Tn, Bn = cy + d, cy - d             # 上・下ノード（直流出力）
# ひし形の枝
wire(ax, [(L, cy), (cx, Tn)]); wire(ax, [(cx, Tn), (R, cy)])
wire(ax, [(L, cy), (cx, Bn)]); wire(ax, [(cx, Bn), (R, cy)])
dio(ax, 0.5 * (L + cx), 0.5 * (cy + Tn), 45)     # D1 左上（L→上，カソード上）
dio(ax, 0.5 * (cx + R), 0.5 * (Tn + cy), 135)    # D2 右上（R→上）
dio(ax, 0.5 * (L + cx), 0.5 * (Bn + cy), 135)    # D3 左下（下→L）
dio(ax, 0.5 * (cx + R), 0.5 * (cy + Bn), 45)     # D4 右下（下→R）
ax.text(0.5 * (L + cx) - 0.28, 0.5 * (cy + Tn) + 0.20, "$D_1$", fontsize=7, ha="center")
ax.text(0.5 * (cx + R) + 0.28, 0.5 * (Tn + cy) + 0.20, "$D_2$", fontsize=7, ha="center")
ax.text(0.5 * (L + cx) - 0.28, 0.5 * (Bn + cy) - 0.20, "$D_3$", fontsize=7, ha="center")
ax.text(0.5 * (cx + R) + 0.28, 0.5 * (cy + Bn) - 0.20, "$D_4$", fontsize=7, ha="center")
dot(ax, L, cy); dot(ax, R, cy); dot(ax, cx, Tn); dot(ax, cx, Bn)
# 交流電源（左）
xS = 0.35
wire(ax, [(xS, cy + 1.0), (L, cy + 1.0)]); wire(ax, [(L, cy + 1.0), (L, cy)])
wire(ax, [(xS, cy - 1.0), (R - 0.0, cy - 1.0)])
wire(ax, [(xS, cy + 1.0), (xS, cy + 0.42)]); wire(ax, [(xS, cy - 1.0), (xS, cy - 0.42)])
ax.add_patch(Circle((xS, cy), 0.42, fc="white", ec=BK, lw=1.0, zorder=2))
s = np.linspace(-0.22, 0.22, 40)
ax.plot(xS + s, cy + 0.14 * np.sin(s / 0.22 * np.pi), color=BK, lw=0.9, zorder=3)
# ここで下側の線を R ノードへ回す
wire(ax, [(R, cy - 1.0), (R, cy)])
ax.text(xS - 0.32, cy, r"$v_S$", ha="right", va="center", fontsize=8)
# 出力（上ノード→R→下ノード）
xout = R + 1.15
wire(ax, [(cx, Tn), (xout, Tn)]); wire(ax, [(cx, Bn), (xout, Bn)])
res_v(ax, xout, Tn, Bn)
ax.text(xout - 0.28, cy, "$R$", ha="right", va="center", fontsize=8)
ax.text(xout + 0.62, Tn - 0.30, "$+$", ha="center", fontsize=7)
ax.text(xout + 0.62, cy, r"$v_R$", ha="center", va="center", fontsize=8)
ax.text(xout + 0.62, Bn + 0.30, "$-$", ha="center", fontsize=7)
ax.set_xlim(-0.4, xout + 1.1)
ax.set_ylim(cy - 1.5, cy + 1.5)
ax.set_aspect("equal")
ax.axis("off")
ax.text(cx, cy - 1.75, "(a) ブリッジ回路", ha="center", fontsize=7.0,
        fontproperties=JP, color="#555")

# --- (b) 出力波形（全波整流 |sin|）
ax = fig.add_subplot(gs[0, 1])
t = np.linspace(0, 2, 1000)
vs = np.sin(2 * np.pi * t)
ax.axhline(0, color=BK, lw=0.8)
ax.plot(t, vs, color="#9aa7bd", lw=1.0, ls="--", zorder=2)
ax.fill_between(t, 0, np.abs(vs), color=SHADE, zorder=1)
ax.plot(t, np.abs(vs), color=BLUE, lw=1.5, zorder=3)
ax.text(0.05, 1.16, r"$v_R=|v_S|$", ha="left", fontsize=7.5, color=BLUE)
for x in [0.5, 1.0, 1.5, 2.0]:
    ax.plot([x, x], [-0.05, 0.05], color=BK, lw=0.8)
ax.text(1.0, -0.18, r"$\pi$", ha="center", va="top", fontsize=7)
ax.text(2.0, -0.18, r"$2\pi$", ha="center", va="top", fontsize=7)
ax.text(2.08, -0.02, r"$\omega t$", ha="left", va="top", fontsize=7)
ax.set_xlim(0, 2.2)
ax.set_ylim(-1.2, 1.3)
ax.axis("off")
ax.text(1.1, -0.52, "(b) 出力波形", ha="center", fontsize=7.0,
        fontproperties=JP, color="#555")

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig8.2.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
