#!/usr/bin/env python3
# fig4.6（第4章）: RLC直列回路のインピーダンスの大きさ |Z|(f)。
# 低周波はCが支配（容量性），高周波はLが支配（誘導性），共振周波数 f0 で |Z|=R。
# 例題4.3と同じ L=100 uH, C=10 uF。
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
GRAY = "#888888"

L = 100e-6
C = 10e-6
f = np.logspace(2, 6, 800)
w = 2 * np.pi * f
f0 = 1 / (2 * np.pi * np.sqrt(L * C))

fig, ax = plt.subplots(figsize=(4.25, 2.35))

for R, color, ls in [(0.5, BLUE, "-"), (5.0, RED, "-")]:
    Z = np.sqrt(R ** 2 + (w * L - 1 / (w * C)) ** 2)
    ax.loglog(f, Z, color=color, lw=1.4, ls=ls,
              label=rf"$R={R}\,\Omega$")

# 漸近線
ax.loglog(f, 1 / (w * C), color=GRAY, lw=0.8, ls="--")
ax.loglog(f, w * L, color=GRAY, lw=0.8, ls="--")
ax.text(2.6e2, 90, r"$\dfrac{1}{\omega C}$", fontsize=8, color=GRAY)
ax.text(4.5e5, 150, r"$\omega L$", fontsize=8, color=GRAY)
ax.text(6e2, 3.5e-2, "容量性（$C$が支配）", fontsize=7.0,
        fontproperties=JP, color="#555")
ax.text(2.6e4, 3.5e-2, "誘導性（$L$が支配）", fontsize=7.0,
        fontproperties=JP, color="#555")

# 共振周波数
ax.axvline(f0, color="#333", lw=0.7, ls=":")
ax.text(f0 * 1.12, 900, r"$f_0=\frac{1}{2\pi\sqrt{LC}}$", fontsize=8,
        color="#333")
ax.annotate(r"共振：$|Z|=R$", xy=(f0, 0.5), xytext=(1.6e4, 0.35),
            fontsize=7.2, fontproperties=JP, color=BLUE,
            arrowprops=dict(arrowstyle="->", lw=0.8, color=BLUE))

ax.set_xlabel("周波数 $f$ [Hz]", fontsize=8, fontproperties=JP)
ax.set_ylabel(r"$|Z|$ [$\Omega$]", fontsize=8)
ax.set_xlim(1e2, 1e6)
ax.set_ylim(1e-2, 3e3)
ax.tick_params(labelsize=7)
ax.legend(fontsize=7, loc="upper left", frameon=False,
          handlelength=1.6, borderaxespad=0.3)
ax.grid(True, which="major", lw=0.4, color="#dddddd")

fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig4.6.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
