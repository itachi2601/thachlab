#!/usr/bin/env python3
"""Hình SVG cho GCPT – Hướng dẫn thuyết trình nhóm, thay <!--FIGn--> trong theory.src.html → theory.html. Chạy lại an toàn."""
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


def fig1():
    # Thanh 12 phút nói + 3 phút hỏi đáp; mỗi phút 24 px (15 phút = 360 px)
    parts = [("Mở", 1, GR), ("Nguyên lý", 3, R), ("Thiết bị", 2, GR), ("Vật liệu", 2, GR),
             ("So sánh", 2, R), ("Ví dụ", 2, GR), ("Hỏi đáp", 3, B)]
    x0, y0, u, h = 30, 46, 24, 46
    b = [T(210, 20, "12 phút nói + 3 phút hỏi đáp", w="700", a="middle")]
    x = x0
    t = 0
    for name, m, c in parts:
        w = m * u
        op = "0.30" if c != GR else "0.22"
        b.append(rect(x, y0, w, h, f'fill="{c}" fill-opacity="{op}" stroke="currentColor" stroke-width="1.4"'))
        if m >= 2:
            b.append(T(x + w / 2, y0 + 20, name, size=10.5, w="700", a="middle"))
            b.append(T(x + w / 2, y0 + 36, f"{m} ph", size=11.5, a="middle"))
        else:
            b.append(T(x + w / 2, y0 + 28, "Mở", size=10.5, w="700", a="middle"))
        b.append(T(x, y0 + h + 16, str(t), size=11, a="middle"))
        x += w
        t += m
    b.append(T(x, y0 + h + 16, str(t), size=11, a="middle"))
    b.append(line(x0 + 12 * u, y0 - 8, x0 + 12 * u, y0 + h + 4, "currentColor", 2, "4 3"))
    # Chú thích: mỗi ý một dòng
    b.append(rect(30, 136, 14, 14, f'fill="{R}" fill-opacity="0.30" stroke="currentColor" stroke-width="1.2"'))
    b.append(T(52, 148, "Đỏ: hai phần chiếm 60% điểm (5 phút)", size=12.5))
    b.append(rect(30, 160, 14, 14, f'fill="{B}" fill-opacity="0.30" stroke="currentColor" stroke-width="1.2"'))
    b.append(T(52, 172, "Xanh: hỏi đáp, cả nhóm cùng đứng", size=12.5))
    b.append(line(30, 192, 44, 192, "currentColor", 2, "4 3"))
    b.append(T(52, 196, "Nét đứt: hết 12 phút nói", size=12.5))
    return fig(svg(210, "Khung thời gian 12 phút thuyết trình chia theo rubric", b),
               "Hình 1. Khung giờ mẫu. Phút nằm dưới thanh. Phần đỏ ăn nhiều điểm nhất nên được nhiều phút nhất.")


def slide(x, y, w, h, bad):
    s = [rect(x, y, w, h, 'fill="#f8fafc" fill-opacity="0.9" stroke="currentColor" stroke-width="1.8"', 4)]
    if bad:
        s.append(f'<text x="{x + 10}" y="{y + 22}" fill="#334155" font-size="13" font-weight="700">Nguyên lý EDM</text>')
        for i in range(9):
            ww = w - 20 - (i * 13) % 50
            s.append(f'<rect x="{x + 10}" y="{y + 34 + i * 10}" width="{ww}" height="4" rx="2" fill="#64748b" fill-opacity="0.6"/>')
    else:
        s.append(f'<text x="{x + 10}" y="{y + 18}" fill="#334155" font-size="10.5" font-weight="700">Tia lửa làm chảy từng điểm,</text>')
        s.append(f'<text x="{x + 10}" y="{y + 31}" fill="#334155" font-size="10.5" font-weight="700">nên phôi cứng mấy cũng được</text>')
        cx = x + w / 2
        # điện cực
        s.append(f'<rect x="{cx - 18}" y="{y + 40}" width="36" height="34" fill="{R}" fill-opacity="0.25" stroke="{R}" stroke-width="1.6"/>')
        # phôi
        s.append(f'<rect x="{x + 18}" y="{y + 84}" width="{w - 36}" height="26" fill="{GR}" fill-opacity="0.45" stroke="#334155" stroke-width="1.6"/>')
        # tia lửa
        for dx in (-10, 0, 10):
            s.append(f'<polyline points="{cx + dx},{y + 75} {cx + dx + 4},{y + 79} {cx + dx - 2},{y + 81} {cx + dx + 2},{y + 84}" fill="none" stroke="{O}" stroke-width="1.6"/>')
        s.append(f'<text x="{cx + 24}" y="{y + 60}" fill="#334155" font-size="10">điện cực</text>')
        s.append(f'<text x="{cx}" y="{y + 101}" fill="#334155" font-size="10" text-anchor="middle">phôi thép tôi</text>')
    return s


def fig2():
    w, h = 190, 122
    b = [T(12, 18, "a) Slide toàn chữ", size=12, w="700"),
         T(218, 18, "b) Tiêu đề là ý, thân là hình", size=12, w="700")]
    b += slide(12, 28, w, h, True)
    b += slide(218, 28, w, h, False)
    b.append(T(107, 172, "người nghe đọc, rồi chờ", size=12.5, a="middle"))
    b.append(T(313, 172, "người nghe nhìn hình,", size=12.5, a="middle"))
    b.append(T(313, 188, "nghe người nói giải thích", size=12.5, w="700", a="middle"))
    return fig(svg(200, "So sánh slide nhiều chữ và slide tiêu đề khẳng định kèm hình", b),
               "Hình 2. Cùng một ý về EDM. Slide b) đọc tiêu đề là biết kết luận; phần còn lại người nói giải thích trên hình.")


if __name__ == "__main__":
    build([fig1, fig2])
