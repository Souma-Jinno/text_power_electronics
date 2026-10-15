#!/bin/bash
# build_fig.sh — Blender 版の図（lib/blfig.py を使う図）を，Blender のレンダから EPS まで作る。
# 電磁界理論の教科書の同名スクリプトの写し（2026-10-15）。最後に本文が読む ../<図番号>.eps（例 ../fig5.10.eps）へ写す所だけ足した。
# 使い方: cd book/figures/blender && ./build_fig.sh <名前（例 fig5.10_miniaturize）> [samples（既定 128）]
#
#   <名前>.py ──(blender -b，Cycles＋Freestyle)──> out/_<名前>.render.png（透明背景）
#        │                                        ＋ <名前>.labels.json（ラベルの画面座標 px，TikZ の anchor）
#        │                                        ＋ <名前>.geom.json（検算用の幾何。ある図だけ）
#        ├─(PIL で白に合成)──> out/_<名前>.art.png（RGB，600 dpi）
#        └─ ラベルを TikZ で重ねる TeX（jarticle，本文と同じ platex の Computer Modern）
#             ──(platex → dvipdfmx → pdfcrop)──> out/<名前>.pdf ──(pdftops -eps)──> <名前>.eps
#   確認用に <名前>.png（300 dpi）も出し，verify_<名前>.py があれば実行する。
# 注意：図形は Blender のレンダ（ラスタ）なので，EPS は 600 dpi の画像 1 枚＋ベクトルの文字（フォント埋め込み）になる。
set -euo pipefail
# OS 非依存化（2026-09-30，zimaboard の Linux 対応）: ツールは PATH から探し，無ければ macOS の既定パスを使う。
#   Blender は環境変数 BLENDER → PATH の blender → ~/opt/blender/blender（Linux の公式版を置いた場所）→ /opt/homebrew/bin/blender の順。
if command -v platex >/dev/null 2>&1; then TEXBIN="$(dirname "$(command -v platex)")"; else TEXBIN=/Library/TeX/texbin; fi
if [ -z "${BLENDER:-}" ]; then
  if command -v blender >/dev/null 2>&1; then BLENDER=$(command -v blender)
  elif [ -x "$HOME/opt/blender/blender" ]; then BLENDER="$HOME/opt/blender/blender"
  else BLENDER=/opt/homebrew/bin/blender; fi
fi
PDFCROP=$(command -v pdfcrop || echo "$TEXBIN/pdfcrop")
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE"
n=$1
S=${2:-128}
mkdir -p out
t0=$(date +%s)
"$BLENDER" -b --factory-startup -P "$n.py" -- out "$S" 2>&1 | grep -E "RENDER_DONE|Error|Traceback|line [0-9]" || true
[ -f "out/_$n.render.png" ] && [ "out/_$n.render.png" -nt "$n.py" ] || { echo "レンダ失敗"; exit 1; }
cp "out/$n.labels.json" .
[ -f "out/$n.geom.json" ] && cp "out/$n.geom.json" . || true
echo "レンダ: $(( $(date +%s) - t0 )) 秒"

python3 - "$n" <<'PY'
import json, sys
from PIL import Image
n = sys.argv[1]
a = Image.open(f"out/_{n}.render.png").convert("RGBA")
w = Image.new("RGBA", a.size, "white"); w.alpha_composite(a)
J = json.load(open(f"{n}.labels.json"))
dpi = J["dpi"]; H = J["height_px"]
w.convert("RGB").save(f"out/_{n}.art.png", dpi=(dpi, dpi))
bp = 72 / dpi
nodes = []
for l in J["labels"]:
    x, y = l["x"] * bp + l.get("dx", 0), (H - l["y"]) * bp + l.get("dy", 0)
    nodes.append(rf"\node[anchor={l['anchor']},inner sep=1.2pt] at ({x:.2f},{y:.2f}) {{{l['tex']}}};")
tex = r"""%% 自動生成（build_fig.sh）：Blender のレンダ画像の上に TeX でラベルを重ねる
\documentclass[dvipdfmx]{jarticle}
\usepackage{amsmath,amssymb}
\usepackage{graphicx,xcolor}
\usepackage{tikz}
\definecolor{accent}{rgb}{0,0,0.6}
\pagestyle{empty}
\begin{document}
\noindent\footnotesize
\begin{tikzpicture}[x=1bp,y=1bp]
  \node[anchor=south west,inner sep=0] at (0,0) {\includegraphics[width=%.3fbp,height=%.3fbp]{_%s.art.png}};
%s
\end{tikzpicture}
\end{document}
""" % (J["width_px"] * bp, H * bp, n, "\n".join("  " + s for s in nodes))
open(f"out/_{n}.tex", "w").write(tex)
PY

( cd out
  $TEXBIN/extractbb "_$n.art.png"
  $TEXBIN/platex -interaction=nonstopmode -halt-on-error "_$n.tex" > "_$n.build.txt" 2>&1 || { tail -20 "_$n.build.txt"; exit 1; }
  $TEXBIN/dvipdfmx -q -o "_$n.full.pdf" "_$n.dvi"
  $PDFCROP --margins 1 "_$n.full.pdf" "$n.pdf" > /dev/null )
pdftops -eps -level3 "out/$n.pdf" "$n.eps"
pdftoppm -png -r 300 -singlefile "out/$n.pdf" "$n"
grep -m1 '%%BoundingBox' "$n.eps"
pdfimages -list "out/$n.pdf" | tail -n +3 | awk '{print "ラスタ画像:", $4"x"$5}'
pdffonts "out/$n.pdf" | tail -n +3 | awk '{printf "%s ", $1} END {print ""}'
ls -l "$n.eps" | awk '{print "EPS サイズ:", $5, "bytes"}'
[ -f "verify_$n.py" ] && python3 "verify_$n.py"
# 本文は figures/<図番号>.eps を読む（名前の「_」より前が図番号）
cp "$n.eps" "../${n%%_*}.eps" && echo "写した: ../${n%%_*}.eps"
echo "完了: $n.eps  $n.png（合計 $(( $(date +%s) - t0 )) 秒）"
