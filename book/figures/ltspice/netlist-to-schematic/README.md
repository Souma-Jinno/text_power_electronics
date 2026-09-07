# netlist-to-schematic

ngspice のネットリスト（`.cir`）から、**接続の正しさを機械的に検証した** LTspice 回路図（`.asc`）を生成するツール一式と、その使い方を定めた skill。

---

## なぜこれがあるのか

LTspice の `.asc` は**座標だけのテキストファイル**で、接続情報は書かれていない。接続は座標の一致から創発する。

つまり——

- 座標を1つ間違えても**構文エラーは出ない**。図もほぼ同じに見える。ネットが静かに切れるだけ
- 局所的に見ても誤りが分からない（1行だけ見て正しいか判定できない）

**だから LLM に座標を直接書かせるのは無謀である。** このパッケージは、その代わりに

1. 接続（ネットリスト）を先に決める
2. 座標は**決定論的なコード**に計算させる
3. 生成物からネットリストを抽出し直し、原本と**機械照合**する

という順序を強制する。LLM は座標を1つも書かない。

---

## 導入

```
netlist-to-schematic/
  SKILL.md          ← エージェントへの指示書（これが skill 本体）
  README.md         ← このファイル
  CHANGELOG.md      ← 三度の独立監査で何が見つかり、何を直したかの履歴
  NET2ASC.md        ← 設計方針・検出可否の全表・監査記録
  tools/            ← 実体（約5,000行）
    net2asc.py        生成＋検証
    asc2ngspice.py    逆変換（ラウンドトリップの相手）
    asc2svg.py        レンダラ
    ltsym/*.asy       シンボル定義10個（res, cap, ind, ind2, diode, voltage,
                      sw, nmos, pmos, Misc/jumper）。これが無いとピン座標が
                      計算できない
  examples/         ← 動作確認用ネットリスト
  tests/            ← 負の対照実験＋セルフテスト
```

**依存関係はほぼ無い。** Python 3 の標準ライブラリのみで動く。
**唯一の例外が PNG 出力で、これだけ `cairosvg` に依存する。**
無ければ SVG のみ生成してその旨を表示する。
その場合 **「図を目で見る」手順は実施できない**ので、SKILL.md 手順2の
「PNG が作れないとき」に従い、**目視未実施であることを報告に明記する**こと
（SVG のテキストを読んだだけで「図を確認した」と書いてはいけない）。

### `examples/buck_sync.cir` はそのままではシミュレーションできない

このデッキは `.include models/mosfet_real.lib`（`.subckt SR_80 d g s` の定義）を必要とするが、
**そのライブラリは同梱していない**（作者の素子モデリング成果物であり、配布対象外）。

- **変換・検証・レンダリングには影響しない。** `SR_80` は既知の3端子ラッパ名なので
  `XM1`/`XM2` は MOSFET シンボルとして描かれ、ラウンドトリップも PASS する。
  このファイルの役割は「変換の例」であり、その役割は果たす。
- **ngspice で走らせることはできない。** `.include` の行で止まる。
  走らせたい場合は、同じインスタンスパラメータを取る 80 V N-MOSFET の
  マクロモデル（`.subckt SR_80 d g s`）を自分で用意し、そのパスに置くこと。
- ファイル冒頭の該当箇所にも同じ注意書きがある。

`tools/` の各スクリプトは `ltsym/` を**自分の隣**から探すので、`tools/` ごと好きな場所へ置いてよい。

### skill として登録する場合

`SKILL.md` を `.claude/skills/netlist-to-schematic/SKILL.md` に置く。
その際、`SKILL.md` 内の `$TOOLS` を実際の `tools/` の絶対パスに読み替えるか、
冒頭にパスを明記した1行を足しておくと確実。

---

## まず動作確認

```
bash tests/selftest.sh            # または  bash tests/selftest.sh /path/to/python
```

**19項目すべて OK になることを確認してから使うこと。** 特に「2) 負の対照実験」が重要で、
ここが FAIL していない場合、**検査器は「常に PASS を返すだけの飾り」**になっている。
負の対照は exit コードだけでなく**出るべきメッセージまで**照合しているので、
別の理由で偶然 FAIL したものは合格にならない。

期待される出力：

```
1) ラウンドトリップ（PASS・exit 0 になるべき）
  [OK]   buck_sync  (layout : v2 FLOW)
  [OK]   rectenna_harvester  (layout : v2b SPINE)

2) 負の対照実験（FAIL・exit 1 になるべき）
  [OK]   corrupt_A_midflag.asc が「SHORT: nets 'sw', 'vout' are ONE connected component」で検出された (exit=1)
  [OK]   corrupt_B_tjunction.asc が「SHORT: nets 'sw', 'vout' are ONE connected component」で検出された (exit=1)
  [OK]   corrupt_C_value.asc が「MISMATCH: L1: VALUE」で検出された (exit=1)
  [OK]   corrupt_D_netrename.asc が「DANGLING NET REFERENCE」で検出された (exit=1)
  [OK]   corrupt_E_spiceline.asc が「MISMATCH: CSN: VALUE '{Csnb}' -> '{Csnb} Rpar=0.001'」で検出された (exit=1)
  [OK]   corrupt_F_value2.asc が「MISMATCH: VSRC: VALUE 'DC {Vin_dc}' -> 'DC {Vin_dc} AC 10'」で検出された (exit=1)
  [OK]   corrupt_G_kcoeff.asc が「K K1 COUPLING COEFFICIENT '{K_VALUE}' -> '0.001'」で検出された (exit=1)
  [OK]   corrupt_H_trandel.asc が「DIRECTIVE MISSING FROM .asc (1 card(s)): .tran 1u 1m」で検出された (exit=1)
  [OK]   corrupt_I_icdel.asc が「DIRECTIVE MISSING FROM .asc (1 card(s)): .ic v(mid)=2」で検出された (exit=1)
  [OK]   corrupt_J_unknownattr.asc が「ERROR: Cout1: SYMATTR SpiceModel is not understood」で検出された (exit=1)
  [OK]   無傷の buck_sync.asc は PASS（負の対照が「常に FAIL」ではない）
  [OK]   無傷の rectenna_harvester.asc は PASS（負の対照が「常に FAIL」ではない）
  [OK]   無傷の directive_test.asc は PASS（負の対照が「常に FAIL」ではない）
  [OK]   dup_test.cir（素子名重複）が検出された
  [OK]   case_test.cir が1ノードに統合され注記が出た

  [OK]   未定義パラメータが標準出力に出た（undefined params: RL_VALUE, TSTOP, K_VALUE ）

  [OK]   asc2ngspice.py 生成デッキと照合しても無傷の .asc は PASS（偽 FAIL の再発なし）
  [OK]   tran削除 が「DIRECTIVE MISSING FROM .asc (1 card(s)): .tran 1u 1m 0 1u uic」で検出された (exit=1)
  [OK]   複数代入から1個削除 が「DIRECTIVE MISSING FROM .asc (1 card(s)): .param spare=3」で検出された (exit=1)
  [OK]   パラメータ値の改変 が「DIRECTIVE ADDED TO .asc (1 card(s)): .param eta=0.5」で検出された (exit=1)
  [OK]   カードの追加 が「DIRECTIVE ADDED TO .asc (1 card(s)): .ic v(mid)=7」で検出された (exit=1)

  [OK]   素子値の中の η も eta に揃った（定義と参照の綴りが一致）
  [OK]   生成デッキを ngspice が読めた（Undefined parameter が出ない）
  [OK]   値の接尾辞 U+03BC が u に正規化された（1μ→1u。放置すると 10^6 倍ずれる）
  [OK]   訳しようのない非ASCII（Ω）が ERROR で拒否された (exit=1)

3) 決定論（2回生成してバイト一致するべき）
  [OK]   バイト一致

  PASS: 28   FAIL: 0
```

セルフテストは中間ファイルを一時ディレクトリに書くので、**走らせてもパッケージは汚れない。**

---

## 使い方

```bash
# 生成＋検証（同時に走る）
python3 tools/net2asc.py 入力.cir -o 出力.asc

# 図として見る
python3 tools/asc2svg.py 出力.asc -o 出力.svg --png 出力.png

# 既存の .asc を検査するだけ
python3 tools/net2asc.py 入力.cir --check 既存.asc
```

`VERIFY: PASS` なら接続が一致。`VERIFY: FAIL` なら**そこで止まること**。

---

## この道具が保証すること・しないこと

**保証する**：生成された `.asc` の接続が、入力ネットリストと一致すること（端子順まで含む全単射）。

**保証しない**：

| | |
|---|---|
| 図の可読性 | レイアウトによっては読めない（`v1 GRID` は配線ゼロ） |
| **回路の電気的妥当性** | **接続が正しくても回路が壊れていることはある** |
| LTspice で開けるか | 接触規則は仕様からの再実装。LTspice 本体と照合したことは一度もない |

### 実例

このツールで描いた降圧コンバータ（48V→12V/10A）は、**接続は完全に正しかった**が、
ローサイド MOSFET を毎サイクル アバランシェ降伏させる設計だった。
スイッチノードは 200V 超（素子定格は 80V）。

**接続の検証では絶対に見つからない。**
見つけたのは**エネルギー保存の検算**だった——`Pin 117.45W < Pout 118.56W` は物理的にありえない。

誤りのクラスごとに、別の検出器が要る：

| 誤りのクラス | 検出手段 |
|---|---|
| 接続の誤り | **ラウンドトリップ照合（このツール）** |
| 設計の誤り | 物理の検算（エネルギー保存・定格との突き合わせ） |
| モデリングの誤り | データシートとの照合 |
| 計測の誤り | 桁の確認・タイムステップ収束の確認 |

---

## 既知の弱点

- **トランスがトランスとして描かれない**（一次と二次が別の島になる）
- ゲート駆動は島に分かれ、ラベル接続のまま
- 配置テンプレートは「4スイッチブリッジ＋結合インダクタ」1つのみ
- 文字の外接矩形は推定値で、LTspice の実描画とは未照合
- 交差配線にホップ記号を描かない
- 描画対象は R/C/L/D/V/S と3端子サブサーキットのみ（B/E/G/F/H はテキスト行になる）

詳細と全24クラスの検出可否表は `NET2ASC.md` を参照。

---

## 独立監査を受けている

このツールは三度、独立した監査エージェントに攻撃されている。その結果：

**2026-08-27（1回目）**

- **検査を素通りする改竄が3種類見つかった**（線分途中の FLAG、T字接続、素子値の改変）
- 原因は `--check` が幾何検査を呼んでいなかったこと、および照合の「権威」が LTspice の接触規則を一部しか実装していなかったこと
- 3種類とも塞ぎ、`tests/` の負の対照実験として**再発防止の証拠**にしてある

**2026-09-04（2回目）**

- **たった1本のネットを一貫改名しただけで素通りした。** 照合はネット名の全単射なので
  改名自体は正しく無視されるが、シンボルの無い素子（B ソース等）は TEXT ディレクティブとして
  `v(sw)` のように**ネットを名前で**参照しており、そちらが宙に浮いていた。
  → ディレクティブ／TEXT 行の中の `v(ネット)` `i(素子)` `@素子[..]` を図と照合するようにし、
  `tests/corrupt_D_netrename.asc` を負の対照実験に追加した。
- **`.asy` の `PINATTR SpiceOrder` を読んでいなかった**（`PIN` 行のファイル順を使い、
  それが SpiceOrder と等しいと仮定していた）。同梱の10シンボルは一致しているので実害は
  無かったが、食い違う合法な `.asy` を渡すと**全電源の極性が黙って反転**し、生成側と抽出側が
  同じ間違いをするためラウンドトリップは PASS した。
  → SpiceOrder を読むようにし、無い場合は NOTE、食い違う場合は WARNING を出す。
  この修正で 5 デッキの `.asc` は**バイト一致**（もともと一致していたため）。

**2026-09-04（3回目・再監査）**

前回の指摘が本当に直っていることを確認したうえで、**新しく3つ**見つかった。3つとも
`VERIFY: PASS` / exit 0 で素通りしていた。

- **`SYMATTR SpiceLine` / `Value2` を黙って捨てていた。** コンデンサに
  `SYMATTR SpiceLine Rpar=0.001` を足すと、LTspice ではそれが**1 mΩ の並列抵抗＝実質短絡**
  になるのに PASS。抽出器が `Rser`/`Lser` 以外のキーを一つ残らず捨て、`Value2` は
  一度も読んでいなかったため、**壊れた部分が比較器まで届いていなかった。**
  → 消費しなかった属性は素子カードに**そのまま付けて**比較に載せ、
  置き場所の無い `SYMATTR` は**拒否**するようにした（`corrupt_E` / `F` / `J`）。
- **`K` の結合係数を比較していなかった。** `{K_VALUE}` を `0.001` に書き換えて
  結合をほぼ 0 にしても PASS。結合する相手だけを比べ、係数は意図的に捨てていた。
  → 素子値と同じ正規化で比較するようにした（`corrupt_G`）。
- **ディレクティブの存在を比較していなかった。** `.tran` や `.ic` のカードを
  `.asc` から消しても PASS。文書化されていた除外は
  「`.model`/`.param`/`.options` の**中身**」であって削除ではなかった——
  **実装のほうが文書より緩かった。**
  → `.asc` が運んでいるディレクティブの多重集合を入力デッキと照合するようにした。
  副作用として `.model`/`.param`/`.options` の**中身も**比較できるようになった
  （`corrupt_H` / `I`）。

### 4回目（2026-09-05）— 見逃しではなく**偽 FAIL**

素通りは1件も出なかった（139本の `.asc` を旧版・新版で変換して比較し、
差が出た4本はどれも v1.3.0 の修正が効いた方向だった）。代わりに逆の欠陥が出た。

- **`asc2ngspice.py` が作ったデッキと照合すると、無傷の図面が FAIL した。**
  ディレクティブ比較が逐語だったため、`emit()` の書き換え（複数代入 `.param` の分解、
  `η`→`eta`、`.tran startup`→`uic`、`pi` と `.options` の注入）がすべて差として出る。
  PSFB の3図面では、素子52個・ネット32本が完全一致していても**30件**の
  「DIRECTIVE MISSING / ADDED」が出た。**常に FAIL する検査は読み飛ばされる**ので、
  これは偽陰性と同じくらい危険である。
  → 入力デッキが `asc2ngspice.py` の生成物のときだけ（先頭の provenance 行で判定）、
  比較の両辺を同じ翻訳器に通すようにした。人が書いたデッキ相手の比較は変えていない。
  緩めた側の修正なので負の対照を追加した（`tests/a2n_dir_test.cir`、セルフテスト 2c）。
- **ngspice が読めない綴りを PASS のまま持ち出していた。** `.param η=0.85` は
  `eta` に音訳していたが、素子値の中の `{1k*η}` は素通りしており、生成デッキは
  `eta` を定義して `η` を参照する状態になった。ngspice-41 は `Undefined parameter` で
  **止まる**のに `--check` は PASS——比較の両辺が同じ未翻訳の文字列を運ぶからである。
  同じ場所で `1μ`（U+03BC）が ngspice に **1.0** と読まれる（`1µ` U+00B5 は 1e-6）
  ＝黙って 10⁶ 倍ずれる罠も見つけた。
  → 曖昧でない音訳（`η`→`eta`、倍率接尾辞の `µ`/`μ`→`u`）をカード全体に一貫して掛け、
  残った非ASCII は**当てずっぽうで訳さず `ERROR`** にした（セルフテスト 2d）。
  本プロジェクトの `.asc` 191 本には該当が無く、**実際に壊れていたデッキは無い**。

> **記録**：それまで `SKILL.md` は「**素子値の改変**を捕まえる」と無条件に書いていた。
> B ソースのテキストカードの値は確かに比較されていたが、上の3つは比較されておらず、
> **この記述は言い過ぎだった。** 「値を比較している」は
> 「その値が比較器まで届いている」の証拠にならない。

「検査が通った」を信じてよいのは、**検査器自身が壊れていないことを確認したときだけ**。
それが `tests/selftest.sh` の「2)」が存在する理由。
