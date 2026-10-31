"""Sinh 4 hình SVG cho bài "Bài 16. Điện từ trường. Mô hình sóng điện từ" (Vật lí 12)
và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html.
Chạy từ thư mục này: python3 build_figs.py
"""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *  # noqa: E402


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def rect(x, y, w, h, fill="rgba(148,163,184,.10)", stroke="currentColor", sw=2, rx=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def arc(cx, cy, r, a1, a2, c="currentColor", w=2, op=1):
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    x2, y2 = cx + r * math.cos(math.radians(a2)), cy + r * math.sin(math.radians(a2))
    return (f'<path d="M {x1:.1f},{y1:.1f} A {r},{r} 0 0 1 {x2:.1f},{y2:.1f}" fill="none" '
            f'stroke="{c}" stroke-width="{w}" opacity="{op}"/>')


def poly(pts, c, w=2.4, op=1):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polyline fill="none" stroke="{c}" stroke-width="{w}" opacity="{op}" points="{p}"/>'


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


# ------------------------------------------------- Hình 1: tiếng rè bên bếp từ
b = defs("f1")
b += text(14, 24, "Không có dây nối, radio vẫn rè", "currentColor", 15, "start", "700")
# bếp từ: mặt bếp + nồi
b += rect(14, 104, 124, 16, rx=4)
b += f'<ellipse cx="76" cy="112" rx="34" ry="4" fill="none" stroke="{ORG}" stroke-width="1.6"/>'
b += rect(40, 70, 72, 34, rx=4)
b += line(30, 76, 40, 76, "currentColor", 3)
b += line(112, 76, 122, 76, "currentColor", 3)
b += text(76, 146, "bếp từ", "currentColor", 15, "middle", "700")
b += text(76, 166, "dòng xoay chiều", "currentColor", 14, "middle", "600")
# sóng lan ra
for r, op in ((28, .95), (52, .7), (76, .45)):
    b += arc(140, 96, r, -48, 48, BLUE, 2.4, op)
# radio + ăng ten
b += rect(262, 72, 136, 58, rx=8)
b += f'<circle cx="294" cy="101" r="17" fill="none" stroke="currentColor" stroke-width="2"/>'
for dy in (-8, 0, 8):
    b += line(282, 101 + dy, 306, 101 + dy, "currentColor", 1.6)
b += rect(326, 88, 56, 14, fill="none", sw=1.6, rx=3)
b += f'<circle cx="368" cy="117" r="5" fill="none" stroke="currentColor" stroke-width="1.8"/>'
b += line(380, 72, 398, 38, "currentColor", 2.4)
b += f'<circle cx="398" cy="38" r="3" fill="currentColor"/>'
b += text(330, 152, "radio chạy pin", "currentColor", 15, "middle", "700")
# khoảng cách 2 m
b += line(76, 188, 180, 188, "currentColor", 1.4) + line(226, 188, 330, 188, "currentColor", 1.4)
b += chevron(76, 188, -1, 0, "currentColor", 1.4, 9) + chevron(330, 188, 1, 0, "currentColor", 1.4, 9)
b += line(76, 180, 76, 196, "currentColor", 1.4) + line(330, 180, 330, 196, "currentColor", 1.4)
b += text(203, 193, "2 m", "currentColor", 15, "middle", "700")
fig1 = wrap("0 0 420 206", "Bếp từ chạy dòng xoay chiều đặt cách một radio chạy pin hai mét: sóng điện từ lan từ bếp từ tới ăng ten radio",
            b, "Hình 1. Bếp từ chạy dòng xoay chiều: điện từ trường lan tới ăng ten radio cách hai mét.",
            exp="tn-l12-dttruong-03")

# ------------------------------------------------- Hình 2: điện trường xoáy
# Vòng E nằm ngang nhìn xiên (ellipse). B hướng lên, đang tăng -> E xoáy chiều kim đồng hồ nhìn từ trên xuống
# (định luật Lenz): nửa sau (trên hình) đi sang phải, nửa trước (dưới hình) đi sang trái; t tăng đúng chiều này.
b = defs("f2")
b += text(14, 24, "Điện trường xoáy bao quanh đường sức từ", "currentColor", 15, "start", "700")
CX, CY, RX, RY = 200, 126, 120, 34
XS = (164, 200, 236)          # ba đường sức từ
GAP = 6
# nửa sau: bị đường sức từ (ở giữa vòng) che -> ngắt khe
seg, segs = [], []
for x, y in arc_pts(CX, CY, RX, RY, 180, 360, 160):
    if any(abs(x - xl) < GAP for xl in XS):
        if len(seg) > 1:
            segs.append(seg)
        seg = []
    else:
        seg.append((x, y))
segs.append(seg)
for sg in segs:
    b += pts_path(sg, BLUE, 2.6)
# đường sức từ: nét đứt, ngắt ở chỗ nửa trước của vòng đi qua phía trước
YT, YB = 50, 204
for xl in XS:
    yf = CY + RY * math.sqrt(1 - ((xl - CX) / RX) ** 2)
    b += line(xl, YB, xl, yf + GAP, RED, 2.2, "6 4")
    b += field_line(xl, yf - GAP, xl, YT, RED, 2.2)
# nửa trước: nét liền đè lên
b += pts_path(arc_pts(CX, CY, RX, RY, 0, 180, 80), BLUE, 2.6)
for t in (120, 300):
    x, y = ell_pt(CX, CY, RX, RY, t)
    b += chevron(x, y, *ell_tan(RX, RY, t, 1), BLUE, 2.6, 13)
b += text(250, 60, "B đang tăng", RED, 15, "start", "700")
b += text(330, 132, "E xoáy", BLUE, 15, "start", "700")
b += text(14, 234, "Nét đứt đỏ: đường sức từ, B hướng lên.", RED, 14, "start", "600")
b += text(14, 254, "Vòng xanh: đường sức điện trường xoáy.", BLUE, 14, "start", "600")
b += text(14, 274, "Vòng khép kín, bao quanh các đường sức từ.", "currentColor", 14, "start", "600")
fig2 = wrap("0 0 420 286", "Ba đường sức từ nét đứt hướng lên, đang tăng; một vòng kín nằm ngang của điện trường xoáy bao quanh chúng, mũi tên chỉ chiều kim đồng hồ khi nhìn từ trên xuống",
            b, "Hình 2. Từ trường biến thiên (ở đây B đang tăng) sinh điện trường xoáy; đường sức điện trường xoáy là đường cong kín bao quanh các đường cảm ứng từ.")

# ------------------------------------------------- Hình 3: sóng điện từ (ảnh OpenStax, chèn trực tiếp)
fig3 = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l12-dien-tu-truong-song-dien-tu/hinh-3.webp" '
        'alt="Một đoạn sóng điện từ truyền sang phải: các mũi tên xanh của vectơ E dao động thẳng đứng, các mũi tên hồng của vectơ B dao động trong mặt phẳng nằm ngang, hai đường cong cùng pha và cùng vuông góc phương truyền" '
        'loading="lazy" width="875" height="602"><figcaption>'
        'Hình 3. Sóng điện từ: E vuông góc B, cả hai vuông góc phương truyền, cùng pha.<br>'
        'Mũi tên xanh: vectơ điện trường E.<br>'
        'Mũi tên hồng: vectơ cảm ứng từ B.<br>'
        'Mũi tên xanh lá c: phương truyền sóng.<br>'
        'Hình: OpenStax, College Physics 2e, Hình 24.7 — CC BY\u2011NC\u2011SA 4.0 — openstax.org/books/college-physics-2e'
        '</figcaption></figure>')

# ------------------------------------------------- Hình 4: thang sóng điện từ (ảnh OpenStax, chèn trực tiếp)
fig4 = ('<figure class="fig" data-tl="1" data-exp="tn-l12-dttruong-04"><img src="/assets/openstax/l12-dien-tu-truong-song-dien-tu/hinh-pho-dien-tu.webp" '
        'alt="Thang sóng điện từ theo bước sóng (trục trên) và tần số (trục dưới): sóng vô tuyến gồm vi ba, TV, FM, AM ở tần số thấp, tiếp đến hồng ngoại, dải ánh sáng nhìn thấy rất hẹp, tử ngoại, tia X, tia gamma ở tần số cao" '
        'loading="lazy" width="1000" height="377"><figcaption>'
        'Hình 4. Thang sóng điện từ: bước sóng giảm dần từ sóng vô tuyến tới tia gamma; ánh sáng nhìn thấy là dải rất hẹp.<br>'
        'Nhãn: Wavelength = bước sóng; Frequency = tần số; Radio waves = sóng vô tuyến; Microwaves = vi ba.<br>'
        'Nhãn: Infrared = hồng ngoại; Visible light = nhìn thấy; Ultraviolet = tử ngoại; X rays = tia X; \u03b3 rays = tia gamma.<br>'
        'Nhãn: \u00c5 = $10^{-10}$ m; fermis = $10^{-15}$ m.<br>'
        'Hình: OpenStax, College Physics 2e, Hình 24.8 \u2014 CC BY\u2011NC\u2011SA 4.0 \u2014 openstax.org/books/college-physics-2e'
        '</figcaption></figure>')

# ------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(margin_figs(src))
print("ok", len(src), "bytes")
