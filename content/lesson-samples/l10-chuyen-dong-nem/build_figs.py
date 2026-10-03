"""Sinh 4 hình SVG cho bài Chuyển động ném (Vật lí 10) và thay các mốc <!--FIGn--> trong theory.src.html.
Chạy: python3 build_figs.py   (từ thư mục bài)

Quy ước màu dùng chung cả bài: RED = vecto vận tốc (v₀, v) · BLUE = thành phần ngang vₓ ·
ORG = thành phần thẳng đứng vy, các điểm/thời điểm, đại lượng đo (h, L) · GRN = quỹ đạo.
"""
from svg_lib import *


def poly(pts, c, w=2.2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline fill="none" stroke="{c}" stroke-width="{w}"{d} opacity="{op}" points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>'


def dot(x, y, r=4.5, c="currentColor"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def seg(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def sub(x, y, base, s, c="currentColor", size=11, anchor="start", weight="700"):
    """Nhãn có chỉ số dưới: v + tspan nhỏ (không dùng KaTeX trong SVG)."""
    return (f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{base}<tspan dy="4" font-size="{size - 2}">{s}</tspan></text>')


# ================= Hình 1: đầu phun CNC — giọt phun ngang và giọt rơi thẳng =================
X0, Y0 = 44, 65          # miệng đầu phun
XL, YL = 380, 210        # điểm chạm máng
W = XL - X0
b = defs("f1")
b += f'<rect x="20" y="56" width="24" height="15" fill="none" stroke="currentColor" stroke-width="2"/>'
b += text(20, 50, "đầu phun", "currentColor", 11, "start", "400")
b += arrow("f1", "r", X0, Y0, X0 + 58, Y0, 3)
b += text(X0 + 62, Y0 - 7, "v₀", RED, 12, "start", "700")
# tia nước (parabol)
jet = [(X0 + W * u / 40, Y0 + (YL - Y0) * (u / 40) ** 2) for u in range(0, 41)]
b += poly(jet, GRN, 2.4)
# giọt rơi thẳng từ cùng độ cao
b += seg(X0, Y0, X0, YL - 2, ORG, 1.8, "5 4", .8)
for u in (0.4, 0.6, 0.8, 1.0):
    xj = X0 + W * u
    yj = Y0 + (YL - Y0) * u * u
    b += dot(xj, yj, 4.2, GRN)
    b += dot(X0, yj, 4.2, ORG)
    if u < 1:
        b += seg(X0 + 6, yj, xj - 6, yj, "currentColor", 1.1, "4 4", .35)
b += text(150, 54, "tia phun ngang", GRN, 11, "start", "400")
b += text(96, 200, "giọt rơi thẳng", ORG, 11, "start", "400")
b += f'<rect x="20" y="208" width="400" height="9" fill="none" stroke="currentColor" stroke-width="2"/>'
b += text(20, 240, "máng hứng", "currentColor", 11, "start", "400")
fig1 = wrap("0 0 440 250",
            "Đầu phun dung dịch làm mát bắn tia ngang; giọt phun ngang và giọt rơi thẳng từ cùng độ cao luôn nằm ngang nhau",
            b,
            "Hình 1. Tia phun ngang cong dần thành parabol. Giọt phun ngang (xanh) và giọt rơi thẳng (cam) <strong>luôn ngang nhau</strong>: cùng hàng thì cùng lúc tới máng.")

# ================= Hình 2: hệ trục Oxy, quỹ đạo và hai chuyển động thành phần =================
OX, OY = 40, 40          # gốc toạ độ
XEND, YEND = 300, 205
b = defs("f2")
b += arrow("f2", "r", OX, OY, OX + 58, OY, 3)
b += text(OX + 62, OY - 4, "v₀", RED, 12, "start", "700")
b += seg(OX, OY, 352, OY, "currentColor", 1.6)          # Ox
b += seg(OX, OY, OX, 226, "currentColor", 1.6)          # Oy
b += text(358, OY + 5, "x", "currentColor", 12, "start", "700")
b += text(OX - 20, 224, "y", "currentColor", 12, "start", "700")
b += text(OX - 20, OY - 6, "O", "currentColor", 12, "start", "700")
curve = [(OX + (XEND - OX) * u / 40, OY + (YEND - OY) * (u / 40) ** 2) for u in range(0, 41)]
b += poly(curve, GRN, 2.6)
xs = [OX + (XEND - OX) * k / 5 for k in range(6)]
for k, (x, y) in enumerate(zip(xs[1:], [OY + (YEND - OY) * (k / 5) ** 2 for k in range(1, 6)]), 1):
    b += seg(x, OY - 5, x, OY + 5, "currentColor", 1.4)
    b += dot(x, y, 4.2, ORG)
ys = [OY] + [OY + (YEND - OY) * (k / 5) ** 2 for k in range(1, 6)]
for y in ys[1:]:
    b += seg(OX - 5, y, OX + 5, y, "currentColor", 1.4)
b += text(140, 16, "Ox: mỗi khoảng thời gian bằng nhau", "currentColor", 11, "start", "400")
b += text(140, 30, "→ đoạn ngang bằng nhau", "currentColor", 11, "start", "400")
b += text(20, 246, "Oy: các đoạn rơi tăng theo tỉ lệ 1 : 3 : 5 : 7 : 9", "currentColor", 11, "start", "400")
b += text(20, 262, "→ quỹ đạo là một phần parabol", GRN, 11, "start", "700")
fig2 = wrap("0 0 440 272",
            "Hệ trục Oxy: theo Ox các đoạn bằng nhau sau những khoảng thời gian bằng nhau, theo Oy các đoạn rơi tăng dần theo tỉ lệ 1:3:5:7:9, nên quỹ đạo là parabol",
            b,
            "Hình 2. Chọn Ox ngang, Oy thẳng đứng hướng xuống. Sau những khoảng thời gian bằng nhau, vật đi được <strong>đoạn ngang bằng nhau</strong> (Ox thẳng đều) nhưng <strong>đoạn rơi tăng dần 1 : 3 : 5 : 7 : 9</strong> (Oy rơi tự do). Ghép hai chuyển động đó lại thành quỹ đạo parabol.")

# ================= Hình 3: cùng độ cao, hai vận tốc ném =================
O3X, O3Y, G3 = 40, 45, 200
b = defs("f3")
b += seg(20, G3, 420, G3, "currentColor", 1.8)
b += arrow("f3", "r", O3X, O3Y, O3X + 150, O3Y, 3)
b += arrow("f3", "r", O3X, O3Y, O3X + 52, O3Y, 3)
b += text(O3X + 156, O3Y - 9, "v₀ = 4,5 m/s", RED, 11, "start", "700")
b += text(O3X + 58, O3Y - 9, "v₀ = 1,5 m/s", RED, 11, "start", "700")
for xend, c in ((170, GRN), (360, GRN)):
    pts = [(O3X + (xend - O3X) * u / 40, O3Y + (G3 - O3Y) * (u / 40) ** 2) for u in range(0, 41)]
    b += poly(pts, c, 2.4)
b += dot(170, G3, 5, ORG) + dot(360, G3, 5, ORG)
b += seg(O3X, O3Y, O3X, G3 - 6, ORG, 1.8, "5 4", .85)
b += text(O3X + 6, 104, "h = 0,80 m", ORG, 11, "start", "700")
for x1, x2, yb, lab in ((O3X, 170, 212, "L = 0,61 m"), (O3X, 360, 236, "L = 1,82 m")):
    b += seg(x1, yb, x2, yb, ORG, 1.4)
    b += seg(x1, yb - 4, x1, yb + 4, ORG, 1.4) + seg(x2, yb - 4, x2, yb + 4, ORG, 1.4)
    b += text((x1 + x2) / 2, yb + 15, lab, ORG, 11, "middle", "700")
b += text(20, 18, "cùng độ cao h → cùng thời gian rơi t = 0,404 s", "currentColor", 11, "start", "400")
b += text(20, 268, "v₀ lớn hơn → tầm xa lớn hơn, thời gian rơi không đổi", "currentColor", 11, "start", "400")
fig3 = wrap("0 0 440 280",
            "Hai vật ném ngang từ cùng độ cao với vận tốc khác nhau: cùng thời gian rơi, tầm xa tỉ lệ với vận tốc ném",
            b,
            "Hình 3. Cùng độ cao $h=0{,}80$ m nên cùng thời gian rơi 0,404 s. Vận tốc ném gấp ba thì tầm xa gấp ba (0,61 m so với 1,82 m) — <strong>vận tốc ném không làm đổi thời gian rơi</strong>.")

# ================= Hình 4: vecto vận tốc tại ba thời điểm =================
O4X, O4Y = 40, 40
US = (0.35, 0.62, 0.9)
PX = lambda u: O4X + 300 * u
PY = lambda u: O4Y + 135 * u * u
VX = 52
VY = {0.35: 22, 0.62: 40, 0.9: 56}
b = defs("f4")
b += seg(O4X, O4Y, 400, O4Y, "currentColor", 1.2, "5 4", .5)
curve = [(PX(u / 40), PY(u / 40)) for u in range(0, 41)]
b += poly(curve, GRN, 2.4, "", .55)
pts = [(PX(u), PY(u)) for u in US]
for u, (x, y) in zip(US, pts):
    b += arrow("f4", "b", x, y, x + VX, y, 2.6)
    b += arrow("f4", "o", x, y, x, y + VY[u], 2.6)
    b += arrow("f4", "r", x, y, x + VX, y + VY[u], 2.6)
    b += dot(x, y, 4.2, ORG)
# đường hoàn thiện hình bình hành ở điểm cuối
xe, ye = pts[-1][0] + VX, pts[-1][1] + VY[0.9]
b += seg(pts[-1][0] + VX, pts[-1][1], xe, ye, "currentColor", 1.1, "4 4", .35)
b += seg(pts[-1][0], pts[-1][1] + VY[0.9], xe, ye, "currentColor", 1.1, "4 4", .35)
b += sub(pts[0][0] + 20, pts[0][1] - 8, "v", "x", BLUE)
b += sub(pts[0][0] - 22, pts[0][1] + VY[0.35] + 18, "v", "y", ORG)
b += text(xe + 6, ye + 2, "v", RED, 12, "start", "700")
b += text(20, 240, "Thành phần ngang không đổi · thành phần đứng lớn dần", "currentColor", 11, "start", "400")
b += text(20, 256, "v là tổng hai vectơ vuông góc", "currentColor", 11, "start", "400")
fig4 = wrap("0 0 440 268",
            "Ba thời điểm trên quỹ đạo: thành phần ngang không đổi, thành phần thẳng đứng lớn dần, vecto vận tốc tổng hợp là tổng hai vectơ vuông góc",
            b,
            "Hình 4. Trên đường parabol: $v_x$ (xanh) <strong>không đổi</strong>, $v_y$ (cam) <strong>lớn dần</strong>, còn $\\vec v$ (đỏ) là tổng hai vectơ vuông góc nên $v=\\sqrt{v_0^2+(gt)^2}$ và ngày càng dốc xuống.")

h = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, f"thiếu mốc FIG{n}"
    h = h.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(h)
print("ok", len(h), "bytes,", h.count('<figure class="fig"'), "hình")
