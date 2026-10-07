"""Sinh 4 hình SVG cho bài "Bài 11. Thực hành đo độ lớn cảm ứng từ" (Vật lí 12)
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


def rect(x, y, w, h, fill, stroke="currentColor", sw=2, rx=6):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


RED_F, BLUE_F, GREY_F = "rgba(248,113,113,.28)", "rgba(56,189,248,.28)", "rgba(148,163,184,.16)"

# ======================================================= Hình 1: bố trí cân dòng điện
b = ""
b += rect(30, 218, 190, 34, GREY_F)                       # bệ cân
b += rect(140, 226, 70, 20, "rgba(52,211,153,.18)", GRN, 1.5, 4)
b += text(175, 241, "1,45 g", GRN, 14, "middle", "700")
b += line(34, 214, 216, 214, "currentColor", 4)           # đĩa cân
# nam châm chữ U trên đĩa
b += rect(60, 120, 36, 94, RED_F, RED, 2, 3)
b += rect(158, 120, 36, 94, BLUE_F, BLUE, 2, 3)
b += rect(60, 182, 134, 32, GREY_F, "currentColor", 2, 3)
b += text(78, 160, "N", RED, 17, "middle", "700")
b += text(176, 160, "S", BLUE, 17, "middle", "700")
# giá đỡ riêng + khung dây
b += line(346, 40, 346, 252, "currentColor", 5)
b += line(127, 40, 346, 40, "currentColor", 5)
b += line(346, 252, 300, 252, "currentColor", 5)
b += line(127, 40, 127, 150, "currentColor", 2)
b += f'<circle cx="127" cy="152" r="7" fill="{ORG}" stroke="{ORG}" stroke-width="2"/>'
b += text(140, 90, "khung dây", "currentColor", 14, "start", "600")
b += text(140, 108, "(cạnh dưới ở trong khe)", "currentColor", 14, "start", "600")
b += text(140, 28, "giá đỡ riêng, không chạm cân", "currentColor", 14, "start", "700")
b += text(206, 170, "nam châm", "currentColor", 14, "start", "600")
b += text(206, 188, "chữ U", "currentColor", 14, "start", "600")
b += text(30, 272, "cân điện tử chia 0,01 g", "currentColor", 14, "start", "600")
b += text(30, 291, "nguồn một chiều + ampe kế nối với khung", "currentColor", 14, "start", "600")
fig1 = wrap("0 0 380 300", "Cân điện tử có nam châm chữ U trên đĩa; khung dây treo trên giá riêng, cạnh dưới nằm trong khe nam châm, cân chỉ 1,45 gam",
            b, "Hình 1. Bố trí cân dòng điện: nam châm chữ U nằm trên đĩa cân, khung dây treo trên giá đứng riêng với cạnh dưới trong khe. Dây không chạm vào cân hay nam châm.")

# ======================================================= Hình 2: lực và phản lực (mặt cắt khe nam châm)
b = defs("f2")
b += text(20, 28, "⊙ dòng điện hướng ra khỏi trang", "currentColor", 14, "start", "700")
b += rect(20, 240, 230, 40, GREY_F)
b += text(135, 266, "cân điện tử", "currentColor", 14, "middle", "700")
b += rect(30, 110, 50, 130, RED_F, RED, 2, 3)
b += rect(190, 110, 50, 130, BLUE_F, BLUE, 2, 3)
b += rect(30, 200, 210, 40, GREY_F, "currentColor", 2, 3)
b += text(55, 160, "N", RED, 18, "middle", "700")
b += text(215, 160, "S", BLUE, 18, "middle", "700")
b += arrow("f2", "g", 88, 172, 182, 172, 3)
b += arrow("f2", "g", 88, 189, 182, 189, 3)
b += text(106, 166, "B", GRN, 16, "middle", "700")
b += line(135, 50, 135, 141, "currentColor", 1.5)
b += '<circle cx="135" cy="150" r="9" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="135" cy="150" r="3" fill="currentColor"/>'
b += arrow("f2", "r", 152, 142, 152, 92, 3.5)
b += text(160, 100, "F lên dây", RED, 14, "start", "700")
b += arrow("f2", "o", 262, 130, 262, 195, 3.5)
b += text(272, 150, "F′ lên", ORG, 14, "start", "700")
b += text(272, 168, "nam châm", ORG, 14, "start", "700")
fig2 = wrap("0 0 380 290", "Mặt cắt khe nam châm: dây có dòng hướng ra khỏi trang chịu lực từ hướng lên, nam châm chịu phản lực hướng xuống làm cân tăng",
            b, "Hình 2. Mặt cắt khe nam châm chữ U. Đường sức từ đi từ cực N sang cực S. Dây chịu lực $F$, nam châm chịu lực $F'$ cùng độ lớn và ngược chiều; cân chỉ cảm nhận $F'$.")

# ======================================================= Hình 3: đồ thị Δm–I
X0, Y0, KX, KY = 56, 215, 56, 62     # gốc, px mỗi A, px mỗi g
pts = [(1, .50), (2, .97), (3, 1.45), (4, 1.97), (5, 2.44)]
SLOPE = sum(i * m for i, m in pts) / sum(i * i for i, _ in pts)
b = text(60, 26, "Δm (g)", "currentColor", 14, "start", "700")
for g in (.5, 1, 1.5, 2, 2.5):
    y = Y0 - g * KY
    b += line(X0, y, 350, y, "currentColor", 1, "", .18)
    b += text(48, y + 5, str(g).replace(".", ",").rstrip("0").rstrip(",") if g != int(g) else str(int(g)), "currentColor", 14, "end", "500")
for i in range(1, 6):
    x = X0 + i * KX
    b += line(x, Y0, x, Y0 + 6, "currentColor", 2)
    b += text(x, Y0 + 24, str(i), "currentColor", 14, "middle", "500")
b += line(X0, Y0, 352, Y0, "currentColor", 2.5)
b += line(X0, Y0, X0, 36, "currentColor", 2.5)
b += text(352, Y0 + 44, "I (A)", "currentColor", 14, "end", "700")
b += line(X0, Y0, X0 + 5.1 * KX, Y0 - SLOPE * 5.1 * KY, GRN, 2.6)
for i, m in pts:
    b += f'<circle cx="{X0 + i * KX}" cy="{Y0 - m * KY:.1f}" r="5.5" fill="{ORG}" stroke="currentColor" stroke-width="1.2"/>'
b += text(78, 92, "độ dốc ≈ 0,489 g/A", GRN, 14, "start", "700")
b += text(78, 112, "→ B ≈ 0,12 T", GRN, 14, "start", "700")
fig3 = wrap("0 0 380 272", "Đồ thị khối lượng tăng theo cường độ dòng điện: năm điểm đo nằm gần đường thẳng qua gốc toạ độ có độ dốc khoảng 0,489 gam trên ampe",
            b, "Hình 3. Δm tăng gần tỉ lệ với $I$: năm điểm đo (số liệu minh hoạ) nằm sát đường thẳng qua gốc toạ độ. Độ dốc đường thẳng bằng $Bl/g$.",
            "tn-l12-thuchanhtu-01")

# ======================================================= Hình 4: dây hợp góc với đường sức
b = defs("f4")
b += arrow("f4", "g", 40, 150, 330, 150, 3)
b += text(342, 157, "B", GRN, 16, "start", "700")
b += line(120, 150, 195, 20, "currentColor", 4)
b += '<circle cx="120" cy="150" r="5" fill="currentColor"/>'
b += text(206, 46, "dây, dòng I", "currentColor", 14, "start", "700")
b += '<path d="M165,150 A45,45 0 0 0 142.5,111" fill="none" stroke="' + ORG + '" stroke-width="2.5"/>'
b += text(176, 134, "θ = 60°", ORG, 14, "start", "700")
b += '<circle cx="64" cy="204" r="9" fill="none" stroke="' + RED + '" stroke-width="2"/><circle cx="64" cy="204" r="3" fill="' + RED + '"/>'
b += text(82, 209, "lực từ F hướng ra khỏi trang", RED, 14, "start", "700")
b += text(40, 238, "F = B·I·l·sin θ", "currentColor", 16, "start", "700")
fig4 = wrap("0 0 380 250", "Dây hợp với đường sức từ một góc 60 độ; lực từ hướng ra khỏi trang và có độ lớn B nhân I nhân l nhân sin theta",
            b, "Hình 4. Dây hợp với đường sức góc $\\theta$ (vẽ trong mặt phẳng chứa $\\vec B$ và dây). Lực từ vuông góc với mặt phẳng đó; độ lớn $F = BIl\\sin\\theta$.",
            "tn-l12-thuchanhtu-03")

# ------------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes; slope", round(SLOPE, 4))
