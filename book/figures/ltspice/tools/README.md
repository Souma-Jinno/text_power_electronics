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

1. `chapterNN/xxx.asc` を作成（`SYMBOL_PINS`に登録済みのシンボル種別=voltage/res/diodeのみ使用可。
   新しい部品が要る章では `asc_to_net.py` の `SYMBOL_PINS`/`SYMBOL_PREFIX` と `symbols/*.asy` を追加する）
2. `bash tools/run_pipeline.sh chapterNN/xxx.asc` で `.net`→ngspice `.raw`→`.svg` を一括生成
   （`asc_to_net.py`が接続チェックNGなら非ゼロ終了するので、このステップでコケたら.ascを直す）
3. 章が揃ったら `tools/gen_verification_html.py <章番号> <章タイトル> <spec.json>` で
   `book/verification/ltspice_chapterNN.html` を生成

## 既知の制約

- `asc_to_net.py`は自作パーサであり、実LTspiceの`-netlist`出力と1:1で同じではない
  （回転はR0/R90/R180/R270とM0/M90/M180/M270の一般式に対応済みだが、実機での動作確認はできていない）。
- 部品種別はチャプター1時点で voltage/res/diode の3種のみ。5章以降でMOSFET/インダクタ/変圧器等が
  要る際は同じパターンで `.asy`と`SYMBOL_PINS`を追加する。
- wine/実LTspiceが将来使えるようになった場合は、`asc_to_net.py`の出力とLTspice実機の`-netlist`
  出力を突き合わせて自作パーサの妥当性を再検証すること。
