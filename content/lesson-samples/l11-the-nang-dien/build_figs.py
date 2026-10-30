"""Sinh 4 hình SVG cho "Bài 19. Thế năng điện" (Vật lí 11, lesson_id 38)
và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được).
Chạy: python3 content/lesson-samples/l11-the-nang-dien/build_figs.py

KHÔNG viết $...$ trong <text> của SVG (KaTeX chèn span HTML vào SVG làm mất chữ).
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import RED, BLUE, ORG, GRN, text, wrap, arrow, chevron, field_line  # noqa: E402
import math


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def dot(x, y, r=5, c="currentColor"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def parrow(x1, y1, x2, y2, c, w=2.5, dash=""):
    """Đoạn thẳng có đầu V 30° tại (x2,y2), không marker."""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d}/>'
            + chevron(x2, y2, x2 - x1, y2 - y1, c, w, 11))


def qcurve(p0, pc, tip, c, w=2.5, dash=""):
    """Bezier bậc 2 p0 -> tip, điều khiển pc, đầu V tại tip theo tiếp tuyến (tip - pc)."""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="M{p0[0]},{p0[1]} Q{pc[0]},{pc[1]} {tip[0]:.1f},{tip[1]:.1f}" fill="none" stroke="{c}" stroke-width="{w}"{d}/>'
            + chevron(tip[0], tip[1], tip[0] - pc[0], tip[1] - pc[1], c, w, 11))


def back(P, Q, r):
    """Điểm cách Q một đoạn r về phía P (để đầu mũi tên dừng ngay mép chấm Q)."""
    dx, dy = Q[0] - P[0], Q[1] - P[1]
    n = math.hypot(dx, dy)
    return (Q[0] - dx / n * r, Q[1] - dy / n * r)


def fieldk(x, y1, y2):
    return f'<g opacity=".7">{field_line(x, y1, x, y2, "currentColor", 1.6)}</g>'


def sub(main, s):
    return f'{main}<tspan baseline-shift="sub" font-size="12">{s}</tspan>'


# ---- Hình 1: máy lọc không khí (đầu kim và tấm thu), hai đường bay cùng đầu, cùng cuối N
S = (95, 115)
N1 = (340, 93)
C1 = (200, 250)              # điểm điều khiển đường cong
b = ""
# đầu kim
b += '<rect x="20" y="104" width="62" height="22" rx="5" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2"/>'
b += '<rect x="40" y="126" width="14" height="34" rx="3" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2"/>'
b += line(82, 115, S[0], S[1], "currentColor", 4)
b += text(16, 184, "đầu kim", "currentColor", 14, "start")
b += text(16, 94, "hạt bụi (−)", BLUE, 14, "start", "700")
# tấm thu nối đất
b += '<rect x="340" y="40" width="44" height="150" rx="4" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2"/>'
b += text(362, 30, "tấm thu", "currentColor", 14, "middle")
b += line(362, 190, 362, 206, "currentColor", 2) + line(348, 206, 376, 206, "currentColor", 2) + line(353, 211, 371, 211, "currentColor", 2) + line(358, 216, 366, 216, "currentColor", 2)
b += text(342, 224, "nối đất", "currentColor", 14, "end", "400")
# đường 1 thẳng (đỏ), đường 2 cong (xanh): cả hai đầu V dừng ngay mép chấm N
b += parrow(S[0], S[1], *back(S, N1, 7), RED, 2.5)
b += qcurve(S, C1, back(C1, N1, 7), BLUE, 2.5, "7 5")
b += dot(S[0], S[1], 6, BLUE)
b += dot(N1[0], N1[1], 5, "currentColor") + text(N1[0] - 4, N1[1] - 14, "N", "currentColor", 16, "end", "700")
b += text(205, 84, "đường 1: bay thẳng", RED, 14, "middle", "700")
b += text(190, 206, "đường 2: lượn cong, dài hơn", BLUE, 14, "middle", "700")
fig1 = wrap("0 0 440 234", "Máy lọc không khí: hai hạt bụi cùng rời đầu kim, cùng tới điểm N theo đường thẳng và đường cong",
            b, "Hình 1. Hai hạt bụi mang điện âm cùng rời đầu kim, cùng bám vào điểm N: một hạt bay thẳng (đỏ), một hạt lượn cong (xanh).")

# ---- Hình 2: điện trường đều giữa hai bản, ba đường M -> N, hình chiếu d
M2, P2, N2 = (110, 80), (300, 80), (300, 180)
C2 = (240, 240)
b = ""
b += line(30, 32, 410, 32, RED, 5) + line(30, 228, 410, 228, BLUE, 5)
b += text(30, 22, "bản (+)", RED, 14, "start", "700") + text(30, 252, "bản (−)", BLUE, 14, "start", "700")
for x in (50, 400):
    b += fieldk(x, 42, 216)
b += text(60, 140, "E", "currentColor", 16, "start", "700")
# đường thẳng (đỏ)
b += parrow(M2[0], M2[1], *back(M2, N2, 7), RED, 2.5)
# gấp khúc M -> P -> N (xanh)
b += parrow(M2[0], M2[1], *back(M2, P2, 6), BLUE, 2.5, "7 4")
b += parrow(P2[0], P2[1], *back(P2, N2, 7), BLUE, 2.5, "7 4")
# đường cong (lục), tới N từ phía dưới trái
b += qcurve(M2, C2, back(C2, N2, 7), GRN, 2.5, "3 4")
b += dot(*M2, 5) + dot(*P2, 4) + dot(*N2, 5)
b += text(M2[0] - 8, M2[1] - 8, "M", "currentColor", 16, "end", "700")
b += text(P2[0] + 2, P2[1] - 10, "P", "currentColor", 16, "start", "700")
b += text(N2[0] + 8, N2[1] + 22, "N", "currentColor", 16, "start", "700")
# hình chiếu d (cam, mũi hai đầu)
b += line(306, 80, 362, 80, "currentColor", 1.2, "3 3", .6) + line(306, 180, 362, 180, "currentColor", 1.2, "3 3", .6)
b += arrow("", "o", 352, 130, 352, 83, 2.2) + arrow("", "o", 352, 130, 352, 177, 2.2)
b += text(362, 136, "d", ORG, 16, "start", "700")
fig2 = wrap("0 0 440 262", "Điện trường đều giữa hai bản: ba đường đi từ M tới N cùng hình chiếu d lên đường sức",
            b, "Hình 2. Ba đường từ M tới N: thẳng (đỏ), gấp khúc M → P → N (xanh), cong (lục). Cả ba có cùng hình chiếu d lên đường sức (cam), nên công của lực điện bằng nhau.")

fig2 = fig2.replace('<figure class="fig" data-tl="1">', '<figure class="fig" data-tl="1" data-exp="tn-l11-the-nang-dien-02">')

# ---- Hình 3: đồ thị V theo x, số đo thí nghiệm khay nước muối
X0, Y0, SX, SY = 50, 200, 36, 170 / 6
data = [(2.0, 1.18), (4.0, 2.43), (6.0, 3.57), (8.0, 4.84)]
px = lambda x: X0 + SX * x
py = lambda v: Y0 - SY * v
b = ""
b += parrow(X0, Y0, 425, Y0, "currentColor", 1.6) + parrow(X0, Y0, X0, 14, "currentColor", 1.6)
for x in range(0, 11, 2):
    b += line(px(x), Y0, px(x), Y0 + 5, "currentColor", 1.4) + text(px(x), Y0 + 20, str(x), "currentColor", 14, "middle", "400")
for v in range(0, 7, 2):
    b += line(X0 - 5, f"{py(v):.1f}", X0, f"{py(v):.1f}", "currentColor", 1.4) + text(X0 - 9, f"{py(v)+5:.1f}", str(v), "currentColor", 14, "end", "400")
b += line(px(0), py(0), px(10), f"{py(6):.1f}", GRN, 2.2, "6 4")
for x, v in data:
    b += dot(f"{px(x):.1f}", f"{py(v):.1f}", 5, RED)
b += text(425, 188, "x (cm)", "currentColor", 14, "end")
b += text(60, 22, "V (V)", "currentColor", 14, "start")
# chú giải: góc trên trái, xa đường lục (đường ở x ≤ 6 cm có V ≤ 3,6 V, tức y ≥ 98)
b += line(80, 44, 104, 44, GRN, 2.2, "6 4") + text(112, 49, "lý thuyết V = 0,60·x", GRN, 14, "start", "700")
b += dot(92, 68, 5, RED) + text(112, 73, "số đo", RED, 14, "start", "700")
b += text(X0, 240, "lá âm (x = 0)", BLUE, 14, "start", "400")
b += text(px(10), 240, "lá dương (x = 10)", RED, 14, "end", "400")
fig3 = wrap("0 0 440 250", "Đồ thị điện thế V theo khoảng cách x tới lá âm: bốn số đo nằm sát đường thẳng V = 0,60x",
            b, "Hình 3. Bốn số đo (đỏ) nằm sát đường thẳng qua gốc: V tỉ lệ với x. Thế năng của q tại đó W = qV cũng tỉ lệ với x, đúng W = qEd.")
fig3 = fig3.replace('<figure class="fig" data-tl="1">', '<figure class="fig" data-tl="1" data-exp="tn-l11-the-nang-dien-01">')

# ---- Hình 4: bài toán mẫu, electron đi M -> P -> N (50 px = 1 cm)
YT, YB, CM = 30, 230, 50
M4 = (110, YB - 1 * CM)      # cách bản âm 1 cm
P4 = (110 + 3 * CM, M4[1])   # sang ngang 3 cm
N4 = (P4[0], M4[1] - 2 * CM) # lên 2 cm -> cách bản âm 3 cm
b = ""
b += line(30, YT, 410, YT, RED, 5) + line(30, YB, 410, YB, BLUE, 5)
b += text(30, YT - 10, "bản (+)", RED, 14, "start", "700") + text(30, YB + 24, "bản (−)", BLUE, 14, "start", "700")
for x in (40, 400):
    b += fieldk(x, YT + 10, YB - 12)
b += text(390, 134, "E", "currentColor", 16, "end", "700")
# đường đi
b += parrow(M4[0] + 10, M4[1], P4[0] - 6, P4[1], BLUE, 2.6)
b += parrow(P4[0], P4[1], N4[0], N4[1] + 7, BLUE, 2.6)
# lực điện lên electron: hướng lên (ngược E)
b += arrow("", "r", M4[0], M4[1] - 10, M4[0], M4[1] - 64, 3)
b += text(M4[0] + 12, M4[1] - 38, "F", RED, 16, "start", "700")
b += dot(*M4, 9, BLUE) + text(M4[0], M4[1] + 5, "−", "#fff", 16, "middle", "700")
b += dot(*P4, 4) + dot(*N4, 5)
b += text(M4[0] - 14, M4[1] + 6, "M", "currentColor", 16, "end", "700")
b += text(P4[0] + 10, P4[1] + 6, "P", "currentColor", 16, "start", "700")
b += text(N4[0] + 10, N4[1] + 6, "N", "currentColor", 16, "start", "700")
b += text((M4[0] + P4[0]) / 2, M4[1] + 22, "3 cm", BLUE, 14, "middle", "700")
b += text(P4[0] + 10, (P4[1] + N4[1]) / 2 + 5, "2 cm", BLUE, 14, "start", "700")
# kích thước 1 cm (M tới bản âm) và 4 cm (giữa hai bản)
b += line(70, M4[1], 70, YB - 3, ORG, 1.6) + line(64, M4[1], 76, M4[1], ORG, 1.6)
b += text(76, (M4[1] + YB) / 2 + 12, "1 cm", ORG, 14, "start", "700")
b += line(340, YT + 3, 340, YB - 3, ORG, 1.4, "4 3")
b += text(346, 112, "4 cm", ORG, 14, "start", "700")
fig4 = wrap("0 0 440 264", "Bài toán mẫu: electron đi từ M sang ngang 3 cm tới P rồi lên 2 cm tới N giữa hai bản cách nhau 4 cm",
            b, "Hình 4. Electron đi M → P (vuông góc đường sức) rồi P → N (ngược đường sức). Lực điện F lên electron hướng lên, ngược chiều E.")
fig4 = fig4.replace('<figure class="fig" data-tl="1">', '<figure class="fig" data-tl="1" data-exp="tn-l11-the-nang-dien-03">')

h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", f)
(HERE / "theory.html").write_text(h, encoding="utf8")
print("ok", len(h))
