#!/usr/bin/env python3
# fig10.1（第10章）: 間接式周波数変換（AC-DC-AC変換）のブロック図。
# 8章の整流回路と9章のインバータを直列につなぎ，間をDCリンクで結ぶ。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrow
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BK = "#222222"
BLUE = "#2a5db0"
GREEN = "#2e7d4f"
RED = "#c0392b"
GY = "#888888"

fig, ax = plt.subplots(figsize=(4.25, 2.05))
ax.set_xlim(0, 10.6)
ax.set_ylim(0, 4.4)
ax.axis("off")
ax.set_aspect("equal")

Y = 1.05          # 主配線の高さ
BW, BH = 1.9, 1.3  # ブロックの幅・高さ


def wire(pts, c=BK, lw=1.0, ls="-"):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=c, lw=lw,
            ls=ls, solid_capstyle="round", zorder=1)


def arrow(x1, x2, y, c=BK):
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="-|>", lw=1.0, color=c,
                                mutation_scale=9))


def block(xc, label, sub, ec):
    ax.add_patch(Rectangle((xc - BW / 2, Y - BH / 2), BW, BH,
                           fc="white", ec=ec, lw=1.2, zorder=2))
    ax.text(xc, Y + 0.22, label, ha="center", va="center", fontsize=7.2,
            fontproperties=JP, color=BK)
    ax.text(xc, Y - 0.30, sub, ha="center", va="center", fontsize=6.4,
            fontproperties=JP, color=ec)


# --- 交流電源（左端）
xs = 0.75
ax.add_patch(Circle((xs, Y), 0.34, fc="white", ec=BK, lw=1.0, zorder=2))
th = np.linspace(0, 2 * np.pi, 100)
ax.plot(xs - 0.20 + 0.40 * th / (2 * np.pi), Y + 0.13 * np.sin(2 * th),
        color=BK, lw=0.8, zorder=3)
ax.text(xs, Y - 0.62, "交流電源", ha="center", va="top", fontsize=6.4,
        fontproperties=JP)

# --- 3つのブロック
x1, x2, x3 = 2.75, 5.35, 7.95
block(x1, "整流回路", "（8章）", BLUE)
block(x2, "DCリンク", "コンデンサ", RED)
block(x3, "インバータ", "（9章）", GREEN)

# --- 負荷（右端）
xl = 9.9
ax.add_patch(Rectangle((xl - 0.22, Y - 0.5), 0.44, 1.0, fc="white",
                       ec=BK, lw=1.0, zorder=2))
ax.text(xl, Y - 0.62, "負荷", ha="center", va="top", fontsize=6.4,
        fontproperties=JP)

# --- 配線と矢印
arrow(xs + 0.36, x1 - BW / 2 - 0.04, Y)
arrow(x1 + BW / 2, x2 - BW / 2 - 0.04, Y)
arrow(x2 + BW / 2, x3 - BW / 2 - 0.04, Y)
arrow(x3 + BW / 2, xl - 0.26, Y)

# --- 各段の波形（上段のミニ波形）
YW = 3.15   # 波形の基準線の高さ
WW = 1.7    # 波形の幅
AMP = 0.52


def mini_axis(xc):
    wire([(xc - WW / 2, YW), (xc + WW / 2, YW)], c=GY, lw=0.6)


def w_sine(xc, freq, c, amp=AMP):
    t = np.linspace(0, 1, 300)
    ax.plot(xc - WW / 2 + WW * t, YW + amp * np.sin(2 * np.pi * freq * t),
            color=c, lw=1.1, zorder=3)


# 入力: 50/60Hzの正弦波
mini_axis(x1 - 1.35)
w_sine(x1 - 1.35, 2, BK)
ax.text(x1 - 1.35, YW + 0.78, "交流", ha="center", fontsize=6.2,
        fontproperties=JP)

# DCリンク: 小さなリプルを残した直流
mini_axis(x2 - 1.30)
t = np.linspace(0, 1, 300)
ax.plot(x2 - 1.30 - WW / 2 + WW * t,
        YW + 0.42 + 0.055 * np.abs(np.sin(2 * np.pi * 4 * t)) - 0.028,
        color=RED, lw=1.1, zorder=3)
ax.text(x2 - 1.30, YW + 0.78, "直流", ha="center", fontsize=6.2,
        fontproperties=JP)

# 出力: 周波数の異なる交流
mini_axis(x3 - 1.30)
w_sine(x3 - 1.30, 5, GREEN)
ax.text(x3 - 1.30, YW + 0.78, "周波数の違う交流", ha="center", fontsize=6.2,
        fontproperties=JP)

mini_axis(xl - 0.9)
w_sine(xl - 0.9, 5, GREEN)

# 波形と回路の対応（点線）
for xw, xb in [(x1 - 1.35, x1 - BW / 2 - 0.35), (x2 - 1.30, x2 - BW / 2 - 0.35),
               (x3 - 1.30, x3 - BW / 2 - 0.35), (xl - 0.9, xl - 0.9)]:
    wire([(xw, YW - 0.62), (xb, Y + 0.85)], c=GY, lw=0.5, ls=":")

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig10.1.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
