"""Sinh 3 hình SVG, thay <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được).
Chạy: python3 content/hsg9/cd05-cong-suat-dien-joule-lenz/build_figs.py
Số liệu hình và mọi số trong bài tính lại bằng assert trước khi ghi."""
import os, sys, math
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "soan-bai-ly-thuyet-tuong-tac", "scripts"))
from svg_lib import RED, BLUE, ORG, GRN, text, wrap, chevron, arrow

PHUT = 12

import re as _re
def rich(s, size=13):
    """`P_{hp}` hoặc `P_R` → chỉ số dưới (tspan hạ dòng rồi trả lại)."""
    out, pos = "", 0
    ms = list(_re.finditer(r"_\{([^}]+)\}|_([A-Za-z0-9]+)", s))
    for k, m in enumerate(ms):
        out += s[pos:m.start()] if k == 0 else ""
        out += f'<tspan dy="4" font-size="{size - 3}">{m.group(1) or m.group(2)}</tspan>'
        nxt = ms[k + 1].start() if k + 1 < len(ms) else len(s)
        rest = s[m.end():nxt]
        if rest:
            out += f'<tspan dy="-4">{rest}</tspan>'
        pos = m.end()
    return out if ms else s

_text = text
def text(x, y, s, c="currentColor", size=13, anchor="start", weight="600"):
    return _text(x, y, rich(s, size), c, size, anchor, weight)
   # điền theo lint_do_dai.py (làm tròn lên)

# ═════════ TỰ KIỂM SỐ LIỆU (độc lập với chữ trong bài) ═════════
def kiem_so():
    # I. hai đèn 220V nối tiếp
    R1, R2 = Fr(220**2, 40), Fr(220**2, 100); assert (R1, R2) == (1210, 484)
    I = Fr(220) / (R1 + R2); assert abs(float(I) - 0.1299) < 1e-4
    assert abs(float(I * I * R1) - 20.4) < .05 and abs(float(I * I * R2) - 8.2) < .05
    # II. định mức / thực tế
    assert Fr(220**2, 1000) == Fr(242, 5) and abs(200**2 / 48.4 - 826.4) < .1 and Fr(100) / 4 == 25
    for U, i, P, R in ((3, .26, .78, 11.5), (6, .36, 2.16, 16.7), (9, .44, 3.96, 20.5), (12, .50, 6.00, 24.0)):
        assert abs(U * i - P) < 1e-9 and abs(round(U / i, 1) - R) < 1e-9
    assert 6**2 / 24 == 1.5
    # III. bài toán mẫu + quiz + tự làm
    Q = 3 * 4200 * 80; assert Q == 1008000
    A = Fr(Q) / Fr(8, 10); assert A == 1260000 and A / 1000 == 1260 and A / 3600000 == Fr(7, 20) and Fr(7, 20) * 2000 == 700
    assert (3 * 100 + 1 * 20) / 4 == 80
    assert Fr(Q) / Fr(6, 10) == 1680000 and 1680000 / 1000 / 60 == 28 and round(1008 * .6) == 605 and 1008 / 60 == 16.8
    Q1 = 1 * 4200 * 80; assert abs(Q1 / .7 - 480000) < 1e-6 and abs(480000 / 800 - 600) < 1e-9 and Q1 / 800 == 420 and abs(420 * .7 - 294) < 1e-9   # 4'54"
    # III mở rộng: hai lần đun
    P = 1000; t1, t2 = 1260, 540
    loss1, loss2 = P * t1 - 3 * 4200 * 80, P * t2 - 1 * 4200 * 80
    k = Fr(loss1 - loss2, t1 - t2); X = loss1 - k * t1
    assert (loss1, loss2) == (252000, 204000) and abs(float(k) - 66.67) < .01 and X == 168000 and X / 80 == 2100
    assert abs(336000 / 540000 - 0.6222) < 1e-4
    # IV. đèn 6V-3W và 6V-6W nối tiếp 9 V
    r1, r2 = Fr(36, 3), Fr(36, 6); i = Fr(9) / (r1 + r2)
    assert (r1, r2, i) == (12, 6, Fr(1, 2)) and i * r1 == 6 and i * r2 == 3 and i * i * r1 == 3 and i * i * r2 == Fr(3, 2) and Fr(6, 6) == 1
    assert min(Fr(3, 6), Fr(6, 6)) * (r1 + r2) == 9
    # V. cực đại trên biến trở
    PR = lambda R, U=12, R0=4: Fr(U * U * R, (R + R0) ** 2)
    assert PR(4) == 9 and PR(2) == PR(8) == 8 and PR(1) == Fr(144, 25) and PR(3) == Fr(432, 49) and PR(6) == Fr(216, 25) and PR(12) == Fr(27, 4)
    assert 12 / 8 == 1.5 and 12 * 1.5 == 18
    assert [R for R in range(1, 100) if PR(R) == 8] == [2, 8] and 2 * 8 == 4 * 4
    assert PR(6) * 100 == 864   # 8,64 W
    # V mở rộng (G1)
    U, R1_, R2_ = 18, 6, 12; Rr = Fr(R1_ * R2_, R1_ + R2_); assert Rr == 4
    rp = Fr(R2_ * 4, R2_ + 4); rm = R1_ + rp; I_ = Fr(U) / rm; Up = I_ * rp
    assert (rp, rm, I_, Up) == (3, 9, 2, 6) and Up**2 / 4 == 9 and I_**2 * R1_ == 24 and Up**2 / R2_ == 3 and U * I_ == 36 and Fr(9, 36) == Fr(1, 4)
    PRr = lambda R: Fr(U**2 * R2_**2 * R, (R1_ * R2_ + R1_ * R + R2_ * R) ** 2); assert PRr(2) == PRr(8) == 8 and PRr(4) == 9
    # VI. truyền tải
    for U_, Ihp in ((10000, 1000), (2000, 25000)):
        i_ = Fr(100000, U_); assert i_ ** 2 * 10 == Ihp
    assert Fr(100000, 10000) == 10 and Fr(100000, 2000) == 50 and Fr(1000, 100000) == Fr(1, 100) and Fr(25000, 100000) == Fr(1, 4)
    assert Fr(100000, 20000) ** 2 * 10 == 250
    # VII. aptomat, dây
    assert abs(2500 / 220 - 11.36) < .01 and 5 * 2 == 10 and 5 * 2.5 == 12.5 and abs(11.36 / 5 - 2.27) < .01
    print("kiểm số liệu: đạt")

kiem_so()

# ═════════ tiện ích hình ═════════
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'

def poly(pts, c="currentColor", w=2.6):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polyline points="{p}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"/>'

def circ(x, y, r, c="currentColor", w=2, fill="none"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{w}"/>'

def lamp(x, y, c, r=13):
    d = r * 0.7071
    return circ(x, y, r, c, 2.4) + line(x - d, y - d, x + d, y + d, c, 2) + line(x - d, y + d, x + d, y - d, c, 2)

def battery(x, y, h=26):
    """pin đặt trên dây dọc tại x; cực dương (vạch dài) ở trên."""
    return (line(x, y - h / 2 - 8, x, y - 6, "currentColor", 2) + line(x - 12, y - 6, x + 12, y - 6, "currentColor", 2.4)
            + line(x - 7, y + 2, x + 7, y + 2, "currentColor", 4) + line(x, y + 2, x, y + h / 2 + 8, "currentColor", 2))

def box(x, y, w, h, c="currentColor", fill="none"):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="5" fill="{fill}" stroke="{c}" stroke-width="2.2"/>'

def resistor(x, y, w=44, h=14, c="currentColor"):
    return box(x - w / 2, y - h / 2, w, h, c)

# ═════════ Hình 1: nối tiếp / song song ═════════
b = text(100, 14, "Nối tiếp", "currentColor", 15, "middle", "700") + text(290, 14, "Song song", "currentColor", 15, "middle", "700")
# nối tiếp
xl, xr, yt, yb = 24, 176, 54, 150
b += poly([(xl, 90), (xl, yt), (xl + 36, yt)], "currentColor", 2) + poly([(xl + 38, yt), (xr, yt), (xr, yb), (xl, yb), (xl, 108)], "currentColor", 2)
b += line(xl, 90, xl, 98, "currentColor", 2)
b += battery(xl, 100, 20)
b += line(70, yt, 78, yt, "currentColor", 2)
b += lamp(64, yt, RED) + lamp(134, yt, BLUE)
b += text(64, yt - 20, "Đ₁ 40 W", RED, 13, "middle", "700") + text(134, yt - 20, "Đ₂ 100 W", BLUE, 13, "middle", "700")
b += arrow("", "o", 90, yb, 120, yb, 2.4) + text(105, yb - 10, "I", ORG, 14, "middle", "700")
b += text(100, 186, "Cùng dòng I", "currentColor", 13, "middle", "600")
# song song
xl2, xr2 = 214, 366
b += poly([(xl2, 90), (xl2, yt), (xr2, yt), (xr2, yb), (xl2, yb), (xl2, 108)], "currentColor", 2)
b += battery(xl2, 100, 20)
x1, x2 = 276, 332
for xx, c, lab in ((x1, RED, "Đ₁ 40 W"), (x2, BLUE, "Đ₂ 100 W")):
    b += line(xx, yt, xx, 90 - 13, "currentColor", 2) + line(xx, 90 + 13, xx, yb, "currentColor", 2) + lamp(xx, 90, c)
b += text(x1, 124, "Đ₁", RED, 13, "middle", "700") + text(x1, 140, "40 W", RED, 13, "middle", "700")
b += text(x2, 124, "Đ₂", BLUE, 13, "middle", "700") + text(x2, 140, "100 W", BLUE, 13, "middle", "700")
b += text(290, 186, "Cùng hiệu điện thế U", "currentColor", 13, "middle", "600")
fig1 = wrap("0 0 390 200", "Hai bóng đèn mắc nối tiếp có chung dòng điện, hai bóng mắc song song có chung hiệu điện thế",
            b, "Hình 1. Nối tiếp: dòng I chạy qua cả hai bóng. Song song: hai bóng cùng nối vào hai cực của nguồn.")

# ═════════ Hình 2: đồ thị P_R theo R ═════════
U, R0 = 12, 4
PRf = lambda R: U * U * R / (R + R0) ** 2
X0, Y0, kx, ky = 46, 200, 20.0, 17.0     # px/Ω, px/W
X = lambda r: X0 + kx * r
Y = lambda p: Y0 - ky * p
b = line(X0, Y0, 366, Y0, "currentColor", 1.8) + chevron(366, Y0, 1, 0, "currentColor", 1.8, 9)
b += line(X0, Y0, X0, 24, "currentColor", 1.8) + chevron(X0, 24, 0, -1, "currentColor", 1.8, 9)
b += text(366, Y0 - 10, "R (Ω)", "currentColor", 14, "end", "600") + text(X0 + 8, 30, "P_R (W)", "currentColor", 14, "start", "600")
for r in (2, 4, 8, 12, 16):
    b += line(X(r), Y0, X(r), Y0 + 5, "currentColor", 1.4) + text(X(r), Y0 + 21, str(r), "currentColor", 13, "middle", "400")
for p in (4, 8, 9):
    b += line(X0 - 5, Y(p), X0, Y(p), "currentColor", 1.4) + text(X0 - 9, Y(p) + 5, str(p), "currentColor", 13, "end", "400")
b += text(X0 - 8, Y0 + 5, "0", "currentColor", 13, "end", "400")
b += line(X0, Y(8), X(8), Y(8), "currentColor", 1.2, "4 4", .6)
b += line(X(2), Y(8), X(2), Y0, "currentColor", 1.2, "4 4", .6) + line(X(8), Y(8), X(8), Y0, "currentColor", 1.2, "4 4", .6)
b += line(X(4), Y(9), X(4), Y0, ORG, 1.4, "4 4", .9)
pts = [(X(r), Y(PRf(r))) for r in [i / 4 for i in range(2, 65)]]
b += poly(pts, GRN, 3)
for r, c in ((2, RED), (8, RED), (4, ORG)):
    b += circ(X(r), Y(PRf(r)), 5, c, 2, c)
b += text(X(4) + 8, Y(9) - 8, "P_{max} = 9 W", ORG, 14, "start", "700")
b += text(X(2) - 4, Y(8) - 10, "2", RED, 13, "end", "700") + text(X(8) + 8, Y(8) - 10, "8", RED, 13, "start", "700")
b += text(X(11), Y(8) - 14, "cùng 8 W", RED, 13, "middle", "700")
fig2 = wrap("0 0 380 236", "Đồ thị công suất trên biến trở theo R: đỉnh 9 W tại R bằng 4 ôm, hai điểm R bằng 2 và 8 ôm cùng 8 W",
            b, "Hình 2. U = 12 V, R₀ = 4 Ω. Đỉnh tại R = R₀ = 4 Ω; hai giá trị R = 2 Ω và 8 Ω (tích bằng R₀²) cho cùng 8 W.")

# ═════════ Hình 3: truyền tải điện ═════════
b = box(14, 62, 84, 74, "currentColor") + text(56, 92, "Trạm phát", "currentColor", 14, "middle", "700") + text(56, 112, "P, U", "currentColor", 14, "middle", "600")
b += box(282, 62, 84, 74, "currentColor") + text(324, 92, "Nơi dùng", "currentColor", 14, "middle", "700") + text(324, 112, "P − P_hp", "currentColor", 13, "middle", "600")
ya, yb2 = 78, 120
b += line(98, ya, 150, ya) + resistor(172, ya) + line(194, ya, 282, ya)
b += line(98, yb2, 150, yb2) + resistor(172, yb2) + line(194, yb2, 282, yb2)
b += text(172, ya - 14, "R/2", ORG, 13, "middle", "700") + text(172, yb2 + 28, "R/2", ORG, 13, "middle", "700")
b += arrow("", "b", 214, ya - 14, 262, ya - 14, 2.4) + text(238, ya - 22, "I = P/U", BLUE, 13, "middle", "700")
b += text(190, 168, "P_hp = I²R = P²R/U²", ORG, 15, "middle", "700")
b += text(190, 190, "R: điện trở cả hai dây", "currentColor", 13, "middle", "400")
fig3 = wrap("0 44 380 156", "Sơ đồ truyền tải điện: trạm phát nối với nơi dùng bằng hai dây có điện trở tổng cộng R, hao phí bằng I bình phương nhân R",
            b, "Hình 3. Hao phí nằm ở dây dẫn: P_hp = I²R. Tăng U thì I = P/U giảm, hao phí giảm theo bình phương.")

# ═════════ ghi theory.html ═════════
src = open(os.path.join(HERE, "theory.src.html"), encoding="utf8").read()
for n, f in ((1, fig1), (2, fig2), (3, fig3)):
    assert f"<!--FIG{n}-->" in src
    src = src.replace(f"<!--FIG{n}-->", f)
src = src.replace("__PHUT__", str(PHUT))
open(os.path.join(HERE, "theory.html"), "w", encoding="utf8").write(src)
print("ok", len(src))
