#!/usr/bin/env python3
"""Sinh hình SVG cho CNCTM 1 – Bài 9 (Gia công mặt tròn xoay trong), thay <!--FIGn--> trong theory.src.html → theory.html.
Dùng: python3 build_figs.py  (chạy lại an toàn: luôn đọc từ theory.src.html)
Quy ước màu: đỏ = chuyển động chính, xanh = chạy dao, cam = dao/phoi, xám = phôi, nâu xám = đá mài.
"""
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import chevron, arc_pts  # noqa: E402

FONT = 'font-family="system-ui, sans-serif" font-size="13"'
R, B, O = "#dc2626", "#0284c7", "#ea580c"
WP = 'fill="#94a3b8" fill-opacity="0.35" stroke="currentColor" stroke-width="1.8"'
STONE = 'fill="#a8a29e" fill-opacity="0.5" stroke="currentColor" stroke-width="1.6"'


def T(x, y, s, c="currentColor", size=13, w="400", a="start"):
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{a}">{s}</text>'


def ar(x1, y1, x2, y2, c, w=2.4, L=10, both=False):
    s = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"/>'
    s += chevron(x2, y2, x2 - x1, y2 - y1, c, w, L)
    if both:
        s += chevron(x1, y1, x1 - x2, y1 - y2, c, w, L)
    return s


def rot(cx, cy, rx, ry, t0, t1, c=R, w=2.4, L=10):
    p = arc_pts(cx, cy, rx, ry, t0, t1, 40)
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in p)
    (xa, ya), (xb, yb) = p[-2], p[-1]
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}"/>' + chevron(xb, yb, xb - xa, yb - ya, c, w, L)


def poly(pts, attr):
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" {attr}/>'


def svg(h, label, body):
    return (f'<svg viewBox="0 0 420 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}" {FONT}>'
            + "".join(body) + "</svg>")


def fig(s, cap):
    return f'<figure class="fig" data-tl="1">{s}<figcaption>{cap}</figcaption></figure>'



HOLE = 'fill="#94a3b8" fill-opacity="0.35" stroke="currentColor" stroke-width="1.6"'
AXIS = 'stroke="currentColor" stroke-width="1" stroke-dasharray="8 3 2 3"'


# Hình 1: khoan – mũi khoan quay, tiến dọc trục
def fig1():
    o = [poly([(40, 110), (186, 110), (186, 150), (210, 166), (234, 150), (234, 110), (380, 110), (380, 190), (40, 190)], WP)]
    o.append(poly([(186, 30), (234, 30), (234, 150), (210, 166), (186, 150)], f'fill="{O}" fill-opacity="0.25" stroke="{O}" stroke-width="1.8"'))
    for y in (44, 76, 108):
        o.append(f'<line x1="186" y1="{y + 18}" x2="234" y2="{y}" stroke="{O}" stroke-width="1.4"/>')
    o.append(rot(210, 52, 40, 9, 20, 160))
    o += [T(262, 36, "mũi khoan quay:", R, 12, "700"), T(262, 52, "chuyển động chính", R, 12)]
    o.append(ar(256, 66, 256, 100, B))
    o += [T(268, 82, "tiến dọc trục:", B, 12, "700"), T(268, 98, "chạy dao", B, 12)]
    o += [T(48, 182, "phôi", size=12, w="700"), T(176, 70, "mũi khoan", O, 12, "700", a="end")]
    return fig(svg(200, "Sơ đồ khoan lỗ", o),
               "Hình 1. Khoan trên máy khoan: mũi khoan quay là chuyển động chính (đỏ), tiến dọc trục là chạy dao (xanh).")


# Hình 2: ba sai hỏng khi khoan (mặt cắt dọc lỗ thông)
def fig2():
    o = []
    cases = (("a) Xiên", (50, 80, 68, 98), "đường tâm nghiêng"),
             ("b) Lay rộng", (44, 86, 44, 86), "lỗ to hơn mũi khoan"),
             ("c) Lệch tâm", (62, 92, 62, 92), "tâm lỗ lệch vị trí"))
    for i, (title, (lt, rt, lb, rb), note) in enumerate(cases):
        x0 = 4 + 138 * i
        o.append(T(x0 + 6, 22, title, w="700"))
        o.append(poly([(x0 + 10, 40), (x0 + lt, 40), (x0 + lb, 150), (x0 + 10, 150)], WP))
        o.append(poly([(x0 + rt, 40), (x0 + 124, 40), (x0 + 124, 150), (x0 + rb, 150)], WP))
        o.append(f'<line x1="{x0 + 67}" y1="32" x2="{x0 + 67}" y2="158" {AXIS}/>')
        if i == 1:                                   # đường kính mũi khoan
            for x in (52, 82):
                o.append(f'<line x1="{x0 + x}" y1="40" x2="{x0 + x}" y2="150" stroke="{O}" stroke-width="1.4" stroke-dasharray="4 3"/>')
        o.append(T(x0 + 6, 176, note, size=12))
    o.append(T(10, 198, "Nét chấm gạch: đường tâm đúng.", size=12))
    o.append(T(10, 214, "Nét đứt cam: đường kính mũi khoan.", O, 12))
    return fig(svg(224, "Ba sai hỏng khi khoan: lỗ xiên, lỗ lay rộng, lỗ lệch tâm", o),
               "Hình 2. Mặt cắt dọc lỗ thông. Phần xám là phôi; khoảng trống giữa là lỗ.")


# Hình 3: mặt đầu dao khoan, khoét, doa (nhìn dọc trục)
def fig3():
    o = []
    for cx, n, name, l1, l2 in ((70, 2, "Mũi khoan", "2 lưỡi", "cấp 14 – 12"),
                                 (210, 3, "Mũi khoét", "3 – 4 lưỡi", "cấp 12 – 9"),
                                 (350, 8, "Dao doa", "nhiều lưỡi", "cấp 10 – 6")):
        cy = 74
        o.append(f'<circle cx="{cx}" cy="{cy}" r="44" fill="{O}" fill-opacity="0.15" stroke="{O}" stroke-width="1.6"/>')
        r_in = 10 if n == 2 else 18
        for k in range(n):
            a = math.radians(90 + 360 * k / n)
            o.append(f'<line x1="{cx + r_in * math.cos(a):.1f}" y1="{cy + r_in * math.sin(a):.1f}" '
                     f'x2="{cx + 44 * math.cos(a):.1f}" y2="{cy + 44 * math.sin(a):.1f}" stroke="{O}" stroke-width="3.2"/>')
        if n == 2:
            o.append(f'<line x1="{cx - 10}" y1="{cy + 10}" x2="{cx + 10}" y2="{cy - 10}" stroke="{O}" stroke-width="3.2"/>')
        o += [T(cx, 140, name, size=13, w="700", a="middle"), T(cx, 158, l1, size=12, a="middle"),
              T(cx, 174, l2, size=12, a="middle")]
    return fig(svg(184, "Mặt đầu mũi khoan, mũi khoét và dao doa", o),
               "Hình 3. Nhìn mặt đầu dao (vạch cam: lưỡi cắt). Càng nhiều lưỡi, dao càng cứng vững, lỗ càng chính xác.")


# Hình 4: chuốt kéo lỗ
def fig4():
    o = []
    ax = 104
    o.append(f'<rect x="196" y="{ax - 60}" width="64" height="40" {WP}/>')
    o.append(f'<rect x="196" y="{ax + 20}" width="64" height="40" {WP}/>')
    o.append(f'<rect x="20" y="{ax - 8}" width="372" height="16" fill="{O}" fill-opacity="0.25" stroke="{O}" stroke-width="1.6"/>')
    teeth = []
    for k in range(13):                     # răng trước (phải) thấp, răng sau (trái) cao
        x = 330 - 15 * k
        h = 2 + k * 0.85
        teeth.append((x, h))
        for sgn in (-1, 1):
            o.append(poly([(x - 12, ax + sgn * 8), (x - 12, ax + sgn * (8 + h)), (x, ax + sgn * 8)],
                          f'fill="{O}" stroke="{O}" stroke-width="1"'))
    o.append(ar(340, ax + 44, 400, ax + 44, R))
    o += [T(404, ax + 66, "dao bị kéo:", R, 12, "700", a="end"), T(404, ax + 82, "chuyển động chính", R, 12, a="end")]
    o += [T(228, ax - 68, "chi tiết đứng yên", size=12, w="700", a="middle")]
    o += [T(20, ax + 40, "răng sau cao hơn", O, 12, "700"), T(20, ax + 56, "răng trước", O, 12, "700")]
    o.append(f'<line x1="20" y1="{ax + 70}" x2="40" y2="{ax + 70}" stroke="currentColor" stroke-width="1"/>')
    return fig(svg(192, "Sơ đồ chuốt kéo lỗ", o),
               "Hình 4. Chuốt kéo: mỗi răng cao hơn răng trước một chút, cắt một lớp mỏng. Một lượt kéo là xong lỗ.")


# Hình 5: mài khôn – vết đan chéo, độ vượt l1, l2
def fig5():
    top, bot = 50, 210
    o = [f'<rect x="100" y="{top}" width="20" height="{bot - top}" {WP}/>',
         f'<rect x="300" y="{top}" width="20" height="{bot - top}" {WP}/>']
    o.append(f'<clipPath id="tl9c5"><rect x="120" y="{top}" width="180" height="{bot - top}"/></clipPath>')
    o.append('<g clip-path="url(#tl9c5)">')
    for k in range(-200, 360, 16):
        o.append(f'<line x1="120" y1="{top + k}" x2="300" y2="{top + k + 70}" stroke="currentColor" stroke-opacity="0.16" stroke-width="1"/>')
        o.append(f'<line x1="120" y1="{top + k + 70}" x2="300" y2="{top + k}" stroke="currentColor" stroke-opacity="0.16" stroke-width="1"/>')
    o.append('</g>')
    up, lo = (top - 18, top + 42), (bot - 42, bot + 18)
    for x in (120, 286):
        o.append(f'<rect x="{x}" y="{up[0]}" width="14" height="{up[1] - up[0]}" {STONE}/>')
        o.append(f'<rect x="{x}" y="{lo[0]}" width="14" height="{lo[1] - lo[0]}" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>')
    o.append(f'<rect x="134" y="{up[0] + 6}" width="152" height="6" fill="currentColor" fill-opacity="0.5"/>')
    o.append(f'<rect x="204" y="6" width="12" height="{up[0]}" fill="currentColor" fill-opacity="0.5"/>')
    o.append(rot(210, 16, 30, 7, 20, 160))
    o.append(T(250, 14, "quay", R, 12, "700"))
    o.append(ar(70, 90, 70, 170, B, both=True))
    o += [T(14, 124, "đi lên –", B, 12, "700"), T(14, 140, "đi xuống", B, 12, "700")]
    for (ya, yb, lab) in ((up[0], top, "l₁"), (bot, lo[1], "l₂")):
        o.append(f'<line x1="330" y1="{ya}" x2="352" y2="{ya}" stroke="currentColor" stroke-width="1"/>')
        o.append(f'<line x1="330" y1="{yb}" x2="352" y2="{yb}" stroke="currentColor" stroke-width="1"/>')
        o.append(f'<line x1="344" y1="{ya}" x2="344" y2="{yb}" stroke="currentColor" stroke-width="1.4"/>')
        o.append(T(356, (ya + yb) / 2 + 5, "độ vượt " + lab, size=12, w="700"))
    o.append(T(210, 134, "vết đan chéo", size=12, w="700", a="middle"))
    o.append(T(14, 250, "Nét liền: thỏi đá ở đầu trên. Nét đứt: ở đầu dưới.", size=12))
    return fig(svg(260, "Sơ đồ mài khôn lỗ và độ vượt của thỏi đá", o),
               "Hình 5. Mặt cắt lỗ khi mài khôn. Đầu khôn vừa quay vừa đi lên – xuống nên vết mài đan chéo. Thỏi đá thò ra khỏi lỗ một đoạn: độ vượt.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in (("<!--FIG1-->", fig1), ("<!--FIG2-->", fig2), ("<!--FIG3-->", fig3), ("<!--FIG4-->", fig4), ("<!--FIG5-->", fig5)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
