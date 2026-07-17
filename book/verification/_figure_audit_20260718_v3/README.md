# 図監査記録 (2026-07-18 第2ラウンド, FLEET.md図監査規約準拠)

対象: 第1章LTspice回路3点（pn_junction_iv / schottky_iv / ohmic_contact_iv、
corpus準拠レイアウト本格適用後）。監査には
`book/figures/ltspice/tools/svg_preview.py` を使用（本ディレクトリの3枚のPNGは
本ラウンド再生成後のSVGをそのまま描画したもの）。

## 3点監査

1. **フォントが小さすぎないか**: 全ラベルfont-size=24px、前ラウンドから不変。OK。
2. **はみ出し・重なりがないか**: 3回路とも目視確認、タイトル・部品ラベル・ディレクティブが
   回路本体および互いに重ならない。SHEETを880x680へ拡大し要素間ピッチも広げたことで、
   前ラウンド(cdee328)より余白バランスが改善（回路が画面左上に寄り、右・下に十分な余白）。
3. **余白バランス（空白過多・偏り）**: 3回路とも右側に大きな空白が残る。これは
   `fix_viewbox.py`が最長コメント行の幅に合わせてviewBoxを広げる仕様のため
   （ohmic_contact_ivのタイトルが最も長く、viewBox幅が3回路中最大）。教科書DTP側で
   個別にトリミング範囲を指定する運用は既存踏襲（電磁気本と同じ）。

## 未解決事項（正直な申し送り）

シンボルのアートワーク自体（voltage/res/diodeの絵）は本パイプライン独自の.asy
（wine/実LTspiceが本機に無いため）のままで、実LTspice内蔵シンボルとの見た目の一致は
本ラウンドでも達成していない。今回改善したのは座標配置・スペーシング・SHEETサイズの
corpus準拠化のみ。詳細は `../ltspice_chapter01_v3.html` の before/after 比較と
`tasks/inbox/zimaboard/20260718_ltspice_corpus_few_shot_regeneration.md` の進捗ログ参照。

## NGを残したままのコミットはしていない

上記1-3点はいずれも問題なしを確認済み。本監査自体がコミット前の検品の一部。
