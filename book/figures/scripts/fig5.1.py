#!/usr/bin/env python3
# fig5.1（第5章）: デューティ比の定義。スイッチのオン・オフを周期 T で繰り返し，
# そのうちオンの時間 T_on の割合が D = T_on/T である。
# D が小さいとき（a）と大きいとき（b）を上下に並べ，T は同じで T_on だけが変わることを示す。
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
BLUE = "#2a5db0"
RED = "#c0392b"
SHADE = "#eef3fb"

T = 1.0          # スイッチング周期（描画上の単位）
NP = 2           # 描く周期の数
XL, XR = -0.32, NP * T + 0.55  # 描画範囲（左に「オン」「オフ」，右に t の余白）


def dim(ax, x1, x2, y, label, c=BK, fs=7.5):
    # 寸法線（両矢印）と，その上のラベル
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="<->", lw=0.8, color=c,
                                mutation_scale=7, shrinkA=0, shrinkB=0),
                zorder=4)
    ax.text(0.5 * (x1 + x2), y + 0.06, label, ha="center", va="bottom",
            fontsize=fs, color=c)


def draw_wave(ax, D, panel):
    ton = D * T
    # オン期間の網掛け（オンの時間の「割合」が面積として見えるように）
    for k in range(NP):
        ax.add_patch(Rectangle((k * T, 0), ton, 1.0, fc=SHADE, ec="none", zorder=0))
    # 矩形波
    # 波形は「オンで始まり，オフで終わる」ちょうど NP 周期ぶんを描く。
    # 末尾にオンの切れ端を足すと，オンの途中で波形が断ち切られたように見える
    # （2026-09-08 著者指摘「波形はオン時は途中で切らないで」）。
    # t=0 では「オフからオンへ立ち上がる」ところから描く。いきなりオンの高さから
    # 始めると，波形が左端で断ち切られたように見える
    # （2026-09-08 著者指摘「開始の波形がおかしい」）。
    xs, ys = [0.0, 0.0], [0.0, 1.0]
    for k in range(NP):
        xs += [k * T + ton, k * T + ton, (k + 1) * T]
        ys += [1.0, 0.0, 0.0]
        if k < NP - 1:                      # 次の周期の立ち上がり
            xs.append((k + 1) * T)
            ys.append(1.0)
    ax.plot(xs, ys, color=BLUE, lw=1.3, solid_joinstyle="miter", zorder=3)
    # 時間軸
    ax.annotate("", xy=(XR - 0.08, 0), xytext=(XL + 0.22, 0),
                arrowprops=dict(arrowstyle="-|>", lw=0.8, color=BK,
                                mutation_scale=7), zorder=2)
    ax.text(XR - 0.05, -0.03, "$t$", ha="left", va="top", fontsize=8, color=BK)
    ax.text(0, -0.06, "$0$", ha="center", va="top", fontsize=7, color=BK)
    # 縦軸の代わりの状態ラベル
    ax.text(XL + 0.14, 1.0, "オン", ha="right", va="center", fontsize=7.5,
            fontproperties=JP, color=BK)
    ax.text(XL + 0.14, 0.0, "オフ", ha="right", va="center", fontsize=7.5,
            fontproperties=JP, color=BK)
    # 寸法線：T_on（オンの時間）と T（1周期）。補助の縦線は細い点線
    yd1, yd2 = 1.22, 1.62
    for x, ytop in ((0, yd2), (ton, yd1), (T, yd2)):
        ax.plot([x, x], [1.0, ytop + 0.05], color="#888888", lw=0.5,
                ls=(0, (1.5, 1.5)), zorder=1)
    dim(ax, 0, ton, yd1, r"$T_{\mathrm{on}}$", c=RED)
    dim(ax, 0, T, yd2, r"$T$", c=BK)
    # 右端に D の値
    ax.text(XR - 0.05, 1.42, r"$D = \dfrac{T_{\mathrm{on}}}{T} = %.2f$" % D,
            ha="right", va="center", fontsize=7.5, color=BK)
    ax.set_xlim(XL, XR)
    ax.set_ylim(-0.42, 1.95)
    ax.axis("off")
    ax.text(0.5 * (XL + XR), -0.40, panel, ha="center", va="top", fontsize=7.2,
            fontproperties=JP, color="#555")


fig, axes = plt.subplots(2, 1, figsize=(3.9, 2.55))
fig.subplots_adjust(hspace=0.30)
draw_wave(axes[0], 0.25, "(a) $D$が小さいとき（オンの時間が短い）")
draw_wave(axes[1], 0.75, "(b) $D$が大きいとき（オンの時間が長い）")

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig5.1.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
