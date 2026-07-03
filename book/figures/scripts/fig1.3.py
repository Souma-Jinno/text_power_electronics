#!/usr/bin/env python3
# fig1.3（第1章）: キャリアが動く2つのしくみ ― ドリフト（電場）と拡散（濃度差）。
# ドリフトはオン抵抗（3章），拡散はpn接合（1.6節）につながる基礎図。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BLUE = "#2a5db0"
RED = "#c0392b"

fig, axes = plt.subplots(1, 2, figsize=(4.4, 1.95))

# --- (a) ドリフト
ax = axes[0]
ax.add_patch(Rectangle((0, 0), 4.0, 2.2, fc="#eef3fb", ec="#888", lw=0.9))
# 電場の矢印（右向き）
ax.annotate("", xy=(3.4, 2.6), xytext=(0.6, 2.6),
            arrowprops=dict(arrowstyle="-|>", lw=1.3, color=RED))
ax.text(2.0, 2.75, r"電場 $\mathcal{E}$", ha="center", fontsize=7.8,
        fontproperties=JP, color=RED)
# 電子のジグザグ軌道（左向きに進む）
rng = np.random.default_rng(7)
x = [3.5]
y = [1.1]
for i in range(7):
    x.append(x[-1] - 0.42)
    y.append(1.1 + (0.45 if i % 2 == 0 else -0.45) * rng.uniform(0.6, 1.0))
ax.plot(x, y, lw=0.9, color=BLUE)
for xi, yi in zip(x[1:-1], y[1:-1]):
    ax.plot(xi, yi, "x", ms=3.4, color="#999", mew=0.9)
ax.plot(x[-1], y[-1], "o", ms=4.2, color=BLUE)
ax.text(0.28, 1.95, "電子", fontsize=7.2, fontproperties=JP,
        color=BLUE, ha="left", va="top")
# 平均速度の矢印
ax.annotate("", xy=(1.0, 0.42), xytext=(2.6, 0.42),
            arrowprops=dict(arrowstyle="-|>", lw=1.4, color=BLUE))
ax.text(1.8, 0.3, r"$v_d=\mu\mathcal{E}$", ha="center", va="top", fontsize=8,
        color=BLUE)
ax.text(2.0, -0.85, "(a) ドリフト：電場に押されて流れる\n（×印は結晶との衝突）",
        ha="center", fontsize=7.2, fontproperties=JP, color="#555")
ax.set_xlim(-0.3, 4.3)
ax.set_ylim(-1.35, 3.1)
ax.axis("off")

# --- (b) 拡散
ax = axes[1]
ax.add_patch(Rectangle((0, 0), 4.0, 2.2, fc="#eef3fb", ec="#888", lw=0.9))
rng = np.random.default_rng(3)
# 左が濃く右が薄い分布
for i in range(46):
    xi = 4.0 * rng.beta(1.3, 2.6)
    yi = rng.uniform(0.15, 2.05)
    ax.plot(xi, yi, "o", ms=2.6, color=BLUE)
ax.annotate("", xy=(3.3, 2.6), xytext=(1.4, 2.6),
            arrowprops=dict(arrowstyle="-|>", lw=1.4, color=BLUE))
ax.text(2.35, 2.75, "キャリアの流れ", ha="center", fontsize=7.2,
        fontproperties=JP, color=BLUE)
ax.text(0.75, -0.28, "濃い", ha="center", fontsize=7.2, fontproperties=JP, color="#555")
ax.text(3.3, -0.28, "薄い", ha="center", fontsize=7.2, fontproperties=JP, color="#555")
ax.text(2.0, -0.85, "(b) 拡散：濃度の高い方から\n低い方へ広がる", ha="center",
        fontsize=7.2, fontproperties=JP, color="#555")
ax.set_xlim(-0.3, 4.3)
ax.set_ylim(-1.35, 3.1)
ax.axis("off")

fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig1.3.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
