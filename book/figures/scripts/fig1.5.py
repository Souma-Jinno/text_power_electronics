#!/usr/bin/env python3
# fig1.5（第1章）: バイアスとpn接合の整流特性。
# 順バイアスで障壁が下がり電流が流れ，逆バイアスで障壁が上がり電流が止まる。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BLUE = "#2a5db0"
RED = "#c0392b"

fig, axes = plt.subplots(1, 3, figsize=(4.4, 1.95),
                         gridspec_kw=dict(width_ratios=[1, 1, 1.15]))

XP, XN0 = -0.5, 0.5

def band(ax, xn, xp, height, title, note):
    L = 1.8
    xx = np.linspace(-L, L, 300)
    def bend(x):
        return np.where(x < xp, 1.0, np.where(x > xn, 0.0,
                        0.5 * (1 + np.cos(np.pi * (x - xp) / (xn - xp)))))
    ec = 0.9 + height * bend(xx)
    ax.plot(xx, ec, color="#333", lw=1.1)
    ax.plot(xx, ec - 0.8, color="#333", lw=1.1)
    ax.annotate("", xy=(-L + 0.25, 0.9 + height), xytext=(-L + 0.25, 0.9),
                arrowprops=dict(arrowstyle="<->", lw=0.8, color=RED))
    ax.set_title(title, fontsize=7.8, fontproperties=JP, pad=2)
    ax.text(0, -0.75, note, ha="center", fontsize=6.9, fontproperties=JP,
            color="#555")
    ax.set_xlim(-L - 0.2, L + 0.2)
    ax.set_ylim(-1.0, 2.9)
    ax.axis("off")
    return ec

# --- (a) 順バイアス：障壁 e(Vbi−V) に下がる
ax = axes[0]
band(ax, 0.35, -0.35, 0.55, "(a) 順バイアス",
     "障壁が下がり\n電流が流れる")
ax.text(-1.75, 1.75, r"$e(V_{bi}-V)$", fontsize=7.2, color=RED)
ax.annotate("", xy=(-1.0, 1.52), xytext=(0.85, 1.02),
            arrowprops=dict(arrowstyle="-|>", lw=1.2, color=BLUE))
ax.plot(1.1, 0.97, "o", ms=3.0, color=BLUE)

# --- (b) 逆バイアス：障壁 e(Vbi+V) に上がる
ax = axes[1]
band(ax, 0.75, -0.75, 1.5, "(b) 逆バイアス",
     "障壁が上がり\n電流は流れない")
ax.text(-1.35, 2.6, r"$e(V_{bi}+V)$", fontsize=7.2, color=RED)
ax.annotate("", xy=(-0.55, 2.15), xytext=(0.75, 1.35),
            arrowprops=dict(arrowstyle="-|>", lw=1.0, color=BLUE, ls="--"))
ax.text(0.12, 1.72, "×", fontsize=9, color=RED, ha="center", va="center")

# --- (c) 電流-電圧特性（整流）
ax = axes[2]
v = np.linspace(-2.0, 0.85, 300)
i = np.expm1(v / 0.24)
i = np.clip(i, -1.2, 22)
ax.plot(v, i, color=BLUE, lw=1.4)
ax.axhline(0, color="#888", lw=0.7)
ax.axvline(0, color="#888", lw=0.7)
ax.text(0.95, 20.5, r"$I$", fontsize=8.5)
ax.text(1.05, -3.6, r"$V$", fontsize=8.5)
ax.text(-1.9, 5.5, "順方向だけ\n電流が流れる\n（整流）", fontsize=6.9,
        fontproperties=JP, color="#555")
ax.set_title("(c) 電流-電圧特性", fontsize=7.8, fontproperties=JP, pad=2)
ax.set_xlim(-2.2, 1.3)
ax.set_ylim(-6, 23)
ax.axis("off")

fig.tight_layout(w_pad=0.3)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig1.5.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
