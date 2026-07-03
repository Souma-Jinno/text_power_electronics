#!/usr/bin/env python3
# fig0.1（序章）: 電力変換の地図。DC/AC の入出力 2×2 マトリクスと担当章。
# 本書の「地図」— 各章の現在地表示の基点になる図。
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BLUE = "#2a5db0"
RED = "#c0392b"

fig, ax = plt.subplots(figsize=(4.4, 3.0))

nodes = {
    "DCin":  (0.0, 2.1, "直流\n(バッテリー・太陽電池)"),
    "ACin":  (0.0, 0.0, "交流\n(コンセント・発電機)"),
    "DCout": (3.4, 2.1, "直流\n(電子機器・充電)"),
    "ACout": (3.4, 0.0, "交流\n(モータ・送電網)"),
}
for key, (x, y, label) in nodes.items():
    box = FancyBboxPatch((x, y), 1.5, 0.85, boxstyle="round,pad=0.08",
                         fc="#eef3fb", ec=BLUE, lw=1.1)
    ax.add_patch(box)
    ax.text(x + 0.75, y + 0.425, label, ha="center", va="center",
            fontsize=7.4, fontproperties=JP)

def arrow(p, q, label, dy, color=BLUE, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=11,
                                 lw=1.3, color=color,
                                 connectionstyle=f"arc3,rad={rad}"))
    m = ((p[0]+q[0])/2, (p[1]+q[1])/2 + dy)
    ax.text(m[0], m[1], label, ha="center", fontsize=7.4,
            fontproperties=JP, color=color)

arrow((1.6, 2.6), (3.3, 2.6), "DC-DC変換（5〜7章）", 0.14)
arrow((1.6, 0.32), (3.3, 0.32), "AC-AC変換（10章）", -0.32)
ax.add_patch(FancyArrowPatch((1.35, 0.95), (3.5, 2.0), arrowstyle="-|>",
                             mutation_scale=11, lw=1.3, color=RED,
                             connectionstyle="arc3,rad=0.12"))
ax.text(3.35, 1.45, "DC-AC変換\nインバータ（9章）", ha="left", fontsize=7.4,
        fontproperties=JP, color=RED)
ax.text(1.55, 1.45, "AC-DC変換\n整流（8章）", ha="right", fontsize=7.4,
        fontproperties=JP, color=RED)
ax.add_patch(FancyArrowPatch((1.35, 2.0), (3.5, 0.95), arrowstyle="-|>",
                             mutation_scale=11, lw=1.3, color=RED,
                             connectionstyle="arc3,rad=0.12"))

ax.text(0.75, 3.25, "入力", ha="center", fontsize=8.2, fontproperties=JP, color="#555")
ax.text(4.15, 3.25, "出力", ha="center", fontsize=8.2, fontproperties=JP, color="#555")
ax.text(2.45, -0.75, "切り替え役＝半導体スイッチ（第I部），蓄え役＝L・C（4章）",
        ha="center", fontsize=7.4, fontproperties=JP, color="#555")

ax.set_xlim(-0.3, 5.2)
ax.set_ylim(-1.0, 3.5)
ax.set_aspect("equal")
ax.axis("off")
fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig0.1.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
