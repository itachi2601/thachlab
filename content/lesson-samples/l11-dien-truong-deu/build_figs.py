#!/usr/bin/env python3
"""Sinh 4 hình SVG cho bài Điện trường đều (lesson 37) và thay <!--FIGn--> trong theory.src.html -> theory.html.
Chạy lại được. Toạ độ quỹ đạo tính từ đúng phương trình parabol y = k·x² (kiểm bằng assert ở cuối)."""
import pathlib
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
PLUS_FILL, MINUS_FILL = "rgba(248,113,113,.28)", "rgba(56,189,248,.28)"


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1, marker=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#{marker})"' if marker else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" '
            f'stroke-width="{w}"{d} opacity="{op}"{m}/>')


def poly(pts, c, w=2.4, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<polyline fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"{d} points="'
            + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>')


def dot(x, y, r=5, c="currentColor"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'


def plate(x, y, w, h, sign):
    fill, col = (PLUS_FILL, RED) if sign == "+" else (MINUS_FILL, BLUE)
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{fill}" stroke="{col}" stroke-width="2"/>'


def fig(vb, label, body, cap, exp=None):
    s = wrap(vb, label, body, cap)
    if exp:
        s = s.replace('<figure class="fig" data-tl="1">', f'<figure class="fig" data-tl="1" data-exp="{exp}">', 1)
    return s


# ---------- Hình 1: máy in phun liên tục (chưa vẽ quỹ đạo — để học sinh dự đoán)
b = defs("f1")
b += f'<rect x="12" y="84" width="46" height="32" rx="4" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2"/>'
b += text(35, 134, "đầu in", "currentColor", 13, "middle")
for x in (72, 92, 112, 132, 152):
    b += dot(x, 100, 4, BLUE)
b += text(112, 82, "giọt mực (−)", BLUE, 13, "middle")
b += plate(180, 52, 130, 8, "+") + plate(180, 140, 130, 8, "-")
b += text(245, 44, "bản dương  + + +", RED, 13, "middle")
b += text(245, 168, "bản âm  − − −", BLUE, 13, "middle")
b += text(245, 110, "?", "currentColor", 30, "middle", "700")
b += f'<rect x="372" y="40" width="44" height="120" rx="6" fill="rgba(148,163,184,.18)" stroke="currentColor" stroke-width="2"/>'
b += text(394, 182, "đáy lon", "currentColor", 13, "middle")
fig1 = fig("0 0 440 192", "Máy in phun liên tục: giọt mực tích điện âm bay ngang vào khe giữa bản dương ở trên và bản âm ở dưới, rồi tới đáy lon",
           b, "Hình 1. Giọt mực tích điện bay qua khe giữa hai bản rồi mới tới đáy lon. Trong khe, giọt đi đường nào?")

# ---------- Hình 2: đường sức giữa hai bản song song
b = defs("f2")
TOP, BOT, X0, X1 = 40, 170, 60, 380          # mặt trong hai bản
b += plate(X0, TOP - 10, X1 - X0, 10, "+") + plate(X0, BOT, X1 - X0, 10, "-")
b += text(X0, 22, "+ + + + + + + + + + +", RED, 13, "start", "700")
b += text(X1, 22, "hiệu điện thế U", "currentColor", 13, "end", "700")
b += text(X0, 200, "− − − − − − − − − − −", BLUE, 13, "start", "700")
xs = [100 + 40 * i for i in range(7)]       # 100..340, cách đều 40 px
for x in xs:
    b += line(x, TOP + 2, x, BOT - 2, ORG, 2.2, marker="f2-o")
b += text(xs[3] + 8, 110, "E", ORG, 15, "start", "700")
for xe, ctrl in ((X0 + 6, 18), (X1 - 6, 422)):  # đường sức cong ở mép
    b += (f'<path d="M{xe},{TOP + 2} Q{ctrl},{(TOP + BOT) / 2} {xe},{BOT - 2}" fill="none" stroke="{ORG}" '
          f'stroke-width="1.8" stroke-dasharray="5 4" opacity=".8" marker-end="url(#f2-o)"/>')
b += text(14, 222, "mép: đường sức cong, không đều", "currentColor", 13, "start", "400")
b += line(432, TOP, 432, BOT, "currentColor", 1.5) + line(426, TOP, 438, TOP, "currentColor", 1.5) + line(426, BOT, 438, BOT, "currentColor", 1.5)
b += text(426, 112, "d", "currentColor", 14, "end", "700")
fig2 = fig("0 0 440 232", "Hai bản phẳng song song, bản trên dương, bản dưới âm. Giữa hai bản các đường sức thẳng, song song, cách đều, hướng từ bản dương xuống bản âm; ở mép đường sức cong ra",
           b, "Hình 2. Giữa hai bản (xa mép): đường sức <strong>thẳng, song song, cách đều</strong>, từ bản dương sang bản âm. Hiệu điện thế giữa hai bản là $U$, khoảng cách $d$.",
           exp="tn-l11-dien-truong-deu-01")

# ---------- Hình 3: quỹ đạo parabol của q > 0 và electron
b = defs("f3")
TOP, BOT, XA, XB = 38, 202, 60, 330          # mặt trong hai bản, đầu vào/ra
YC = (TOP + BOT) / 2                          # 120: chính giữa
L3, DY3 = XB - XA, 50                         # lệch 50 px khi ra khỏi bản
k3 = DY3 / L3 ** 2
b += plate(XA, TOP - 8, L3, 8, "+") + plate(XA, BOT, L3, 8, "-")
b += text(XA, 22, "+ + + + + + + + +", RED, 13, "start", "700")
b += text(XA, 228, "− − − − − − − − −", BLUE, 13, "start", "700")
for x in (110, 150, 250, 290):
    b += line(x, TOP + 2, x, BOT - 2, ORG, 1.6, op=.45, marker="f3-o")
b += text(256, 186, "E", ORG, 13, "start", "700")
b += line(14, YC, 54, YC, GRN, 3, marker="f3-g") + text(24, YC - 8, "v₀", GRN, 13, "start", "700")
slope3 = 2 * k3 * L3
for sgn, col, lab, ly in ((+1, "currentColor", "q &gt; 0", 160), (-1, BLUE, "electron", 92)):
    pts = [(XA + s, YC + sgn * k3 * s * s) for s in range(0, L3 + 1, 6)]
    b += poly(pts, col, 2.6)
    ye = YC + sgn * DY3
    b += line(XB, ye, 420, ye + sgn * slope3 * (420 - XB), col, 2, "6 4", .9)
    b += text(342, ly, lab, col, 13, "start", "700")
    sm = L3 / 2
    xm, ym = XA + sm, YC + sgn * k3 * sm * sm
    b += dot(xm, ym, 5, col)
    b += line(xm, ym + sgn * 6, xm, ym + sgn * 34, RED, 3, marker="f3-r")
    b += text(xm + 8, ym + sgn * 30 + 4, "F", RED, 13, "start", "700")
fig3 = fig("0 0 440 240", "Hai bản nằm ngang, bản trên dương, bản dưới âm, đường sức hướng xuống. Điện tích dương bay ngang vào giữa, chịu lực hướng xuống, cong theo parabol về bản âm. Electron chịu lực hướng lên, cong về bản dương. Ra khỏi bản cả hai đi thẳng",
           b, "Hình 3. Cùng bay ngang vào giữa: $q \\gt 0$ bị lực $F$ kéo về <strong>bản âm</strong>, electron về <strong>bản dương</strong>. Trong khe: parabol; ra khỏi bản: đi thẳng. Sơ đồ <strong>không đúng tỉ lệ</strong>.",
           exp="tn-l11-dien-truong-deu-03")

# ---------- Hình 4: bài toán mẫu, đúng tỉ lệ (50 px = 1 cm)
b = defs("f4")
S = 50                                         # px / cm
XA, XB = 80, 80 + 5.0 * S                      # L = 5,0 cm -> 250 px
TOP, BOT = 50, 50 + 2.0 * S                    # d = 2,0 cm -> 100 px
YC = (TOP + BOT) / 2
DY4 = 0.25 * S                                 # y = 2,5 mm = 0,25 cm -> 12,5 px
L4 = XB - XA
k4 = DY4 / L4 ** 2
b += plate(XA, TOP - 6, L4, 6, "+") + plate(XA, BOT, L4, 6, "-")
b += text(XA, 36, "+ + + + + + +   U = 91 V", RED, 13, "start", "700")
b += text(XA, 172, "− − − − − − −", BLUE, 13, "start", "700")
b += line(XA, YC, 340, YC, "currentColor", 1, "3 3", .4)
b += line(20, YC, 74, YC, GRN, 3, marker="f4-g") + text(28, YC - 8, "v₀", GRN, 13, "start", "700")
b += line(110, TOP + 4, 110, TOP + 38, ORG, 2, marker="f4-o") + text(116, TOP + 26, "E", ORG, 13, "start", "700")
pts = [(XA + s, YC - k4 * s * s) for s in range(0, int(L4) + 1, 5)]
b += poly(pts, BLUE, 2.6)
ye = YC - DY4
slope4 = 2 * k4 * L4
b += line(XB, ye, 420, ye - slope4 * (420 - XB), BLUE, 2, "6 4", .9)
xm = XA + L4 / 2; ym = YC - k4 * (L4 / 2) ** 2
b += dot(xm, ym, 5, BLUE)
b += line(xm, ym - 6, xm, ym - 32, RED, 3, marker="f4-r") + text(xm + 8, ym - 20, "F", RED, 13, "start", "700")
b += text(xm - 10, ym + 20, "electron", BLUE, 13, "end", "700")
b += line(346, YC, 346, ye, "currentColor", 1.5) + line(341, YC, 351, YC, "currentColor", 1.5) + line(341, ye, 351, ye, "currentColor", 1.5)
b += text(346, YC + 14, "y = 2,5 mm", "currentColor", 13, "start", "700")
b += line(XA, 184, XB, 184, "currentColor", 1.5) + line(XA, 178, XA, 190, "currentColor", 1.5) + line(XB, 178, XB, 190, "currentColor", 1.5)
b += text((XA + XB) / 2, 202, "L = 5,0 cm", "currentColor", 13, "middle", "700")
b += line(430, TOP, 430, BOT, "currentColor", 1.5) + line(424, TOP, 436, TOP, "currentColor", 1.5) + line(424, BOT, 436, BOT, "currentColor", 1.5)
b += text(424, BOT - 8, "d = 2,0 cm", "currentColor", 13, "end", "700")
fig4 = fig("0 0 440 212", "Bài toán mẫu vẽ đúng tỉ lệ: hai bản dài 5 cm cách nhau 2 cm, bản trên dương. Electron bay vào chính giữa với v0, lực điện hướng lên, lệch 2,5 mm khi ra khỏi bản rồi đi thẳng",
           b, "Hình 4. Bài toán mẫu, vẽ đúng tỉ lệ. Electron lệch lên về bản dương; ra khỏi bản lệch $2{,}5$ mm, nhỏ hơn $10$ mm từ đường giữa tới bản trên nên không chạm.",
           exp="tn-l11-dien-truong-deu-03")

# ---------- Kiểm toạ độ: chấm nằm trên parabol, mép ra đúng độ lệch, chiều lực đúng
assert abs(k3 * (L3 / 2) ** 2 - DY3 / 4) < 1e-9
assert abs(k4 * L4 ** 2 - DY4) < 1e-9 and abs(DY4 / S - 0.25) < 1e-12   # 2,5 mm
assert TOP < YC - DY4 and abs(slope4 - 0.1) < 1e-9                       # tan α = 0,10 như lời giải

src = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, n
    src = src.replace(f"<!--FIG{n}-->", f)
(HERE / "theory.html").write_text(src, encoding="utf8")
print("ok", len(src))
