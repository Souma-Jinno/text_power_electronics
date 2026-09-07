#!/usr/bin/env python3
# fig5.2（第5章）: 降圧チョッパの定常状態波形（v_L, i_L, i_C）。
# ボルト秒平衡（正負の面積が等しい）とリプル電流の定義を示す。
# 波形は配布モデル ltspice/chapter05/buck_chopper.net（V_in=10 V, D=0.5,
# f=1 kHz, L=30 mH, C=100 uF, R=10 Ω，ダイオードはほぼ理想）を ngspice で解いた結果そのもの。
# 定常状態に達した 19〜21 ms（2周期）を切り出し，切り出しの先頭を t=0 として描く
# （fig5.4・fig5.7 と同じ流儀）。解析時間はネットリストの .tran（22 ms）と同じ。
import os
import shutil
import subprocess
import sys
import tempfile
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BK = "#222222"
BLUE = "#2a5db0"
RED = "#c0392b"
SHADE = "#eef3fb"

NET = os.path.expanduser(
    "~/text_power_electronics/book/figures/ltspice/chapter05/buck_chopper.net")
W0, W1 = 19.0, 21.0   # 切り出し区間 [ms]（定常状態の2周期）
T0, T1 = 0.0, W1 - W0  # 描画の時間軸 [ms]（切り出しの先頭を 0 とする）
TSW, DUTY = 1.0, 0.5  # 周期 [ms]，デューティ比（ネットリストと同じ値）


def run_ngspice():
    """buck_chopper.net を ngspice で過渡解析し，(t[ms], vL, iL, iC, vout) を返す。"""
    exe = shutil.which("ngspice") or os.path.expanduser("~/miniforge3/bin/ngspice")
    if not os.path.isfile(exe):
        sys.exit("error: ngspice が見つかりません（PATH か ~/miniforge3/bin に置いてください）")
    if not os.path.isfile(NET):
        sys.exit(f"error: ネットリストがありません: {NET}")
    with open(NET) as f:
        cards = [ln for ln in f
                 if not ln.lower().startswith((".tran", ".end"))]
    deck = "".join(cards) + """
.control
set filetype=ascii
save all @l1[i] @c1[i]
tran 200n 22m
let iL = @l1[i]
let iC = @c1[i]
let vL = v(N002)-v(N003)
linearize iL iC vL v(N003) v(N002)
wrdata buck.txt vL iL iC v(N003) v(N002)
.endc
.end
"""
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "buck.cir"), "w") as f:
            f.write(deck)
        r = subprocess.run([exe, "-b", "buck.cir"], cwd=d,
                           capture_output=True, text=True)
        out = os.path.join(d, "buck.txt")
        if r.returncode != 0 or not os.path.isfile(out):
            sys.exit("error: ngspice の実行に失敗しました\n" + r.stdout + r.stderr)
        data = np.loadtxt(out)  # wrdata: (時刻, 値) の対が列に並ぶ
    t = data[:, 0] * 1e3
    return t, data[:, 1], data[:, 3], data[:, 5], data[:, 7]


t, vL, iL, iC, vout = run_ngspice()
m = (t >= W0) & (t <= W1)
t, vL, iL, iC, vout = t[m] - W0, vL[m], iL[m], iC[m], vout[m]
Iout = iL.mean()
print(f"Vout={vout.mean():.3f} V  Iout={Iout:.3f} A  "
      f"dIL={iL.max() - iL.min():.4f} A  vL=({vL.min():.2f},{vL.max():.2f}) V")

XL, XR = T0 - 0.55, T1 + 0.60  # 描画範囲 [ms]（左右に注記の余白）
TON = [(T0 + k * TSW, DUTY * TSW) for k in range(2)]  # オン期間


def setup(ax, ymin, ymax, yticks, label, xaxis_at_zero=True):
    """矢印付きの手描き軸。x軸は 0（または ymin）の高さに置く。"""
    dy = ymax - ymin
    y0 = 0.0 if xaxis_at_zero else ymin
    for x, w in TON:
        ax.add_patch(Rectangle((x, ymin), w, dy, fc=SHADE, ec="none", zorder=0))
    ax.annotate("", xy=(T1 + 0.22, y0), xytext=(T0 - 0.02, y0),
                arrowprops=dict(arrowstyle="-|>", lw=0.8, color=BK,
                                mutation_scale=8))
    ax.plot([T0, T0], [ymin, ymax], color=BK, lw=0.8)
    for x in np.arange(T0, T1 + 1e-9, 0.5):
        ax.plot([x, x], [y0 - 0.02 * dy, y0 + 0.02 * dy], color=BK, lw=0.7)
        ax.text(x, ymin - 0.11 * dy, f"{x:g}", ha="center", va="top",
                fontsize=6.2)
    ax.text(T1 + 0.24, y0 - 0.06 * dy, "$t$ [ms]", ha="left", va="top",
            fontsize=6.6)
    for y in yticks:
        ax.plot([T0 - 0.02, T0 + 0.02], [y, y], color=BK, lw=0.7)
        ax.text(T0 - 0.05, y, f"{y:g}", ha="right", va="center", fontsize=6.2)
    ax.text(T0 - 0.03, ymax + 0.21 * dy, label, ha="right", va="center",
            fontsize=7.4, color=BLUE)
    ax.set_xlim(XL, XR)
    ax.set_ylim(ymin - 0.36 * dy, ymax + 0.18 * dy)
    ax.axis("off")


fig, axes = plt.subplots(3, 1, figsize=(4.25, 3.3))

# --- (1) v_L：正負の面積が等しい（ボルト秒平衡）
ax = axes[0]
setup(ax, -6.5, 6.5, [-5, 0, 5], "$v_L$ [V]")
ax.plot(t, vL, color=BLUE, lw=1.1, zorder=3)
# 1周期目のオン区間（正）とオフ区間（負）にハッチ
on = (t >= T0) & (t <= T0 + DUTY * TSW)
off = (t >= T0 + DUTY * TSW) & (t <= T0 + TSW)
ax.fill_between(t[on], 0, vL[on], fc="none", ec=BLUE, hatch="////",
                lw=0, alpha=0.45, zorder=1)
ax.fill_between(t[off], 0, vL[off], fc="none", ec=RED, hatch="\\\\\\\\",
                lw=0, alpha=0.45, zorder=1)
# ラベルはハッチに重ねない（斜線と文字が干渉して読めない）。
# 1周期目のオフ区間は波形が負側にいるので，その真上が空いている（2026-09-08）。
# 中央を 0.75T に置くと文字の左端が青ハッチの右辺（0.5T）に接するので，少し右へ寄せる。
ax.text(T0 + 0.80 * TSW, 2.6, "面積が等しい", fontsize=6.2, fontproperties=JP,
        color="#555", ha="center", va="center", zorder=4)
vp, vn = vL[on].mean(), vL[off].mean()
ax.plot([T0, T1 + 0.05], [vp] * 2, color="#999", lw=0.5, ls=":", zorder=1)
ax.plot([T0, T1 + 0.05], [vn] * 2, color="#999", lw=0.5, ls=":", zorder=1)
ax.text(T1 + 0.08, vp, r"$V_{\mathrm{in}}-V_{\mathrm{out}}$", ha="left",
        va="center", fontsize=6.4)
ax.text(T1 + 0.08, vn, r"$-V_{\mathrm{out}}$", ha="left",
        va="center", fontsize=6.4)
for k, s in [(0, "オン"), (1, "オフ")]:
    ax.text(T0 + (k + 0.5) * DUTY * TSW, 8.2, s, ha="center", fontsize=6.2,
            fontproperties=JP, color="#555")

# --- (2) i_L：平均値 I_out のまわりの三角波，リプル ΔI_L
ax = axes[1]
setup(ax, 0.45, 0.55, [0.45, 0.50, 0.55], "$i_L$ [A]",
      xaxis_at_zero=False)
ax.plot(t, iL, color=BLUE, lw=1.1, zorder=3)
ax.plot([T0, T1], [Iout] * 2, color=RED, lw=0.8, ls="--", zorder=2)
ax.text(T0 + TSW, Iout + 0.006, r"$I_{\mathrm{out}}$", ha="center",
        va="bottom", fontsize=6.6, color=RED)
imax, imin = iL.max(), iL.min()
xd = T1 + 0.12
ax.annotate("", xy=(xd, imax), xytext=(xd, imin),
            arrowprops=dict(arrowstyle="<->", lw=0.9, color=BK,
                            mutation_scale=7))
ax.plot([T1 - DUTY * TSW, xd + 0.04], [imax] * 2, color="#999", lw=0.5, ls=":")
ax.plot([T1 - 0.02, xd + 0.04], [imin] * 2, color="#999", lw=0.5, ls=":")
ax.text(xd + 0.05, 0.5 * (imax + imin), r"$\Delta I_L$", ha="left",
        va="center", fontsize=7.0)

# --- (3) i_C：i_L から平均を除いた成分（平均 0）
ax = axes[2]
setup(ax, -0.06, 0.06, [-0.05, 0, 0.05], "$i_C$ [A]")
ax.plot(t, iC, color=BLUE, lw=1.1, zorder=3)
ax.text(T0 + 0.05, -0.098, r"$i_C=i_L-I_{\mathrm{out}}$（平均は0）",
        ha="left", va="top", fontsize=6.2, fontproperties=JP, color="#555")

fig.subplots_adjust(hspace=0.62)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig5.2.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
