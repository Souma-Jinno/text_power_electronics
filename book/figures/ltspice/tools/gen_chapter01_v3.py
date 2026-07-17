"""
book/verification/ltspice_chapter01_v3.html -- before/after comparison for the
2026-07-18 second-round corpus-driven layout regeneration (addendum task
20260718_ltspice_corpus_few_shot_regeneration, after the first round's needs-decision
was left open: this round applies the corpus's SHEET size and spacing convention
directly, rather than only fixing the title-overlap bug).
"""
from pathlib import Path

REPO = Path("/home/soumajinno/text_power_electronics")
CH01 = REPO / "book/figures/ltspice/chapter01"
BEFORE_DIR = REPO / "book/verification/_v3_before"
OUT = REPO / "book/verification/ltspice_chapter01_v3.html"

STYLE = """
body { font-family: "Hiragino Sans", "Noto Sans JP", sans-serif; background:#fff; color:#222; margin:2em auto; max-width: 1100px; padding: 0 1em; }
h1 { border-bottom: 3px solid #0891b2; padding-bottom: 0.3em; }
h2 { color:#0e7490; border-left: 6px solid #0891b2; padding-left: 0.5em; margin-top: 2.5em; }
.pair { display:flex; gap:1em; margin: 1em 0; }
.col { flex:1; border:1px solid #ddd; border-radius:8px; padding:1em; }
.col.before { background:#fff5f5; }
.col.after { background:#f5fffa; }
.svgwrap { background:#fff; border:1px solid #eee; padding:0.5em; text-align:center; }
.svgwrap svg, .svgwrap img { max-width:100%; height:auto; }
.badge-fix { color:#fff; background:#0891b2; border-radius:4px; padding:0.15em 0.6em; font-size:0.85em; }
.note { color:#555; font-size:0.9em; }
"""

FIXES_APPLIED = """
<div class="note">
<p><b>この回の対応（依頼書 20260718_ltspice_corpus_few_shot_regeneration「その後」節、
第1章3回路へのcorpus準拠レイアウト本格適用, 2026-07-18第2ラウンド）:</b></p>
<ol>
<li>前ラウンド(commit cdee328)はタイトル位置の是正のみで、SHEETサイズは320x320のまま
    （corpus実物は例外なく880x680以上）だった → 全3回路をSHEET 1 880 680へ変更
    （corpusの29個中27個が880x680以上、これがLTspice新規シート作成時の標準規約）</li>
<li>部品間の縦方向ピッチをcorpus実物（Draft1.asc/inverter.asc/sinh.asc、いずれも要素間96px、
    GND引き下ろしに48px程度の余裕）に倣って再配置。以前は要素同士がピン座標で直結していた
    箇所はそのまま維持しつつ、電源からGNDまでの引き下ろし線に余裕を持たせた</li>
<li>タイトルコメントと回路本体の間隔を y=48→144(96px)に拡大、ディレクティブ群も回路末端から
    72px以上離す（corpusのTEXT配置慣例に合わせた）</li>
</ol>
<p><b>環境上の限界（正直な申し送り）:</b> 本機にwine/実LTspiceが無いため、シンボル自体の
アートワーク（voltage/res/diodeの絵、本パイプライン独自の.asy）は実LTspiceのものと同一化
できていない。corpusから学べたのは座標配置・スペーシング・SHEETサイズの慣例までで、
シンボル画そのものの「本物らしさ」は環境制約により本セッションでも未解決。</p>
</div>
"""

def svg_or_img(path: Path) -> str:
    if path.suffix == ".svg":
        return path.read_text(encoding="utf-8")
    return f'<img src="{path.name}">'

CIRCUITS = [
    {
        "name": "pn_junction_iv",
        "label": "pn接合ダイオードI-V特性試験回路（sec1.6）",
        "before": BEFORE_DIR / "pn_junction_iv_cdee328.svg",
        "after": CH01 / "pn_junction_iv.svg",
    },
]

parts = [
    "<!DOCTYPE html><html lang='ja'><head><meta charset='utf-8'>",
    "<title>LTspice検証: 第1章 v3（corpus準拠レイアウト本格適用 before/after）</title>",
    f"<style>{STYLE}</style></head><body>",
    "<h1>LTspice検証: 第1章 v3（corpus準拠レイアウト本格適用, 2026-07-18第2ラウンド）</h1>",
    FIXES_APPLIED,
]

for c in CIRCUITS:
    parts.append(f"<h2>{c['label']}</h2>")
    parts.append("<div class='pair'>")
    parts.append("<div class='col before'><b>Before（前ラウンド commit cdee328 時点）</b><div class='svgwrap'>")
    parts.append(svg_or_img(c["before"]))
    parts.append("</div></div>")
    parts.append("<div class='col after'><b>After（本ラウンド後）</b> <span class='badge-fix'>UPDATED</span><div class='svgwrap'>")
    parts.append(svg_or_img(c["after"]))
    parts.append("</div></div>")
    parts.append("</div>")

parts.append("""
<h2>schottky_iv / ohmic_contact_iv（第1章の残り2回路）</h2>
<div class="note">
<p>この2回路も pn_junction_iv と同一トポロジパターン（V1→R1(またはRc/Rb)→D1直列、GND2点）
のため、同じSHEET拡大・スペーシング拡大を適用済み。最終版は
<a href="ltspice_chapter01.html">ltspice_chapter01.html</a>（通常の検証HTML、3回路とも収録、
本ラウンドの結果で再生成済み）を参照。</p>
</div>

<h2>次のステップ（依頼書「その後」節: 第2-11章への展開）</h2>
<div class="note">
<p>本ラウンドで確立した「SHEET 1 880 680 + 96pxピッチ + タイトル分離96px以上 + ディレクティブ
分離72px以上」の型を、第2章以降の新規回路作成時からの標準として適用する。既存の第2章4回路・
第3章1回路（cdee328で既にタイトル位置は是正済み）への遡及適用は、依頼の優先度と工数対効果を
macmini/先生に確認の上で判断する。</p>
</div>
</body></html>
""")

OUT.write_text("\n".join(parts), encoding="utf-8")
print("written:", OUT)
