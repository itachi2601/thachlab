"""Sinh 4 hình SVG cho "Bài 19. Thế năng điện" (Vật lí 11, lesson_id 38)
và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được).
Chạy: python3 content/lesson-samples/l11-the-nang-dien/build_figs.py

KHÔNG viết $...$ trong <text> của SVG (KaTeX chèn span HTML vào SVG làm mất chữ).
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from svg_lib import *  # noqa: E402,F401


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def dot(x, y, r=5, c="currentColor"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def kdefs(p):
    """defs 4 màu của svg_lib + marker màu chữ (p-k) cho đường sức."""
    d = defs(p)
    return d.replace("</defs>", f'<marker id="{p}-k" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" '
                                f'markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker></defs>')


def karrow(p, x1, y1, x2, y2, w=1.6, op=.7):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="currentColor" stroke-width="{w}" '
            f'opacity="{op}" marker-end="url(#{p}-k)"/>')


def sub(main, s):
    return f'{main}<tspan baseline-shift="sub" font-size="9">{s}</tspan>'


# ---- Hình 1: súng phun sơn tĩnh điện, hai đường bay cùng đầu, cùng cuối
S = (95, 115)
N1 = (340, 90)
b = kdefs("f1")
# súng phun
b += '<rect x="20" y="104" width="62" height="22" rx="5" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2"/>'
b += '<rect x="40" y="126" width="14" height="34" rx="3" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2"/>'
b += line(82, 115, S[0], S[1], "currentColor", 4)
b += text(20, 182, "súng phun", "currentColor", 12, "start")
b += text(20, 96, "hạt sơn (−)", BLUE, 12, "start")
# chi tiết nối đất
b += '<rect x="340" y="40" width="44" height="150" rx="4" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2"/>'
b += text(362, 30, "chi tiết", "currentColor", 12, "middle")
b += line(362, 190, 362, 206, "currentColor", 2) + line(348, 206, 376, 206, "currentColor", 2) + line(353, 211, 371, 211, "currentColor", 2) + line(358, 216, 366, 216, "currentColor", 2)
b += text(392, 214, "nối đất", "currentColor", 11, "start", "400")
# đường 1 thẳng, đường 2 cong (Bezier bậc 2, điểm điều khiển (200,250))
b += f'<line x1="{S[0]}" y1="{S[1]}" x2="{N1[0]-6}" y2="{N1[1]+0.6}" stroke="{RED}" stroke-width="2.5" marker-end="url(#f1-r)"/>'
b += f'<path d="M{S[0]},{S[1]} Q200,250 {N1[0]-4},{N1[1]+4}" fill="none" stroke="{BLUE}" stroke-width="2.5" stroke-dasharray="7 5" marker-end="url(#f1-b)"/>'
b += dot(S[0], S[1], 6, BLUE)
b += dot(N1[0], N1[1], 5, "currentColor") + text(N1[0] - 8, N1[1] - 10, "N", "currentColor", 14, "end", "700")
b += text(200, 88, "đường 1: bay thẳng", RED, 12, "middle", "700")
b += text(215, 204, "đường 2: lượn cong, dài hơn", BLUE, 12, "middle", "700")
fig1 = wrap("0 0 440 226", "Súng phun sơn tĩnh điện: hai hạt sơn cùng rời đầu súng, cùng tới điểm N theo đường thẳng và đường cong",
            b, "Hình 1. Hai hạt sơn mang điện âm cùng rời đầu súng, cùng bám vào điểm N: một hạt bay thẳng (đỏ), một hạt lượn cong (xanh).")

# ---- Hình 2: điện trường đều giữa hai bản, ba đường M -> N, hình chiếu d
M2, P2, N2 = (110, 80), (300, 80), (300, 180)
b = kdefs("f2")
b += line(30, 32, 410, 32, RED, 5) + line(30, 228, 410, 228, BLUE, 5)
b += text(30, 22, "bản (+)", RED, 12, "start", "700") + text(30, 250, "bản (−)", BLUE, 12, "start", "700")
for x in (50, 400):
    b += karrow("f2", x, 42, x, 216)
b += text(58, 140, "E", "currentColor", 14, "start", "700")
# đường thẳng (đỏ)
b += f'<line x1="{M2[0]}" y1="{M2[1]}" x2="{N2[0]-5}" y2="{N2[1]-2.6}" stroke="{RED}" stroke-width="2.5" marker-end="url(#f2-r)"/>'
# gấp khúc M -> P -> N (xanh)
b += f'<line x1="{M2[0]}" y1="{M2[1]}" x2="{P2[0]-6}" y2="{P2[1]}" stroke="{BLUE}" stroke-width="2.5" stroke-dasharray="7 4" marker-end="url(#f2-b)"/>'
b += f'<line x1="{P2[0]}" y1="{P2[1]}" x2="{N2[0]}" y2="{N2[1]-6}" stroke="{BLUE}" stroke-width="2.5" stroke-dasharray="7 4" marker-end="url(#f2-b)"/>'
# đường cong (lục), Bezier bậc 2 điều khiển (240,240), tới N từ phía dưới trái
b += f'<path d="M{M2[0]},{M2[1]} Q240,240 {N2[0]-3},{N2[1]+4}" fill="none" stroke="{GRN}" stroke-width="2.5" stroke-dasharray="3 4" marker-end="url(#f2-g)"/>'
b += dot(*M2, 5) + dot(*P2, 4) + dot(*N2, 5)
b += text(M2[0] - 8, M2[1] - 8, "M", "currentColor", 14, "end", "700")
b += text(P2[0] + 2, P2[1] - 10, "P", "currentColor", 14, "start", "700")
b += text(N2[0] + 8, N2[1] + 22, "N", "currentColor", 14, "start", "700")
# hình chiếu d
b += line(306, 80, 362, 80, "currentColor", 1.2, "3 3", .6) + line(306, 180, 362, 180, "currentColor", 1.2, "3 3", .6)
b += arrow("f2", "o", 352, 130, 352, 83, 2.2) + arrow("f2", "o", 352, 130, 352, 177, 2.2)
b += text(360, 135, "d", ORG, 15, "start", "700")
fig2 = wrap("0 0 440 262", "Điện trường đều giữa hai bản: ba đường đi từ M tới N cùng hình chiếu d lên đường sức",
            b, "Hình 2. Ba đường từ M tới N: thẳng (đỏ), gấp khúc M → P → N (xanh), cong (lục). Cả ba có cùng hình chiếu d lên đường sức (cam), nên công của lực điện bằng nhau.")

fig2 = fig2.replace('<figure class="fig" data-tl="1">', '<figure class="fig" data-tl="1" data-exp="tn-l11-the-nang-dien-02">')

# ---- Hình 3: đồ thị V theo x, số đo thí nghiệm khay nước muối
X0, Y0, SX, SY = 50, 200, 36, 170 / 6
data = [(2.0, 1.18), (4.0, 2.43), (6.0, 3.57), (8.0, 4.84)]
px = lambda x: X0 + SX * x
py = lambda v: Y0 - SY * v
b = kdefs("f3")
b += karrow("f3", X0, Y0, 425, Y0, 1.6, 1) + karrow("f3", X0, Y0, X0, 14, 1.6, 1)
for x in range(0, 11, 2):
    b += line(px(x), Y0, px(x), Y0 + 5, "currentColor", 1.4) + text(px(x), Y0 + 19, str(x), "currentColor", 11, "middle", "400")
for v in range(0, 7, 2):
    b += line(X0 - 5, f"{py(v):.1f}", X0, f"{py(v):.1f}", "currentColor", 1.4) + text(X0 - 9, f"{py(v)+4:.1f}", str(v), "currentColor", 11, "end", "400")
b += line(px(0), py(0), px(10), f"{py(6):.1f}", GRN, 2.2, "6 4")
for x, v in data:
    b += dot(f"{px(x):.1f}", f"{py(v):.1f}", 5, RED)
b += text(425, 190, "x (cm)", "currentColor", 12, "end")
b += text(58, 22, "V (V)", "currentColor", 12, "start")
b += text(150, 62, "đường lý thuyết V = 0,60·x", GRN, 12, "start", "700")
b += text(150, 80, "● số đo", RED, 12, "start", "700")
b += text(X0, 238, "lá âm (x = 0)", BLUE, 11, "start", "400")
b += text(px(10), 238, "lá dương (x = 10)", RED, 11, "end", "400")
fig3 = wrap("0 0 440 246", "Đồ thị điện thế V theo khoảng cách x tới lá âm: bốn số đo nằm sát đường thẳng V = 0,60x",
            b, "Hình 3. Bốn số đo (đỏ) nằm sát đường thẳng qua gốc: V tỉ lệ với x. Thế năng của q tại đó W = qV cũng tỉ lệ với x, đúng W = qEd.")
fig3 = fig3.replace('<figure class="fig" data-tl="1">', '<figure class="fig" data-tl="1" data-exp="tn-l11-the-nang-dien-01">')

# ---- Hình 4: bài toán mẫu, electron đi M -> P -> N (50 px = 1 cm)
YT, YB, CM = 30, 230, 50
M4 = (110, YB - 1 * CM)      # cách bản âm 1 cm
P4 = (110 + 3 * CM, M4[1])   # sang ngang 3 cm
N4 = (P4[0], M4[1] - 2 * CM) # lên 2 cm -> cách bản âm 3 cm
b = kdefs("f4")
b += line(30, YT, 410, YT, RED, 5) + line(30, YB, 410, YB, BLUE, 5)
b += text(30, YT - 10, "bản (+)", RED, 12, "start", "700") + text(30, YB + 22, "bản (−)", BLUE, 12, "start", "700")
for x in (40, 400):
    b += karrow("f4", x, YT + 10, x, YB - 12)
b += text(392, 134, "E", "currentColor", 14, "end", "700")
# đường đi
b += f'<line x1="{M4[0]}" y1="{M4[1]}" x2="{P4[0]-6}" y2="{P4[1]}" stroke="{BLUE}" stroke-width="2.6" marker-end="url(#f4-b)"/>'
b += f'<line x1="{P4[0]}" y1="{P4[1]}" x2="{N4[0]}" y2="{N4[1]+6}" stroke="{BLUE}" stroke-width="2.6" marker-end="url(#f4-b)"/>'
# lực điện lên electron: hướng lên (ngược E)
b += arrow("f4", "r", M4[0], M4[1] - 6, M4[0], M4[1] - 60, 3)
b += text(M4[0] + 12, M4[1] - 34, "F", RED, 14, "start", "700")
b += dot(*M4, 7, BLUE) + text(M4[0], M4[1] + 4, "−", "#fff", 12, "middle", "700")
b += dot(*P4, 4) + dot(*N4, 5)
b += text(M4[0] - 12, M4[1] + 5, "M", "currentColor", 14, "end", "700")
b += text(P4[0] + 10, P4[1] + 5, "P", "currentColor", 14, "start", "700")
b += text(N4[0] + 10, N4[1] + 5, "N", "currentColor", 14, "start", "700")
b += text((M4[0] + P4[0]) / 2, M4[1] + 20, "3 cm", BLUE, 12, "middle", "700")
b += text(P4[0] + 10, (P4[1] + N4[1]) / 2 + 4, "2 cm", BLUE, 12, "start", "700")
# kích thước 1 cm (M tới bản âm) và 4 cm (giữa hai bản)
b += line(70, M4[1], 70, YB - 3, ORG, 1.6) + line(64, M4[1], 76, M4[1], ORG, 1.6)
b += text(76, (M4[1] + YB) / 2 + 10, "1 cm", ORG, 11, "start", "700")
b += line(340, YT + 3, 340, YB - 3, ORG, 1.4, "4 3")
b += text(346, 112, "4 cm", ORG, 11, "start", "700")
fig4 = wrap("0 0 440 262", "Bài toán mẫu: electron đi từ M sang ngang 3 cm tới P rồi lên 2 cm tới N giữa hai bản cách nhau 4 cm",
            b, "Hình 4. Electron đi M → P (vuông góc đường sức) rồi P → N (ngược đường sức). Lực điện F lên electron hướng lên, ngược chiều E.")
fig4 = fig4.replace('<figure class="fig" data-tl="1">', '<figure class="fig" data-tl="1" data-exp="tn-l11-the-nang-dien-03">')

h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", f)
(HERE / "theory.html").write_text(h, encoding="utf8")
print("ok", len(h))
