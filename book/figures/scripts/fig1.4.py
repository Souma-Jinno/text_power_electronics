#!/usr/bin/env python3
# fig1.4（第1章）: pn接合と空乏層。構造（固定電荷）→電荷密度→電場→バンドの曲がり
# を1本の軸でつなぎ，「電荷→電場→電位→バンド」の因果を読む図。
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

XP, XN = -0.9, 0.9        # 空乏層の端
L = 3.0                    # 図の半幅

fig, axes = plt.subplots(4, 1, figsize=(4.4, 3.55),
                         gridspec_kw=dict(height_ratios=[1.5, 0.85, 0.85, 1.6]))

def setup(ax, ylo, yhi):
    ax.set_xlim(-L - 0.9, L + 0.9)
    ax.set_ylim(ylo, yhi)
    ax.axis("off")
    ax.axvline(XP, color="#999", lw=0.7, ls=":")
    ax.axvline(XN, color="#999", lw=0.7, ls=":")

# --- (a) 構造
ax = axes[0]
setup(ax, -1.5, 1.9)
ax.add_patch(Rectangle((-L, -1.0), L + XP, 2.0, fc="#fdeceb", ec="#888", lw=0.8))
ax.add_patch(Rectangle((XP, -1.0), XN - XP, 2.0, fc="#f5f5f5", ec="#888", lw=0.8))
ax.add_patch(Rectangle((XN, -1.0), L - XN, 2.0, fc="#eaf0fa", ec="#888", lw=0.8))
ax.text(-L + 0.15, 1.25, "p形", fontsize=8.2, fontproperties=JP)
ax.text(L - 0.55, 1.25, "n形", fontsize=8.2, fontproperties=JP)
ax.text(0, 1.25, "空乏層", ha="center", fontsize=7.6, fontproperties=JP, color="#555")
rng = np.random.default_rng(5)
for i in range(9):   # p側の正孔
    xi = rng.uniform(-L + 0.15, XP - 0.25)
    yi = rng.uniform(-0.75, 0.75)
    ax.plot(xi, yi, "o", ms=3.6, mfc="white", mec=RED, mew=0.9)
for i in range(9):   # n側の電子
    xi = rng.uniform(XN + 0.25, L - 0.15)
    yi = rng.uniform(-0.75, 0.75)
    ax.plot(xi, yi, "o", ms=3.2, color=BLUE)
from matplotlib.patches import Circle
for xi in (-0.62, -0.28):   # アクセプタイオン（−）
    for yi in (0.42, -0.42):
        ax.add_patch(Circle((xi, yi), 0.11, fc="white", ec=RED, lw=0.9))
        ax.plot([xi - 0.055, xi + 0.055], [yi, yi], color=RED, lw=0.9)
for xi in (0.28, 0.62):     # ドナーイオン（＋）
    for yi in (0.42, -0.42):
        ax.add_patch(Circle((xi, yi), 0.11, fc="white", ec=BLUE, lw=0.9))
        ax.plot([xi - 0.055, xi + 0.055], [yi, yi], color=BLUE, lw=0.9)
        ax.plot([xi, xi], [yi - 0.055, yi + 0.055], color=BLUE, lw=0.9)
ax.text(-0.45, -0.85, "固定イオン", ha="center", fontsize=6.8,
        fontproperties=JP, color="#555")
ax.text(-L - 0.15, 0, "(a)", ha="right", va="center", fontsize=8)

# --- (b) 電荷密度 ρ(x)
ax = axes[1]
setup(ax, -1.3, 1.55)
ax.plot([-L, L], [0, 0], color="#777", lw=0.7)
ax.add_patch(Rectangle((XP, -1.0), -XP, 1.0, fc="#f6c9c4", ec=RED, lw=0.9))
ax.add_patch(Rectangle((0, 0), XN, 1.0, fc="#c9d8f0", ec=BLUE, lw=0.9))
ax.text(0.45, 0.42, r"$+eN_d$", fontsize=7.6, color=BLUE, ha="center")
ax.text(-0.45, -0.62, r"$-eN_a$", fontsize=7.6, color=RED, ha="center")
ax.text(-L - 0.15, 0.1, "(b)", ha="right", va="center", fontsize=8)
ax.text(L + 0.15, 0.35, r"$\rho(x)$", fontsize=8, va="center")

# --- (c) 電場 𝓔(x)
ax = axes[2]
setup(ax, -1.5, 0.7)
ax.plot([-L, L], [0, 0], color="#777", lw=0.7)
ax.plot([-L, XP, 0, XN, L], [0, 0, -1.15, 0, 0], color=RED, lw=1.3)
ax.annotate("", xy=(-0.55, -0.35), xytext=(0.55, -0.35),
            arrowprops=dict(arrowstyle="-|>", lw=1.1, color=RED))
ax.text(1.35, -1.15, "電場はn形→p形の向き", fontsize=7.2, fontproperties=JP,
        color=RED, ha="left", va="center")
ax.text(-L - 0.15, -0.3, "(c)", ha="right", va="center", fontsize=8)
ax.text(L + 0.15, -0.2, r"$\mathcal{E}(x)$", fontsize=8, va="center")

# --- (d) バンド図
ax = axes[3]
setup(ax, -0.9, 2.75)
xx = np.linspace(-L, L, 300)
def bend(x):
    # 空乏層内でなめらかに下がる形（p側が高くn側が低い）
    y = np.where(x < XP, 1.0, np.where(x > XN, 0.0,
                 0.5 * (1 + np.cos(np.pi * (x - XP) / (XN - XP)))))
    return y
ec = 1.1 + 1.05 * bend(xx)
ev = ec - 1.35
ax.plot(xx, ec, color="#333", lw=1.2)
ax.plot(xx, ev, color="#333", lw=1.2)
ax.plot([-L, L], [0.95, 0.95], ls="--", color="#777", lw=1.0)
ax.text(L + 0.15, 0.93, r"$E_F$", fontsize=8, va="top", color="#555")
ax.text(L + 0.15, 1.12, r"$E_c$", fontsize=8, va="bottom")
ax.text(L + 0.15, -0.25, r"$E_v$", fontsize=8, va="center")
ax.plot([-2.7, XP], [1.1, 1.1], ls=":", color=RED, lw=0.8)
ax.annotate("", xy=(-2.4, 2.15), xytext=(-2.4, 1.1),
            arrowprops=dict(arrowstyle="<->", lw=0.9, color=RED))
ax.text(-2.25, 1.68, r"$eV_{bi}$", fontsize=8, color=RED, va="center")
ax.text(0, -0.75, "電位の差がバンドの曲がりになる", ha="center", fontsize=7.4,
        fontproperties=JP, color="#555")
ax.text(-L - 0.15, 1.0, "(d)", ha="right", va="center", fontsize=8)

fig.tight_layout(h_pad=0.4)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig1.4.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
