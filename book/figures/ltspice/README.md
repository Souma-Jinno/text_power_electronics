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

- **21ファイルすべて照合済み**（`verify_all.sh` が PASS=21 / FAIL=0）
- **未接続ピン 0 / 290**
- **図に描かれた素子 125 / 137**

残り12個は，シンボルではなく `!` 付きの SPICE 文として `.asc` に入っている。
**LTspice はこの行もネットリストに入れて計算するので，動作は正しい。**
図として描かれていないだけである。

| 素子 | 数 | ファイル | なぜ描けないか |
|---|---|---|---|
| `E`（電圧制御電圧源） | 1 | chapter07/linear_reg_opamp | `e.asy` が無い |
| `B`（ビヘイビア電源） | 11 | chapter09 の2件 | 搬送波・基準波の式そのものなので，文字のままでも読める |

描きたい場合は LTspice で部品を足し，保存後に `verify_all.sh` を通すこと。


## ngspice で「同じ波形が出るか」まで確かめる

`verify_all.sh` は回路の**構造**（どの素子がどのノードにつながっているか）を照合する。
`compare_asc_vs_net.py` はもう一歩進めて，**実際に ngspice で走らせて数値を比べる**。

```bash
python3 compare_asc_vs_net.py
```

`.net` と，`.asc` から起こし直したネットリストの両方を同じ解析にかけ，
共通ノードの電圧を全時刻で突き合わせる（相対差 1e-3 まで許容）。

**結果（2026-09-08，ngspice-41）: 一致=18 / 相違=0 / 対象外=3**

対象外の3件（chapter08 のブリッジ整流器，chapter09 のHブリッジPWM 2件）は，
ノードをまとめて書き出すと ngspice が
「no such vector」で止まってしまい，スクリプトでは自動比較できなかった。
**この3件は手で1ノードずつ比べて一致を確認してある**：

| ファイル | 比べたノード | 点数 | 最大相対差 |
|---|---|---|---|
| chapter08/bridge_rectifier | `v(vout)` | 20001 | 8.8e-09 |
| chapter09/hbridge_pwm_bipolar | `v(carr)` | 80001 | 0 |
| chapter09/hbridge_pwm_unipolar | `v(carr)` | 80001 | 0 |

つまり**21ファイルすべて，配布する `.asc` は元の `.net` と同じ回路で，
同じ波形を出す**ことが確かめられている。

## ツールへの変更点

`netlist-to-schematic` は配布物をそのまま置いているが，1か所だけ直してある。

- `tools/asc2ngspice.py` の `parse_asc()`：`.asc` を UTF-16LE 固定で読んでいたため，
  UTF-8 で保存された `.asc` を読めなかった。BOM と NUL バイトの有無で
  UTF-16(BOM付き)／UTF-16LE／UTF-8 を見分けるようにした。
