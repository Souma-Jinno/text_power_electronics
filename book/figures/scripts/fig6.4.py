#!/usr/bin/env python3
# fig6.4（第6章）: フォワードコンバータ。(a)リセット巻線付き回路，
# (b)動作波形（Vin=100V, N1:N2=10:1, N3=N1, D=0.3, T=50us, L=1mH, Vo=3V）。
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
GREEN = "#1e7a3c"

def coil_v(ax, x, y0, y1, n=4, side=1, color="k", lw=1.1):
    ys = np.linspace(y0, y1, n + 1)
    for i in range(n):
        t = np.linspace(-np.pi / 2, np.pi / 2, 24)
        r = (ys[i + 1] - ys[i]) / 2
        yc = (ys[i] + ys[i + 1]) / 2
        ax.plot(x + side * r * 1.4 * np.cos(t), yc + r * np.sin(t), lw=lw, color=color)

def coil_h(ax, x0, x1, y, n=4, color="k", lw=1.1):
    xs = np.linspace(x0, x1, n + 1)
    for i in range(n):
        t = np.linspace(np.pi, 0, 24)
        r = (xs[i + 1] - xs[i]) / 2
        xc = (xs[i] + xs[i + 1]) / 2
        ax.plot(xc + r * np.cos(t), y + r * 1.4 * np.sin(t), lw=lw, color=color)

def diode(ax, x, y, ang=0, s=0.16, color="k"):
    """中心(x,y)，ang=0で右向き導通"""
    c, si = np.cos(np.radians(ang)), np.sin(np.radians(ang))
    def R(px, py):
        return (x + c * px - si * py, y + si * px + c * py)
    tri = [R(-s, s), R(-s, -s), R(s, 0)]
    ax.add_patch(plt.Polygon(tri, closed=True, fc=color, ec=color, lw=0))
    b1, b2 = R(s, s), R(s, -s)
    ax.plot([b1[0], b2[0]], [b1[1], b2[1]], lw=1.2, color=color)

def source(ax, x, yc, r=0.3, label=""):
    t = np.linspace(0, 2 * np.pi, 60)
    ax.plot(x + r * np.cos(t), yc + r * np.sin(t), lw=1.1, color="k")
    ax.text(x, yc + r * 0.45, "+", ha="center", va="center", fontsize=7)
    ax.text(x, yc - r * 0.5, "−", ha="center", va="center", fontsize=7)
    if label:
        ax.text(x - r - 0.12, yc, label, ha="right", va="center", fontsize=8.5)

def cap(ax, x, yc, w=0.22, gap=0.08):
    ax.plot([x - w, x + w], [yc + gap, yc + gap], lw=1.4, color="k")
    ax.plot([x - w, x + w], [yc - gap, yc - gap], lw=1.4, color="k")

def res_v(ax, x, y0, y1, w=0.14):
    ax.add_patch(plt.Rectangle((x - w, y0), 2 * w, y1 - y0, fc="w", ec="k", lw=1.1))

fig = plt.figure(figsize=(4.3, 4.1))
gs = fig.add_gridspec(4, 1, height_ratios=[2.5, 1.0, 1.0, 1.0], hspace=0.5)

# ============ (a) 回路 ============
ax = fig.add_subplot(gs[0])
YT, YB = 2.4, 0.0
# 電源
source(ax, 0.0, 1.2, label=r"$V_{in}$")
ax.plot([0.0, 0.0], [1.5, YT], lw=1.1, color="k")
ax.plot([0.0, 0.0], [0.9, YB], lw=1.1, color="k")
ax.plot([0.0, 2.2], [YT, YT], lw=1.1, color="k")
ax.plot([0.0, 2.2], [YB, YB], lw=1.1, color="k")
# リセット巻線 N3 + D3
ax.plot([1.0, 1.0], [YB, 0.45], lw=1.1, color="k")
coil_v(ax, 1.0, 0.45, 1.55, n=3, side=-1, color=BLUE)
ax.plot([1.0, 1.0], [1.55, 1.75], lw=1.1, color="k")
diode(ax, 1.0, 1.95, ang=90, color="k")
ax.plot([1.0, 1.0], [2.15, YT], lw=1.1, color="k")
ax.plot(1.13, 0.62, "o", ms=2.4, color="k")   # ドット（下側）
ax.text(0.62, 1.0, r"$N_3$", fontsize=7.5, ha="center")
ax.text(0.62, 1.95, r"$\mathrm{D_3}$", fontsize=7.5, ha="center")
ax.text(1.0, 2.75, "リセット巻線", fontsize=6.6, fontproperties=JP,
        ha="center", color=BLUE)
ax.plot(1.0, YT, "o", ms=2.0, color="k")
ax.plot(1.0, YB, "o", ms=2.0, color="k")
# 1次巻線 N1 とスイッチ
coil_v(ax, 2.2, 1.0, YT, n=4, side=-1, color=BLUE)
ax.plot(2.07, 2.22, "o", ms=2.4, color="k")   # ドット（上側）
ax.text(1.85, 1.6, r"$N_1$", fontsize=7.5, ha="center")
ax.plot([2.2, 2.2], [1.0, 0.8], lw=1.1, color="k")
ax.plot([2.2, 2.45], [0.8, 0.25], lw=1.2, color="k")   # スイッチ
ax.plot(2.2, 0.8, "o", ms=2.6, mfc="w", mec="k", mew=0.9)
ax.plot(2.2, 0.25, "o", ms=2.6, mfc="w", mec="k", mew=0.9)
ax.plot([2.2, 2.2], [0.25, YB], lw=1.1, color="k")
ax.text(2.62, 0.55, r"$\mathrm{S}$", fontsize=8)
# 鉄心
ax.plot([2.48, 2.48], [0.85, 2.55], lw=1.1, color="#777")
ax.plot([2.58, 2.58], [0.85, 2.55], lw=1.1, color="#777")
# 2次巻線 N2
coil_v(ax, 2.86, 1.0, YT, n=4, side=1, color=BLUE)
ax.plot(2.99, 2.22, "o", ms=2.4, color="k")   # ドット（上側）
ax.text(3.22, 1.6, r"$N_2$", fontsize=7.5, ha="center")
ax.plot([2.86, 2.86], [1.0, YB], lw=1.1, color="k")
ax.plot([2.86, 5.75], [YB, YB], lw=1.1, color="k")
# D1 → L → 出力
ax.plot([2.86, 3.3], [YT, YT], lw=1.1, color="k")
diode(ax, 3.5, YT, ang=0)
ax.text(3.5, 2.72, r"$\mathrm{D_1}$", fontsize=7.5, ha="center")
ax.plot([3.7, 4.0], [YT, YT], lw=1.1, color="k")
ax.plot(4.0, YT, "o", ms=2.0, color="k")
# D2（還流）
diode(ax, 4.0, 1.2, ang=90)
ax.plot([4.0, 4.0], [YB, 1.0], lw=1.1, color="k")
ax.plot([4.0, 4.0], [1.4, YT], lw=1.1, color="k")
ax.plot(4.0, YB, "o", ms=2.0, color="k")
ax.text(4.32, 1.2, r"$\mathrm{D_2}$", fontsize=7.5, ha="center")
# L
coil_h(ax, 4.25, 5.05, YT, n=4)
ax.plot([4.0, 4.25], [YT, YT], lw=1.1, color="k")
ax.plot([5.05, 5.75], [YT, YT], lw=1.1, color="k")
ax.text(4.65, 2.75, r"$L$", fontsize=8, ha="center")
ax.annotate("", xy=(5.0, 2.18), xytext=(4.35, 2.18),
            arrowprops=dict(arrowstyle="-|>", lw=1.0, color=GREEN))
ax.text(4.65, 2.0, r"$i_L$", fontsize=7.5, ha="center", va="top", color=GREEN)
# C, R
ax.plot([5.05, 5.05], [YB, 1.08], lw=1.1, color="k")
ax.plot([5.05, 5.05], [1.32, YT], lw=1.1, color="k")
cap(ax, 5.05, 1.2)
ax.plot(5.05, YT, "o", ms=2.0, color="k")
ax.plot(5.05, YB, "o", ms=2.0, color="k")
ax.text(5.32, 1.2, r"$C$", fontsize=8)
res_v(ax, 5.75, 0.85, 1.55)
ax.plot([5.75, 5.75], [YB, 0.85], lw=1.1, color="k")
ax.plot([5.75, 5.75], [1.55, YT], lw=1.1, color="k")
ax.text(6.0, 1.2, r"$R$", fontsize=8)
ax.annotate("", xy=(6.55, 1.65), xytext=(6.55, 0.75),
            arrowprops=dict(arrowstyle="-|>", lw=0.9, color="k"))
ax.text(6.72, 1.2, r"$V_o$", fontsize=8.5, va="center")
ax.text(3.1, -0.6, "(a) 回路", ha="center", fontsize=7.4,
        fontproperties=JP, color="#555")
ax.set_xlim(-0.75, 7.0)
ax.set_ylim(-0.9, 3.05)
ax.set_aspect("equal")
ax.axis("off")

# ============ (b) 波形 ============
T = 50.0
D = 0.3
t = np.linspace(0, 2 * T, 3001)
ph = t % T
on = ph < D * T
sw = np.where(on, 1.0, 0.0)
vL = np.where(on, 7.0, -3.0)
# iL: 0.6 A 中心の三角波
dIL = 3.0 * (1 - D) * T * 1e-6 / 1e-3   # = 0.105 A
iL = np.where(on, 0.6 - dIL / 2 + dIL * ph / (D * T),
              0.6 + dIL / 2 - dIL * (ph - D * T) / ((1 - D) * T))
# im: オンで増加，リセット(N3=N1: 同じ時間)で減少，残りゼロ
Impk = 100.0 / 10e-3 * D * T * 1e-6     # = 0.15 A
im = np.where(on, Impk * ph / (D * T),
              np.where(ph < 2 * D * T, Impk * (1 - (ph - D * T) / (D * T)), 0.0))

axs = [fig.add_subplot(gs[i]) for i in range(1, 4)]
for a in axs:
    for k in range(2):
        a.axvspan(k * T, (k + D) * T, color="#eef3fb", zorder=0)
    a.tick_params(labelsize=7)
    a.set_xlim(0, 2 * T)

axs[0].plot(t, vL, lw=1.3, color=RED)
axs[0].axhline(0, lw=0.5, color="#999")
axs[0].set_ylim(-5.5, 10.5)
axs[0].set_yticks([-3, 0, 7])
axs[0].set_ylabel(r"$v_L$ [V]", fontsize=7.5)
axs[0].text(16, 7.4, r"$\frac{N_2}{N_1}V_{in}-V_o$", fontsize=7.5, color=RED)
axs[0].text(31, -2.6, r"$-V_o$", fontsize=7.5, color=RED, va="top")
axs[0].text(2.0, 8.2, "オン", fontsize=6.4, fontproperties=JP, color="#555")
axs[0].text(97.5, 7.6, "(b) 動作波形", fontsize=7.2, fontproperties=JP,
            color="#555", ha="right")

axs[1].plot(t, iL, lw=1.3, color=GREEN)
axs[1].set_ylim(0.47, 0.73)
axs[1].set_yticks([0.55, 0.65])
axs[1].set_ylabel(r"$i_L$ [A]", fontsize=7.5)

axs[2].plot(t, im, lw=1.3, color=BLUE)
axs[2].set_ylim(-0.03, 0.24)
axs[2].set_yticks([0, 0.15])
axs[2].set_ylabel(r"$i_m$ [A]", fontsize=7.5)
axs[2].set_xlabel(r"$t$ [$\mu$s]", fontsize=7.5)
axs[2].text(20.5, 0.13, "リセット", fontsize=6.8, fontproperties=JP, color=BLUE)

fig.align_ylabels(axs)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig6.4.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
PNG = "/tmp/claude-1000/-home-soumajinno/e7688596-6b6f-45e4-950d-929e196c5bb6/scratchpad/fig6.4.png"
fig.savefig(PNG, format="png", dpi=160, bbox_inches="tight")
print("wrote", EPS)
