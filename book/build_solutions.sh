#!/bin/bash
# build_solutions.sh — Webで配布する別冊解答をビルドする。
# 本文の式・図・節番号を xr で参照するので，先に ./build.sh を通して
# main.aux を最新にしておくこと。
set -euo pipefail
WORKDIR="$(cd "$(dirname "$0")" && pwd)"
cd "$WORKDIR"

if [ ! -f main.aux ]; then
    echo "ERROR: main.aux がありません。先に ./build.sh を実行してください。"
    exit 1
fi

if command -v platex >/dev/null 2>&1; then
    PLATEX=$(command -v platex); DVIPDFMX=$(command -v dvipdfmx)
else
    PLATEX=/Library/TeX/texbin/platex; DVIPDFMX=/Library/TeX/texbin/dvipdfmx
fi

for i in 1 2; do
    echo "=== platex ${i}回目 ==="
    if ! ${PLATEX} -interaction=nonstopmode -halt-on-error solutions.tex; then
        echo "ERROR: platex 失敗"
        grep -n -E "^(! |.*Error)" solutions.log | head -20 || true
        exit 1
    fi
done
${DVIPDFMX} -o solutions.pdf solutions.dvi
echo "=== 完了 ==="
ls -lh solutions.pdf
