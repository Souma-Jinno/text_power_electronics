"""
book/verification/ltspice_chapter01_v2.html -- before/after comparison for the
2026-07-18 corpus-driven cleanup (task 20260718_ltspice_corpus_few_shot_regeneration).
"""
from pathlib import Path

REPO = Path("/home/soumajinno/text_power_electronics")
CH01 = REPO / "book/figures/ltspice/chapter01"
BEFORE_DIR = REPO / "book/verification/_v2_before"
OUT = REPO / "book/verification/ltspice_chapter01_v2.html"

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
<p><b>この回の対応（先生指摘「なんか図がぐちゃぐちゃ」への対応, 2026-07-18）:</b></p>
<ol>
<li>タイトルの説明コメントが回路図と同じ高さ(y=8)に置かれ、V1シンボルの直上と衝突していた
    → タイトルを回路の上端より明確に上(y=-56)へ移動</li>
<li>第1章自体は元々コメント量が少なく致命的ではなかったが、第2章(4回路)・第3章(1回路)では
    詳細な日本語説明が10行前後、回路の高さ全域(y=32〜248)に渡って配置されており、
    回路図の上に文章が重なって読めない状態だった → 詳細説明は全てVERIFICATION_NOTES.mdへ移し、
    .asc内のコメントはタイトル1行のみに削減(先生指示の「コメントTEXTは必要最小限」ルールに準拠)</li>
<li>.model/.controlディレクティブ等の必須SPICE文は残す(実LTspiceコーパスの例にも見られる
    慣例)が、回路本体および他のシンボルと縦方向に重ならない位置へ再配置</li>
</ol>
<p>部品シンボル名(res/cap/ind/diode/nmos/npn/pnp)は前回コミットで既に実LTspice規約へ統一済み。
ピン座標そのものは本機にwine/実LTspiceが無いため未検証(自前ジオメトリのまま)。</p>
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
        "before": BEFORE_DIR / "pn_junction_iv_v1.svg",
        "after": CH01 / "pn_junction_iv.svg",
    },
]

parts = [
    "<!DOCTYPE html><html lang='ja'><head><meta charset='utf-8'>",
    "<title>LTspice検証: 第1章 v2（コーパス準拠クリーンアップ before/after）</title>",
    f"<style>{STYLE}</style></head><body>",
    "<h1>LTspice検証: 第1章 v2（先生指摘「図がぐちゃぐちゃ」への対応, 2026-07-18）</h1>",
    FIXES_APPLIED,
]

for c in CIRCUITS:
    parts.append(f"<h2>{c['label']}</h2>")
    parts.append("<div class='pair'>")
    parts.append("<div class='col before'><b>Before（先生に送付した版）</b><div class='svgwrap'>")
    parts.append(svg_or_img(c["before"]))
    parts.append("</div></div>")
    parts.append("<div class='col after'><b>After（本対応後）</b> <span class='badge-fix'>FIXED</span><div class='svgwrap'>")
    parts.append(svg_or_img(c["after"]))
    parts.append("</div></div>")
    parts.append("</div>")

parts.append("""
<h2>schottky_iv / ohmic_contact_iv（第1章の残り2回路）</h2>
<div class="note">
<p>この2回路は元々 pn_junction_iv と同一パターン（コメント1行+ディレクティブ2行のみ）で、
タイトル位置の軽微な重なり以外は before から大きな崩れはなかった。同じタイトル位置修正
（y=8→y=-56）のみ適用済み。個別の before/after 画像は省略し、最終版（after 相当）を
<a href="ltspice_chapter01.html">ltspice_chapter01.html</a>（通常の検証HTML、3回路とも収録）
に統合済み。</p>
</div>

<h2>参考: 第2章・第3章の同種修正（本ラウンドの主な対象ではないが、同じ罠のため合わせて修正）</h2>
<div class="note">
<p>先生の指摘は第1章+第2章の図を見た上でのものだったため、第2章4回路・第3章1回路にも
同じ「コメントが回路に重なる」問題が（第1章より深刻な形で）存在することを本セッションで発見し、
同じ方針（詳細説明をVERIFICATION_NOTES.mdへ、.asc内はタイトル1行+最小限のディレクティブのみ）
で合わせて修正した。詳細は
<a href="ltspice_chapter02.html">ltspice_chapter02.html</a> /
<a href="ltspice_chapter03.html">ltspice_chapter03.html</a> の各回路を参照。
第2-11章の本格的な「コーパスを使ったfew-shot再生成」（座標配置パターン・シンボル向きまで
corpusに倣う再設計）は本タスクの次回以降のスコープ（依頼書「その後(第2章以降)」）。</p>
</div>
</body></html>
""")

OUT.write_text("\n".join(parts), encoding="utf-8")
print("written:", OUT)
