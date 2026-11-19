#!/usr/bin/env python3
"""Sinh 6 đề thi phay CNC (phôi 50x50, G01/G02/G03 + khoan 4 lỗ Ø4 sâu 4).

Bản vẽ ghi kích thước kiểu toạ độ từ gốc W (góc dưới trái) như bản vẽ mẫu:
mỗi toạ độ X kéo đường gióng xuống chân đường kích thước bên dưới, mỗi toạ
độ Y kéo sang chân đường kích thước bên phải.

Chạy:  python3 scripts/cnc/de-thi-phay-6-de.py [thư_mục_svg]
Ra:    docs/cnc-de-thi-phay-6-de.html (+ từng file SVG nếu có thư mục).
"""
import math, os, sys

# ---------------------------------------------------------------- dữ liệu đề
# Biên dạng luôn đi CÙNG chiều kim đồng hồ: cung lồi = G02, cung lõm = G03.
# Mỗi bước: ("L", x, y) hoặc ("A", x, y, R, "G02"/"G03").
DE = [
    dict(ten="Vuông bo góc – lõm cạnh trên",
         mo_ta="Biên dạng vuông bo 4 góc R5 (G02), cạnh trên có cung lõm R8 (G03).",
         start=(3, 8),
         path=[("L", 3, 42), ("A", 8, 47, 5, "G02"), ("L", 19, 47), ("A", 31, 47, 8, "G03"),
               ("L", 42, 47), ("A", 47, 42, 5, "G02"), ("L", 47, 8), ("A", 42, 3, 5, "G02"),
               ("L", 8, 3), ("A", 3, 8, 5, "G02")],
         holes=[(25, 12), (12, 25), (38, 25), (25, 33)]),
    dict(ten="Vát góc – lõm cạnh phải",
         mo_ta="Hai góc trên bo R7 (G02), hai góc dưới vát 7×45° (G01), cạnh phải có cung lõm R6 (G03).",
         start=(3, 10),
         path=[("L", 3, 40), ("A", 10, 47, 7, "G02"), ("L", 40, 47), ("A", 47, 40, 7, "G02"),
               ("L", 47, 30), ("A", 47, 20, 6, "G03"), ("L", 47, 10), ("L", 40, 3),
               ("L", 10, 3), ("L", 3, 10)],
         holes=[(14, 14), (34, 14), (14, 36), (34, 36)], lo_nhan=(0, 44, -40)),
    dict(ten="Đầu vòm – lõm cạnh dưới",
         mo_ta="Đỉnh vòm R25 (G02), hai góc dưới bo R5 (G02), cạnh dưới có cung lõm R7 (G03).",
         start=(3, 8),
         path=[("L", 3, 30), ("A", 47, 30, 25, "G02"), ("L", 47, 8), ("A", 42, 3, 5, "G02"),
               ("L", 31, 3), ("A", 19, 3, 7, "G03"), ("L", 8, 3), ("A", 3, 8, 5, "G02")],
         holes=[(12, 14), (38, 14), (14, 30), (36, 30)]),
    dict(ten="Khuyết góc tròn",
         mo_ta="Góc trên trái khuyết cung lõm R12 (G03), góc trên phải vát 7×45°, hai góc dưới bo R5 (G02).",
         start=(3, 8),
         path=[("L", 3, 35), ("A", 15, 47, 12, "G03"), ("L", 40, 47), ("L", 47, 40),
               ("L", 47, 8), ("A", 42, 3, 5, "G02"), ("L", 8, 3), ("A", 3, 8, 5, "G02")],
         holes=[(13, 13), (37, 13), (37, 37), (25, 25)]),
    dict(ten="Hai đầu vòm – lõm cạnh dưới",
         mo_ta="Hai đầu vòm R18 (G02), cạnh dưới có cung lõm R6 (G03).",
         start=(15, 40),
         path=[("L", 35, 40), ("A", 35, 10, 18, "G02", {"t": 0.75}), ("L", 30, 10),
               ("A", 20, 10, 6, "G03", {"L": -5}), ("L", 15, 10), ("A", 15, 40, 18, "G02", {"t": 0.25})],
         holes=[(13, 25), (37, 25), (25, 33), (25, 19)]),
    dict(ten="Bo lồi trái – bo lõm phải",
         mo_ta="Hai góc trái bo lồi R5 (G02), hai góc phải bo lõm R5 (G03).",
         start=(3, 13),
         path=[("L", 3, 37), ("A", 8, 42, 5, "G02"), ("L", 42, 42), ("A", 47, 37, 5, "G03", {"L": 4}),
               ("L", 47, 13), ("A", 42, 8, 5, "G03", {"L": 4}), ("L", 8, 8), ("A", 3, 13, 5, "G02")],
         holes=[(13, 18), (35, 18), (13, 32), (35, 32)], lo_nhan=(0, 44, -40)),
]

Z_VIEN, Z_LO = -4, -4          # rãnh biên dạng và lỗ khoan cùng sâu 4


def arc_center(p0, p1, r, g):
    """Tâm cung nhỏ (≤180°) đi từ p0 tới p1; G02 = cùng chiều kim đồng hồ."""
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    c = math.hypot(dx, dy)
    h = math.sqrt(max(r * r - (c / 2) ** 2, 0))
    ux, uy = dx / c, dy / c
    nx, ny = (uy, -ux) if g == "G02" else (-uy, ux)   # phải / trái hướng đi
    return (x0 + dx / 2 + h * nx, y0 + dy / 2 + h * ny)


def arc_points(p0, p1, r, g, n=60):
    cx, cy = arc_center(p0, p1, r, g)
    a0 = math.atan2(p0[1] - cy, p0[0] - cx)
    a1 = math.atan2(p1[1] - cy, p1[0] - cx)
    if g == "G02":
        while a1 > a0: a1 -= 2 * math.pi
    else:
        while a1 < a0: a1 += 2 * math.pi
    return [(cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n))
            for i in range(n + 1)], (cx, cy), (a0 + a1) / 2


def kiem(de, i):
    """Kiểm biên dạng kín, nằm trong phôi, rãnh không chạm lỗ."""
    pts, cur = [], de["start"]
    for s in de["path"]:
        if s[0] == "L":
            pts += [(cur[0] + (s[1] - cur[0]) * k / 40, cur[1] + (s[2] - cur[1]) * k / 40) for k in range(41)]
        else:
            ap, _, _ = arc_points(cur, (s[1], s[2]), s[3], s[4])
            pts += ap
        cur = (s[1], s[2])
    assert cur == de["start"], f"Đề {i}: biên dạng không kín"
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    assert min(xs) >= 3 - 1e-6 and max(xs) <= 47 + 1e-6 and min(ys) >= 3 - 1e-6 and max(ys) <= 47 + 1e-6, \
        f"Đề {i}: ra ngoài vùng 3..47"
    # chiều quay: diện tích có dấu < 0 nghĩa là cùng chiều kim đồng hồ
    area = sum(pts[k][0] * pts[k + 1][1] - pts[k + 1][0] * pts[k][1] for k in range(len(pts) - 1))
    assert area < 0, f"Đề {i}: không đi cùng chiều kim đồng hồ"
    for hx, hy in de["holes"]:
        d = min(math.hypot(px - hx, py - hy) for px, py in pts)
        assert d >= 5, f"Đề {i}: lỗ ({hx},{hy}) cách rãnh {d:.1f} < 5"
    return min(xs), max(ys)


# ---------------------------------------------------------------- vẽ
S = 6.4                       # px / mm
OX, OY = 70, 380              # pixel của gốc W
GAP = 22                      # khoảng cách các đường kích thước xếp chồng
FS = 15


def P(x, y):
    return OX + x * S, OY - y * S


def fmt(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def ve(de, so):
    o = []
    add = o.append
    W, H = 1000, 690
    add(f'<svg viewBox="0 0 {W} {H}" width="{W}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="Times New Roman,serif" role="img" aria-label="Bản vẽ thi phay CNC {so}">')
    add('<defs><marker id="ar" markerWidth="10" markerHeight="6" refX="9" refY="3" orient="auto-start-reverse">'
        '<path d="M0,0 L10,3 L0,6 Z" fill="#000"/></marker></defs>')
    add(f'<rect width="{W}" height="{H}" fill="#fff"/>')
    add('<rect x="20" y="20" width="960" height="650" fill="none" stroke="#000" stroke-width="2.5"/>')
    # phôi
    x0, y0 = P(0, 50)
    add(f'<rect x="{x0}" y="{y0}" width="{50*S}" height="{50*S}" fill="none" stroke="#000" stroke-width="1.6"/>')
    # biên dạng
    sx, sy = P(*de["start"])
    d = f"M {sx:.1f} {sy:.1f}"
    cur = de["start"]
    arcs = []
    for s in de["path"]:
        ex, ey = P(s[1], s[2])
        if s[0] == "L":
            d += f" L {ex:.1f} {ey:.1f}"
        else:
            sweep = 1 if s[4] == "G02" else 0
            d += f" A {s[3]*S:.1f} {s[3]*S:.1f} 0 0 {sweep} {ex:.1f} {ey:.1f}"
            arcs.append((cur, (s[1], s[2]), s[3], s[4], s[5] if len(s) > 5 else {}))
        cur = (s[1], s[2])
    add(f'<path d="{d}" fill="none" stroke="#000" stroke-width="2.2"/>')
    # lỗ
    for hx, hy in de["holes"]:
        cx, cy = P(hx, hy)
        add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{2*S:.1f}" fill="none" stroke="#000" stroke-width="1.6"/>')
        L = 3.4 * S
        add(f'<path d="M {cx-L:.1f} {cy:.1f} H {cx+L:.1f} M {cx:.1f} {cy-L:.1f} V {cy+L:.1f}" '
            f'stroke="#000" stroke-width="0.7" stroke-dasharray="9 2 2 2"/>')
    # nhãn R (đặt phía trong chi tiết, mũi tên chỉ vào cung)
    for p0, p1, r, g, opt in arcs:
        _, (cx, cy), _am = arc_points(p0, p1, r, g)
        a0 = math.atan2(p0[1] - cy, p0[0] - cx)
        am = a0 + (_am - a0) * 2 * opt.get("t", 0.5)
        mx, my = cx + r * math.cos(am), cy + r * math.sin(am)
        ux, uy = math.cos(am), math.sin(am)
        k = -1 if g == "G02" else 1            # hướng vào trong chi tiết
        L = opt.get("L", 7.5 if r < 15 else 9)
        tx, ty = mx + k * ux * L, my + k * uy * L
        a, b = P(tx, ty)
        c_, e = P(mx, my)
        add(f'<line x1="{a:.1f}" y1="{b:.1f}" x2="{c_:.1f}" y2="{e:.1f}" stroke="#000" stroke-width="0.9" marker-end="url(#ar)"/>')
        add(f'<rect x="{a-13:.1f}" y="{b-9:.1f}" width="26" height="17" fill="#fff"/>')
        add(f'<text x="{a:.1f}" y="{b+5:.1f}" font-size="{FS}" text-anchor="middle">R{r}</text>')
    # ghi chú lỗ
    if "lo_nhan" in de:
        idx, dxp, dyp = de["lo_nhan"]
        hx, hy = de["holes"][idx]
    else:
        hx, hy = max(de["holes"], key=lambda h: (h[0] + h[1]))
        dxp, dyp = 44, -40
    a, b = P(hx, hy)
    rr = 2 * S * 0.7071
    qa, qb = a + (rr if dxp > 0 else -rr), b + (rr if dyp > 0 else -rr)
    add(f'<line x1="{qa+dxp:.1f}" y1="{qb+dyp:.1f}" x2="{qa:.1f}" y2="{qb:.1f}" stroke="#000" stroke-width="0.9" marker-end="url(#ar)"/>')
    add(f'<rect x="{qa+dxp-4:.1f}" y="{qb+dyp-18:.1f}" width="72" height="18" fill="#fff"/>')
    add(f'<text x="{qa+dxp-2:.1f}" y="{qb+dyp-4:.1f}" font-size="{FS}">4 lỗ Ø4</text>')
    # W
    wx, wy = P(0, 0)
    add(f'<circle cx="{wx}" cy="{wy}" r="9" fill="#fff" stroke="#000" stroke-width="1.4"/>'
        f'<path d="M {wx} {wy-9} A 9 9 0 0 0 {wx-9} {wy} L {wx} {wy} Z M {wx} {wy+9} A 9 9 0 0 0 {wx+9} {wy} L {wx} {wy} Z" fill="#000"/>'
        f'<text x="{wx-30}" y="{wy-4}" font-size="17">W</text>')

    # ---- kích thước toạ độ: X ở dưới, Y bên phải
    pts_xy = [de["start"]] + [(s[1], s[2]) for s in de["path"]]
    xs = sorted({p[0] for p in pts_xy} | {h[0] for h in de["holes"]} | {50})
    ys = sorted({p[1] for p in pts_xy} | {h[1] for h in de["holes"]} | {50})

    def chan_x(v):   # điểm thấp nhất có toạ độ x = v (để kéo gióng xuống)
        c = [p[1] for p in pts_xy if p[0] == v] + [h[1] for h in de["holes"] if h[0] == v]
        return min(c) if c else 0

    def chan_y(v):   # điểm xa phải nhất có toạ độ y = v
        c = [p[0] for p in pts_xy if p[1] == v] + [h[0] for h in de["holes"] if h[1] == v]
        return max(c) if c else 50

    base_y = OY + 26
    for i, v in enumerate(xs):
        yl = base_y + i * GAP
        px, _ = P(v, 0)
        _, py0 = P(v, chan_x(v) if v != 50 else 0)
        add(f'<line x1="{px:.1f}" y1="{py0+3:.1f}" x2="{px:.1f}" y2="{yl+5}" stroke="#000" stroke-width="0.6"/>')
        add(f'<line x1="{OX}" y1="{yl}" x2="{px:.1f}" y2="{yl}" stroke="#000" stroke-width="0.8" marker-start="url(#ar)" marker-end="url(#ar)"/>')
        if v * S >= 30:
            add(f'<text x="{OX + v*S/2:.1f}" y="{yl-3}" font-size="{FS}" text-anchor="middle">{fmt(v)}</text>')
        else:
            add(f'<text x="{px+5:.1f}" y="{yl-3}" font-size="{FS}">{fmt(v)}</text>')
    add(f'<line x1="{OX}" y1="{OY}" x2="{OX}" y2="{base_y + (len(xs)-1)*GAP + 5}" stroke="#000" stroke-width="0.6"/>')

    base_x = OX + 50 * S + 26
    for i, v in enumerate(ys):
        xl = base_x + i * GAP
        _, py = P(0, v)
        px0, _ = P(chan_y(v) if v != 50 else 50, 0)
        add(f'<line x1="{px0+3:.1f}" y1="{py:.1f}" x2="{xl+5}" y2="{py:.1f}" stroke="#000" stroke-width="0.6"/>')
        add(f'<line x1="{xl}" y1="{OY}" x2="{xl}" y2="{py:.1f}" stroke="#000" stroke-width="0.8" marker-start="url(#ar)" marker-end="url(#ar)"/>')
        if v * S >= 30:
            add(f'<text transform="translate({xl-4},{OY - v*S/2:.1f}) rotate(-90)" font-size="{FS}" text-anchor="middle">{fmt(v)}</text>')
        else:
            add(f'<text transform="translate({xl-4},{py-5:.1f}) rotate(-90)" font-size="{FS}">{fmt(v)}</text>')
    add(f'<line x1="{OX+50*S}" y1="{OY}" x2="{base_x + (len(ys)-1)*GAP + 5}" y2="{OY}" stroke="#000" stroke-width="0.6"/>')

    # ---- YCKT + khung tên
    tx = 720
    add(f'<text x="{tx}" y="70" font-size="17" text-decoration="underline">YCKT:</text>')
    for k, t in enumerate([
        "- Phôi 50 × 50 × 10, gốc W góc dưới trái,",
        "  mặt trên Z0.",
        f"- Rãnh biên dạng: dao phay ngón Ø4,",
        f"  tâm dao đi trên đường vẽ, sâu {-Z_VIEN} mm.",
        f"- Khoan 4 lỗ Ø4 sâu {-Z_LO} mm.",
        "- Bắt buộc dùng G01, G02, G03.",
        "- Kích thước không chỉ dẫn ± 0,1.",
    ]):
        add(f'<text x="{tx}" y="{96 + k*22}" font-size="15" xml:space="preserve">{t}</text>')
    add('<g stroke="#000" stroke-width="1.5" fill="none"><rect x="580" y="590" width="400" height="80"/>'
        '<line x1="580" y1="630" x2="740" y2="630"/><line x1="740" y1="590" x2="740" y2="670"/>'
        '<line x1="740" y1="630" x2="980" y2="630"/><line x1="900" y1="630" x2="900" y2="670"/>'
        '<line x1="900" y1="650" x2="980" y2="650"/></g>')
    add('<text x="590" y="615" font-size="14">Người vẽ</text><text x="590" y="655" font-size="14">Kiểm tra</text>')
    add(f'<text x="860" y="617" font-size="18" text-anchor="middle">BÀI THI PHAY CNC – ĐỀ {so}</text>')
    add('<text x="820" y="655" font-size="14" text-anchor="middle">NHỰA POM</text>'
        '<text x="905" y="645" font-size="14">TL: 1:1</text><text x="905" y="665" font-size="14">Số: ' + str(so) + '</text>')
    add('</svg>')
    return "".join(o)


def chuong_trinh(de, so):
    n = [0]
    out = []

    def b(t):
        n[0] += 10
        out.append(f"N{n[0]} {t} ;")
    out.append(f"O{1100+so:04d} ;")
    b("G17 G71 G90 G94 G54")
    b("T01 M06")
    b("G43 H01")
    b("S1500 M03")
    sx, sy = de["start"]
    b(f"G00 X{sx} Y{sy} Z5")
    b(f"G01 Z{Z_VIEN} F60")
    first = True
    for s in de["path"]:
        f = " F150" if first else ""
        first = False
        if s[0] == "L":
            b(f"G01 X{s[1]} Y{s[2]}{f}")
        else:
            b(f"{s[4]} X{s[1]} Y{s[2]} R{s[3]}{f}")
    b("G00 Z50")
    b("T02 M06")
    b("G43 H02")
    b("S2000 M03")
    h0 = de["holes"][0]
    b(f"G00 X{h0[0]} Y{h0[1]} Z5")
    b(f"G99 G81 X{h0[0]} Y{h0[1]} Z{Z_LO} R2 F80")
    for hx, hy in de["holes"][1:]:
        b(f"X{hx} Y{hy}")
    b("G80")
    b("G00 Z50")
    b("M05")
    b("M30")
    return "\n".join(out)


def bang(de):
    rows = [("1", *de["start"], "G01 (xuống Z%d)" % Z_VIEN)]
    for k, s in enumerate(de["path"], 2):
        lenh = "G01" if s[0] == "L" else f"{s[4]} R{s[3]}"
        rows.append((str(k) if k <= len(de["path"]) else "1", s[1], s[2], lenh))
    h = '<table><tr><th>Điểm</th><th>X</th><th>Y</th><th>Lệnh tới điểm</th></tr>'
    h += "".join(f"<tr><td>{a}</td><td>{x}</td><td>{y}</td><td>{l}</td></tr>" for a, x, y, l in rows)
    h += "".join(f"<tr><td>Lỗ {i}</td><td>{x}</td><td>{y}</td><td>G81 Z{Z_LO}</td></tr>"
                 for i, (x, y) in enumerate(de["holes"], 1))
    return h + "</table>"


def main():
    svgdir = sys.argv[1] if len(sys.argv) > 1 else None
    for i, de in enumerate(DE, 1):
        kiem(de, i)
    html = ['<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Đề thi phay CNC – 6 đề</title><style>svg{max-width:100%;height:auto}body{font:15px/1.5 system-ui;max-width:1000px;'
            'margin:auto;padding:16px;color:#111;background:#fff}h2{border-bottom:2px solid #124;margin-top:28px}pre{background:#f4f4f4;'
            'padding:10px;overflow:auto;font-size:13px}table{border-collapse:collapse;width:100%}td,th{border:1px solid #999;'
            'padding:4px 8px;text-align:left}.de{break-before:page}@page{size:A4 landscape;margin:8mm}</style>'
            '<h1>Đề thi phay CNC – 6 đề (Win-NC32 / Fanuc 21M)</h1><h2>Điều kiện chung</h2><ul>'
            '<li>Phôi 50 × 50 × 10 (nhựa POM), gốc W ở góc dưới trái mặt trên (G54), mặt trên Z0. Kích thước ghi theo toạ độ tính từ W.</li>'
            f'<li>Rãnh biên dạng: dao phay ngón Ø4 (T01), tâm dao chạy trên đường vẽ, không bù bán kính, sâu {-Z_VIEN} mm. '
            f'Khoan 4 lỗ Ø4 sâu {-Z_LO} mm bằng mũi khoan Ø4 (T02), chu trình G81 (G83 cũng chấp nhận).</li>'
            '<li>Bắt buộc dùng <b>G01</b>, <b>G02</b>, <b>G03</b>: mọi đề đều có cung lồi và cung lõm. Ghi cung bằng R (hoặc I, J).</li>'
            '<li>Biên dạng trong đáp án đi cùng chiều kim đồng hồ từ điểm 1; SV đi ngược chiều vẫn đúng nếu đổi G02 ↔ G03 hợp lý.</li>'
            '<li>Dung sai kích thước không chỉ dẫn ±0,1; mỗi ca thi 45 phút.</li></ul>'
            '<h2>Thang điểm (10)</h2><table><tr><th>Tiêu chí</th><th>Điểm</th></tr>'
            '<tr><td>Đọc bản vẽ, tính toạ độ đúng (có bảng điểm)</td><td>2</td></tr>'
            '<tr><td>Cấu trúc chương trình đúng (G17/G71/G90/G94/G54, thay dao, M03, M05, M30)</td><td>1</td></tr>'
            '<tr><td>G02/G03 đúng chiều và R ở mọi cung</td><td>2</td></tr>'
            '<tr><td>Chu trình khoan đúng (Z-4, R, G80 huỷ chu trình)</td><td>1</td></tr>'
            '<tr><td>Mô phỏng không báo lỗi/không va chạm</td><td>1</td></tr>'
            '<tr><td>Gia công đạt kích thước (±0,1) và bề mặt</td><td>3</td></tr></table>']
    for i, de in enumerate(DE, 1):
        svg = ve(de, i)
        if svgdir:
            os.makedirs(svgdir, exist_ok=True)
            open(os.path.join(svgdir, f"de-{i}.svg"), "w").write(svg)
        html.append(f'<div class="de"><h2>Đề {i}: {de["ten"]}</h2><p>{de["mo_ta"]}</p>{svg}'
                    f'<h3>Bảng toạ độ (giám khảo)</h3>{bang(de)}<h3>Đáp án chương trình</h3><pre>{chuong_trinh(de, i)}</pre></div>')
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out = os.path.join(root, "docs", "cnc-de-thi-phay-6-de.html")
    open(out, "w").write("".join(html))
    print("Đã ghi", out)


if __name__ == "__main__":
    main()
