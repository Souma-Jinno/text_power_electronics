#!/usr/bin/env python3
# fig5.7（第5章）: 昇降圧コンバータの回路構成と，オン期間・オフ期間の等価回路。
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




def ind_v(ax, x, y1, y2, c=BK):
    # y1: 上端，y2: 下端。右へ膨らむ。横向き ind_h と同じ巻き数・同じ大きさ。
    yc = 0.5 * (y1 + y2)
    yt, yb = yc + COILLEN / 2, yc - COILLEN / 2
    if y1 > yt:
        wire(ax, [(x, y1), (x, yt)], c)
    if yb > y2:
        wire(ax, [(x, yb), (x, y2)], c)
    dy = COILLEN / TURNS
    r = dy / 2
    t = np.linspace(-np.pi / 2, np.pi / 2, 30)
    for k in range(TURNS):
        yk = yt - dy * (k + 0.5)
        ax.plot(x + 0.85 * r * np.cos(t), yk + r * np.sin(t),
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


_ARROWS = []


def iarr(ax, x, y, dx, dy, c=None):
    # 矢印はここでは描かず，軸の縮尺が決まってから draw_arrows() でまとめて描く。
    # (a) と (b)(c) では縮尺が違うので，データ座標で長さを指定すると小さい図では
    # 矢じりだけになって線が潰れて見えてしまうため（著者指摘 2026-09-08）。
    _ARROWS.append((ax, x, y, dx, dy, c))


def draw_arrows():
    # 紙面上の長さを一定にして，どの図でも同じ形の矢印にする。
    # c=None のとき「電流の経路」を示す太い矢印，色を指定したときは細い矢印（i_L など）。
    for ax, x, y, dx, dy, c in _ARROWS:
        n = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / n, dy / n
        # 全長は 12 pt（細い矢印は 10 pt）を上限に，指定された区間に収まる長さにする。
        # 下限 7.5 pt は，矢じりだけになって線が潰れて見えないための最小の長さ。
        span = n * abs(ax.transData.transform((1, 0))[0]
                       - ax.transData.transform((0, 0))[0]) * 72.0 / ax.figure.dpi
        arrlen = min(12.0 if c is None else 10.0, max(7.5, span))
        lw = 1.7 if c is None else 1.0
        ms = 7.5 if c is None else 6.5           # 矢じりの大きさ
        col = BK if c is None else c
        # 指定された区間の中央に，一定の長さで置く
        px = ax.transData.transform((x + 0.5 * dx, y + 0.5 * dy))
        half = 0.5 * arrlen * ax.figure.dpi / 72.0
        head = ax.transData.inverted().transform(
            (px[0] + ux * half, px[1] + uy * half))
        ax.annotate("", xy=(head[0], head[1]), xycoords="data",
                    xytext=(-ux * arrlen, -uy * arrlen),
                    textcoords="offset points",
                    arrowprops=dict(arrowstyle="-|>", lw=lw, color=col,
                                    mutation_scale=ms,
                                    shrinkA=0, shrinkB=0), zorder=4)
    _ARROWS.clear()


def draw_bb(ax, mode, small=False):
    yT, yB = 2.9, 0.6
    if small:
        # (b)(c) の等価回路：素子間の配線を詰めて回路全体の幅を縮め，同じ紙幅に
        # 描いたとき素子記号が (a) に近い大きさになるようにする
        # （2026-09-08 著者指摘「(b)と(c)の回路大きくして」）
        xV, xS0, xS1, xA, xD0, xD1, xB, xR = 0.6, 1.1, 2.5, 3.2, 3.7, 4.9, 5.5, 6.7
        xlim = (-0.8, 7.5)
    else:
        xV, xS0, xS1, xA, xD0, xD1, xB, xR = 0.7, 1.4, 3.2, 3.9, 4.5, 5.7, 6.6, 8.2
        xlim = (-1.3, 9.7)
    fs = 7.2 if small else 8
    fsd = 6.6 if small else 7.4
    left_c = GY if mode == "off" else BK
    dio_c = GY if mode == "on" else BK
    # 上側
    wire(ax, [(xV, yT), (xS0, yT)], left_c)
    sw_h(ax, xS0, xS1, yT, c=left_c, fs=fs,
         state="closed" if mode == "on" else "open", r=0.085 if small else 0.075)
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
    if not small:
        gnd(ax, 0.5 * (xA + xB), yB)
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
        # 極性表示は V_in と同じく「上を正」で測る（本文の約束）。V_out は負になる
        ax.text(xR + 1.05, yT - 0.45, "$+$", ha="center", fontsize=fsd)
        ax.text(xR + 1.05, 0.5 * (yB + yT), r"$V_{\mathrm{out}}$",
                ha="center", va="center", fontsize=fs)
        ax.text(xR + 1.05, yB + 0.45, "$-$", ha="center", fontsize=fsd)
    # 電流経路の矢印
    # 矢印は配線の上に置き，素子や節点の丸と重ならない範囲を指定する
    if mode == "on":
        iarr(ax, xV + 0.06, yT, 0.38, 0)
        iarr(ax, 0.5 * (xV + xA) + 0.65, yB, -0.7, 0)
    elif mode == "off":
        iarr(ax, 0.5 * (xA + xB) - 0.35, yB, 0.7, 0)
        iarr(ax, xB - 0.05, yT, -0.5, 0)
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
draw_bb(ax, "full")
ax.text(4.2, -0.55, "(a) 回路構成（出力の極性が反転する）", ha="center",
        fontsize=7.2, fontproperties=JP, color="#555")

ax = fig.add_subplot(gs[1, 0])
draw_bb(ax, "on", small=True)
ax.text(3.35, -0.62, "(b) オン期間（Lに蓄える）", ha="center", fontsize=6.8,
        fontproperties=JP, color="#555")

ax = fig.add_subplot(gs[1, 1])
draw_bb(ax, "off", small=True)
ax.text(3.35, -0.62, "(c) オフ期間（Lが放出）", ha="center", fontsize=6.8,
        fontproperties=JP, color="#555")

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig5.7.eps")
fig.canvas.draw()   # aspect="equal" の縮尺を確定させてから矢印を描く
draw_arrows()
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
