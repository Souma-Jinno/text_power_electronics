#!/usr/bin/env python3
# fig9.5（第9章）: 正弦波PWM（バイポーラ変調）の生成原理。
# (a)三角波キャリアと正弦波の指令（変調波）の比較，
# (b)比較で決まる出力電圧 v（±E の方形パルス列。パルス幅が正弦波状に変わる）。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BK = "#222222"
RED = "#c0392b"
BLUE = "#2a5db0"

mf = 15          # キャリア比
m = 0.8          # 変調率
wt = np.linspace(0, 2 * np.pi, 6001)
ref = m * np.sin(wt)
# 三角波キャリア（±1）
carr = 2 / np.pi * np.arcsin(np.sin(mf * wt))
out = np.where(ref >= carr, 1.0, -1.0)

fig, axes = plt.subplots(2, 1, figsize=(4.3, 2.4), sharex=True)

ax = axes[0]
ax.axhline(0, color=BK, lw=0.6)
ax.plot(wt, carr, color=BK, lw=0.7, label="搬送波（三角波）")
ax.plot(wt, ref, color=RED, lw=1.6, label="指令信号（正弦波）")
ax.set_ylim(-1.25, 1.55)
ax.set_yticks([-1, 0, 1])
ax.set_yticklabels(["$-1$", "0", "1"], fontsize=6.4)
ax.legend(prop=fm.FontProperties(fname=JP.get_file(), size=5.8), ncol=2,
          loc="upper center", frameon=False, handlelength=1.4, columnspacing=1.0)
for sp in ax.spines.values():
    sp.set_visible(False)
ax.set_title("(a) 搬送波と指令信号の比較", fontproperties=JP, fontsize=7.2, color="#555")

ax = axes[1]
ax.axhline(0, color=BK, lw=0.6)
ax.plot(wt, out, color=BLUE, lw=1.0)
# 基本波（正弦）を重ねる
ax.plot(wt, m * np.sin(wt), color=RED, lw=1.2, ls="--")
ax.set_ylim(-1.5, 1.5)
ax.set_yticks([-1, 0, 1])
ax.set_yticklabels(["$-E$", "0", "$E$"], fontsize=6.4)
ax.set_xlim(0, 2 * np.pi)
ax.set_xticks([0, np.pi, 2 * np.pi])
ax.set_xticklabels(["0", r"$\pi$", r"$2\pi$"], fontsize=6.6)
ax.text(1.0, -0.02, r"$\omega t$", transform=ax.transAxes, fontsize=7)
ax.text(2 * np.pi * 0.5, 1.14, "出力 $v$（破線は基本波）", ha="center",
        fontsize=6.0, fontproperties=JP, color="#555")
for sp in ax.spines.values():
    sp.set_visible(False)
ax.set_title("(b) 出力電圧（バイポーラ）", fontproperties=JP, fontsize=7.2, color="#555")

fig.subplots_adjust(hspace=0.45)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig9.5.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
