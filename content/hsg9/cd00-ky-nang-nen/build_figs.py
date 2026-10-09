"""Sinh 3 hình SVG, thay <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được).
Chạy: python3 content/hsg9/cd00-ky-nang-nen/build_figs.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "soan-bai-ly-thuyet-tuong-tac", "scripts"))
from svg_lib import RED, BLUE, ORG, GRN, text, wrap, chevron

def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'

def rect(x, y, w, h, fill, stroke):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'

def dot(x, y, c, r=5):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'

def sub(main, s, c="currentColor", x=0, y=0, size=14, anchor="start"):
    return (f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="600" text-anchor="{anchor}">{main}'
            f'<tspan baseline-shift="sub" font-size="{size-3}">{s}</tspan></text>')

def axes(X0, Y0, xend, ytop):
    b = line(X0, Y0, xend, Y0, "currentColor", 1.8) + chevron(xend, Y0, 1, 0, "currentColor", 1.8, 9)
    b += line(X0, Y0, X0, ytop, "currentColor", 1.8) + chevron(X0, ytop, 0, -1, "currentColor", 1.8, 9)
    return b

def fmt(v, nd=1):
    return f"{v:.{nd}f}".replace(".", ",")

# ---------- Hình 1: đồ thị U–I, hệ số góc, nội suy ----------
X0, Y0, kx, ky = 70, 250, 700.0, 28.0          # px: gốc ; px/A ; px/V
X = lambda i: X0 + kx * i
Y = lambda u: Y0 - ky * u
R = 15.0
pts = [(0.0, 0.0), (0.1, 1.5), (0.2, 3.0), (0.3, 4.5), (0.4, 6.0)]
assert all(abs(u - R * i) < 1e-9 for i, u in pts)       # các điểm nằm đúng trên U = 15·I
b = axes(X0, Y0, 425, 16)
for i in (0.1, 0.2, 0.3, 0.4, 0.5):
    b += line(X(i), Y0, X(i), Y0 + 5, "currentColor", 1.4) + text(X(i), Y0 + 21, fmt(i), "currentColor", 14, "middle", "400")
b += text(X(0), Y0 + 21, "0", "currentColor", 14, "middle", "400")
for u in (2, 4, 6, 8):
    b += line(X0 - 5, Y(u), X0, Y(u), "currentColor", 1.4) + text(X0 - 9, Y(u) + 5, str(u), "currentColor", 14, "end", "400")
b += text(422, Y0 + 40, "I (A)", "currentColor", 14, "end", "700") + text(X0 + 8, 20, "U (V)", "currentColor", 14, "start", "700")
b += line(X(0), Y(0), X(0.44), Y(R * 0.44), BLUE, 2.6)
# tam giác hệ số góc giữa (0,1; 1,5) và (0,4; 6,0)
b += line(X(0.1), Y(1.5), X(0.4), Y(1.5), GRN, 2, "6 4") + line(X(0.4), Y(1.5), X(0.4), Y(6.0), GRN, 2, "6 4")
b += text(X(0.25) - 8, Y(1.5) + 21, "ΔI = 0,30 A", GRN, 14, "end", "700")
b += text(X(0.4) + 8, (Y(1.5) + Y(6.0)) / 2 + 5, "ΔU = 4,5 V", GRN, 14, "start", "700")
b += text(100, 70, "R = ΔU/ΔI = 15 Ω", BLUE, 15, "start", "700")
# nội suy U = 3,75 V -> I = 0,25 A
b += line(X0, Y(3.75), X(0.25), Y(3.75), ORG, 1.6, "4 4") + line(X(0.25), Y(3.75), X(0.25), Y0, ORG, 1.6, "4 4")
b += f'<circle cx="{X(0.25):.1f}" cy="{Y(3.75):.1f}" r="6" fill="none" stroke="{ORG}" stroke-width="2.4"/>'
b += text(X(0.25) - 8, Y(3.75) - 28, "nội suy: U = 3,75 V", ORG, 14, "end", "700")
b += text(X(0.25) - 8, Y(3.75) - 10, "cho I = 0,25 A", ORG, 14, "end", "700")
for i, u in pts:
    b += dot(X(i), Y(u), RED)
fig1 = wrap("0 0 440 292", "Đồ thị U theo I của một dây dẫn: đường thẳng qua gốc, hệ số góc 15 ôm",
            b, "Hình 1. Bốn điểm đo và gốc toạ độ nằm trên đường thẳng qua gốc: U tỉ lệ thuận với I. Hệ số góc là R = 15 Ω.")

# ---------- Hình 2: đồ thị P–t bậc thang ----------
X0, Y0, kx, ky = 64, 200, 336 / 900, 0.14       # px: gốc ; px/s ; px/W
X = lambda t: X0 + kx * t
Y = lambda p: Y0 - ky * p
b = axes(X0, Y0, 424, 14)
b += rect(X(0), Y(800), X(300) - X(0), 800 * ky, "rgba(56,189,248,.25)", BLUE)
b += rect(X(300), Y(1200), X(900) - X(300), 1200 * ky, "rgba(251,146,60,.25)", ORG)
for t in (0, 300, 900):
    b += line(X(t), Y0, X(t), Y0 + 5, "currentColor", 1.4) + text(X(t), Y0 + 21, str(t), "currentColor", 14, "middle", "400")
for p in (800, 1200):
    b += line(X0 - 5, Y(p), X0, Y(p), "currentColor", 1.4) + text(X0 - 9, Y(p) + 5, str(p), "currentColor", 14, "end", "400")
b += text(424, Y0 + 40, "t (s)", "currentColor", 14, "end", "700") + text(X0 + 8, 20, "P (W)", "currentColor", 14, "start", "700")
b += sub("A", "1", BLUE, X(150), Y(400) - 6, 15, "middle") + text(X(150), Y(400) + 14, "800·300", "currentColor", 14, "middle", "400")
b += text(X(150), Y(400) + 32, "= 240 000 J", BLUE, 14, "middle", "700")
b += sub("A", "2", ORG, X(600), Y(600) - 6, 15, "middle") + text(X(600), Y(600) + 14, "1 200·600", "currentColor", 14, "middle", "400")
b += text(X(600), Y(600) + 32, "= 720 000 J", ORG, 14, "middle", "700")
fig2 = wrap("0 0 440 246", "Đồ thị công suất theo thời gian dạng bậc thang: diện tích hai hình chữ nhật là điện năng",
            b, "Hình 2. Bếp điện hai giai đoạn (5 phút = 300 s, 15 phút = 900 s). Diện tích mỗi hình chữ nhật là điện năng của giai đoạn đó.")

# ---------- Hình 3: năm lần đo và khoảng 5,9 ± 0,1 ----------
V0, X0, kx, Y0 = 5.6, 40, 600.0, 100
X = lambda v: X0 + kx * (v - V0)
b = line(X0, Y0, 420, Y0, "currentColor", 1.8) + chevron(420, Y0, 1, 0, "currentColor", 1.8, 9)
b += rect(X(5.8), 38, X(6.0) - X(5.8), Y0 - 38, "rgba(56,189,248,.22)", BLUE)
b += line(X(5.9), 38, X(5.9), Y0, BLUE, 1.6, "5 4")
for k in range(7):
    v = V0 + 0.1 * k
    b += line(X(v), Y0, X(v), Y0 + 5, "currentColor", 1.4) + text(X(v), Y0 + 22, fmt(v), "currentColor", 16, "middle", "400")
for v, n in ((5.8, 2), (5.9, 2), (6.1, 1)):
    for j in range(n):
        b += dot(X(v), Y0 - 12 - 18 * j, ORG, 7)
b += text(X(5.9), 28, "5,9 ± 0,1", BLUE, 17, "middle", "700")
b += text(420, Y0 + 44, "U (V)", "currentColor", 16, "end", "700")
fig3 = wrap("0 0 440 150", "Năm lần đo hiệu điện thế trên trục số và khoảng 5,9 ± 0,1 V",
            b, "Hình 3. Mỗi chấm là một lần đo. Vùng tô là 5,9 ± 0,1 V; lần đo 6,1 V nằm ngoài vì sai số là mức lệch trung bình, không phải lệch lớn nhất.")

src = open(os.path.join(HERE, "theory.src.html"), encoding="utf8").read()
for n, f in ((1, fig1), (2, fig2), (3, fig3)):
    assert f"<!--FIG{n}-->" in src
    src = src.replace(f"<!--FIG{n}-->", f)
open(os.path.join(HERE, "theory.html"), "w", encoding="utf8").write(src)
print("ok", len(src))
