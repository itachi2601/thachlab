#!/usr/bin/env python3
"""Sinh hình SVG cho CNCTM 1 – Bài 12 (Gia công bánh răng), thay <!--FIGn--> trong theory.src.html → theory.html.
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




def gear(cx, cy, rt, rr, z, rot=0.0, extra=None):
    """Đường bao bánh răng đơn giản (răng hình thang), rot tính bằng độ."""
    p = 360 / z
    pts = []
    for k in range(z):
        a = rot + k * p
        for da, r in ((-0.30, rr), (-0.14, rt), (0.14, rt), (0.30, rr)):
            t = math.radians(a + da * p)
            pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    return P(pts, extra or (METAL + ' stroke="currentColor" stroke-width="1.5"'))


# Hình 1: khe hở cạnh răng
def fig_khe_ho():
    o = []
    k = 15 / 70
    o.append(P([(40, 20), (380, 20), (380, 50), (40, 50)], METAL + ' stroke="currentColor" stroke-width="1.4"'))
    o.append(T(210, 40, "bánh răng 1", 13, "middle", "700"))
    for xl, xr in ((90, 150), (250, 310)):
        o.append(P([(xl, 50), (xr, 50), (xr - 15, 120), (xl + 15, 120)], METAL + ' stroke="currentColor" stroke-width="1.4"'))
    # răng bánh 2 chen vào rãnh, tựa sườn trái, hở sườn phải 14
    lx = lambda y: 150 - (y - 50) * k
    rx = lambda y: 250 + (y - 50) * k - 14
    o.append(P([(lx(70), 70), (rx(70), 70), (rx(170), 170), (lx(170), 170)], METAL + ' stroke="currentColor" stroke-width="1.4"'))
    o.append(P([(40, 170), (380, 170), (380, 200), (40, 200)], METAL + ' stroke="currentColor" stroke-width="1.4"'))
    o.append(T(210, 190, "bánh răng 2", 13, "middle", "700"))
    o.append(Ln(lx(72), 72, lx(118), 118, RED, 4))
    o.append(T(130, 150, "sườn đang tiếp xúc", 12, "end", c=RED))
    o.append(Ln(132, 146, 143, 112, RED, 1))
    y = 100
    o.append(Ar(222, y, rx(y) - 1, y, BLUE, 1.8))
    o.append(Ar(290, y, 250 + (y - 50) * k + 1, y, BLUE, 1.8))
    o.append(Ln(rx(140), 140, 292, 150, BLUE, 1))
    o.append(T(296, 154, "khe hở cạnh răng", 13, c=BLUE, w="700"))
    o.append(T(12, 228, "4 dạng: A bằng 0, B nhỏ, C trung bình, D lớn", 13))
    o.append(T(12, 248, "Khoảng cách tâm càng lớn, khe hở càng lớn", 13))
    return fig(svg(258, "Khe hở cạnh răng giữa hai bánh răng ăn khớp", o),
               "Hình 1. Khe hở cạnh răng: một sườn tiếp xúc, sườn kia để hở cho dầu bôi trơn và giãn nở nhiệt.")


# Hình 2: định hình và bao hình
def teeth_row(x0, pitch, n, o):
    for i in range(n):
        c = x0 + i * pitch
        o.append(P([(c - 14, 200), (c - 7, 150), (c + 7, 150), (c + 14, 200)], METAL + ' stroke="currentColor" stroke-width="1.3"'))


def fig_dinh_hinh_bao_hinh():
    o = []
    # a) định hình
    o.append(T(105, 18, "a) Định hình", 13, "middle", "700"))
    teeth_row(30, 40, 5, o)
    o.append(P([(16, 200), (204, 200), (204, 218), (16, 218)], METAL + ' stroke="currentColor" stroke-width="1.3"'))
    o.append(P([(60, 70), (120, 70), (120, 140), (103, 140), (96, 198), (84, 198), (77, 140), (60, 140)],
               'fill="#64748b" fill-opacity="0.4" stroke="currentColor" stroke-width="1.4"'))
    o.append(PL([(77, 140), (84, 198), (96, 198), (103, 140)], RED, 3))
    o.append(T(126, 62, "dao phay đĩa", 12))
    o.append(T(126, 78, "mô-đun", 12))
    o.append(Ar(112, 236, 150, 236))
    o.append(T(105, 256, "phân độ 360°/Z", 12, "middle"))
    o.append(T(105, 274, "sau mỗi rãnh", 12, "middle"))
    # b) bao hình
    o.append(T(315, 18, "b) Bao hình (phay lăn)", 13, "middle", "700"))
    o.append(Ln(226, 85, 404, 85, w=1, dash="6 4"))
    o.append(P([(240, 62), (388, 62), (388, 108), (240, 108)], 'fill="#64748b" fill-opacity="0.4" stroke="currentColor" stroke-width="1.4"'))
    for x in range(244, 380, 14):
        o.append(Ln(x, 108, x + 12, 62, RED, 1.6))
    o.append(T(314, 50, "dao phay lăn", 12, "middle"))
    o.append(Rot(396, 85, 7, 26, -70, 70))
    teeth_row(235, 40, 5, o)
    o.append(P([(220, 200), (410, 200), (410, 218), (220, 218)], METAL + ' stroke="currentColor" stroke-width="1.3"'))
    o.append(Ar(260, 236, 370, 236))
    o.append(T(315, 256, "phôi quay ăn khớp liên tục", 12, "middle"))
    o.append(T(315, 274, "không cần phân độ", 12, "middle"))
    return fig(svg(284, "Gia công răng định hình và bao hình", o),
               "Hình 2. a) Định hình: prôfin dao (đỏ) giống rãnh răng, cắt từng rãnh. b) Bao hình: dao phay lăn như trục vít, phôi như bánh vít.")


# Hình 3: bộ 8 dao phay mô-đun
def fig_bo_dao():
    o = []
    o.append(T(210, 20, "Bộ 8 dao phay mô-đun (cùng m, cùng góc ăn khớp)", 13, "middle", "700"))
    ranges = ["12÷13", "14÷16", "17÷20", "21÷25", "26÷34", "35÷54", "55÷134", "≥135"]
    for i, r in enumerate(ranges):
        x = 18 + 48 * i
        hl = i in (2, 6)
        fill = 'fill="#dc2626" fill-opacity="0.15"' if hl else METAL
        o.append(P([(x, 36), (x + 46, 36), (x + 46, 76), (x, 76)], fill + ' stroke="currentColor" stroke-width="1.3"'))
        o.append(T(x + 23, 62, f"số {i + 1}", 13, "middle", "700"))
        o.append(T(x + 23, 96, r, 12, "middle"))
    o.append(T(10, 116, "Z:", 12))
    for cx, s in ((138, "Z = 20 → dao số 3"), (330, "Z = 60 → dao số 7")):
        o.append(Ar(cx, 136, cx, 104))
        o.append(T(cx, 154, s, 13, "middle", "700", RED))
    o.append(T(12, 186, "Mỗi dao làm đúng prôfin cho một số răng;", 13))
    o.append(T(12, 204, "số răng khác trong khoảng chỉ gần đúng.", 13))
    return fig(svg(214, "Bộ 8 dao phay mô-đun và khoảng số răng", o),
               "Hình 3. Bộ 8 dao phay mô-đun: chọn dao theo số răng Z. Hai bánh răng cùng mô-đun nhưng Z khác nhau có thể cần hai dao khác nhau.")


# Hình 4: xọc răng bằng dao dạng bánh răng
def fig_xoc_rang():
    o = []
    o.append(gear(120, 130, 82, 70, 24))
    o.append(f'<circle cx="120" cy="130" r="18" fill="none" stroke="currentColor" stroke-width="1.3"/>')
    o.append(T(120, 112, "phôi", 13, "middle", "700"))
    o.append(Rot(120, 130, 42, 42, 20, 110))
    o.append(T(120, 192, "n phôi", 12, "middle", c=RED))
    o.append(gear(237, 130, 48, 36, 14, rot=180 + 180 / 14,
                  extra='fill="#64748b" fill-opacity="0.45" stroke="currentColor" stroke-width="1.5"'))
    o.append(T(237, 134, "dao", 13, "middle", "700"))
    o.append(Rot(237, 130, 26, 26, 160, 70))
    o.append(T(237, 196, "n dao", 12, "middle", c=RED))
    # hình chiếu đứng: dao xọc lên xuống
    o.append(T(362, 24, "nhìn ngang", 12, "middle"))
    o.append(Ln(362, 36, 362, 70, w=3))
    o.append(P([(336, 70), (388, 70), (388, 90), (336, 90)], 'fill="#64748b" fill-opacity="0.45" stroke="currentColor" stroke-width="1.4"'))
    o.append(P([(322, 120), (402, 120), (402, 176), (322, 176)], METAL + ' stroke="currentColor" stroke-width="1.4"'))
    o.append(T(362, 152, "phôi", 12, "middle"))
    o.append(Ar(316, 60, 316, 100))
    o.append(Ar(406, 100, 406, 60))
    o.append(T(362, 196, "dao xọc lên xuống", 12, "middle", c=RED))
    o.append(T(12, 232, "Tỉ số quay: n phôi / n dao = Z dao / Z phôi", 13))
    o.append(T(12, 252, "Xọc được bánh răng bậc; phay lăn thì không", 13))
    return fig(svg(262, "Xọc răng bao hình bằng dao dạng bánh răng", o),
               "Hình 4. Xọc răng bao hình: dao là một bánh răng có lưỡi cắt, quay ăn khớp với phôi và chạy lên xuống dọc trục.")


# Hình 5: chọn nguyên công tinh
def box(x, y, w, h, lines, o, color="currentColor", bold_first=True):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="none" stroke="{color}" stroke-width="1.6"/>')
    for i, s in enumerate(lines):
        o.append(T(x + w / 2, y + 22 + 19 * i, s, 13, "middle", "700" if (i == 0 and bold_first) else "400",
                   color if i == 0 else "currentColor"))


def fig_gia_cong_tinh():
    o = []
    box(100, 10, 220, 34, ["Răng sau phay lăn, xọc"], o)
    o.append(Ar(210, 44, 210, 66, "currentColor", 1.6))
    box(120, 68, 180, 34, ["Răng có tôi không?"], o)
    o.append(PL([(120, 85), (105, 85), (105, 128)], "currentColor", 1.6))
    o.append(Ar(105, 110, 105, 128, "currentColor", 1.6))
    o.append(PL([(300, 85), (315, 85), (315, 128)], "currentColor", 1.6))
    o.append(Ar(315, 110, 315, 128, "currentColor", 1.6))
    o.append(T(96, 106, "Không", 12, "end"))
    o.append(T(324, 106, "Có", 12))
    box(10, 130, 190, 90, ["Cà răng", "dư lớn nhất 0,15 mm", "tăng 1 ÷ 2 cấp", "Ra 0,63 ÷ 0,16 µm"], o, BLUE)
    box(220, 130, 190, 90, ["Tôi → mài răng", "đạt cấp 6 ÷ 4", "Ra 1,25 ÷ 0,32 µm", "bánh răng chính xác cao"], o, RED)
    o.append(T(12, 246, "Chạy rà: không phoi, ăn khớp với bánh mẫu đã tôi", 13))
    return fig(svg(256, "Chọn nguyên công gia công tinh răng", o),
               "Hình 5. Gia công tinh răng: chưa tôi thì cà, đã tôi thì mài.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in (("<!--FIG1-->", fig_khe_ho), ("<!--FIG2-->", fig_dinh_hinh_bao_hinh), ("<!--FIG3-->", fig_bo_dao),
               ("<!--FIG4-->", fig_xoc_rang), ("<!--FIG5-->", fig_gia_cong_tinh)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
