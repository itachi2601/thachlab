"""Sinh 4 hình SVG cho bài "Bài 3. Nội năng. Định luật I Nhiệt động lực học" (Vật lí 12)
và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html.
Chạy từ thư mục này: python3 build_figs.py
"""
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
b += text(16, 22, "Cùng 5 °C — vì sao kim loại buốt hơn gỗ?", "currentColor", 12.5, "start", "700")

# bàn tay
b += f'<path d="M158 74 q0 -16 16 -16 q16 0 16 16 l0 18 q10 -6 18 2 q6 6 2 14 l-8 16 q-4 8 -12 8 l-24 0 q-8 0 -12 -8 l-10 -20 q-4 -8 2 -14 q8 -8 16 -2 z" fill="rgba(148,163,184,.20)" stroke="currentColor" stroke-width="2"/>'
b += text(210, 60, "tay em 33 °C", "currentColor", 11, "start", "600")

# thanh kim loại
b += rect(40, 140, 150, 46, "rgba(56,189,248,.18)", BLUE, 2.5)
b += text(115, 168, "kim loại", BLUE, 13, "middle", "700")
b += text(115, 206, "5 °C", BLUE, 12, "middle", "700")
# mũi tên nhiệt đi ra, dài (dẫn nhanh)
b += arrow("f1", "r", 66, 128, 66, 72, 4.5)
b += text(78, 104, "rút nhiệt", RED, 11, "start", "700")
b += text(78, 119, "rất nhanh", RED, 11, "start", "600")

# thanh gỗ (vẽ thêm vân gỗ)
b += rect(250, 140, 150, 46, "rgba(251,146,60,.20)", ORG, 2.5)
b += line(250, 156, 400, 156, ORG, 1, "4 4", .5)
b += line(250, 170, 400, 170, ORG, 1, "4 4", .5)
b += text(325, 168, "gỗ", ORG, 13, "middle", "700")
b += text(325, 206, "5 °C", ORG, 12, "middle", "700")
# mũi tên nhiệt đi ra, ngắn (dẫn chậm)
b += arrow("f1", "r", 274, 132, 274, 96, 2.5)
b += text(286, 118, "rút nhiệt chậm", RED, 11, "start", "600")

b += line(16, 222, 404, 222, "currentColor", 1.5, "", .5)
b += text(16, 240, "Cùng nhiệt độ, khác tốc độ dẫn nhiệt → khác cảm giác", "currentColor", 11, "start", "600")
fig1 = wrap("0 0 420 252", "Bàn tay đặt lên thanh kim loại 5 độ C và thanh gỗ 5 độ C: kim loại rút nhiệt từ tay nhanh hơn nên thấy buốt hơn",
            b, "Hình 1. Hai vật cùng 5 °C nhưng kim loại dẫn nhiệt nhanh hơn gỗ, rút nhiệt từ tay nhanh hơn — nên tay thấy buốt. Cảm giác không phải là nhiệt độ.")

# ======================================================= Hình 2: hai cách làm biến đổi nội năng
b = defs("f2")
b += text(16, 20, "Hai cách làm biến đổi nội năng", "currentColor", 12.5, "start", "700")

# --- a) thực hiện công: xilanh bị nén
b += text(16, 50, "a) Thực hiện công", "currentColor", 12, "start", "700")
b += rect(46, 100, 66, 87, "rgba(56,189,248,.12)", "currentColor", 2.5)
for i in range(6):                      # các phân tử khí
    x = 56 + (i % 3) * 18
    y = 120 + (i // 3) * 28
    b += dot(x, y, 3.2, BLUE)
b += rect(40, 86, 78, 14, "rgba(148,163,184,.35)", "currentColor", 2, 4)   # pit-tông
b += line(79, 74, 79, 84, "currentColor", 3)
b += arrow("f2", "r", 79, 72, 79, 46, 4)
b += text(92, 78, "đẩy xuống", RED, 11, "start", "700")
b += text(79, 204, "khí bị nén", "currentColor", 11.5, "middle", "600")
b += text(79, 222, "A dương", RED, 11.5, "middle", "700")

# --- b) truyền nhiệt: ngọn lửa
b += text(166, 50, "b) Truyền nhiệt", "currentColor", 12, "start", "700")
b += rect(178, 100, 66, 92, "rgba(248,113,113,.10)", "currentColor", 2.5)
for i in range(6):
    x = 188 + (i % 3) * 18
    y = 120 + (i // 3) * 28
    b += dot(x, y, 3.2, RED)
b += arrow("f2", "r", 204, 126, 204, 96, 3.5)
b += text(222, 100, "nhiệt", RED, 11, "start", "700")
b += f'<path d="M204 242 q-14 -14 0 -26 q14 12 0 26 z" fill="{ORG}" stroke="{ORG}" stroke-width="2"/>'
b += text(216, 236, "ngọn lửa", ORG, 11, "start", "700")
b += text(209, 264, "Q dương", RED, 11.5, "middle", "700")
b += text(209, 284, "cùng một kết quả: nội năng tăng", "currentColor", 11, "middle", "600")

# --- hai ví dụ đời thường bên phải
b += line(292, 40, 292, 240, "currentColor", 1, "4 4", .4)
b += text(304, 60, "Xoa hai bàn tay", "currentColor", 11.5, "start", "700")
b += text(304, 76, "→ công của ma sát", GRN, 11, "start", "600")
b += text(304, 108, "Hơ ống nghiệm", "currentColor", 11.5, "start", "700")
b += text(304, 124, "trên ngọn lửa", "currentColor", 11.5, "start", "700")
b += text(304, 140, "→ nhiệt truyền vào", GRN, 11, "start", "600")
b += text(304, 176, "Cách phân biệt:", "currentColor", 11.5, "start", "700")
b += text(304, 192, "có lực làm vật", GRN, 11, "start", "600")
b += text(304, 206, "dịch chuyển không?", GRN, 11, "start", "600")
fig2 = wrap("0 0 440 300", "Hai cách làm biến đổi nội năng: nén khí bằng công và hơ nóng bằng truyền nhiệt, cùng làm nội năng tăng",
            b, "Hình 2. Nội năng đổi bằng hai đường: thực hiện công (có lực làm dịch chuyển) hoặc truyền nhiệt (chênh nhiệt độ). Cả hai đều dẫn tới nội năng tăng.")

# ======================================================= Hình 3: cùng khối lượng, cùng độ tăng nhiệt độ
b = defs("f3")
b += text(16, 24, "Cùng 1 kg, cùng tăng 1 K — khác nhiệt lượng", "currentColor", 13, "start", "700")

# cốc nước
b += f'<path d="M56 52 l8 122 q1 10 11 10 l48 0 q10 0 11 -10 l8 -122 z" fill="rgba(56,189,248,.16)" stroke="currentColor" stroke-width="2.5"/>'
b += line(58, 76, 140, 76, BLUE, 3)          # mặt nước
b += text(99, 118, "1 kg", BLUE, 13, "middle", "700")
b += text(99, 138, "nước", BLUE, 12, "middle", "600")
b += text(99, 200, "c nước = 4180", BLUE, 13, "middle", "700")
b += text(99, 218, "nhiệt cần: 4180 J", "currentColor", 11.5, "middle", "600")
for i in range(5):                            # ô nhiệt lượng
    b += rect(58 + i * 17, 160, 14, 22, "rgba(56,189,248,.45)", BLUE, 1.5, 3)

# thỏi nhôm
b += rect(258, 96, 104, 66, "rgba(251,146,60,.20)", ORG, 2.5)
b += text(310, 128, "1 kg", ORG, 13, "middle", "700")
b += text(310, 146, "nhôm", ORG, 12, "middle", "600")
b += text(310, 200, "c nhôm = 880", ORG, 13, "middle", "700")
b += text(310, 218, "nhiệt cần: 880 J", "currentColor", 11.5, "middle", "600")
for i in range(2):
    b += rect(282 + i * 17, 160, 14, 22, "rgba(251,146,60,.45)", ORG, 1.5, 3)

b += text(220, 70, "cùng", "currentColor", 11, "middle", "600")
b += text(220, 86, "tăng 1 K", "currentColor", 11, "middle", "600")
b += line(16, 236, 424, 236, "currentColor", 1.5, "", .5)
b += text(16, 254, "c nước lớn gấp ~4,7 lần c nhôm → nước “khó nóng, khó nguội”", "currentColor", 11, "start", "600")
fig3 = wrap("0 0 440 266", "So sánh nhiệt lượng cần để làm 1 kg nước và 1 kg nhôm tăng thêm 1 K: nước cần 4180 J, nhôm chỉ cần 880 J",
            b, "Hình 3. Cùng khối lượng và cùng độ tăng nhiệt độ, nước cần nhiều nhiệt hơn nhôm gần 5 lần — vì nhiệt dung riêng của nước lớn hơn. Đó là lí do nước làm mát tốt.")

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
b += line(192, 62, 192, 78, "currentColor", 3)
b += arrow("f4", "r", 192, 60, 192, 32, 4)
b += text(206, 46, "công 60 J", RED, 12, "start", "700")
b += text(206, 62, "tay truyền cho khí", "currentColor", 11, "start", "600")
b += text(192, 236, "khối khí", "currentColor", 11.5, "middle", "600")

# nhiệt toả ra
b += arrow("f4", "b", 240, 132, 308, 110, 3.5)
b += text(314, 100, "toả ra 15 J", BLUE, 12, "start", "700")
b += text(314, 116, "qua thành ống bơm", "currentColor", 11, "start", "600")

# hộp kết quả
b += rect(302, 146, 122, 84, "rgba(52,211,153,.14)", GRN, 2.5)
b += text(363, 172, "ΔU = A + Q", "currentColor", 12.5, "middle", "700")
b += text(363, 196, "= 60 + (−15)", "currentColor", 12, "middle", "600")
b += text(363, 219, "= +45 J", GRN, 14, "middle", "700")

b += line(16, 268, 432, 268, "currentColor", 1.5, "", .5)
b += text(16, 286, "Nhận vào thì dương (công +60) · mất đi thì âm (nhiệt −15)", "currentColor", 11, "start", "600")
fig4 = wrap("0 0 440 298", "Sơ đồ định luật I cho một lần ấn bơm: công 60 J truyền vào khí, khí toả ra 15 J, độ biến thiên nội năng bằng 45 J",
            b, "Hình 4. Cùng một lần bơm: công 60 J đi vào khí, nhiệt 15 J đi ra khỏi khí. Định luật I cộng hai số đại số lại: ΔU = 60 + (−15) = +45 J.")

# ------------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
