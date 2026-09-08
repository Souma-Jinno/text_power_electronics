#!/usr/bin/env python3
# fig5.6（第5章）: 昇圧コンバータの定常状態波形（v_L, i_L, i_D）。
# オフ期間だけダイオードを通して出力へエネルギーが送られることを示す。
# 波形は配布モデル ltspice/chapter05/boost_chopper.net（V_in=5 V, D=0.583,
# f=20 kHz, L=700 uH, C=500 uF, R=28.8 Ω，ダイオードはほぼ理想）を ngspice で解いた結果そのもの。
# 定常状態に達した 200.0〜200.1 ms（2周期）を切り出し，切り出しの先頭を t=0 として描く。
# 理論値: V_out = V_in/(1-D) = 12.0 V, I_in = I_out/(1-D) = 1.00 A,
#         ΔI_L = V_in D/(f L) = 0.208 A, I_out = 0.416 A
# 注意: インダクタ電流は i(L1) では取れないので @l1[i] を使う。
#       ダイオード電流 @d1[id] はスイッチ切替えの瞬間に数値的なスパイクを含むため，
#       出力ノードのキルヒホッフの電流則 i_D = i_C + i_R（@c1[i] + @r1[i]）で求める。
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
    "~/text_power_electronics/book/figures/ltspice/chapter05/boost_chopper.net")
T0, T1 = 200.0, 200.1   # 表示区間 [ms]（定常状態の2周期）
TSW, DUTY = 50.0, 0.583  # 周期 [us]，デューティ比（ネットリストと同じ値）


def run_ngspice():
    """boost_chopper.net を ngspice で過渡解析し，(t[ms], vL, iL, iD, vout) を返す。"""
    exe = shutil.which("ngspice") or os.path.expanduser("~/miniforge3/bin/ngspice")
    if not os.path.isfile(exe):
        sys.exit("error: ngspice が見つかりません（PATH か ~/miniforge3/bin に置いてください）")
    if not os.path.isfile(NET):
        sys.exit(f"error: ネットリストがありません: {NET}")
    with open(NET) as f:
        cards = [ln for ln in f
                 if not ln.lower().startswith((".tran", ".end"))]
    # 終了時刻はスイッチの切替え時刻（50 us の整数倍）を避ける（ngspice が最後の
    # 1点で "timestep too small" を出して止まるため）。
    deck = "".join(cards) + """
.control
set filetype=ascii
save all @l1[i] @c1[i] @r1[i]
tran 100n 200.13m 199.9m
let iL = @l1[i]
let iD = @c1[i] + @r1[i]
let vL = v(N001)-v(N002)
linearize iL iD vL v(N003)
wrdata boost.txt vL iL iD v(N003)
.endc
.end
"""
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "boost.cir"), "w") as f:
            f.write(deck)
        r = subprocess.run([exe, "-b", "boost.cir"], cwd=d,
                           capture_output=True, text=True)
        out = os.path.join(d, "boost.txt")
        if r.returncode != 0 or not os.path.isfile(out):
            sys.exit("error: ngspice の実行に失敗しました\n" + r.stdout + r.stderr)
        data = np.loadtxt(out)  # wrdata: (時刻, 値) の対が列に並ぶ
    t = data[:, 0] * 1e3
    return t, data[:, 1], data[:, 3], data[:, 5], data[:, 7]


t, vL, iL, iD, vout = run_ngspice()
m = (t >= T0) & (t <= T1)
t, vL, iL, iD, vout = t[m], vL[m], iL[m], iD[m], vout[m]
t = (t - T0) * 1e3  # 切り出しの先頭を 0 とした時刻 [us]
Iin = iL.mean()
Iout = iD.mean()
print(f"Vout={vout.mean():.3f} V  Iin={Iin:.4f} A  Iout={Iout:.4f} A  "
      f"dIL={iL.max() - iL.min():.4f} A  vL=({vL.min():.3f},{vL.max():.3f}) V")

TMAX = 2 * TSW
XL, XR = -0.30 * TMAX, 1.32 * TMAX  # 描画範囲 [us]（左右に注記の余白）
TON = [(k * TSW, DUTY * TSW) for k in range(2)]  # オン期間


def setup(ax, ymin, ymax, yticks, label, xaxis_at_zero=True):
    """矢印付きの手描き軸。x軸は 0（または ymin）の高さに置く。"""
    dy = ymax - ymin
    y0 = 0.0 if xaxis_at_zero else ymin
    for x, w in TON:
        ax.add_patch(Rectangle((x, ymin), w, dy, fc=SHADE, ec="none", zorder=0))
    ax.annotate("", xy=(TMAX + 0.11 * TMAX, y0), xytext=(-0.01 * TMAX, y0),
                arrowprops=dict(arrowstyle="-|>", lw=0.8, color=BK,
                                mutation_scale=8))
    ax.plot([0, 0], [ymin, ymax], color=BK, lw=0.8)
    for x in np.arange(0, TMAX + 1e-9, 25):
        ax.plot([x, x], [y0 - 0.02 * dy, y0 + 0.02 * dy], color=BK, lw=0.7)
        ax.text(x, ymin - 0.11 * dy, f"{x:g}", ha="center", va="top",
                fontsize=6.2)
    ax.text(TMAX + 0.12 * TMAX, y0 - 0.06 * dy, r"$t$ [$\mathrm{\mu}$s]", ha="left",
            va="top", fontsize=6.6)
    for y in yticks:
        ax.plot([-0.01 * TMAX, 0.01 * TMAX], [y, y], color=BK, lw=0.7)
        ax.text(-0.025 * TMAX, y, f"{y:g}", ha="right", va="center", fontsize=6.2)
    ax.text(-0.015 * TMAX, ymax + 0.21 * dy, label, ha="right", va="center",
            fontsize=7.4, color=BLUE)
    ax.set_xlim(XL, XR)
    ax.set_ylim(ymin - 0.36 * dy, ymax + 0.18 * dy)
    ax.axis("off")


fig, axes = plt.subplots(3, 1, figsize=(4.25, 3.3))

# --- (1) v_L：オン期間は +V_in，オフ期間は V_in - V_out（負）
ax = axes[0]
setup(ax, -8.5, 6.5, [-7, 0, 5], "$v_L$ [V]")
ax.plot(t, vL, color=BLUE, lw=1.1, zorder=3)
on = (t >= 0) & (t <= DUTY * TSW)
off = (t >= DUTY * TSW) & (t <= TSW)
vp, vn = vL[on].mean(), vL[off].mean()
ax.plot([0, TMAX + 0.02 * TMAX], [vp] * 2, color="#999", lw=0.5, ls=":", zorder=1)
ax.plot([0, TMAX + 0.02 * TMAX], [vn] * 2, color="#999", lw=0.5, ls=":", zorder=1)
ax.text(TMAX + 0.04 * TMAX, vp, r"$V_{\mathrm{in}}$", ha="left",
        va="center", fontsize=6.4)
ax.text(TMAX + 0.04 * TMAX, vn, r"$V_{\mathrm{in}}-V_{\mathrm{out}}$", ha="left",
        va="center", fontsize=6.4)
for k, s in [(0, "オン"), (1, "オフ")]:
    x = 0.5 * DUTY * TSW if k == 0 else 0.5 * (1 + DUTY) * TSW
    ax.text(x, 8.6, s, ha="center", fontsize=6.2,
            fontproperties=JP, color="#555")

# --- (2) i_L：平均値は入力電流 I_in，リプル ΔI_L
ax = axes[1]
setup(ax, 0.85, 1.15, [0.9, 1.0, 1.1], "$i_L$ [A]", xaxis_at_zero=False)
ax.plot(t, iL, color=BLUE, lw=1.1, zorder=3)
ax.plot([0, TMAX], [Iin] * 2, color=RED, lw=0.8, ls="--", zorder=2)
ax.text(TSW, Iin + 0.018, r"$I_{\mathrm{in}}$", ha="center",
        va="bottom", fontsize=6.6, color=RED)
imax, imin = iL.max(), iL.min()
xd = TMAX + 0.06 * TMAX
ax.annotate("", xy=(xd, imax), xytext=(xd, imin),
            arrowprops=dict(arrowstyle="<->", lw=0.9, color=BK,
                            mutation_scale=7))
ax.plot([TSW + DUTY * TSW, xd + 0.02 * TMAX], [imax] * 2, color="#999", lw=0.5, ls=":")
ax.plot([TMAX - 0.01 * TMAX, xd + 0.02 * TMAX], [imin] * 2, color="#999", lw=0.5, ls=":")
ax.text(xd + 0.025 * TMAX, 0.5 * (imax + imin), r"$\Delta I_L$", ha="left",
        va="center", fontsize=7.0)

# --- (3) i_D：オフ期間だけ i_L が流れ，その平均が負荷電流 I_out
ax = axes[2]
setup(ax, 0, 1.25, [0, 0.5, 1.0], r"$i_{\mathrm{D}}$ [A]")
ax.plot(t, iD, color=BLUE, lw=1.1, zorder=3)
ax.plot([0, TMAX], [Iout] * 2, color=RED, lw=0.8, ls="--", zorder=2)
ax.text(TMAX + 0.04 * TMAX, Iout, r"$I_{\mathrm{out}}$", ha="left",
        va="center", fontsize=6.6, color=RED)
ax.text(0.02 * TMAX, -0.50, "平均が負荷電流になる", ha="left", va="top",
        fontsize=6.2, fontproperties=JP, color="#555")

fig.subplots_adjust(hspace=0.62)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig5.6.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
