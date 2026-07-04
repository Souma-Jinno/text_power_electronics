#!/usr/bin/env python3
# fig7.5（第7章）: パストランジスタを用いた実用リニアレギュレータ。
# ツェナーで作った基準V_refとオペアンプ（誤差増幅器）が，分圧V_fbを見て
# パストランジスタの導通度を連続的に調整し，V_out=V_ref(1+R1/R2)に保つ。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BK = "#222222"
BLUE = "#2a5db0"
RED = "#c0392b"


def wire(ax, pts, c=BK):
    ax.plot([p[0] for p in pts], [p[1] for p in pts],
            color=c, lw=1.0, solid_capstyle="round", zorder=1)


def dot(ax, x, y, c=BK):
    ax.plot([x], [y], "o", ms=2.4, color=c, zorder=3)


def source(ax, x, ybot, ytop, c=BK):
    r = 0.34
    yc = 0.5 * (ybot + ytop)
    wire(ax, [(x, ybot), (x, yc - r)], c)
    wire(ax, [(x, yc + r), (x, ytop)], c)
    ax.add_patch(Circle((x, yc), r, fc="white", ec=c, lw=1.0, zorder=2))
    ax.text(x, yc + 0.15, "$+$", ha="center", va="center", fontsize=6, color=c)
    ax.text(x, yc - 0.16, "$-$", ha="center", va="center", fontsize=6, color=c)


def res_v(ax, x, y1, y2, lab=None, lx=0.3):
    yc = 0.5 * (y1 + y2)
    w, h = 0.32, 0.72
    wire(ax, [(x, y1), (x, yc + h / 2)])
    wire(ax, [(x, yc - h / 2), (x, y2)])
    ax.add_patch(Rectangle((x - w / 2, yc - h / 2), w, h,
                           fc="white", ec=BK, lw=1.0, zorder=2))
    if lab:
        ax.text(x + lx, yc, lab, ha="left", va="center", fontsize=8.5)


def zener_v(ax, x, y1, y2):
    # 上y1→下y2。カソード（上）にツェナー特有の折れ線
    yc = 0.5 * (y1 + y2)
    s = 0.26
    a = 0.62 * s
    wire(ax, [(x, y1), (x, yc + a)])
    wire(ax, [(x, yc - a), (x, y2)])
    # 三角（下向き，アノード下）
    ax.add_patch(Polygon([(x - s, yc + a), (x + s, yc + a), (x, yc - a)],
                         closed=True, fc="white", ec=BK, lw=1.0, zorder=2))
    # カソードのバー（両端を折る）
    ax.plot([x - s, x + s], [yc - a, yc - a], color=BK, lw=1.2, zorder=2)
    ax.plot([x - s, x - s + 0.12], [yc - a, yc - a - 0.14], color=BK, lw=1.2)
    ax.plot([x + s, x + s - 0.12], [yc - a, yc - a + 0.14], color=BK, lw=1.2)


def opamp(ax, xl, xr, yc, hh=0.72):
    ax.add_patch(Polygon([(xl, yc + hh), (xl, yc - hh), (xr, yc)],
                         closed=True, fc="white", ec=BK, lw=1.1, zorder=2))
    ax.text(xl + 0.20, yc + 0.34, "$+$", ha="center", va="center", fontsize=8)
    ax.text(xl + 0.20, yc - 0.34, "$-$", ha="center", va="center", fontsize=8)


def bjt_npn(ax, xb, yc):
    # ベースバー，コレクタ上，エミッタ下（矢印外向き）
    ax.add_patch(Circle((xb + 0.32, yc), 0.62, fc="none", ec="#bbb", lw=0.0))
    wire(ax, [(xb, yc - 0.34), (xb, yc + 0.34)])            # ベースバー
    wire(ax, [(xb - 0.55, yc), (xb, yc)])                   # ベース線
    wire(ax, [(xb, yc + 0.22), (xb + 0.5, yc + 0.6)])       # コレクタ
    wire(ax, [(xb + 0.5, yc + 0.6), (xb + 0.5, yc + 0.95)])
    wire(ax, [(xb, yc - 0.22), (xb + 0.5, yc - 0.6)])       # エミッタ
    wire(ax, [(xb + 0.5, yc - 0.6), (xb + 0.5, yc - 0.95)])
    # エミッタ矢印
    ax.annotate("", xy=(xb + 0.5, yc - 0.6), xytext=(xb + 0.25, yc - 0.41),
                arrowprops=dict(arrowstyle="-|>", lw=0.9, color=BK,
                                mutation_scale=7), zorder=4)
    return (xb + 0.5, yc + 0.95), (xb + 0.5, yc - 0.95)     # コレクタ端子, エミッタ端子


def gnd(ax, x, y):
    wire(ax, [(x, y), (x, y - 0.18)])
    for i, wd in enumerate([0.32, 0.19, 0.07]):
        yy = y - 0.18 - i * 0.09
        ax.plot([x - wd / 2, x + wd / 2], [yy, yy], color=BK, lw=1.0)


fig, ax = plt.subplots(figsize=(4.4, 3.05))

GNDy = 0.0
TOPy = 4.4

# 入力電源
xV = 0.4
source(ax, xV, GNDy, TOPy)
ax.text(xV - 0.5, 0.5 * TOPy, r"$V_{\mathrm{in}}$", ha="right", va="center", fontsize=9)
wire(ax, [(xV, TOPy), (9.2, TOPy)])          # 上レール
wire(ax, [(xV, GNDy), (11.0, GNDy)])         # 下レール（グラウンド）

# ツェナー基準（Rs + ツェナー）
xZ = 2.4
res_v(ax, xZ, TOPy, 3.4, lab=r"$R_s$")
dot(ax, xZ, 3.4)
ax.text(xZ - 0.35, 3.4, r"$V_{\mathrm{ref}}$", ha="right", va="center",
        fontsize=8.5, color=RED)
zener_v(ax, xZ, 3.4, 1.5)
ax.text(xZ + 0.30, 2.45, r"$D_Z$", ha="left", va="center", fontsize=8.5)
wire(ax, [(xZ, 1.5), (xZ, GNDy)])

# オペアンプ（誤差増幅器）
xol, xor, yo = 4.3, 5.9, 2.7
opamp(ax, xol, xor, yo)
yp = yo + 0.34   # + 入力（上）
ym = yo - 0.34   # - 入力（下）
# + 入力 ← Vref（左から）
wire(ax, [(xZ, 3.4), (3.5, 3.4), (3.5, yp), (xol, yp)])
# 出力 → パストランジスタのベース
xb = 8.2
ctop, ebot = bjt_npn(ax, xb, 3.0)
wire(ax, [(xor, yo), (xb - 0.55, yo), (xb - 0.55, 3.0)])
ax.text(0.5 * (xor + xb) - 0.05, yo + 0.55, "誤差増幅", ha="center",
        fontproperties=JP, fontsize=6.8, color="#555")

# パストランジスタ：コレクタ→上レール，エミッタ→出力
wire(ax, [(ctop[0], ctop[1]), (ctop[0], TOPy)])
ax.text(xb + 0.75, 3.4, "パス\nトランジスタ", ha="left", va="center",
        fontproperties=JP, fontsize=6.6, color="#555")
xout = ebot[0]
wire(ax, [(ebot[0], ebot[1]), (xout, 1.9)])
dot(ax, xout, 1.9)
ax.text(xout + 0.15, 1.9 + 0.28, r"$V_{\mathrm{out}}$", ha="left",
        va="bottom", fontsize=9)

# 分圧抵抗 R1, R2（出力→グラウンド），タップV_fb
xd = xout
res_v(ax, xd, 1.9, 1.05, lab=r"$R_1$")
dot(ax, xd, 1.05)
res_v(ax, xd, 1.05, GNDy, lab=r"$R_2$")
# 負荷
xR = 10.4
wire(ax, [(xout, 1.9), (xR, 1.9)])
res_v(ax, xR, 1.9, GNDy, lab=r"$R_L$")
ax.text(xR + 0.02, 2.15, "負荷", ha="center", fontproperties=JP,
        fontsize=6.6, color="#555")

# フィードバック：タップ→ - 入力（オペアンプの下を通す）
wire(ax, [(xd, 1.05), (3.9, 1.05), (3.9, ym), (xol, ym)])
ax.text(xd - 0.9, 1.05 + 0.28, r"$V_{\mathrm{fb}}$", ha="center",
        fontsize=8, color=BLUE)
dot(ax, xd, 1.05)

ax.set_xlim(-0.4, 11.6)
ax.set_ylim(-0.7, 4.9)
ax.set_aspect("equal")
ax.axis("off")

fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig7.5.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
