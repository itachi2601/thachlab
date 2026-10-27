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
b += text(14, 24, "Trong hạt nhân: đẩy và hút cùng tồn tại", "currentColor", 14, "start", "700")
b += rect(20, 44, 186, 142, "rgba(248,113,113,.10)", RED, 1.6, 12)
b += text(113, 57, "hạt nhân heli-4", RED, 14, "middle", "700")
# 2 proton (đỏ) + 2 neutron (xanh), bán kính 13, đặt giãn ra để thấy lực hút giữa các cặp kề nhau
b += f'<circle cx="113" cy="119" r="57" fill="none" stroke="{RED}" stroke-width="2" stroke-dasharray="6 5" opacity=".85"/>'
P1, P2, N1, N2 = (70, 119), (156, 119), (113, 157), (113, 81)
for (x, y), c in ((P1, RED), (P2, RED), (N1, BLUE), (N2, BLUE)):
    b += dot(x, y, 13, c)
for (x, y), t in ((P1, "p"), (P2, "p"), (N1, "n"), (N2, "n")):
    b += text(x, y + 5, t, "#0f172a", 14, "middle", "700")
# lực hạt nhân (cam): mỗi cặp p–n kề nhau hút nhau, hai mũi tên ngắn hướng vào nhau
import math
for A, B in ((P1, N2), (P2, N2), (P1, N1), (P2, N1)):
    d = math.hypot(B[0] - A[0], B[1] - A[1])
    ux, uy = (B[0] - A[0]) / d, (B[1] - A[1]) / d
    for (S, sg) in ((A, 1), (B, -1)):
        x0, y0 = S[0] + sg * ux * 14.5, S[1] + sg * uy * 14.5
        x1, y1 = S[0] + sg * ux * 26.5, S[1] + sg * uy * 26.5
        b += arrow("f1", "o", round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1), 2)
# hai prôtôn đẩy nhau (xanh lá): mũi tên ngang, hướng ra phía ngoài mỗi hạt
b += arrow("f1", "g", 55, 119, 28, 119, 2.2)
b += arrow("f1", "g", 171, 119, 198, 119, 2.2)
b += text(113, 210, "hai prôtôn đẩy nhau", GRN, 14, "middle", "700")
# chú thích: nhãn đặt ngay cạnh khung, cùng màu cam với mũi tên lực hút
b += text(214, 84, "lực hạt nhân:", ORG, 14, "start", "700")
b += text(214, 104, "mũi tên cam", ORG, 14, "start", "600")
b += text(214, 124, "hút các nuclôn", ORG, 14, "start", "600")
b += text(214, 144, "kề nhau", ORG, 14, "start", "600")
b += text(214, 172, "mạnh hơn lực đẩy", "currentColor", 14, "start", "600")
b += text(214, 192, "tầm 10⁻¹⁵ m", "currentColor", 14, "start", "600")
b += text(14, 232, "4 nuclôn = 2 prôtôn (p) + 2 nơtron (n)", "currentColor", 14, "start", "600")
fig1 = wrap_fig("0 0 420 244",
                "Mô hình hạt nhân heli-4 gồm hai prôtôn đẩy nhau và hai nơtron, được lực hạt nhân hút lại",
                b,
                "Hình 1. Hạt nhân heli-4: hai prôtôn đẩy nhau, nhưng lực hạt nhân hút mọi cặp nuclôn mạnh hơn hẳn "
                "nên hạt nhân vẫn đứng vững.", exp="tn-l12-nllk-01")

# ------------------------------------------------- Hình 2: các nuclôn rời kết hợp thành hạt nhân (mục 4)
b = defs("f2")
b += text(14, 24, "Các hạt rời kết hợp lại: hụt khối, toả năng lượng", "currentColor", 13, "start", "700")
# nhóm hạt rời bên trái
b += rect(16, 46, 150, 116, "rgba(56,189,248,.10)", BLUE, 1.6, 10)
b += dot(58, 86, 13, RED) + dot(124, 86, 13, RED)
b += dot(58, 122, 13, BLUE) + dot(124, 122, 13, BLUE)
b += text(58, 91, "p", "#0f172a", 13, "middle", "700") + text(124, 91, "p", "#0f172a", 13, "middle", "700")
b += text(58, 127, "n", "#0f172a", 13, "middle", "700") + text(124, 127, "n", "#0f172a", 13, "middle", "700")
b += text(91, 182, "4 nuclôn rời", BLUE, 12.5, "middle", "700")
b += text(91, 198, "4,032980 u", BLUE, 13, "middle", "700")
b += text(91, 214, "kể cả 2 êlectron", "currentColor", 11.5, "middle", "500")
# mũi tên kết hợp
b += arrow("f2", "g", 172, 104, 232, 104, 2.6)
b += text(202, 92, "kết hợp", GRN, 12.5, "middle", "700")
b += text(202, 126, "toả", GRN, 12.5, "middle", "700")
b += text(202, 142, "28,30 MeV", GRN, 12.5, "middle", "700")
# hạt nhân bên phải
b += f'<circle cx="300" cy="104" r="46" fill="rgba(52,211,153,.12)" stroke="{GRN}" stroke-width="2"/>'
b += dot(288, 92, 11, RED) + dot(313, 92, 11, RED) + dot(288, 118, 11, BLUE) + dot(313, 118, 11, BLUE)
b += text(288, 97, "p", "#0f172a", 12, "middle", "700") + text(313, 97, "p", "#0f172a", 12, "middle", "700")
b += text(288, 123, "n", "#0f172a", 12, "middle", "700") + text(313, 123, "n", "#0f172a", 12, "middle", "700")
b += text(300, 182, "hạt nhân heli-4", GRN, 12.5, "middle", "700")
b += text(300, 198, "4,002603 u", GRN, 13, "middle", "700")
b += text(300, 214, "nhẹ hơn 0,030377 u", ORG, 12.5, "middle", "700")
b += text(16, 240, "khối lượng hụt 0,030377 u × 931,5 MeV/u = 28,30 MeV", "currentColor", 12.5, "start", "600")
fig2 = wrap_fig("0 0 420 254",
                "Bốn nuclôn rời có tổng khối lượng 4,032980 u kết hợp thành hạt nhân heli-4 khối lượng 4,002603 u, hụt 0,030377 u và toả 28,30 MeV",
                b,
                "Hình 2. Tổng khối lượng bốn nuclôn rời (kể cả hai êlectron) là 4,032980 u, còn nguyên tử heli-4 chỉ 4,002603 u: phần hụt 0,030377 u đã toả ra 28,30 MeV khi hạt nhân hình thành.")

# ------------------------------------------------- Hình 3: đường cong năng lượng liên kết riêng (mục 5)
b = defs("f3")
b += text(14, 18, "Năng lượng liên kết riêng theo số khối", "currentColor", 14, "start", "700")
# trục: A chia đúng tỉ lệ (x = 52 + 1,5·A), E/A: 0 → 190, 8,8 → 60
def X(a): return 52 + 1.5 * a
def Y(e): return round(190 - e * 130 / 8.8, 1)
b += line(52, 190, 414, 190, "currentColor", 2)
b += line(52, 190, 52, 50, "currentColor", 2)
b += text(414, 224, "A", "currentColor", 14, "end", "700")
b += text(14, 40, "MeV/nuclôn", "currentColor", 14, "start", "600")
b += line(52, 60, 414, 60, "currentColor", 1, "5 4", .3)
b += text(46, 64, "8,8", "currentColor", 14, "end", "600")
b += line(52, 125, 414, 125, "currentColor", 1, "5 4", .3)
b += text(46, 129, "4,4", "currentColor", 14, "end", "600")
b += text(46, 193, "0", "currentColor", 14, "end", "600")
for a in (0, 50, 100, 150, 200):
    b += line(X(a), 190, X(a), 196, "currentColor", 2)
    b += text(X(a), 212, str(a), "currentColor", 14, "middle", "600")
# vùng bền A = 50..80 tô nhạt
b += rect(X(50), 68, X(80) - X(50), 122, "rgba(52,211,153,.10)", GRN, 1, 6)
b += text(X(65), 242, "vùng bền nhất: A ≈ 50 – 80", GRN, 14, "middle", "700")
# đường cong theo số liệu thực (A, E/A MeV): He-4 nhô lên so với H-3, Li-6
diem = [(2, 1.11), (3, 2.83), (4, 7.07), (6, 5.33), (9, 6.46), (12, 7.68), (16, 7.98), (30, 8.52),
        (56, 8.79), (100, 8.55), (150, 8.2), (200, 7.87), (238, 7.57)]
d = " ".join(f"{X(a):.1f},{Y(e)}" for a, e in diem)
b += f'<polyline fill="none" stroke="{GRN}" stroke-width="2.6" points="{d}"/>'
for a, e in ((4, 7.07), (56, 8.79), (235, 7.6)):
    b += dot(round(X(a), 1), Y(e), 4, GRN)
b += text(X(56), 50, "Fe-56", GRN, 14, "middle", "700")
b += line(round(X(4), 1), Y(7.07) + 5, 70, 132, BLUE, 1.2)
b += text(68, 146, "He-4", BLUE, 14, "start", "700")
b += text(410, 100, "U-235", ORG, 14, "end", "700")
# hai mũi tên chỉ hai chiều tiến về đỉnh
b += arrow("f3", "b", 118, 176, 124, 112, 2.2)
b += text(60, 164, "nhẹ:", BLUE, 14, "start", "700")
b += text(60, 180, "hợp lại", BLUE, 14, "start", "700")
b += arrow("f3", "o", 384, 114, 300, 96, 2.2)
b += text(350, 146, "nặng: vỡ ra", ORG, 14, "middle", "700")
fig3 = wrap_fig("0 0 420 252",
                "Đường cong theo số liệu năng lượng liên kết riêng theo số khối, đạt đỉnh quanh sắt-56 ở 8,8 MeV mỗi nuclôn",
                b,
                "Hình 3. Năng lượng liên kết riêng đạt đỉnh quanh sắt-56 (8,8 MeV/nuclôn).<br>"
                "Trái đỉnh: hợp hạt nhân nhẹ lại toả năng lượng.<br>"
                "Phải đỉnh: hạt nhân nặng vỡ ra cũng toả năng lượng.<br>"
                "Hình: vẽ lại theo OpenStax, College Physics 2e, Hình 31.24 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e")

# ------------------------------------------------- Hình 4: hai thang năng lượng (hoá học vs hạt nhân, mục 6)
b = defs("f4")
b += text(14, 22, "Hai thang năng lượng, cách nhau cả triệu lần", "currentColor", 14, "start", "700")
# trục năng lượng đứng: mũi tên chỉ LÊN, các cột cùng đứng trên một đáy chung
b += arrow("f4", "r", 22, 252, 22, 70, 2)
b += text(14, 42, "năng lượng", "currentColor", 14, "start", "600")
b += text(14, 58, "tăng lên", "currentColor", 14, "start", "600")
b += line(40, 260, 410, 260, "currentColor", 2)
# hai mốc năng lượng: mỗi đường đứt nét đi đúng ĐỈNH cột tương ứng
b += line(104, 74, 410, 74, "currentColor", 1, "5 4", .3)
b += line(104, 240, 410, 240, "currentColor", 1, "5 4", .3)
b += text(98, 79, "28,3 MeV", "currentColor", 14, "end", "600")
b += text(98, 245, "8 eV", "currentColor", 14, "end", "600")
# cột hoá học (đứng trên đáy chung)
b += rect(108, 240, 36, 20, "rgba(251,146,60,.35)", ORG, 1.6, 4)
b += text(126, 282, "hoá học", ORG, 14, "middle", "700")
b += text(126, 298, "≈ 8 eV", ORG, 14, "middle", "700")
b += text(126, 314, "một phân tử", "currentColor", 14, "middle", "500")
# cột hạt nhân: cùng bề rộng, cao hơn hẳn
b += rect(262, 74, 36, 186, "rgba(56,189,248,.35)", BLUE, 1.6, 4)
b += text(280, 282, "hạt nhân", BLUE, 14, "middle", "700")
b += text(280, 298, "≈ 28,3 MeV", BLUE, 14, "middle", "700")
b += text(280, 314, "một nguyên tử He-4", "currentColor", 14, "middle", "500")
# chênh lệch giữa hai đỉnh cột: mũi tên hai đầu, nhãn ngay cạnh
b += arrow("f4", "r", 318, 157, 318, 79, 2)
b += arrow("f4", "r", 318, 157, 318, 235, 2)
b += text(324, 150, "lớn hơn cỡ", RED, 14, "start", "700")
b += text(324, 166, "ba triệu lần", RED, 14, "start", "700")
b += text(14, 340, "hai cột không đúng tỉ lệ: cột hoá học vẽ phóng đại", "currentColor", 14, "start", "500")
b += text(14, 360, "cùng khối lượng: năng lượng hạt nhân", "currentColor", 14, "start", "600")
b += text(14, 380, "lớn hơn hoá học rất nhiều", "currentColor", 14, "start", "600")
fig4 = wrap_fig("0 0 420 390",
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
