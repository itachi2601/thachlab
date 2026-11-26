#!/usr/bin/env python3
"""Sinh hình SVG cho GCPT – Bài 7 (siêu âm), thay <!--FIGn--> trong theory.src.html → theory.html.
Màu: xanh = nước/tia, cam = hạt mài, xám = vật rắn, đỏ = hướng chuyển động."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import chevron  # noqa: E402

FONT = 'font-family="system-ui, sans-serif" font-size="13"'
R, B, O = "#dc2626", "#0284c7", "#ea580c"
SOLID = 'fill="#94a3b8" fill-opacity="0.4" stroke="currentColor" stroke-width="1.8"'
PLATE = 'fill="#94a3b8" fill-opacity="0.3" stroke="currentColor" stroke-width="1.8"'


def T(x, y, s, c="currentColor", size=13, w="400", a="start"):
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{a}">{s}</text>'


def ar(x1, y1, x2, y2, c, w=2.4, L=10):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"/>'
            + chevron(x2, y2, x2 - x1, y2 - y1, c, w, L))


def poly(pts, attr):
    return f'<polygon points="{" ".join(f"{x},{y}" for x, y in pts)}" {attr}/>'


def svg(h, label, body):
    return (f'<svg viewBox="0 0 420 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}" {FONT}>'
            + "".join(body) + "</svg>")


def fig(s, cap):
    return f'<figure class="fig" data-tl="1">{s}<figcaption>{cap}</figcaption></figure>'


def fig1():
    o = []
    o.append(f'<rect x="120" y="18" width="60" height="36" {SOLID}/>')
    o.append(T(190, 32, "Bộ phát siêu âm", size=12.5))
    o.append(T(190, 48, "khoảng 20 kHz", size=12.5))
    o.append(poly([(125, 54), (175, 54), (158, 118), (142, 118)], SOLID))
    o.append(T(190, 88, "Cần khuếch đại (horn)", size=12.5))
    o.append(f'<rect x="142" y="118" width="16" height="36" {SOLID}/>')
    o.append(T(190, 128, "Dụng cụ", size=12.5))
    o.append(T(190, 144, "(thép mềm)", size=12.5))
    o.append(f'<line x1="104" y1="122" x2="104" y2="152" stroke="{R}" stroke-width="2.2"/>' + chevron(104, 122, 0, -1, R, 2.2, 9) + chevron(104, 152, 0, 1, R, 2.2, 9))
    o.append(T(12, 120, "Rung dọc", c=R, size=12.5, w="700"))
    o.append(T(12, 136, "vài chục µm", c=R, size=12.5))
    for x in (140, 148, 156, 164):
        o.append(f'<circle cx="{x}" cy="161" r="3" fill="{O}"/>')
    o.append(T(190, 166, "Bùn hạt mài", c=O, size=12.5, w="700"))
    o.append(f'<rect x="70" y="170" width="160" height="40" {PLATE}/>')
    o.append(T(240, 194, "Phôi giòn", size=12.5))
    o.append(T(240, 210, "(kính, gốm, silic)", size=12.5))
    return fig(svg(232, "Sơ đồ máy USM", o),
               "Hình 1. Sơ đồ máy USM: bộ phát, cần khuếch đại, dụng cụ rung dọc; giữa dụng cụ và phôi là bùn hạt mài (cam).")


def fig2():
    o = []
    o.append(f'<rect x="40" y="56" width="170" height="26" {SOLID}/>')
    for x in (80, 170):
        o.append(ar(x, 14, x, 52, R, 2.2, 9))
    o.append(T(220, 74, "Dụng cụ rung", size=12.5))
    for x, y in ((80, 96), (125, 100), (170, 96)):
        o.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{O}" fill-opacity="0.8" stroke="{O}" stroke-width="1.5"/>')
    o.append(T(220, 98, "Hạt mài", c=O, size=12.5, w="700"))
    d = "M40 112 L68 112 L80 130 L92 112 L112 112 L125 136 L138 112 L158 112 L170 128 L182 112 L210 112 L210 176 L40 176 Z"
    o.append(f'<path d="{d}" {PLATE}/>')
    o.append(T(220, 130, "Vi nứt → bong", size=12.5))
    o.append(T(220, 146, "mảnh rất nhỏ", size=12.5))
    o.append(T(220, 170, "Phôi giòn", size=12.5))
    return fig(svg(196, "Hạt mài đập vào phôi giòn", o),
               "Hình 2. Dụng cụ rung đẩy hạt mài đập xuống; mỗi điểm hạt đập, phôi giòn vi nứt và bong mảnh nhỏ.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in (("<!--FIG1-->", fig1), ("<!--FIG2-->", fig2)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
