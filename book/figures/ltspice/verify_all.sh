#!/usr/bin/env bash
# 配布する LTspice 回路図（.asc）が，対応するネットリスト（.net）と
# 同じ回路を表しているかを機械照合する。
#
#   .asc は座標だけのテキストで，つながっているかは書かれていない。
#   座標が1つずれても構文エラーは出ず，図もほとんど同じに見えるので，
#   目で見て確かめることはできない。必ずこのスクリプトを通すこと。
#
# 使い方:  bash verify_all.sh
# 終了値:  全件 PASS なら 0，1件でも FAIL なら 1
set -u
cd "$(dirname "$0")"
T="netlist-to-schematic/tools/net2asc.py"
pass=0; fail=0; skip=0
for n in chapter*/*.net; do
  a="${n%.net}.asc"
  [ -f "$a" ] || { echo "SKIP $n  （.asc がない）"; skip=$((skip+1)); continue; }
  if out=$(python3 "$T" "$n" --check "$a" 2>&1); then
    echo "PASS $a"; pass=$((pass+1))
  else
    echo "FAIL $a"; fail=$((fail+1))
    echo "$out" | grep -iE 'MISMATCH|ERROR|MISSING|ADDED|Unknown' | head -4 | sed 's/^/       /'
  fi
done
echo "---- PASS=$pass FAIL=$fail SKIP=$skip ----"
[ "$fail" -eq 0 ]
