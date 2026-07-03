#!/usr/bin/env python3
# fig5.8（第5章）: スイッチング周波数と必要な L・C の値。
# 例題5.3・5.4 の設計（12 V→5 V, 2 A, ΔI_L=0.4 A, ΔV_out=50 mV）で，
# 同じリプルを保ったまま f を変えると L も C も 1/f で小さくできる。
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

Vin, Vout, dI, dV = 12.0, 5.0, 0.4, 0.05
Dd = Vout / Vin

f = np.logspace(4, 6, 200)
L_uH = (Vin - Vout) * Dd / (f * dI) * 1e6
C_uF = dI / (8 * f * dV) * 1e6

fig, axes = plt.subplots(1, 2, figsize=(4.25, 1.9))

for ax, y, lab, mark in [(axes[0], L_uH, r"$L$ [$\mu$H]", 72.9),
                         (axes[1], C_uF, r"$C$ [$\mu$F]", 10.0)]:
    ax.loglog(f, y, color=BLUE, lw=1.3)
    ax.loglog([1e5], [mark], "o", ms=4, color=RED, zorder=3)
    ax.set_xlabel("$f$ [Hz]", fontsize=7)
    ax.set_ylabel(lab, fontsize=7)
    ax.tick_params(labelsize=6.5, which="both")
    ax.grid(True, which="both", lw=0.3, color="#ccc", ls=":")
    for s in ax.spines.values():
        s.set_linewidth(0.6)

axes[0].annotate(r"$73\ \mu$H", xy=(1e5, 72.9), xytext=(1.7e5, 150),
                 fontsize=6.6, color=RED,
                 arrowprops=dict(arrowstyle="-", lw=0.5, color=RED))
axes[1].annotate(r"$10\ \mu$F", xy=(1e5, 10.0), xytext=(1.7e5, 21),
                 fontsize=6.6, color=RED,
                 arrowprops=dict(arrowstyle="-", lw=0.5, color=RED))
axes[0].text(3e4, 25, r"$\propto 1/f$", fontsize=7, color=BLUE)
axes[1].text(3e4, 3.5, r"$\propto 1/f$", fontsize=7, color=BLUE)

fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig5.8.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
