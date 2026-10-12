"""Bài 11. Điện trở. Định luật Ohm (KHTN 9, lesson_id 89).
Sinh 4 hình SVG + bảng số liệu thí nghiệm + 3 file content/thi-nghiem/tn-l9-ohm-0N.json,
thay mốc <!--FIGn--> / __...__ trong theory.src.html -> theory.html.
Mọi số liệu tính từ mô hình I = U/R, R = ρl/S (assert). Chạy: cd <thư mục bài> && python3 build_figs.py
"""
import json, math, pathlib
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PHUT = 15          # số phút đọc: lấy từ lint_do_dai.py, làm tròn lên

def vn(x, nd=1):
    return f"{x:.{nd}f}".replace(".", "{,}")
def vt(x, nd=1):
    """Số thập phân cho <text> SVG (dấu phẩy thường)."""
    return f"{x:.{nd}f}".replace(".", ",")
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'
def poly(pts, c="currentColor", w=2.2):
    return pts_path(pts, c, w)
def T(x, y, s, c="currentColor", size=18, anchor="start", weight="700"):
    return text(x, y, s, c, size, anchor, weight)
def it_(s):
    """Ký hiệu đại lượng trong SVG: chữ nghiêng có chân (I sans-serif trông như vạch đứng)."""
    return f'<tspan font-family="Georgia, \'Times New Roman\', serif" font-style="italic">{s}</tspan>'
def dot(x, y, c="currentColor", r=3.5):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'
def cur(x, y, dx, dy):
    """Đầu V chỉ chiều dòng điện quy ước trên dây."""
    return chevron(x, y, dx, dy, RED, 2.6, 13)

# ---------- Hình 1: cảnh mở bài (chỉ vẽ hiện tượng, không vẽ dòng điện, không nói cơ chế)
def battery_pic(x, y):
    """Pin vẽ đứng: thân (x..x+46, y..y+90), cực + ở trên."""
    g = f'<rect x="{x}" y="{y}" width="46" height="90" rx="5" fill="rgba(251,146,60,.12)" stroke="currentColor" stroke-width="2.2"/>'
    g += f'<rect x="{x+15}" y="{y-8}" width="16" height="8" fill="currentColor"/>'
    g += T(x + 23, y + 52, "9 V", "currentColor", 16, "middle")
    g += T(x + 52, y + 6, "+", "currentColor", 20) + T(x + 52, y + 92, "−", "currentColor", 20)
    return g
def led_pic(cx, cy, ok=True):
    """LED: chóp tròn tâm (cx, cy) bán kính 12, đế, hai chân dài xuống y = cy + 50."""
    fill = "rgba(248,113,113,.55)" if ok else "rgba(120,120,120,.35)"
    g = (f'<path d="M{cx-12},{cy+12} L{cx-12},{cy} A12 12 0 0 1 {cx+12},{cy} L{cx+12},{cy+12} Z" fill="{fill}" '
         f'stroke="currentColor" stroke-width="2"/>')
    g += f'<rect x="{cx-15}" y="{cy+12}" width="30" height="5" fill="currentColor"/>'
    g += line(cx - 6, cy + 17, cx - 6, cy + 50, "currentColor", 2) + line(cx + 6, cy + 17, cx + 6, cy + 50, "currentColor", 2)
    if ok:
        for a in (-160, -125, -90, -55, -20):
            r = math.radians(a)
            g += line(cx + 20 * math.cos(r), cy + 20 * math.sin(r), cx + 31 * math.cos(r), cy + 31 * math.sin(r), RED, 2.6)
    else:
        g += f'<path d="M{cx-7},{cy-6} L{cx-1},{cy+2} L{cx-5},{cy+6} L{cx+3},{cy+12}" fill="none" stroke="currentColor" stroke-width="1.8"/>'
        g += f'<path d="M{cx},{cy-18} q-8,-8 0,-16 q8,-8 0,-16" fill="none" stroke="currentColor" stroke-width="2" opacity=".55"/>'
    return g
def resistor_pic(x, y):
    """Điện trở 'hạt đậu' nằm ngang từ x tới x+40, tâm y; ba vạch màu."""
    g = f'<rect x="{x}" y="{y-9}" width="40" height="18" rx="8" fill="rgba(251,146,60,.35)" stroke="currentColor" stroke-width="2"/>'
    for k, c in enumerate((RED, "currentColor", ORG)):
        g += line(x + 11 + 9 * k, y - 9, x + 11 + 9 * k, y + 9, c, 3.2)
    return g

b = ""
# (a) pin -> điện trở -> LED -> pin
bx, by = 20, 80
cxa = 170
b += battery_pic(bx, by)
b += poly([(bx + 23, by - 8), (bx + 23, 40), (90, 40)])
b += resistor_pic(90, 40)
b += poly([(130, 40), (148, 40), (148, 165), (cxa - 6, 165), (cxa - 6, 150)])
b += led_pic(cxa, 100, True)
b += poly([(cxa + 6, 150), (cxa + 6, 195), (bx + 23, 195), (bx + 23, by + 90)])
b += T(12, 228, "(a) có “hạt đậu”:", "currentColor", 17) + T(12, 249, "LED sáng đều", "currentColor", 17)
# vạch ngăn
b += line(208, 20, 208, 250, "currentColor", 1.2, "5 5", .5)
# (b) pin -> LED trực tiếp
dx = 215
cxb = 385
b += battery_pic(bx + dx, by)
b += poly([(bx + dx + 23, by - 8), (bx + dx + 23, 40), (363, 40), (363, 165), (cxb - 6, 165), (cxb - 6, 150)])
b += led_pic(cxb, 100, False)
b += poly([(cxb + 6, 150), (cxb + 6, 195), (bx + dx + 23, 195), (bx + dx + 23, by + 90)])
b += T(225, 228, "(b) nối thẳng:", "currentColor", 17) + T(225, 249, "LED cháy, tắt hẳn", "currentColor", 17)
fig1 = wrap("0 0 420 260", "Hai mạch đèn LED với pin 9 V: có linh kiện vạch màu thì LED sáng đều, nối thẳng thì LED cháy", b,
            "Hình 1. (a) LED nối tiếp với “hạt đậu” vạch màu: sáng đều.<br>(b) LED nối thẳng vào pin 9 V: loé sáng rồi cháy.")

# ---------- Hình 2: sơ đồ đo U, I của điện trở R
b = ""
X0, X1, Y0, Y1 = 50, 300, 60, 240
AX, VY = 175, 150            # tâm ampe kế (AX, Y0); tâm vôn kế (390, VY)
RA = 22
PX, NX = 168, 182            # bản cực + (dài) và − (ngắn) của nguồn trên dây dưới
J1, J2 = 90, 210             # hai điểm nút của nhánh vôn kế
RT, RB = 120, 180            # đầu trên, dưới của điện trở
KT, KB = 125, 175            # hai chốt khoá K
W = 2.4
b += poly([(PX, Y1), (X0, Y1), (X0, KB)], "currentColor", W)
b += poly([(X0, KT), (X0, Y0), (AX - RA, Y0)], "currentColor", W)
b += poly([(AX + RA, Y0), (X1, Y0), (X1, RT)], "currentColor", W)
b += poly([(X1, RB), (X1, Y1), (NX, Y1)], "currentColor", W)
# khoá K (đóng)
b += dot(X0, KT, "currentColor", 4) + dot(X0, KB, "currentColor", 4) + line(X0, KB, X0, KT, "currentColor", 3)
b += T(X0 + 14, 156, "K", "currentColor", 18)
# nguồn
b += line(PX, Y1 - 18, PX, Y1 + 18, "currentColor", 2.4) + line(NX, Y1 - 9, NX, Y1 + 9, "currentColor", 5)
b += T(PX - 6, Y1 - 24, "+", "currentColor", 20, "end") + T(NX + 6, Y1 - 24, "−", "currentColor", 20)
# ampe kế
b += f'<circle cx="{AX}" cy="{Y0}" r="{RA}" fill="none" stroke="currentColor" stroke-width="2.4"/>' + T(AX, Y0 + 8, "A", "currentColor", 22, "middle")
b += T(AX - RA - 4, Y0 - 12, "+", "currentColor", 20, "end") + T(AX + RA + 4, Y0 - 12, "−", "currentColor", 20)
# điện trở
b += f'<rect x="{X1-12}" y="{RT}" width="24" height="{RB-RT}" fill="rgba(251,146,60,.2)" stroke="currentColor" stroke-width="2.4"/>'
b += T(X1 - 20, 156, it_("R"), "currentColor", 22, "end")
# vôn kế song song với R
b += dot(X1, J1) + dot(X1, J2)
b += poly([(X1, J1), (390, J1), (390, VY - RA)], "currentColor", W)
b += poly([(390, VY + RA), (390, J2), (X1, J2)], "currentColor", W)
b += f'<circle cx="390" cy="{VY}" r="{RA}" fill="none" stroke="currentColor" stroke-width="2.4"/>' + T(390, VY + 8, "V", "currentColor", 22, "middle")
b += T(400, VY - RA - 2, "+", "currentColor", 20) + T(400, VY + RA + 18, "−", "currentColor", 20)
# chiều dòng điện quy ước (đỏ): + -> trái -> lên -> phải -> xuống -> trái -> −
b += cur(110, Y1, -1, 0) + cur(X0, 100, 0, -1) + cur(245, Y0, 1, 0) + cur(X1, 230, 0, 1) + cur(240, Y1, -1, 0)
b += T(245, Y0 - 12, it_("I"), RED, 22, "middle")
b += T(20, 284, "Dòng điện: từ (+) qua mạch ngoài về (−)", RED, 16)
# kiểm chiều: mũi tên dây dưới bên trái phải chỉ ra xa cực + (sang trái), dây dưới bên phải chỉ về cực − (sang trái)
assert PX < NX and 110 < PX and 240 > NX
fig2 = wrap("0 0 440 296", "Sơ đồ mạch: nguồn, khoá K, ampe kế nối tiếp, điện trở R, vôn kế song song với R; mũi tên đỏ chỉ chiều dòng điện", b,
            "Hình 2. Ampe kế mắc nối tiếp, vôn kế mắc song song với $R$.<br>Chốt (+) của hai dụng cụ nối về phía cực (+) của nguồn.")

# ---------- Thí nghiệm 2: số liệu đo U–I (minh hoạ, từ mô hình R = 20 Ω + làm tròn theo độ chia)
R2 = 20.0
U2 = (1.5, 3.0, 4.5, 6.0)
LECH2 = (0.004, 0.0, -0.004, 0.0)          # độ lệch khi đọc kim ampe kế (A), dưới nửa vạch 0,005 A
rows2 = []
for u, e in zip(U2, LECH2):
    it = u / R2
    ido = round(it + e, 2)
    assert abs(ido - it) <= 0.005 + 1e-9, (u, ido, it)   # sai lệch không quá nửa độ chia
    rows2.append((u, it, ido, u / ido))
rs = [r[3] for r in rows2]
mean2 = sum(rs) / len(rs)
dev2 = [abs(x - R2) for x in rs]
mx2 = max(dev2)
worst2 = [i for i, d in enumerate(dev2) if abs(d - mx2) < 1e-6]
assert worst2 == [0], worst2                 # lần 1 lệch nhiều nhất, duy nhất
exact2 = [i + 1 for i, d in enumerate(dev2) if d < 1e-9]
assert exact2 == [2, 4]
assert [r[2] for r in rows2] == [0.08, 0.15, 0.22, 0.30]
bang2 = "\n".join(f"<tr><td>${vn(u, 1)}$</td><td>${vn(ido, 2)}$</td><td>${vn(q, 2)}$</td></tr>" for u, _, ido, q in rows2)
U_TN2 = ";\\ ".join(vn(u, 1) for u in U2) + "\\ \\text{V}"
p_small = 0.005 / rows2[0][2] * 100
p_big = 0.005 / rows2[3][2] * 100
assert 6 < p_small < 7 and 1 < p_big < 2
FB2 = (f"Kim chỉ lệch chừng nửa vạch $(0{{,}}005\\ \\text{{A}}).$ So với ${vn(rows2[0][2], 2)}\\ \\text{{A}}$ đó là khoảng "
       f"${round(p_small)}\\ \\%,$ so với ${vn(rows2[3][2], 2)}\\ \\text{{A}}$ chỉ gần ${math.ceil(p_big)}\\ \\%.$ "
       f"Dòng càng nhỏ, cùng một sai lệch đọc càng làm $U/I$ lệch nhiều.")
NX2 = (f"Trung bình $\\dfrac{{U}}{{I}} \\approx {vn(mean2, 1)}\\ \\Omega.$<br>"
       f"Lần 2 và lần 4 ra đúng $20\\ \\Omega.$<br>"
       f"Lần 1 lệch nhiều nhất $({vn(rs[0], 2)}\\ \\Omega)$ vì dòng nhỏ nhất.<br>"
       f"Sai số đến từ việc đọc kim ampe kế, vôn kế theo độ chia; muốn bớt sai số thì đo nhiều lần, lấy trung bình.")

# ---------- Thí nghiệm 3: R = ρl/S (constantan, nichrome), nguồn 1,5 V
U3 = 1.5
RHO = {"constantan": 0.50e-6, "nichrome": 1.10e-6}
DAY3 = [("constantan", 1.0, 0.1), ("constantan", 2.0, 0.1), ("constantan", 1.0, 0.2), ("nichrome", 1.0, 0.1)]
rows3 = []
for vl, l, s_mm2 in DAY3:
    R = RHO[vl] * l / (s_mm2 * 1e-6)
    rows3.append((vl, l, s_mm2, R, U3 / R))
I3 = [round(r[4], 2) for r in rows3]
assert I3 == [0.30, 0.15, 0.60, 0.14], I3
assert [round(r[3], 2) for r in rows3] == [5.0, 10.0, 2.5, 11.0]
IMAX3 = U3 * 0.2e-6 / (RHO["constantan"] * 1.0)
assert IMAX3 <= 1.0 + 1e-9, IMAX3
I_TN3 = "; ".join(f"${vn(i, 2)}\\ \\text{{A}}$" for i in I3)
U_TN3 = f"${vn(U3, 1)}\\ \\text{{V}}$"

# ---------- Kiểm số liệu các quiz/bài toán mẫu bằng mô hình
assert abs(6 / 0.2 - 30) < 1e-9                       # Câu 1
assert abs(6 / 200 - 0.03) < 1e-9 and 6 * 200 == 1200 and abs(6 * 0.2 - 1.2) < 1e-9
assert 3 / 15 == 0.2 and 6 / 15 == 0.4                # Câu 4
Rm = 1.1e-6 * 5 / 0.1e-6                              # bài toán mẫu
assert abs(Rm - 55) < 1e-9 and abs(220 / Rm - 4) < 1e-9
assert abs(220 / 2 - 110) < 1e-9 and abs(1.1e-6 * 10 / 0.1e-6 - 110) < 1e-9
assert abs(1.1e-6 * 5 / 0.2e-6 - 27.5) < 1e-9 and abs(220 / 27.5 - 8) < 1e-9
assert abs(0.5e-6 * 5 / 0.1e-6 - 25) < 1e-9 and abs(220 / 25 - 8.8) < 1e-9
Rq = 0.5e-6 * 4 / 0.5e-6                              # Câu 7
assert abs(Rq - 4) < 1e-9 and abs(12 / Rq - 3) < 1e-9 and abs(12 * Rq - 48) < 1e-9
assert abs(Rq / 12 - 0.333) < 1e-3 and abs(12 / (0.5e-6 * 4 / 0.5) - 3e6) < 1e-3
assert 12 / 2 == 6 and 12 / 4 == 3                    # Câu 3, thử thách ⭐⭐

# ---------- Hình 3: đồ thị I theo U, số liệu thí nghiệm 2
def axes(ox, oy, xend, ytop, xl, yl):
    g = line(ox, oy, xend, oy, "currentColor", 2) + chevron(xend, oy, 1, 0, "currentColor", 2, 11)
    g += line(ox, oy, ox, ytop, "currentColor", 2) + chevron(ox, ytop, 0, -1, "currentColor", 2, 11)
    g += T(xend - 4, oy + 40, xl, "currentColor", 17, "end") + T(ox + 10, ytop + 6, yl, "currentColor", 17)
    g += T(ox - 8, oy + 20, "O", "currentColor", 17, "end")
    return g
OX, OY, KX, KY = 64, 250, 50.0, 600.0        # px/V, px/A
def gx(u): return OX + KX * u
def gy(i): return OY - KY * i
b = axes(OX, OY, 400, 30, it_("U") + " (V)", it_("I") + " (A)")
for u in U2:
    b += line(gx(u), OY, gx(u), OY + 6, "currentColor", 2) + T(gx(u), OY + 24, vt(u, 1).replace(",0", ""), "currentColor", 16, "middle")
for i in (0.1, 0.2, 0.3):
    b += line(OX - 6, gy(i), OX, gy(i), "currentColor", 2) + line(OX, gy(i), 390, gy(i), "currentColor", 1, "3 5", .35)
    b += T(OX - 10, gy(i) + 6, vt(i, 1), "currentColor", 16, "end")
UL = 6.6
b += line(gx(0), gy(0), gx(UL), gy(UL / R2), GRN, 2.6)
for u, it, ido, q in rows2:
    px, py = gx(u), gy(ido)
    assert abs(py - gy(u / R2)) <= 4.0, (u, py, gy(u / R2))   # chấm cách đường thẳng ≤ 4 px (sai số đọc ≤ nửa vạch)
    b += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="{ORG}" stroke="currentColor" stroke-width="1.2"/>'
LB = (100, 120)                              # vùng trống giữa vạch lưới 0,3 A (y=70) và 0,2 A (y=130), bên trái đường
assert gy(0.3) + 16 <= LB[0] - 14 and LB[1] + 4 < gy(0.2)
b += T(gx(2.6), LB[0], "đường thẳng", GRN, 17, "end") + T(gx(2.6), LB[1], "qua gốc O", GRN, 17, "end")
fig3 = wrap("0 0 420 300", "Đồ thị cường độ dòng điện theo hiệu điện thế: bốn chấm số liệu nằm sát một đường thẳng đi qua gốc toạ độ", b,
            "Hình 3. Bốn chấm là bốn lần đo trong bảng.<br>Các chấm nằm sát một đường thẳng đi qua gốc O.")

# ---------- Hình 4: đồ thị I theo U của hai dây (bẫy 2) — không ghi R, không kẻ đường gióng (để học sinh tự đọc)
R41, R42 = 10.0, 30.0
OX, OY, KX, KY = 64, 250, 52.0, 340.0
b = axes(OX, OY, 400, 30, it_("U") + " (V)", it_("I") + " (A)")
for u in range(1, 7):
    b += line(gx(u), OY, gx(u), OY + 6, "currentColor", 2) + T(gx(u), OY + 24, str(u), "currentColor", 16, "middle")
for k in range(1, 7):
    i = k / 10
    b += line(OX - 6, gy(i), OX, gy(i), "currentColor", 2) + line(OX, gy(i), 390, gy(i), "currentColor", 1, "3 5", .3)
    b += T(OX - 10, gy(i) + 6, vt(i, 1), "currentColor", 15, "end")
UL1, UL2 = 6.0, 6.4
b += line(gx(0), gy(0), gx(UL1), gy(UL1 / R41), RED, 2.8)
b += line(gx(0), gy(0), gx(UL2), gy(UL2 / R42), BLUE, 2.8)
assert gy(UL1 / R41) >= 30 and gx(UL2) <= 400
# điểm lưới mà học sinh sẽ đọc: (3 V; 0,3 A) và (3 V; 0,1 A) nằm đúng trên hai đường
assert abs(gy(3 / R41) - gy(0.3)) < 1e-9 and abs(gy(3 / R42) - gy(0.1)) < 1e-9
b += T(gx(4.2) - 14, gy(4.2 / R41), "(1)", RED, 18, "end")
b += T(gx(UL2) - 4, gy(UL2 / R42) - 12, "(2)", BLUE, 18, "end")
fig4 = wrap("0 0 420 300", "Đồ thị cường độ dòng điện theo hiệu điện thế của hai dây dẫn: đường (1) dốc hơn đường (2), cả hai qua gốc", b,
            "Hình 4. Đồ thị $I$ theo $U$ của dây (1) (đỏ) và dây (2) (xanh).")

# ---------- Dựng theory.html
h = (HERE / "theory.src.html").read_text(encoding="utf8")
for k, v in (("__U_TN2__", U_TN2), ("__BANG_TN2__", bang2), ("__FB_TN2__", FB2), ("__NHAN_XET_TN2__", NX2),
             ("__U_TN3__", U_TN3), ("__I_TN3__", I_TN3), ("__PHUT__", str(PHUT))):
    assert k in h, k
    h = h.replace(k, v)
for n, fg in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
assert "__" not in h.replace("___", "")
(HERE / "theory.html").write_text(h, encoding="utf8")

# ---------- Kho thí nghiệm
BAI = "Bài 11. Điện trở. Định luật Ohm"
SRC = "content/lesson-samples/l9-dien-tro-dinh-luat-ohm/theory.html"
base = {"mon": "vat-ly", "lop": 9, "bai": BAI, "lesson_id": 89, "nguon_trong_bai": SRC}
tn = []
tn.append({**base,
  "id": "tn-l9-ohm-01", "ten": "Cùng hiệu điện thế, hai dây cho hai dòng điện khác nhau", "loai": "thi_nghiem", "muc_do": "co_ban",
  "kien_thuc": ["ohm.dien_tro", "ohm.r_bang_u_chia_i", "ohm.ampe_von_ke"],
  "muc_tieu": "Thấy cùng một hiệu điện thế, các dây khác nhau cho cường độ dòng điện khác nhau; từ đó định nghĩa R = U/I.",
  "dung_cu": [{"ten": "Nguồn điện chỉnh được 0–6 V (bài dùng 3 V)", "so_luong": 1},
              {"ten": "Ampe kế (GHĐ 1 A, ĐCNN 0,01 A)", "so_luong": 1},
              {"ten": "Vôn kế (GHĐ 6 V, ĐCNN 0,1 V)", "so_luong": 1},
              {"ten": "Dây A, dây B (cuộn dây điện trở 10 Ω và 20 Ω)", "so_luong": 2},
              {"ten": "Khoá K và dây nối", "so_luong": 1}],
  "cac_buoc": {"lam": ["Mắc mạch: nguồn, khoá K, ampe kế nối tiếp với dây cần đo; vôn kế song song với dây (Hình 2).",
                       "Mắc dây A, đóng khoá, đọc vôn kế và ampe kế.",
                       "Thay dây A bằng dây B, đọc lại hai dụng cụ."],
               "quan_sat": ["Vôn kế đều chỉ 3,0 V.", "Ampe kế chỉ 0,30 A với dây A, 0,15 A với dây B."],
               "rut_ra": ["Cùng U, dây cho I nhỏ hơn là dây cản trở dòng điện nhiều hơn.",
                          "Đặc trưng mức cản trở bằng R = U/I: dây A 10 Ω, dây B 20 Ω."]},
  "tham_so": [{"ky_hieu": "U", "ten": "Hiệu điện thế nguồn", "don_vi": "V", "kieu": "dieu_chinh", "min": 1.5, "max": 6, "mac_dinh": 3, "buoc": 1.5},
              {"ky_hieu": "R_A", "ten": "Điện trở dây A", "don_vi": "Ω", "kieu": "co_dinh", "gia_tri": 10},
              {"ky_hieu": "R_B", "ten": "Điện trở dây B", "don_vi": "Ω", "kieu": "co_dinh", "gia_tri": 20},
              {"ky_hieu": "I", "ten": "Cường độ dòng điện", "don_vi": "A", "kieu": "do_duoc", "sai_so_do": 0.005}],
  "mo_hinh": {"phuong_trinh": ["I = U/R", "R = U/I"],
              "gia_thiet": ["bỏ qua điện trở của ampe kế, dây nối và nguồn", "vôn kế có điện trở rất lớn"]},
  "so_lieu_mau": {"cot": ["Dây", "U (V)", "I (A)", "R = U/I (Ω)"],
                  "hang": [["A", 3.0, round(3.0 / 10, 2), 10.0], ["B", 3.0, round(3.0 / 20, 2), 20.0]],
                  "ghi_chu": "Số liệu minh hoạ tính từ mô hình I = U/R, chưa phải số đo thật."},
  "ket_qua_ky_vong": "Dây B cho dòng bằng một nửa dây A nên điện trở gấp đôi.",
  "hien_tuong_hay_sai": ["Tưởng dây nào cũng cho cùng một dòng nếu cùng nguồn.", "Tính R = U·I thay vì U/I."],
  "an_toan": "Không mắc ampe kế song song với nguồn; đóng khoá ngắn rồi ngắt để dây không nóng.",
  "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu", "y_tuong": "Chọn dây A hoặc B, kim ampe kế quay tới giá trị I = U/R; bảng tự tính U/I.",
                     "diem_nhan": "Cùng U, dây cản nhiều thì kim ampe kế lệch ít."}})
tn.append({**base,
  "id": "tn-l9-ohm-02", "ten": "Đo U và I của một dây constantan, vẽ đồ thị I theo U", "loai": "thi_nghiem", "muc_do": "trung_binh",
  "kien_thuc": ["ohm.dinh_luat", "ohm.do_thi_iu", "ohm.sai_so_do"],
  "muc_tieu": "Từ bảng U–I thấy I tỉ lệ thuận với U, U/I gần như không đổi; đồ thị I theo U là đường thẳng qua gốc.",
  "dung_cu": [{"ten": "Nguồn điện điều chỉnh 0–6 V", "so_luong": 1},
              {"ten": "Ampe kế (GHĐ 0,5 A, ĐCNN 0,01 A)", "so_luong": 1},
              {"ten": "Vôn kế (GHĐ 6 V, ĐCNN 0,1 V)", "so_luong": 1},
              {"ten": "Đoạn dây constantan khoảng 20 Ω", "so_luong": 1},
              {"ten": "Khoá K và dây nối", "so_luong": 1}],
  "cac_buoc": {"lam": ["Mắc mạch như Hình 2 với đoạn dây constantan.",
                       "Lần lượt đặt U = " + "; ".join(vt(u, 1) for u in U2) + " V; mỗi lần đọc ampe kế.",
                       "Tính U/I mỗi lần, chấm các điểm (U; I) lên đồ thị."],
               "quan_sat": ["U tăng gấp 2, 3, 4 lần thì I tăng gần đúng chừng ấy lần.", "U/I gần như không đổi, quanh 20 Ω."],
               "rut_ra": ["I tỉ lệ thuận với U: định luật Ohm I = U/R.", "Đồ thị I theo U là đường thẳng đi qua gốc toạ độ.",
                          "Lần dòng nhỏ nhất lệch nhiều nhất vì sai lệch đọc kim chiếm tỉ lệ lớn."]},
  "tham_so": [{"ky_hieu": "U", "ten": "Hiệu điện thế đặt vào dây", "don_vi": "V", "kieu": "dieu_chinh", "min": 0, "max": 6, "mac_dinh": 3, "buoc": 0.5},
              {"ky_hieu": "R", "ten": "Điện trở dây constantan", "don_vi": "Ω", "kieu": "co_dinh", "gia_tri": R2},
              {"ky_hieu": "I", "ten": "Cường độ dòng điện đọc được", "don_vi": "A", "kieu": "do_duoc", "sai_so_do": 0.005},
              {"ky_hieu": "U/I", "ten": "Thương U/I", "don_vi": "Ω", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["I = U/R", "I_doc = lam_tron(I + lech, 0,01 A)", "U/I_doc"],
              "gia_thiet": ["dây constantan: điện trở gần như không đổi theo nhiệt độ",
                            "lech là sai lệch khi đọc kim, không quá nửa vạch: " + ", ".join(str(e) for e in LECH2) + " A"]},
  "so_lieu_mau": {"cot": ["U (V)", "I (A)", "U/I (Ω)"],
                  "hang": [[u, ido, round(q, 2)] for u, _, ido, q in rows2],
                  "ghi_chu": f"Số liệu minh hoạ: I = U/20 cộng sai lệch đọc kim, làm tròn 0,01 A; chưa phải số đo thật. Trung bình U/I = {mean2:.2f} Ω; lần 1 lệch nhiều nhất."},
  "ket_qua_ky_vong": f"U/I trung bình khoảng {mean2:.1f} Ω; các điểm nằm sát đường thẳng qua gốc.",
  "hien_tuong_hay_sai": ["Nghĩ U tăng thì R tăng vì R = U/I.", "Nối các điểm thành đường gấp khúc thay vì kẻ đường thẳng qua gốc.",
                         "Cho rằng lần lệch nhiều là do định luật Ohm sai ở U nhỏ."],
  "sai_so_thuong_gap": "Đọc kim ampe kế lệch nửa vạch; ở dòng nhỏ sai lệch này chiếm tỉ lệ lớn (khoảng 6 % ở 0,08 A).",
  "an_toan": "Không để dòng chạy lâu ở U lớn; ngắt khoá giữa các lần đo.",
  "goi_y_mo_phong": {"loai": "do_thi+bang_so_lieu", "y_tuong": "Kéo thanh U, kim ampe kế nhảy theo độ chia; mỗi lần bấm 'ghi' thêm một chấm lên đồ thị I–U.",
                     "diem_nhan": "Chấm ở U nhỏ lệch khỏi đường thẳng nhiều nhất (tính theo phần trăm)."}})
tn.append({**base,
  "id": "tn-l9-ohm-03", "ten": "Điện trở dây dẫn theo chiều dài, tiết diện, vật liệu", "loai": "thi_nghiem", "muc_do": "trung_binh",
  "kien_thuc": ["ohm.phu_thuoc_chieu_dai", "ohm.phu_thuoc_tiet_dien", "ohm.dien_tro_suat"],
  "muc_tieu": "Thấy điện trở tỉ lệ thuận với chiều dài, tỉ lệ nghịch với tiết diện và phụ thuộc vật liệu: R = ρl/S.",
  "dung_cu": [{"ten": "Pin 1,5 V", "so_luong": 1},
              {"ten": "Ampe kế (GHĐ 1 A, ĐCNN 0,01 A)", "so_luong": 1},
              {"ten": "Dây constantan tiết diện 0,1 mm² (dài 1 m và 2 m)", "so_luong": 2},
              {"ten": "Dây constantan tiết diện 0,2 mm², dài 1 m", "so_luong": 1},
              {"ten": "Dây nichrome tiết diện 0,1 mm², dài 1 m", "so_luong": 1},
              {"ten": "Khoá K và dây nối", "so_luong": 1}],
  "cac_buoc": {"lam": ["Giữ nguồn 1,5 V, lần lượt mắc từng dây vào mạch nối tiếp với ampe kế.",
                       "Mỗi lần đóng khoá, đọc ampe kế rồi ngắt ngay."],
               "quan_sat": ["Dây constantan 1 m, 0,1 mm²: khoảng 0,30 A.", "Dài 2 m: khoảng 0,15 A.",
                            "Tiết diện 0,2 mm²: khoảng 0,60 A.", "Nichrome 1 m, 0,1 mm²: khoảng 0,14 A."],
               "rut_ra": ["Dài gấp đôi, điện trở gấp đôi.", "Tiết diện gấp đôi, điện trở giảm một nửa.",
                          "Cùng kích thước, nichrome có điện trở lớn hơn constantan: R = ρl/S."]},
  "tham_so": [{"ky_hieu": "l", "ten": "Chiều dài dây", "don_vi": "m", "kieu": "dieu_chinh", "min": 1, "max": 3, "mac_dinh": 1, "buoc": 0.5},
              {"ky_hieu": "S", "ten": "Tiết diện dây", "don_vi": "mm²", "kieu": "dieu_chinh", "min": 0.1, "max": 0.2, "mac_dinh": 0.1, "buoc": 0.05},
              {"ky_hieu": "vat_lieu", "ten": "Vật liệu dây", "don_vi": "", "kieu": "dieu_chinh", "min": 0, "max": 1, "mac_dinh": 0, "buoc": 1,
               "lua_chon": [{"gia_tri": 0, "ten": "constantan", "rho": RHO["constantan"]}, {"gia_tri": 1, "ten": "nichrome", "rho": RHO["nichrome"]}]},
              {"ky_hieu": "ρ", "ten": "Điện trở suất theo vật liệu đã chọn", "don_vi": "Ω·m", "kieu": "tinh_ra"},
              {"ky_hieu": "U", "ten": "Hiệu điện thế nguồn", "don_vi": "V", "kieu": "co_dinh", "gia_tri": U3},
              {"ky_hieu": "I", "ten": "Cường độ dòng điện", "don_vi": "A", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["ρ = 0,50·10⁻⁶ Ω·m (constantan) hoặc 1,10·10⁻⁶ Ω·m (nichrome)", "R = ρ·l/S (S đổi ra m²)", "I = U/R"],
              "gia_thiet": ["bỏ qua điện trở trong của pin, ampe kế, dây nối", "nhiệt độ dây coi như không đổi",
                            "giới hạn l, S sao cho I = U·S/(ρ·l) ≤ 1 A (GHĐ ampe kế): với khoảng l, S khai ở trên, I lớn nhất "
                            + vt(IMAX3, 2) + f" A (constantan, l = 1 m, S = 0,2 mm²)"]},
  "so_lieu_mau": {"cot": ["Dây", "l (m)", "S (mm²)", "R (Ω)", "I (A)"],
                  "hang": [[vl, l, s, round(R, 2), round(i, 2)] for vl, l, s, R, i in rows3],
                  "ghi_chu": "Số liệu minh hoạ tính từ R = ρl/S và I = U/R với U = 1,5 V, chưa phải số đo thật."},
  "ket_qua_ky_vong": "Dòng giảm một nửa khi dây dài gấp đôi, gấp đôi khi tiết diện gấp đôi, nhỏ hơn hẳn khi đổi sang nichrome.",
  "hien_tuong_hay_sai": ["Nghĩ dây to hơn thì cản nhiều hơn.", "Nghĩ điện trở chỉ phụ thuộc vật liệu.",
                         "Thay S tính bằng mm² vào công thức mà không đổi ra m²."],
  "sai_so_thuong_gap": "Pin yếu dần và điện trở trong của pin làm dòng đo được nhỏ hơn tính toán, nhất là với dây 0,2 mm² (dòng lớn).",
  "an_toan": "Không thay bằng dây đồng cùng cỡ: điện trở chỉ khoảng 0,17 Ω, gần như nối tắt pin.",
  "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu", "y_tuong": "Kéo dài/thu ngắn dây, đổi độ dày và vật liệu; kim ampe kế và R tính ra đổi theo.",
                     "diem_nhan": "Gập đôi dây: dài một nửa và tiết diện gấp đôi, R còn một phần tư."}})
assert abs(1.7e-8 * 1 / 0.1e-6 - 0.17) < 1e-9
for dct in tn:
    p = ROOT / "content" / "thi-nghiem" / f"{dct['id']}.json"
    p.write_text(json.dumps(dct, ensure_ascii=False, indent=1), encoding="utf8")

print("ok", len(h), "| TN2 U/I:", [round(x, 2) for x in rs], "mean=%.3f" % mean2,
      "| TN3 I:", I3, "| %% nho=%.2f lon=%.2f" % (p_small, p_big))
