#!/usr/bin/env python3
# fig4.1（第4章）: インダクタの積分作用。(a)正の電圧をかけ続けると電流は増え続ける。
# (b)正負の面積（ボルト秒）が等しいとき，電流は三角波の定常状態に落ち着く。
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

fig, axes = plt.subplots(2, 2, figsize=(4.25, 2.5), sharex="col")

V0 = 1.0
D = 0.4
VN = -D / (1 - D) * V0  # 負側の電圧（面積が釣り合う値）

# ---------- (a) 正の電圧のみ ----------
ax = axes[0, 0]
ax.plot([0, 3], [V0, V0], color=RED, lw=1.4)
ax.axhline(0, color="#888", lw=0.6)
ax.fill_between([0, 3], 0, V0, color="#f7dfdb", lw=0, zorder=0)
ax.set_ylim(-1.0, 1.5)
ax.set_yticks([0, V0])
ax.set_yticklabels(["$0$", "$V_0$"], fontsize=7)
ax.set_ylabel("$v_L$", fontsize=8)
ax.set_xticks([])
ax.text(1.5, 1.18, "正の電圧だけ", ha="center", fontsize=7.2,
        fontproperties=JP, color=RED)

ax = axes[1, 0]
t = np.array([0, 3])
ax.plot(t, t * V0, color=BLUE, lw=1.4)
ax.axhline(0, color="#888", lw=0.6)
ax.set_ylim(-0.4, 3.4)
ax.set_yticks([0])
ax.set_yticklabels(["$0$"], fontsize=7)
ax.set_ylabel("$i_L$", fontsize=8)
ax.set_xticks([0, 1, 2, 3])
ax.set_xticklabels(["$0$", "$T$", "$2T$", "$3T$"], fontsize=7)
ax.text(1.75, 2.6, "傾き $V_0/L$ で\n増え続ける", ha="center", fontsize=7.2,
        fontproperties=JP, color=BLUE)
ax.text(1.5, -1.75, "(a) 正の電圧をかけ続けた場合", ha="center", fontsize=7.4,
        fontproperties=JP, color="#555", transform=ax.transData, clip_on=False)

# ---------- (b) 正負を交互 ----------
ax = axes[0, 1]
tv, vv = [], []
for k in range(3):
    tv += [k, k + D, k + D, k + 1]
    vv += [V0, V0, VN, VN]
# ステップ描画
tt, vs = [], []
for k in range(3):
    tt += [k, k + D]
    vs += [V0, V0]
    tt += [k + D, k + 1]
    vs += [VN, VN]
ax.plot([0, 0], [VN, V0], color=RED, lw=1.0)
for k in range(3):
    ax.plot([k, k + D], [V0, V0], color=RED, lw=1.4)
    ax.plot([k + D, k + D], [V0, VN], color=RED, lw=1.0)
    ax.plot([k + D, k + 1], [VN, VN], color=RED, lw=1.4)
    if k < 2:
        ax.plot([k + 1, k + 1], [VN, V0], color=RED, lw=1.0)
    ax.fill_between([k, k + D], 0, V0, color="#f7dfdb", lw=0, zorder=0)
    ax.fill_between([k + D, k + 1], VN, 0, color="#dde7f7", lw=0, zorder=0)
ax.axhline(0, color="#888", lw=0.6)
ax.set_ylim(-1.0, 1.5)
ax.set_yticks([VN, 0, V0])
ax.set_yticklabels(["$-V_1$", "$0$", "$V_0$"], fontsize=7)
ax.set_xticks([])
ax.text(0.2, 1.16, "I", ha="center", fontsize=7.6, color=RED)
ax.text(0.72, -0.45, "II", ha="center", va="center", fontsize=7.6, color=BLUE)
ax.text(2.0, 1.18, "面積 I ＝ 面積 II", ha="center", fontsize=7.2,
        fontproperties=JP, color="#333")

ax = axes[1, 1]
i0 = 0.3
ti = [0]
ii = [i0]
for k in range(3):
    ti += [k + D, k + 1]
    ii += [i0 + D * V0, i0]
ax.plot(ti, ii, color=BLUE, lw=1.4)
ax.axhline(0, color="#888", lw=0.6)
ax.axhline(i0 + D * V0 / 2, color=BLUE, lw=0.7, ls="--")
ax.text(3.02, i0 + D * V0 / 2, "平均", fontsize=6.8, fontproperties=JP,
        color=BLUE, va="center")
ax.set_ylim(-0.4, 3.4 * (0.75 / 3.4) * 3.4)  # 同縮尺にせず見やすく
ax.set_ylim(-0.15, 1.05)
ax.set_yticks([0])
ax.set_yticklabels(["$0$"], fontsize=7)
ax.set_xticks([0, D, 1, 2, 3])
ax.set_xticklabels(["$0$", "$DT$", "$T$", "$2T$", "$3T$"], fontsize=7)
ax.text(1.5, -0.62, "(b) 正負の面積が等しい場合（定常状態）", ha="center",
        fontsize=7.4, fontproperties=JP, color="#555",
        transform=ax.transData, clip_on=False)

for ax in axes.flat:
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

fig.tight_layout(h_pad=0.6, w_pad=1.2)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig4.1.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
