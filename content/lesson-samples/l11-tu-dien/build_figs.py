"""Sinh 3 hình SVG và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được).
Hình 2 vẽ đúng số liệu bảng thí nghiệm tn-l11-tudien-02 (C ≈ 480 μF)."""
import pathlib, re
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent

def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'

def dot(x, y, r=4, c="currentColor"): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'

def sub(base, s, x, y, c="currentColor", size=13, anchor="start", weight="700"):
    size = max(size, 13)
    """Chữ có chỉ số dưới (không dùng KaTeX trong SVG)."""
    return (f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{base}<tspan baseline-shift="sub" font-size="{max(size-3, 11)}">{s}</tspan></text>')

def subs(parts, x, y, c="currentColor", size=12, anchor="start", weight="600"):
    size = max(size, 13)
    """Một dòng chữ nhiều chỉ số dưới: parts = [("U = U", "1"), (" + U", "2")]."""
    t = "".join(f'<tspan>{a}</tspan><tspan baseline-shift="sub" font-size="{max(size-3, 11)}">{s}</tspan>' for a, s in parts)
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{t}</text>'

def cap_sym(x, y, h=30, gap=10, c="currentColor"):
    """Kí hiệu tụ nằm ngang: hai vạch đứng tại x và x+gap, tâm y."""
    return line(x, y - h / 2, x, y + h / 2, c, 3.5) + line(x + gap, y - h / 2, x + gap, y + h / 2, c, 3.5)

# ---------------- Hình 1: cấu tạo tụ phẳng nối nguồn + kí hiệu
b = defs("f1")
L, R, top, bot = 170, 250, 40, 160          # bản trái (x 170–176), bản phải (x 244–250)
b += f'<rect x="176" y="{top}" width="68" height="{bot-top}" fill="{ORG}" opacity=".15"/>'
b += f'<rect x="{L}" y="{top}" width="6" height="{bot-top}" fill="{RED}"/>'
b += f'<rect x="244" y="{top}" width="6" height="{bot-top}" fill="{BLUE}"/>'
for y in (58, 86, 114, 142):
    b += text(183, y + 5, "+", RED, 15, "middle", "700") + text(237, y + 5, "−", BLUE, 15, "middle", "700")
for y in (72, 100, 128):
    b += arrow("f1", "g", 192, y, 226, y, 2)
b += text(209, 92, "E", GRN, 12, "middle", "700")
b += text(173, 30, "bản +Q", RED, 12, "middle", "700") + text(250, 30, "bản −Q", BLUE, 12, "middle", "700")
b += text(210, 178, "điện môi", ORG, 12, "middle", "700")
# dây nối nguồn: bản trái -> cực dương (vạch dài), bản phải -> cực âm (vạch ngắn)
b += line(L, 100, 90, 100) + line(90, 100, 90, 210) + line(90, 210, 200, 210)
b += line(200, 196, 200, 224, "currentColor", 3) + line(212, 202, 212, 218, "currentColor", 5)
b += line(212, 210, 330, 210) + line(330, 210, 330, 100) + line(330, 100, R, 100)
b += text(194, 194, "+", RED, 13, "end", "700") + text(218, 200, "−", BLUE, 13, "start", "700")
b += text(206, 238, "nguồn U", "currentColor", 12, "middle", "600")
# kí hiệu tụ trong sơ đồ
b += line(352, 30, 352, 232, "currentColor", 1, "3 4", .4)
b += line(362, 120, 392, 120) + cap_sym(392, 120) + line(402, 120, 432, 120)
b += text(397, 92, "kí hiệu", "currentColor", 12, "middle", "600")
fig1 = wrap("0 0 440 246", "Tụ điện phẳng: hai bản kim loại song song, giữa là điện môi, nối với hai cực nguồn; bên phải là kí hiệu tụ",
            b, "Hình 1. Tụ điện phẳng nối với nguồn: bản nối cực dương tích +Q, bản kia −Q; điện trường E (lục) hướng từ bản + sang bản −. Bên phải: kí hiệu tụ trong sơ đồ.")

# ---------------- Hình 2: đồ thị Q theo U (số liệu thí nghiệm) + diện tích = năng lượng
DATA = [(2, 980), (4, 1900), (6, 2890), (8, 3820), (10, 4800)]
C_FIT = 480                                   # μF, đường thẳng Q = 480·U
X0, Y0, SX, SY = 60, 200, 34, 0.034            # gốc, px/V, px/μC
X = lambda u: X0 + SX * u
Y = lambda q: Y0 - SY * q
b = defs("f2")
U_SH = 8
b += (f'<polygon points="{X(0)},{Y(0)} {X(U_SH)},{Y(0)} {X(U_SH)},{Y(C_FIT*U_SH):.1f}" '
      f'fill="{ORG}" opacity=".28"/>')
b += line(X0, Y0, X(11), Y0, "currentColor", 1.6) + line(X0, Y0, X0, Y(5600), "currentColor", 1.6)
for u in (2, 4, 6, 8, 10):
    b += line(X(u), Y0, X(u), Y0 + 5, "currentColor", 1.2) + text(X(u), Y0 + 18, str(u), "currentColor", 11, "middle", "400")
for q in (2000, 4000):
    b += line(X0 - 5, Y(q), X0, Y(q), "currentColor", 1.2) + text(X0 - 8, Y(q) + 4, str(q), "currentColor", 11, "end", "400")
b += text(X(11), Y0 - 7, "U (V)", "currentColor", 12, "end", "700")
b += text(X0 + 6, Y(5600) + 4, "Q (μC)", "currentColor", 12, "start", "700")
b += line(X(0), Y(0), X(10.6), Y(C_FIT * 10.6), RED, 2.2)
for u, q in DATA:
    b += dot(X(u), Y(q), 4.5, BLUE)
b += text(X(4.2), Y(2900), "Q = C·U", RED, 12, "end", "700")
b += text(X(5.6), Y(450), "W = ½QU", ORG, 13, "middle", "700")
b += line(X(U_SH), Y(C_FIT*U_SH), X(U_SH), Y0, ORG, 1.2, "3 3")
fig2 = wrap("0 0 440 230", "Đồ thị Q theo U: năm điểm đo nằm sát đường thẳng qua gốc, hệ số góc C khoảng 480 microfara; diện tích tam giác dưới đường là năng lượng",
            b, "Hình 2. Năm điểm đo (xanh) nằm sát đường thẳng qua gốc: Q tỉ lệ U, hệ số góc là C ≈ 480 μF. Phần tô cam (tam giác tới U = 8 V) là năng lượng W = ½QU.")

# ---------------- Hình 3: ghép nối tiếp và song song
b = ""
# nối tiếp: y = 80, A(20) — C1(80..90) — C2(150..160) — B(220)
yS = 84
b += text(110, 20, "Nối tiếp", "currentColor", 13, "middle", "700")
b += dot(22, yS, 4) + line(22, yS, 80, yS) + cap_sym(80, yS) + line(90, yS, 150, yS) + cap_sym(150, yS) + line(160, yS, 202, yS) + dot(202, yS, 4)
b += sub("C", "1", 85, yS - 24, "currentColor", 13, "middle") + sub("C", "2", 155, yS - 24, "currentColor", 13, "middle")
b += text(110, 136, "Q chung", RED, 13, "middle", "700")
b += subs([("U = U", "1"), (" + U", "2")], 110, 160, anchor="middle")
b += text(22, yS + 22, "A", "currentColor", 12, "middle", "700") + text(202, yS + 22, "B", "currentColor", 12, "middle", "700")
# song song: A(248) — hai nhánh y=60, y=110 — B(422)
xa, xb, y1, y2 = 250, 420, 58, 112
b += line(226, 58 + 1, 226, 172, "currentColor", 1, "3 4", .4)
b += text(335, 20, "Song song", "currentColor", 13, "middle", "700")
b += line(xa, y1, xa, y2) + line(xb, y1, xb, y2)
b += dot(xa, 85, 4) + dot(xb, 85, 4) + text(xa - 8, 89, "A", "currentColor", 12, "end", "700") + text(xb + 8, 89, "B", "currentColor", 12, "start", "700")
for y, n in ((y1, "1"), (y2, "2")):
    b += line(xa, y, 330, y) + cap_sym(330, y, 26) + line(340, y, xb, y)
    b += sub("C", n, 324, y - 10, "currentColor", 13, "end")
b += text(335, 150, "U chung", BLUE, 13, "middle", "700")
b += subs([("Q = Q", "1"), (" + Q", "2")], 335, 172, anchor="middle")
fig3 = wrap("0 0 440 184", "Sơ đồ hai tụ ghép nối tiếp (bên trái) và ghép song song (bên phải)",
            b, "Hình 3. Nối tiếp: các tụ chung điện tích Q, hiệu điện thế cộng lại. Song song: các tụ chung hiệu điện thế U, điện tích cộng lại.")

h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, f in enumerate((fig1, fig2, fig3), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", f)
(HERE / "theory.html").write_text(h, encoding="utf8")
print("ok", len(h))
