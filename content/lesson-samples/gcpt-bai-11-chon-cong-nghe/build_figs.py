#!/usr/bin/env python3
"""Sinh hình SVG cho GCPT – Bài 11 (Chọn công nghệ gia công), thay <!--FIGn--> trong theory.src.html → theory.html.
Chạy lại an toàn: luôn đọc từ theory.src.html.
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import chevron  # noqa: E402

FONT = 'font-family="system-ui, sans-serif" font-size="13"'
R, B, O = "#dc2626", "#0284c7", "#ea580c"
BOX = 'fill="#94a3b8" fill-opacity="0.18" stroke="currentColor" stroke-width="1.6"'


def T(x, y, s, c="currentColor", size=13, w="400", a="start"):
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{a}">{s}</text>'


def svg(h, label, body):
    return (f'<svg viewBox="0 0 420 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}" {FONT}>'
            + "".join(body) + "</svg>")


def fig(s, cap):
    return f'<figure class="fig" data-tl="1">{s}<figcaption>{cap}</figcaption></figure>'


def arrow_down(x, y1, y2, c="currentColor"):
    return f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{c}" stroke-width="2"/>' + chevron(x, y2, 0, 1, c, 2, 8)


def fig1():
    steps = [("1  Vật liệu", "Dẫn điện? Cứng, giòn, chịu nhiệt?"),
             ("2  Hình học", "Xuyên suốt hay hốc? 2D hay 3D? Dày bao nhiêu?"),
             ("3  Chính xác", "Dung sai và độ nhám yêu cầu?"),
             ("4  Số lượng", "Một chiếc hay loạt? Dụng cụ riêng có đáng?"),
             ("5  Ràng buộc", "Cấm nhiệt, hoá chất, tia? An toàn?")]
    o = [T(210, 18, "Cổng vào: truyền thống làm được và đủ rẻ thì dừng", c=O, size=12.5, w="700", a="middle")]
    y = 56
    o.append(arrow_down(210, 26, 48, O))
    for i, (a, b) in enumerate(steps):
        o.append(f'<rect x="20" y="{y}" width="380" height="46" rx="6" {BOX}/>')
        o.append(T(34, y + 20, a, w="700"))
        o.append(T(34, y + 37, b, size=12.5))
        if i < 4:
            o.append(arrow_down(210, y + 46, y + 58))
        y += 58
    o.append(T(210, y + 18, "→ chọn công nghệ · lý do chọn · lý do loại", c=B, size=13, w="700", a="middle"))
    return fig(svg(y + 30, "Quy trình 5 bước chọn công nghệ gia công", o),
               "Hình 1. Năm bước theo thứ tự: Vật – Hình – Chính – Số – Ràng. Mỗi bước loại bớt công nghệ.")


def leaf(x, y, w, lines, c="currentColor"):
    h = 12 + 16 * len(lines)
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" {BOX}/>'
    for i, ln in enumerate(lines):
        s += T(x + 8, y + 18 + 16 * i, ln, c=c, size=12, w="700" if i == 0 else "400")
    return s, h


def fig2():
    o = []
    o.append(f'<rect x="130" y="8" width="160" height="30" rx="6" fill="{B}" fill-opacity="0.18" stroke="{B}" stroke-width="1.6"/>')
    o.append(T(210, 28, "Vật liệu dẫn điện?", w="700", a="middle"))
    o.append(f'<line x1="170" y1="38" x2="105" y2="58" stroke="currentColor" stroke-width="1.6"/>')
    o.append(f'<line x1="250" y1="38" x2="315" y2="58" stroke="currentColor" stroke-width="1.6"/>')
    o.append(T(120, 50, "Có", c=B, w="700", a="end"))
    o.append(T(300, 50, "Không", c=O, w="700"))
    left = [["WEDM", "xuyên suốt, biên dạng 2D"],
            ["EDM chìm", "hốc, khoang 3D, ít chiếc"],
            ["ECM", "hình 3D, loạt lớn"],
            ["Laser", "tấm mỏng, cho phép nhiệt"],
            ["Tia nước hạt mài", "tấm vừa, cấm nhiệt"],
            ["Plasma", "tấm dày, dung sai thô"],
            ["Ăn mòn hoá học", "lá mỏng, nhiều lỗ, loạt lớn"]]
    right = [["Tia nước hạt mài", "composite, cấm nhiệt"],
             ["USM", "giòn, cứng: kính, gốm"],
             ["Laser", "nhựa, tấm mỏng chịu nhiệt"]]
    y = 62
    for ln in left:
        s, h = leaf(14, y, 196, ln)
        o.append(s)
        y += h + 6
    yl = y
    y = 62
    for ln in right:
        ln2 = ln
        s, h = leaf(222, y, 190, ln2, c="currentColor")
        o.append(s)
        y += h + 6
    return fig(svg(max(yl, y) + 8, "Bản đồ chọn công nghệ lối vào", o),
               "Hình 2. Chỉ là lối vào theo vật liệu, chưa phải đáp án: còn phải qua bước chính xác, số lượng, ràng buộc.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in (("<!--FIG1-->", fig1), ("<!--FIG2-->", fig2)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
