#!/usr/bin/env python3
"""Hình SVG cho GCPT – Bài 3 (WEDM). Chạy: python3 build_figs.py (đọc theory.src.html → theory.html)."""
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import chevron  # noqa: E402

FONT = 'font-family="system-ui, sans-serif" font-size="13"'
R, B, O = "#dc2626", "#0284c7", "#ea580c"   # đỏ: điện/chuyển động chính · xanh: điện môi/chạy dao · cam: vật liệu bóc/nhiệt
GR = "#94a3b8"
WP = f'fill="{GR}" fill-opacity="0.35" stroke="currentColor" stroke-width="1.8"'
LQ = f'fill="{B}" fill-opacity="0.13"'


def T(x, y, s, c="currentColor", size=13, w="400", a="start"):
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{a}">{s}</text>'


def ar(x1, y1, x2, y2, c, w=2.4, L=10, both=False):
    s = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"/>'
    s += chevron(x2, y2, x2 - x1, y2 - y1, c, w, L)
    if both:
        s += chevron(x1, y1, x1 - x2, y1 - y2, c, w, L)
    return s


def rect(x, y, w, h, attr=WP, rx=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" {attr}/>'


def line(x1, y1, x2, y2, c="currentColor", w=1.6, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d}/>'


def poly(pts, attr):
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" {attr}/>'


def svg(h, label, body):
    return (f'<svg viewBox="0 0 420 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}" {FONT}>'
            + "".join(body) + "</svg>")


def fig(s, cap):
    return f'<figure class="fig" data-tl="1">{s}<figcaption>{cap}</figcaption></figure>'


def build(figs):
    src = (HERE / "theory.src.html").read_text(encoding="utf8")
    for i, f in enumerate(figs, 1):
        tag = f"<!--FIG{i}-->"
        assert src.count(tag) == 1, tag
        src = src.replace(tag, f())
    assert "<!--FIG" not in src
    (HERE / "theory.html").write_text(src, encoding="utf8")
    print("đã ghi theory.html")


# Hình 1: sơ đồ cắt dây (nhìn nghiêng từ bên)
def fig1():
    o = [rect(110, 100, 200, 50, WP)]                                   # phôi
    o.append(T(150, 129, "phôi", size=12.5, w="700", a="middle"))
    o.append(rect(190, 74, 40, 24, 'fill="#475569" fill-opacity="0.5" stroke="currentColor" stroke-width="1.6"', 3))   # dẫn trên
    o.append(rect(190, 152, 40, 24, 'fill="#475569" fill-opacity="0.5" stroke="currentColor" stroke-width="1.6"', 3))  # dẫn dưới
    o.append(T(236, 90, "ống dẫn trên", size=11.5))
    o.append(T(236, 168, "ống dẫn dưới", size=11.5))
    # dây
    o.append(line(210, 20, 210, 74, R, 2.4))
    o.append(line(210, 98, 210, 152, R, 2.4))
    o.append(line(210, 176, 210, 222, R, 2.4))
    o.append(f'<circle cx="210" cy="16" r="12" fill="none" stroke="currentColor" stroke-width="1.6"/>')
    o.append(f'<circle cx="210" cy="228" r="12" fill="none" stroke="currentColor" stroke-width="1.6"/>')
    o.append(T(190, 20, "cuộn cấp", size=11.5, a="end"))
    o.append(T(190, 232, "cuộn thu", size=11.5, a="end"))
    o.append(ar(224, 56, 224, 74, R, 1.8, 8))
    o.append(T(232, 50, "dây chạy liên tục", R, 12, "700"))
    # nước phun
    for xx in (200, 220):
        o.append(line(xx, 98, xx - 6 if xx < 210 else xx + 6, 106, B, 1.6))
        o.append(line(xx, 152, xx - 6 if xx < 210 else xx + 6, 146, B, 1.6))
    o.append(T(24, 70, "nước khử ion", B, 12, "700"))
    o.append(T(24, 85, "phun qua ống dẫn", B, 11.5))
    o.append(ar(126, 88, 188, 102, B, 1.4, 7))
    # bàn X-Y
    o.append(ar(110, 162, 60, 162, "#0f766e", 2, 9, both=True))
    o.append(T(60, 182, "bàn X–Y chạy", "#0f766e", 12, "700"))
    o.append(T(60, 196, "theo biên dạng", "#0f766e", 11.5))
    o.append(f'<polyline points="203,112 208,117 203,122 208,127 203,132" fill="none" stroke="{R}" stroke-width="1.8"/>')
    o.append(T(240, 120, "tia lửa", R, 12, "700"))
    o.append(T(240, 134, "ở khe cắt", size=11.5))
    return fig(svg(244, "Sơ đồ nguyên lý cắt dây WEDM", o),
               "Hình 1. Cắt dây. Đỏ: dây và tia lửa. Xanh: nước khử ion. Xanh lục: bàn máy mang phôi chạy theo biên dạng. Dây không chạm phôi; hình không theo tỉ lệ.")


# Hình 2: cắt thô rồi cắt tinh – bề mặt sau mỗi lượt
def fig2():
    o = []
    rows = [("Lượt 1: cắt thô", 50, 28, 7, "nhanh, chừa dư"),
            ("Lượt 2: cắt tinh", 126, 12, 4, "bóc lớp mỏng"),
            ("Lượt 3: tinh nữa", 202, 4, 2, "mịn, chính xác")]
    for name, y, allow, amp, note in rows:
        o.append(T(14, y - 10, name, size=12.5, w="700"))
        o.append(rect(14, y + 14, 392, 30, f'fill="{GR}" fill-opacity="0.3" stroke="none"', 0))
        pts = []
        for i in range(0, 393, 7):
            wob = amp * (1 if (i // 7) % 2 == 0 else -1) * (0.6 + 0.4 * math.sin(i / 17))
            pts.append((14 + i, y + 14 - allow + wob))
        o.append(poly(pts + [(406, y + 14), (14, y + 14)], f'fill="{O}" fill-opacity="0.35" stroke="{O}" stroke-width="1.6"'))
        o.append(line(14, y + 14, 406, y + 14, "currentColor", 1.6, "5 3"))
        o.append(T(300, y - 10, note, size=11.5))
    o.append(T(14, 276, "Nét đứt: biên dạng đúng. Cam: phần còn dư, nhám giảm dần.", size=11.5))
    return fig(svg(288, "Cắt thô rồi cắt tinh nhiều lượt", o),
               "Hình 3. Mỗi lượt dùng dòng nhỏ hơn, bóc lớp mỏng hơn: phần dư (cam) và độ nhám giảm dần về biên dạng đúng.")


# Hình 3: khe cắt và đường tâm dây
def fig3():
    o = [rect(20, 20, 150, 140, WP), rect(250, 20, 150, 140, WP)]
    o.append(rect(170, 20, 80, 140, 'fill="none" stroke="none"', 0))
    cx, cy, rd, g = 210, 90, 24, 16
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{rd}" fill="{R}" fill-opacity="0.3" stroke="{R}" stroke-width="2"/>')
    o.append(T(cx, cy + rd + 14, "dây", R, 12, "700", "middle"))
    o.append(T(95, 140, "phôi", size=12.5, w="700", a="middle"))
    o.append(T(325, 140, "phôi", size=12.5, w="700", a="middle"))
    o.append(ar(cx - rd, 176, cx + rd, 176, R, 1.6, 7, both=True))
    o.append(T(cx, 192, "d", R, 13, "700", "middle"))
    o.append(ar(cx - rd - g, 206, cx - rd, 206, B, 1.6, 7, both=True))
    o.append(T(cx - rd - g / 2, 222, "g", B, 13, "700", "middle"))
    o.append(ar(cx - rd - g, 236, cx + rd + g, 236, "currentColor", 1.6, 7, both=True))
    o.append(T(cx, 254, "W = d + 2g", "currentColor", 13, "700", "middle"))
    o.append(ar(cx, cy, cx + rd + g - 2, cy, "currentColor", 1.4, 6))
    o.append(T(cx + rd + g + 8, cy - 4, "d/2 + g", size=12, w="700"))
    o.append(T(cx + rd + g + 8, cy + 10, "tâm → biên", size=11))
    o.append(T(14, 276, "g: khe phóng điện hai bên dây; W: bề rộng khe cắt", size=11.5))
    return fig(svg(288, "Khe cắt rộng hơn đường kính dây", o),
               "Hình 2. Nhìn từ trên xuống. Dây tròn đường kính d, khe phóng điện g mỗi bên, bề rộng khe cắt W. Đường tâm dây phải cách biên d/2 + g. Khe g vẽ phóng to, không theo tỉ lệ.")


build([fig1, fig3, fig2])
