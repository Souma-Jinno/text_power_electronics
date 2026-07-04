#!/usr/bin/env python3
# fig7.2（第7章）: 12 V→5 V・1 A の降圧を，リニアレギュレータと降圧チョッパで
# 行ったときの電力の内訳。出力5 Wは同じでも，リニアは差分7 Wをすべて熱で捨てる
# （η=42%）のに対し，チョッパは損失がわずか（η>90%）。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BLUE = "#2a5db0"
RED = "#c0392b"
BK = "#222222"

Pout = 5.0                      # 出力電力 [W]（5 V×1 A）
# リニア: 入力12 W，損失7 W
lin_out, lin_loss = Pout, 7.0
eta_lin = Pout / (Pout + 7.0)
# チョッパ: η=90% とすると入力≒5.56 W，損失≒0.56 W
eta_ch = 0.90
ch_in = Pout / eta_ch
ch_loss = ch_in - Pout

fig, ax = plt.subplots(figsize=(3.6, 2.4))

x = [0, 1]
w = 0.55
# 出力（下段・青）
ax.bar(x, [lin_out, Pout], w, color=BLUE, label="出力電力", zorder=2)
# 損失（上段・赤）
ax.bar(x, [lin_loss, ch_loss], w, bottom=[lin_out, Pout],
       color=RED, label="損失（発熱）", zorder=2)

# 数値ラベル
ax.text(0, lin_out / 2, "5 W", ha="center", va="center",
        fontsize=8, color="white")
ax.text(0, lin_out + lin_loss / 2, "7 W", ha="center", va="center",
        fontsize=8, color="white")
ax.text(1, Pout / 2, "5 W", ha="center", va="center",
        fontsize=8, color="white")
ax.text(0, lin_out + lin_loss + 0.35, r"$\eta=42\%$",
        ha="center", fontsize=8, color=BK)
ax.text(1, ch_in + 0.35, r"$\eta>90\%$", ha="center", fontsize=8, color=BK)

ax.set_xticks(x)
ax.set_xticklabels(["リニア\nレギュレータ", "降圧\nチョッパ"],
                   fontproperties=JP, fontsize=8)
ax.set_ylabel("入力電力 [W]", fontproperties=JP, fontsize=8.5)
ax.set_ylim(0, 13.5)
ax.tick_params(labelsize=7.5)
ax.legend(prop=fm.FontProperties(fname=JP.get_file(), size=7.5),
          loc="upper right", frameon=False)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_linewidth(0.6)

fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig7.2.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
