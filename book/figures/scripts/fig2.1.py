#!/usr/bin/env python3
# fig2.1（第2章）: 半導体スイッチの応用マップ。
# 縦軸=扱う電力（容量），横軸=スイッチング周波数。サイリスタ・IGBT・MOSFETの
# 得意領域と代表的な応用先を示す概念図。
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BLUE = "#2a5db0"
RED = "#c0392b"

fig, ax = plt.subplots(figsize=(4.3, 2.9))

# 概念図：軸はけた（対数）のイメージ。x=log10(f/Hz), y=log10(S/VA)
def region(x0, y0, w, h, fc, ec):
    r = FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.12",
                       fc=fc, ec=ec, lw=1.1)
    ax.add_patch(r)

# サイリスタ: 低周波・大容量
region(1.7, 6.2, 1.5, 2.3, "#fdeceb", RED)
ax.text(2.45, 8.05, "サイリスタ", ha="center", fontsize=8.2, fontproperties=JP, color=RED)
ax.text(2.45, 7.15, "電鉄・製鉄\n直流送電", ha="center", va="center",
        fontsize=7.0, fontproperties=JP, color="#555")

# IGBT: 中周波・中〜大容量
region(3.2, 4.0, 1.9, 2.6, "#f5f0e3", "#8a6d1f")
ax.text(4.15, 6.1, "IGBT", ha="center", fontsize=8.2, color="#8a6d1f")
ax.text(4.15, 5.1, "電気自動車\n産業用モータ\n太陽光発電", ha="center", va="center",
        fontsize=7.0, fontproperties=JP, color="#555")

# MOSFET: 高周波・小容量
region(5.0, 1.6, 1.9, 2.5, "#eaf0fa", BLUE)
ax.text(5.95, 3.6, "MOSFET", ha="center", fontsize=8.2, color=BLUE)
ax.text(5.95, 2.65, "電源装置\n家電・情報機器", ha="center", va="center",
        fontsize=7.0, fontproperties=JP, color="#555")

# SiC・GaNによる拡大の矢印
ax.annotate("", xy=(6.4, 5.6), xytext=(5.1, 4.3),
            arrowprops=dict(arrowstyle="-|>", lw=1.2, color="#3a7d44", ls="--"))
ax.text(6.05, 5.85, "SiC・GaNで\n領域が広がる", ha="center", fontsize=7.0,
        fontproperties=JP, color="#3a7d44")

# 軸
ax.annotate("", xy=(7.6, 0.6), xytext=(1.0, 0.6),
            arrowprops=dict(arrowstyle="-|>", lw=1.0, color="#333"))
ax.annotate("", xy=(1.0, 9.3), xytext=(1.0, 0.6),
            arrowprops=dict(arrowstyle="-|>", lw=1.0, color="#333"))
ax.text(4.4, -0.55, "スイッチング周波数", ha="center", fontsize=7.8, fontproperties=JP)
ax.text(-0.35, 5.0, "扱う電力", rotation=90, va="center", ha="center",
        fontsize=7.8, fontproperties=JP)

# 目盛りのめやす（けた）
for x, lab in [(2.0, "50 Hz"), (3.9, "10 kHz"), (5.9, "1 MHz")]:
    ax.plot([x, x], [0.52, 0.68], color="#333", lw=0.8)
    ax.text(x, 0.15, lab, ha="center", fontsize=6.8)
for y, lab in [(2.3, "1 kW"), (5.1, "1 MW"), (7.9, "1 GW")]:
    ax.plot([0.93, 1.07], [y, y], color="#333", lw=0.8)
    ax.text(0.85, y, lab, ha="right", va="center", fontsize=6.8)

ax.set_xlim(-0.7, 7.9)
ax.set_ylim(-1.0, 9.6)
ax.axis("off")
fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig2.1.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
