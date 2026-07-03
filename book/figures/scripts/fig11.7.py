#!/usr/bin/env python3
# fig11.7（第11章）: EMCフィルタの代表的な構成。
# Xコンデンサ（線間・DM対策），コモンモードチョーク，Yコンデンサ（対地・CM対策）。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BK = "#222222"
BLUE = "#2a5db0"
RED = "#c0392b"


def wire(ax, pts, c=BK, lw=1.0):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=c, lw=lw,
            solid_capstyle="round", zorder=1)


def dot(ax, x, y):
    ax.plot([x], [y], "o", ms=2.2, color=BK, zorder=3)


def coil_h(ax, xa, xb, y, c=BK, n=4, flip=False):
    dx = (xb - xa) / n
    r = dx / 2
    t = np.linspace(0, np.pi, 30)
    s = -0.9 if flip else 0.9
    for k in range(n):
        xc = xa + dx * (k + 0.5)
        ax.plot(xc - r * np.cos(t), y + s * r * np.sin(t), color=c, lw=1.0)


def cap_v(ax, x, y1, y2, c=BK, yc=None):
    if yc is None:
        yc = 0.5 * (y1 + y2)
    g, w = 0.10, 0.28
    wire(ax, [(x, y1), (x, yc + g)], c)
    wire(ax, [(x, yc - g), (x, y2)], c)
    ax.plot([x - w, x + w], [yc + g, yc + g], color=c, lw=1.2, zorder=2)
    ax.plot([x - w, x + w], [yc - g, yc - g], color=c, lw=1.2, zorder=2)


def earth(ax, x, y, c=BK):
    wire(ax, [(x - 0.28, y), (x + 0.28, y)], c, lw=1.2)
    wire(ax, [(x - 0.18, y - 0.12), (x + 0.18, y - 0.12)], c, lw=1.0)
    wire(ax, [(x - 0.08, y - 0.24), (x + 0.08, y - 0.24)], c, lw=0.8)


fig, ax = plt.subplots(figsize=(4.25, 2.1))

yT, yB = 2.6, 0.9
xL, xR = 0.5, 9.5
xX = 2.0                 # Xコンデンサ
xC0, xC1 = 3.6, 5.0      # CMチョーク
xY = 6.8                 # Yコンデンサ
yG = -0.35               # 大地レール

# 幹線
wire(ax, [(xL, yT), (xC0, yT)])
wire(ax, [(xC1, yT), (xR, yT)])
wire(ax, [(xL, yB), (xC0, yB)])
wire(ax, [(xC1, yB), (xR, yB)])
coil_h(ax, xC0, xC1, yT)
coil_h(ax, xC0, xC1, yB, flip=True)
# 磁心（共通コア）
for dx in (-0.10, 0.10):
    wire(ax, [(0.5 * (xC0 + xC1) + dx, yB + 0.42), (0.5 * (xC0 + xC1) + dx, yT - 0.42)],
         c="#888", lw=1.1)
# 極性ドット
ax.plot([xC0 + 0.12], [yT + 0.30], "o", ms=2.0, color=BK)
ax.plot([xC0 + 0.12], [yB - 0.30], "o", ms=2.0, color=BK)

# Xコンデンサ（線間）
cap_v(ax, xX, yT, yB)
dot(ax, xX, yT)
dot(ax, xX, yB)

# Yコンデンサ（各線-大地）。上の線からのキャパシタは下の線と交差する
# （交点に黒丸なし = 接続なし）
xY1, xY2 = xY, xY + 0.9
cap_v(ax, xY1, yT, yG, yc=1.75)
cap_v(ax, xY2, yB, yG, yc=0.30)
dot(ax, xY1, yT)
dot(ax, xY2, yB)
wire(ax, [(xY1, yG), (xY2, yG)])
earth(ax, 0.5 * (xY1 + xY2), yG)

# ラベル
ax.text(xL - 0.15, 0.5 * (yT + yB), "電源側", ha="right", va="center",
        fontsize=7, fontproperties=JP)
ax.text(xR + 0.15, 0.5 * (yT + yB), "変換器側\n（ノイズ源）", ha="left", va="center",
        fontsize=7, fontproperties=JP)
ax.text(xX, yB - 0.55, "Xコンデンサ\n（DM対策）", ha="center", va="top",
        fontsize=6.4, fontproperties=JP, color=BLUE)
ax.text(0.5 * (xC0 + xC1), yT + 0.75, "コモンモードチョーク", ha="center",
        fontsize=6.4, fontproperties=JP, color=BLUE)
ax.text(xY + 0.45, yT + 0.42, "Yコンデンサ（CM対策）", ha="center",
        va="bottom", fontsize=6.4, fontproperties=JP, color=BLUE)
ax.text(xY - 0.55, yG - 0.15, "大地へ", ha="right", va="center",
        fontsize=6.2, fontproperties=JP, color="#777")

ax.set_xlim(-1.0, 11.6)
ax.set_ylim(-1.0, 3.6)
ax.set_aspect("equal")
ax.axis("off")

fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig11.7.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
