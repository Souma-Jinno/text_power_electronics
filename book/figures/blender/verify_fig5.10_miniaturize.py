"""verify_fig5.10_miniaturize.py — 図5.10（Blender 版）の検算

  (a) 2 組の線寸法の比が (1/10)^(1/3)（≈ 0.464）ずつ，体積の比が 1/10 ずつ（誇張していない）。
  (b) ラベルの L・C が設計式 L = (V_in − V_out) D / (f ΔI_L)，C = ΔI_L / (8 f ΔV_out) の値（有効数字 2 桁）に一致し，
      100 kHz で 73 µH・10 µF（章末問題（旧例題 5.2）・旧図の値）。
  (c) f が 10 倍ずつで，L・C が 1/10 ずつ。
  (d) 2 組が左から右へ並び重ならず，右ほど小さい。矢印（f×10）が 2 組の間にあり右向き。
      [2026-10-15 r7] 3 組目（1 MHz）を外したので 2 組を確かめる。
  (e) EPS の幅が版面幅 318 pt 以下。
"""
import json
import re
from pathlib import Path

H = Path(__file__).resolve().parent
G = json.loads((H / "fig5.10_miniaturize.geom.json").read_text())
gs, K = G["groups"], G["K"]
D = G["Vout"] / G["Vin"]

assert abs(K - 0.1 ** (1 / 3)) < 1e-12
for a, b in zip(gs[:-1], gs[1:]):
    r = b["s"] / a["s"]
    rv = (b["ind_outer_d"] / a["ind_outer_d"]) ** 3
    rc = (b["cap_r"] ** 2 * b["cap_h"]) / (a["cap_r"] ** 2 * a["cap_h"])
    print(f"(a) {a['f']:.0e}→{b['f']:.0e} Hz: 線寸法 ×{r:.3f}，体積 インダクタ ×{rv:.3f}，コンデンサ ×{rc:.3f}")
    assert abs(r - K) < 1e-9 and abs(rv - 0.1) < 1e-9 and abs(rc - 0.1) < 1e-9

for g in gs:
    L = (G["Vin"] - G["Vout"]) * D / (g["f"] * G["dI"]) * 1e6
    C = G["dI"] / (8 * g["f"] * G["dV"]) * 1e6
    print(f"(b) f = {g['f']:.0e} Hz: L = {L:.2f} µH（ラベル {g['label_L_uH']:g}），C = {C:.2f} µF（ラベル {g['label_C_uF']:g}）")
    assert abs(g["label_L_uH"] / L - 1) < 0.02 and abs(g["label_C_uF"] / C - 1) < 0.02
g1 = gs[1]
assert g1["f"] == 1e5 and g1["label_L_uH"] == 73 and g1["label_C_uF"] == 10

for a, b in zip(gs[:-1], gs[1:]):
    assert abs(b["f"] / a["f"] - 10) < 1e-9
    assert abs(b["L"] / a["L"] - 0.1) < 1e-9 and abs(b["C"] / a["C"] - 0.1) < 1e-9
    assert a["x1"] < b["x0"] and b["s"] < a["s"]
assert len(gs) == 2 and gs[0]["f"] == 1e4
A = G["arrow"]
assert gs[0]["x1"] < A["x0"] < A["x1"] < gs[1]["x0"]
assert 0 < A["z"] < 2 * max(gs[1]["cap_h"], gs[1]["ind_outer_d"])
print("(c)(d) f は 10 倍，L・C は 1/10，2 組は左から右へ重ならず右が小さい。矢印は 2 組の間で右向き")

bb = re.search(r"%%BoundingBox: (\S+) (\S+) (\S+) (\S+)", (H / "fig5.10_miniaturize.eps").read_text(errors="ignore"))
w = float(bb.group(3)) - float(bb.group(1))
h = float(bb.group(4)) - float(bb.group(2))
print(f"(e) EPS {w:.0f} × {h:.0f} pt（版面幅 318 pt 以下）")
assert w <= 318
print("verify OK")
