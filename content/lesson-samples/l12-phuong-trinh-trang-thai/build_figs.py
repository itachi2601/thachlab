"""Sinh 4 hình SVG cho bài "Bài 7. Phương trình trạng thái của khí lí tưởng" (Vật lí 12)
và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html.
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
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


# ------------------------------------------------- Hình 1: bình kín để ngoài nắng
b = defs("f1")
b += text(14, 24, "Bình kín để ngoài nắng", "currentColor", 13, "start", "700")
for x, ten in ((68, "sáng"), (372, "trưa")):
    b += rect(x - 32, 68, 64, 92, "rgba(148,163,184,.10)", "currentColor", 2.5, 10)
    b += f'<circle cx="{x}" cy="54" r="17" fill="rgba(148,163,184,.14)" stroke="currentColor" stroke-width="2"/>'
    for a in (-30, 0, 30):                       # vạch chia áp kế để đọc được góc kim
        rad = math.radians(a)
        dx, dy = math.sin(rad), -math.cos(rad)
        b += line(x + 13 * dx, 54 + 13 * dy, x + 17 * dx, 54 + 17 * dy, "currentColor", 1.2, "", .45)
# 5,0 bar (sáng) → 5,3 bar (trưa): kim nhích lên ~16°; kim mờ = vị trí buổi sáng
b += line(68, 54, 78, 39, RED, 2.2)
b += line(372, 54, 382, 39, RED, 1.6, "2 2", .5)
b += line(372, 54, 377, 37, RED, 2.2)
b += text(436, 22, "kim: 5,0 → 5,3 bar", ORG, 11, "end", "700")
b += f'<circle cx="220" cy="48" r="14" fill="{ORG}" opacity="0.9"/>'
for dx, dy in ((0, -24), (17, -17), (24, 0), (17, 17), (0, 24), (-17, 17), (-24, 0), (-17, -17)):
    b += line(220 + dx * 0.75, 48 + dy * 0.75, 220 + dx, 48 + dy, ORG, 2.2)
b += text(220, 96, "trời nắng", ORG, 12, "middle", "700")
b += arrow("f1", "o", 112, 112, 328, 112, 2.6)
b += text(220, 134, "nhiệt độ tăng, áp suất tăng", ORG, 12, "middle", "700")
b += text(68, 180, "sáng", "currentColor", 12, "middle", "700")
b += text(68, 198, "27 °C · 5,0 bar", RED, 12, "middle", "700")
b += text(372, 180, "trưa", "currentColor", 12, "middle", "700")
b += text(372, 198, "47 °C · 5,3 bar", RED, 12, "middle", "700")
b += text(220, 216, "thể tích bình không đổi", GRN, 11, "middle", "700")
fig1 = wrap("0 0 440 228",
            "Bình khí nén mini kín để ngoài nắng: nhiệt độ tăng từ 27 lên 47 độ C làm áp suất tăng từ 5,0 lên 5,3 bar, kim áp kế nhích lên, thể tích bình không đổi",
            b, "Hình 1. Bình kín, lượng khí không đổi, thể tích không đổi: chỉ nhiệt độ tăng mà kim áp kế đã nhích từ 5,0 lên 5,3 bar — đó là quá trình đẳng tích.",
            exp="tn-l12-pttrangthai-03")

# ------------------------------------------------- Hình 2: bóng bàn bẹp phồng lại
b = defs("f2")
b += text(14, 24, "Quả bóng bàn bẹp trong nước nóng", "currentColor", 13, "start", "700")
b += f'<ellipse cx="86" cy="112" rx="42" ry="34" fill="rgba(248,113,113,.10)" stroke="currentColor" stroke-width="2.5"/>'
b += f'<path d="M 56 98 Q 86 126 116 98" fill="none" stroke="{RED}" stroke-width="2.4"/>'
b += text(86, 168, "vỏ bẹp", RED, 11, "middle", "700")
b += text(86, 186, "khí ở nhiệt độ phòng", "currentColor", 11, "middle", "600")
b += arrow("f2", "o", 140, 112, 214, 112, 2.6)
b += text(177, 98, "nước 80 °C", ORG, 11, "middle", "700")
b += rect(250, 84, 130, 100, "rgba(56,189,248,.10)", "currentColor", 2.5, 6)
b += line(250, 106, 380, 106, BLUE, 2, "", .8)
b += f'<path d="M 276 76 q 7 -9 0 -18" fill="none" stroke="{ORG}" stroke-width="1.6" opacity="0.85"/>'
b += f'<path d="M 315 74 q 7 -9 0 -18" fill="none" stroke="{ORG}" stroke-width="1.6" opacity="0.85"/>'
b += f'<path d="M 354 76 q 7 -9 0 -18" fill="none" stroke="{ORG}" stroke-width="1.6" opacity="0.85"/>'
b += f'<circle cx="315" cy="128" r="30" fill="rgba(52,211,153,.18)" stroke="{GRN}" stroke-width="2.5"/>'
b += text(315, 205, "vỏ phồng trở lại", GRN, 11, "middle", "700")
fig2 = wrap("0 0 440 214",
            "Quả bóng bàn bẹp được nhúng vào cốc nước nóng: khí bên trong nóng lên, áp suất tăng và đẩy vỏ bóng phồng trở lại",
            b, "Hình 2. Khí trong bóng nóng lên: cả ba thông số đều đổi (nhiệt độ tăng, áp suất tăng, vỏ bóng phồng ra) — vì thế cần một phương trình cho cả ba.")

# ------------------------------------------------- Hình 3: hai đường đẳng tích trên đồ thị p - T
b = defs("f3")
b += text(14, 22, "Đồ thị p – T: hai đường đẳng tích", "currentColor", 13, "start", "700")
b += line(70, 205, 420, 205, "currentColor", 2)
b += line(70, 205, 70, 42, "currentColor", 2)
b += text(412, 228, "T (K)", "currentColor", 12, "end", "600")
b += text(54, 44, "p", "currentColor", 12, "start", "600")
b += text(60, 222, "O", "currentColor", 12, "middle", "600")
b += line(70, 205, 215, 62, RED, 2.6)
b += line(70, 205, 410, 120, BLUE, 2.6)
b += line(200, 205, 200, 68, "currentColor", 1.2, "5 4", .65)
b += dot(200, 77, 4.5, RED)
b += dot(200, 173, 4.5, BLUE)
b += text(200, 222, "cùng một T", "currentColor", 11, "middle", "600")
b += text(222, 58, "đường V nhỏ", RED, 12, "start", "700")
b += text(412, 108, "đường V lớn", BLUE, 12, "end", "700")
b += text(208, 84, "p lớn hơn", RED, 11, "start", "700")
b += text(208, 192, "p nhỏ hơn", BLUE, 11, "start", "700")
fig3 = wrap("0 0 440 240",
            "Đồ thị áp suất theo nhiệt độ tuyệt đối của hai quá trình đẳng tích: hai đường thẳng kéo dài qua gốc tọa độ, đường dốc hơn ứng với thể tích nhỏ hơn",
            b, "Hình 3. Đường đẳng tích là đường thẳng kéo dài qua gốc toạ độ. Kẻ một đường thẳng đứng tại một giá trị T: đường nằm trên cho p lớn hơn, tức thể tích nhỏ hơn.")

# ------------------------------------------------- Hình 4: ba định luật là ba trường hợp riêng
b = defs("f4")
b += rect(105, 16, 230, 48, "rgba(148,163,184,.12)", "currentColor", 2, 10)
b += text(220, 38, "Phương trình trạng thái", "currentColor", 12, "middle", "700")
b += text(220, 56, "pV/T = hằng số", "currentColor", 12, "middle", "600")
b += arrow("f4", "b", 220, 64, 75, 96, 2.2)
b += arrow("f4", "g", 220, 64, 220, 96, 2.2)
b += arrow("f4", "o", 220, 64, 365, 96, 2.2)
b += rect(10, 96, 130, 68, "rgba(56,189,248,.10)", BLUE, 2, 10)
b += text(75, 118, "Giữ T", BLUE, 12, "middle", "700")
b += text(75, 137, "pV = hằng số", "currentColor", 11, "middle", "600")
b += text(75, 155, "Boyle", BLUE, 11, "middle", "700")
b += rect(155, 96, 130, 68, "rgba(52,211,153,.10)", GRN, 2, 10)
b += text(220, 118, "Giữ p", GRN, 12, "middle", "700")
b += text(220, 137, "V/T = hằng số", "currentColor", 11, "middle", "600")
b += text(220, 155, "Charles", GRN, 11, "middle", "700")
b += rect(300, 96, 130, 68, "rgba(251,146,60,.10)", ORG, 2, 10)
b += text(365, 118, "Giữ V", ORG, 12, "middle", "700")
b += text(365, 137, "p/T = hằng số", "currentColor", 11, "middle", "600")
b += text(365, 155, "Gay-Lussac", ORG, 11, "middle", "700")
b += text(220, 190, "giữ một thông số không đổi, còn lại hai", "currentColor", 11, "middle", "600")
fig4 = wrap("0 0 440 205",
            "Sơ đồ: phương trình trạng thái ở trên, ba nhánh đi xuống là định luật Boyle khi giữ nhiệt độ, định luật Charles khi giữ áp suất và định luật Gay-Lussac khi giữ thể tích",
            b, "Hình 4. Ba định luật đã học là ba trường hợp riêng của phương trình trạng thái: giữ một thông số không đổi thì nó triệt tiêu, còn lại hệ thức của định luật tương ứng.")

# ------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
