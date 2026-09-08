#!/usr/bin/env python3
# fig5.2（第5章）: 過渡状態から定常状態へ。電源を入れた直後は V_out がまだ低いので
# v_L の正の面積が負の面積より大きく，インダクタ電流は周期ごとに増えていく（過渡状態）。
# V_out が D*V_in に落ち着くと正負の面積が等しくなり（ボルト秒平衡），
# i_L は毎周期同じ三角波を繰り返す（定常状態）。
# 波形は配布モデル ltspice/chapter05/buck_chopper.net（V_in=10 V, D=0.5,
# f=1 kHz, L=30 mH, C=100 uF, R=10 Ω，ダイオードはほぼ理想）を ngspice で解いた結果そのもの。
# fig5.4 が定常状態（19〜21 ms）を切り出すのに対し，この図は起動 t=0 から 12 ms
# （12周期）をそのまま描く。解析時間はネットリストの .tran（22 ms）と同じ。
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
FILL_P = "#c5d5ef"  # v_L の正の面積（fig5.8 の ΔQ と同じ色）
FILL_N = "#f3cfcb"  # v_L の負の面積

NET = os.path.expanduser(
    "~/text_power_electronics/book/figures/ltspice/chapter05/buck_chopper.net")
T0, T1 = 0.0, 12.0    # 描画の時間軸 [ms]（起動から12周期）
TSW, DUTY = 1.0, 0.5  # 周期 [ms]，デューティ比（ネットリストと同じ値）
NP = int(round((T1 - T0) / TSW))
KA = 1   # 過渡状態の例として注記する周期（2周期目）
KB = 10  # 定常状態の例として注記する周期（11周期目）
TB = 8.0  # 図の上の「過渡状態」「定常状態」の矢印の境目 [ms]（1周期の増え分が ΔI_L の 1% を切る）


def run_ngspice():
    """buck_chopper.net を ngspice で過渡解析し，(t[ms], vL, iL, vout) を返す。"""
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
    return t, data[:, 1], data[:, 3], data[:, 7]


t, vL, iL, vout = run_ngspice()
m = (t >= T0) & (t <= T1)
t, vL, iL, vout = t[m], vL[m], iL[m], vout[m]


def period(k):
    """k 周期目（t = kT〜(k+1)T）の正の面積，負の面積 [V·ms]，始点・終点の i_L [A]。"""
    on = (t >= k * TSW) & (t <= (k + DUTY) * TSW)
    off = (t >= (k + DUTY) * TSW) & (t <= (k + 1) * TSW)
    ap = np.trapezoid(vL[on], t[on])
    an = np.trapezoid(vL[off], t[off])
    return ap, an, np.interp(k * TSW, t, iL), np.interp((k + 1) * TSW, t, iL)


last = (t >= T1 - 2 * TSW)
Iout = iL[last].mean()
dIL = iL[last].max() - iL[last].min()
print(f"steady (last 2 periods): Vout={vout[last].mean():.3f} V  "
      f"Iout={Iout:.4f} A  dIL={dIL:.4f} A")
for k in range(NP):
    ap, an, i0, i1 = period(k)
    print(f"  k={k:2d}: A+={ap:.3f} A-={an:.3f} V*ms  "
          f"iL({k}T)={i0:.4f} iL({k + 1}T)={i1:.4f} diff={i1 - i0:+.4f} A")

XL, XR = T0 - 2.6, T1 + 3.6  # 描画範囲 [ms]（左右に注記の余白）
TON = [(T0 + k * TSW, DUTY * TSW) for k in range(NP)]  # オン期間


def setup(ax, ymin, ymax, yticks, label, xaxis_at_zero=True, top=0.18,
          label_y=0.21):
    """矢印付きの手描き軸。x軸は 0（または ymin）の高さに置く（fig5.4 と同じ流儀）。"""
    dy = ymax - ymin
    y0 = 0.0 if xaxis_at_zero else ymin
    for x, w in TON:
        ax.add_patch(Rectangle((x, ymin), w, dy, fc=SHADE, ec="none", zorder=0))
    ax.annotate("", xy=(T1 + 1.0, y0), xytext=(T0 - 0.1, y0),
                arrowprops=dict(arrowstyle="-|>", lw=0.8, color=BK,
                                mutation_scale=8))
    ax.plot([T0, T0], [ymin, ymax], color=BK, lw=0.8)
    for x in np.arange(T0, T1 + 1e-9, 2.0):
        ax.plot([x, x], [y0 - 0.02 * dy, y0 + 0.02 * dy], color=BK, lw=0.7)
        ax.text(x, ymin - 0.11 * dy, f"{x:g}", ha="center", va="top",
                fontsize=6.2)
    ax.text(T1 + 1.1, y0 - 0.06 * dy, "$t$ [ms]", ha="left", va="top",
            fontsize=6.6)
    for y in yticks:
        ax.plot([T0 - 0.1, T0 + 0.1], [y, y], color=BK, lw=0.7)
        ax.text(T0 - 0.25, y, f"{y:g}", ha="right", va="center", fontsize=6.2)
    ax.text(T0 - 0.15, ymax + label_y * dy, label, ha="right", va="center",
            fontsize=7.4, color=BLUE)
    ax.set_xlim(XL, XR)
    ax.set_ylim(ymin - 0.36 * dy, ymax + top * dy)
    ax.axis("off")


fig, axes = plt.subplots(2, 1, figsize=(4.25, 3.3))

# --- (1) v_L：正の面積（青）と負の面積（赤）。はじめは正が大きく，やがて等しくなる
ax = axes[0]
setup(ax, -6.5, 10.5, [-5, 0, 5, 10], "$v_L$ [V]", top=0.55, label_y=0.40)
ax.fill_between(t, 0, vL, where=vL > 0, fc=FILL_P, ec="none", zorder=1)
ax.fill_between(t, 0, vL, where=vL < 0, fc=FILL_N, ec="none", zorder=1)
ax.plot(t, vL, color=BLUE, lw=0.9, zorder=3)
# 定常値 V_in-V_out，-V_out の点線と右側のラベル
on = (t >= T1 - TSW) & (t <= T1 - (1 - DUTY) * TSW)
off = (t >= T1 - (1 - DUTY) * TSW) & (t <= T1)
vp, vn = vL[on].mean(), vL[off].mean()
ax.plot([TB, T1 + 0.3], [vp] * 2, color="#999", lw=0.5, ls=":", zorder=2)
ax.plot([TB, T1 + 0.3], [vn] * 2, color="#999", lw=0.5, ls=":", zorder=2)
ax.text(T1 + 0.45, vp, r"$V_{\mathrm{in}}-V_{\mathrm{out}}$", ha="left",
        va="center", fontsize=6.4)
ax.text(T1 + 0.45, vn, r"$-V_{\mathrm{out}}$", ha="left",
        va="center", fontsize=6.4)
# 起動直後は V_out がほぼ 0 なので v_L はほぼ V_in
ax.text(T0 + 0.7, 9.2, r"起動直後は$V_{\mathrm{out}}\approx 0$",
        ha="left", va="bottom", fontsize=6.0, fontproperties=JP, color="#555")
# 面積の注記：過渡状態（負の面積がまだ小さい区間の下）と定常状態（波形の上）
ax.text(T0 + 2.4, -5.3, "正の面積＞負の面積", ha="center", va="center",
        fontsize=6.2, fontproperties=JP, color="#555")
ax.text(T1 - 2.0, 8.0, "正の面積＝負の面積\n（ボルト秒平衡）", ha="center",
        va="center", fontsize=6.2, fontproperties=JP, color="#555",
        linespacing=1.15)
# 図の上：過渡状態 → 定常状態
ya = 13.8
for xa, xb, s in [(T0, TB, "過渡状態"), (TB, T1, "定常状態")]:
    ax.annotate("", xy=(xb, ya), xytext=(xa, ya),
                arrowprops=dict(arrowstyle="<->", lw=0.7, color=BK,
                                mutation_scale=6, shrinkA=0, shrinkB=0))
    ax.text(0.5 * (xa + xb), ya, s, ha="center", va="center", fontsize=6.6,
            fontproperties=JP, color=BK,
            bbox=dict(fc="white", ec="none", pad=1.0))
ax.plot([TB, TB], [ya - 0.6, ya + 0.6], color=BK, lw=0.6)

# --- (2) i_L：三角波が周期ごとに持ち上がり，やがて一定の高さで振動する
ax = axes[1]
setup(ax, 0.0, 0.6, [0, 0.2, 0.4, 0.6], "$i_L$ [A]", top=0.30)
ax.plot(t, iL, color=BLUE, lw=0.9, zorder=3)
ax.plot([T0, T1 + 0.3], [Iout] * 2, color=RED, lw=0.8, ls="--", zorder=2)
ax.text(T1 + 0.45, Iout, r"$I_{\mathrm{out}}$", ha="left", va="center",
        fontsize=6.6, color=RED)
# 過渡状態の例（KA 周期目）：1周期で電流が増える
_, _, ia0, ia1 = period(KA)
xa, xb = KA * TSW, (KA + 1) * TSW
ax.plot([xa, xb], [ia0] * 2, color="#999", lw=0.5, ls=":", zorder=2)
ax.annotate("", xy=(xb, ia1), xytext=(xb, ia0),
            arrowprops=dict(arrowstyle="-|>", lw=0.9, color=RED,
                            mutation_scale=7, shrinkA=0, shrinkB=0), zorder=4)
ax.plot(xa, ia0, "o", ms=2.2, color=BK, zorder=5)
ax.text(xb + 0.2, 0.05, "1周期で増える", ha="left", va="bottom",
        fontsize=6.2, fontproperties=JP, color="#555")
# 定常状態の例（KB 周期目）：1周期でもとの値に戻る
_, _, ib0, ib1 = period(KB)
xa, xb = KB * TSW, (KB + 1) * TSW
ax.plot([xa, xb], [ib0] * 2, color="#999", lw=0.5, ls=":", zorder=2)
ax.plot([xa, xb], [ib0, ib1], "o", ms=2.2, color=BK, zorder=5)
ax.text(0.5 * (xa + xb), 0.62, "1周期で戻る", ha="center", va="bottom",
        fontsize=6.2, fontproperties=JP, color="#555")

fig.subplots_adjust(hspace=0.12)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig5.2.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
