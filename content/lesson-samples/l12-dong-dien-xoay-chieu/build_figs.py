"""Chèn 3 hình SVG tự vẽ vào theory.src.html -> theory.html (idempotent).
Chạy từ thư mục này:  python3 build_figs.py"""
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

# ---- Hình 1: khung quay, nhìn dọc trục
b = defs("f1")
for y in (48, 88, 128, 168):
    b += field_line(14, y, 410, y, RED, 1.9)
b += text(16, 38, "đường sức, vectơ B", RED, 12)
cx, cy, a = 250, 108, math.radians(40)
nx, ny = math.cos(a), -math.sin(a)
dx, dy = -ny, nx
L = 66
b += f'<line x1="{cx-dx*L:.0f}" y1="{cy-dy*L:.0f}" x2="{cx+dx*L:.0f}" y2="{cy+dy*L:.0f}" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>'
b += f'<circle cx="{cx}" cy="{cy}" r="4" fill="currentColor"/>'
b += arrow("f1", "o", cx, cy, round(cx + nx * 72), round(cy + ny * 72), 3)
b += text(round(cx + nx * 72) + 6, round(cy + ny * 72) - 6, "n", ORG, 15, "start", "700")
b += f'<path d="M{cx+34} {cy} A34 34 0 0 0 {cx+34*nx:.0f} {cy+34*ny:.0f}" fill="none" stroke="{GRN}" stroke-width="2.2"/>'
b += text(cx + 40, cy - 8, "α", GRN, 15, "start", "700")
# mũi tên quay (ngược chiều kim đồng hồ) phía trên khung
R = 92
t0, t1 = math.radians(72), math.radians(118)
x0, y0 = cx + R * math.cos(t0), cy - R * math.sin(t0)
x1, y1 = cx + R * math.cos(t1), cy - R * math.sin(t1)
b += f'<path d="M{x0:.0f} {y0:.0f} A{R} {R} 0 0 0 {x1:.0f} {y1:.0f}" fill="none" stroke="{GRN}" stroke-width="2.6" marker-end="url(#f1-g)"/>'
b += text(round(x0) + 10, round(y0) + 6, "ω", GRN, 16, "start", "700")
b += text(16, 206, "Chấm tròn ở tâm khung: trục quay O (vuông góc trang)", "currentColor", 12)
b += text(16, 226, "α = ωt + φ  →  Φ = NBS·cos α", "currentColor", 14, "start", "700")
fig1 = wrap("0 0 430 238", "Khung dây quay đều quanh trục O trong từ trường đều, pháp tuyến n hợp với B góc alpha tăng dần",
            b, "Hình 1. Nhìn dọc trục quay: khung quay đều nên góc α tăng đều theo thời gian, và Φ = NBS·cos α dao động tuần hoàn.",
            exp="tn-l12-xoaychieu-01")

# ---- Hình 2: Φ và e vuông pha
b = defs("f2")
x0, x1, yc, A = 40, 410, 105, 58
W = x1 - x0
b += f'<line x1="{x0}" y1="{yc}" x2="{x1+8}" y2="{yc}" stroke="currentColor" stroke-width="1.5" opacity=".6"/>'
b += text(x1 + 12, yc + 4, "t", "currentColor", 13, "start", "700")
def curve(fn, col):
    pts = " ".join(f"{x0 + W*k/100:.1f},{yc - A*fn(2*math.pi*k/100):.1f}" for k in range(101))
    return f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.8" stroke-linejoin="round"/>'
b += curve(math.cos, BLUE) + curve(math.sin, RED)
for k, lab in ((0, "0"), (25, "T/4"), (50, "T/2"), (75, "3T/4"), (100, "T")):
    x = x0 + W * k / 100
    b += f'<line x1="{x:.0f}" y1="{yc-4}" x2="{x:.0f}" y2="{yc+4}" stroke="currentColor" stroke-width="1.5"/>'
    if k not in (0, 100):
        b += text(round(x), yc + 18, lab, "currentColor", 11, "middle", "500")
b += text(x0, yc + 18, "0", "currentColor", 11, "middle", "500")
b += text(x1, yc + 18, "T", "currentColor", 11, "middle", "500")
xq = x0 + W / 4
b += f'<line x1="{x0}" y1="30" x2="{x0}" y2="170" stroke="currentColor" stroke-width="1" stroke-dasharray="4 4" opacity=".5"/>'
b += f'<line x1="{xq:.0f}" y1="30" x2="{xq:.0f}" y2="170" stroke="currentColor" stroke-width="1" stroke-dasharray="4 4" opacity=".5"/>'
b += f'<circle cx="{x0}" cy="{yc-A}" r="4.5" fill="{BLUE}"/><circle cx="{x0}" cy="{yc}" r="4.5" fill="{RED}"/>'
b += f'<circle cx="{xq:.0f}" cy="{yc-A}" r="4.5" fill="{RED}"/><circle cx="{xq:.0f}" cy="{yc}" r="4.5" fill="{BLUE}"/>'
b += text(x0 + 6, 20, "Φ đỉnh · e = 0", "currentColor", 12, "start", "700")
b += text(round(xq) + 8, 20, "e đỉnh · Φ = 0", "currentColor", 12, "start", "700")
b += f'<line x1="40" y1="196" x2="68" y2="196" stroke="{BLUE}" stroke-width="3"/>' + text(74, 200, "Φ (từ thông)", BLUE, 12)
b += f'<line x1="190" y1="196" x2="218" y2="196" stroke="{RED}" stroke-width="3"/>' + text(224, 200, "e (suất điện động)", RED, 12)
fig2 = wrap("0 0 430 212", "Đồ thị từ thông Φ và suất điện động e theo thời gian, lệch nhau một phần tư chu kì",
            b, "Hình 4. Φ và e lệch nhau T/4 (vuông pha): cái này ở đỉnh thì cái kia đi qua 0.",
            exp="tn-l12-xoaychieu-01")

# ---- Hình 3: u(t), đỉnh 311 V, hiệu dụng 220 V, T = 20 ms
b = defs("f3")
x0, x1, yc = 50, 400, 125
S = 0.34  # px / V
ms = (x1 - x0) / 40
def Y(v): return yc - v * S
for v, col, dash in ((311, RED, "6 4"), (-311, RED, "6 4"), (220, BLUE, "3 4"), (-220, BLUE, "3 4")):
    b += f'<line x1="{x0}" y1="{Y(v):.0f}" x2="{x1}" y2="{Y(v):.0f}" stroke="{col}" stroke-width="1.6" stroke-dasharray="{dash}"/>'
b += f'<line x1="{x0}" y1="{yc}" x2="{x1+6}" y2="{yc}" stroke="currentColor" stroke-width="1.5" opacity=".6"/>'
pts = " ".join(f"{x0 + ms*t/2:.1f},{Y(311*math.cos(2*math.pi*(t/2)/20)):.1f}" for t in range(0, 81))
b += f'<polyline points="{pts}" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linejoin="round"/>'
for t in (5, 15, 25, 35):
    b += f'<circle cx="{x0+ms*t:.0f}" cy="{yc}" r="4.5" fill="{GRN}"/>'
for t in (0, 10, 20, 30, 40):
    b += text(round(x0 + ms * t), yc + 16, str(t) + (" ms" if t == 40 else ""), "currentColor", 11, "middle", "500")
b += text(round(x0 + ms * 10), 13, "U₀ = 311 V (đỉnh)", RED, 12, "middle", "700")
b += text(round(x0 + ms * 10), 44, "U = 220 V hiệu dụng", BLUE, 11, "middle", "700")
xa, xb = x0, x0 + ms * 20
b += f'<line x1="{xa}" y1="252" x2="{xb:.0f}" y2="252" stroke="{ORG}" stroke-width="2.4"/>'
b += f'<line x1="{xa}" y1="246" x2="{xa}" y2="258" stroke="{ORG}" stroke-width="2.4"/><line x1="{xb:.0f}" y1="246" x2="{xb:.0f}" y2="258" stroke="{ORG}" stroke-width="2.4"/>'
b += text(round((xa + xb) / 2), 244, "T = 20 ms", ORG, 12, "middle", "700")
fig3 = wrap("0 0 430 266", "Đồ thị điện áp lưới 220 V 50 Hz: đỉnh 311 V, hiệu dụng 220 V, chu kì 20 mili giây",
            b, "Hình 3. Điện áp ổ điện nhà em. Chấm xanh: lúc dòng đổi chiều, 2 lần mỗi chu kì, tức 100 lần mỗi giây.",
            exp="tn-l12-xoaychieu-03")

# ---- Hình 2 (mới): lấy điện ra khỏi khung quay bằng vành trượt + chổi than (vẽ lại theo OpenStax Hình 23.19)
b = defs("f4")
for x, lab in ((20, "N"), (340, "S")):
    b += f'<rect x="{x}" y="110" width="70" height="110" rx="4" fill="currentColor" fill-opacity=".12" stroke="currentColor" stroke-width="2"/>'
    b += text(x + 35, 172, lab, "currentColor", 22, "middle", "700")
for y in (140, 160, 180, 200):
    b += field_line(92, y, 338, y, RED, 1.8)
b += text(96, 130, "vectơ B", RED, 14, "start", "700")
b += f'<rect x="150" y="120" width="130" height="100" fill="none" stroke="{ORG}" stroke-width="3.2" stroke-linejoin="round"/>'
b += f'<line x1="215" y1="100" x2="215" y2="250" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>'
b += f'<line x1="209" y1="88" x2="209" y2="120" stroke="{ORG}" stroke-width="2.4"/><line x1="221" y1="62" x2="221" y2="120" stroke="{ORG}" stroke-width="2.4"/>'
for y in (62, 88):
    b += f'<ellipse cx="215" cy="{y}" rx="14" ry="5" fill="none" stroke="currentColor" stroke-width="2.2"/>'
b += f'<rect x="188" y="83" width="16" height="10" fill="{BLUE}" stroke="{BLUE}" stroke-width="1"/><rect x="226" y="57" width="16" height="10" fill="{BLUE}" stroke="{BLUE}" stroke-width="1"/>'
b += f'<polyline points="188,88 150,88 150,21 172,21" fill="none" stroke="{BLUE}" stroke-width="2.2"/>'
b += f'<polyline points="242,62 280,62 280,21 258,21" fill="none" stroke="{BLUE}" stroke-width="2.2"/>'
b += f'<rect x="172" y="8" width="86" height="26" rx="4" fill="none" stroke="currentColor" stroke-width="2"/>' + text(215, 26, "tải", "currentColor", 13, "middle", "700")
b += text(142, 76, "vành trượt", "currentColor", 14, "end", "600")
b += text(290, 80, "chổi than", BLUE, 14, "start", "700")
b += text(292, 242, "khung dây", ORG, 14, "start", "700")
b += text(205, 270, "trục quay", "currentColor", 14, "end", "600")
b += f'<path d="M232 262 Q262 282 292 262" fill="none" stroke="{GRN}" stroke-width="2.6" marker-end="url(#f4-g)"/>'
b += text(246, 292, "ω", GRN, 16, "start", "700")
fig4 = wrap("0 0 430 300", "Máy phát điện xoay chiều: khung dây quay giữa hai cực nam châm, hai vành trượt và hai chổi than đưa dòng ra tải",
            b, "Hình 2. Lấy điện ra khỏi khung quay.<br>Hai đầu khung nối hai vành trượt, quay cùng trục.<br>Hai chổi than (màu xanh) tì lên vành, nối với tải.<br>"
               "Vẽ lại theo OpenStax, College Physics 2e, Hình 23.19 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e")

src = (HERE / "theory.src.html").read_text(encoding="utf-8")
for n, f in ((1, fig1), (2, fig2), (3, fig3), (4, fig4)):
    assert f"<!--FIG:{n}-->" in src, n
    src = src.replace(f"<!--FIG:{n}-->", f)
(HERE / "theory.html").write_text(src, encoding="utf-8")
print("ok", len(src))
