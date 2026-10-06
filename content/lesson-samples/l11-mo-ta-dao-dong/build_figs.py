"""Sinh 4 hình SVG cho bài "Mô tả dao động điều hoà" và thay mốc <!--FIGn-->.

Chạy trong thư mục bài: python3 build_figs.py
Số liệu chấm trên Hình 4 lấy đúng từ x = A·cos(2πt/T), A = 5 cm, T = 1 s, φ = 0.
"""
import math
from svg_lib import *

def poly(pts, c, w=2.2, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline fill="none" stroke="{c}" stroke-width="{w}"{d} points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>'

def dot(x, y, r=4.5, c="currentColor"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'

def line(x1, y1, x2, y2, c="currentColor", w=1.6, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>')

def dbl_h(x1, x2, y, c, w=1.6):
    b = f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" stroke="{c}" stroke-width="{w}"/>'
    b += f'<path d="M{x1+7:.1f},{y-4:.1f} L{x1:.1f},{y:.1f} L{x1+7:.1f},{y+4:.1f}" fill="none" stroke="{c}" stroke-width="{w}"/>'
    b += f'<path d="M{x2-7:.1f},{y-4:.1f} L{x2:.1f},{y:.1f} L{x2-7:.1f},{y+4:.1f}" fill="none" stroke="{c}" stroke-width="{w}"/>'
    return b

def dbl_v(x, y1, y2, c, w=1.6):
    b = f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"/>'
    b += f'<path d="M{x-4:.1f},{y1+7:.1f} L{x:.1f},{y1:.1f} L{x+4:.1f},{y1+7:.1f}" fill="none" stroke="{c}" stroke-width="{w}"/>'
    b += f'<path d="M{x-4:.1f},{y2-7:.1f} L{x:.1f},{y2:.1f} L{x+4:.1f},{y2-7:.1f}" fill="none" stroke="{c}" stroke-width="{w}"/>'
    return b

def text_sub(x, y, base, sub, c="currentColor", size=15, anchor="middle", weight="700"):
    return (f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{base}<tspan baseline-shift="sub" font-size="{max(13, int(size*0.72))}">{sub}</tspan></text>')

def with_exp(fig, exp):
    return fig.replace('<figure class="fig" data-tl="1">',
                       f'<figure class="fig" data-tl="1" data-exp="{exp}">', 1)

# ---- Hình 1: con lắc đồng hồ, trục li độ [-A, A]
PIVOT = (214, 58)
L = 92
TH = 0.56  # rad, lệch khỏi phương thẳng đứng

def bob(theta):
    return (PIVOT[0] + L * math.sin(theta), PIVOT[1] + L * math.cos(theta))

left, mid, right = bob(-TH), bob(0), bob(TH)
for p in (left, mid, right):
    assert abs(math.hypot(p[0] - PIVOT[0], p[1] - PIVOT[1]) - L) < 0.05

arc = [bob(-TH + 2 * TH * i / 40) for i in range(41)]
assert abs(arc[0][0] - left[0]) < 0.05 and abs(arc[-1][0] - right[0]) < 0.05

# Mũi "sắp về": giảm góc, tiếp tuyến cung, hướng về O
ux, uy = -math.cos(TH), math.sin(TH)
tip = (right[0] + 30 * ux, right[1] + 30 * uy)
tip_th = math.atan2(tip[0] - PIVOT[0], tip[1] - PIVOT[1])
assert 0 < tip_th < TH, tip_th

axis_y = 196
b = defs("f1")
b += f'<circle cx="214" cy="30" r="22" fill="none" stroke="currentColor" stroke-width="2"/>'
b += line(214, 30, 214, 16, "currentColor", 1.6)
b += line(214, 30, 226, 36, "currentColor", 1.6)
b += text(188, 34, "đồng hồ", "currentColor", 13, "end", "600")
b += poly(arc, "currentColor", 1.6)
b += line(PIVOT[0], PIVOT[1], left[0], left[1], "currentColor", 1.4, "", 0.35)
b += line(PIVOT[0], PIVOT[1], mid[0], mid[1], "currentColor", 1.5, "", 0.45)
b += line(PIVOT[0], PIVOT[1], right[0], right[1], "currentColor", 2.4)
b += dot(left[0], left[1], 7, "none")
b += f'<circle cx="{left[0]:.1f}" cy="{left[1]:.1f}" r="7" fill="none" stroke="{BLUE}" stroke-width="2"/>'
b += f'<circle cx="{mid[0]:.1f}" cy="{mid[1]:.1f}" r="7" fill="none" stroke="currentColor" stroke-width="2"/>'
b += dot(right[0], right[1], 8, ORG)
b += line(left[0], left[1], left[0], axis_y, BLUE, 1.1, "4 3", 0.7)
b += line(mid[0], mid[1] + 8, mid[0], axis_y, "currentColor", 1.1, "4 3", 0.55)
b += line(right[0], right[1], right[0], axis_y, ORG, 1.1, "4 3", 0.8)
b += line(108, axis_y, 392, axis_y, "currentColor", 1.8)
b += f'<path d="M392,{axis_y} L382,{axis_y-5} L382,{axis_y+5} Z" fill="currentColor"/>'
b += text(404, axis_y + 5, "x", "currentColor", 15, "start", "700")
b += text(left[0], axis_y + 22, "−A", BLUE, 15, "middle", "700")
b += text(mid[0], axis_y + 22, "O", "currentColor", 15, "middle", "700")
b += text(right[0], axis_y + 22, "+A", ORG, 15, "middle", "700")
b += arrow("f1", "g", right[0], right[1], tip[0], tip[1], 2.4)
b += text(tip[0] - 36, tip[1] + 18, "sắp về O", GRN, 13, "start", "700")
b += text(16, 48, "lúc bắt đầu nhìn", ORG, 13, "start", "700")
fig1 = with_exp(wrap(
    "0 0 440 232",
    "Con lắc đồng hồ chỉ đi trong đoạn từ trừ A đến cộng A; ở biên dương thì sắp về vị trí cân bằng",
    b,
    "Hình 1. Quả lắc chỉ trong [−A, A]; ở biên dương thì sắp về O.",
), "tn-l11-motadddh-01")

# ---- Hình 2: vòng tròn lượng giác, φ₀ = 60°
cx, cy, R = 168, 132, 74
PHI = math.pi / 3
Mx = cx + R * math.cos(PHI)
My = cy - R * math.sin(PHI)
assert abs(math.hypot(Mx - cx, My - cy) - R) < 0.05
ang = math.atan2(-(My - cy), Mx - cx)
assert abs(ang - PHI) < 0.01
Px, Py = Mx, cy
# cung φ₀, bán kính 34, chiều kim đồng hồ của SVG = ngược chiều kim đồng hồ trên hình
ax0, ay0 = cx + 34, cy
ax1 = cx + 34 * math.cos(PHI)
ay1 = cy - 34 * math.sin(PHI)
# tiếp tuyến chiều tăng pha (ngược chiều kim đồng hồ trên hình)
tx, ty = -math.sin(PHI), -math.cos(PHI)
t2 = (Mx + 26 * tx, My + 26 * ty)
assert t2[0] < Mx and t2[1] < My

b = defs("f2")
b += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="currentColor" stroke-width="1.8"/>'
b += line(cx - R - 28, cy, cx + R + 36, cy, "currentColor", 1.6)
b += f'<path d="M{cx+R+36},{cy} L{cx+R+26},{cy-5} L{cx+R+26},{cy+5} Z" fill="currentColor"/>'
b += text(cx + R + 42, cy + 5, "x", "currentColor", 15, "start", "700")
b += line(Mx, My, Px, Py, ORG, 1.4, "4 3", 0.9)
b += line(cx, cy, Mx, My, RED, 2.4)
b += f'<path d="M{ax0:.1f},{ay0:.1f} A34,34 0 0 1 {ax1:.1f},{ay1:.1f}" fill="none" stroke="{GRN}" stroke-width="2"/>'
b += dot(Mx, My, 5.5, RED)
b += dot(Px, Py, 4.5, ORG)
b += arrow("f2", "g", Mx, My, t2[0], t2[1], 2.2)
lx = cx + 22 * math.cos(PHI / 2)
ly = cy - 22 * math.sin(PHI / 2)
b += text_sub(Mx + 6, cy - 20, "φ", "0", GRN, 14, "start", "700")
b += text(cx - R - 8, cy + 20, "−A", "currentColor", 14, "end", "700")
b += text(cx + R + 4, cy - 10, "+A", "currentColor", 14, "start", "700")
b += text(cx - 6, cy + 18, "O", "currentColor", 14, "end", "700")
b += text(Mx + 12, My - 14, "M", RED, 15, "start", "700")
b += text(Px + 8, Py + 18, "P", ORG, 14, "start", "700")
# nhãn t = 0 ở góc trống, không đè nét đứt M–P và không chạm chú thích phải
b += text(12, 22, "M lúc t = 0", RED, 13, "start", "700")
b += text(268, 28, "chiều tăng pha", GRN, 13, "start", "700")
b += text(268, 48, "P: hình chiếu", ORG, 13, "start", "700")
b += text(268, 66, "của M lên Ox", ORG, 13, "start", "700")
fig2 = wrap(
    "0 0 440 236",
    "Vòng tròn lượng giác: pha ban đầu là góc giữa bán kính lúc t bằng 0 và trục Ox",
    b,
    "Hình 2. φ₀ là góc giữa bán kính lúc t = 0 và trục Ox.",
)

# ---- Hình 3: x1 = A cos(ωt), x2 = A cos(ωt − π/2), lệch T/4
ox, oy, Tpx, Amp = 58, 128, 280, 42

def y_cos(t_frac, phi):
    return oy - Amp * math.cos(2 * math.pi * t_frac + phi)

pts1 = [(ox + (i / 100) * Tpx, y_cos(i / 100, 0)) for i in range(0, 116)]
pts2 = [(ox + (i / 100) * Tpx, y_cos(i / 100, -math.pi / 2)) for i in range(0, 116)]
# đỉnh đường 1 tại t = 0; đỉnh đường 2 tại t = T/4
assert abs(y_cos(0, 0) - (oy - Amp)) < 0.01
assert abs(y_cos(0.25, -math.pi / 2) - (oy - Amp)) < 0.01
x_peak2 = ox + 0.25 * Tpx
# trục t chia đều: 0, T/2, T
ticks = [ox + f * Tpx for f in (0, 0.5, 1)]
assert abs((ticks[1] - ticks[0]) - (ticks[2] - ticks[1])) < 0.01

b = defs("f3")
b += text(70, 24, "đường 1", BLUE, 14, "start", "700")
b += text(168, 24, "φ = 0", BLUE, 14, "start", "600")
b += text(250, 24, "đường 2", ORG, 14, "start", "700")
b += text(348, 24, "φ = −π/2", ORG, 14, "start", "600")
b += line(ox, oy - Amp - 8, ox, oy + Amp + 16, "currentColor", 1.3, "", 0.8)
b += line(ox, oy, ox + Tpx + 48, oy, "currentColor", 1.6)
b += f'<path d="M{ox+Tpx+48},{oy} L{ox+Tpx+38},{oy-5} L{ox+Tpx+38},{oy+5} Z" fill="currentColor"/>'
b += text(ox + Tpx + 54, oy + 5, "t", "currentColor", 15, "start", "700")
b += text(ox - 8, oy - Amp + 4, "A", "currentColor", 14, "end", "700")
b += text(ox - 8, oy + 5, "0", "currentColor", 13, "end", "600")
b += text(ox - 8, oy + Amp + 4, "−A", "currentColor", 14, "end", "700")
b += poly(pts1, BLUE, 2.4)
b += poly(pts2, ORG, 2.4)
b += dot(ox, oy - Amp, 4.5, BLUE)
b += dot(x_peak2, oy - Amp, 4.5, ORG)
b += dbl_h(ox, x_peak2, oy - Amp - 18, GRN, 1.6)
b += text((ox + x_peak2) / 2, oy - Amp - 26, "T/4", GRN, 14, "middle", "700")
for x, lab in ((ox, "0"), (ox + 0.5 * Tpx, "T/2"), (ox + Tpx, "T")):
    b += line(x, oy - 4, x, oy + 4, "currentColor", 1.3)
    b += text(x, oy + Amp + 28, lab, "currentColor", 13, "middle", "600")
fig3 = wrap(
    "0 0 440 214",
    "Hai dao động cùng biên độ cùng chu kì: đường 1 đạt đỉnh sớm hơn đường 2 một khoảng T/4",
    b,
    "Hình 3. Đường 1 đạt đỉnh sớm hơn đường 2 đúng T/4.",
)

# ---- Hình 4: đọc đồ thị, năm chấm đúng phương trình
# x = 5·cos(2πt), T = 1 s, A = 5 cm. Trục t tuyến tính.
A_CM, T_S = 5.0, 1.0
ox, oy, Tpx, Amp = 72, 100, 280, 40
TIMES = [0.0, 0.1, 0.2, 0.3, 0.4]

def x_cm(t):
    return A_CM * math.cos(2 * math.pi * t / T_S)

def xy(t):
    return ox + (t / T_S) * Tpx, oy - (Amp / A_CM) * x_cm(t)

pts = [xy(i / 120) for i in range(121)]
dots = [xy(t) for t in TIMES]
for t, (xd, yd) in zip(TIMES, dots):
    # chấm phải đúng hàm, và trục cm tuyến tính
    y_expect = oy - (Amp / A_CM) * x_cm(t)
    assert abs(yd - y_expect) < 0.05
    assert abs(xd - (ox + t * Tpx)) < 0.05
# hai đỉnh cách đúng một T
assert abs(xy(0)[0] - ox) < 0.05
assert abs(xy(1)[0] - (ox + Tpx)) < 0.05
assert abs(xy(0)[1] - xy(1)[1]) < 0.05
# vạch 0; 0,5; 1 cách đều
tick_x = [ox + f * Tpx for f in (0, 0.5, 1)]
assert abs((tick_x[1] - tick_x[0]) - (tick_x[2] - tick_x[1])) < 0.01
# giá trị làm tròn khớp bảng bài (3 chữ số, và đọc 0,1 cm)
expect = [(0.0, 5.0, 5.0), (0.1, 4.045, 4.0), (0.2, 1.545, 1.5),
          (0.3, -1.545, -1.5), (0.4, -4.045, -4.0)]
for t, xt, xr in expect:
    assert abs(round(x_cm(t), 3) - xt) < 1e-9
    assert abs(round(x_cm(t), 1) - xr) < 1e-9

b = defs("f4")
b += line(ox, 28, ox, oy + Amp + 14, "currentColor", 1.4)
b += line(ox, oy, ox + Tpx + 36, oy, "currentColor", 1.6)
b += f'<path d="M{ox+Tpx+36},{oy} L{ox+Tpx+26},{oy-5} L{ox+Tpx+26},{oy+5} Z" fill="currentColor"/>'
b += text(ox + Tpx + 42, oy + 5, "t (s)", "currentColor", 13, "start", "700")
b += text(ox - 10, oy - Amp + 4, "5", "currentColor", 13, "end", "700")
b += text(ox - 10, oy + 4, "0", "currentColor", 13, "end", "600")
b += text(ox - 10, oy + Amp + 4, "−5", "currentColor", 13, "end", "700")
b += text(16, 22, "x (cm)", "currentColor", 13, "start", "700")
b += poly(pts, BLUE, 2.4)
b += dbl_v(ox - 28, oy, oy - Amp, GRN, 1.5)
b += text(ox - 28, oy - Amp / 2 + 4, "A", GRN, 14, "end", "700")
for x, lab in ((ox, "0"), (ox + 0.5 * Tpx, "0,5"), (ox + Tpx, "1")):
    b += line(x, oy - 4, x, oy + 4, "currentColor", 1.3)
    b += text(x, oy + Amp + 48, lab, "currentColor", 13, "middle", "600")
b += dbl_h(ox, ox + Tpx, oy + Amp + 28, GRN, 1.5)
b += text(ox + Tpx / 2, oy + Amp + 22, "T", GRN, 14, "middle", "700")
for xd, yd in dots:
    b += dot(xd, yd, 4.2, RED)
fig4 = with_exp(wrap(
    "0 0 440 228",
    "Đồ thị li độ theo thời gian với năm chấm tính từ phương trình x bằng 5 cos 2 pi t",
    b,
    "Hình 4. Năm chấm từ x = 5 cos(2πt) cm. Đỉnh là A, hai đỉnh cách T.",
), "tn-l11-motadddh-02")

h = open("theory.src.html", encoding="utf8").read()
for n, fig in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fig, 1)
assert "<!--FIG" not in h
open("theory.html", "w", encoding="utf8").write(h)
print("ok", len(h))
