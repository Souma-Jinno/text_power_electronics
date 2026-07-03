#!/usr/bin/env python3
# fig10.4（第10章）: サイクロコンバータの出力合成のイメージ。
# 三相サイリスタブリッジの点弧角αを周期ごとに変えると，区分的な線間電圧の
# つぎはぎの「平均」が低い周波数の正弦波を描く（正群ブリッジ・電流正の期間）。
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
GY = "#b5b5b5"

V0 = 1.0
M = 0.9            # 出力振幅の指令（変調率）
FDIV = 6           # 出力周波数 = 入力周波数 / FDIV
THMAX = FDIV * 2 * np.pi  # 出力1周期分


def alpha_k(theta_mid):
    """区間中央の位相で目標平均電圧に合わせた点弧角を返す"""
    target = M * np.sin(theta_mid / FDIV)
    return np.arccos(np.clip(target, -1, 1))


# --- 区分的な出力波形を合成する
xs, ys = [], []
k = 0
fire_prev = None
while True:
    th_nom = np.pi / 3 + k * np.pi / 3          # α=0での転流点
    th_mid = th_nom + np.pi / 6
    ak = alpha_k(th_mid)
    fire = th_nom + ak                           # 実際の点弧点
    if fire_prev is not None:
        # 前の区間の導通を今回の点弧まで延長
        seg = np.linspace(fire_prev, fire, 40)
        xs.append(seg)
        ys.append(V0 * np.sin(seg - (k - 1) * np.pi / 3))
    fire_prev = fire
    k += 1
    if fire > THMAX:
        break

xs = np.concatenate(xs)
ys = np.concatenate(ys)
mask = xs <= THMAX
xs, ys = xs[mask], ys[mask]

fig, ax = plt.subplots(figsize=(4.25, 1.85))

# 入力の線間電圧群（薄いグレー）
tt = np.linspace(0, THMAX, 4000)
for j in range(6):
    ax.plot(tt, V0 * np.sin(tt - j * np.pi / 3), color="#cccccc", lw=0.4,
            zorder=1)

# 合成された出力電圧（青）と目標の平均電圧（赤破線）
ax.plot(xs, ys, color=BLUE, lw=1.0, zorder=3)
ax.plot(tt, (3 / np.pi) * V0 * M * np.sin(tt / FDIV), color=RED, lw=1.1,
        ls="--", zorder=4)

# 軸
ax.annotate("", xy=(THMAX * 1.04, 0), xytext=(-0.8, 0),
            arrowprops=dict(arrowstyle="-|>", lw=0.8, color=BK,
                            mutation_scale=8))
ax.plot([0, 0], [-1.15, 1.15], color=BK, lw=0.8)
ax.text(THMAX * 1.045, -0.18, r"$t$", fontsize=7.5, va="top")
ax.text(-1.2, 1.05, r"$v$", fontsize=8)
ax.text(THMAX * 0.30, 1.22, "ブリッジの出力電圧", fontsize=6.6,
        fontproperties=JP, color=BLUE)
ax.text(THMAX * 0.72, 1.22, "その平均（低周波の交流）", fontsize=6.6,
        fontproperties=JP, color=RED)
ax.text(THMAX * 0.5, -1.5, "入力の線間電圧（灰色）から点弧角を変えながら切り出す",
        fontsize=6.4, fontproperties=JP, color="#555", ha="center")

ax.set_xlim(-1.6, THMAX * 1.1)
ax.set_ylim(-1.65, 1.45)
ax.axis("off")

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig10.4.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
