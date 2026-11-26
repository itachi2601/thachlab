#!/usr/bin/env python3
"""Hình SVG cho GCPT – Bài 5 (laser): thay <!--FIGn--> trong theory.src.html → theory.html.
Quy ước màu: đỏ = chùm laser, xanh = khí trợ / dòng thổi, cam = vùng ảnh hưởng nhiệt (HAZ).
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
    # chùm vào
    o.append(f'<rect x="190" y="14" width="40" height="40" fill="{R}" fill-opacity="0.35" stroke="{R}" stroke-width="1.4"/>')
    o.append(ar(210, 12, 210, 48, R, w=2.2))
    o.append(T(240, 30, "chùm laser", c=R, size=12.5, w="700"))
    # thấu kính
    o.append('<ellipse cx="210" cy="64" rx="46" ry="9" fill="#94a3b8" fill-opacity="0.35" stroke="currentColor" stroke-width="1.8"/>')
    o.append(T(262, 68, "thấu kính hội tụ", size=12.5))
    # chùm hội tụ
    o.append(f'<polygon points="168,70 252,70 214,172 206,172" fill="{R}" fill-opacity="0.35" stroke="{R}" stroke-width="1.4"/>')
    # đầu cắt
    o.append('<polyline points="150,80 150,128 192,160 228,160 270,128 270,80" fill="none" stroke="currentColor" stroke-width="1.8"/>')
    o.append(T(280, 110, "đầu cắt", size=12.5))
    # khí trợ vào
    o.append(ar(70, 100, 148, 100, B, w=2.2))
    o.append(T(10, 90, "khí trợ (O₂ / N₂)", c=B, size=12.5, w="700"))
    for x in (178, 242):
        o.append(ar(x, 112, x + (8 if x < 210 else -8), 150, B, w=1.6, L=7))
    # phôi + vết cắt
    o.append('<rect x="60" y="172" width="145" height="50" fill="#94a3b8" fill-opacity="0.3" stroke="currentColor" stroke-width="1.8"/>')
    o.append('<rect x="215" y="172" width="145" height="50" fill="#94a3b8" fill-opacity="0.3" stroke="currentColor" stroke-width="1.8"/>')
    o.append(f'<rect x="192" y="172" width="13" height="50" fill="{O}" fill-opacity="0.4"/>')
    o.append(f'<rect x="215" y="172" width="13" height="50" fill="{O}" fill-opacity="0.4"/>')
    o.append(T(100, 202, "phôi", a="middle", size=13, w="700"))
    # dòng thổi xuống
    o.append(ar(210, 226, 210, 252, B, w=2.2))
    o.append(T(222, 244, "kim loại lỏng + khí thổi ra", c=B, size=12.5, w="700"))
    o.append(T(238, 190, "kerf", size=12.5, w="700"))
    # chú giải
    o.append(f'<rect x="12" y="266" width="14" height="12" fill="{O}" fill-opacity="0.4"/>')
    o.append(T(32, 277, "HAZ: vùng nóng hai bên vết cắt, không chảy", c=O, size=12.5, w="700"))
    return fig(svg(290, "Sơ đồ cắt bằng laser có khí trợ", o),
               "Hình 1. Cắt laser: thấu kính hội tụ chùm xuống điểm nhỏ; khí trợ đồng trục thổi kim loại lỏng ra khỏi vết cắt; hai bên vết cắt có vùng ảnh hưởng nhiệt (HAZ, vẽ phóng to).")


def panel(x0, h, d, inten):
    o = []
    o.append(f'<polygon points="{x0},30 {x0+110},30 {x0+55+h},120 {x0+110},210 {x0},210 {x0+55-h},120" fill="{R}" fill-opacity="0.3" stroke="{R}" stroke-width="1.6"/>')
    o.append(f'<line x1="{x0+55-h}" y1="120" x2="{x0+55+h}" y2="120" stroke="currentColor" stroke-width="2.4"/>')
    o.append(T(x0 + 55, 22, "chùm vào, cùng 3 kW", a="middle", size=12))
    o.append(T(x0 + 55, 238, d, a="middle", size=13, w="700"))
    o.append(T(x0 + 55, 256, inten, c=R, a="middle", size=13, w="700"))
    return o


def fig2():
    o = panel(30, 14, "d = 0,2 mm", "I ≈ 9,5·10⁶ W/cm²")
    o += panel(250, 7, "d = 0,1 mm", "I ≈ 3,8·10⁷ W/cm² (×4)")
    return fig(svg(268, "Điểm hội tụ nhỏ một nửa thì cường độ gấp bốn", o),
               "Hình 2. Cùng công suất, đường kính điểm hội tụ giảm một nửa thì diện tích giảm bốn lần, cường độ tăng bốn lần (điểm hội tụ vẽ phóng to).")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in (("<!--FIG1-->", fig1), ("<!--FIG2-->", fig2)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
