#!/usr/bin/env python3
"""Sinh hình SVG cho CNCTM 1 – Bài 4 (Chuẩn), thay <!--FIGn--> trong theory.src.html → theory.html.
Dùng: python3 build_figs.py  (chạy lại an toàn: luôn đọc từ theory.src.html)
Mọi hình là sơ đồ nguyên lý tự vẽ, không theo tỉ lệ.
"""
import math
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
FONT = 'font-family="system-ui, sans-serif" font-size="13"'
RED = "#dc2626"
ORANGE = "#ea580c"
BLUE = "#0284c7"
GREY = "#94a3b8"
DEFS = ('<defs>'
        '<marker id="b4{p}-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path d="M1 1 L9 5 L1 9" fill="none" stroke="currentColor" stroke-width="1.6"/></marker>'
        '<marker id="b4{p}-rr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        f'orient="auto-start-reverse"><path d="M1 1 L9 5 L1 9" fill="none" stroke="{RED}" stroke-width="1.6"/></marker>'
        '<marker id="b4{p}-br" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        f'orient="auto-start-reverse"><path d="M1 1 L9 5 L1 9" fill="none" stroke="{BLUE}" stroke-width="1.6"/></marker>'
        '</defs>')
EPS_C = 'ε<tspan font-size="9" baseline-shift="sub">c</tspan>'


def fig(svg, cap):
    return f'<figure class="fig" data-tl="1">{svg}<figcaption>{cap}</figcaption></figure>'


def svg_open(w, h, label, p):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}" {FONT}>'
            + DEFS.format(p=p))


def t(x, y, s, extra=""):
    return f'<text x="{x}" y="{y}" fill="currentColor" font-size="12"{extra}>{s}</text>'


def tc(x, y, s, color, extra=""):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="12"{extra}>{s}</text>'


# Hình 1: gá đặt — ① định vị (tì đáy, chặn cạnh) → ② kẹp chặt (lực W)
def fig1():
    o = [svg_open(420, 220, "Gá đặt: định vị trước, kẹp chặt sau", "f1")]
    for i, dx in enumerate((0, 210)):
        # bàn máy
        o.append(f'<rect x="{20 + dx}" y="170" width="175" height="14" fill="{GREY}" fill-opacity=".5" stroke="currentColor"/>')
        # chi tiết
        o.append(f'<rect x="{60 + dx}" y="110" width="100" height="48" fill="{ORANGE}" fill-opacity=".2" '
                 f'stroke="{ORANGE}" stroke-width="2"/>')
        # hai điểm tì dưới đáy (tam giác đỉnh chạm đáy chi tiết)
        for px in (78, 142):
            x = px + dx
            o.append(f'<path d="M{x} 158 L{x - 7} 170 L{x + 7} 170 Z" fill="{BLUE}"/>')
        # cữ chặn cạnh trái
        o.append(f'<rect x="{40 + dx}" y="118" width="12" height="52" fill="{GREY}" stroke="currentColor"/>')
        o.append(f'<path d="M{60 + dx} 136 L{52 + dx} 129 L{52 + dx} 143 Z" fill="{BLUE}"/>')
    # ① đẩy chi tiết về phía cữ
    o.append(t(20, 22, "① Định vị", ' font-weight="700"'))
    o.append(f'<line x1="192" y1="134" x2="166" y2="134" stroke="{BLUE}" stroke-width="2" marker-end="url(#b4f1-br)"/>')
    o.append(tc(20, 204, "tì đáy + chặn cạnh", BLUE))
    o.append(t(84, 104, "mặt A"))
    # ② kẹp
    o.append(t(230, 22, "② Kẹp chặt", ' font-weight="700"'))
    o.append(f'<line x1="320" y1="50" x2="320" y2="106" stroke="{RED}" stroke-width="3" marker-end="url(#b4f1-rr)"/>')
    o.append(tc(328, 78, "W", RED, ' font-weight="700"'))
    o.append(tc(230, 204, "lực W giữ nguyên vị trí", RED))
    o.append("</svg>")
    return fig("".join(o), "Hình 1. Gá đặt: định vị trước (tì đáy, chặn cạnh), kẹp chặt sau (lực W).")


# Hình 2: chuẩn thiết kế thực (mặt A trục bậc) và ảo (đỉnh nón O bánh răng côn)
def fig2():
    o = [svg_open(420, 240, "Chuẩn thiết kế thực và ảo", "f2")]
    o.append(t(20, 22, "Trục bậc", ' font-weight="700"'))
    o.append(f'<rect x="20" y="80" width="70" height="60" fill="{GREY}" fill-opacity=".3" stroke="currentColor" stroke-width="1.6"/>')
    o.append(f'<rect x="90" y="95" width="90" height="30" fill="{GREY}" fill-opacity=".3" stroke="currentColor" stroke-width="1.6"/>')
    o.append(f'<line x1="12" y1="110" x2="190" y2="110" stroke="currentColor" stroke-dasharray="10 3 2 3" stroke-width=".8"/>')
    o.append(f'<line x1="20" y1="76" x2="20" y2="144" stroke="{RED}" stroke-width="4"/>')
    # đường gióng + kích thước từ mặt A
    for x, y0, y1 in ((20, 144, 205), (90, 142, 180), (180, 127, 205)):
        o.append(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="currentColor" stroke-width=".8" stroke-dasharray="3 2"/>')
    o.append('<line x1="20" y1="174" x2="90" y2="174" stroke="currentColor" stroke-width="1.2" '
             'marker-start="url(#b4f2-ar)" marker-end="url(#b4f2-ar)"/>')
    o.append(t(48, 168, "l₁"))
    o.append('<line x1="20" y1="199" x2="180" y2="199" stroke="currentColor" stroke-width="1.2" '
             'marker-start="url(#b4f2-ar)" marker-end="url(#b4f2-ar)"/>')
    o.append(t(94, 193, "l₂"))
    o.append(tc(20, 228, "mặt A — chuẩn thực", RED, ' font-weight="700"'))
    # bánh răng côn
    o.append(t(240, 22, "Bánh răng côn", ' font-weight="700"'))
    ox, oy = 360, 130
    ytop = oy - 70 * (ox - 295) / (ox - 250)
    ybot = 2 * oy - ytop
    o.append(f'<path d="M250 60 L295 {ytop:.1f} L295 {ybot:.1f} L250 200 Z" fill="{ORANGE}" fill-opacity=".2" '
             f'stroke="{ORANGE}" stroke-width="2"/>')
    o.append(f'<rect x="250" y="118" width="45" height="24" fill="none" stroke="{ORANGE}" stroke-width="1.4"/>')
    o.append(f'<line x1="295" y1="{ytop:.1f}" x2="{ox}" y2="{oy}" stroke="currentColor" stroke-dasharray="5 4"/>')
    o.append(f'<line x1="295" y1="{ybot:.1f}" x2="{ox}" y2="{oy}" stroke="currentColor" stroke-dasharray="5 4"/>')
    o.append(f'<line x1="236" y1="{oy}" x2="380" y2="{oy}" stroke="currentColor" stroke-dasharray="10 3 2 3" stroke-width=".8"/>')
    o.append(f'<circle cx="{ox}" cy="{oy}" r="5" fill="{RED}"/>')
    o.append(tc(ox + 4, oy - 12, "O", RED, ' font-weight="700"'))
    o.append(tc(240, 228, "đỉnh nón O — chuẩn ảo", RED, ' font-weight="700"'))
    o.append("</svg>")
    return fig("".join(o), "Hình 2. Chuẩn thiết kế: mặt A có thật (thực); đỉnh nón O không có thật (ảo).")


# Hình 3: cây phân loại chuẩn, kèm ví dụ
def fig3():
    rows = [  # (mức, tên, màu, ví dụ)
        (0, "Chuẩn", "currentColor", ""),
        (1, "Thiết kế", BLUE, "vẽ, ghi kích thước"),
        (2, "Thực", "currentColor", "mặt đầu trục bậc"),
        (2, "Ảo", "currentColor", "đỉnh nón, tâm lỗ"),
        (1, "Công nghệ", ORANGE, ""),
        (2, "Gia công", RED, "gá để cắt — luôn thực"),
        (3, "Thô", "currentColor", "mặt chưa gia công"),
        (3, "Tinh", "currentColor", "mặt đã gia công"),
        (4, "Tinh chính", RED, "lỗ bánh răng: gá + lắp"),
        (4, "Tinh phụ", RED, "lỗ tâm trục: chỉ gá"),
        (2, "Lắp ráp", "currentColor", "vị trí khi lắp"),
        (2, "Đo lường", "currentColor", "căn cứ để đo"),
    ]
    dy, y0 = 25, 26
    h = y0 + dy * (len(rows) - 1) + 16
    o = [svg_open(420, h, "Sơ đồ phân loại chuẩn", "f3")]
    X = lambda lv: 14 + lv * 26
    ys = [y0 + i * dy for i in range(len(rows))]
    # nối cha – con
    for i, (lv, *_rest) in enumerate(rows):
        kids = []
        for j in range(i + 1, len(rows)):
            if rows[j][0] <= lv:
                break
            if rows[j][0] == lv + 1:
                kids.append(j)
        if not kids:
            continue
        xv = X(lv) + 7
        o.append(f'<line x1="{xv}" y1="{ys[i] + 5}" x2="{xv}" y2="{ys[kids[-1]] - 4}" stroke="{GREY}" stroke-width="1.4"/>')
        for j in kids:
            o.append(f'<line x1="{xv}" y1="{ys[j] - 4}" x2="{X(lv + 1) - 4}" y2="{ys[j] - 4}" stroke="{GREY}" stroke-width="1.4"/>')
    for (lv, name, color, ex), y in zip(rows, ys):
        weight = ' font-weight="700"' if lv <= 2 and name not in ("Thực", "Ảo", "Lắp ráp", "Đo lường") or lv == 4 else ""
        o.append(f'<text x="{X(lv)}" y="{y}" fill="{color}" font-size="13"{weight}>{name}</text>')
        if ex:
            o.append(f'<line x1="214" y1="{y - 4}" x2="222" y2="{y - 4}" stroke="{GREY}"/>')
            o.append(t(228, y, ex))
    o.append("</svg>")
    return fig("".join(o), "Hình 3. Các loại chuẩn; cột phải là ví dụ.")


# Hình 4: 6 bậc tự do — 3 tịnh tiến (xanh) + 3 quay (đỏ)
def fig4():
    o = [svg_open(420, 270, "Sáu bậc tự do của vật rắn", "f4")]
    O = (200, 150)
    ends = {"x": (85, 213), "y": (350, 150), "z": (200, 40)}
    for name, (ex, ey) in ends.items():
        o.append(f'<line x1="{O[0]}" y1="{O[1]}" x2="{ex}" y2="{ey}" stroke="currentColor" stroke-width="1.6" '
                 'marker-end="url(#b4f4-ar)"/>')
    o.append(t(72, 226, "x", ' font-weight="700" font-size="14"'))
    o.append(t(356, 155, "y", ' font-weight="700" font-size="14"'))
    o.append(t(207, 38, "z", ' font-weight="700" font-size="14"'))
    o.append(f'<circle cx="{O[0]}" cy="{O[1]}" r="3.5" fill="currentColor"/>')
    o.append(t(176, 146, "O"))
    # tịnh tiến (mũi tên hai đầu song song trục)
    blue = f'stroke="{BLUE}" stroke-width="2.4" marker-start="url(#b4f4-br)" marker-end="url(#b4f4-br)"'
    o.append(f'<line x1="240" y1="100" x2="240" y2="58" {blue}/>')
    o.append(f'<line x1="255" y1="182" x2="335" y2="182" {blue}/>')
    # trục x: hướng (-115, 63); pháp tuyến (cos61°, sin61°)
    d = (-115, 63)
    nx, ny = math.cos(math.radians(61)), math.sin(math.radians(61))
    p = lambda s, off: (O[0] + d[0] * s + nx * off, O[1] + d[1] * s + ny * off)
    a, b = p(0.55, 18), p(0.9, 18)
    o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" {blue}/>')
    # quay (cung elip quanh trục)
    red = f'fill="none" stroke="{RED}" stroke-width="2.4" marker-end="url(#b4f4-rr)"'
    o.append(f'<path d="M178 75 A22 7 0 0 0 222 75" {red}/>')
    o.append(f'<path d="M300 128 A7 22 0 0 1 300 172" {red}/>')
    c = p(0.3, 0)
    e1 = (c[0] - 22 * nx, c[1] - 22 * ny)
    e2 = (c[0] + 22 * nx, c[1] + 22 * ny)
    o.append(f'<path d="M{e1[0]:.1f} {e1[1]:.1f} A22 7 61 0 0 {e2[0]:.1f} {e2[1]:.1f}" {red}/>')
    # chú giải
    o.append(f'<line x1="20" y1="252" x2="56" y2="252" {blue}/>')
    o.append(tc(64, 256, "3 tịnh tiến dọc x, y, z", BLUE))
    o.append(f'<path d="M236 256 A16 6 0 0 0 268 256" {red}/>')
    o.append(tc(276, 256, "3 quay quanh x, y, z", RED))
    o.append("</svg>")
    return fig("".join(o), "Hình 4. Vật rắn tự do có 6 bậc tự do: 3 tịnh tiến (xanh), 3 quay (đỏ).")


# Hình 5: định vị hình hộp 3 – 2 – 1
def fig5():
    o = [svg_open(420, 320, "Định vị chi tiết hình hộp theo sơ đồ 3 – 2 – 1, nhìn từ dưới lên", "f5")]
    # hộp chiếu xiên nhìn từ dưới: mặt trước (90,110)-(300,140) cao 30, độ sâu (70,+70) → thấy mặt đáy lớn
    F = [(90, 110), (300, 110), (300, 140), (90, 140)]
    D = (70, 70)
    sh = lambda P: (P[0] + D[0], P[1] + D[1])
    pts = lambda P: " ".join(f"{x},{y}" for x, y in P)
    o.append(f'<polygon points="{pts([F[3], F[2], sh(F[2]), sh(F[3])])}" fill="{RED}" fill-opacity=".1" stroke="{ORANGE}" stroke-width="1.8"/>')
    o.append(f'<polygon points="{pts([F[1], sh(F[1]), sh(F[2]), F[2]])}" fill="#16a34a" fill-opacity=".1" stroke="{ORANGE}" stroke-width="1.8"/>')
    o.append(f'<polygon points="{pts(F)}" fill="{BLUE}" fill-opacity=".1" stroke="{ORANGE}" stroke-width="1.8"/>')
    hid = sh(F[0])
    for b in (F[0], sh(F[1]), sh(F[3])):
        o.append(f'<line x1="{hid[0]}" y1="{hid[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{ORANGE}" stroke-width="1" stroke-dasharray="4 3"/>')

    def pin(px, py, qx, qy, color, label, lx, ly):
        o.append(f'<line x1="{px}" y1="{py}" x2="{qx}" y2="{qy}" stroke="{color}" stroke-width="2.4"/>')
        o.append(f'<circle cx="{px}" cy="{py}" r="4.5" fill="{color}"/>')
        o.append(tc(lx, ly, label, color, ' font-weight="700"'))

    # mặt đáy (lớn nhất, thấy được khi nhìn từ dưới): 3 điểm, chốt thẳng xuống
    for k, (u, v) in enumerate(((0.2, 0.25), (0.88, 0.25), (0.45, 0.75)), 1):
        x, y = round(90 + 210 * u + 70 * v, 1), 140 + 70 * v
        o.append(f'<path d="M{x} 246 L{x - 7} 256 L{x + 7} 256 Z" fill="{RED}"/>')
        pin(x, y, x, 246, RED, str(k), round(x + 8, 1), 242)
    # mặt trước (dài nhất): 2 điểm, chốt hướng về phía người nhìn
    for k, u in ((4, 0.18), (5, 0.84)):
        x = round(90 + 210 * u, 1)
        pin(x, 125, round(x - 18, 1), 113, BLUE, str(k), round(x + 8, 1), 131)
    # mặt đầu phải (nhỏ nhất): 1 điểm
    pin(335, 160, 385, 160, "#16a34a", "6", 391, 165)
    o.append(tc(20, 280, "1 – 2 – 3: mặt đáy lớn nhất, định vị chính", RED))
    o.append(tc(20, 298, "4 – 5: mặt dài nhất, dẫn hướng", BLUE))
    o.append(tc(20, 316, "6: mặt nhỏ nhất, chặn", "#16a34a"))
    o.append("</svg>")
    return fig("".join(o), "Hình 5. Sơ đồ 3 – 2 – 1 (hộp nhìn từ dưới lên): sáu điểm khử đủ 6 bậc tự do.")


# Hình 6: sai số chuẩn kích thước 35 — tì mặt B (trái) và tì mặt C (phải)
def fig6():
    o = [svg_open(420, 262, "Sai số chuẩn khi tì mặt B và khi tì mặt C", "f6")]
    top, bot, step = 86, 190, 142

    def block(dx):
        o.append(f'<path d="M{50 + dx} {bot} L{170 + dx} {bot} L{170 + dx} {step} L{120 + dx} {step} L{120 + dx} {top} '
                 f'L{50 + dx} {top} Z" fill="{ORANGE}" fill-opacity=".18" stroke="{ORANGE}" stroke-width="2"/>')
        # dao phay
        o.append(f'<circle cx="{145 + dx}" cy="{step - 21}" r="20" fill="{GREY}" fill-opacity=".35" stroke="currentColor"/>')
        o.append(t(136 + dx, step - 16, "dao"))
        # kích thước 35 từ mặt C
        o.append(f'<line x1="{120 + dx}" y1="{top}" x2="{190 + dx}" y2="{top}" stroke="currentColor" stroke-width=".8" stroke-dasharray="3 2"/>')
        o.append(f'<line x1="{170 + dx}" y1="{step}" x2="{190 + dx}" y2="{step}" stroke="currentColor" stroke-width=".8" stroke-dasharray="3 2"/>')
        o.append(f'<line x1="{185 + dx}" y1="{top}" x2="{185 + dx}" y2="{step}" stroke="currentColor" stroke-width="1.2" '
                 'marker-start="url(#b4f6-ar)" marker-end="url(#b4f6-ar)"/>')
        o.append(t(189 + dx, 118, "35"))
        o.append(tc(58 + dx, top + 16, "C", RED, ' font-weight="700"'))
        o.append(tc(58 + dx, bot - 6, "B", BLUE, ' font-weight="700"'))
        o.append(f'<line x1="{50 + dx}" y1="{top}" x2="{120 + dx}" y2="{top}" stroke="{RED}" stroke-width="3"/>')
        o.append(f'<line x1="{50 + dx}" y1="{bot}" x2="{170 + dx}" y2="{bot}" stroke="{BLUE}" stroke-width="3"/>')

    # trái: tì mặt B trên bàn máy
    o.append(t(20, 18, "Tì mặt B", ' font-weight="700"'))
    block(0)
    o.append(f'<rect x="30" y="{bot + 1}" width="160" height="10" fill="{GREY}" fill-opacity=".5" stroke="currentColor"/>')
    o.append(f'<line x1="26" y1="{top}" x2="46" y2="{top}" stroke="currentColor" stroke-width=".8" stroke-dasharray="3 2"/>')
    o.append(f'<line x1="30" y1="{top}" x2="30" y2="{bot}" stroke="currentColor" stroke-width="1.2" '
             'marker-start="url(#b4f6-ar)" marker-end="url(#b4f6-ar)"/>')
    o.append(t(6, 142, "65"))
    o.append(tc(20, 234, "chuẩn B ≠ gốc C", RED))
    o.append(tc(20, 254, f"{EPS_C}(35) = 0,24 mm", RED, ' font-weight="700"'))
    # phải: mặt C áp vào tấm tì cố định của đồ gá, lực W đẩy từ dưới
    dx = 210
    o.append(t(230, 18, "Tì mặt C", ' font-weight="700"'))
    block(dx)
    o.append(f'<rect x="{40 + dx}" y="{top - 12}" width="80" height="12" fill="{GREY}" fill-opacity=".6" stroke="currentColor"/>')
    o.append(t(42 + dx, top - 18, "tấm tì cố định"))
    o.append(f'<line x1="{85 + dx}" y1="222" x2="{85 + dx}" y2="{bot + 4}" stroke="{RED}" stroke-width="3" marker-end="url(#b4f6-rr)"/>')
    o.append(tc(103 + dx, 214, "W", RED, ' font-weight="700"'))
    o.append(tc(95 + dx, 236, "chuẩn C = gốc C", BLUE))
    o.append(tc(95 + dx, 254, f"{EPS_C}(35) = 0", BLUE, ' font-weight="700"'))
    o.append("</svg>")
    return fig("".join(o), "Hình 6. Kích thước 35 đo từ mặt C: tì B thì có sai số chuẩn, tì C thì bằng 0.")


FIGS = [fig1, fig2, fig3, fig4, fig5, fig6]

src = (HERE / "theory.src.html").read_text(encoding="utf8")
for i, f in enumerate(FIGS, 1):
    key = f"<!--FIG{i}-->"
    assert src.count(key) == 1, key
    src = src.replace(key, f())
assert "<!--FIG" not in src
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html,", len(FIGS), "hình")
