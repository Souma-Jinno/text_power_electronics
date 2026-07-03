#!/bin/bash
# render.sh — TikZ 図（jarticle ベース）を EPS に変換する共通スクリプト
# 使い方: ./render.sh fig1.1   （fig1.1.tex → ../fig1.1.eps）
#         ./render.sh all      （scripts/ 内の全 fig*.tex を変換）
#
# 経路: platex → dvips で PS 化 → eps2eps でインクにタイトクロップ →
#        gs(eps2write,-dEPSCrop) で BoundingBox を原点 (0,0) に正規化。
#   ・標準の standalone+preview は platex（dvips ドライバ）下で tikzpicture の
#     バウンディングボックスを正しく測れなかったため，jarticle に普通に
#     組版して eps2eps でクロップする方式に統一している。
#   ・dvipdfmx は BoundingBox の原点が (0,0) でない EPS を取り込めない
#     （図が空白になる）ため，最後に gs で原点正規化する。
#   ・このため図中の文字は数式・英数字のみとし，和文ラベルは入れない
#     （eps2write 経路が和文グリフを保持できないため）。和文の説明は
#     キャプション側に書く。
#   生成 EPS は book/figures/ 直下に置き，本文から原寸・clip 付きで読み込む。
set -uo pipefail
TEXBIN=/Library/TeX/texbin
EPS2EPS=/usr/local/bin/eps2eps
GS=/usr/local/bin/gs
SCRIPTDIR="$(cd "$(dirname "$0")" && pwd)"
OUTDIR="$(cd "$SCRIPTDIR/.." && pwd)"

render_one() {
  local base="$1"
  cd "$SCRIPTDIR"
  echo "--- $base ---"
  ${TEXBIN}/platex -interaction=nonstopmode -halt-on-error "${base}.tex" > "${base}.build.log" 2>&1
  if [ ! -f "${base}.dvi" ]; then
    echo "ERROR: ${base}.dvi が生成されませんでした。ログ末尾:"
    tail -15 "${base}.build.log"
    return 1
  fi
  ${TEXBIN}/dvips -o "${base}.ps" "${base}.dvi" > "${base}.dvips.log" 2>&1
  ${EPS2EPS} "${base}.ps" "${base}.crop.eps" > "${base}.crop.log" 2>&1
  # BoundingBox を原点 (0,0) に正規化（dvipdfmx 取り込み用）
  ${GS} -q -dNOPAUSE -dBATCH -dEPSCrop -sDEVICE=eps2write \
        -sOutputFile="${OUTDIR}/${base}.eps" "${base}.crop.eps" -c quit \
        > "${base}.norm.log" 2>&1
  if [ ! -f "${OUTDIR}/${base}.eps" ]; then
    echo "ERROR: ${base}.eps が生成されませんでした"
    return 1
  fi
  grep "%%BoundingBox" "${OUTDIR}/${base}.eps" | head -1
  rm -f "${base}.ps" "${base}.crop.eps"
}

if [ "${1:-}" = "all" ]; then
  for f in "$SCRIPTDIR"/fig*.tex; do
    b="$(basename "$f" .tex)"
    render_one "$b" || exit 1
  done
else
  render_one "$1" || exit 1
fi
echo "完了"
