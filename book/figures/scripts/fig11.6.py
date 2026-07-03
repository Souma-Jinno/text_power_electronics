#!/usr/bin/env python3
# fig11.6（第11章）: ディファレンシャルモードとコモンモードの電流経路の対比。
# (a) DM: 往復2線を逆向きに流れ，回路のループを回る
# (b) CM: 2線を同じ向きに流れ，対地寄生容量 C_p と大地を通って戻る
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
GY = "#e6e6e6"


def wire(ax, pts, c=BK, lw=1.0):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=c, lw=lw,
            solid_capstyle="round", zorder=1)


def arrow(ax, x, y, dx, dy, c=RED, lw=1.1):
    ax.annotate("", xy=(x + dx, y + dy), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", lw=lw, color=c,
                                mutation_scale=8), zorder=5)


def box(ax, x, y, w, h, label, fs=7):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=BK, lw=1.0, zorder=2))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=fs, fontproperties=JP, zorder=3)


def ground_bar(ax, x0, x1, y):
    ax.add_patch(Rectangle((x0, y - 0.28), x1 - x0, 0.28,
                           fc=GY, ec="#999", lw=0.6, zorder=0))
    for xx in np.arange(x0 + 0.15, x1, 0.45):
        ax.plot([xx, xx - 0.2], [y - 0.02, y - 0.26], color="#999", lw=0.5, zorder=1)


def cap_v(ax, x, y1, y2, c=BK):
    yc = 0.5 * (y1 + y2)
    g, w = 0.09, 0.26
    wire(ax, [(x, y1), (x, yc + g)], c)
    wire(ax, [(x, yc - g), (x, y2)], c)
    ax.plot([x - w, x + w], [yc + g, yc + g], color=c, lw=1.2, zorder=2)
    ax.plot([x - w, x + w], [yc - g, yc - g], color=c, lw=1.2, zorder=2)


def panel(ax, mode):
    yT, yB, yG = 2.55, 1.45, 0.0
    xs0, xs1 = 0.4, 2.0     # 電源箱
    xc0, xc1 = 6.6, 8.6     # 変換器箱
    box(ax, xs0, yB - 0.35, xs1 - xs0, yT - yB + 0.7, "電源", fs=6.8)
    box(ax, xc0, yB - 0.35, xc1 - xc0, yT - yB + 0.7, "電力\n変換器", fs=6.4)
    wire(ax, [(xs1, yT), (xc0, yT)])
    wire(ax, [(xs1, yB), (xc0, yB)])
    ground_bar(ax, 0.0, 9.4, yG)
    ax.text(0.18, yG - 0.14, "大地（グラウンド）", ha="left", va="center",
            fontsize=6.0, fontproperties=JP, color="#555",
            bbox=dict(fc="white", ec="none", pad=0.6), zorder=2)
    if mode == "dm":
        for xx in (3.3, 5.3):
            arrow(ax, xx, yT, 0.7, 0, RED)
            arrow(ax, xx + 0.7, yB, -0.7, 0, RED)
        ax.text(4.35, yT + 0.28, r"$i_{\mathrm{DM}}$", ha="center",
                fontsize=7.5, color=RED)
        ax.text(4.35, yB - 0.40, r"$i_{\mathrm{DM}}$", ha="center",
                fontsize=7.5, color=RED)
    else:
        for xx in (3.3, 5.3):
            arrow(ax, xx, yT, 0.7, 0, RED)
            arrow(ax, xx, yB, 0.7, 0, RED)
        ax.text(4.35, yT + 0.28, r"$i_{\mathrm{CM}}/2$", ha="center",
                fontsize=7.5, color=RED)
        ax.text(4.35, yB - 0.40, r"$i_{\mathrm{CM}}/2$", ha="center",
                fontsize=7.5, color=RED)
        # 対地寄生容量
        xp = 0.5 * (xc0 + xc1)
        cap_v(ax, xp, yB - 0.35, yG + 0.02)
        ax.text(xp + 0.35, 0.55, r"$C_p$", ha="left", fontsize=7.5)
        arrow(ax, xp + 0.02, 0.75, 0, -0.4, RED, lw=1.0)
        # 大地を戻る
        arrow(ax, 4.8, yG + 0.14, -1.2, 0, RED)
        ax.text(4.2, yG + 0.35, r"$i_{\mathrm{CM}}$", ha="center",
                fontsize=7.5, color=RED)
        # 電源の接地
        xg = 0.5 * (xs0 + xs1)
        wire(ax, [(xg, yB - 0.35), (xg, yG + 0.02)])
        arrow(ax, xg + 0.02, yG + 0.35, 0, 0.35, RED, lw=1.0)
    ax.set_xlim(-0.3, 9.7)
    ax.set_ylim(-0.85, 3.45)
    ax.set_aspect("equal")
    ax.axis("off")


fig, axes = plt.subplots(2, 1, figsize=(4.25, 2.6))
panel(axes[0], "dm")
axes[0].text(4.7, -0.8, "(a) ディファレンシャルモード（往復逆向き）",
             ha="center", fontsize=6.8, fontproperties=JP, color="#555")
panel(axes[1], "cm")
axes[1].text(4.7, -0.8, "(b) コモンモード（同じ向き，大地経由で戻る）",
             ha="center", fontsize=6.8, fontproperties=JP, color="#555")

fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig11.6.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
