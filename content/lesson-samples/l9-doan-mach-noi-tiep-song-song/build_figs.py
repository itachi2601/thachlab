"""Bài 12. Đoạn mạch nối tiếp, song song (KHTN 9, lesson_id 90).
Sinh 4 hình SVG + bảng số liệu thí nghiệm + 3 file content/thi-nghiem/tn-l9-doanmach-0N.json,
thay mốc <!--FIGn--> / __...__ trong theory.src.html -> theory.html.
Mọi số liệu tính từ mô hình (assert). Chạy: cd <thư mục bài> && python3 build_figs.py
"""
import json, math, pathlib
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PHUT = 15          # số phút đọc: lấy từ lint_do_dai.py, làm tròn lên

def vn(x, nd=1):
    return f"{x:.{nd}f}".replace(".", "{,}")
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'
def poly(pts, c="currentColor", w=2.4):
    return pts_path(pts, c, w)
def T(x, y, s, c="currentColor", size=17, anchor="start", weight="700"):
    return text(x, y, s, c, size, anchor, weight)
def it_(s):
    """Ký hiệu đại lượng trong SVG: chữ nghiêng có chân."""
    return f'<tspan font-family="Georgia, \'Times New Roman\', serif" font-style="italic">{s}</tspan>'
def sb(base, idx, size=17, italic=True):
    """Ký hiệu có chỉ số dưới bằng tspan dy (không dùng ký tự Unicode ₁₂)."""
    b = it_(base) if italic else base
    return f'{b}<tspan dy="5" font-size="{size - 4}">{idx}</tspan><tspan dy="-5"> </tspan>'
def dot(x, y, c="currentColor", r=4):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'
def cur(x, y, dx, dy):
    """Đầu V chỉ chiều dòng điện quy ước trên dây."""
    return chevron(x, y, dx, dy, RED, 2.6, 12)
def res_h(cx, cy, w=50, h=22):
    return f'<rect x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" width="{w}" height="{h}" fill="rgba(251,146,60,.2)" stroke="currentColor" stroke-width="2.4"/>'
def meter(cx, cy, letter, idx=None, r=19):
    g = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="currentColor" stroke-width="2.4"/>'
    if idx is None:
        g += T(cx, cy + 7, letter, "currentColor", 19, "middle")
    else:
        g += (f'<text x="{cx - 3}" y="{cy + 6}" fill="currentColor" font-size="17" font-weight="700" text-anchor="middle">{letter}'
              f'<tspan dy="4" font-size="12">{idx}</tspan></text>')
    return g
def battery_h(px, nx, y):
    """Nguồn trên dây ngang: bản (+) dài tại px, bản (−) ngắn đậm tại nx."""
    return (line(px, y - 18, px, y + 18, "currentColor", 2.4) + line(nx, y - 9, nx, y + 9, "currentColor", 5)
            + T(px - 6, y - 22, "+", "currentColor", 20, "end") + T(nx + 6, y - 22, "−", "currentColor", 20))

# ---------- Hình 1: cảnh mở bài (chỉ vẽ hiện tượng)
def bulb(cx, cy, lit, broken=False):
    fill = "rgba(251,191,36,.65)" if lit else "rgba(120,120,120,.25)"
    g = f'<circle cx="{cx}" cy="{cy}" r="11" fill="{fill}" stroke="currentColor" stroke-width="2"/>'
    g += f'<rect x="{cx - 6}" y="{cy - 20}" width="12" height="9" fill="currentColor"/>'
    if lit:
        for a in (-20, 20, 60, 90, 120, 160, 200):
            r_ = math.radians(a)
            g += line(cx + 15 * math.cos(r_), cy + 15 * math.sin(r_), cx + 24 * math.cos(r_), cy + 24 * math.sin(r_), ORG, 2.4)
    if broken:
        g += line(cx - 7, cy - 7, cx + 7, cy + 7, RED, 2.6) + line(cx - 7, cy + 7, cx + 7, cy - 7, RED, 2.6)
    return g
b = ""
# (a) dây đèn trang trí: phích cắm + dây võng + 4 bóng, bóng thứ 3 hỏng, cả dây tắt
b += f'<rect x="8" y="42" width="16" height="16" rx="3" fill="none" stroke="currentColor" stroke-width="2"/>' + line(4, 46, 8, 46, "currentColor", 2) + line(4, 54, 8, 54, "currentColor", 2)
hooks = [24, 64, 104, 144, 184]
d = f"M24,50"
for x0, x1 in zip(hooks, hooks[1:]):
    d += f" Q{(x0 + x1) / 2},86 {x1},50"
b += f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="2"/>'
for k, x0 in enumerate(hooks[:-1]):
    xm = x0 + 20
    b += bulb(xm, 88, False, broken=(k == 2))
b += T(10, 150, "(a) dây đèn trang trí:", "currentColor", 16) + T(10, 172, "một bóng hỏng,", "currentColor", 16) + T(10, 194, "cả dây tắt", "currentColor", 16)
b += line(212, 16, 212, 200, "currentColor", 1.2, "5 5", .5)
# (b) trong nhà: hai đèn treo trần
b += line(222, 24, 412, 24, "currentColor", 2.4)
for cx, lit, name in ((265, False, "phòng khách"), (365, True, "bếp")):
    b += line(cx, 24, cx, 58, "currentColor", 2) + bulb(cx, 78, lit, broken=not lit) + line(cx, 89, cx, 110, "currentColor", 2)
    b += T(cx, 130, name, "currentColor", 15, "middle", "600")
b += line(222, 110, 412, 110, "currentColor", 2.4)
b += T(222, 150, "(b) trong nhà:", "currentColor", 16) + T(222, 172, "đèn này hỏng,", "currentColor", 16) + T(222, 194, "đèn kia vẫn sáng", "currentColor", 16)
fig1 = wrap("0 0 420 206", "Hai cảnh: dây đèn trang trí có một bóng hỏng thì cả dây tắt; trong nhà đèn phòng khách hỏng, đèn bếp vẫn sáng", b,
            "Hình 1. (a) Dây đèn trang trí kiểu cũ: một bóng hỏng, cả dây tắt.<br>(b) Trong nhà: đèn phòng khách hỏng, đèn bếp vẫn sáng.")

# ---------- Hình 2: đoạn mạch nối tiếp, ampe kế + vôn kế đo U_AB
b = ""
YT, XL, XR, YB = 150, 40, 380, 262
XA, XM, XB = 95, 210, 325
R1C, R2C, RW = 150, 268, 50
AYc = 205
PX, NX = 203, 217
b += poly([(XL, AYc - 19), (XL, YT), (R1C - RW / 2, YT)])
b += res_h(R1C, YT) + poly([(R1C + RW / 2, YT), (R2C - RW / 2, YT)]) + res_h(R2C, YT)
b += poly([(R2C + RW / 2, YT), (XR, YT), (XR, YB), (NX, YB)])
b += poly([(PX, YB), (XL, YB), (XL, AYc + 19)])
b += meter(XL, AYc, "A") + T(XL + 22, AYc + 30, "+", "currentColor", 18) + T(XL + 22, AYc - 16, "−", "currentColor", 18)
b += battery_h(PX, NX, YB)
# vôn kế mắc giữa A và B
VYc = 62
b += poly([(XA, YT), (XA, VYc), (210 - 19, VYc)]) + poly([(210 + 19, VYc), (XB, VYc), (XB, YT)])
b += meter(210, VYc, "V") + T(186, VYc - 10, "+", "currentColor", 18, "end") + T(234, VYc - 10, "−", "currentColor", 18)
for x, nm in ((XA, "A"), (XM, "M"), (XB, "B")):
    b += dot(x, YT) + T(x, YT + 30, nm, "currentColor", 17, "middle")
b += T(R1C, YT - 18, sb("R", "1"), "currentColor", 18, "middle") + T(R2C, YT - 18, sb("R", "2"), "currentColor", 18, "middle")
# chiều dòng điện quy ước: + -> trái -> lên qua ampe kế -> phải qua R1, R2 -> xuống -> trái về −
b += cur(120, YB, -1, 0) + cur(XL, 168, 0, -1) + cur(70, YT, 1, 0) + cur(362, YT, 1, 0) + cur(XR, 210, 0, 1) + cur(300, YB, -1, 0)
b += T(70, YT - 12, it_("I"), RED, 19, "middle") + T(352, YT - 12, it_("I"), RED, 19, "middle")
assert PX < NX and 120 < PX and 300 > NX
assert XA < R1C - RW / 2 and R1C + RW / 2 < XM < R2C - RW / 2 and R2C + RW / 2 < XB
fig2 = wrap("0 0 420 290", "Sơ đồ đoạn mạch nối tiếp: R1 và R2 nối liền nhau tại điểm M giữa A và B; ampe kế nối tiếp; vôn kế mắc giữa A và B; mũi tên đỏ chỉ chiều dòng điện", b,
            "Hình 2. $R_1$ nối tiếp $R_2.$ Vôn kế đang đo $U_{AB}.$<br>Đo $U_1{:}$ chuyển hai dây vôn kế sang $A$ và $M.$<br>Chuyển ampe kế sang giữa $R_1,$ $R_2$ và sau $R_2$ để đo lần lượt.")

# ---------- Hình 3: đoạn mạch song song, ba ampe kế + vôn kế
b = ""
XA3, XB3, YU, YL = 120, 330, 118, 206
YM = (YU + YL) / 2
XL3, XR3, YB3 = 40, 385, 296
AM = 230                     # tâm ampe kế mạch chính (trên dây trái)
A1X, R3X = 170, 268
b += poly([(XA3, YU), (XA3, YL)]) + poly([(XB3, YU), (XB3, YL)])
for y, k in ((YU, "1"), (YL, "2")):
    b += poly([(XA3, y), (A1X - 19, y)]) + meter(A1X, y, "A", k) + poly([(A1X + 19, y), (R3X - 25, y)])
    b += res_h(R3X, y) + poly([(R3X + 25, y), (XB3, y)])
    b += T(A1X - 22, y - 12, "+", "currentColor", 17, "end") + T(A1X + 22, y - 12, "−", "currentColor", 17)
    b += cur(218, y, 1, 0)
b += T(R3X, YU - 20, sb("R", "1"), "currentColor", 18, "middle") + T(R3X, YL + 36, sb("R", "2"), "currentColor", 18, "middle")
b += poly([(XA3, YM), (XL3, YM), (XL3, AM - 19)]) + meter(XL3, AM, "A") + poly([(XL3, AM + 19), (XL3, YB3), (203, YB3)])
b += T(XL3 + 22, AM + 30, "+", "currentColor", 18) + T(XL3 + 22, AM - 16, "−", "currentColor", 18)
b += battery_h(203, 217, YB3) + poly([(217, YB3), (XR3, YB3), (XR3, YM), (XB3, YM)])
VY3 = 46
b += poly([(XA3, YU), (XA3, VY3), (225 - 19, VY3)]) + poly([(225 + 19, VY3), (XB3, VY3), (XB3, YU)])
b += meter(225, VY3, "V") + T(201, VY3 - 8, "+", "currentColor", 18, "end") + T(249, VY3 - 8, "−", "currentColor", 18)
b += dot(XA3, YM) + dot(XB3, YM) + dot(XA3, YU, r=3.5) + dot(XB3, YU, r=3.5)
b += T(XA3 - 8, YM + 26, "A", "currentColor", 18, "end") + T(XB3 + 8, YM + 26, "B", "currentColor", 18)
b += cur(80, YM, 1, 0) + cur(XL3, 270, 0, -1) + cur(XR3, 250, 0, 1) + cur(300, YB3, -1, 0) + cur(120, YB3, -1, 0)
b += T(80, YM - 12, it_("I"), RED, 19, "middle")
assert XA3 < A1X - 19 and A1X + 19 < R3X - 25 and R3X + 25 < XB3 and 120 < 203 and 300 > 217
fig3 = wrap("0 0 420 320", "Sơ đồ đoạn mạch song song: R1 và R2 nối chung hai điểm A và B; ampe kế A1, A2 trong từng nhánh, ampe kế mạch chính, vôn kế giữa A và B", b,
            "Hình 3. $R_1$ song song $R_2.$ Ampe kế $A_1,$ $A_2$ đo dòng từng nhánh.<br>Ampe kế ở dây bên trái đo dòng mạch chính.")

# ---------- Hình 4: mạch hỗn hợp R1 nt (R2 // R3), gộp từng bước
b = ""
def row_label(y, s):
    return T(10, y, s, "currentColor", 16, "start", "700")
# (a)
y, yu, yl = 92, 62, 122
b += row_label(26, "(a) Mạch ban đầu")
b += dot(30, y) + T(30, y + 26, "A", "currentColor", 17, "middle")
b += poly([(30, y), (60, y)]) + res_h(85, y) + poly([(110, y), (160, y)])
b += poly([(160, yu), (160, yl)]) + poly([(300, yu), (300, yl)]) + dot(160, y, r=3.5) + dot(300, y, r=3.5)
for yy in (yu, yl):
    b += poly([(160, yy), (205, yy)]) + res_h(230, yy) + poly([(255, yy), (300, yy)])
b += poly([(300, y), (390, y)]) + dot(390, y) + T(390, y + 26, "B", "currentColor", 17, "middle")
b += T(85, y - 18, sb("R", "1"), "currentColor", 17, "middle")
b += T(230, yu - 18, sb("R", "2"), "currentColor", 17, "middle") + T(230, yl + 32, sb("R", "3"), "currentColor", 17, "middle")
# (b)
y = 224
b += row_label(176, "(b) Gộp cụm song song")
b += dot(30, y) + T(30, y + 26, "A", "currentColor", 17, "middle")
b += poly([(30, y), (60, y)]) + res_h(85, y) + poly([(110, y), (205, y)]) + res_h(230, y) + poly([(255, y), (390, y)])
b += dot(390, y) + T(390, y + 26, "B", "currentColor", 17, "middle")
b += T(85, y - 18, sb("R", "1"), "currentColor", 17, "middle") + T(230, y - 18, sb("R", "23"), BLUE, 17, "middle")
# (c)
y = 318
b += row_label(274, "(c) Gộp nối tiếp")
b += dot(30, y) + T(30, y + 26, "A", "currentColor", 17, "middle")
b += poly([(30, y), (185, y)]) + res_h(210, y) + poly([(235, y), (390, y)])
b += dot(390, y) + T(390, y + 26, "B", "currentColor", 17, "middle")
b += T(260, y - 14, sb("R", "td"), GRN, 17, "start")
fig4 = wrap("0 0 420 352", "Mạch hỗn hợp: R1 nối tiếp với cụm R2 song song R3; gộp cụm song song thành R23, rồi gộp nối tiếp thành một điện trở tương đương", b,
            "Hình 4. (a) $R_1$ nối tiếp cụm ($R_2$ song song $R_3$).<br>(b) Gộp cụm song song thành $R_{23}.$<br>(c) Gộp nối tiếp thành $R_{td}.$")

# ---------- Thí nghiệm 1: đo U trong mạch nối tiếp (số liệu minh hoạ từ mô hình + làm tròn theo độ chia 0,1 V)
R1, R2 = 10.0, 20.0
U_THAT = (3.0, 4.5, 6.07)            # hiệu điện thế thật giữa A, B (nguồn chỉnh "khoảng" 3; 4,5; 6 V)
rows1 = []
for u in U_THAT:
    i = u / (R1 + R2)
    u1, u2 = i * R1, i * R2
    r = (round(u1, 1), round(u2, 1), round(u, 1), round(i, 2))
    for doc, that in ((r[0], u1), (r[1], u2), (r[2], u)):
        assert abs(doc - that) <= 0.05 + 1e-9                   # mỗi số đọc lệch ≤ nửa vạch 0,1 V
    rows1.append(r)
assert [x[3] for x in rows1] == [0.10, 0.15, 0.20]
lech = [round(x[2] - (x[0] + x[1]), 2) for x in rows1]
assert lech == [0.0, 0.0, 0.1], lech                              # chỉ lần 3 lệch, đúng 0,1 V
assert all(abs(x[1] - 2 * x[0]) < 1e-9 for x in rows1)              # U2 gấp đôi U1 ở cả ba lần
assert lech[2] <= 3 * 0.05 + 1e-9                                  # ba số đọc, mỗi số lệch ≤ 0,05 V
bang1 = "\n".join(f"<tr><td>${vn(a)}$</td><td>${vn(b_)}$</td><td>${vn(c)}$</td></tr>" for a, b_, c, _ in rows1)
I_TN1 = "<br>".join(f"Lần {k}: ${vn(x[3], 2)}\\ \\text{{A}}.$" for k, x in enumerate(rows1, 1))
TONG3, UAB3 = vn(rows1[2][0] + rows1[2][1]), vn(rows1[2][2])
FB1 = (f"Vôn kế có độ chia $0{{,}}1\\ \\text{{V}},$ mỗi lần đọc có thể lệch tới $0{{,}}05\\ \\text{{V}}.$ "
       f"Ba số đọc cộng trừ với nhau thì có thể lệch tới $0{{,}}15\\ \\text{{V}},$ nên lệch $0{{,}}1\\ \\text{{V}}$ vẫn trong sai số.")
NX1 = (f"Lần 1 và lần 2: $U_1 + U_2$ đúng bằng $U_{{AB}}.$<br>"
       f"Lần 3: lệch $0{{,}}1\\ \\text{{V}},$ nhỏ hơn sai số tối đa của ba lần đọc $(0{{,}}15\\ \\text{{V}}).$<br>"
       f"Cả ba lần, $U_2$ gấp đôi $U_1,$ đúng bằng ${{R_2 : R_1 = 2}}.$<br>"
       f"Muốn bớt sai số: dùng vôn kế có độ chia nhỏ hơn, đo nhiều lần rồi lấy trung bình.")
assert abs(3.0 / (R1 + R2) - 0.1) < 1e-12                         # ví dụ "khớp lần đo 1"

# ---------- Thí nghiệm 2: song song R1 = 10, R2 = 15, U = 6 V
Ra, Rb, U2_ = 10.0, 15.0, 6.0
I1, I2 = U2_ / Ra, U2_ / Rb
Rp = Ra * Rb / (Ra + Rb)
assert 6 / 10 + 6 / 10 <= 1.5 and abs(I1 - 0.6) < 1e-12 and abs(I2 - 0.4) < 1e-12 and abs(Rp - 6) < 1e-12 and abs(U2_ / Rp - (I1 + I2)) < 1e-12

# ---------- Thí nghiệm 3: hai bóng đèn pin (coi R bóng không đổi, 6 Ω), nguồn 3 V
RBONG, U3 = 6.0, 3.0
I_nt, I_ss = U3 / (2 * RBONG), U3 / RBONG
assert abs(I_nt - 0.25) < 1e-12 and abs(I_ss - 0.5) < 1e-12

# ---------- Kiểm số liệu các quiz / bài toán mẫu
def ss(a, b_): return a * b_ / (a + b_)
assert abs(12 / 6 + 12 / 12 - 3) < 1e-12 and abs(12 / ss(6, 12) - 3) < 1e-12           # Câu 2
assert abs(12 / 18 - 0.667) < 1e-3 and abs(6 / 6 + 6 / 12 - 1.5) < 1e-12               # nhiễu Câu 2
assert abs(2 + ss(6, 6) - 5) < 1e-12 and abs(2 + 6 + 6 - 14) < 1e-12                   # Câu 3
assert abs(1 / (1 / 2 + 1 / 6 + 1 / 6) - 1.2) < 1e-12 and abs(ss(2 + 6, 6) - 3.43) < 0.01
assert abs(ss(20, 30) - 12) < 1e-12 and abs(1 / 20 + 1 / 30 - 0.083) < 1e-3            # Câu 5
assert abs(1 / 4 + 1 / 12 - 1 / 3) < 1e-12 and abs(ss(4, 12) - 3) < 1e-12              # bảng Bẫy 2
R23 = ss(12, 6); Rtd = 4 + R23; I_ = 12 / Rtd; U1_ = I_ * 4; U23 = 12 - U1_            # bài toán mẫu
assert abs(R23 - 4) < 1e-12 and abs(Rtd - 8) < 1e-12 and abs(I_ - 1.5) < 1e-12 and abs(U1_ - 6) < 1e-12
assert abs(U23 / 12 - 0.5) < 1e-12 and abs(U23 / 6 - 1) < 1e-12
R23b = ss(12, 12); Rtdb = 4 + R23b; Ib = 12 / Rtdb                                       # điền bước
assert abs(R23b - 6) < 1e-12 and abs(Rtdb - 10) < 1e-12 and abs(Ib - 1.2) < 1e-12 and abs(Ib * R23b - 7.2) < 1e-9
assert abs(7.2 / 12 - 0.6) < 1e-12
assert abs(12 / 16 - 0.75) < 1e-12 and abs(0.75 * 12 - 9) < 1e-12                      # thử sức R3 đứt
R23c = ss(6, 3); Ic = 10 / (3 + R23c); U23c = Ic * R23c                                  # Câu 7
assert abs(R23c - 2) < 1e-12 and abs(Ic - 2) < 1e-12 and abs(U23c - 4) < 1e-12
assert abs(U23c / 6 - 0.67) < 0.005 and abs(U23c / 3 - 1.33) < 0.005 and abs(Ic / 2 - 1) < 1e-12
assert abs(6 + ss(6, 6) - 9) < 1e-12 and abs(ss(6 + 6, 6) - 4) < 1e-12                 # thử thách ⭐⭐⭐

# ---------- Dựng theory.html
h = (HERE / "theory.src.html").read_text(encoding="utf8")
for k, v in (("__BANG_TN1__", bang1), ("__I_TN1__", I_TN1), ("__TONG3__", TONG3), ("__UAB3__", UAB3),
             ("__FB_TN1__", FB1), ("__NHAN_XET_TN1__", NX1),
             ("__I1_TN2__", vn(I1, 2)), ("__I2_TN2__", vn(I2, 2)), ("__I_TN2__", vn(I1 + I2, 2)), ("__PHUT__", str(PHUT))):
    assert k in h, k
    h = h.replace(k, v)
for n, fg in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
assert "__" not in h.replace("___", "")
(HERE / "theory.html").write_text(h, encoding="utf8")

# ---------- Kho thí nghiệm
BAI = "Bài 12. Đoạn mạch nối tiếp, song song"
SRC = "content/lesson-samples/l9-doan-mach-noi-tiep-song-song/theory.html"
base = {"mon": "vat-ly", "lop": 9, "bai": BAI, "lesson_id": 90, "nguon_trong_bai": SRC}
tn = []
tn.append({**base,
  "id": "tn-l9-doanmach-01", "ten": "Đo cường độ dòng điện và hiệu điện thế trong đoạn mạch nối tiếp", "loai": "thi_nghiem", "muc_do": "trung_binh",
  "kien_thuc": ["doan_mach.noi_tiep_i_bang_nhau", "doan_mach.noi_tiep_u_cong", "doan_mach.noi_tiep_r_td", "doan_mach.sai_so_do"],
  "muc_tieu": "Thấy trong đoạn mạch nối tiếp, cường độ dòng điện như nhau ở mọi chỗ, U = U1 + U2, và U chia theo tỉ lệ điện trở.",
  "dung_cu": [{"ten": "Nguồn điện chỉnh được 0–6 V", "so_luong": 1},
              {"ten": "Điện trở 10 Ω và 20 Ω", "so_luong": 2},
              {"ten": "Ampe kế (GHĐ 0,5 A, ĐCNN 0,01 A)", "so_luong": 1},
              {"ten": "Vôn kế (GHĐ 10 V, ĐCNN 0,1 V)", "so_luong": 1},
              {"ten": "Khoá K và dây nối", "so_luong": 1}],
  "cac_buoc": {"lam": ["Mắc R1 = 10 Ω nối tiếp R2 = 20 Ω, ampe kế nối tiếp, vôn kế giữa A và B (Hình 2).",
                       "Lần lượt chỉnh nguồn khoảng 3 V; 4,5 V; 6 V.",
                       "Mỗi lần: đặt ampe kế ở ba chỗ (trước R1, giữa hai điện trở, sau R2) và đọc.",
                       "Dùng vôn kế đo U1 (giữa A, M), U2 (giữa M, B) và U_AB."],
               "quan_sat": ["Ở mỗi lần, ampe kế ở ba chỗ chỉ cùng một số: " + "; ".join(f"{x[3]:.2f}".replace(".", ",") + " A" for x in rows1) + ".",
                            "U1 + U2 bằng hoặc gần bằng U_AB; U2 gấp đôi U1."],
               "rut_ra": ["Nối tiếp: I = I1 = I2.", "U = U1 + U2.", "U1/U2 = R1/R2: điện trở lớn nhận hiệu điện thế lớn.",
                          "Lệch 0,1 V ở lần 3 nằm trong sai số đọc của ba lần đo (tối đa 0,15 V)."]},
  "tham_so": [{"ky_hieu": "U", "ten": "Hiệu điện thế thật giữa A và B (nguồn chỉnh được)", "don_vi": "V", "kieu": "dieu_chinh", "min": 0, "max": 6.5, "mac_dinh": 3, "buoc": 0.01},
              {"ky_hieu": "U_AB", "ten": "Số chỉ vôn kế giữa A và B", "don_vi": "V", "kieu": "do_duoc", "sai_so_do": 0.05},
              {"ky_hieu": "R1", "ten": "Điện trở 1", "don_vi": "Ω", "kieu": "co_dinh", "gia_tri": R1},
              {"ky_hieu": "R2", "ten": "Điện trở 2", "don_vi": "Ω", "kieu": "co_dinh", "gia_tri": R2},
              {"ky_hieu": "I", "ten": "Cường độ dòng điện", "don_vi": "A", "kieu": "do_duoc", "sai_so_do": 0.005},
              {"ky_hieu": "U1", "ten": "Hiệu điện thế giữa hai đầu R1", "don_vi": "V", "kieu": "do_duoc", "sai_so_do": 0.05},
              {"ky_hieu": "U2", "ten": "Hiệu điện thế giữa hai đầu R2", "don_vi": "V", "kieu": "do_duoc", "sai_so_do": 0.05}],
  "mo_hinh": {"phuong_trinh": ["R_td = R1 + R2", "I = U/R_td", "U1 = I·R1", "U2 = I·R2", "U1_doc = làm tròn(U1, 0,1 V); U2_doc = làm tròn(U2, 0,1 V); U_AB_doc = làm tròn(U, 0,1 V); I_doc = làm tròn(I, 0,01 A)", "ví dụ hàng 3: U = 6,07 V → U1 = 2,023 → 2,0; U2 = 4,047 → 4,0; U_AB → 6,1; I = 0,2023 → 0,20"],
              "gia_thiet": ["bỏ qua điện trở ampe kế, dây nối; vôn kế có điện trở rất lớn",
                            "hiệu điện thế thật giữa A, B ba lần: " + "; ".join(str(u).replace(".", ",") for u in U_THAT) + " V"]},
  "so_lieu_mau": {"cot": ["U1 (V)", "U2 (V)", "U_AB (V)", "I (A)"],
                  "hang": [list(x) for x in rows1],
                  "ghi_chu": "Số liệu minh hoạ: giá trị tính từ mô hình rồi làm tròn theo độ chia của dụng cụ; chưa phải số đo thật. Lần 3: nguồn chỉnh khoảng 6 V, đo thực tế 6,07 V. Lần 3 lệch 0,1 V vì mỗi số đọc có sai số tới nửa độ chia (mô hình làm tròn đến 0,1 V)."},
  "ket_qua_ky_vong": "I như nhau ở ba chỗ; U1 + U2 ≈ U_AB; U2 = 2U1.",
  "hien_tuong_hay_sai": ["Nghĩ dòng điện giảm dần sau mỗi điện trở.", "Nghĩ hiệu điện thế chia đều cho hai điện trở.",
                         "Cho rằng lệch 0,1 V nghĩa là định luật cộng hiệu điện thế sai."],
  "sai_so_thuong_gap": "Mỗi lần đọc vôn kế lệch tới nửa vạch (0,05 V); tổng hiệu của ba số đọc có thể lệch tới 0,15 V.",
  "an_toan": "Không mắc ampe kế song song với điện trở hay nguồn; ngắt khoá giữa các lần đổi chỗ dụng cụ.",
  "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu", "y_tuong": "Kéo thanh U; kéo ampe kế tới ba vị trí trên mạch, số chỉ không đổi; vôn kế kẹp vào A–M, M–B, A–B.",
                     "diem_nhan": "Số chỉ ampe kế giống nhau ở mọi chỗ; vôn kế chia theo tỉ lệ R."}})
tn.append({**base,
  "id": "tn-l9-doanmach-02", "ten": "Dòng điện rẽ nhánh trong đoạn mạch song song", "loai": "thi_nghiem", "muc_do": "co_ban",
  "kien_thuc": ["doan_mach.song_song_u_bang_nhau", "doan_mach.song_song_i_cong", "doan_mach.song_song_r_td"],
  "muc_tieu": "Thấy dòng mạch chính bằng tổng dòng các nhánh, mỗi nhánh nhận đủ hiệu điện thế và không phụ thuộc nhánh kia.",
  "dung_cu": [{"ten": "Nguồn điện 6 V", "so_luong": 1},
              {"ten": "Điện trở 10 Ω và 15 Ω", "so_luong": 2},
              {"ten": "Ampe kế (GHĐ 1,5 A, ĐCNN 0,02 A)", "so_luong": 3},
              {"ten": "Vôn kế (GHĐ 10 V, ĐCNN 0,1 V)", "so_luong": 1},
              {"ten": "Khoá K và dây nối", "so_luong": 1}],
  "cac_buoc": {"lam": ["Mắc R1 = 10 Ω song song R2 = 15 Ω giữa A và B, ampe kế A1, A2 trong từng nhánh, ampe kế mạch chính, vôn kế giữa A và B (Hình 3).",
                       "Đóng khoá, đọc vôn kế và ba ampe kế."],
               "quan_sat": ["Vôn kế chỉ 6,0 V.", "A1 chỉ 0,60 A.", "A2 chỉ 0,40 A.", "Ampe kế mạch chính chỉ 1,00 A."],
               "rut_ra": ["Song song: U = U1 = U2; I = I1 + I2.", "1/R_td = 1/R1 + 1/R2: R_td = 6 Ω nhỏ hơn cả 10 Ω và 15 Ω.",
                          "Hai nhánh cùng hiệu điện thế U."]},
  "tham_so": [{"ky_hieu": "U", "ten": "Hiệu điện thế giữa A và B", "don_vi": "V", "kieu": "co_dinh", "gia_tri": U2_},
              {"ky_hieu": "R1", "ten": "Điện trở nhánh 1", "don_vi": "Ω", "kieu": "dieu_chinh", "min": 10, "max": 30, "mac_dinh": Ra, "buoc": 5},
              {"ky_hieu": "R2", "ten": "Điện trở nhánh 2", "don_vi": "Ω", "kieu": "dieu_chinh", "min": 10, "max": 30, "mac_dinh": Rb, "buoc": 5},
              {"ky_hieu": "I1", "ten": "Dòng nhánh 1", "don_vi": "A", "kieu": "tinh_ra"},
              {"ky_hieu": "I2", "ten": "Dòng nhánh 2", "don_vi": "A", "kieu": "tinh_ra"},
              {"ky_hieu": "I", "ten": "Dòng mạch chính", "don_vi": "A", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["I1 = U/R1", "I2 = U/R2", "I = I1 + I2", "R_td = R1·R2/(R1 + R2)"],
              "gia_thiet": ["bỏ qua điện trở trong của nguồn, ampe kế, dây nối", "vôn kế có điện trở rất lớn",
                            "với khoảng R1, R2 khai ở trên, I lớn nhất = 6/10 + 6/10 = 1,2 A, trong GHĐ 1,5 A của ampe kế"]},
  "so_lieu_mau": {"cot": ["Trạng thái", "U (V)", "I1 (A)", "I2 (A)", "I (A)"],
                  "hang": [["đủ hai nhánh", U2_, I1, I2, I1 + I2]],
                  "ghi_chu": "Số liệu minh hoạ tính từ mô hình, chưa phải số đo thật."},
  "ket_qua_ky_vong": "I = I1 + I2 = 1,00 A; vôn kế chỉ 6,0 V cho cả hai nhánh.",
  "hien_tuong_hay_sai": ["Nghĩ hiệu điện thế chia đôi cho hai nhánh.", "Nghĩ tháo một nhánh thì nhánh kia nhận thêm dòng, sáng hơn.",
                         "Cộng R1 + R2 như mạch nối tiếp."],
  "an_toan": "Không nối tắt A với B bằng dây trần (gần như nối tắt nguồn).",
  "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu", "y_tuong": "Chấm điện tích chạy, tới A rẽ hai nhánh theo tỉ lệ I1 : I2; nút tháo/lắp từng nhánh.",
                     "diem_nhan": "Tháo một nhánh: dòng nhánh kia không đổi, chỉ dòng mạch chính giảm."}})
tn.append({**base,
  "id": "tn-l9-doanmach-03", "ten": "Tháo một bóng đèn trong mạch nối tiếp và song song", "loai": "thi_nghiem", "muc_do": "co_ban",
  "kien_thuc": ["doan_mach.noi_tiep_mot_duong", "doan_mach.song_song_doc_lap", "doan_mach.mang_dien_gia_dinh"],
  "muc_tieu": "Thấy trong mạch nối tiếp một bóng hỏng thì mạch hở, tắt hết; trong mạch song song các nhánh còn lại vẫn hoạt động.",
  "dung_cu": [{"ten": "Hai pin 1,5 V (nguồn 3 V)", "so_luong": 1},
              {"ten": "Bóng đèn pin 3 V giống nhau, có đui", "so_luong": 2},
              {"ten": "Khoá K và dây nối", "so_luong": 1}],
  "cac_buoc": {"lam": ["Mắc hai bóng nối tiếp với nguồn 3 V, đóng khoá.", "Tháo một bóng khỏi đui.",
                       "Mắc lại hai bóng song song, đóng khoá.", "Tháo một bóng khỏi đui."],
               "quan_sat": ["Nối tiếp: hai bóng sáng mờ.", "Nối tiếp, tháo một bóng: bóng kia tắt.",
                            "Song song: hai bóng sáng rõ.", "Song song, tháo một bóng: bóng kia sáng như cũ."],
               "rut_ra": ["Nối tiếp chỉ có một đường đi: hở một chỗ là hở cả mạch.",
                          "Song song: mỗi nhánh nhận đủ U của nguồn, độc lập với nhánh khác.",
                          "Đèn, quạt trong nhà mắc song song để mỗi thiết bị nhận đủ 220 V và bật tắt riêng."]},
  "tham_so": [{"ky_hieu": "U", "ten": "Hiệu điện thế nguồn", "don_vi": "V", "kieu": "co_dinh", "gia_tri": U3},
              {"ky_hieu": "R_b", "ten": "Điện trở mỗi bóng (coi không đổi)", "don_vi": "Ω", "kieu": "co_dinh", "gia_tri": RBONG},
              {"ky_hieu": "cach_mac", "ten": "Cách mắc", "don_vi": "", "kieu": "dieu_chinh", "min": 0, "max": 1, "mac_dinh": 0, "buoc": 1,
               "lua_chon": [{"gia_tri": 0, "ten": "nối tiếp"}, {"gia_tri": 1, "ten": "song song"}]},
              {"ky_hieu": "I_bong", "ten": "Dòng qua mỗi bóng", "don_vi": "A", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["nối tiếp: I = U/(2R_b), mỗi bóng U/2", "song song: mỗi bóng I = U/R_b, nhận đủ U",
                               "tháo một bóng: nối tiếp I = 0; song song bóng còn lại I = U/R_b"],
              "gia_thiet": ["coi điện trở bóng không đổi (thực tế dây tóc nguội thì điện trở nhỏ hơn)", "bỏ qua điện trở trong của pin"]},
  "so_lieu_mau": {"cot": ["Cách mắc", "Dòng mỗi bóng (A)", "Tháo một bóng: dòng bóng còn lại (A)"],
                  "hang": [["nối tiếp", I_nt, 0], ["song song", I_ss, I_ss]],
                  "ghi_chu": "Số liệu minh hoạ từ mô hình R bóng = 6 Ω không đổi, chưa phải số đo thật; bài chỉ dùng phần định tính."},
  "ket_qua_ky_vong": "Nối tiếp: tháo một bóng, bóng kia tắt. Song song: bóng kia sáng như cũ.",
  "hien_tuong_hay_sai": ["Nghĩ trong mạch song song, tháo một bóng thì bóng kia sáng hơn vì nhận thêm dòng.",
                         "Nghĩ bóng đứt dây tóc vẫn cho dòng đi qua yếu hơn."],
  "an_toan": "Dùng pin, không làm với điện lưới 220 V.",
  "goi_y_mo_phong": {"loai": "2d_dong_hoc", "y_tuong": "Chọn nối tiếp hoặc song song; bấm vào một bóng để tháo; độ sáng các bóng đổi theo dòng tính ra.",
                     "diem_nhan": "Song song: tháo một bóng, bóng còn lại không đổi độ sáng."}})
for dct in tn:
    p = ROOT / "content" / "thi-nghiem" / f"{dct['id']}.json"
    p.write_text(json.dumps(dct, ensure_ascii=False, indent=1), encoding="utf8")

print("ok", len(h), "| TN1:", rows1, "lech", lech, "| TN2:", I1, I2, Rp)
