#!/usr/bin/env python3
"""Sinh hình SVG cho CNCTM 1 – Bài 13 (Gia công mặt định hình), thay <!--FIGn--> trong theory.src.html → theory.html.
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



TOOL = 'fill="#64748b" fill-opacity="0.45" stroke="currentColor" stroke-width="1.4"'
WORK = METAL + ' stroke="currentColor" stroke-width="1.5"'


def path(d, c="currentColor", w=1.5, fill="none", extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{c}" stroke-width="{w}" {extra}/>'


# Hình 1: bốn loại mặt định hình
def fig_bon_loai():
    o = []
    # a) mặt côn
    o.append(Ln(30, 55, 186, 55, w=1, dash="6 4"))
    o.append(P([(50, 30), (160, 45), (160, 65), (50, 80)], WORK))
    o.append(Ln(50, 30, 160, 45, RED, 3))
    o.append(Rot(176, 55, 6, 18, -70, 70))
    o.append(T(105, 112, "a) Mặt côn", 13, "middle", "700"))
    o.append(T(105, 129, "chuôi côn, lỗ côn trục chính", 12, "middle"))
    # b) mặt tròn xoay
    o.append(Ln(232, 55, 404, 55, w=1, dash="6 4"))
    o.append(path("M240,45 C280,45 300,22 340,22 C372,22 388,38 388,55 C388,72 372,88 340,88 C300,88 280,65 240,65 Z",
                  fill="#94a3b8", extra='fill-opacity="0.28"'))
    o.append(path("M240,45 C280,45 300,22 340,22 C372,22 388,38 388,55", RED, 3))
    o.append(T(315, 112, "b) Mặt tròn xoay", 13, "middle", "700"))
    o.append(T(315, 129, "tay nắm, mặt cầu", 12, "middle"))
    # c) cam đĩa
    cx, cy = 105, 190
    pts = []
    for i in range(72):
        t = math.radians(i * 5)
        r = 30 + 16 * max(0.0, math.cos(t)) ** 2
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    o.append(P(pts, WORK))
    o.append(P(pts, f'fill="none" stroke="{RED}" stroke-width="2.6"'))
    o.append(f'<circle cx="{cx}" cy="{cy}" r="7" fill="none" stroke="currentColor" stroke-width="1.4"/>')
    o.append(T(105, 252, "c) Định hình đường thẳng", 13, "middle", "700"))
    o.append(T(105, 269, "cam đĩa, cam trống", 12, "middle"))
    # d) khối
    o.append(path("M250,215 C262,170 300,150 350,160 C385,167 392,190 372,205 C345,224 300,232 250,215 Z",
                  RED, 2.6, "#94a3b8", 'fill-opacity="0.28"'))
    for k in range(4):
        x = 280 + 24 * k
        o.append(Ln(x, 170 + (6 if k == 0 else 0), x + 10, 222 - 4 * k, w=1, dash="4 3"))
    o.append(T(315, 252, "d) Mặt định hình khối", 13, "middle", "700"))
    o.append(T(315, 269, "cánh tuabin, khuôn mẫu", 12, "middle"))
    return fig(svg(280, "Bốn loại mặt định hình", o),
               "Hình 1. Bốn loại mặt định hình. Nét đỏ là đường sinh hoặc đường bao tạo nên mặt.")


# Hình 2: dao lưỡi rộng và quay con trượt trên
def fig_tien_con_ngan():
    o = []
    o.append(T(105, 18, "a) Dao lưỡi rộng", 13, "middle", "700"))
    o.append(Ln(12, 80, 196, 80, w=1, dash="6 4"))
    o.append(P([(20, 50), (130, 50), (150, 62), (150, 98), (130, 110), (20, 110)], WORK))
    o.append(P([(134, 115), (156, 102), (186, 132), (164, 145)], TOOL))
    o.append(Ln(134, 115, 156, 102, RED, 3))
    o.append(Ar(196, 150, 176, 132))
    o.append(T(105, 172, "lưỡi cắt nghiêng", 12, "middle"))
    o.append(T(105, 188, "đúng góc côn", 12, "middle"))
    o.append(T(105, 206, "côn dài ≤ 20 mm", 12, "middle", c=BLUE))
    o.append(T(315, 18, "b) Quay con trượt trên", 13, "middle", "700"))
    o.append(Ln(222, 80, 408, 80, w=1, dash="6 4"))
    o.append(P([(230, 50), (320, 50), (380, 68), (380, 92), (320, 110), (230, 110)], WORK))
    dx, dy = 60, -18
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux                      # pháp tuyến hướng xuống
    x0, y0 = 300, 140
    o.append(P([(x0 - 6 * nx, y0 - 6 * ny), (x0 + 96 * ux - 6 * nx, y0 + 96 * uy - 6 * ny),
                (x0 + 96 * ux + 14 * nx, y0 + 96 * uy + 14 * ny), (x0 + 14 * nx, y0 + 14 * ny)],
               'fill="#64748b" fill-opacity="0.25" stroke="currentColor" stroke-width="1.2"'))
    o.append(P([(344, 114), (360, 110), (352, 99)], TOOL))
    o.append(Ar(x0 + 8 * ux, y0 + 8 * uy - 16, x0 + 70 * ux, y0 + 70 * uy - 16))
    o.append(Ln(x0, y0, x0 + 60, y0, w=1, dash="4 3"))
    a = math.degrees(math.atan2(dy, dx))
    o.append(f'<path d="M{x0 + 40:.1f},{y0:.1f} A40,40 0 0,0 {x0 + 40 * ux:.1f},{y0 + 40 * uy:.1f}" fill="none" stroke="{BLUE}" stroke-width="1.4"/>')
    o.append(T(x0 + 46, y0 - 2, "α/2", 13, w="700", c=BLUE))
    o.append(T(315, 172, "con trượt quay α/2", 12, "middle"))
    o.append(T(315, 188, "tiến tay, côn ngắn", 12, "middle"))
    o.append(T(315, 206, "góc côn bất kỳ", 12, "middle", c=BLUE))
    _ = a
    return fig(svg(216, "Tiện côn bằng dao lưỡi rộng và quay con trượt trên", o),
               "Hình 2. Tiện côn ngắn. a) Lưỡi cắt đặt nghiêng đúng góc côn. b) Con trượt trên quay nửa góc côn α/2, dao tiến tay theo đường sinh.")


# Hình 3: đánh lệch ụ động
def fig_lech_u_dong():
    o = []
    o.append(Ln(12, 90, 408, 90, w=1, dash="6 4"))
    o.append(T(14, 84, "tâm máy", 12))
    o.append(P([(40, 64), (380, 82), (380, 134), (40, 116)], WORK))
    o.append(Ln(40, 90, 380, 108, w=1, dash="2 3"))
    o.append(P([(22, 80), (40, 90), (22, 100)], TOOL))
    o.append(P([(398, 98), (380, 108), (398, 118)], TOOL))
    o.append(P([(304, 36), (320, 36), (312, 70)], TOOL))
    o.append(Ar(290, 30, 160, 30))
    o.append(T(150, 24, "dao chạy dọc", 12, "end"))
    o.append(Ln(366, 90, 412, 90, BLUE, 1.2))
    o.append(Ln(366, 108, 412, 108, BLUE, 1.2))
    o.append(Ar(408, 72, 408, 90, BLUE, 1.4))
    o.append(Ar(408, 126, 408, 108, BLUE, 1.4))
    o.append(T(400, 150, "h", 14, "middle", "700", BLUE))
    o.append(T(12, 176, "Ụ động lệch h, trục chi tiết nghiêng α/2", 13))
    o.append(T(12, 196, "Dao chạy song song băng máy → mặt côn dài", 13))
    o.append(T(12, 216, "Sổ tay: h = L(D − d) / (2l)", 13, w="700"))
    o.append(T(12, 234, "L: dài chi tiết; l: dài đoạn côn", 12))
    return fig(svg(244, "Tiện côn bằng cách đánh lệch ụ động", o),
               "Hình 3. Đánh lệch ụ động (nhìn từ trên, độ lệch vẽ phóng to): chạy dao tự động nên mặt côn dài nhẵn và chính xác hơn tiến tay.")


# Hình 4: thước côn / dưỡng chép hình
def fig_thuoc_con():
    o = []
    o.append(Ln(20, 60, 400, 60, w=1, dash="6 4"))
    o.append(P([(40, 30), (120, 30), (360, 46), (360, 74), (120, 90), (40, 90)], WORK))
    k = 16 / 240
    yt = 90 - k * 140
    o.append(P([(250, 118), (270, 118), (260, yt + 1)], TOOL))
    o.append(P([(244, 118), (276, 118), (276, 140), (244, 140)], TOOL))
    yr = lambda x: 200 - (x - 100) * k
    o.append(Ln(100, yr(100), 380, yr(380), RED, 4))
    o.append(P([(248, yr(260) - 8), (272, yr(260) - 8), (272, yr(260) + 6), (248, yr(260) + 6)],
               'fill="#64748b" fill-opacity="0.6" stroke="currentColor" stroke-width="1.4"'))
    o.append(Ln(260, 140, 260, yr(260) - 8, w=2.5))
    o.append(T(96, 214, "thước côn nghiêng α/2", 12, "middle", c=RED))
    o.append(T(284, 134, "dao", 12))
    o.append(T(284, 154, "con trượt ngang", 12))
    o.append(T(284, 170, "đã tháo vít", 12))
    o.append(Ar(400, 228, 300, 228))
    o.append(T(296, 232, "xe dao chạy dọc", 12, "end"))
    o.append(T(12, 256, "Côn ≤ 10 ÷ 12°: hiệu quả và năng suất nhất", 13))
    o.append(T(12, 274, "Thay thước bằng dưỡng cong → tiện chép hình", 13))
    return fig(svg(284, "Tiện côn bằng thước côn", o),
               "Hình 4. Thước côn: con trượt ngang được tháo vít, khối trượt bám theo thước nghiêng nên dao vừa chạy dọc vừa lùi ra đều.")


# Hình 5: dao định hình
def fig_dao_dinh_hinh():
    o = []
    import math as m
    xs = [160 + 4 * i for i in range(36)]
    f = lambda x: 22 * m.sin(m.pi * (x - 160) / 140)
    top = [(x, 30 + f(x)) for x in xs]
    bot = [(x, 110 - f(x)) for x in reversed(xs)]
    o.append(Ln(40, 70, 390, 70, w=1, dash="6 4"))
    o.append(P([(60, 30)] + top + [(360, 30), (360, 110)] + bot + [(60, 110)], WORK))
    o.append(Rot(60, 70, 8, 30, 110, 250))
    prof = [(x, 124 - f(x)) for x in xs]
    o.append(P(prof + [(300, 172), (160, 172)], TOOL))
    o.append(PL(prof, RED, 3))
    o.append(Ar(330, 186, 330, 136))
    o.append(T(336, 162, "tiến ngang", 12))
    o.append(T(230, 160, "dao định hình", 12, "middle"))
    o.append(T(12, 206, "Prôfin lưỡi dao = prôfin chi tiết", 13, w="700"))
    o.append(T(12, 226, "Lưỡi rộng ≤ 60 mm, mài lại prôfin không đổi", 13))
    o.append(T(12, 246, "Dao đắt: sản lượng lớn mới kinh tế", 13))
    return fig(svg(256, "Tiện mặt tròn xoay bằng dao định hình", o),
               "Hình 5. Dao định hình chỉ cần tiến ngang một lần là ra cả đoạn prôfin, quãng chạy dao ngắn hơn chép hình.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in (("<!--FIG1-->", fig_bon_loai), ("<!--FIG2-->", fig_tien_con_ngan), ("<!--FIG3-->", fig_lech_u_dong),
               ("<!--FIG4-->", fig_thuoc_con), ("<!--FIG5-->", fig_dao_dinh_hinh)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
