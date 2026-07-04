#!/usr/bin/env python3
# tex → HTML 変換（電磁気本のWebプレビュー様式に合わせる）。
# corona環境を box divへ、図をSVG base64埋め込み、\ref はauxで解決。
import re, io, os, base64, glob

ROOT = os.path.expanduser("~/text_power_electronics/book")
SVG = "/tmp/claude-1000/-home-soumajinno/e7688596-6b6f-45e4-950d-929e196c5bb6/scratchpad/pe_svg"
HEAD = open("/tmp/claude-1000/-home-soumajinno/e7688596-6b6f-45e4-950d-929e196c5bb6/scratchpad/em_head.html", encoding="utf-8").read()

TITLES = {0:"電力変換はエネルギーの受け渡しである",1:"半導体の物理",2:"パワー半導体の動作原理",
 3:"デバイス特性とデバイス選択",4:"リアクティブ素子とエネルギー",5:"直流-直流変換(1) 非絶縁型",
 6:"直流-直流変換(2) 絶縁型",7:"直流-直流変換(3) リニアレギュレータ",8:"交流-直流変換 ― 整流回路",
 9:"直流-交流変換 ― インバータ",10:"交流-交流変換",11:"電力変換で生じる電磁ノイズとEMC"}

# --- auxからlabel→番号 ---
def sanitize_num(v):
    # aux値に生TeX（\hbox to...{\bfseries N}等）が混ざることがあるので数字/記号だけ抜く
    if "\\" in v or "{" in v:
        m = re.search(r"([0-9]+(?:\.[0-9]+)?)", v)
        return m.group(1) if m else re.sub(r"\\[a-zA-Z]+|[{}]|to[\d.]+pt|\\hfill", "", v).strip()
    return v

LAB = {}
aux = open(f"{ROOT}/main.aux", encoding="utf-8", errors="replace").read()
for m in re.finditer(r"\\newlabel\{([^}]+)\}\{\{(.*?)\}\{", aux):
    LAB[m.group(1)] = sanitize_num(m.group(2))

def svg_img(base, alt):
    png = f"{SVG}/{base}.png"
    if os.path.exists(png):  # 重いSVGはPNGに差し替え済み
        d = base64.b64encode(open(png, "rb").read()).decode()
        return f'<img src="data:image/png;base64,{d}" alt="{alt}">'
    p = f"{SVG}/{base}.svg"
    if not os.path.exists(p): return f'<span style="color:red">[{base} なし]</span>'
    d = base64.b64encode(open(p, "rb").read()).decode()
    return f'<img src="data:image/svg+xml;base64,{d}" alt="{alt}">'

def inline(s):
    # インライン記法（数式$...$は温存）
    s = re.sub(r"\\index\{[^}]*\}", "", s)
    s = re.sub(r"\\FIGref\{([^}]+)\}", lambda m: "<b>図"+LAB.get(m.group(1),"?")+"</b>", s)
    s = re.sub(r"\\TABref\{([^}]+)\}", lambda m: "<b>表"+LAB.get(m.group(1),"?")+"</b>", s)
    # \ref{figX}/\ref{tabX}/\ref{secX}/\ref{eqX}/\ref{reiX} → 番号（eqは(x.y)込み）
    def refrep(m):
        k = m.group(1); v = LAB.get(k, "?")
        if k.startswith("fig"): return "図"+v
        if k.startswith("tab"): return "表"+v
        if k.startswith("sec"): return v+"節"
        return v
    s = re.sub(r"\\ref\{([^}]+)\}", refrep, s)
    s = re.sub(r"\\textbf\{([^{}]*)\}", r"<b>\1</b>", s)
    s = re.sub(r"\\emph\{([^{}]*)\}", r"<em>\1</em>", s)
    s = s.replace("~", " ").replace("\\,", " ").replace("\\ ", " ")
    s = s.replace("\\%", "%").replace("\\&", "&amp;").replace("\\_", "_")
    s = re.sub(r"\\(quad|qquad)\b", " ", s)
    return s

def convert_body(tex, chnum):
    tex = re.sub(r"(?<!\\)%.*", "", tex)  # コメント除去（\%は残す）
    # 環境をプレースホルダ化して段落処理と混ざらないようにする
    out = []
    # トークナイズ: 既知の\begin{env}...\end{env}を1ブロックとして食う
    envs = "定義|定理|補題|系|例題|注意|問|章末問題|screen|COLUMN|箇条書|figure|table"
    pos = 0
    pat = re.compile(r"\\(chapter\*?|section\*?|subsection\*?)\{([^}]*)\}"
                     r"|\\begin\{("+envs+r")\}(\[[^\]]*\])?"
                     r"|\\begin\{(equation\*?|eqnarray\*?|align\*?)\}")
    while pos < len(tex):
        m = pat.search(tex, pos)
        if not m:
            out.append(("text", tex[pos:])); break
        if m.start() > pos:
            out.append(("text", tex[pos:m.start()]))
        if m.group(1):  # 見出し
            out.append(("head", m.group(1), m.group(2))); pos = m.end()
        elif m.group(3):  # コーナー環境
            env = m.group(3); opt = (m.group(4) or "")[1:-1]
            e = tex.find(r"\end{"+env+"}", m.end())
            body = tex[m.end():e]
            out.append(("env", env, opt, body)); pos = e + len(r"\end{"+env+"}")
        else:  # 数式環境 → そのままMathJaxへ
            env = m.group(5)
            e = tex.find(r"\end{"+env+"}", m.end())
            out.append(("math", tex[m.start():e+len(r'\end{'+env+'}')])); pos = e + len(r"\end{"+env+"}")

    html = []
    reic = [0]; probc=[0]
    def render_text(t):
        # 段落・数式ブロックを分けてHTMLに
        parts = re.split(r"\n\s*\n", t)
        for p in parts:
            p = p.strip()
            if not p: continue
            html.append("<p>"+inline(p)+"</p>")
    for item in out:
        if item[0] == "text":
            render_text(item[1])
        elif item[0] == "math":
            html.append('<p>'+item[1]+'</p>')
        elif item[0] == "head":
            kind, title = item[1], inline(item[2])
            if kind.startswith("section"): html.append(f"<h2>{title}</h2>")
            elif kind.startswith("subsection"): html.append(f"<h3>{title}</h3>")
        elif item[0] == "env":
            env, opt, body = item[1], item[2], item[3]
            html.append(render_env(env, opt, body, chnum))
    return "\n".join(html)

def items_to_ol(body):
    its = re.split(r"\\item", body)
    out = []
    for x in its:
        x = x.strip()
        if not x: continue
        x = re.sub(r"^\[([^\]]*)\]\s*", r"", x)  # \item[(a)] の手動ラベルは番号付きolに任せる
        out.append("<li>"+inline(x)+"</li>")
    return "<ol>"+"".join(out)+"</ol>"

CN = {"定義":"def","定理":"thm","補題":"thm","系":"thm","注意":"note"}
def render_env(env, opt, body, chnum):
    if env in CN:
        head = env + (("　"+opt) if opt else "")
        return f'<div class="box {CN[env]}"><div class="bh">{head}</div><div class="bc">\n{convert_inner(body,chnum)}\n</div></div>'
    if env == "例題":
        # 内部の\begin{解答}...\end{解答}を取り出す
        sol = ""
        ms = re.search(r"\\begin\{解答\}(.*?)\\end\{解答\}", body, re.S)
        prob = body
        if ms:
            sol = ms.group(1); prob = body[:ms.start()]+body[ms.end():]
        head = "例題" + (("　"+opt) if opt else "")
        h = f'<div class="box rei"><div class="bh">{head}</div><div class="bc">\n{convert_inner(prob,chnum)}\n'
        if sol:
            h += f'<div class="box sol"><div class="bh">解答</div><div class="bc">\n{convert_inner(sol,chnum)}\n</div></div>\n'
        h += "</div></div>"
        return h
    if env in ("問","章末問題"):
        head = "問" if env=="問" else "章末問題"
        return f'<div class="box prob"><div class="bh">{head}</div>{items_to_ol(body)}</div>'
    if env == "screen":
        return f'<div class="box screen"><div class="bc">\n{convert_inner(body,chnum)}\n</div></div>'
    if env == "COLUMN":
        b = re.sub(r"\\FIVEjidori\{\{?\\bf\s*([^{}]*)\}?\}", r"<p><b>\1</b></p>", body)
        return f'<div class="box column"><div class="bh">コラム</div><div class="bc">\n{convert_inner(b,chnum)}\n</div></div>'
    if env == "箇条書":
        its = re.split(r"\\item", body)
        lis = "".join("<li>"+inline(x.strip())+"</li>" for x in its if x.strip())
        return "<ul>"+lis+"</ul>"
    if env in ("figure","table"):
        return render_float(body, env)
    return ""

def convert_inner(body, chnum):
    # 環境内の本文（数式・箇条書・inline）
    body = body.strip()
    # 内部の箇条書
    body = re.sub(r"\\begin\{箇条書\}(.*?)\\end\{箇条書\}",
                  lambda m: "\x00UL"+m.group(1)+"\x00", body, flags=re.S)
    out=[]
    for p in re.split(r"\n\s*\n", body):
        p=p.strip()
        if not p: continue
        if p.startswith("\x00UL"):
            its=re.split(r"\\item", p[3:].strip("\x00"))
            out.append("<ul>"+"".join("<li>"+inline(x.strip())+"</li>" for x in its if x.strip())+"</ul>")
        elif re.match(r"\\begin\{(equation|eqnarray|align)", p):
            out.append(p)
        else:
            out.append("<p>"+inline(p)+"</p>")
    return "\n".join(out)

def render_float(body, env):
    imgs = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{figures/([\w.]+)\.eps\}", body)
    capm = re.search(r"\\caption\{(.*?)\}\s*\\label", body, re.S) or re.search(r"\\caption\{(.*?)\}", body, re.S)
    labm = re.search(r"\\label\{([^}]+)\}", body)
    cap = inline(capm.group(1).strip()) if capm else ""
    num = LAB.get(labm.group(1), "") if labm else ""
    kind = "図" if (imgs and imgs[0].startswith("fig")) else "表"
    h = "<figure>"
    for ig in imgs:
        h += svg_img(ig, kind+num)
    if cap:
        h += f'<figcaption><b>{kind}{num}</b>　{cap}</figcaption>'
    h += "</figure>"
    return h

for chnum in range(0, 12):
    fn = f"{ROOT}/contents/chapter{chnum:02d}.tex"
    tex = open(fn, encoding="utf-8").read()
    # \chapter{...} or \chapter*{...}
    cm = re.search(r"\\chapter\*?\{([^}]*)\}", tex)
    ctitle = re.sub(r"\\quad", " ", cm.group(1)) if cm else TITLES[chnum]
    body = tex[cm.end():] if cm else tex
    body = re.sub(r"\\label\{chap\d+\}", "", body, count=1)
    chno = "序章" if chnum==0 else f"第{chnum}章"
    disp = TITLES[chnum]
    prev = "index.html" if chnum==0 else f"ch{chnum-1:02d}.html"
    nxt = f"ch{chnum+1:02d}.html" if chnum<11 else "index.html"
    head = HEAD.replace("序章 すべての電気工学は電磁気現象である｜電磁回路理論",
                        f"{chno} {disp}｜パワーエレクトロニクス")
    bodyhtml = convert_body(body, chnum)
    page = head + f'''<body>
<div class="topbar"><a href="{prev}">← 前</a><span>パワーエレクトロニクス</span><a href="{nxt}">次 →</a></div>
<div class="page">
<div class="chno">{chno}</div>
<h1>{disp}</h1>
{bodyhtml}
<div class="topbar" style="margin-top:40px"><a href="{prev}">← 前</a><span></span><a href="{nxt}">次 →</a></div>
</div></body></html>'''
    open(f"{ROOT}/../docs/ch{chnum:02d}.html", "w", encoding="utf-8").write(page)
    print(f"ch{chnum:02d}: {len(bodyhtml)} chars")
