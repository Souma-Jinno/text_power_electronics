#!/usr/bin/env python3
# fig11.5（第11章）: ノイズ源の等価回路とリンギング。
# (a) 階段状の電圧源 + 配線の寄生 L_p・R + ダイオードの寄生 C_p の直列RLC回路
# (b) ステップ応答: L=40nH, R=0.1Ω, C=0.1nF, 10V → f_r≈80MHz のリンギング
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BK = "#222222"
BLUE = "#2a5db0"
RED = "#c0392b"


def wire(ax, pts, c=BK):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=c, lw=1.0,
            solid_capstyle="round", zorder=1)


def coil_h(ax, xa, xb, y, c=BK, n=4):
    dx = (xb - xa) / n
    r = dx / 2
    t = np.linspace(0, np.pi, 30)
    for k in range(n):
        xc = xa + dx * (k + 0.5)
        ax.plot(xc - r * np.cos(t), y + 0.9 * r * np.sin(t), color=c, lw=1.0)


def res_h(ax, xa, xb, y, c=BK):
    xc = 0.5 * (xa + xb)
    w, h = 0.9, 0.42
    wire(ax, [(xa, y), (xc - w / 2, y)], c)
    wire(ax, [(xc + w / 2, y), (xb, y)], c)
    ax.add_patch(Rectangle((xc - w / 2, y - h / 2), w, h,
                           fc="white", ec=c, lw=1.0, zorder=2))


def cap_v(ax, x, y1, y2, c=BK):
    yc = 0.5 * (y1 + y2)
    g, w = 0.10, 0.32
    wire(ax, [(x, y1), (x, yc + g)], c)
    wire(ax, [(x, yc - g), (x, y2)], c)
    ax.plot([x - w, x + w], [yc + g, yc + g], color=c, lw=1.3, zorder=2)
    ax.plot([x - w, x + w], [yc - g, yc - g], color=c, lw=1.3, zorder=2)


def step_src(ax, x, y1, y2, c=BK):
    r = 0.42
    yc = 0.5 * (y1 + y2)
    wire(ax, [(x, y1), (x, yc - r)], c)
    wire(ax, [(x, yc + r), (x, y2)], c)
    ax.add_patch(Circle((x, yc), r, fc="white", ec=c, lw=1.0, zorder=2))
    ax.plot([x - 0.2, x, x, x + 0.2], [yc - 0.13, yc - 0.13, yc + 0.13, yc + 0.13],
            color=c, lw=1.0, zorder=3)


fig = plt.figure(figsize=(4.25, 1.95))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.25], wspace=0.30)

# ---- (a) 回路 ----
ax = fig.add_subplot(gs[0])
yT, yB = 2.9, 0.5
xV, xL0, xL1, xR1, xC = 0.7, 1.4, 2.9, 4.1, 4.9
step_src(ax, xV, yB, yT)
ax.text(xV - 0.55, 0.5 * (yB + yT), "$v_{\\mathrm{sw}}$",
        ha="right", va="center", fontsize=8)
wire(ax, [(xV, yT), (xL0, yT)])
coil_h(ax, xL0, xL1, yT)
ax.text(0.5 * (xL0 + xL1), yT + 0.45, "$L_p$", ha="center", fontsize=8)
res_h(ax, xL1, xR1, yT)
ax.text(0.5 * (xL1 + xR1), yT + 0.45, "$R$", ha="center", fontsize=8)
wire(ax, [(xR1, yT), (xC, yT)])
cap_v(ax, xC, yT, yB)
ax.text(xC - 0.45, 1.15, "$C_p$", ha="right", va="center", fontsize=8)
wire(ax, [(xV, yB), (xC, yB)])
ax.annotate("", xy=(xC + 0.95, 2.15), xytext=(xC + 0.95, 1.15),
            arrowprops=dict(arrowstyle="-|>", lw=1.0, color=RED, mutation_scale=8))
ax.text(xC + 1.12, 1.65, "$v_C$", ha="left", va="center", fontsize=8, color=RED)
ax.set_xlim(-0.7, 6.7)
ax.set_ylim(-0.5, 3.9)
ax.set_aspect("equal")
ax.axis("off")
ax.text(3.0, -0.45, "(a) 等価回路", ha="center", fontsize=6.8,
        fontproperties=JP, color="#555")

# ---- (b) リンギング波形 ----
ax = fig.add_subplot(gs[1])
L, R, C, A = 40e-9, 0.1, 0.1e-9, 10.0
al = R / (2 * L)
w0 = 1 / np.sqrt(L * C)
wd = np.sqrt(w0**2 - al**2)
t = np.linspace(0, 100e-9, 4000)
v = A * (1 - np.exp(-al * t) * (np.cos(wd * t) + al / wd * np.sin(wd * t)))
ax.plot(t * 1e9, v, color=RED, lw=0.9)
ax.axhline(A, color="#888", lw=0.5, ls=":")
ax.text(97, A + 1.0, "10 V", ha="right", fontsize=6.5, color="#555")
Tp = 2 * np.pi / wd * 1e9
ax.annotate("", xy=(3 * Tp, 21.3), xytext=(2 * Tp, 21.3),
            arrowprops=dict(arrowstyle="<|-|>", lw=0.7, color=BLUE, mutation_scale=6))
ax.text(2.5 * Tp + 9, 21.2, r"12.6 ns（$f_r \approx 80$ MHz）",
        fontsize=6.5, color=BLUE, fontproperties=JP, va="center")
ax.set_xlabel("時間 [ns]", fontsize=7, fontproperties=JP)
ax.set_ylabel("$v_C$ [V]", fontsize=7)
ax.set_xlim(0, 100)
ax.set_ylim(-1.5, 24.5)
ax.tick_params(labelsize=6.5)
ax.grid(True, lw=0.3, color="#ccc", ls=":")
for s in ax.spines.values():
    s.set_linewidth(0.6)
ax.set_title("(b) $C_p$ の電圧（リンギング）", fontsize=6.8,
             fontproperties=JP, pad=3)

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig11.5.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
