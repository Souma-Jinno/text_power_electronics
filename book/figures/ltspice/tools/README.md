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
- **理想AC電圧源+ダイオード+大容量Cの組合せは突入電流でNewton法が発散しやすい**
  （2026-07-18chapter08のブリッジ整流回路で発見）。電源に直列で現実的な内部抵抗（`Rsrc`、
  数Ω程度、電源線・簡易トランスの巻線抵抗に相当）を追加し、あわせて`.options reltol=0.01
  gmin=1e-9`（デフォルトreltol=0.001から緩和）を指定すると解消する。片方だけでは不十分な
  ケースがあることを確認済み（`chapter08/bridge_rectifier.asc`が実装例）。整流回路など
  AC電源を扱う今後の章（9章以降）でも同じ罠に当たる可能性が高い。
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
- **PWM比較器等の連続時間ロジックは`voltage`シンボル流用のbehavioral source(B-element)で実装
  できる（2026-07-18、chapter09で追加）**: `SYMBOL voltage`のInstNameを`B<name>`にし、
  `SYMATTR Value V=<式>`（式にasin/sin/三項演算子`?:`等を含めてよい、ngspice B-source式
  パーサーが対応済み）とするだけで、`asc_to_net.py`のコード変更なしにSPICE B-element行
  `B<name> <net+> <net-> V=<式>`が生成される（genericなSYMATTR処理がそのまま通る、opamp用の
  特別処理は不要）。三角搬送波は`(2/pi*asin(sin(2*pi*fc*time)))`で振幅±1を生成できる。
  視覚上は電圧源記号になるため、opamp/zenerと同じく「実体は制御ブロック」である旨を
  VERIFICATION_NOTES.mdに明記すること。
- **`.meas ... to=<tran終了時刻>`ちょうどの境界でアーティファクトが出る（2026-07-18、
  chapter09で発見）**: スイッチング回路で測定窓の上端をtranのtstopちょうどに合わせると、
  最終強制サンプル点で桁違いの異常値が出ることがある（実測例: 期待100Vに対し24847V）。
  `to=<tstop-0.1ms程度>`のように終了時刻より僅かに手前までの窓にすること。
- **`.control`内の`let`式は`.param`を直接参照できない（2026-07-18、chapter09で発見）**:
  `let x = sin(2*pi*fm*time)`のように`.param`名を`let`式に書くと`vector fm is not available`
  で失敗する。`let`はSPICEデッキの`.param`置換とは独立した別スクリプト言語のため。`let`式では
  数値を直接埋め込むこと（SYMATTR Value等のSPICEカード内では`.param`置換は問題なく機能する）。
- **`.four`組込みFourier解析は高周波PWM波形を過小評価する（2026-07-18、chapter09で発見）**:
  デフォルトgridsize=200点固定のため、搬送波周期を200点未満でしか解像できない場合に基本波
  振幅を大きく誤る（実測例: 期待80Vに対し127V）。フーリエ係数の正確な抽出には代わりに相関積分法
  （`let ib=vab*sin(wt)`等を作り`meas tran ... integ ib from=<1周期分>`でフーリエ係数を数値
  積分、既知振幅の校正テストで誤差<0.01%を確認済み）を使うこと。`fft`コマンドは定性的な
  「どの周波数帯に集まるか」の確認には使えるが、ゼロパディングでビン間隔が理論値と僅かにずれ
  基本波がリークするため、絶対値の抽出には向かない。
- **逆並列に2個のラッチ素子(サイリスタ等)を接続する回路では、両素子の端子を両方とも浮遊ノードに
  すると2個目の点弧時にNewton法が収束破綻する（2026-07-18 chapter10で発見）**:
  トライアック相当回路(2章の2トランジスタサイリスタ等価回路を逆並列に2組)で、両サイリスタの
  アノード/カソードを新規の浮遊ノード2つ(どちらも回路グラウンド"0"と直接つながらない)で構成した
  ところ、2個目のゲートパルスが入る時刻に`Timestep too small; ... trouble with node "gbasep"`
  で`tran`が中断した。片方のサイリスタのカソード(またはアノード)を回路グラウンド"0"に固定する
  （2章の元回路と同じ構成）ことで解消した。逆並列ペアを構成する際は、必ずどちらか一方の端子を
  回路の基準ノードに固定すること。
- **`alter @<inst>[pulse] = [...]`によるPULSE電流源/電圧源パラメータの書き換えはこの環境の
  ngspice(ngspice-41)では動作しない（2026-07-18 chapter10で発見）**: `PPerror: syntax error in
  line segment` / `Error: cannot evaluate new parameter value`で失敗し、しかもエラー後も後続の
  `tran`は(変更が反映されないまま)実行されてしまうため気づきにくい。代わりに`.param
  adelp=<初期値>`を定義し`PULSE(0 10m {adelp} 1u 1u 1m 20m)`のように波括弧参照させたうえで、
  `alterparam adelp = <新しい値>` → `reset` → `tran`の順で実行すること（`chapter10/
  phase_control_r_load.net`が実装例、5ケースの点弧角スイープに使用）。`reset`は回路全体を
  再読込するため、副次的にラッチ素子の内部状態がケース間で引き継がれる心配も自動的に解消される
  （5ケースそれぞれが実質的に独立実行になり、ケース間の状態汚染を心配する必要がない）。
- **`tran`が収束破綻で中断した状態のまま`.meas ... FROM=/TO=`を呼ぶと、エラーを出さずに0や
  無意味な値を返すことがある（2026-07-18 chapter10で発見）**: 上記の収束破綻の状態で`.meas tran
  ... RMS/MAX v(...) FROM=60m TO=99.9m`を実行すると、`out of interval`エラーが出るケースと、
  エラーなしで`0.0`が返るケース（引数の違いで挙動が変わる）の両方を確認した。後者は一見
  「measコマンド自体のバグ」に見えるが実態はシミュレーションが中断していただけ、という紛らわしい
  罠。`.meas`の結果を信用する前に、ログに`Timestep too small`/`tran simulation(s) aborted`が
  無いことを確認すること。逆に、収束が正常な回路では`.meas tran ... RMS ... FROM=/TO=`は
  信頼できる（chapter10でPython側のsqrt(mean(v^2))台形積分と誤差0.0006%で一致することを確認済み）。
- **`fix_viewbox.py`は右端・下端（`max_x`/`max_y`）しか広げない実装であり、上端・左端
  （`min_y`/`min_x`）のはみ出しには無力（2026-07-18 chapter10で発見）**: 回路説明コメントを
  `TEXT 16 -140`のように回路本体から大きく上に離して置くと、SVGのviewBox上端からコメント1行目が
  はみ出し、`overflow:hidden`でサイレントに読めなくなることがある（chapter08の既存ファイルにも
  同種の小さなはみ出しが残っている可能性がある、未修正）。`fix_viewbox.py`のスクリプト自体は
  「TEXT幅を考慮しない」という右端方向の罠（既存項目参照）しか対策していないため、上端方向は
  `.asc`側でコメントTEXTのY座標を回路本体の直近（目安: 最上段シンボルのY座標から概ね100px以内、
  フォントサイズ24pxならY座標のマージンは1行あたり24〜28px程度に収める）に置くことで回避する
  しかない。新しい回路を追加したら、必ず`svg_preview.py`で1行目・最終行の両方が欠けていないか
  目視確認すること。
- **`.control`ブロック内で`alterparam`+`alter`を併用する場合、`reset`の直後に置けるのは
  片方だけ（2026-07-18、chapter11で発見）**: `alterparam <param>=<値>`による`.param`変更を
  反映させるには直後に`reset`が必須だが、`reset`は回路をオリジナルの`.net`から丸ごと再読込する
  ため、**その直前までに実行した`alter <inst>=<値>`（直接の素子値変更）も一緒に巻き戻ってしまう**。
  両方を1ケースで使う場合は「`alterparam`→`reset`→`alter`→（`reset`を挟まず）`tran`」の順にする
  こと。逆順（`alter`の後にもう一度`reset`する）で書くと、`alter`が無かったことになったまま
  `tran`が走り、`.meas`の結果が意図した値変更なしのケースと数値的に完全一致するという紛らわしい
  形で失敗が現れる（エラーは出ない）。`chapter11/ringing_lrc_step.net`のR=1Ωケースが実装例。
