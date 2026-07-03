#!/usr/bin/env python3
# fig2.5（第2章）: MOSFETの出力特性（ドレイン電流-ドレイン・ソース間電圧）。
# ゲート電圧をパラメータとした特性曲線。原点からまっすぐ立ち上がる
# （オン電圧の下駄がない＝抵抗として振る舞う）ことがポイント。
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

fig, ax = plt.subplots(figsize=(3.6, 2.6))

VTH = 2.0
K = 4.0   # A/V^2
vds = np.linspace(0, 5, 400)

for vgs in [3.0, 3.5, 4.0, 4.5, 5.0]:
    vov = vgs - VTH
    i = np.where(vds < vov, K * (vov * vds - vds**2 / 2), K * vov**2 / 2)
    ax.plot(vds, i, color=BLUE, lw=1.3)
    ax.text(5.05, K * vov**2 / 2, rf"$v_{{GS}}={vgs:.1f}$ V",
            fontsize=6.8, va="center", color="#333")

# 線形領域（オンで使う領域）の強調
ax.plot(vds[vds < 0.55], K * 3.0 * vds[vds < 0.55], color=RED, lw=2.0, ls="--")
ax.annotate("スイッチとして使う領域\n（傾きの逆数がオン抵抗$R_{on}$）",
            xy=(0.32, 5.2), xytext=(0.55, 18.6), va="top",
            fontsize=6.8, fontproperties=JP, color=RED,
            arrowprops=dict(arrowstyle="->", lw=0.8, color=RED,
                            shrinkB=4))
ax.text(2.2, 0.5, r"$v_{GS}<V_{th}$では$i_D=0$（オフ）", fontsize=6.8,
        fontproperties=JP, color="#555")

ax.set_xlim(0, 5)
ax.set_ylim(0, 20)
ax.set_yticks([0, 5, 10, 15, 20])
ax.set_xlabel("ドレイン-ソース間電圧 $v_{DS}$ 〔V〕",
              fontsize=7.6, fontproperties=JP)
ax.set_ylabel("ドレイン電流 $i_D$ 〔A〕", fontsize=7.6, fontproperties=JP)
ax.tick_params(labelsize=7)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig2.5.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
