#!/usr/bin/env python3
# fig7.3（第7章）: ツェナーダイオードの電圧-電流特性。順方向は普通のダイオードと
# 同じ。逆方向はツェナー電圧V_Zで降伏し，電流が変わっても電圧はほぼV_Zに保たれる
# （垂直に近い特性）。この垂直部を動作点に使うと定電圧源になる。
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
BK = "#222222"

Vz = 4.7

fig, ax = plt.subplots(figsize=(3.7, 2.5))

# 順方向（V>0.6で立ち上がる）
vf = np.linspace(0.0, 0.85, 200)
i_f = 0.02 * (np.exp((vf - 0.6) / 0.06) - 1)
i_f = np.clip(i_f, 0, 6.0)
ax.plot(vf, i_f, color=BLUE, lw=1.6, zorder=3)

# 逆方向（-Vz付近で降伏，電圧はほぼV_Zのまま電流が流れる＝垂直に近い）
vr = np.linspace(-Vz - 0.45, 0.0, 400)
i_r = -0.02 * (np.exp(-(vr + Vz) / 0.06) - 1)
i_r = np.clip(i_r, -6.0, 0)
ax.plot(vr, i_r, color=BLUE, lw=1.6, zorder=3)

# 軸
ax.axhline(0, color=BK, lw=0.7)
ax.axvline(0, color=BK, lw=0.7)

# 動作点（逆方向の垂直部・曲線上）
vop = -Vz - 0.30
ax.plot([vop], [-3.0], "o", ms=5, color=RED, zorder=5)
ax.annotate("動作点", xy=(vop, -3.0), xytext=(-3.3, -4.7),
            fontproperties=JP, fontsize=8, color=RED,
            arrowprops=dict(arrowstyle="-|>", lw=0.8, color=RED))

# V_Z の表示
ax.annotate("", xy=(-Vz, 0.4), xytext=(0, 0.4),
            arrowprops=dict(arrowstyle="<->", lw=0.8, color=BK))
ax.text(-Vz / 2, 0.9, r"$V_Z$", ha="center", fontsize=9, color=BK)
ax.plot([-Vz, -Vz], [0, -5.5], color="#999", lw=0.6, ls=":")

ax.text(0.55, 4.9, r"順方向", fontproperties=JP, fontsize=7.5, color=BLUE)
ax.text(-4.5, 2.0, r"逆方向", fontproperties=JP, fontsize=7.5, color=BLUE)
ax.text(-1.6, -1.5, "降伏", fontproperties=JP, fontsize=7.5, color=BK)

ax.set_xlabel(r"逆電圧 $\leftarrow\ V\ \rightarrow$ 順電圧 [V]",
              fontproperties=JP, fontsize=8)
ax.set_ylabel("電流 $I$ [任意単位]", fontproperties=JP, fontsize=8)
ax.set_xlim(-6.2, 1.4)
ax.set_ylim(-6.0, 6.0)
ax.tick_params(labelsize=7)
for s in ax.spines.values():
    s.set_visible(False)

fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig7.3.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
