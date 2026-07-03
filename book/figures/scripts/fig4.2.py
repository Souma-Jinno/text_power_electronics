#!/usr/bin/env python3
# fig4.2（第4章）: エネルギーバッファとしてのインダクタ。
# 上段: 定常状態の三角波電流，下段: 磁気エネルギー W_L = (1/2)L i_L^2 の増減。
# オン期間に蓄え，オフ期間に放出する1往復が電力変換の心臓であることを見せる。
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
GREEN = "#1e8449"

D = 0.4
Imin, Imax = 1.0, 1.6

t = np.linspace(0, 2, 2001)


def i_L(t):
    tm = t % 1.0
    return np.where(tm < D, Imin + (Imax - Imin) * tm / D,
                    Imax - (Imax - Imin) * (tm - D) / (1 - D))


i = i_L(t)
W = 0.5 * i ** 2  # L=1 として正規化

fig, axes = plt.subplots(2, 1, figsize=(4.25, 2.45), sharex=True)

# 上段: 電流
ax = axes[0]
ax.plot(t, i, color=BLUE, lw=1.4)
ax.axhline((Imin + Imax) / 2, color=BLUE, lw=0.7, ls="--")
ax.text(2.02, (Imin + Imax) / 2, "平均", fontsize=6.8, fontproperties=JP,
        color=BLUE, va="center")
ax.set_ylabel("$i_L$", fontsize=8)
ax.set_yticks([Imin, Imax])
ax.set_yticklabels([r"$I_{\min}$", r"$I_{\max}$"], fontsize=7)
ax.set_ylim(0.85, 1.85)

# 下段: エネルギー
ax = axes[1]
ax.plot(t, W, color=GREEN, lw=1.4)
ax.set_ylabel(r"$W_L=\frac{1}{2}Li_L^2$", fontsize=8)
ax.set_yticks([])
ax.set_ylim(0.42, 1.55)
ax.set_xticks([0, D, 1, 1 + D, 2])
ax.set_xticklabels(["$0$", "$DT$", "$T$", "$T+DT$", "$2T$"], fontsize=7)
ax.annotate("蓄積", xy=(D / 2, 1.36), ha="center", fontsize=7.4,
            fontproperties=JP, color=RED)
ax.annotate("放出", xy=(D + (1 - D) / 2, 1.36), ha="center", fontsize=7.4,
            fontproperties=JP, color=BLUE)

# オン期間の背景を両段で塗る
for ax in axes:
    for k in range(2):
        ax.axvspan(k, k + D, color="#faeae7", lw=0, zorder=0)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.set_xlim(0, 2.0)

axes[0].text(D / 2, 1.72, "オン", ha="center", fontsize=7.0,
             fontproperties=JP, color=RED)
axes[0].text(D + (1 - D) / 2, 1.72, "オフ", ha="center", fontsize=7.0,
             fontproperties=JP, color="#555")

fig.tight_layout(h_pad=0.5)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig4.2.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
