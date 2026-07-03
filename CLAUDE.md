# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

大阪工業大学「パワーエレクトロニクス」講義（全14回）をもとにした教科書を、森北出版へ提案・出版するプロジェクト。
組版はコロナ社テンプレート（corona-a5-1.1、pLaTeX）を流用する（電磁気教科書 `~/text_electromagnetic_theory` と同一体制）。

- 書籍タイトル: 仮題『パワーエレクトロニクス ― エネルギーの蓄えと放出で読み解く電力変換』
- 章立て: 序章+11章・3部構成（`morikita_proposal` の企画書が正。本リポの `book/main.tex` に反映済み）
- 企画書: `~/power_electronics_oit_jinno/morikita_proposal/教科書企画_要旨と目次案_20260611.pdf`

## 本書の理念（企画書より・全章で貫く）

1. **素子が「なぜそう動くか」から機能を導く**（読める→作れるへ）
2. **「エネルギーをどう蓄え、どう放出するか」の一貫視点**で全変換回路を串刺し
3. **仮定を毎回明示**（理想スイッチ・定常状態・小リプル。崩れたときの話も）
4. **設計手順まで下ろす**（目標リプル→L・C値の決定）
5. **LTspice連携**（全回路を再現可能に）

## 最重要ルール

1. **執筆前に必ず `WRITING_GUIDE.md` を読む**（コロナ社規約+パワエレ固有規約）
2. ビルドは **pLaTeX**（platex→mendex→platex→dvipdfmx。このマシンでは /usr/bin の各コマンド直叩き）
3. **スライド画像・LTspiceスクショの貼り込み禁止**。図は全点スクリプト生成EPS（1図=1スクリプト、`book/figures/scripts/`。TikZは `render.sh` 相当のパイプラインで、matplotlibは直接EPS出力）
4. 図ファイル名は `fig{章}.{番}.eps`=ラベル名。図の幅は318pt以下
5. ベクトル `\boldsymbol`、句読点「，」「。」、である調
6. corona-a5-1.1.cls の改変禁止
7. **こまめにcommit＆push。1修正1コミット、まとめコミット禁止**
8. **ユーザーへの返信は必ずTelegramへ**（`mcp__plugin_telegram_telegram__reply`）
9. 実装エージェントはコミットしない（メインセッションが監査後に実施）

## 素材

- 講義スライドPDF: 本リポ `pdf/`（全14回）
- 講義テキスト（LaTeX・です・ます調）: `~/power_electronics_oit_jinno/lecture_notes/chapters/chapter01〜11`（である調へ変換して素材化）
- LTspiceシミュレーション: `~/power_electronics_oit_jinno/LTspice/`
- 電磁気教科書 `~/text_electromagnetic_theory`: 体裁・環境の使い方・「本章の現在地」等の様式の参照元

## 新章と素材の対応

| 新章 | タイトル | 講義回 | lecture_notes |
|---|---|---|---|
| 序章 | 電力変換はエネルギーの受け渡しである | 1 | chapter01 |
| 1 | 半導体の物理 | 2 | chapter02 |
| 2 | パワー半導体の動作原理 | 3 | chapter03 |
| 3 | デバイス特性とデバイス選択 | 1,3 | chapter01,03 |
| 4 | リアクティブ素子とエネルギー | 4 | chapter04 |
| 5 | 直流-直流変換(1) 非絶縁型 | 5 | chapter05 |
| 6 | 直流-直流変換(2) 絶縁型 | 6 | chapter06 |
| 7 | 直流-直流変換(3) リニアレギュレータ | 7 | chapter07 |
| 8 | 交流-直流変換 整流回路 | 9,10 | chapter08,09相当 |
| 9 | 直流-交流変換 インバータ | 11,12 | chapter10,11相当 |
| 10 | 交流-交流変換 | 13 | （スライドのみ） |
| 11 | 電磁ノイズとEMC | 14 | （スライドのみ） |

※lecture_notes の章番号は要確認（8以降は講義回とずれている可能性あり）。

## 執筆フロー

1. `WRITING_GUIDE.md` と企画書の該当章概要を読む
2. lecture_notes の該当章とスライドPDFを素材に corona 環境（定義・例題・解答・問・章末問題・注意・COLUMN）で書き直す（です・ます調→である調）
3. 第II部の章は冒頭に「本章の現在地」（fig0.1の地図+エネルギー視点の一言）を置く
4. 問・章末問題には巻末解答（toianswerNN/answerNN）を同期
5. `platex` でエラー0を確認
6. コミットはメインセッションが監査後に実施

## Webプレビュー（docs/ = GitHub Pages）

電磁気本と同じ体裁：`docs/index.html`（執筆ダッシュボード）+ `docs/chNN.html`（章プレビュー、MathJax+図はSVG base64埋め込み）。
