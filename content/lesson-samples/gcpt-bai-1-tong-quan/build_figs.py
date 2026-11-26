#!/usr/bin/env python3
"""Hình SVG cho GCPT – Bài 1 (Tổng quan), thay <!--FIGn--> trong theory.src.html → theory.html. Chạy lại an toàn."""
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


# Hình 1: ba nhóm theo dạng năng lượng
def fig1():
    o = []
    cols = [(10, "Cơ", "va đập, mài mòn", [("Siêu âm", "USM"), ("Tia nước", "WJM / AWJ")], "#64748b"),
            (146, "Điện – nhiệt", "nóng chảy, bốc hơi", [("Xung điện", "EDM, WEDM"), ("Laser", "LBM"), ("Chùm điện tử", "EBM"), ("Plasma", "PAC")], R),
            (282, "Hoá – điện hoá", "hoà tan", [("Điện hoá", "ECM"), ("Hoá học", "CHM / PCM")], B)]
    for x, name, how, items, c in cols:
        o.append(rect(x, 10, 128, 44, f'fill="{c}" fill-opacity="0.16" stroke="{c}" stroke-width="1.8"', 8))
        o.append(T(x + 64, 29, name, c, 14, "700", "middle"))
        o.append(T(x + 64, 46, how, "currentColor", 11.5, "400", "middle"))
        for i, (a, b) in enumerate(items):
            y = 66 + i * 38
            o.append(rect(x, y, 128, 32, f'fill="none" stroke="{c}" stroke-width="1.2"', 6))
            o.append(T(x + 8, y + 14, a, size=12.5, w="700"))
            o.append(T(x + 8, y + 27, b, size=11.5))
    o.append(T(210, 232, "Gốc chung: bóc vật liệu không bằng lực cắt của dao cứng hơn phôi", size=12, w="700", a="middle"))
    return fig(svg(244, "Ba nhóm gia công phi truyền thống theo dạng năng lượng", o),
               "Hình 2. Ba nhóm theo dạng năng lượng bóc vật liệu. Mỗi công nghệ có một bài riêng (Bài 2–9).")


# Hình 2: góc trong khi phay và khi dùng điện cực
def fig2():
    o = [T(12, 20, "a) Phay: dao tròn", w="700"), T(222, 20, "b) Điện cực có góc", w="700")]
    for x0, sharp in ((12, False), (222, True)):
        o.append(rect(x0, 32, 186, 112, WP))
        rx = 2 if sharp else 22
        o.append(rect(x0 + 40, 52, 106, 72, f'fill="#f8fafc" fill-opacity="0.9" stroke="currentColor" stroke-width="1.8"', rx))
    o.append(f'<circle cx="{12 + 40 + 22}" cy="{52 + 22}" r="22" fill="{O}" fill-opacity="0.35" stroke="{O}" stroke-width="1.6" stroke-dasharray="4 3"/>')
    o.append(T(12 + 93, 168, "góc trong bo tròn,", size=12.5, a="middle"))
    o.append(T(12 + 93, 184, "bán kính ≥ bán kính dao", size=12.5, w="700", a="middle"))
    o.append(rect(222 + 40, 52, 36, 36, f'fill="{R}" fill-opacity="0.25" stroke="{R}" stroke-width="1.6"', 1))
    o.append(T(222 + 93, 168, "góc nhọn hơn nhiều,", size=12.5, a="middle"))
    o.append(T(222 + 93, 184, "chỉ còn khe phóng điện", size=12.5, w="700", a="middle"))
    return fig(svg(196, "So sánh góc trong khi phay và khi gia công bằng điện cực", o),
               "Hình 1. Nhìn từ trên xuống, hốc vuông trong phôi. Cam: dao phay tròn nằm ở góc. Đỏ: góc của điện cực in lên phôi.")


build([fig2, fig1])
