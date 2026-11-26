#!/usr/bin/env python3
"""Sinh hình SVG cho CNCTM 1 – Bài 7 (Gia công mặt phẳng), thay <!--FIGn--> trong theory.src.html → theory.html.
Dùng: python3 build_figs.py  (chạy lại an toàn: luôn đọc từ theory.src.html)
Quy ước màu: đỏ = chuyển động chính, xanh = chạy dao, cam = dao/phoi, xám = phôi, nâu xám = đá mài.
"""
import math
import pathlib
import random
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


def tool(x, y):
    """Dao bào nhìn từ trên: tam giác nhỏ màu cam, mũi tại (x, y)."""
    return poly([(x, y), (x + 12, y - 6), (x + 12, y + 6)], f'fill="{O}" stroke="{O}" stroke-width="1"')


# Hình 1: bào ngang – bào giường nhìn từ trên xuống
def fig1():
    o = [T(12, 20, "a) Bào ngang (nhìn từ trên xuống)", w="700")]
    o.append(f'<rect x="40" y="36" width="160" height="84" {WP}/>')
    o.append('<rect x="40" y="36" width="160" height="30" fill="#f8fafc" fill-opacity="0.6"/>')
    for y in (46, 56, 66):
        o.append(f'<line x1="40" y1="{y}" x2="200" y2="{y}" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3 3"/>')
    o.append(ar(26, 112, 26, 62, B))                         # bàn máy nhích lên (phần đã bào ở trên)
    o.append(ar(30, 78, 210, 78, R, both=True))               # dao đi – về
    o.append(tool(212, 78))
    o += [T(240, 64, "Dao đi – về:", R, w="700"), T(240, 80, "chuyển động chính", R),
          T(240, 102, "Bàn máy nhích S", B, w="700"), T(240, 118, "sau mỗi hành trình kép:", B),
          T(240, 134, "chạy dao", B)]
    y0 = 158
    o.append(T(12, y0 + 12, "b) Bào giường (nhìn từ trên xuống)", w="700"))
    o.append(f'<rect x="40" y="{y0 + 28}" width="160" height="84" {WP}/>')
    o.append(f'<rect x="40" y="{y0 + 28}" width="160" height="30" fill="#f8fafc" fill-opacity="0.6"/>')
    for y in (38, 48, 58):
        o.append(f'<line x1="40" y1="{y0 + y}" x2="200" y2="{y0 + y}" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3 3"/>')
    o.append(tool(112, y0 + 70))
    o.append(ar(140, y0 + 62, 140, y0 + 92, B))               # dao nhích xuống phần chưa bào
    o.append(ar(40, y0 + 128, 200, y0 + 128, R, both=True))    # bàn máy mang phôi đi – về
    o += [T(240, y0 + 66, "Dao nhích ngang:", B, w="700"), T(240, y0 + 82, "chạy dao", B),
          T(240, y0 + 116, "Bàn mang phôi đi – về:", R, w="700"), T(240, y0 + 132, "chuyển động chính", R)]
    return fig(svg(300, "Sơ đồ bào ngang và bào giường", o),
               "Hình 1. Bào ngang và bào giường đổi vai cho nhau. Đỏ: chuyển động chính. Xanh: chạy dao. Vùng nhạt: phần đã bào.")


def teeth_pts(cx, cy, r_in, r_out, n):
    pts = []
    for k in range(2 * n):
        a = math.radians(k * 180 / n)
        r = r_out if k % 2 == 0 else r_in
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# Hình 2: phay mặt phẳng bằng dao phay mặt đầu và dao phay trụ
def fig2():
    o = [T(12, 20, "a) Dao phay mặt đầu", w="700"), T(222, 20, "b) Dao phay trụ", w="700")]
    # a) phôi: bên phải chưa phay (cao), bên trái đã phay (thấp 6 px)
    o.append(poly([(14, 156), (60, 156), (60, 150), (194, 150), (194, 186), (14, 186)], WP))
    o.append(f'<rect x="60" y="120" width="90" height="36" fill="{O}" fill-opacity="0.25" stroke="{O}" stroke-width="1.8"/>')
    o.append('<rect x="93" y="50" width="24" height="70" fill="none" stroke="currentColor" stroke-width="1.8"/>')
    o.append(rot(105, 80, 34, 9, 20, 160))
    o.append(T(146, 86, "dao quay", R, 12))
    o.append(ar(150, 204, 60, 204, B))
    o.append(T(60, 224, "phôi tịnh tiến", B, 12))
    # b) dao phay trụ, tâm (310,110), đỉnh răng r = 46 → chạm mặt đã phay y = 156
    cx, cy = 310, 110
    xi = cx + math.sqrt(46 ** 2 - (150 - cy) ** 2)
    arc = [(cx + 46 * math.cos(math.radians(t)), cy + 46 * math.sin(math.radians(t))) for t in range(90, 59, -2)]
    arc = [p for p in arc if p[1] >= 150] + [(xi, 150)]
    o.append(poly([(222, 156)] + arc + [(408, 150), (408, 186), (222, 186)], WP))
    o.append(poly(teeth_pts(cx, cy, 40, 46, 12), f'fill="{O}" fill-opacity="0.22" stroke="{O}" stroke-width="1.6"'))
    o.append(f'<circle cx="{cx}" cy="{cy}" r="8" fill="none" stroke="currentColor" stroke-width="1.6"/>')
    o.append(rot(cx, cy, 56, 56, -40, -140))
    o.append(T(cx, 44, "dao quay", R, 12, a="middle"))
    o.append(ar(390, 204, 300, 204, B))
    o.append(T(300, 224, "phôi tịnh tiến", B, 12))
    return fig(svg(236, "Phay mặt phẳng bằng dao phay mặt đầu và dao phay trụ", o),
               "Hình 2. Hai cách phay mặt phẳng. Đỏ: dao quay là chuyển động chính. Xanh: phôi tịnh tiến là chạy dao.")


# Hình 3: phay nghịch – phay thuận, phoi hình dấu phẩy
def mill_panel(cx, title, nghich, lines):
    cy, Rr, a, fz = 90, 46, 24, 16
    y_top, y_bot = cy + Rr - a, cy + Rr
    th = math.degrees(math.asin((y_top - cy) / Rr))
    ts = [90 - (90 - th) * i / 30 for i in range(31)]
    cur = [(cx + Rr * math.cos(math.radians(t)), cy + Rr * math.sin(math.radians(t))) for t in ts]
    prev = [(x - fz, y) for x, y in cur]
    L, Rx = cx - 95, cx + 95
    o = [T(cx - 93, 18, title, w="700")]
    o.append(poly([(L, y_bot)] + prev + [(Rx, y_top), (Rx, 168), (L, 168)], WP))
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{Rr}" fill="#94a3b8" fill-opacity="0.12" stroke="currentColor" stroke-width="1.6"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="7" fill="none" stroke="currentColor" stroke-width="1.4"/>')
    o.append(poly(cur + prev[::-1], f'fill="{O}" fill-opacity="0.85" stroke="{O}" stroke-width="1"'))
    o.append(rot(cx, cy, 58, 58, -40, -140) if nghich else rot(cx, cy, 58, 58, -140, -40))
    o.append(ar(cx + 40, 184, cx - 40, 184, B))
    o.append(T(cx + 46, 188, "chạy dao", B, 12))
    for i, s in enumerate(lines):
        o.append(T(cx - 93, 210 + 16 * i, s, size=12.5, w="700" if i == 2 else "400"))
    return o


def fig3():
    o = mill_panel(105, "a) Phay nghịch", True, ["dao ngược chiều chạy dao", "phoi: mỏng → dày", "→ gia công thô"])
    o += mill_panel(315, "b) Phay thuận", False, ["dao cùng chiều chạy dao", "phoi: dày → mỏng", "→ tinh, máy ít rơ"])
    o.append('<line x1="210" y1="30" x2="210" y2="240" stroke="currentColor" stroke-opacity="0.25" stroke-width="1"/>')
    return fig(svg(252, "Phay nghịch và phay thuận bằng dao phay trụ", o),
               "Hình 3. Cùng chiều chạy dao (xanh), chỉ đổi chiều quay của dao (đỏ). Phoi (cam) được vẽ phóng to.")


# Hình 4: mài phẳng bằng lưng đá và bằng mặt đầu đá
def fig4():
    o = [T(12, 20, "a) Lưng đá (máy mài ngang)", w="700"), T(222, 20, "b) Mặt đầu đá", w="700")]
    o.append(f'<rect x="14" y="150" width="182" height="30" {WP}/>')
    o.append(f'<circle cx="105" cy="94" r="56" {STONE}/>')
    o.append('<circle cx="105" cy="94" r="12" fill="none" stroke="currentColor" stroke-width="1.6"/>')
    o.append(rot(105, 94, 66, 66, -40, -140))
    o.append(f'<line x1="94" y1="150" x2="116" y2="150" stroke="{O}" stroke-width="5"/>')
    o.append(ar(60, 196, 150, 196, B, both=True))
    o.append(T(14, 218, "tiếp xúc hẹp, dễ thoát nhiệt", size=12.5))
    o.append(T(14, 234, "→ chính xác, nhẵn hơn", size=12.5, w="700"))
    o.append(f'<rect x="226" y="150" width="182" height="30" {WP}/>')
    o.append(f'<rect x="250" y="112" width="134" height="38" {STONE}/>')
    o.append('<rect x="305" y="46" width="24" height="66" fill="none" stroke="currentColor" stroke-width="1.6"/>')
    o.append(rot(317, 76, 34, 9, 20, 160))
    o.append(f'<line x1="250" y1="150" x2="384" y2="150" stroke="{O}" stroke-width="5"/>')
    o.append(ar(272, 196, 362, 196, B, both=True))
    o.append(T(226, 218, "tiếp xúc rộng → năng suất cao", size=12.5, w="700"))
    o.append(T(226, 234, "nóng hơn, kém chính xác hơn", size=12.5))
    o.append(T(122, 146, "vùng tiếp xúc", O, 12))
    return fig(svg(244, "Mài mặt phẳng bằng lưng đá và bằng mặt đầu đá", o),
               "Hình 4. Vùng tiếp xúc (cam) quyết định cách mài: hẹp thì mát và chính xác, rộng thì năng suất. Xanh: bàn máy đi – về.")


# Hình 5: điểm bắt màu trên ô 25 × 25 mm khi cạo thô và cạo tinh
def spots(x0, y0, size, n, r, seed):
    rnd = random.Random(seed)
    pts = []
    while len(pts) < n:
        x, y = x0 + rnd.uniform(r + 4, size - r - 4), y0 + rnd.uniform(r + 4, size - r - 4)
        if all(math.hypot(x - a, y - b) > 2.6 * r + 4 for a, b in pts):
            pts.append((x, y))
    return pts


def fig5():
    o = []
    for x0, title, n, r, seed, yc in ((30, "Cạo thô: 15 điểm", 15, 7, 3, "cần 12–18 điểm"),
                                      (240, "Cạo tinh: 23 điểm", 23, 4.5, 11, "cần 20–25 điểm")):
        y0, s = 34, 150
        o.append(T(x0, 22, title, w="700"))
        o.append(f'<rect x="{x0}" y="{y0}" width="{s}" height="{s}" fill="#94a3b8" fill-opacity="0.2" stroke="currentColor" stroke-width="1.8"/>')
        for k in range(-s, s, 14):                     # vết cạo đan hai hướng (vuông góc nhau)
            o.append(f'<line x1="{x0 + max(k, 0)}" y1="{y0 + max(-k, 0)}" x2="{x0 + min(k + s, s)}" y2="{y0 + min(s - k, s)}" '
                     'stroke="currentColor" stroke-opacity="0.18" stroke-width="1"/>')
            o.append(f'<line x1="{x0 + max(k, 0)}" y1="{y0 + s - max(-k, 0)}" x2="{x0 + min(k + s, s)}" y2="{y0 + s - min(s - k, s)}" '
                     'stroke="currentColor" stroke-opacity="0.18" stroke-width="1"/>')
        pts = spots(x0, y0, s, n, r, seed)
        assert len(pts) == n
        for x, y in pts:
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{R}" fill-opacity="0.8"/>')
        o.append(T(x0, y0 + s + 18, "ô 25 × 25 mm", size=12.5))
        o.append(T(x0, y0 + s + 34, yc, size=12.5, w="700"))
    return fig(svg(232, "Điểm bắt màu khi cạo thô và cạo tinh", o),
               "Hình 5. Cạo càng nhiều lượt, điểm bắt màu (đỏ) càng nhỏ và càng dày. Vết cạo đan hai hướng lệch nhau 90°.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in (("<!--FIG1-->", fig1), ("<!--FIG2-->", fig2), ("<!--FIG3-->", fig3), ("<!--FIG4-->", fig4), ("<!--FIG5-->", fig5)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
