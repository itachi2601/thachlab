"""Chèn 3 hình SVG tự vẽ vào theory.html (idempotent). Chạy từ thư mục này:
python3 build_figs.py"""
import math, re, sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *

def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')

# ---- Hình 1: từ thông, pháp tuyến, góc alpha (nhìn cạnh khung)
b = defs("f1")
for y in (60, 110, 160):
    b += f'<line x1="20" y1="{y}" x2="400" y2="{y}" stroke="{RED}" stroke-width="1.8" opacity=".75" marker-end="url(#f1-r)"/>'
b += text(24, 50, "đường sức, vectơ B", RED, 12)
cx, cy, a = 270, 110, math.radians(40)
nx, ny = math.cos(a), -math.sin(a)
dx, dy = -ny, nx  # hướng dọc mặt khung (vuông góc n)
L = 70
b += f'<line x1="{cx-dx*L:.0f}" y1="{cy-dy*L:.0f}" x2="{cx+dx*L:.0f}" y2="{cy+dy*L:.0f}" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>'
b += arrow("f1", "o", cx, cy, round(cx + nx * 75), round(cy + ny * 75), 3)
b += text(round(cx + nx * 75) + 6, round(cy + ny * 75) - 8, "n", ORG, 15, "start", "700")
b += f'<path d="M{cx+36} {cy} A36 36 0 0 0 {cx+36*nx:.0f} {cy+36*ny:.0f}" fill="none" stroke="{GRN}" stroke-width="2.2"/>'
b += text(cx + 42, cy - 8, "α", GRN, 15, "start", "700")
b += text(20, 205, "Mặt khung (nhìn cạnh)", "currentColor", 12)
b += text(20, 222, "Φ = B·S·cos α", "currentColor", 14, "start", "700")
fig1 = wrap("0 0 420 235", "Khung dây đặt trong từ trường đều, pháp tuyến n hợp với B góc alpha",
            b, "Hình 1. Số đường sức xuyên qua khung giảm khi pháp tuyến <strong>n</strong> nghiêng khỏi <strong>B</strong> (α tăng). α là góc của pháp tuyến, không phải của mặt khung.", exp="tn-l12-camungdt-03")

# ---- Hình 2: nam châm, cuộn dây, điện kế
b = defs("f2")
b += '<rect x="30" y="85" width="50" height="32" fill="rgba(56,189,248,.25)" stroke="currentColor" stroke-width="2"/>'
b += '<rect x="80" y="85" width="50" height="32" fill="rgba(248,113,113,.25)" stroke="currentColor" stroke-width="2"/>'
b += text(55, 107, "S", BLUE, 15, "middle", "700") + text(105, 107, "N", RED, 15, "middle", "700")
b += arrow("f2", "g", 40, 148, 130, 148, 3) + text(40, 170, "v: đưa vào cuộn dây", GRN, 12)
for x in (240, 256, 272):
    b += f'<ellipse cx="{x}" cy="101" rx="13" ry="38" fill="none" stroke="currentColor" stroke-width="2.5"/>'
b += text(222, 194, "Cuộn dây", "currentColor", 12)
b += '<path d="M240 139 V150 H336" fill="none" stroke="currentColor" stroke-width="2"/>'
b += '<path d="M272 63 V28 H360 V126" fill="none" stroke="currentColor" stroke-width="2"/>'
b += '<circle cx="360" cy="150" r="24" fill="rgba(148,163,184,.18)" stroke="currentColor" stroke-width="2"/>'
b += text(360, 156, "G", "currentColor", 16, "middle", "700")
b += f'<line x1="360" y1="150" x2="373" y2="131" stroke="{GRN}" stroke-width="2.5"/>'
b += text(360, 194, "Điện kế: kim lệch", GRN, 12, "middle")
fig2 = wrap("0 0 430 205", "Đưa nam châm vào cuộn dây nối điện kế, kim điện kế lệch",
            b, "Hình 2. Nam châm <em>đang chuyển động</em> thì kim lệch; đứng yên thì kim về 0; rút ra thì kim lệch ngược lại.", exp="tn-l12-camungdt-01")

# ---- Hình 3: định luật Lenz, cực Bắc tiến lại, vòng dây sinh cực Bắc đẩy ra
b = defs("f3")
b += '<rect x="24" y="85" width="50" height="32" fill="rgba(56,189,248,.25)" stroke="currentColor" stroke-width="2"/>'
b += '<rect x="74" y="85" width="50" height="32" fill="rgba(248,113,113,.25)" stroke="currentColor" stroke-width="2"/>'
b += text(49, 107, "S", BLUE, 15, "middle", "700") + text(99, 107, "N", RED, 15, "middle", "700")
b += arrow("f3", "g", 30, 60, 110, 60, 3) + text(30, 50, "nam châm tiến lại", GRN, 12)
b += '<ellipse cx="300" cy="101" rx="16" ry="48" fill="none" stroke="currentColor" stroke-width="3"/>'
b += text(300, 168, "vòng dây kín", "currentColor", 12, "middle")
b += arrow("f3", "b", 292, 101, 215, 101, 3)
b += text(278, 124, "đầu gần = cực Bắc", BLUE, 12, "end")
b += text(222, 90, "B", BLUE, 14, "start", "700").replace("</text>", '<tspan dy="4" font-size="9">cảm ứng</tspan></text>')
b += arrow("f3", "r", 76, 134, 26, 134, 3)
b += text(24, 156, "lực đẩy cản lại", RED, 12)
b += text(24, 192, "Từ thông tăng → từ trường cảm ứng ngược chiều → cản sự tăng", "currentColor", 12, "start", "400")
fig3 = wrap("0 0 430 205", "Định luật Lenz: nam châm tiến lại gần, vòng dây tạo cực cùng tên để đẩy ra",
            b, "Hình 3. Từ thông tăng nên vòng dây tạo cực Bắc ở đầu gần: hai cực cùng tên <em>đẩy</em> nhau, cản nam châm tiến vào.")

src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
