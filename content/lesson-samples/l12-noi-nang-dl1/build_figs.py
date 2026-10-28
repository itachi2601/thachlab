"""Sinh 4 hình SVG cho bài "Bài 3. Nội năng. Định luật I Nhiệt động lực học" (Vật lí 12)
và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html.
Chạy từ thư mục này: python3 build_figs.py
"""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *  # noqa: E402


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def dot(x, y, r=5, c="currentColor"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def rect(x, y, w, h, fill, stroke="currentColor", sw=2, rx=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


# ======================================================= Hình 1: cùng 5 °C, khác cảm giác
b = defs("f1")
b += text(16, 22, "Cùng 5 °C — vì sao kim loại buốt hơn gỗ?", "currentColor", 13, "start", "700")

HAND = ('<path d="M158 74 q0 -16 16 -16 q16 0 16 16 l0 18 q10 -6 18 2 q6 6 2 14 l-8 16 q-4 8 -12 8 l-24 0 '
        'q-8 0 -12 -8 l-10 -20 q-4 -8 2 -14 q8 -8 16 -2 z" fill="rgba(148,163,184,.20)" stroke="currentColor" stroke-width="2"/>')


def hand(dx):          # bàn tay (đáy ở y=140) đặt đúng lên mặt vật
    return f'<g transform="translate({dx} 8)">{HAND}</g>'


# thanh kim loại + tay chạm vào mặt trên
b += rect(40, 140, 150, 46, "rgba(56,189,248,.18)", BLUE, 2.5)
b += hand(-89)
b += text(122, 78, "tay em 33 °C", "currentColor", 12.5, "start", "600")
b += text(150, 168, "kim loại", BLUE, 13, "middle", "700")
b += text(115, 206, "5 °C", BLUE, 12.5, "middle", "700")
# nhiệt đi từ tay xuống kim loại: ba mũi, dài (dẫn nhanh)
for x in (68, 88, 108):
    b += arrow("f1", "r", x, 120, x, 172, 3)
b += text(128, 102, "rút nhiệt", RED, 12.5, "start", "700")
b += text(128, 118, "rất nhanh", RED, 12.5, "start", "700")

# thanh gỗ (vẽ thêm vân gỗ) + tay chạm vào mặt trên
b += rect(250, 140, 150, 46, "rgba(251,146,60,.20)", ORG, 2.5)
b += line(250, 150, 400, 150, ORG, 1, "4 4", .5)
b += line(250, 178, 400, 178, ORG, 1, "4 4", .5)
b += hand(121)
b += text(374, 168, "gỗ", ORG, 13, "middle", "700")
b += text(325, 206, "5 °C", ORG, 12.5, "middle", "700")
# nhiệt đi từ tay xuống gỗ: một mũi, ngắn (dẫn chậm)
b += arrow("f1", "r", 298, 124, 298, 150, 3)
b += text(338, 102, "rút nhiệt", RED, 12.5, "start", "600")
b += text(338, 118, "chậm", RED, 12.5, "start", "600")

b += line(16, 222, 404, 222, "currentColor", 1.5, "", .5)
b += text(16, 240, "Cùng nhiệt độ, khác tốc độ dẫn nhiệt → khác cảm giác", "currentColor", 12.5, "start", "600")
fig1 = wrap("0 0 420 252", "Bàn tay đặt lên thanh kim loại 5 độ C và thanh gỗ 5 độ C: kim loại rút nhiệt từ tay nhanh hơn nên thấy buốt hơn",
            b, "Hình 1. Cùng 5 °C, nhưng kim loại rút nhiệt từ tay nhanh hơn gỗ. Cảm giác không phải là nhiệt độ.")

# ======================================================= Hình 2: hai cách làm biến đổi nội năng
b = defs("f2")
b += text(16, 20, "Hai cách làm biến đổi nội năng", "currentColor", 12.5, "start", "700")

# --- a) thực hiện công: xilanh bị nén
b += text(16, 42, "a) Thực hiện công", "currentColor", 12.5, "start", "700")
b += rect(46, 100, 66, 87, "rgba(56,189,248,.12)", "currentColor", 2.5)
for i in range(6):                      # các phân tử khí
    x = 56 + (i % 3) * 18
    y = 120 + (i // 3) * 28
    b += dot(x, y, 3.2, BLUE)
b += rect(40, 86, 78, 14, "rgba(148,163,184,.35)", "currentColor", 2, 4)   # pit-tông
b += arrow("f2", "r", 79, 54, 79, 84, 3)          # đẩy pit-tông XUỐNG (y tăng)
b += text(92, 72, "đẩy xuống", RED, 12.5, "start", "700")
b += text(79, 206, "khí bị nén", "currentColor", 12.5, "middle", "600")
b += text(79, 224, "A dương", RED, 12.5, "middle", "700")

# --- b) truyền nhiệt: ngọn lửa
b += text(166, 42, "b) Truyền nhiệt", "currentColor", 12.5, "start", "700")
b += rect(178, 100, 66, 92, "rgba(248,113,113,.10)", "currentColor", 2.5)
for i in range(6):
    x = 188 + (i % 3) * 18
    y = 120 + (i // 3) * 28
    b += dot(x, y, 3.2, RED)
b += arrow("f2", "r", 204, 212, 204, 170, 3)      # nhiệt đi từ ngọn lửa VÀO ống
b += text(252, 200, "nhiệt", RED, 12.5, "start", "700")
b += f'<path d="M204 242 q-14 -14 0 -26 q14 12 0 26 z" fill="{ORG}" stroke="{ORG}" stroke-width="2"/>'
b += text(222, 238, "ngọn lửa", ORG, 12.5, "start", "700")
b += text(209, 264, "Q dương", RED, 12.5, "middle", "700")
b += text(209, 284, "cùng một kết quả: nội năng tăng", "currentColor", 12.5, "middle", "600")

# --- hai ví dụ đời thường bên phải
b += line(292, 36, 292, 240, "currentColor", 1, "4 4", .4)
b += text(304, 60, "Xoa hai bàn tay", "currentColor", 12.5, "start", "700")
b += text(304, 76, "→ công của ma sát", GRN, 12, "start", "600")
b += text(304, 108, "Hơ ống nghiệm", "currentColor", 12.5, "start", "700")
b += text(304, 124, "trên ngọn lửa", "currentColor", 12.5, "start", "700")
b += text(304, 140, "→ nhiệt truyền vào", GRN, 12, "start", "600")
b += text(304, 176, "Cách phân biệt:", "currentColor", 12.5, "start", "700")
b += text(304, 192, "có lực làm vật", GRN, 12, "start", "600")
b += text(304, 206, "dịch chuyển không?", GRN, 12, "start", "600")
fig2 = wrap("0 0 440 300", "Hai cách làm biến đổi nội năng: nén khí bằng công và hơ nóng bằng truyền nhiệt, cùng làm nội năng tăng",
            b, "Hình 2. Hai đường làm đổi nội năng: thực hiện công (có lực làm dịch chuyển) và truyền nhiệt (chênh nhiệt độ).")

# ======================================================= Hình 3: ảnh OpenStax College Physics 2e, Hình 14.4 (đợt 2, 27/10/2026)
fig3 = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l12-noi-nang-dl1/hinh-nhiet-luong-3-yeu-to.webp" '
        'alt="Ba cặp hình trụ nhận nhiệt: (a) nhiệt gấp đôi thì độ tăng nhiệt độ gấp đôi, (b) khối lượng gấp đôi thì cần nhiệt gấp đôi, '
        '(c) cùng khối lượng và cùng độ tăng nhiệt độ, nước cần nhiệt gấp 10,8 lần đồng" loading="lazy" width="708" height="858">'
        '<figcaption>Hình 3. Nhiệt lượng cần để vật nóng lên phụ thuộc ba yếu tố:<br>'
        '(a) độ tăng nhiệt độ: tăng gấp đôi thì cần nhiệt gấp đôi.<br>'
        '(b) khối lượng: gấp đôi thì cần nhiệt gấp đôi.<br>'
        '(c) chất: cùng khối lượng, cùng độ tăng nhiệt độ, nước cần nhiệt gấp 10,8 lần đồng — nên nước “khó nóng, khó nguội”.<br>'
        'Nhãn: Q = nhiệt lượng · m = khối lượng · ΔT = độ tăng nhiệt độ · Cu = đồng · water = nước.<br>'
        '<small>Hình: OpenStax, College Physics 2e, Hình 14.4 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small>'
        '</figcaption></figure>')

# ======================================================= Hình 4: sơ đồ định luật I cho bài toán bơm
b = defs("f4")
b += text(16, 24, "Định luật I cho một lần ấn bơm", "currentColor", 13, "start", "700")

# xilanh
b += rect(150, 96, 84, 118, "rgba(56,189,248,.12)", "currentColor", 2.5)
for i in range(6):
    x = 162 + (i % 3) * 24
    y = 140 + (i // 3) * 34
    b += dot(x, y, 3.4, BLUE)
b += rect(142, 80, 100, 15, "rgba(148,163,184,.35)", "currentColor", 2, 4)
b += arrow("f4", "r", 192, 36, 192, 78, 3)        # công ép pit-tông XUỐNG
b += text(206, 52, "công 60 J", RED, 13, "start", "700")
b += text(206, 70, "tay truyền cho khí", "currentColor", 12, "start", "600")
b += text(192, 236, "khối khí", "currentColor", 12.5, "middle", "600")

# nhiệt toả ra
b += arrow("f4", "b", 240, 132, 308, 110, 3.5)
b += text(314, 100, "toả ra 15 J", BLUE, 13, "start", "700")
b += text(314, 116, "qua thành ống bơm", "currentColor", 12, "start", "600")

# hộp kết quả
b += rect(302, 146, 122, 84, "rgba(52,211,153,.14)", GRN, 2.5)
b += text(363, 172, "ΔU = A + Q", "currentColor", 12.5, "middle", "700")
b += text(363, 196, "= 60 + (−15)", "currentColor", 12, "middle", "600")
b += text(363, 219, "= +45 J", GRN, 14, "middle", "700")

b += line(16, 268, 432, 268, "currentColor", 1.5, "", .5)
b += text(16, 286, "Nhận vào thì dương (công +60) · mất đi thì âm (nhiệt −15)", "currentColor", 12, "start", "600")
fig4 = wrap("0 0 440 298", "Sơ đồ định luật I cho một lần ấn bơm: công 60 J truyền vào khí, khí toả ra 15 J, độ biến thiên nội năng bằng 45 J",
            b, "Hình 4. Một lần bơm: công 60 J vào khí, nhiệt 15 J ra khỏi khí: ΔU = 60 + (−15) = +45 J.")

# ------------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(margin_figs(src))
print("ok", len(src), "bytes")
