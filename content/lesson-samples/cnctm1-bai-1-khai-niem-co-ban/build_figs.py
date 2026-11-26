#!/usr/bin/env python3
"""Sinh hình SVG cho CNCTM 1 – Bài 1, thay <!--FIGn--> trong theory.src.html → theory.html.
Hình 2 và Hình 3 (thành phần lồng nhau, chốt bậc) viết thẳng SVG trong theory.src.html.
Dùng: python3 build_figs.py  (chạy lại an toàn: luôn đọc từ theory.src.html)
"""
import math
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
FONT = 'font-family="system-ui, sans-serif" font-size="13"'
RED, GREEN, BLUE, ORANGE = "#dc2626", "#059669", "#0284c7", "#ea580c"


def fig(svg, cap):
    return f'<figure class="fig" data-tl="1">{svg}<figcaption>{cap}</figcaption></figure>'


def svg_open(w, h, label):
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}" {FONT}>'


def text(x, y, s, size=None, color="currentColor", bold=False, anchor=None):
    a = f' font-size="{size}"' if size else ""
    a += ' font-weight="700"' if bold else ""
    a += f' text-anchor="{anchor}"' if anchor else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}"{a}>{s}</text>'


def chev(x, y, dx, dy, color="currentColor", L=8, w=1.8):
    """Mũi chevron 30°: đỉnh tại (x,y), hướng chuyển động (dx,dy)."""
    n = math.hypot(dx, dy)
    bx, by = -dx / n, -dy / n
    pts = []
    for a in (math.radians(30), -math.radians(30)):
        rx = bx * math.cos(a) - by * math.sin(a)
        ry = bx * math.sin(a) + by * math.cos(a)
        pts.append((x + L * rx, y + L * ry))
    (x1, y1), (x2, y2) = pts
    return (f'<path d="M{x1:.1f} {y1:.1f} L{x:.1f} {y:.1f} L{x2:.1f} {y2:.1f}" fill="none" '
            f'stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def arrow(x1, y1, x2, y2, color="currentColor", w=1.8):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{w}"/>'
            + chev(x2, y2, x2 - x1, y2 - y1, color, w=w))


# ---------------------------------------------------------------- Hình 1: dòng chảy quá trình sản xuất
def fig1():
    o = [svg_open(420, 384, "Dòng chảy từ kho phôi đến kho thành phẩm")]
    steps = [("Kho phôi", 0), ("Chế tạo phôi (đúc, rèn)", 1), ("Gia công cắt gọt", 1),
             ("Nhiệt luyện (tôi, ram)", 1), ("Lắp ráp, kiểm tra", 1), ("Sơn, đóng gói", 0),
             ("Kho thành phẩm", 0)]
    x, w, h = 20, 210, 30
    for i, (s, cn) in enumerate(steps):
        y = 14 + i * 46
        if cn:
            o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{GREEN}" fill-opacity="0.15" '
                     f'stroke="{GREEN}" stroke-width="2"/>')
        else:
            o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="none" stroke="{ORANGE}" '
                     f'stroke-width="2" stroke-dasharray="6 4"/>')
        o.append(text(x + w / 2, y + 20, s, anchor="middle"))
        if i < len(steps) - 1:
            o.append(arrow(x + w / 2, y + h + 2, x + w / 2, y + 46 - 2))
    # ngoặc quá trình công nghệ: hộp 1..4 (y 60 → 228)
    y1, y2 = 60, 228
    o.append(f'<path d="M244 {y1} H252 V{y2} H244" fill="none" stroke="{GREEN}" stroke-width="2"/>')
    o.append(text(260, 140, "Quá trình", color=GREEN, bold=True))
    o.append(text(260, 158, "công nghệ", color=GREEN, bold=True))
    # ngoặc quá trình sản xuất: cả dòng (y 14 → 320)
    o.append('<path d="M332 14 H340 V320 H332" fill="none" stroke="currentColor" stroke-width="2"/>')
    o.append(text(346, 160, "Quá trình", bold=True))
    o.append(text(346, 178, "sản xuất", bold=True))
    # chú giải
    o.append(f'<rect x="20" y="340" width="26" height="14" rx="3" fill="none" stroke="{ORANGE}" stroke-width="2" '
             f'stroke-dasharray="6 4"/>')
    o.append(text(54, 352, "khung đứt: quá trình phụ", size=12))
    o.append(arrow(22, 372, 46, 372))
    o.append(text(54, 377, "mũi tên: vận chuyển, cũng là quá trình phụ", size=12))
    o.append("</svg>")
    return fig("".join(o), "Hình 1. Khung xanh làm thay đổi chính chi tiết, nên thuộc quá trình công nghệ.")


# ---------------------------------------------------------------- Hình 4: gá A, gá B trên máy tiện
def shaft_panel(oy, title, segs, tool_x, ends=None):
    """segs: [(x0, x1, nửa_chiều_cao, nét_màu)], dao ở tool_x cắt tại nửa chiều cao bên phải."""
    o = []
    a = oy + 95
    o.append(text(14, oy + 18, title, bold=True))
    # đường tâm
    o.append(f'<line x1="22" y1="{a}" x2="398" y2="{a}" stroke="currentColor" stroke-width="0.8" '
             f'stroke-dasharray="10 3 2 3"/>')
    # mũi tâm hai đầu
    for bx, tip, base in ((30, 80, 62), (358, 340, 358)):
        o.append(f'<rect x="{bx}" y="{a - 12}" width="32" height="24" fill="currentColor" fill-opacity="0.12" '
                 f'stroke="currentColor" stroke-width="1.5"/>')
        o.append(f'<polygon points="{base},{a - 10} {tip},{a} {base},{a + 10}" fill="currentColor" '
                 f'fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>')
    o.append(text(24, a + 32, "mũi tâm", size=12))
    o.append(text(352, a + 32, "mũi tâm", size=12))
    # phôi
    for x0, x1, hh, col in segs:
        o.append(f'<rect x="{x0}" y="{a - hh}" width="{x1 - x0}" height="{2 * hh}" fill="{col}" fill-opacity="0.12" '
                 f'stroke="{col}" stroke-width="2"/>')
    # dao: đỉnh chạm mặt vừa cắt
    hc = segs[-1][2]
    t = a - hc
    o.append(f'<polygon points="{tool_x},{t} {tool_x + 10},{t - 14} {tool_x + 10},{t - 34} {tool_x - 4},{t - 34} '
             f'{tool_x - 4},{t - 12}" fill="{BLUE}" fill-opacity="0.3" stroke="{BLUE}" stroke-width="1.8"/>')
    o.append(text(tool_x + 16, t - 22, "dao", size=12, color=BLUE))
    # chạy dao sang trái
    ya = t - 26
    o.append(arrow(tool_x - 12, ya, tool_x - 58, ya, RED))
    o.append(text(tool_x - 64, ya - 8, "chạy dao", size=12, color=RED))
    # phôi quay: cung dưới phôi
    hl = max(s[2] for s in segs)
    yq = a + hl + 6
    o.append(f'<path d="M100 {yq} A25 9 0 0 0 150 {yq}" fill="none" stroke="{RED}" stroke-width="1.8"/>')
    o.append(chev(150, yq, 0, -1, RED))
    o.append(text(158, yq + 14, "phôi quay", size=12, color=RED))
    if ends:
        for x, s, col in ends:
            o.append(text(x, a - hl - 8, s, size=12, color=col, bold=True))
    return o


def fig4():
    o = [svg_open(420, 300, "Gá A và gá B khi tiện chốt bậc")]
    # Gá A: Ø32 (nửa 22) bên trái dao, Ø30 (nửa 18) bên phải dao
    o += shaft_panel(0, "Gá A: bước 1, tiện Ø32 → Ø30",
                     [(80, 230, 22, "currentColor"), (230, 340, 18, "currentColor")], 230,
                     ends=[(84, "đầu C", BLUE), (296, "đầu A", ORANGE)])
    o.append('<line x1="10" y1="150" x2="410" y2="150" stroke="currentColor" stroke-width="0.8" '
             'stroke-dasharray="4 4" opacity="0.6"/>')
    # Gá B: trở đầu; đầu A (Ø30) bên trái, trụ C: Ø30 chưa cắt | Ø18 đã cắt
    o += shaft_panel(150, "Gá B (trở đầu): bước 2–4, tiện trụ C",
                     [(80, 121, 18, ORANGE), (121, 250, 18, "currentColor"), (250, 340, 11, BLUE)], 250,
                     ends=[(92, "A", ORANGE), (300, "C", BLUE)])
    o.append("</svg>")
    return fig("".join(o), "Hình 4. Trở đầu là tháo phôi ra, kẹp lại: một lần gá mới.")


# ---------------------------------------------------------------- Hình 5: phay đầu vuông trên đầu phân độ
def fig5():
    o = [svg_open(420, 252, "Phay bốn mặt đầu vuông nhờ đầu phân độ")]
    cx, cy, r = 140, 125, 75
    o.append(text(10, 20, "Nhìn dọc trục, từ đầu A", size=12))
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="currentColor" stroke-width="1.5" '
             f'stroke-dasharray="6 4"/>')
    o.append(f'<rect x="{cx - 50}" y="{cy - 50}" width="100" height="100" fill="{ORANGE}" fill-opacity="0.12" '
             f'stroke="currentColor" stroke-width="2.2"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="currentColor"/>')
    for x, y, s in ((cx, cy - 28, "1"), (cx + 32, cy + 5, "2"), (cx, cy + 38, "3"), (cx - 32, cy + 5, "4")):
        o.append(text(x, y, s, color=ORANGE, bold=True, anchor="middle"))
    # dao phay trên mặt 1
    o.append(f'<rect x="{cx - 45}" y="40" width="90" height="35" rx="4" fill="{BLUE}" fill-opacity="0.25" '
             f'stroke="{BLUE}" stroke-width="1.8"/>')
    o.append(text(cx + 54, 52, "dao phay", size=12, color=BLUE))
    # đầu phân độ quay 90°: cung r=92, từ 0° đến 70°
    R = 92
    a0, a1 = 0, math.radians(70)
    p0 = (cx + R * math.cos(a0), cy + R * math.sin(a0))
    p1 = (cx + R * math.cos(a1), cy + R * math.sin(a1))
    o.append(f'<path d="M{p0[0]:.1f} {p0[1]:.1f} A{R} {R} 0 0 1 {p1[0]:.1f} {p1[1]:.1f}" fill="none" '
             f'stroke="{RED}" stroke-width="2"/>')
    o.append(chev(p1[0], p1[1], -math.sin(a1), math.cos(a1), RED))
    o.append(text(222, 212, "đầu phân độ", size=12, color=RED))
    o.append(text(222, 228, "quay 90°", size=12, color=RED))
    # ghi chú bên phải
    o.append(text(262, 104, "4 vị trí, 1 lần gá", bold=True))
    o.append(text(262, 124, "phôi không tháo ra", size=12))
    o.append(text(262, 142, "giữa các mặt", size=12))
    o.append(text(10, 244, "nét đứt: Ø30 trước khi phay", size=12))
    o.append("</svg>")
    return fig("".join(o), "Hình 5. Mỗi lần xoay 90° là một vị trí mới.")


# ---------------------------------------------------------------- Hình 6: dải sản lượng, chi tiết < 4 kg
def fig6():
    o = [svg_open(420, 170, "Dải sản lượng theo dạng sản xuất, chi tiết dưới 4 kg")]
    x0, x1, lo, hi = 20, 400, 1.0, math.log10(500000)

    def X(n):
        return x0 + (x1 - x0) * (math.log10(n) - lo) / (hi - lo)

    bounds = [10, 100, 500, 5000, 50000, 500000]
    names = [("Đơn", "chiếc"), ("Loạt", "nhỏ"), ("Loạt", "vừa"), ("Loạt", "lớn"), ("Hàng", "khối")]
    ops = [0.04, 0.09, 0.3, 0.16, 0.24]
    yt, yb = 62, 112
    for i, (a, b) in enumerate(names):
        xa, xb = X(bounds[i]), X(bounds[i + 1])
        hl = i == 2
        col = GREEN if hl else "currentColor"
        o.append(f'<rect x="{xa:.1f}" y="{yt}" width="{xb - xa:.1f}" height="{yb - yt}" fill="{col}" '
                 f'fill-opacity="{0.3 if hl else ops[i]}" stroke="currentColor" stroke-width="1.2"/>')
        xm = (xa + xb) / 2
        o.append(text(xm, 83, a, anchor="middle", bold=hl))
        o.append(text(xm, 101, b, anchor="middle", bold=hl))
    o.append(f'<line x1="{x0}" y1="{yb}" x2="{x1 + 8}" y2="{yb}" stroke="currentColor" stroke-width="1.5"/>')
    o.append(chev(x1 + 8, yb, 1, 0))
    for n, s in ((100, "100"), (500, "500"), (5000, "5.000"), (50000, "50.000")):
        o.append(f'<line x1="{X(n):.1f}" y1="{yb}" x2="{X(n):.1f}" y2="{yb + 6}" stroke="currentColor" '
                 f'stroke-width="1.5"/>')
        o.append(text(X(n), yb + 22, s, size=12, anchor="middle"))
    o.append(text(x0, 160, "N (chiếc/năm), thang lôgarit", size=12))
    o.append(text(x0, 20, "Cột chi tiết &lt; 4 kg", bold=True))
    # điểm ví dụ máy bơm
    xp = X(2200)
    o.append(text(xp, 38, "trục bơm: N = 2.200", size=12, color=RED, anchor="middle"))
    o.append(arrow(xp, 43, xp, yt - 3, RED))
    o.append("</svg>")
    return fig("".join(o), "Hình 6. Trục bơm 2,5 kg, N = 2.200 rơi vào dải hàng loạt vừa.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in (("<!--FIG1-->", fig1), ("<!--FIG4-->", fig4), ("<!--FIG5-->", fig5), ("<!--FIG6-->", fig6)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
