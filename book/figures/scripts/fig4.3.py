#!/usr/bin/env python3
# fig4.3（第4章）: キャパシタの積分作用（インダクタとの双対）。
# 上段: 方形波電流，下段: 三角波電圧。fig4.1(b) の v と i を入れ替えた形。
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

I0 = 1.0
D = 0.4
IN = -D / (1 - D) * I0  # 負側の電流（電荷が釣り合う値）

fig, axes = plt.subplots(2, 1, figsize=(4.25, 2.4), sharex=True)

# 上段: 方形波電流
ax = axes[0]
ax.plot([0, 0], [IN, I0], color=RED, lw=1.0)
for k in range(3):
    ax.plot([k, k + D], [I0, I0], color=RED, lw=1.4)
    ax.plot([k + D, k + D], [I0, IN], color=RED, lw=1.0)
    ax.plot([k + D, k + 1], [IN, IN], color=RED, lw=1.4)
    if k < 2:
        ax.plot([k + 1, k + 1], [IN, I0], color=RED, lw=1.0)
    ax.fill_between([k, k + D], 0, I0, color="#f7dfdb", lw=0, zorder=0)
    ax.fill_between([k + D, k + 1], IN, 0, color="#dde7f7", lw=0, zorder=0)
ax.axhline(0, color="#888", lw=0.6)
ax.set_yticks([IN, 0, I0])
ax.set_yticklabels(["$-I_1$", "$0$", "$I_0$"], fontsize=7)
ax.set_ylabel("$i_C$", fontsize=8)
ax.set_ylim(-1.05, 1.55)
ax.text(0.2, 1.14, "I", ha="center", fontsize=7.6, color=RED)
ax.text(0.72, -0.45, "II", ha="center", va="center", fontsize=7.6, color=BLUE)
ax.text(2.0, 1.16, "電荷 I ＝ 電荷 II", ha="center", fontsize=7.2,
        fontproperties=JP, color="#333")

# 下段: 三角波電圧
ax = axes[1]
v0 = 0.3
tv = [0]
vv = [v0]
for k in range(3):
    tv += [k + D, k + 1]
    vv += [v0 + D * I0, v0]
ax.plot(tv, vv, color=BLUE, lw=1.4)
ax.axhline(0, color="#888", lw=0.6)
ax.axhline(v0 + D * I0 / 2, color=BLUE, lw=0.7, ls="--")
ax.text(3.02, v0 + D * I0 / 2, "平均", fontsize=6.8, fontproperties=JP,
        color=BLUE, va="center")
ax.set_yticks([0])
ax.set_yticklabels(["$0$"], fontsize=7)
ax.set_ylabel("$v_C$", fontsize=8)
ax.set_ylim(-0.15, 1.0)
ax.set_xticks([0, D, 1, 2, 3])
ax.set_xticklabels(["$0$", "$DT$", "$T$", "$2T$", "$3T$"], fontsize=7)
ax.text(1.55, 0.84, "傾き $i_C/C$ の三角波", ha="center", fontsize=7.2,
        fontproperties=JP, color=BLUE)

for ax in axes:
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.set_xlim(0, 3.0)

fig.tight_layout(h_pad=0.5)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig4.3.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
