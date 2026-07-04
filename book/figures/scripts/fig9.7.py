#!/usr/bin/env python3
# fig9.7（第9章）: マルチレベルインバータの階段状出力。
# 2レベル方形波と3レベル（0, ±E/2, ±E）階段波を正弦波と比べ，
# 段数が増えるほど正弦波に近づき高調波が減ることを示す。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BK = "#222222"
RED = "#c0392b"
BLUE = "#2a5db0"
GRN = "#2e8b57"

wt = np.linspace(0, 2 * np.pi, 4001)
sine = np.sin(wt)


def quantize(x, levels):
    # levels: 昇順の許容レベル配列。最も近いレベルに丸める（階段化）
    idx = np.argmin(np.abs(x[:, None] - levels[None, :]), axis=1)
    return levels[idx]


# 2レベル: ±1
two = np.where(sine >= 0, 1.0, -1.0)
# 5レベル（フルブリッジ3レベルNPC×2 相当）: -1,-0.5,0,0.5,1
lv5 = np.array([-1.0, -0.5, 0.0, 0.5, 1.0])
five = quantize(0.98 * sine, lv5)

fig, axes = plt.subplots(1, 2, figsize=(4.3, 1.9), sharey=True)

for ax, wave, ttl, c in [(axes[0], two, "(a) 2レベル（方形波）", BLUE),
                         (axes[1], five, "(b) 多レベル（階段波）", GRN)]:
    ax.axhline(0, color=BK, lw=0.6)
    ax.plot(wt, sine, color=RED, lw=1.0, ls="--", zorder=2)
    ax.step(wt, wave, color=c, lw=1.3, where="post", zorder=3)
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(-1.4, 1.4)
    ax.set_xticks([0, np.pi, 2 * np.pi])
    ax.set_xticklabels(["0", r"$\pi$", r"$2\pi$"], fontsize=6.4)
    ax.set_title(ttl, fontproperties=JP, fontsize=7.0, color="#555")
    for s in ax.spines.values():
        s.set_visible(False)

axes[0].set_yticks([-1, -0.5, 0, 0.5, 1])
axes[0].set_yticklabels(["$-E$", r"$-\frac{E}{2}$", "0", r"$\frac{E}{2}$", "$E$"],
                        fontsize=6.2)
axes[1].text(2 * np.pi * 0.5, -1.75, "破線は目標の正弦波", ha="center",
             fontsize=6.0, fontproperties=JP, color="#555")

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig9.7.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
