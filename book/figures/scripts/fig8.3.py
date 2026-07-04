#!/usr/bin/env python3
# fig8.3（第8章）: キャパシタインプット形の平滑動作。
# 充電（ダイオード導通）と放電（負荷へ供給）でリプル電圧が生じ，
# 電源電流がピーク付近のパルス状になることを示す。
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
SHADE = "#eef3fb"

Tr = 0.5              # リプル周期（全波なので電源半周期）
tau = 2.2            # 放電時定数（RC）
peak_t = 0.25        # 最初のピーク位置
t = np.linspace(0, 2.0, 4000)
env = np.abs(np.sin(np.pi * t / Tr))     # 整流電圧の包絡線
peaks = np.arange(peak_t, 2.05, Tr)

# キャパシタ電圧: 直前ピークからの指数放電と整流電圧の大きい方
vc = np.zeros_like(t)
for i, ti in enumerate(t):
    pv = peaks[peaks <= ti]
    if len(pv) == 0:
        vc[i] = env[i]
        continue
    disch = np.exp(-(ti - pv[-1]) / tau)
    vc[i] = env[i] if env[i] >= disch else disch
charging = env >= vc - 1e-6              # ダイオード導通区間

fig, axes = plt.subplots(2, 1, figsize=(4.15, 2.9), sharex=True)

# --- 上：電圧
ax = axes[0]
ax.axhline(0, color=BK, lw=0.8)
ax.plot(t, env, color="#9aa7bd", lw=1.0, ls="--", zorder=2)
ax.fill_between(t, 0, vc, color=SHADE, zorder=1)
ax.plot(t, vc, color=BLUE, lw=1.6, zorder=3)
vtop, vbot = 1.0, np.exp(-Tr / tau)
xr = peaks[1] + 0.03
ax.annotate("", xy=(xr, vtop), xytext=(xr, vbot),
            arrowprops=dict(arrowstyle="<->", lw=0.9, color=BK, mutation_scale=6))
ax.text(xr + 0.04, 0.5 * (vtop + vbot), r"$\Delta V$", fontsize=7.5, va="center")
ax.text(0.30, 1.12, "整流電圧", fontsize=6.6, fontproperties=JP, color="#888")
ax.text(1.02, 0.55, r"$v_C$（出力）", fontsize=7.4, fontproperties=JP, color=BLUE)
ax.text(0.60, 0.86, "放電", fontsize=6.4, fontproperties=JP, color="#555")
ax.set_ylim(-0.05, 1.32)
ax.axis("off")

# --- 下：電源（ダイオード）電流＝充電中のパルス
ax = axes[1]
ax.axhline(0, color=BK, lw=0.8)
isrc = np.zeros_like(t)
for lp in peaks:
    seg = (t > lp - 0.10) & (t <= lp)
    if seg.any():
        isrc[seg] = 1.0 * (1 - (lp - t[seg]) / 0.10)
ax.fill_between(t, 0, isrc, color="#fbecea", zorder=1)
ax.plot(t, isrc, color=RED, lw=1.4, zorder=3)
ax.text(1.02, 0.74, r"$i_S$（電源電流）", fontsize=7.4, fontproperties=JP, color=RED)
ax.text(0.50, 0.34, "充電時だけ\nパルス状に流れる", fontsize=6.2,
        fontproperties=JP, color="#555")
for x in [0.5, 1.0, 1.5, 2.0]:
    ax.plot([x, x], [-0.04, 0.04], color=BK, lw=0.8)
ax.text(2.06, -0.02, r"$t$", ha="left", va="top", fontsize=7)
ax.set_ylim(-0.1, 1.25)
ax.axis("off")

fig.subplots_adjust(hspace=0.12)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig8.3.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
