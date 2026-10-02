"""Sinh theory.html (chèn 3 hình SVG vào theory.src.html), 3 mục kho thí nghiệm và bundle.json.
Chạy từ thư mục này: python3 build.py"""
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
b = defs("f1")
O, A, y = 230, 100, 100
b += f'<line x1="22" y1="55" x2="22" y2="135" stroke="currentColor" stroke-width="4"/>'
for yy in range(60, 135, 12):
    b += f'<line x1="22" y1="{yy}" x2="12" y2="{yy+8}" stroke="currentColor" stroke-width="1.5" opacity=".5"/>'
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
b += f'<line x1="20" y1="148" x2="410" y2="148" stroke="currentColor" stroke-width="1.5" opacity=".6" marker-end="url(#f1-b)"/>'
for px, s in ((O - A, "−A"), (O, "O"), (O + A, "+A")):
    b += f'<line x1="{px}" y1="{y+20}" x2="{px}" y2="152" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3,3" opacity=".5"/>'
    b += text(px, 170, s, ORG if s != "O" else "currentColor", 14, "middle", "700")
b += text(400, 166, "x", "currentColor", 13, "end")
b += arrow("f1", "g", O - 30, 40, O - A + 22, 40, 2.5) + arrow("f1", "g", O + 30, 40, O + A - 22, 40, 2.5)
b += text(O, 32, "dao động qua lại", GRN, 13, "middle")
b += text(O, 205, "O là vị trí cân bằng", "currentColor", 12, "middle", "500")
FIG1 = wrap("0 0 440 215", "Con lắc lò xo dao động qua lại quanh vị trí cân bằng O giữa hai biên −A và +A", b,
            "Hình 1. Con lắc lò xo: vật dao động quanh vị trí cân bằng O, giữa hai biên −A và +A.", "tn-l11-daodongdieuhoa-01")

# ---- Hình 2: đồ thị li độ - thời gian (φ = 0)
b = defs("f2")
ox, oy, amp, Tpx = 50, 110, 62, 150
b += f'<line x1="{ox}" y1="14" x2="{ox}" y2="205" stroke="currentColor" stroke-width="1.5" opacity=".6"/>'
b += f'<line x1="{ox-12}" y1="{oy}" x2="425" y2="{oy}" stroke="currentColor" stroke-width="1.5" opacity=".6" marker-end="url(#f2-b)"/>'
for yy in (oy - amp, oy + amp):
    b += f'<line x1="{ox}" y1="{yy}" x2="400" y2="{yy}" stroke="currentColor" stroke-width="1" stroke-dasharray="4,4" opacity=".35"/>'
pts = " ".join(f"{ox + t:.0f},{oy - amp * math.cos(2 * math.pi * t / Tpx):.1f}" for t in range(0, 331, 5))
b += f'<polyline points="{pts}" fill="none" stroke="{BLUE}" stroke-width="2.5"/>'
b += f'<line x1="{ox+Tpx}" y1="{oy-amp}" x2="{ox+Tpx}" y2="188" stroke="currentColor" stroke-width="1" stroke-dasharray="3,3" opacity=".5"/>'
b += arrow("f2", "g", ox + 3, 188, ox + Tpx - 2, 188, 2) + arrow("f2", "g", ox + Tpx - 3, 188, ox + 4, 188, 2)
b += text(ox + Tpx / 2, 203, "T", GRN, 14, "middle", "700")
b += text(ox - 8, oy - amp + 5, "A", ORG, 14, "end", "700") + text(ox - 8, oy + amp + 5, "−A", ORG, 14, "end", "700")
b += text(ox - 8, oy + 16, "O", "currentColor", 13, "end") + text(ox + 6, 24, "x", "currentColor", 13) + text(418, oy + 18, "t", "currentColor", 13, "end")
FIG2 = wrap("0 0 440 215", "Đồ thị li độ theo thời gian của dao động điều hoà là đường hình sin, biên độ A, chu kì T", b,
            "Hình 2. Đồ thị li độ – thời gian: đường hình sin, biên độ A, chu kì T.", "tn-l11-daodongdieuhoa-02")

# ---- Hình 3: chuyển động tròn đều và hình chiếu
b = defs("f3")
cx, cy, r, ph = 112, 120, 80, math.radians(50)
mx, my = cx + r * math.cos(ph), cy - r * math.sin(ph)
b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="currentColor" stroke-width="1.5" opacity=".45"/>'
b += f'<line x1="{cx-r-22}" y1="{cy}" x2="{cx+r+30}" y2="{cy}" stroke="currentColor" stroke-width="1.5" opacity=".6" marker-end="url(#f3-b)"/>'
b += f'<line x1="{cx-r}" y1="{cy}" x2="{cx+r}" y2="{cy}" stroke="{BLUE}" stroke-width="5" stroke-linecap="round" opacity=".7"/>'
b += arrow("f3", "r", cx, cy, round(mx - 4), round(my + 4), 2.5)
b += f'<line x1="{mx:.0f}" y1="{my:.0f}" x2="{mx:.0f}" y2="{cy}" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,3" opacity=".6"/>'
b += f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="5" fill="{RED}"/><circle cx="{mx:.0f}" cy="{cy}" r="5" fill="{BLUE}"/>'
b += f'<path d="M{cx+28} {cy} A28 28 0 0 0 {cx+28*math.cos(ph):.0f} {cy-28*math.sin(ph):.0f}" fill="none" stroke="{GRN}" stroke-width="2"/>'
b += text(cx + 33, cy - 8, "φ", GRN, 14, "start", "700")
a1, a2 = math.radians(75), math.radians(125)
b += f'<path d="M{cx+92*math.cos(a1):.0f} {cy-92*math.sin(a1):.0f} A92 92 0 0 0 {cx+92*math.cos(a2):.0f} {cy-92*math.sin(a2):.0f}" fill="none" stroke="{GRN}" stroke-width="2.2" marker-end="url(#f3-g)"/>'
b += text(cx + 4, 14, "ω", GRN, 15, "middle", "700")
b += text(mx + 8, my - 6, "M", RED, 14, "start", "700") + text(mx, cy + 36, "Q", BLUE, 14, "middle", "700")
b += text(cx - 10, cy + 18, "O", "currentColor", 13, "end") + text(cx - r, cy + 18, "−A", ORG, 13, "middle", "700") + text(cx + r, cy + 18, "A", ORG, 13, "middle", "700")
b += text(cx + 12, cy - 44, "A", RED, 13, "end", "700")
b += text(236, 60, "M quay đều", RED, 13) + text(236, 80, "Q: hình chiếu của M", BLUE, 13) + text(236, 100, "Q dao động giữa −A và A", "currentColor", 13, "start", "500")
FIG3 = wrap("0 0 440 230", "Điểm M quay đều trên đường tròn bán kính A, hình chiếu Q lên trục x dao động điều hoà quanh O", b,
            "Hình 3. M quay đều trên đường tròn bán kính A; hình chiếu Q dao động điều hoà quanh O.", "tn-l11-daodongdieuhoa-03")

html = (HERE / "theory.src.html").read_text(encoding="utf-8")
html = html.replace("{{FIG1}}", FIG1).replace("{{FIG2}}", FIG2).replace("{{FIG3}}", FIG3)
(HERE / "theory.html").write_text(html, encoding="utf-8")
print("theory.html", len(html.encode()), "bytes")
