#!/usr/bin/env python3
# fig5.5（第5章）: 昇圧チョッパの回路構成と，オン期間・オフ期間の等価回路。
# 灰色は電流が流れない（切り離された）部分，太い矢印は電流の経路を表す。
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


def sw_v(ax, x, y1, y2, c=BK, fs=8, state="open", r=0.075):
    # 開閉の分かるスイッチ記号（縦置き）：端子2つ（小さい丸）と，下端子を支点にした可動接片。
    # state="open" は接片が左へ持ち上がった状態，"closed" は接片が上端子に接した状態。
    yc = 0.5 * (y1 + y2)
    g = 0.40
    ya, yb = yc - g, yc + g
    wire(ax, [(x, y1), (x, ya - r)], c)
    wire(ax, [(x, yb + r), (x, y2)], c)
    ax.add_patch(Circle((x, ya), r, fc="white", ec=c, lw=0.9, zorder=3))
    ax.add_patch(Circle((x, yb), r, fc="white", ec=c, lw=0.9, zorder=3))
    if state == "closed":
        ax.plot([x, x], [ya + r, yb - r], color=c, lw=1.0, zorder=2)
    else:
        th = np.deg2rad(30)
        ln = 2 * g
        ax.plot([x - r * np.sin(th), x - ln * np.sin(th)],
                [ya + r * np.cos(th), ya + ln * np.cos(th)],
                color=c, lw=1.0, solid_capstyle="round", zorder=2)
    ax.text(x - 0.62, yc, "S", ha="right", va="center", fontsize=fs, color=c)


def ind_h(ax, x1, x2, y, c=BK, n=4):
    dx = (x2 - x1) / n
    r = dx / 2
    t = np.linspace(0, np.pi, 30)
    for k in range(n):
        xc = x1 + dx * (k + 0.5)
        ax.plot(xc - r * np.cos(t), y + 0.85 * r * np.sin(t),
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


def dio_h(ax, x1, x2, y, c=BK):
    # 左から右へ導通（アノードが左）
    xc = 0.5 * (x1 + x2)
    s = 0.28
    a = 0.7 * s
    wire(ax, [(x1, y), (xc - a, y)], c)
    wire(ax, [(xc + a, y), (x2, y)], c)
    ax.add_patch(Polygon([(xc - a, y - s), (xc - a, y + s), (xc + a, y)],
                         closed=True, fc="white", ec=c, lw=1.0, zorder=2))
    ax.plot([xc + a, xc + a], [y - s, y + s], color=c, lw=1.2, zorder=2)


def iarr(ax, x, y, dx, dy, c=None):
    # c=None のとき「電流の経路」を示す太い矢印（色に依らず太さで区別する）。
    # 色を指定したときは細い矢印（i_L の向きなど）。
    if c is None:
        ax.annotate("", xy=(x + dx, y + dy), xytext=(x, y),
                    arrowprops=dict(arrowstyle="-|>", lw=1.9, color=BK,
                                    mutation_scale=10), zorder=4)
    else:
        ax.annotate("", xy=(x + dx, y + dy), xytext=(x, y),
                    arrowprops=dict(arrowstyle="-|>", lw=1.1, color=c,
                                    mutation_scale=8), zorder=4)


def draw_boost(ax, mode, small=False):
    yT, yB = 2.9, 0.6
    if small:
        # (b)(c) の等価回路：素子間の配線を詰めて回路全体の幅を縮め，同じ紙幅に
        # 描いたとき素子記号が (a) に近い大きさになるようにする
        # （2026-09-08 著者指摘「(b)と(c)の回路大きくして」）
        xV, xL0, xL1, xA, xD0, xD1, xB, xR = 0.6, 1.2, 2.8, 3.4, 3.8, 5.0, 5.6, 6.8
        xlim = (-0.8, 7.6)
    else:
        xV, xL0, xL1, xA, xD0, xD1, xB, xR = 0.7, 1.5, 3.1, 3.9, 4.4, 5.6, 6.6, 8.2
        xlim = (-1.3, 9.7)
    fs = 7.2 if small else 8
    fsd = 6.6 if small else 7.4
    sw_c = GY if mode == "off" else BK
    dio_c = GY if mode == "on" else BK
    # 上側
    wire(ax, [(xV, yT), (xL0, yT)])
    ind_h(ax, xL0, xL1, yT)
    wire(ax, [(xL1, yT), (xA, yT)])
    dot(ax, xA, yT)
    wire(ax, [(xA, yT), (xD0, yT)], dio_c)
    dio_h(ax, xD0, xD1, yT, c=dio_c)
    wire(ax, [(xD1, yT), (xB, yT)], dio_c if mode == "on" else BK)
    wire(ax, [(xB, yT), (xR, yT)])
    dot(ax, xB, yT)
    # 下側
    wire(ax, [(xV, yB), (xR, yB)])
    dot(ax, xA, yB)
    dot(ax, xB, yB)
    # 素子
    source(ax, xV, yB, yT)
    ax.text(xV - 0.5, 0.5 * (yB + yT), r"$V_{\mathrm{in}}$",
            ha="right", va="center", fontsize=fs)
    sw_v(ax, xA, yB, yT, c=sw_c, fs=fs,
         state="closed" if mode == "on" else "open", r=0.085 if small else 0.075)
    dio_c_lab = dio_c
    ax.text(0.5 * (xD0 + xD1), yT + 0.42, r"$\mathrm{D}$",
            ha="center", fontsize=fs, color=dio_c_lab)
    cap_v(ax, xB, yT, yB)
    ax.text(xB + 0.4, 0.5 * (yB + yT), "$C$", ha="left", va="center", fontsize=fs)
    res_v(ax, xR, yT, yB)
    ax.text(xR + 0.32, 0.5 * (yB + yT), "$R$", ha="left", va="center", fontsize=fs)
    # ラベル
    ax.text(0.5 * (xL0 + xL1), yT + 0.42, "$L$", ha="center", fontsize=fs)
    ax.text(xL0 + 0.05, yT - 0.42, "$+$", ha="center", fontsize=fsd)
    ax.text(0.5 * (xL0 + xL1), yT - 0.46, "$v_L$", ha="center", fontsize=fsd)
    ax.text(xL1 - 0.05, yT - 0.42, "$-$", ha="center", fontsize=fsd)
    if not small:
        iarr(ax, 3.2, yT + 0.25, 0.45, 0, c=BLUE)
        ax.text(3.4, yT + 0.42, "$i_L$", ha="center", fontsize=fsd, color=BLUE)
        ax.text(xR + 1.05, yT - 0.45, "$+$", ha="center", fontsize=fsd)
        ax.text(xR + 1.05, 0.5 * (yB + yT), r"$V_{\mathrm{out}}$",
                ha="center", va="center", fontsize=fs)
        ax.text(xR + 1.05, yB + 0.45, "$-$", ha="center", fontsize=fsd)
    # 電流経路の矢印
    if mode == "on":
        iarr(ax, xV + 0.25, yT, 0.3, 0)
        iarr(ax, xA + 0.55, 2.0, 0, -0.6)
        iarr(ax, 0.5 * (xV + xA) + 0.4, yB, -0.6, 0)
        iarr(ax, xB + 0.5, yT, 0.4, 0)  # CからRへ
    elif mode == "off":
        iarr(ax, xV + 0.25, yT, 0.3, 0)
        iarr(ax, xD1 + 0.1, yT, 0.4, 0)
        iarr(ax, 0.5 * (xA + xB) - 0.25, yB, -0.6, 0)
    ax.set_xlim(*xlim)
    ax.set_ylim(-0.8, 3.65)
    ax.set_aspect("equal")
    ax.axis("off")


fig = plt.figure(figsize=(4.05, 2.4))   # bbox tight の余白 0.1 in ×2 を足して幅 4.25 in（見本原稿の本文幅 4.35 in に収める）
# (a) は従来の大きさのまま。(b)(c) は横に2つ並べたまま図の幅いっぱいに広げ，
# 回路の配線を詰めて描くことで素子記号を (a) の8割程度の大きさにする。
gs = fig.add_gridspec(2, 2, height_ratios=[1.31, 1.12], left=0, right=1,
                      top=1, bottom=0, hspace=0.0, wspace=0.03)

ax = fig.add_subplot(gs[0, :])
draw_boost(ax, "full")
ax.text(4.2, -0.55, "(a) 回路構成", ha="center", fontsize=7.2,
        fontproperties=JP, color="#555")

ax = fig.add_subplot(gs[1, 0])
draw_boost(ax, "on", small=True)
ax.text(3.4, -0.62, "(b) オン期間（Lに蓄える）", ha="center", fontsize=6.8,
        fontproperties=JP, color="#555")

ax = fig.add_subplot(gs[1, 1])
draw_boost(ax, "off", small=True)
ax.text(3.4, -0.62, "(c) オフ期間（Lが放出）", ha="center", fontsize=6.8,
        fontproperties=JP, color="#555")

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig5.5.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
