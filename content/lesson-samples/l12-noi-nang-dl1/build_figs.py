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
# (vẽ lại 31/10/2026: chữ >= 14, bàn tay áp phẳng lên mặt vật, mũi tên nhiệt bắt đầu ở đáy lòng bàn tay)
b = defs("f1")
b += text(16, 24, "Cùng 5 °C — vì sao kim loại buốt hơn gỗ?", "currentColor", 15, "start", "700")


def hand(dx):
    """Bàn tay áp phẳng lên mặt vật (mặt vật ở y=140), cẳng tay chếch lên trái."""
    g = (f'<rect x="{56+dx}" y="112" width="104" height="27" rx="13" fill="rgba(148,163,184,.25)" '
          f'stroke="currentColor" stroke-width="2"/>')
    # cẳng tay vẽ sau, đáy trùng mép trên lòng bàn tay (y=112) để không lộ nét chồng
    g += (f'<path d="M{96+dx} 112 L{62+dx} 50 L{36+dx} 60 L{66+dx} 112" fill="rgba(148,163,184,.25)" '
          f'stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>')
    return g


# --- kim loại
b += rect(30, 140, 170, 46, "rgba(56,189,248,.18)", BLUE, 2.5)
b += hand(0)
b += text(76, 62, "tay em 33 °C", "currentColor", 14, "start", "600")
for x in (82, 108, 134):                          # nhiệt đi từ tay xuống kim loại: ba mũi dài
    b += arrow("f1", "r", x, 142, x, 180, 3)
b += text(116, 88, "rút nhiệt", RED, 14, "start", "700")
b += text(116, 106, "rất nhanh", RED, 14, "start", "700")
b += text(115, 208, "kim loại", BLUE, 15, "middle", "700")
b += text(115, 228, "5 °C", BLUE, 14, "middle", "700")

# --- gỗ (vân gỗ nét đứt)
b += rect(240, 140, 170, 46, "rgba(251,146,60,.20)", ORG, 2.5)
b += line(240, 152, 410, 152, ORG, 1, "4 4", .5)
b += line(240, 174, 410, 174, ORG, 1, "4 4", .5)
b += hand(210)
b += arrow("f1", "r", 318, 142, 318, 162, 3)      # một mũi ngắn: dẫn chậm
b += text(326, 88, "rút nhiệt", RED, 14, "start", "700")
b += text(326, 106, "chậm", RED, 14, "start", "700")
b += text(325, 208, "gỗ", ORG, 15, "middle", "700")
b += text(325, 228, "5 °C", ORG, 14, "middle", "700")

b += line(16, 244, 424, 244, "currentColor", 1.5, "", .5)
b += text(16, 266, "Cùng nhiệt độ, khác tốc độ dẫn nhiệt", "currentColor", 14, "start", "600")
b += text(16, 286, "→ khác cảm giác", "currentColor", 14, "start", "600")
fig1 = wrap("0 0 440 298", "Bàn tay đặt lên thanh kim loại 5 độ C và thanh gỗ 5 độ C: kim loại rút nhiệt từ tay nhanh hơn nên thấy buốt hơn",
            b, "Hình 1. Cùng 5 °C, nhưng kim loại rút nhiệt từ tay nhanh hơn gỗ. Cảm giác không phải là nhiệt độ.")

# ======================================================= Hình 2: hai cách làm biến đổi nội năng (vẽ lại 31/10/2026: chữ >= 14)
b = defs("f2")
b += text(16, 22, "Hai cách làm biến đổi nội năng", "currentColor", 15, "start", "700")

# --- a) thực hiện công: xilanh bị nén
b += text(16, 48, "a) Thực hiện công", "currentColor", 14, "start", "700")
b += rect(42, 144, 62, 48, "rgba(56,189,248,.16)", "none", 0, 0)        # phần khí bị nén (dưới pit-tông)
b += '<path d="M40 106 L40 188 Q40 194 46 194 L100 194 Q106 194 106 188 L106 106" fill="none" stroke="currentColor" stroke-width="2.5"/>'  # xilanh hở miệng
for i in range(9):                      # cùng số phân tử dồn vào thể tích nhỏ hơn -> dày hơn
    b += dot(54 + (i % 3) * 19, 156 + (i // 3) * 14, 3.4, BLUE)
b += rect(42, 130, 62, 14, "rgba(148,163,184,.35)", "currentColor", 2, 3)  # pit-tông nằm trong xilanh, đã ép xuống thấp
b += arrow("f2", "r", 73, 62, 73, 128, 3)         # đẩy pit-tông XUỐNG (y tăng)
b += text(84, 92, "đẩy xuống", RED, 14, "start", "700")
b += text(73, 216, "khí bị nén", "currentColor", 14, "middle", "600")
b += text(73, 236, "A dương", RED, 14, "middle", "700")

# --- b) truyền nhiệt: ống nghiệm hơ trên ngọn lửa
b += text(162, 48, "b) Truyền nhiệt", "currentColor", 14, "start", "700")
b += rect(176, 104, 66, 90, "rgba(248,113,113,.10)", "currentColor", 2.5)
for i in range(6):
    b += dot(188 + (i % 3) * 21, 128 + (i // 3) * 30, 3.4, RED)
b += arrow("f2", "r", 209, 220, 209, 178, 3)      # nhiệt đi từ ngọn lửa VÀO ống
b += text(200, 214, "nhiệt", RED, 14, "end", "700")
b += f'<path d="M209 252 q-14 -14 0 -27 q14 13 0 27 z" fill="{ORG}" stroke="{ORG}" stroke-width="2"/>'
b += text(224, 246, "ngọn lửa", ORG, 14, "start", "700")
b += text(209, 274, "Q dương", RED, 14, "middle", "700")
b += text(146, 304, "cùng một kết quả: nội năng tăng", "currentColor", 14, "middle", "600")

# --- hai ví dụ đời thường bên phải
b += line(294, 36, 294, 282, "currentColor", 1, "4 4", .4)
b += text(304, 62, "Xoa hai bàn tay", "currentColor", 14, "start", "700")
b += text(304, 80, "→ công ma sát", GRN, 14, "start", "600")
b += text(304, 114, "Hơ ống nghiệm", "currentColor", 14, "start", "700")
b += text(304, 132, "trên ngọn lửa", "currentColor", 14, "start", "700")
b += text(304, 150, "→ nhiệt truyền vào", GRN, 14, "start", "600")
b += text(304, 186, "Cách phân biệt:", "currentColor", 14, "start", "700")
b += text(304, 204, "có lực làm vật", GRN, 14, "start", "600")
b += text(304, 222, "dịch chuyển", GRN, 14, "start", "600")
b += text(304, 240, "hay không?", GRN, 14, "start", "600")
fig2 = wrap("0 0 440 316", "Hai cách làm biến đổi nội năng: nén khí bằng công và hơ nóng bằng truyền nhiệt, cùng làm nội năng tăng",
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

# ======================================================= Hình 4: sơ đồ định luật I cho bài toán bơm (vẽ lại 31/10/2026: chữ >= 14)
b = defs("f4")
b += text(16, 24, "Định luật I cho một lần ấn bơm", "currentColor", 15, "start", "700")

# xilanh
b += rect(120, 100, 84, 116, "rgba(56,189,248,.12)", "currentColor", 2.5)
for i in range(6):
    b += dot(136 + (i % 3) * 26, 140 + (i // 3) * 36, 3.4, BLUE)
b += rect(112, 84, 100, 15, "rgba(148,163,184,.35)", "currentColor", 2, 4)
b += arrow("f4", "r", 162, 40, 162, 82, 3)        # công ép pit-tông XUỐNG
b += text(176, 54, "công 60 J", RED, 15, "start", "700")
b += text(176, 74, "tay truyền cho khí", "currentColor", 14, "start", "600")
b += text(162, 240, "khối khí", "currentColor", 14, "middle", "600")

# nhiệt toả ra qua thành ống
b += arrow("f4", "b", 208, 150, 276, 128, 3.5)
b += text(284, 116, "toả ra 15 J", BLUE, 15, "start", "700")
b += text(284, 136, "qua thành ống", "currentColor", 14, "start", "600")

# hộp kết quả
b += rect(284, 156, 144, 86, "rgba(52,211,153,.14)", GRN, 2.5)
b += text(356, 182, "ΔU = A + Q", "currentColor", 15, "middle", "700")
b += text(356, 206, "= 60 + (−15)", "currentColor", 15, "middle", "600")
b += text(356, 231, "= +45 J", GRN, 16, "middle", "700")

b += line(16, 262, 424, 262, "currentColor", 1.5, "", .5)
b += text(16, 284, "Nhận vào thì dương: công +60 J", "currentColor", 14, "start", "600")
b += text(16, 304, "Mất đi thì âm: nhiệt −15 J", "currentColor", 14, "start", "600")
fig4 = wrap("0 0 440 316", "Sơ đồ định luật I cho một lần ấn bơm: công 60 J truyền vào khí, khí toả ra 15 J, độ biến thiên nội năng bằng 45 J",
            b, "Hình 4. Một lần bơm: công 60 J vào khí, nhiệt 15 J ra khỏi khí: ΔU = 60 + (−15) = +45 J.")

# ------------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(margin_figs(src))
print("ok", len(src), "bytes")
