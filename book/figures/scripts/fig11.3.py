#!/usr/bin/env python3
# fig11.3（第11章）: dBスケールの読み方。
# 電圧の対数目盛（1μV〜1V）と dBμV 表示の対応。10倍=+20dB, 2倍=+6dB。
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
GRN = "#1e8449"

fig, ax = plt.subplots(figsize=(4.25, 1.5))

y = 0.0
ax.plot([-0.3, 6.3], [y, y], color=BK, lw=1.2)
vlabels = [r"1 $\mathrm{\mu V}$", r"10 $\mathrm{\mu V}$", r"100 $\mathrm{\mu V}$",
           "1 mV", "10 mV", "100 mV", "1 V"]
for k in range(7):
    ax.plot([k, k], [y - 0.09, y + 0.09], color=BK, lw=1.0)
    ax.text(k, y + 0.20, vlabels[k], ha="center", fontsize=6.8)
    ax.text(k, y - 0.33, f"{20*k}", ha="center", fontsize=7.2, color=BLUE)
ax.text(-0.55, y + 0.20, "電圧", ha="right", fontsize=6.8, fontproperties=JP)
ax.text(-0.55, y - 0.33, r"dB$\mathrm{\mu}$V", ha="right", fontsize=7.0, color=BLUE)

# ×10 = +20 dB
ax.annotate("", xy=(4.0, y - 0.62), xytext=(3.0, y - 0.62),
            arrowprops=dict(arrowstyle="-|>", lw=0.9, color=GRN, mutation_scale=8))
ax.text(3.5, y - 0.86, r"$\times 10 = +20$ dB", ha="center", fontsize=6.8, color=GRN)

# ×2 = +6 dB
x2 = np.log10(2)
ax.annotate("", xy=(1 + x2, y + 0.55), xytext=(1.0, y + 0.55),
            arrowprops=dict(arrowstyle="-|>", lw=0.9, color=RED, mutation_scale=7))
ax.text(1.35, y + 0.68, r"$\times 2 = +6$ dB", ha="left", fontsize=6.8, color=RED)

# 例題の値 2 mV = 66 dBμV
xm = 3 + np.log10(2)
ax.plot([xm], [y], "o", ms=4, color=RED, zorder=3)
ax.annotate(r"2 mV = 66 dB$\mathrm{\mu}$V", xy=(xm, y + 0.04), xytext=(4.35, y + 0.62),
            fontsize=6.8, color=RED,
            arrowprops=dict(arrowstyle="-", lw=0.6, color=RED))

ax.set_xlim(-1.6, 6.6)
ax.set_ylim(-1.05, 1.0)
ax.axis("off")

fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig11.3.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
