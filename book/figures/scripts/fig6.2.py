#!/usr/bin/env python3
# fig6.2（第6章）: 変圧器の構造と等価回路。(a)鉄心と2巻線・磁束Φ，
# (b)理想変圧器+励磁インダクタンス Lm の等価回路。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BLUE = "#2a5db0"
RED = "#c0392b"

def coil_v(ax, x, y0, y1, n=4, side=1, color="k"):
    ys = np.linspace(y0, y1, n + 1)
    for i in range(n):
        t = np.linspace(-np.pi / 2, np.pi / 2, 24)
        r = (ys[i + 1] - ys[i]) / 2
        yc = (ys[i] + ys[i + 1]) / 2
        ax.plot(x + side * r * 1.1 * np.cos(t), yc + r * np.sin(t),
                lw=1.2, color=color)

fig, axes = plt.subplots(1, 2, figsize=(4.3, 2.25),
                         gridspec_kw={"width_ratios": [1.05, 1.0]})

# --- (a) 構造
ax = axes[0]
# 鉄心（外形と窓）
ax.add_patch(Rectangle((0.6, 0.3), 2.4, 2.4, fc="#e7e7e7", ec="#777", lw=1.1))
ax.add_patch(Rectangle((1.15, 0.85), 1.3, 1.3, fc="w", ec="#777", lw=1.1))
# 磁束の周回矢印（窓の中を回る破線）
ax.add_patch(FancyArrowPatch((1.62, 2.47), (2.05, 2.47), arrowstyle="-|>",
                             mutation_scale=9, lw=1.0, color=RED))
t = np.linspace(0, 2 * np.pi, 100)
ax.plot(1.8 + 1.0 * np.cos(t), 1.5 + 0.97 * np.sin(t), ls=(0, (3, 2)),
        lw=1.0, color=RED)
ax.text(1.8, 1.5, r"$\mathit{\Phi}$", ha="center", va="center",
        fontsize=9, color=RED)
# 1次巻線
ax.plot([-0.15, 0.38], [2.35, 2.35], lw=1.1, color="k")
ax.plot([-0.15, 0.38], [0.65, 0.65], lw=1.1, color="k")
coil_v(ax, 0.38, 0.65, 2.35, n=4, side=-1, color=BLUE)
ax.text(-0.32, 1.5, r"$v_1$", ha="center", va="center", fontsize=8.5)
ax.plot(-0.15, 2.35, "o", ms=2.8, mfc="w", mec="k", mew=0.9)
ax.plot(-0.15, 0.65, "o", ms=2.8, mfc="w", mec="k", mew=0.9)
ax.text(0.62, 1.5, r"$N_1$", ha="center", va="center", fontsize=8)
# 2次巻線
ax.plot([3.22, 3.75], [2.35, 2.35], lw=1.1, color="k")
ax.plot([3.22, 3.75], [0.65, 0.65], lw=1.1, color="k")
coil_v(ax, 3.22, 0.65, 2.35, n=4, side=1, color=BLUE)
ax.text(3.94, 1.5, r"$v_2$", ha="center", va="center", fontsize=8.5)
ax.plot(3.75, 2.35, "o", ms=2.8, mfc="w", mec="k", mew=0.9)
ax.plot(3.75, 0.65, "o", ms=2.8, mfc="w", mec="k", mew=0.9)
ax.text(2.99, 1.5, r"$N_2$", ha="center", va="center", fontsize=8)
ax.text(1.8, 3.0, "鉄心", ha="center", fontsize=7.2, fontproperties=JP,
        color="#555")
ax.text(1.8, -0.4, "(a) 構造", ha="center", fontsize=7.4,
        fontproperties=JP, color="#555")
ax.set_xlim(-0.85, 4.45)
ax.set_ylim(-0.75, 3.35)
ax.set_aspect("equal")
ax.axis("off")

# --- (b) 等価回路
ax = axes[1]
# 端子とリード
ax.plot([-0.1, 1.0], [2.35, 2.35], lw=1.1, color="k")
ax.plot([-0.1, 1.0], [0.65, 0.65], lw=1.1, color="k")
ax.plot(-0.1, 2.35, "o", ms=2.8, mfc="w", mec="k", mew=0.9)
ax.plot(-0.1, 0.65, "o", ms=2.8, mfc="w", mec="k", mew=0.9)
# 励磁インダクタンス（並列枝）
ax.plot([1.0, 1.0], [2.35, 2.05], lw=1.1, color="k")
ax.plot([1.0, 1.0], [0.65, 0.95], lw=1.1, color="k")
coil_v(ax, 1.0, 0.95, 2.05, n=4, side=-1, color=RED)
ax.plot(1.0, 2.35, "o", ms=2.0, color="k")
ax.plot(1.0, 0.65, "o", ms=2.0, color="k")
ax.text(0.62, 1.5, r"$L_m$", ha="center", va="center", fontsize=8.5, color=RED)
ax.text(0.55, 2.85, "励磁インダクタンス", ha="center", va="bottom", fontsize=6.6,
        fontproperties=JP, color=RED)
# 理想変圧器
ax.plot([1.0, 2.1], [2.35, 2.35], lw=1.1, color="k")
ax.plot([1.0, 2.1], [0.65, 0.65], lw=1.1, color="k")
coil_v(ax, 2.1, 0.85, 2.15, n=4, side=1, color=BLUE)
ax.plot([2.1, 2.1], [2.15, 2.35], lw=1.1, color="k")
ax.plot([2.1, 2.1], [0.65, 0.85], lw=1.1, color="k")
ax.plot([2.32, 2.32], [0.7, 2.3], lw=1.1, color="k")
ax.plot([2.42, 2.42], [0.7, 2.3], lw=1.1, color="k")
coil_v(ax, 2.64, 0.85, 2.15, n=4, side=-1, color=BLUE)
ax.plot([2.64, 2.64], [2.15, 2.35], lw=1.1, color="k")
ax.plot([2.64, 2.64], [0.65, 0.85], lw=1.1, color="k")
ax.plot([2.64, 3.6], [2.35, 2.35], lw=1.1, color="k")
ax.plot([2.64, 3.6], [0.65, 0.65], lw=1.1, color="k")
ax.plot(3.6, 2.35, "o", ms=2.8, mfc="w", mec="k", mew=0.9)
ax.plot(3.6, 0.65, "o", ms=2.8, mfc="w", mec="k", mew=0.9)
# 極性マーク
ax.plot(1.92, 2.18, "o", ms=2.6, color="k")
ax.plot(2.82, 2.18, "o", ms=2.6, color="k")
ax.text(2.37, 2.72, r"$N_1:N_2$", ha="center", fontsize=8)
ax.text(2.37, 0.25, "理想変圧器", ha="center", va="top", fontsize=6.6,
        fontproperties=JP, color=BLUE)
ax.text(1.55, -0.62, "(b) 等価回路", ha="center", fontsize=7.4,
        fontproperties=JP, color="#555")
ax.set_xlim(-0.6, 4.0)
ax.set_ylim(-0.75, 3.35)
ax.set_aspect("equal")
ax.axis("off")

fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig6.2.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
PNG = "/tmp/claude-1000/-home-soumajinno/e7688596-6b6f-45e4-950d-929e196c5bb6/scratchpad/fig6.2.png"
fig.savefig(PNG, format="png", dpi=160, bbox_inches="tight")
print("wrote", EPS)
