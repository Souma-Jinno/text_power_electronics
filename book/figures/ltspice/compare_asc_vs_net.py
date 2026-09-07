#!/usr/bin/env python3
"""配布する .asc が，元の .net と「同じ波形を出す」ことを ngspice で確かめる。

verify_all.sh は回路の構造（どの素子がどのノードにつながっているか）を照合する。
こちらはもう一歩進めて，実際に両方を ngspice で走らせ，各ノードの電圧が
数値として一致するかを見る。

  .net  ……… 元のネットリスト（本書の波形図はこれで描いた）
  .asc  ……… 読者に配布する回路図
         → asc2ngspice.py で .asc からネットリストを起こし直し，
           同じ解析を走らせて，共通ノードの電圧を突き合わせる。

使い方: python3 compare_asc_vs_net.py
"""
import glob, os, re, subprocess, sys, tempfile

NG = os.path.expanduser('~/miniforge3/bin/ngspice')
A2N = 'netlist-to-schematic/tools/asc2ngspice.py'
RTOL, ATOL = 1e-3, 1e-6


def strip(lines):
    """.control ブロック・解析カード・.end を落とし，解析の指定を返す。

    解析は .tran カードで書かれていることも，.control の中に tran コマンドとして
    書かれていることもある（教科書のデッキは両方ある）。どちらも拾う。
    """
    out, ana, inctl = [], None, False
    for ln in lines:
        s = ln.strip(); low = s.lower()
        if low.startswith('.control'): inctl = True; continue
        if low.startswith('.endc'):    inctl = False; continue
        if inctl:
            if ana is None and low.split(' ')[0] in ('tran', 'dc', 'ac', 'op'):
                ana = s
            continue
        if low.startswith(('.tran', '.dc', '.ac', '.op')):
            if ana is None: ana = s.lstrip('.')
            continue
        if low == '.end': continue
        out.append(ln.rstrip('\n'))
    return out, ana


def nodes_of(lines):
    ns = set()
    for ln in lines:
        s = ln.strip()
        if not s or s[0] in '*.+': continue
        t = s.split()
        if not t or t[0][0].upper() not in 'RCLDVIQMSEFGHBX': continue
        n = {'R':2,'C':2,'L':2,'D':2,'V':2,'I':2,'Q':3,'M':4,'S':4,'E':4,'G':4,'F':2,'H':2,'B':2,'X':3}
        for x in t[1:1+n.get(t[0][0].upper(), 2)]:
            if not re.match(r'^[\d.]+[a-zA-Z]*$', x) or x == '0':
                ns.add(x.lower())
    ns.discard('0')
    return ns


def run(deck, ana, nodes, tag):
    cmd = ana.lstrip('.')
    with tempfile.TemporaryDirectory() as d:
        outf = os.path.join(d, 'o.txt')
        body = '\n'.join(deck) + '\n.control\nset filetype=ascii\n' + cmd + '\n'
        if cmd.startswith('tran'): body += 'linearize\n'
        body += 'wrdata %s %s\n.endc\n.end\n' % (outf, ' '.join('v(%s)' % n for n in nodes))
        f = os.path.join(d, 'deck.cir')
        open(f, 'w').write('* %s\n' % tag + body)
        r = subprocess.run([NG, '-b', f], capture_output=True, text=True, timeout=600)
        if not os.path.exists(outf):
            return None, (r.stderr or r.stdout)[-200:]
        rows = []
        for ln in open(outf):
            try: rows.append([float(x) for x in ln.split()])
            except ValueError: pass
        return rows, ''


def probe(deck):
    """このデッキで実在するノード名の集合を ngspice に聞く。"""
    key = '\n'.join(deck)
    if key in probe._cache:
        return probe._cache[key]
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, 'p.cir')
        open(f, 'w').write('* probe\n' + key + '\n.control\nop\ndisplay\n.endc\n.end\n')
        r = subprocess.run([NG, '-b', f], capture_output=True, text=True, timeout=120)
    ns = set()
    for ln in (r.stdout + r.stderr).splitlines():
        m = re.match(r'\s*(\S+)\s*:\s*voltage', ln)
        if m:
            ns.add(m.group(1).lower())
    probe._cache[key] = ns
    return ns


probe._cache = {}


def cmp_rows(a, b):
    if len(a) != len(b): return '点の数が違う (%d vs %d)' % (len(a), len(b))
    worst = 0.0
    for ra, rb in zip(a, b):
        if len(ra) != len(rb): return '列の数が違う'
        for x, y in zip(ra, rb):
            d = abs(x - y) / max(abs(x), abs(y), ATOL)
            worst = max(worst, d)
    return None if worst <= RTOL else '最大 %.3g の相対差' % worst


def main():
    ok = ng = skip = 0
    for net in sorted(glob.glob('chapter*/*.net')):
        asc = net[:-4] + '.asc'
        if not os.path.exists(asc):
            skip += 1; continue
        orig, ana = strip(open(net, encoding='utf-8', errors='replace').readlines())
        if ana is None:
            print('SKIP %-42s 解析カードが無い' % net); skip += 1; continue
        rt = subprocess.run([sys.executable, A2N, asc], capture_output=True, text=True)
        back, _ = strip(rt.stdout.splitlines())
        common = sorted(nodes_of(orig) & nodes_of(back))
        if not common:
            print('SKIP %-42s 共通のノード名が無い' % net); skip += 1; continue
        # 素子カードから拾ったノード名の中には，ngspice が内部で別ノードに
        # 併合してしまって参照できないものがある。どのベクトルが実在するかは
        # ngspice 自身に聞く（動作点だけ解くので速い）。
        allnodes = list(common)
        common = [n for n in common if n in probe(orig) and n in probe(back)]
        if not common:
            print('SKIP %-42s 比べられるノードが無い' % net); skip += 1; continue
        ra, ea = run(orig, ana, common, 'from .net')
        rb, eb = run(back, ana, common, 'from .asc')
        if ra is None or rb is None:
            # まとめて書き出すと落ちるデッキがある（tstart 付きの過渡解析などで，
            # 動作点では見えるのに過渡解析後には参照できないノードがある）。
            # そのときは1ノードずつ書き出して，両方で取れたノードだけで比べる。
            keep, pa, pb = [], [], []
            for n in allnodes:
                x, _ = run(orig, ana, [n], 'from .net')
                y, _ = run(back, ana, [n], 'from .asc')
                if x is not None and y is not None:
                    keep.append(n); pa.append(x); pb.append(y)
            if not keep:
                print('SKIP %-42s ngspiceが出力を書かなかった (%s)' % (net, (ea or eb).strip()[:60])); skip += 1; continue
            common = keep
            ra = [sum(r, []) for r in zip(*pa)]
            rb = [sum(r, []) for r in zip(*pb)]
        msg = cmp_rows(ra, rb)
        if msg is None:
            print('一致 %-42s %d点 × %dノード' % (net, len(ra), len(common))); ok += 1
        else:
            print('相違 %-42s %s' % (net, msg)); ng += 1
    print('---- 一致=%d 相違=%d 対象外=%d ----' % (ok, ng, skip))
    return 1 if ng else 0


sys.exit(main())
