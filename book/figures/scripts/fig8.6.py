#!/usr/bin/env python3
# fig8.6（第8章）: 歪み電流の高調波スペクトル（棒グラフ）とTHD。
# 基本波を1に規格化し，奇数次高調波の相対振幅を示す。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BK = "#222222"
BLUE = "#2a5db0"
RED = "#c0392b"

# 例題と対応: 基本波1，3次0.5，5次0.2（THD=0.54）
orders = [1, 3, 5, 7, 9]
amp = [1.0, 0.5, 0.2, 0.10, 0.05]

fig, ax = plt.subplots(figsize=(3.9, 2.1))
colors = [BLUE] + [RED] * (len(orders) - 1)
bars = ax.bar([str(n) for n in orders], amp, width=0.5, color=colors, zorder=3)
for n, a in zip(orders, amp):
    ax.text(str(n), a + 0.03, f"{a:.2f}", ha="center", fontsize=6.6)
ax.axhline(0, color=BK, lw=0.8)
ax.set_ylim(0, 1.2)
ax.set_xlabel("高調波の次数 $n$", fontproperties=JP, fontsize=8)
ax.set_ylabel("相対振幅 $i_n/i_1$", fontproperties=JP, fontsize=8)
ax.text(2.3, 0.85, r"基本波$=1$", color=BLUE, fontsize=7, fontproperties=JP)
ax.text(2.3, 0.68, r"$\mathrm{THD}=\dfrac{\sqrt{i_3^2+i_5^2+\cdots}}{i_1}$",
        color=RED, fontsize=7.5)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.tick_params(labelsize=7)
for lb in ax.get_yticklabels():
    lb.set_fontsize(7)

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig8.6.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
