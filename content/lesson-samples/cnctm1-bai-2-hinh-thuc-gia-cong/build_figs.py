#!/usr/bin/env python3
"""Sinh hình SVG cho CNCTM 1 – Bài 2, thay <!--FIGn--> trong theory.src.html → theory.html.
Dùng: python3 build_figs.py  (chạy lại an toàn: luôn đọc từ theory.src.html)
"""
import math
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
FONT = 'font-family="system-ui, sans-serif" font-size="13"'


def fig(svg, cap):
    return f'<figure class="fig" data-tl="1">{svg}<figcaption>{cap}</figcaption></figure>'


# Hình 4: sơ đồ nhiệt luyện nhiệt độ – thời gian, ba cách làm nguội
def fig4():
    o = []
    o.append(f'<svg viewBox="0 0 420 250" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Sơ đồ nhiệt luyện" {FONT}>')
    # trục
    o.append('<line x1="40" y1="210" x2="405" y2="210" stroke="currentColor" stroke-width="1.5"/>')
    o.append('<line x1="40" y1="210" x2="40" y2="70" stroke="currentColor" stroke-width="1.5"/>')
    o.append('<path d="M34 80 L40 70 L46 80" fill="none" stroke="currentColor" stroke-width="1.5"/>')
    o.append('<path d="M395 204 L405 210 L395 216" fill="none" stroke="currentColor" stroke-width="1.5"/>')
    o.append('<text x="48" y="80" fill="currentColor" font-size="12">nhiệt độ</text>')
    o.append('<text x="330" y="232" fill="currentColor" font-size="12">thời gian</text>')
    # nung + giữ
    o.append('<path d="M40 205 L130 100 L210 100" fill="none" stroke="currentColor" stroke-width="2.5"/>')
    o.append('<text x="70" y="140" fill="currentColor" font-weight="700">I</text>')
    o.append('<text x="164" y="92" fill="currentColor" font-weight="700">II</text>')
    o.append('<text x="98" y="172" fill="currentColor" font-size="12">nung</text>')
    o.append('<text x="150" y="122" fill="currentColor" font-size="12">giữ nhiệt</text>')
    # ba đường nguội (giai đoạn III)
    o.append('<path d="M210 100 C215 160 222 200 238 207" fill="none" stroke="#dc2626" stroke-width="2.5"/>')
    o.append('<path d="M210 100 C240 150 270 195 320 205" fill="none" stroke="#059669" stroke-width="2.5"/>')
    o.append('<path d="M210 100 C280 120 350 165 400 192" fill="none" stroke="#0284c7" stroke-width="2.5"/>')
    o.append('<text x="222" y="150" fill="currentColor" font-weight="700">III</text>')
    # chú giải, mỗi ý một dòng
    rows = [("#dc2626", "nguội nhanh (nước, dầu) → TÔI"),
            ("#059669", "nguội trong không khí → THƯỜNG HOÁ"),
            ("#0284c7", "nguội chậm cùng lò → Ủ")]
    for i, (c, s) in enumerate(rows):
        y = 18 + i * 20
        o.append(f'<line x1="150" y1="{y - 4}" x2="172" y2="{y - 4}" stroke="{c}" stroke-width="3"/>')
        o.append(f'<text x="178" y="{y}" fill="currentColor" font-size="12">{s}</text>')
    o.append('</svg>')
    return fig("".join(o), "Hình 4. Ba giai đoạn nhiệt luyện. Cùng nung và giữ nhiệt, cách làm nguội quyết định thép mềm hay cứng.")


# Hình 3: thớ kim loại khi cắt ren (tiện) và khi cán ren
def teeth(x0, dy=0, amp=30):
    return " ".join(f"{x0 + i * 20},{(80 if i % 2 == 0 else 80 - amp) + dy}" for i in range(9))


def fig3():
    o = []
    o.append(f'<svg viewBox="0 0 420 210" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Thớ kim loại khi tiện ren và khi cán ren" {FONT}>')
    o.append('<defs>')
    for side, x0 in (("l", 15), ("r", 225)):
        o.append(f'<clipPath id="f2-c{side}"><polygon points="{x0},140 {teeth(x0)} {x0 + 160},140"/></clipPath>')
    o.append('</defs>')
    # trái: thớ thẳng bị cắt đứt
    o.append('<g clip-path="url(#f2-cl)" stroke="#0284c7" stroke-width="1.3">')
    for y in range(56, 140, 8):
        o.append(f'<line x1="15" y1="{y}" x2="175" y2="{y}"/>')
    o.append('</g>')
    # phải: thớ uốn theo biên dạng răng, càng sâu càng phẳng
    o.append('<g clip-path="url(#f2-cr)" fill="none" stroke="#059669" stroke-width="1.3">')
    for k, dy in enumerate(range(4, 64, 8)):
        amp = max(30 - k * 4, 0)
        o.append(f'<polyline points="{teeth(225, dy, amp)}"/>')
    o.append('</g>')
    for side, x0 in (("l", 15), ("r", 225)):
        o.append(f'<polygon points="{x0},140 {teeth(x0)} {x0 + 160},140" fill="none" stroke="currentColor" stroke-width="2"/>')
    o.append('<text x="15" y="30" fill="currentColor" font-weight="700">Tiện ren (có phoi)</text>')
    o.append('<text x="225" y="30" fill="currentColor" font-weight="700">Cán ren (không phoi)</text>')
    o.append('<text x="15" y="162" fill="currentColor" font-size="12">Thớ thẳng bị cắt đứt</text>')
    o.append('<text x="15" y="180" fill="currentColor" font-size="12">ở sườn răng.</text>')
    o.append('<text x="225" y="162" fill="currentColor" font-size="12">Thớ uốn theo răng,</text>')
    o.append('<text x="225" y="180" fill="currentColor" font-size="12">không bị cắt, bề mặt biến cứng.</text>')
    o.append('</svg>')
    return fig("".join(o), "Hình 3. Cùng một biên dạng ren, cách làm khác nhau cho thớ kim loại khác nhau (hình minh hoạ, không theo tỉ lệ).")


RED, GREEN, BLUE, ORANGE = "#dc2626", "#059669", "#0284c7", "#ea580c"


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
        pts.append((x + L * (bx * math.cos(a) - by * math.sin(a)), y + L * (bx * math.sin(a) + by * math.cos(a))))
    (x1, y1), (x2, y2) = pts
    return (f'<path d="M{x1:.1f} {y1:.1f} L{x:.1f} {y:.1f} L{x2:.1f} {y2:.1f}" fill="none" '
            f'stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def arrow(x1, y1, x2, y2, color="currentColor", w=1.8):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{w}"/>'
            + chev(x2, y2, x2 - x1, y2 - y1, color, w=w))


def zigzag(x0, x1, y_base, y_peak, step):
    """Điểm răng cưa từ x0 sang x1 (hoặc ngược lại nếu x1 < x0)."""
    pts, k = [], 0
    sgn = 1 if x1 > x0 else -1
    x = x0
    while (x1 - x) * sgn > 0:
        pts.append((x, y_base if k % 2 == 0 else y_peak))
        x += sgn * step / 2
        k += 1
    pts.append((x1, y_base))
    return pts


def P(pts):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


# Hình 1: tiện thô và tiện tinh — mặt cắt dọc, nhám vẽ phóng to
def tien_panel(ox, title, t, h, f, chip_w, l1, l2):
    o = []
    ys, tx = 110, ox + 120
    pts = [(ox + 10, 150), (ox + 10, ys - t), (tx, ys - t), (tx, ys)]
    pts += zigzag(tx, ox + 200, ys, ys - h, f)[1:]
    pts += [(ox + 200, 150)]
    o.append(f'<polygon points="{P(pts)}" fill="currentColor" fill-opacity="0.12" stroke="currentColor" '
             f'stroke-width="1.8" stroke-linejoin="round"/>')
    xd = tx + 28 * min(t / 22, 1)  # mặt sau của dao ở độ cao mặt phôi cũ
    o.append(f'<line x1="{xd:.1f}" y1="{ys - t}" x2="{ox + 200}" y2="{ys - t}" stroke="currentColor" stroke-width="1" '
             f'stroke-dasharray="4 3"/>')
    # phoi
    o.append(f'<path d="M{tx - 2} {ys - t + chip_w / 2} Q{tx - 6} {ys - t - 40} {tx - 40} {ys - t - 44}" fill="none" '
             f'stroke="{ORANGE}" stroke-width="{chip_w}" stroke-linecap="round"/>')
    o.append(text(ox + 30, ys - t - 40, "phoi", size=12, color=ORANGE))
    # dao
    o.append(f'<polygon points="{tx},{ys} {tx + 28},{ys - 22} {tx + 28},{ys - 55} {tx + 8},{ys - 55} {tx + 2},{ys - 12}" '
             f'fill="{BLUE}" fill-opacity="0.3" stroke="{BLUE}" stroke-width="1.8"/>')
    o.append(text(tx + 34, ys - 44, "dao", size=12, color=BLUE))
    o.append(text(ox + 10, 20, title, bold=True))
    o.append(text(ox + 10, 172, l1, size=12))
    o.append(text(ox + 10, 190, l2, size=12, color=RED))
    return o


def fig1():
    o = [svg_open(420, 200, "Tiện thô và tiện tinh")]
    o += tien_panel(0, "Tiện thô", 30, 8, 22, 9, "cắt sâu, phoi dày", "nhấp nhô cao")
    o.append('<line x1="210" y1="8" x2="210" y2="194" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4 4" opacity="0.6"/>')
    o += tien_panel(212, "Tiện tinh", 6, 2.5, 8, 2, "lớp mỏng, phoi mỏng", "nhấp nhô thấp")
    o.append("</svg>")
    return fig("".join(o), "Hình 1. Lớp cắt và nhấp nhô (phóng to).")


# Hình 2: cán lăn mặt trụ và nong lỗ
def fig2():
    o = [svg_open(420, 350, "Cán lăn mặt trụ và nong lỗ")]
    # --- cán lăn
    a, xr = 118, 200
    top = zigzag(30, xr - 12, a - 30, a - 34, 8) + [(330, a - 30)]
    bot = [(330, a + 30)] + zigzag(xr - 12, 30, a + 30, a + 34, 8)
    o.append(f'<polygon points="{P(top + bot)}" fill="currentColor" fill-opacity="0.12" stroke="currentColor" '
             f'stroke-width="1.8" stroke-linejoin="round"/>')
    o.append(f'<line x1="18" y1="{a}" x2="342" y2="{a}" stroke="currentColor" stroke-width="0.8" stroke-dasharray="10 3 2 3"/>')
    o.append(f'<circle cx="{xr}" cy="{a - 54}" r="24" fill="{BLUE}" fill-opacity="0.25" stroke="{BLUE}" stroke-width="2"/>')
    o.append(f'<circle cx="{xr}" cy="{a - 54}" r="3" fill="{BLUE}"/>')
    o.append(text(xr + 30, a - 50, "con lăn", size=12, color=BLUE))
    o.append(arrow(xr, 8, xr, a - 82, RED))
    o.append(text(xr + 10, 24, "lực ép", size=12, color=RED))
    o.append(arrow(xr - 32, a - 54, xr - 72, a - 54, RED))
    o.append(text(xr - 90, a - 64, "chạy dao", size=12, color=RED))
    o.append(text(14, 18, "Cán lăn mặt trụ", bold=True))
    o.append(text(36, a - 46, "chưa cán", size=12))
    o.append(f'<path d="M60 {a + 40} A25 9 0 0 0 110 {a + 40}" fill="none" stroke="{RED}" stroke-width="1.8"/>')
    o.append(chev(110, a + 40, 0, -1, RED))
    o.append(text(118, a + 54, "phôi quay", size=12, color=RED))
    o.append(text(xr + 14, a + 52, "đã cán: nhẵn, biến cứng", size=12, color=GREEN))
    o.append('<line x1="10" y1="182" x2="410" y2="182" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4 4" opacity="0.6"/>')
    # --- nong lỗ (mặt cắt dọc qua tâm lỗ)
    b, xb = 277, 230
    o.append(text(14, 203, "Nong lỗ", bold=True))
    for s in (-1, 1):
        rough = zigzag(310, xb + 12, b + s * 22, b + s * 19, 8)
        pts = [(150, b + s * 48), (310, b + s * 48)] + rough + [(xb, b + s * 24), (150, b + s * 24)]
        o.append(f'<polygon points="{P(pts)}" fill="currentColor" fill-opacity="0.15" stroke="currentColor" '
                 f'stroke-width="1.8" stroke-linejoin="round"/>')
    o.append(f'<line x1="60" y1="{b}" x2="320" y2="{b}" stroke="currentColor" stroke-width="0.8" stroke-dasharray="10 3 2 3"/>')
    o.append(f'<rect x="70" y="{b - 8}" width="{xb - 24 - 70}" height="16" fill="currentColor" fill-opacity="0.25" '
             f'stroke="currentColor" stroke-width="1.5"/>')
    o.append(f'<circle cx="{xb}" cy="{b}" r="24" fill="{BLUE}" fill-opacity="0.3" stroke="{BLUE}" stroke-width="2"/>')
    o.append(text(178, b - 58, "viên bi tôi cứng", size=12, color=BLUE))
    o.append(arrow(26, b, 64, b, RED))
    o.append(text(20, b - 16, "lực đẩy", size=12, color=RED))
    o.append(text(76, b + 26, "thanh đẩy", size=12))
    o.append(text(150, b + 66, "đã nong: nhẵn", size=12, color=GREEN))
    o.append(text(258, b + 66, "chưa nong", size=12))
    o.append("</svg>")
    return fig("".join(o), "Hình 2. Con lăn, viên bi ép cho lớp mặt chảy dẻo, không tạo phoi (nhám vẽ phóng to).")


# Hình 5: mặt cắt trục thép ít cacbon sau thấm cacbon + tôi + ram
def fig5():
    o = [svg_open(420, 262, "Lớp mặt thấm cacbon và lõi dẻo")]
    cx, cy, R, r = 95, 110, 78, 66
    o.append(text(15, 18, "Mặt cắt ngang trục", size=12))
    o.append(f'<path d="M{cx - R} {cy} A{R} {R} 0 1 0 {cx + R} {cy} A{R} {R} 0 1 0 {cx - R} {cy} Z '
             f'M{cx - r} {cy} A{r} {r} 0 1 0 {cx + r} {cy} A{r} {r} 0 1 0 {cx - r} {cy} Z" fill="{RED}" '
             f'fill-opacity="0.75" fill-rule="evenodd" stroke="currentColor" stroke-width="1.8"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BLUE}" fill-opacity="0.12" stroke="{RED}" stroke-width="1"/>')
    o.append(f'<rect x="15" y="201" width="20" height="13" fill="{RED}" fill-opacity="0.75" stroke="currentColor"/>')
    o.append(text(42, 212, "lớp mặt: giàu C, tôi cứng", size=12))
    o.append(f'<rect x="15" y="221" width="20" height="13" fill="{BLUE}" fill-opacity="0.12" stroke="currentColor"/>')
    o.append(text(42, 232, "lõi: ít C, vẫn dẻo dai", size=12))
    o.append(text(15, 254, "(lớp thấm mỏng, vẽ phóng dày)", size=12))
    # đồ thị độ cứng theo chiều sâu
    gx, gy0, gy1, gx1 = 232, 30, 180, 405
    o.append(f'<rect x="{gx}" y="{gy0}" width="44" height="{gy1 - gy0}" fill="{RED}" fill-opacity="0.1"/>')
    o.append(f'<line x1="{gx}" y1="{gy1}" x2="{gx}" y2="{gy0 - 6}" stroke="currentColor" stroke-width="1.5"/>')
    o.append(chev(gx, gy0 - 6, 0, -1))
    o.append(f'<line x1="{gx}" y1="{gy1}" x2="{gx1}" y2="{gy1}" stroke="currentColor" stroke-width="1.5"/>')
    o.append(chev(gx1, gy1, 1, 0))
    o.append(text(gx + 8, 26, "độ cứng", size=12))
    o.append(f'<path d="M{gx} 62 H272 C292 62 296 150 322 150 H398" fill="none" stroke="{RED}" stroke-width="2.5"/>')
    o.append(text(gx + 8, 54, "56–60 HRC", size=12, color=RED, bold=True))
    o.append(text(gx + 4, 172, "lớp thấm", size=12))
    o.append(text(338, 142, "lõi dẻo", size=12))
    o.append(text(gx, 198, "khoảng cách từ mặt vào tâm", size=12))
    o.append("</svg>")
    return fig("".join(o), "Hình 5. Trục thép ít cacbon sau khi thấm cacbon, tôi và ram.")


# Hình 6: sơ đồ gia công tia lửa điện (EDM)
def fig6():
    o = [svg_open(420, 250, "Sơ đồ gia công tia lửa điện")]
    o.append('<rect x="20" y="20" width="100" height="42" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/>')
    o.append(text(70, 37, "nguồn xung", size=12, anchor="middle"))
    o.append(f'<polyline points="34,57 34,46 46,46 46,57 58,57 58,46 70,46 70,57 82,57 82,46 94,46 94,57 106,57" '
             f'fill="none" stroke="{ORANGE}" stroke-width="1.5"/>')
    o.append('<polyline points="120,34 170,34 170,60" fill="none" stroke="currentColor" stroke-width="1.5"/>')
    o.append('<polyline points="30,62 30,195 90,195" fill="none" stroke="currentColor" stroke-width="1.5"/>')
    # bể + điện môi
    o.append(f'<rect x="41" y="120" width="258" height="109" fill="{BLUE}" fill-opacity="0.1"/>')
    o.append(f'<line x1="41" y1="120" x2="299" y2="120" stroke="{BLUE}" stroke-width="1.2"/>')
    o.append('<path d="M40 108 V230 H300 V108" fill="none" stroke="currentColor" stroke-width="2"/>')
    # phôi có hốc
    o.append('<polygon points="90,170 140,170 140,185 200,185 200,170 250,170 250,215 90,215" fill="currentColor" '
             'fill-opacity="0.18" stroke="currentColor" stroke-width="2"/>')
    o.append(text(100, 205, "phôi", bold=True))
    # điện cực
    o.append(f'<rect x="145" y="60" width="50" height="115" fill="{BLUE}" fill-opacity="0.3" stroke="{BLUE}" stroke-width="2"/>')
    o.append(text(205, 78, "điện cực", size=12, color=BLUE))
    o.append(text(205, 94, "(dụng cụ)", size=12, color=BLUE))
    o.append(arrow(132, 72, 132, 104, RED))
    o.append(text(58, 92, "tiến xuống", size=12, color=RED))
    # tia lửa trong khe hở
    for x in (156, 170, 184):
        o.append(f'<path d="M{x} 176 L{x - 3} 179 L{x + 2} 181 L{x - 1} 184" fill="none" stroke="{ORANGE}" '
                 f'stroke-width="2" stroke-linejoin="round"/>')
    o.append(text(206, 140, "dung dịch", size=12, color=BLUE))
    o.append(text(206, 156, "điện môi", size=12, color=BLUE))
    o.append(f'<line x1="188" y1="180" x2="304" y2="154" stroke="{ORANGE}" stroke-width="1"/>')
    o.append(text(308, 152, "tia lửa", size=12, color=ORANGE, bold=True))
    o.append(text(308, 168, "trong khe hở", size=12, color=ORANGE))
    o.append("</svg>")
    return fig("".join(o), "Hình 6. Tia lửa điện trong khe hở làm chảy, bốc hơi từng hạt kim loại của phôi.")

src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in ((f"<!--FIG{n}-->", f) for n, f in enumerate((fig1, fig2, fig3, fig4, fig5, fig6), 1)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
