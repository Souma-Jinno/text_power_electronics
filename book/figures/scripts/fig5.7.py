#!/usr/bin/env python3
# fig5.7（第5章）: インダクタ電流の連続モード（CCM）・境界・不連続モード（DCM）。
# 負荷電流が ΔI_L/2 を下回ると電流がゼロに張り付く期間が現れる。
# 波形は配布モデル ltspice/chapter05/buck_chopper.net（V_in=10 V, D=0.5, f=1 kHz,
# L=30 mH, C=100 uF，ダイオードはほぼ理想）の負荷抵抗 R だけを 3 通りに変えて
# ngspice で解いた結果そのもの（定常状態に達した 118〜120 ms の 2 周期を切り出し，
# 切り出しの先頭を t=0 として描く）。
#   (a) R = 40 Ω  … I_out = 0.125 A > ΔI_L/2 = 0.042 A → CCM
#   (b) R = 120 Ω … I_out = ΔI_L/2 → 境界（R_B = 2fL/(1-D) = 120 Ω，章末問題【4】）
#   (c) R = 300 Ω … I_out < ΔI_L/2 → DCM（出力は 5 V から 6.57 V に浮き上がる）
# 3 つのパネルは同じ電流目盛りで描く（谷がゼロにどれだけ近いかを比べるため）。
# 注意: インダクタ電流は i(L1) では取れないので @l1[i] を使う。
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
T0, T1 = 118.0, 120.0   # 表示区間 [ms]（定常状態の2周期）
TSW, DUTY = 1.0, 0.5    # 周期 [ms]，デューティ比（ネットリストと同じ値）
LOADS = [40.0, 120.0, 300.0]  # 負荷抵抗 [Ω]：CCM／境界／DCM


def run_ngspice(R):
    """buck_chopper.net の R1 を R に置き換えて過渡解析し，(t[ms], iL, vout) を返す。"""
    exe = shutil.which("ngspice") or os.path.expanduser("~/miniforge3/bin/ngspice")
    if not os.path.isfile(exe):
        sys.exit("error: ngspice が見つかりません（PATH か ~/miniforge3/bin に置いてください）")
    if not os.path.isfile(NET):
        sys.exit(f"error: ネットリストがありません: {NET}")
    cards = []
    with open(NET) as f:
        for ln in f:
            if ln.lower().startswith((".tran", ".end")):
                continue
            if ln.startswith("R1 "):
                ln = f"R1 N003 0 {R:g}\n"
            cards.append(ln)
    deck = "".join(cards) + """
.control
set filetype=ascii
save all @l1[i]
tran 1u 120.3m 117.9m
let iL = @l1[i]
linearize iL v(N003)
wrdata buck.txt iL v(N003)
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
    return t, data[:, 1], data[:, 3]


waves = []
for R in LOADS:
    t, iL, vout = run_ngspice(R)
    m = (t >= T0) & (t <= T1)
    t, iL, vout = t[m] - T0, iL[m], vout[m]
    waves.append((t, iL))
    zero = (iL < 1e-4).mean()
    print(f"R={R:g} Ω: Vout={vout.mean():.3f} V  Iout={iL.mean():.4f} A  "
          f"iL=({iL.min():.4f},{iL.max():.4f}) A  dIL={iL.max() - iL.min():.4f} A  "
          f"zero-fraction={zero:.3f}")

TMAX = 2 * TSW
YM = 0.18  # 共通の電流目盛り [A]
TON = [(k * TSW, DUTY * TSW) for k in range(2)]  # オン期間


def setup(ax, title):
    for x, w in TON:
        ax.add_patch(Rectangle((x, 0), w, YM, fc=SHADE, ec="none", zorder=0))
    ax.annotate("", xy=(1.14 * TMAX, 0), xytext=(-0.01 * TMAX, 0),
                arrowprops=dict(arrowstyle="-|>", lw=0.8, color=BK,
                                mutation_scale=8))
    ax.plot([0, 0], [0, YM], color=BK, lw=0.8)
    for x in np.arange(0, TMAX + 1e-9, 0.5):
        ax.plot([x, x], [-0.02 * YM, 0.02 * YM], color=BK, lw=0.7)
    for x in (0, 1, 2):
        ax.text(x, -0.08 * YM, f"{x:g}", ha="center", va="top", fontsize=6.0)
    ax.text(1.16 * TMAX, -0.05 * YM, "$t$ [ms]", ha="left", va="top", fontsize=6.0)
    for y in (0, 0.05, 0.10, 0.15):
        ax.plot([-0.02, 0.02], [y, y], color=BK, lw=0.7)
        ax.text(-0.05, y, f"{y:g}", ha="right", va="center", fontsize=5.8)
    ax.text(-0.04, YM + 0.10 * YM, "$i_L$ [A]", ha="right", va="center",
            fontsize=7.0, color=BLUE)
    ax.text(TMAX / 2, -0.50 * YM, title, ha="center", fontsize=6.6,
            fontproperties=JP, color="#555")
    ax.set_xlim(-0.42 * TMAX, 1.30 * TMAX)
    ax.set_ylim(-0.66 * YM, 1.20 * YM)
    ax.axis("off")


fig, axes = plt.subplots(1, 3, figsize=(4.25, 1.6))

# --- (a) CCM（R = 40 Ω）：谷が 0 より十分上にある
ax = axes[0]
setup(ax, "(a) 連続（CCM）")
t, iL = waves[0]
ax.plot(t, iL, color=BLUE, lw=1.1, zorder=3)
mean = iL.mean()
ax.plot([0, TMAX], [mean] * 2, color=RED, lw=0.8, ls="--", zorder=2)
ax.text(TMAX + 0.10, mean, r"$I_{\mathrm{out}}$", ha="left", va="center",
        fontsize=6.4, color=RED)

# --- (b) 境界（R = 120 Ω）：谷がちょうど 0 に触れる
ax = axes[1]
setup(ax, "(b) 境界")
t, iL = waves[1]
ax.plot(t, iL, color=BLUE, lw=1.1, zorder=3)
mean = iL.mean()
ax.plot([0, TMAX], [mean] * 2, color=RED, lw=0.8, ls="--", zorder=2)
ax.text(TMAX + 0.10, mean, r"$\frac{\Delta I_L}{2}$", ha="left", va="center",
        fontsize=7.0, color=RED)

# --- (c) DCM（R = 300 Ω）：電流が 0 に張り付く第3の期間が現れる
ax = axes[2]
setup(ax, "(c) 不連続（DCM）")
t, iL = waves[2]
ax.plot(t, iL, color=BLUE, lw=1.1, zorder=3)
# 1周期目の電流が 0 に達した時刻（減少中に 1e-4 A を下回る点）を実データから求める
per = (t >= DUTY * TSW) & (t < TSW)
tz = t[per][np.argmax(iL[per] < 1e-4)]
ya = 0.62 * YM
ax.annotate("", xy=(TSW, ya), xytext=(tz, ya),
            arrowprops=dict(arrowstyle="<->", lw=0.7, color=BK,
                            mutation_scale=6))
ax.text(0.5 * (tz + TSW), ya + 0.05 * YM, "$i_L=0$", ha="center",
        va="bottom", fontsize=6.2)
ax.plot([tz, tz], [0, ya], color="#999", lw=0.5, ls=":")
ax.plot([TSW, TSW], [0, ya], color="#999", lw=0.5, ls=":")

fig.subplots_adjust(wspace=0.30)
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig5.7.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
