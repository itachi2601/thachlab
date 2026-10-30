#!/usr/bin/env python3
"""Sinh 4 hình SVG cho bài Điện trường đều (lesson 37) và thay <!--FIGn--> trong theory.src.html -> theory.html.
Chạy lại được. Toạ độ quỹ đạo tính từ đúng phương trình parabol y = k·x² (kiểm bằng assert ở cuối).
Vẽ lại 31/10/2026: svg_lib của skill (đầu V 30°, không marker), đường sức nét đứt, chữ ≥ 14, chỉ số bằng tspan."""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
_sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import RED, BLUE, ORG, GRN, wrap, arrow, field_line  # noqa: E402
from svg_lib import text as _text  # noqa: E402

PLUS_FILL, MINUS_FILL = "rgba(248,113,113,.28)", "rgba(56,189,248,.28)"
FS = 14
V0 = 'v<tspan dy="5" font-size="14">0</tspan>'


def text(x, y, s, c="currentColor", size=FS, anchor="start", weight="700"):
    return _text(x, y, s, c, max(size, FS), anchor, weight)


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" '
            f'stroke-width="{w}"{d} opacity="{op}"/>')


def poly(pts, c, w=2.4, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<polyline fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"{d} points="'
            + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>')


def dot(x, y, r=5, c="currentColor"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'


def plate(x, y, w, h, sign):
    fill, col = (PLUS_FILL, RED) if sign == "+" else (MINUS_FILL, BLUE)
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{fill}" stroke="{col}" stroke-width="2"/>'


def dim_v(x, y1, y2, t=5):
    return (line(x, y1, x, y2, "currentColor", 1.5) + line(x - t, y1, x + t, y1, "currentColor", 1.5)
            + line(x - t, y2, x + t, y2, "currentColor", 1.5))


def fig(vb, label, body, cap, exp=None):
    s = wrap(vb, label, body, cap)
    if exp:
        s = s.replace('<figure class="fig" data-tl="1">', f'<figure class="fig" data-tl="1" data-exp="{exp}">', 1)
    return s


# ---------- Hình 1: máy in phun liên tục (chưa vẽ quỹ đạo — để học sinh dự đoán)
b = '<rect x="12" y="84" width="46" height="32" rx="4" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2"/>'
b += text(35, 136, "đầu in", anchor="middle")
for x in (72, 92, 112, 132, 152):
    b += dot(x, 100, 4, BLUE)
b += text(112, 80, "giọt mực (−)", BLUE, anchor="middle")
b += plate(180, 52, 130, 8, "+") + plate(180, 140, 130, 8, "-")
b += text(245, 42, "bản dương (+)", RED, anchor="middle")
b += text(245, 170, "bản âm (−)", BLUE, anchor="middle")
b += text(245, 110, "?", "currentColor", 30, "middle")
b += '<rect x="372" y="40" width="44" height="120" rx="6" fill="rgba(148,163,184,.18)" stroke="currentColor" stroke-width="2"/>'
b += text(394, 182, "đáy lon", anchor="middle")
fig1 = fig("0 0 440 192", "Máy in phun liên tục: giọt mực tích điện âm bay ngang vào khe giữa bản dương ở trên và bản âm ở dưới, rồi tới đáy lon",
           b, "Hình 1. Giọt mực tích điện bay qua khe giữa hai bản rồi mới tới đáy lon. Trong khe, giọt đi đường nào?")

# ---------- Hình 2: ảnh OpenStax College Physics 2e, Hình 19.5 (đợt 28/10/2026)
fig2 = ('<figure class="fig" data-tl="1" data-exp="tn-l11-dien-truong-deu-01"><img src="/assets/openstax/l11-dien-truong-deu/hinh-hai-ban-song-song.webp" '
        'alt="Hai bản dẫn điện song song cách nhau d, bản A dương bên trái, bản B âm bên phải; giữa hai bản các đường sức thẳng, song song, cách đều, cong ra ở mép" '
        'loading="lazy" width="410" height="768" style="max-width:min(100%,300px);height:auto">'
        '<figcaption>Hình 2. Giữa hai bản (xa mép): đường sức thẳng, song song, cách đều.<br>'
        'V<sub>AB</sub> (bài ghi U) = E·d, tức E = U/d; d là khoảng cách hai bản.<br>'
        '<small>Hình: OpenStax, College Physics 2e, Hình 19.5 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>')


# ---------- Hình 3: quỹ đạo parabol của q > 0 và electron (sơ đồ, không đúng tỉ lệ)
TOP, BOT, XA, XB = 44, 204, 60, 320          # mặt trong hai bản, đầu vào/ra
YC = (TOP + BOT) / 2                          # 124: chính giữa
L3, DY3 = XB - XA, 46                         # lệch 46 px khi ra khỏi bản
k3 = DY3 / L3 ** 2
slope3 = 2 * k3 * L3                          # hệ số góc tiếp tuyến tại mép ra
XEND = 404
b = plate(XA, TOP - 8, L3, 8, "+") + plate(XA, BOT, L3, 8, "-")
b += text(XA, 26, "bản dương (+)", RED)
b += text(XA, 232, "bản âm (−)", BLUE)
for x in (100, 140, 240, 280):                # đường sức: nét đứt, bản dương → bản âm (hướng xuống)
    b += field_line(x, TOP + 2, x, BOT - 2, ORG, 1.8)
b += text(252, 178, "E", ORG)
b += arrow("", "g", 12, YC, 56, YC) + text(16, YC - 10, V0, GRN)
for sgn, col, lab in ((+1, "currentColor", "q &gt; 0"), (-1, BLUE, "electron")):
    pts = [(XA + s, YC + sgn * k3 * s * s) for s in range(0, L3 + 1, 5)]
    ye = YC + sgn * DY3
    pts.append((XEND, ye + sgn * slope3 * (XEND - XB)))   # ra khỏi bản: thẳng theo tiếp tuyến
    b += poly(pts, col, 2.6)
    yl = ye + sgn * slope3 * (XEND - XB)
    b += text(436, yl + (22 if sgn > 0 else -12), lab, col, anchor="end")
    sm = L3 / 2
    xm, ym = XA + sm, YC + sgn * k3 * sm * sm
    b += dot(xm, ym, 5, col)
    b += arrow("", "r", xm, ym + sgn * 6, xm, ym + sgn * 36)          # cùng |q|E → dài bằng nhau
    b += text(xm + 10, ym + sgn * 30 + 5, "F", RED)
fig3 = fig("0 0 440 244", "Hai bản nằm ngang, bản trên dương, bản dưới âm, đường sức hướng xuống. Điện tích dương bay ngang vào giữa, chịu lực hướng xuống, cong theo parabol về bản âm. Electron chịu lực hướng lên, cong về bản dương. Ra khỏi bản cả hai đi thẳng",
           b, "Hình 3. Cùng bay ngang vào giữa: $q \\gt 0$ bị lực $F$ kéo về <strong>bản âm</strong>, electron về <strong>bản dương</strong>. Trong khe: parabol; ra khỏi bản: đi thẳng. Sơ đồ <strong>không đúng tỉ lệ</strong>.",
           exp="tn-l11-dien-truong-deu-03")

# ---------- Hình 4: bài toán mẫu, đúng tỉ lệ (50 px = 1 cm)
S = 50                                         # px / cm
XA, XB = 70, 70 + 5.0 * S                      # L = 5,0 cm -> 250 px
TOP, BOT = 58, 58 + 2.0 * S                    # d = 2,0 cm -> 100 px
YC = (TOP + BOT) / 2
DY4 = 0.25 * S                                 # y = 2,5 mm = 0,25 cm -> 12,5 px
L4 = XB - XA
k4 = DY4 / L4 ** 2
slope4 = 2 * k4 * L4
XEND = 408
b = plate(XA, TOP - 6, L4, 6, "+") + plate(XA, BOT, L4, 6, "-")
b += text(XA, 42, "bản dương (+)", RED) + text(XB, 42, "U = 91 V", "currentColor", anchor="end")
b += text(XA, 182, "bản âm (−)", BLUE)
b += line(XA, YC, XEND, YC, "currentColor", 1, "3 3", .4)
b += arrow("", "g", 12, YC, 66, YC) + text(18, YC - 10, V0, GRN)
b += field_line(110, TOP + 4, 110, TOP + 40, ORG, 2) + text(118, TOP + 28, "E", ORG)
pts = [(XA + s, YC - k4 * s * s) for s in range(0, int(L4) + 1, 5)]
ye = YC - DY4
pts.append((XEND, ye - slope4 * (XEND - XB)))   # ra khỏi bản: thẳng theo tiếp tuyến
b += poly(pts, BLUE, 2.6)
xm = XA + L4 / 2; ym = YC - k4 * (L4 / 2) ** 2
b += dot(xm, ym, 5, BLUE)
b += arrow("", "r", xm, ym - 6, xm, ym - 34) + text(xm + 10, ym - 18, "F", RED)
b += text(xm - 12, ym + 24, "electron", BLUE, anchor="end")
b += dim_v(XB + 16, YC, ye) + text(XB + 24, YC + 20, "y = 2,5 mm")
b += line(XA, 196, XB, 196, "currentColor", 1.5) + line(XA, 190, XA, 202, "currentColor", 1.5) + line(XB, 190, XB, 202, "currentColor", 1.5)
b += text((XA + XB) / 2, 218, "L = 5,0 cm", anchor="middle")
b += dim_v(432, TOP, BOT) + text(424, BOT + 22, "d = 2,0 cm", anchor="end")
fig4 = fig("0 0 440 226", "Bài toán mẫu vẽ đúng tỉ lệ: hai bản dài 5 cm cách nhau 2 cm, bản trên dương. Electron bay vào chính giữa với v0, lực điện hướng lên, lệch 2,5 mm khi ra khỏi bản rồi đi thẳng",
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
(HERE / "theory.html").write_text(margin_figs(src), encoding="utf8")
print("ok", len(src))
