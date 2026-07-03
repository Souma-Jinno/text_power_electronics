#!/usr/bin/env python3
# fig3.5（第3章）: デバイス選択の地図（スイッチング周波数-電力容量平面のすみ分け）。
# 軸は log10。サイリスタ/IGBT/Si-MOSFETのすみ分けと，SiC/GaNによる拡張を示す。
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

fig, ax = plt.subplots(figsize=(4.25, 2.95))

# (log10 f中心, log10 P中心, 幅, 高さ, 名称, 色, 実線/破線)
regions = [
    (2.2, 7.5, 1.6, 3.2, "サイリスタ", "#b8cce4", "solid"),
    (3.7, 5.3, 2.2, 3.4, "IGBT",       "#f2c48c", "solid"),
    (5.0, 2.1, 2.4, 2.8, "Si-MOSFET",  "#c9e0b8", "solid"),
    (4.9, 4.6, 2.0, 2.6, "SiC-MOSFET", "#8fb8e8", "dashed"),
    (6.0, 2.6, 2.2, 2.4, "GaN",        "#88c8a0", "dashed"),
]
for x, y, w, h, name, col, ls in regions:
    e = Ellipse((x, y), w, h, fc=col, ec="#444", lw=0.9, alpha=0.55, ls=ls)
    ax.add_patch(e)
for x, y, name in [(2.2, 8.35, "サイリスタ"), (3.15, 6.35, "IGBT"),
                   (4.35, 1.15, "Si-MOSFET"), (5.35, 5.35, "SiC-MOSFET"),
                   (6.45, 3.35, "GaN")]:
    ax.text(x, y, name, ha="center", fontsize=7.4, fontproperties=JP, color="#222")

apps = [
    (1.28, 7.0, "直流送電・電鉄\n製鉄"),
    (3.28, 4.35, "EV・産業モータ\n鉄道"),
    (4.35, 2.7, "電源アダプタ\nサーバ電源"),
    (6.35, 1.6, "急速充電器\n小型電源"),
]
for x, y, s in apps:
    ax.text(x, y, s, fontsize=6.2, fontproperties=JP, color="#555",
            ha="center", va="center")

# SiC/GaN が Si の領域を右上へ広げる矢印
ax.annotate("", xy=(5.45, 4.6), xytext=(4.3, 5.6),
            arrowprops=dict(arrowstyle="-|>", lw=1.0, color="#1a5276", ls="--"))
ax.text(5.6, 6.3, "SiC・GaNが\n高周波側へ広げる（3.5節）", fontsize=6.6,
        fontproperties=JP, color="#1a5276", ha="center")

ax.set_xlim(0.7, 7.6)
ax.set_ylim(0.5, 9.2)
ax.set_xticks(range(1, 8))
ax.set_xticklabels(["10", "100", "1k", "10k", "100k", "1M", "10M"], fontsize=7)
ax.set_yticks(range(1, 10))
ax.set_yticklabels(["10", "100", "1k", "10k", "100k", "1M", "10M", "100M", "1G"],
                   fontsize=7)
ax.set_xlabel("スイッチング周波数 [Hz]", fontsize=8, fontproperties=JP)
ax.set_ylabel("電力容量 [V$\\cdot$A]", fontsize=8, fontproperties=JP)
ax.grid(True, ls=":", lw=0.4, color="#ccc")
fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig3.5.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
fig.savefig("/tmp/claude-1000/-home-soumajinno/e7688596-6b6f-45e4-950d-929e196c5bb6/scratchpad/fig3.5.png",
            dpi=180, bbox_inches="tight")
print("wrote", EPS)
