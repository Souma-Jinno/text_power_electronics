#!/usr/bin/env python3
# fig5.7（第5章）: インダクタ電流の連続モード（CCM）・境界・不連続モード（DCM）。
# 負荷電流が ΔI_L/2 を下回ると電流がゼロに張り付く期間が現れる。
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
SHADE = "#eef3fb"

D = 0.42
T = 1.0
NP = 2
TMAX = NP * T
AMP = 0.5

t = np.linspace(0, TMAX, 2001)


def tri_wave(t, mean, amp):
    tt = np.mod(t, T)
    y = np.where(tt < D * T,
                 -amp / 2 + amp * tt / (D * T),
                 amp / 2 - amp * (tt - D * T) / ((1 - D) * T))
    return mean + y


def setup(ax, ymax):
    for k in range(NP):
        ax.add_patch(Rectangle((k * T, 0), D * T, ymax,
                               fc=SHADE, ec="none", zorder=0))
    ax.annotate("", xy=(1.16 * TMAX, 0), xytext=(-0.05 * TMAX, 0),
                arrowprops=dict(arrowstyle="-|>", lw=0.8, color=BK,
                                mutation_scale=8))
    ax.plot([0, 0], [0, ymax], color=BK, lw=0.8)
    for x, s in [(D * T, "$DT$"), (T, "$T$")]:
        ax.plot([x, x], [-0.02 * ymax, 0.02 * ymax], color=BK, lw=0.8)
        ax.text(x, -0.07 * ymax, s, ha="center", va="top", fontsize=6.4)
    ax.set_xlim(-0.34 * TMAX, 1.26 * TMAX)
    ax.set_ylim(-0.62 * ymax, 1.16 * ymax)
    ax.axis("off")


fig, axes = plt.subplots(1, 3, figsize=(4.25, 1.55))
YM = 1.35

# --- (a) CCM
ax = axes[0]
setup(ax, YM)
mean = 0.75
ax.plot(t, tri_wave(t, mean, AMP), color=BLUE, lw=1.2, zorder=3)
ax.plot([0, TMAX], [mean] * 2, color=RED, lw=0.8, ls="--", zorder=2)
ax.text(-0.08 * TMAX, mean, r"$I_{\mathrm{out}}$", ha="right", va="center",
        fontsize=6.6, color=RED)
ax.text(-0.08 * TMAX, YM, "$i_L$", ha="right", va="center", fontsize=7.2,
        color=BLUE)
ax.text(TMAX / 2, -0.5 * YM, "(a) 連続（CCM）", ha="center", fontsize=6.6,
        fontproperties=JP, color="#555")

# --- (b) 境界
ax = axes[1]
setup(ax, YM)
mean = AMP / 2
ax.plot(t, tri_wave(t, mean, AMP), color=BLUE, lw=1.2, zorder=3)
ax.plot([0, TMAX], [mean] * 2, color=RED, lw=0.8, ls="--", zorder=2)
ax.text(-0.08 * TMAX, mean, r"$\frac{\Delta I_L}{2}$", ha="right",
        va="center", fontsize=7.0, color=RED)
ax.text(TMAX / 2, -0.5 * YM, "(b) 境界", ha="center", fontsize=6.6,
        fontproperties=JP, color="#555")

# --- (c) DCM
ax = axes[2]
setup(ax, YM)
peak = 0.75
t2 = 0.35  # 電流が減少する期間の長さ
tt = np.mod(t, T)
iL = np.where(tt < D * T, peak * tt / (D * T),
              np.where(tt < D * T + t2,
                       peak * (1 - (tt - D * T) / t2), 0.0))
ax.plot(t, iL, color=BLUE, lw=1.2, zorder=3)
ax.annotate("", xy=(T, 0.52 * YM), xytext=(D * T + t2, 0.52 * YM),
            arrowprops=dict(arrowstyle="<->", lw=0.7, color=BK,
                            mutation_scale=6))
ax.text(0.5 * (D * T + t2 + T), 0.58 * YM, "$i_L=0$", ha="center",
        va="bottom", fontsize=6.4)
ax.plot([D * T + t2] * 2, [0, 0.52 * YM], color="#999", lw=0.5, ls=":")
ax.plot([T] * 2, [0, 0.52 * YM], color="#999", lw=0.5, ls=":")
ax.text(TMAX / 2, -0.5 * YM, "(c) 不連続（DCM）", ha="center", fontsize=6.6,
        fontproperties=JP, color="#555")

fig.subplots_adjust(wspace=0.28)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig5.7.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
