#!/usr/bin/env python3
# fig5.8（第5章）: リプル電圧の発生。キャパシタ電流 i_C の正の面積が
# 電荷 ΔQ となり，出力電圧を ΔV だけ持ち上げる。
# 波形は配布モデル ltspice/chapter05/buck_chopper.net（V_in=10 V, D=0.5,
# f=1 kHz, L=30 mH, C=100 uF, R=10 Ω，ダイオードはほぼ理想）を ngspice で解いた結果そのもの。
# 定常状態に達した 19〜21 ms（2周期）を切り出し，切り出しの先頭を t=0 として描く
# （fig5.4・fig5.6・fig5.9 と同じ流儀）。解析時間はネットリストの .tran（22 ms）と同じ。
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
t, iC, vout = t[m] - W0, iC[m], vout[m]
Vout = vout.mean()
dV = vout.max() - vout.min()
print(f"Vout={Vout:.3f} V  dVout={dV * 1e3:.1f} mV  "
      f"iC=({iC.min():.4f},{iC.max():.4f}) A")

XL, XR = T0 - 0.55, T1 + 0.72  # 描画範囲 [ms]（左右に注記の余白）
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
    ax.set_ylim(ymin - 0.36 * dy, ymax + 0.20 * dy)
    ax.axis("off")


fig, axes = plt.subplots(2, 1, figsize=(4.25, 2.7))

# --- (1) i_C：正の半周期（ゼロ交差の間）の面積が ΔQ
ax = axes[0]
setup(ax, -0.06, 0.06, [-0.05, 0, 0.05], "$i_C$ [A]")
ax.plot(t, iC, color=BLUE, lw=1.1, zorder=3)
# 1周期目のゼロ交差（上向き→下向き）を実データから求める
zc = np.where(np.diff(np.sign(iC)) != 0)[0]
zc = zc[t[zc] < T0 + TSW]
t1, t2 = t[zc[0]], t[zc[1]]
pos = (t >= t1) & (t <= t2)
ax.fill_between(t[pos], 0, iC[pos], fc="#c5d5ef", ec=BLUE, hatch="////",
                lw=0, alpha=0.6, zorder=1)  # 斜線部 = ΔQ
ax.text(0.5 * (t1 + t2), 0.012, r"$\Delta Q$", ha="center", va="bottom",
        fontsize=7.4, color=BLUE, zorder=4,
        bbox=dict(fc="white", ec="none", alpha=0.85, pad=0.3))
yb = 0.052
ax.annotate("", xy=(t2, yb), xytext=(t1, yb),
            arrowprops=dict(arrowstyle="<->", lw=0.8, color=BK,
                            mutation_scale=7))
ax.text(0.5 * (t1 + t2), yb + 0.006, "$T/2$", ha="center", va="bottom",
        fontsize=6.6)
ax.plot([t1, t1], [0, yb], color="#999", lw=0.5, ls=":")
ax.plot([t2, t2], [0, yb], color="#999", lw=0.5, ls=":")
imax = iC.max()
ax.plot([T0 + DUTY * TSW, T1 + 0.05], [imax] * 2, color="#999", lw=0.5, ls=":")
ax.text(T1 + 0.08, imax, r"$\Delta I_L/2$", ha="left", va="center",
        fontsize=7.2)

# --- (2) v_out：i_C の積分。山と谷は i_C のゼロ交差の時刻
ax = axes[1]
setup(ax, 4.90, 5.10, [4.90, 4.95, 5.00, 5.05, 5.10], r"$v_{\mathrm{out}}$ [V]",
      xaxis_at_zero=False)
ax.plot(t, vout, color=BLUE, lw=1.1, zorder=3)
ax.plot([T0, T1], [Vout] * 2, color=RED, lw=0.8, ls="--", zorder=2)
ax.text(T0 + TSW, Vout + 0.012, r"$V_{\mathrm{out}}$", ha="center",
        va="bottom", fontsize=6.6, color=RED)
vmax, vmin = vout.max(), vout.min()
xd = T1 + 0.12
ax.annotate("", xy=(xd, vmax), xytext=(xd, vmin),
            arrowprops=dict(arrowstyle="<->", lw=0.9, color=BK,
                            mutation_scale=7))
ax.text(xd + 0.05, Vout, r"$\Delta V_{\mathrm{out}}$", ha="left",
        va="center", fontsize=7.0)
ax.plot([t2 + TSW, xd + 0.04], [vmax] * 2, color="#999", lw=0.5, ls=":")
ax.plot([t1 + TSW, xd + 0.04], [vmin] * 2, color="#999", lw=0.5, ls=":")
# 山と谷が i_C のゼロ交差に現れることを縦の点線で示す
for x in (t1, t2, t1 + TSW, t2 + TSW):
    ax.plot([x, x], [4.90, vmax if x in (t2, t2 + TSW) else vmin],
            color="#999", lw=0.5, ls=":")

fig.subplots_adjust(hspace=0.62)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig5.8.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
