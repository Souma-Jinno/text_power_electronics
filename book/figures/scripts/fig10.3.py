#!/usr/bin/env python3
# fig10.3（第10章）: 交流位相調整回路の点弧角αと出力実効値・電力の関係。
# 実効値比 sqrt(1 - α/π + sin(2α)/(2π)) と電力比（その2乗）を描く。
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
GY = "#999999"

a = np.linspace(0, np.pi, 400)
ratio = np.sqrt(np.clip(1 - a / np.pi + np.sin(2 * a) / (2 * np.pi), 0, None))
power = ratio ** 2

fig, ax = plt.subplots(figsize=(3.4, 2.3))
ax.plot(np.degrees(a), ratio, color=BLUE, lw=1.4,
        label=r"$V_{\mathrm{rms}}(\alpha)/V_{\mathrm{rms}}(0)$")
ax.plot(np.degrees(a), power, color=RED, lw=1.2, ls="--",
        label=r"$P(\alpha)/P(0)$")

# α=90°の目安線
ax.plot([90, 90], [0, 0.707], color=GY, lw=0.6, ls=":")
ax.plot([0, 90], [0.707, 0.707], color=GY, lw=0.6, ls=":")
ax.plot([0, 90], [0.5, 0.5], color=GY, lw=0.6, ls=":")
ax.text(92, 0.72, "0.707", fontsize=6.4, color=BLUE)
ax.text(97, 0.53, "0.5", fontsize=6.4, color=RED)

ax.set_xlim(0, 180)
ax.set_ylim(0, 1.05)
ax.set_xticks([0, 30, 60, 90, 120, 150, 180])
ax.set_xlabel(r"点弧角 $\alpha$ [deg]", fontsize=7.5, fontproperties=JP)
ax.tick_params(labelsize=7)
ax.legend(fontsize=6.8, loc="upper right", frameon=False)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig10.3.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
