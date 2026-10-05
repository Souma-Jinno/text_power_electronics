"""教科書 book/main.pdf を 1 頁ずつ PNG にし、赤枠レビュー画面の一覧 figs.js を作る。
main.pdf を作り直したら: python3 book/review/make_pages.py"""
import glob, json, os, subprocess, time
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); BOOK = os.path.dirname(HERE)
pdf = os.path.join(BOOK, "main.pdf")
for f in glob.glob(os.path.join(HERE, "pages", "p-*.png")): os.remove(f)
subprocess.run(["pdftoppm", "-png", "-r", "150", pdf, os.path.join(HERE, "pages", "p")], check=True)
v = str(int(time.time())); figs = []
for f in sorted(glob.glob(os.path.join(HERE, "pages", "p-*.png")), key=lambda s: int(s.rsplit("-", 1)[1][:-4])):
    n = int(f.rsplit("-", 1)[1][:-4]); w, h = Image.open(f).size
    figs.append({"name": f"p{n}", "png": "review/pages/" + os.path.basename(f) + "?v=" + v, "compare": None, "prev": None, "cur": None, "w": w, "h": h})
open(os.path.join(HERE, "figs.js"), "w").write(f"window.ROUND=\"{int(time.time())}\";\n" + "window.FIGS=" + json.dumps(figs, ensure_ascii=False) + ";\n")
print(len(figs), "pages")
