"""CĐ08 Cảm ứng điện từ & dòng xoay chiều (bài 152): sinh 6 hình SVG, thay <!--FIGn--> trong theory.src.html -> theory.html.
Chạy lại được: python3 content/hsg9/cd08-cam-ung-dien-tu/build_figs.py
Mọi số liệu dùng trong theory.src.html (quiz, bài toán mẫu, thử thách, bảng thí nghiệm) được tính + assert ở khối SỐ LIỆU dưới đây."""
import os, sys
from math import sqrt, pi, sin, cos, radians
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "soan-bai-ly-thuyet-tuong-tac", "scripts"))
from svg_lib import RED, BLUE, ORG, GRN, text, wrap, chevron, field_line, field_path, cubic, pts_path

PHUT = 18

# ═════════ SỐ LIỆU (kiểm trước khi vẽ) ═════════
RHO_CU = 1.7e-8


def near(a, b, tol=1e-6):
    return abs(a - b) <= tol * max(1, abs(b))


def line_loss(P, U, R):
    I = P / U
    return I, R * I * I, 1 - R * I * I / P, R * I, U - R * I


# q0: tăng U gấp đôi, cùng P, cùng dây -> hao phí giảm 4 lần
assert near((1 / 1) ** 2 / (1 / 2) ** 2, 4)
# q4: máy phát 6 cực = 3 cặp, 1000 vòng/phút
assert near(1000 / 60 * 3, 50)
assert near(1000 / 60 * 6, 100) and near(1000 * 3, 3000) and near(round(1000 / 60, 1), 16.7)
# q5: biến áp lí tưởng 220 V -> 12 V cấp đèn 12 V - 36 W
I2 = 36 / 12
I1 = 36 / 220
assert near(I2, 3) and round(I1, 2) == 0.16 and near(I2 * 220 / 12, 55)
# q6: tiết diện gấp đôi -> R giảm 2 -> hao phí giảm 2 lần (cùng P, U)
# bài toán mẫu: P = 400 kW, dây đồng đôi dài 10 km, S = 34 mm²
P, ell, S = 400e3, 10e3, 34e-6
R = RHO_CU * 2 * ell / S
assert near(R, 10)
I, Php, H, dU, Utt = line_loss(P, 20e3, R)
assert near(I, 20) and near(Php, 4e3) and near(H, 0.99) and near(dU, 200) and near(Utt, 19800)
I, Php, H, dU, Utt = line_loss(P, 5e3, R)
assert near(I, 80) and near(Php, 64e3) and near(H, 0.84) and near(dU, 800)
assert near(sqrt(P * R / 0.0025), 40e3)                       # bước điền: hao phí <= 0,25 % -> U >= 40 kV
# q7: cùng đường dây, U = 10 kV
I, Php, H, dU, Utt = line_loss(P, 10e3, R)
assert near(I, 40) and near(Php, 16e3) and near(H, 0.96)
assert near((10e3) ** 2 / R, 10e6)                             # bẫy U²/R với U đầu dây
# ⭐ máy tăng áp 500/10 000 vòng, U1 = 1 kV, P = 400 kW
assert near(1e3 * 10000 / 500, 20e3) and near(400e3 / 1e3, 400) and near(400e3 / 20e3, 20)
# ⭐⭐ đường kính gấp đôi -> S gấp 4 -> R/4 -> hao phí/4; giữ dây cũ thì U gấp 2
assert near(2 ** 2, 4) and near(sqrt(4), 2)
# Thí nghiệm máy biến áp: N1 = 400 vòng, U1 = 12 V (nguồn xoay chiều học sinh), đo U2
N1_tn, U1_tn = 400, 12
TN = [(100, 2.9), (200, 5.8), (400, 11.6)]
for N2, U2do in TN:
    lt = U1_tn * N2 / N1_tn
    assert 0.94 < U2do / lt < 0.98, (N2, U2do, lt)
assert [U1_tn * n / N1_tn for n, _ in TN] == [3, 6, 12]
# Trả bài: 2 cặp cực, 1500 vòng/phút
assert near(1500 / 60 * 2, 50)

# ═════════ helpers ═════════
GRAY = "rgba(148,163,184,.25)"


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def rect(x, y, w, h, fill="none", c="currentColor", sw=2, rx=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'


def cub_d(P0, P1, P2, P3):
    return f"M{P0[0]:.1f},{P0[1]:.1f} C{P1[0]:.1f},{P1[1]:.1f} {P2[0]:.1f},{P2[1]:.1f} {P3[0]:.1f},{P3[1]:.1f}"


def cub_pt(P0, P1, P2, P3, t):
    u = 1 - t
    return tuple(u**3 * P0[k] + 3 * u * u * t * P1[k] + 3 * u * t * t * P2[k] + t**3 * P3[k] for k in (0, 1))


def cub_tan(P0, P1, P2, P3, t):
    u = 1 - t
    return tuple(3 * u * u * (P1[k] - P0[k]) + 6 * u * t * (P2[k] - P1[k]) + 3 * t * t * (P3[k] - P2[k]) for k in (0, 1))


def loop(P0, P1, P2, P3, c, t=0.5, w=1.8):
    """Đường sức cong nét đứt (cubic) + đầu V tại tham số t, hướng đi P0 -> P3."""
    tip = cub_pt(P0, P1, P2, P3, t)
    return field_path(cub_d(P0, P1, P2, P3), (round(tip[0], 1), round(tip[1], 1)), cub_tan(P0, P1, P2, P3, t), c, w, "6 4", 11)


def magnet(x, y, w, h, left="N"):
    """Nam châm thẳng tô 2 nửa: N đỏ, S xanh."""
    cN, cS = RED, BLUE
    fl = "rgba(248,113,113,.28)" if left == "N" else "rgba(56,189,248,.28)"
    fr = "rgba(56,189,248,.28)" if left == "N" else "rgba(248,113,113,.28)"
    cl, cr = (cN, cS) if left == "N" else (cS, cN)
    right = "S" if left == "N" else "N"
    b = rect(x, y, w / 2, h, fl, cl, 2, 3) + rect(x + w / 2, y, w / 2, h, fr, cr, 2, 3)
    b += text(x + w / 4, y + h / 2 + 6, left, cl, 18, "middle", "800")
    b += text(x + 3 * w / 4, y + h / 2 + 6, right, cr, 18, "middle", "800")
    return b


# ═════════ Hình 1: đường sức của nam châm thẳng ═════════
b = ""
MX0, MX1, MY = 140, 260, 150          # mép trái (N), mép phải (S), trục
for dy, h, dx in ((-8, 62, 34), (-14, 112, 60)):
    y0 = MY + dy
    b += loop((MX0, y0), (MX0 - dx, y0 - h), (MX1 + dx, y0 - h), (MX1, y0), RED)
    y0 = MY - dy
    b += loop((MX0, y0), (MX0 - dx, y0 + h), (MX1 + dx, y0 + h), (MX1, y0), RED)
b += field_line(MX0, MY, 34, MY, RED, 1.8, "6 4", 11)        # đi ra khỏi cực Bắc
b += field_line(366, MY, MX1, MY, RED, 1.8, "6 4", 11)       # đi vào cực Nam
b += magnet(MX0, MY - 20, MX1 - MX0, 40, "N")
b += field_line(MX1 - 14, MY + 12, MX0 + 22, MY + 12, "currentColor", 1.6, "4 3", 9)   # trong nam châm: S -> N
b += text(200, 34, "chỗ đường sức dày: từ trường mạnh", "currentColor", 15, "middle", "600")
b += text(24, 278, "bên ngoài: ra ở N, vào ở S", RED, 15, "start", "700")
b += text(24, 300, "bên trong: từ S sang N (nét mảnh)", "currentColor", 15, "start", "600")
fig1 = wrap("0 12 400 300",
            "Đường sức từ của nam châm thẳng: nét đứt đi ra ở cực Bắc, vòng ra ngoài rồi đi vào cực Nam, trong lòng nam châm đi từ cực Nam sang cực Bắc",
            b, "Hình 1. Đường sức từ của nam châm thẳng là những đường khép kín.<br>Ở gần hai cực, đường sức dày nhất.")

# ═════════ Hình 2: ống dây có dòng điện + nắm tay phải ═════════
b = ""
CY, RY = 120, 42                      # trục ống, bán kính (nửa chiều cao)
XS, XE, NT = 130, 290, 6              # đầu trái, đầu phải, số vòng
pitch = (XE - XS) / NT
# đường sức (vẽ trước, nằm dưới ống)
b += field_line(XS - 20, CY, XE + 24, CY, RED, 1.8, "6 4", 11)                         # trong lòng: trái -> phải
WIRES = [(XS - 30, CY - RY, XS - 30, 236), (XE + 30, CY - RY, XE + 30, 236), (XS - 30, CY - RY, XS, CY - RY), (XE, CY - RY, XE + 30, CY - RY)]


def near_wire(x, y, gap=7):
    for x1, y1, x2, y2 in WIRES:
        if x1 == x2 and abs(x - x1) < gap and min(y1, y2) - gap < y < max(y1, y2) + gap:
            return True
        if y1 == y2 and abs(y - y1) < gap and min(x1, x2) - gap < x < max(x1, x2) + gap:
            return True
    return False


def loop_gap(P0, P1, P2, P3, c):
    """Đường sức cong nét đứt, NGẮT khe chỗ dây nối đi qua phía trước (quy ước che khuất svg_lib)."""
    pts = cubic(P0, P1, P2, P3, 160)
    out, seg = "", []
    for p in pts:
        if near_wire(*p):
            if len(seg) > 1:
                out += pts_path(seg, c, 1.8, "6 4")
            seg = []
        else:
            seg.append(p)
    if len(seg) > 1:
        out += pts_path(seg, c, 1.8, "6 4")
    tip = cub_pt(P0, P1, P2, P3, .5)
    assert not near_wire(*tip)
    return out + chevron(round(tip[0], 1), round(tip[1], 1), *cub_tan(P0, P1, P2, P3, .5), c, 1.8, 11)


b += loop_gap((XE + 8, CY - 22), (XE + 90, CY - 22 - 70), (XS - 90, CY - 22 - 70), (XS - 8, CY - 22), RED)
b += loop_gap((XE + 8, CY + 22), (XE + 90, CY + 22 + 70), (XS - 90, CY + 22 + 70), (XS - 8, CY + 22), RED)
for i in range(NT):
    x0 = XS + i * pitch
    xt, xb = x0, x0 + pitch / 2
    # nét sau (bị che, mảnh): từ đáy lên đỉnh vòng kế
    b += line(xb, CY + RY, x0 + pitch, CY - RY, "currentColor", 1.4, "", .45)
    # nét trước (đậm): từ đỉnh xuống đáy — dòng điện đi XUỐNG ở mặt trước
    b += line(xt, CY - RY, xb, CY + RY, ORG, 3)
    mx, my = (xt + xb) / 2, CY + 14
    b += chevron(mx + (xb - xt) / (2 * RY) * 14, my, xb - xt, 2 * RY, ORG, 2.4, 10)
# dây dẫn tới nguồn
b += line(XS, CY - RY, XS - 30, CY - RY, ORG, 2.4) + line(XS - 30, CY - RY, XS - 30, 236, ORG, 2.4)
b += line(XE, CY - RY, XE + 30, CY - RY, ORG, 2.4) + line(XE + 30, CY - RY, XE + 30, 236, ORG, 2.4)
b += line(XS - 30, 236, 192, 236, ORG, 2.4) + line(208, 236, XE + 30, 236, ORG, 2.4)
b += line(192, 222, 192, 250, "currentColor", 3) + line(208, 228, 208, 244, "currentColor", 5)   # pin: dài (+) bên trái
b += text(184, 218, "+", "currentColor", 16, "end", "700") + text(216, 218, "−", "currentColor", 16, "start", "700")
b += chevron(XS - 30, 200, 0, -1, ORG, 2.4, 10)       # dòng đi từ cực + lên đầu trái
b += text(XS - 38, CY + 6, "S", BLUE, 20, "end", "800")
b += text(XE + 52, CY - 8, "N", RED, 20, "start", "800")
b += text(20, 276, "4 ngón tay: theo chiều dòng điện", ORG, 15, "start", "700")
b += text(20, 298, "ngón cái: chiều đường sức trong lòng ống", RED, 15, "start", "700")
b += text(20, 320, "đầu ngón cái chỉ ra là cực Bắc", "currentColor", 15, "start", "600")
fig2 = wrap("0 40 400 292",
            "Ống dây có dòng điện: dòng ở mặt trước các vòng đi xuống, đường sức trong lòng ống hướng sang phải nên đầu phải là cực Bắc, đầu trái là cực Nam",
            b, "Hình 2. Ống dây có dòng điện giống một nam châm thẳng.<br>Nhìn từ đầu phải: dòng chạy ngược chiều kim đồng hồ, đầu phải là cực Bắc.")

# ═════════ Hình 3: thí nghiệm cảm ứng + định luật Lenz ═════════
b = ""
CY = 110
# nam châm bên trái, cực N quay về cuộn dây
b += magnet(24, CY - 18, 120, 36, "S")                     # trái S, phải N
b += line(84, CY + 40, 142, CY + 40, "currentColor", 2) + chevron(142, CY + 40, 1, 0, "currentColor", 2, 10)
b += text(84, CY + 64, "lại gần", "currentColor", 15, "start", "700")
# cuộn dây
X0, X1, NT = 210, 330, 5
pitch = (X1 - X0) / NT
for i in range(NT):
    x0 = X0 + i * pitch
    b += line(x0 + pitch / 2, CY + 34, x0 + pitch, CY - 34, "currentColor", 1.4, "", .45)
    b += line(x0, CY - 34, x0 + pitch / 2, CY + 34, "currentColor", 2.6)
    if i in (1, 3):   # chiều dòng cảm ứng ở mặt trước: đi LÊN (nhìn từ A ngược chiều kim đồng hồ -> A là N)
        b += chevron(x0 + pitch / 4 - 4 * pitch / 136, CY - 8, -pitch / 2, -68, BLUE, 2.4, 10)
# đường sức của nam châm (đỏ) đi vào cuộn dây, từ trường cảm ứng (xanh) hướng ngược lại
b += field_line(146, CY - 6, 196, CY - 6, RED, 1.8, "6 4", 10)
b += field_line(300, CY + 8, 222, CY + 8, BLUE, 2, "6 4", 11)
b += text(204, CY - 30, "A", "currentColor", 18, "end", "800")
b += text(204, CY - 52, "đầu A: thành cực N", BLUE, 15, "middle", "700")
# điện kế
b += line(X0 + pitch / 2, CY + 34, X0 + pitch / 2, 210) + line(X1, CY - 34, 352, CY - 34) + line(352, CY - 34, 352, 210)
b += line(X0 + pitch / 2, 210, 256, 210) + line(284, 210, 352, 210)
b += f'<circle cx="270" cy="210" r="16" fill="{GRAY}" stroke="currentColor" stroke-width="2"/>'
b += text(270, 216, "G", "currentColor", 16, "middle", "800")
b += line(270, 210, 279, 199, GRN, 2.4)
b += text(24, 252, "đỏ: đường sức của nam châm", RED, 15, "start", "700")
b += text(24, 274, "xanh: từ trường của dòng cảm ứng", BLUE, 15, "start", "700")
b += text(24, 296, "hai cực N đối diện: đẩy nhau", "currentColor", 15, "start", "600")
b += text(24, 318, "mũi tên xanh trên vòng dây: chiều dòng cảm ứng", BLUE, 15, "start", "600")
fig3 = wrap("0 34 400 294",
            "Đưa cực Bắc của nam châm lại gần đầu A của cuộn dây kín nối điện kế: kim điện kế lệch, đầu A trở thành cực Bắc để đẩy nam châm",
            b, "Hình 3. Nam châm đang lại gần: số đường sức qua cuộn dây tăng.<br>Dòng cảm ứng làm đầu A thành cực Bắc, cản nam châm tiến vào.")

# ═════════ Hình 4: dòng xoay chiều đổi chiều 2 lần mỗi chu kì ═════════
b = ""
X0, XAX, Y0, AMP = 56, 384, 120, 64
TPX = 200                               # 1 chu kì = 200 px
b += line(X0, Y0, XAX, Y0, "currentColor", 1.8) + chevron(XAX, Y0, 1, 0, "currentColor", 1.8, 10)
b += line(X0, 214, X0, 30, "currentColor", 1.8) + chevron(X0, 30, 0, -1, "currentColor", 1.8, 10)
b += text(X0 + 8, 38, "i", "currentColor", 16, "start", "700")
b += text(XAX, Y0 + 24, "t", "currentColor", 16, "end", "700")
pts = [(X0 + k, Y0 - AMP * sin(2 * pi * k / TPX)) for k in range(0, 311, 2)]
b += pts_path(pts, GRN, 2.8)
for k in (TPX / 2, TPX):                 # hai lần đổi chiều trong một chu kì
    x = X0 + k
    b += f'<circle cx="{x:.1f}" cy="{Y0}" r="4.5" fill="{ORG}"/>'
b += text(X0 + TPX / 2 - 8, Y0 + 26, "đổi chiều", ORG, 15, "end", "700")
b += text(X0 + TPX + 8, Y0 + 26, "đổi chiều", ORG, 15, "start", "700")
b += text(X0 + TPX / 4, Y0 - AMP - 10, "chiều 1", "currentColor", 15, "middle", "600")
b += text(X0 + 3 * TPX / 4, Y0 + AMP + 22, "chiều 2", "currentColor", 15, "middle", "600")
# chú thích chu kì T
b += line(X0, 232, X0 + TPX, 232, "currentColor", 1.6) + chevron(X0 + TPX, 232, 1, 0, "currentColor", 1.6, 8) + chevron(X0, 232, -1, 0, "currentColor", 1.6, 8)
b += line(X0 + TPX, 214, X0 + TPX, 240, "currentColor", 1.2, "4 3", .7)
b += text(X0 + TPX / 2, 254, "một chu kì T (rôto quay một vòng)", "currentColor", 15, "middle", "600")
fig4 = wrap("0 20 400 244",
            "Đồ thị cường độ dòng điện xoay chiều theo thời gian: hình sin, trong một chu kì dòng điện đổi chiều hai lần",
            b, "Hình 4. Dòng xoay chiều: lúc theo chiều 1, lúc theo chiều 2.<br>Trong một chu kì, dòng đổi chiều hai lần.<br>Máy phát một cặp cực: một chu kì ứng với một vòng quay.")

# ═════════ Hình 5: máy biến áp ═════════
b = ""
# lõi thép kín (khung dày)
b += rect(110, 40, 180, 170, "none", "currentColor", 22, 4)
b += rect(110, 40, 180, 170, "none", GRAY, 18, 4)
# từ trường biến thiên trong lõi (nét đứt, khép kín)
b += field_path("M110,72 L110,40 L290,40 L290,210 L110,210 L110,178", (200, 40), (1, 0), BLUE, 1.8, "6 4", 11)
b += chevron(200, 210, -1, 0, BLUE, 1.8, 11)
# cuộn sơ cấp (trái) — nhiều vòng; thứ cấp (phải) — ít vòng
for i in range(8):
    y = 78 + i * 12
    b += line(94, y, 126, y + 6, ORG, 3)
for i in range(4):
    y = 96 + i * 18
    b += line(274, y, 306, y + 6, GRN, 3)
b += line(94, 78, 50, 78, ORG, 2.4) + line(94, 168, 50, 168, ORG, 2.4)
b += line(306, 102, 352, 102, GRN, 2.4) + line(306, 156, 352, 156, GRN, 2.4)
b += f'<circle cx="40" cy="123" r="16" fill="none" stroke="{ORG}" stroke-width="2"/>'
b += text(40, 129, "~", ORG, 22, "middle", "800")
b += line(40, 78, 50, 78, ORG, 2.4) + line(40, 78, 40, 107, ORG, 2.4) + line(40, 139, 40, 168, ORG, 2.4) + line(40, 168, 50, 168, ORG, 2.4)
# đèn (tải)
b += f'<circle cx="362" cy="129" r="14" fill="none" stroke="{GRN}" stroke-width="2"/>'
b += line(352, 119, 372, 139, GRN, 1.6) + line(372, 119, 352, 139, GRN, 1.6)
b += line(352, 102, 362, 102, GRN, 2.4) + line(362, 102, 362, 115, GRN, 2.4) + line(362, 143, 362, 156, GRN, 2.4) + line(352, 156, 362, 156, GRN, 2.4)
b += text(24, 244, "cam: cuộn sơ cấp N₁, nối nguồn xoay chiều U₁", ORG, 15, "start", "700")
b += text(24, 266, "xanh lá: cuộn thứ cấp N₂, nối tải U₂", GRN, 15, "start", "700")
b += text(24, 288, "xanh: từ trường biến thiên trong lõi", BLUE, 15, "start", "700")
b += text(200, 132, "lõi thép", "currentColor", 15, "middle", "700")
fig5 = wrap("0 22 400 278",
            "Máy biến áp: lõi thép kín, cuộn sơ cấp nhiều vòng nối nguồn xoay chiều, cuộn thứ cấp ít vòng nối bóng đèn, từ trường biến thiên chạy vòng trong lõi",
            b, "Hình 5. Máy biến áp (ở đây là máy hạ áp vì N₂&nbsp;&lt;&nbsp;N₁).<br>Hai cuộn không nối điện với nhau.<br>Năng lượng truyền sang cuộn thứ cấp nhờ từ trường biến thiên trong lõi.")

# ═════════ Hình 6: sơ đồ truyền tải nhiều cấp ═════════
b = ""
boxes = [("Nhà máy: máy phát", "currentColor"), ("Trạm tăng áp", ORG), ("Trạm hạ áp khu vực", GRN),
         ("Máy hạ áp khu dân cư", GRN), ("Nhà em: ổ cắm", BLUE)]
links = [("10–20 kV", "currentColor"), ("dây cao thế 500, 220, 110 kV", RED), ("dây trung thế 22 kV", "currentColor"),
         ("0,4 kV (220 V mỗi pha)", "currentColor")]
BH, GAP, BX, BW = 34, 46, 40, 200
y = 20
for i, (name, col) in enumerate(boxes):
    b += rect(BX, y, BW, BH, GRAY if col == "currentColor" else "none", col, 2, 8)
    b += text(BX + BW / 2, y + 23, name, col, 15, "middle", "700")
    if i < len(links):
        lab, lc = links[i]
        x = BX + 30
        b += line(x, y + BH, x, y + BH + GAP - 2, lc, 3 if lc == RED else 2) + chevron(x, y + BH + GAP - 2, 0, 1, lc, 2, 9)
        b += text(x + 14, y + BH + GAP / 2 + 6, lab, lc, 15, "start", "700")
    y += BH + GAP
fig6 = wrap("0 10 400 384",
            "Sơ đồ truyền tải điện từ nhà máy: máy phát, trạm tăng áp, đường dây cao thế 500, 220 hoặc 110 kV, trạm hạ áp, đường dây 22 kV, máy hạ áp khu dân cư, ổ cắm 220 V",
            b, "Hình 6. Điện đi xa ở hiệu điện thế rất cao, tới gần nơi dùng mới hạ dần.<br>Mỗi lần đổi hiệu điện thế là một máy biến áp.")

# ═════════ ghi theory.html ═════════
src = open(os.path.join(HERE, "theory.src.html"), encoding="utf8").read()
figs = (fig1, fig2, fig3, fig4, fig5, fig6)
for n, f in enumerate(figs, 1):
    assert src.count(f"<!--FIG{n}-->") == 1, n
    src = src.replace(f"<!--FIG{n}-->", f)
pos = [src.find(f"Hình {n}.") for n in range(1, len(figs) + 1)]
assert pos == sorted(pos), "số hình phải theo thứ tự xuất hiện"
src = src.replace("__PHUT__", str(PHUT))
assert "$" not in "".join(figs), "không để $…$ trong SVG"
open(os.path.join(HERE, "theory.html"), "w", encoding="utf8").write(src)
print("ok", len(src))
