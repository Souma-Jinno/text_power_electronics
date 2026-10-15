# fig5.10_miniaturize.py — 図5.10 高周波化で L と C が小さくなるイメージ（Blender 版）
#
# 狙い（一行）：同じリプルを許すなら L も C も 1/f で済む（式 5.21・5.25）。f = 10 kHz・100 kHz・1 MHz の 3 組の
#               インダクタ（トロイダルコアに巻線）とキャパシタ（電解コンデンサの円筒）を横に並べ，右へ行くほど小さくなる様子を見せる。
# [2026-10-15 先生の赤枠（森北送付案 r6 note01 p32）「このグラフなんか当たり前なので、素子が小さくなるイメージを載せてくれない？
#   blenderとかで作れる？」] L ∝ 1/f, C ∝ 1/f の両対数グラフ（旧 scripts/fig5.10.py）をこの図に替えた。
#
# 大きさの決め方：L・C の値は 1 組ごとに 1/10。部品の体積は（同じ材料・同じ電流・同じ電圧なら）おおよそ L・C の値に比例するとみて，
#   体積を 1/10 ずつ → 線寸法を (1/10)^(1/3) ≈ 0.464 倍ずつにした（誇張しない目安。実際の部品は材料や定格で変わる）。
# 数値：章末問題【5】（旧 例題 5.2）の設計（12 V → 5 V，2 A，ΔI_L = 0.4 A）の L = (V_in − V_out) D / (f ΔI_L) と，
#   章末問題（ΔV_out = 50 mV）の C = ΔI_L / (8 f ΔV_out)。100 kHz で 73 µH・10 µF（旧図の印と同じ値）。
# 図に和文は入れない（数値と単位だけ）。白背景，版面幅（318 pt）以内，文字は \footnotesize（8 pt）。
# 検算：verify_fig5.10_miniaturize.py（geom.json の寸法比が (1/10)^(1/3)，体積比が 1/10，ラベルの L・C が設計式の値に一致，
#   3 組が左から右へ単調に小さく重ならない，EPS の幅が 318 pt 以下）。
# 使い方：./build_fig.sh fig5.10_miniaturize   （最後に ../fig5.10.eps へ写る）

import sys
import math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import bpy
from mathutils import Vector
from blfig import Fig, args, col, cyl_solid, circle_pts, flat_poly

OUT, SAMPLES = args()
F = Fig("fig5.10_miniaturize", SAMPLES, world=0.9)

UNIT_CM = 1.62
PT = 1 / 72 * 2.54 / UNIT_CM              # 1 pt を図の単位に
VIEW = Vector((0.0, -1.0, 0.42))          # 正面やや上から見る（横向きの成分を入れると 3 組の接地の高さが画面でずれる）

# ---------------- 設計値（章末問題【5】（旧 例題 5.2）と章末問題の ΔV_out = 50 mV） ----------------
Vin, Vout, dI, dV = 12.0, 5.0, 0.4, 0.05
D = Vout / Vin
FREQ = [1e4, 1e5, 1e6]
Lval = [(Vin - Vout) * D / (f * dI) for f in FREQ]       # [H]
Cval = [dI / (8 * f * dV) for f in FREQ]                 # [F]
K = (1 / 10) ** (1 / 3)                                  # 1 組ごとの線寸法の比
SC = [K ** k for k in range(3)]

# ---------------- 色 ----------------
M_CORE = F.solid("core", col(0.30, 0.30, 0.32), emit=0.05, rough=0.55)          # フェライトのコア（濃い灰）
M_CU = F.solid("copper", col(0.78, 0.45, 0.22), emit=0.08, rough=0.3, metallic=0.7)
M_SLV = F.solid("sleeve", col(0.165, 0.365, 0.69), emit=0.12, rough=0.35)       # 電解コンデンサのスリーブ（本文の青 #2a5db0）
M_BAND = F.solid("band", col(0.86, 0.88, 0.92), emit=0.15, rough=0.4)           # 極性の帯（淡い灰）
M_TOP = F.solid("top", col(0.80, 0.81, 0.83), emit=0.1, rough=0.25, metallic=0.6)  # アルミの天面
M_VENT = F.solid("vent", col(0.45, 0.46, 0.48), emit=0.0, rough=0.4)

sil = bpy.data.collections.new("Sil")     # 輪郭線（silhouette）だけを描く
F.scene.collection.children.link(sil)

# 単位の大きさ（s = 1，10 kHz の組）
R_MAJ, R_MIN = 0.62, 0.25                 # トロイダルコア（中心半径，断面半径）
NTURN = 16                                # 巻数（3 組とも同じ形をそのまま縮める）
R_W = 0.042                               # 巻線の太さ（半径）
RC, HC = 0.42, 1.30                       # コンデンサの半径・高さ
GAP_IC = 0.30                             # インダクタとコンデンサの間
W_GROUP = 2 * (R_MAJ + R_MIN + R_W) + GAP_IC + 2 * RC


def torus_mesh(name, c, s, nu=96, nv=32):
    """軸を y（カメラの方）に向けて立てたトロイダルコア"""
    V, Fc = [], []
    for i in range(nu):
        th = 2 * math.pi * i / nu
        for j in range(nv):
            ph = 2 * math.pi * j / nv
            rr = (R_MAJ + R_MIN * math.cos(ph)) * s
            V.append((c.x + rr * math.cos(th), c.y + R_MIN * s * math.sin(ph), c.z + rr * math.sin(th)))
    for i in range(nu):
        for j in range(nv):
            a, b = i * nv + j, i * nv + (j + 1) % nv
            d, e = ((i + 1) % nu) * nv + j, ((i + 1) % nu) * nv + (j + 1) % nv
            Fc.append((a, b, e, d))
    return F.mesh(name, V, Fc, [M_CORE], mark_edges=False, coll=sil, smooth=True)


def winding(c, s, n=2400):
    """コアに巻いた巻線（下の 50° を空けて NTURN 回）。両端から下へ引き出し線"""
    th0, th1 = math.radians(-90 + 28), math.radians(-90 + 360 - 28)
    rw = R_MIN + R_W * 0.9
    pts = []
    for k in range(n + 1):
        u = k / n
        th = th0 + (th1 - th0) * u
        ph = 2 * math.pi * NTURN * u + math.pi        # 内側から巻き始める
        rr = R_MAJ + rw * math.cos(ph)
        pts.append(Vector((c.x + rr * s * math.cos(th), c.y + rw * s * math.sin(ph), c.z + rr * s * math.sin(th))))
    F.tube("wind", pts, R_W * s, M_CU)
    # 引き出し線：巻線の両端から真下（地面）まで
    for p in (pts[0], pts[-1]):
        F.tube("lead", [p, Vector((p.x, p.y, 0.0))], R_W * s * 0.8, M_CU)
    return pts


def capacitor(c, s):
    """電解コンデンサ：青いスリーブの円筒，アルミの天面に K 字の防爆弁の溝，正面寄りに極性の帯"""
    r, h = RC * s, HC * s
    cyl_solid(F, "cap", Vector((c.x, c.y, 0.0)), Vector((c.x, c.y, h)), 0, r, M_SLV, coll=sil)
    # 天面（少し内側の円板）
    top = circle_pts(Vector((c.x, c.y, h + 0.002 * s)), (0, 0, 1), 0.86 * r, n=97)[:-1]
    flat_poly(F, "top", top, M_TOP, mark=False, coll=F.other)
    # 防爆弁の溝（十字）
    for a in (0.0, math.pi / 2):
        d = Vector((math.cos(a), math.sin(a), 0)) * 0.55 * r
        z = Vector((0, 0, h + 0.006 * s))
        F.tube("vent", [Vector((c.x, c.y, 0)) + z - d, Vector((c.x, c.y, 0)) + z + d], 0.018 * s, M_VENT)
    # 極性の帯（スリーブの手前右寄り，角度 −60°〜−30°）
    nb, a0, a1 = 16, math.radians(-62), math.radians(-34)
    V, Fc = [], []
    for k in range(nb + 1):
        a = a0 + (a1 - a0) * k / nb
        for z in (0.06 * h, 0.94 * h):
            V.append((c.x + 1.004 * r * math.cos(a), c.y + 1.004 * r * math.sin(a), z))
    for k in range(nb):
        Fc.append((2 * k, 2 * k + 2, 2 * k + 3, 2 * k + 1))
    F.mesh("band", V, Fc, [M_BAND], mark_edges=False, coll=F.other, smooth=True)


# ---------------- 3 組を左から右へ（地面 z = 0 にそろえて置く） ----------------
GAP = 0.62                                # 組と組の間（ラベルの幅を確保）
groups, x = [], 0.0
for k, s in enumerate(SC):
    w = W_GROUP * s
    x_ind = x + (R_MAJ + R_MIN + R_W) * s
    x_cap = x + w - RC * s
    ci = Vector((x_ind, 0, (R_MAJ + R_MIN + R_W) * s))
    torus_mesh(f"core{k}", ci, s)
    winding(ci, s)
    capacitor(Vector((x_cap, 0, 0)), s)
    groups.append(dict(k=k, s=s, x0=x, x1=x + w, xc=x + w / 2, ind_center=list(ci),
                       ind_outer_d=2 * (R_MAJ + R_MIN + R_W) * s, cap_r=RC * s, cap_h=HC * s,
                       f=FREQ[k], L=Lval[k], C=Cval[k]))
    x += w + GAP * (1.0 if k == 0 else 0.85)

# ---------------- 光・カメラ ----------------
F.area_light((x / 2 - 3.5, -6.5, 7.5), (x / 2, 0, 0), size=8, energy=1100)
xe = groups[-1]["x1"]
pts = [Vector((0, 0, 0)), Vector((xe, 0, 0)), Vector((0, 0, 2 * (R_MAJ + R_MIN + R_W))), Vector((0, -0.4, 0)),
       Vector((xe, 0.4, 0)), Vector((groups[0]["xc"], 0, -1.12)), Vector((xe + 0.2, 0, -1.12)), Vector((-0.15, 0, 0))]
F.camera(VIEW, pts, UNIT_CM, margin=0.06)
F.freestyle(front_pt=0.4, hidden=False, sil=sil, sil_pt=0.4, sil_color=(0.15, 0.15, 0.15))


# ---------------- ラベル（各組の下：f，L，C） ----------------
def fmt(v, unit):
    """有効数字 2 桁で µ 単位の TeX 文字列"""
    u = v * 1e6
    return f"{float(f'{u:.2g}'):g}"           # 729.2 → 730，72.9 → 73，100.0 → 100


labels = []
for g in groups:
    ftxt = {1e4: r"10\,\mathrm{kHz}", 1e5: r"100\,\mathrm{kHz}", 1e6: r"1\,\mathrm{MHz}"}[g["f"]]
    Lt, Ct = fmt(g["L"], "H"), fmt(g["C"], "F")
    tex = (r"\begin{tabular}{@{}c@{}}$f=" + ftxt + r"$\\[1pt]"
           r"$L=" + Lt + r"\,\mu\mathrm{H}$\\$C=" + Ct + r"\,\mu\mathrm{F}$\end{tabular}")
    F.label(Vector((g["xc"], 0, -0.30)), tex, anchor="north")   # コンデンサの底の楕円より下
    g["label_L_uH"], g["label_C_uF"] = float(Lt), float(Ct)
    labels.append(tex)

geom = dict(K=K, groups=groups, Vin=Vin, Vout=Vout, dI=dI, dV=dV, unit_cm=UNIT_CM, labels=labels)
F.render(OUT, geom)
