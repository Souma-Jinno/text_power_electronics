#!/usr/bin/env python3
# fig4.5（第4章）: PWMによる任意波形の生成。
# デューティ比を正弦波状に変えたスイッチング波形と，その平均（フィルタ後の出力）。
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

V0 = 1.0
N = 24  # 1正弦波周期あたりのスイッチング回数

fig, ax = plt.subplots(figsize=(4.25, 1.75))

Ts = 1.0 / N
tx = [0.0]
vx = [0.0]
for k in range(N):
    t0 = k * Ts
    d = 0.5 + 0.45 * np.sin(2 * np.pi * (t0 + Ts / 2))
    # 立ち上がり
    tx += [t0, t0, t0 + d * Ts, t0 + d * Ts]
    vx += [0, V0, V0, 0]
tx.append(1.0)
vx.append(0.0)
ax.plot(tx, vx, color=RED, lw=0.8)

t = np.linspace(0, 1, 600)
avg = V0 * (0.5 + 0.45 * np.sin(2 * np.pi * t))
ax.plot(t, avg, color=BLUE, lw=1.8)
ax.text(0.0, 1.09, "スイッチング波形", fontsize=7.2,
        fontproperties=JP, color=RED, ha="left")
ax.text(1.0, 1.09, r"平均 $D(t)V_0$（フィルタ後の出力）", fontsize=7.4,
        fontproperties=JP, color=BLUE, ha="right")

ax.set_ylim(-0.1, 1.28)
ax.set_yticks([0, V0])
ax.set_yticklabels(["$0$", "$V_0$"], fontsize=7)
ax.set_xticks([0, 0.5, 1])
ax.set_xticklabels(["$0$", "$T_1/2$", "$T_1$"], fontsize=7)
ax.set_xlabel("時刻 $t$（$T_1$: 作りたい正弦波の周期）", fontsize=7,
              fontproperties=JP)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)

fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig4.5.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
