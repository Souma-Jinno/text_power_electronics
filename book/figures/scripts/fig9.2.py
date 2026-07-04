#!/usr/bin/env python3
# fig9.2（第9章）: フルブリッジ方形波インバータの出力電圧と負荷電流。
# (1)方形波電圧 v_R，(2)抵抗負荷の電流（同相の方形波），
# (3)誘導性(RL)負荷の電流（指数関数状，方形波電圧に対して遅れる）。
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BK = "#222222"
BLUE = "#2a5db0"
RED = "#c0392b"

T = 1.0
NP = 2
TMAX = NP * T
t = np.linspace(0, TMAX, 4001)


def sq(tt):
    return np.where(np.mod(tt, T) < T / 2, 1.0, -1.0)


def setup(ax, ymin, ymax, label, lc=BK):
    ax.axhline(0, color=BK, lw=0.7)
    ax.annotate("", xy=(1.12 * TMAX, 0), xytext=(-0.03 * TMAX, 0),
                arrowprops=dict(arrowstyle="-|>", lw=0.8, color=BK, mutation_scale=8))
    for x, s in [(T / 2, "$T/2$"), (T, "$T$"), (1.5 * T, r"$\frac{3T}{2}$"),
                 (2 * T, "$2T$")]:
        ax.plot([x, x], [ymin, ymax], color="#bbb", lw=0.5, ls=":", zorder=0)
        ax.text(x, ymin - 0.16 * (ymax - ymin), s, ha="center", va="top", fontsize=6.2)
    ax.text(1.13 * TMAX, -0.10 * (ymax - ymin), "$t$", fontsize=7)
    ax.text(-0.24 * TMAX, ymax, label, ha="right", va="center",
            fontsize=8.5, color=lc)
    ax.set_xlim(-0.28 * TMAX, 1.20 * TMAX)
    ax.set_ylim(ymin - 0.32 * (ymax - ymin), ymax + 0.20 * (ymax - ymin))
    ax.axis("off")


# RL負荷電流：区分的な指数（時定数tau），定常周期波形を数値的に作る
def rl_current(tau):
    dt = t[1] - t[0]
    i = np.zeros_like(t)
    v = sq(t)
    # 数周期回して定常に収束させる
    ic = 0.0
    for _ in range(6):
        ic_series = []
        for k in range(len(t)):
            ic += (v[k] - ic) * dt / tau
            ic_series.append(ic)
    # 最後の1巡を格納
    ic = 0.0
    for k in range(len(t)):
        ic += (v[k] - ic) * dt / tau
        i[k] = ic
    # もう一度定常化（初期値を末尾に合わせる）
    ic = i[-1]
    for k in range(len(t)):
        ic += (v[k] - ic) * dt / tau
        i[k] = ic
    return i


fig, axes = plt.subplots(3, 1, figsize=(4.0, 3.3))

ax = axes[0]
setup(ax, -1.0, 1.0, "$v_R$", RED)
ax.plot(t, sq(t), color=RED, lw=1.4, zorder=3)
ax.text(-0.02 * TMAX, 1.0, "$E$", ha="right", va="center", fontsize=6.8)
ax.text(-0.02 * TMAX, -1.0, "$-E$", ha="right", va="center", fontsize=6.8)

ax = axes[1]
setup(ax, -1.0, 1.0, "$i_R$", BLUE)
ax.plot(t, sq(t), color=BLUE, lw=1.4, zorder=3)
ax.text(-0.02 * TMAX, 1.0, r"$\frac{E}{R}$", ha="right", va="center", fontsize=6.8)
ax.text(1.35 * T, 1.25, "抵抗負荷（電圧と同相）", ha="center", fontsize=6.2,
        fontproperties=JP, color="#555")

ax = axes[2]
i = rl_current(0.22 * T)
i = i / np.max(np.abs(i))
setup(ax, -1.0, 1.0, "$i$", BLUE)
ax.plot(t, i, color=BLUE, lw=1.4, zorder=3)
ax.text(1.35 * T, 1.28, "誘導性(RL)負荷（指数関数状・電流が遅れる）",
        ha="center", fontsize=6.2, fontproperties=JP, color="#555")

fig.subplots_adjust(hspace=0.42)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig9.2.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
