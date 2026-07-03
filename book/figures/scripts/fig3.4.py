#!/usr/bin/env python3
# fig3.4（第3章）: スイッチング波形と損失。
# 誘導性負荷のターンオン・ターンオフで電圧と電流が重なる期間に p=vi の損失が出る。
# 上段: v, i の波形。下段: 瞬時電力 p=vi（山の面積が E_on, E_off）。
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

V, I, VON = 1.0, 1.0, 0.06
t1, t2, t3 = 1.5, 2.1, 2.7      # ターンオン: 電流上昇 → 電圧下降
t4, t5, t6 = 5.3, 5.9, 6.5      # ターンオフ: 電圧上昇 → 電流下降
T = 8.0

t = np.linspace(0, T, 2000)
v = np.piecewise(t,
    [t < t1, (t >= t1) & (t < t2), (t >= t2) & (t < t3),
     (t >= t3) & (t < t4), (t >= t4) & (t < t5), t >= t5],
    [V, V, lambda x: V + (VON - V) * (x - t2) / (t3 - t2),
     VON, lambda x: VON + (V - VON) * (x - t4) / (t5 - t4), V])
i = np.piecewise(t,
    [t < t1, (t >= t1) & (t < t2), (t >= t2) & (t < t5),
     (t >= t5) & (t < t6), t >= t6],
    [0, lambda x: I * (x - t1) / (t2 - t1), I,
     lambda x: I * (1 - (x - t5) / (t6 - t5)), 0])
p = v * i

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(4.25, 2.75), sharex=True,
                               gridspec_kw=dict(height_ratios=[1, 0.9]))

ax1.plot(t, v, color=RED, lw=1.3)
ax1.plot(t, i, color=BLUE, lw=1.3)
ax1.text(0.55, V + 0.10, "電圧 $v$", fontsize=7.2, fontproperties=JP, color=RED)
ax1.text(3.85, I + 0.10, "電流 $i$", fontsize=7.2, fontproperties=JP, color=BLUE)
ax1.text(0.55, 0.08, "オフ", fontsize=7.0, fontproperties=JP, color="#555")
ax1.text(3.80, 0.30, "オン", fontsize=7.0, fontproperties=JP, color="#555")
for x0, x1, lab in [(t1, t3, "$t_{\\mathrm{on}}$"), (t4, t6, "$t_{\\mathrm{off}}$")]:
    ax1.axvspan(x0, x1, color="#f6e2b8", alpha=0.55, lw=0)
    ax2.axvspan(x0, x1, color="#f6e2b8", alpha=0.55, lw=0)
    ax1.annotate("", xy=(x1, 1.28), xytext=(x0, 1.28),
                 arrowprops=dict(arrowstyle="<->", lw=0.7, color="#555"))
    ax1.text((x0 + x1) / 2, 1.36, lab, ha="center", fontsize=7.2, color="#555")
ax1.set_ylim(-0.08, 1.62)
ax1.set_yticks([])
ax1.tick_params(labelsize=7)

ax2.plot(t, p, color="#555", lw=1.1)
ax2.fill_between(t, p, 0, where=(t >= t1) & (t <= t3), color="#e0876d", alpha=0.85)
ax2.fill_between(t, p, 0, where=(t >= t4) & (t <= t6), color="#e0876d", alpha=0.85)
ax2.fill_between(t, p, 0, where=(t > t3) & (t < t4), color="#c8d8f0", alpha=0.9)
ax2.text(2.1, 1.13, "面積 $=E_{\\mathrm{on}}$", ha="center", fontsize=7.2,
         fontproperties=JP, color="#a04020")
ax2.text(5.9, 1.13, "面積 $=E_{\\mathrm{off}}$", ha="center", fontsize=7.2,
         fontproperties=JP, color="#a04020")
ax2.text(4.0, 0.28, "導通損失 $R_{\\mathrm{on}}I^2$", ha="center", fontsize=6.8,
         fontproperties=JP, color=BLUE)
ax2.annotate("ピークは $VI$", xy=(t2, 1.0), xytext=(0.35, 0.72),
             fontsize=7.0, fontproperties=JP, color="#333",
             arrowprops=dict(arrowstyle="-|>", lw=0.7, color="#555"))
ax2.set_ylim(0, 1.45)
ax2.set_yticks([])
ax2.set_xticks([])
ax2.set_xlabel("時間 $t$", fontsize=8, fontproperties=JP)
ax2.text(-0.25, 0.72, "$p = vi$", fontsize=8, rotation=90, va="center", ha="right")

fig.tight_layout(h_pad=0.4)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig3.4.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
fig.savefig("/tmp/claude-1000/-home-soumajinno/e7688596-6b6f-45e4-950d-929e196c5bb6/scratchpad/fig3.4.png",
            dpi=180, bbox_inches="tight")
print("wrote", EPS)
