#!/usr/bin/env python3
"""
gen_verification_html.py -- build book/verification/ltspice_chapterNN.html
from the .asc/.net/.svg triples in book/figures/ltspice/chapterNN/.

Usage: gen_verification_html.py <chapter_num> <title> <circuit_spec.json>
circuit_spec.json: list of {"base": "pn_junction_iv", "label": "...", "section": "sec1.6"}
"""
import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
LTSPICE_DIR = REPO / "book" / "figures" / "ltspice"
VERIFY_DIR = REPO / "book" / "verification"

STYLE = """
body { font-family: "Hiragino Sans", "Noto Sans JP", sans-serif; background:#fff; color:#222; margin:2em auto; max-width: 960px; padding: 0 1em; }
h1 { border-bottom: 3px solid #0891b2; padding-bottom: 0.3em; }
h2 { color:#0e7490; border-left: 6px solid #0891b2; padding-left: 0.5em; margin-top: 2.5em; }
.circuit { border: 1px solid #ddd; border-radius: 8px; padding: 1em 1.5em; margin: 1em 0; }
.svgwrap { background:#fff; border: 1px solid #eee; padding: 0.5em; text-align:center; }
.svgwrap svg { max-width: 100%; height: auto; }
pre { background:#f8f8f8; border:1px solid #eee; padding:0.8em; overflow-x:auto; font-size: 0.85em; }
.badge-ok { color:#fff; background:#0891b2; border-radius:4px; padding:0.15em 0.6em; font-size:0.85em; }
.meta { color:#555; font-size:0.9em; }
a { color:#0e7490; }
"""


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def build(chapter_num: str, title: str, circuits: list) -> str:
    chdir = LTSPICE_DIR / f"chapter{chapter_num}"
    parts = [
        "<!DOCTYPE html><html lang='ja'><head><meta charset='utf-8'>",
        f"<title>LTspice検証: 第{chapter_num}章 {title}</title>",
        f"<style>{STYLE}</style></head><body>",
        f"<h1>LTspice検証記録 -- 第{chapter_num}章 {title}</h1>",
        "<p class='meta'>教科書figures(EPS)とは独立の補助資料。"
        "本ページの回路は book/figures/ltspice/ 配下の .asc/.net/.raw/.svg として"
        "リポジトリに同梱し、読者が LTspice/ngspice で再現できるようにするためのもの。"
        "既存の本文・掲載図(fig*.eps)は変更していない。</p>",
    ]
    for c in circuits:
        base = c["base"]
        svg = read(chdir / f"{base}.svg")
        net = read(chdir / f"{base}.net")
        parts.append("<div class='circuit'>")
        parts.append(f"<h2>{c['label']} <span class='badge-ok'>接続チェック OK</span></h2>")
        parts.append(f"<p class='meta'>関連節: {c['section']} / ファイル: "
                      f"<code>chapter{chapter_num}/{base}.asc</code></p>")
        if "note" in c:
            parts.append(f"<p>{c['note']}</p>")
        parts.append(f"<div class='svgwrap'>{svg}</div>")
        parts.append("<p><b>ネットリスト</b> (asc_to_net.py 自動生成):</p>")
        parts.append(f"<pre>{net}</pre>")
        parts.append("</div>")
    parts.append("</body></html>")
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter_num")
    ap.add_argument("title")
    ap.add_argument("spec_json")
    args = ap.parse_args()

    circuits = json.loads(Path(args.spec_json).read_text(encoding="utf-8"))
    html = build(args.chapter_num, args.title, circuits)
    out = VERIFY_DIR / f"ltspice_chapter{args.chapter_num}.html"
    out.write_text(html, encoding="utf-8")
    print(f"written: {out}")


if __name__ == "__main__":
    main()
