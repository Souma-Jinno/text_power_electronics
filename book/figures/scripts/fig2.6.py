#!/usr/bin/env python3
# fig2.6（第2章）: 縦型パワーMOSFETとIGBTの断面比較。
# (a) 縦型MOSFET: 電流はチップの表から裏へ縦に流れる。耐圧はn-ドリフト層が受け持つ。
# (b) IGBT: 縦型MOSFETのドレイン側にp形層を1枚加えた構造。オン時にこのpn接合から
#     正孔が注入され，n-層の抵抗が下がる（伝導度変調）。
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BLUE = "#2a5db0"
RED = "#c0392b"
MAG = "#c93c8c"

fig, axes = plt.subplots(1, 2, figsize=(4.4, 2.5))

def draw(ax, igbt):
    W = 10.0
    # 下層: MOSFETはn+基板，IGBTはp形コレクタ層
    if igbt:
        ax.add_patch(Rectangle((0, 0), W, 1.1, fc="#fdeceb", ec="#555", lw=0.9))
        ax.text(5.0, 0.55, "p（コレクタ層）", ha="center", va="center",
                fontsize=6.6, fontproperties=JP)
    else:
        ax.add_patch(Rectangle((0, 0), W, 1.1, fc="#d9e4f5", ec="#555", lw=0.9))
        ax.text(5.0, 0.55, "n$^+$", ha="center", va="center", fontsize=7.2)
    # n-ドリフト層
    ax.add_patch(Rectangle((0, 1.1), W, 2.6, fc="#eaf0fa", ec="#555", lw=0.9))
    ax.text(5.0, 2.1, "n$^-$（ドリフト層：耐圧を受け持つ）", ha="center",
            va="center", fontsize=6.6, fontproperties=JP)
    # p形ボディ（左右）
    ax.add_patch(Rectangle((0, 3.7), 3.4, 1.5, fc="#fdeceb", ec="#555", lw=0.9))
    ax.add_patch(Rectangle((6.6, 3.7), 3.4, 1.5, fc="#fdeceb", ec="#555", lw=0.9))
    ax.text(1.0, 4.05, "p", ha="center", va="center", fontsize=7.2)
    ax.text(9.0, 4.05, "p", ha="center", va="center", fontsize=7.2)
    # n+ソース（ボディ内）
    ax.add_patch(Rectangle((1.4, 4.5), 2.0, 0.7, fc="#d9e4f5", ec="#555", lw=0.9))
    ax.add_patch(Rectangle((6.6, 4.5), 2.0, 0.7, fc="#d9e4f5", ec="#555", lw=0.9))
    ax.text(2.4, 4.85, "n$^+$", ha="center", va="center", fontsize=6.8)
    ax.text(7.6, 4.85, "n$^+$", ha="center", va="center", fontsize=6.8)
    # 酸化膜+ゲート（中央）
    ax.add_patch(Rectangle((3.0, 5.2), 4.0, 0.45, fc="#e8e8e8", ec="#555", lw=0.9))
    ax.add_patch(Rectangle((3.4, 5.65), 3.2, 0.5, fc="#c9c9c9", ec="#555", lw=0.9))
    # 上部電極（左右）
    ax.plot([1.6, 1.6], [5.2, 6.7], color="#333", lw=1.0)
    ax.plot([8.4, 8.4], [5.2, 6.7], color="#333", lw=1.0)
    ax.plot([1.6, 8.4], [6.7, 6.7], color="#333", lw=1.0)
    ax.plot([5.0, 5.0], [6.7, 7.2], color="#333", lw=1.0)
    ax.plot([5.0, 5.0], [6.15, 6.45], color="#666", lw=0.9)
    ax.text(5.55, 6.25, "G", ha="center", fontsize=7.6)
    # 下部電極
    ax.plot([5.0, 5.0], [0, -0.6], color="#333", lw=1.0)
    # 反転層とキャリアの流れ
    for x0 in (2.75, 6.75):
        ax.add_patch(Rectangle((x0, 3.75), 0.5, 1.42, fc=MAG, ec="none"))
    # 電子の流れ（上→下）
    ax.annotate("", xy=(3.0, 0.9), xytext=(3.0, 4.9),
                arrowprops=dict(arrowstyle="-|>", lw=1.2, color=BLUE))
    ax.text(2.6, 2.6, "電子", ha="right", fontsize=6.6, fontproperties=JP, color=BLUE)
    if igbt:
        ax.annotate("", xy=(7.0, 4.6), xytext=(7.0, 0.7),
                    arrowprops=dict(arrowstyle="-|>", lw=1.2, color=RED))
        ax.text(7.4, 2.6, "正孔が注入される\n（伝導度変調）", ha="left",
                fontsize=6.4, fontproperties=JP, color=RED)
        ax.text(5.0, 7.5, "E", ha="center", fontsize=8)
        ax.text(5.5, -0.5, "C", ha="left", va="center", fontsize=8)
        ax.text(5.0, -1.5, "(b) IGBT", ha="center", fontsize=7.6, fontproperties=JP)
    else:
        ax.text(5.0, 7.5, "S", ha="center", fontsize=8)
        ax.text(5.5, -0.5, "D", ha="left", va="center", fontsize=8)
        ax.text(5.0, -1.5, "(a) 縦型MOSFET", ha="center", fontsize=7.6,
                fontproperties=JP)
    ax.set_xlim(-0.6, 12.2)
    ax.set_ylim(-2.1, 8.1)
    ax.axis("off")

draw(axes[0], igbt=False)
draw(axes[1], igbt=True)

fig.tight_layout(w_pad=0.4)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig2.6.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
