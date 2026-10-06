"""Sinh 3 hình SVG và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được)."""
from svg_lib import *

def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'

def dot(x, y, r=5, c="currentColor"): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'

def sub(main, s, rest=""):
    return f'{main}<tspan baseline-shift="sub" font-size="9">{s}</tspan>{rest}'

# ---- Hình 1: chim đậu trên dây 500 kV, cột nối đất
b = defs("f1")
WY = 90
b += line(12, WY, 370, WY, "currentColor", 3)                        # dây
b += line(390, 40, 390, 205, "currentColor", 5)                       # cột
b += line(355, 40, 425, 40, "currentColor", 4)                        # xà
for y in (50, 62, 74):                                                 # chuỗi sứ cách điện
    b += f'<ellipse cx="370" cy="{y}" rx="9" ry="4" fill="none" stroke="{BLUE}" stroke-width="2"/>'
b += line(370, 40, 370, WY, BLUE, 1.5)
b += line(300, 205, 432, 205, "currentColor", 2)                      # mặt đất
for x in range(306, 432, 14): b += line(x, 205, x - 8, 214, "currentColor", 1.2, "", .6)
# chim
b += f'<ellipse cx="150" cy="66" rx="22" ry="12" fill="rgba(148,163,184,.3)" stroke="currentColor" stroke-width="2"/>'
b += f'<circle cx="172" cy="52" r="8" fill="rgba(148,163,184,.3)" stroke="currentColor" stroke-width="2"/>'
b += '<path d="M179,50 L188,53 L179,56 z" fill="currentColor"/>'
b += line(128, 64, 112, 58, "currentColor", 2)
b += line(142, 77, 138, WY, "currentColor", 2) + line(158, 77, 162, WY, "currentColor", 2)
b += dot(138, WY, 4, RED) + dot(162, WY, 4, RED)
b += text(128, 108, "A", RED, 13, "middle", "700") + text(172, 108, "B", RED, 13, "middle", "700")
b += text(380, 180, "dây – cột: cỡ hàng trăm kV", RED, 13, "end", "700")
b += text(410, 225, "cột nối đất: V = 0", "currentColor", 13, "end", "400")
b += text(14, 78, "dây 500 kV", "currentColor", 13, "start", "400")
fig1 = wrap("0 0 440 232", "Chim đậu trên dây 500 kV: hai chân cùng điện thế nên hiệu điện thế gần bằng 0; giữa dây và cột nối đất hiệu điện thế khoảng 500 kV",
            b, "Hình 1. Hai chân chim cùng trên một dây: hiệu điện thế giữa A và B gần bằng 0. Nguy hiểm là chạm cùng lúc dây và cột (V = 0).")
fig1 = fig1.replace('<figure class="fig" data-tl="1">', '<figure class="fig" data-tl="1" data-exp="tn-l11-dien-the-03">')

# ---- Hình 2: điện trường đều giữa hai bản, M, N, hai đường đi, hình chiếu d
XP, XN = 45, 395          # bản dương (trái), bản âm (phải)
b = defs("f2")
b += f'<rect x="{XP-5}" y="20" width="10" height="180" fill="rgba(248,113,113,.25)" stroke="currentColor" stroke-width="2"/>'
b += f'<rect x="{XN-5}" y="20" width="10" height="180" fill="rgba(56,189,248,.25)" stroke="currentColor" stroke-width="2"/>'
for y in (40, 85, 130, 175):
    b += text(XP - 18, y + 5, "+", RED, 16, "middle", "700") + text(XN + 18, y + 5, "−", BLUE, 16, "middle", "700")
for y in (40, 195):
    b += arrow("f2", "r", XP + 12, y, XN - 12, y, 2.5)
b += text(220, 32, "E", RED, 14, "middle", "700")
volts = {XP: "12 V", 132.5: "9 V", 220: "6 V", 307.5: "3 V", XN: "0 V"}
for x, lab in volts.items():
    if x not in (XP, XN):
        b += line(x, 52, x, 183, BLUE, 1.5, "5 4", .8)
    b += text(x, 218, lab, BLUE, 13, "middle", "700")
MX, MY, NX, NY = 110, 80, 280, 160
b += line(MX, MY, NX, NY, "currentColor", 2)
b += f'<path d="M{MX},{MY} Q250,48 {NX},{NY}" fill="none" stroke="{ORG}" stroke-width="2" stroke-dasharray="6 4"/>'
b += dot(MX, MY, 5) + dot(NX, NY, 5)
b += text(MX - 10, MY - 6, "M", "currentColor", 14, "end", "700") + text(NX + 10, NY + 4, "N", "currentColor", 14, "start", "700")
b += line(MX, MY + 6, MX, 238, "currentColor", 1, "3 3", .6) + line(NX, NY + 6, NX, 238, "currentColor", 1, "3 3", .6)
mid = (MX + NX) / 2
b += arrow("f2", "g", mid, 235, MX + 2, 235, 2) + arrow("f2", "g", mid, 235, NX - 2, 235, 2)
b += text(mid, 229, "d", GRN, 14, "middle", "700")
b += text(14, 254, "điện thế cao", "currentColor", 13, "start", "400") + text(426, 254, "điện thế thấp", "currentColor", 13, "end", "400")
fig2 = wrap("0 0 440 260", "Điện trường đều giữa hai bản: điện thế giảm từ 12 V ở bản dương xuống 0 V ở bản âm; công từ M đến N không phụ thuộc đường đi, chỉ phụ thuộc hình chiếu d",
            b, "Hình 2. Đường liền và đường cong cam cho cùng một công. Chỉ hình chiếu <strong>d</strong> của MN lên đường sức là đáng kể. Nét đứt xanh: đường đẳng thế.")

# ---- Hình 3: đồ thị V theo x của thí nghiệm đo (d = 10 cm, U = 6 V)
OX, OY, SX, SV = 60, 210, 34, 30          # gốc, px/cm, px/V
U, D = 6.0, 10.0
data = [(2, 1.18), (4, 2.43), (6, 3.57), (8, 4.84)]
px = lambda x: OX + SX * x
py = lambda v: OY - SV * v
b = defs("f3")
b += line(OX, OY, 425, OY, "currentColor", 1.8) + '<path d="M432,210 L422,205 L422,215 z" fill="currentColor"/>'
b += line(OX, OY, OX, 14, "currentColor", 1.8) + '<path d="M60,7 L55,17 L65,17 z" fill="currentColor"/>'

for x in range(0, 11, 2):
    b += line(px(x), OY, px(x), OY + 5, "currentColor", 1.5) + text(px(x), OY + 18, str(x), "currentColor", 13, "middle", "400")
for v in (2, 4, 6):
    b += line(OX - 5, py(v), OX, py(v), "currentColor", 1.5) + text(OX - 8, py(v) + 4, str(v), "currentColor", 13, "end", "400")
    b += line(OX, py(v), px(10), py(v), "currentColor", 1, "2 4", .3)
b += line(px(0), py(0), px(D), py(U), GRN, 2.5)
for x, v in data:
    assert abs(py(v) - py(U * x / D)) < 2, (x, v)          # chấm nằm sát đường lí thuyết
    b += dot(px(x), py(v), 5, RED)
b += text(425, 244, "x (cm) — cách lá âm", "currentColor", 13, "end", "400")
b += text(68, 18, "V (V)", "currentColor", 13, "start", "700")
b += text(120, 70, "lí thuyết: V = U·x/d", GRN, 13, "start", "700")
b += text(250, 196, "● số đo", RED, 13, "start", "700")
fig3 = wrap("0 0 440 248", "Đồ thị điện thế V theo khoảng cách x từ lá âm: bốn điểm đo nằm sát đường thẳng V = 0,6x",
            b, "Hình 3. Bốn số đo (đỏ) nằm sát đường thẳng: V tăng đều theo x, nghĩa là điện trường giữa hai lá gần như đều.")

h = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(h)
print("ok", len(h))
