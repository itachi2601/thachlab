"""Sinh 4 hình SVG cho bài "Mô tả sóng" và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được)."""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import math
# dùng svg_lib của skill (arrow đầu V 30°, chevron) — bản svg_lib.py cũ trong thư mục bài còn marker tam giác
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[3] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *

def poly(pts, c, w=2, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline fill="none" stroke="{c}" stroke-width="{w}"{d} points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>'

def dot(x, y, r=5, c="currentColor"): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'

def dbl_h(x1, x2, y, c, w=1.6):
    """Đoạn thẳng hai đầu mũi tên nằm ngang (dùng để đo T, λ, d, Δφ)."""
    b = f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{c}" stroke-width="{w}"/>'
    b += f'<path d="M{x1+7},{y-4} L{x1},{y} L{x1+7},{y+4}" fill="none" stroke="{c}" stroke-width="{w}"/>'
    b += f'<path d="M{x2-7},{y-4} L{x2},{y} L{x2-7},{y+4}" fill="none" stroke="{c}" stroke-width="{w}"/>'
    return b

def dbl_v(x, y1, y2, c, w=1.6):
    """Đoạn thẳng hai đầu mũi tên thẳng đứng (dao động lên – xuống)."""
    b = f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{c}" stroke-width="{w}"/>'
    b += f'<path d="M{x-4},{y1+7} L{x},{y1} L{x+4},{y1+7}" fill="none" stroke="{c}" stroke-width="{w}"/>'
    b += f'<path d="M{x-4},{y2-7} L{x},{y2} L{x+4},{y2-7}" fill="none" stroke="{c}" stroke-width="{w}"/>'
    return b

# ---- Hình 1: làn sóng người trên khán đài (vẽ lại 30/10/2026: chữ 14, người có chân/ghế, xung đứng lên có độ cao biến thiên, mũi tên đầu V)
SEAT, FLOOR, AMP, TORSO, HR = 192, 218, 40, 30, 7
XC, W = 262, 58                                   # đỉnh làn sóng (xung) đang ở x = XC
r_of = lambda x: math.exp(-((x - XC) / W) ** 2)   # 0 = ngồi, 1 = đứng thẳng
b = text(14, 26, "Mỗi người chỉ đứng lên rồi ngồi xuống tại ghế", "currentColor", 14, "start", "600")
b += f'<rect x="12" y="{SEAT}" width="416" height="8" rx="2" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="1.4"/>'
b += line(12, FLOOR, 428, FLOOR, "currentColor", 1.6)
for i in range(12):
    x = 26 + 35 * i
    r = r_of(x)
    hipY = SEAT - 3 - AMP * r
    footX = x + 11
    kx = (1 - r) * (x + 13) + r * (x + 6)
    ky = (1 - r) * hipY + r * (hipY + FLOOR) / 2
    sh = hipY - TORSO + 6                          # vai
    hy = hipY - TORSO - HR
    b += f'<polyline fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round" points="{x:.1f},{hipY:.1f} {kx:.1f},{ky:.1f} {footX:.1f},{FLOOR - 1}"/>'
    b += line(x, hipY, x, hy + HR, "currentColor", 2.2)
    b += f'<circle cx="{x:.1f}" cy="{hy:.1f}" r="{HR}" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    if r > 0.5:                                    # đang đứng: giơ tay
        b += line(x, sh, x - 11, sh - 20, "currentColor", 2.2) + line(x, sh, x + 11, sh - 20, "currentColor", 2.2)
    else:                                          # đang ngồi: tay đặt lên đùi
        b += line(x, sh, x + 10, hipY - 6, "currentColor", 2.2)
# đường đỏ đi sát đỉnh đầu mọi người = "trạng thái đứng lên" tại một lúc
b += poly([(x, SEAT - 3 - AMP * r_of(x) - TORSO - 2 * HR - 12) for x in range(16, 425, 3)], RED, 2.2, "6 4")
b += text(XC, SEAT - 3 - AMP - TORSO - 2 * HR - 22, "trạng thái đứng lên", RED, 14, "middle", "700")
b += arrow("f1", "g", 30, 242, 290, 242, 2.8) + text(300, 247, "chiều làn sóng", GRN, 14, "start", "700")
fig1 = wrap("0 0 440 258", "Khán đài: làn sóng người chạy sang phải, mỗi người chỉ đứng lên rồi ngồi xuống tại ghế của mình",
            b, "Hình 1. Làn sóng người: đường đỏ là “trạng thái đứng lên” đang chạy qua; không ai rời ghế.")

# ---------------- Hình 2: ảnh OpenStax College Physics 2e, Hình 16.28 (28/10/2026) — thay SVG tự vẽ
fig2 = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l11-mo-ta-song/hinh-hai-au-nhap-nho.webp" '
        'alt="Sóng nước lan sang phải; chim hải âu chỉ nhấp nhô lên xuống tại chỗ; λ là khoảng cách hai đỉnh liên tiếp, X là biên độ" loading="lazy" width="875" height="404">'
        '<figcaption>Hình 2. Hải âu chỉ nhấp nhô tại chỗ.<br>λ: hai đỉnh liên tiếp. X: biên độ.<br><small>Hình: OpenStax, College Physics 2e, Hình 16.28 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>')

# ---- Hình 3: trễ pha — O và M, đồ thị u(t) lệch nhau (vẽ lại 30/10/2026: chữ ≥14, mũi tên đầu V, khoảng lệch trên trục t ghi d/v)
PER, T0, Y0, AU = 120, 30, 200, 28        # chu kì 120 px; sóng tới M sau d/v = 30 px = T/4 (d = λ/4)
b = line(20, 60, 420, 60, "currentColor", 1.6, "", .7)
b += arrow("f3", "g", 300, 24, 400, 24, 2.6) + text(292, 29, "chiều truyền", GRN, 14, "end", "700")
b += dot(80, 60, 6, ORG) + dot(330, 60, 6, BLUE)
b += text(80, 84, "O (nguồn)", ORG, 14, "middle", "700") + text(330, 84, "M", BLUE, 14, "middle", "700")
b += dbl_h(80, 330, 104, GRN, 1.6) + text(205, 97, "d", GRN, 15, "middle", "700")
X0 = 40                                   # gốc thời gian
b += arrow("f3", "g", X0, Y0, 418, Y0, 1.6).replace(GRN, "currentColor") + text(416, Y0 + 20, "t", "currentColor", 15, "end", "700")
b += arrow("f3", "g", X0, Y0 + 40, X0, 138, 1.6).replace(GRN, "currentColor") + text(X0 + 8, 148, "u", "currentColor", 15, "start", "700")
b += poly([(x, Y0 - AU * math.sin(2 * math.pi * (x - X0) / PER)) for x in range(X0, 391)], RED, 2.4)
b += line(X0, Y0, X0 + T0, Y0, BLUE, 3.2)   # trước lúc sóng tới, M đứng yên
b += poly([(x, Y0 - AU * math.sin(2 * math.pi * (x - X0 - T0) / PER)) for x in range(X0 + T0, 391)], BLUE, 2.4)
pO, pM = X0 + PER / 4, X0 + T0 + PER / 4    # hai đỉnh đầu tiên
b += line(pO, Y0 - AU, pO, 154, RED, 1.2, "3 3") + line(pM, Y0 - AU, pM, 154, BLUE, 1.2, "3 3")
b += dbl_h(pO, pM, 156, GRN, 1.6) + text(pM + 8, 161, "trễ d/v", GRN, 14, "start", "700")
b += text(398, Y0 - 28, "u", RED, 14, "start", "700").replace(">u<", '>u<tspan baseline-shift="sub" font-size="11">O</tspan><')
b += text(398, Y0 + 30, "u", BLUE, 14, "start", "700").replace(">u<", '>u<tspan baseline-shift="sub" font-size="11">M</tspan><')
b += text(20, 264, "M dao động chậm hơn O khoảng d/v", "currentColor", 14, "start", "500")
b += text(20, 284, "→ trễ pha Δφ = 2πd/λ", "currentColor", 14, "start", "600")
fig3 = wrap("0 0 440 294", "Điểm M cách nguồn O đoạn d: sóng tới M chậm hơn d/v, dao động tại M trễ pha hơn O đúng Δφ = 2πd/λ",
            b, "Hình 3. Sóng đi thêm đoạn d mới tới M, nên u(t) tại M trễ pha hơn O đúng Δφ = 2πd/λ.")

# ---- Hình 4: hai loại đồ thị u–t và u–x (vẽ lại 30/10/2026: chữ ≥14, trục có mũi tên + nhãn ở đầu trục, bỏ khoảng trắng)
b = line(220, 8, 220, 214, "currentColor", 1.2, "4 4", .35)
for xL, col, t1, t2, lab, ax in ((22, RED, "Tại MỘT điểm", "theo thời gian", "T", "t"),
                                 (238, BLUE, "Tại MỘT lúc", "theo không gian", "λ", "x")):
    Y, A, P = 132, 30, 80
    xr = xL + 180
    b += text(xL + 90, 24, t1, col, 14, "middle", "700") + text(xL + 90, 44, t2, col, 14, "middle", "700")
    b += arrow("f4", "g", xL, Y, xr, Y, 1.6).replace(GRN, "currentColor") + text(xr, Y + 22, ax, "currentColor", 15, "end", "700")
    b += arrow("f4", "g", xL, Y + 42, xL, 72, 1.6).replace(GRN, "currentColor") + text(xL + 8, 80, "u", "currentColor", 15, "start", "700")
    b += poly([(x, Y - A * math.sin(2 * math.pi * (x - xL) / P)) for x in range(xL, xr - 14)], col, 2.4)
    a, c = xL + P / 4, xL + P / 4 + P          # hai đỉnh liên tiếp
    b += line(a, Y - A, a, 196, GRN, 1.2, "3 3") + line(c, Y - A, c, 196, GRN, 1.2, "3 3")
    b += dbl_h(a, c, 190, GRN, 1.8) + text((a + c) / 2, 214, lab, GRN, 16, "middle", "700")
fig4 = wrap("0 0 440 222", "Hai loại đồ thị sóng: bên trái u theo thời gian (hai đỉnh liên tiếp cách nhau T), bên phải u theo không gian (hai đỉnh liên tiếp cách nhau λ)",
            b, "Hình 4. Cùng một sóng, khác trục hoành: u–t (một điểm) một bước là T; u–x (một lúc) một bước là λ.")

h = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(margin_figs(h))
print("ok", len(h))
