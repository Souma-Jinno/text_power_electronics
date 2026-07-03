#!/usr/bin/env python3
# fig4.4（第4章）: LCフィルタの平滑イメージ。
# 左: スイッチング方形波（入力），右: フィルタ後のほぼ平坦な直流＋小さなリプル（出力）。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BLUE = "#2a5db0"
RED = "#c0392b"

V0 = 1.0
D = 0.4

fig, axes = plt.subplots(1, 3, figsize=(4.25, 1.7),
                         gridspec_kw={"width_ratios": [1, 0.52, 1]})

# ---------- 左: 入力方形波 ----------
ax = axes[0]
for k in range(4):
    ax.plot([k, k + D], [V0, V0], color=RED, lw=1.3)
    ax.plot([k + D, k + D], [V0, 0], color=RED, lw=0.9)
    ax.plot([k + D, k + 1], [0, 0], color=RED, lw=1.3)
    if k < 3:
        ax.plot([k + 1, k + 1], [0, V0], color=RED, lw=0.9)
ax.plot([0, 0], [0, V0], color=RED, lw=0.9)
ax.axhline(D * V0, color="#555", lw=0.8, ls="--")
ax.text(2.0, D * V0 - 0.09, "平均 $DV_0$", ha="center", va="top",
        fontsize=6.8, fontproperties=JP, color="#555")
ax.set_ylim(-0.28, 1.3)
ax.set_yticks([0, V0])
ax.set_yticklabels(["$0$", "$V_0$"], fontsize=7)
ax.set_xticks([])
ax.set_title("スイッチング波形", fontsize=7.4, fontproperties=JP, pad=3)
ax.set_xlabel("時刻 $t$", fontsize=7, fontproperties=JP)

# ---------- 中央: フィルタのブロック ----------
ax = axes[1]
ax.axis("off")
box = FancyBboxPatch((0.08, 0.36), 0.84, 0.34,
                     boxstyle="round,pad=0.03", fc="#eef3fb", ec="#666",
                     lw=0.9, transform=ax.transAxes)
ax.add_patch(box)
ax.text(0.5, 0.53, "LC\nフィルタ", ha="center", va="center", fontsize=7.4,
        fontproperties=JP, transform=ax.transAxes)
ax.annotate("", xy=(1.06, 0.26), xytext=(-0.06, 0.26),
            xycoords="axes fraction",
            arrowprops=dict(arrowstyle="-|>", lw=1.2, color="#333"))
ax.text(0.5, 0.13, "直流は通し\n高周波は遮る", ha="center", va="top",
        fontsize=6.6, fontproperties=JP, color="#555",
        transform=ax.transAxes)

# ---------- 右: 出力（平均＋小リプル） ----------
ax = axes[2]
t = np.linspace(0, 4, 1601)
tm = t % 1.0
rip = np.where(tm < D, -1 + 2 * tm / D, 1 - 2 * (tm - D) / (1 - D))
vout = D * V0 + 0.045 * rip
ax.plot(t, vout, color=BLUE, lw=1.3)
ax.axhline(D * V0, color="#555", lw=0.8, ls="--")
ax.text(2.0, D * V0 - 0.13, "平均 $DV_0$", ha="center", va="top",
        fontsize=6.8, fontproperties=JP, color="#555")
ax.annotate("リプル", xy=(3.4, D * V0 + 0.05), xytext=(2.6, 0.85),
            fontsize=6.8, fontproperties=JP, color=BLUE,
            arrowprops=dict(arrowstyle="->", lw=0.8, color=BLUE))
ax.set_ylim(-0.28, 1.3)
ax.set_yticks([0, V0])
ax.set_yticklabels(["$0$", "$V_0$"], fontsize=7)
ax.set_xticks([])
ax.set_title("フィルタ後の出力", fontsize=7.4, fontproperties=JP, pad=3)
ax.set_xlabel("時刻 $t$", fontsize=7, fontproperties=JP)

for ax in (axes[0], axes[2]):
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

fig.tight_layout(w_pad=0.3)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig4.4.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
