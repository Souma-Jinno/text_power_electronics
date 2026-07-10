#!/bin/bash
# build.sh — コロナ社テンプレート pLaTeX ビルドスクリプト
# 手順: platex(2回) → mendex(corona+.ist) → platex → dvipdfmx
# 注: dvips+ps2pdf 経路は corona クラスの jis/jisg フォントの和文が
#     文字化けする（マップ不足）。校正PDFは dvipdfmx で生成する。
#     出版社入稿は TeX ソース+EPS 一式なので dvips 経路の解決は不要。

set -euo pipefail

# OS 非依存化: PATH に platex があればそれを使い（Linux/TeX Live 等）、
# 無ければ macOS の既定パス /Library/TeX/texbin にフォールバックする。
if command -v platex >/dev/null 2>&1; then
    PLATEX=$(command -v platex)
    DVIPDFMX=$(command -v dvipdfmx)
    MENDEX=$(command -v mendex)
else
    TEXBIN=/Library/TeX/texbin
    PLATEX=${TEXBIN}/platex
    DVIPDFMX=${TEXBIN}/dvipdfmx
    MENDEX=${TEXBIN}/mendex
fi

MAIN=main
WORKDIR="$(cd "$(dirname "$0")" && pwd)"
cd "$WORKDIR"

# エラー時にlogの該当行を表示する関数
show_log_errors() {
    local logfile="$1"
    if [ -f "$logfile" ]; then
        echo "---------- ログのエラー・警告行 ----------"
        grep -n -E "^(! |.*Error|.*Warning)" "$logfile" | head -30 || true
        echo "-------------------------------------------"
    fi
}

echo "=== [1/5] platex 1回目 ==="
if ! ${PLATEX} -interaction=nonstopmode -halt-on-error ${MAIN}.tex; then
    echo "ERROR: platex 1回目 失敗"
    show_log_errors "${MAIN}.log"
    exit 1
fi

echo "=== [2/5] platex 2回目（相互参照解決） ==="
if ! ${PLATEX} -interaction=nonstopmode -halt-on-error ${MAIN}.tex; then
    echo "ERROR: platex 2回目 失敗"
    show_log_errors "${MAIN}.log"
    exit 1
fi

echo "=== [3/5] mendex（索引生成，corona+.ist 使用） ==="
${MENDEX} -s corona+.ist -o ${MAIN}.ind ${MAIN}.idx || true
# 索引エントリが0件の場合 mendex は exit 255 を返し .ind を生成しない。
# platex が \printindex で .ind を要求するので空ファイルを用意する。
if [ ! -f ${MAIN}.ind ]; then
    echo "(索引エントリなし: 空の .ind を生成します)"
    touch ${MAIN}.ind
fi

echo "=== [4/5] platex 3回目（索引反映） ==="
if ! ${PLATEX} -interaction=nonstopmode -halt-on-error ${MAIN}.tex; then
    echo "ERROR: platex 3回目 失敗"
    show_log_errors "${MAIN}.log"
    exit 1
fi

echo "=== [5/5] dvipdfmx ==="
if ! ${DVIPDFMX} -o ${MAIN}.pdf ${MAIN}.dvi; then
    echo "ERROR: dvipdfmx 失敗"
    exit 1
fi

echo ""
echo "=== ビルド完了 ==="
echo "出力: ${WORKDIR}/${MAIN}.pdf"
ls -lh "${MAIN}.pdf"
