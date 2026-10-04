"""Sinh 4 hình SVG cho bài "Bài 10. Lực từ. Cảm ứng từ" (Vật lí 12) và thay các mốc
<!--FIGn--> trong theory.src.html -> theory.html. Chạy từ thư mục này: python3 build_figs.py

Quy ước màu dùng chung cả bài: đỏ = lực từ F · cam = dòng điện I · xanh dương = cảm ứng từ B
(chỉ dùng chữ và nét bằng currentColor cho vật thể).
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


def vao(x, y, r=14, c=BLUE):
    """Kí hiệu ⊗: vectơ hướng vào trong mặt phẳng hình vẽ."""
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{c}" stroke-width="2.5"/>'
            f'<line x1="{x - r * 0.7:.0f}" y1="{y - r * 0.7:.0f}" x2="{x + r * 0.7:.0f}" y2="{y + r * 0.7:.0f}" stroke="{c}" stroke-width="2.5"/>'
            f'<line x1="{x + r * 0.7:.0f}" y1="{y - r * 0.7:.0f}" x2="{x - r * 0.7:.0f}" y2="{y + r * 0.7:.0f}" stroke="{c}" stroke-width="2.5"/>')


def ellipse(cx, cy, rx, ry, c=BLUE, w=2, fill="none"):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{c}" stroke-width="{w}"/>'


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


# ------------------------------------------------- Hình 1: dây dẫn trong khe nam châm chữ U
b = defs("f1")
b += rect(96, 30, 228, 30, "rgba(148,163,184,.16)", "currentColor", 2, 8)       # cực N
b += rect(96, 190, 228, 30, "rgba(148,163,184,.16)", "currentColor", 2, 8)      # cực S
b += text(210, 52, "N", "currentColor", 16, "middle", "700")
b += text(210, 212, "S", "currentColor", 16, "middle", "700")
b += arrow("f1", "b", 150, 68, 150, 184, 2.6)                                   # đường sức B
b += arrow("f1", "b", 300, 68, 300, 184, 2.6)
b += text(160, 88, "B", BLUE, 14, "start", "700")
b += line(30, 120, 390, 120, "currentColor", 3.5)                               # dây dẫn
b += arrow("f1", "o", 58, 120, 108, 120, 3)
b += text(78, 108, "I", ORG, 14, "middle", "700")
b += vao(210, 120, 14, RED)                                                     # lực từ F (vào trong)
b += text(232, 116, "F", RED, 14, "start", "700")
b += text(16, 250, "⊗: lực từ F hướng vào trong mặt phẳng hình vẽ", RED, 11, "start", "600")
fig1 = wrap("0 0 420 260", "Đoạn dây mang dòng điện đặt giữa hai cực nam châm chữ U, đường sức từ hướng xuống, lực từ hướng vuông góc vào trong mặt phẳng hình vẽ",
            b, "Hình 1. Dây mang dòng điện trong khe nam châm: B hướng xuống, F vuông góc và hướng vào mặt phẳng hình vẽ (⊗).")

# ------------------------------------------------- Hình 2: quy tắc bàn tay trái
b = defs("f2")
b += rect(150, 70, 90, 120, "rgba(148,163,184,.10)", "currentColor", 2.5, 18)   # lòng bàn tay
b += line(240, 88, 300, 88, "currentColor", 3.5)
b += line(240, 116, 300, 116, "currentColor", 3.5)
b += line(240, 144, 300, 144, "currentColor", 3.5)
b += line(240, 172, 300, 172, "currentColor", 3.5)
b += line(166, 76, 140, 30, "currentColor", 3.5)                                # ngón cái
b += line(150, 130, 124, 130, "currentColor", 3.5)                              # cổ tay
b += vao(195, 130, 16, BLUE)                                                    # B xuyên vào lòng bàn tay
b += text(195, 108, "B", BLUE, 14, "middle", "700")
b += text(140, 20, "F", RED, 15, "middle", "700")
b += text(312, 126, "I", ORG, 15, "start", "700")
b += text(312, 146, "cổ tay → ngón tay", ORG, 11, "start", "600")
b += text(16, 236, "⊗: đường sức từ xuyên vào lòng bàn tay · ngón cái choãi 90° chỉ chiều F", BLUE, 11, "start", "600")
fig2 = wrap("0 0 440 250", "Bàn tay trái duỗi thẳng: các đường sức từ xuyên vào lòng bàn tay, chiều từ cổ tay đến ngón tay theo chiều dòng điện, ngón cái choãi ra chỉ chiều lực từ",
            b, "Hình 2. Bàn tay trái: đường sức (⊗) xuyên vào lòng bàn tay, cổ tay → ngón tay theo chiều I, ngón cái chỉ F.")

# ------------------------------------------------- Hình 3: đồ thị F theo I của thí nghiệm đo
b = defs("f3")
b += line(70, 200, 420, 200, "currentColor", 2)
b += line(70, 200, 70, 40, "currentColor", 2)
for fx, nhan in ((136, "10"), (72, "20")):
    b += line(64, fx, 70, fx, "currentColor", 2)
    b += text(60, fx + 4, nhan, "currentColor", 11, "end", "600")
    b += line(70, fx, 400, fx, "currentColor", 1, "5 6", .22)
for i in range(1, 6):
    x = 70 + 62 * i
    b += line(x, 200, x, 205, "currentColor", 2)
    b += text(x, 220, str(i), "currentColor", 11, "middle", "600")
b += text(42, 30, "F (mN)", "currentColor", 12, "start", "700")
b += text(418, 190, "I (A)", "currentColor", 12, "end", "700")
b += line(70, 200, 380, 38, GRN, 2.4, "7 5", .95)                              # đường hồi quy qua gốc (5,05 mN/A)
for i, f in enumerate((4.6, 10.4, 14.2, 20.6, 25.5), 1):
    b += dot(70 + 62 * i, 200 - 6.4 * f, 4.5, GRN)
b += text(238, 166, "độ dốc ≈ 5,1 mN/A", GRN, 11, "start", "700")
b += text(238, 184, "= B·l  →  B ≈ 0,10 T", GRN, 11, "start", "700")
fig3 = wrap("0 0 440 232", "Đồ thị lực từ theo cường độ dòng điện: năm điểm đo nằm gần một đường thẳng đi qua gốc toạ độ, độ dốc bằng cảm ứng từ nhân chiều dài đoạn dây",
            b, "Hình 3. Lực từ tỉ lệ thuận với dòng điện: đường hồi quy qua gốc, độ dốc B·l ≈ 5,1 mN/A → B ≈ 0,10 T.")

# ------------------------------------------------- Hình 4: ba dạng dòng điện
b = defs("f4")
# a) dây dẫn thẳng
b += text(14, 20, "a) dây thẳng", "currentColor", 11, "start", "700")
b += line(78, 52, 78, 196, "currentColor", 3.5)
b += arrow("f4", "o", 78, 150, 78, 86, 3)
b += text(92, 100, "I", ORG, 13, "start", "700")
b += ellipse(78, 138, 44, 13, BLUE, 2)
b += ellipse(78, 138, 27, 8, BLUE, 2)
b += text(126, 162, "B", BLUE, 13, "start", "700")
# b) vòng dây
b += text(158, 20, "b) vòng dây", "currentColor", 11, "start", "700")
b += ellipse(222, 140, 44, 17, "currentColor", 3)
b += arrow("f4", "b", 222, 178, 222, 96, 2.6)
b += arrow("f4", "o", 176, 132, 176, 154, 2.4)
b += arrow("f4", "o", 268, 148, 268, 126, 2.4)
b += text(166, 122, "I", ORG, 13, "start", "700")
b += text(232, 104, "B", BLUE, 13, "start", "700")
# c) ống dây
b += text(300, 20, "c) ống dây", "currentColor", 11, "start", "700")
b += line(304, 140, 430, 140, "currentColor", 1.2, "5 5", .35)
for x in (312, 337, 362, 387, 412):
    b += ellipse(x, 140, 8, 24, "currentColor", 2.4)
b += arrow("f4", "b", 308, 140, 424, 140, 2.6)
b += text(366, 100, "B", BLUE, 13, "middle", "700")
fig4 = wrap("0 0 440 206", "Ba dạng dòng điện: dây dẫn thẳng có đường sức là đường tròn đồng tâm, vòng dây có cảm ứng từ vuông góc mặt phẳng vòng dây, ống dây có từ trường đều song song trục ống",
            b, "Hình 4. Dây thẳng — đường sức là đường tròn đồng tâm; vòng dây — B vuông góc mặt phẳng vòng; ống dây — B đều trong lòng.")

# ------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
