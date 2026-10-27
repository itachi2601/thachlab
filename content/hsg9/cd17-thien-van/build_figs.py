"""CĐ17 Thiên văn (bài 178): sinh 6 hình SVG, thay <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được).
Chạy: python3 content/hsg9/cd17-thien-van/build_figs.py
Số liệu các quiz được kiểm bằng assert ở cuối file (cùng quy ước với tinh.py)."""
import os, sys
from math import pi, sin, cos, tan, atan, radians, degrees, hypot, sqrt
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "soan-bai-ly-thuyet-tuong-tac", "scripts"))
from svg_lib import RED, BLUE, ORG, GRN, text, wrap, chevron
from svg_lib import text as _text
# Màu CHỮ đậm cho nền sáng (giống CĐ14); khối hình vẫn giữ màu svg_lib.
_TXT = {"#fbbf24": "#b45309", "#fb923c": "#c2410c", "#38bdf8": "#0369a1", "#34d399": "#047857", "#f87171": "#b91c1c"}
def text(x, y, s, c="currentColor", *a, **k):
    return _text(x, y, s, _TXT.get(c, c), *a, **k)

PHUT = 18          # theo lint_do_dai.py (17,9 phút)
SUN = "#fbbf24"
LIT = "#fde047"
DARK = "#475569"
SHADE = "rgba(100,116,139,.85)"
PEN = "rgba(148,163,184,.22)"
KTL = "<em>Hình không theo tỉ lệ.</em>"


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def circ(x, y, r, fill="none", c="currentColor", w=1.6, op=1):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{c}" stroke-width="{w}" opacity="{op}"/>'


def poly(pts, fill, c="none", w=0):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{p}" fill="{fill}" stroke="{c}" stroke-width="{w}"/>'


def path(pts, c="currentColor", w=2, dash="", close=False):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + (" Z" if close else "")
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}"{da} stroke-linejoin="round"/>'


def ray(x1, y1, x2, y2, c=SUN, w=2):
    """Tia sáng: nét liền, đầu V ở giữa tia."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    return line(x1, y1, x2, y2, c, w) + chevron(mx, my, x2 - x1, y2 - y1, c, w, 9)


def moon_lit_half(x, y, r, sun_dir=(-1, 0)):
    """Mặt Trăng: nửa hướng về Mặt Trời sáng (vẽ nhìn từ trên xuống)."""
    ux, uy = sun_dir
    ang = degrees(atan2(uy, ux))
    a1, a2 = radians(ang - 90), radians(ang + 90)
    p1 = (x + r * cos(a1), y + r * sin(a1))
    p2 = (x + r * cos(a2), y + r * sin(a2))
    s = circ(x, y, r, DARK, "currentColor", 1.2)
    s += (f'<path d="M{p1[0]:.1f},{p1[1]:.1f} A{r},{r} 0 0 1 {p2[0]:.1f},{p2[1]:.1f} Z" fill="{LIT}" stroke="none"/>')
    return s + circ(x, y, r, "none", "currentColor", 1.2)


from math import atan2


def moon_face(cx, cy, r, e):
    """Hình dạng trăng nhìn từ bán cầu Bắc, góc lệch e (độ) tính từ trăng non. Trăng đầu tháng sáng bên phải."""
    e = e % 360
    s = circ(cx, cy, r, DARK, "currentColor", 1.2)
    if e == 0:
        return s
    if e == 180:
        return circ(cx, cy, r, LIT, "currentColor", 1.2)
    rx = abs(r * cos(radians(e)))
    top, bot = (cx, cy - r), (cx, cy + r)
    if e < 180:   # sáng bên phải
        first = f"A{r},{r} 0 0 1 {bot[0]:.1f},{bot[1]:.1f}"
        sweep = 0 if e < 90 else 1
    else:         # sáng bên trái
        first = f"A{r},{r} 0 0 0 {bot[0]:.1f},{bot[1]:.1f}"
        sweep = 1 if e > 270 else 0
    term = f"L{top[0]:.1f},{top[1]:.1f}" if abs(e % 180 - 90) < 1e-9 else f"A{rx:.2f},{r} 0 0 {sweep} {top[0]:.1f},{top[1]:.1f}"
    s += f'<path d="M{top[0]:.1f},{top[1]:.1f} {first} {term} Z" fill="{LIT}" stroke="none"/>'
    return s + circ(cx, cy, r, "none", "currentColor", 1.2)


# ═════════ Hình 1: pha Mặt Trăng ═════════
EX, EY, R = 222, 172, 116
b = ""
for y in (70, 120, 172, 224, 274):                      # tia Mặt Trời từ trái sang
    b += ray(12, y, 64, y)
b += text(12, 30, "ánh sáng", SUN, 15, "start", "700")
b += text(12, 48, "Mặt Trời", SUN, 15, "start", "700")
b += circ(EX, EY, R, "none", "currentColor", 1.4, .6).replace('opacity', 'stroke-dasharray="5 5" opacity')
# chiều quay quanh Trái Đất (ngược kim đồng hồ khi nhìn từ phía Bắc)
ta = radians(200)
b += chevron(EX + R * cos(ta), EY - R * sin(ta), -sin(ta), -cos(ta), "currentColor", 2, 11)
# Trái Đất: nửa trái sáng
b += circ(EX, EY, 24, "rgba(56,189,248,.35)", BLUE, 1.8)
b += f'<path d="M{EX},{EY-24} A24,24 0 0 1 {EX},{EY+24} Z" fill="rgba(15,23,42,.55)" stroke="none"/>'
b += circ(EX, EY, 24, "none", BLUE, 1.8)
b += text(EX, EY + 44, "Trái Đất", BLUE, 15, "middle", "700")
for k in range(8):
    a = radians(180 + 45 * k)                            # k=0: trăng non (phía Mặt Trời); đi ngược kim đồng hồ
    mx, my = EX + R * cos(a), EY - R * sin(a)
    b += moon_lit_half(mx, my, 13)
    lx, ly = EX + (R + 27) * cos(a), EY - (R + 27) * sin(a)
    b += text(round(lx, 1), round(ly + 5, 1), str(k + 1), "currentColor", 15, "middle", "700")
# dải hình dạng nhìn thấy
Y0 = 376
b += text(210, Y0 - 32, "Nhìn từ Việt Nam:", "currentColor", 15, "middle", "700")
for k in range(8):
    cx = 34 + 50 * k
    b += moon_face(cx, Y0, 17, 45 * k)
    b += text(cx, Y0 + 38, str(k + 1), "currentColor", 15, "middle", "700")
fig1 = wrap("0 0 420 424", "Tám vị trí của Mặt Trăng trên quỹ đạo quanh Trái Đất, nửa hướng về Mặt Trời luôn sáng; hàng dưới là hình dạng nhìn thấy từ Việt Nam ở mỗi vị trí",
            b, "Hình 1. Mặt Trăng luôn sáng nửa hướng về Mặt Trời (nhìn từ phía cực Bắc).<br>" + KTL +
            "<br>1: không trăng.<br>2: lưỡi liềm đầu tháng.<br>3: thượng huyền.<br>4: trăng khuyết (gần tròn).<br>5: trăng tròn.<br>6: trăng khuyết (gần tròn).<br>7: hạ huyền.<br>8: lưỡi liềm cuối tháng.")

# ═════════ Hình 2: quỹ đạo Mặt Trăng nghiêng — mùa thực ═════════
SX, SY, ORX, F = 210, 150, 165, 0.42
INC = radians(-32)            # vẽ phóng đại (thật ~5°)
NODE = (1 / sqrt(2), 1 / sqrt(2))      # hướng giao tuyến (cố định trong không gian)
PERP = (-1 / sqrt(2), 1 / sqrt(2))
b = ""
pts = [(SX + ORX * cos(radians(t)), SY + F * ORX * sin(radians(t))) for t in range(0, 361, 6)]
b += path(pts, "currentColor", 1.3, "5 5")
b += circ(SX, SY, 17, SUN, ORG, 1.6)
b += text(SX, SY + 36, "Mặt Trời", ORG, 15, "middle", "700")


def scr(wx, wy, wz=0.0, ox=SX, oy=SY):
    return ox + wx, oy + F * wy - 0.9 * wz


labels = {45: ("mùa thực", GRN, 1), 225: ("mùa thực", GRN, -1), 135: ("không có thực", RED, 1), 315: ("không có thực", RED, -1)}
for th, (lab, col, side) in labels.items():
    ew = (ORX * cos(radians(th)), ORX * sin(radians(th)))
    ex, ey = scr(*ew)
    rm = 44
    up, dn = [], []
    for t in range(0, 361, 6):
        tr = radians(t)
        wx = rm * cos(tr) * NODE[0] + rm * sin(tr) * cos(INC) * PERP[0]
        wy = rm * cos(tr) * NODE[1] + rm * sin(tr) * cos(INC) * PERP[1]
        wz = rm * sin(tr) * sin(INC)
        (up if wz >= -1e-9 else dn).append(scr(wx, wy, wz, ex, ey))
    # nửa trên mặt phẳng: nét liền; nửa dưới: nét đứt
    up_pts = [scr(rm * cos(radians(t)) * NODE[0] + rm * sin(radians(t)) * cos(INC) * PERP[0],
                  rm * cos(radians(t)) * NODE[1] + rm * sin(radians(t)) * cos(INC) * PERP[1],
                  rm * sin(radians(t)) * sin(INC), ex, ey) for t in range(180, 361, 6)]
    dn_pts = [scr(rm * cos(radians(t)) * NODE[0] + rm * sin(radians(t)) * cos(INC) * PERP[0],
                  rm * cos(radians(t)) * NODE[1] + rm * sin(radians(t)) * cos(INC) * PERP[1],
                  rm * sin(radians(t)) * sin(INC), ex, ey) for t in range(0, 181, 6)]
    b += path(dn_pts, "currentColor", 1.6, "4 3")
    b += path(up_pts, "currentColor", 2)
    for t in (0, 180):        # hai điểm nút
        nx, ny = scr(rm * cos(radians(t)) * NODE[0], rm * cos(radians(t)) * NODE[1], 0, ex, ey)
        b += circ(nx, ny, 2.6, "currentColor", "currentColor", 1)
    # vị trí trăng non: hướng về Mặt Trời
    sd = (-ew[0] / ORX, -ew[1] / ORX)
    cu = sd[0] * NODE[0] + sd[1] * NODE[1]
    cv = sd[0] * PERP[0] + sd[1] * PERP[1]
    t0 = atan2(cv, cu)
    wx = rm * cos(t0) * NODE[0] + rm * sin(t0) * cos(INC) * PERP[0]
    wy = rm * cos(t0) * NODE[1] + rm * sin(t0) * cos(INC) * PERP[1]
    wz = rm * sin(t0) * sin(INC)
    mx, my = scr(wx, wy, wz, ex, ey)
    px, py = scr(wx, wy, 0, ex, ey)
    if abs(wz) > 2:
        b += line(mx, my, px, py, "currentColor", 1.2, "2 3")
        b += circ(px, py, 1.8, "currentColor", "currentColor", 1, .7)
    b += circ(mx, my, 6, DARK, "currentColor", 1.4)
    b += circ(ex, ey, 9, "rgba(56,189,248,.45)", BLUE, 1.6)
    b += text(round(ex, 1), round(ey + side * 46 + (5 if side > 0 else 0), 1), lab, col, 15, "middle", "700")
fig2 = wrap("36 34 348 236", "Trái Đất ở bốn vị trí quanh Mặt Trời, mỗi vị trí có quỹ đạo Mặt Trăng nghiêng; giao tuyến giữ hướng cố định nên chỉ ở hai vị trí giao tuyến chĩa vào Mặt Trời mới có thực",
            b, "Hình 2. Quỹ đạo Mặt Trăng nghiêng so với quỹ đạo Trái Đất, giao tuyến (nối hai chấm nhỏ) giữ hướng cố định.<br>" + KTL +
            "<br>Chấm xanh: Trái Đất ở bốn vị trí trong năm." +
            "<br>Góc nghiêng vẽ phóng đại, thật chỉ khoảng 5°.<br>Nét liền: nửa quỹ đạo ở phía trên; nét đứt: phía dưới.<br>Chấm xám: Mặt Trăng lúc trăng non; vạch chấm nối xuống mặt phẳng quỹ đạo Trái Đất cho thấy nó lệch lên hay xuống.")

# ═════════ Hình 3: nhật thực — bóng Mặt Trăng ═════════
YA = 130
S3 = (42, YA, 34)           # Mặt Trời (x, y, r)
M3 = (236, YA, 16)          # Mặt Trăng
E3 = (548, YA, 186)         # Trái Đất (mép trái x = 362)


def hit_earth(p, q, E):
    """Giao của tia p→q (kéo dài) với đường tròn Trái Đất, điểm gần nhất phía trước q."""
    (x1, y1), (x2, y2) = p, q
    dx, dy = x2 - x1, y2 - y1
    fx, fy = x1 - E[0], y1 - E[1]
    A = dx * dx + dy * dy
    B = 2 * (fx * dx + fy * dy)
    C = fx * fx + fy * fy - E[2] ** 2
    t = (-B - sqrt(B * B - 4 * A * C)) / (2 * A)
    return (x1 + t * dx, y1 + t * dy)


sT, sB = (S3[0], S3[1] - S3[2]), (S3[0], S3[1] + S3[2])
mT, mB = (M3[0], M3[1] - M3[2]), (M3[0], M3[1] + M3[2])
# chóp nón tối (giao hai tia mép–mép cùng phía)
apx = M3[0] + M3[2] * (M3[0] - S3[0]) / (S3[2] - M3[2])
assert E3[0] - E3[2] < apx, "chóp nón phải chạm đất (nhật thực toàn phần)"
uT, uB = hit_earth(sT, mT, E3), hit_earth(sB, mB, E3)
pT, pB = hit_earth(sB, mT, E3), hit_earth(sT, mB, E3)
b = ""
b += circ(*E3, "rgba(56,189,248,.25)", BLUE, 2)
b += poly([mT, pT, pB, mB], PEN)
b += poly([mT, uT, uB, mB], SHADE)
b += circ(*S3, SUN, ORG, 1.6)
for p, q in ((sT, mT), (sB, mB)):
    b += line(*p, *hit_earth(p, q, E3), ORG, 1.3)
for p, q in ((sB, mT), (sT, mB)):
    b += line(*p, *hit_earth(p, q, E3), ORG, 1.3, "5 4")
b += circ(*M3, DARK, "currentColor", 1.4)
b += text(S3[0], S3[1] + S3[2] + 24, "Mặt Trời", ORG, 15, "middle", "700")
b += text(M3[0], M3[1] - 30, "Mặt Trăng", "currentColor", 15, "middle", "700")
b += text(352, 44, "Trái Đất", BLUE, 15, "end", "700")
ux0 = (uT[0] + uB[0]) / 2
b += circ(ux0, YA, 4.5, "#0f172a", "currentColor", 1.4)
b += line(ux0 - 3, YA + 6, 300, 208, "currentColor", 1.1, "", .8)
b += text(230, 226, "vùng tối:", "currentColor", 15, "start", "700")
b += text(230, 244, "thấy toàn phần", "currentColor", 15, "start", "600")
b += line(pB[0] - 6, pB[1] - 10, 150, 200, "currentColor", 1.1, "", .8)
b += text(60, 216, "vùng nửa tối:", "currentColor", 15, "start", "700")
b += text(60, 234, "thấy một phần", "currentColor", 15, "start", "600")
fig3 = wrap("0 10 420 250", "Nhật thực: Mặt Trăng nằm giữa Mặt Trời và Trái Đất; tia mép–mép tạo nón bóng tối có chóp vừa chạm mặt đất và vùng nửa tối rộng hơn",
            b, "Hình 3. Nhật thực: bóng của Mặt Trăng rơi lên Trái Đất.<br>" + KTL +
            "<br>Nét liền: tia mép–mép cùng phía, giới hạn vùng tối.<br>Nét đứt: tia mép–mép chéo, giới hạn vùng nửa tối.<br>Mặt Trăng ở xa hơn một chút thì chóp nón không chạm đất: nhật thực hình khuyên.")

# ═════════ Hình 4: nguyệt thực — bóng Trái Đất ═════════
S4 = (46, YA, 40)
E4 = (196, YA, 34)
M4 = (362, YA, 10)
apx4 = E4[0] + E4[2] * (E4[0] - S4[0]) / (S4[2] - E4[2])
X4 = 410


def at_x(p, q, x):
    (x1, y1), (x2, y2) = p, q
    return (x, y1 + (y2 - y1) * (x - x1) / (x2 - x1))


sT, sB = (S4[0], S4[1] - S4[2]), (S4[0], S4[1] + S4[2])
eT, eB = (E4[0], E4[1] - E4[2]), (E4[0], E4[1] + E4[2])
uT, uB = at_x(sT, eT, X4), at_x(sB, eB, X4)
pT, pB = at_x(sB, eT, X4), at_x(sT, eB, X4)
half_u = (uB[1] - uT[1]) / 2 * (apx4 - M4[0]) / (apx4 - X4)
assert M4[2] * 2 < half_u * 2, "Mặt Trăng phải nằm gọn trong vùng tối"
b = ""
b += poly([eT, pT, pB, eB], PEN)
b += poly([eT, uT, uB, eB], SHADE)
b += circ(*S4, SUN, ORG, 1.6)
for p, q in ((sT, eT), (sB, eB)):
    b += line(*p, *at_x(p, q, X4), ORG, 1.3)
for p, q in ((sB, eT), (sT, eB)):
    b += line(*p, *at_x(p, q, X4), ORG, 1.3, "5 4")
b += circ(*E4, BLUE, BLUE, 1.8)
b += circ(*M4, "#b45309", "currentColor", 1.4)
b += text(S4[0] + 4, S4[1] + S4[2] + 24, "Mặt Trời", ORG, 15, "start", "700")
b += text(E4[0], E4[1] + 5, "Trái Đất", "#0f172a", 15, "middle", "700")
b += text(M4[0], 80, "Mặt Trăng", "currentColor", 15, "middle", "700")
b += line(M4[0], 85, M4[0], M4[1] - M4[2] - 3, "currentColor", 1.1, "", .7)
b += text(238, 156, "vùng tối", "currentColor", 15, "start", "700")
fig4 = wrap("0 60 420 160", "Nguyệt thực: Trái Đất nằm giữa Mặt Trời và Mặt Trăng; Mặt Trăng đi vào vùng tối rộng của Trái Đất",
            b, "Hình 4. Nguyệt thực: Mặt Trăng đi vào bóng của Trái Đất.<br>" + KTL +
            "<br>Vùng tối ở quỹ đạo Mặt Trăng rộng gấp khoảng 2,7 lần Mặt Trăng.<br>Ai đang ở nửa Trái Đất ban đêm cũng thấy.")

# ═════════ Hình 5: góc cao Mặt Trời buổi trưa ═════════
OX, OY, RE5 = 160, 172, 112
PHI, DEL = 35.0, 10.0      # chỉ để vẽ (không ghi số lên hình)
aS, aA, aEq = 0.0, PHI - DEL, -DEL


def P(a, r=RE5):
    return (OX + r * cos(radians(a)), OY - r * sin(radians(a)))


b = ""
b += circ(OX, OY, RE5, "rgba(56,189,248,.18)", BLUE, 2)
q1, q2 = P(aEq + 180, RE5 + 14), P(aEq, RE5 + 14)
b += line(*q1, *q2, "currentColor", 1.4, "6 4", .8)
b += text(round(q1[0] + 26, 1), round(q1[1] - 8, 1), "xích đạo", "currentColor", 15, "start", "600")
for y in (OY - RE5 * sin(radians(aA)), OY, OY + 62):   # tia nắng song song từ phải sang
    xs = OX + sqrt(max(RE5 ** 2 - (y - OY) ** 2, 0))
    b += line(410, y, xs, y, SUN, 2) + chevron((410 + xs) / 2, y, -1, 0, SUN, 2, 9)
b += text(410, OY + 90, "tia nắng", SUN, 15, "end", "700")
A = P(aA)
S = P(aS)
b += line(OX, OY, *A, "currentColor", 1.6)
b += line(OX, OY, *S, "currentColor", 1.6)
Z = P(aA, RE5 + 70)
b += line(*A, *Z, "currentColor", 1.3, "4 4", .8)
b += text(round(Z[0] + 6, 1), round(Z[1] + 4, 1), "thiên đỉnh", "currentColor", 15, "start", "600")
tg = (sin(radians(aA)), cos(radians(aA)))       # tiếp tuyến tại A (hướng về phía Mặt Trời, xuống dưới trên màn hình)
H1 = (A[0] + 48 * tg[0], A[1] + 48 * tg[1])
H0 = (A[0] - 84 * tg[0], A[1] - 84 * tg[1])
b += line(*H0, *H1, GRN, 2)
b += text(round(H0[0] + 8, 1), round(H0[1] + 4, 1), "chân trời", GRN, 15, "start", "700")
# cung góc h tại A: từ hướng chân trời (về phía Mặt Trời) tới hướng tia (sang phải)
rh = 30
a_h0 = -(90 - aA)
arc = [(A[0] + rh * cos(radians(t)), A[1] - rh * sin(radians(t))) for t in [a_h0 + i * (0 - a_h0) / 20 for i in range(21)]]
b += path(arc, RED, 2)
mid = radians(a_h0 / 2)
b += text(round(A[0] + (rh + 14) * cos(mid), 1), round(A[1] - (rh + 14) * sin(mid) + 6, 1), "h", RED, 17, "middle", "700")
# cung góc ở tâm
rc = 46
arc = [(OX + rc * cos(radians(t)), OY - rc * sin(radians(t))) for t in [aS + i * (aA - aS) / 20 for i in range(21)]]
b += path(arc, ORG, 2)
b += f'<text x="{OX + 52:.1f}" y="{OY - 4:.1f}" fill="{_TXT[ORG]}" font-size="15" font-weight="700">φ − δ</text>'
b += circ(*A, 3.4, "currentColor", "currentColor", 1)
b += circ(*S, 3.4, "currentColor", "currentColor", 1)
b += text(round(A[0] + 8, 1), round(A[1] - 8, 1), "A", "currentColor", 16, "start", "700")
b += text(round(S[0] + 8, 1), round(S[1] + 24, 1), "S", "currentColor", 16, "start", "700")
b += circ(OX, OY, 2.6, "currentColor", "currentColor", 1)
b += text(OX - 8, OY + 20, "O", "currentColor", 15, "end", "700")
fig5 = wrap("0 20 420 290", "Mặt cắt Trái Đất với chùm tia nắng song song; tại điểm A vĩ độ phi, góc cao h giữa tia nắng và đường chân trời bằng 90 độ trừ góc ở tâm giữa A và điểm S nơi Mặt Trời đứng bóng",
            b, "Hình 5. Góc cao Mặt Trời buổi trưa tại A (vĩ độ φ).<br>S: nơi Mặt Trời đứng bóng hôm đó (vĩ độ δ).<br>Góc ở tâm AOS bằng |φ − δ|.<br>Chân trời vuông góc bán kính OA, nên h = 90° − |φ − δ|.")

# ═════════ Hình 6: Ngân Hà ═════════
GX, GY, GR = 210, 150, 120          # bán kính đĩa 50 000 ly ứng với 120 px
b = ""
b += circ(GX, GY, GR, "rgba(148,163,184,.10)", "currentColor", 1, .5)
for arm in range(4):
    base = arm * 90
    pts = []
    for i in range(0, 61):
        t = i / 60
        r = 22 + (GR - 26) * t
        a = radians(base + 25 + 200 * t)
        pts.append((GX + r * cos(a), GY - r * sin(a) * 0.9))
    b += path(pts, "rgba(148,163,184,.55)", 9)
b += (f'<ellipse cx="{GX}" cy="{GY}" rx="30" ry="11" transform="rotate(-25 {GX} {GY})" '
      f'fill="rgba(253,224,71,.55)" stroke="none"/>')
b += circ(GX, GY, 3, "currentColor", "currentColor", 1)
b += text(GX + 4, GY - 16, "tâm", "currentColor", 15, "start", "700")
rS = GR * 26_000 / 50_000
aSun = radians(201)
sx, sy = GX + rS * cos(aSun), GY - rS * sin(aSun) * 0.9
b += circ(sx, sy, 5, SUN, ORG, 1.6)
b += line(sx - 4, sy + 6, 70, 236, ORG, 1.2, "", .8)
b += text(18, 254, "Mặt Trời", ORG, 15, "start", "700")
b += text(18, 272, "(cách tâm ~26 000 ly)", ORG, 15, "start", "600")
b += line(GX - GR, 296, GX + GR, 296, "currentColor", 1.4)
b += chevron(GX - GR, 296, -1, 0, "currentColor", 1.4, 9) + chevron(GX + GR, 296, 1, 0, "currentColor", 1.4, 9)
b += text(GX + 40, 316, "~100 000 ly", "currentColor", 15, "start", "700")
# nhìn ngang
YS = 358
b += f'<ellipse cx="{GX}" cy="{YS}" rx="{GR}" ry="5" fill="rgba(148,163,184,.45)" stroke="none"/>'
b += f'<ellipse cx="{GX}" cy="{YS}" rx="26" ry="15" fill="rgba(253,224,71,.55)" stroke="none"/>'
b += circ(GX - rS, YS, 4, SUN, ORG, 1.4)
b += text(GX, YS + 36, "Nhìn ngang: đĩa mỏng, Mặt Trời nằm trong đĩa", "currentColor", 15, "middle", "600")
fig6 = wrap("0 20 420 384", "Sơ đồ Ngân Hà nhìn từ trên xuống: thanh chắn ở tâm, bốn nhánh xoắn, Mặt Trời ở một nhánh cách tâm khoảng 26 nghìn năm ánh sáng; bên dưới là hình nhìn ngang đĩa mỏng",
            b, "Hình 6. Ngân Hà nhìn từ trên xuống và nhìn ngang.<br>" + KTL +
            "<br>Mặt Trời không ở tâm.<br>Nhìn dọc theo đĩa từ bên trong, ta thấy dải sáng mờ Ngân Hà.")

# ═════════ kiểm số liệu các quiz (cùng quy ước tinh.py) ═════════
AU, DS, DM, RE, c = 1.5e8, 1.39e6, 3470, 6370, 3e5
assert round(AU / 384_000) == 391 and round(DS / DM) == 401                       # q0: to gấp ~400, xa gấp ~390
assert 3 * 49 == 147 and (19 * 60 + 147) == 21 * 60 + 27                          # q2
d = 380_000
L = (AU - d) * DM / (DS - DM)
x = d - RE
assert x < L < d and abs(L - 374_450) < 50 and abs((AU - 384_000) * DM / (DS - DM) - 374_400) < 50 and round(DM * (L - x) / L) == 8       # q3: toàn phần, vùng tối ~8 km
assert abs((106.7 - 105.8) * 4 - 3.6) < 1e-9                                      # q5
assert 90 - abs(10.0 - (-23.5)) == 56.5 and 90 - abs(10.0 + (-23.5)) == 76.5      # q6
assert round(5.2 * AU / c) == 2600 and round(5.2 * AU / c / 60) == 43             # q7
th = degrees(atan(0.158 / 1.5))
assert abs(th - 6.0) < 0.05 and abs(667 * 360 / 6.0 - 40_000) < 50 and abs(40_000 / (2 * pi) - 6366) < 1   # bài toán mẫu
assert abs(degrees(atan(0.07)) - 4.0) < 0.01 and abs(445 * 360 / 4.0 - 40_000) < 100                     # điền bước
assert abs(384_000 / c - 1.28) < 1e-9                                             # thử thách 2
assert round(120 / (0.90 - 0.46)) == 273 and round(120 / 0.90 / 60, 1) == 2.2     # thử thách 3
S_syn = 1 / (1 / 27.32 - 1 / 365.25)
assert abs(S_syn - 29.53) < 0.01                                                   # mở rộng II
assert abs(24 * 60 / 29.5 - 49) < 0.2

# ═════════ ghi theory.html ═════════
src = open(os.path.join(HERE, "theory.src.html"), encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4, fig5, fig6), 1):
    assert f"<!--FIG{n}-->" in src, n
    src = src.replace(f"<!--FIG{n}-->", f)
src = src.replace("__PHUT__", str(PHUT))
open(os.path.join(HERE, "theory.html"), "w", encoding="utf8").write(src)
print("ok", len(src))
