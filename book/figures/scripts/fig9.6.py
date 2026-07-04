#!/usr/bin/env python3
# fig9.6（第9章）: バイポーラ変調とユニポーラ変調の出力波形と高調波スペクトル比較。
# ユニポーラは実効スイッチング周波数が2倍になり，高調波が搬送波の2倍付近に移る。
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

mf = 21
m = 0.8
N = 24000
wt = np.linspace(0, 2 * np.pi, N, endpoint=False)
ref = m * np.sin(wt)
carr = 2 / np.pi * np.arcsin(np.sin(mf * wt))

# バイポーラ
v_bi = np.where(ref >= carr, 1.0, -1.0)
# ユニポーラ（レグA:ref, レグB:-ref）
gA = np.where(ref >= carr, 1.0, 0.0)
gB = np.where(-ref >= carr, 1.0, 0.0)
v_uni = gA - gB


def spectrum(v):
    F = np.fft.rfft(v) / (N / 2)
    mag = np.abs(F)
    mag[0] *= 0.5
    return mag / mag[1]  # 基本波で規格化


sp_bi = spectrum(v_bi)
sp_uni = spectrum(v_uni)

wt_plot = np.linspace(0, 2 * np.pi, N, endpoint=False)
fig = plt.figure(figsize=(4.3, 3.0))
gs = fig.add_gridspec(2, 2, hspace=0.55, wspace=0.28,
                      height_ratios=[1.0, 1.0])

# 出力波形（バイポーラ）
ax = fig.add_subplot(gs[0, 0])
ax.axhline(0, color=BK, lw=0.5)
ax.plot(wt_plot, v_bi, color=BLUE, lw=0.5)
ax.plot(wt_plot, m * np.sin(wt_plot), color=RED, lw=1.0, ls="--")
ax.set_ylim(-1.5, 1.5)
ax.set_xticks([])
ax.set_yticks([-1, 0, 1])
ax.set_yticklabels(["$-E$", "0", "$E$"], fontsize=5.6)
ax.set_title("バイポーラ 出力 $v$", fontproperties=JP, fontsize=6.8, color="#555")
for s in ax.spines.values():
    s.set_visible(False)

# 出力波形（ユニポーラ）
ax = fig.add_subplot(gs[0, 1])
ax.axhline(0, color=BK, lw=0.5)
ax.plot(wt_plot, v_uni, color=BLUE, lw=0.5)
ax.plot(wt_plot, m * np.sin(wt_plot), color=RED, lw=1.0, ls="--")
ax.set_ylim(-1.5, 1.5)
ax.set_xticks([])
ax.set_yticks([-1, 0, 1])
ax.set_yticklabels(["$-E$", "0", "$E$"], fontsize=5.6)
ax.set_title("ユニポーラ 出力 $v$", fontproperties=JP, fontsize=6.8, color="#555")
for s in ax.spines.values():
    s.set_visible(False)

# スペクトル（バイポーラ）
ax = fig.add_subplot(gs[1, 0])
n = np.arange(len(sp_bi))
ax.bar(n, sp_bi, width=0.9, color=BLUE)
ax.axvline(mf, color=RED, lw=0.7, ls=":")
ax.text(mf, 1.05, r"$m_f$", color=RED, fontsize=6.0, ha="center")
ax.set_xlim(0, 2.6 * mf)
ax.set_ylim(0, 1.15)
ax.set_xlabel("高調波次数", fontproperties=JP, fontsize=6.2)
ax.set_yticks([0, 1])
ax.tick_params(labelsize=5.6)
ax.set_title("高調波（基本波=1）", fontproperties=JP, fontsize=6.6, color="#555")

# スペクトル（ユニポーラ）
ax = fig.add_subplot(gs[1, 1])
ax.bar(n, sp_uni, width=0.9, color=BLUE)
ax.axvline(2 * mf, color=RED, lw=0.7, ls=":")
ax.text(2 * mf, 1.05, r"$2m_f$", color=RED, fontsize=6.0, ha="center")
ax.set_xlim(0, 2.6 * mf)
ax.set_ylim(0, 1.15)
ax.set_xlabel("高調波次数", fontproperties=JP, fontsize=6.2)
ax.set_yticks([0, 1])
ax.tick_params(labelsize=5.6)
ax.set_title("高調波が高周波側へ", fontproperties=JP, fontsize=6.6, color="#555")

EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig9.6.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
