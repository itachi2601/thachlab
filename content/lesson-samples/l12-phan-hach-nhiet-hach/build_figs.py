"""Sinh 4 hình SVG cho bài "Bài 16. Phản ứng phân hạch, phản ứng nhiệt hạch và ứng dụng"
(Vật lí 12) và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html.
Chạy từ thư mục này: python3 build_figs.py
"""
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
    "Nhãn: control rods = thanh điều khiển; fuel rods = nhiên liệu; steam turbine = tua bin hơi.<br>"
    "<small>Hình: OpenStax, College Physics 2e, Hình 32.23 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small>")

fig2 = anh(
    "hinh-phan-hach-4-buoc-d2.webp",
    "Bốn bước phân hạch: nơtron đến gần hạt nhân nặng, hạt nhân biến dạng thắt ở giữa, tách thành hai mảnh mang điện dương đẩy nhau, rồi hai mảnh vỡ bay ra cùng nơtron mới",
    661, 1000,
    "Hình 2. Phân hạch: hạt nhân thắt giữa rồi vỡ thành hai mảnh (FF).<br>"
    "<small>Hình: OpenStax, College Physics 2e, Hình 32.21 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small>")

# ------------------------------------------------- Hình 3: ba kiểu phát triển dây chuyền
b = defs("f3")
b += text(14, 22, "Số nơtron theo từng thế hệ", "currentColor", 13, "start", "700")
b += text(56, 38, "số nơtron", "currentColor", 12, "middle", "600")
b += line(56, 190, 420, 190, "currentColor", 2)
b += line(56, 190, 56, 46, "currentColor", 2)
b += arrow("f3", "g", 56, 62, 56, 46, 2)
b += arrow("f3", "g", 400, 190, 418, 190, 2)
b += text(432, 212, "thế hệ", "currentColor", 12.5, "end", "600")
for gx, nhan in ((100, "1"), (200, "2"), (300, "3")):
    b += text(gx, 208, nhan, "currentColor", 12.5, "middle", "600")
    b += dot(gx, 192, 2, "currentColor")
b += text(48, 154, "4", "currentColor", 12.5, "end", "600")
b += f'<polyline fill="none" stroke="{RED}" stroke-width="2.6" points="100,150 200,130 300,100"/>'
for x, y in ((100, 150), (200, 130), (300, 100)):
    b += dot(x, y, 4, RED)
b += f'<polyline fill="none" stroke="{GRN}" stroke-width="2.6" points="100,150 200,150 300,150"/>'
for x in (200, 300):
    b += dot(x, 150, 4, GRN)
b += f'<polyline fill="none" stroke="{BLUE}" stroke-width="2.6" points="100,150 200,166 300,176"/>'
for x, y in ((200, 166), (300, 176)):
    b += dot(x, y, 4, BLUE)
b += text(310, 96, "k &gt; 1: tăng nhanh", RED, 12.5, "start", "700")
b += text(310, 146, "k = 1: giữ nguyên", GRN, 12.5, "start", "700")
b += text(310, 180, "k &lt; 1: tắt dần", BLUE, 12.5, "start", "700")
b += text(56, 232, "mỗi điểm là một thế hệ nơtron; k = tỉ số hai thế hệ liền nhau", "currentColor", 11.5)
fig3 = wrap("0 0 440 240",
            "Đồ thị số nơtron theo thế hệ với ba trường hợp: k nhỏ hơn 1 giảm dần, k bằng 1 giữ nguyên, k lớn hơn 1 tăng nhanh",
            b, "Hình 3. Số nơtron theo từng thế hệ: ba kiểu phát triển.")

# ------------------------------------------------- Hình 4: nhiệt hạch và Mặt trời
b = defs("f4")
b += text(14, 22, "a) Một phản ứng nhiệt hạch", "currentColor", 13, "start", "700")
for px, py in ((32, 80), (60, 80), (32, 112), (60, 112)):
    b += circ(px, py, 11, "rgba(56,189,248,.18)", BLUE)
    b += text(px, py + 4, "p", BLUE, 13, "middle", "700")
b += arrow("f4", "r", 80, 96, 124, 96, 2.4)
b += text(106, 84, "kết hợp", RED, 12.5, "middle", "700")
b += circ(162, 96, 30, "rgba(52,211,153,.18)", GRN)
b += text(162, 101, "He-4", GRN, 13, "middle", "700")
b += text(200, 88, '2e<tspan baseline-shift="super" font-size="10">+</tspan>', BLUE, 12.5, "start", "700")
b += text(200, 108, "2 nơtrinô", BLUE, 12.5, "start", "700")
b += text(162, 156, "toả 26,7 MeV", ORG, 12.5, "middle", "700")
b += text(240, 22, "b) Lò nhiệt hạch tự nhiên", "currentColor", 13, "start", "700")
b += circ(330, 105, 48, "rgba(251,146,60,.16)", ORG)
for k in range(8):
    a = k * math.pi / 4
    b += line(round(330 + 52 * math.cos(a), 1), round(105 + 52 * math.sin(a), 1),
              round(330 + 62 * math.cos(a), 1), round(105 + 62 * math.sin(a), 1), ORG, 2.4)
b += text(330, 111, "Mặt trời", ORG, 13, "middle", "700")
b += text(330, 186, "lõi ~15 triệu K", "currentColor", 12, "middle")
b += text(330, 202, "giam bằng lực hấp dẫn", "currentColor", 12, "middle")
fig4 = wrap("0 0 440 216",
            "Nhiệt hạch: bốn prôtôn kết hợp thành hạt nhân heli và toả năng lượng; Mặt trời là lò nhiệt hạch tự nhiên",
            b, "Hình 4. Nhiệt hạch: hạt nhân nhẹ kết hợp lại; Mặt trời là lò tự nhiên.")

# ------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
