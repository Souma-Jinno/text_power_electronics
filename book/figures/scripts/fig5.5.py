#!/usr/bin/env python3
# fig5.5（第5章）: 昇降圧チョッパの回路構成と，オン期間・オフ期間の等価回路。
# エネルギーがいったんすべて L に蓄えられてから負荷へ渡ること，
# 出力の極性が反転することを示す。
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
GY = "#b8b8b8"
BLUE = "#2a5db0"
RED = "#c0392b"


def wire(ax, pts, c=BK):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs, ys, color=c, lw=1.0, solid_capstyle="round", zorder=1)


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


def sw_h(ax, x1, x2, y, c=BK, fs=8):
    xc = 0.5 * (x1 + x2)
    w, h = 0.66, 0.46
    wire(ax, [(x1, y), (xc - w / 2, y)], c)
    wire(ax, [(xc + w / 2, y), (x2, y)], c)
    ax.add_patch(Rectangle((xc - w / 2, y - h / 2), w, h,
                           fc="white", ec=c, lw=1.0, zorder=2))
    ax.text(xc, y, "S", ha="center", va="center", fontsize=fs, color=c)


def ind_v(ax, x, y1, y2, c=BK, n=4):
    # y1: 上端，y2: 下端。右へ膨らむ
    dy = (y1 - y2) / n
    r = dy / 2
    t = np.linspace(-np.pi / 2, np.pi / 2, 30)
    for k in range(n):
        yc = y1 - dy * (k + 0.5)
        ax.plot(x + 0.85 * r * np.cos(t), yc + r * np.sin(t),
                color=c, lw=1.0, zorder=2)


def cap_v(ax, x, y1, y2, c=BK):
    yc = 0.5 * (y1 + y2)
    g, w = 0.09, 0.30
    wire(ax, [(x, y1), (x, yc + g)], c)
    wire(ax, [(x, yc - g), (x, y2)], c)
    ax.plot([x - w, x + w], [yc + g, yc + g], color=c, lw=1.2, zorder=2)
    ax.plot([x - w, x + w], [yc - g, yc - g], color=c, lw=1.2, zorder=2)


def res_v(ax, x, y1, y2, c=BK):
    yc = 0.5 * (y1 + y2)
    w, h = 0.36, 0.85
    wire(ax, [(x, y1), (x, yc + h / 2)], c)
    wire(ax, [(x, yc - h / 2), (x, y2)], c)
    ax.add_patch(Rectangle((x - w / 2, yc - h / 2), w, h,
                           fc="white", ec=c, lw=1.0, zorder=2))


def dio_h_left(ax, x1, x2, y, c=BK):
    # 右から左へ導通（アノードが右）
    xc = 0.5 * (x1 + x2)
    s = 0.28
    a = 0.7 * s
    wire(ax, [(x1, y), (xc - a, y)], c)
    wire(ax, [(xc + a, y), (x2, y)], c)
    ax.add_patch(Polygon([(xc + a, y - s), (xc + a, y + s), (xc - a, y)],
                         closed=True, fc="white", ec=c, lw=1.0, zorder=2))
    ax.plot([xc - a, xc - a], [y - s, y + s], color=c, lw=1.2, zorder=2)


def iarr(ax, x, y, dx, dy, c=RED):
    ax.annotate("", xy=(x + dx, y + dy), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", lw=1.1, color=c,
                                mutation_scale=8), zorder=4)


def draw_bb(ax, mode, small=False):
    yT, yB = 2.9, 0.6
    xV = 0.7
    xS0, xS1 = 1.4, 3.2
    xA = 3.9
    xD0, xD1 = 4.5, 5.7
    xB = 6.6
    xR = 8.2
    fs = 6.6 if small else 8
    fsd = 6.2 if small else 7.4
    left_c = GY if mode == "off" else BK
    dio_c = GY if mode == "on" else BK
    # 上側
    wire(ax, [(xV, yT), (xS0, yT)], left_c)
    sw_h(ax, xS0, xS1, yT, c=left_c, fs=fs)
    wire(ax, [(xS1, yT), (xA, yT)], left_c)
    dot(ax, xA, yT)
    wire(ax, [(xA, yT), (xD0, yT)], dio_c)
    dio_h_left(ax, xD0, xD1, yT, c=dio_c)
    wire(ax, [(xD1, yT), (xB, yT)], dio_c)
    wire(ax, [(xB, yT), (xR, yT)])
    dot(ax, xB, yT)
    # 下側
    wire(ax, [(xV, yB), (xA, yB)], left_c)
    wire(ax, [(xA, yB), (xR, yB)])
    dot(ax, xA, yB)
    dot(ax, xB, yB)
    # 素子
    source(ax, xV, yB, yT, c=left_c)
    ax.text(xV - 0.5, 0.5 * (yB + yT), r"$V_{\mathrm{in}}$",
            ha="right", va="center", fontsize=fs, color=left_c)
    ind_v(ax, xA, yT, yB)
    ax.text(xA - 0.42, 0.5 * (yB + yT), "$L$", ha="right", va="center",
            fontsize=fs)
    ax.text(xA - 0.42, yT - 0.35, "$+$", ha="right", fontsize=fsd)
    ax.text(xA - 0.42, yB + 0.18, "$-$", ha="right", fontsize=fsd)
    ax.text(0.5 * (xD0 + xD1), yT + 0.42, r"$\mathrm{D}$",
            ha="center", fontsize=fs, color=dio_c)
    cap_v(ax, xB, yT, yB)
    ax.text(xB + 0.4, 0.5 * (yB + yT), "$C$", ha="left", va="center", fontsize=fs)
    res_v(ax, xR, yT, yB)
    ax.text(xR + 0.32, 0.5 * (yB + yT), "$R$", ha="left", va="center", fontsize=fs)
    if not small:
        iarr(ax, xA + 0.55, 2.15, 0, -0.5, c=BLUE)
        ax.text(xA + 0.75, 1.9, "$i_L$", ha="left", fontsize=fsd, color=BLUE)
        ax.text(xR + 1.05, yT - 0.45, "$-$", ha="center", fontsize=fsd)
        ax.text(xR + 1.05, 0.5 * (yB + yT), r"$V_{\mathrm{out}}$",
                ha="center", va="center", fontsize=fs)
        ax.text(xR + 1.05, yB + 0.45, "$+$", ha="center", fontsize=fsd)
    # 電流経路の矢印
    if mode == "on":
        iarr(ax, 0.95, yT, 0.3, 0)
        iarr(ax, 2.9, yB, -0.6, 0)
    elif mode == "off":
        iarr(ax, 4.9, yB, 0.6, 0)
        iarr(ax, 6.3, yT, -0.4, 0)
    ax.set_xlim(-1.3, 9.7)
    ax.set_ylim(-0.75, 3.75)
    ax.set_aspect("equal")
    ax.axis("off")


fig = plt.figure(figsize=(4.25, 3.0))
gs = fig.add_gridspec(2, 2, height_ratios=[1.35, 1.0], hspace=0.02, wspace=0.02)

ax = fig.add_subplot(gs[0, :])
draw_bb(ax, "full")
ax.text(4.2, -0.55, "(a) 回路構成（出力の極性が反転する）", ha="center",
        fontsize=7.2, fontproperties=JP, color="#555")

ax = fig.add_subplot(gs[1, 0])
draw_bb(ax, "on", small=True)
ax.text(4.2, -0.62, "(b) オン期間（Lに蓄える）", ha="center", fontsize=6.8,
        fontproperties=JP, color="#555")

ax = fig.add_subplot(gs[1, 1])
draw_bb(ax, "off", small=True)
ax.text(4.2, -0.62, "(c) オフ期間（Lが放出）", ha="center", fontsize=6.8,
        fontproperties=JP, color="#555")

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig5.5.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
