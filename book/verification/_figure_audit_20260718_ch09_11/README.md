# 第9-11章 LTspice図 3点監査（2026-07-18、inbox一括処理セッション）

対象: `hbridge_pwm_bipolar.svg`/`hbridge_pwm_unipolar.svg`（chapter09）、
`phase_control_r_load.svg`/`phase_control_rl_load.svg`（chapter10）、
`ringing_lrc_step.svg`（chapter11）。監査ツール: `tools/svg_preview.py`（変更なしで流用）。
第9-11章はLTspice本体パイプライン完走（`20260717_ltspice_asc_svg_pipeline_pwreletron`）時に
未実施のまま残っていた3点監査を、本セッションでまとめて実施。

## 3点監査

### (i) フォントサイズ
全5図とも部品ラベル・値・ディレクティブは24px統一（既存章と同一）。縮小・潰れなし。

### (ii) はみ出し・重なり
- **hbridge系2図**: 主回路（左）と制御ブロック電圧源群（右）が広い余白で分離、重なりなし。
- **phase_control系2図**: 主回路・ゲート駆動電流源・サイリスタ対・シャント抵抗の4カラム構成、
  重なりなし。**1点、軽微な観察**: ゲート駆動電流源`Igatep`/`Igaten`（R180配置、InstNameラベルは
  回路図上で180°回転＝実LTspiceでもR180部品のWINDOWラベルは既定で反転する既知の挙動と同型）の
  ラベルと、同じ配線に付く`mid`ネットラベルフラグが約27px間隔と近接している（`phase_control_r_load.svg`
  145行目`translate(176,938) rotate(180)`のInstNameテキストと413行目`x="176" y="933.2"`の`mid`フラグ）。
  実害（配線誤り・可読不能）はなく、ch08監査で記録した「D3ラベル回転」と同種のコスメティック差異
  と判断し、修正は見送り記録のみ（同種事案の一貫した扱い）。
- **ringing_lrc_step**: **必須修正1件（本セッションで是正済み）**。V1の`Value`
  (`PULSE(0 10 0 {tr} {tr} 5000n 10000n)`、37文字・レンダ幅約490px)が、既存の160px間隔（corpus標準
  ピッチ）でV1直後に置かれていたLp（インダクタ）のリード線を貫通していた（`ringing_lrc_step_before.png`
  で"5000n"のうち"0"がLpのリード線と交差）。**先生指摘「図がぐちゃぐちゃ」の原因パターンと同種**
  （長いValue文字列が隣接シンボルと衝突）のため、`.asc`のLp/R1/Cpカラムをx=320→x=720へ移設し解消
  （`ringing_lrc_step_after.png`で交差消失を確認）。`run_pipeline.sh`で.net/.raw/.svgを再生成し、
  ngspice実測値（vpeak_a=19.82, t_zc1_a/t_zc2_a, pk2_a/pk3_a, vpeak_b1, vpeak_b2, pk2_b2/pk3_b2）が
  座標変更前後で完全一致（トポロジー不変・座標のみの変更）を確認。

### (iii) 余白バランス
全5図とも既存章と同程度の余白配分。ringing_lrc_stepはLp-R1-Cpカラム移設で主回路とV1の間の
余白が広がったが、hbridge/phase_control系で既に確立された「主回路・制御ブロック間の広い余白」
パターンと同型であり違和感なし。

## 監査結果
- hbridge_pwm_bipolar / hbridge_pwm_unipolar / phase_control_r_load / phase_control_rl_load:
  **NGなし**（phase_control系のIgate/mid近接はコスメティックのみ、既存precedentと同様に許容）。
  4図は元SVGのまま変更なし。
- ringing_lrc_step: **必須1件是正済み**（Lp/R1/Cpカラムのx座標移設、電気的トポロジー不変）。

## 未解決の環境的制約（既知・本セッションでも変化なし）
シンボルの絵柄そのもの（本パイプライン独自の簡易アートワーク vs 実LTspiceの見た目）は、本機に
wine/実LTspiceが無いため引き続き未解決。本セッションで`mamba`（既にngspice導入実績のある
conda-forge経路）経由のwine導入を試みたが、`~/.claude/settings.json`のBash許可リストに
`mamba`が含まれておらず、非対話（watcher駆動）セッションでは承認ゲートを通過できず実行不能
（`sudo`同様、対話セッションでの人間の承認が必須）であることを確認。これは既知の環境制約
（`20260718_ltspice_corpus_few_shot_regeneration.md`のneeds-decision）を裏付ける新規の具体的証拠であり、
allowlist変更（設定ファイル編集）は本タスクのスコープ外のため実施していない。
