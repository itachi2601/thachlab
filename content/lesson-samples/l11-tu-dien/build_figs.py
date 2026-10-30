"""Sinh 3 hình SVG và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được).
Hình 2 vẽ đúng số liệu bảng thí nghiệm tn-l11-tudien-02 (C ≈ 480 μF)."""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import pathlib, re
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[3] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import RED, BLUE, ORG, GRN, arrow, wrap, text as _text  # svg_lib của skill: arrow = thân + đầu V 30°, không marker

def text(x, y, s, c="currentColor", size=14, anchor="start", weight="600"):
    """Chữ trong hình: tối thiểu 14 (viewBox 440 → còn ~12 px ở màn 375 px)."""
    return _text(x, y, s, c, max(size, 14), anchor, weight)

HERE = pathlib.Path(__file__).resolve().parent

def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'

def dot(x, y, r=4, c="currentColor"): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'

def sub(base, s, x, y, c="currentColor", size=13, anchor="start", weight="700"):
    size = max(size, 13)
    """Chữ có chỉ số dưới (không dùng KaTeX trong SVG)."""
    return (f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{base}<tspan baseline-shift="sub" font-size="{max(size-3, 11)}">{s}</tspan></text>')

def subs(parts, x, y, c="currentColor", size=12, anchor="start", weight="600"):
    size = max(size, 13)
    """Một dòng chữ nhiều chỉ số dưới: parts = [("U = U", "1"), (" + U", "2")]."""
    t = "".join(f'<tspan>{a}</tspan><tspan baseline-shift="sub" font-size="{max(size-3, 11)}">{s}</tspan>' for a, s in parts)
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{t}</text>'

def cap_sym(x, y, h=30, gap=10, c="currentColor"):
    """Kí hiệu tụ nằm ngang: hai vạch đứng tại x và x+gap, tâm y."""
    return line(x, y - h / 2, x, y + h / 2, c, 3.5) + line(x + gap, y - h / 2, x + gap, y + h / 2, c, 3.5)

# ---------------- Hình 1: cấu tạo tụ phẳng nối nguồn + kí hiệu
b = ""
L, R, top, bot = 170, 250, 40, 160          # bản trái (x 170–176), bản phải (x 244–250)
b += f'<rect x="176" y="{top}" width="68" height="{bot-top}" fill="{ORG}" opacity=".15"/>'
b += f'<rect x="{L}" y="{top}" width="6" height="{bot-top}" fill="{RED}"/>'
b += f'<rect x="244" y="{top}" width="6" height="{bot-top}" fill="{BLUE}"/>'
for y in (58, 86, 114, 142):
    b += text(183, y + 5, "+", RED, 15, "middle", "700") + text(237, y + 5, "−", BLUE, 15, "middle", "700")
for y in (72, 100, 128):
    b += arrow("f1", "g", 192, y, 226, y, 2)
b += text(209, 91, "E", GRN, 15, "middle", "700")
b += text(173, 30, "bản +Q", RED, 14, "middle", "700") + text(250, 30, "bản −Q", BLUE, 14, "middle", "700")
b += text(210, 178, "điện môi", ORG, 14, "middle", "700")
# dây nối nguồn: bản trái -> cực dương (vạch dài), bản phải -> cực âm (vạch ngắn)
b += line(L, 100, 90, 100) + line(90, 100, 90, 210) + line(90, 210, 200, 210)
b += line(200, 196, 200, 224, "currentColor", 3) + line(212, 202, 212, 218, "currentColor", 5)
b += line(212, 210, 330, 210) + line(330, 210, 330, 100) + line(330, 100, R, 100)
b += text(192, 204, "+", RED, 15, "end", "700") + text(220, 204, "−", BLUE, 15, "start", "700")
b += text(206, 238, "nguồn U", "currentColor", 14, "middle", "600")
# kí hiệu tụ trong sơ đồ
b += line(352, 30, 352, 232, "currentColor", 1, "3 4", .4)
b += line(362, 120, 392, 120) + cap_sym(392, 120) + line(402, 120, 432, 120)
b += text(397, 92, "kí hiệu", "currentColor", 14, "middle", "600")
fig1 = wrap("70 12 376 236", "Tụ điện phẳng: hai bản kim loại song song, giữa là điện môi, nối với hai cực nguồn; bên phải là kí hiệu tụ",
            b, "Hình 1. Tụ điện phẳng nối với nguồn.<br>Bản nối cực dương tích +Q, bản kia −Q.<br>Điện trường E (lục) hướng từ bản + sang bản −.<br>Bên phải: kí hiệu tụ trong sơ đồ.")

# ---------------- Hình 2: đồ thị Q theo U (số liệu thí nghiệm) + diện tích = năng lượng
DATA = [(2, 980), (4, 1900), (6, 2890), (8, 3820), (10, 4800)]
C_FIT = 480                                   # μF, đường thẳng Q = 480·U
X0, Y0, SX, SY = 64, 200, 33.6, 0.034            # gốc, px/V, px/μC
X = lambda u: X0 + SX * u
Y = lambda q: Y0 - SY * q
b = ""
U_SH = 8
b += (f'<polygon points="{X(0)},{Y(0)} {X(U_SH)},{Y(0)} {X(U_SH)},{Y(C_FIT*U_SH):.1f}" '
      f'fill="{ORG}" opacity=".28"/>')
b += line(X0, Y0, X(11), Y0, "currentColor", 1.6) + line(X0, Y0, X0, Y(5600), "currentColor", 1.6)
for u in (2, 4, 6, 8, 10):
    b += line(X(u), Y0, X(u), Y0 + 5, "currentColor", 1.2) + text(X(u), Y0 + 18, str(u), "currentColor", 14, "middle", "400")
for q in (2000, 4000):
    b += line(X0 - 5, Y(q), X0, Y(q), "currentColor", 1.2) + text(X0 - 8, Y(q) + 4, str(q), "currentColor", 14, "end", "400")
b += text(X(11), Y0 - 7, "U (V)", "currentColor", 14, "end", "700")
b += text(X0 + 6, Y(5600) + 4, "Q (μC)", "currentColor", 14, "start", "700")
b += line(X(0), Y(0), X(10.6), Y(C_FIT * 10.6), RED, 2.2)
for u, q in DATA:
    b += dot(X(u), Y(q), 4.5, BLUE)
b += text(X(4.2), Y(2900), "Q = C·U", RED, 14, "end", "700")
b += text(X(5.6), Y(450), "W = ½QU", ORG, 14, "middle", "700")
b += line(X(U_SH), Y(C_FIT*U_SH), X(U_SH), Y0, ORG, 1.2, "3 3")
fig2 = wrap("0 0 440 230", "Đồ thị Q theo U: năm điểm đo nằm sát đường thẳng qua gốc, hệ số góc C khoảng 480 microfara; diện tích tam giác dưới đường là năng lượng",
            b, "Hình 2. Năm điểm đo (xanh) sát đường thẳng qua gốc.<br>Q tỉ lệ U.<br>Hệ số góc là C ≈ 480 μF.<br>Phần tô cam (tới U = 8 V) là năng lượng W = ½QU.")

# ---------------- Hình 3, 4: ảnh OpenStax College Physics 2e, Hình 19.19 và 19.20 (đợt 2, 28/10/2026), thay SVG
fig3 = ('<figure class="fig">'
        '<img src="/assets/openstax/l11-tu-dien/hinh-ghep-noi-tiep.webp" '
        'alt="Ba tụ nối tiếp, mỗi tụ có +Q và −Q (trái); tụ tương đương là một tụ có khoảng cách hai bản d lớn hơn (phải)" '
        'loading="lazy" width="378" height="640" style="max-width:min(100%,250px);height:auto">'
        '<img src="/assets/openstax/l11-tu-dien/hinh-ghep-song-song.webp" '
        'alt="Ba tụ song song, mỗi tụ có điện tích riêng (trên); tụ tương đương có diện tích bản bằng tổng, Q bằng Q1 cộng Q2 cộng Q3 (dưới)" '
        'loading="lazy" width="628" height="690" style="max-width:100%;height:auto">'
        '<figcaption>Hình 3. Nối tiếp: d lớn nên C nhỏ.<br>Song song: bản rộng nên C lớn.<br>Hình vẽ 3 tụ.<br>'
        '<small>Hình: OpenStax, College Physics 2e, Hình 19.19 và 19.20 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>')

h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, f in enumerate((fig1, fig2, fig3), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", f)
(HERE / "theory.html").write_text(margin_figs(h), encoding="utf8")
print("ok", len(h))
