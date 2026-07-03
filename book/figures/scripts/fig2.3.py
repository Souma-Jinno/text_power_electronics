#!/usr/bin/env python3
# fig2.3（第2章）: ダイオードの電流-電圧特性（概念図）。
# 順方向は約0.7 Vから指数関数的に立ち上がり，逆方向はごく小さい漏れ電流のみ。
# 逆電圧が降伏電圧に達するとなだれ降伏で電流が急増する。
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

fig, ax = plt.subplots(figsize=(4.2, 2.7))

# 概念図なので軸は目盛りなし（順方向と逆方向でスケールが違うことを注記）
# 順方向: 0.7V付近から立ち上がる指数カーブ
vf = np.linspace(0, 1.0, 300)
i_f = 0.012 * (np.exp(vf / 0.075) - 1)
i_f = np.clip(i_f, 0, 6.5)
ax.plot(vf[i_f < 6.5], i_f[i_f < 6.5], color=BLUE, lw=1.6)

# 逆方向: 小さい漏れ電流 → 降伏で急増
vr = np.linspace(-3.4, 0, 200)
i_r = -0.09 * np.ones_like(vr)
ax.plot(vr, i_r, color=BLUE, lw=1.6)
vb = np.linspace(-3.75, -3.4, 120)
i_b = -0.09 - 5.5 * (np.exp(-(vb + 3.4) / 0.09) - 1)
i_b = np.clip(i_b, -5.6, 0)
ax.plot(vb, i_b, color=BLUE, lw=1.6)

# 軸
ax.axhline(0, color="#555", lw=0.8)
ax.axvline(0, color="#555", lw=0.8)
ax.annotate("", xy=(1.35, 0), xytext=(-4.35, 0),
            arrowprops=dict(arrowstyle="-|>", lw=0.8, color="#555"))
ax.annotate("", xy=(0, 7.0), xytext=(0, -6.2),
            arrowprops=dict(arrowstyle="-|>", lw=0.8, color="#555"))
ax.text(1.28, 0.55, r"$v_D$", fontsize=9)
ax.text(0.12, 6.6, r"$i_D$", fontsize=9)

# 注釈
ax.annotate("約0.7 Vから\n電流が流れる", xy=(0.72, 1.3), xytext=(1.6, 3.3),
            fontsize=7.2, fontproperties=JP, ha="center", color="#333",
            arrowprops=dict(arrowstyle="->", lw=0.8, color="#777"))
ax.plot([0.7, 0.7], [0, -0.4], ls=":", color="#999", lw=0.8)
ax.text(0.7, -1.1, "0.7 V", ha="center", fontsize=7.2, color="#555")
ax.text(-1.7, -1.15, "漏れ電流（ごく小さい）", ha="center", fontsize=7.2,
        fontproperties=JP, color="#555")
ax.annotate("降伏\n（絶縁が破れる）", xy=(-3.62, -3.6), xytext=(-2.4, -4.6),
            fontsize=7.2, fontproperties=JP, ha="center", color=RED,
            arrowprops=dict(arrowstyle="->", lw=0.8, color=RED))
ax.plot([-3.4, -3.4], [0, 0.4], ls=":", color="#999", lw=0.8)
ax.text(-3.4, 0.75, r"$-V_{BR}$", ha="center", fontsize=7.6, color="#555")

ax.text(0.65, 5.9, "順方向\n（オン）", ha="left", fontsize=7.6, fontproperties=JP, color=BLUE)
ax.text(-2.6, 2.2, "逆方向（オフ）", ha="center", fontsize=7.6,
        fontproperties=JP, color=BLUE)
ax.text(-4.2, -5.9, "※順方向と逆方向で電圧・電流のスケールは大きく異なる",
        fontsize=6.6, fontproperties=JP, color="#888", ha="left")

ax.set_xlim(-4.5, 2.6)
ax.set_ylim(-6.4, 7.3)
ax.axis("off")
fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig2.3.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
