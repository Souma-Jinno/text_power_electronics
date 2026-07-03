#!/usr/bin/env python3
# fig5.4（第5章）: 昇圧チョッパの定常状態波形（v_L, i_L, i_D）。
# オフ期間だけダイオードを通して出力へエネルギーが送られることを示す。
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

D = 0.58
T = 1.0
NP = 2
TMAX = NP * T


def tri_wave(t, mean, amp):
    tt = np.mod(t, T)
    y = np.where(tt < D * T,
                 -amp / 2 + amp * tt / (D * T),
                 amp / 2 - amp * (tt - D * T) / ((1 - D) * T))
    return mean + y


def setup(ax, ymin, ymax, label, label_c=BLUE):
    for k in range(NP):
        ax.add_patch(Rectangle((k * T, ymin), D * T, ymax - ymin,
                               fc=SHADE, ec="none", zorder=0))
    ax.annotate("", xy=(1.10 * TMAX, 0), xytext=(-0.04 * TMAX, 0),
                arrowprops=dict(arrowstyle="-|>", lw=0.8, color=BK,
                                mutation_scale=8))
    ax.plot([0, 0], [ymin, ymax], color=BK, lw=0.8)
    for x, s in [(D * T, "$DT$"), (T, "$T$"), (2 * T, "$2T$")]:
        ax.plot([x, x], [-0.02 * (ymax - ymin), 0.02 * (ymax - ymin)],
                color=BK, lw=0.8)
        ax.text(x, ymin - 0.10 * (ymax - ymin), s, ha="center",
                va="top", fontsize=6.6)
    ax.text(1.11 * TMAX, -0.05 * (ymax - ymin), "$t$", ha="left",
            va="top", fontsize=7)
    ax.text(-0.03 * TMAX, ymax + 0.18 * (ymax - ymin), label, ha="right",
            va="center", fontsize=7.6, color=label_c)
    ax.set_xlim(-0.34 * TMAX, 1.20 * TMAX)
    ax.set_ylim(ymin - 0.34 * (ymax - ymin), ymax + 0.12 * (ymax - ymin))
    ax.axis("off")


t = np.linspace(0, TMAX, 2001)
fig, axes = plt.subplots(3, 1, figsize=(4.25, 3.0))

# --- (1) v_L
ax = axes[0]
setup(ax, -1.0, 0.8, "$v_L$")
von, voff = 0.714, -1.0  # +Vin, Vin-Vout（Vin=5, Vout=12 を 7 で正規化）
v = np.where(np.mod(t, T) < D * T, von, voff)
ax.plot(t, v, color=BLUE, lw=1.3, zorder=3)
for k in range(NP):
    ax.plot([k * T + D * T] * 2, [voff, von], color=BLUE, lw=1.0, zorder=3)
    if k > 0:
        ax.plot([k * T] * 2, [voff, von], color=BLUE, lw=1.0, zorder=3)
ax.text(-0.07 * TMAX, von, r"$V_{\mathrm{in}}$",
        ha="right", va="center", fontsize=6.8)
ax.text(-0.07 * TMAX, voff, r"$V_{\mathrm{in}}-V_{\mathrm{out}}$",
        ha="right", va="center", fontsize=6.8)
ax.plot([-0.02, TMAX], [von] * 2, color="#999", lw=0.5, ls=":", zorder=1)
ax.plot([-0.02, TMAX], [voff] * 2, color="#999", lw=0.5, ls=":", zorder=1)
ax.text(D * T / 2, 1.0, "オン", ha="center", fontsize=6.4,
        fontproperties=JP, color="#555")
ax.text((1 + D) * T / 2, 1.0, "オフ", ha="center", fontsize=6.4,
        fontproperties=JP, color="#555")

# --- (2) i_L
ax = axes[1]
setup(ax, 0, 1.45, "$i_L$")
mean, amp = 1.0, 0.5
ax.plot(t, tri_wave(t, mean, amp), color=BLUE, lw=1.3, zorder=3)
ax.plot([0, TMAX], [mean] * 2, color=RED, lw=0.8, ls="--", zorder=2)
ax.text(-0.07 * TMAX, mean, r"$I_{\mathrm{in}}$", ha="right",
        va="center", fontsize=6.8, color=RED)
xd = 2.06 * T
ax.annotate("", xy=(xd, mean + amp / 2), xytext=(xd, mean - amp / 2),
            arrowprops=dict(arrowstyle="<->", lw=0.9, color=BK,
                            mutation_scale=7))
ax.text(xd + 0.05, mean, r"$\Delta I_L$", ha="left", va="center",
        fontsize=7.2)

# --- (3) i_D（オフ期間だけ i_L が流れる）
ax = axes[2]
setup(ax, 0, 1.45, r"$i_{\mathrm{D}}$")
iL = tri_wave(t, mean, amp)
iD = np.where(np.mod(t, T) < D * T, 0.0, iL)
ax.plot(t, iD, color=BLUE, lw=1.3, zorder=3)
for k in range(NP):
    ax.plot([k * T + D * T] * 2, [0, mean + amp / 2], color=BLUE, lw=1.0,
            zorder=3)
    ax.plot([(k + 1) * T] * 2, [0, mean - amp / 2], color=BLUE, lw=1.0,
            zorder=3)
iout = (1 - D) * mean
ax.plot([0, TMAX], [iout] * 2, color=RED, lw=0.8, ls="--", zorder=2)
ax.text(-0.07 * TMAX, iout, r"$I_{\mathrm{out}}$", ha="right",
        va="center", fontsize=6.8, color=RED)
ax.text(1.28, -0.52, "平均が負荷電流になる", ha="left", va="top",
        fontsize=6.4, fontproperties=JP, color="#555")

fig.subplots_adjust(hspace=0.55)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig5.4.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
