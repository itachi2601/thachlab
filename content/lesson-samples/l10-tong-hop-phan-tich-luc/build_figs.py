"""Sinh 4 hình SVG cho bài 'Tổng hợp và phân tích lực. Cân bằng lực' và thay mốc <!--FIGn--> trong theory.src.html -> theory.html."""
import math
from svg_lib import *

def P(x, y): return f"{x:.1f},{y:.1f}"
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'
def dot(x, y, r=4, c="currentColor"): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'
def vec(p, c, x, y, ang, L, w=3, dash=""):
    """Mũi tên từ (x,y), góc ang (độ, ngược chiều kim đồng hồ, trục y hướng lên), dài L; trả (chuỗi, đầu mút)."""
    a = math.radians(ang); x2, y2 = x + L * math.cos(a), y - L * math.sin(a)
    return arrow(p, c, x, y, round(x2, 1), round(y2, 1), w, dash), (x2, y2)
def sub(base, s): return f'{base}<tspan dy="4" font-size="9">{s}</tspan>'
def arc(x, y, r, a1, a2, c="currentColor", w=1.5):
    p1 = (x + r * math.cos(math.radians(a1)), y - r * math.sin(math.radians(a1)))
    p2 = (x + r * math.cos(math.radians(a2)), y - r * math.sin(math.radians(a2)))
    sweep = 0 if a2 > a1 else 1
    return f'<path d="M{P(*p1)} A{r},{r} 0 0 {sweep} {P(*p2)}" fill="none" stroke="{c}" stroke-width="{w}"/>'

# ---- Hình 1: quy tắc hình bình hành
ox, oy = 90, 190
a1, a2 = 15, 85              # hướng F1, F2 (alpha = 70 độ)
L1, L2 = 190, 120
x1, y1 = ox + L1 * math.cos(math.radians(a1)), oy - L1 * math.sin(math.radians(a1))
x2, y2 = ox + L2 * math.cos(math.radians(a2)), oy - L2 * math.sin(math.radians(a2))
xf, yf = x1 + x2 - ox, y1 + y2 - oy
b = defs("f1")
b += line(x1, y1, xf, yf, "currentColor", 1.5, "5 4", .6) + line(x2, y2, xf, yf, "currentColor", 1.5, "5 4", .6)
b += arrow("f1", "r", ox, oy, round(x1, 1), round(y1, 1), 3.2) + arrow("f1", "b", ox, oy, round(x2, 1), round(y2, 1), 3.2)
b += arrow("f1", "g", ox, oy, round(xf, 1), round(yf, 1), 3.6)
b += arc(ox, oy, 46, a1, a2, "currentColor") + text(ox + 26, oy - 44, "α", "currentColor", 14, "start", "700")
fa = math.degrees(math.atan2(oy - yf, xf - ox))
b += arc(ox, oy, 78, a1, fa, GRN) + text(ox + 82, oy - 40, "θ", GRN, 13, "start", "700")
b += text(x1 - 34, y1 + 30, sub("F", "1"), RED, 15, "end", "700")
b += text(x2 - 10, y2 + 4, sub("F", "2"), BLUE, 15, "end", "700")
b += text(xf + 10, yf + 8, "F", GRN, 16, "start", "700")
b += dot(ox, oy, 4)
b += text(ox - 6, oy + 18, "O", "currentColor", 12, "end", "600")
fig1 = wrap("0 0 440 220", "Quy tắc hình bình hành: hai lực F1, F2 hợp nhau góc alpha, đường chéo là hợp lực F",
            b, "Hình 1. Quy tắc hình bình hành: đường chéo xuất phát từ O (xanh lá) là hợp lực <em>F</em>; α là góc giữa hai lực.")

# ---- Hình 2: phân tích lực khi kéo vali / xe
gx = 70                       # mặt đất
b = defs("f2")
b += line(20, 190, 420, 190, "currentColor", 2, "", .7)
b += f'<rect x="{gx+10}" y="146" width="96" height="44" rx="4" fill="rgba(148,163,184,.2)" stroke="currentColor" stroke-width="2.4"/>'
b += f'<circle cx="{gx+30}" cy="192" r="6" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="{gx+88}" cy="192" r="6" fill="none" stroke="currentColor" stroke-width="2"/>'
hx, hy = gx + 106, 160        # điểm đặt lực (tay kéo)
alpha = 40
s, (ex, ey) = vec("f2", "r", hx, hy, alpha, 140, 3.4)
b += s
b += line(hx, hy, ex, hy, GRN, 2.4, "", 1) + arrow("f2", "g", hx, hy, round(ex, 1), hy, 3)
b += arrow("f2", "o", ex, hy, round(ex, 1), round(ey, 1), 3)
b += line(ex, hy, ex, ey, ORG, 2.4)  # trục dựng
b += line(hx, hy, ex, ey, RED, 0)    # không vẽ thêm
b += arc(hx, hy, 52, 0, alpha, "currentColor") + text(hx + 56, hy - 8, "α", "currentColor", 14, "start", "700")
b += text((hx + ex) / 2 - 12, (hy + ey) / 2 - 8, "F", RED, 16, "end", "700")
b += text(hx + 8, hy + 20, sub("F", "x") + " = F cos α", GRN, 13, "start", "700")
b += text(ex + 8, (hy + ey) / 2 + 4, sub("F", "y") + " = F sin α", ORG, 13, "start", "700")
fig2 = wrap("0 0 440 220", "Phân tích lực kéo F của tay thành thành phần nằm ngang Fx và thẳng đứng Fy",
            b, "Hình 2. Lực kéo nghiêng <em>F</em> phân tích thành <em>F<sub>x</sub></em> (làm xe chạy) và <em>F<sub>y</sub></em> (nhấc bớt xe lên); α là góc với phương ngang.")

# ---- Hình 3: mặt phẳng nghiêng
al = 30
bx, by = 40, 200               # chân dốc
Ls = 340
tx, ty = bx + Ls * math.cos(math.radians(al)), by - Ls * math.sin(math.radians(al))
b = defs("f3")
b += f'<polygon points="{P(bx,by)} {P(tx,ty)} {P(tx,by)}" fill="rgba(148,163,184,.12)" stroke="currentColor" stroke-width="2.4"/>'
# khối đặt trên dốc ở khoảng giữa
u = (math.cos(math.radians(al)), -math.sin(math.radians(al)))      # vector đơn vị dọc dốc (hướng lên)
nvec = (math.sin(math.radians(al)), math.cos(math.radians(al)))    # pháp tuyến ra ngoài (lên-trái? -> lên-phải)
nvec = (-math.sin(math.radians(al)), -math.cos(math.radians(al)))  # lên trên-trái (y hướng xuống màn hình = âm)
cx0, cy0 = bx + 205 * u[0], by + 205 * u[1]
hw, hh = 34, 24
pts = [(cx0 - hw*u[0], cy0 - hw*u[1]), (cx0 + hw*u[0], cy0 + hw*u[1]),
       (cx0 + hw*u[0] + hh*nvec[0], cy0 + hw*u[1] + hh*nvec[1]), (cx0 - hw*u[0] + hh*nvec[0], cy0 - hw*u[1] + hh*nvec[1])]
b += f'<polygon points="{" ".join(P(*p) for p in pts)}" fill="rgba(251,146,60,.18)" stroke="currentColor" stroke-width="2.4"/>'
gx0, gy0 = cx0 + 12 * nvec[0], cy0 + 12 * nvec[1]       # trọng tâm
b += dot(gx0, gy0, 3.5)
Lp = 96
b += arrow("f3", "r", round(gx0, 1), round(gy0, 1), round(gx0, 1), round(gy0 + Lp, 1), 3.4)               # P thẳng đứng xuống
px, pyy = Lp * math.sin(math.radians(al)), Lp * math.cos(math.radians(al))
b += arrow("f3", "g", round(gx0, 1), round(gy0, 1), round(gx0 - px * math.cos(math.radians(al)), 1), round(gy0 + px * math.sin(math.radians(al)), 1), 3)   # Px dọc dốc xuống
b += arrow("f3", "o", round(gx0, 1), round(gy0, 1), round(gx0 + pyy * math.sin(math.radians(al)), 1), round(gy0 + pyy * math.cos(math.radians(al)), 1), 3)   # Py vuông góc, vào dốc
b += text(gx0 + 10, gy0 + Lp + 4, "P", RED, 16, "start", "700")
b += text(gx0 - px * math.cos(math.radians(al)) - 4, gy0 + px * math.sin(math.radians(al)) - 12, sub("P", "x") + " = P sin α", GRN, 13, "end", "700")
b += text(gx0 + pyy * math.sin(math.radians(al)) + 10, gy0 + pyy * math.cos(math.radians(al)) - 4, sub("P", "y"), ORG, 14, "start", "700") + text(gx0 + pyy * math.sin(math.radians(al)) + 10, gy0 + pyy * math.cos(math.radians(al)) + 12, "= P cos α", ORG, 12, "start", "700")
b += arc(bx, by, 70, 0, al, "currentColor") + text(bx + 78, by - 8, "α", "currentColor", 14, "start", "700")
fig3 = wrap("0 0 440 232", "Vật trên mặt phẳng nghiêng góc alpha: trọng lực P phân tích thành Px dọc dốc và Py vuông góc dốc",
            b, "Hình 3. Trên dốc nghiêng góc α, trọng lực <em>P</em> phân tích thành <em>P<sub>x</sub></em> = <em>P</em> sin α (dọc dốc) và <em>P<sub>y</sub></em> = <em>P</em> cos α (ép vào dốc).")

# ---- Hình 4: đèn treo bằng hai dây
half = 30
ox, oy = 220, 160              # chỗ buộc dây
L = 100
b = defs("f4")
b += line(60, 22, 380, 22, "currentColor", 3, "", 1)
for k in range(10):
    b += line(64 + k * 34, 22, 56 + k * 34, 12, "currentColor", 1.6, "", .5)
ax, ay = ox - L * math.sin(math.radians(half)) * 1.6, 22
bx2 = ox + L * math.sin(math.radians(half)) * 1.6
b += line(ax, 22, ox, oy, "currentColor", 1.8, "", .6) + line(bx2, 22, ox, oy, "currentColor", 1.8, "", .6)
# vectơ lực tại O
dx, dy = ox - ax, oy - 22
nrm = math.hypot(dx, dy)
Tl = 62
b += arrow("f4", "r", ox, oy, round(ox - dx / nrm * Tl, 1), round(oy - dy / nrm * Tl, 1), 3.2)
b += arrow("f4", "b", ox, oy, round(ox + dx / nrm * Tl, 1), round(oy - dy / nrm * Tl, 1), 3.2)
b += arrow("f4", "o", ox, oy, ox, oy + 74, 3.4)
Fy = 2 * (dy / nrm) * Tl
b += arrow("f4", "g", ox, oy, ox, round(oy - Fy, 1), 3.2, "6 4")
b += line(ox - dx / nrm * Tl, oy - dy / nrm * Tl, ox, oy - Fy, "currentColor", 1.4, "5 4", .55)
b += line(ox + dx / nrm * Tl, oy - dy / nrm * Tl, ox, oy - Fy, "currentColor", 1.4, "5 4", .55)
b += dot(ox, oy, 4.5)
b += f'<path d="M{ox-20},{oy+98} L{ox+20},{oy+98} L{ox+14},{oy+132} L{ox-14},{oy+132} Z" fill="rgba(251,146,60,.2)" stroke="currentColor" stroke-width="2.2"/>' + line(ox, oy + 74, ox, oy + 98, "currentColor", 1.6)
b += text(ox - dx / nrm * Tl - 14, oy - dy / nrm * Tl + 18, sub("T", "1"), RED, 15, "end", "700")
b += text(ox + dx / nrm * Tl + 14, oy - dy / nrm * Tl + 18, sub("T", "2"), BLUE, 15, "start", "700")
b += text(ox + 10, oy + 66, "P", ORG, 16, "start", "700")
b += text(ox, oy - Fy - 7, sub("F", "12") + " = P", GRN, 13, "middle", "700")
b += arc(ox, oy, 34, 90 - half, 90 + half, "currentColor") + text(ox + 8, oy - 24, "α", "currentColor", 13, "start", "700")
fig4 = wrap("0 0 440 304", "Đèn treo bằng hai dây: hai lực căng T1, T2 có hợp lực F12 cân bằng với trọng lực P",
            b, "Hình 4. Đèn đứng yên: hợp lực <em>F</em><sub>12</sub> của hai lực căng <em>T</em><sub>1</sub>, <em>T</em><sub>2</sub> cân bằng với trọng lực <em>P</em>; α là góc giữa hai dây.")

fig4 = fig4.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-tonghopluc-03"', 1)
h = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(h)
print("ok", len(h))
