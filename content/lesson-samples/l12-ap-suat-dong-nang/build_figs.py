"""Sinh 4 hình SVG cho bài "Bài 8. Áp suất - động năng của phân tử khí" (Vật lí 12) và thay các
mốc <!--FIGn--> trong theory.src.html -> theory.html. Chạy từ thư mục này: python3 build_figs.py
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


def sub(x, y, before, sub_, after, c="currentColor", size=11, anchor="start", weight="700"):
    """Chữ có chỉ số dưới: before + <tspan>sub_</tspan> + after."""
    return (f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{before}<tspan dy="4" font-size="{size - 3}">{sub_}</tspan>'
            f'<tspan dy="-4">{after}</tspan></text>')


def subsup(x, y, before, sub_, sup_, after="", c="currentColor", size=11, anchor="start", weight="700"):
    """Chữ có cả chỉ số dưới và chỉ số trên: v thì ghi v₁²."""
    return (f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{before}<tspan dy="4" font-size="{size - 3}">{sub_}</tspan>'
            f'<tspan dy="-8" font-size="{size - 3}">{sup_}</tspan>'
            f'<tspan dy="4">{after}</tspan></text>')


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


# ------------------------------------------------- Hình 1: bóng bàn bẹp gặp nước nóng
b = defs("f1")
b += text(20, 22, "a) Khí nguội", "currentColor", 12, "start", "700")
b += f'<circle cx="105" cy="105" r="42" fill="rgba(148,163,184,.10)" stroke="currentColor" stroke-width="2.5"/>'
b += f'<path d="M132,77 A38,38 0 0 0 132,131" fill="none" stroke="{ORG}" stroke-width="2" stroke-dasharray="5 4"/>'
b += text(140, 66, "vỏ bẹp", ORG, 11, "start", "700")
b += dot(80, 95, 4, BLUE) + arrow("f1", "b", 86, 95, 106, 95, 2.4)
b += dot(100, 125, 4, BLUE) + arrow("f1", "b", 106, 125, 122, 116, 2.4)
b += text(105, 184, "va chạm thưa, nhẹ", BLUE, 11, "middle", "600")
b += text(228, 22, "b) Gặp nước nóng", "currentColor", 12, "start", "700")
b += f'<path d="M250,58 L258,172 L372,172 L380,58" fill="none" stroke="currentColor" stroke-width="2.5"/>'
b += line(256, 92, 374, 92, BLUE, 1.6, "6 5", .75)
b += f'<circle cx="315" cy="118" r="40" fill="rgba(56,189,248,.14)" stroke="{BLUE}" stroke-width="2.2"/>'
b += dot(288, 104, 4, BLUE) + arrow("f1", "b", 294, 104, 320, 104, 2.4)
b += dot(302, 138, 4, BLUE) + arrow("f1", "b", 308, 138, 334, 124, 2.4)
b += dot(342, 138, 4, BLUE) + arrow("f1", "b", 338, 134, 320, 120, 2.4)
b += text(315, 184, "va chạm dày, mạnh", BLUE, 11, "middle", "600")
fig1 = wrap("0 0 420 200",
            "Hai trạng thái của quả bóng bàn: khí nguội thì phân tử đập thưa và nhẹ, khí nóng thì phân tử đập dày và mạnh nên đẩy vỏ bóng phồng ra",
            b, "Hình 1. Khí nguội: phân tử đập thưa, nhẹ nên vỏ bẹp. Gặp nước nóng: phân tử bay nhanh hơn, đập dày và mạnh hơn nên đẩy vỏ phồng lại.",
            exp="tn-l12-apsuatdongnang-03")

# ------------------------------------------------- Hình 2: một phân tử va chạm vào thành
b = defs("f2")
b += text(14, 20, "Một phân tử đập vuông góc vào thành bình", "currentColor", 12, "start", "700")
b += line(50, 38, 350, 38, "currentColor", 1.2, "5 4", .8)
b += line(50, 33, 50, 43, "currentColor", 1.6)
b += line(350, 33, 350, 43, "currentColor", 1.6)
b += text(356, 42, "cạnh l", "currentColor", 11, "start", "600")
b += text(14, 190, "V = l³", "currentColor", 11, "start", "600")
b += rect(50, 50, 300, 120, "rgba(148,163,184,.06)")
b += line(350, 50, 350, 170, RED, 3.5)
b += line(30, 110, 404, 110, "currentColor", 1.2, "6 5", .5)
b += text(404, 108, "Ox", "currentColor", 11, "end", "600")
b += dot(95, 110, 6, BLUE)
b += arrow("f2", "b", 112, 110, 338, 110, 2.8)
b += text(210, 100, "tới: v, p = +mv", BLUE, 11, "middle", "700")
b += arrow("f2", "g", 338, 142, 120, 142, 2.8)
b += text(232, 160, "bật ra: v, p = -mv", GRN, 11, "middle", "700")
b += text(350, 190, "thành bình, diện tích S = l²", RED, 11, "end", "700")
b += text(210, 214, "Độ biến thiên động lượng: 2mv", ORG, 12, "middle", "700")
fig2 = wrap("0 0 420 224",
            "Phân tử khối lượng m bay song song trục Ox với tốc độ v, đập vào thành bình rồi bật ngược lại với cùng tốc độ",
            b, "Hình 2. Động lượng của phân tử đổi chiều từ +mv thành -mv khi va chạm; thành bình nhận đúng 2mv.")

# ------------------------------------------------- Hình 3: nhiều tốc độ, lấy trung bình bình phương
b = defs("f3")
b += text(14, 20, "Ba phân tử, ba tốc độ khác nhau", "currentColor", 12, "start", "700")
b += text(410, 22, "v² rồi lấy trung bình", "currentColor", 11, "end", "600")
b += rect(20, 40, 210, 120, "rgba(148,163,184,.06)")
# Mũi tên dài 26/46/70 px tỉ lệ với v (1 : 1,77 : 2,69); cột phải tỉ lệ với v² nên cùng một hệ số
# cho cả ba cột → cao 8/25/58 px (1 : 3,13 : 7,25), KHÔNG dùng lại chiều cao của mũi tên.
DAI = (26, 46, 70)                        # px, ∝ v
CAO = [round(d * d / 84.5) for d in DAI]  # px, ∝ v²  → 8 / 25 / 58
NEN, RONG = 165, 24                       # y đáy cột, bề rộng cột
for y, d, nhan in zip((65, 105, 145), DAI, "123"):
    b += dot(50, y, 5, BLUE) + arrow("f3", "b", 57, y, 57 + d, y, 2.4)
    b += sub(62 + d, y + 4, "v", nhan, "", BLUE, 11, "start", "700")
b += text(20, 36, "mũi tên dài = tốc độ lớn", "currentColor", 10, "start", "600")
b += line(280, NEN, 410, NEN, "currentColor", 2)
for h, x in zip(CAO, (288, 320, 352)):
    b += f'<rect x="{x}" y="{NEN - h}" width="{RONG}" height="{h}" fill="rgba(56,189,248,.30)" stroke="{BLUE}" stroke-width="1.5"/>'
b += subsup(300, 181, "v", "1", "2", "", "currentColor", 11, "middle", "600")
b += subsup(332, 181, "v", "2", "2", "", "currentColor", 11, "middle", "600")
b += subsup(364, 181, "v", "3", "2", "", "currentColor", 11, "middle", "600")
MUC_TB = round(NEN - sum(CAO) / len(CAO), 1)  # 165 − (8+25+58)/3 ≈ 134,7 — mức trung bình của v²
b += line(282, MUC_TB, 410, MUC_TB, GRN, 1.6, "6 5")
b += text(410, 202, "mức trung bình của v²", GRN, 11, "end", "700")
fig3 = wrap("0 0 420 214",
            "Ba phân tử có tốc độ khác nhau, bình phương các tốc độ rồi lấy trung bình thành tốc độ trung bình bình phương",
            b, "Hình 3. Các phân tử có tốc độ khác nhau, nên phải bình phương từng tốc độ rồi lấy trung bình.")

# ------------------------------------------------- Hình 4: động năng tỉ lệ thuận với nhiệt độ
b = defs("f4")
b += text(14, 18, "Động năng trung bình tỉ lệ thuận với nhiệt độ tuyệt đối", "currentColor", 12, "start", "700")
b += sub(66, 36, "E", "d", " (10⁻²¹ J)", "currentColor", 11, "start", "600")
b += line(60, 195, 400, 195, "currentColor", 2)
b += line(60, 195, 60, 40, "currentColor", 2)
b += text(400, 214, "T (K)", "currentColor", 11, "end", "600")
b += f'<polyline fill="none" stroke="{GRN}" stroke-width="2.6" points="60,195 350,54"/>'
for x, y, nhan in ((197, 128, "300"), (334, 62, "600")):
    b += line(x, y, x, 195, "currentColor", 1.2, "5 4", .55)
    b += line(60, y, x, y, "currentColor", 1.2, "5 4", .55)
    b += line(x, 190, x, 200, "currentColor", 1.8)
    b += text(x, 214, nhan, "currentColor", 11, "middle", "600")
b += dot(197, 128, 5, GRN) + dot(334, 62, 5, GRN)
b += text(203, 142, "6,2", GRN, 11, "start", "700")
b += text(352, 48, "12,4", GRN, 11, "start", "700")
b += text(66, 84, "gấp đôi T thì gấp đôi động năng", ORG, 11, "start", "700")
b += text(60, 234, "Mọi chất khí đều nằm trên cùng một đường — chỉ phụ thuộc T.", "currentColor", 11, "start", "600")
fig4 = wrap("0 0 420 244",
            "Đồ thị động năng tịnh tiến trung bình theo nhiệt độ tuyệt đối là đường thẳng qua gốc toạ độ, dùng chung cho mọi chất khí",
            b, "Hình 4. Động năng tịnh tiến trung bình tỉ lệ thuận với nhiệt độ tuyệt đối: đường thẳng qua gốc, dùng chung cho mọi chất khí.")

# ------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
