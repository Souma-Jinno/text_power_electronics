#!/usr/bin/env python3
# fig6.3（第6章）: 励磁電流と負荷電流。N1=N2, Lm=1mH, 負荷500Ω,
# ±10V・半周期1μsの方形波駆動。i1 = im（三角波）+ iℓ（方形波）。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BLUE = "#2a5db0"
RED = "#c0392b"
GREEN = "#1e7a3c"

T_half = 1.0        # us
t = np.linspace(0, 4.0, 2001)
v1 = np.where((t % (2 * T_half)) < T_half, 10.0, -10.0)   # V
# 励磁電流: 三角波 ±5 mA（定常）
phase = t % (2 * T_half)
im = np.where(phase < T_half, -5 + 10 * phase / T_half,
              5 - 10 * (phase - T_half) / T_half)          # mA
il = np.where(phase < T_half, 20.0, -20.0)                 # mA（= i2, N1=N2）
i1 = im + il

fig, axes = plt.subplots(4, 1, figsize=(4.3, 3.6), sharex=True)

axes[0].plot(t, v1, lw=1.3, color="k")
axes[0].set_ylabel(r"$v_1$ [V]", fontsize=7.5)
axes[0].set_ylim(-14, 14)
axes[0].set_yticks([-10, 0, 10])

axes[1].plot(t, im, lw=1.3, color=RED)
axes[1].set_ylabel(r"$i_m$ [mA]", fontsize=7.5)
axes[1].set_ylim(-9, 9)
axes[1].set_yticks([-5, 0, 5])
axes[1].text(3.92, 6.3, "磁束を作る（三角波）", ha="right", fontsize=6.8,
             fontproperties=JP, color=RED)

axes[2].plot(t, il, lw=1.3, color=GREEN)
axes[2].set_ylabel(r"$i_{\ell}$ [mA]", fontsize=7.5)
axes[2].set_ylim(-30, 30)
axes[2].set_yticks([-20, 0, 20])
axes[2].text(3.92, 21, "電力を運ぶ（方形波）", ha="right", fontsize=6.8,
             fontproperties=JP, color=GREEN)

axes[3].plot(t, i1, lw=1.3, color=BLUE)
axes[3].plot(t, il, lw=0.8, color=GREEN, ls=(0, (3, 2)))
axes[3].set_ylabel(r"$i_1$ [mA]", fontsize=7.5)
axes[3].set_ylim(-33, 33)
axes[3].set_yticks([-25, 0, 25])
axes[3].set_xlabel(r"$t$ [$\mu$s]", fontsize=7.5)
axes[3].text(3.92, 24.5, r"$i_1=i_m+i_{\ell}$", ha="right", fontsize=7.5,
             color=BLUE)

for ax in axes:
    ax.tick_params(labelsize=7)
    ax.axhline(0, lw=0.5, color="#999")
    for x0 in np.arange(0, 4.1, 1.0):
        ax.axvline(x0, lw=0.4, color="#ccc", zorder=0)
    ax.set_xlim(0, 4)

fig.align_ylabels(axes)
fig.tight_layout(h_pad=0.4)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig6.3.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
PNG = "/tmp/claude-1000/-home-soumajinno/e7688596-6b6f-45e4-950d-929e196c5bb6/scratchpad/fig6.3.png"
fig.savefig(PNG, format="png", dpi=160, bbox_inches="tight")
print("wrote", EPS)
