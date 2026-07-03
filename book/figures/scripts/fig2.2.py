#!/usr/bin/env python3
# fig2.2（第2章）: 本章で扱う5つの半導体スイッチ。回路記号と半導体の層構成，
# 制御のしかたを1枚に並べた見取り図。
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from matplotlib import font_manager as fm

JP = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
plt.rcParams["axes.unicode_minus"] = False

BLUE = "#2a5db0"
RED = "#c0392b"
LC = "#333"

fig, ax = plt.subplots(figsize=(4.4, 3.0))

COLS = [1.0, 2.9, 4.8, 6.7, 8.6]   # 各素子の中心x
YSYM = 5.6                          # 記号の中心y
YLAY = 2.9                          # 層構成の中心y

def wire(x0, y0, x1, y1, lw=1.0):
    ax.plot([x0, x1], [y0, y1], color=LC, lw=lw, solid_capstyle="round")

def layers(xc, labels, w=0.42, h=0.7):
    n = len(labels)
    x0 = xc - n * w / 2
    for i, lab in enumerate(labels):
        fc = "#eaf0fa" if lab.startswith("n") else "#fdeceb"
        ax.add_patch(Rectangle((x0 + i * w, YLAY - h / 2), w, h, fc=fc, ec="#555", lw=0.8))
        ax.text(x0 + i * w + w / 2, YLAY, lab, ha="center", va="center", fontsize=7.4)
    wire(x0 - 0.35, YLAY, x0, YLAY)
    wire(x0 + n * w, YLAY, x0 + n * w + 0.35, YLAY)
    return x0, x0 + n * w

# ============ ダイオード ============
xc = COLS[0]
wire(xc - 0.75, YSYM, xc - 0.28, YSYM)
wire(xc + 0.28, YSYM, xc + 0.75, YSYM)
ax.add_patch(Polygon([(xc - 0.28, YSYM + 0.3), (xc - 0.28, YSYM - 0.3), (xc + 0.28, YSYM)],
                     closed=True, fc="black", ec="black"))
wire(xc + 0.28, YSYM - 0.35, xc + 0.28, YSYM + 0.35, lw=1.4)
ax.text(xc - 0.75, YSYM + 0.35, "A", ha="center", fontsize=7.4)
ax.text(xc + 0.75, YSYM + 0.35, "K", ha="center", fontsize=7.4)
layers(xc, ["p", "n"])

# ============ BJT ============
xc = COLS[1]
wire(xc - 0.15, YSYM - 0.55, xc - 0.15, YSYM + 0.55, lw=1.6)   # ベースバー
wire(xc - 0.75, YSYM, xc - 0.15, YSYM)                          # B
wire(xc - 0.15, YSYM + 0.25, xc + 0.55, YSYM + 0.7)             # C
wire(xc - 0.15, YSYM - 0.25, xc + 0.55, YSYM - 0.7)             # E
ax.annotate("", xy=(xc + 0.55, YSYM - 0.7), xytext=(xc + 0.18, YSYM - 0.46),
            arrowprops=dict(arrowstyle="-|>", lw=1.0, color=LC))
ax.text(xc - 0.75, YSYM + 0.3, "B", ha="center", fontsize=7.4)
ax.text(xc + 0.78, YSYM + 0.72, "C", ha="center", fontsize=7.4)
ax.text(xc + 0.78, YSYM - 0.78, "E", ha="center", fontsize=7.4)
x0, x1 = layers(xc, ["n", "p", "n"])
wire(xc, YLAY - 0.35, xc, YLAY - 0.62)   # ベース端子

# ============ MOSFET ============
xc = COLS[2]
wire(xc - 0.42, YSYM - 0.55, xc - 0.42, YSYM + 0.55, lw=1.4)     # ゲート電極
for dy in (-0.42, 0.0, 0.42):                                     # チャネル3分割
    wire(xc - 0.2, YSYM + dy - 0.14, xc - 0.2, YSYM + dy + 0.14, lw=1.6)
wire(xc - 0.75, YSYM - 0.55, xc - 0.42, YSYM - 0.55)              # G
wire(xc - 0.2, YSYM + 0.42, xc + 0.45, YSYM + 0.42)               # D
wire(xc + 0.45, YSYM + 0.42, xc + 0.45, YSYM + 0.7)
wire(xc - 0.2, YSYM - 0.42, xc + 0.45, YSYM - 0.42)               # S
wire(xc + 0.45, YSYM - 0.42, xc + 0.45, YSYM - 0.7)
wire(xc - 0.2, YSYM, xc + 0.45, YSYM)
wire(xc + 0.45, YSYM, xc + 0.45, YSYM - 0.42)
ax.annotate("", xy=(xc - 0.2, YSYM), xytext=(xc + 0.16, YSYM),
            arrowprops=dict(arrowstyle="-|>", lw=1.0, color=LC))
ax.text(xc - 0.85, YSYM - 0.55, "G", ha="right", va="center", fontsize=7.4)
ax.text(xc + 0.45, YSYM + 0.82, "D", ha="center", fontsize=7.4)
ax.text(xc + 0.45, YSYM - 0.95, "S", ha="center", fontsize=7.4)
x0, x1 = layers(xc, ["n", "p", "n"])
ax.add_patch(Rectangle((xc - 0.45, YLAY - 0.62), 0.9, 0.14, fc="#ddd", ec="#555", lw=0.7))
ax.add_patch(Rectangle((xc - 0.35, YLAY - 0.78), 0.7, 0.16, fc="#bbb", ec="#555", lw=0.7))
wire(xc, YLAY - 0.78, xc, YLAY - 0.98)

# ============ IGBT ============
xc = COLS[3]
wire(xc - 0.42, YSYM - 0.55, xc - 0.42, YSYM + 0.55, lw=1.4)     # ゲート
wire(xc - 0.2, YSYM - 0.55, xc - 0.2, YSYM + 0.55, lw=1.6)       # ボディバー
wire(xc - 0.75, YSYM - 0.55, xc - 0.42, YSYM - 0.55)             # G
wire(xc - 0.2, YSYM + 0.25, xc + 0.5, YSYM + 0.7)                # C
wire(xc - 0.2, YSYM - 0.25, xc + 0.5, YSYM - 0.7)                # E
ax.annotate("", xy=(xc + 0.5, YSYM - 0.7), xytext=(xc + 0.14, YSYM - 0.47),
            arrowprops=dict(arrowstyle="-|>", lw=1.0, color=LC))
ax.text(xc - 0.85, YSYM - 0.55, "G", ha="right", va="center", fontsize=7.4)
ax.text(xc + 0.73, YSYM + 0.72, "C", ha="center", fontsize=7.4)
ax.text(xc + 0.73, YSYM - 0.78, "E", ha="center", fontsize=7.4)
x0, x1 = layers(xc, ["n", "p", "n", "p"])
ax.add_patch(Rectangle((xc - 0.62, YLAY - 0.62), 0.9, 0.14, fc="#ddd", ec="#555", lw=0.7))
ax.add_patch(Rectangle((xc - 0.52, YLAY - 0.78), 0.7, 0.16, fc="#bbb", ec="#555", lw=0.7))
wire(xc - 0.17, YLAY - 0.78, xc - 0.17, YLAY - 0.98)

# ============ サイリスタ ============
xc = COLS[4]
wire(xc - 0.75, YSYM, xc - 0.28, YSYM)
wire(xc + 0.28, YSYM, xc + 0.75, YSYM)
ax.add_patch(Polygon([(xc - 0.28, YSYM + 0.3), (xc - 0.28, YSYM - 0.3), (xc + 0.28, YSYM)],
                     closed=True, fc="black", ec="black"))
wire(xc + 0.28, YSYM - 0.35, xc + 0.28, YSYM + 0.35, lw=1.4)
wire(xc - 0.05, YSYM - 0.17, xc + 0.3, YSYM - 0.75)               # ゲート
ax.text(xc - 0.75, YSYM + 0.35, "A", ha="center", fontsize=7.4)
ax.text(xc + 0.75, YSYM + 0.35, "K", ha="center", fontsize=7.4)
ax.text(xc + 0.42, YSYM - 0.9, "G", ha="center", fontsize=7.4)
x0, x1 = layers(xc, ["p", "n", "p", "n"])
wire(xc + 0.05, YLAY - 0.35, xc + 0.05, YLAY - 0.62)

# ============ 見出しと制御方式 ============
names = ["ダイオード", "BJT", "MOSFET", "IGBT", "サイリスタ"]
ctrl = ["制御端子なし\n（電圧の向き）", "ベース電流\nで制御", "ゲート電圧\nで制御",
        "ゲート電圧\nで制御", "ゲート電流で\nオンのみ制御"]
for xc, nm, ct in zip(COLS, names, ctrl):
    ax.text(xc, 6.9, nm, ha="center", fontsize=8.0, fontproperties=JP)
    ax.text(xc, 1.35, ct, ha="center", va="top", fontsize=6.8,
            fontproperties=JP, color="#555")

ax.set_xlim(-0.1, 9.7)
ax.set_ylim(0.4, 7.3)
ax.axis("off")
fig.tight_layout()
EPS = os.path.expanduser("~/text_power_electronics/book/figures/fig2.2.eps")
fig.savefig(EPS, format="eps", bbox_inches="tight")
print("wrote", EPS)
