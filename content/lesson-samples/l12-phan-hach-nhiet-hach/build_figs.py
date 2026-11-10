"""Sinh 4 hình SVG cho bài "Bài 16. Phản ứng phân hạch, phản ứng nhiệt hạch và ứng dụng"
(Vật lí 12) và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html.
Chạy từ thư mục này: python3 build_figs.py
"""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import math
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
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>')


def circ(x, y, r, fill, stroke, sw=2):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def hop(x, y, w, h, s, c="currentColor", size=11):
    return rect(x, y, w, h, "rgba(148,163,184,.10)") + text(x + w / 2, y + h / 2 + 4, s, c, size, "middle", "700")


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


# ------------------------------------------------- Hình 1, 2: ảnh OpenStax (đợt 2, 27/10/2026)
def anh(file, alt, w, h, cap):
    return (f'<figure class="fig" data-tl="1"><img src="/assets/openstax/l12-phan-hach-nhiet-hach/{file}" alt="{alt}" '
            f'loading="lazy" width="{w}" height="{h}"><figcaption>{cap}</figcaption></figure>')


fig1 = anh(
    "hinh-lo-ap-luc-d2.webp",
    "Sơ đồ nhà máy điện hạt nhân lò nước áp lực: thanh nhiên liệu và thanh điều khiển trong lò, bộ trao đổi nhiệt, tua bin hơi, máy phát điện, bình ngưng",
    1000, 611,
    "Hình 1. Nhà máy điện hạt nhân: nhiệt sinh ra trong lò.<br>"
    "Nhãn: control rods = thanh điều khiển; fuel rods = nhiên liệu; heat exchanger = bộ trao đổi nhiệt; steam turbine = tua bin hơi; condenser = bình ngưng; electric generator = máy phát; primary/secondary system = vòng sơ cấp/thứ cấp.<br>"
    "<small>Hình: OpenStax, College Physics 2e, Hình 32.23 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small>")

fig2 = anh(
    "hinh-phan-hach-4-buoc-d2.webp",
    "Bốn bước phân hạch: nơtron đến gần hạt nhân nặng, hạt nhân biến dạng thắt ở giữa, tách thành hai mảnh mang điện dương đẩy nhau, rồi hai mảnh vỡ bay ra cùng nơtron mới",
    661, 1000,
    "Hình 2. Phân hạch: hạt nhân thắt giữa rồi vỡ thành hai mảnh (FF).<br>"
    "<small>Hình: OpenStax, College Physics 2e, Hình 32.21 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small>")

# ------------------------------------------------- Hình 3: ba kiểu phát triển dây chuyền
# Số liệu thật trên trục tuyến tính (16 px / nơtron, gốc y0 = 220):
#   k = 1,5: 4 -> 6 -> 9 ; k = 1: 4 -> 4 -> 4 ; k = 0,5: 4 -> 2 -> 1
Y0, KY = 220, 16
GX = (110, 200, 290)
F = 14


def yv(v):
    return Y0 - KY * v


b = defs("f3")
b += text(14, 22, "Số nơtron theo từng thế hệ", "currentColor", 15, "start", "700")
b += line(60, Y0, 300, Y0, "currentColor", 2)
b += line(60, Y0, 60, 56, "currentColor", 2)
b += line(60, 56, 60, 48, "currentColor", 2)
b += chevron(60, 48, 0, -1, "currentColor", 2, 9)
b += line(300, Y0, 306, Y0, "currentColor", 2)
b += chevron(306, Y0, 1, 0, "currentColor", 2, 9)
b += text(70, 54, "số nơtron", "currentColor", F, "start", "600")
for v in (2, 4, 6, 8):
    b += line(56, yv(v), 60, yv(v), "currentColor", 1.6)
    b += line(60, yv(v), 290, yv(v), "currentColor", 1, "3 4", .25)
    b += text(50, yv(v) + 5, str(v), "currentColor", F, "end", "600")
b += text(50, Y0 + 5, "0", "currentColor", F, "end", "600")
for gx, nhan in zip(GX, ("1", "2", "3")):
    b += line(gx, Y0, gx, Y0 + 4, "currentColor", 1.6)
    b += text(gx, Y0 + 21, nhan, "currentColor", F, "middle", "600")
b += text(316, Y0 + 21, "thế hệ", "currentColor", F, "start", "600")
for col, vals in ((RED, (4, 6, 9)), (GRN, (4, 4, 4)), (BLUE, (4, 2, 1))):
    pts = " ".join(f"{x},{yv(v)}" for x, v in zip(GX, vals))
    b += f'<polyline fill="none" stroke="{col}" stroke-width="2.6" points="{pts}"/>'
    for x, v in zip(GX, vals):
        b += dot(x, yv(v), 4, col)
b += dot(GX[0], yv(4), 4.5, "currentColor")
b += text(316, yv(9) + 5, "k = 1,5", RED, F, "start", "700")
b += text(316, yv(9) + 23, "tăng nhanh", RED, F, "start", "600")
b += text(316, yv(4) - 4, "k = 1", GRN, F, "start", "700")
b += text(316, yv(4) + 14, "giữ nguyên", GRN, F, "start", "600")
b += text(316, yv(1) - 8, "k = 0,5", BLUE, F, "start", "700")
b += text(316, yv(1) + 10, "tắt dần", BLUE, F, "start", "600")
b += text(14, 268, "Mỗi chấm: số nơtron của một thế hệ.", "currentColor", F, "start", "500")
b += text(14, 288, "k = số nơtron thế hệ sau ÷ thế hệ trước.", "currentColor", F, "start", "500")
fig3 = wrap("0 0 440 298",
            "Đồ thị số nơtron theo thế hệ, cùng xuất phát 4 nơtron: k bằng 1,5 tăng 4, 6, 9; k bằng 1 giữ 4; k bằng 0,5 giảm 4, 2, 1",
            b, "Hình 3. Số nơtron theo từng thế hệ: ba kiểu phát triển.")

# ------------------------------------------------- Hình 4: nhiệt hạch và Mặt trời
GREY = "#94a3b8"


def nuc(x, y, kind):
    c, f, lab = (BLUE, "rgba(56,189,248,.22)", "p") if kind == "p" else (GREY, "rgba(148,163,184,.25)", "n")
    return circ(x, y, 11, f, c, 1.8) + text(x, y + 5, lab, c, 13, "middle", "700")


b = defs("f4")
b += text(14, 22, "a) Phản ứng nhiệt hạch", "currentColor", 15, "start", "700")
for px, py in ((24, 84), (50, 84), (24, 110), (50, 110)):
    b += nuc(px, py, "p")
b += arrow("f4", "r", 68, 97, 108, 97, 2.4)
b += text(88, 62, "kết hợp", RED, 14, "middle", "700")
b += circ(146, 97, 31, "rgba(52,211,153,.12)", GRN, 2)
for (dx, dy), k in (((-12, -12), "p"), ((12, -12), "n"), ((-12, 12), "n"), ((12, 12), "p")):
    b += nuc(146 + dx, 97 + dy, k)
b += text(146, 150, "He-4 = 2p + 2n", GRN, 14, "middle", "700")
b += arrow("f4", "b", 179, 84, 198, 70, 2.2)
b += text(202, 74, '2e<tspan baseline-shift="super" font-size="11">+</tspan>', BLUE, 14, "start", "700")
b += arrow("f4", "b", 179, 110, 198, 124, 2.2)
b += text(202, 130, "2 nơtrinô", BLUE, 14, "start", "700")
b += text(14, 182, "toả 26,7 MeV", ORG, 14, "start", "700")
b += text(14, 202, "điện tích: 4 = 2 (He) + 2 (e⁺)", "currentColor", 14, "start", "600")
SX, SY, SR = 366, 100, 42
b += text(SX, 22, "b) Mặt trời", "currentColor", 15, "middle", "700")
b += circ(SX, SY, SR, "rgba(251,146,60,.16)", ORG)
for k in range(8):
    a = k * math.pi / 4 + math.pi / 8
    b += line(round(SX + 47 * math.cos(a), 1), round(SY + 47 * math.sin(a), 1),
              round(SX + 56 * math.cos(a), 1), round(SY + 56 * math.sin(a), 1), ORG, 2.4)
b += circ(SX, SY, 16, "rgba(251,146,60,.40)", ORG, 1.8)
b += text(SX, SY + 5, "lõi", "currentColor", 13, "middle", "700")
for k in range(4):
    a = k * math.pi / 2 + math.pi / 4
    b += arrow("f4", "r", round(SX + 39 * math.cos(a), 1), round(SY + 39 * math.sin(a), 1),
               round(SX + 21 * math.cos(a), 1), round(SY + 21 * math.sin(a), 1), 2.2)
b += text(SX, 182, "lõi ~15 triệu K", "currentColor", 14, "middle", "600")
b += text(SX, 202, "hấp dẫn ép vào lõi", RED, 14, "middle", "700")
fig4 = wrap("0 0 440 212",
            "a) Bốn prôtôn kết hợp thành hạt nhân heli gồm 2 prôtôn và 2 nơtron, phát ra 2 pôzitron và 2 nơtrinô, toả 26,7 MeV. b) Mặt trời: lõi khoảng 15 triệu K, lực hấp dẫn ép khối khí vào lõi",
            b, "Hình 4. Nhiệt hạch: hạt nhân nhẹ kết hợp lại; Mặt trời là lò tự nhiên.")

# ------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(margin_figs(src))
print("ok", len(src), "bytes")
