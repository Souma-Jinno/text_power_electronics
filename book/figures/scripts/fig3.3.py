#!/usr/bin/env python3
# fig3.3（第3章）: 耐圧と特性オン抵抗のトレードオフ（材料限界線）。
# R_on A = 4 V_B^2 / (eps * mu_n * Ec^3) を Si / 4H-SiC / GaN について描く。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

E0 = 8.854e-12
mats = [
    # 名称, 比誘電率, 移動度[m^2/Vs], Ec[V/m], 色, ラベル位置(V, 倍率)
    ("Si",     11.7, 0.135, 3.0e7, "#c0392b"),
    ("4H-SiC",  9.7, 0.100, 2.5e8, "#2a5db0"),
    ("GaN",     9.0, 0.120, 3.3e8, "#1e8449"),
]

VB = np.logspace(1, 4, 200)

fig, ax = plt.subplots(figsize=(4.25, 2.9))

for name, er, mu, ec, col in mats:
    RonA = 4 * VB**2 / (er * E0 * mu * ec**3)   # [Ohm m^2]
    ax.loglog(VB, RonA * 1e7, color=col, lw=1.3)  # -> [mOhm cm^2]

ax.text(300, 14, "Si限界", fontsize=7.6, fontproperties=JP,
        color="#c0392b", rotation=25)
ax.text(1100, 0.028, "4H-SiC限界", fontsize=7.6, fontproperties=JP,
        color="#2a5db0", rotation=25)
ax.text(3300, 0.13, "GaN限界", fontsize=7.6, fontproperties=JP,
        color="#1e8449", rotation=25)

# 1200 V での比較（例題3.3）
Si = mats[0]; SiC = mats[1]
r_si = 4 * 1200**2 / (Si[1] * E0 * Si[2] * Si[3]**3) * 1e7
r_sic = 4 * 1200**2 / (SiC[1] * E0 * SiC[2] * SiC[3]**3) * 1e7
ax.plot([1200, 1200], [r_si, r_sic], ls=":", lw=0.9, color="#555")
ax.plot([1200], [r_si], "o", ms=3.5, color="#c0392b")
ax.plot([1200], [r_sic], "o", ms=3.5, color="#2a5db0")
ax.annotate("同じ耐圧で\n約1/360", xy=(1200, np.sqrt(r_si * r_sic)),
            xytext=(150, 0.35), fontsize=7.0, fontproperties=JP, color="#333",
            arrowprops=dict(arrowstyle="-|>", lw=0.8, color="#555"))

ax.text(16, 1.1e3, "傾き：$R_{\\mathrm{on}}A \\propto V_B^{\\,2}$\n"
        "（耐圧2倍で抵抗4倍）", fontsize=7.0, fontproperties=JP, color="#333")

ax.set_xlim(10, 1e4)
ax.set_ylim(1e-4, 1e4)
ax.set_xlabel("耐圧 $V_B$ [V]", fontsize=8, fontproperties=JP)
ax.set_ylabel("特性オン抵抗 $R_{\\mathrm{on}}A$ [m$\\Omega\\cdot$cm$^2$]",
              fontsize=8, fontproperties=JP)
ax.grid(True, which="major", ls=":", lw=0.5, color="#bbb")
ax.tick_params(labelsize=7)
fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig3.3.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
fig.savefig("/tmp/claude-1000/-home-soumajinno/e7688596-6b6f-45e4-950d-929e196c5bb6/scratchpad/fig3.3.png",
            dpi=180, bbox_inches="tight")
print("wrote", EPS)
