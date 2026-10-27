"""Chèn hình 1 (SVG tự vẽ) + hình 2, 3 (ảnh OpenStax) vào theory.html (idempotent). Chạy từ thư mục này:
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
    b += field_line(20, y, 400, y, RED, 1.9)
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

# ---- Hình 2 và 3: ảnh OpenStax College Physics 2e (CC BY-NC-SA 4.0), chèn trực tiếp (webp trong public/assets/openstax/)
OSX = "Hình: OpenStax, College Physics 2e, Hình {n} — CC BY\u2011NC\u2011SA 4.0 — openstax.org/books/college-physics-2e"
fig2 = ('<figure class="fig" data-tl="1" data-exp="tn-l12-camungdt-01"><img src="/assets/openstax/l12-cam-ung-dien-tu/hinh-2.webp" '
        'alt="Thanh nam châm đưa vào rồi kéo ra khỏi cuộn dây nối điện kế, kim điện kế lệch ngược chiều nhau" loading="lazy" width="420" height="372">'
        '<figcaption>Hình 2. Nam châm vào (a), ra (b): kim lệch ngược nhau.<br>'
        'Galvanometer: điện kế · Coil: cuộn dây · I: dòng cảm ứng<br>'
        + OSX.format(n="23.4 (hai phần a, b)") + '</figcaption></figure>')

# ---- Hình 3: định luật Lenz, cực Bắc tiến lại, vòng dây sinh cực Bắc đẩy ra
b = defs("f3")
b += '<rect x="24" y="114" width="50" height="32" fill="rgba(56,189,248,.25)" stroke="currentColor" stroke-width="2"/>'
b += '<rect x="74" y="114" width="50" height="32" fill="rgba(248,113,113,.25)" stroke="currentColor" stroke-width="2"/>'
b += text(49, 136, "S", BLUE, 15, "middle", "700") + text(99, 136, "N", RED, 15, "middle", "700")
b += arrow("f3", "g", 30, 90, 110, 90, 3) + text(30, 80, "nam châm tiến lại", GRN, 14)
b += '<ellipse cx="300" cy="130" rx="16" ry="50" fill="none" stroke="currentColor" stroke-width="3"/>'
b += text(300, 204, "vòng dây kín", "currentColor", 14, "middle")
b += arrow("f3", "b", 288, 130, 205, 130, 3)
b += text(206, 116, "B", BLUE, 14, "start", "700").replace("</text>", '<tspan dy="4" font-size="12">cảm ứng</tspan></text>')
b += text(272, 158, "đầu gần = cực Bắc", BLUE, 14, "end")
b += arrow("f3", "r", 76, 168, 26, 168, 3)
b += text(24, 190, "lực đẩy cản lại", RED, 14)
b += field_line(150, 52, 395, 52, RED, 1.9)
b += text(402, 57, "B", RED, 14, "start", "700")
b += text(150, 38, "từ trường nam châm", RED, 14)
b += arrow("f3", "o", 316, 142, 316, 118, 3)
b += text(326, 134, "i", ORG, 15, "start", "700")
b += text(326, 154, "dòng cảm ứng", ORG, 14)
b += text(430, 228, "nhìn từ phía nam châm: ngược chiều kim đồng hồ", ORG, 14, "end")
b += text(24, 254, "Từ thông tăng → từ trường cảm ứng ngược chiều", "currentColor", 14, "start", "400")
b += text(24, 274, "→ cản sự tăng của từ thông", "currentColor", 14, "start", "400")
fig3 = wrap("0 0 440 285", "Định luật Lenz: nam châm tiến lại gần, vòng dây tạo cực cùng tên để đẩy ra; dòng cảm ứng nhìn từ phía nam châm ngược chiều kim đồng hồ",
            b, "Hình 3. Từ thông tăng nên vòng dây tạo cực Bắc ở đầu gần: hai cực cùng tên <em>đẩy</em> nhau, cản nam châm tiến vào.<br>Vẽ lại theo OpenStax, College Physics 2e, Hình 23.7 — CC BY\u2011NC\u2011SA 4.0 — openstax.org/books/college-physics-2e")

src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
