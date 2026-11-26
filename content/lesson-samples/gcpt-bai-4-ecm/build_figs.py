#!/usr/bin/env python3
"""Hình SVG cho GCPT – Bài 4 (ECM): thay <!--FIGn--> trong theory.src.html → theory.html.
Quy ước màu: đỏ = dòng điện / cực dương, xanh = dung dịch điện phân, cam = ion / khí.
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import chevron  # noqa: E402

FONT = 'font-family="system-ui, sans-serif" font-size="13"'
R, B, O = "#dc2626", "#0284c7", "#ea580c"
GR = 'fill="#94a3b8" fill-opacity="0.4" stroke="currentColor" stroke-width="1.8"'


def T(x, y, s, c="currentColor", size=13, w="400", a="start"):
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{a}">{s}</text>'


def ar(x1, y1, x2, y2, c, w=2.2, L=9):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"/>'
            + chevron(x2, y2, x2 - x1, y2 - y1, c, w, L))


def svg(h, label, body):
    return (f'<svg viewBox="0 0 420 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}" {FONT}>'
            + "".join(body) + "</svg>")


def fig(s, cap):
    return f'<figure class="fig" data-tl="1">{s}<figcaption>{cap}</figcaption></figure>'


def fig1():
    o = []
    o.append('<rect x="12" y="10" width="124" height="46" rx="6" fill="none" stroke="currentColor" stroke-width="1.8"/>')
    o.append(T(74, 29, "Nguồn một chiều", a="middle", size=12.5, w="700"))
    o.append(T(74, 47, "5 – 30 V", a="middle", size=12.5))
    o.append('<polyline points="136,33 210,33 210,70" fill="none" stroke="currentColor" stroke-width="1.8"/>')
    o.append(T(146, 26, "−", size=18, w="700"))
    o.append('<polyline points="30,56 30,208 70,208" fill="none" stroke="currentColor" stroke-width="1.8"/>')
    o.append(T(38, 76, "+", c=R, size=18, w="700"))
    # dụng cụ
    o.append(f'<rect x="170" y="70" width="80" height="26" {GR}/>')
    o.append(f'<rect x="186" y="96" width="48" height="34" {GR}/>')
    o.append(T(262, 88, "Dụng cụ", size=12.5, w="700"))
    o.append(T(262, 104, "(cực âm)", size=12.5))
    # phôi
    o.append('<rect x="70" y="170" width="290" height="76" fill="#94a3b8" fill-opacity="0.3" stroke="currentColor" stroke-width="1.8"/>')
    o.append(T(215, 232, "Phôi (cực dương)", c=R, a="middle", size=13, w="700"))
    # dòng dung dịch qua khe
    for y in (144, 153, 162):
        o.append(ar(76, y, 150, y, B))
        o.append(ar(300, y, 372, y, B))
    o.append(T(40, 134, "dung dịch điện phân", c=B, size=12.5, w="700"))
    # bọt khí H2
    for x, y in ((196, 138), (214, 142), (228, 136)):
        o.append(f'<circle cx="{x}" cy="{y}" r="3.2" fill="none" stroke="{O}" stroke-width="1.6"/>')
    # ion rời phôi
    for x in (190, 214, 238):
        o.append(ar(x, 168, x, 152, O, w=1.6, L=7))
    # khe hở: đường kích thước
    o.append('<line x1="262" y1="130" x2="262" y2="170" stroke="currentColor" stroke-width="1.2"/>')
    o.append('<line x1="256" y1="130" x2="268" y2="130" stroke="currentColor" stroke-width="1.2"/>')
    o.append('<line x1="256" y1="170" x2="268" y2="170" stroke="currentColor" stroke-width="1.2"/>')
    o.append(T(252, 120, "khe hở 0,1–0,5 mm", size=12.5, w="700"))
    # chú giải
    o.append(T(12, 268, "○ H₂↑: bọt khí sinh ra ở dụng cụ", c=O, size=12.5, w="700"))
    o.append(T(12, 286, "↑ Fe²⁺: ion rời bề mặt phôi", c=O, size=12.5, w="700"))
    return fig(svg(296, "Sơ đồ nguyên lý gia công điện hoá ECM", o),
               "Hình 1. Nguyên lý ECM: phôi (+) tan thành ion Fe²⁺, dụng cụ (−) sinh khí H₂; dung dịch điện phân chảy nhanh trong khe cuốn bùn, khí và nhiệt (khe vẽ phóng to).")


def panel(x0, bump, title):
    o = [T(x0, 20, title, w="700")]
    top, base = 60, 150
    o.append(f'<rect x="{x0}" y="{top-28}" width="190" height="28" {GR}/>')
    o.append(T(x0 + 95, top - 9, "dụng cụ (−)", a="middle", size=12.5))
    if bump:
        pts = f"{x0},{base} {x0+60},{base} {x0+75},{base-28} {x0+115},{base-28} {x0+130},{base} {x0+190},{base}"
    else:
        pts = f"{x0},{base} {x0+190},{base}"
    o.append(f'<polygon points="{pts} {x0+190},{base+36} {x0},{base+36}" fill="#94a3b8" fill-opacity="0.3" stroke="currentColor" stroke-width="1.8"/>')
    o.append(T(x0 + 95, base + 26, "phôi (+)", c=R, a="middle", size=12.5))
    xs = (x0 + 18, x0 + 40, x0 + 85, x0 + 95, x0 + 105, x0 + 150, x0 + 172) if bump else (x0 + 22, x0 + 55, x0 + 95, x0 + 135, x0 + 168)
    for x in xs:
        hot = bump and (x0 + 75 <= x <= x0 + 115)
        o.append(ar(x, top + 3, x, (base - 28 - 3) if hot else (base - 3), R, w=2.8 if hot else 1.6, L=8))
    return o


def fig2():
    o = panel(8, True, "a) Lúc đầu: có chỗ gồ")
    o += panel(222, False, "b) Sau một lúc: khe đều")
    o.append(T(8, 224, "Khe hẹp → dòng đậm", c=R, size=12.5, w="700"))
    o.append(T(8, 241, "→ tan nhanh", c=R, size=12.5, w="700"))
    o.append(T(222, 224, "Khe đều; phôi “sao chép”", size=12.5, w="700"))
    o.append(T(222, 241, "hình ngược của dụng cụ", size=12.5, w="700"))
    return fig(svg(252, "Khe hở tự san đều khi gia công điện hoá", o),
               "Hình 2. Chỗ gồ làm khe hẹp, dòng điện (mũi tên đỏ) đậm hơn nên tan nhanh hơn. Khe dần đều và bề mặt phôi có hình ngược với dụng cụ.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in (("<!--FIG1-->", fig1), ("<!--FIG2-->", fig2)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
