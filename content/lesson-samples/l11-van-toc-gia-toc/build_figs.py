"""Sinh 4 hình SVG cho bài vận tốc, gia tốc dao động điều hoà.

Thay <!--FIGn--> trong theory.src.html → theory.html. Chạy lại được.
Hình kiểm bằng toạ độ: sin φ = 0, elip đúng phương trình, a = −ω²x là đoạn thẳng qua gốc.
Rà soát 30/10/2026: chữ ≥ 14, mọi đầu mũi tên (vectơ, trục, chiều đi trên elip) là chữ V 30° (chevron),
lấy svg_lib của skill (không dùng marker tam giác); màu nhất quán: cam = x, xanh lá = v, đỏ = a, xanh dương = đường elip.
"""
import sys as _sys, pathlib as _pl
_HERE = _pl.Path(__file__).resolve().parent
_sys.path.insert(0, str(_HERE.parent))
from _margin_fig import margin_figs
_sys.path.insert(0, str(_HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
import math
from svg_lib import RED, BLUE, ORG, GRN, defs, arrow, text, wrap, chevron  # noqa: E402

FS = 14  # cỡ chữ tối thiểu trong viewBox 440


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


def axis(x1, y1, x2, y2, w=1.5):
    """Trục toạ độ: thân + đầu V 30° ở (x2, y2)."""
    return line(x1, y1, x2, y2, "currentColor", w) + chevron(x2, y2, x2 - x1, y2 - y1, "currentColor", w, 10)


def guide(x1, y1, x2, y2):
    return line(x1, y1, x2, y2, "currentColor", 1.1, "4 3", 0.55)


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
a_left = {"mA": False, "mH": False, "O": None, "pH": True, "pA": True}
for key, x in pos.items():  # a luôn về O: bên phải O thì sang trái
    if a_left[key] is not None:
        assert a_left[key] == (x > O)
    assert abs(alen[key] - AMAX * abs(x - O) / AMP_PX) < 1e-9  # |a| tỉ lệ |x|
    assert abs(vlen[key] - VMAX * math.sqrt(max(0.0, 1 - ((x - O) / AMP_PX) ** 2))) < 1e-9

YV, YR, YA, YL = 92.0, 128.0, 164.0, 200.0
b = text(16, 24, "Mũi xanh lá: vận tốc v", GRN, FS, "start", "700")
b += text(16, 46, "Mũi đỏ: gia tốc a, luôn hướng về O", RED, FS, "start", "700")
# trục Ox, chiều dương sang phải
b += axis(30, YR, 412, YR, 2)
b += text(418, YR + 5, "x", "currentColor", FS, "start", "700")
for key, x in pos.items():
    b += dot(x, YR, 6.5, "currentColor")
# mũi v, hướng trái (chiều âm)
for key, x in pos.items():
    L = vlen[key]
    if L < 1:
        b += text(x, YV + 5, "v = 0", GRN, FS, "middle", "700")
    else:
        b += arrow("", "g", x, YV, round(x - L, 1), YV, 2.6)
# mũi a, về O
for key, x in pos.items():
    L = alen[key]
    if L < 1:
        b += text(x, YA + 5, "a = 0", RED, FS, "middle", "700")
    elif a_left[key]:
        b += arrow("", "r", x, YA, round(x - L, 1), YA, 2.6)
    else:
        b += arrow("", "r", x, YA, round(x + L, 1), YA, 2.6)
labels = (("mA", "−A"), ("mH", "−A/2"), ("O", "O"), ("pH", "+A/2"), ("pA", "+A"))
for key, lab in labels:
    b += text(pos[key], YL, lab, "currentColor", FS, "middle", "700")
b += text(16, 232, "Từ +A về O: v và a cùng chiều, nhanh dần.", "currentColor", FS, "start", "500")
b += text(16, 254, "Từ O ra −A: v và a ngược chiều, chậm dần.", "currentColor", FS, "start", "500")
fig1 = wrap(
    "0 0 440 266",
    "Năm thời điểm của con lắc lò xo, nửa chu kì từ biên dương sang biên âm",
    b,
    "Hình 1. Nửa chu kì từ +A sang −A.<br>Mũi xanh lá là vận tốc, mũi đỏ là gia tốc (luôn về O).",
)

# kiểm mũi không đè nhau trên cùng một hàng, chữ "v = 0"/"a = 0" (rộng ~40) không chạm mũi bên cạnh
assert pos["pH"] - vlen["pH"] > pos["O"] + 8
assert pos["O"] - vlen["O"] > pos["mH"] + 8
assert pos["mH"] - vlen["mH"] > pos["mA"] + 22
assert pos["pA"] - 22 > pos["pH"]
assert pos["pA"] - alen["pA"] > pos["pH"] + 8
assert pos["mH"] - (pos["mA"] + alen["mA"]) > 8
assert pos["mH"] + alen["mH"] < pos["O"] - 22 and pos["pH"] - alen["pH"] > pos["O"] + 22


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
b += text(220, 16, "φ = 0", "currentColor", 13, "middle", "700")
b += text(16, 16, "cam: x", ORG, 13, "start", "700")
b += text(300, 16, "xanh: v", GRN, 13, "start", "700")
b += text(372, 16, "đỏ: a", RED, 13, "start", "700")
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
    b += text(X1 + 16, base + 4, "t", "currentColor", 13, "start", "700")
    b += text(18, base + 4, name, "currentColor", 13, "start", "700")
    b += poly([(X(th), Y(base, fn(th))) for th in ths], col, 2.3)
# lưới T/4, T/2, 3T/4
for k, lab in ((1, "T/4"), (2, "T/2"), (3, "3T/4")):
    x = X(k * math.pi / 2)
    b += line(x, 46, x, 276, "currentColor", 1, "3 3", 0.35)
for k, lab in ((0, "0"), (1, "T/4"), (2, "T/2"), (3, "3T/4"), (4, "T")):
    b += text(X(k * math.pi / 2), 294, lab, "currentColor", 13, "middle", "600")
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

# Hình 2 thay bằng ảnh OpenStax (28/10/2026, ngoại lệ có chủ đích: ảnh raster), giữ mốc FIG2
fig2 = '<figure class="fig" data-tl="1" data-exp="tn-l11-vantocdddh-02"><img src="/assets/openstax/l11-van-toc-gia-toc/hinh-do-thi-x-v-a.webp" alt="Ba đồ thị theo thời gian của vật dao động trên lò xo: li độ x bắt đầu ở cực đại, vận tốc v bắt đầu bằng 0, gia tốc a bắt đầu ở cực tiểu" loading="lazy" width="704" height="515"><figcaption>Hình 2. φ = 0: x, v, a theo thời gian (trục đứng là x, v, a).<br>X = A; v<sub>max</sub> = Aω; a<sub>max</sub> = Aω².<br>v sớm x một góc π/2.<br>a ngược pha với x.<br>Position / Velocity / Acceleration = li độ / vận tốc / gia tốc.<br><small>Hình: OpenStax, College Physics 2e, Hình 16.12 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>'


# ---- Hình 3: elip (x/A)² + (v/(ωA))² = 1
# x = A cos θ, v = −Aω sin θ. Màn hình: v dương hướng lên → y = CY + RY·sin θ → θ tăng là chiều kim đồng hồ.
CX, CY, RX, RY = 214.0, 136.0, 118.0, 72.0


def ell_xy(th):
    return CX + RX * math.cos(th), CY + RY * math.sin(th)


def ell_dir(th):  # hướng đi khi θ (t) tăng
    return -RX * math.sin(th), RY * math.cos(th)


pts = [ell_xy(i * 2 * math.pi / 120) for i in range(121)]
for x, y in pts:
    xn, vn = (x - CX) / RX, (CY - y) / RY
    th = math.atan2(-vn, xn)
    assert abs(xn * xn + vn * vn - 1) < 1e-6
    assert abs(xn - math.cos(th)) < 1e-6 and abs(vn + math.sin(th)) < 1e-6  # v = −Aω sin θ
r, d, l, u = ell_xy(0), ell_xy(math.pi / 2), ell_xy(math.pi), ell_xy(3 * math.pi / 2)
assert r[0] > CX and abs(r[1] - CY) < 1
assert d[1] > CY and abs(d[0] - CX) < 1  # θ = π/2: x = 0, v = −Aω (dưới)
assert u[1] < CY and abs(u[0] - CX) < 1  # θ = 3π/2: v = +Aω (trên)
TH3 = (0.6, math.pi + 0.6)
for th in TH3:  # θ = 0,6: góc dưới-phải, đi sang trái-xuống
    dx_, dy_ = ell_dir(th)
    if th < 1:
        assert dx_ < 0 and dy_ > 0

b = axis(28, CY, 410, CY)
b += axis(CX, 236, CX, 22)
b += poly(pts, BLUE, 2.4)
for th in TH3:
    x, y = ell_xy(th)
    b += chevron(x, y, *ell_dir(th), BLUE, 2.6, 13)
b += dot(r[0], r[1], 4.5, ORG)
b += dot(l[0], l[1], 4.5, ORG)
b += dot(u[0], u[1], 4.5, GRN)
b += dot(d[0], d[1], 4.5, GRN)
b += text(404, CY - 10, "x", "currentColor", FS, "start", "700")
b += text(CX - 10, 30, "v", "currentColor", FS, "end", "700")
b += text(r[0] + 6, CY - 10, "+A", ORG, FS, "start", "700")
b += text(l[0] - 6, CY - 10, "−A", ORG, FS, "end", "700")
b += text(u[0] + 10, u[1] - 8, "+Aω", GRN, FS, "start", "700")
b += text(d[0] + 10, d[1] + 20, "−Aω", GRN, FS, "start", "700")
b += text(16, 262, "Khi t tăng, điểm (x, v) đi theo chiều kim đồng hồ.", "currentColor", FS, "start", "500")
fig3 = wrap(
    "0 0 440 274",
    "Elip li độ và vận tốc, phương trình (x/A) bình phương cộng (v chia A omega) bình phương bằng 1",
    b,
    "Hình 3. Đồ thị x–v là elip: (x/A)² + (v/(ωA))² = 1.<br>Hai trục khác thang.",
)


# ---- Hình 4: đoạn thẳng a = −ω²x và elip v–a
# Trái: điểm (+A, −ω²A) góc dưới-phải, (−A, +ω²A) góc trên-trái — độ dốc âm.
LX, LY, H = 112.0, 122.0, 62.0
# Phải: v_n = −sin θ, a_n = −cos θ (v dương sang phải, a dương lên trên)
RXC, RYC, RV, RA = 328.0, 122.0, 64.0, 54.0


def va_xy(th):
    return RXC - RV * math.sin(th), RYC + RA * math.cos(th)


def va_dir(th):
    return -RV * math.cos(th), -RA * math.sin(th)


va = [va_xy(i * 2 * math.pi / 120) for i in range(121)]
for i, (x, y) in enumerate(va):
    th = i * 2 * math.pi / 120
    vn, an = (x - RXC) / RV, (RYC - y) / RA
    assert abs(vn + math.sin(th)) < 1e-6 and abs(an + math.cos(th)) < 1e-6
assert abs(va_xy(0)[0] - RXC) < 1 and va_xy(0)[1] > RYC  # t = 0 (x = +A): v = 0, a = −amax (dưới)
assert va_xy(math.pi)[1] < RYC  # x = −A: a = +amax (trên)
p_pos = (LX + H, LY + H)  # +A, −amax
p_neg = (LX - H, LY - H)  # −A, +amax
assert abs((p_pos[0] + p_neg[0]) / 2 - LX) < 1e-6 and abs((p_pos[1] + p_neg[1]) / 2 - LY) < 1e-6
assert p_pos[1] > p_neg[1]  # x tăng thì a giảm
TH4 = (0.9, math.pi + 0.9)
assert va_dir(0.9)[0] < 0 and va_dir(0.9)[1] < 0  # từ đáy: v âm dần (trái), a tăng (lên)

b = ""
# panel trái: a theo x
b += text(LX, 20, "a theo x", "currentColor", FS, "middle", "700")
b += axis(LX - H - 20, LY, LX + H + 26, LY)
b += axis(LX, LY + H + 22, LX, LY - H - 22)
b += guide(p_neg[0], p_neg[1], p_neg[0], LY)
b += guide(p_neg[0], p_neg[1], LX, p_neg[1])
b += guide(p_pos[0], p_pos[1], p_pos[0], LY)
b += guide(p_pos[0], p_pos[1], LX, p_pos[1])
b += line(p_neg[0], p_neg[1], p_pos[0], p_pos[1], RED, 2.6)
b += dot(p_pos[0], p_pos[1], 4.5, RED)
b += dot(p_neg[0], p_neg[1], 4.5, RED)
b += text(LX + H + 22, LY + 20, "x", "currentColor", FS, "start", "700")
b += text(LX + 10, LY - H - 12, "a", "currentColor", FS, "start", "700")
b += text(p_pos[0], LY - 8, "+A", ORG, FS, "middle", "700")
b += text(p_neg[0], LY + 20, "−A", ORG, FS, "middle", "700")
b += text(LX + 8, p_neg[1] + 5, "+ω²A", RED, FS, "start", "700")
b += text(LX - 8, p_pos[1] + 5, "−ω²A", RED, FS, "end", "700")
# panel phải: v và a
b += text(RXC, 20, "a theo v", "currentColor", FS, "middle", "700")
b += axis(RXC - RV - 18, RYC, RXC + RV + 22, RYC)
b += axis(RXC, RYC + RA + 18, RXC, RYC - RA - 22)
b += poly(va, BLUE, 2.4)
for th in TH4:
    x, y = va_xy(th)
    b += chevron(x, y, *va_dir(th), BLUE, 2.6, 13)
top, bot = va_xy(math.pi), va_xy(0)
left, right = va_xy(math.pi / 2), va_xy(3 * math.pi / 2)
b += dot(right[0], right[1], 4.5, GRN)
b += dot(left[0], left[1], 4.5, GRN)
b += dot(top[0], top[1], 4.5, RED)
b += dot(bot[0], bot[1], 4.5, RED)
b += text(RXC + RV + 14, RYC - 8, "v", "currentColor", FS, "start", "700")
b += text(RXC - 10, RYC - RA - 12, "a", "currentColor", FS, "end", "700")
b += text(right[0] + 4, RYC + 20, "+Aω", GRN, FS, "start", "700")
b += text(left[0] - 4, RYC + 20, "−Aω", GRN, FS, "end", "700")
b += text(top[0] + 10, top[1] - 6, "+ω²A", RED, FS, "start", "700")
b += text(bot[0] + 10, bot[1] + 18, "−ω²A", RED, FS, "start", "700")
fig4 = wrap(
    "0 0 440 222",
    "Đoạn thẳng gia tốc theo li độ qua gốc, và elip gia tốc theo vận tốc",
    b,
    "Hình 4. Trái: a theo x là đoạn thẳng qua gốc, dốc xuống (a = −ω²x).<br>Phải: a theo v là một elip.",
)

h = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert "<!--FIG%d-->" % n in h, n
    h = h.replace("<!--FIG%d-->" % n, f)
assert "<!--FIG" not in h
open("theory.html", "w", encoding="utf8").write(margin_figs(h))
print("ok", len(h))
