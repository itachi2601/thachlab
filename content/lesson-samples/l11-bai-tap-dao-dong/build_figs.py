"""Sinh 4 hình SVG cho Bài 4. Bài tập về dao động điều hoà (VL11, lesson 23).
Thay mốc <!--FIGn--> trong theory.src.html → theory.html (chạy lại được, không sửa .src).
Hình kiểm bằng TOẠ ĐỘ: điểm trên đường tròn đúng góc pha, đồ thị đúng x = A cos(2πt/T),
mũi tên quay ngược chiều kim đồng hồ (pha tăng), nhãn không vượt viewBox.
Chạy: python3 build_figs.py (từ bất kỳ đâu)."""
import math, pathlib, os
HERE = pathlib.Path(__file__).resolve().parent
os.chdir(HERE)
from svg_lib import *

FS = 17      # cỡ chữ nhãn (viewBox 420)
FSS = 13     # chỉ số dưới

def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'

def dot(x, y, r=5, c="currentColor"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'

def vec(x1, y1, x2, y2, c="currentColor", w=2.2, L=10):
    """Mũi tên một đầu, đầu chữ V 30° (không dùng marker)."""
    return line(x1, y1, x2, y2, c, w) + chevron(x2, y2, x2 - x1, y2 - y1, c, w, L)

def dvec(x1, y1, x2, y2, c="currentColor", w=2, L=10):
    """Mũi tên hai đầu (đo khoảng)."""
    return (line(x1, y1, x2, y2, c, w) + chevron(x2, y2, x2 - x1, y2 - y1, c, w, L)
            + chevron(x1, y1, x1 - x2, y1 - y2, c, w, L))

def T(x, y, s, c="currentColor", anchor="start", weight="600", size=FS):
    return text(x, y, s, c, size, anchor, weight)

BOXES = {}   # hình -> danh sách hộp nhãn (x0, y0, x1, y1) để kiểm chồng/biên

def lab(fig, x, y, s, c="currentColor", anchor="start", weight="600", size=FS, w=None):
    """Nhãn + ghi hộp bao ước lượng (0,56·size mỗi ký tự) để kiểm chồng chữ."""
    n = len(s.replace("&lt;", "<").replace("&gt;", ">"))
    wd = w if w else 0.56 * size * n
    x0 = x if anchor == "start" else (x - wd / 2 if anchor == "middle" else x - wd)
    BOXES.setdefault(fig, []).append((x0, y - size * 0.8, x0 + wd, y + size * 0.2, s))
    return T(x, y, s, c, anchor, weight, size)

def check(fig, W, H):
    bs = BOXES.get(fig, [])
    for x0, y0, x1, y1, s in bs:
        assert x0 >= 2 and x1 <= W - 2 and y0 >= 0 and y1 <= H, (fig, s, x0, x1, y0, y1)
    for i in range(len(bs)):
        for j in range(i + 1, len(bs)):
            a, b = bs[i], bs[j]
            ov = not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])
            assert not ov, (fig, a[4], b[4])

def pts(P, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<polyline fill="none" stroke="{c}" stroke-width="{w}"{d} opacity="{op}" stroke-linejoin="round" points="'
            + " ".join(f"{x:.1f},{y:.1f}" for x, y in P) + '"/>')

# =========================== Hình 1: đồng hồ quả lắc treo tường (chỉ cảnh, không số liệu)
W1, H1 = 420, 262
b = ""
CASE = (130, 290)
b += f'<rect x="{CASE[0]}" y="10" width="{CASE[1]-CASE[0]}" height="240" rx="12" fill="none" stroke="currentColor" stroke-width="3"/>'
b += '<circle cx="210" cy="58" r="36" fill="none" stroke="currentColor" stroke-width="2.4"/>'
for k in range(12):
    a_ = math.radians(30 * k)
    b += line(210 + 30 * math.sin(a_), 58 - 30 * math.cos(a_), 210 + 34 * math.sin(a_), 58 - 34 * math.cos(a_), "currentColor", 1.6)
b += line(210, 58, 210, 36, "currentColor", 2.4) + line(210, 58, 226, 64, "currentColor", 2.4)
PX, PY, R, AMP = 210, 104, 110, 20
b += dot(PX, PY, 4)
def bob(ang):
    a_ = math.radians(ang)
    return PX + R * math.sin(a_), PY + R * math.cos(a_)
arc = [bob(-AMP + 2 * AMP * i / 40) for i in range(41)]
b += pts(arc, BLUE, 2, "6 5", .9)
lx, ly = bob(-AMP)
b += line(PX, PY, lx, ly, "currentColor", 1.6, "4 4", .45) + f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="13" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="4 3" opacity=".5"/>'
sx, sy = bob(AMP)
b += line(PX, PY, sx, sy, "currentColor", 2.4) + f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="13" fill="{ORG}" stroke="currentColor" stroke-width="1.6"/>'
# điện thoại bấm giờ
b += '<rect x="22" y="40" width="36" height="58" rx="6" fill="none" stroke="currentColor" stroke-width="2.4"/>'
b += line(30, 52, 50, 52, "currentColor", 1.4) + f'<circle cx="40" cy="72" r="9" fill="none" stroke="{GRN}" stroke-width="2"/>'
b += line(40, 72, 40, 66, GRN, 2)
b += lab(1, 12, 124, "bấm giờ", "currentColor", "start", "600")
b += lab(1, 122, ly + 6, "biên trái", "currentColor", "end", "600")
b += lab(1, 298, sy + 6, "biên phải", "currentColor", "start", "600")
b += line(124, ly, lx - 15, ly, "currentColor", 1.2, "2 3", .7) + line(296, sy, sx + 15, sy, "currentColor", 1.2, "2 3", .7)
check(1, W1, H1)
for x0, y0, x1, y1, s_ in BOXES[1]:
    assert all(not (x0 - 4 <= px <= x1 + 4) for px in CASE), s_   # nhãn không bị vỏ đồng hồ cắt
assert abs(lx + sx - 2 * PX) < 1e-9 and sy + 13 < 250          # hai biên đối xứng, quả lắc trong vỏ
fig1 = wrap(f"0 0 {W1} {H1}", "Đồng hồ quả lắc treo tường: quả lắc đi qua lại giữa biên trái và biên phải, một bạn cầm điện thoại bấm giờ",
            b, "Hình 1. Quả lắc đồng hồ đi qua lại giữa hai biên.<br>Em bấm giờ từ biên trái tới biên phải.")

# =========================== Hình 2: đồ thị x–t, x = A cos(2πt/T)
W2, H2 = 420, 262
b = ""
X0, Y0 = 52, 128
AP = 68          # px ứng với A
TP = 150         # px ứng với T
XT = lambda t: X0 + t * TP
XV = lambda v: Y0 - v * AP
curve = [(XT(i / 200 * 2.2), XV(math.cos(2 * math.pi * i / 200 * 2.2))) for i in range(201)]
# trục
b += vec(X0, Y0, 404, Y0, "currentColor", 1.6)
b += vec(X0, H2 - 18, X0, 18, "currentColor", 1.6)
b += lab(2, 408, Y0 - 10, "t", "currentColor", "end", "700")
b += lab(2, X0 + 10, 26, "x", "currentColor", "start", "700")
b += pts(curve, ORG, 2.8)
# đường gióng +A, −A
b += line(X0, XV(1), 392, XV(1), "currentColor", 1, "4 4", .45)
b += line(X0, XV(-1), 392, XV(-1), "currentColor", 1, "4 4", .45)
# đỉnh, đáy
pk1, pk2, tr1 = XT(1), XT(2), XT(1.5)
for t in (0, 1, 2):
    assert abs(math.cos(2 * math.pi * t) - 1) < 1e-9
    b += dot(XT(t), XV(1), 4.5, ORG)
for t in (0.5, 1.5):
    assert abs(math.cos(2 * math.pi * t) + 1) < 1e-9
    b += dot(XT(t), XV(-1), 4.5, ORG)
# A: từ trục tới đỉnh, ở t = 0 bên trái trục tung? -> đặt ở t = 0,25T bên phải trục: dùng x = X0+18
xa = X0 + 20
b += dvec(xa, Y0, xa, XV(1) + 1, RED, 2)
b += lab(2, xa + 8, Y0 - 30, "A", RED, "start", "700")
# 2A: đỉnh t = T (x=pk1) xuống đáy t = 1,5T
x2a = (pk1 + tr1) / 2
b += dvec(x2a, XV(1), x2a, XV(-1), BLUE, 2)
b += lab(2, x2a + 8, Y0 + 26, "2A", BLUE, "start", "700")
# T: đỉnh → đỉnh (trên đỉnh)
yT = XV(1) - 18
b += line(pk1, XV(1) - 4, pk1, yT - 6, "currentColor", 1, "3 3", .6) + line(pk2, XV(1) - 4, pk2, yT - 6, "currentColor", 1, "3 3", .6)
b += dvec(pk1 + 2, yT, pk2 - 2, yT, GRN, 2.2)
b += lab(2, (pk1 + pk2) / 2, yT - 8, "T", GRN, "middle", "700")
# T/2: đỉnh → đáy (dưới đáy)
yH = XV(-1) + 24
b += line(pk1, Y0 + 6, pk1, yH + 6, "currentColor", 1, "3 3", .6) + line(tr1, XV(-1) + 6, tr1, yH + 6, "currentColor", 1, "3 3", .6)
b += dvec(pk1 + 2, yH, tr1 - 2, yH, GRN, 2.2)
b += lab(2, (pk1 + tr1) / 2, yH + 24, "T/2", GRN, "middle", "700")
check(2, W2, H2)
# nhãn 2A nằm giữa hai nhánh đồ thị (không chạm đường cong): đường cong tại y nhãn cách x nhãn > 8 px
fig2 = wrap(f"0 0 {W2} {H2}", "Đồ thị li độ theo thời gian dạng côsin: A từ trục tới đỉnh, đỉnh tới đáy cao 2A, hai đỉnh liền kề cách nhau T, đỉnh tới đáy cách nhau nửa chu kì",
            b, "Hình 2. Đồ thị li độ – thời gian.<br>Hai đỉnh liền kề cách nhau $T$.<br>Đỉnh tới đáy: cao $2A$, cách nhau $T/2$.")

# =========================== Hình 3: vòng tròn pha, mốc T/12 và T/6
W3, H3 = 420, 300
b = ""
CX, CY, RR = 210, 152, 112
def P(deg, r=RR):
    a = math.radians(deg)
    return CX + r * math.cos(a), CY - r * math.sin(a)     # góc pha tăng = ngược chiều kim đồng hồ
b += f'<circle cx="{CX}" cy="{CY}" r="{RR}" fill="none" stroke="currentColor" stroke-width="1.8" opacity=".75"/>'
b += vec(64, CY, 384, CY, "currentColor", 1.6)
b += lab(3, 392, CY + 6, "x", "currentColor", "start", "700")
# cung O→A/2 (90°→60°) cam, A/2→A (60°→0°) xanh lá
b += pts([P(90 - 30 * i / 30) for i in range(31)], ORG, 4.5)
b += pts([P(60 - 60 * i / 60) for i in range(61)], GRN, 4.5)
for deg in (90, 60, 0, 120, 180):
    x, y = P(deg)
    b += dot(x, y, 5)
for deg in (60, 120):
    x, y = P(deg)
    b += line(x, y, x, CY, "currentColor", 1.3, "4 4", .7)
# vạch chia trên trục: x = A cos(deg)
ticks = ((180, "−A", "end", -6), (120, "−A/2", "middle", 0), (90, "O", "middle", 0), (60, "A/2", "middle", 0), (0, "A", "start", 6))
for deg, s, an, dx in ticks:
    x = P(deg)[0]
    b += line(x, CY - 5, x, CY + 5, "currentColor", 2)
    b += lab(3, x + dx, CY + 24, s, "currentColor", an, "700")
assert abs(P(60)[0] - (CX + RR / 2)) < 1e-9 and abs(P(120)[0] - (CX - RR / 2)) < 1e-9   # hình chiếu đúng ±A/2
# nhãn cung
x, y = P(77, RR + 16); b += lab(3, x, y, "T/12", ORG, "start", "700")
x, y = P(28, RR + 14); b += lab(3, x, y, "T/6", GRN, "start", "700")
# chiều quay: ngược chiều kim đồng hồ, đặt ở góc −50°
(x1, y1), (x2, y2) = P(-56), P(-44)
b += chevron(x2, y2, x2 - x1, y2 - y1, BLUE, 2.6, 13)
assert y2 < y1   # pha tăng ở nửa dưới bên phải: điểm đi lên
b += lab(3, 12, 28, "nửa trên: v &lt; 0", "currentColor", "start", "600", w=0.56 * FS * 15)
b += lab(3, 12, 286, "nửa dưới: v &gt; 0", "currentColor", "start", "600", w=0.56 * FS * 15)
check(3, W3, H3)
fig3 = wrap(f"0 0 {W3} {H3}", "Vòng tròn pha bán kính A: từ O tới A/2 điểm M quét 30 độ, mất T/12; từ A/2 ra biên quét 60 độ, mất T/6",
            b, "Hình 3. M quay ngược chiều kim đồng hồ, góc $2\\pi$ ứng với $T$.<br>Từ O tới $A/2$: quét $30^\\circ$, mất $T/12$.<br>Từ $A/2$ ra biên: quét $60^\\circ$, mất $T/6$.")

# =========================== Hình 4 (trong lời giải): pha −π/3 → π/2
W4, H4 = 420, 276
b = ""
CY4 = 142
def Q(deg, r=RR):
    a = math.radians(deg)
    return CX + r * math.cos(a), CY4 - r * math.sin(a)
b += f'<circle cx="{CX}" cy="{CY4}" r="{RR}" fill="none" stroke="currentColor" stroke-width="1.8" opacity=".75"/>'
b += vec(64, CY4, 384, CY4, "currentColor", 1.6)
b += lab(4, 392, CY4 + 6, "x", "currentColor", "start", "700")
sweep = [Q(-60 + 150 * i / 75) for i in range(76)]
b += pts(sweep, RED, 4)
b += chevron(sweep[-1][0], sweep[-1][1], sweep[-1][0] - sweep[-3][0], sweep[-1][1] - sweep[-3][1], RED, 3, 14)
m0, m1 = Q(-60), Q(90)
b += dot(*m0, 6, RED) + dot(*m1, 6, RED)
b += line(m0[0], m0[1], m0[0], CY4, "currentColor", 1.3, "4 4", .7)
assert abs(m0[0] - (CX + 4 / 8 * RR)) < 1e-9     # x0 = 4 cm = A/2
assert abs(m1[0] - CX) < 1e-9                   # pha π/2 ⇒ x = 0
for xv, s in ((0, "0"), (4, "4"), (8, "8 cm")):
    x = CX + xv / 8 * RR
    b += line(x, CY4 - 5, x, CY4 + 5, "currentColor", 2)
    b += lab(4, x + 6, CY4 - 10, s, "currentColor", "start", "700")
b += lab(4, m0[0] + 12, m0[1] + 16, "t = 0", RED, "start", "700")
b += lab(4, m1[0] + 12, m1[1] - 6, "qua O lần đầu", RED, "start", "700")
b += lab(4, CX, CY4 + 52, "Δφ = 5π/6", "currentColor", "middle", "700").replace("<text ", '<text font-family="Georgia, \'Times New Roman\', serif" ', 1)
check(4, W4, H4)
fig4 = wrap(f"0 0 {W4} {H4}", "Vòng tròn pha: M đi từ pha âm pi phần ba ở nửa dưới, qua biên dương, tới pha pi phần hai ở đỉnh, quét năm pi phần sáu",
            b, "Hình 4. M quét từ pha $-\\pi/3$ tới $\\pi/2$.<br>Trên trục (cm): vật đi $4 \\to 8 \\to 0$.")

h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert h.count(f"<!--FIG{n}-->") == 1, n
    h = h.replace(f"<!--FIG{n}-->", f)
assert "$" not in "".join(s for s in (fig1, fig2, fig3, fig4) for s in [s.split("<figcaption>")[0]])  # không $ trong SVG
# số hình theo thứ tự xuất hiện
order = [h.index(f"Hình {n}.") for n in (1, 2, 3, 4)]
assert order == sorted(order)
(HERE / "theory.html").write_text(h, encoding="utf8")
print("ok", len(h), "bytes,", h.count('<figure class="fig"'), "hình")
