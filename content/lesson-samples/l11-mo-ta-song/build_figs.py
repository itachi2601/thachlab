"""Sinh 4 hình SVG cho bài "Mô tả sóng" và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được)."""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import math
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

# ---- Hình 1: làn sóng người trên khán đài
base, x0, L, AMP = 168, 30, 190, 34
env = lambda x: max(0.0, math.sin(2 * math.pi * (x - x0) / L))
b = text(14, 24, "mỗi người: đứng lên – ngồi xuống tại chỗ, không rời ghế", "currentColor", 12, "start", "500")
b += f'<rect x="14" y="{base}" width="412" height="9" rx="2" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="1.5"/>'
for i in range(9):
    x = x0 + 47.5 * i
    rise = AMP * env(x)
    hip = base - 6 - rise
    hy = hip - 34
    b += line(x, hip, x, hy + 8, "currentColor", 2.2)
    b += f'<circle cx="{x:.1f}" cy="{hy:.1f}" r="8" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    if rise > 12:  # chỉ người đang đứng lên mới giơ tay
        b += line(x, hy + 19, x - 15, hy - 4, "currentColor", 2.2)
        b += line(x, hy + 19, x + 15, hy - 4, "currentColor", 2.2)
b += poly([(x, base - 40 - AMP * env(x)) for x in range(18, 423, 6)], RED, 2.2)
b += arrow("f1", "g", 30, 208, 410, 208, 3) + text(220, 200, "chiều làn sóng", GRN, 12, "middle", "700")
fig1 = wrap("0 0 440 224", "Khán đài: làn sóng người chạy qua, mỗi người chỉ đứng lên rồi ngồi xuống tại chỗ",
            b, "Hình 1. Làn sóng người: đường đỏ là “trạng thái đứng lên” đang chạy qua; không ai rời ghế.")

# ---------------- Hình 2: ảnh OpenStax College Physics 2e, Hình 16.28 (28/10/2026) — thay SVG tự vẽ
fig2 = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l11-mo-ta-song/hinh-hai-au-nhap-nho.webp" '
        'alt="Sóng nước lan sang phải; chim hải âu chỉ nhấp nhô lên xuống tại chỗ; λ là khoảng cách hai đỉnh liên tiếp, X là biên độ" loading="lazy" width="875" height="404">'
        '<figcaption>Hình 2. Hải âu chỉ nhấp nhô tại chỗ.<br>λ: hai đỉnh liên tiếp. X: biên độ.<br><small>Hình: OpenStax, College Physics 2e, Hình 16.28 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>')

# ---- Hình 3: trễ pha — O và M, đồ thị u(t) lệch nhau
b = line(30, 70, 410, 70, "currentColor", 1.6, "", .7)
b += arrow("f3", "g", 330, 44, 408, 44, 2.2) + text(330, 36, "chiều truyền", GRN, 11, "middle", "600")
b += dot(70, 70, 6, ORG) + dot(330, 70, 6, BLUE)
b += text(70, 92, "O", ORG, 14, "middle", "700") + text(330, 92, "M", BLUE, 14, "middle", "700")
b += dbl_h(70, 330, 56, GRN, 1.6) + text(200, 48, "d", GRN, 13, "middle", "700")
b += line(30, 200, 410, 200, "currentColor", 1.6)
b += line(30, 130, 30, 226, "currentColor", 1.2, "3 3", .5) + text(414, 204, "t", "currentColor", 13, "start", "700")
b += poly([(x, 200 - 30 * math.sin(2 * math.pi * (x - 30) / 120.0)) for x in range(30, 391)], RED, 2.4)
b += poly([(x, 200 - 30 * math.sin(2 * math.pi * (x - 60) / 120.0)) for x in range(60, 391)], BLUE, 2.4)
b += line(60, 162, 60, 196, RED, 1, "3 3", .7) + line(90, 162, 90, 196, BLUE, 1, "3 3", .7)
b += dbl_h(60, 90, 166, GRN, 1.6) + text(75, 152, "Δφ", GRN, 12, "middle", "700")
b += text(36, 122, "O (nguồn)", RED, 11, "start", "700") + text(120, 122, "M (trễ pha hơn)", BLUE, 11, "start", "700")
b += text(36, 240, "Δφ = 2πd/λ: sóng tới M chậm hơn O một khoảng thời gian d/v", "currentColor", 11, "start", "500")
fig3 = wrap("0 0 440 248", "Điểm M cách nguồn O đoạn d: dao động tại M trễ pha hơn O đúng Δφ = 2πd/λ",
            b, "Hình 3. Sóng đi thêm đoạn d mới tới M, nên u(t) tại M trễ pha hơn O đúng Δφ = 2πd/λ.")

# ---- Hình 4: hai loại đồ thị u–t và u–x
b = line(220, 10, 220, 244, "currentColor", 1.2, "4 4", .35)
for xL, col, t1, t2, lab, axlab in ((30, RED, "Tại MỘT điểm,", "theo thời gian t", "T", "t (s)"),
                                    (240, BLUE, "Tại MỘT lúc,", "theo không gian x", "λ", "x (cm)")):
    xr = xL + 175
    b += text(xL + 87, 20, t1, col, 12, "middle", "700") + text(xL + 87, 36, t2, col, 12, "middle", "700")
    b += line(xL, 180, xr + 5, 180, "currentColor", 1.6)
    b += line(xL, 140, xL, 208, "currentColor", 1.2, "3 3", .5)
    b += poly([(x, 180 - 26 * math.sin(2 * math.pi * (x - xL) / 90.0)) for x in range(xL, xr + 1)], col, 2.4)
    a, c = xL + 22.5, xL + 112.5
    b += line(a, 200, a, 220, GRN, 1.2, "3 3", .8) + line(c, 200, c, 220, GRN, 1.2, "3 3", .8)
    b += dbl_h(a, c, 214, GRN, 1.8) + text((a + c) / 2, 240, lab, GRN, 13, "middle", "700")
    b += text(xL + 4, 197, axlab, "currentColor", 12, "start", "600")
fig4 = wrap("0 0 440 250", "Hai loại đồ thị sóng: bên trái u theo thời gian (một bước là T), bên phải u theo không gian (một bước là λ)",
            b, "Hình 4. Cùng một sóng, khác trục hoành: u–t (một điểm) một bước là T; u–x (một lúc) một bước là λ.")

h = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(margin_figs(h))
print("ok", len(h))
