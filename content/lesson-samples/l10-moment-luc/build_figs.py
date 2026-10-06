"""Sinh 5 hình SVG cho bài 'Moment lực. Cân bằng của vật rắn' (lesson 66) và thay mốc <!--FIGn--> trong
theory.src.html -> theory.html. Chạy: python3 build_figs.py (từ thư mục bài hoặc gốc repo).
Tự kiểm bằng toạ độ: nhãn không chồng nhau, không vượt viewBox, không bị nét vẽ cắt xuyên; cánh tay đòn tính lại
bằng khoảng cách vuông góc từ trục tới đường tác dụng; chiều quay suy từ dấu moment (r × F)."""
import math, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import RED, BLUE, ORG, GRN, wrap  # noqa: E402

COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}
LABELS = []   # (fig, x0, y0, x1, y1, text)
SEGS = []     # (fig, x1, y1, x2, y2) nét vẽ để kiểm nhãn bị cắt
BAD = []
CUR = {"fig": 0}


def defs(p):
    out = "<defs>"
    for n, c in COL.items():
        out += (f'<marker id="{p}-{n}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="12" markerHeight="12" '
                f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
    return out + "</defs>"


def seg(x1, y1, x2, y2):
    SEGS.append((CUR["fig"], x1, y1, x2, y2))


def arrow(p, c, x1, y1, x2, y2, w=3, dash=""):
    seg(x1, y1, x2, y2)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{COL[c]}" stroke-width="{w}"{d} '
            f'marker-end="url(#{p}-{c})"/>')


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1, track=True):
    if track:
        seg(x1, y1, x2, y2)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def sub(base, s):
    return f'{base}<tspan baseline-shift="sub" font-size="12">{s}</tspan>'


def text(x, y, s, c="currentColor", size=14, anchor="start", weight="700", italic=False):
    plain = re.sub(r"<[^>]+>", "", s)
    w = 0.58 * size * len(plain)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
    LABELS.append((CUR["fig"], x0, y - 0.75 * size, x0 + w, y + 0.2 * size, plain))
    it = ' font-style="italic" font-family="serif"' if italic else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}"{it}>{s}</text>')


def arc_arrow(p, c, cx, cy, r, a0, a1, w=2.6):
    """Cung tròn từ góc a0 tới a1 (độ, hệ SVG: y hướng xuống). a1 > a0 => quay THUẬN chiều kim đồng hồ trên màn hình."""
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    sweep = 1 if a1 > a0 else 0
    large = 1 if abs(a1 - a0) > 180 else 0
    return (f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 {large} {sweep} {x1:.1f},{y1:.1f}" fill="none" stroke="{COL[c]}" '
            f'stroke-width="{w}" marker-end="url(#{p}-{c})"/>')


def moment_sign(ox, oy, ax, ay, fx, fy):
    """Dấu của r × F trong hệ SVG (y xuống): >0 nghĩa là quay THUẬN kim đồng hồ trên màn hình."""
    return (ax - ox) * fy - (ay - oy) * fx


def dist_point_line(px, py, ax, ay, ux, uy):
    """Khoảng cách từ điểm P tới đường thẳng qua A, hướng (ux, uy)."""
    n = math.hypot(ux, uy)
    return abs((px - ax) * uy - (py - ay) * ux) / n


def expect(cond, msg):
    if not cond:
        BAD.append(msg)


VB = {}

# ---------------- Hình 1: búa nhổ đinh, hai chỗ cầm (mở bài) ----------------
CUR["fig"] = 1
VB[1] = (440, 150)
PXM = 1000                       # 1000 px cho 1 m (cán búa)
PXN = 80 / 300                   # 300 N -> 80 px
OX1, OY1 = 60, 110
b = defs("f1")
hexa = " ".join(f"{OX1 + 22*math.cos(math.radians(30 + 60*k)):.1f},{OY1 + 22*math.sin(math.radians(30 + 60*k)):.1f}" for k in range(6))
b += f'<rect x="{OX1-24}" y="{OY1-20}" width="48" height="40" rx="5" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2.4"/>'
b += f'<circle cx="{OX1}" cy="{OY1}" r="3.5" fill="currentColor"/>'
b += f'<rect x="{OX1+22}" y="{OY1-9}" width="{400-OX1-22}" height="18" rx="9" fill="rgba(148,163,184,.18)" stroke="currentColor" stroke-width="2.2"/>'
seg(OX1 + 22, OY1 - 9, 400, OY1 - 9); seg(OX1 + 22, OY1 + 9, 400, OY1 + 9)
for who, dm, F, c in (("Minh", 0.08, 300, "r"), ("anh Tuấn", 0.30, 150, "b")):
    x = OX1 + dm * PXM
    L = F * PXN
    b += arrow("f1", c, x, OY1 - 9 - L - 2, x, OY1 - 9 - 2, 3.2)       # ấn xuống, đầu mũi chạm mặt trên cán
    sgn = moment_sign(OX1, OY1, x, OY1, 0, 1)
    expect(sgn > 0, f"Hình 1: lực của {who} phải làm quay thuận kim (nhổ đinh)")
b += text(OX1 + 0.08 * PXM + 8, OY1 - 9 - 300 * PXN + 12, "300 N", RED, 14, "start")
b += text(OX1 + 0.30 * PXM - 8, OY1 - 9 - 150 * PXN + 6, "150 N", BLUE, 14, "end")
b += arc_arrow("f1", "k", OX1, OY1, 34, -150, -40, 2.4)        # nhổ đinh: thuận kim
b += text(OX1 + 6, 50, "nhổ đinh", "currentColor", 13, "start", "600")
expect(-40 > -150, "Hình 1: cung nhổ đinh phải thuận kim")
expect(abs(300 * 0.08 - 24) < 1e-9 and abs(150 * 0.30 - 45) < 1e-9, "Hình 1: số moment")
fig1 = wrap(f"0 0 {VB[1][0]} {VB[1][1]}",
            "Búa nhổ đinh: Minh ấn 300 N sát đầu búa, anh Tuấn ấn 150 N ở cuối cán", b,
            "Hình 1. Minh ấn lực lớn (đỏ) sát đầu búa, anh Tuấn ấn lực nhỏ (xanh) ở cuối cán. Mũi tên vẽ tỉ lệ độ lớn lực.")

# ---------------- Hình 2: lực xiên — cánh tay đòn là khoảng cách tới GIÁ ----------------
CUR["fig"] = 2
VB[2] = (440, 272)
O2 = (60, 95)
R2 = 240                          # OA (px)
ALPHA = 30
A2 = (O2[0] + R2, O2[1])
u = (math.cos(math.radians(ALPHA)), -math.sin(math.radians(ALPHA)))   # hướng lực: lên-phải, hợp với cán 30°
FL = 90
F_end = (A2[0] + FL * u[0], A2[1] + FL * u[1])
t = (O2[0] - A2[0]) * u[0] + (O2[1] - A2[1]) * u[1]
H2 = (A2[0] + t * u[0], A2[1] + t * u[1])                             # chân đường vuông góc từ O
d_px = math.hypot(H2[0] - O2[0], H2[1] - O2[1])
expect(abs(d_px - R2 * math.sin(math.radians(ALPHA))) < 0.01, "Hình 2: d ≠ r sinα")
expect(abs(dist_point_line(*O2, *A2, *u) - d_px) < 0.01, "Hình 2: H không phải chân vuông góc")
b = defs("f2")
b += f'<rect x="{O2[0]-6}" y="{O2[1]-8}" width="{R2+30}" height="16" rx="8" fill="rgba(148,163,184,.18)" stroke="currentColor" stroke-width="2.2"/>'
seg(O2[0] - 6, O2[1] - 8, O2[0] + R2 + 24, O2[1] - 8); seg(O2[0] - 6, O2[1] + 8, O2[0] + R2 + 24, O2[1] + 8)
b += f'<circle cx="{O2[0]}" cy="{O2[1]}" r="5" fill="currentColor"/>'
b += f'<circle cx="{A2[0]}" cy="{A2[1]}" r="4" fill="{RED}"/>'
b += line(H2[0] - 25 * u[0], H2[1] - 25 * u[1], A2[0], A2[1], RED, 1.6, "6 5", .9)     # giá của lực (kéo dài)
b += arrow("f2", "r", A2[0], A2[1], *F_end, 3.2)
b += line(*O2, *H2, GRN, 2.6)
# dấu góc vuông tại H
n_ = ((O2[0] - H2[0]) / d_px, (O2[1] - H2[1]) / d_px)
k = 10
p1 = (H2[0] + k * n_[0], H2[1] + k * n_[1]); p3 = (H2[0] + k * u[0], H2[1] + k * u[1])
p2 = (p1[0] + k * u[0], p1[1] + k * u[1])
b += f'<path d="M{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} L{p3[0]:.1f},{p3[1]:.1f}" fill="none" stroke="{GRN}" stroke-width="1.6"/>'
# góc alpha giữa cán (hướng ra xa O) và lực, tại A
b += f'<path d="M{A2[0]+34:.1f},{A2[1]:.1f} A34,34 0 0 0 {A2[0]+34*u[0]:.1f},{A2[1]+34*u[1]:.1f}" fill="none" stroke="currentColor" stroke-width="1.5"/>'
b += text(A2[0] + 40, A2[1] - 6, "α", "currentColor", 15, "start", "700", True)
b += text(O2[0] - 2, O2[1] - 16, "O (trục)", "currentColor", 14, "start")
b += text(A2[0] - 4, A2[1] + 28, "A", RED, 14, "middle")
b += text(F_end[0] - 6, F_end[1] - 6, "F", RED, 16, "end", "700", True)
mx, my = (O2[0] + H2[0]) / 2, (O2[1] + H2[1]) / 2
b += text(mx - 10, my + 8, "d", GRN, 16, "end", "700", True)
b += text(150, O2[1] + 32, "r = OA", "currentColor", 14, "middle")
b += text(H2[0] + 26, H2[1] + 6, "giá của lực", RED, 13, "start", "600")
b += text(150, 262, "d = r·sinα", GRN, 15, "middle")
expect(moment_sign(*O2, *A2, *u) < 0, "Hình 2: lực lên-phải ở bên phải trục phải làm quay ngược kim")
fig2 = wrap(f"0 0 {VB[2][0]} {VB[2][1]}",
            "Lực F đặt tại A, xiên góc alpha với cán; kéo dài giá của lực, đoạn vuông góc từ trục O tới giá là cánh tay đòn d", b,
            "Hình 2. Kéo dài giá của lực (nét đứt đỏ), hạ vuông góc từ trục <em>O</em>: đoạn xanh lá là cánh tay đòn <em>d</em>, ngắn hơn <em>r</em> = <em>OA</em>.")

# ---------------- Hình 3: thước có trục ở giữa — quy tắc moment ----------------
CUR["fig"] = 3
VB[3] = (440, 270)
S3 = 5.5                         # px/cm
OX3, RY = 220, 110               # trục O, mặt trên thước ở RY-6
PN = 30                          # px/N
P1, D1, D2, F2 = 2.0, 15, 20, 1.52
b = defs("f3")
b += f'<rect x="{OX3-35*S3:.1f}" y="{RY-6}" width="{70*S3:.1f}" height="12" rx="2" fill="rgba(251,146,60,.18)" stroke="currentColor" stroke-width="2"/>'
seg(OX3 - 35 * S3, RY - 6, OX3 + 35 * S3, RY - 6); seg(OX3 - 35 * S3, RY + 6, OX3 + 35 * S3, RY + 6)
b += line(OX3, RY, OX3, RY + 120, "currentColor", 3)   # giá đỡ trục
b += line(OX3 - 30, RY + 120, OX3 + 30, RY + 120, "currentColor", 3)
b += f'<circle cx="{OX3}" cy="{RY}" r="5" fill="rgba(148,163,184,.35)" stroke="currentColor" stroke-width="2.4"/>'
b += text(OX3 + 10, RY + 36, "O", "currentColor", 15, "start", "700", True)
for dcm in (10, 15, 20, 30):
    x = OX3 + dcm * S3
    b += line(x, RY - 6, x, RY - 1, "currentColor", 1.4, track=False)
xl, xr = OX3 - D1 * S3, OX3 + D2 * S3
# trái: dây + quả nặng; mũi tên P1 đặt tại điểm treo trên thước, hướng xuống
b += line(xl, RY + 6, xl, RY + 96, "currentColor", 1.4, track=False)
b += f'<rect x="{xl-13:.1f}" y="{RY+96}" width="26" height="30" rx="3" fill="rgba(148,163,184,.35)" stroke="currentColor" stroke-width="2"/>'
b += arrow("f3", "r", xl, RY + 6, xl, RY + 6 + P1 * PN, 3.2)
b += text(xl + 10, RY + 6 + P1 * PN - 6, sub("P", "1"), RED, 15, "start", "700", True)
# phải: lực kế kéo thẳng đứng xuống
b += line(xr, RY + 6, xr, RY + 80, "currentColor", 1.4, track=False)
b += f'<rect x="{xr-10:.1f}" y="{RY+80}" width="20" height="58" rx="4" fill="rgba(56,189,248,.15)" stroke="currentColor" stroke-width="2"/>'
b += line(xr, RY + 138, xr, RY + 152, "currentColor", 1.6, track=False)
b += text(xr + 16, RY + 128, "lực kế", BLUE, 13, "start", "600")
b += arrow("f3", "b", xr, RY + 6, xr, RY + 6 + F2 * PN, 3.2)
b += text(xr - 10, RY + 6 + F2 * PN - 4, sub("F", "2"), BLUE, 15, "end", "700", True)
# kích thước trên thước
for x, lab, c in ((xl, sub("d", "1") + " = 15 cm", RED), (xr, sub("d", "2"), BLUE)):
    yy = RY - 30
    b += line(OX3, yy, x, yy, c, 1.6) + line(x, yy - 6, x, yy + 6, c, 1.6) + line(OX3, yy - 6, OX3, yy + 6, c, 1.6)
    b += text((OX3 + x) / 2, yy - 10, lab, c, 14, "middle")
b += text(18, 30, "quay ngược kim", RED, 13, "start", "600")
b += text(422, 30, "quay thuận kim", BLUE, 13, "end", "600")
expect(moment_sign(OX3, RY, xl, RY, 0, 1) < 0, "Hình 3: P1 bên trái hướng xuống phải quay ngược kim")
expect(moment_sign(OX3, RY, xr, RY, 0, 1) > 0, "Hình 3: F2 bên phải hướng xuống phải quay thuận kim")
fig3 = wrap(f"0 0 {VB[3][0]} {VB[3][1]}",
            "Thước quay quanh trục O ở giữa; quả nặng P1 = 2,0 N treo cách trục 15 cm bên trái, lực kế kéo thẳng đứng xuống bên phải cách trục d2", b,
            "Hình 3. Quả nặng <em>P</em><sub>1</sub> làm thước quay ngược kim, lực kế kéo <em>F</em><sub>2</sub> làm quay thuận kim. Hình vẽ lần đo <em>d</em><sub>2</sub> = 20 cm, <em>F</em><sub>2</sub> = 1,52 N.")
fig3 = fig3.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-moment-luc-02"', 1)

# ---------------- Hình 4: ngẫu lực trên vô lăng ----------------
CUR["fig"] = 4
VB[4] = (440, 290)
CX4, CY4, R4 = 220, 140, 90
FL4 = 64
b = defs("f4")
b += f'<circle cx="{CX4}" cy="{CY4}" r="{R4}" fill="none" stroke="currentColor" stroke-width="7" opacity=".55"/>'
b += line(CX4 - R4, CY4, CX4 + R4, CY4, "currentColor", 3, "", .45, track=False)
b += line(CX4, CY4, CX4, CY4 + R4, "currentColor", 3, "", .45, track=False)
b += f'<circle cx="{CX4}" cy="{CY4}" r="14" fill="rgba(148,163,184,.3)" stroke="currentColor" stroke-width="2"/>'
xL, xR = CX4 - R4, CX4 + R4
b += arrow("f4", "r", xL, CY4, xL, CY4 - FL4, 3.4)        # tay trái đẩy lên
b += arrow("f4", "r", xR, CY4, xR, CY4 + FL4, 3.4)        # tay phải kéo xuống
b += f'<circle cx="{xL}" cy="{CY4}" r="5" fill="{RED}"/><circle cx="{xR}" cy="{CY4}" r="5" fill="{RED}"/>'
b += text(xL - 10, CY4 - FL4 + 10, sub("F", "1"), RED, 16, "end", "700", True)
b += text(xR + 10, CY4 + FL4 - 4, sub("F", "2"), RED, 16, "start", "700", True)
# giá hai lực (nét đứt) và khoảng cách d
for x in (xL, xR):
    b += line(x, 30, x, 262, RED, 1.3, "5 5", .7, track=False)
yd = 258
b += line(xL, yd, xR, yd, GRN, 2) + line(xL, yd - 7, xL, yd + 7, GRN, 2) + line(xR, yd - 7, xR, yd + 7, GRN, 2)
b += text(CX4, yd - 8, "d", GRN, 16, "middle", "700", True)
b += arc_arrow("f4", "g", CX4, CY4, R4 + 22, -130, -50, 2.8)    # thuận kim
b += text(CX4, 22, "quay thuận kim", GRN, 13, "middle", "600")
expect(moment_sign(CX4, CY4, xL, CY4, 0, -1) > 0 and moment_sign(CX4, CY4, xR, CY4, 0, 1) > 0,
       "Hình 4: hai lực của ngẫu lực phải cùng làm quay thuận kim")
expect(abs((xR - xL) - 2 * R4) < 1e-9, "Hình 4: d phải bằng khoảng cách hai giá")
fig4 = wrap(f"0 0 {VB[4][0]} {VB[4][1]}",
            "Ngẫu lực trên vô lăng: tay trái đẩy lên, tay phải kéo xuống, hai lực bằng nhau; d là khoảng cách giữa hai giá", b,
            "Hình 4. Ngẫu lực: <em>F</em><sub>1</sub> = <em>F</em><sub>2</sub>, song song, ngược chiều. Cả hai cùng làm vô lăng quay thuận kim; <em>d</em> là khoảng cách giữa hai giá (nét đứt).")

# ---------------- Hình 5: bài toán mẫu — thanh gỗ trên giá đỡ ----------------
CUR["fig"] = 5
VB[5] = (440, 270)
SM = 300                          # px/m
AX5, BY = 40, 120
PN5 = 1.5                         # px/N
OA, L5, P_bar = 0.4, 1.2, 40.0
P1_5 = P_bar * (L5 / 2 - OA) / OA
N5 = P1_5 + P_bar
xA, xB, xO, xG = AX5, AX5 + L5 * SM, AX5 + OA * SM, AX5 + L5 / 2 * SM
expect(abs(P1_5 - 20) < 1e-9 and abs(N5 - 60) < 1e-9, "Hình 5: P1 = 20 N, N = 60 N")
expect(abs(N5 * OA - P_bar * L5 / 2) < 1e-9, "Hình 5: kiểm moment quanh A")
b = defs("f5")
b += f'<rect x="{xA}" y="{BY-6}" width="{L5*SM}" height="12" fill="rgba(148,163,184,.3)" stroke="currentColor" stroke-width="2"/>'
seg(xA, BY - 6, xB, BY - 6); seg(xA, BY + 6, xB, BY + 6)
b += f'<path d="M{xO},{BY+6} L{xO-16},{BY+34} H{xO+16} z" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2"/>'
b += arrow("f5", "b", xO, BY - 6, xO, BY - 6 - N5 * PN5, 3.2)
b += arrow("f5", "r", xA + 1, BY + 6, xA + 1, BY + 6 + P1_5 * PN5, 3.2)
b += arrow("f5", "o", xG, BY + 6, xG, BY + 6 + P_bar * PN5, 3.2)
b += f'<circle cx="{xG}" cy="{BY}" r="3.5" fill="currentColor"/>'
b += text(xO + 10, BY - 6 - N5 * PN5 + 12, "N = ?", BLUE, 14, "start")
b += text(xA + 10, BY + 6 + P1_5 * PN5 + 2, sub("P", "1") + " = ?", RED, 14, "start")
b += text(xG + 10, BY + 6 + P_bar * PN5 - 4, "P = 40 N", ORG, 14, "start")
for x, lab in ((xA, "A"), (xB, "B")):
    b += text(x, BY - 14, lab, "currentColor", 15, "middle")
b += text(xO - 22, BY + 30, "O", "currentColor", 15, "end", "700", True)
b += text(xG, BY - 14, "G", "currentColor", 15, "middle")
yd5 = 226
b += line(xA, yd5, xG, yd5, "currentColor", 1.5)
for x in (xA, xO, xG):
    b += line(x, yd5 - 6, x, yd5 + 6, "currentColor", 1.5)
b += text((xA + xO) / 2, yd5 + 22, "0,4 m", "currentColor", 14, "middle")
b += text((xO + xG) / 2, yd5 + 22, "0,2 m", "currentColor", 14, "middle")
expect(abs((xO - xA) / SM - 0.4) < 1e-9 and abs((xG - xO) / SM - 0.2) < 1e-9, "Hình 5: thước đo khoảng cách")
expect(moment_sign(xO, BY, xA, BY, 0, 1) < 0 and moment_sign(xO, BY, xG, BY, 0, 1) > 0,
       "Hình 5: P1 ở A quay ngược kim, P ở G quay thuận kim")
fig5 = wrap(f"0 0 {VB[5][0]} {VB[5][1]}",
            "Thanh gỗ AB dài 1,2 m kê trên giá đỡ O cách A 0,4 m; trọng lượng 40 N đặt tại trung điểm G; túi gạo P1 treo ở A; lực giá đỡ N hướng lên", b,
            "Hình 5. Ba lực lên thanh: <em>P</em><sub>1</sub> (túi gạo, ở <em>A</em>), <em>P</em> (trọng lượng thanh, ở <em>G</em>), <em>N</em> (giá đỡ, ở <em>O</em>). Mũi tên vẽ tỉ lệ độ lớn lực.")
fig5 = fig5.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-moment-luc-04"', 1)


# ---------------- Kiểm toạ độ nhãn ----------------
def seg_hits_box(x1, y1, x2, y2, bx0, by0, bx1, by1):
    """Liang–Barsky: đoạn thẳng có đi qua túi gạo không."""
    dx, dy = x2 - x1, y2 - y1
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x1 - bx0), (dx, bx1 - x1), (-dy, y1 - by0), (dy, by1 - y1)):
        if p == 0:
            if q < 0:
                return False
        else:
            r = q / p
            if p < 0:
                t0 = max(t0, r)
            else:
                t1 = min(t1, r)
            if t0 > t1:
                return False
    return True


for i, (f, x0, y0, x1, y1, s) in enumerate(LABELS):
    W, H = VB[f]
    if x0 < 2 or y0 < 2 or x1 > W - 2 or y1 > H - 2:
        BAD.append(f"Hình {f}: nhãn '{s}' vượt viewBox ({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f})")
    for g, a0, b0, a1, b1, t in LABELS[i + 1:]:
        if g == f and x0 < a1 and a0 < x1 and y0 < b1 and b0 < y1:
            BAD.append(f"Hình {f}: nhãn '{s}' chồng '{t}'")
    for g, sx1, sy1, sx2, sy2 in SEGS:
        if g == f and seg_hits_box(sx1, sy1, sx2, sy2, x0 + 1, y0 + 1, x1 - 1, y1 - 1):
            BAD.append(f"Hình {f}: nhãn '{s}' bị nét ({sx1:.0f},{sy1:.0f})-({sx2:.0f},{sy2:.0f}) cắt")
print("\n".join(BAD) if BAD else "kiểm toạ độ: ok")

src = (HERE / "theory.src.html").read_text(encoding="utf8")
figs = [fig1, fig2, fig3, fig4, fig5]
order = [int(n) for n in re.findall(r"<!--FIG(\d)-->", src)]
assert order == sorted(order) == list(range(1, len(figs) + 1)), order
for n, f in enumerate(figs, 1):
    assert f"Hình {n}." in f, n
    src = src.replace(f"<!--FIG{n}-->", f)

lint = HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = HERE / "theory.html"
out.write_text(src.replace("__PHUT__", "?"), encoding="utf8")
r = subprocess.run([sys.executable, str(lint), str(out), "--json"], capture_output=True, text=True)
m = re.search(r'"phut"\s*:\s*([\d.]+)', r.stdout) or re.search(r'"minutes"\s*:\s*([\d.]+)', r.stdout)
phut = round(float(m.group(1))) if m else None
if phut is None:
    print("KHÔNG đọc được số phút từ lint_do_dai:", r.stdout[:300])
    phut = "?"
out.write_text(src.replace("__PHUT__", str(phut)), encoding="utf8")
print("ok", len(src), "ký tự; phút =", phut)
sys.exit(1 if BAD else 0)
