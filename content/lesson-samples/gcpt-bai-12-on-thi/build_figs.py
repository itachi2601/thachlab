#!/usr/bin/env python3
"""Sinh hình SVG cho GCPT – Bài 12 (Ôn thi), thay <!--FIGn--> trong theory.src.html → theory.html."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import chevron  # noqa: E402

FONT = 'font-family="system-ui, sans-serif" font-size="13"'
R, B, O, G = "#dc2626", "#0284c7", "#ea580c", "#16a34a"
BOX = 'fill="#94a3b8" fill-opacity="0.18" stroke="currentColor" stroke-width="1.6"'


def T(x, y, s, c="currentColor", size=13, w="400", a="start"):
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{a}">{s}</text>'


def svg(h, label, body):
    return (f'<svg viewBox="0 0 420 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}" {FONT}>'
            + "".join(body) + "</svg>")


def fig(s, cap):
    return f'<figure class="fig" data-tl="1">{s}<figcaption>{cap}</figcaption></figure>'


def fig1():
    rows = [("Chọn", "1 điểm", "Gọi tên một công nghệ", B),
            ("Vì", "1,5 điểm", "≥ 3 lý do lấy từ dữ kiện của đề", G),
            ("Loại", "1 điểm", "≥ 2 công nghệ khác, mỗi cái một lý do", R),
            ("Lưu", "0,5 điểm", "Điều kiện, thông số, an toàn", O)]
    o, y = [], 8
    for name, pts, txt, c in rows:
        o.append(f'<rect x="14" y="{y}" width="392" height="52" rx="6" fill="{c}" fill-opacity="0.12" stroke="{c}" stroke-width="1.8"/>')
        o.append(T(28, y + 32, name, c=c, size=18, w="700"))
        o.append(T(96, y + 23, pts, w="700"))
        o.append(T(96, y + 42, txt, size=12.5))
        y += 60
    return fig(svg(y + 4, "Bốn phần của câu chọn công nghệ và điểm", o),
               "Hình 1. Câu chọn công nghệ 4 điểm: Chọn – Vì – Loại – Lưu.")


def fig2():
    parts = [("Đọc, gạch dữ kiện", 15, B), ("Lập bảng 5 bước", 20, G), ("Viết", 55, O), ("Soát", 10, R)]
    o = [T(14, 18, "Gợi ý chia thời gian cho câu chọn công nghệ", w="700", size=12.5)]
    x, W = 14, 392
    for name, pct, c in parts:
        w = W * pct / 100
        o.append(f'<rect x="{x:.1f}" y="30" width="{w:.1f}" height="38" fill="{c}" fill-opacity="0.25" stroke="{c}" stroke-width="1.6"/>')
        o.append(T(x + w / 2, 54, f"{pct}%", w="700", a="middle"))
        x += w
    o.append(T(14, 92, "Đọc 15%", c=B, size=12))
    o.append(T(14 + W * 0.15 + 4, 108, "Bảng 20%", c=G, size=12))
    o.append(T(14 + W * 0.35 + 60, 92, "Viết 55%", c=O, size=12))
    o.append(T(406, 108, "Soát 10%", c=R, size=12, a="end"))
    return fig(svg(120, "Chia thời gian cho câu chọn công nghệ", o),
               "Hình 2. Lập bảng 5 bước trước khi viết giúp không bỏ sót phần Loại.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in (("<!--FIG1-->", fig1), ("<!--FIG2-->", fig2)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
