#!/usr/bin/env python3
# fig6.5（第6章）: フライバックコンバータ。(a)回路（極性マークが上下逆），
# (b)動作波形（Vin=12V, N1=N2, Lm=0.7mH, D=0.2941, T=50us, Vo=5V, R=5Ω）。
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

def diode(ax, x, y, ang=0, s=0.16, color="k"):
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

fig = plt.figure(figsize=(4.3, 3.9))
gs = fig.add_gridspec(3, 1, height_ratios=[2.3, 1.0, 1.15], hspace=0.5)

# ============ (a) 回路 ============
ax = fig.add_subplot(gs[0])
YT, YB = 2.4, 0.0
source(ax, 0.0, 1.2, label=r"$V_{in}$")
ax.plot([0.0, 0.0], [1.5, YT], lw=1.1, color="k")
ax.plot([0.0, 0.0], [0.9, YB], lw=1.1, color="k")
# スイッチ（上側）
ax.plot([0.0, 0.8], [YT, YT], lw=1.1, color="k")
ax.plot([0.8, 1.35], [YT, YT + 0.28], lw=1.2, color="k")
ax.plot(0.8, YT, "o", ms=2.6, mfc="w", mec="k", mew=0.9)
ax.plot(1.4, YT, "o", ms=2.6, mfc="w", mec="k", mew=0.9)
ax.text(1.1, 2.95, r"$\mathrm{S}$", fontsize=8)
ax.plot([1.4, 2.3], [YT, YT], lw=1.1, color="k")
# 1次巻線（励磁インダクタンス）
coil_v(ax, 2.3, 1.0, YT, n=4, side=-1, color=BLUE)
ax.plot(2.17, 2.22, "o", ms=2.4, color="k")     # ドット上
ax.text(1.58, 1.85, r"$N_1$", fontsize=7.5, ha="center")
ax.plot([2.3, 2.3], [1.0, YB], lw=1.1, color="k")
ax.plot([0.0, 2.3], [YB, YB], lw=1.1, color="k")
ax.annotate("", xy=(1.95, 1.15), xytext=(1.95, 1.75),
            arrowprops=dict(arrowstyle="-|>", lw=1.0, color=GREEN))
ax.text(1.66, 1.2, r"$i_1$", fontsize=7.5, color=GREEN)
# 鉄心
ax.plot([2.58, 2.58], [0.85, 2.55], lw=1.1, color="#777")
ax.plot([2.68, 2.68], [0.85, 2.55], lw=1.1, color="#777")
# 2次巻線（ドットは下側＝逆向き）
coil_v(ax, 2.96, 1.0, YT, n=4, side=1, color=BLUE)
ax.plot(3.09, 1.18, "o", ms=2.4, color="k")     # ドット下
ax.text(3.42, 0.6, r"$N_2$", fontsize=7.5, ha="center")
ax.annotate("", xy=(3.55, 1.95), xytext=(3.55, 1.35),
            arrowprops=dict(arrowstyle="-|>", lw=1.0, color=GREEN))
ax.text(3.72, 1.3, r"$i_2$", fontsize=7.5, color=GREEN)
ax.plot([2.96, 2.96], [1.0, YB], lw=1.1, color="k")
ax.plot([2.96, 5.6], [YB, YB], lw=1.1, color="k")
# D → C, R
ax.plot([2.96, 4.0], [YT, YT], lw=1.1, color="k")
diode(ax, 4.2, YT, ang=0)
ax.text(4.2, 2.72, r"$\mathrm{D}$", fontsize=7.5, ha="center")
ax.plot([4.4, 4.9], [YT, YT], lw=1.1, color="k")
ax.plot(4.9, YT, "o", ms=2.0, color="k")
ax.plot([4.9, 4.9], [YB, 1.08], lw=1.1, color="k")
ax.plot([4.9, 4.9], [1.32, YT], lw=1.1, color="k")
cap(ax, 4.9, 1.2)
ax.plot(4.9, YB, "o", ms=2.0, color="k")
ax.text(5.17, 1.2, r"$C$", fontsize=8)
ax.plot([4.9, 5.6], [YT, YT], lw=1.1, color="k")
res_v(ax, 5.6, 0.85, 1.55)
ax.plot([5.6, 5.6], [YB, 0.85], lw=1.1, color="k")
ax.plot([5.6, 5.6], [1.55, YT], lw=1.1, color="k")
ax.text(5.85, 1.2, r"$R$", fontsize=8)
ax.annotate("", xy=(6.4, 1.65), xytext=(6.4, 0.75),
            arrowprops=dict(arrowstyle="-|>", lw=0.9, color="k"))
ax.text(6.57, 1.2, r"$V_o$", fontsize=8.5, va="center")
ax.text(3.35, 3.1, "極性マークが上下逆", fontsize=6.6, fontproperties=JP,
        ha="left", color=RED)
ax.annotate("", xy=(2.75, 2.65), xytext=(3.45, 3.02),
            arrowprops=dict(arrowstyle="->", lw=0.8, color=RED))
ax.text(3.0, -0.6, "(a) 回路", ha="center", fontsize=7.4,
        fontproperties=JP, color="#555")
ax.set_xlim(-0.75, 6.85)
ax.set_ylim(-0.9, 3.35)
ax.set_aspect("equal")
ax.axis("off")

# ============ (b) 波形 ============
T = 50.0
D = 0.2941
Vin, Vo = 12.0, 5.0
Lm = 0.7e-3
t = np.linspace(0, 2 * T, 3001)
ph = t % T
on = ph < D * T
vLm = np.where(on, Vin, -Vo)
Io = Vo / 5.0
Im_avg = Io / (1 - D)
dIm = Vin * D * T * 1e-6 / Lm
i1 = np.where(on, Im_avg - dIm / 2 + dIm * ph / (D * T), np.nan)
i2 = np.where(~on, Im_avg + dIm / 2 - dIm * (ph - D * T) / ((1 - D) * T), np.nan)
axs = [fig.add_subplot(gs[i]) for i in range(1, 3)]
for a in axs:
    for k in range(2):
        a.axvspan(k * T, (k + D) * T, color="#eef3fb", zorder=0)
    a.tick_params(labelsize=7)
    a.set_xlim(0, 2 * T)

axs[0].plot(t, vLm, lw=1.3, color=RED)
axs[0].axhline(0, lw=0.5, color="#999")
axs[0].set_ylim(-9, 17)
axs[0].set_yticks([-5, 0, 12])
axs[0].set_ylabel(r"$v_{Lm}$ [V]", fontsize=7.5)
axs[0].text(3, 13.3, r"$V_{in}$", fontsize=7.5, color=RED)
axs[0].text(30, -7.8, r"$-\frac{N_1}{N_2}V_o$", fontsize=7.5, color=RED)
axs[0].text(1.5, -7.2, "(b) 動作波形", fontsize=7.2, fontproperties=JP,
            color="#555")

axs[1].plot(t, i1, lw=1.3, color=BLUE, label=r"$i_1$")
axs[1].plot(t, i2, lw=1.3, color=GREEN, label=r"$i_2$")
axs[1].set_ylim(0, 2.1)
axs[1].set_yticks([0, 1, 2])
axs[1].set_ylabel(r"$i_1,\ i_2$ [A]", fontsize=7.5)
axs[1].text(5.5, 0.35, r"$i_1$ 蓄える", fontsize=6.8, fontproperties=JP,
            color=BLUE)
axs[1].text(27, 0.35, r"$i_2$ 渡す", fontsize=6.8, fontproperties=JP,
            color=GREEN)
axs[1].annotate("", xy=(D * T + 3.2, 1.72), xytext=(D * T - 3.2, 1.72),
                arrowprops=dict(arrowstyle="->", lw=0.9, color="#555"))
axs[1].text(D * T + 4.0, 1.72, "引き継ぎ", fontsize=6.4, fontproperties=JP,
            color="#555", va="center")
axs[1].set_xlabel(r"$t$ [$\mu$s]", fontsize=7.5)

fig.align_ylabels(axs)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig6.5.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
PNG = "/tmp/claude-1000/-home-soumajinno/e7688596-6b6f-45e4-950d-929e196c5bb6/scratchpad/fig6.5.png"
fig.savefig(PNG, format="png", dpi=160, bbox_inches="tight")
print("wrote", EPS)
