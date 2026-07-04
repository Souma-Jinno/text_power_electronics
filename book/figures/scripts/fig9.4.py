#!/usr/bin/env python3
# fig9.4（第9章）: 方形波のフーリエ分解。
# (a)基本波(1次)・3次・5次を足し合わせると方形波に近づく様子，
# (b)高調波の振幅スペクトル 4E/(nπ)（奇数次のみ）。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BK = "#222222"
RED = "#c0392b"
BLUE = "#2a5db0"
GRN = "#2e8b57"
ORG = "#e08a1e"

wt = np.linspace(0, 2 * np.pi, 2001)


def sq(x):
    return np.where(np.mod(x, 2 * np.pi) < np.pi, 1.0, -1.0)


def partial(x, N):
    y = np.zeros_like(x)
    for n in range(1, N + 1, 2):
        y += (4 / np.pi) * np.sin(n * x) / n
    return y


fig = plt.figure(figsize=(4.3, 2.3))
gs = fig.add_gridspec(1, 2, width_ratios=[1.3, 1.0], wspace=0.30)

# (a) 足し合わせ
ax = fig.add_subplot(gs[0, 0])
ax.axhline(0, color=BK, lw=0.7)
ax.plot(wt, sq(wt), color="#999", lw=1.0, ls="-", label="方形波", zorder=1)
ax.plot(wt, partial(wt, 1), color=BLUE, lw=1.2, label="1次のみ", zorder=3)
ax.plot(wt, partial(wt, 3), color=GRN, lw=1.2, label="1+3次", zorder=3)
ax.plot(wt, partial(wt, 5), color=RED, lw=1.2, label="1+3+5次", zorder=3)
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1.5, 1.5)
ax.set_xticks([0, np.pi, 2 * np.pi])
ax.set_xticklabels(["0", r"$\pi$", r"$2\pi$"], fontsize=6.6)
ax.set_yticks([-1, 0, 1])
ax.set_yticklabels(["$-E$", "0", "$E$"], fontsize=6.6)
ax.set_xlabel(r"$\omega t$", fontsize=7.5)
ax.legend(prop=fm.FontProperties(fname=JP.get_file(), size=5.6),
          loc="lower center", ncol=2, frameon=False, handlelength=1.3,
          columnspacing=0.9, bbox_to_anchor=(0.5, -0.02))
ax.set_title("(a) 高調波の足し合わせ", fontproperties=JP, fontsize=7.2, color="#555")
for sp in ax.spines.values():
    sp.set_visible(False)

# (b) スペクトル
ax = fig.add_subplot(gs[0, 1])
ns = np.arange(1, 12)
amp = np.array([(4 / np.pi) / n if n % 2 == 1 else 0.0 for n in ns])
ax.bar(ns, amp, width=0.5, color=BLUE, zorder=3)
ax.axhline(0, color=BK, lw=0.7)
for n in [1, 3, 5]:
    ax.text(n, (4 / np.pi) / n + 0.05, r"$\frac{4E}{%d\pi}$" % n if n > 1
            else r"$\frac{4E}{\pi}$", ha="center", fontsize=6.0)
ax.set_xlim(0, 12)
ax.set_ylim(0, 1.55)
ax.set_xticks([1, 3, 5, 7, 9, 11])
ax.set_xticklabels(["1", "3", "5", "7", "9", "11"], fontsize=6.6)
ax.set_yticks([])
ax.set_xlabel("次数 $n$", fontproperties=JP, fontsize=6.8)
ax.set_title("(b) 振幅スペクトル", fontproperties=JP, fontsize=7.2, color="#555")
for sp in ["top", "right", "left"]:
    ax.spines[sp].set_visible(False)

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig9.4.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
