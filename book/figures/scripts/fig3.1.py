#!/usr/bin/env python3
# fig3.1（第3章）: 物理特性→デバイス特性→回路性能の対応マップ。
# 材料の物理量（1章）がデバイス特性（本章）を決め，回路の性能（5章以降）に届く。
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BLUE = "#2a5db0"
RED = "#c0392b"
C_L = "#dce8f8"   # 材料
C_M = "#fdf0c8"   # デバイス
C_R = "#e8f4e0"   # 回路

fig, ax = plt.subplots(figsize=(4.25, 2.95))

CX = [1.55, 5.0, 8.45]      # 列の中心
W, H = 2.8, 0.82
RY = [4.55, 3.45, 2.35, 1.25]  # 行の中心

def box(cx, cy, text, fc, fs=7.0):
    r = FancyBboxPatch((cx - W / 2, cy - H / 2), W, H,
                       boxstyle="round,pad=0.06,rounding_size=0.10",
                       fc=fc, ec="#555", lw=0.8)
    ax.add_patch(r)
    ax.text(cx, cy, text, ha="center", va="center",
            fontsize=fs, fontproperties=JP)

# 列見出し
heads = ["材料の物理（1章）", "デバイス特性（本章）", "回路の性能（5章以降）"]
for cx, h in zip(CX, heads):
    ax.text(cx, 5.35, h, ha="center", va="center",
            fontsize=7.6, fontproperties=JP, color="#333")

L = ["バンドギャップ $E_g$", "絶縁破壊電界 $\\mathcal{E}_c$",
     "移動度 $\\mu$", "素子の容量 $C$\n（寸法・構造，2章）"]
M = ["漏れ電流・\n高温動作", "耐圧 $V_B$\n（ドリフト層 $W$，$N_d$）",
     "オン抵抗 $R_{\\mathrm{on}}$", "スイッチング時間\n$t_{\\mathrm{on}}$，$t_{\\mathrm{off}}$"]
R = ["確実なオフ状態", "扱える電圧", "導通損失", "スイッチング損失・\n高周波化"]

for cy, tl, tm, tr in zip(RY, L, M, R):
    box(CX[0], cy, tl, C_L)
    box(CX[1], cy, tm, C_M)
    box(CX[2], cy, tr, C_R)
    for x0, x1 in [(CX[0] + W / 2 + 0.06, CX[1] - W / 2 - 0.06),
                   (CX[1] + W / 2 + 0.06, CX[2] - W / 2 - 0.06)]:
        ax.annotate("", xy=(x1, cy), xytext=(x0, cy),
                    arrowprops=dict(arrowstyle="-|>", lw=0.9, color="#666"))

# E_g → E_c（左列内の因果，3.1節）
ax.annotate("", xy=(CX[0] - 1.62, 3.45), xytext=(CX[0] - 1.62, 4.55),
            arrowprops=dict(arrowstyle="-|>", lw=0.9, color=BLUE, ls="--",
                            connectionstyle="arc3,rad=0.35"))

# 耐圧⇔オン抵抗のトレードオフ（中央列，3.2節）
ax.annotate("", xy=(CX[1], 2.35 + H / 2 + 0.05), xytext=(CX[1], 3.45 - H / 2 - 0.05),
            arrowprops=dict(arrowstyle="<|-|>", lw=1.2, color=RED))
ax.text(CX[1] + 0.28, 2.90, "$W$，$N_d$ を共有\n（トレードオフ，3.2節）",
        fontsize=6.4, fontproperties=JP, color=RED, va="center")

ax.set_xlim(-0.35, 10.1)
ax.set_ylim(0.65, 5.75)
ax.axis("off")
fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig3.1.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
fig.savefig("/tmp/claude-1000/-home-soumajinno/e7688596-6b6f-45e4-950d-929e196c5bb6/scratchpad/fig3.1.png",
            dpi=180, bbox_inches="tight")
print("wrote", EPS)
