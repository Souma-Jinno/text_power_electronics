#!/usr/bin/env python3
# fig1.2（第1章）: 真性・n型・p型半導体のバンド図とキャリア。
# ドーピングでフェルミ準位の位置と多数キャリアが変わることを示す。
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BLUE = "#2a5db0"
RED = "#c0392b"
GRAY = "#777777"

fig, axes = plt.subplots(1, 3, figsize=(4.4, 2.1))

EC, EV = 2.0, 0.0   # バンド端

def frame(ax, title):
    ax.plot([0, 3], [EC, EC], color="#333", lw=1.2)
    ax.plot([0, 3], [EV, EV], color="#333", lw=1.2)
    ax.text(3.05, EC, r"$E_c$", fontsize=8, va="center")
    ax.text(3.05, EV, r"$E_v$", fontsize=8, va="center")
    ax.set_title(title, fontsize=8.4, fontproperties=JP, pad=3)
    ax.set_xlim(-0.95, 4.1)
    ax.set_ylim(-1.15, 2.9)
    ax.axis("off")

def electrons(ax, xs, y):
    for x in xs:
        ax.plot(x, y, "o", ms=3.4, color=BLUE)

def holes(ax, xs, y):
    for x in xs:
        ax.plot(x, y, "o", ms=3.8, mfc="white", mec=RED, mew=1.0)

# --- (a) 真性半導体
ax = axes[0]
frame(ax, "(a) 真性")
ax.plot([0, 3], [1.0, 1.0], ls="--", color=GRAY, lw=1.0)
ax.text(3.05, 1.0, r"$E_F$", fontsize=8, va="center", color=GRAY)
electrons(ax, [1.0], 2.15)
holes(ax, [2.0], -0.15)
ax.text(1.5, -1.0, "電子と正孔が\n同数（少ない）", ha="center", fontsize=7.2,
        fontproperties=JP, color="#555")

# --- (b) n形
ax = axes[1]
frame(ax, "(b) n形")
ax.plot([0, 3], [1.42, 1.42], ls="--", color=GRAY, lw=1.0)
ax.text(3.05, 1.42, r"$E_F$", fontsize=8, va="center", color=GRAY)
ax.plot([0.4, 2.6], [1.8, 1.8], ls=(0, (2, 2)), color=RED, lw=1.0)
ax.text(-0.05, 1.8, r"$E_d$", fontsize=7.6, va="center", color=RED, ha="right")
for x in (0.8, 1.5, 2.2):
    ax.text(x, 1.8, "+", ha="center", va="center", fontsize=7, color=RED)
electrons(ax, [0.6, 1.2, 1.8, 2.4], 2.15)
holes(ax, [1.5], -0.15)
ax.text(1.5, -1.0, "多数キャリア：電子\n（ドナーが供給）", ha="center", fontsize=7.2,
        fontproperties=JP, color="#555")

# --- (c) p形
ax = axes[2]
frame(ax, "(c) p形")
ax.plot([0, 3], [0.58, 0.58], ls="--", color=GRAY, lw=1.0)
ax.text(3.05, 0.58, r"$E_F$", fontsize=8, va="center", color=GRAY)
ax.plot([0.4, 2.6], [0.2, 0.2], ls=(0, (2, 2)), color=BLUE, lw=1.0)
ax.text(-0.05, 0.2, r"$E_a$", fontsize=7.6, va="center", color=BLUE, ha="right")
for x in (0.8, 1.5, 2.2):
    ax.text(x, 0.2, "−", ha="center", va="center", fontsize=7, color=BLUE)
holes(ax, [0.6, 1.2, 1.8, 2.4], -0.15)
electrons(ax, [1.5], 2.15)
ax.text(1.5, -1.0, "多数キャリア：正孔\n（アクセプタが供給）", ha="center", fontsize=7.2,
        fontproperties=JP, color="#555")

fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig1.2.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
