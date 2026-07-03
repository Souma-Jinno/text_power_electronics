#!/usr/bin/env python3
# fig11.1（第11章）: 高周波化のトレードオフ。
# (a) 必要な L・C はスイッチング周波数 f に反比例して小さくなる（5章の設計式）。
# (b) 台形波の高調波の包絡線は，f を10倍にすると -20dB/dec 領域で 20dB 持ち上がる。
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
GRN = "#1e8449"

fig, axes = plt.subplots(1, 2, figsize=(4.25, 2.0))

# ---- (a) 必要な L・C ∝ 1/f （100 kHz の値を 1 と置いた相対値）----
ax = axes[0]
f = np.logspace(4.5, 7, 200)
ax.loglog(f, 1e5 / f, color=BLUE, lw=1.3)
ax.loglog([1e5], [1.0], "o", ms=4, color=RED, zorder=3)
ax.text(2.2e5, 1.3, r"$\propto 1/f$", fontsize=7, color=BLUE)
ax.set_xlabel("$f$ [Hz]", fontsize=7)
ax.set_ylabel("必要な $L$・$C$（相対値）", fontsize=6.6, fontproperties=JP)
ax.set_ylim(3e-3, 6)
ax.tick_params(labelsize=6.5, which="both")
ax.grid(True, which="both", lw=0.3, color="#ccc", ls=":")
ax.set_title("(a) 部品は小さくなる", fontsize=7, fontproperties=JP, pad=3)

# ---- (b) スペクトル包絡線が持ち上がる ----
ax = axes[1]
A, D, tr = 1.0, 0.5, 10e-9
f = np.logspace(4, 8.5, 400)


def env_db(f, fsw):
    tau = D / fsw
    f1 = 1 / (np.pi * tau)
    f2 = 1 / (np.pi * tr)
    e = 2 * A * D * np.minimum(1, f1 / f) * np.minimum(1, f2 / f)
    return 20 * np.log10(e)


ax.semilogx(f, env_db(f, 1e5), color=BLUE, lw=1.3, label="$f=100$ kHz")
ax.semilogx(f, env_db(f, 1e6), color=RED, lw=1.3, label="$f=1$ MHz")
ax.annotate("", xy=(3e6, env_db(np.array([3e6]), 1e6)[0]),
            xytext=(3e6, env_db(np.array([3e6]), 1e5)[0]),
            arrowprops=dict(arrowstyle="-|>", lw=1.0, color=GRN, mutation_scale=8))
ax.text(4e6, -32, "+20 dB", fontsize=6.6, color=GRN)
ax.set_xlabel("周波数 [Hz]", fontsize=7, fontproperties=JP)
ax.set_ylabel("高調波の包絡線 [dB]", fontsize=6.6, fontproperties=JP)
ax.set_ylim(-80, 8)
ax.tick_params(labelsize=6.5, which="both")
ax.grid(True, which="both", lw=0.3, color="#ccc", ls=":")
ax.legend(fontsize=6, loc="lower left", frameon=False)
ax.set_title("(b) ノイズは増える", fontsize=7, fontproperties=JP, pad=3)

for ax in axes:
    for s in ax.spines.values():
        s.set_linewidth(0.6)

fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig11.1.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
