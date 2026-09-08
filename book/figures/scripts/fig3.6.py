#!/usr/bin/env python3
# fig3.6（第3章）: ドリフト層の電界分布と耐圧。
# 電界は接合面で最大の三角形分布。面積が耐圧V_B，高さの上限が絶縁破壊電界E_c。
# 高耐圧には低濃度・厚いドリフト層が要る＝抵抗が増える，を視覚化する。
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BLUE = "#2a5db0"
RED = "#c0392b"
FILLA = "#f2c48c"
GRAY = "#555555"

fig, ax = plt.subplots(figsize=(4.25, 2.45))

EC = 1.55          # 絶縁破壊電界の高さ
BAR_Y, BAR_H = 2.05, 0.42

def device(x0, wp, wn, wsub, labels=True):
    # p+ | n-（ドリフト層）| n+ の構造バー
    ax.add_patch(Rectangle((x0, BAR_Y), wp, BAR_H, fc="#e9b7b0", ec="#555", lw=0.8))
    ax.add_patch(Rectangle((x0 + wp, BAR_Y), wn, BAR_H, fc="#dce8f8", ec="#555", lw=0.8))
    ax.add_patch(Rectangle((x0 + wp + wn, BAR_Y), wsub, BAR_H, fc="#9fbde8", ec="#555", lw=0.8))
    ax.text(x0 + wp / 2, BAR_Y + BAR_H / 2, "p$^+$", ha="center", va="center", fontsize=8)
    ax.text(x0 + wp + wn / 2, BAR_Y + BAR_H / 2, "n$^-$", ha="center", va="center", fontsize=8)
    ax.text(x0 + wp + wn + wsub / 2, BAR_Y + BAR_H / 2, "n$^+$", ha="center", va="center", fontsize=8)
    return x0 + wp          # 接合面の位置

# (a) 低耐圧: 高濃度・薄い
xj1 = device(0.25, 0.32, 1.35, 0.45)
W1 = 1.35
ax.fill([xj1, xj1, xj1 + W1], [0, EC, 0], fc=FILLA, ec=RED, lw=1.1, alpha=0.85)
# 小さい三角形には入らないので，ラベルは外に出して引き出し線で示す
ax.annotate("面積 $=V_B$", xy=(xj1 + W1 * 0.38, 0.42), xytext=(xj1 + W1 + 0.12, 0.22),
            fontsize=8, fontproperties=JP, color="#7a4a10", va="center",
            arrowprops=dict(arrowstyle="-", lw=0.6, color="#7a4a10", shrinkB=2))
ax.text(xj1 + W1 + 0.12, 0.95, "傾き $\\dfrac{eN_d}{\\varepsilon}$",
        fontsize=8, color=RED, fontproperties=JP)
ax.text(xj1 + W1 / 2, -0.98, "(a) 高濃度・薄い\n耐圧小・抵抗小", ha="center",
        va="top", fontsize=8, fontproperties=JP, color="#333")

# (b) 高耐圧: 低濃度・厚い
xj2 = device(4.05, 0.32, 3.6, 0.45)
W2 = 3.6
ax.fill([xj2, xj2, xj2 + W2], [0, EC, 0], fc=FILLA, ec=RED, lw=1.1, alpha=0.85)
ax.text(xj2 + W2 * 0.28, 0.5, "面積 $=V_B$（大）", fontsize=8,
        fontproperties=JP, color="#7a4a10")
ax.text(xj2 + W2 / 2, -0.98, "(b) 低濃度・厚い\n耐圧大・抵抗大", ha="center",
        va="top", fontsize=8, fontproperties=JP, color="#333")
for xj, W in [(xj1, W1), (xj2, W2)]:
    ax.annotate("", xy=(xj + W, -0.15), xytext=(xj, -0.15),
                arrowprops=dict(arrowstyle="<->", lw=0.8, color=GRAY))
    ax.text(xj + W / 2, -0.40, "$W$", ha="center", va="center",
            fontsize=8, color=GRAY)

# 絶縁破壊電界の上限線
ax.plot([0.0, 8.6], [EC, EC], ls="--", lw=0.9, color=RED)
ax.text(8.55, EC + 0.09, "$\\mathcal{E}_c$（これ以上で絶縁破壊）", ha="right",
        fontsize=8, fontproperties=JP, color=RED)

# 軸
ax.annotate("", xy=(-0.35, 2.0), xytext=(-0.35, 0),
            arrowprops=dict(arrowstyle="-|>", lw=0.9, color="#777"))
ax.text(-0.55, 1.0, "電界の大きさ $\\mathcal{E}$", rotation=90, va="center",
        ha="center", fontsize=8, fontproperties=JP, color="#555")
ax.annotate("", xy=(8.75, 0), xytext=(-0.35, 0),
            arrowprops=dict(arrowstyle="-|>", lw=0.9, color="#777"))
ax.text(8.72, -0.28, "位置 $x$", ha="right", fontsize=8,
        fontproperties=JP, color="#555")

ax.set_xlim(-0.8, 8.9)
ax.set_ylim(-1.6, 2.75)
ax.axis("off")
fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig3.6.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
