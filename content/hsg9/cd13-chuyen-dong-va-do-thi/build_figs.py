"""Sinh 4 hình SVG, thay <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được).
Chạy: python3 content/hsg9/cd13-chuyen-dong-va-do-thi/build_figs.py
Số liệu hình tính từ phương trình (không gõ tay toạ độ)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "soan-bai-ly-thuyet-tuong-tac", "scripts"))
from svg_lib import RED, BLUE, ORG, GRN, text, wrap, chevron, arrow

PHUT = 12   # điền theo lint_do_dai.py (làm tròn lên)


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def poly(pts, c="currentColor", w=2.6, fill="none", op=1):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polyline points="{p}" fill="{fill}" stroke="{c}" stroke-width="{w}" stroke-linejoin="round" opacity="{op}"/>'


def area(pts, c, op=0.22):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{p}" fill="{c}" fill-opacity="{op}" stroke="none"/>'


def axes(X0, Y0, xend, ytop, xlab, ylab, dy=-8):
    b = line(X0, Y0, xend, Y0, "currentColor", 1.8) + chevron(xend, Y0, 1, 0, "currentColor", 1.8, 9)
    b += line(X0, Y0, X0, ytop, "currentColor", 1.8) + chevron(X0, ytop, 0, -1, "currentColor", 1.8, 9)
    b += text(xend, Y0 + dy, xlab, "currentColor", 14, "end", "600")
    b += text(X0 + 8, ytop + 4, ylab, "currentColor", 14, "start", "600")
    return b


# ---------- Hình 1: đồ thị x–t của xe A (3 đoạn) và xe B ----------
X0, Y0, kt, kx = 46, 210, 60.0, 0.85          # gốc; px/giờ; px/km
X = lambda t: X0 + kt * t
Y = lambda x: Y0 - kx * x
A = [(0, 0), (2, 80), (3, 80), (5, 180)]       # (t giờ, x km)
B = [(0, 160), (4, 0)]
# kiểm: giao điểm A-B là (2, 80)
assert 40 * 2 == 160 - 40 * 2 == 80
b = axes(X0, Y0, 366, 30, "t (h)", "x (km)")
for t in range(1, 6):
    b += line(X(t), Y0, X(t), Y0 + 5, "currentColor", 1.4) + text(X(t), Y0 + 21, str(t), "currentColor", 14, "middle", "400")
b += text(X0 - 8, Y0 + 5, "0", "currentColor", 14, "end", "400")
for x in (40, 80, 120, 160, 200):
    b += line(X0 - 5, Y(x), X0, Y(x), "currentColor", 1.4) + text(X0 - 9, Y(x) + 5, str(x), "currentColor", 14, "end", "400")
b += line(X(2), Y(80), X(2), Y0, "currentColor", 1.2, "4 4", .6) + line(X0, Y(80), X(2), Y(80), "currentColor", 1.2, "4 4", .6)
b += poly([(X(t), Y(x)) for t, x in A], RED, 2.8)
b += poly([(X(t), Y(x)) for t, x in B], BLUE, 2.8)
b += f'<circle cx="{X(2):.1f}" cy="{Y(80):.1f}" r="5.5" fill="{ORG}"/>'
b += text(X(2) + 8, Y(80) - 14, "gặp nhau", ORG, 14, "start", "700")
b += text(X(4.2), Y(172), "A", RED, 16, "middle", "700")
b += text(X(0.35), Y(160) - 12, "B", BLUE, 16, "middle", "700")
fig1 = wrap("0 0 380 246", "Đồ thị toạ độ thời gian của xe A và xe B cắt nhau tại t bằng 2 giờ, x bằng 80 km",
            b, "Hình 1. Đồ thị x–t: xe A đi, nghỉ, đi tiếp; xe B đi về gốc O. Hai đường cắt nhau tại t = 2 h, x = 80 km.")

# ---------- Hình 3 (biến fig2): bố trí đề bài hai xe ngược chiều (chưa lộ chỗ gặp) ----------
S_AB, xa, xb, ky = 120.0, 40.0, 340.0, 1.6      # km ; px ; px ; px/(km/h)
road_y = 108
b = line(xa - 14, road_y, xb + 14, road_y, "currentColor", 2.2)


def car(cx, col):
    return (f'<rect x="{cx-17:.1f}" y="{road_y-24}" width="34" height="18" rx="3" fill="none" stroke="{col}" stroke-width="2.4"/>'
            f'<circle cx="{cx-9:.1f}" cy="{road_y-4}" r="4" fill="{col}"/><circle cx="{cx+9:.1f}" cy="{road_y-4}" r="4" fill="{col}"/>')


b += car(xa, RED) + car(xb, BLUE)
v1, v2 = 50, 30
b += arrow("", "r", xa + 22, 62, xa + 22 + ky * v1, 62, 2.6)
b += arrow("", "b", xb - 22, 62, xb - 22 - ky * v2, 62, 2.6)
b += text(xa - 14, 40, "ô tô 50 km/h", RED, 14, "start", "700")
b += text(xb + 14, 40, "xe máy 30 km/h", BLUE, 14, "end", "700")
b += text(xa, 134, "A (gốc O)", "currentColor", 15, "middle", "700")
b += text(xb, 134, "B", "currentColor", 15, "middle", "700")
b += line(xa, 154, xb, 154, "currentColor", 1.8) + line(xa, 148, xa, 160, "currentColor", 1.8) + line(xb, 148, xb, 160, "currentColor", 1.8)
b += text((xa + xb) / 2, 178, "120 km", "currentColor", 15, "middle", "700")
fig2 = wrap("0 0 380 190", "Ô tô đi từ A với 50 km/h, xe máy đi từ B với 30 km/h, ngược chiều nhau, A và B cách 120 km",
            b, "Hình 3. Hai xe xuất phát cùng lúc, đi ngược chiều. Độ dài mũi tên tỉ lệ với vận tốc.")

# ---------- Hình 4 (biến fig3): đoàn tàu qua cầu, mũi tàu đi L + S ----------
L, Sx = 80.0, 160.0                            # px: L = 1 đơn vị, S = 2L (chỉ minh hoạ, không phải số đo)
x0 = 20.0
b = text(x0, 20, "Mũi tàu vừa lên cầu", "currentColor", 14, "start", "600")
b += f'<rect x="{x0:.1f}" y="30" width="{L:.1f}" height="28" rx="3" fill="{RED}" fill-opacity=".18" stroke="{RED}" stroke-width="2.4"/>'
b += text(x0 + L / 2, 50, "L", RED, 16, "middle", "700")
b += f'<rect x="{x0+L:.1f}" y="58" width="{Sx:.1f}" height="10" fill="none" stroke="currentColor" stroke-width="2.4"/>'
b += text(x0 + L + Sx / 2, 90, "cầu dài S", "currentColor", 15, "middle", "700")
b += f'<circle cx="{x0+L:.1f}" cy="44" r="5" fill="{ORG}"/>'
y2 = 168
b += text(x0, y2 - 10, "Đuôi tàu vừa rời cầu", "currentColor", 14, "start", "600")
b += f'<rect x="{x0+L+Sx:.1f}" y="{y2}" width="{L:.1f}" height="28" rx="3" fill="{RED}" fill-opacity=".18" stroke="{RED}" stroke-width="2.4"/>'
b += text(x0 + L + Sx + L / 2, y2 + 20, "L", RED, 16, "middle", "700")
b += f'<rect x="{x0+L:.1f}" y="{y2+28}" width="{Sx:.1f}" height="10" fill="none" stroke="currentColor" stroke-width="2.4"/>'
b += f'<circle cx="{x0+2*L+Sx:.1f}" cy="{y2+14}" r="5" fill="{ORG}"/>'
ya = 128
b += line(x0 + L, 62, x0 + L, ya + 8, "currentColor", 1.2, "4 4", .6) + line(x0 + 2 * L + Sx, ya - 8, x0 + 2 * L + Sx, y2 + 14, "currentColor", 1.2, "4 4", .6)
b += arrow("", "o", x0 + L, ya, x0 + 2 * L + Sx, ya, 2.6)
b += text(x0 + L + (L + Sx) / 2, ya - 8, "mũi tàu đi s = L + S", ORG, 15, "middle", "700")
fig3 = wrap("0 0 380 232", "Đoàn tàu dài L qua cầu dài S: mũi tàu đi quãng đường L cộng S",
            b, "Hình 4. Từ lúc mũi tàu lên cầu đến lúc đuôi tàu rời cầu, mũi tàu (chấm cam) đi được L + S.")

# ---------- Hình 2 (biến fig4): đồ thị v–t, diện tích = quãng đường ----------
X0, Y0, kt, kv = 46, 190, 25.0, 13.0
X = lambda t: X0 + kt * t
Y = lambda v: Y0 - kv * v
prof = [(0, 0), (3, 10), (9, 10), (12, 0)]     # (t s, v m/s)
a1, a2, a3 = 0.5 * 3 * 10, 6 * 10, 0.5 * 3 * 10
assert (a1, a2, a3, a1 + a2 + a3, (a1 + a2 + a3) / 12) == (15, 60, 15, 90, 7.5)
b = axes(X0, Y0, 366, 30, "t (s)", "v (m/s)", 40)
b += area([(X(0), Y(0)), (X(3), Y(0)), (X(3), Y(10))], ORG)
b += area([(X(3), Y(0)), (X(3), Y(10)), (X(9), Y(10)), (X(9), Y(0))], GRN)
b += area([(X(9), Y(0)), (X(9), Y(10)), (X(12), Y(0))], BLUE)
for t in (3, 6, 9, 12):
    b += line(X(t), Y0, X(t), Y0 + 5, "currentColor", 1.4) + text(X(t), Y0 + 21, str(t), "currentColor", 14, "middle", "400")
b += text(X0 - 8, Y0 + 5, "0", "currentColor", 14, "end", "400")
for v in (5, 10):
    b += line(X0 - 5, Y(v), X0, Y(v), "currentColor", 1.4) + text(X0 - 9, Y(v) + 5, str(v), "currentColor", 14, "end", "400")
b += line(X(3), Y(10), X(3), Y0, "currentColor", 1.2, "4 4", .6) + line(X(9), Y(10), X(9), Y0, "currentColor", 1.2, "4 4", .6)
b += poly([(X(t), Y(v)) for t, v in prof], "currentColor", 2.8)
b += text(X(1.4), Y(0) - 14, "15 m", ORG, 14, "middle", "700")
b += text(X(6), Y(5), "60 m", GRN, 15, "middle", "700")
b += text(X(10.0), Y(0) - 14, "15 m", BLUE, 14, "middle", "700")
fig4 = wrap("0 0 380 236", "Đồ thị vận tốc thời gian hình thang, ba phần diện tích 15 mét, 60 mét và 15 mét",
            b, "Hình 2. Đồ thị v–t gồm ba giai đoạn: tăng đều, giữ 10 m/s, giảm đều. Mỗi phần diện tích là quãng đường đi trong giai đoạn đó.")

src = open(os.path.join(HERE, "theory.src.html"), encoding="utf8").read()
for n, f in ((1, fig1), (3, fig2), (4, fig3), (2, fig4)):
    assert f"<!--FIG{n}-->" in src
    src = src.replace(f"<!--FIG{n}-->", f)
src = src.replace("__PHUT__", str(PHUT))
open(os.path.join(HERE, "theory.html"), "w", encoding="utf8").write(src)
print("ok", len(src))
