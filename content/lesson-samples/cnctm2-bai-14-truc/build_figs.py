#!/usr/bin/env python3
"""Sinh hình SVG cho CNCTM 2 – Bài 14 (Công nghệ gia công chi tiết dạng trục), thay <!--FIGn--> trong
theory.src.html → theory.html, rồi điền __PHUT__ bằng số phút đọc của lint_do_dai.py.
Dùng: python3 build_figs.py  (chạy lại an toàn: luôn đọc từ theory.src.html)
Hình vẽ nguyên lý tự vẽ, không theo tỉ lệ. Chữ ≥ 12 trong viewBox 420 (đọc được ở 375px).
Ký hiệu định vị: tam giác xanh đặc, đỉnh chạm mặt chuẩn, kèm số bậc tự do khống chế (như CNCTM 1 bài 4).
"""
import math
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import chevron  # noqa: E402

FONT = 'font-family="system-ui, sans-serif" font-size="13"'
RED, BLUE, GREEN, ORANGE = "#dc2626", "#0369a1", "#047857", "#ea580c"
METAL = 'fill="#94a3b8" fill-opacity="0.28"'
WORK = METAL + ' stroke="currentColor" stroke-width="1.5"'
TOOL = 'fill="#64748b" fill-opacity="0.45" stroke="currentColor" stroke-width="1.4"'
FIX = 'fill="#64748b" fill-opacity="0.18" stroke="currentColor" stroke-width="1.3"'
ALLOW = f'fill="{ORANGE}" fill-opacity="0.35" stroke="{ORANGE}" stroke-width="1"'


def T(x, y, s, size=13, anchor="start", w="400", c="currentColor"):
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{anchor}">{s}</text>'


def Ln(x1, y1, x2, y2, c="currentColor", w=1.5, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'


def Ar(x1, y1, x2, y2, c=RED, w=2.2, L=10):
    """Mũi tên thẳng, đầu chữ V 30°."""
    return Ln(x1, y1, x2, y2, c, w) + chevron(x2, y2, x2 - x1, y2 - y1, c, w, L=L)


def Dim(x1, y1, x2, y2, c=BLUE):
    """Đường kích thước hai đầu mũi tên."""
    return (Ln(x1, y1, x2, y2, c, 1.2) + chevron(x2, y2, x2 - x1, y2 - y1, c, 1.2, L=7)
            + chevron(x1, y1, x1 - x2, y1 - y2, c, 1.2, L=7))


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


def R(x, y, w, h, extra=WORK):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" {extra}/>'


def Loc(x, y, dx, dy, n, lx, ly, anchor="start"):
    """Ký hiệu định vị: tam giác xanh đặc, đỉnh tại (x, y), thân lùi theo hướng (dx, dy); số bậc n đặt ở (lx, ly)."""
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    bx, by = x + 14 * ux, y + 14 * uy
    px, py = -uy * 7, ux * 7
    return (P([(x, y), (bx + px, by + py), (bx - px, by - py)], f'fill="{BLUE}" stroke="none"')
            + T(lx, ly, str(n), 14, anchor, "700", BLUE))


def svg(h, label, body):
    return (f'<svg viewBox="0 0 420 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}" {FONT}>'
            + "".join(body) + "</svg>")


def fig(s, cap):
    return f'<figure class="fig" data-tl="1">{s}<figcaption>{cap}</figcaption></figure>'


def stepped(x0, cy, steps, extra=WORK):
    """Trục bậc nằm ngang: steps = [(dài, đường kính), …] từ trái sang; trả (polygon, danh sách x biên)."""
    top, bot, xs, x = [], [], [x0], x0
    for L, d in steps:
        top += [(x, cy - d / 2), (x + L, cy - d / 2)]
        bot += [(x, cy + d / 2), (x + L, cy + d / 2)]
        x += L
        xs.append(x)
    return P(top + bot[::-1], extra), xs


# Hình 1: bốn dạng trục
def fig_dang_truc():
    o = []
    # a) trục trơn
    o.append(T(12, 18, "a) Trục trơn", 13, w="700"))
    o.append(Ln(14, 56, 200, 56, w=1, dash="6 4"))
    o.append(R(24, 44, 166, 24))
    o.append(Dim(24, 84, 190, 84))
    o.append(T(107, 100, "L", 13, "middle", "700", BLUE))
    o.append(Dim(200, 44, 200, 68))
    o.append(T(206, 60, "d", 13, w="700", c=BLUE))
    o.append(T(12, 118, "L/d &lt; 4: ngắn", 12))
    o.append(T(12, 133, "L/d = 4 ÷ 10: thường", 12))
    o.append(T(12, 148, "L/d &gt; 10: dài", 12))
    # b) trục bậc có rãnh then
    o.append(T(232, 18, "b) Trục bậc, rãnh then", 13, w="700"))
    o.append(Ln(226, 66, 412, 66, w=1, dash="6 4"))
    poly, xs = stepped(236, 66, [(36, 22), (60, 38), (16, 48), (40, 30), (18, 20)])
    o.append(poly)
    o.append(f'<rect x="{xs[1] + 12:.1f}" y="{66 - 19 + 1:.1f}" width="34" height="8" rx="4" fill="{RED}" fill-opacity="0.75"/>')
    o.append(T(300, 110, "rãnh then (đỏ)", 12, "middle", c=RED))
    o.append(T(300, 126, "đường kính giảm dần về hai đầu", 12, "middle"))
    # c) trục rỗng (cắt dọc nửa trên)
    o.append(T(12, 180, "c) Trục rỗng", 13, w="700"))
    cy = 224
    o.append(Ln(14, cy, 200, cy, w=1, dash="6 4"))
    o.append(R(24, cy - 20, 166, 40))
    o.append(R(24, cy - 9, 166, 18, 'fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 3"'))
    o.append(T(107, 266, "lỗ suốt (nét đứt):", 12, "middle"))
    o.append(T(107, 282, "giảm khối lượng hoặc để lắp ghép", 12, "middle"))
    # d) trục lệch tâm
    o.append(T(232, 180, "d) Trục lệch tâm", 13, w="700"))
    o.append(Ln(226, cy, 412, cy, w=1, dash="6 4"))
    o.append(R(238, cy - 12, 50, 24))
    o.append(R(352, cy - 12, 50, 24))
    e = 16
    o.append(R(288, cy - e - 14, 64, 28, f'fill="{GREEN}" fill-opacity="0.25" stroke="{GREEN}" stroke-width="1.5"'))
    o.append(Ln(280, cy - e, 360, cy - e, GREEN, 1, "4 3"))
    o.append(Ln(320, cy - e, 320, cy, BLUE, 1.4))
    o.append(T(326, cy - e / 2 + 5, "e", 13, w="700", c=BLUE))
    o.append(T(320, 266, "cổ lệch (xanh lá) lệch tâm e", 12, "middle"))
    o.append(T(320, 282, "trục cam, trục khuỷu", 12, "middle"))
    return fig(svg(292, "Bốn dạng chi tiết trục: trơn, bậc, rỗng, lệch tâm", o),
               "Hình 1. Bốn dạng trục thường gặp. Nét gạch chấm là đường tâm trục.")


# Hình 2: trục gá trên hai mũi tâm
def fig_hai_mui_tam():
    o = []
    cy = 92
    o.append(Ln(12, cy, 408, cy, w=1, dash="8 3 2 3"))
    poly, xs = stepped(96, cy, [(50, 34), (110, 50), (40, 40), (36, 30)])
    o.append(poly)
    xl, xr = xs[0], xs[-1]
    # mũi tâm trước (trái) và sau (phải): côn 60°, đỉnh lọt vào lỗ tâm 8 px
    h = 8 * math.tan(math.radians(30))
    o.append(P([(xl + 8, cy), (xl - 22, cy - 22 * math.tan(math.radians(30)) - h), (xl - 22, cy + 22 * math.tan(math.radians(30)) + h)], TOOL))
    o.append(R(xl - 66, cy - 18, 44, 36, FIX))
    o.append(P([(xr - 8, cy), (xr + 22, cy - 22 * math.tan(math.radians(30)) - h), (xr + 22, cy + 22 * math.tan(math.radians(30)) + h)], TOOL))
    o.append(R(xr + 22, cy - 18, 44, 36, FIX))
    # tốc kẹp đầu trái
    o.append(R(xl + 10, cy - 26, 16, 52, f'fill="none" stroke="{ORANGE}" stroke-width="2.2"'))
    o.append(Ln(xl + 18, cy + 26, xl + 18, cy + 52, ORANGE, 2.2))
    o.append(T(xl + 26, cy + 52, "tốc: truyền mômen", 12, c=ORANGE))
    # ký hiệu định vị
    o.append(Loc(xl - 10, cy - 18 * math.tan(math.radians(30)) - 0.5, 0, -1, 3, xl - 10, cy - 34, "middle"))
    o.append(Loc(xr + 10, cy - 18 * math.tan(math.radians(30)) - 0.5, 0, -1, 2, xr + 10, cy - 34, "middle"))
    # chiều quay
    o.append(Rot((xs[1] + xs[2]) / 2, cy, 10, 30, -60, 60))
    o.append(T(12, 22, "mũi tâm trước", 12))
    o.append(T(408, 22, "mũi tâm sau", 12, "end"))
    o.append(T(12, 176, "Mũi tâm trước: 3 bậc tịnh tiến", 13, c=BLUE))
    o.append(T(12, 194, "Mũi tâm sau: 2 bậc quay", 13, c=BLUE))
    o.append(T(12, 214, "Còn quay quanh trục: chuyển động cắt", 13))
    o.append(T(12, 234, "Mọi bậc trục quay quanh cùng một đường tâm", 13, w="700"))
    return fig(svg(244, "Trục gá trên hai mũi tâm, tốc truyền mômen", o),
               "Hình 2. Gá trục trên hai lỗ tâm: tam giác xanh là ký hiệu định vị, số là bậc tự do được khống chế.")


# Hình 3: khoả mặt đầu và khoan tâm trên máy chuyên dùng
def fig_khoan_tam():
    o = []
    cy = 104
    o.append(Ln(12, cy, 408, cy, w=1, dash="8 3 2 3"))
    x0, xs_, x1 = 100, 170, 320          # mặt đầu trái (sau khoả), vai phôi dập, mặt đầu phải
    ds, dl = 24, 54                       # đường kính đoạn nhỏ, đoạn lớn
    o.append(R(x0 - 10, cy - ds / 2, 10, ds, ALLOW))
    o.append(R(x1, cy - dl / 2, 10, dl, ALLOW))
    poly, _ = stepped(x0, cy, [(xs_ - x0, ds), (x1 - xs_, dl)])
    o.append(poly)
    # khối V tự định tâm dưới đoạn lớn: 4 bậc
    for xv in (210, 290):
        o.append(R(xv - 22, cy + dl / 2, 44, 22, FIX))
        o.append(Loc(xv, cy + dl / 2, 0, 1, "", 0, 0))
    o.append(T(250, cy + dl / 2 + 18, "4", 14, "middle", "700", BLUE))
    # chốt tì dọc: tì vào vai phôi (mặt bậc), 1 bậc
    yv = cy + (ds / 2 + dl / 2) / 2
    o.append(Loc(xs_, yv, -1, 0, 1, xs_ - 24, yv + 22, "middle"))
    assert yv - 7 >= cy + ds / 2 and yv + 7 <= cy + dl / 2
    # lực kẹp
    o.append(Ar(250, cy - 64, 250, cy - dl / 2 - 8))
    o.append(T(258, cy - 48, "W", 13, w="700", c=RED))
    # dao phay mặt đầu hai phía + chiều tiến
    xL = x0 - 10 - 10 - 14
    o.append(R(xL, cy - 40, 14, 80, TOOL))
    o.append(Ar(xL - 36, cy - 50, xL - 8, cy - 50, RED, 2))
    xR = x1 + 10 + 10
    o.append(R(xR, cy - 40, 14, 80, TOOL))
    o.append(Ar(xR + 50, cy - 50, xR + 22, cy - 50, RED, 2))
    o.append(T(12, 22, "① Phay hai mặt đầu cùng lúc", 13, w="700"))
    o.append(T(12, 40, "② Ụ khoan hai phía khoan hai lỗ tâm", 13, w="700"))
    o.append(T(12, 192, "Cam: lượng dư mặt đầu bị phay đi", 13, c=ORANGE))
    o.append(T(12, 210, "Xám đậm: dao phay mặt đầu", 13))
    o.append(T(12, 228, "Khối V tự định tâm 4 bậc + chốt tì vai 1 bậc", 13, c=BLUE))
    o.append(T(12, 248, "Hai lỗ tâm làm trong một lần gá → cùng một trục", 13, w="700"))
    return fig(svg(258, "Phay mặt đầu và khoan tâm hai phía trên máy chuyên dùng", o),
               "Hình 3. Máy chuyên dùng (hàng loạt lớn): phôi dập nằm trên khối V tự định tâm, phay hai mặt đầu rồi khoan hai lỗ tâm.")


# Hình 4: phay rãnh then, trục trên khối V
def fig_phay_then():
    o = []
    # a) nhìn dọc trục: tròn trong khối V 90°
    cx, cy, r = 100, 120, 40
    o.append(T(12, 18, "a) Nhìn dọc trục", 13, w="700"))
    vy = cy + r * math.sqrt(2)                       # đỉnh V
    top = cy - 10
    lx, rx_ = cx - (vy - top), cx + (vy - top)
    o.append(P([(lx - 14, top), (lx, top), (cx, vy), (rx_, top), (rx_ + 14, top), (rx_ + 14, vy + 22), (lx - 14, vy + 22)], FIX))
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" {WORK}/>')
    # rãnh then ở đỉnh
    o.append(R(cx - 7, cy - r - 1, 14, 12, f'fill="{RED}" fill-opacity="0.8" stroke="none"'))
    # dao phay ngón
    o.append(R(cx - 7, cy - r - 46, 14, 34, TOOL))
    o.append(Rot(cx, cy - r - 30, 14, 5, 200, 340, RED, 1.8))
    # ký hiệu định vị tại hai điểm tiếp xúc 45°
    for s in (-1, 1):
        px, py = cx + s * r * math.sin(math.radians(45)), cy + r * math.cos(math.radians(45))
        o.append(Loc(px, py, s, 1, "", 0, 0))
    o.append(T(cx, vy + 44, "khối V dài: 4 bậc", 12, "middle", c=BLUE))
    # kiểm nhãn không đè đường tròn
    for (tx, ty) in ((cx, vy + 44),):
        assert math.hypot(tx - cx, ty - cy) > r + 8
    o.append(T(cx + 30, cy - r - 30, "dao phay ngón", 12))
    # b) nhìn cạnh: trục trên khối V dài + chốt tì đầu
    o.append(T(232, 18, "b) Nhìn cạnh", 13, w="700"))
    by = 120
    o.append(Ln(220, by, 412, by, w=1, dash="8 3 2 3"))
    o.append(R(250, by - 28, 150, 56))
    o.append(R(260, by + 28, 130, 22, FIX))
    o.append(Loc(300, by + 28, 0, 1, "", 0, 0))
    o.append(Loc(350, by + 28, 0, 1, "", 0, 0))
    o.append(T(325, by + 68, "4", 14, "middle", "700", BLUE))
    o.append(R(226, by - 10, 12, 20, FIX))
    o.append(Loc(250, by, -1, 0, 1, 234, by - 18, "middle"))
    o.append(f'<rect x="290" y="{by - 29}" width="60" height="9" rx="4.5" fill="{RED}" fill-opacity="0.8"/>')
    o.append(R(300, by - 70, 14, 40, TOOL))
    o.append(Ar(322, by - 52, 356, by - 52, RED, 1.8, 8))
    o.append(T(362, by - 48, "chạy dao", 12))
    o.append(T(232, 228, "Chốt tì mặt đầu: 1 bậc", 12, c=BLUE))
    o.append(T(232, 246, "Rãnh then kín: biết vị trí dọc", 12))
    o.append(T(12, 246, "Đỏ: rãnh then đang phay", 12, c=RED))
    return fig(svg(256, "Phay rãnh then: trục đặt trên khối V dài, đầu trục tì chốt chặn", o),
               "Hình 4. Phay rãnh then kín bằng dao phay ngón: khối V dài 4 bậc + chốt tì mặt đầu 1 bậc = 5 bậc.")


# Hình 5: kiểm độ đảo hướng tâm
def fig_kiem_dao():
    o = []
    cy = 140
    o.append(Ln(12, cy, 408, cy, w=1, dash="8 3 2 3"))
    poly, xs = stepped(90, cy, [(70, 36), (100, 50), (70, 36)])
    o.append(poly)
    xl, xr = xs[0], xs[-1]
    k = math.tan(math.radians(30))
    o.append(P([(xl + 8, cy), (xl - 22, cy - 30 * k), (xl - 22, cy + 30 * k)], TOOL))
    o.append(P([(xr - 8, cy), (xr + 22, cy - 30 * k), (xr + 22, cy + 30 * k)], TOOL))
    o.append(R(xl - 60, cy - 16, 38, 32, FIX))
    o.append(R(xr + 22, cy - 16, 38, 32, FIX))
    # đồng hồ so đo cổ Ø36 bên phải
    xm = (xs[2] + xs[3]) / 2
    surf = cy - 18
    gx, gy, gr = xm, 50, 26
    o.append(f'<circle cx="{gx:.1f}" cy="{gy}" r="{gr}" fill="none" stroke="currentColor" stroke-width="1.8"/>')
    o.append(Ln(gx, gy, gx + 15, gy - 12, RED, 2))
    o.append(R(gx - 3, gy + gr, 6, surf - (gy + gr), 'fill="currentColor"'))
    assert surf - (gy + gr) > 8
    o.append(T(gx - gr - 8, gy - 6, "đồng hồ so", 12, "end"))
    o.append(T(gx - gr - 8, gy + 10, "đầu đo hướng vào tâm", 12, "end"))
    # chiều quay tay
    o.append(Rot((xs[1] + xs[2]) / 2, cy, 12, 36, -60, 60))
    o.append(T((xs[1] + xs[2]) / 2 - 30, cy - 34, "quay 1 vòng", 12, "end"))
    o.append(T(12, 214, "Độ đảo = số chỉ lớn nhất − số chỉ nhỏ nhất", 13, w="700"))
    o.append(T(12, 234, "Đo trên hai mũi tâm: chuẩn kiểm = chuẩn gia công", 13))
    return fig(svg(244, "Kiểm tra độ đảo hướng tâm cổ trục bằng đồng hồ so trên hai mũi tâm", o),
               "Hình 5. Kiểm độ đảo hướng tâm: trục quay trên hai mũi tâm, đầu đo đồng hồ so tì vào cổ cần kiểm.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
figs = [fig_dang_truc, fig_hai_mui_tam, fig_khoan_tam, fig_phay_then, fig_kiem_dao]
order = [int(n) for n in re.findall(r"<!--FIG(\d)-->", src)]
assert order == list(range(1, len(figs) + 1)), order
for n, f in enumerate(figs, 1):
    s = f()
    assert f"Hình {n}." in s, n
    src = src.replace(f"<!--FIG{n}-->", s)

lint = HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = HERE / "theory.html"
out.write_text(src.replace("__PHUT__", "?"), encoding="utf8")
r = subprocess.run([sys.executable, str(lint), str(out), "--json"], capture_output=True, text=True)
m_ = re.search(r'"phut"\s*:\s*([\d.]+)', r.stdout)
phut = round(float(m_.group(1))) if m_ else "?"
out.write_text(src.replace("__PHUT__", str(phut)), encoding="utf8")
print("đã ghi theory.html; phút đọc =", phut)
