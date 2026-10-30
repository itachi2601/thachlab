"""Sinh 4 hình SVG cho bài "Mô tả dao động điều hoà" và thay mốc <!--FIGn-->.

Chạy trong thư mục bài: python3 build_figs.py
Số liệu chấm trên Hình 4 lấy đúng từ x = A·cos(2πt/T), A = 5 cm, T = 1 s, φ = 0.
"""
import math
import importlib.util as _iu
import pathlib as _pl
from svg_lib import RED, BLUE, ORG, GRN, text, wrap
# Đầu mũi tên chữ V 30° (thầy chốt 7/10/2026) lấy từ thư viện của skill — không dùng marker tam giác
_sp = _iu.spec_from_file_location("svg_lib_skill", _pl.Path(__file__).resolve().parents[3]
                                  / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/svg_lib.py")
_sk = _iu.module_from_spec(_sp)
_sp.loader.exec_module(_sk)
chevron = _sk.chevron

FS = 15      # cỡ nhãn chính (viewBox 440 → ~13 px ở 375 px)
FS2 = 14     # cỡ nhãn phụ, không dưới 14

def poly(pts, c, w=2.2, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline fill="none" stroke="{c}" stroke-width="{w}"{d} points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>'

def dot(x, y, r=4.5, c="currentColor"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'

def line(x1, y1, x2, y2, c="currentColor", w=1.6, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>')

def vec(x1, y1, x2, y2, c, w=2.4, L=11):
    """Mũi tên thân thẳng + đầu V 30° tại (x2, y2)."""
    return line(x1, y1, x2, y2, c, w) + chevron(x2, y2, x2 - x1, y2 - y1, c, w, L)

def axis(x1, y1, x2, y2, w=1.6):
    """Trục toạ độ: đầu V 30° ở cuối trục."""
    return vec(x1, y1, x2, y2, "currentColor", w, 10)

def dbl_h(x1, x2, y, c, w=1.6):
    """Kích thước ngang: hai đầu V chĩa ra ngoài (x1 < x2)."""
    assert x1 < x2
    return (line(x1, y, x2, y, c, w) + chevron(x1, y, -1, 0, c, w, 8) + chevron(x2, y, 1, 0, c, w, 8))

def dbl_v(x, y_top, y_bot, c, w=1.6):
    """Kích thước dọc: hai đầu V chĩa ra ngoài (y_top < y_bot)."""
    assert y_top < y_bot
    return (line(x, y_top, x, y_bot, c, w) + chevron(x, y_top, 0, -1, c, w, 8) + chevron(x, y_bot, 0, 1, c, w, 8))

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
# −A và +A đối xứng qua O (hình chiếu lên trục x)
assert abs((mid[0] - left[0]) - (right[0] - mid[0])) < 0.05

arc = [bob(-TH + 2 * TH * i / 40) for i in range(41)]
assert abs(arc[0][0] - left[0]) < 0.05 and abs(arc[-1][0] - right[0]) < 0.05

# Mũi "sắp về O": tiếp tuyến cung tại biên phải, chiều giảm góc (về O); gốc ở mép quả lắc
ux, uy = -math.cos(TH), math.sin(TH)
start = (right[0] + 9 * ux, right[1] + 9 * uy)
tip = (right[0] + 40 * ux, right[1] + 40 * uy)
tip_th = math.atan2(tip[0] - PIVOT[0], tip[1] - PIVOT[1])
assert 0 < tip_th < TH, tip_th     # đầu mũi tên nằm giữa O và +A
assert tip[0] < right[0]           # chĩa về phía O

axis_y = 200
b = f'<circle cx="214" cy="30" r="22" fill="none" stroke="currentColor" stroke-width="2"/>'
b += line(214, 30, 214, 16, "currentColor", 1.6)
b += line(214, 30, 226, 36, "currentColor", 1.6)
b += text(184, 35, "đồng hồ", "currentColor", FS2, "end", "600")
b += poly(arc, "currentColor", 1.6)
b += line(PIVOT[0], PIVOT[1], left[0], left[1], "currentColor", 1.4, "", 0.35)
b += line(PIVOT[0], PIVOT[1], mid[0], mid[1] - 7, "currentColor", 1.5, "", 0.45)
b += line(PIVOT[0], PIVOT[1], right[0], right[1], "currentColor", 2.4)
b += f'<circle cx="{left[0]:.1f}" cy="{left[1]:.1f}" r="7" fill="none" stroke="{BLUE}" stroke-width="2"/>'
b += f'<circle cx="{mid[0]:.1f}" cy="{mid[1]:.1f}" r="7" fill="none" stroke="currentColor" stroke-width="2" opacity="0.6"/>'
b += dot(right[0], right[1], 8, ORG)
b += line(left[0], left[1] + 7, left[0], axis_y, BLUE, 1.1, "4 3", 0.7)
b += line(mid[0], mid[1] + 7, mid[0], axis_y, "currentColor", 1.1, "4 3", 0.55)
b += line(right[0], right[1] + 8, right[0], axis_y, ORG, 1.1, "4 3", 0.8)
b += axis(108, axis_y, 396, axis_y, 1.8)
b += text(404, axis_y + 5, "x", "currentColor", FS, "start", "700")
b += text(left[0], axis_y + 22, "−A", BLUE, FS, "middle", "700")
b += text(mid[0], axis_y + 22, "O", "currentColor", FS, "middle", "700")
b += text(right[0], axis_y + 22, "+A", ORG, FS, "middle", "700")
b += vec(start[0], start[1], tip[0], tip[1], GRN, 2.4)
# nhãn đặt sát quả lắc cam, mỗi ý một dòng, bên phải nét đứt
b += text(right[0] + 14, right[1] - 6, "em bắt đầu nhìn", ORG, FS2, "start", "700")
b += text(right[0] + 14, right[1] + 30, "sắp về O", GRN, FS2, "start", "700")
fig1 = with_exp(wrap(
    "0 0 440 234",
    "Con lắc đồng hồ chỉ đi trong đoạn từ trừ A đến cộng A; ở biên dương thì sắp về vị trí cân bằng",
    b,
    "Hình 1. Quả lắc chỉ trong [−A, A]; ở biên dương thì sắp về O.",
), "tn-l11-motadddh-01")

# ---- Hình 2: vòng tròn lượng giác, φ = 60°
cx, cy, R = 168, 132, 80
PHI = math.pi / 3
Mx = cx + R * math.cos(PHI)
My = cy - R * math.sin(PHI)
assert abs(math.hypot(Mx - cx, My - cy) - R) < 0.05
ang = math.atan2(-(My - cy), Mx - cx)
assert abs(ang - PHI) < 0.01
Px, Py = Mx, cy
assert abs((Px - cx) - R * math.cos(PHI)) < 0.05      # OP = A cos φ (li độ)
# cung φ, bán kính 30, từ Ox tới OM, ngược chiều kim đồng hồ trên hình (sweep 0 trong SVG)
RA = 30
ax0, ay0 = cx + RA, cy
ax1 = cx + RA * math.cos(PHI)
ay1 = cy - RA * math.sin(PHI)
# mũi cung "chiều tăng pha" ngoài vòng tròn, từ 70° tới 105° (góc tăng = ngược chiều kim đồng hồ)
RP = R + 14
g0, g1 = math.radians(70), math.radians(105)
parc = [(cx + RP * math.cos(g0 + (g1 - g0) * i / 30), cy - RP * math.sin(g0 + (g1 - g0) * i / 30)) for i in range(31)]
assert parc[-1][0] < parc[0][0]                       # đi sang trái ở phía trên = ngược kim
tdx, tdy = -math.sin(g1), -math.cos(g1)               # tiếp tuyến chiều góc tăng tại cuối cung

b = f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="currentColor" stroke-width="1.8"/>'
b += axis(cx - R - 26, cy, cx + R + 36, cy, 1.6)
b += text(cx + R + 42, cy + 5, "x", "currentColor", FS, "start", "700")
b += line(Mx, My, Px, Py, ORG, 1.4, "4 3", 0.9)
b += line(cx, cy, Mx, My, RED, 2.4)
b += f'<path d="M{ax0:.1f},{ay0:.1f} A{RA},{RA} 0 0 0 {ax1:.1f},{ay1:.1f}" fill="none" stroke="{GRN}" stroke-width="2"/>'
b += dot(Mx, My, 5.5, RED)
b += dot(Px, Py, 4.5, ORG)
b += dot(cx, cy, 3, "currentColor")
b += poly(parc, GRN, 2.2)
b += chevron(parc[-1][0], parc[-1][1], tdx, tdy, GRN, 2.2, 10)
b += text(Mx + 7, cy - 14, "φ", GRN, 17, "start", "700")
b += text(cx - R - 6, cy + 20, "−A", "currentColor", FS, "end", "700")
b += text(cx + R + 5, cy - 9, "+A", "currentColor", FS, "start", "700")
b += text(cx - 6, cy + 20, "O", "currentColor", FS, "end", "700")
b += text(Mx + 10, My - 6, "M", RED, FS, "start", "700")
b += text(Px + 7, Py + 20, "P", ORG, FS, "start", "700")
b += text(parc[-1][0] - 6, parc[-1][1] - 6, "chiều tăng pha", GRN, FS2, "end", "700")
# chú thích bên phải, mỗi ý một dòng
b += text(282, 40, "M: lúc t = 0", RED, FS2, "start", "700")
b += text(282, 62, "P: hình chiếu", ORG, FS2, "start", "700")
b += text(282, 80, "của M lên Ox", ORG, FS2, "start", "700")
fig2 = wrap(
    "0 0 440 236",
    "Vòng tròn lượng giác: pha ban đầu là góc giữa bán kính lúc t bằng 0 và trục Ox",
    b,
    "Hình 2. φ là góc giữa bán kính lúc t = 0 và trục Ox.",
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

b = text(66, 24, "đường 1", BLUE, FS2, "start", "700")
b += text(166, 24, "φ = 0", BLUE, FS2, "start", "600")
b += text(246, 24, "đường 2", ORG, FS2, "start", "700")
b += text(346, 24, "φ = −π/2", ORG, FS2, "start", "600")
b += line(ox, oy - Amp - 8, ox, oy + Amp + 16, "currentColor", 1.3, "", 0.8)
b += axis(ox, oy, ox + Tpx + 48, oy, 1.6)
b += text(ox + Tpx + 54, oy + 5, "t", "currentColor", FS, "start", "700")
b += text(ox - 8, oy - Amp + 5, "A", "currentColor", FS2, "end", "700")
b += text(ox - 8, oy + 5, "0", "currentColor", FS2, "end", "600")
b += text(ox - 8, oy + Amp + 5, "−A", "currentColor", FS2, "end", "700")
b += poly(pts1, BLUE, 2.4)
b += poly(pts2, ORG, 2.4)
b += dot(ox, oy - Amp, 4.5, BLUE)
b += dot(x_peak2, oy - Amp, 4.5, ORG)
b += dbl_h(ox, x_peak2, oy - Amp - 18, GRN, 1.6)
b += text((ox + x_peak2) / 2, oy - Amp - 26, "T/4", GRN, FS2, "middle", "700")
for x, lab in ((ox, "0"), (ox + 0.5 * Tpx, "T/2"), (ox + Tpx, "T")):
    b += line(x, oy - 4, x, oy + 4, "currentColor", 1.3)
    b += text(x, oy + Amp + 30, lab, "currentColor", FS2, "middle", "600")
fig3 = wrap(
    "0 0 440 214",
    "Hai dao động cùng biên độ cùng chu kì: đường 1 đạt đỉnh sớm hơn đường 2 một khoảng T/4",
    b,
    "Hình 3. Đường 1 đạt đỉnh sớm hơn đường 2 đúng T/4.",
)

# ---- Hình 4: đọc đồ thị, năm chấm đúng phương trình
# x = 5·cos(2πt), T = 1 s, A = 5 cm. Trục t tuyến tính.
A_CM, T_S = 5.0, 1.0
ox, oy, Tpx, Amp = 84, 104, 280, 40
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

trough_y = xy(0.5)[1]
dim_y = oy + Amp + 32
assert dim_y - 18 > trough_y + 4      # nhãn T không chạm đáy đường cong

b = axis(ox, oy + Amp + 14, ox, 26, 1.4)
b += axis(ox, oy, ox + Tpx + 36, oy, 1.6)
b += text(ox + Tpx + 42, oy + 5, "t (s)", "currentColor", FS2, "start", "700")
for v, lab in ((A_CM, "5"), (0, "0"), (-A_CM, "−5")):
    yy = oy - (Amp / A_CM) * v
    b += line(ox - 4, yy, ox + 4, yy, "currentColor", 1.3)
    b += text(ox - 9, yy + 5, lab, "currentColor", FS2, "end", "700" if v else "600")
b += text(ox + 10, 24, "x (cm)", "currentColor", FS2, "start", "700")
b += poly(pts, BLUE, 2.4)
b += dbl_v(ox - 38, oy - Amp, oy, GRN, 1.5)
b += text(ox - 46, oy - Amp / 2 + 5, "A", GRN, FS, "end", "700")
for x, lab in ((ox, "0"), (ox + 0.5 * Tpx, "0,5"), (ox + Tpx, "1")):
    b += line(x, oy - 4, x, oy + 4, "currentColor", 1.3)
    b += text(x, dim_y + 24, lab, "currentColor", FS2, "middle", "600")
b += dbl_h(ox, ox + Tpx, dim_y, GRN, 1.5)
b += text(ox + Tpx / 2, dim_y - 6, "T", GRN, FS, "middle", "700")
for xd, yd in dots:
    b += dot(xd, yd, 4.2, RED)
fig4 = with_exp(wrap(
    "0 0 440 212",
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
