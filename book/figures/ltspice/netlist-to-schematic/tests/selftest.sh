#!/usr/bin/env bash
# netlist-to-schematic セルフテスト
#
# 使い方:  bash tests/selftest.sh  [python実行ファイル]
# 既定の python は python3。
#
# 合格条件:
#   1. examples/ のネットリストがラウンドトリップ PASS（exit 0）
#   2. tests/ の改竄ファイルがすべて FAIL（exit 1）  ← 検査器が形骸化していない証明
#   3. 2回生成した .asc がバイト一致（決定論）
#
# 2 が通らない場合、検査は「常に PASS を返すだけの飾り」になっている。
# そのときは結果を信用してはいけない。

set -u
PY="${1:-python3}"
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$HERE")"
TOOLS="$ROOT/tools"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

pass=0; fail=0
ok()   { echo "  [OK]   $1"; pass=$((pass+1)); }
ng()   { echo "  [FAIL] $1"; fail=$((fail+1)); }

echo "python : $PY"
echo "tools  : $TOOLS"
echo "work   : $WORK"
echo

# ---------------------------------------------------------------- 1. 正常系
echo "1) ラウンドトリップ（PASS・exit 0 になるべき）"
for cir in "$ROOT"/examples/*.cir; do
  n="$(basename "$cir" .cir)"
  "$PY" "$TOOLS/net2asc.py" "$cir" -o "$WORK/$n.asc" >"$WORK/$n.log" 2>&1
  rc=$?
  if [ "$rc" -eq 0 ] && grep -q "VERIFY: PASS" "$WORK/$n.log"; then
    lay=$(grep -o 'layout : [^ ]*\( [A-Z]*\)\?' "$WORK/$n.log" | head -1)
    ok "$n  ($lay)"
  else
    ng "$n  exit=$rc"; sed 's/^/       /' "$WORK/$n.log" | tail -5
  fi
done
echo

# ------------------------------------------------- 2. 負の対照実験（本命）
echo "2) 負の対照実験（FAIL・exit 1 になるべき）"
BUCK="$ROOT/examples/buck_sync.cir"
# --rt を $WORK に向けるのは意図的：既定のままだと tests/ に *_rt.cir が
# 書き戻され、セルフテストを走らせるだけでパッケージが汚れる（2026-09-04 監査 C3）。
#
# 各行 = 「壊した .asc | 照合先のネットリスト | 出ていなければならないメッセージ」。
# exit!=0 だけでは足りない。**別の理由で偶然 FAIL しても合格にしてはいけない**ので、
# その改竄でしか出ないメッセージまで確認する（corrupt_D で確立したやり方）。
NEG="\
corrupt_A_midflag.asc|examples/buck_sync.cir|SHORT: nets 'sw', 'vout' are ONE connected component
corrupt_B_tjunction.asc|examples/buck_sync.cir|SHORT: nets 'sw', 'vout' are ONE connected component
corrupt_C_value.asc|examples/buck_sync.cir|MISMATCH: L1: VALUE
corrupt_D_netrename.asc|examples/buck_sync.cir|DANGLING NET REFERENCE
corrupt_E_spiceline.asc|examples/buck_sync.cir|MISMATCH: CSN: VALUE '{Csnb}' -> '{Csnb} Rpar=0.001'
corrupt_F_value2.asc|examples/buck_sync.cir|MISMATCH: VSRC: VALUE 'DC {Vin_dc}' -> 'DC {Vin_dc} AC 10'
corrupt_G_kcoeff.asc|examples/rectenna_harvester.cir|K K1 COUPLING COEFFICIENT '{K_VALUE}' -> '0.001'
corrupt_H_trandel.asc|tests/directive_test.cir|DIRECTIVE MISSING FROM .asc (1 card(s)): .tran 1u 1m
corrupt_I_icdel.asc|tests/directive_test.cir|DIRECTIVE MISSING FROM .asc (1 card(s)): .ic v(mid)=2
corrupt_J_unknownattr.asc|examples/buck_sync.cir|ERROR: Cout1: SYMATTR SpiceModel is not understood"

echo "$NEG" | while IFS='|' read -r n deck want; do
  [ -n "$n" ] || continue
  bad="$HERE/$n"
  if [ ! -f "$bad" ]; then ng "$n が見つからない"; continue; fi
  "$PY" "$TOOLS/net2asc.py" "$ROOT/$deck" --check "$bad" --rt "$WORK/$n.rt.cir" \
       >"$WORK/$n.log" 2>&1
  rc=$?
  if [ "$rc" -eq 0 ]; then
    ng "$n が素通りした ← 検査器が壊れている"
  elif grep -qF "$want" "$WORK/$n.log"; then
    ok "$n が「$want」で検出された (exit=$rc)"
  else
    ng "$n は FAIL したが理由が違う（期待: $want）← その検査は働いていない"
    sed 's/^/       /' "$WORK/$n.log" | tail -6
  fi
done > "$WORK/neg.out" 2>&1
cat "$WORK/neg.out"
# パイプ内の while はサブシェルなので pass/fail の加算が親に戻らない。集計し直す。
pass=$((pass + $(grep -c '^  \[OK\]' "$WORK/neg.out")))
fail=$((fail + $(grep -c '^  \[FAIL\]' "$WORK/neg.out")))

# 壊していない .asc は PASS でなければならない（上の検査が「常に FAIL」でない証明）。
for pair in "examples/buck_sync.cir" "examples/rectenna_harvester.cir" \
            "tests/directive_test.cir"; do
  b="$(basename "$pair" .cir)"
  "$PY" "$TOOLS/net2asc.py" "$ROOT/$pair" -o "$WORK/$b.pos.asc" \
       --rt "$WORK/$b.pos.rt.cir" >"$WORK/$b.pos.log" 2>&1
  "$PY" "$TOOLS/net2asc.py" "$ROOT/$pair" --check "$WORK/$b.pos.asc" \
       --rt "$WORK/$b.pos2.rt.cir" >>"$WORK/$b.pos.log" 2>&1
  if [ $? -eq 0 ]; then ok "無傷の $b.asc は PASS（負の対照が「常に FAIL」ではない）"
  else ng "無傷の $b.asc が FAIL した ← 誤検出"; sed 's/^/       /' "$WORK/$b.pos.log" | tail -6; fi
done

# 素子名の重複も FAIL するべき
if [ -f "$HERE/dup_test.cir" ]; then
  "$PY" "$TOOLS/net2asc.py" "$HERE/dup_test.cir" -o "$WORK/dup.asc" >"$WORK/dup.log" 2>&1
  rc=$?
  if [ "$rc" -ne 0 ]; then ok "dup_test.cir（素子名重複）が検出された"
  else ng "dup_test.cir が素通りした"; fi
fi

# 大小文字違いのネット名は「1ノードに統合＋注記」で PASS が正しい
if [ -f "$HERE/case_test.cir" ]; then
  "$PY" "$TOOLS/net2asc.py" "$HERE/case_test.cir" -o "$WORK/case.asc" >"$WORK/case.log" 2>&1
  if grep -qi "NOTE" "$WORK/case.log" && grep -q "VERIFY: PASS" "$WORK/case.log"; then
    ok "case_test.cir が1ノードに統合され注記が出た"
  else
    ng "case_test.cir の大小文字統合が働いていない"
  fi
fi
echo

# ---------------------------------------- 2b. 未定義パラメータが標準出力に出るか
# （2026-09-04 監査 D1: 以前は .asc の中の TEXT にしか書かれておらず、
#   SKILL.md の手順どおり標準出力だけを読むエージェントには見えなかった）
RTF="$ROOT/examples/rectenna_harvester.cir"
if [ -f "$RTF" ]; then
  "$PY" "$TOOLS/net2asc.py" "$RTF" -o "$WORK/und.asc" >"$WORK/und.log" 2>&1
  if grep -q "undefined params:" "$WORK/und.log"; then
    ok "未定義パラメータが標準出力に出た（$(grep -o 'undefined params: [^(]*' "$WORK/und.log" | head -1)）"
  else
    ng "未定義パラメータが標準出力に出ていない"
  fi
fi
echo

# ------------------- 2c. asc2ngspice.py が作ったデッキと照合する方向
# （2026-09-05 監査 audit_fable4）
# 2 の負の対照はすべて「人が書いた .cir と、そこから net2asc.py が描いた .asc」
# の向きで、この向きではディレクティブは逐語コピーなので集合比較がそのまま成り立つ。
# 逆向き――.asc と、その .asc から asc2ngspice.py が作ったデッキ――では逐語ではない：
# 複数代入 .param の分解、η→eta、.tran startup→uic、pi と .options の注入がかかる。
# 修正前はこの向きで無傷の図面が FAIL した（PSFB 3図面で偽メッセージ 30件）。
# ここで確かめるのは2つ：無傷なら PASS になること（偽陽性の再発防止）と、
# それでも改竄は依然すべて捕まること（緩めた結果、検査が骨抜きになっていない証明）。
A2N="$HERE/a2n_dir_test.cir"
if [ -f "$A2N" ]; then
  "$PY" "$TOOLS/net2asc.py" "$A2N" -o "$WORK/a2n.asc" --rt "$WORK/a2n.rt.cir" \
       >"$WORK/a2n.gen.log" 2>&1
  "$PY" "$TOOLS/asc2ngspice.py" "$WORK/a2n.asc" -o "$WORK/a2n.gen.cir" \
       >>"$WORK/a2n.gen.log" 2>&1

  # (1) 無傷 → PASS
  "$PY" "$TOOLS/net2asc.py" "$WORK/a2n.gen.cir" --check "$WORK/a2n.asc" \
       --rt "$WORK/a2n.pos.rt.cir" >"$WORK/a2n.pos.log" 2>&1
  if [ $? -eq 0 ]; then
    ok "asc2ngspice.py 生成デッキと照合しても無傷の .asc は PASS（偽 FAIL の再発なし）"
  else
    ng "無傷の .asc が生成デッキ相手に FAIL した ← 偽検出の再発"
    grep -E 'DIRECTIVE|MISMATCH' "$WORK/a2n.pos.log" | sed 's/^/       /' | head -6
  fi

  # (2) 改竄はこの向きでも捕まること。各行 = 改竄名|python の書き換え式|出るべきメッセージ
  #     （書き換えは UTF-16LE の .asc をテキストとして扱う。$SRC/$DST は下の python が渡す）
  A2NNEG="
tran削除|[l for l in L if '!.tran' not in l]|DIRECTIVE MISSING FROM .asc (1 card(s)): .tran 1u 1m 0 1u uic
複数代入から1個削除|[l.replace('b1=1 c1=a1/b1 spare=3','b1=1 c1=a1/b1') for l in L]|DIRECTIVE MISSING FROM .asc (1 card(s)): .param spare=3
パラメータ値の改変|[l.replace('!.param η=0.85','!.param η=0.5') for l in L]|DIRECTIVE ADDED TO .asc (1 card(s)): .param eta=0.5
カードの追加|L[:1]+['TEXT 0 500 Left 2 !.ic v(mid)=7']+L[1:]|DIRECTIVE ADDED TO .asc (1 card(s)): .ic v(mid)=7
"
  echo "$A2NNEG" | while IFS='|' read -r nm expr want; do
    [ -z "$nm" ] && continue
    "$PY" - "$WORK/a2n.asc" "$WORK/a2n.$$.asc" "$expr" <<'EOPY'
import sys
src, dst, expr = sys.argv[1], sys.argv[2], sys.argv[3]
L = open(src, encoding='utf-16-le').read().replace('\r\n', '\n').split('\n')
out = eval(expr, {'L': L})
assert out != L, 'tamper expression changed nothing: ' + expr
open(dst, 'wb').write('\n'.join(out).encode('utf-16-le'))
EOPY
    if [ $? -ne 0 ]; then ng "$nm: 改竄ファイルを作れなかった"; continue; fi
    "$PY" "$TOOLS/net2asc.py" "$WORK/a2n.gen.cir" --check "$WORK/a2n.$$.asc" \
         --rt "$WORK/a2n.neg.rt.cir" >"$WORK/a2n.neg.log" 2>&1
    rc=$?
    if [ "$rc" -eq 0 ]; then
      ng "$nm が生成デッキ相手に素通りした ← 検査が骨抜き"
    elif grep -qF "$want" "$WORK/a2n.neg.log"; then
      ok "$nm が「$want」で検出された (exit=$rc)"
    else
      ng "$nm は FAIL したが理由が違う（期待: $want）"
      grep -E 'DIRECTIVE|MISMATCH' "$WORK/a2n.neg.log" | sed 's/^/       /' | head -4
    fi
  done >"$WORK/a2nneg.out" 2>&1
  cat "$WORK/a2nneg.out"
  pass=$((pass + $(grep -c '^  \[OK\]' "$WORK/a2nneg.out")))
  fail=$((fail + $(grep -c '^  \[FAIL\]' "$WORK/a2nneg.out")))
fi
echo

# ------------------- 2d. ngspice が読めない綴りを持ち込まないこと
# （2026-09-05 監査 audit_fable4 E1）
# `.param η=0.85` は `eta` に音訳されていたが、素子値の中の `{1k*η}` は素通りしていた。
# 生成デッキは eta を定義して η を参照する状態になり、ngspice は
# 「Undefined parameter」で止まるのに、--check は PASS と言っていた
# （比較の両辺が同じ未翻訳の文字列を運ぶので差が出ない）。走らないデッキは PASS ではない。
# ついでに U+03BC（ギリシャ文字μ）も潰す：ngspice-41 では `1μ` が **1.0** と解釈され
# （警告のみ）、`1µ`（U+00B5）だけが 1e-6 になる＝黙って 10^6 倍ずれる。
if [ -f "$WORK/a2n.asc" ]; then
  "$PY" - "$WORK" <<'EOPY'
import sys
W = sys.argv[1]
L = open(W + '/a2n.asc', encoding='utf-16-le').read().replace('\r\n', '\n').split('\n')
def w(name, ls, why):
    assert ls != L, why
    open(W + '/' + name, 'wb').write('\n'.join(ls).encode('utf-16-le'))
# η を素子値の中でも使う（定義側は .asc がもともと持っている）
w('a2n_eta.asc', [l.replace('SYMATTR Value {Rload}', 'SYMATTR Value {Rload*η}') for l in L],
  'eta tamper matched nothing')
# 値の接尾辞にギリシャ文字μ
w('a2n_mu.asc', [l.replace('SYMATTR Value 1u', 'SYMATTR Value 1μ') for l in L],
  'mu tamper matched nothing')
# 音訳のしようがない非ASCII（Ω）
w('a2n_ohm.asc', [l.replace('SYMATTR Value 1k', 'SYMATTR Value 10Ω') for l in L],
  'ohm tamper matched nothing')
EOPY
  if [ $? -ne 0 ]; then ng "2d の入力を作れなかった"; fi

  # (1) η は素子値の中でも eta に揃うこと（揃わなければデッキは走らない）
  "$PY" "$TOOLS/asc2ngspice.py" "$WORK/a2n_eta.asc" -o "$WORK/a2n_eta.cir" \
       >"$WORK/a2n_eta.log" 2>&1
  if grep -q '{Rload\*eta}' "$WORK/a2n_eta.cir" && ! grep -q 'η' "$WORK/a2n_eta.cir"; then
    ok "素子値の中の η も eta に揃った（定義と参照の綴りが一致）"
  else
    ng "素子値の中の η が音訳されていない ← 走らないデッキが出る"
    grep -n 'Rload' "$WORK/a2n_eta.cir" | sed 's/^/       /' | head -3
  fi

  # (1b) 実機確認：ngspice があるなら、そのデッキが本当に読めること
  # （exit code は見ない。この小さなデッキには .print が無いので ngspice は
  #   「no simulations run」で非ゼロを返す。見たいのは綴りが読めたかどうかである）
  if command -v ngspice >/dev/null 2>&1; then
    ngspice -b "$WORK/a2n_eta.cir" >"$WORK/a2n_eta.ng.log" 2>&1
    if grep -qiE 'undefined parameter|cannot compute substitute|fatal error' \
            "$WORK/a2n_eta.ng.log"; then
      ng "生成デッキを ngspice が読めなかった"
      grep -iE 'undefined|substitute|error' "$WORK/a2n_eta.ng.log" | sed 's/^/       /' | head -3
    else
      ok "生成デッキを ngspice が読めた（Undefined parameter が出ない）"
    fi
  fi

  # (2) 値の接尾辞のギリシャ文字μ は u になること（1μ が 1.0 と読まれる事故を防ぐ）
  "$PY" "$TOOLS/asc2ngspice.py" "$WORK/a2n_mu.asc" -o "$WORK/a2n_mu.cir" \
       >"$WORK/a2n_mu.log" 2>&1
  if grep -qE '^C1 .* 1u$' "$WORK/a2n_mu.cir"; then
    ok "値の接尾辞 U+03BC が u に正規化された（1μ→1u。放置すると 10^6 倍ずれる）"
  else
    ng "U+03BC が正規化されていない"
    grep -n '^C1' "$WORK/a2n_mu.cir" | sed 's/^/       /' | head -2
  fi

  # (3) 音訳のしようがない非ASCII は ERROR にして FAIL すること（当てずっぽうで訳さない）
  "$PY" "$TOOLS/net2asc.py" "$HERE/a2n_dir_test.cir" --check "$WORK/a2n_ohm.asc" \
       --rt "$WORK/a2n_ohm.rt.cir" >"$WORK/a2n_ohm.log" 2>&1
  rc=$?
  if [ "$rc" -ne 0 ] && grep -qF "U+03A9" "$WORK/a2n_ohm.log"; then
    ok "訳しようのない非ASCII（Ω）が ERROR で拒否された (exit=$rc)"
  else
    ng "非ASCII の値が素通りした (exit=$rc)"
    grep -E 'ERROR|VERIFY' "$WORK/a2n_ohm.log" | sed 's/^/       /' | head -3
  fi
fi
echo

# ---------------------------------------------------------------- 3. 決定論
echo "3) 決定論（2回生成してバイト一致するべき）"
"$PY" "$TOOLS/net2asc.py" "$BUCK" -o "$WORK/det1.asc" >/dev/null 2>&1
"$PY" "$TOOLS/net2asc.py" "$BUCK" -o "$WORK/det2.asc" >/dev/null 2>&1
if cmp -s "$WORK/det1.asc" "$WORK/det2.asc"; then ok "バイト一致"
else ng "出力が揺れている ← 決定論が壊れている"; fi
echo

# ---------------------------------------------------------------- 結果
echo "================================"
echo "  PASS: $pass   FAIL: $fail"
echo "================================"
[ "$fail" -eq 0 ] || echo "!! FAIL があります。結果を信用しないでください。"
exit $([ "$fail" -eq 0 ] && echo 0 || echo 1)
