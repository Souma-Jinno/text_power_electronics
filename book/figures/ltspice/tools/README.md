# LTspice→SVG図生成パイプライン（book/figures/ltspice/）

先生指示(2026-07-17, `agent-logs/tasks/inbox/zimaboard/20260717_ltspice_asc_svg_pipeline_pwreletron.md`)
に基づく、教科書『パワーエレクトロニクス』の回路図をLTspiceネイティブの.ascから起こしてSVG化する
補助パイプライン。**本文・既存の掲載図(book/figures/fig*.eps)は変更しない**。あくまで
book/figures/ltspice/ 配下に独立の補助資料（.asc/.net/.raw/.svg一式 + book/verification/のHTML）
を積み上げるもの。

## 環境（このマシン=zimaboardでの実態）

- **wine / 実LTspice.exe は未導入**（`apt`/`wine`ともに本セッションのサンドボックス権限では
  導入試行不可）。よって `.asc → .net`（接続チェック）と `.asc → .raw`（波形）を
  LTspice本体で行うことはできない。
- 代わりに、依頼書のPhase 0が明示的に許可しているフォールバックを採用:
  1. **`asc_to_net.py`**: .ascを自前パースし、WIRE+シンボルピン+FLAGの座標を
     Union-Findで結線してSPICEネットリスト(.net)を出力。未接続ピン・GND欠落を検出する
     簡易「接続チェック」を実装。
  2. **ngspice**（`/home/soumajinno/miniforge3/bin/ngspice`、rectenna broadband_loopで
     既に導入済みのものを流用）で `.net` をバッチ実行し `.raw` を生成。LTspice実機ではないが
     同じSPICE系列で物理的に妥当な波形が得られることを都度検算している。
  3. **`ltspice_to_svg`**（pip, `pip install --user ltspice-to-svg`）で `.asc → .svg`。
     このツールは実LTspiceのシンボルライブラリ(.asy)を必要とするが、本機にはそれも無いため、
     `symbols/` 配下に**独自の最小限.asyシンボル**（voltage/res/diode）を作成して使用している。
     LTspice実物のアートワークの複製ではなく、機能的に等価な自作シンボル(白背景+シンプルな線画)。

## 使い方

新しい回路を1つ作るときの流れ:

1. `chapterNN/xxx.asc` を作成（`SYMBOL_PINS`に登録済みのシンボル種別=
   voltage/current/res/diode/bjt_npn/bjt_pnp/mosfet_n のみ使用可。
   新しい部品が要る章では `asc_to_net.py` の `SYMBOL_PINS`/`SYMBOL_PREFIX` と `symbols/*.asy` を追加する）
2. `bash tools/run_pipeline.sh chapterNN/xxx.asc` で `.net`→ngspice `.raw`→`.svg` を一括生成
   （`asc_to_net.py`が接続チェックNGなら非ゼロ終了するので、このステップでコケたら.ascを直す）
3. 章が揃ったら `tools/gen_verification_html.py <章番号> <章タイトル> <spec.json>` で
   `book/verification/ltspice_chapterNN.html` を生成

## 既知の制約

- `asc_to_net.py`は自作パーサであり、実LTspiceの`-netlist`出力と1:1で同じではない
  （回転はR0/R90/R180/R270とM0/M90/M180/M270の一般式に対応済みだが、実機での動作確認はできていない）。
- 部品種別はチャプター1時点で voltage/res/diode の3種のみ。チャプター2で3端子素子(BJT/MOSFET)と
  電流源が必要になったため `bjt_npn`・`bjt_pnp`・`mosfet_n`・`current` の4種を追加した
  （2026-07-17）。mosfet_nはD/G/S/Bの4ノードを持つが、SYMBOL_PINSでB座標をS座標と全く同じ点に
  重ねることでUnion-Findが自動的にB=Sとして結線する（特別なコード分岐は追加していない）。
  チャプター3でインダクタと寄生容量素子(cap)を追加した（2026-07-17、下記2点参照）。
  5章以降で変圧器等が要る際も同じパターンで`.asy`と`SYMBOL_PINS`を追加する。
- **`.control`ブロックで内部デバイス電流(`@d1[id]`等)を`wrdata`/`print`する場合は、必ず
  `tran`/`dc`より前に`save all @d1[id]`（またはそのパラメータを明示指定した`save`）を置くこと**
  （2026-07-17、chapter03図監査で発見）。`save`せずに`wrdata ... @d1[id]`だけ書くと、ngspiceは
  エラーを出さずに**トランジェント解析中ずっとt=0のDC動作点の値で固定した列**を出力する
  （chapter03のswitching_loss_double_pulseで実際に発生: ダイオード電流が全時刻14.19Aの定数に
  なり、後処理のKCL計算 i_sw=i(L1)-i(D1) が常時マイナスという物理的にありえない値になっていた）。
  rectenna broadband_loop（別リポ）の過去記録にも同じ罠の言及があり、艦を跨いで再発した既知の罠。
- **インダクタ性負荷をハードスイッチングする回路では、スイッチノードに寄生容量(Coss)が0だと
  ngspiceのニュートン法が収束せず桁違いの数値異常（chapter03で実測: 最大約109万A）を出すことが
  ある**（2026-07-17）。実デバイスのCoss・配線浮遊容量に相当する現実的な容量値（今回100pFでは
  不十分で470pFに増量）を`cap`シンボルでスイッチノード-GND間に追加すると収束する。ただし
  この容量値がターンオン/オフの実際の速度（≒スイッチング損失の絶対値）を支配してしまう副作用が
  あるため、教科書本文が仮定する理想的な切替時間との定量比較はできない旨をVERIFICATION_NOTES.md
  に明記すること（`chapter03/VERIFICATION_NOTES.md`参照）。
- `.control`/`.endc`ブロックを使うネットリスト（BJT/MOSFETの内部電流`@q1[ic]`等を`print`したい
  場合や、複数行のシミュレーション制御をまとめたい場合に必要）では、`run_pipeline.sh`の
  `ngspice -b -r <raw>`（-rフラグでの自動raw書き出し）と組み合わせると、このマシンでは
  ngspiceが「binary raw file "..."」とログに出すにもかかわらず実際には.rawファイルが
  生成されない現象を確認した（原因未特定、恐らく-rフラグと.controlブロック内の暗黙の
  自動再解析が競合している）。回避策として`run_pipeline.sh`は`.net`に`.control`があれば
  `-r`を付けずに`ngspice -b`のみで実行し、`.control`ブロック内に明示的な
  `write chapterNN/xxx.raw`コマンドを置く方式に統一した。新しい回路で`.control`ブロックを
  使う場合は、必ず末尾（`.endc`直前）に`write chapterNN/<回路名>.raw`を入れること。
- wine/実LTspiceが将来使えるようになった場合は、`asc_to_net.py`の出力とLTspice実機の`-netlist`
  出力を突き合わせて自作パーサの妥当性を再検証すること。
- **`.step param <name> list <v1> <v2> ...`はngspiceのバッチモード(`-b`)では動作しない**
  （`unimplemented control card`で即エラー、2026-07-17chapter07で発見。LTspice/ngspice対話
  モードでは動くはずだが、本パイプラインは常に`-b`で回している）。負荷/パラメータスイープが
  要る回路では、代わりに`.control`ブロック内で`alter <inst> = <値>`→`tran`をケースの数だけ
  繰り返し、最後に`write chapterNN/xxx.raw all`で全plotを1本の`.raw`にまとめるパターンを
  使うこと（chapter07の`linear_reg_zener.asc`/`linear_reg_opamp.asc`が実装例）。
- **ngspiceの`.op`は、電流無制限の理想E素子（下記opampシンボル参照）を含む回路では収束しない
  ことがある**（2026-07-18chapter07で発見）。`.tran`なら同じ回路が収束するため、DC動作点だけ
  見たい場合でも`.op`ではなく短い`.tran`を使うこと。
- **`opamp`シンボル（2026-07-18chapter07で追加）**: ngspiceに組み込みopamp素子が無いため、
  `asc_to_net.py`は`SYMBOL_PINS["opamp"]`(in+/in-/out の3ピン)を通常の素子と別扱いし、
  理想E素子`E<name> <out> 0 <in+> <in-> <gain>`（電流無制限の高ゲインVCVS、gain既定1e5）へ
  変換する。LTspiceの`UniversalOpamp2`（内部補償・出力飽和あり）の代替であり、飽和/GB積を
  再現しない点をそのシンボルを使う章のVERIFICATION_NOTES.mdに明記すること。
- **`zener`シンボル（2026-07-18chapter07で追加）**: footprintは`diode`と同一（2ピン、
  anode top/cathode bottom）だが`.asy`のカソードバーに折れ線を足して視覚的に区別。電気的には
  `.model <name> D(... BV=<Vz> IBV=<試験電流>)`のBV/IBVパラメータで逆方向降伏を表現する
  （ngspice標準diodeモデルの機能、新規SPICE素子は不要）。
- **`fix_viewbox.py`（2026-07-17、図監査で発見・追加）**: `ltspice_to_svg`のviewBox自動計算
  （site-packages内`ViewboxCalculator`）はwire/shape/symbol/flagの座標だけを見ており、
  `<text>`要素（回路上のTEXTコメント・SPICE directiveの表示）の実際の描画幅を一切考慮しない。
  そのため、コメント行を教科書的に詳しく書く（日本語を含む長い注記など）と、その行がSVGの
  viewBox右端をはみ出し、`overflow:hidden`のデフォルト挙動で**サイレントに読めなくなる**
  （chapter01の短い1行コメントでも実際に発生していたことを2026-07-17のchapter02図監査で発見、
  3回路とも遡って修正済み）。`run_pipeline.sh`は`asc→svg`の直後に自動で
  `fix_viewbox.py <svg>`を呼び、`<text>`の内容とfont-sizeからASCII≈0.55em/CJK≈1.0emの
  概算幅ではみ出し量を推定してviewBoxを広げる（正確なフォントメトリクスではなく安全側の概算な
  ので、広げすぎることはあっても文字が切れることは無いはず）。**新しい回路を追加したら、
  `run_pipeline.sh`経由で実行する限り自動適用されるが、SVGを個別に再生成した場合は
  `fix_viewbox.py`を忘れずに呼ぶこと**。verification HTMLはSVGを内容ごと埋め込むので、
  SVGを修正したら対応する`ltspice_chapterNN.html`も`gen_verification_html.py`で再生成が必要。
