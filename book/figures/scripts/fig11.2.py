#!/usr/bin/env python3
# fig11.2（第11章）: 台形波とそのスペクトル。
# (a) 台形波の記号の定義（模式図）。(b) 高調波振幅と包絡線。
# f=100kHz, D=0.5, t_r=10ns → f1=1/(πτ)=63.7kHz, f2=1/(π t_r)=31.8MHz。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BK = "#222222"
BLUE = "#2a5db0"
RED = "#c0392b"

fig = plt.figure(figsize=(4.25, 2.95))
gs = fig.add_gridspec(2, 1, height_ratios=[0.8, 1.5], hspace=0.5)

# ---- (a) 台形波の模式図 ----
ax = fig.add_subplot(gs[0])
tr, tau, T = 1.2, 4.6, 10.5  # 模式図なので誇張した比率
xs, ys = [], []
for t0 in (0.0, T):
    pts = [(t0, 0), (t0 + tr, 1), (t0 + tau, 1), (t0 + tau + tr, 0)]
    for p in pts:
        xs.append(p[0]); ys.append(p[1])
xs.append(2 * T); ys.append(0)
ax.plot(xs, ys, color=BK, lw=1.4)
# 注釈
ax.annotate("", xy=(tau + tr / 2, 0.5), xytext=(tr / 2, 0.5),
            arrowprops=dict(arrowstyle="<|-|>", lw=0.8, color=BLUE, mutation_scale=7))
ax.text(0.5 * (tau + tr), 0.62, r"$\tau$", ha="center", fontsize=8, color=BLUE)
ax.annotate("", xy=(T, -0.30), xytext=(0, -0.30),
            arrowprops=dict(arrowstyle="<|-|>", lw=0.8, color="#1e8449", mutation_scale=7))
ax.text(0.5 * T, -0.64, "$T$", ha="center", fontsize=8, color="#1e8449")
ax.annotate("", xy=(tr, 1.16), xytext=(0, 1.16),
            arrowprops=dict(arrowstyle="<|-|>", lw=0.8, color=RED, mutation_scale=6))
ax.text(0.1, 1.30, "$t_r$", ha="center", fontsize=7.5, color=RED)
ax.annotate("", xy=(tau + tr, 1.16), xytext=(tau, 1.16),
            arrowprops=dict(arrowstyle="<|-|>", lw=0.8, color=RED, mutation_scale=6))
ax.text(tau + tr + 0.3, 1.30, "$t_f\\;(=t_r)$", ha="left", fontsize=7.5, color=RED)
ax.plot([-0.9, -0.3], [1, 1], color=BK, lw=0.6, ls=":")
ax.text(-1.1, 1.0, "$A$", ha="right", va="center", fontsize=8)
ax.plot([-0.5, 21.3], [0, 0], color="#888", lw=0.5, zorder=0)
ax.text(21.5, 0, "$t$", ha="left", va="center", fontsize=8)
ax.set_xlim(-2.2, 22.3)
ax.set_ylim(-0.98, 1.62)
ax.axis("off")
ax.set_title("(a) 台形波の記号", fontsize=7.2, fontproperties=JP, pad=1)

# ---- (b) スペクトルと包絡線 ----
ax = fig.add_subplot(gs[1])
A, fsw, D, trr = 1.0, 1e5, 0.5, 10e-9
tau_s = D / fsw
f1 = 1 / (np.pi * tau_s)
f2 = 1 / (np.pi * trr)
n = np.arange(1, 3001)
fn = n * fsw
x1 = np.pi * fn * tau_s
x2 = np.pi * fn * trr
an = 2 * A * D * np.abs(np.sinc(x1 / np.pi)) * np.abs(np.sinc(x2 / np.pi))
db = 20 * np.log10(np.maximum(an, 1e-8))
m = db > -105
ax.semilogx(fn[m], db[m], ".", ms=1.6, color=BLUE, zorder=2)

f = np.logspace(4.7, 8.5, 400)
env = 2 * A * D * np.minimum(1, f1 / f) * np.minimum(1, f2 / f)
ax.semilogx(f, 20 * np.log10(env), color="#eba79e", lw=2.2, zorder=1.5)

for fc, lab in [(f1, r"$f_1=\dfrac{1}{\pi\tau}$"), (f2, r"$f_2=\dfrac{1}{\pi t_r}$")]:
    ax.axvline(fc, color="#888", lw=0.8, ls="--", zorder=1)
ax.text(f1 * 1.15, -97, r"$f_1=1/\pi\tau$", fontsize=6.8, color="#555")
ax.text(f2 * 1.15, -97, r"$f_2=1/\pi t_r$", fontsize=6.8, color="#555")
ax.text(6e5, -16, "$-20$ dB/dec", fontsize=7, color=RED, rotation=-13)
ax.text(1.0e8, -52, "$-40$ dB/dec", fontsize=7, color=RED, rotation=-25)
ax.set_xlabel("周波数 [Hz]", fontsize=7, fontproperties=JP)
ax.set_ylabel(r"振幅 $20\log_{10}(a_n/A)$ [dB]", fontsize=6.8, fontproperties=JP)
ax.set_xlim(5e4, 3e8)
ax.set_ylim(-105, 8)
ax.tick_params(labelsize=6.5, which="both")
ax.grid(True, which="both", lw=0.3, color="#ccc", ls=":")
for s in ax.spines.values():
    s.set_linewidth(0.6)
ax.set_title("(b) 高調波の振幅（点）と包絡線（実線）", fontsize=7.2,
             fontproperties=JP, pad=2)

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig11.2.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
