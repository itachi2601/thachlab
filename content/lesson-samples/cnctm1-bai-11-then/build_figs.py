#!/usr/bin/env python3
"""Sinh hình SVG cho CNCTM 1 – Bài 11 (Gia công then – then hoa), thay <!--FIGn--> trong theory.src.html → theory.html.
Dùng: python3 build_figs.py  (chạy lại an toàn: luôn đọc từ theory.src.html)
Hình vẽ minh hoạ, không theo tỉ lệ. Chữ ≥ 12 trong viewBox 420 (đọc được ở 375px).
"""
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import chevron  # noqa: E402

FONT = 'font-family="system-ui, sans-serif" font-size="13"'
RED, BLUE, GREEN, ORANGE = "#dc2626", "#0369a1", "#047857", "#ea580c"
METAL = 'fill="#94a3b8" fill-opacity="0.28"'


def T(x, y, s, size=13, anchor="start", w="400", c="currentColor"):
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{anchor}">{s}</text>'


def Ln(x1, y1, x2, y2, c="currentColor", w=1.5, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'


def Ar(x1, y1, x2, y2, c=RED, w=2.2):
    """Mũi tên thẳng, đầu chữ V 30°."""
    return Ln(x1, y1, x2, y2, c, w) + chevron(x2, y2, x2 - x1, y2 - y1, c, w, L=10)


def Rot(cx, cy, rx, ry, t0, t1, c=RED, w=2.2):
    """Cung elip (độ, y hướng xuống) từ t0 tới t1 + đầu V ở t1: chiều quay."""
    n = 30
    pts = [(cx + rx * math.cos(math.radians(t0 + (t1 - t0) * i / n)),
            cy + ry * math.sin(math.radians(t0 + (t1 - t0) * i / n))) for i in range(n + 1)]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    (xa, ya), (xb, yb) = pts[-2], pts[-1]
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}"/>' + chevron(xb, yb, xb - xa, yb - ya, c, w, L=9)


def P(pts, extra='fill="none" stroke="currentColor" stroke-width="2"'):
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" {extra}/>'


def PL(pts, c="currentColor", w=2):
    return f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{c}" stroke-width="{w}"/>'


def svg(h, label, body):
    return (f'<svg viewBox="0 0 420 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}" {FONT}>'
            + "".join(body) + "</svg>")


def fig(s, cap):
    return f'<figure class="fig" data-tl="1">{s}<figcaption>{cap}</figcaption></figure>'


def spline_pts(cx, cy, ri, ro, b, n=6, start=-90, arc_n=8):
    """Biên dạng trục then hoa răng chữ nhật: trả về (điểm, cạnh bên, cung ngoài, cung trong)."""
    di, do = math.asin(b / 2 / ri), math.asin(b / 2 / ro)
    pts, sides, outer, inner = [], [], [], []
    step = 2 * math.pi / n
    for k in range(n):
        t = math.radians(start) + k * step
        p1 = (cx + ri * math.cos(t - di), cy + ri * math.sin(t - di))
        p2 = (cx + ro * math.cos(t - do), cy + ro * math.sin(t - do))
        arc_o = [(cx + ro * math.cos(t - do + 2 * do * j / arc_n), cy + ro * math.sin(t - do + 2 * do * j / arc_n))
                 for j in range(arc_n + 1)]
        p4 = (cx + ri * math.cos(t + di), cy + ri * math.sin(t + di))
        t2 = t + step
        arc_i = [(cx + ri * math.cos(t + di + (step - 2 * di) * j / arc_n),
                  cy + ri * math.sin(t + di + (step - 2 * di) * j / arc_n)) for j in range(arc_n + 1)]
        pts += [p1] + arc_o + arc_i
        sides += [(p1, p2), (arc_o[-1], p4)]
        outer.append(arc_o)
        inner.append(arc_i)
    return pts, sides, outer, inner


HUB = 'fill="#64748b" fill-opacity="0.30" stroke="currentColor" stroke-width="1.4"'
SHAFT = 'fill="#cbd5e1" stroke="currentColor" stroke-width="1.6"'


# Hình 1: mặt cắt ngang mối ghép then bằng và then hoa
def fig_moi_ghep():
    o = []
    cx, cy = 105, 105
    o.append(f'<circle cx="{cx}" cy="{cy}" r="75" {HUB}/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="45" {SHAFT}/>')
    o.append(P([(93, 48), (117, 48), (117, 72), (93, 72)], f'fill="{ORANGE}" stroke="currentColor" stroke-width="1.4"'))
    o.append(Ln(93, 48, 93, 72, RED, 3))
    o.append(Ln(117, 48, 117, 72, RED, 3))
    o.append(T(cx, 112, "trục", 13, "middle", "700"))
    o.append(T(cx, 172, "bạc", 13, "middle", "700"))
    o.append(Ln(120, 52, 168, 22, w=1))
    o.append(T(172, 22, "then", 13, w="700", c=ORANGE))
    o.append(T(cx, 202, "a) Then bằng", 14, "middle", "700"))
    o.append(T(cx, 221, "làm việc bằng", 13, "middle"))
    o.append(T(cx, 239, "hai mặt bên (đỏ)", 13, "middle", c=RED))
    # then hoa
    cx2 = 315
    o.append(f'<circle cx="{cx2}" cy="{cy}" r="75" {HUB}/>')
    pts, sides, outer, inner = spline_pts(cx2, cy, 38, 52, 16)
    o.append(P(pts, SHAFT))
    o.append(f'<circle cx="{cx2}" cy="{cy}" r="38" fill="none" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="5 4"/>')
    o.append(f'<circle cx="{cx2}" cy="{cy}" r="52" fill="none" stroke="{GREEN}" stroke-width="1.6" stroke-dasharray="5 4"/>')
    for a, bb in sides[:2]:
        o.append(Ln(*a, *bb, RED, 3))
    o.append(T(cx2, 202, "b) Then hoa 6 răng", 14, "middle", "700"))
    o.append(T(cx2, 221, "d: đường kính trong", 13, "middle", c=BLUE))
    o.append(T(cx2, 239, "D: đường kính ngoài", 13, "middle", c=GREEN))
    o.append(T(cx2, 257, "b: bề rộng răng (đỏ)", 13, "middle", c=RED))
    return fig(svg(266, "Mặt cắt mối ghép then bằng và then hoa", o),
               "Hình 1. Mặt cắt ngang mối ghép then bằng và then hoa. Then hoa như nhiều then liền với trục.")


# Hình 2: ba loại rãnh then bằng trên trục (nhìn từ trên)
def fig_loai_ranh():
    o = []
    rows = [(20, "Rãnh kín", "→ dao phay ngón"), (88, "Rãnh hở một đầu", "→ dao phay ngón hoặc đĩa"),
            (156, "Rãnh suốt", "→ dao phay đĩa")]
    for k, (y, n1, n2) in enumerate(rows):
        o.append(T(30, y, n1, 13, w="700"))
        o.append(T(30 + len(n1) * 7.6 + 8, y, n2, 13, c=BLUE))
        y0 = y + 8
        o.append(f'<rect x="30" y="{y0}" width="360" height="34" rx="4" {SHAFT}/>')
        o.append(Ln(20, y0 + 17, 400, y0 + 17, w=1, dash="14 4 3 4"))
        if k == 0:
            o.append(f'<rect x="150" y="{y0 + 9}" width="120" height="16" rx="8" fill="{ORANGE}" fill-opacity="0.75" stroke="currentColor" stroke-width="1.4"/>')
        elif k == 1:
            o.append(f'<path d="M390,{y0 + 9} L288,{y0 + 9} A8,8 0 0 0 288,{y0 + 25} L390,{y0 + 25}" '
                     f'fill="{ORANGE}" fill-opacity="0.75" stroke="currentColor" stroke-width="1.4"/>')
        else:
            o.append(f'<rect x="30" y="{y0 + 9}" width="360" height="16" fill="{ORANGE}" fill-opacity="0.75" stroke="currentColor" stroke-width="1.4"/>')
    return fig(svg(206, "Ba loại rãnh then bằng trên trục", o),
               "Hình 2. Ba loại rãnh then bằng trên trục, nhìn từ trên xuống, và dao thường dùng.")


# Hình 3: phay rãnh then bằng dao phay ngón và dao phay đĩa (nhìn ngang trục)
def fig_phay_ranh():
    o = []
    # a) dao phay ngón
    o.append(T(105, 16, "a) Dao phay ngón", 13, "middle", "700"))
    o.append(f'<rect x="15" y="110" width="180" height="50" {SHAFT}/>')
    o.append(f'<rect x="60" y="110" width="70" height="14" fill="#ffffff" fill-opacity="0.9" stroke="currentColor" stroke-width="1.2"/>')
    o.append(f'<rect x="130" y="110" width="20" height="14" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="3 3"/>')
    o.append(P([(108, 36), (130, 36), (130, 124), (108, 124)], 'fill="#64748b" fill-opacity="0.45" stroke="currentColor" stroke-width="1.4"'))
    for y in range(74, 122, 9):
        o.append(Ln(108, y, 130, y - 8, w=1))
    o.append(Rot(119, 52, 22, 6, 20, 160))
    o.append(Ar(34, 96, 84, 96))
    o.append(T(30, 86, "chạy dao", 12))
    o.append(T(105, 182, "rãnh kín", 13, "middle", "700"))
    o.append(T(105, 200, "khoan mồi trước", 13, "middle"))
    o.append(T(105, 218, "năng suất thấp, sửa nguội", 12, "middle", c=BLUE))
    # b) dao phay đĩa
    o.append(T(315, 16, "b) Dao phay đĩa", 13, "middle", "700"))
    o.append(f'<rect x="225" y="110" width="180" height="50" {SHAFT}/>')
    o.append('<path d="M225,110 L335.5,110 A44,44 0 0,1 300,128 L225,128 Z" fill="#ffffff" fill-opacity="0.9" stroke="currentColor" stroke-width="1.2"/>')
    o.append(f'<circle cx="300" cy="84" r="44" fill="#64748b" fill-opacity="0.45" stroke="currentColor" stroke-width="1.6"/>')
    o.append(f'<circle cx="300" cy="84" r="34" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3 3"/>')
    o.append(f'<circle cx="300" cy="84" r="7" fill="none" stroke="currentColor" stroke-width="1.6"/>')
    o.append(Rot(300, 84, 52, 52, 195, 285))
    o.append(Ar(356, 100, 398, 100))
    o.append(T(356, 90, "chạy dao", 12))
    o.append(T(315, 182, "rãnh suốt, hở đầu", 13, "middle", "700"))
    o.append(T(315, 200, "năng suất cao", 13, "middle"))
    o.append(T(315, 218, "rãnh bị rộng thêm ≥ 0,1 mm", 12, "middle", c=RED))
    return fig(svg(226, "Phay rãnh then bằng dao phay ngón và dao phay đĩa", o),
               "Hình 3. Phay rãnh then, nhìn ngang trục. Nét đứt là phần rãnh dao sắp cắt tới.")


# Hình 4: đường chạy dao của dao phay ngón hai lưỡi trên máy chuyên dùng
def fig_duong_chay_dao():
    o = []
    o.append(T(20, 20, "Chạy dọc hết chiều dài rãnh,", 13))
    o.append(T(20, 38, "S = 150 ÷ 300 mm/phút", 13, w="700", c=BLUE))
    o.append(f'<rect x="60" y="56" width="300" height="100" fill="#cbd5e1" fill-opacity="0.5" stroke="none"/>')
    o.append(Ln(30, 56, 390, 56, w=1.6))
    xs, ys = (72, 348), [56 + 12 * i for i in range(9)]
    path = [(xs[0], ys[0])]
    for i in range(1, len(ys)):
        xcur = path[-1][0]
        path.append((xcur, ys[i]))
        path.append((xs[1] if xcur == xs[0] else xs[0], ys[i]))
    o.append(PL(path, RED, 2))
    for i in range(1, len(path)):
        (x1, y1), (x2, y2) = path[i - 1], path[i]
        if abs(x2 - x1) > 50:
            mx = (x1 + x2) / 2
            o.append(chevron(mx, y2, x2 - x1, 0, RED, 2, L=9))
    o.append(Ln(60, 56, 60, 160, w=1.6))
    o.append(Ln(360, 56, 360, 160, w=1.6))
    o.append(Ln(60, 160, 360, 160, w=1.6, dash="5 4"))
    o.append(T(52, 74, "ăn sâu", 12, "end"))
    o.append(T(52, 92, "0,2 ÷ 0,4", 12, "end", w="700"))
    o.append(T(52, 108, "mm", 12, "end"))
    o.append(T(368, 166, "đáy rãnh", 12))
    o.append(T(20, 186, "Cuối mỗi hành trình: dừng, ăn sâu, đảo chiều.", 13))
    o.append(T(20, 204, "Máy tự làm cho tới hết chiều sâu rãnh.", 13, c=GREEN))
    return fig(svg(212, "Đường chạy dao của dao phay ngón hai lưỡi", o),
               "Hình 4. Phay rãnh then trên máy chuyên dùng bằng dao phay ngón hai lưỡi (có lưỡi mặt đầu nên không cần khoan mồi). Hình phóng to chiều sâu.")


# Hình 5: ba kiểu định tâm then hoa
def fig_dinh_tam():
    o = []
    specs = [("Theo D", "thấp hơn d", "mài dễ", "outer"),
             ("Theo d", "đồng tâm cao nhất", "hay dùng", "inner"),
             ("Theo b", "đồng tâm kém nhất", "mômen lớn nhất", "sides")]
    for i, (n1, n2, n3, kind) in enumerate(specs):
        cx, cy = 70 + i * 140, 70
        o.append(f'<circle cx="{cx}" cy="{cy}" r="60" {HUB}/>')
        pts, sides, outer, inner = spline_pts(cx, cy, 32, 44, 14)
        o.append(P(pts, SHAFT))
        if kind == "outer":
            for a in outer:
                o.append(PL(a, RED, 3.5))
        elif kind == "inner":
            for a in inner:
                o.append(PL(a, RED, 3.5))
        else:
            for a, bb in sides:
                o.append(Ln(*a, *bb, RED, 3.5))
        o.append(T(cx, 154, n1, 14, "middle", "700"))
        o.append(T(cx, 173, n2, 13, "middle"))
        o.append(T(cx, 191, n3, 13, "middle", c=BLUE))
    o.append(Ln(12, 206, 34, 206, RED, 3.5))
    o.append(T(40, 210, "mặt định tâm: phải gia công chính xác nhất", 12))
    return fig(svg(218, "Ba kiểu định tâm mối ghép then hoa", o),
               "Hình 5. Ba kiểu định tâm then hoa. Mặt tô đỏ là mặt quyết định độ đồng tâm giữa trục và bạc.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in (("<!--FIG1-->", fig_moi_ghep), ("<!--FIG2-->", fig_loai_ranh), ("<!--FIG3-->", fig_phay_ranh),
               ("<!--FIG4-->", fig_duong_chay_dao), ("<!--FIG5-->", fig_dinh_tam)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
