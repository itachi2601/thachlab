"""Sinh 4 hình SVG cho bài vận tốc, gia tốc dao động điều hoà.

Thay <!--FIGn--> trong theory.src.html → theory.html. Chạy lại được.
Hình kiểm bằng toạ độ: sin φ = 0, elip đúng phương trình, a = −ω²x là đoạn thẳng qua gốc.
"""
import math
from svg_lib import *

def poly(pts, c, w=2.2):
    return (
        '<polyline fill="none" stroke="%s" stroke-width="%s" points="%s"/>'
        % (c, w, " ".join("%.1f,%.1f" % (x, y) for x, y in pts))
    )

def dot(x, y, r=4.5, c="currentColor"):
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>' % (x, y, r, c)

def line(x1, y1, x2, y2, c="currentColor", w=1.6, dash="", op=1):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s opacity="%s"/>' % (
        x1, y1, x2, y2, c, w, d, op)

def sub(x, y, base, idx, c="currentColor", size=12, anchor="middle", weight="600"):
    """Chỉ số dưới bằng tspan — không dùng $ trong SVG."""
    return (
        '<text x="%.1f" y="%.1f" fill="%s" font-size="%d" font-weight="%s" text-anchor="%s">'
        '%s<tspan dy="4" font-size="9">%s</tspan></text>'
    ) % (x, y, c, size, weight, anchor, base, idx)


# ---- Hình 1: năm thời điểm, nửa chu kì từ +A sang −A
# O = 214; A = 156 px. |v| tại ±A/2 = (√3/2)·|v|_max, |a| tỉ lệ |x|.
O, AMP_PX = 214.0, 156.0
pos = {
    "mA": O - AMP_PX,
    "mH": O - AMP_PX / 2,
    "O": O,
    "pH": O + AMP_PX / 2,
    "pA": O + AMP_PX,
}
VMAX, AMAX = 50.0, 44.0
vlen = {
    "mA": 0.0,
    "mH": VMAX * math.sqrt(3) / 2,
    "O": VMAX,
    "pH": VMAX * math.sqrt(3) / 2,
    "pA": 0.0,
}
alen = {"mA": AMAX, "mH": AMAX / 2, "O": 0.0, "pH": AMAX / 2, "pA": AMAX}
# Chiều: nửa chu kì này v luôn hướng âm (sang trái). a hướng về O.
v_left = True
a_left = {"mA": False, "mH": False, "O": None, "pH": True, "pA": True}

b = defs("f1")
b += text(16, 22, "xanh lá: v", GRN, 12, "start", "700")
b += text(150, 22, "đỏ: a, luôn hướng về O", RED, 12, "start", "700")
# ray + chiều dương
b += line(36, 112, 400, 112, "currentColor", 2)
b += '<path d="M393,107 L404,112 L393,117" fill="currentColor"/>'
b += text(408, 116, "+", "currentColor", 13, "start", "700")
# thành
b += line(36, 96, 36, 128, "currentColor", 3)
for key, x in pos.items():
    b += dot(x, 112, 6.5, "currentColor")
# mũi v (y = 78), hướng trái
for key, x in pos.items():
    L = vlen[key]
    if L < 1:
        b += text(x, 58, "v = 0", GRN, 11, "middle", "700")
    else:
        b += arrow("f1", "g", x, 78, x - L, 78, 2.6)
# mũi a (y = 150)
for key, x in pos.items():
    L = alen[key]
    if L < 1:
        b += text(x, 168, "a = 0", RED, 11, "middle", "700")
    elif a_left[key]:
        b += arrow("f1", "r", x, 150, x - L, 150, 2.6)
    else:
        b += arrow("f1", "r", x, 150, x + L, 150, 2.6)
labels = (("mA", "−A"), ("mH", "−A/2"), ("O", "O"), ("pH", "+A/2"), ("pA", "+A"))
for key, lab in labels:
    b += text(pos[key], 196, lab, "currentColor", 13, "middle", "700")
b += text(16, 216, "Từ +A về O: v và a cùng chiều, nhanh dần.", "currentColor", 11, "start", "500")
b += text(16, 232, "Từ O ra −A: v và a ngược chiều, chậm dần.", "currentColor", 11, "start", "500")
fig1 = wrap(
    "0 0 440 246",
    "Năm thời điểm của con lắc lò xo, nửa chu kì từ biên dương sang biên âm",
    b,
    "Hình 1. Nửa chu kì từ +A sang −A: mũi xanh lá là vận tốc, mũi đỏ là gia tốc (luôn về O).",
)

# kiểm mũi không đè nhau trên cùng một hàng
assert vlen["pH"] == VMAX * math.sqrt(3) / 2
assert pos["pH"] - vlen["pH"] > pos["O"] + 8  # mũi +A/2 chưa chạm gốc mũi tại O
assert pos["O"] - vlen["O"] > pos["mH"] + 8
assert pos["pA"] - alen["pA"] > pos["pH"] + 8
assert pos["mH"] - (pos["mA"] + alen["mA"]) > 8


# ---- Hình 2: x, v, a theo t, φ = 0
# x = cos θ, v = −sin θ, a = −cos θ. Trục tung hướng lên = giá trị dương.
X0, X1 = 56.0, 408.0
bases = {"x": 78.0, "v": 164.0, "a": 250.0}
AMP = 26.0

def X(th):
    return X0 + th / (2 * math.pi) * (X1 - X0)

def Y(base, norm):
    return base - AMP * norm

b = defs("f2")
b += text(220, 16, "φ = 0", "currentColor", 12, "middle", "700")
b += text(16, 16, "cam: x", ORG, 12, "start", "700")
b += text(300, 16, "xanh: v", GRN, 12, "start", "700")
b += text(372, 16, "đỏ: a", RED, 12, "start", "700")
ths = [i * 2 * math.pi / 80 for i in range(81)]
curves = {
    "x": (ORG, lambda th: math.cos(th)),
    "v": (GRN, lambda th: -math.sin(th)),
    "a": (RED, lambda th: -math.cos(th)),
}
# kiểm pha tại các mốc
assert abs(curves["x"][1](0) - 1) < 1e-9
assert abs(curves["v"][1](0)) < 1e-9
assert abs(curves["a"][1](0) + 1) < 1e-9
assert abs(curves["v"][1](math.pi / 2) + 1) < 1e-9  # T/4: v = −Aω
assert abs(curves["x"][1](math.pi / 2)) < 1e-9
assert abs(curves["a"][1](math.pi)) - 1 < 1e-9 or abs(curves["a"][1](math.pi) - 1) < 1e-9
for name, (col, fn) in curves.items():
    base = bases[name]
    b += line(X0, base, X1 + 12, base, "currentColor", 1.4)
    b += '<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f" fill="currentColor"/>' % (
        X1 + 6, base - 3.2, X1 + 14, base, X1 + 6, base + 3.2)
    b += text(X1 + 16, base + 4, "t", "currentColor", 12, "start", "700")
    b += text(18, base + 4, name, "currentColor", 13, "start", "700")
    b += poly([(X(th), Y(base, fn(th))) for th in ths], col, 2.3)
# lưới T/4, T/2, 3T/4
for k, lab in ((1, "T/4"), (2, "T/2"), (3, "3T/4")):
    x = X(k * math.pi / 2)
    b += line(x, 46, x, 276, "currentColor", 1, "3 3", 0.35)
for k, lab in ((0, "0"), (1, "T/4"), (2, "T/2"), (3, "3T/4"), (4, "T")):
    b += text(X(k * math.pi / 2), 294, lab, "currentColor", 11, "middle", "600")
# chấm t = 0: x cực đại, v = 0, a cực tiểu
b += dot(X(0), Y(bases["x"], 1), 4, ORG)
b += dot(X(0), Y(bases["v"], 0), 4, GRN)
b += dot(X(0), Y(bases["a"], -1), 4, RED)
fig2 = wrap(
    "0 0 440 308",
    "Ba đồ thị li độ, vận tốc, gia tốc theo thời gian khi pha ban đầu bằng 0",
    b,
    "Hình 2. φ = 0: v sớm x một góc π/2; a ngược pha với x và sớm v một góc π/2.",
)
fig2 = fig2.replace(
    '<figure class="fig" data-tl="1">',
    '<figure class="fig" data-tl="1" data-exp="tn-l11-vantocdddh-02">',
    1,
)


# ---- Hình 3: elip (x/A)² + (v/(ωA))² = 1
# x = A cos θ, v = −Aω sin θ → xuôi chiều kim đồng hồ.
CX, CY, RX, RY = 214.0, 132.0, 118.0, 72.0

def ell_xy(th):
    return CX + RX * math.cos(th), CY + RY * math.sin(th)

pts = [ell_xy(i * 2 * math.pi / 120) for i in range(121)]
for x, y in pts:
    xn, yn = (x - CX) / RX, (y - CY) / RY
    assert abs(xn * xn + yn * yn - 1) < 1e-6
# bốn đỉnh: phải v=0, dưới v âm, trái v=0, trên v dương
r, d, l, u = ell_xy(0), ell_xy(math.pi / 2), ell_xy(math.pi), ell_xy(3 * math.pi / 2)
assert r[0] > CX and abs(r[1] - CY) < 1
assert d[1] > CY and abs(d[0] - CX) < 1
assert u[1] < CY and abs(u[0] - CX) < 1
# mũi chiều kim đồng hồ: θ = 0,25 → 0,6 (sang trái và xuống)
p1, p2 = ell_xy(0.25), ell_xy(0.62)
assert p2[0] < p1[0] and p2[1] > p1[1]

b = defs("f3")
b += line(28, CY, 400, CY, "currentColor", 1.5)
b += '<path d="M393,%.1f L404,%.1f L393,%.1f" fill="currentColor"/>' % (CY - 3.2, CY, CY + 3.2)
b += line(CX, 28, CX, 228, "currentColor", 1.5)
b += '<path d="M%.1f,35 L%.1f,26 L%.1f,35" fill="currentColor"/>' % (CX - 3.2, CX, CX + 3.2)
b += poly(pts, BLUE, 2.4)
b += arrow("f3", "b", p1[0], p1[1], p2[0], p2[1], 2.2)
b += dot(r[0], r[1], 4, ORG)
b += dot(l[0], l[1], 4, ORG)
b += dot(u[0], u[1], 4, GRN)
b += dot(d[0], d[1], 4, GRN)
b += text(390, CY - 12, "x", "currentColor", 13, "start", "700")
b += text(CX - 16, 22, "v", "currentColor", 13, "end", "700")
b += text(r[0] + 6, CY - 12, "+A", ORG, 12, "start", "700")
b += text(l[0] - 6, CY - 12, "−A", ORG, 12, "end", "700")
b += text(u[0] + 14, u[1] - 8, "+Aω", GRN, 12, "start", "700")
b += text(d[0] + 14, d[1] + 18, "−Aω", GRN, 12, "start", "700")
b += text(16, 244, "Chiều mũi tên: chiều kim đồng hồ khi θ tăng.", "currentColor", 11, "start", "500")
fig3 = wrap(
    "0 0 440 258",
    "Elip li độ và vận tốc, phương trình (x/A) bình phương cộng (v chia A omega) bình phương bằng 1",
    b,
    "Hình 3. Đồ thị x–v là elip: (x/A)² + (v/(ωA))² = 1. Trục chia đều.",
)


# ---- Hình 4: đoạn thẳng a = −ω²x và elip v–a
# Trái: điểm (+A, −ω²A) góc dưới-phải, (−A, +ω²A) góc trên-trái — độ dốc âm.
LX, LY, H = 112.0, 118.0, 62.0
# Phải: v_n = −sin θ, a_n = −cos θ
RXC, RYC, RV, RA = 328.0, 118.0, 64.0, 52.0

def va_xy(th):
    return RXC - RV * math.sin(th), RYC + RA * math.cos(th)

va = [va_xy(i * 2 * math.pi / 120) for i in range(121)]
for x, y in va:
    vn, an = (RXC - x) / RV, (y - RYC) / RA
    # vn = sin θ, an = cos θ khi ys = cy + RA cos và xs = cx - RV sin
    assert abs(vn * vn + an * an - 1) < 1e-6
# θ = 0: v = 0, a = −amax (dưới)
assert abs(va_xy(0)[0] - RXC) < 1 and va_xy(0)[1] > RYC
# θ = π: a = +amax (trên)
assert va_xy(math.pi)[1] < RYC
# đoạn thẳng qua gốc
p_pos = (LX + H, LY + H)  # +A, −amax
p_neg = (LX - H, LY - H)  # −A, +amax
assert abs((p_pos[0] + p_neg[0]) / 2 - LX) < 1e-6
assert abs((p_pos[1] + p_neg[1]) / 2 - LY) < 1e-6
assert p_pos[1] > p_neg[1]  # x tăng thì a giảm trên hình (y màn hình tăng)

q1, q2 = va_xy(0.15), va_xy(0.55)
assert q2[0] < q1[0]  # θ tăng, v giảm (sang trái)

b = defs("f4")
# panel trái
b += text(LX, 18, "a theo x", RED, 12, "middle", "700")
b += line(LX - H - 18, LY, LX + H + 22, LY, "currentColor", 1.4)
b += '<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f" fill="currentColor"/>' % (
    LX + H + 14, LY - 3, LX + H + 24, LY, LX + H + 14, LY + 3)
b += line(LX, LY + H + 22, LX, LY - H - 16, "currentColor", 1.4)
b += '<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f" fill="currentColor"/>' % (
    LX - 3.2, LY - H - 8, LX, LY - H - 18, LX + 3.2, LY - H - 8)
b += '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.6"/>' % (
    p_neg[0], p_neg[1], p_pos[0], p_pos[1], RED)
b += dot(p_pos[0], p_pos[1], 4, RED)
b += dot(p_neg[0], p_neg[1], 4, RED)
b += dot(LX, LY, 3.5, "currentColor")
b += text(LX + H + 26, LY + 4, "x", "currentColor", 12, "start", "700")
b += text(LX + 8, LY - H - 20, "a", "currentColor", 12, "start", "700")
b += text(p_pos[0] - 4, LY + 16, "+A", ORG, 11, "end", "700")
b += text(p_neg[0] + 4, LY + 16, "−A", ORG, 11, "start", "700")
b += text(LX + 8, p_neg[1] - 2, "+ω²A", RED, 11, "start", "700")
b += text(p_pos[0] - 2, p_pos[1] + 16, "−ω²A", RED, 11, "end", "700")
# panel phải
b += text(RXC, 18, "v và a", GRN, 12, "middle", "700")
b += line(RXC - RV - 16, RYC, RXC + RV + 18, RYC, "currentColor", 1.4)
b += '<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f" fill="currentColor"/>' % (
    RXC + RV + 10, RYC - 3, RXC + RV + 20, RYC, RXC + RV + 10, RYC + 3)
b += line(RXC, RYC + RA + 16, RXC, RYC - RA - 14, "currentColor", 1.4)
b += '<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f" fill="currentColor"/>' % (
    RXC - 3.2, RYC - RA - 6, RXC, RYC - RA - 16, RXC + 3.2, RYC - RA - 6)
b += poly(va, GRN, 2.4)
b += arrow("f4", "g", q1[0], q1[1], q2[0], q2[1], 2.2)
top, bot = va_xy(math.pi), va_xy(0)
left, right = va_xy(math.pi / 2), va_xy(3 * math.pi / 2)
b += dot(right[0], right[1], 4, BLUE)
b += dot(left[0], left[1], 4, BLUE)
b += dot(top[0], top[1], 4, RED)
b += dot(bot[0], bot[1], 4, RED)
b += text(RXC + RV + 22, RYC - 12, "v", "currentColor", 12, "start", "700")
b += text(RXC - 8, RYC - RA - 10, "a", "currentColor", 12, "end", "700")
b += text(right[0] + 4, RYC + 16, "+Aω", BLUE, 11, "start", "700")
b += text(left[0] - 4, RYC + 4, "−Aω", BLUE, 11, "end", "700")
b += text(top[0] + 12, top[1] - 2, "+ω²A", RED, 11, "start", "700")
b += text(bot[0] + 12, bot[1] + 16, "−ω²A", RED, 11, "start", "700")
fig4 = wrap(
    "0 0 440 230",
    "Đoạn thẳng gia tốc theo li độ qua gốc, và elip vận tốc với gia tốc",
    b,
    "Hình 4. a theo x là đoạn thẳng qua gốc (a = −ω²x). v và a nằm trên một elip.",
)

h = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert "<!--FIG%d-->" % n in h, n
    h = h.replace("<!--FIG%d-->" % n, f)
assert "<!--FIG" not in h
open("theory.html", "w", encoding="utf8").write(h)
print("ok", len(h))
