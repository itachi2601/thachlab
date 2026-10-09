"""Sinh 3 hình SVG, thay <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được).
Chạy: python3 content/hsg9/cd02-dong-nang-the-nang-co-nang/build_figs.py"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "soan-bai-ly-thuyet-tuong-tac", "scripts"))
from svg_lib import RED, BLUE, ORG, GRN, text, wrap, chevron

def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'

def path(d, c="currentColor", w=2.4, dash=""):
    dd = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}"{dd}/>'

def sub(main, s, c="currentColor", x=0, y=0, size=13, anchor="start"):
    return (f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="600" text-anchor="{anchor}">{main}'
            f'<tspan baseline-shift="sub" font-size="{size-3}">{s}</tspan></text>')

# ---------- Hình 1: ba dốc cùng độ cao h -> cùng vận tốc ----------
top, gnd = 40, 170
b = line(14, top, 426, top, "currentColor", 1.2, "3 4", .5)
b += line(14, top, 14, gnd, "currentColor", 1.6)
b += chevron(14, top, 0, -1, "currentColor", 1.6, 8) + chevron(14, gnd, 0, 1, "currentColor", 1.6, 8)
b += text(22, 110, "h", "currentColor", 14, "start", "700")
panels = [(30, "Dốc dựng", 55), (165, "Dốc thoải", 105), (300, "Dốc cong", 0)]
for x0, name, run in panels:
    b += text(x0 + 60, 22, name, "currentColor", 13, "middle", "700")
    if name == "Dốc cong":
        b += path(f"M{x0+8},{top} C{x0+8},{top+85} {x0+35},{gnd} {x0+125},{gnd}", "currentColor", 2.6)
    else:
        b += path(f"M{x0+8},{top} L{x0+8+run},{gnd} L{x0+125},{gnd}", "currentColor", 2.6)
    if name == "Dốc cong":
        b += line(x0 - 4, gnd, x0 + 135, gnd, "currentColor", 1.2, "", .5)
    else:
        b += line(x0 - 4, gnd, x0 + 135, gnd, "currentColor", 1.2, "", .5)
    b += f'<circle cx="{x0+8}" cy="{top-6}" r="6" fill="{ORG}"/>'
    b += text(x0 + 70, 196, "v = 10 m/s", GRN, 13, "middle", "700")
fig1 = wrap("0 0 440 210", "Ba dốc khác hình dạng cùng cao h: vận tốc ở chân dốc như nhau",
            b, "Hình 1. Ba dốc có cùng độ cao h = 5 m, bỏ qua ma sát. Vận tốc ở chân dốc đều là 10 m/s, không phụ thuộc hình dạng dốc.")

# ---------- Hình 2: mặt phẳng nghiêng, s, d, h ----------
ax, ay, bx, by = 60, 50, 340, 150            # đỉnh dốc, chân dốc (cùng mức với đáy)
L = math.hypot(bx - ax, by - ay)
ux, uy = (bx - ax) / L, (by - ay) / L         # dọc dốc (xuống)
nx, ny = uy, -ux                              # pháp tuyến hướng lên
b = line(ax, ay, ax, by, "currentColor", 2)            # h
b += line(ax, by, bx, by, "currentColor", 2)           # đáy
b += line(ax, ay, bx, by, "currentColor", 2.6)         # dốc
# khối trượt ở t = 0.38
t = 0.38
px, py = ax + (bx - ax) * t, ay + (by - ay) * t
cx, cy = px + nx * 9, py + ny * 9
ang = math.degrees(math.atan2(uy, ux))
b += (f'<rect x="{cx-16:.1f}" y="{cy-9:.1f}" width="32" height="18" rx="2" fill="rgba(148,163,184,.3)" stroke="currentColor" '
      f'stroke-width="2" transform="rotate({ang:.1f} {cx:.1f} {cy:.1f})"/>')
# lực ma sát: dọc dốc, hướng lên (ngược chiều trượt)
fx, fy = cx - ux * 56, cy - uy * 56
b += line(cx - ux * 20, cy - uy * 20, fx, fy, RED, 2.6) + chevron(fx, fy, -ux, -uy, RED, 2.6, 12)
b += sub("F", "ms", RED, fx - 4, fy - 12, 13, "end")
# nhãn s, h, α
b += text((px + 62 + nx * 30) , py + 30 + ny * 30 + 14, "s", ORG, 15, "middle", "700")
b += text(ax - 10, (ay + by) / 2 + 5, "h", BLUE, 15, "end", "700")
b += (f'<path d="M{bx-48},{by} A48,48 0 0 0 {bx-48*math.cos(math.atan2(by-ay,bx-ax)):.1f},{by-48*math.sin(math.atan2(by-ay,bx-ax)):.1f}" '
      f'fill="none" stroke="currentColor" stroke-width="1.6"/>')
b += text(bx - 62, by - 8, "α", "currentColor", 14, "middle", "700")
# d: hình chiếu ngang
b += line(ax, 168, bx, 168, GRN, 2.2) + line(ax, 162, ax, 174, GRN, 2.2) + line(bx, 162, bx, 174, GRN, 2.2)
b += text((ax + bx) / 2, 186, "d", GRN, 15, "middle", "700")
b += text(14, 214, "s: quãng đường trượt trên dốc", ORG, 12, "start", "400")
b += text(14, 231, "d = s·cosα: hình chiếu ngang của s", GRN, 12, "start", "400")
b += (f'<text x="14" y="248" fill="{RED}" font-size="12" font-weight="600">A<tspan baseline-shift="sub" font-size="9">ms</tspan> = μmg·cosα·s = μmg·d</text>')
fig2 = wrap("0 0 440 258", "Mặt phẳng nghiêng: quãng đường s, hình chiếu ngang d, độ cao h, góc nghiêng α",
            b, "Hình 2. Công của lực ma sát trên mặt phẳng nghiêng chỉ phụ thuộc hình chiếu ngang d của quãng đường.")

# ---------- Hình 3: đồ thị năng lượng theo độ cao (m = 2 kg, H = 20 m) ----------
X0, Y0, kx, ky = 60, 190, 17.0, 0.4            # px: h=0, 0 J ; px/m ; px/J
X = lambda h: X0 + kx * h
Y = lambda e: Y0 - ky * e
b = line(X0, Y0, 420, Y0, "currentColor", 1.8) + chevron(420, Y0, 1, 0, "currentColor", 1.8, 9)
b += line(X0, Y0, X0, 14, "currentColor", 1.8) + chevron(X0, 14, 0, -1, "currentColor", 1.8, 9)
for h in (0, 5, 10, 15, 20):
    b += line(X(h), Y0, X(h), Y0 + 5, "currentColor", 1.4) + text(X(h), Y0 + 19, str(h), "currentColor", 12, "middle", "400")
for e in (0, 200, 400):
    b += line(X0 - 5, Y(e), X0, Y(e), "currentColor", 1.4) + text(X0 - 8, Y(e) + 4, str(e), "currentColor", 12, "end", "400")
b += text(X(10), Y0 + 36, "độ cao h (m)", "currentColor", 12, "middle", "400")
b += text(X0 + 14, 18, "năng lượng (J)", "currentColor", 12, "start", "400")
b += line(X(0), Y(400), X(20), Y(400), GRN, 2.6)                 # W
b += line(X(0), Y(0), X(20), Y(400), BLUE, 2.6)                  # Wt = 20h
b += line(X(0), Y(400), X(20), Y(0), RED, 2.6)                   # Wđ = 400 - 20h
b += line(X(10), Y(200), X(10), Y0, "currentColor", 1.2, "3 4", .6)
b += f'<circle cx="{X(10)}" cy="{Y(200)}" r="5" fill="currentColor"/>'
b += text(X(20) - 4, Y(400) - 7, "W = 400 J (cơ năng)", GRN, 12, "end", "700")
b += sub("W", "t", BLUE, 352, 74, 13) + sub("W", "đ", RED, 150, 56, 13)
b += text(292, 106, "Cắt nhau ở h = 10 m:", "currentColor", 11, "start", "600")
b += text(292, 122, "Wđ = Wt = 200 J", "currentColor", 11, "start", "600")
fig3 = wrap("0 0 440 232", "Đồ thị năng lượng theo độ cao: thế năng tăng, động năng giảm, cơ năng nằm ngang",
            b, "Hình 3. Vật 2 kg rơi tự do từ H = 20 m (mốc mặt đất). Thế năng và động năng là hai đường thẳng cắt nhau tại h = H/2; cơ năng không đổi.")

src = open(os.path.join(HERE, "theory.src.html"), encoding="utf8").read()
for n, f in ((1, fig1), (2, fig2), (3, fig3)):
    src = src.replace(f"<!--FIG{n}-->", f)
open(os.path.join(HERE, "theory.html"), "w", encoding="utf8").write(src)
print("ok", len(src))
