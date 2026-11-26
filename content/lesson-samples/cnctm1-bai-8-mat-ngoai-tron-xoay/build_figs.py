#!/usr/bin/env python3
"""Sinh hình SVG cho CNCTM 1 – Bài 8 (Gia công mặt ngoài tròn xoay), thay <!--FIGn--> trong theory.src.html → theory.html.
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


def tool(x, y):
    """Dao bào nhìn từ trên: tam giác nhỏ màu cam, mũi tại (x, y)."""
    return poly([(x, y), (x + 12, y - 6), (x + 12, y + 6)], f'fill="{O}" stroke="{O}" stroke-width="1"')



def center(x, y, right=True):
    """Mũi tâm: tam giác, mũi tại (x, y), thân về phía ngoài."""
    k = 1 if right else -1
    return poly([(x, y), (x + 20 * k, y - 10), (x + 20 * k, y + 10)], 'fill="none" stroke="currentColor" stroke-width="1.6"')


# Hình 1: tiện trụ ngoài – phôi quay, dao chạy dọc
def fig1():
    o = [f'<rect x="14" y="48" width="40" height="104" fill="none" stroke="currentColor" stroke-width="1.8"/>']
    o += [f'<rect x="54" y="{y}" width="12" height="12" fill="currentColor" fill-opacity="0.5"/>' for y in (68, 120)]
    o.append(f'<rect x="54" y="80" width="150" height="40" {WP}/>')              # phần chưa tiện
    o.append(f'<rect x="204" y="86" width="128" height="28" {WP}/>')             # phần đã tiện
    o.append('<line x1="20" y1="100" x2="404" y2="100" stroke="currentColor" stroke-width="0.8" stroke-dasharray="10 3 2 3"/>')
    o.append(center(332, 100))
    o.append('<rect x="352" y="90" width="52" height="20" fill="none" stroke="currentColor" stroke-width="1.6"/>')
    o.append(poly([(204, 114), (216, 134), (250, 134), (250, 150), (210, 150), (200, 130)], f'fill="{O}" fill-opacity="0.85" stroke="{O}" stroke-width="1"'))
    o.append(rot(110, 100, 10, 34, -60, 230))
    o.append(T(110, 54, "phôi quay", R, 12, "700", a="middle"))
    o.append(T(110, 40, "chuyển động chính", R, 12, a="middle"))
    o.append(ar(300, 174, 214, 174, B))
    o.append(T(306, 170, "dao chạy dọc:", B, 12, "700"))
    o.append(T(306, 186, "chạy dao", B, 12))
    o += [T(34, 172, "mâm cặp", size=12, a="middle"), T(378, 80, "mũi tâm", size=12, a="middle"),
          T(258, 146, "dao", O, 12, "700")]
    return fig(svg(200, "Sơ đồ tiện trụ ngoài trên máy tiện", o),
               "Hình 1. Tiện trụ ngoài: phôi quay là chuyển động chính (đỏ), dao chạy dọc trục là chạy dao (xanh).")


# Hình 2: trục mảnh võng dưới lực cắt → phình giữa; luynét đỡ giữa
def fig2():
    o = [T(12, 18, "a) Chỉ chống tâm hai đầu", w="700")]
    o += [center(30, 64, right=False), center(390, 64)]
    o.append('<rect x="30" y="54" width="360" height="20" fill="none" stroke="currentColor" stroke-opacity="0.45" stroke-width="1" stroke-dasharray="4 3"/>')
    o.append(f'<path d="M30,54 Q210,22 390,54 L390,74 Q210,42 30,74 Z" {WP}/>')
    o.append(poly([(210, 64), (198, 86), (222, 86)], f'fill="{O}" stroke="{O}" stroke-width="1"'))
    o.append(T(228, 94, "dao", O, 12, "700"))
    o.append(ar(250, 40, 250, 20, "currentColor", 2))
    o.append(T(258, 30, "lực cắt", size=12, w="700"))
    o.append(T(120, 100, "lực cắt đẩy giữa trục võng lên,", size=12, a="middle"))
    o.append(T(120, 116, "dao ăn ít hơn ở giữa", size=12, a="middle"))
    o.append(f'<path d="M40,130 Q210,118 380,130 L380,150 Q210,162 40,150 Z" {WP}/>')
    o += [T(40, 174, "hai đầu Ø20,00", size=12), T(380, 174, "sau khi tiện", size=12, a="end"),
          T(210, 174, "giữa Ø20,15", R, 12, "700", a="middle")]
    y0 = 196
    o.append(T(12, y0, "b) Thêm luynét đỡ giữa trục", w="700"))
    o += [center(30, y0 + 40, right=False), center(390, y0 + 40)]
    o.append(f'<rect x="30" y="{y0 + 30}" width="360" height="20" {WP}/>')
    for x, y in ((180, y0 + 21), (180, y0 + 59)):
        o.append(f'<circle cx="{x}" cy="{y}" r="8" fill="none" stroke="{B}" stroke-width="1.8"/>')
    o.append(f'<path d="M180,{y0 + 13} L180,{y0 + 6} L150,{y0 + 6} L150,{y0 + 74} L180,{y0 + 74} L180,{y0 + 67}" fill="none" stroke="{B}" stroke-width="1.8"/>')
    o.append(T(144, y0 + 72, "luynét", B, 12, "700", a="end"))
    o.append(poly([(260, y0 + 50), (248, y0 + 72), (272, y0 + 72)], f'fill="{O}" stroke="{O}" stroke-width="1"'))
    o.append(T(278, y0 + 70, "dao", O, 12, "700"))
    o.append(T(210, y0 + 96, "trục không võng → đường kính đều", size=12, w="700", a="middle"))
    return fig(svg(302, "Trục mảnh bị võng khi tiện và cách đỡ bằng luynét", o),
               "Hình 2. Trục dài, mảnh võng ra xa dao nên giữa trục phình to (vẽ phóng đại). Luynét (xanh) đỡ giữa trục.")


# Hình 3: cắt từng lớp và cắt từng đoạn (nửa trên trục bậc)
def layer(x1, y1, x2, y2, n):
    return [f'<rect x="{x1}" y="{y1}" width="{x2 - x1}" height="{y2 - y1}" fill="{O}" fill-opacity="0.18" stroke="{O}" stroke-width="1.4" stroke-dasharray="4 2"/>',
            T(x1 + 10, (y1 + y2) / 2 + 5, str(n), O, 13, "700"),
            ar(x2 - 8, (y1 + y2) / 2, x1 + 30, (y1 + y2) / 2, B, 2, 8)]


def step_panel(x0, title, layers, lines):
    o = [T(x0 + 2, 18, title, w="700")]
    o.append(f'<rect x="{x0}" y="36" width="14" height="110" fill="none" stroke="currentColor" stroke-width="1.6"/>')
    a, b, c = x0 + 14, x0 + 84, x0 + 192
    o.append(poly([(a, 74), (b, 74), (b, 98), (c, 98), (c, 140), (a, 140)], WP))
    o.append(f'<line x1="{a}" y1="140" x2="{c}" y2="140" stroke="currentColor" stroke-width="0.8" stroke-dasharray="10 3 2 3"/>')
    for (u1, y1, u2, y2, n) in layers:
        o += layer(x0 + u1, y1, x0 + u2, y2, n)
    for i, s in enumerate(lines):
        o.append(T(x0 + 2, 168 + 16 * i, s, size=12.5, w="700" if i == 2 else "400"))
    return o


def fig3():
    o = step_panel(8, "a) Cắt từng lớp", [(14, 50, 192, 74, 1), (84, 74, 192, 98, 2)],
                   ["lớp mỏng, chạy suốt chiều dài", "lực nhỏ, chính xác", "→ năng suất không cao"])
    o += step_panel(218, "b) Cắt từng đoạn", [(84, 50, 192, 98, 1), (14, 50, 84, 74, 2)],
                    ["ăn sâu, xong từng bậc", "lực cắt lớn, kém cứng vững", "→ năng suất cao"])
    o.append('<line x1="212" y1="30" x2="212" y2="210" stroke="currentColor" stroke-opacity="0.25" stroke-width="1"/>')
    return fig(svg(214, "Cắt từng lớp và cắt từng đoạn khi tiện trục bậc", o),
               "Hình 3. Nửa trên trục bậc. Vùng cam: lượng dư; số là thứ tự lượt cắt; xanh: chiều chạy dao.")


# Hình 4: mài có tâm tiến dọc – tiến ngang (nhìn từ trên xuống)
def fig4():
    o = [T(12, 18, "a) Tiến dọc: đoạn mài dài hơn đá", w="700")]
    o += [center(40, 62, right=False), center(380, 62)]
    o.append(f'<rect x="40" y="50" width="340" height="24" {WP}/>')
    o.append(f'<rect x="180" y="76" width="40" height="40" {STONE}/>')
    o.append(T(226, 102, "đá mài", size=12, w="700"))
    o.append(ar(130, 136, 270, 136, B, both=True))
    o.append(T(200, 156, "bàn máy mang trục đi – về", B, 12, a="middle"))
    y0 = 186
    o.append(T(12, y0, "b) Tiến ngang: đoạn mài hẹp hơn đá", w="700"))
    o += [center(110, y0 + 44, right=False), center(310, y0 + 44)]
    o.append(f'<rect x="110" y="{y0 + 32}" width="200" height="24" {WP}/>')
    o.append(f'<rect x="185" y="{y0 + 32}" width="50" height="24" fill="none" stroke="{O}" stroke-width="2"/>')
    o.append(f'<rect x="175" y="{y0 + 64}" width="70" height="40" {STONE}/>')
    o.append(T(251, y0 + 90, "đá mài", size=12, w="700"))
    o.append(ar(210, y0 + 128, 210, y0 + 110, B))
    o.append(T(222, y0 + 128, "đá ăn vào theo hướng kính", B, 12))
    return fig(svg(326, "Mài tròn ngoài có tâm: tiến dọc và tiến ngang", o),
               "Hình 4. Nhìn từ trên xuống. Viền cam: đoạn cần mài. Đá rộng hơn đoạn mài thì chỉ cần tiến ngang.")


# Hình 5: mài vô tâm nhìn dọc trục chi tiết
def fig5():
    G, Rg = (110, 132), 88          # đá mài
    r = 26                          # chi tiết
    py = 104
    px = G[0] + math.sqrt((Rg + r) ** 2 - (py - G[1]) ** 2)
    Rd, gy = 60, 140                # đá dẫn
    gx = px + math.sqrt((Rd + r) ** 2 - (gy - py) ** 2)
    n = (-math.sin(math.radians(25)), math.cos(math.radians(25)))
    C = (px + r * n[0], py + r * n[1])
    d = (math.cos(math.radians(30)), math.sin(math.radians(30)))
    p1, p2 = (C[0] - 5 * d[0], C[1] - 5 * d[1]), (C[0] + 8 * d[0], C[1] + 8 * d[1])
    edge = [p1, p2] + [(p1[0], y) for y in range(int(p1[1]), 237, 4)] + [(p2[0], y) for y in range(int(p2[1]), 237, 4)]
    for q in edge:                   # thanh đỡ cách hai đá ≥ 4 px
        assert math.dist(q, G) > Rg + 4 and math.dist(q, (gx, gy)) > Rd + 4, q
    o = [f'<circle cx="{G[0]}" cy="{G[1]}" r="{Rg}" {STONE}/>',
         f'<circle cx="{gx:.1f}" cy="{gy}" r="{Rd}" {STONE}/>',
         poly([p1, p2, (p2[0], 236), (p1[0], 236)], 'fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="1.4"'),
         f'<circle cx="{px:.1f}" cy="{py}" r="{r}" {WP}/>',
         f'<line x1="{G[0]}" y1="{G[1]}" x2="{gx:.1f}" y2="{gy}" stroke="currentColor" stroke-width="1" stroke-dasharray="5 3"/>']
    yl = G[1] + (gy - G[1]) * (px - G[0]) / (gx - G[0])
    o.append(f'<line x1="{px:.1f}" y1="{py}" x2="{px:.1f}" y2="{yl:.1f}" stroke="{B}" stroke-width="1.6"/>')
    o.append(T(px + 5, (py + yl) / 2 + 5, "h", B, 14, "700"))
    o.append(rot(G[0], G[1], 50, 50, 200, 320))
    o.append(rot(gx, gy, 36, 36, 200, 320))
    o.append(rot(px, py, r + 9, r + 9, 330, 215))
    o += [T(G[0], G[1] + 44, "đá mài", size=13, w="700", a="middle"),
          T(gx, gy + 30, "đá dẫn", size=13, w="700", a="middle"),
          T(px, py - r - 16, "chi tiết", O, 12, "700", a="middle"),
          T(p1[0] - 6, 230, "thanh đỡ", size=12, a="end")]
    return fig(svg(244, "Sơ đồ mài vô tâm", o),
               "Hình 5. Mài vô tâm nhìn dọc trục. Đá mài và đá dẫn quay cùng chiều; chi tiết quay ngược lại. Tâm chi tiết cao hơn đường nối tâm hai đá một đoạn h.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in (("<!--FIG1-->", fig1), ("<!--FIG2-->", fig2), ("<!--FIG3-->", fig3), ("<!--FIG4-->", fig4), ("<!--FIG5-->", fig5)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
