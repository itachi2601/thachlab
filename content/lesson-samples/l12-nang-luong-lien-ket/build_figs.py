"""Sinh 4 hình SVG cho bài "Bài 15. Năng lượng liên kết hạt nhân" (Vật lí 12) và thay
các mốc <!--FIGn--> trong theory.src.html -> theory.html.
Chạy từ thư mục này: python3 build_figs.py

Thứ tự trong file = thứ tự xuất hiện trong bài: fig1 (mở bài), fig2 (mục 4),
fig3 (mục 5), fig4 (mục 6) — nhờ vậy số "Hình n." luôn khớp dòng đọc.
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


def rect(x, y, w, h, fill, stroke="currentColor", sw=2, rx=8, op=None):
    o = f' opacity="{op}"' if op is not None else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"{o}/>')


def chan(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    """Đường gấp khúc."""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<polyline fill="none" stroke="{c}" stroke-width="{w}"{d} opacity="{op}" '
            f'points="{x1},{y1} {x2},{y2}"/>')


def vach(x, y1, y2, c, w=3):
    return line(x, y1, x, y2, c, w)


def wrap_fig(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


# ------------------------------------------------- Hình 1: lực hạt nhân thắng lực đẩy tĩnh điện
b = defs("f1")
b += text(14, 24, "Trong hạt nhân: đẩy và hút cùng tồn tại", "currentColor", 12, "start", "700")
b += rect(20, 44, 186, 142, "rgba(248,113,113,.10)", RED, 1.6, 12)
b += text(113, 64, "hạt nhân heli-4", RED, 11, "middle", "700")
# 2 proton (đỏ) + 2 neutron (xanh)
b += f'<circle cx="113" cy="126" r="57" fill="none" stroke="{RED}" stroke-width="2" stroke-dasharray="6 5" opacity=".85"/>'
b += dot(76, 112, 15, RED) + dot(150, 112, 15, RED)
b += dot(113, 152, 15, BLUE) + dot(113, 86, 15, BLUE)
b += text(76, 117, "p", "#0f172a", 13, "middle", "700")
b += text(150, 117, "p", "#0f172a", 13, "middle", "700")
b += text(113, 157, "n", "#0f172a", 13, "middle", "700")
b += text(113, 91, "n", "#0f172a", 13, "middle", "700")
# hai mũi tên đẩy nhau giữa hai prôtôn
b += arrow("f1", "g", 84, 190, 142, 190, 2.6)
b += arrow("f1", "g", 142, 190, 84, 190, 2.6)
b += text(113, 210, "hai prôtôn đẩy nhau", GRN, 11, "middle", "700")
# chú thích lực hạt nhân
b += text(222, 84, "lực hạt nhân", RED, 12, "start", "700")
b += text(222, 104, "hút mọi cặp", RED, 11, "start", "600")
b += text(222, 120, "nuclôn, mạnh", RED, 11, "start", "600")
b += text(222, 136, "hơn hẳn lực", RED, 11, "start", "600")
b += text(222, 152, "đẩy tĩnh điện", RED, 11, "start", "600")
b += text(222, 176, "tầm 10⁻¹⁵ m", BLUE, 12, "start", "700")
b += text(14, 232, "4 nuclôn = 2 prôtôn (p) + 2 nơtron (n)", "currentColor", 11, "start", "600")
fig1 = wrap_fig("0 0 420 244",
                "Mô hình hạt nhân heli-4 gồm hai prôtôn đẩy nhau và hai nơtron, được lực hạt nhân hút lại",
                b,
                "Hình 1. Hạt nhân heli-4: hai prôtôn đẩy nhau, nhưng lực hạt nhân hút mọi cặp nuclôn mạnh hơn hẳn "
                "nên hạt nhân vẫn đứng vững.", exp="tn-l12-nllk-01")

# ------------------------------------------------- Hình 2: các nuclôn rời kết hợp thành hạt nhân (mục 4)
b = defs("f2")
b += text(14, 24, "Các hạt rời kết hợp lại: hụt khối, toả năng lượng", "currentColor", 12, "start", "700")
# nhóm hạt rời bên trái
b += rect(16, 46, 150, 116, "rgba(56,189,248,.10)", BLUE, 1.6, 10)
b += dot(58, 86, 13, RED) + dot(124, 86, 13, RED)
b += dot(58, 122, 13, BLUE) + dot(124, 122, 13, BLUE)
b += text(58, 91, "p", "#0f172a", 11, "middle", "700") + text(124, 91, "p", "#0f172a", 11, "middle", "700")
b += text(58, 127, "n", "#0f172a", 11, "middle", "700") + text(124, 127, "n", "#0f172a", 11, "middle", "700")
b += text(91, 182, "4 nuclôn rời", BLUE, 11, "middle", "700")
b += text(91, 198, "4,032980 u", BLUE, 12, "middle", "700")
b += text(91, 214, "kể cả 2 êlectron", "currentColor", 10, "middle", "500")
# mũi tên kết hợp
b += arrow("f2", "g", 172, 104, 232, 104, 2.6)
b += text(202, 94, "kết hợp", GRN, 11, "middle", "700")
b += text(202, 124, "toả 28,30 MeV", GRN, 11, "middle", "700")
# hạt nhân bên phải
b += f'<circle cx="300" cy="104" r="46" fill="rgba(52,211,153,.12)" stroke="{GRN}" stroke-width="2"/>'
b += dot(288, 92, 11, RED) + dot(313, 92, 11, RED) + dot(288, 118, 11, BLUE) + dot(313, 118, 11, BLUE)
b += text(288, 97, "p", "#0f172a", 10, "middle", "700") + text(313, 97, "p", "#0f172a", 10, "middle", "700")
b += text(288, 123, "n", "#0f172a", 10, "middle", "700") + text(313, 123, "n", "#0f172a", 10, "middle", "700")
b += text(300, 182, "hạt nhân heli-4", GRN, 11, "middle", "700")
b += text(300, 198, "4,002603 u", GRN, 12, "middle", "700")
b += text(300, 214, "nhẹ hơn 0,030377 u", ORG, 11, "middle", "700")
b += text(16, 240, "khối lượng hụt 0,030377 u × 931,5 MeV/u = 28,30 MeV", "currentColor", 11, "start", "600")
fig2 = wrap_fig("0 0 420 254",
                "Bốn nuclôn rời có tổng khối lượng 4,032980 u kết hợp thành hạt nhân heli-4 khối lượng 4,002603 u, hụt 0,030377 u và toả 28,30 MeV",
                b,
                "Hình 2. Tổng khối lượng bốn nuclôn rời (kể cả hai êlectron) là 4,032980 u, còn nguyên tử heli-4 chỉ 4,002603 u: phần hụt 0,030377 u đã toả ra 28,30 MeV khi hạt nhân hình thành.")

# ------------------------------------------------- Hình 3: đường cong năng lượng liên kết riêng (mục 5)
b = defs("f3")
b += text(14, 22, "Năng lượng liên kết riêng theo số khối", "currentColor", 12, "start", "700")
# trục
b += line(52, 190, 414, 190, "currentColor", 2)
b += line(52, 190, 52, 40, "currentColor", 2)
b += text(408, 208, "A", "currentColor", 12, "end", "700")
b += text(16, 36, "MeV/nuclôn", "currentColor", 11, "start", "600")
b += line(52, 60, 414, 60, "currentColor", 1, "5 4", .3)
b += text(46, 64, "8,8", "currentColor", 10, "end", "600")
b += line(52, 125, 414, 125, "currentColor", 1, "5 4", .3)
b += text(46, 129, "4,4", "currentColor", 10, "end", "600")
b += text(46, 193, "0", "currentColor", 10, "end", "600")
# vùng A=50..80 tô nhạt
b += rect(160, 44, 74, 146, "rgba(52,211,153,.10)", GRN, 1, 6)
b += text(197, 224, "vùng bền nhất", GRN, 11, "middle", "700")
b += text(197, 240, "A ≈ 50 – 80", GRN, 11, "middle", "600")
# đường cong phác hoạ: trục tung đúng thang 0–4,4–8,8, các điểm đúng giá trị
# (A, E/A) -> toạ độ; trục hoành vẽ phác hoạ, không theo tỉ lệ
diem = [(56, 174), (72, 86), (100, 77), (125, 72), (197, 60), (250, 61), (310, 66), (368, 74), (404, 78)]
d = " ".join(f"{x},{y}" for x, y in diem)
b += f'<polyline fill="none" stroke="{GRN}" stroke-width="2.6" points="{d}"/>'
for x, y in diem:
    b += dot(x, y, 3.5, GRN)
b += text(197, 52, "Fe-56", GRN, 11, "middle", "700")
b += text(38, 90, "He-4", BLUE, 10, "end", "700")
b += text(392, 66, "U-235", ORG, 10, "middle", "700")
b += text(14, 240, "trục hoành: vẽ phác hoạ", "currentColor", 9, "start", "500")
# hai mũi tên chỉ hai chiều tiến về đỉnh
b += arrow("f3", "b", 78, 170, 150, 98, 2.2)
b += text(122, 184, "nhẹ: hợp lại", BLUE, 10, "middle", "700")
b += arrow("f3", "o", 400, 94, 300, 86, 2.2)
b += text(368, 108, "nặng: vỡ ra", ORG, 10, "middle", "700")
fig3 = wrap_fig("0 0 420 250",
                "Đường cong phác hoạ năng lượng liên kết riêng theo số khối, đạt đỉnh quanh sắt-56 ở 8,8 MeV mỗi nuclôn",
                b,
                "Hình 3. Năng lượng liên kết riêng đạt đỉnh quanh sắt-56 (khoảng 8,8 MeV/nuclôn). Bên trái đỉnh, "
                "hợp hạt nhân nhẹ lại thì toả năng lượng; bên phải đỉnh, cho hạt nhân nặng vỡ ra cũng toả năng lượng.")

# ------------------------------------------------- Hình 4: hai thang năng lượng (hoá học vs hạt nhân, mục 6)
b = defs("f4")
b += text(14, 22, "Hai thang năng lượng, cách nhau cả triệu lần", "currentColor", 12, "start", "700")
b += arrow("f4", "r", 30, 40, 404, 40, 2)
b += text(30, 58, "năng lượng tăng theo chiều này", "currentColor", 11, "start", "600")
# hai mốc năng lượng: mỗi đường đứt nét đi đúng ĐỈNH cột tương ứng
b += line(96, 74, 404, 74, "currentColor", 1, "5 4", .3)
b += line(96, 198, 404, 198, "currentColor", 1, "5 4", .3)
b += text(90, 78, "28,3 MeV", "currentColor", 10, "end", "600")
b += text(90, 202, "8 eV", "currentColor", 10, "end", "600")
# cột hoá học
b += rect(92, 198, 36, 20, "rgba(251,146,60,.35)", ORG, 1.6, 4)
b += arrow("f4", "o", 110, 248, 110, 220, 2)
b += text(110, 264, "hoá học", ORG, 12, "middle", "700")
b += text(110, 280, "≈ 8 eV", ORG, 12, "middle", "700")
b += text(110, 296, "một phân tử", "currentColor", 10, "middle", "500")
# cột hạt nhân: cùng bề rộng, cao hơn hẳn
b += rect(262, 74, 36, 144, "rgba(56,189,248,.35)", BLUE, 1.6, 4)
b += text(280, 264, "hạt nhân", BLUE, 12, "middle", "700")
b += text(280, 280, "≈ 28,3 MeV", BLUE, 12, "middle", "700")
b += text(280, 296, "một nguyên tử He-4", "currentColor", 10, "middle", "500")
# chú thích
b += line(168, 158, 250, 150, GRN, 1.4, "4 3", .9)
b += text(196, 132, "lớn hơn cỡ", RED, 12, "start", "700")
b += text(196, 148, "ba triệu lần", RED, 12, "start", "700")
b += text(30, 122, "cột vẽ phóng đại", "currentColor", 10, "start", "500")
b += text(30, 136, "cho thấy được", "currentColor", 10, "start", "500")
b += text(14, 320, "cùng một khối lượng: năng lượng hạt nhân lớn hơn hẳn năng lượng hoá học", "currentColor", 11, "start", "600")
fig4 = wrap_fig("0 0 420 334",
                "So sánh thang năng lượng hoá học cỡ vài eV với năng lượng liên kết hạt nhân cỡ vài MeV",
                b,
                "Hình 4. Năng lượng hoá học cỡ vài eV cho một phân tử, năng lượng liên kết hạt nhân cỡ vài MeV — "
                "lớn hơn khoảng ba triệu lần.")

# ------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
