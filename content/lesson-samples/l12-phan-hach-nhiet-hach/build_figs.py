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


# ------------------------------------------------- Hình 1: nhà máy điện hạt nhân (mở bài)
b = defs("f1")
b += text(14, 22, "Nhà máy điện hạt nhân: không đốt gì cả", "currentColor", 13, "start", "700")
b += text(3, 52, "nhiên liệu + thanh điều khiển", ORG, 10, "start", "600")
for x, nhan in ((3, "Lò phản ứng"), (117, "Bộ trao đổi nhiệt"), (231, "Tua bin"), (345, "Máy phát điện")):
    b += rect(x, 60, 92, 80, "rgba(148,163,184,.10)")
    if nhan == "Bộ trao đổi nhiệt":
        b += text(x + 46, 96, "Bộ trao", "currentColor", 11, "middle", "700")
        b += text(x + 46, 112, "đổi nhiệt", "currentColor", 11, "middle", "700")
    else:
        b += text(x + 46, 104, nhan, "currentColor", 10 if len(nhan) > 11 else 11, "middle", "700")
for x in (95, 209, 323):
    b += arrow("f1", "r", x, 100, x + 20, 100, 2.4)
b += text(3, 168, "nhiệt của phản ứng → hơi nước → tua bin → điện năng", ORG, 11, "start", "700")
b += text(3, 192, "nguồn nhiệt nằm trong lòng thanh nhiên liệu, không có ngọn lửa nào", "currentColor", 10)
fig1 = wrap("0 0 440 210",
            "Sơ đồ nhà máy điện hạt nhân: lò phản ứng cấp nhiệt cho bộ trao đổi nhiệt, hơi nước chạy tua bin rồi máy phát điện",
            b, "Hình 1. Nhà máy điện hạt nhân: lò phản ứng → bộ trao đổi nhiệt → tua bin → máy phát điện, "
               "không hề đốt nhiên liệu.")

# ------------------------------------------------- Hình 2: phân hạch U-235
b = defs("f2")
b += text(14, 22, "Phân hạch U-235", "currentColor", 13, "start", "700")
b += circ(78, 112, 36, "rgba(248,113,113,.18)", RED)
b += text(78, 117, "U-235", RED, 12, "middle", "700")
b += circ(24, 74, 8, BLUE, BLUE)
b += text(24, 58, "n", BLUE, 11, "middle", "700")
b += arrow("f2", "b", 36, 80, 50, 92, 2.4)
b += arrow("f2", "r", 116, 112, 166, 112, 2.6)
b += text(141, 102, "vỡ ra", RED, 11, "middle", "700")
b += circ(230, 84, 28, "rgba(251,146,60,.18)", ORG)
b += text(230, 89, "Ba-144", ORG, 11, "middle", "700")
b += circ(222, 160, 26, "rgba(56,189,248,.18)", BLUE)
b += text(222, 165, "Kr-89", BLUE, 11, "middle", "700")
for ny in (56, 100, 144):
    b += circ(306, ny, 8, BLUE, BLUE)
    b += text(320, ny + 4, "n", BLUE, 10, "start", "700")
b += arrow("f2", "b", 256, 74, 290, 62, 2)
b += arrow("f2", "b", 246, 148, 290, 140, 2)
b += text(200, 196, "2–3 neutron mới", BLUE, 11, "start", "700")
b += text(432, 196, "toả ≈ 173 MeV", ORG, 12, "end", "700")
fig2 = wrap("0 0 440 210",
            "Một neutron chậm bị U-235 hấp thụ, hạt nhân vỡ thành hai mảnh Ba-144 và Kr-89, nhả thêm 2 đến 3 neutron và toả năng lượng",
            b, "Hình 2. Neutron chậm bị U-235 hấp thụ: hạt nhân vỡ thành Ba-144 và Kr-89, nhả thêm "
               "2–3 neutron và toả cỡ 173 MeV.")

# ------------------------------------------------- Hình 3: ba kiểu phát triển dây chuyền
b = defs("f3")
b += text(14, 22, "Số neutron theo từng thế hệ", "currentColor", 13, "start", "700")
b += text(56, 38, "số neutron", "currentColor", 10, "middle", "600")
b += line(56, 190, 420, 190, "currentColor", 2)
b += line(56, 190, 56, 46, "currentColor", 2)
b += arrow("f3", "g", 56, 62, 56, 46, 2)
b += arrow("f3", "g", 400, 190, 418, 190, 2)
b += text(432, 212, "thế hệ", "currentColor", 11, "end", "600")
for gx, nhan in ((100, "1"), (200, "2"), (300, "3")):
    b += text(gx, 208, nhan, "currentColor", 11, "middle", "600")
    b += dot(gx, 192, 2, "currentColor")
b += text(48, 154, "4", "currentColor", 10, "end", "600")
b += f'<polyline fill="none" stroke="{RED}" stroke-width="2.6" points="100,150 200,130 300,100"/>'
for x, y in ((100, 150), (200, 130), (300, 100)):
    b += dot(x, y, 4, RED)
b += f'<polyline fill="none" stroke="{GRN}" stroke-width="2.6" points="100,150 200,150 300,150"/>'
for x in (200, 300):
    b += dot(x, 150, 4, GRN)
b += f'<polyline fill="none" stroke="{BLUE}" stroke-width="2.6" points="100,150 200,166 300,176"/>'
for x, y in ((200, 166), (300, 176)):
    b += dot(x, y, 4, BLUE)
b += text(310, 96, "k &gt; 1: tăng nhanh", RED, 11, "start", "700")
b += text(310, 146, "k = 1: giữ nguyên", GRN, 11, "start", "700")
b += text(310, 180, "k &lt; 1: tắt dần", BLUE, 11, "start", "700")
b += text(56, 232, "mỗi điểm là một thế hệ neutron; k là tỉ số giữa hai thế hệ liền nhau", "currentColor", 10)
fig3 = wrap("0 0 440 240",
            "Đồ thị số neutron theo thế hệ với ba trường hợp: k nhỏ hơn 1 giảm dần, k bằng 1 giữ nguyên, k lớn hơn 1 tăng nhanh",
            b, "Hình 3. Ba kiểu phát triển: k &lt; 1 giảm dần rồi tắt, k = 1 giữ nguyên, k &gt; 1 tăng nhanh.")

# ------------------------------------------------- Hình 4: nhiệt hạch và Mặt trời
b = defs("f4")
b += text(14, 22, "a) Một phản ứng nhiệt hạch", "currentColor", 13, "start", "700")
for px, py in ((40, 80), (72, 80), (40, 112), (72, 112)):
    b += circ(px, py, 11, "rgba(56,189,248,.18)", BLUE)
    b += text(px, py + 4, "p", BLUE, 11, "middle", "700")
b += arrow("f4", "r", 86, 96, 124, 96, 2.4)
b += text(105, 85, "kết hợp", RED, 10, "middle", "700")
b += circ(162, 96, 30, "rgba(52,211,153,.18)", GRN)
b += text(162, 101, "He-4", GRN, 12, "middle", "700")
b += text(200, 88, "2e+", BLUE, 10, "start", "700")
b += text(200, 106, "2 nơtrino", BLUE, 10, "start", "700")
b += text(162, 156, "toả 26,7 MeV", ORG, 11, "middle", "700")
b += text(240, 22, "b) Lò nhiệt hạch tự nhiên", "currentColor", 13, "start", "700")
b += circ(330, 105, 48, "rgba(251,146,60,.16)", ORG)
for k in range(8):
    a = k * math.pi / 4
    b += line(round(330 + 52 * math.cos(a), 1), round(105 + 52 * math.sin(a), 1),
              round(330 + 62 * math.cos(a), 1), round(105 + 62 * math.sin(a), 1), ORG, 2.4)
b += text(330, 111, "Mặt trời", ORG, 12, "middle", "700")
b += text(240, 186, "lõi ~15 triệu K · giam bằng lực hấp dẫn", "currentColor", 10)
fig4 = wrap("0 0 440 216",
            "Nhiệt hạch: bốn proton kết hợp thành hạt nhân heli và toả năng lượng; Mặt trời là lò nhiệt hạch tự nhiên",
            b, "Hình 4. Nhiệt hạch: hạt nhân rất nhẹ kết hợp thành hạt nhân nặng hơn và toả năng lượng; "
               "Mặt trời là lò nhiệt hạch tự nhiên.")

# ------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
