"""Sinh 5 hình SVG và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được)."""
import math, re
from svg_lib import *

def poly(pts, c, w=2, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline fill="none" stroke="{c}" stroke-width="{w}"{d} points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>'

def dot(x, y, r=5, c="currentColor"): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'

# ---- Hình 1: hai loa, đi dọc nghe to nhỏ
b = ""
for x in (150, 290):
    b += f'<rect x="{x-12}" y="22" width="24" height="34" rx="3" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2"/>'
    b += f'<circle cx="{x}" cy="42" r="7" fill="none" stroke="currentColor" stroke-width="2"/>'
    for r in (40, 70, 100, 130, 160):
        b += f'<path d="M{x-r*.7:.0f},{56+r*.7:.0f} A{r},{r} 0 0 0 {x+r*.7:.0f},{56+r*.7:.0f}" fill="none" stroke="{BLUE}" stroke-width="1" opacity=".35"/>'
b += text(150, 18, "Loa 1", "currentColor", 12, "middle") + text(290, 18, "Loa 2", "currentColor", 12, "middle")
b += line(14, 188, 426, 188, "currentColor", 2, "", .6) + text(426, 208, "đường em đi", "currentColor", 11, "end", "400")
for x, lab in ((220, "TO"), (100, "TO"), (340, "TO")):
    b += dot(x, 188, 7, RED) + text(x, 172, lab, RED, 13, "middle", "700")
for x in (160, 280, 40, 400):
    b += dot(x, 188, 7, BLUE) + text(x, 172, "nhỏ", BLUE, 12, "middle", "700")
fig1 = wrap("0 0 440 215", "Hai loa phát cùng một âm: đi dọc trước hai loa nghe to rồi nhỏ xen kẽ",
            b, "Hình 1. Hai loa cùng phát một âm. Đi dọc đường, tiếng <strong>to – nhỏ xen kẽ</strong> và các vị trí đó cố định.")

# ---- Hình 2: vân giao thoa hypebol (AB = 4λ)
lam, c, cx, cy = 36, 72, 220, 125
b = ""
def hyp(a, sign, col, dash):
    bb = math.sqrt(c * c - a * a)
    pts = [(cx + sign * a * math.sqrt(1 + (y / bb) ** 2), cy + y) for y in range(-105, 106, 5)]
    return poly(pts, col, 2.2, dash)
b += line(cx, cy - 105, cx, cy + 105, RED, 2.4)
for k in (1, 2, 3):
    for s in (-1, 1): b += hyp(k * lam / 2, s, RED, "")
for k in range(4):
    for s in (-1, 1): b += hyp((k + .5) * lam / 2, s, BLUE, "6 4")
b += line(cx - c, cy, cx + c, cy, "currentColor", 1.2, "2 3", .5)
b += dot(cx - c, cy, 6, ORG) + dot(cx + c, cy, 6, ORG)
b += text(cx - c - 16, cy + 5, "A", "currentColor", 14, "middle", "700") + text(cx + c + 16, cy + 5, "B", "currentColor", 14, "middle", "700")
b += text(cx, 14, "k = 0", RED, 12, "middle", "700")
for k, xx in ((1, cx + 18), (2, cx + 36), (3, cx + 54)):
    pass
b += text(14, 255, "━ cực đại (đỏ)", RED, 12, "start") + text(150, 255, "┅ cực tiểu (xanh)", BLUE, 12, "start") + text(300, 255, "● hai nguồn A, B", ORG, 12, "start")
fig2 = wrap("0 0 440 266", "Hai nguồn cùng pha A, B: các đường cực đại (đỏ, liền) và cực tiểu (xanh, đứt) xen kẽ dạng hypebol",
            b, "Hình 2. AB = 4λ: có 7 đường cực đại và 8 đường cực tiểu. Đường trung trực của AB là cực đại k = 0.")

# ---------------- Hình 3: ảnh OpenStax College Physics 2e, Hình 27.11 (28/10/2026) — thay SVG tự vẽ
fig3 = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l11-giao-thoa-song/hinh-cung-pha-nguoc-pha.webp" '
        'alt="Hai sóng cộng lại: (a) cùng pha thì sóng tổng có biên độ 2X; (b) ngược pha thì sóng tổng bằng 0" loading="lazy" width="750" height="1025">'
        '<figcaption>Hình 3. Hai sóng cộng lại thành sóng tổng.<br>(a) Cùng pha: biên độ gấp đôi.<br>(b) Ngược pha: triệt tiêu.<br>Nhãn: Wave = sóng · Resultant = sóng tổng.<br><small>Hình: OpenStax, College Physics 2e, Hình 27.11 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>')

# ---- Hình 4: khe Young
b = defs("f4")
b += line(130, 20, 130, 90, "currentColor", 4) + line(130, 100, 130, 130, "currentColor", 4) + line(130, 140, 130, 200, "currentColor", 4)
b += text(130, 14, "hai khe", "currentColor", 12, "middle")
b += dot(40, 115, 5, ORG) + text(40, 138, "nguồn", ORG, 12, "middle") + line(45, 115, 126, 95, ORG, 1.3, "", .6) + line(45, 115, 126, 135, ORG, 1.3, "", .6)
b += line(130, 95, 380, 115, "currentColor", 1, "3 3", .5) + line(130, 135, 380, 115, "currentColor", 1, "3 3", .5)
b += line(380, 12, 380, 218, "currentColor", 3)
i = 24
for k in range(-4, 5):
    y = 115 + k * i
    b += f'<rect x="372" y="{y-6}" width="16" height="12" rx="2" fill="{ORG}" opacity="{1 if k==0 else .85}"/>'
b += text(396, 119, "k = 0", ORG, 11, "start", "700") + text(396, 119 + i, "k = 1", ORG, 11, "start", "700") + text(396, 119 - i, "k = −1", ORG, 11, "start", "700")
b += line(364, 115, 364, 115 + i, "currentColor", 1.5) + text(358, 132, "i", "currentColor", 13, "end", "700")
b += arrow("f4", "g", 130, 208, 376, 208, 2) + text(250, 204, "D", GRN, 13, "middle", "700")
b += text(112, 118, "a", "currentColor", 13, "end", "700")
b += line(120, 95, 120, 135, "currentColor", 1.5)
fig4 = wrap("0 0 440 222", "Sơ đồ khe Young: hai khe cách nhau a, màn cách khe D, khoảng vân i",
            b, "Hình 4. a: khoảng cách hai khe; D: từ khe đến màn; i: khoảng cách hai vân sáng liên tiếp (cam: vân sáng).")

# ---- Hình 5: đếm cực trị trên AB (AB = 10 cm, λ = 1,5 cm)
x0, x1 = 20, 420
mid, step = 220, 30
b = line(x0, 70, x1, 70, "currentColor", 2.5)
b += dot(x0, 70, 6, ORG) + dot(x1, 70, 6, ORG) + text(x0, 118, "A", "currentColor", 14, "middle", "700") + text(x1, 118, "B", "currentColor", 14, "middle", "700")
for k in range(-6, 7):
    x = mid + k * step
    b += line(x, 40, x, 70, RED, 3)
for k in range(-7, 7):
    x = mid + (2 * k + 1) * step / 2
    b += line(x, 70, x, 98, BLUE, 3)
b += text(mid, 30, "k = 0", RED, 11, "middle", "700") + text(mid + 6 * step, 30, "k = 6", RED, 11, "middle", "700") + text(mid - 6 * step, 30, "k = −6", RED, 11, "middle", "700")
b += line(mid, 112, mid + step, 112, GRN, 2) + text(mid + step / 2, 130, "λ/2", GRN, 11, "middle", "700")
b += text(14, 148, "▌ 13 cực đại", RED, 12, "start") + text(160, 148, "▌ 14 cực tiểu", BLUE, 12, "start")
fig5 = wrap("0 0 440 160", "Trên đoạn AB = 10 cm, λ = 1,5 cm có 13 cực đại (đỏ) và 14 cực tiểu (xanh)",
            b, "Hình 5. Cực đại (đỏ) và cực tiểu (xanh) cách đều nhau λ/4; hai cực đại liên tiếp cách λ/2.")

h = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4, fig5), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(h)
print("ok", len(h))
