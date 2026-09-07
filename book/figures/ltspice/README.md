# 配布用 LTspice ファイル

本書は「波形図は LTspice で描いたもの」を見せ，パラメータを変えたい読者のために
`.asc` を配布する方針である（森北出版との打合せ 2026-09-02）。ここはその置き場。

```
chapterNN/xxx.net    ngspice のネットリスト（回路の定義。これが正）
chapterNN/xxx.asc    LTspice の回路図（読者に配布するもの）
corpus/              著者が実際に LTspice で描いた図（作図の見本。編集しない）
netlist-to-schematic/  .net から .asc を作り，機械照合するツール一式
verify_all.sh        全ファイルの照合（コミット前に必ず通すこと）
```

## なぜ照合が要るのか（2026-09-08 に起きたこと）

`.asc` は**座標だけのテキスト**で，どの部品がどこにつながっているかは書かれていない。
接続は座標が一致することから生まれる。したがって

- 座標を1つ間違えても**構文エラーは出ない**
- 図もほとんど同じに見える
- **黙ってネットが切れるだけ**

2026-09-08 の全数検査で，配布用 21 ファイルの**ピン 194 個／257 個が，どの配線にも
つながっていない**ことが分かった（著者が LTspice で実際に描いた corpus 16 ファイルは
0 個／241 個）。原因は，部品の原点とピンの位置を同じだと思って座標を書いていたこと。
たとえば LTspice のコンデンサはシンボル原点から x に $+16$ ずれた位置にピンがある
（`cap.asy` の `PIN 16 0`）ので，配線を原点の x に引くと 16 だけ外れる。

**この種の誤りは目で見て見つけられない。** だから機械照合する。

## 作り直しかた

```bash
# 1つ作る（生成と同時に .asc → ネットリスト → 原本 の往復照合が走る）
python3 netlist-to-schematic/tools/net2asc.py chapter05/buck_chopper.net -o chapter05/buck_chopper.asc

# 既にある .asc が .net と同じ回路かを確かめるだけ
python3 netlist-to-schematic/tools/net2asc.py chapter05/buck_chopper.net --check chapter05/buck_chopper.asc

# 全部確かめる
bash verify_all.sh
```

**LTspice で図を描き直してよい。** 部品を動かしても LTspice が接続を保つので，
保存したあと `verify_all.sh` を通せば，回路が変わっていないことを機械で確かめられる。
自動生成の配置が読みにくい図（ブリッジ整流器など）は，この手順で描き直すのがよい。

## 現状（2026-09-08）

- **12 ファイルは照合済み**（`verify_all.sh` が PASS）
- **9 ファイルは未対応**。ツールに次のシンボル定義が無いため描けない：
  `npn` `pnp` `current` `zener` `opamp` `bi` `bv`
  LTspice の `lib/sym/` から本物の `.asy` を `netlist-to-schematic/tools/ltsym/` に
  置けば対応できる。**ピン座標は推測しないこと**（推測すると同じ事故になる）。
  対象：chapter02 の3件，chapter07 の2件，chapter09 の2件，chapter10 の2件

## ツールへの変更点

`netlist-to-schematic` は配布物をそのまま置いているが，1か所だけ直してある。

- `tools/asc2ngspice.py` の `parse_asc()`：`.asc` を UTF-16LE 固定で読んでいたため，
  UTF-8 で保存された `.asc` を読めなかった。BOM と NUL バイトの有無で
  UTF-16(BOM付き)／UTF-16LE／UTF-8 を見分けるようにした。
