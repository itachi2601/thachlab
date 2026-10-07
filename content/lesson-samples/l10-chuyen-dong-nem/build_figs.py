"""Sinh 6 hình SVG cho bài Chuyển động ném (Vật lí 10) và thay các mốc <!--FIGn--> trong theory.src.html.
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


def sub(x, y, base, s, c="currentColor", size=14, anchor="start", weight="700"):
    """Nhãn có chỉ số dưới: v + tspan nhỏ (không dùng KaTeX trong SVG)."""
    return (f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{base}<tspan dy="4" font-size="{size - 3}">{s}</tspan></text>')


# ================= Hình 1: máy bay cứu hộ thả gói hàng =================
Y0 = 67                  # độ cao thả: đáy khoang máy bay và đáy trực thăng
XL, YL = 300, 206        # gói của máy bay chạm đất
XH = 350                 # trực thăng đứng yên, thả gói rơi thẳng đứng
b = defs("f1")
# máy bay (nhìn nghiêng, kiểu que)
pl = '<rect x="26" y="56" width="58" height="11" rx="5" fill="none" stroke="currentColor" stroke-width="2.5"/>'
pl += '<path d="M34,56 L26,46 L26,56 Z" fill="none" stroke="currentColor" stroke-width="2"/>'
pl += seg(54, 67, 45, 78, "currentColor", 2.2)
pl += '<circle cx="73" cy="61" r="3" fill="none" stroke="currentColor" stroke-width="1.6"/>'
b += text(24, 36, "máy bay cứu hộ", "currentColor", 14, "start", "400")
pl += arrow("f1", "r", 70, Y0, 128, Y0, 3)
pl += text(132, Y0 - 4, "v₀", RED, 14, "start", "700")
NS = 40; DUR = 4.0   # mô phỏng thu gọn: 40 mẫu cách đều thời gian, chạy 1 lần khi bấm nút
def smil(attr, vals):
    return f'<animate attributeName="{attr}" values="{";".join(f"{v:.1f}" for v in vals)}" dur="{DUR}s" begin="indefinite" fill="freeze"/>'
tr = ";".join(f"{(XL - 70) * u / NS:.1f} 0" for u in range(NS + 1))
b += f'<g><animateTransform attributeName="transform" type="translate" values="{tr}" dur="{DUR}s" begin="indefinite" fill="freeze"/>{pl}</g>'
# quỹ đạo gói hàng thả từ máy bay
par = [(70 + (XL - 70) * u / 40, Y0 + (YL - Y0) * (u / 40) ** 2) for u in range(0, 41)]
b += poly(par, GRN, 2.4)
# trực thăng đứng yên ở cùng độ cao
b += seg(XH - 16, 46, XH + 16, 46, "currentColor", 2.2)                      # cánh quạt chính
b += seg(XH, 46, XH, 52, "currentColor", 2)                                  # trục quạt
b += f'<rect x="{XH - 13}" y="52" width="26" height="13" rx="6" fill="none" stroke="currentColor" stroke-width="2.5"/>'
b += seg(XH - 13, 58, XH - 30, 53, "currentColor", 2)                        # đuôi
b += f'<circle cx="{XH - 30}" cy="53" r="3" fill="none" stroke="currentColor" stroke-width="1.6"/>'
b += seg(XH - 12, 74, XH + 12, 74, "currentColor", 2)                        # thanh trượt
b += seg(XH - 8, 65, XH - 8, 74, "currentColor", 1.4) + seg(XH + 8, 65, XH + 8, 74, "currentColor", 1.4)
b += text(432, 36, "trực thăng đứng yên", "currentColor", 14, "end", "400")
# các vị trí sau những khoảng thời gian bằng nhau
b += seg(XH, Y0, XH, YL - 2, ORG, 1.8, "5 4", .85)
for u in (0.4, 0.6, 0.8, 1.0):
    xj = 70 + (XL - 70) * u
    yj = Y0 + (YL - Y0) * u * u
    b += dot(xj, yj, 4.2, GRN)
    b += dot(XH, yj, 4.2, ORG)
    if u < 1:
        b += seg(xj + 6, yj, XH - 6, yj, "currentColor", 1.1, "4 4", .35)
PA = [(70 + (XL - 70) * u / NS, Y0 + (YL - Y0) * (u / NS) ** 2) for u in range(NS + 1)]
b += f'<circle cx="70" cy="{Y0}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">{smil("cx", [p[0] for p in PA])}{smil("cy", [p[1] for p in PA])}</circle>'
b += f'<circle cx="{XH}" cy="{Y0}" r="5.5" fill="{ORG}" stroke="currentColor" stroke-width="1.5">{smil("cy", [p[1] for p in PA])}</circle>'
b += text(150, 16, "cùng độ cao, cùng lúc", "currentColor", 14, "start", "400")
b += '<rect x="20" y="206" width="400" height="9" fill="none" stroke="currentColor" stroke-width="2"/>'
b += text(20, 238, "mặt đất", "currentColor", 14, "start", "400")
fig1 = wrap("0 0 440 250",
            "Máy bay cứu hộ bay ngang thả gói hàng rơi theo parabol; trực thăng đứng yên thả gói rơi thẳng đứng từ cùng độ cao, hai gói luôn nằm ngang nhau",
            b,
            "Hình 1. Gói thả từ máy bay rơi theo parabol (xanh), gói thả từ trực thăng rơi thẳng đứng (cam). Hai gói <strong>luôn ngang nhau</strong>: cùng hàng thì cùng lúc chạm đất.")

# ================= Hình 2: hệ trục Oxy, quỹ đạo và hai chuyển động thành phần =================
OX, OY = 40, 40          # gốc toạ độ
XEND, YEND = 300, 205
b = defs("f2")
b += arrow("f2", "r", OX, OY, OX + 58, OY, 3)
b += text(OX + 62, OY - 4, "v₀", RED, 14, "start", "700")
b += seg(OX, OY, 352, OY, "currentColor", 1.6)          # Ox
b += seg(OX, OY, OX, 226, "currentColor", 1.6)          # Oy
b += text(358, OY + 5, "x", "currentColor", 14, "start", "700")
b += text(OX - 20, 224, "y", "currentColor", 14, "start", "700")
b += text(OX - 20, OY - 6, "O", "currentColor", 14, "start", "700")
curve = [(OX + (XEND - OX) * u / 40, OY + (YEND - OY) * (u / 40) ** 2) for u in range(0, 41)]
b += poly(curve, GRN, 2.6)
xs = [OX + (XEND - OX) * k / 5 for k in range(6)]
for k, (x, y) in enumerate(zip(xs[1:], [OY + (YEND - OY) * (k / 5) ** 2 for k in range(1, 6)]), 1):
    b += seg(x, OY - 5, x, OY + 5, "currentColor", 1.4)
    b += dot(x, y, 4.2, ORG)
ys = [OY] + [OY + (YEND - OY) * (k / 5) ** 2 for k in range(1, 6)]
for y in ys[1:]:
    b += seg(OX - 5, y, OX + 5, y, "currentColor", 1.4)
b += text(140, 16, "Ox: mỗi khoảng thời gian bằng nhau", "currentColor", 14, "start", "400")
b += text(140, 32, "→ đoạn ngang bằng nhau", "currentColor", 14, "start", "400")
b += text(20, 248, "Oy: các đoạn rơi tăng theo tỉ lệ 1 : 3 : 5 : 7 : 9", "currentColor", 14, "start", "400")
b += text(20, 267, "→ quỹ đạo là một phần parabol", GRN, 14, "start", "700")
fig2 = wrap("0 0 440 278",
            "Hệ trục Oxy: theo Ox các đoạn bằng nhau sau những khoảng thời gian bằng nhau, theo Oy các đoạn rơi tăng dần theo tỉ lệ 1:3:5:7:9, nên quỹ đạo là parabol",
            b,
            "Hình 2. Chọn Ox ngang, Oy thẳng đứng hướng xuống. Sau những khoảng thời gian bằng nhau, vật đi được <strong>đoạn ngang bằng nhau</strong> (Ox thẳng đều) nhưng <strong>đoạn rơi tăng dần 1 : 3 : 5 : 7 : 9</strong> (Oy rơi tự do). Ghép hai chuyển động đó lại thành quỹ đạo parabol.")

# ================= Hình 3: cùng độ cao, hai vận tốc ném =================
O3X, O3Y, G3 = 40, 45, 200
b = defs("f3")
b += seg(20, G3, 420, G3, "currentColor", 1.8)
b += arrow("f3", "r", O3X, O3Y, O3X + 150, O3Y, 3)
b += arrow("f3", "r", O3X, O3Y, O3X + 50, O3Y, 3)
b += text(O3X + 160, O3Y - 12, "v₀ = 4,5 m/s", RED, 14, "start", "700")
b += text(O3X + 56, O3Y - 12, "v₀ = 1,5 m/s", RED, 14, "start", "700")
for xend, c in ((150, GRN), (370, GRN)):  # tầm xa 110 : 330 = 1 : 3 đúng tỉ lệ vận tốc
    pts = [(O3X + (xend - O3X) * u / 40, O3Y + (G3 - O3Y) * (u / 40) ** 2) for u in range(0, 41)]
    b += poly(pts, c, 2.4)
b += dot(150, G3, 5, ORG) + dot(370, G3, 5, ORG)
b += seg(O3X, O3Y, O3X, G3 - 6, ORG, 1.8, "5 4", .85)
b += text(O3X + 6, 182, "h = 0,80 m", ORG, 14, "start", "700")
for x1, x2, yb, lab in ((O3X, 150, 212, "L = 0,61 m"), (O3X, 370, 236, "L = 1,82 m")):
    b += seg(x1, yb, x2, yb, ORG, 1.4)
    b += seg(x1, yb - 4, x1, yb + 4, ORG, 1.4) + seg(x2, yb - 4, x2, yb + 4, ORG, 1.4)
    b += text((x1 + x2) / 2, yb + 15, lab, ORG, 14, "middle", "700")
b += text(20, 16, "cùng độ cao h → cùng thời gian rơi t = 0,404 s", "currentColor", 14, "start", "400")
b += text(20, 274, "v₀ lớn hơn → tầm xa lớn hơn, thời gian rơi không đổi", "currentColor", 14, "start", "400")
fig3 = wrap("0 0 440 286",
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
b += sub(pts[0][0] + 20, pts[0][1] - 20, "v", "x", BLUE)
b += sub(pts[0][0] - 22, pts[0][1] + VY[0.35] + 18, "v", "y", ORG)
b += text(xe + 6, ye + 2, "v", RED, 14, "start", "700")
b += text(20, 244, "Thành phần ngang không đổi · thành phần đứng lớn dần", "currentColor", 14, "start", "400")
b += text(20, 263, "v là tổng hai vectơ vuông góc", "currentColor", 14, "start", "400")
fig4 = wrap("0 0 440 274",
            "Ba thời điểm trên quỹ đạo: thành phần ngang không đổi, thành phần thẳng đứng lớn dần, vecto vận tốc tổng hợp là tổng hai vectơ vuông góc",
            b,
            "Hình 4. Trên đường parabol: $v_x$ (xanh) <strong>không đổi</strong>, $v_y$ (cam) <strong>lớn dần</strong>, còn $\\vec v$ (đỏ) là tổng hai vectơ vuông góc nên $v=\\sqrt{v_0^2+(gt)^2}$ và ngày càng dốc xuống.")

# ================= Hình 5: ném xiên từ mặt đất — tách v₀, đỉnh, tầm cao, tầm xa =================
G5, O5X, L5, H5 = 200, 50, 340, 130
b = defs("f5")
b += seg(20, G5, 420, G5, "currentColor", 1.8)
par5 = [(O5X + L5 * u / 40, G5 - 4 * H5 * (u / 40) * (1 - u / 40)) for u in range(0, 41)]
b += poly(par5, GRN, 2.5)
VX5, VY5 = 43.6, 67.0                                    # tan(alpha) = 4H/L = 1,53 (khoảng 57°)
b += arrow("f5", "r", O5X, G5, O5X + VX5, G5 - VY5, 3)
b += arrow("f5", "b", O5X, G5, O5X + VX5, G5, 2.6)
b += arrow("f5", "o", O5X, G5, O5X, G5 - VY5, 2.6)
b += seg(O5X + VX5, G5 - VY5, O5X + VX5, G5, "currentColor", 1.1, "4 4", .35)
b += seg(O5X, G5 - VY5, O5X + VX5, G5 - VY5, "currentColor", 1.1, "4 4", .35)
b += text(O5X + 14, G5 - VY5 - 8, "v₀", RED, 14, "start", "700")
b += sub(O5X + VX5 - 12, G5 + 17, "v", "0x", BLUE)
b += sub(O5X - 8, G5 - VY5 + 24, "v", "0y", ORG, 14, "end")
b += text(O5X + 32, G5 - 6, "α", "currentColor", 14, "start", "700")
AX = O5X + L5 / 2
b += dot(AX, G5 - H5, 4.5, ORG)
b += seg(AX, G5 - H5, AX, G5, ORG, 1.6, "5 4", .9)
b += text(AX + 8, G5 - H5 / 2, "tầm cao H", ORG, 14, "start", "700")
b += arrow("f5", "r", AX, G5 - H5, AX + 44, G5 - H5, 3)
b += text(AX + 50, G5 - H5 - 4, "v nằm ngang", RED, 14, "start", "700")
b += text(AX, 34, "đỉnh: không còn thành phần đứng", "currentColor", 14, "middle", "400")
b += dot(O5X, G5, 4.5, ORG) + dot(O5X + L5, G5, 4.5, ORG)
b += seg(O5X, 226, O5X + L5, 226, ORG, 1.4)
b += seg(O5X, 222, O5X, 230, ORG, 1.4) + seg(O5X + L5, 222, O5X + L5, 230, ORG, 1.4)
b += text(AX, 246, "tầm xa L", ORG, 14, "middle", "700")
fig5 = wrap("0 0 440 256",
            "Ném xiên từ mặt đất: vận tốc đầu tách thành thành phần ngang và thẳng đứng, tại đỉnh vận tốc nằm ngang, tầm cao H và tầm xa L",
            b,
            "Hình 5. Ném xiên từ mặt đất: $\\vec v_0$ (đỏ) tách thành $v_{0x}$ (xanh) và $v_{0y}$ (cam). Ở <strong>đỉnh</strong> chỉ còn thành phần ngang; quỹ đạo đối xứng qua đỉnh nên bóng rơi xuống cùng độ cao lúc ném.")

# ================= Hình 6: hai góc phụ nhau (30° và 60°) cùng tầm xa =================
G6, O6X, L6 = 200, 50, 340
b = defs("f6")
b += seg(20, G6, 420, G6, "currentColor", 1.8)
for H6, dash, w in ((147, "", 2.6), (49, "7 5", 2.4)):
    pts = [(O6X + L6 * u / 40, G6 - 4 * H6 * (u / 40) * (1 - u / 40)) for u in range(0, 41)]
    b += poly(pts, GRN, w, dash)
    b += dot(O6X + L6 / 2, G6 - H6, 4.2, ORG)
b += dot(O6X, G6, 4.5, ORG) + dot(O6X + L6, G6, 4.5, ORG)
b += seg(O6X, 224, O6X + L6, 224, ORG, 1.4)
b += seg(O6X, 220, O6X, 228, ORG, 1.4) + seg(O6X + L6, 220, O6X + L6, 228, ORG, 1.4)
b += text(O6X + L6 / 2, 244, "cùng tầm xa L", ORG, 14, "middle", "700")
b += text(20, 18, "α = 60° (nét liền): lên cao gấp 3, bay lâu hơn", GRN, 14, "start", "700")
b += text(20, 38, "α = 30° (nét đứt): thấp hơn, bay nhanh hơn", GRN, 14, "start", "700")
fig6 = wrap("0 0 440 254",
            "Hai góc ném phụ nhau 30 độ và 60 độ với cùng vận tốc đầu cho cùng tầm xa; góc 60 độ lên cao gấp ba và bay lâu hơn",
            b,
            "Hình 6. Cùng $v_0$, ném ở $30^\\circ$ và $60^\\circ$ (hai góc <strong>phụ nhau</strong>): hai quỹ đạo rơi xuống <strong>cùng một điểm</strong>, nhưng quỹ đạo $60^\\circ$ cao gấp ba ($H\\sim\\sin^2\\alpha$) và bay lâu hơn.")

fig1 = fig1.replace("</svg>", '</svg><button type="button" class="bt-run" data-bt-run="1">▶ Chạy mô phỏng</button>', 1)
h = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4, fig5, fig6), 1):
    assert f"<!--FIG{n}-->" in h, f"thiếu mốc FIG{n}"
    h = h.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(h)
print("ok", len(h), "bytes,", h.count('<figure class="fig"'), "hình")
