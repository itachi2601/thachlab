#!/usr/bin/env python3
"""Sinh hình SVG cho GCPT – Bài 6 (tia nước), thay <!--FIGn--> trong theory.src.html → theory.html.
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
    o = [T(12, 20, "a) WJM", w="700"), T(222, 20, "b) AWJ", w="700")]
    # a) WJM
    o.append(ar(60, 30, 60, 56, B))
    o.append(T(72, 44, "Nước áp cao"))
    o.append(f'<rect x="40" y="58" width="40" height="22" {SOLID}/>')
    o.append(T(88, 72, "Lỗ phun", size=12.5))
    o.append(T(88, 88, "cỡ Ø 0,1–0,4 mm", size=12.5))
    o.append(f'<line x1="60" y1="80" x2="60" y2="198" stroke="{B}" stroke-width="2.5"/>')
    o.append(chevron(60, 200, 0, 1, B, 2.4, 10))
    o.append(f'<rect x="15" y="202" width="90" height="22" {PLATE}/>')
    o.append(T(112, 218, "Phôi mềm", size=12.5))
    o.append(T(12, 246, "xốp, cao su, thực phẩm", size=12.5))
    # b) AWJ
    o.append(ar(250, 30, 250, 56, B))
    o.append(T(262, 44, "Nước áp cao"))
    o.append(f'<rect x="230" y="58" width="40" height="18" {SOLID}/>')
    o.append(f'<rect x="232" y="76" width="36" height="28" fill="{O}" fill-opacity="0.25" stroke="currentColor" stroke-width="1.6"/>')
    o.append(ar(334, 92, 272, 92, O))
    o.append(T(284, 84, "Hạt mài", c=O, size=12.5, w="700"))
    o.append(T(284, 114, "Buồng trộn", size=12.5))
    o.append(f'<rect x="243" y="104" width="14" height="58" {SOLID}/>')
    o.append(T(266, 138, "Ống tập trung", size=12.5))
    o.append(T(266, 154, "cỡ Ø 0,7–1,2 mm", size=12.5))
    o.append(f'<line x1="250" y1="162" x2="250" y2="198" stroke="{B}" stroke-width="4"/>')
    for yy in (172, 184, 194):
        o.append(f'<circle cx="250" cy="{yy}" r="2.2" fill="{O}"/>')
    o.append(chevron(250, 200, 0, 1, B, 2.4, 10))
    o.append(f'<rect x="215" y="202" width="70" height="20" {PLATE}/>')
    o.append(T(292, 216, "Kim loại, đá,", size=12.5))
    o.append(T(292, 232, "kính, composite", size=12.5))
    o.append(f'<path d="M225 232 L225 262 L275 262 L275 232" fill="none" stroke="currentColor" stroke-width="1.8"/>')
    o.append(T(292, 256, "Bể hứng", size=12.5))
    return fig(svg(276, "Đầu cắt WJM và AWJ", o),
               "Hình 1. a) WJM chỉ có lỗ phun và tia nước. b) AWJ thêm buồng trộn và ống tập trung, hạt mài (cam) hoà vào tia.")


def fig2():
    o = [T(12, 20, "a) Độ côn", w="700"), T(222, 20, "b) Vệt trễ", w="700")]
    # a) mặt cắt vết cắt hình côn
    o.append(poly([(12, 74), (80, 74), (88, 180), (12, 180)], PLATE))
    o.append(poly([(112, 74), (190, 74), (190, 180), (104, 180)], PLATE))
    o.append(ar(96, 28, 96, 70, B))
    o.append(T(104, 52, "tia", c=B, size=12.5))
    o.append(T(12, 200, "Miệng vào rộng,", size=12.5))
    o.append(T(12, 216, "đáy hẹp hơn", size=12.5))
    # b) mặt vách vết cắt: vệt cong
    o.append(f'<rect x="225" y="74" width="180" height="106" {PLATE}/>')
    o.append(ar(300, 52, 380, 52, R))
    o.append(T(300, 44, "Hướng cắt", c=R, size=12.5, w="700"))
    for x0 in (290, 330, 370, 400):
        o.append(f'<path d="M{x0} 74 C{x0} 118 {x0 - 20} 148 {x0 - 45} 180" fill="none" stroke="{B}" stroke-width="1.8" stroke-dasharray="6 4"/>')
    o.append(T(222, 200, "Đáy cắt chậm hơn miệng:", size=12.5))
    o.append(T(222, 216, "vệt cong ngược hướng cắt", size=12.5))
    return fig(svg(232, "Độ côn và vệt trễ", o),
               "Hình 2. a) Tia loe và yếu dần khi đi sâu nên đáy vết cắt hẹp hơn miệng. b) Nhìn vách vết cắt, vệt tia (nét xanh) cong về phía sau.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in (("<!--FIG1-->", fig1), ("<!--FIG2-->", fig2)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
