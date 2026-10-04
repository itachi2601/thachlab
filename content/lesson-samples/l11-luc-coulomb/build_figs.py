"""Sinh 4 hình SVG và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được).
Chạy từ thư mục này: python3 build_figs.py"""
import math
from svg_lib import *

def dot(x, y, r=5, c="currentColor"): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'
def charge(x, y, sign, r=14):
    fill = "rgba(248,113,113,.18)" if sign == "+" else "rgba(56,189,248,.18)"
    s = "+" if sign == "+" else "−"
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="currentColor" stroke-width="2"/>'
            + text(x, y + 6, s, "currentColor", 18, "middle", "700"))
def sub(base, s):  # chữ có chỉ số dưới, không dùng KaTeX trong SVG
    return f'{base}<tspan baseline-shift="sub" font-size="9">{s}</tspan>'

# ---- Hình 1: cùng dấu đẩy, trái dấu hút; hai lực bằng nhau, ngược chiều
b = defs("f1")
b += text(12, 22, "Cùng dấu: đẩy nhau", "currentColor", 13, "start", "700")
y = 55
b += line(150, y, 290, y, "currentColor", 1.2, "3 3", .5)
b += arrow("f1", "r", 136, y, 86, y) + arrow("f1", "b", 304, y, 354, y)
b += charge(150, y, "+") + charge(290, y, "+")
b += text(111, y - 16, sub("F", "21"), RED, 13, "middle", "700") + text(329, y - 16, sub("F", "12"), BLUE, 13, "middle", "700")
b += text(150, y + 32, sub("q", "1"), "currentColor", 13, "middle") + text(290, y + 32, sub("q", "2"), "currentColor", 13, "middle")
b += text(12, 117, "Trái dấu: hút nhau", "currentColor", 13, "start", "700")
y = 150
b += line(150, y, 290, y, "currentColor", 1.2, "3 3", .5)
b += arrow("f1", "r", 164, y, 214, y) + arrow("f1", "b", 276, y, 226, y)
b += charge(150, y, "+") + charge(290, y, "-")
b += text(186, y - 16, sub("F", "21"), RED, 13, "middle", "700") + text(254, y - 16, sub("F", "12"), BLUE, 13, "middle", "700")
b += text(150, y + 32, sub("q", "1"), "currentColor", 13, "middle") + text(290, y + 32, sub("q", "2"), "currentColor", 13, "middle")
b += line(150, 196, 290, 196, "currentColor", 1.2) + line(150, 190, 150, 202, "currentColor", 1.2) + line(290, 190, 290, 202, "currentColor", 1.2)
b += text(220, 214, "r", "currentColor", 13, "middle", "700")
fig1 = wrap("0 0 440 222", "Hai điện tích cùng dấu đẩy nhau, trái dấu hút nhau; hai lực cùng độ lớn, ngược chiều, nằm trên đường nối",
            b, "Hình 1. F<sub>12</sub>: lực q<sub>1</sub> tác dụng lên q<sub>2</sub>; F<sub>21</sub>: lực q<sub>2</sub> tác dụng lên q<sub>1</sub>. Hai lực dài bằng nhau, ngược chiều, nằm trên đường nối hai điện tích.")

# ---- Hình 2: tổng hợp hai lực vuông góc tại C (thang 40 px/cm, lực 10 px/mN)
C, A, B = (300, 100), (180, 100), (300, 260)
F1, F2 = 9.0, 6.75
t1 = (C[0] - F1 * 10, C[1])          # hút về A (sang trái)
t2 = (C[0], C[1] - F2 * 10)          # đẩy ra xa B (lên trên)
tr = (t1[0], t2[1])
b = defs("f2")
b += line(*A, *C, "currentColor", 1.2, "3 3", .5) + line(*C, *B, "currentColor", 1.2, "3 3", .5)
b += line(*t1, *tr, "currentColor", 1.2, "5 4", .6) + line(*t2, *tr, "currentColor", 1.2, "5 4", .6)
b += f'<polyline fill="none" stroke="currentColor" stroke-width="1.2" points="288,100 288,112 300,112"/>'
b += arrow("f2", "r", *C, *t1) + arrow("f2", "b", *C, *t2) + arrow("f2", "g", *C, *tr)
b += charge(*A, "-", 13) + charge(*B, "+", 13) + dot(*C, 6, ORG)
b += text(255, 87, sub("F", "1"), RED, 13, "middle", "700") + text(310, 64, sub("F", "2"), BLUE, 13, "start", "700")
b += text(204, 26, "F", GRN, 14, "end", "700")
b += text(180, 132, "A (âm)", "currentColor", 12, "middle") + text(240, 122, "3 cm", "currentColor", 11, "middle", "400")
b += text(320, 265, "B (dương)", "currentColor", 12, "start") + text(310, 185, "4 cm", "currentColor", 11, "start", "400")
b += text(318, 105, "C: q₀ > 0", ORG, 12, "start", "700")
fig2 = wrap("0 0 440 285", "Điện tích dương tại C bị A âm hút sang trái, bị B dương đẩy lên trên; hợp lực là đường chéo hình chữ nhật",
            b, "Hình 2. q₀ &gt; 0 tại C: A (âm) <strong>hút</strong> q₀ về phía A, B (dương) <strong>đẩy</strong> q₀ ra xa B. Hai lực vuông góc, hợp lực F theo quy tắc hình bình hành.")

# ---- Hình 3: vị trí cân bằng của q0 (giả sử q0 > 0)
b = defs("f3")
b += text(12, 18, "Cùng dấu → C ở giữa, gần điện tích nhỏ", "currentColor", 12, "start", "700")
y = 60
b += line(60, y, 360, y, "currentColor", 1.2, "3 3", .5)
b += arrow("f3", "r", 260, y, 305, y) + arrow("f3", "b", 260, y, 215, y)
b += charge(60, y, "+") + charge(360, y, "+") + dot(260, y, 6, ORG)
b += text(60, y - 20, sub("q", "1") + " = +4q", "currentColor", 12, "middle", "700") + text(360, y - 20, sub("q", "2") + " = +q", "currentColor", 12, "middle", "700")
b += text(290, y - 14, sub("F", "1"), RED, 12, "middle", "700") + text(230, y - 14, sub("F", "2"), BLUE, 12, "middle", "700")
b += text(260, y + 24, "C", ORG, 12, "middle", "700")
b += line(60, 96, 258, 96, "currentColor", 1.2) + line(262, 96, 360, 96, "currentColor", 1.2)
b += text(160, 112, sub("r", "1") + " = 2" + sub("r", "2"), "currentColor", 12, "middle") + text(310, 112, sub("r", "2"), "currentColor", 12, "middle")
b += text(12, 140, "Trái dấu → C ở ngoài, gần điện tích nhỏ", "currentColor", 12, "start", "700")
y = 180
b += line(80, y, 380, y, "currentColor", 1.2, "3 3", .5)
b += arrow("f3", "r", 80, y, 35, y) + arrow("f3", "b", 80, y, 125, y)
b += charge(180, y, "+") + charge(380, y, "-") + dot(80, y, 6, ORG)
b += text(180, y - 20, sub("q", "1") + " = +q", "currentColor", 12, "middle", "700") + text(372, y - 20, sub("q", "2") + " = −9q", "currentColor", 12, "middle", "700")
b += text(55, y - 17, sub("F", "1"), RED, 12, "middle", "700") + text(105, y - 17, sub("F", "2"), BLUE, 12, "middle", "700")
b += text(80, y + 24, "C", ORG, 12, "middle", "700")
b += line(80, 214, 180, 214, "currentColor", 1.2) + text(130, 208, sub("r", "1"), "currentColor", 12, "middle")
b += line(80, 236, 380, 236, "currentColor", 1.2) + text(230, 230, sub("r", "2") + " = 3" + sub("r", "1"), "currentColor", 12, "middle")
fig3 = wrap("0 0 440 246", "Vị trí cân bằng: hai điện tích cùng dấu thì C ở giữa, trái dấu thì C ở ngoài đoạn, đều gần điện tích nhỏ hơn",
            b, "Hình 3. F<sub>1</sub> (đỏ) do q<sub>1</sub>, F<sub>2</sub> (xanh) do q<sub>2</sub> gây ra cho q₀ &gt; 0 tại C: cùng phương, ngược chiều, bằng nhau. Tỉ số khoảng cách bằng căn tỉ số độ lớn điện tích.")

# ---- Hình 4: hai quả cầu treo, mỗi dây lệch 45°
O = (220, 24); L = 150; a = math.radians(45)
S1 = (O[0] - L * math.sin(a), O[1] + L * math.cos(a)); S2 = (O[0] + L * math.sin(a), O[1] + L * math.cos(a))
P = 70; T = P / math.cos(a)
b = defs("f4")
b += line(170, 24, 270, 24, "currentColor", 3)
for x in range(175, 270, 12): b += line(x, 24, x - 8, 14, "currentColor", 1.2, "", .6)
b += line(*O, *S1, "currentColor", 1.6) + line(*O, *S2, "currentColor", 1.6)
b += line(220, 24, 220, 118, "currentColor", 1.2, "4 4", .5)
b += f'<path d="M220,54 A30,30 0 0 0 {220+30*math.sin(a):.1f},{24+30*math.cos(a):.1f}" fill="none" stroke="currentColor" stroke-width="1.2"/>'
b += text(226, 74, "45°", "currentColor", 11, "start", "700")
b += line(*S2, S2[0] + P, S2[1] + P, "currentColor", 1.2, "4 3", .55)
b += arrow("f4", "o", *S2, S2[0], S2[1] + P) + arrow("f4", "r", *S2, S2[0] + P, S2[1])
b += arrow("f4", "g", *S2, S2[0] - T * math.sin(a), S2[1] - T * math.cos(a))
b += arrow("f4", "r", *S1, S1[0] - P, S1[1])
b += f'<circle cx="{S1[0]:.1f}" cy="{S1[1]:.1f}" r="9" fill="rgba(248,113,113,.25)" stroke="currentColor" stroke-width="2"/>'
b += f'<circle cx="{S2[0]:.1f}" cy="{S2[1]:.1f}" r="9" fill="rgba(248,113,113,.25)" stroke="currentColor" stroke-width="2"/>'
b += text(S2[0] + 10, S2[1] + P + 4, "P", ORG, 13, "start", "700")
b += text(S2[0] + P, S2[1] - 10, "F", RED, 13, "middle", "700") + text(S1[0] - P + 8, S1[1] - 10, "F", RED, 13, "middle", "700")
b += text(290, 116, "T", GRN, 13, "middle", "700")
b += text(S2[0] + P + 4, S2[1] + P + 14, "F + P", "currentColor", 11, "end", "400")
b += line(S1[0] + 9, S1[1], S2[0] - 9, S2[1], "currentColor", 1.2, "2 3", .6)
b += text(220, 152, "r = 6 cm", "currentColor", 12, "middle")
fig4 = wrap("0 0 440 222", "Hai quả cầu tích điện cùng dấu treo cùng một điểm, đẩy nhau, mỗi dây lệch 45 độ; quả bên phải chịu P, F, T",
            b, "Hình 4. Quả bên phải chịu trọng lực P (cam), lực điện F (đỏ, đẩy ra xa) và lực căng T (lục, dọc dây). Hợp lực F + P (đứt nét) nằm dọc dây, ngược chiều T.")
fig4 = fig4.replace('<figure class="fig" data-tl="1">', '<figure class="fig" data-tl="1" data-exp="tn-l11-coulomb-03">', 1)

h = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(h)
print("ok", len(h))
