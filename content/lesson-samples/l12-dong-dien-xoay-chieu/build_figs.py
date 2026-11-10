"""Chèn 3 hình SVG tự vẽ + 1 ảnh OpenStax vào theory.src.html -> theory.html (idempotent).
Chạy từ thư mục này:  python3 build_figs.py"""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import math, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *

def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')

def sub(base, idx):
    return f'{base}<tspan dy="4" font-size="14">{idx}</tspan><tspan dy="-4"> </tspan>'

# ---- Hình 1: khung quay, nhìn dọc trục (vẽ lại 31/10: chữ ≥14, đầu V 30°, nhãn không đè đường sức)
cx, cy, a = 236, 142, math.radians(40)
b = ""
for y in (cy - 88, cy - 38, cy + 12, cy + 62):
    b += field_line(14, y, 414, y, RED, 1.9)
b += text(14, 26, "Đường sức từ: chiều của vectơ B", RED, 14, "start", "700")
nx, ny = math.cos(a), -math.sin(a)
dx, dy = -ny, nx
L = 70
b += f'<line x1="{cx-dx*L:.0f}" y1="{cy-dy*L:.0f}" x2="{cx+dx*L:.0f}" y2="{cy+dy*L:.0f}" stroke="currentColor" stroke-width="6" stroke-linecap="round"/>'
b += f'<circle cx="{cx}" cy="{cy}" r="5" fill="currentColor"/>'
b += text(cx - 26, cy + 8, "O", "currentColor", 15, "start", "700")
b += arrow("f1", "o", cx, cy, round(cx + nx * 80), round(cy + ny * 80), 2.8)
b += text(round(cx + nx * 80) + 8, round(cy + ny * 80) - 4, "n", ORG, 16, "start", "700")
r = 34
b += f'<path d="M{cx+r} {cy} A{r} {r} 0 0 0 {cx+r*nx:.1f} {cy+r*ny:.1f}" fill="none" stroke="{GRN}" stroke-width="2.4"/>'
b += text(cx + 40, cy - 18, "α", GRN, 16, "start", "700")
# mũi tên quay ngược chiều kim đồng hồ (góc α tăng), nằm trong khe giữa hai đường sức
R = 62
t0, t1 = math.radians(56), math.radians(112)
pts = [(cx + R * math.cos(t0 + (t1 - t0) * i / 30), cy - R * math.sin(t0 + (t1 - t0) * i / 30)) for i in range(31)]
b += '<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="none" stroke="{GRN}" stroke-width="2.6"/>'
b += chevron(pts[-1][0], pts[-1][1], pts[-1][0] - pts[-3][0], pts[-1][1] - pts[-3][1], GRN, 2.6, 11)
b += text(cx - 6, cy - 68, "ω", GRN, 17, "start", "700")
b += text(14, 236, "Chấm tròn O: trục quay, vuông góc trang giấy", "currentColor", 14)
b += text(14, 258, "Đường đậm: khung dây nhìn từ cạnh", "currentColor", 14)
b += text(14, 282, "α = ωt + φ  →  Φ = NBS·cos α", "currentColor", 15, "start", "700")
fig1 = wrap("0 0 430 294", "Khung dây quay đều quanh trục O trong từ trường đều, pháp tuyến n hợp với B góc alpha tăng dần",
            b, "Hình 1. Nhìn dọc trục quay: khung quay đều nên góc α tăng đều theo thời gian, và Φ = NBS·cos α dao động tuần hoàn.",
            exp="tn-l12-xoaychieu-01")

# ---- Hình 2 (chú thích "Hình 4"): Φ và e vuông pha (vẽ lại 31/10: chữ ≥14, mỗi ý một dòng)
b = ""
x0, x1, yc, A = 40, 396, 122, 58
W = x1 - x0
b += f'<line x1="{x0}" y1="{yc}" x2="{x1+12}" y2="{yc}" stroke="currentColor" stroke-width="1.5" opacity=".6"/>'
b += chevron(x1 + 14, yc, 1, 0, "currentColor", 1.5, 9)
b += text(x1 + 18, yc + 5, "t", "currentColor", 15, "start", "700")
def curve(fn, col):
    pts = " ".join(f"{x0 + W*k/100:.1f},{yc - A*fn(2*math.pi*k/100):.1f}" for k in range(101))
    return f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.8" stroke-linejoin="round"/>'
for k in (0, 25, 50, 75, 100):
    x = x0 + W * k / 100
    b += f'<line x1="{x:.1f}" y1="{yc-A-6}" x2="{x:.1f}" y2="{yc+A+8}" stroke="currentColor" stroke-width="1" stroke-dasharray="4 4" opacity=".4"/>'
b += curve(math.cos, BLUE) + curve(math.sin, RED)
for k, lab in ((0, "0"), (25, "T/4"), (50, "T/2"), (75, "3T/4"), (100, "T")):
    x = x0 + W * k / 100
    b += text(round(x), yc + A + 26, lab, "currentColor", 14, "middle", "600")
xq = x0 + W / 4
b += f'<circle cx="{x0}" cy="{yc-A}" r="5" fill="{BLUE}"/><circle cx="{x0}" cy="{yc}" r="5" fill="{RED}"/>'
b += f'<circle cx="{xq:.1f}" cy="{yc-A}" r="5" fill="{RED}"/><circle cx="{xq:.1f}" cy="{yc}" r="5" fill="{BLUE}"/>'
b += text(x0 + 6, 22, "Φ đỉnh", BLUE, 14, "start", "700") + text(x0 + 6, 42, "e = 0", RED, 14, "start", "700")
b += text(round(xq) + 8, 22, "e đỉnh", RED, 14, "start", "700") + text(round(xq) + 8, 42, "Φ = 0", BLUE, 14, "start", "700")
b += f'<line x1="40" y1="236" x2="66" y2="236" stroke="{BLUE}" stroke-width="3"/>' + text(72, 241, "Φ: từ thông", BLUE, 14)
b += f'<line x1="196" y1="236" x2="222" y2="236" stroke="{RED}" stroke-width="3"/>' + text(228, 241, "e: suất điện động", RED, 14)
fig2 = wrap("0 0 430 252", "Đồ thị từ thông Φ và suất điện động e theo thời gian, lệch nhau một phần tư chu kì",
            b, "Hình 4. Φ và e lệch nhau T/4 (vuông pha): cái này ở đỉnh thì cái kia đi qua 0.",
            exp="tn-l12-xoaychieu-01")

# ---- Hình 3: u(t), đỉnh 311 V, hiệu dụng 220 V, T = 20 ms (vẽ lại 31/10: chữ ≥14, chỉ số tspan, thêm nhãn trục)
b = ""
x0, x1, yc = 52, 372, 140
S = 0.34  # px / V
ms = (x1 - x0) / 40
def Y(v): return yc - v * S
for v, col, dash in ((311, RED, "6 4"), (-311, RED, "6 4"), (220, BLUE, "3 4"), (-220, BLUE, "3 4")):
    b += f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x1}" y2="{Y(v):.1f}" stroke="{col}" stroke-width="1.6" stroke-dasharray="{dash}"/>'
b += f'<line x1="{x0}" y1="{yc}" x2="{x1+10}" y2="{yc}" stroke="currentColor" stroke-width="1.5" opacity=".6"/>'
b += chevron(x1 + 12, yc, 1, 0, "currentColor", 1.5, 9)
b += text(x1 + 6, yc - 10, "t (ms)", "currentColor", 14, "start", "700")
b += text(14, 22, "u", "currentColor", 16, "start", "700")
pts = " ".join(f"{x0 + ms*t/2:.1f},{Y(311*math.cos(2*math.pi*(t/2)/20)):.1f}" for t in range(0, 81))
b += f'<polyline points="{pts}" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linejoin="round"/>'
for t in (5, 15, 25, 35):
    b += f'<circle cx="{x0+ms*t:.1f}" cy="{yc}" r="5" fill="{GRN}"/>'
for t in (0, 10, 20, 30, 40):
    b += text(round(x0 + ms * t), yc + 22, str(t), "currentColor", 14, "middle", "600")
b += text(round(x0 + ms * 10), round(Y(311)) - 12, sub("U", "0") + "= 311 V", RED, 14, "middle", "700")
b += text(round(x0 + ms * 10), round(Y(220)) - 7, "U = 220 V", BLUE, 14, "middle", "700")
xa, xb = x0, x0 + ms * 20
yb = 274
b += f'<line x1="{xa}" y1="{yb}" x2="{xb:.1f}" y2="{yb}" stroke="{ORG}" stroke-width="2.4"/>'
b += f'<line x1="{xa}" y1="{yb-6}" x2="{xa}" y2="{yb+6}" stroke="{ORG}" stroke-width="2.4"/><line x1="{xb:.1f}" y1="{yb-6}" x2="{xb:.1f}" y2="{yb+6}" stroke="{ORG}" stroke-width="2.4"/>'
b += text(round(xb) + 10, yb + 5, "T = 20 ms", ORG, 14, "start", "700")
b += f'<line x1="14" y1="300" x2="40" y2="300" stroke="{RED}" stroke-width="1.8" stroke-dasharray="6 4"/>' + text(46, 305, "đỉnh (cực đại)", RED, 14)
b += f'<line x1="200" y1="300" x2="226" y2="300" stroke="{BLUE}" stroke-width="1.8" stroke-dasharray="3 4"/>' + text(232, 305, "hiệu dụng", BLUE, 14)
fig3 = wrap("0 0 430 316", "Đồ thị điện áp lưới 220 V 50 Hz: đỉnh 311 V, hiệu dụng 220 V, chu kì 20 mili giây",
            b, "Hình 3. Điện áp ổ điện nhà em. Chấm xanh: lúc dòng đổi chiều, 2 lần mỗi chu kì, tức 100 lần mỗi giây.",
            exp="tn-l12-xoaychieu-03")

# ---- Hình 2 (mới): ảnh OpenStax Hình 23.21 (vành trượt + chổi than + đồ thị e theo t), chèn trực tiếp, không vẽ lại
fig4 = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l12-dong-dien-xoay-chieu/hinh-may-phat-vanh-truot-choi-than.webp" '
        'alt="Máy phát điện xoay chiều: khung dây quay giữa hai cực N và S, hai vành trượt có hai chổi than nối với bóng đèn; bên phải là đồ thị suất điện động hình sin theo thời gian" '
        'loading="lazy" width="1000" height="554"><figcaption>Hình 2. Lấy điện ra khỏi khung quay.<br>'
        'Hai đầu khung nối hai vành trượt quay cùng trục; hai chổi than tì lên vành và nối với bóng đèn.<br>'
        'Suất điện động có dạng hình sin, chu kì T = 2π/ω.<br>'
        'Nhãn: Brushes = chổi than; ω = tốc độ góc; ℰ = suất điện động; ℰ₀ = suất điện động cực đại; T = chu kì; t = thời gian.<br>'
        '<small>Hình: OpenStax, College Physics 2e, Hình 23.21 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>')

src = (HERE / "theory.src.html").read_text(encoding="utf-8")
for n, f in ((1, fig1), (2, fig2), (3, fig3), (4, fig4)):
    assert f"<!--FIG:{n}-->" in src, n
    src = src.replace(f"<!--FIG:{n}-->", f)
(HERE / "theory.html").write_text(margin_figs(src), encoding="utf-8")
print("ok", len(src))
