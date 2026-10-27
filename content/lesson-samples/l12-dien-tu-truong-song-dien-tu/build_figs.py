"""Sinh 4 hình SVG cho bài "Bài 16. Điện từ trường. Mô hình sóng điện từ" (Vật lí 12)
và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html.
Chạy từ thư mục này: python3 build_figs.py
"""
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
b += text(14, 22, "Không có dây nối, radio vẫn rè", "currentColor", 12.5, "start", "700")
b += rect(14, 62, 96, 74)
b += text(62, 92, "bếp từ", "currentColor", 12, "middle", "700")
b += text(62, 110, "dòng xoay chiều", "currentColor", 9.5, "middle", "600")
b += text(62, 124, "biến thiên", "currentColor", 9.5, "middle", "600")
for r, op in ((26, .95), (44, .7), (62, .45)):
    b += arc(125, 100, r, -52, 52, BLUE, 2.2, op)
b += rect(250, 64, 88, 72)
b += text(294, 96, "radio", "currentColor", 12, "middle", "700")
b += text(294, 114, "chạy pin", "currentColor", 9.5, "middle", "600")
b += text(294, 128, "cách 2 m", "currentColor", 9.5, "middle", "600")
b += line(294, 64, 282, 30, "currentColor", 2.4)
fig1 = wrap("0 0 420 158", "Bếp từ chạy dòng xoay chiều đặt cạnh một radio chạy pin: sóng điện từ lan từ bếp từ tới ăng ten radio",
            b, "Hình 1. Bếp từ chạy dòng xoay chiều: điện từ trường lan tới ăng ten radio cách hai mét.",
            exp="tn-l12-dttruong-03")

# ------------------------------------------------- Hình 2: điện trường xoáy
b = defs("f2")
b += text(14, 22, "Điện trường xoáy bao quanh đường sức từ", "currentColor", 14, "start", "700")
b += f'<ellipse cx="210" cy="118" rx="96" ry="56" fill="none" stroke="{BLUE}" stroke-width="2.6"/>'
b += line(210, 52, 210, 184, RED, 3)
b += f'<path d="M210,56 L204,68 L216,68 z" fill="{RED}"/>'
b += arrow("f2", "b", 176, 62, 244, 62, 2.4)
b += arrow("f2", "b", 244, 174, 176, 174, 2.4)
b += text(222, 44, "từ trường B đang tăng", RED, 14, "start", "600")
b += text(22, 214, "đường sức điện trường xoáy:", BLUE, 14, "start", "600")
b += text(22, 232, "đường cong kín bao quanh đường cảm ứng từ", BLUE, 14, "start", "600")
fig2 = wrap("0 0 420 244", "Đường sức từ thẳng đứng có một mũi tên ở đầu trên chỉ chiều, bao quanh là một đường cong kín của điện trường xoáy với hai mũi tên chỉ chiều",
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
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
