#!/usr/bin/env python3
# fig6.1（第6章）: 絶縁の役割。(a)非絶縁型は出力が入力側の電位を引きずり，
# (b)絶縁型はトランスが電流の道を断ち切って2次側で新しい基準電位を選べる。
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

def ground(ax, x, y, s=0.16):
    ax.plot([x, x], [y, y - s], lw=1.0, color="k")
    for i, w in enumerate([s * 1.0, s * 0.62, s * 0.28]):
        ax.plot([x - w, x + w], [y - s - i * 0.07, y - s - i * 0.07],
                lw=1.0, color="k")

def coil_v(ax, x, y0, y1, n=4, side=1, color="k"):
    """縦向き巻線: (x,y0)-(x,y1) に n 個の半円こぶ"""
    ys = np.linspace(y0, y1, n + 1)
    for i in range(n):
        t = np.linspace(-np.pi / 2, np.pi / 2, 24)
        r = (ys[i + 1] - ys[i]) / 2
        yc = (ys[i] + ys[i + 1]) / 2
        ax.plot(x + side * r * 1.1 * np.cos(t), yc + r * np.sin(t),
                lw=1.1, color=color)

fig, axes = plt.subplots(1, 2, figsize=(4.3, 2.35))

for k, ax in enumerate(axes):
    iso = (k == 1)
    # 入力端子（コンセント系）
    ax.text(0.15, 2.62, "コンセント側\n（片側が接地）", ha="center", fontsize=6.8,
            fontproperties=JP)
    ax.plot([0.0, 0.7], [2.1, 2.1], lw=1.1, color="k")
    ax.plot([0.0, 0.7], [0.6, 0.6], lw=1.1, color="k")
    ax.plot([0.0, 0.0], [0.6, 2.1], lw=1.1, color="k")
    ground(ax, 0.0, 0.6)
    if not iso:
        # 変換器の箱（入出力が導線で直結）
        box = FancyBboxPatch((0.7, 0.35), 1.6, 2.0, boxstyle="round,pad=0.05",
                             fc="#eef3fb", ec=BLUE, lw=1.1)
        ax.add_patch(box)
        ax.text(1.5, 1.35, "非絶縁\nDC-DC", ha="center", va="center",
                fontsize=7.2, fontproperties=JP, color=BLUE)
        # 下側レールが素通し
        ax.plot([0.7, 2.3], [0.6, 0.6], lw=1.6, color=RED, zorder=3)
        ax.plot([2.3, 3.1], [2.1, 2.1], lw=1.1, color="k")
        ax.plot([2.3, 3.1], [0.6, 0.6], lw=1.6, color=RED)
        ax.plot(3.1, 2.1, "o", ms=3.2, mfc="w", mec="k", mew=1.0)
        ax.plot(3.1, 0.6, "o", ms=3.2, mfc="w", mec="k", mew=1.0)
        ax.text(3.3, 1.35, "出力", fontsize=7.2, fontproperties=JP,
                ha="left", va="center")
        # 大地との電位差
        ax.annotate("", xy=(3.55, 0.0), xytext=(3.55, 0.55),
                    arrowprops=dict(arrowstyle="<->", lw=1.0, color=RED))
        ax.plot([3.35, 3.75], [0.0, 0.0], lw=1.0, color="k")
        ax.text(2.05, -0.25, "大地との間に\n電位差が残る", ha="center", va="top",
                fontsize=6.8, fontproperties=JP, color=RED)
        ax.text(2.0, -1.15, "(a) 非絶縁型", ha="center", fontsize=7.4,
                fontproperties=JP, color="#555")
    else:
        # トランスで切り離す
        ax.plot([0.7, 1.25], [2.1, 2.1], lw=1.1, color="k")
        ax.plot([0.7, 1.25], [0.6, 0.6], lw=1.1, color="k")
        coil_v(ax, 1.2, 0.6, 2.1, side=1)
        ax.plot([1.47, 1.47], [0.5, 2.2], lw=1.1, color="k")
        ax.plot([1.55, 1.55], [0.5, 2.2], lw=1.1, color="k")
        coil_v(ax, 1.82, 0.6, 2.1, side=-1)
        ax.plot([1.82, 2.3], [2.1, 2.1], lw=1.1, color="k")
        ax.plot([1.82, 2.3], [0.6, 0.6], lw=1.1, color="k")
        ax.plot([2.3, 3.1], [2.1, 2.1], lw=1.1, color="k")
        ax.plot([2.3, 3.1], [0.6, 0.6], lw=1.1, color="k")
        ax.plot(3.1, 2.1, "o", ms=3.2, mfc="w", mec="k", mew=1.0)
        ax.plot(3.1, 0.6, "o", ms=3.2, mfc="w", mec="k", mew=1.0)
        ax.text(3.3, 1.35, "出力", fontsize=7.2, fontproperties=JP,
                ha="left", va="center")
        ground(ax, 2.6, 0.6)
        ax.text(2.6, -0.25, "2次側で新しい\n基準電位を選べる", ha="center", va="top",
                fontsize=6.8, fontproperties=JP, color=BLUE)
        ax.text(1.5, 2.45, "トランス", ha="center", fontsize=6.8,
                fontproperties=JP, color=BLUE)
        ax.text(2.0, -1.15, "(b) 絶縁型", ha="center", fontsize=7.4,
                fontproperties=JP, color="#555")
    ax.set_xlim(-0.5, 4.1)
    ax.set_ylim(-1.45, 3.15)
    ax.set_aspect("equal")
    ax.axis("off")

fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig6.1.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
PNG = "/tmp/claude-1000/-home-soumajinno/e7688596-6b6f-45e4-950d-929e196c5bb6/scratchpad/fig6.1.png"
fig.savefig(PNG, format="png", dpi=160, bbox_inches="tight")
print("wrote", EPS)
