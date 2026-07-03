#!/usr/bin/env python3
# fig2.4（第2章）: MOSFETの構造と反転層。
# (a) 横型MOSFETの断面。ゲート電圧ゼロでは2つのpn接合が電流を止める。
# (b) ゲートに正電圧をかけると酸化膜下のp形表面に反転層（nチャネル）ができ，
#     ソース-ドレイン間がつながる。
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

fig, axes = plt.subplots(1, 2, figsize=(4.4, 2.15))

def draw_mosfet(ax, on):
    # p形基板
    ax.add_patch(Rectangle((0, 0), 10, 5, fc="#fdeceb", ec="#555", lw=0.9))
    # n形ウェル（ソース・ドレイン）
    ax.add_patch(Rectangle((0.7, 3.4), 2.2, 1.6, fc="#eaf0fa", ec="#555", lw=0.9))
    ax.add_patch(Rectangle((7.1, 3.4), 2.2, 1.6, fc="#eaf0fa", ec="#555", lw=0.9))
    ax.text(1.8, 4.15, "n", ha="center", va="center", fontsize=8)
    ax.text(8.2, 4.15, "n", ha="center", va="center", fontsize=8)
    ax.text(5.0, 1.6, "p", ha="center", va="center", fontsize=8)
    # 酸化膜とゲート電極
    ax.add_patch(Rectangle((2.9, 5.0), 4.2, 0.5, fc="#e8e8e8", ec="#555", lw=0.9))
    ax.add_patch(Rectangle((3.3, 5.5), 3.4, 0.55, fc="#c9c9c9", ec="#555", lw=0.9))
    ax.annotate("ゲート電極", xy=(3.5, 5.78), xytext=(-0.2, 7.5),
                fontsize=6.2, fontproperties=JP, color="#333", ha="left",
                arrowprops=dict(arrowstyle="-", lw=0.6, color="#888"))
    ax.annotate("酸化膜（絶縁体）", xy=(6.9, 5.25), xytext=(10.4, 7.5),
                fontsize=6.2, fontproperties=JP, color="#333", ha="right",
                arrowprops=dict(arrowstyle="-", lw=0.6, color="#888"))
    # 端子
    ax.plot([1.8, 1.8], [5.0, 6.6], color="#333", lw=1.0)
    ax.plot([8.2, 8.2], [5.0, 6.6], color="#333", lw=1.0)
    ax.plot([5.0, 5.0], [6.05, 6.6], color="#333", lw=1.0)
    ax.text(1.35, 6.5, "S", ha="right", fontsize=8)
    ax.text(5.0, 6.95, "G", ha="center", fontsize=8)
    ax.text(8.65, 6.5, "D", ha="left", fontsize=8)
    if not on:
        # 空乏層（pn接合のところ）で電流が止まる
        ax.text(5.0, 3.9, "×", ha="center", va="center", fontsize=11, color=RED)
        ax.text(5.0, -0.8, r"$v_{GS}=0$：オフ", ha="center", fontsize=7.2,
                fontproperties=JP, color="#333")
        ax.text(5.0, -1.75, "2つのpn接合が\n電流を止める", ha="center", va="top",
                fontsize=6.6, fontproperties=JP, color="#555")
    else:
        # 反転層
        ax.add_patch(Rectangle((2.9, 4.62), 4.2, 0.38, fc=MAG, ec="none"))
        ax.annotate("反転層（nチャネル）", xy=(5.0, 4.7), xytext=(5.0, 2.6),
                    fontsize=6.6, fontproperties=JP, ha="center", color=MAG,
                    arrowprops=dict(arrowstyle="->", lw=0.8, color=MAG))
        # 電子の流れ
        ax.annotate("", xy=(8.0, 4.15), xytext=(2.0, 4.15),
                    arrowprops=dict(arrowstyle="-|>", lw=1.3, color=BLUE))
        ax.text(5.0, -0.8, r"$v_{GS}>V_{th}$：オン", ha="center", fontsize=7.2,
                fontproperties=JP, color="#333")
        ax.text(5.0, -1.75, "表面がn形に反転し\n電子の通り道ができる", ha="center",
                va="top", fontsize=6.6, fontproperties=JP, color="#555")
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-4.6, 8.5)
    ax.axis("off")

draw_mosfet(axes[0], on=False)
draw_mosfet(axes[1], on=True)
axes[0].text(5.0, -4.3, "(a)", ha="center", fontsize=8)
axes[1].text(5.0, -4.3, "(b)", ha="center", fontsize=8)

fig.tight_layout(w_pad=0.5)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig2.4.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
