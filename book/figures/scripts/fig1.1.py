#!/usr/bin/env python3
# fig1.1（第1章）: 導体・半導体・絶縁体のバンド構造の比較。
# バンドギャップの大小が電気の流れやすさを決める（半導体はその中間）。
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
VB = "#f2c48c"   # 価電子帯
CB = "#fdf0c8"   # 伝導帯

fig, ax = plt.subplots(figsize=(4.4, 2.5))

W = 1.7          # バンドの幅
panels = [
    ("導体（金属）", 0.0),
    ("半導体", 2.7),
    ("絶縁体", 5.4),
]

def band(x0, y0, h, color, hatch=None):
    r = Rectangle((x0, y0), W, h, fc=color, ec="#555", lw=0.8)
    ax.add_patch(r)
    return r

# --- 導体: 伝導帯に電子が入っている（バンドが重なる/部分的に満ちる）
x0 = panels[0][1]
band(x0, 0.0, 1.1, VB)
band(x0, 0.9, 1.1, CB)   # 重なり
for i in range(4):
    ax.plot(x0 + 0.3 + 0.37 * i, 1.05, "o", ms=3.2, color=BLUE)
ax.text(x0 + W / 2, 1.55, "動ける電子", ha="center", fontsize=7.2,
        fontproperties=JP, color=BLUE)
ax.text(x0 + W / 2, 0.4, "価電子帯", ha="center", va="center",
        fontsize=7.2, fontproperties=JP, color="#7a5a2a")
ax.text(x0 + W / 2, -0.45, "バンドが重なる\n（すき間なし）", ha="center",
        fontsize=7.2, fontproperties=JP, color="#555")

# --- 半導体: 小さいギャップ。熱でわずかに励起
x0 = panels[1][1]
band(x0, 0.0, 1.0, VB)
band(x0, 1.7, 1.0, CB)
ax.annotate("", xy=(x0 + W + 0.18, 1.7), xytext=(x0 + W + 0.18, 1.0),
            arrowprops=dict(arrowstyle="<->", lw=0.9, color=RED))
ax.text(x0 + W + 0.28, 1.35, r"$E_g\approx$1 eV", fontsize=7.6, color=RED, va="center")
ax.plot(x0 + 0.55, 1.85, "o", ms=3.2, color=BLUE)
ax.plot(x0 + 0.55, 0.82, "o", ms=3.6, mfc="white", mec=RED, mew=0.9)
ax.annotate("", xy=(x0 + 0.55, 1.78), xytext=(x0 + 0.55, 0.95),
            arrowprops=dict(arrowstyle="-|>", lw=0.9, color=BLUE, ls="--"))
ax.text(x0 + W / 2, -0.45, "熱でわずかに\n電子が飛び移れる", ha="center",
        fontsize=7.2, fontproperties=JP, color="#555")

# --- 絶縁体: 大きいギャップ
x0 = panels[2][1]
band(x0, 0.0, 1.0, VB)
band(x0, 2.6, 1.0, CB)
ax.annotate("", xy=(x0 + W + 0.18, 2.6), xytext=(x0 + W + 0.18, 1.0),
            arrowprops=dict(arrowstyle="<->", lw=0.9, color=RED))
ax.text(x0 + W + 0.28, 1.8, r"$E_g\gtrsim$5 eV", fontsize=7.6, color=RED, va="center")
ax.text(x0 + W / 2, -0.45, "ギャップが広く\n電子は飛び移れない", ha="center",
        fontsize=7.2, fontproperties=JP, color="#555")

# 共通ラベル
for name, x0 in panels:
    ax.text(x0 + W / 2, 3.85, name, ha="center", fontsize=8.4, fontproperties=JP)
    if x0 > 0:
        ax.text(x0 + W / 2, 0.5, "価電子帯", ha="center", va="center",
                fontsize=7.2, fontproperties=JP, color="#7a5a2a")
ax.text(panels[1][1] + W / 2, 2.2, "伝導帯", ha="center", va="center",
        fontsize=7.2, fontproperties=JP, color="#7a5a2a")
ax.text(panels[2][1] + W / 2, 3.1, "伝導帯", ha="center", va="center",
        fontsize=7.2, fontproperties=JP, color="#7a5a2a")

# エネルギー軸
ax.annotate("", xy=(-1.05, 3.6), xytext=(-1.05, 0.0),
            arrowprops=dict(arrowstyle="-|>", lw=0.9, color="#777"))
ax.text(-1.25, 1.8, "電子のエネルギー", rotation=90, va="center", ha="center",
        fontsize=7.6, fontproperties=JP, color="#555")

ax.set_xlim(-1.5, 8.1)
ax.set_ylim(-1.1, 4.2)
ax.axis("off")
fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig1.1.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
