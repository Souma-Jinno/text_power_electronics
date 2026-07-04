#!/usr/bin/env python3
# fig8.5（第8章）: キャパシタインプット形の電源電流と力率低下。
# 電圧は正弦波だが電流はピーク付近のパルス状。基本波成分は電圧と
# 位相はほぼ合うが振幅が小さく，高調波が実効値を膨らませて力率を下げる。
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

t = np.linspace(0, 2, 2000)
vs = np.sin(2 * np.pi * t)

# パルス状電流: 各電圧ピーク近傍で正負に鋭く流れる
def pulse(center, width, amp):
    return amp * np.exp(-((t - center) / width) ** 2)

isrc = (pulse(0.25, 0.045, 1.0) + pulse(1.25, 0.045, 1.0)
        - pulse(0.75, 0.045, 1.0) - pulse(1.75, 0.045, 1.0))
# 基本波成分（点線）: 電圧と同位相・小振幅
i1 = 0.42 * np.sin(2 * np.pi * t)

fig, ax = plt.subplots(figsize=(4.2, 2.1))
ax.axhline(0, color=BK, lw=0.8)
ax.plot(t, vs, color="#9aa7bd", lw=1.2, ls="--", zorder=2)
ax.text(0.02, 1.05, r"$v_S$（正弦波）", fontsize=7, color="#888", fontproperties=JP)
ax.plot(t, isrc, color=RED, lw=1.5, zorder=4)
ax.text(0.29, 1.02, r"$i_S$", fontsize=8, color=RED)
ax.plot(t, i1, color=BLUE, lw=1.1, ls=(0, (4, 2)), zorder=3)
ax.text(1.44, 0.30, r"基本波 $i_{S1}$", fontsize=6.6, color=BLUE, fontproperties=JP)
for x in [0.5, 1.0, 1.5, 2.0]:
    ax.plot([x, x], [-0.05, 0.05], color=BK, lw=0.8)
ax.text(1.0, -0.16, r"$\pi$", ha="center", va="top", fontsize=7)
ax.text(2.0, -0.16, r"$2\pi$", ha="center", va="top", fontsize=7)
ax.text(2.07, -0.02, r"$\omega t$", ha="left", va="top", fontsize=7)
ax.set_xlim(0, 2.2)
ax.set_ylim(-1.25, 1.3)
ax.axis("off")

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig8.5.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
