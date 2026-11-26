#!/usr/bin/env python3
"""Sinh hình SVG cho CNCTM 2 – Bài 16 (Công nghệ gia công chi tiết dạng bạc),
thay <!--FIGn--> và __PHUT__ trong theory.src.html → theory.html.
Dùng: python3 build_figs.py  (chạy lại an toàn: luôn đọc từ theory.src.html)
Mọi hình là sơ đồ nguyên lý tự vẽ, không theo tỉ lệ. Chữ ≥ 12 trong viewBox 420.
Màu: xanh dương = mặt chuẩn định vị / lỗ; cam = mặt được gia công / mặt ngoài; đỏ = lực kẹp W, đường cắt; xanh lá = mặt đầu.
"""
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SCR = ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"
sys.path.insert(0, str(SCR))
from svg_lib import chevron  # noqa: E402
import lint_do_dai  # noqa: E402

FONT = 'font-family="system-ui, sans-serif" font-size="13"'
RED, BLUE, GREEN, ORANGE = "#dc2626", "#0369a1", "#047857", "#ea580c"
GREY = 'fill="#64748b" fill-opacity="0.35" stroke="currentColor" stroke-width="1.3"'
WALL = 'fill="#94a3b8" fill-opacity="0.32" stroke="currentColor" stroke-width="1.4"'


def T(x, y, s, size=13, anchor="start", w="400", c="currentColor"):
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{anchor}">{s}</text>'


def Ln(x1, y1, x2, y2, c="currentColor", w=1.5, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'


def Ar(x1, y1, x2, y2, c=RED, w=2.2, L=10):
    return Ln(x1, y1, x2, y2, c, w) + chevron(x2, y2, x2 - x1, y2 - y1, c, w, L=L)


def Dim(x1, y1, x2, y2, c="currentColor"):
    """Đường kích thước hai đầu mũi tên (đầu chạm đường gióng là đúng quy ước vẽ kỹ thuật)."""
    return (Ln(x1, y1, x2, y2, c, 1.1) + chevron(x2, y2, x2 - x1, y2 - y1, c, 1.1, L=7)
            + chevron(x1, y1, x1 - x2, y1 - y2, c, 1.1, L=7))


def Rot(cx, cy, rx, ry, t0, t1, c=RED, w=2.2):
    n = 30
    pts = [(cx + rx * math.cos(math.radians(t0 + (t1 - t0) * i / n)),
            cy + ry * math.sin(math.radians(t0 + (t1 - t0) * i / n))) for i in range(n + 1)]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    (xa, ya), (xb, yb) = pts[-2], pts[-1]
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}"/>' + chevron(xb, yb, xb - xa, yb - ya, c, w, L=9)


def P(pts, extra=WALL):
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" {extra}/>'


def mirror(pts, axis):
    return [(x, 2 * axis - y) for x, y in pts]


def svg(h, label, body):
    return (f'<svg viewBox="0 0 420 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}" {FONT}>'
            + "".join(body) + "</svg>")


def fig(s, cap):
    return f'<figure class="fig" data-tl="1">{s}<figcaption>{cap}</figcaption></figure>'


def loc(x, y, dx, dy, n, lx, ly, c=BLUE, size=13):
    """Ký hiệu định vị: tam giác đặc, đỉnh chạm mặt chuẩn tại (x, y), hướng (dx, dy) là hướng từ ngoài vào mặt; nhãn số bậc tự do."""
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    bx, by = x - 11 * ux, y - 11 * uy
    px, py = -uy * 6, ux * 6
    tri = P([(x, y), (bx + px, by + py), (bx - px, by - py)], f'fill="{c}"')
    return tri + T(lx, ly, str(n), size, "middle", "700", c)


def text_box(x, y, s, size=13, anchor="start"):
    """Hộp bao gần đúng của một dòng chữ (rộng ~0,56·size mỗi ký tự)."""
    w = 0.56 * size * len(s)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
    return x0, y - size * 0.8, x0 + w, y + size * 0.2


def assert_clear_of_circle(box, cx, cy, r, gap=4, name=""):
    x0, y0, x1, y1 = box
    nx, ny = min(max(cx, x0), x1), min(max(cy, y0), y1)
    d = math.hypot(nx - cx, ny - cy)
    inside = x0 <= cx - r and x1 >= cx + r and y0 <= cy - r and y1 >= cy + r
    assert d >= r + gap and not inside, f"nhãn {name!r} chạm đường tròn (d={d:.1f}, r={r})"


# Hình 1: bốn dạng bạc
def fig_loai_bac():
    o = []
    cells = [(0, 0), (210, 0), (0, 140), (210, 140)]
    # a) bạc trơn, có kích thước D, d, L
    ox, oy = cells[0]
    ax = oy + 58
    top = [(ox + 30, oy + 22), (ox + 170, oy + 22), (ox + 170, oy + 40), (ox + 30, oy + 40)]
    o += [P(top), P(mirror(top, ax)), Ln(ox + 18, ax, ox + 182, ax, w=1, dash="6 4")]
    o.append(Dim(ox + 186, oy + 22, ox + 186, 2 * ax - oy - 22))
    o.append(T(ox + 192, ax + 5, "D", 13, "start", "700"))
    o.append(Dim(ox + 120, oy + 40, ox + 120, 2 * ax - oy - 40))
    o.append(T(ox + 126, ax - 4, "d", 13, "start", "700"))
    o.append(Dim(ox + 30, oy + 104, ox + 170, oy + 104))
    o.append(T(ox + 24, oy + 109, "L", 13, "end", "700"))
    o.append(T(ox + 100, oy + 128, "a) Bạc trơn", 13, "middle", "700"))
    # b) bạc có gờ
    ox, oy = cells[1]
    ax = oy + 58
    top = [(ox + 30, oy + 8), (ox + 54, oy + 8), (ox + 54, oy + 22), (ox + 180, oy + 22),
           (ox + 180, oy + 40), (ox + 30, oy + 40)]
    o += [P(top), P(mirror(top, ax)), Ln(ox + 18, ax, ox + 192, ax, w=1, dash="6 4")]
    o.append(T(ox + 105, oy + 128, "b) Bạc có gờ", 13, "middle", "700"))
    # c) bạc lỗ côn
    ox, oy = cells[2]
    ax = oy + 58
    top = [(ox + 30, oy + 22), (ox + 170, oy + 22), (ox + 170, oy + 46), (ox + 30, oy + 34)]
    o += [P(top), P(mirror(top, ax)), Ln(ox + 18, ax, ox + 182, ax, w=1, dash="6 4")]
    o.append(T(ox + 100, oy + 128, "c) Bạc lỗ côn", 13, "middle", "700"))
    # d) bạc xẻ rãnh, nhìn từ đầu
    ox, oy = cells[3]
    cx, cy, R, r, g = ox + 105, oy + 58, 44, 33, 9
    t1, t2 = math.radians(-90 + g), math.radians(-90 - g + 360)
    po = lambda t, rr: (cx + rr * math.cos(t), cy + rr * math.sin(t))
    (a1, b1), (a2, b2), (a3, b3), (a4, b4) = po(t1, R), po(t2, R), po(t2, r), po(t1, r)
    d = (f"M{a1:.1f},{b1:.1f} A{R},{R} 0 1 1 {a2:.1f},{b2:.1f} L{a3:.1f},{b3:.1f} "
         f"A{r},{r} 0 1 0 {a4:.1f},{b4:.1f} Z")
    o.append(f'<path d="{d}" {WALL}/>')
    o.append(T(ox + 105, oy + 128, "d) Bạc xẻ rãnh (nhìn đầu)", 13, "middle", "700"))
    return fig(svg(280, "Bốn dạng bạc thường gặp, vẽ mặt cắt dọc", o),
               "Hình 1. Bốn dạng bạc (a, b, c vẽ mặt cắt dọc; phần xám là thành bạc). "
               "L: chiều dài, D: đường kính ngoài, d: đường kính lỗ.")


# Hình 2: yêu cầu kỹ thuật trên bạc có gờ
def fig_yeu_cau():
    o = []
    ax = 112
    top = [(80, 28), (110, 28), (110, 62), (330, 62), (330, 88), (80, 88)]
    o += [P(top), P(mirror(top, ax)), Ln(62, ax, 350, ax, w=1, dash="6 4")]
    # lỗ: xanh dương; mặt ngoài: cam; mặt đầu A (mặt gờ bên trái): xanh lá
    o.append(Ln(80, 88, 330, 88, BLUE, 3.2))
    o.append(Ln(80, 136, 330, 136, BLUE, 3.2))
    o.append(Ln(110, 62, 330, 62, ORANGE, 3.2))
    o.append(Ln(110, 162, 330, 162, ORANGE, 3.2))
    o.append(Ln(80, 28, 80, 88, GREEN, 3.2))
    o.append(Ln(80, 136, 80, 196, GREEN, 3.2))
    o.append(T(66, 60, "A", 14, "middle", "700", GREEN))
    o.append(T(220, 104, "lỗ", 13, "middle", "700", BLUE))
    o.append(T(220, 52, "mặt ngoài", 13, "middle", "700", ORANGE))
    o.append(T(12, 226, "◎ Mặt ngoài đồng tâm với lỗ: thường 0,015 mm", 13, "start", "400", ORANGE))
    o.append(T(12, 246, "⊥ Mặt đầu A vuông góc với tâm lỗ", 13, "start", "400", GREEN))
    o.append(T(12, 266, "Lỗ: cấp 7, Ra 2,5 ÷ 0,63 µm", 13, "start", "400", BLUE))
    o.append(T(12, 286, "Mặt ngoài: cấp 7 ÷ 10", 13, "start", "400", ORANGE))
    return fig(svg(296, "Yêu cầu kỹ thuật chính của bạc có gờ", o),
               "Hình 2. Hai yêu cầu chính của bạc: mặt ngoài (cam) đồng tâm với lỗ (xanh), "
               "mặt đầu A (xanh lá) vuông góc với tâm lỗ.")


# Hình 3: phương án 1 — một lần gá trên phôi thanh, cắt đứt cuối (chữ 15 để còn ≥13 px ở 375 px)
def fig_mot_lan_ga():
    o = []
    ax = 110
    # mâm cặp: hai chấu kẹp phôi, mỗi chấu một lực W (đầu mũi tên cách chấu 8 px)
    o.append(P([(20, 52), (90, 52), (90, 76), (20, 76)], GREY))
    o.append(P([(20, 144), (90, 144), (90, 168), (20, 168)], GREY))
    o.append(T(98, 44, "mâm cặp", 15))
    o.append(Ar(55, 10, 55, 44, RED))
    o.append(T(63, 24, "W", 15, "start", "700", RED))
    o.append(Ar(55, 210, 55, 176, RED))
    o.append(T(63, 204, "W", 15, "start", "700", RED))
    bar_top = [(20, 76), (268, 76), (268, 144), (20, 144)]
    o.append(P(bar_top, 'fill="#94a3b8" fill-opacity="0.18" stroke="currentColor" stroke-width="1.4"'))
    part_top = [(268, 84), (380, 84), (380, 98), (268, 98)]
    o += [P(part_top), P(mirror(part_top, ax))]
    o.append(Ln(268, 84, 380, 84, ORANGE, 3))
    o.append(Ln(268, 136, 380, 136, ORANGE, 3))
    o.append(Ln(262, 98, 380, 98, BLUE, 3))
    o.append(Ln(262, 122, 380, 122, BLUE, 3))
    o.append(Ln(262, 98, 262, 122, BLUE, 1.4))
    o.append(Ln(380, 84, 380, 98, GREEN, 3))
    o.append(Ln(380, 122, 380, 136, GREEN, 3))
    o.append(Ln(10, ax, 400, ax, w=1, dash="6 4"))
    o.append(Ln(268, 66, 268, 154, RED, 2.2, "5 3"))
    o.append(T(268, 178, "cắt đứt (bước cuối)", 15, "middle", "700", RED))
    o.append(T(12, 240, "Cùng một lần gá:", 15, "start", "700"))
    o.append(T(12, 262, "mặt ngoài (cam)", 15, "start", "400", ORANGE))
    o.append(T(12, 284, "lỗ (xanh dương)", 15, "start", "400", BLUE))
    o.append(T(12, 306, "mặt đầu (xanh lá)", 15, "start", "400", GREEN))
    return fig(svg(316, "Phương án một lần gá trên phôi thanh", o),
               "Hình 3. Phương án 1: phôi thanh kẹp trên mâm cặp, tiện xong mặt ngoài, lỗ, mặt đầu "
               "rồi mới cắt đứt, nên các mặt chính đồng tâm với nhau.")


# Hình 4: phương án 2 — hai lần gá (Gá 2 lật bạc: mặt đầu vừa tiện ở Gá 1 thành mặt tì bên trái)
def fig_hai_lan_ga():
    o = []
    ax = 100
    for k, ox in enumerate((0, 210)):
        top = [(ox + 60, 60), (ox + 170, 60), (ox + 170, 80), (ox + 60, 80)]
        if k == 1:
            # trục gá đàn hồi: vai tì phủ cả vành mặt đầu (y 56–144) + thân nằm trong lỗ
            o.append(P([(ox + 36, 56), (ox + 58, 56), (ox + 58, 144), (ox + 36, 144)], GREY))
            o.append(P([(ox + 58, 81), (ox + 196, 81), (ox + 196, 119), (ox + 58, 119)], GREY))
        o += [P(top), P(mirror(top, ax))]
        o.append(Ln(ox + 22, ax, ox + 204, ax, w=1, dash="6 4"))
    # Gá 1: chuẩn = mặt ngoài (2, cả hai nửa) + mặt đầu trái (3); gia công lỗ + mặt đầu phải
    o.append(Ln(60, 60, 170, 60, BLUE, 3))
    o.append(Ln(60, 140, 170, 140, BLUE, 3))
    o.append(Ln(60, 60, 60, 80, BLUE, 3))
    o.append(Ln(60, 120, 60, 140, BLUE, 3))
    o.append(Ln(60, 80, 170, 80, ORANGE, 3))
    o.append(Ln(60, 120, 170, 120, ORANGE, 3))
    o.append(Ln(170, 60, 170, 80, ORANGE, 3))
    o.append(Ln(170, 120, 170, 140, ORANGE, 3))
    o.append(loc(96, 60, 0, 1, 2, 114, 56, size=15))
    o.append(loc(60, 130, 1, 0, 3, 38, 136, size=15))
    o.append(Ar(120, 182, 120, 148, RED))
    o.append(T(128, 176, "W", 15, "start", "700", RED))
    o.append(T(105, 18, "Gá 1", 16, "middle", "700"))
    o.append(T(105, 38, "chuẩn: ngoài + mặt đầu", 15, "middle", "400", BLUE))
    o.append(T(105, 208, "→ gia công lỗ,", 15, "middle", "400", ORANGE))
    o.append(T(105, 228, "mặt đầu bên kia", 15, "middle", "400", ORANGE))
    # Gá 2 (lật bạc): chuẩn = lỗ (2) + mặt đầu vừa gia công ở Gá 1, nay ở bên trái (3)
    ox = 210
    o.append(Ln(ox + 60, 80, ox + 170, 80, BLUE, 3))
    o.append(Ln(ox + 60, 120, ox + 170, 120, BLUE, 3))
    o.append(Ln(ox + 60, 60, ox + 60, 80, BLUE, 3))
    o.append(Ln(ox + 60, 120, ox + 60, 140, BLUE, 3))
    o.append(Ln(ox + 60, 60, ox + 170, 60, ORANGE, 3))
    o.append(Ln(ox + 60, 140, ox + 170, 140, ORANGE, 3))
    o.append(Ln(ox + 170, 60, ox + 170, 80, ORANGE, 3))
    o.append(Ln(ox + 170, 120, ox + 170, 140, ORANGE, 3))
    o.append(loc(ox + 60, 70, 1, 0, 3, ox + 26, 76, size=15))
    o.append(loc(ox + 156, 81, 0, -1, 2, ox + 186, 76, size=15))
    o.append(T(ox + 105, 168, "trục gá đàn hồi", 15, "middle"))
    o.append(T(ox + 105, 18, "Gá 2 (lật bạc)", 16, "middle", "700"))
    o.append(T(ox + 105, 38, "chuẩn: lỗ + mặt đầu", 15, "middle", "400", BLUE))
    o.append(T(ox + 105, 208, "→ gia công ngoài,", 15, "middle", "400", ORANGE))
    o.append(T(ox + 105, 228, "mặt đầu bên kia", 15, "middle", "400", ORANGE))
    o.append(T(12, 258, "Xanh dương: mặt chuẩn", 15, "start", "400", BLUE))
    o.append(T(12, 278, "Số: bậc tự do khống chế", 15, "start", "400", BLUE))
    o.append(T(12, 298, "Cam: mặt gia công trong lần gá đó", 15, "start", "400", ORANGE))
    return fig(svg(308, "Phương án hai lần gá: ngoài làm chuẩn gia công lỗ, lỗ làm chuẩn gia công ngoài", o),
               "Hình 4. Phương án 2. Gá 1 lấy mặt ngoài + mặt đầu làm chuẩn để gia công lỗ và mặt đầu bên kia. "
               "Gá 2 lật bạc, lồng lên trục gá theo lỗ, tì mặt đầu vừa gia công để gia công mặt ngoài.")


# Hình 5: kiểm tra độ đồng tâm bằng trục tâm và đồng hồ so
def fig_kiem_dong_tam():
    o = []
    ax = 128
    o.append(P([(40, 112), (40, 144), (70, ax)], GREY))
    o.append(P([(370, 112), (370, 144), (340, ax)], GREY))
    o.append(P([(70, 114), (340, 114), (340, 142), (70, 142)], GREY))
    top = [(150, 84), (270, 84), (270, 114), (150, 114)]
    o += [P(top), P(mirror(top, ax))]
    o.append(Ln(30, ax, 410, ax, w=1, dash="6 4"))
    o.append(Ln(150, 84, 270, 84, ORANGE, 3))
    gx, gy, gr = 210, 34, 18
    o.append(f'<circle cx="{gx}" cy="{gy}" r="{gr}" fill="none" stroke="currentColor" stroke-width="1.8"/>')
    o.append(Ln(gx, gy, gx + 9, gy - 10, RED, 1.8))
    o.append(Ln(gx, gy + gr, gx, 84, "currentColor", 2.4))
    # mũi tên quay đặt trên đường tâm, ngoài mũi tâm phải (không đè trục tâm)
    o.append(Rot(392, ax, 7, 30, -60, 60))
    labels = [(gx + 28, 30, "đồng hồ so", "start"), (12, 176, "mũi tâm", "start"),
              (110, 168, "trục tâm", "middle"), (210, 198, "bạc cần kiểm", "middle"), (404, 86, "quay", "end")]
    for x, y, s, a in labels:
        assert_clear_of_circle(text_box(x, y, s, 15, a), gx, gy, gr, name=s)
        o.append(T(x, y, s, 15, a))
    o.append(T(12, 232, "Quay bạc một vòng, đọc dao động kim", 15))
    o.append(T(12, 254, "Trục tâm khít lỗ, nên kim báo", 15))
    o.append(T(12, 276, "độ lệch giữa mặt ngoài và lỗ", 15))
    return fig(svg(286, "Kiểm tra độ đồng tâm của bạc bằng trục tâm và đồng hồ so", o),
               "Hình 5. Kiểm độ đồng tâm: bạc lồng trên trục tâm chống hai mũi tâm, "
               "đầu đồng hồ so chạm mặt ngoài.")


# Hình 6: kẹp ba chấu bóp méo thành mỏng (phóng đại)
def fig_kep_meo():
    o = []
    R, r, a = 40, 30, 4.5
    jaws = (-90, 30, 150)

    def ring(cx, cy, fr, n=120):
        pts = [(cx + fr(t) * math.cos(t), cy + fr(t) * math.sin(t))
               for t in (2 * math.pi * i / n for i in range(n))]
        return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"

    lobe = lambda t: math.cos(3 * (t + math.pi / 2))  # = 1 tại vị trí ba chấu
    for k, cx in enumerate((105, 315)):
        cy = 112
        if k == 0:
            outer = ring(cx, cy, lambda t: R - a * lobe(t))
            inner = ring(cx, cy, lambda t: r)
        else:
            outer = ring(cx, cy, lambda t: R)
            inner = ring(cx, cy, lambda t: r + a * lobe(t))
        o.append(f'<path d="{outer} {inner}" fill="#94a3b8" fill-opacity="0.32" fill-rule="evenodd" '
                 f'stroke="currentColor" stroke-width="1.4"/>')
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="4 3"/>')
        if k == 0:
            for deg in jaws:
                t = math.radians(deg)
                ux, uy, vx, vy = math.cos(t), math.sin(t), -math.sin(t), math.cos(t)
                q = [(cx + ux * rr + vx * s, cy + uy * rr + vy * s) for rr, s in
                     ((R - a + 0.5, -8), (R - a + 0.5, 8), (R + 10, 8), (R + 10, -8))]
                o.append(P(q, GREY))
                o.append(Ar(cx + ux * (R + 34), cy + uy * (R + 34), cx + ux * (R + 18), cy + uy * (R + 18), RED, 2.2, 8))
    o.append(T(105, 18, "Lúc kẹp", 13, "middle", "700"))
    o.append(T(315, 18, "Sau khi tháo", 13, "middle", "700"))
    for x, y, s in ((105, 210, "thành bị ép méo,"), (105, 226, "lỗ tiện tròn"),
                    (315, 210, "thành bật lại tròn,"), (315, 226, "lỗ thành méo")):
        for cx0 in (105, 315):
            assert_clear_of_circle(text_box(x, y, s, 13, "middle"), cx0, 112, R + 34, name=s)
        o.append(T(x, y, s, 13, "middle"))
    o.append(T(12, 254, "Nét đứt xanh: lỗ tròn chuẩn để so", 13, "start", "400", BLUE))
    return fig(svg(264, "Kẹp ba chấu làm méo bạc thành mỏng, vẽ phóng đại", o),
               "Hình 6. Kẹp ba chấu thật chặt (vẽ phóng đại): thành mỏng bị ép méo, lỗ tiện tròn lúc kẹp "
               "nhưng méo ba múi khi tháo ra.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in (("<!--FIG1-->", fig_loai_bac), ("<!--FIG2-->", fig_yeu_cau), ("<!--FIG3-->", fig_mot_lan_ga),
               ("<!--FIG4-->", fig_hai_lan_ga), ("<!--FIG5-->", fig_kiem_dong_tam), ("<!--FIG6-->", fig_kep_meo)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
assert src.count("__PHUT__") == 1
tmp = HERE / ".theory.tmp.html"
tmp.write_text(src.replace("__PHUT__", "15"), encoding="utf8")
try:
    phut = round(lint_do_dai.kiem(str(tmp))["phut"])
finally:
    tmp.unlink()
src = src.replace("__PHUT__", str(phut))
assert "__" not in src
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html, đọc ~", phut, "phút")
