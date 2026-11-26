#!/usr/bin/env python3
"""Hình SVG cho GCPT – Bài 2 (EDM chìm). Chạy: python3 build_figs.py (đọc theory.src.html → theory.html)."""
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


# Hình 1: sơ đồ EDM chìm
def fig1():
    o = [rect(20, 70, 280, 150, LQ, 0)]                       # bể điện môi
    o.append(T(26, 134, "điện môi (dầu)", B, 12, "700"))
    o.append(rect(70, 184, 180, 36, WP))                      # phôi
    o.append(T(160, 206, "phôi", size=12.5, w="700", a="middle"))
    o.append(poly([(120, 40), (200, 40), (200, 120), (190, 150), (130, 150), (120, 120)],
                  'fill="#475569" fill-opacity="0.55" stroke="currentColor" stroke-width="1.8"'))
    o.append(T(160, 88, "điện cực", "#fff", 12.5, "700", "middle"))
    o.append(T(160, 104, "than chì/đồng", "#fff", 11, "400", "middle"))
    o.append(line(160, 20, 160, 40))
    o.append(ar(100, 46, 100, 110, B))
    o.append(T(94, 60, "tiến dần", B, 11.5, "700", "end"))
    # tia lửa
    o.append(f'<polyline points="150,150 156,160 148,168 158,176 152,184" fill="none" stroke="{R}" stroke-width="2.4"/>')
    o.append(ar(188, 168, 172, 168, R, 1.6, 8))
    o.append(T(194, 164, "tia lửa", R, 12, "700"))
    o.append(T(194, 178, "khe hở", size=11.5))
    # nguồn xung
    o.append(rect(318, 40, 90, 54, 'fill="none" stroke="currentColor" stroke-width="1.8"', 6))
    o.append(T(363, 62, "nguồn", size=12.5, w="700", a="middle"))
    o.append(T(363, 80, "xung", size=12.5, w="700", a="middle"))
    o.append(f'<polyline points="160,20 160,14 363,14 363,40" fill="none" stroke="{R}" stroke-width="1.8"/>')
    o.append(f'<polyline points="363,94 363,202 250,202" fill="none" stroke="{R}" stroke-width="1.8"/>')
    # dòng rửa
    o.append(ar(60, 168, 112, 168, B, 1.8, 9))
    o.append(T(54, 162, "dòng rửa", B, 11.5, "700", "end"))
    o.append(T(54, 176, "cuốn mạt", B, 11.5, "400", "end"))
    return fig(svg(232, "Sơ đồ nguyên lý EDM chìm", o),
               "Hình 1. EDM chìm. Đỏ: nguồn xung và tia lửa. Xanh: điện môi, dòng rửa và chuyển động tiến của điện cực. Điện cực không chạm phôi. Khe hở vẽ phóng to, không theo tỉ lệ.")


# Hình 2: dạng xung
def fig2():
    o = []
    x0, yb, yt = 40, 130, 50
    o.append(line(x0, 30, x0, yb + 6, w=1.4))
    o.append(line(x0, yb, 400, yb, w=1.4))
    o.append(chevron(400, yb, 1, 0, "currentColor", 1.4, 8))
    o.append(T(46, 28, "Dòng I", size=12.5, w="700"))
    o.append(T(400, yb + 16, "t", size=12.5, w="700", a="end"))
    pts, x = [(x0, yb)], x0 + 30
    for _ in range(3):
        pts += [(x, yb), (x, yt), (x + 60, yt), (x + 60, yb)]
        x += 60 + 40
    o.append(f'<polyline points="{" ".join(f"{a},{b}" for a, b in pts)} {x},{yb}" fill="none" stroke="{R}" stroke-width="2.4"/>')
    o.append(ar(x0 + 8, yb, x0 + 8, yt, "currentColor", 1.4, 7, both=True))
    o.append(T(x0 + 14, 94, "Ip", size=12.5, w="700"))
    o.append(ar(70, 150, 130, 150, B, 1.6, 8, both=True))
    o.append(T(100, 168, "Ton", B, 12.5, "700", "middle"))
    o.append(ar(130, 150, 170, 150, O, 1.6, 8, both=True))
    o.append(T(150, 168, "Toff", O, 12.5, "700", "middle"))
    o.append(T(40, 192, "Ip: dòng đỉnh · Ton: xung phóng điện · Toff: nghỉ để rửa mạt", size=12))
    return fig(svg(206, "Dạng xung dòng điện trong EDM", o),
               "Hình 2. Dòng điện chỉ chảy trong Ton. Toff đủ dài để điện môi cuốn mạt và hồi phục cách điện.")


# Hình 3: mặt cắt lớp tái đúc
def fig3():
    o = [rect(40, 30, 220, 120, f'fill="{GR}" fill-opacity="0.35" stroke="currentColor" stroke-width="1.8"', 0)]
    o.append(rect(40, 30, 220, 20, f'fill="{R}" fill-opacity="0.35" stroke="none"', 0))
    o.append(rect(40, 50, 220, 30, f'fill="{O}" fill-opacity="0.25" stroke="none"', 0))
    for xx in (80, 130, 190, 230):
        o.append(f'<polyline points="{xx},32 {xx - 3},42 {xx + 2},50" fill="none" stroke="currentColor" stroke-width="1"/>')
    o.append(line(40, 50, 260, 50, w=1, dash="4 3"))
    o.append(line(40, 80, 260, 80, w=1, dash="4 3"))
    o.append(T(270, 44, "lớp tái đúc", R, 12.5, "700"))
    o.append(T(270, 58, "giòn, vi nứt", size=11.5))
    o.append(T(270, 70, "(lớp trắng)", size=11.5))
    o.append(T(270, 100, "vùng ảnh hưởng nhiệt", O, 12.5, "700"))
    o.append(T(270, 114, "tôi lại / ram lại", size=11.5))
    o.append(T(270, 140, "nền vật liệu", size=12.5, w="700"))
    o.append(T(150, 24, "bề mặt sau EDM", size=12.5, w="700", a="middle"))
    o.append(T(40, 172, "Dày mỏng tuỳ xung: xung lớn → lớp dày hơn", size=12))
    return fig(svg(184, "Mặt cắt bề mặt sau EDM: lớp tái đúc và vùng ảnh hưởng nhiệt", o),
               "Hình 3. Mặt cắt thẳng đứng dưới bề mặt (phóng to, không theo tỉ lệ). Xung càng lớn, hai lớp trên càng dày.")


build([fig1, fig2, fig3])
