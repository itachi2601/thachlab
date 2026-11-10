"""Sinh 3 hình SVG cho bài cơ năng dao động và thay <!--FIGn--> trong theory.src.html."""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
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

# Rà soát 30/10/2026: vẽ lại cả 3 hình — chữ 15 (≥ 14), đầu mũi tên V 30° (không tam giác đặc),
# trục có đầu V, nhãn tách khỏi nét.
FS = 15


def chevron(x, y, dx, dy, c="currentColor", w=2, L=11, ang=30):
    """Đầu V tại (x, y) hướng (dx, dy), hai vạch lệch ang° (bản sao svg_lib của skill)."""
    n = math.hypot(dx, dy) or 1
    ux, uy = dx / n, dy / n
    t = math.radians(ang)
    pts = []
    for s in (1, -1):
        c_, s_ = math.cos(t), math.sin(s * t)
        bx, by = ux * c_ - uy * s_, ux * s_ + uy * c_
        pts.append((x - L * bx, y - L * by))
    (ax, ay), (bx, by) = pts
    return ('<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f" fill="none" stroke="%s" stroke-width="%s" '
            'stroke-linejoin="miter" stroke-miterlimit="10"/>' % (ax, ay, x, y, bx, by, c, w))


def axis(x1, y1, x2, y2):
    return line(x1, y1, x2, y2, "currentColor", 1.6) + chevron(x2, y2, x2 - x1, y2 - y1, "currentColor", 1.6, 10)


# ---------- Hình 1: xích đu + lò xo cửa + nam châm tủ ----------
PIV = (145, 30)
LL = 130
ANG = math.radians(40)
GROUND = 222


def seat_at(a):
    """Điểm treo ghế khi dây lệch góc a (a < 0: lệch trái)."""
    return PIV[0] + LL * math.sin(a), PIV[1] + LL * math.cos(a)


def seat(a, c, op=1):
    px, py = seat_at(a)
    ux, uy = math.cos(a), -math.sin(a)          # vuông góc với dây
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="7" stroke-linecap="round" opacity="%s"/>'
            % (px - 15 * ux, py - 15 * uy, px + 15 * ux, py + 15 * uy, c, op))


hx, hy = seat_at(-ANG)
lx, ly = seat_at(0)
rx, ry = seat_at(ANG)
assert abs(lx - PIV[0]) < 1e-9 and abs(ly - (PIV[1] + LL)) < 1e-9
assert hy < ly and abs(hy - ry) < 1e-9          # biên cao hơn VTCB, hai biên đối xứng
# khung xích đu
b = line(28, 30, 262, 30, "currentColor", 3.2)
b += line(40, 30, 26, GROUND, "currentColor", 3)
b += line(250, 30, 264, GROUND, "currentColor", 3)
b += line(14, GROUND, 276, GROUND, "currentColor", 2)
# quỹ đạo ghế (nét đứt mờ) từ biên trái sang biên phải
b += poly([seat_at(-ANG + 2 * ANG * i / 40) for i in range(41)], "currentColor", 1.2).replace(
    "/>", ' stroke-dasharray="4 4" opacity="0.45"/>')
# dây + ghế: biên phải mờ, biên trái và VTCB rõ
b += line(PIV[0], PIV[1], rx, ry, "currentColor", 1.6, "4 4", 0.4) + seat(ANG, "currentColor", 0.3)
b += line(PIV[0], PIV[1], hx, hy, "currentColor", 2) + seat(-ANG, ORG)
b += line(PIV[0], PIV[1], lx, ly, "currentColor", 2) + seat(0, BLUE)
b += dot(PIV[0], PIV[1], 4)
# mũi tên chuyển động: cung bên trong, từ gần biên trái về gần VTCB, đầu V hướng sang phải-xuống
R_IN = LL - 22
arc = [(PIV[0] + R_IN * math.sin(a), PIV[1] + R_IN * math.cos(a))
       for a in (-ANG + 0.12 + (ANG - 0.30) * i / 24 for i in range(25))]
b += poly(arc, GRN, 2.4)
(ax_, ay_), (bx_, by_) = arc[-2], arc[-1]
assert bx_ > ax_ and by_ > ay_                  # đang đi sang phải, xuống thấp: về VTCB
b += chevron(bx_, by_, bx_ - ax_, by_ - ay_, GRN, 2.4, 11)
b += T(hx - 4, hy + 38, "biên", ORG, FS, "middle")
b += T(hx - 4, hy + 56, "v = 0", ORG, FS, "middle")
b += T(lx, ly + 30, "VTCB", BLUE, FS, "middle")
b += T(lx, ly + 48, "v lớn nhất", BLUE, FS, "middle")
# lò xo cửa: tường — lò xo — mép cửa; buông tay thì cửa bị kéo về tường
b += T(296, 40, "lò xo cửa", ORG, FS, "start")
b += line(298, 56, 298, 112, "currentColor", 3)
for yy in range(60, 112, 10):
    b += line(298, yy, 290, yy + 8, "currentColor", 1.2)
zz = [(298, 84)] + [(306 + 7 * i, 84 + (7 if i % 2 else -7)) for i in range(8)] + [(366, 84)]
b += poly(zz, ORG, 2)
b += '<rect x="366" y="60" width="12" height="48" rx="2" fill="none" stroke="currentColor" stroke-width="2"/>'
b += line(424, 128, 372, 128, GRN, 2.2) + chevron(372, 128, -1, 0, GRN, 2.2, 10)
b += T(382, 150, "buông: sập", GRN, FS, "middle")
# nam châm tủ: N và S đối diện, hút nhau (hai mũi tên chĩa vào nhau)
b += T(296, 180, "nam châm tủ", BLUE, FS, "start")
b += '<rect x="296" y="190" width="34" height="22" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/>'
b += '<rect x="400" y="190" width="34" height="22" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/>'
b += T(313, 207, "N", "currentColor", FS, "middle")
b += T(417, 207, "S", "currentColor", FS, "middle")
b += line(336, 201, 360, 201, GRN, 2.2) + chevron(360, 201, 1, 0, GRN, 2.2, 9)
b += line(394, 201, 370, 201, GRN, 2.2) + chevron(370, 201, -1, 0, GRN, 2.2, 9)
b += T(365, 234, "hút nhau", GRN, FS, "middle")
VB1 = "0 0 440 244"
fig1 = wrap(VB1,
            "Xích đu dừng ở biên và lao nhanh qua vị trí cân bằng; lò xo cửa và nam châm tủ cùng kiểu đổi năng lượng",
            b, "Hình 1. Ở biên đu dừng (thế năng lớn). Qua chỗ thấp thì nhanh (động năng lớn).")
kiem_nhan(VB1, "hình 1")

# ---------- Hình 2 (Hình 3 trong bài): parabol Et(x), Ed(x) ----------
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
gan = min(pet, key=lambda p: (p[0] - X(xi)) ** 2 + (p[1] - Yet(xi)) ** 2)
assert math.hypot(gan[0] - X(xi), gan[1] - Yet(xi)) < 2.0, gan

b = axis(X(-1) - 10, OY, X(1) + 34, OY)
b += axis(OX, OY + 8, OX, yW - 28)
b += line(X(-1), yW, X(1), yW, GRN, 1.6, "5 4")
b += poly(pet, ORG, 2.6)
b += poly(ped, BLUE, 2.6)
for sgn in (-1, 1):
    b += line(X(sgn * xi), Yet(xi), X(sgn * xi), OY, "currentColor", 1.2, "3 3", 0.7)
    b += dot(X(sgn * xi), Yet(xi), 5, RED)
b += T(OX + 10, yW - 18, "E", "currentColor", FS, "start")
b += T(X(1) + 38, OY + 5, "x", "currentColor", FS, "start")
b += T(X(-1), OY + 24, "−A", "currentColor", FS, "middle")
b += T(OX, OY + 24, "0", "currentColor", FS, "middle")
b += T(X(1), OY + 24, "+A", "currentColor", FS, "middle")
b += T(X(1) + 10, yW + 5, "W", GRN, FS, "start")
b += T(X(0.22), yW + 36, "Ed", BLUE, FS, "middle")
b += T(X(0.86) + 16, Yet(0.86) + 6, "Et", ORG, FS, "start")
b += T(X(-xi), OY + 24, "−A/√2", RED, FS, "middle")
b += T(X(xi), OY + 24, "A/√2", RED, FS, "middle")
# nhãn Ed nằm dưới đỉnh Ed và trên đáy Et: cách cả hai đường ≥ 10 px
assert Yed(0.22) + 10 < yW + 36 - FS and yW + 36 + 10 < Yet(0.22)
VB2 = "0 0 440 256"
fig2 = wrap(VB2,
            "Đồ thị thế năng lõm lên và động năng lõm xuống theo li độ, cắt nhau tại cộng trừ A trên căn hai",
            b, "Hình 3. $E_t$ lõm lên, $E_d$ lõm xuống.<br>Cắt nhau tại x = ±A/√2.")
kiem_nhan(VB2, "hình 2")

# ---------- Hình 3 (Hình 4 trong bài): Et(t), Ed(t), W ----------
x0, x1 = 48, 392
y0, yW = 206, 54
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

b = axis(x0, y0, x1 + 22, y0)
b += axis(x0, y0 + 6, x0, yW - 30)
b += line(x0, yW, x1, yW, GRN, 1.8)
b += poly(pd, BLUE, 2.6)
b += poly(pt, ORG, 2.6)
b += dot(Xt(0.125), Ye(0.5), 5, RED)
# đoạn T/2: từ đỉnh Et này sang đỉnh Et kế
yb = y0 + 22
b += line(Xt(0), yb, Xt(0.5), yb, GRN, 1.6)
b += chevron(Xt(0), yb, -1, 0, GRN, 1.6, 9) + chevron(Xt(0.5), yb, 1, 0, GRN, 1.6, 9)
b += line(Xt(0.5), y0, Xt(0.5), y0 + 6, "currentColor", 1.4) + line(Xt(1), y0, Xt(1), y0 + 6, "currentColor", 1.4)
b += T(x0 + 10, yW - 22, "E", "currentColor", FS, "start")
b += T(x1 + 28, y0 + 5, "t", "currentColor", FS, "start")
b += T(x1, yW - 8, "W", GRN, FS, "end")
b += T(Xt(1), y0 + 24, "T", "currentColor", FS, "middle")
b += T((Xt(0) + Xt(0.5)) / 2, yb + 20, "T/2", GRN, FS, "middle")
# Et: phía trên nhánh Et đi xuống ngay sau t = 0; Ed: phía trên nhánh Ed đi xuống sau đỉnh T/4
b += T(Xt(0.085), Ye(0.84), "Et", ORG, FS, "start")
b += T(Xt(0.33), Ye(0.84), "Ed", BLUE, FS, "start")
b += T(Xt(0.125) + 12, Ye(0.5) + 5, "Et = Ed", RED, FS, "start")
for tn in (0.085, 0.085 + 18 / (x1 - x0)):     # nhãn Et cao hơn đường Et ≥ 8 px
    assert Ye(math.cos(2 * math.pi * tn) ** 2) > Ye(0.84) + 8, tn
for tn in (0.33, 0.33 + 18 / (x1 - x0)):       # nhãn Ed cao hơn đường Ed ≥ 8 px
    assert Ye(math.sin(2 * math.pi * tn) ** 2) > Ye(0.84) + 8, tn
VB3 = "0 0 440 256"
fig3 = wrap(VB3,
            "Thế năng và động năng ngược pha, chu kì bằng nửa chu kì li độ; cơ năng là đường nằm ngang",
            b, "Hình 4. $E_t$ và $E_d$ ngược pha, chu kì $T/2$. $W$ là đường nằm ngang.")
kiem_nhan(VB3, "hình 3")

# Ảnh OpenStax College Physics 2e (28/10/2026): THÊM Hình 16.14 trước hai đồ thị, xem nguon.md
figos = (
    '<figure class="fig"><img src="/assets/openstax/l11-co-nang-dao-dong/hinh-bien-doi-nang-luong-lo-xo.webp" alt="Khối m gắn lò xo trên mặt không ma sát ở năm vị trí: biên x = X (v = 0), qua x = 0 (v âm cực đại), biên x = −X (v = 0), qua x = 0 (v cực đại), lại biên x = X; ghi kèm năng lượng ở mỗi vị trí" loading="lazy" width="875" height="550">'
    '<figcaption>Hình 2. a, c, e: biên, <em>v</em> = 0, thế năng ½<em>kX</em>².<br>b, d: <em>x</em> = 0, |<em>v</em>| cực đại, động năng ½<em>mv</em><sub>max</sub>².<br>Sách: <em>X</em> = <em>A</em>.<br>'
    '<small>Hình: OpenStax, College Physics 2e, Hình 16.14 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>')

h = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3), 1):
    assert "<!--FIG%d-->" % n in h, n
    assert "$" not in f.split("<figcaption>")[0], n
    h = h.replace("<!--FIG%d-->" % n, f)
h = h.replace("<!--FIGOS-->", figos)
open("theory.html", "w", encoding="utf8").write(margin_figs(h))
print("ok", len(h))
