#!/usr/bin/env python3
# fig8.4（第8章）: 実効値の意味＝同じ発熱。
# 正弦波の瞬時電力 v^2/R は脈動するが，その時間平均は
# 実効値の直流を加えたときの一定電力に等しい（等しい発熱）。
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
SHADE = "#eef3fb"

t = np.linspace(0, 2, 1000)
v = np.sin(2 * np.pi * t)          # v(t)=Vm sin, Vm=1
p = v ** 2                          # 瞬時電力 ∝ v^2（R=1）
pavg = 0.5                          # 平均 = Vm^2/2 = Vrms^2

fig, axes = plt.subplots(2, 1, figsize=(4.0, 3.0), sharex=True)

# --- 上：電圧波形と実効値レベル
ax = axes[0]
ax.axhline(0, color=BK, lw=0.8)
ax.plot(t, v, color=BLUE, lw=1.5, zorder=3)
vrms = 1 / np.sqrt(2)
ax.axhline(vrms, color=RED, lw=1.1, ls="--", zorder=2)
ax.axhline(-vrms, color=RED, lw=1.1, ls="--", zorder=2)
ax.text(2.02, vrms, r"$V_{\mathrm{rms}}=V_m/\sqrt{2}$", color=RED, fontsize=7,
        va="center", ha="left")
ax.text(0.25, 1.10, r"$v(t)=V_m\sin\omega t$", fontsize=7, color=BLUE)
ax.set_ylim(-1.25, 1.4)
ax.set_xlim(0, 2.55)
ax.axis("off")

# --- 下：瞬時電力とその平均
ax = axes[1]
ax.axhline(0, color=BK, lw=0.8)
ax.fill_between(t, 0, p, color=SHADE, zorder=1)
ax.plot(t, p, color=BLUE, lw=1.4, zorder=3)
ax.axhline(pavg, color=RED, lw=1.3, zorder=4)
ax.text(2.02, pavg, r"平均 $=V_{\mathrm{rms}}^2/R$", color=RED, fontsize=7,
        va="center", ha="left", fontproperties=JP)
ax.text(0.20, 1.02, r"$p(t)=v^2/R$", fontsize=7, color=BLUE)
ax.text(0.62, 0.30, "山と谷が\nならされる", fontsize=6.2, fontproperties=JP,
        color="#555", ha="center")
for x in [0.5, 1.0, 1.5, 2.0]:
    ax.plot([x, x], [-0.04, 0.04], color=BK, lw=0.8)
ax.text(2.06, -0.02, r"$t$", ha="left", va="top", fontsize=7)
ax.set_ylim(-0.12, 1.15)
ax.set_xlim(0, 2.55)
ax.axis("off")

fig.subplots_adjust(hspace=0.15)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig8.4.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
