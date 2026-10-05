"""Sinh 3 hình SVG cho bài cơ năng dao động và thay <!--FIGn--> trong theory.src.html."""
import math
import sys
from svg_lib import *

def poly(pts, c, w=2.4):
    return ('<polyline fill="none" stroke="%s" stroke-width="%s" points="%s"/>'
            % (c, w, " ".join("%.1f,%.1f" % (x, y) for x, y in pts)))

def dot(x, y, r=5, c="currentColor"):
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>' % (x, y, r, c)

def line(x1, y1, x2, y2, c="currentColor", w=1.6, dash="", op=1):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s opacity="%s"/>'
            % (x1, y1, x2, y2, c, w, d, op))

# Nhãn đã đặt: (x, y, chuỗi, cỡ, anchor) — kiểm chồng chữ và mép trước khi ghi file.
LABELS = []

def T(x, y, s, c="currentColor", size=13, anchor="start", weight="600"):
    if "$" in s:
        raise SystemExit("SVG có dấu $: " + s)
    LABELS.append((x, y, s, size, anchor))
    return text(x, y, s, c, size, anchor, weight)

def _box(item):
    x, y, s, size, anchor = item
    w = 0.62 * size * len(s)
    h = size
    if anchor == "middle":
        x0 = x - w / 2
    elif anchor == "end":
        x0 = x - w
    else:
        x0 = x
    return (x0, y - h, x0 + w, y + 2)

def kiem_nhan(vb, ten):
    x0, y0, x1, y1 = (float(v) for v in vb.split())
    boxes = [_box(it) for it in LABELS]
    loi = []
    for (a, b, s, size, anchor), (bx0, by0, bx1, by1) in zip(LABELS, boxes):
        if bx0 < x0 + 4 or by0 < y0 + 2 or bx1 > x1 - 4 or by1 > y1 - 2:
            loi.append("mép %s: %r (%.0f,%.0f)-(%.0f,%.0f)" % (ten, s, bx0, by0, bx1, by1))
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            A, B = boxes[i], boxes[j]
            if A[0] < B[2] - 2 and B[0] < A[2] - 2 and A[1] < B[3] - 2 and B[1] < A[3] - 2:
                loi.append("chồng %s: %r và %r" % (ten, LABELS[i][2], LABELS[j][2]))
    if loi:
        print("\n".join(loi))
        sys.exit(1)
    LABELS.clear()

# ---------- Hình 1: xích đu ----------
PIV = (168, 36)
LL = 112
ANG = math.radians(42)
hx = PIV[0] - LL * math.sin(ANG)
hy = PIV[1] + LL * math.cos(ANG)
lx, ly = PIV[0], PIV[1] + LL
b = line(48, 36, 292, 36, "currentColor", 3)
b += line(48, 36, 62, 196, "currentColor", 3)
b += line(292, 36, 278, 196, "currentColor", 3)
b += line(36, 196, 400, 196, "currentColor", 2)
b += line(PIV[0], PIV[1], hx, hy, "currentColor", 2)
b += line(PIV[0], PIV[1], lx, ly, "currentColor", 2)
b += dot(hx, hy, 8, ORG) + dot(lx, ly, 8, BLUE)
arc = []
for i in range(0, 25):
    a = ANG * (1 - i / 24)
    arc.append((PIV[0] - (LL - 16) * math.sin(a), PIV[1] + (LL - 16) * math.cos(a)))
b += poly(arc, GRN, 2.2)
# đầu mũi tại chỗ thấp, hướng sang phải (đang lao về VTCB)
ax, ay = arc[-1]
b += '<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z" fill="%s"/>' % (
    ax + 9, ay, ax - 2, ay - 5, ax - 2, ay + 5, GRN)
b += T(hx - 10, hy - 16, "biên", ORG, 13, "end")
b += T(hx - 10, hy + 28, "v = 0", ORG, 12, "end")
b += T(lx + 14, ly - 8, "VTCB", BLUE, 13, "start")
b += T(lx + 14, ly + 14, "v lớn", BLUE, 12, "start")
b += T(300, 78, "lò xo cửa", ORG, 12, "start")
b += T(300, 148, "nam châm tủ", BLUE, 12, "start")
# lò xo nhỏ
zx = [300 + 8 * i for i in range(8)]
zy = [96 + (8 if i % 2 else -8) for i in range(8)]
b += poly(list(zip(zx, zy)), ORG, 2)
# hai cực nam châm, mũi hút vào nhau
b += '<rect x="300" y="162" width="28" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="1.6"/>'
b += '<rect x="346" y="162" width="28" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="1.6"/>'
b += T(314, 174, "N", "currentColor", 11, "middle")
b += T(360, 174, "S", "currentColor", 11, "middle")
b += line(330, 170, 344, 170, GRN, 2)
b += '<path d="M336,166 L344,170 L336,174 Z" fill="%s"/>' % GRN
fig1 = wrap("0 0 440 214",
            "Xích đu dừng ở biên và lao nhanh qua vị trí cân bằng; lò xo cửa và nam châm tủ cùng kiểu đổi năng lượng",
            b, "Hình 1. Ở biên đu dừng (thế năng lớn). Qua chỗ thấp thì nhanh (động năng lớn).")
kiem_nhan("0 0 440 214", "hình 1")

# ---------- Hình 2: parabol Et(x), Ed(x) ----------
OX, OY = 214, 222
HX, HY = 148, 160  # 1 đơn vị li độ = HX px; W = HY px
yW = OY - HY

def X(xn):
    return OX + HX * xn

def Yet(xn):
    return OY - HY * (xn * xn)

def Yed(xn):
    return OY - HY * (1 - xn * xn)

xs = [i / 80 for i in range(-80, 81)]
pet = [(X(u), Yet(u)) for u in xs]
ped = [(X(u), Yed(u)) for u in xs]
xi = 1 / math.sqrt(2)
# Kiểm toạ độ: parabol và giao A/√2
assert abs(Yet(0) - OY) < 1e-6 and abs(Yet(1) - yW) < 1e-6
assert abs(Yed(0) - yW) < 1e-6 and abs(Yed(1) - OY) < 1e-6
assert Yet(0) > Yet(1)          # Et lõm lên: đáy ở VTCB (thấp trên màn hình)
assert Yed(0) < Yed(1)          # Ed lõm xuống: đỉnh ở VTCB
assert abs(Yet(xi) - Yed(xi)) < 1e-6
assert abs(Yet(xi) - (OY - HY / 2)) < 1e-6
assert abs(X(xi) - (OX + HX / math.sqrt(2))) < 1e-6
# điểm lấy mẫu gần nhất phải nằm sát giao đúng
gan = min(pet, key=lambda p: (p[0] - X(xi)) ** 2 + (p[1] - Yet(xi)) ** 2)
assert math.hypot(gan[0] - X(xi), gan[1] - Yet(xi)) < 2.0, gan

b = line(X(-1) - 8, OY, X(1) + 18, OY, "currentColor", 1.6)
b += line(OX, OY + 8, OX, yW - 16, "currentColor", 1.6)
b += line(X(-1), yW, X(1), yW, GRN, 1.6, "5 4")
b += poly(pet, ORG)
b += poly(ped, BLUE)
for sgn in (-1, 1):
    b += line(X(sgn * xi), Yet(xi), X(sgn * xi), OY, "currentColor", 1.2, "3 3", 0.7)
    b += dot(X(sgn * xi), Yet(xi), 5, RED)
b += T(OX - 22, yW - 22, "E", "currentColor", 13, "end")
b += T(X(1) + 8, OY + 4, "x", "currentColor", 13, "start")
b += T(X(-1), OY + 20, "−A", "currentColor", 12, "middle")
b += T(OX, OY + 20, "0", "currentColor", 12, "middle")
b += T(X(1), OY + 20, "+A", "currentColor", 12, "middle")
b += T(X(-0.78), yW - 18, "W", GRN, 13, "middle")
b += T(X(0.16), yW + 28, "Ed", BLUE, 13, "start")
b += T(OX + 36, OY - 18, "Et", ORG, 13, "start")
b += T(X(1) + 10, Yet(xi) + 4, "A/√2", RED, 12, "start")
fig2 = wrap("0 0 440 252",
            "Đồ thị thế năng lõm lên và động năng lõm xuống theo li độ, cắt nhau tại cộng trừ A trên căn hai",
            b, "Hình 2. $E_t$ lõm lên, $E_d$ lõm xuống.<br>Cắt nhau tại x = ±A/√2.")
kiem_nhan("0 0 440 252", "hình 2")
print("giao phải px", round(X(xi), 1), round(Yet(xi), 1), "trái", round(X(-xi), 1))

# ---------- Hình 3: Et(t), Ed(t), W ----------
x0, x1 = 48, 392
y0, yW = 198, 46
span = y0 - yW

def Xt(tn):
    return x0 + (x1 - x0) * tn

def Ye(e):
    return y0 - span * e

pt, pd = [], []
for i in range(0, 121):
    tn = i / 120
    pt.append((Xt(tn), Ye(math.cos(2 * math.pi * tn) ** 2)))
    pd.append((Xt(tn), Ye(math.sin(2 * math.pi * tn) ** 2)))
# t = 0: Et = W, Ed = 0; t = T/4 đảo; t = T/2 Et trở lại; cắt tại T/8
assert abs(pt[0][1] - yW) < 1e-6 and abs(pd[0][1] - y0) < 1e-6
assert abs(pt[30][1] - y0) < 0.2 and abs(pd[30][1] - yW) < 0.2
assert abs(pt[60][1] - yW) < 0.2
assert abs(pt[15][1] - pd[15][1]) < 0.2
assert abs(pt[15][1] - Ye(0.5)) < 0.2

b = line(x0, y0, x1 + 16, y0, "currentColor", 1.6)
b += line(x0, y0 + 6, x0, yW - 14, "currentColor", 1.6)
b += line(x0, yW, x1, yW, GRN, 1.8)
b += poly(pd, BLUE)
b += poly(pt, ORG)
b += dot(Xt(0.125), Ye(0.5), 4.5, RED)
# đoạn T/2: từ đỉnh Et này sang đỉnh Et kế
b += line(Xt(0), y0 + 18, Xt(0.5), y0 + 18, GRN, 1.6)
b += '<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f" fill="none" stroke="%s" stroke-width="1.6"/>' % (
    Xt(0) + 7, y0 + 14, Xt(0), y0 + 18, Xt(0) + 7, y0 + 22, GRN)
b += '<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f" fill="none" stroke="%s" stroke-width="1.6"/>' % (
    Xt(0.5) - 7, y0 + 14, Xt(0.5), y0 + 18, Xt(0.5) - 7, y0 + 22, GRN)
b += T(x0 - 6, yW + 4, "E", "currentColor", 13, "end")
b += T(x1 + 8, y0 + 4, "t", "currentColor", 13, "start")
b += T(x1 - 4, yW - 8, "W", GRN, 13, "end")
b += T(x0 + 10, yW - 16, "Et", ORG, 12, "start")
b += T(Xt(0.25), yW + 48, "Ed", BLUE, 12, "middle")
b += T((Xt(0) + Xt(0.5)) / 2, y0 + 34, "T/2", GRN, 13, "middle")
fig3 = wrap("0 0 440 246",
            "Thế năng và động năng ngược pha, chu kì bằng nửa chu kì li độ; cơ năng là đường nằm ngang",
            b, "Hình 3. $E_t$ và $E_d$ ngược pha, chu kì $T/2$. $W$ là đường nằm ngang.")
kiem_nhan("0 0 440 246", "hình 3")

h = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3), 1):
    assert "<!--FIG%d-->" % n in h, n
    assert "$" not in f.split("<figcaption>")[0], n
    h = h.replace("<!--FIG%d-->" % n, f)
open("theory.html", "w", encoding="utf8").write(h)
print("ok", len(h))
