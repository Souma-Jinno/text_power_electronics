#!/usr/bin/env python3
# fig6.6（第6章）: エネルギーの流れの対比。フォワード＝オン期間に素通しで渡す
# （励磁分はリセットで返却），フライバック＝オンで溜めてオフで渡す。
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

fig, ax = plt.subplots(figsize=(4.3, 3.0))

def box(x, y, label, w=0.95, h=0.5, fc="#eef3fb", ec=BLUE):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                                fc=fc, ec=ec, lw=1.0))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=7.0, fontproperties=JP)

def arrow(p, q, color=BLUE, lw=1.6, rad=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=11,
                                 lw=lw, color=color, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}"))

# 列見出し
ax.text(1.75, 4.6, "オン期間", ha="center", fontsize=7.6, fontproperties=JP)
ax.text(5.05, 4.6, "オフ期間", ha="center", fontsize=7.6, fontproperties=JP)

# ---- フォワード（上段）----
ax.text(-0.15, 3.9, "フォワード", ha="left", fontsize=7.6,
        fontproperties=JP, color="k")
y1 = 2.9
box(0.0, y1, "電源")
box(1.3, y1, "トランス")
box(2.6, y1, "$L$・負荷", w=1.05)
arrow((1.0, y1 + 0.25), (1.32, y1 + 0.25))
arrow((2.3, y1 + 0.25), (2.62, y1 + 0.25))
ax.text(1.8, y1 - 0.32, "素通しで渡す", ha="center", fontsize=6.6,
        fontproperties=JP, color=BLUE)
ax.text(1.78, y1 + 0.98, "励磁分だけ残る", ha="center", fontsize=6.2,
        fontproperties=JP, color=RED)
arrow((1.55, y1 + 0.9), (1.72, y1 + 0.58), color=RED, lw=1.0)

box(3.9, y1, "電源")
box(5.2, y1, "トランス")
box(6.5, y1, "$L$・負荷", w=1.05)
arrow((5.2, y1 + 0.42), (4.88, y1 + 0.42), color=RED, lw=1.2, rad=0.35)
ax.text(5.05, y1 - 0.32, "リセットで返却", ha="center", fontsize=6.6,
        fontproperties=JP, color=RED)
ax.text(7.02, y1 + 0.85, "$L$の蓄えで\n負荷へ", ha="center", fontsize=6.2,
        fontproperties=JP, color=BLUE)

# ---- フライバック（下段）----
ax.text(-0.15, 1.55, "フライバック", ha="left", fontsize=7.6,
        fontproperties=JP, color="k")
y2 = 0.55
box(0.0, y2, "電源")
box(1.3, y2, "トランス", fc="#fdecea", ec=RED)
box(2.6, y2, "負荷", w=1.05)
arrow((1.0, y2 + 0.25), (1.32, y2 + 0.25))
ax.text(1.78, y2 - 0.32, "溜める", ha="center", fontsize=6.6,
        fontproperties=JP, color=RED)
ax.text(3.12, y2 + 0.85, "渡らない\n（$C$が支える）", ha="center", fontsize=6.2,
        fontproperties=JP, color="#777")

box(3.9, y2, "電源")
box(5.2, y2, "トランス", fc="#fdecea", ec=RED)
box(6.5, y2, "負荷", w=1.05)
arrow((6.2, y2 + 0.25), (6.52, y2 + 0.25), color=RED)
ax.text(5.85, y2 - 0.32, "蓄えを渡す", ha="center", fontsize=6.6,
        fontproperties=JP, color=RED)

# 仕切り
ax.plot([3.7, 3.7], [0.0, 4.4], lw=0.6, color="#bbb", ls=(0, (4, 3)))
ax.plot([-0.2, 7.75], [2.25, 2.25], lw=0.6, color="#bbb", ls=(0, (4, 3)))

ax.set_xlim(-0.3, 7.85)
ax.set_ylim(-0.35, 4.9)
ax.axis("off")

fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig6.6.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
PNG = "/tmp/claude-1000/-home-soumajinno/e7688596-6b6f-45e4-950d-929e196c5bb6/scratchpad/fig6.6.png"
fig.savefig(PNG, format="png", dpi=160, bbox_inches="tight")
print("wrote", EPS)
