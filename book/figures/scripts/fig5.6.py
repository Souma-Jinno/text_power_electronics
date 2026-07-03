#!/usr/bin/env python3
# fig5.6（第5章）: リプル電圧の発生。キャパシタ電流 i_C の正の面積が
# 電荷 ΔQ となり，出力電圧を ΔV だけ持ち上げる。
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
AMP = 0.6  # ΔI_L


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
    y0 = 0.0 if ymin <= 0 else ymin
    ax.annotate("", xy=(1.10 * TMAX, y0), xytext=(-0.04 * TMAX, y0),
                arrowprops=dict(arrowstyle="-|>", lw=0.8, color=BK,
                                mutation_scale=8))
    ax.plot([0, 0], [ymin, ymax], color=BK, lw=0.8)
    for x, s in [(D * T, "$DT$"), (T, "$T$"), (2 * T, "$2T$")]:
        ax.plot([x, x], [y0 - 0.02 * (ymax - ymin), y0 + 0.02 * (ymax - ymin)],
                color=BK, lw=0.8)
        ax.text(x, ymin - 0.10 * (ymax - ymin), s, ha="center",
                va="top", fontsize=6.6)
    ax.text(1.11 * TMAX, y0 - 0.05 * (ymax - ymin), "$t$", ha="left",
            va="top", fontsize=7)
    ax.text(-0.03 * TMAX, ymax + 0.18 * (ymax - ymin), label, ha="right",
            va="center", fontsize=7.6, color=label_c)
    ax.set_xlim(-0.30 * TMAX, 1.20 * TMAX)
    ax.set_ylim(ymin - 0.34 * (ymax - ymin), ymax + 0.14 * (ymax - ymin))
    ax.axis("off")


t = np.linspace(0, TMAX, 4001)
fig, axes = plt.subplots(2, 1, figsize=(4.25, 2.5))

# --- (1) i_C
ax = axes[0]
setup(ax, -0.45, 0.5, "$i_C$")
iC = tri_wave(t, 0, AMP)
ax.plot(t, iC, color=BLUE, lw=1.3, zorder=3)
# 正の半周期（DT/2 〜 (1+D)T/2）を塗る
t1, t2 = D * T / 2, (1 + D) * T / 2
mask = (t >= t1) & (t <= t2)
ax.fill_between(t[mask], 0, iC[mask], color="#c5d5ef", zorder=1)
ax.text(0.5 * (t1 + t2), 0.09, r"$\Delta Q$", ha="center", fontsize=7.4,
        color=BLUE)
ax.annotate("", xy=(t2, 0.42), xytext=(t1, 0.42),
            arrowprops=dict(arrowstyle="<->", lw=0.8, color=BK,
                            mutation_scale=7))
ax.text(0.5 * (t1 + t2), 0.47, "$T/2$", ha="center", va="bottom", fontsize=6.6)
ax.plot([t1, t1], [0, 0.42], color="#999", lw=0.5, ls=":")
ax.plot([t2, t2], [0, 0.42], color="#999", lw=0.5, ls=":")
ax.text(-0.06 * TMAX, AMP / 2 - 0.03, r"$\frac{\Delta I_L}{2}$", ha="right",
        va="center", fontsize=7.2)
ax.plot([-0.02, D * T], [AMP / 2] * 2, color="#999", lw=0.5, ls=":")

# --- (2) v_out（i_C の積分）
ax = axes[1]
setup(ax, 0, 1.1, r"$v_{\mathrm{out}}$")
dt = t[1] - t[0]
v = np.cumsum(iC) * dt
v = v - v.mean()
v = 0.55 + v / (v.max() - v.min()) * 0.55
ax.plot(t, v, color=BLUE, lw=1.3, zorder=3)
ax.plot([0, TMAX], [0.55] * 2, color=RED, lw=0.8, ls="--", zorder=2)
ax.text(-0.06 * TMAX, 0.55, r"$V_{\mathrm{out}}$", ha="right", va="center",
        fontsize=6.8, color=RED)
xd = 2.10 * T
ax.annotate("", xy=(xd, v.max()), xytext=(xd, v.min()),
            arrowprops=dict(arrowstyle="<->", lw=0.9, color=BK,
                            mutation_scale=7))
ax.text(xd + 0.04, 0.55, r"$\Delta V_{\mathrm{out}}$", ha="left",
        va="center", fontsize=7.2)
ax.plot([t2 + T, xd + 0.04], [v.max()] * 2, color="#999", lw=0.5, ls=":")
ax.plot([t1 + T, xd + 0.04], [v.min()] * 2, color="#999", lw=0.5, ls=":")

fig.subplots_adjust(hspace=0.6)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig5.6.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
