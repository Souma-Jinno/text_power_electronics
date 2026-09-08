#!/usr/bin/env python3
# fig5.3（第5章）: 降圧コンバータの回路構成と，オン期間・オフ期間の等価回路。
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


PITCH = 0.40                    # コイル1巻きぶんの長さ
TURNS = 3                       # 巻き数（2026-09-08 著者指示「コイルですが3巻にして」）
COILLEN = TURNS * PITCH         # コイルの長さ。区間の中央にこの長さぶんだけ描き，
                                # 残りは素の配線でつなぐ。こうすると，置き場所の
                                # 長さが違っても，巻き数も1巻きの大きさも変わらない。

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


def sw_h(ax, x1, x2, y, c=BK, fs=8, state="open", r=0.075):
    # 開閉の分かるスイッチ記号：端子2つ（小さい丸）と，左端子を支点にした可動接片。
    # state="open" は接片が持ち上がった状態，"closed" は接片が右端子に接した状態。
    xc = 0.5 * (x1 + x2)
    g = 0.40
    xa, xb = xc - g, xc + g
    wire(ax, [(x1, y), (xa - r, y)], c)
    wire(ax, [(xb + r, y), (x2, y)], c)
    ax.add_patch(Circle((xa, y), r, fc="white", ec=c, lw=0.9, zorder=3))
    ax.add_patch(Circle((xb, y), r, fc="white", ec=c, lw=0.9, zorder=3))
    if state == "closed":
        ax.plot([xa + r, xb - r], [y, y], color=c, lw=1.0, zorder=2)
        ax.text(xc, y + 0.28, "S", ha="center", va="bottom", fontsize=fs, color=c)
    else:
        th = np.deg2rad(30)
        ln = 2 * g
        ax.plot([xa + r * np.cos(th), xa + ln * np.cos(th)],
                [y + r * np.sin(th), y + ln * np.sin(th)],
                color=c, lw=1.0, solid_capstyle="round", zorder=2)
        ax.text(xc, y + 0.50, "S", ha="center", va="bottom", fontsize=fs, color=c)


def ind_h(ax, x1, x2, y, c=BK):
    xc = 0.5 * (x1 + x2)
    xa, xb = xc - COILLEN / 2, xc + COILLEN / 2
    if xa > x1:
        wire(ax, [(x1, y), (xa, y)], c)
    if x2 > xb:
        wire(ax, [(xb, y), (x2, y)], c)
    dx = COILLEN / TURNS
    r = dx / 2
    t = np.linspace(0, np.pi, 30)
    for k in range(TURNS):
        xk = xa + dx * (k + 0.5)
        ax.plot(xk - r * np.cos(t), y + 0.85 * r * np.sin(t),
                color=c, lw=1.0, zorder=2)



def gnd(ax, x, y, c=BK):
    # 基準電位（グランド）。2026-09-08 著者指示「回路図にグランド入れて」。
    wire(ax, [(x, y), (x, y - 0.30)], c)
    for i, wd in enumerate([0.44, 0.26, 0.10]):
        yy = y - 0.30 - i * 0.11
        ax.plot([x - wd / 2, x + wd / 2], [yy, yy], color=c, lw=1.0, zorder=2)


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


def dio_v_up(ax, x, y1, y2, c=BK):
    # y1: 下端，y2: 上端。下から上へ導通（アノードが下）
    yc = 0.5 * (y1 + y2)
    s = 0.28
    a = 0.7 * s
    wire(ax, [(x, y1), (x, yc - a)], c)
    wire(ax, [(x, yc + a), (x, y2)], c)
    ax.add_patch(Polygon([(x - s, yc - a), (x + s, yc - a), (x, yc + a)],
                         closed=True, fc="white", ec=c, lw=1.0, zorder=2))
    ax.plot([x - s, x + s], [yc + a, yc + a], color=c, lw=1.2, zorder=2)


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


def draw_buck(ax, mode, small=False):
    yT, yB = 2.9, 0.6
    if small:
        # (b)(c) の等価回路：素子間の配線を詰めて回路全体の幅を縮め，同じ紙幅に
        # 描いたとき素子記号が (a) に近い大きさになるようにする
        # （2026-09-08 著者指摘「(b)と(c)の回路大きくして」）
        xV, xS0, xS1, xA, xL0, xL1, xB, xR = 0.6, 1.1, 2.5, 3.0, 3.5, 5.1, 5.7, 6.9
        xlim = (-0.8, 7.7)
    else:
        xV, xS0, xS1, xA, xL0, xL1, xB, xR = 0.7, 1.35, 3.15, 3.9, 4.5, 6.1, 6.9, 8.5
        xlim = (-1.3, 10.0)
    fs = 7.2 if small else 8
    fsd = 6.6 if small else 7.4
    left_c = GY if mode == "off" else BK
    dio_c = GY if mode in ("full_on_only",) else (GY if mode == "on" else BK)
    if mode == "full":
        dio_c = BK
    # 上側
    wire(ax, [(xV, yT), (xS0, yT)], left_c)
    sw_h(ax, xS0, xS1, yT, c=left_c, fs=fs,
         state="closed" if mode == "on" else "open", r=0.085 if small else 0.075)
    wire(ax, [(xS1, yT), (xA, yT)], left_c)
    dot(ax, xA, yT)
    wire(ax, [(xA, yT), (xL0, yT)])
    ind_h(ax, xL0, xL1, yT)
    wire(ax, [(xL1, yT), (xR, yT)])
    dot(ax, xB, yT)
    # 下側
    wire(ax, [(xV, yB), (xA, yB)], left_c)
    wire(ax, [(xA, yB), (xR, yB)])
    dot(ax, xA, yB)
    dot(ax, xB, yB)
    if not small:
        gnd(ax, 0.5 * (xA + xB), yB)
    # 素子
    source(ax, xV, yB, yT, c=left_c)
    ax.text(xV - 0.5, 0.5 * (yB + yT), r"$V_{\mathrm{in}}$",
            ha="right", va="center", fontsize=fs, color=left_c)
    dio_v_up(ax, xA, yB, yT, c=dio_c)
    ax.text(xA - 0.4, 0.5 * (yB + yT), r"$\mathrm{D}$",
            ha="right", va="center", fontsize=fs, color=dio_c)
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
        iarr(ax, 6.3, yT + 0.25, 0.45, 0, c=BLUE)
        ax.text(6.5, yT + 0.42, "$i_L$", ha="center", fontsize=fsd, color=BLUE)
        ax.text(xR + 1.05, yT - 0.45, "$+$", ha="center", fontsize=fsd)
        ax.text(xR + 1.05, 0.5 * (yB + yT), r"$V_{\mathrm{out}}$",
                ha="center", va="center", fontsize=fs)
        ax.text(xR + 1.05, yB + 0.45, "$-$", ha="center", fontsize=fsd)
    # 電流経路の矢印
    if mode == "on":
        iarr(ax, xV + 0.25, yT, 0.3, 0)
        iarr(ax, 0.5 * (xA + xB) + 0.3, yB, -0.6, 0)
    elif mode == "off":
        iarr(ax, xA + 0.5, 0.85, 0, 0.5)
        iarr(ax, 0.5 * (xA + xB) + 0.3, yB, -0.6, 0)
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
draw_buck(ax, "full")
ax.text(4.35, -0.55, "(a) 回路構成", ha="center", fontsize=7.2,
        fontproperties=JP, color="#555")

ax = fig.add_subplot(gs[1, 0])
draw_buck(ax, "on", small=True)
ax.text(3.45, -0.62, "(b) オン期間（Sが導通）", ha="center", fontsize=6.8,
        fontproperties=JP, color="#555")

ax = fig.add_subplot(gs[1, 1])
draw_buck(ax, "off", small=True)
ax.text(3.45, -0.62, "(c) オフ期間（Dが還流）", ha="center", fontsize=6.8,
        fontproperties=JP, color="#555")

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig5.3.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
