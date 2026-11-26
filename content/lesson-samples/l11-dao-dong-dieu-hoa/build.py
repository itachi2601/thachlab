"""Sinh theory.html (chèn 3 hình SVG vào theory.src.html), 3 mục kho thí nghiệm và bundle.json.
Chạy từ thư mục này: python3 build.py"""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import math, json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *

def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')

# ---- Hình 1: con lắc lò xo, VTCB và hai biên
# 31/10/2026: bỏ marker-end tam giác (trục x dùng chevron V 30°), chữ ≥ 14, tách chữ "dao động qua lại" khỏi
# hai mũi tên, thêm mặt sàn nằm ngang dưới vật (vật không lơ lửng).
b = ""
O, A, y = 230, 100, 100
b += f'<line x1="22" y1="55" x2="22" y2="124" stroke="currentColor" stroke-width="4"/>'
for yy in range(60, 120, 12):
    b += f'<line x1="22" y1="{yy}" x2="12" y2="{yy+8}" stroke="currentColor" stroke-width="1.5" opacity=".5"/>'
b += f'<line x1="22" y1="{y+21}" x2="380" y2="{y+21}" stroke="currentColor" stroke-width="2"/>'
for xx in range(34, 380, 16):
    b += f'<line x1="{xx}" y1="{y+21}" x2="{xx-8}" y2="{y+29}" stroke="currentColor" stroke-width="1.2" opacity=".4"/>'
pts = [(22, y)]
x0, x1 = 22, O - 20
n = 10
for i in range(n):
    pts.append((x0 + (x1 - x0) * (i + .5) / n, y + (-14 if i % 2 == 0 else 14)))
pts.append((x1, y))
b += '<polyline points="' + " ".join(f"{px:.0f},{py:.0f}" for px, py in pts) + '" fill="none" stroke="currentColor" stroke-width="2"/>'
b += f'<rect x="{O-20}" y="{y-20}" width="40" height="40" rx="4" fill="rgba(148,163,184,.3)" stroke="currentColor" stroke-width="2.5"/>'
for px in (O - A, O + A):
    b += f'<rect x="{px-20}" y="{y-20}" width="40" height="40" rx="4" fill="none" stroke="{ORG}" stroke-width="2" stroke-dasharray="5,4"/>'
b += f'<line x1="20" y1="152" x2="410" y2="152" stroke="currentColor" stroke-width="1.6"/>' + chevron(410, 152, 1, 0, "currentColor", 1.6, 10)
for px, s in ((O - A, "−A"), (O, "O"), (O + A, "+A")):
    b += f'<line x1="{px}" y1="{y+30}" x2="{px}" y2="156" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3,3" opacity=".5"/>'
    b += text(px, 176, s, ORG if s != "O" else "currentColor", 15, "middle", "700")
b += text(408, 176, "x", "currentColor", 15, "end", "700")
b += arrow("f1", "g", O - 26, 62, O - A + 4, 62, 2.5) + arrow("f1", "g", O + 26, 62, O + A - 4, 62, 2.5)
b += text(O, 36, "dao động qua lại", GRN, 15, "middle")
b += text(O, 204, "O là vị trí cân bằng", "currentColor", 14, "middle", "500")
FIG1 = wrap("0 0 440 215", "Con lắc lò xo dao động qua lại quanh vị trí cân bằng O giữa hai biên −A và +A", b,
            "Hình 1. Con lắc lò xo: vật dao động quanh vị trí cân bằng O, giữa hai biên −A và +A.", "tn-l11-daodongdieuhoa-01")

# ---- Hình 2, 3 (26/11/2026): vẽ lại theo OpenStax College Physics 2e Hình 16.11 và 16.18, nhãn tiếng Việt (H3, N8)
# Hình 2: giấy chạy sang TRÁI qua đầu bút → nét cũ nằm bên trái, trục t hướng về bút (đọc trái → phải đúng chiều thời gian).
SRC_OS = "openstax.org/books/college-physics-2e"
b = ""
y0, Ap, xs, Tp, xpen = 150, 50, 56, 88, 284
b += f'<rect x="16" y="62" width="284" height="160" rx="3" fill="rgba(148,163,184,.12)" stroke="currentColor" stroke-width="1.5" opacity=".7"/>'
b += f'<line x1="48" y1="214" x2="48" y2="76" stroke="currentColor" stroke-width="1.6"/>' + chevron(48, 74, 0, -1, "currentColor", 1.6, 9)
b += f'<line x1="48" y1="{y0}" x2="268" y2="{y0}" stroke="currentColor" stroke-width="1.6"/>' + chevron(270, y0, 1, 0, "currentColor", 1.6, 9)
b += text(36, 84, "x", "currentColor", 15, "end", "700") + text(275, 143, "t", "currentColor", 15, "start", "700")
for yy, s in ((y0 - Ap, "A"), (y0, "O"), (y0 + Ap, "−A")):
    b += f'<line x1="44" y1="{yy}" x2="52" y2="{yy}" stroke="currentColor" stroke-width="1.6"/>' + text(39, yy + 5, s, "currentColor", 14, "end", "700")
pts = [(x, y0 - Ap * math.cos(2 * math.pi * (x - xs) / Tp)) for x in range(xs, xpen + 1, 2)]
b += '<polyline points="' + " ".join(f"{px},{py:.1f}" for px, py in pts) + f'" fill="none" stroke="{BLUE}" stroke-width="2.4"/>'
ypen = pts[-1][1]
# chu kì T giữa hai đỉnh liên tiếp
for xx in (xs + Tp, xs + 2 * Tp):
    b += f'<line x1="{xx}" y1="{y0-Ap-4}" x2="{xx}" y2="{y0-Ap-20}" stroke="{ORG}" stroke-width="1.4"/>'
b += f'<line x1="{xs+Tp+2}" y1="{y0-Ap-12}" x2="{xs+2*Tp-2}" y2="{y0-Ap-12}" stroke="{ORG}" stroke-width="1.6"/>'
b += chevron(xs + Tp + 1, y0 - Ap - 12, -1, 0, ORG, 1.6, 7) + chevron(xs + 2 * Tp - 1, y0 - Ap - 12, 1, 0, ORG, 1.6, 7)
b += text(xs + 1.5 * Tp, y0 - Ap - 17, "T", ORG, 15, "middle", "700")
# giá treo + lò xo + vật + bút
b += f'<line x1="272" y1="20" x2="344" y2="20" stroke="currentColor" stroke-width="3"/>'
for xx in range(278, 344, 10):
    b += f'<line x1="{xx}" y1="20" x2="{xx+8}" y2="12" stroke="currentColor" stroke-width="1.2" opacity=".5"/>'
top = ypen - 18
sp = [(308, 20), (308, 30)]
n = 12
for i in range(n):
    sp.append((308 + (8 if i % 2 == 0 else -8), 30 + (top - 40) * (i + .5) / n))
sp += [(308, top - 10), (308, top)]
b += '<polyline points="' + " ".join(f"{px:.0f},{py:.0f}" for px, py in sp) + '" fill="none" stroke="currentColor" stroke-width="2"/>'
b += f'<rect x="290" y="{top:.0f}" width="36" height="36" rx="4" fill="rgba(148,163,184,.35)" stroke="currentColor" stroke-width="2.5"/>'
b += text(308, ypen + 6, "m", "currentColor", 15, "middle", "700")
b += f'<path d="M290,{ypen-5:.0f} L{xpen},{ypen:.0f} L290,{ypen+5:.0f} Z" fill="currentColor"/>'
b += text(281, ypen - 14, "bút", GRN, 14, "end", "700")
b += f'<line x1="346" y1="{ypen-26:.0f}" x2="346" y2="{ypen+26:.0f}" stroke="{GRN}" stroke-width="2"/>'
b += chevron(346, ypen - 28, 0, -1, GRN, 2, 8) + chevron(346, ypen + 28, 0, 1, GRN, 2, 8)
# chiều giấy chạy
b += f'<line x1="226" y1="244" x2="126" y2="244" stroke="{ORG}" stroke-width="2.2"/>' + chevron(124, 244, -1, 0, ORG, 2.2, 10)
b += text(234, 249, "giấy chạy đều", ORG, 14, "start", "700")
FIG2 = wrap("0 0 360 258", "Vật treo lò xo dao động lên xuống, bút gắn vào vật vẽ lên tờ giấy chạy đều sang trái một đường hình sin; trục đứng là li độ x từ −A đến A, khoảng giữa hai đỉnh liên tiếp là một chu kì T", b,
            "Hình 2. Bút gắn vào vật vẽ trên giấy chạy đều ra đường hình sin.<br>Trục đứng: li độ $x$, từ $-A$ đến $A$.<br>$T$: một chu kì.<br>"
            f"<small>Vẽ lại theo OpenStax, College Physics 2e, Hình 16.11 — CC BY‑NC‑SA 4.0 — {SRC_OS}</small>")

# Hình 3: quả cầu M quay đều, đèn chiếu thẳng xuống; bóng Q của M trên trục Ox chạy qua lại giữa −A và A.
b = ""
O_x, O_y, R, phi = 170, 170, 80, math.radians(50)
Mx, My = O_x + R * math.cos(phi), O_y - R * math.sin(phi)
b += text(170, 18, "đèn chiếu thẳng xuống", ORG, 14, "middle", "700")
for xx in (110, 150, round(Mx), 270):
    b += f'<line x1="{xx}" y1="28" x2="{xx}" y2="58" stroke="{ORG}" stroke-width="1.8"/>' + chevron(xx, 60, 0, 1, ORG, 1.8, 8)
b += f'<circle cx="{O_x}" cy="{O_y}" r="{R}" fill="rgba(148,163,184,.12)" stroke="currentColor" stroke-width="2"/>'
b += f'<line x1="56" y1="{O_y}" x2="320" y2="{O_y}" stroke="currentColor" stroke-width="1.8"/>' + chevron(322, O_y, 1, 0, "currentColor", 1.8, 10)
b += text(322, O_y + 22, "x", "currentColor", 15, "end", "700")
# vùng bóng chạy qua lại trên Ox
b += f'<line x1="{O_x-R+3}" y1="{O_y}" x2="{O_x+R-3}" y2="{O_y}" stroke="{BLUE}" stroke-width="4" opacity=".55"/>'
for xx in (O_x - R, O_x + R):
    b += f'<line x1="{xx}" y1="{O_y-6}" x2="{xx}" y2="{O_y+6}" stroke="currentColor" stroke-width="2"/>'
b += text(O_x - R - 6, O_y - 8, "−A", "currentColor", 14, "end", "700") + text(O_x + R + 6, O_y - 8, "A", "currentColor", 14, "start", "700")
b += f'<circle cx="{O_x}" cy="{O_y}" r="3.5" fill="currentColor"/>' + text(O_x - 6, O_y + 20, "O", "currentColor", 15, "end", "700")
# bán kính OM = A, góc φ
b += f'<line x1="{O_x}" y1="{O_y}" x2="{Mx:.1f}" y2="{My:.1f}" stroke="currentColor" stroke-width="2"/>'
b += text(O_x + 0.5 * (Mx - O_x) - 16, O_y + 0.5 * (My - O_y) - 6, "A", "currentColor", 15, "middle", "700")
r_a = 28
b += f'<path d="M{O_x+r_a},{O_y} A{r_a},{r_a} 0 0 0 {O_x+r_a*math.cos(phi):.1f},{O_y-r_a*math.sin(phi):.1f}" fill="none" stroke="{GRN}" stroke-width="1.8"/>'
b += text(O_x + 42 * math.cos(phi / 2), O_y - 42 * math.sin(phi / 2) + 6, "φ", GRN, 16, "middle", "700")
# chiều quay ω
r_w = 92
a0, a1 = math.radians(72), math.radians(112)
b += (f'<path d="M{O_x+r_w*math.cos(a0):.1f},{O_y-r_w*math.sin(a0):.1f} A{r_w},{r_w} 0 0 0 '
      f'{O_x+r_w*math.cos(a1):.1f},{O_y-r_w*math.sin(a1):.1f}" fill="none" stroke="{GRN}" stroke-width="2"/>')
b += chevron(O_x + r_w * math.cos(a1), O_y - r_w * math.sin(a1), -math.sin(a1), -math.cos(a1), GRN, 2, 9)
b += text(O_x + 104 * math.cos(math.radians(124)), O_y - 104 * math.sin(math.radians(124)) + 4, "ω", GRN, 16, "middle", "700")
# M, tia sáng qua M, bóng Q
b += f'<line x1="{Mx:.1f}" y1="{My+8:.1f}" x2="{Mx:.1f}" y2="{O_y-6}" stroke="currentColor" stroke-width="1.6" stroke-dasharray="4 3"/>'
b += f'<circle cx="{Mx:.1f}" cy="{My:.1f}" r="8" fill="{RED}" stroke="currentColor" stroke-width="1.5"/>'
b += text(Mx + 12, My - 6, "M", RED, 15, "start", "700")
b += f'<circle cx="{Mx:.1f}" cy="{O_y}" r="5.5" fill="{BLUE}"/>'
b += text(Mx + 6, O_y + 22, "Q (bóng)", BLUE, 14, "start", "700")
FIG3 = wrap("0 0 360 258", "Quả cầu M quay đều quanh O, đèn chiếu thẳng xuống; bóng Q của M trên trục Ox chạy qua lại giữa −A và A", b,
            "Hình 3. Quả cầu $M$ quay đều, bóng $Q$ của nó trên trục $Ox$ chạy qua lại giữa $-A$ và $A$.<br>"
            "Ghi vị trí $Q$ lên giấy chạy đều sẽ được đường hình sin như Hình 2.<br>"
            f"<small>Vẽ lại theo OpenStax, College Physics 2e, Hình 16.18 — CC BY‑NC‑SA 4.0 — {SRC_OS}</small>")

html = (HERE / "theory.src.html").read_text(encoding="utf-8")
html = html.replace("{{FIG1}}", FIG1).replace("{{FIG2}}", FIG2).replace("{{FIG3}}", FIG3)
(HERE / "theory.html").write_text(margin_figs(html), encoding="utf-8")
print("theory.html", len(html.encode()), "bytes")
