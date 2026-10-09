"""Sinh 4 hình SVG cho Bài 7 (Bài tập năng lượng trong dao động điều hoà, Vật lí 11, lesson 26)
và thay mốc <!--FIGn--> trong theory.src.html -> theory.html.  Chạy: python3 build_figs.py (từ thư mục bài)."""
import math, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from svg_lib import *

FS, SUB = 17, 13          # cỡ chữ nhãn / chỉ số dưới (viewBox rộng 420)
LABELS = []               # (x, y, số ký tự hiển thị, cỡ, anchor, chuỗi) để kiểm chồng chữ + mép


def line(x1, y1, x2, y2, c="currentColor", w=1.8, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" '
            f'stroke-width="{w}"{d} opacity="{op}"/>')


def poly(pts, c, w=2.6, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<polyline fill="none" stroke="{c}" stroke-width="{w}"{d} stroke-linejoin="round" points="'
            + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>')


def dot(x, y, r=5, c="currentColor", fill=True):
    if fill:
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="{c}" stroke-width="2"/>'


def T(x, y, s, c="currentColor", anchor="start", weight="600", sub=None, size=FS):
    """Nhãn chữ; `sub` là chỉ số dưới (tspan baseline-shift). Cấm $ trong SVG."""
    assert "$" not in s and (sub is None or "$" not in sub), s
    n = len(s) + (0.8 * len(sub) if sub else 0)
    LABELS.append((x, y, n, size, anchor, s + (sub or "")))
    body = s + (f'<tspan baseline-shift="sub" font-size="{SUB}">{sub}</tspan>' if sub else "")
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}">{body}</text>')


def _box(it):
    x, y, n, size, anchor, _ = it
    w = 0.58 * size * n
    x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
    return (x0, y - 0.8 * size, x0 + w, y + 0.25 * size)


def kiem_nhan(vb, ten, vat_can=()):
    """Nhãn không chồng nhau, không vượt viewBox, không đè lên điểm vật cản (x, y, r)."""
    _, _, W, H = (float(v) for v in vb.split())
    bx = [_box(it) for it in LABELS]
    loi = []
    for it, (a0, b0, a1, b1) in zip(LABELS, bx):
        if a0 < 3 or b0 < 2 or a1 > W - 3 or b1 > H - 2:
            loi.append(f"{ten}: nhãn {it[5]!r} ra ngoài mép ({a0:.0f},{b0:.0f})-({a1:.0f},{b1:.0f})")
        for (cx, cy, r) in vat_can:
            if a0 - r < cx < a1 + r and b0 - r < cy < b1 + r:
                loi.append(f"{ten}: nhãn {it[5]!r} đè điểm ({cx:.0f},{cy:.0f})")
    for i in range(len(bx)):
        for j in range(i + 1, len(bx)):
            A, B = bx[i], bx[j]
            if A[0] < B[2] and B[0] < A[2] and A[1] < B[3] and B[1] < A[3]:
                loi.append(f"{ten}: chồng {LABELS[i][5]!r} và {LABELS[j][5]!r}")
    if loi:
        print("\n".join(loi)); sys.exit(1)
    LABELS.clear()


def legend(items, y, x0=40, gap=118):
    b = ""
    for i, (c, s, sub, dash) in enumerate(items):
        x = x0 + i * gap
        b += line(x, y - 6, x + 26, y - 6, c, 3, dash)
        b += T(x + 32, y, s, c, sub=sub)
    return b


# ---------------- Hình 1: xích đu, hai lần đẩy (chỉ vẽ cảnh, không số liệu) ----------------
VB1 = "0 0 420 266"
P = (170.0, 30.0); L = 170.0
def on_rope(deg, r=L):
    a = math.radians(deg)
    return P[0] + r * math.sin(a), P[1] + r * math.cos(a)
b = ""
b += line(22, 30, 398, 30, "currentColor", 4) + line(26, 30, 26, 240, "currentColor", 3) + line(394, 30, 394, 240, "currentColor", 3)
b += line(30, 240, 400, 240, "currentColor", 2)
b += dot(*P, 5)
arc = [on_rope(d) for d in range(-32, 33, 2)]
b += poly(arc, "currentColor", 1.4, "3 5")
low = on_rope(0)
b += dot(*low, 5, "currentColor", fill=False)
def seat(deg, c, dash=""):
    sx, sy = on_rope(deg)
    hx, hy = on_rope(deg, L - 30)
    a = math.radians(deg)
    ux, uy = math.cos(a), -math.sin(a)          # vuông góc dây: hướng mặt ghế
    g = line(P[0], P[1], sx, sy, c, 2.2, dash)
    g += line(sx - 14 * ux, sy - 14 * uy, sx + 14 * ux, sy + 14 * uy, c, 5)
    g += f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="9" fill="none" stroke="{c}" stroke-width="2.2"{" stroke-dasharray=" + chr(34) + dash + chr(34) if dash else ""}/>'
    return g, (sx, sy)
g1, s1 = seat(15, BLUE)
g2, s2 = seat(30, ORG, "6 4")
b += g1 + g2
b += T(s1[0] + 24, s1[1] + 22, "lần 1", BLUE)
b += T(s2[0] + 18, s2[1] - 8, "lần 2:", ORG)
b += T(s2[0] + 18, s2[1] + 14, "góc gấp đôi", ORG)
b += T(low[0], low[1] + 28, "chỗ thấp nhất", "currentColor", "middle", "400")
kiem_nhan(VB1, "hình 1", [(*s1, 6), (*s2, 6), (*low, 5)])
fig1 = wrap(VB1, "Xích đu ở sân trường: lần một đẩy nhẹ, lần hai đẩy cho góc lệch lớn gấp đôi",
            b, "Hình 1. Cùng một xích đu, hai lần đẩy.<br>Lần 2 góc lệch lớn gấp đôi lần 1.")

# ---------------- Hình 2: năng lượng theo li độ ----------------
VB2 = "0 0 420 262"
OX, OY, HX, HY = 210.0, 216.0, 170.0, 150.0
X = lambda u: OX + HX * u
Yt = lambda u: OY - HY * u * u
Yd = lambda u: OY - HY * (1 - u * u)
yW = OY - HY
us = [i / 100 for i in range(-100, 101)]
# kiểm toạ độ: đáy/đỉnh, giao điểm ±A/√2 ở nửa W, tổng luôn bằng W
assert abs(Yt(0) - OY) < 1e-9 and abs(Yt(1) - yW) < 1e-9 and abs(Yd(0) - yW) < 1e-9
xi = 1 / math.sqrt(2)
assert abs(Yt(xi) - Yd(xi)) < 1e-9 and abs(Yt(xi) - (OY - HY / 2)) < 1e-9
for u in us:
    assert abs((OY - Yt(u)) + (OY - Yd(u)) - HY) < 1e-9
b = ""
b += line(28, OY, 396, OY, "currentColor", 1.6) + chevron(400, OY, 1, 0, "currentColor", 1.6, 10)
b += line(OX, OY, OX, 46, "currentColor", 1.6) + chevron(OX, 42, 0, -1, "currentColor", 1.6, 10)
b += T(404, OY - 10, "x", "currentColor", "end", "700")
b += T(OX - 8, 52, "năng lượng (J)", "currentColor", "end", "400")
b += line(X(-1), yW, X(1), yW, GRN, 3)
b += poly([(X(u), Yt(u)) for u in us], ORG, 3)
b += poly([(X(u), Yd(u)) for u in us], BLUE, 3)
for u in (-xi, xi):
    b += line(X(u), Yt(u), X(u), OY, "currentColor", 1.2, "4 4", .7) + dot(X(u), Yt(u), 5)
for u in (-1, 1):
    b += line(X(u), yW, X(u), OY, "currentColor", 1.2, "4 4", .5)
b += T(X(-1), OY + 26, "−A", anchor="middle", weight="400")
b += T(X(-xi), OY + 26, "−A/√2", anchor="middle", weight="400")
b += T(OX, OY + 26, "0", anchor="middle", weight="400")
b += T(X(xi), OY + 26, "A/√2", anchor="middle", weight="400")
b += T(X(1), OY + 26, "A", anchor="middle", weight="400")
b += legend([(GRN, "W", None, ""), (ORG, "W", "t", ""), (BLUE, "W", "đ", "")], 24, 60, 110)
kiem_nhan(VB2, "hình 2", [(X(-xi), Yt(-xi), 5), (X(xi), Yt(xi), 5)])
fig2 = wrap(VB2, "Đồ thị năng lượng theo li độ: thế năng là parabol đáy ở vị trí cân bằng, động năng là parabol úp, cơ năng là đường nằm ngang; hai parabol cắt nhau tại cộng trừ A chia căn hai",
            b, "Hình 2. Năng lượng theo li độ $x$.<br>$W_t$: parabol đáy ở VTCB; $W_{\\text{đ}}$: parabol úp.<br>$W$: đường ngang; hai parabol cắt nhau tại $x\\approx\\pm0{,}71A$.")

# ---------------- Hình 3: li độ và năng lượng theo thời gian ----------------
VB3 = "0 0 420 334"
T0, T1 = 56.0, 376.0          # t = 0 .. T
tx = lambda s: T0 + (T1 - T0) * s
XC, XA = 64.0, 30.0           # khung li độ
EB, EH = 284.0, 112.0         # khung năng lượng: đáy, chiều cao W
ts = [i / 160 for i in range(161)]
xt = [(tx(s), XC - XA * math.cos(2 * math.pi * s)) for s in ts]
Et = [(tx(s), EB - EH * math.cos(2 * math.pi * s) ** 2) for s in ts]
Ed = [(tx(s), EB - EH * math.sin(2 * math.pi * s) ** 2) for s in ts]
# kiểm: x lặp sau T (một đỉnh dương ở 0 và T), Wt có đỉnh ở 0, T/2, T; Wt + Wđ = W
for s in (0, .5, 1):
    assert abs(EB - EH * math.cos(2 * math.pi * s) ** 2 - (EB - EH)) < 1e-9
assert abs(math.cos(2 * math.pi * .5) - (-1)) < 1e-9          # x ở biên âm lúc T/2 -> chu kì x là T
for (a, y1), (_, y2) in zip(Et, Ed):
    assert abs((EB - y1) + (EB - y2) - EH) < 1e-9
cross = [tx(k / 8) for k in (1, 3, 5, 7)]
for k, cx in zip((1, 3, 5, 7), cross):
    s = k / 8
    assert abs(math.cos(2 * math.pi * s) ** 2 - .5) < 1e-9
b = ""
b += line(T0, XC, T1 + 14, XC, "currentColor", 1.2, op=.6)
b += poly(xt, "currentColor", 2.4)
b += T(T0 - 10, XC + 6, "x", "currentColor", "end", "700")
b += T(T0 + 4, 20, "li độ x (cm)", "currentColor", "start", "400")
b += T(T0 + 6, EB - EH - 14, "năng lượng (J)", "currentColor", "start", "400")
b += line(T0, EB, T1 + 14, EB, "currentColor", 1.6) + chevron(T1 + 18, EB, 1, 0, "currentColor", 1.6, 10)
b += T(T1 + 18, EB - 10, "t", "currentColor", "end", "700")
b += line(T0, EB, T0, EB - EH - 12, "currentColor", 1.6)
b += line(T0, EB - EH, T1, EB - EH, GRN, 3)
b += poly(Et, ORG, 3) + poly(Ed, BLUE, 3)
for cx in cross:
    b += dot(cx, EB - EH / 2, 4.5)
for k, lab in ((1, "T/4"), (2, "T/2"), (3, "3T/4"), (4, "T")):
    gx = tx(k / 4)
    b += line(gx, XC - XA - 6, gx, XC + XA + 6, "currentColor", 1.1, "3 5", .55)
    b += line(gx, EB - EH - 8, gx, EB, "currentColor", 1.1, "3 5", .55)
    b += T(gx, EB + 24, lab, anchor="middle", weight="400")
b += T(T0, EB + 24, "0", anchor="middle", weight="400")
b += legend([(GRN, "W", None, ""), (ORG, "W", "t", ""), (BLUE, "W", "đ", "")], 128, 60, 110)
kiem_nhan(VB3, "hình 3", [(cx, EB - EH / 2, 4.5) for cx in cross])
fig3 = wrap(VB3, "Trên: li độ theo thời gian, lặp lại sau một chu kì T. Dưới: thế năng và động năng theo thời gian, ngược pha nhau, lặp lại sau nửa chu kì; cơ năng là đường nằm ngang",
            b, "Hình 3. Trên: li độ $x$ lặp lại sau $T$.<br>Dưới: $W_t$ và $W_{\\text{đ}}$ ngược pha, lặp lại sau $T/2$.<br>$W$ nằm ngang.")

# ---------------- Hình 4: con lắc đơn ----------------
VB4 = "0 0 420 286"
P4 = (210.0, 30.0); L4 = 200.0
def pos(deg):   # deg > 0: lệch sang phải
    a = math.radians(deg)
    return P4[0] + L4 * math.sin(a), P4[1] + L4 * math.cos(a)
A0, AL = -40, 20
B0, BA, BOT = pos(A0), pos(AL), pos(0)
h_px = BOT[1] - B0[1]
assert abs(h_px - L4 * (1 - math.cos(math.radians(40)))) < 1e-9
b = ""
b += line(150, P4[1], 270, P4[1], "currentColor", 4)
b += line(P4[0], P4[1], P4[0], BOT[1] + 18, "currentColor", 1.2, "5 5", .7)
b += poly([pos(d) for d in range(-44, 45, 2)], "currentColor", 1.2, "3 5")
b += line(P4[0], P4[1], B0[0], B0[1], ORG, 2.2, "6 4") + dot(*B0, 11, ORG)
b += line(P4[0], P4[1], BA[0], BA[1], BLUE, 2.2) + dot(*BA, 11, BLUE)
b += dot(*BOT, 11, "currentColor", fill=False)
# cung góc
b += poly([(P4[0] + 46 * math.sin(math.radians(d)), P4[1] + 46 * math.cos(math.radians(d))) for d in range(-40, 1, 2)], ORG, 2)
b += poly([(P4[0] + 66 * math.sin(math.radians(d)), P4[1] + 66 * math.cos(math.radians(d))) for d in range(0, 21, 2)], BLUE, 2)
# độ cao h: từ ngang biên xuống ngang đáy
HXL = 46
b += line(B0[0] - 12, B0[1], HXL - 6, B0[1], "currentColor", 1.2, "4 4", .8)
b += line(BOT[0] - 12, BOT[1], HXL - 6, BOT[1], "currentColor", 1.2, "4 4", .8)
b += line(HXL, B0[1], HXL, BOT[1], "currentColor", 1.8)
b += chevron(HXL, B0[1], 0, -1, "currentColor", 1.8, 9) + chevron(HXL, BOT[1], 0, 1, "currentColor", 1.8, 9)
b += T(HXL - 10, (B0[1] + BOT[1]) / 2 + 6, "h", "currentColor", "end", "700")
# vận tốc tại góc α (đang đi lên sang phải): tiếp tuyến (cos α, −sin α)
a = math.radians(AL)
vx, vy = BA[0] + 44 * math.cos(a), BA[1] - 44 * math.sin(a)
b += line(BA[0] + 12 * math.cos(a), BA[1] - 12 * math.sin(a), vx, vy, GRN, 2.6) + chevron(vx, vy, math.cos(a), -math.sin(a), GRN, 2.6)
b += T(vx + 8, vy - 4, "v", GRN, weight="700")
lm = ((P4[0] + B0[0]) / 2, (P4[1] + B0[1]) / 2)
b += T(lm[0] - 14, lm[1], "l", "currentColor", "end", "700")
b += T(P4[0] - 22, P4[1] + 70, "α", ORG, "middle", "700", sub="0")
b += T(P4[0] + 15, P4[1] + 92, "α", BLUE, "middle", "700")
b += T(B0[0] - 17, B0[1] - 33, "v = 0", ORG, "end", "600")
b += T(B0[0] - 17, B0[1] - 13, "biên", ORG, "end", "600")
b += T(BOT[0] + 18, BOT[1] + 36, "đáy: mốc thế năng", "currentColor", "start", "400")
kiem_nhan(VB4, "hình 4", [(B0[0], B0[1], 11), (BA[0], BA[1], 11), (BOT[0], BOT[1], 11)])
fig4 = wrap(VB4, "Con lắc đơn dây dài l: vật ở biên lệch góc alpha 0, cao hơn đáy một đoạn h; vật ở góc alpha đang chuyển động với vận tốc v; mốc thế năng ở đáy",
            b, "Hình 4. Con lắc đơn, mốc thế năng ở đáy.<br>Độ cao của biên: $h=l(1-\\cos\\alpha_0)$.")

h = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    assert "$" not in f.split("<figcaption>")[0], n
    h = h.replace(f"<!--FIG{n}-->", f)
pos_fig = [h.find(f"Hình {n}.") for n in (1, 2, 3, 4)]
assert pos_fig == sorted(pos_fig), "số hình không theo thứ tự xuất hiện"
open("theory.html", "w", encoding="utf8").write(h)
print("ok", len(h), "bytes,", h.count('<figure class="fig"'), "hình")
