"""Sinh 5 hình SVG cho bài "Bài 9. Khái niệm từ trường" (Vật lí 12) và thay các mốc
<!--FIGn--> trong theory.src.html -> theory.html. Chạy từ thư mục này: python3 build_figs.py
"""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *  # noqa: E402


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def rect(x, y, w, h, fill, stroke="currentColor", sw=2, rx=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def dot(x, y, r=4, c="currentColor"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def wrap(vb, label, body, cap):
    return (f'<figure class="fig" data-tl="1"><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


# ------------------------------------------- Hình 1: la bàn trong điện thoại
b = defs("f1")
b += rect(24, 56, 96, 168, "rgba(148,163,184,.10)", "currentColor", 2, 12)
b += rect(38, 70, 68, 140, "rgba(148,163,184,.16)", "currentColor", 1.4, 6)
b += f'<circle cx="72" cy="140" r="42" fill="none" stroke="currentColor" stroke-width="1.4" opacity="0.55"/>'
b += f'<circle cx="72" cy="140" r="4" fill="currentColor"/>'
b += f'<polygon points="72,106 78,140 72,134 66,140" fill="{RED}"/>'
b += f'<polygon points="72,174 78,140 72,146 66,140" fill="{BLUE}"/>'
b += text(72, 91, "N", RED, 14, "middle", "700")
b += text(72, 199, "S", BLUE, 14, "middle", "700")
b += text(84, 246, "la bàn trong máy", "currentColor", 14, "start", "500")
b += arrow("f1", "r", 132, 176, 132, 100, 2.6)
b += text(144, 132, "kim chỉ bắc", RED, 14, "start", "700")
b += text(144, 152, "dù xoay máy", "currentColor", 14, "start", "500")
b += rect(252, 50, 184, 188, "rgba(52,211,153,.14)", GRN, 1.8, 10)
b += text(344, 76, "cạnh cửa sắt", GRN, 14, "middle", "700")
b += f'<circle cx="344" cy="130" r="34" fill="none" stroke="currentColor" stroke-width="1.4" opacity="0.55"/>'
b += line(344, 92, 344, 104, "currentColor", 1.2, "3 3", .6)
b += f'<g transform="translate(344,130) rotate(55)"><polygon points="0,-28 6,0 0,-6 -6,0" fill="{RED}"/><polygon points="0,28 6,0 0,6 -6,0" fill="{BLUE}"/></g>'
b += text(344, 200, "kim lệch hẳn", GRN, 14, "middle", "500")
b += text(344, 220, "khỏi hướng bắc", GRN, 14, "middle", "500")
fig1 = wrap("0 0 440 258",
            "Điện thoại có la bàn: kim chỉ về phía bắc dù xoay máy; đặt cạnh cửa sắt thì kim lệch hẳn",
            b, "Hình 1. La bàn chỉ một phía; gần cửa sắt thì kim lệch.")

# ------------------------------------------- Hình 2: hút – đẩy giữa hai nam châm (ảnh OpenStax chèn trực tiếp, webp)
fig2 = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l12-khai-niem-tu-truong/hinh-2.webp" '
        'alt="Hai cặp nam châm thanh: hai cực khác tên đặt gần nhau thì hút nhau, hai cực cùng tên đặt gần nhau thì đẩy nhau; mũi tên đỏ chỉ chiều lực" '
        'loading="lazy" width="640" height="593" style="display:block;margin:0 auto;max-width:min(100%,420px);height:auto;border-radius:8px">'
        '<figcaption>Hình 2. Mũi tên đỏ: chiều lực.<br>'
        'Unlikes attract = khác tên hút; likes repel = cùng tên đẩy.<br>'
        'Hình: OpenStax, <em>College Physics 2e</em>, Hình 22.5 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</figcaption></figure>')

# ------------------------------------------- Hình 3 (OpenStax, đầu hàm) + Hình 4: ba khung (SVG)
# Đường sức thanh nam châm vẽ trên MẶT PHẲNG HÌNH (như mạt sắt rắc trên tấm bìa): hai cực N (+q, trái) và
# S (−q, phải) đặt trong thân, cách mỗi đầu thanh 6 px; trường phẳng của hai "từ tích" có HÀM THÔNG LƯỢNG
#   Ψ(z, x) = θ_N − θ_S ,   θ_N = atan2(x, z + a), θ_S = atan2(x, z − a)   (z dọc trục sang phải, x lên; px)
# Đường sức là ĐƯỜNG MỨC của Ψ (cung tròn qua hai cực). Thông lượng giữa hai đường kề nhau = hiệu Ψ, nên chọn
# các mức Ψ CÁCH ĐỀU → mật độ đường trên hình ∝ |B| tự nhiên: mau ở hai cực, thưa dần ra xa. Sát cực N,
# Ψ ≈ φ − π (φ: góc rời cực đo từ +z) → mức cách đều = góc rời cực cách đều. Mỗi đường vẽ bằng RK4 theo B,
# xuất phát trên vòng nhỏ quanh N tại đúng điểm có Ψ = mức (chia đôi), rồi kiểm Ψ không trôi dọc đường.
import math as _mm


def _psi(z, x, a):
    return _mm.atan2(x, z + a) - _mm.atan2(x, z - a)


def _Bdir(z, x, a):
    bz = bx = 0.0
    for zc, q in ((-a, 1.0), (a, -1.0)):
        dz, dx = z - zc, x
        r2 = dz * dz + dx * dx + 1e-12
        bz += q * dz / r2; bx += q * dx / r2
    n = _mm.hypot(bz, bx) + 1e-15
    return bz / n, bx / n


def duong_muc(level, a, e=1.0, h=0.5, maxn=20000):
    """Đường sức có Ψ = level (nửa trên, x > 0), từ N (z = −a) tới S (z = +a); toạ độ px quanh tâm thanh."""
    lo, hi = 1e-6, _mm.pi - 1e-6
    for _ in range(60):                      # Ψ trên vòng bán kính e quanh N tăng đơn điệu theo góc
        ph = (lo + hi) / 2
        if _psi(-a + e * _mm.cos(ph), e * _mm.sin(ph), a) < level: lo = ph
        else: hi = ph
    z, x = -a + e * _mm.cos(ph), e * _mm.sin(ph)
    P = [(z, x)]
    f = lambda z, x: _Bdir(z, x, a)
    for _ in range(maxn):
        k1 = f(z, x); k2 = f(z + h / 2 * k1[0], x + h / 2 * k1[1])
        k3 = f(z + h / 2 * k2[0], x + h / 2 * k2[1]); k4 = f(z + h * k3[0], x + h * k3[1])
        z += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); x += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        P.append((z, x))
        if _mm.hypot(z - a, x) < e:
            break
    assert max(abs(_psi(z, x, a) - level) for z, x in P[3:-3]) < 2e-3, "Ψ trôi"
    return P


def _trong_than(px, py, cx, cy, g=2.0):
    """Điểm màn hình có nằm trong khối nam châm (mặt trước + mặt trên + mặt bên, nới g px) không."""
    dx, dy = BAR_D
    x0, x1, y0, y1 = cx - BAR_L / 2, cx + BAR_L / 2, cy - BAR_H / 2, cy + BAR_H / 2
    if x0 - g <= px <= x1 + g and y0 - g <= py <= y1 + g:
        return True
    if y0 + dy - g <= py <= y0:                                   # mặt trên (hình bình hành)
        t = (y0 - py) / -dy
        if x0 + dx * t - g <= px <= x1 + dx * t + g:
            return True
    return x1 <= px <= x1 + dx + g and y0 + dy - g <= py <= y1 + g  # mặt bên


def _cat_doan(Q, ok):
    """Tách polyline thành các đoạn liên tục gồm những điểm thoả ok(p)."""
    seg, out = [], []
    for p in Q:
        if ok(p):
            seg.append(p)
        elif seg:
            if len(seg) > 2: out.append(seg)
            seg = []
    if len(seg) > 2: out.append(seg)
    return out


def _bar_lines(cx, cy, fr):
    """Danh sách (Q, k) — các đoạn polyline màn hình nằm trong khung fr = (x0, y0, x1, y1) (nới 3 px, phần còn lại
    do clipPath cắt) và ngoài thân nam châm; k = chỉ số mức (0 = sát thân)."""
    X0, Y0, X1, Y1 = fr
    out = []
    for k, lv in enumerate(BAR_PSI):
        # dừng cách thân 3 px; sát hai cực các đường chụm lại nên đường lẻ dừng xa cực hơn (so le) cho nét khỏi dính cục
        r0 = BAR_R0[k % 2]
        ok = lambda p: (X0 - 3 <= p[0] <= X1 + 3 and Y0 - 3 <= p[1] <= Y1 + 3 and not _trong_than(p[0], p[1], cx, cy, 3)
                        and min(_mm.hypot(p[0] - cx - z, p[1] - cy) for z in (-BAR_A, BAR_A)) >= r0)
        P = duong_muc(lv, BAR_A, maxn=40000)
        for sg in (1, -1):
            for Q in _cat_doan([(cx + z, cy - sg * x) for z, x in P], ok):
                out.append((Q, k))
    return out


def _rdp(Q, tol):
    """Giản lược Ramer–Douglas–Peucker: bỏ điểm lệch dây cung < tol px (HTML gọn, đường cong vẫn trơn)."""
    if len(Q) < 3: return list(Q)
    (x1, y1), (x2, y2) = Q[0], Q[-1]
    n = _mm.hypot(x2 - x1, y2 - y1) or 1e-9
    i, dm = max(((j, abs((x2 - x1) * (y1 - Q[j][1]) - (x1 - Q[j][0]) * (y2 - y1)) / n) for j in range(1, len(Q) - 1)),
                key=lambda t: t[1])
    if dm < tol: return [Q[0], Q[-1]]
    return _rdp(Q[:i + 1], tol)[:-1] + _rdp(Q[i:], tol)


def _poly(Q, c, w, dash, op=1, tol=0):
    K = [Q[0]]
    for p in Q[1:-1]:                      # thưa điểm: cách nhau ≥ 4 px cho HTML gọn
        if (p[0] - K[-1][0]) ** 2 + (p[1] - K[-1][1]) ** 2 >= 16:
            K.append(p)
    K.append(Q[-1])
    if tol: K = _rdp(K, tol)
    d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in K)
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-dasharray="{dash}" opacity="{op}" stroke-linecap="round"/>'


# Bộ đường sức chung cho khung ii và iii (bắt chước kiểu hình SGK): thanh dài 192 px (≈ 47 % bề rộng khung 412),
# mỏng 20 px; hai cực cách tâm a = 92 px (4 px trong mỗi đầu) nên đường sức toả như quạt từ mặt đầu thanh.
# 14 mức Ψ cách đều (góc rời cực 29° … 172°, bước ≈ 11°): đường trong cùng ôm sát thân (cao 24 px ở giữa),
# đường ngoài ra khỏi khung — clipPath cắt ở mép, cho thấy trường còn lan ra xa. Thêm đường trục thẳng hai đầu.
BAR_L, BAR_H, BAR_D, BAR_A = 192, 20, (8, -6), 92
BAR_N = 14
BAR_R0 = (12, 22)              # bán kính quanh cực mà đường chẵn / lẻ bắt đầu hiện
_PH0, _PH1 = 2 * _mm.degrees(_mm.atan(24 / BAR_A)), 172.0
BAR_PSI = tuple(_mm.radians(_PH0 + (_PH1 - _PH0) * k / (BAR_N - 1)) - _mm.pi for k in range(BAR_N))
FR_W, FR_H = 412, 240           # khung ii, iii


b = defs("f3")
# i) nam châm chữ U: N trái (đỏ), S phải (xanh); đường sức giữa hai cực thẳng, song song, cách đều, chiều N → S
b += text(14, 20, "i) Chữ U", "currentColor", 14, "start", "700")
# Nam châm chữ U có chiều sâu: khối sau (lệch 8 px lên phải) + mặt trước; gông bo góc, hai cánh rộng 28, khe 56–164.
DP = 8
def _U(dx, dy, fill, sw):
    return (f'<path d="M{28+dx},{40+dy} L{28+dx},{100+dy} Q{28+dx},{128+dy} {56+dx},{128+dy} L{164+dx},{128+dy} '
            f'Q{192+dx},{128+dy} {192+dx},{100+dy} L{192+dx},{40+dy} L{164+dx},{40+dy} L{164+dx},{92+dy} '
            f'Q{164+dx},{100+dy} {156+dx},{100+dy} L{64+dx},{100+dy} Q{56+dx},{100+dy} {56+dx},{92+dy} L{56+dx},{40+dy} Z" '
            f'fill="{fill}" stroke="currentColor" stroke-width="{sw}" stroke-linejoin="round"/>')
b += _U(DP, -DP, "#64748b", 1.2)                       # khối phía sau
for x in (28, 56, 164, 192):                                          # cạnh nối sau – trước ở đầu cánh
    b += line(x, 40, x + DP, 40 - DP, "currentColor", 1.2)
b += f'<polygon points="28,40 {28+DP},{40-DP} {56+DP},{40-DP} 56,40" fill="#fca5a5" stroke="currentColor" stroke-width="1.2"/>'
b += f'<polygon points="164,40 {164+DP},{40-DP} {192+DP},{40-DP} 192,40" fill="#7dd3fc" stroke="currentColor" stroke-width="1.2"/>'
b += _U(0, 0, "#cbd5e1", 1.6)                            # mặt trước (thép, xám)
b += f'<rect x="28" y="40" width="28" height="42" fill="{RED}" stroke="currentColor" stroke-width="1.6"/>'
b += f'<rect x="164" y="40" width="28" height="42" fill="{BLUE}" stroke="currentColor" stroke-width="1.6"/>'
b += text(42, 67, "N", "#0f172a", 16, "middle", "800")
b += text(178, 67, "S", "#0f172a", 16, "middle", "800")
for y in (50, 61, 72):                                                # trong khe: thẳng, song song, cách đều, N → S
    b += field_line(60, y, 160, y, GRN, 1.8, "5 3", 9)
b += text(232, 74, "song song, cách đều", "#047857", 14, "start", "600")
b += text(232, 96, "→ từ trường đều", "#047857", 14, "start", "600")


def _gan_nhat(G, x, y, bo=None):
    """Khoảng cách nhỏ nhất từ (x, y) tới các điểm trong lưới G (ô 8 px), bỏ qua đường có id = bo."""
    best = 1e9
    gx, gy = int(x // 8), int(y // 8)
    for i in range(gx - 2, gx + 3):
        for j in range(gy - 2, gy + 3):
            for px, py, idn in G.get((i, j), ()):
                if idn != bo:
                    best = min(best, _mm.hypot(px - x, py - y))
    return best


def _bo_duong(cx, cy, fr, kieu):
    """kieu='mat_sat': vạch ngắn xám (từ phổ); 'quy_uoc': nét đứt xanh lục + đầu V rải đều, so le (ra N, vào S)."""
    X0, Y0, X1, Y1 = fr
    L = _bar_lines(cx, cy, fr)
    xl, xr = cx - BAR_L / 2, cx + BAR_L / 2 + BAR_D[0]
    g = ""
    if kieu == "mat_sat":
        for Q, k in L:
            g += _poly(Q, "currentColor", 2.2, "3 4", .75, .6)
        g += f'<line x1="{X0}" y1="{cy}" x2="{xl-4}" y2="{cy}" stroke="currentColor" stroke-width="2.2" stroke-dasharray="3 4" opacity=".75"/>'
        g += f'<line x1="{xr+4}" y1="{cy}" x2="{X1}" y2="{cy}" stroke="currentColor" stroke-width="2.2" stroke-dasharray="3 4" opacity=".75"/>'
        return g
    # lưới điểm của mọi đường (kể cả trục) để đầu V không đè lên đường khác
    G = {}
    def _them(pts, idn):
        for i in range(len(pts) - 1):
            (x1, y1), (x2, y2) = pts[i], pts[i + 1]
            n = max(1, int(_mm.hypot(x2 - x1, y2 - y1) / 1.5))
            for t in range(n):
                x, y = x1 + (x2 - x1) * t / n, y1 + (y2 - y1) * t / n
                G.setdefault((int(x // 8), int(y // 8)), []).append((x, y, idn))
    for idn, (Q, k) in enumerate(L):
        _them(Q, idn)
    _them([(X0, cy), (xl - 4, cy)], -1); _them([(xr + 4, cy), (X1, cy)], -2)
    TIP, BUOC, CH = [], 74, 8          # đầu V đã đặt; khoảng cách dọc đường giữa hai đầu V; cỡ đầu V

    def _dat(x, y, dx, dy, idn):
        n = _mm.hypot(dx, dy); ux, uy = dx / n, dy / n
        diem = [(x, y)] + [(x - CH * (ux * _mm.cos(t) - uy * _mm.sin(t)), y - CH * (ux * _mm.sin(t) + uy * _mm.cos(t)))
                           for t in (_mm.radians(30), -_mm.radians(30))]
        for px, py in diem:
            if not (X0 + 8 <= px <= X1 - 8 and Y0 + 8 <= py <= Y1 - 8): return False
            if _trong_than(px, py, cx, cy, 5): return False
            if _gan_nhat(G, px, py, idn) < 4.5: return False
        if any(_mm.hypot(x - a, y - b) < 22 for a, b in TIP): return False
        TIP.append((x, y)); return True

    for idn, (Q, k) in enumerate(L):
        g += _poly(Q, GRN, 1.6, "7 3", 1, .6)
        s = [0.0]
        for i in range(1, len(Q)):
            s.append(s[-1] + _mm.hypot(Q[i][0] - Q[i - 1][0], Q[i][1] - Q[i - 1][1]))
        goc = 26 + (k * 0.38 % 1) * BUOC          # so le giữa các mức
        m = 0
        while goc + m * BUOC < s[-1] - 10:
            for lech in (0, 6, -6, 12, -12, 18, -18, 24, -24, 30, -30):
                sv = goc + m * BUOC + lech
                if not (10 < sv < s[-1] - 10): continue
                i = next(j for j in range(1, len(Q)) if s[j] >= sv)
                i = min(max(i, 2), len(Q) - 3)
                if _dat(Q[i][0], Q[i][1], Q[i + 2][0] - Q[i - 2][0], Q[i + 2][1] - Q[i - 2][1], idn):
                    g += chevron(Q[i][0], Q[i][1], Q[i + 2][0] - Q[i - 2][0], Q[i + 2][1] - Q[i - 2][1], GRN, 1.6, CH)
                    break
            m += 1
    # đường trục hai đầu: ra xa N (trái), đi vào S (phải); đầu V cùng chiều sang trái
    g += f'<line x1="{X0}" y1="{cy}" x2="{xl-4}" y2="{cy}" stroke="{GRN}" stroke-width="1.6" stroke-dasharray="7 3"/>'
    g += f'<line x1="{xr+4}" y1="{cy}" x2="{X1}" y2="{cy}" stroke="{GRN}" stroke-width="1.6" stroke-dasharray="7 3"/>'
    for x in (xl - 40, X0 + 26, X1 - 26, xr + 40):
        g += chevron(x, cy, -1, 0, GRN, 1.6, CH)
    return g


# ii) từ phổ: mạt sắt xếp dọc đúng bộ đường của khung iii
FY2, FY3 = 172, 476
b += text(14, 162, "ii) Từ phổ (mạt sắt)", "currentColor", 14, "start", "700")
b += f'<clipPath id="f3-c2"><rect x="14" y="{FY2}" width="{FR_W}" height="{FR_H}" rx="6"/></clipPath>'
b += rect(14, FY2, FR_W, FR_H, "rgba(148,163,184,.08)", "currentColor", 1.2, 6)
C2 = FY2 + FR_H // 2
b += f'<g clip-path="url(#f3-c2)">{_bo_duong(220, C2, (14, FY2, 14 + FR_W, FY2 + FR_H), "mat_sat")}</g>' + bar_magnet(220, C2, BAR_L, BAR_H, BAR_D)
b += text(14, FY2 + FR_H + 24, "mạt sắt dày ở hai cực", "currentColor", 14, "start", "600")
# iii) đường sức vẽ theo quy ước: cùng bộ đường, nét đứt, có chiều
b += text(14, FY3 - 10, "iii) Đường sức quy ước", "currentColor", 14, "start", "700")
b += f'<clipPath id="f3-c3"><rect x="14" y="{FY3}" width="{FR_W}" height="{FR_H}" rx="6"/></clipPath>'
b += rect(14, FY3, FR_W, FR_H, "rgba(148,163,184,.08)", "currentColor", 1.2, 6)
C3 = FY3 + FR_H // 2
b += f'<g clip-path="url(#f3-c3)">{_bo_duong(220, C3, (14, FY3, 14 + FR_W, FY3 + FR_H), "quy_uoc")}</g>' + bar_magnet(220, C3, BAR_L, BAR_H, BAR_D)
for i, (c1, c2) in enumerate((("ra ở N, vào ở S", "gần cực: mau"), ("không cắt nhau", "xa cực: thưa"), ("khép kín", None))):
    yy = FY3 + FR_H + 24 + 22 * i
    b += text(14, yy, c1, "currentColor", 14, "start", "600")
    if c2: b += text(230, yy, c2, "currentColor", 14, "start", "600")
fig3b = wrap("0 0 440 796",
            "Ba khung: đường sức từ của nam châm chữ U (từ trường đều), từ phổ mạt sắt quanh thanh nam châm và đường sức vẽ theo quy ước",
            b, "Hình 4.<br>i) Chữ U: từ trường đều.<br>ii) Từ phổ.<br>iii) Đường quy ước.")
fig3 = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l12-khai-niem-tu-truong/hinh-duong-suc-thanh-nam-cham.webp" '
        'alt="Thanh nam châm thẳng: a) kim la bàn đặt quanh nam châm chỉ theo từ trường; b) và c) đường sức đi ra ở cực bắc, vào ở cực nam, đường c khép kín qua thân nam châm" '
        'loading="lazy" width="1000" height="344" style="display:block;margin:0 auto;max-width:100%;height:auto;border-radius:8px">'
        '<figcaption>Hình 3. Đường sức khép kín.<br>'
        
        '<small>Hình: OpenStax, <em>College Physics 2e</em>, Hình 22.14 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>')

# ------------------------------------------- Hình 5: từ trường Trái Đất (lưỡng cực, trục từ lệch trục quay 11°)
import math as _m
b = defs("f4")
CX, CY, RE, TILT = 200, 168, 72, -11       # TILT: góc quay trục từ so với trục địa lí (độ, âm = ngược kim đồng hồ)
_c, _s = _m.cos(_m.radians(TILT)), _m.sin(_m.radians(TILT))


def _rot(u, v):      # (u, v) trong hệ nam châm (v hướng xuống, trục từ dọc v) → màn hình
    return CX + u * _c - v * _s, CY + u * _s + v * _c


b += f'<circle cx="{CX}" cy="{CY}" r="{RE}" fill="rgba(56,189,248,.10)" stroke="currentColor" stroke-width="2"/>'
b += line(CX, 32, CX, 300, "currentColor", 1.2, "6 5", .5)
b += text(CX, 24, "Bắc địa lí", "currentColor", 14, "middle", "700")
b += text(CX, 322, "Nam địa lí", "currentColor", 14, "middle", "700")
# đường sức lưỡng cực r = L sin²θ (θ đo từ cực trên = cực từ nam); ngoài Trái Đất đi từ cực dưới (N) lên cực trên (S)
for L in (1.35 * RE, 2.1 * RE, 2.6 * RE):
    th0 = _m.asin(_m.sqrt(RE / L))
    for sg in (1, -1):
        pts = [_rot(sg * L * _m.sin(t) ** 3, -L * _m.sin(t) ** 2 * _m.cos(t))
               for t in [th0 + (_m.pi - 2 * th0) * k / 80 for k in range(81)]]
        b += _poly(pts, GRN, 1.8, "6 4")
        tx, ty = _rot(sg * L, 0)
        ax, ay = _rot(0, -1); ax -= CX; ay -= CY    # tại xích đạo từ: B song song trục, hướng về cực trên (S)
        b += chevron(tx, ty, ax, ay, GRN, 1.8, 10)
# nam châm trong lòng Trái Đất: nửa trên S (xanh), nửa dưới N (đỏ)
(x1, y1), (x0, y0), (x2, y2) = _rot(0, -46), _rot(0, 0), _rot(0, 46)
b += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x0:.1f}" y2="{y0:.1f}" stroke="{BLUE}" stroke-width="10"/>'
b += f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{RED}" stroke-width="10"/>'
b += text(round(x1 - 16), round(y1 + 6), "S", BLUE, 14, "middle", "700")
b += text(round(x2 + 16), round(y2 + 6), "N", RED, 14, "middle", "700")
b += text(14, 24, "S: cực từ nam", BLUE, 14, "start", "700")
b += text(14, 322, "N: cực từ bắc", RED, 14, "start", "700")
# kim la bàn đặt trên đường sức L = 2,1 RE, tại xích đạo từ bên phải: nằm dọc đường sức, đầu bắc (đỏ) chỉ về cực từ nam
kx, ky = _rot(2.1 * RE, 0)
ux, uy = _rot(0, -1); ux -= CX; uy -= CY
b += (f'<polygon points="{kx+24*ux:.1f},{ky+24*uy:.1f} {kx-8*uy:.1f},{ky+8*ux:.1f} {kx+8*uy:.1f},{ky-8*ux:.1f}" fill="{RED}"/>'
      f'<polygon points="{kx-24*ux:.1f},{ky-24*uy:.1f} {kx-8*uy:.1f},{ky+8*ux:.1f} {kx+8*uy:.1f},{ky-8*ux:.1f}" fill="{BLUE}"/>'
      f'<circle cx="{kx:.1f}" cy="{ky:.1f}" r="2.5" fill="currentColor"/>'
      f'<circle cx="{kx:.1f}" cy="{ky:.1f}" r="28" fill="none" stroke="currentColor" stroke-width="1.4" opacity=".6"/>')
b += text(426, 24, "kim la bàn", "currentColor", 14, "end", "700")
b += text(426, 42, "nằm theo đường sức", GRN, 14, "end", "600")
fig4 = wrap("0 0 440 334",
            "Trái Đất như một nam châm khổng lồ có trục từ lệch trục quay: gần bắc địa lí là cực từ nam, đường sức ngoài Trái Đất đi vào đó; kim la bàn nằm theo đường sức",
            b, "Hình 5. Gần bắc địa lí là <strong>cực từ nam</strong>, nên cực bắc của kim bị hút về đó.")

# ------------------------------------------- Hình 6: hai từ trường vuông góc
# tỉ lệ chung 2,4 px/µT: 30 µT → 72 px, 40 µT → 96 px, 50 µT → 120 px lệch 53° so với bắc
OX, OY, K = 150, 204, 2.4
b = defs("f5")
b += line(40, OY, 400, OY, "currentColor", 1.6)
b += line(OX, OY, OX, 46, "currentColor", 1.6)
b += text(400, 228, "đông", "currentColor", 14, "end", "600")
b += text(OX, 36, "bắc", "currentColor", 14, "middle", "600")
b += f'<circle cx="{OX}" cy="{OY}" r="5" fill="currentColor"/>'
b += arrow("f5", "g", OX, OY, OX, OY - K * 30, 2.8)
b += arrow("f5", "r", OX, OY, OX + K * 40, OY, 2.8)
b += arrow("f5", "b", OX, OY, OX + K * 40, OY - K * 30, 2.8)
assert abs(_m.hypot(K * 40, K * 30) - K * 50) < 1e-9
b += f'<text x="{OX-14}" y="{OY-K*30+6}" fill="{GRN}" font-size="14" font-weight="700" text-anchor="end">B<tspan font-size="14" baseline-shift="sub">đ</tspan> = 30 µT</text>'
b += f'<text x="{OX+K*20}" y="{OY+24}" fill="{RED}" font-size="14" font-weight="700" text-anchor="middle">B<tspan font-size="14" baseline-shift="sub">1</tspan> = 40 µT</text>'
b += text(OX + K * 40 + 8, OY - K * 30 - 4, "B = 50 µT", BLUE, 14, "start", "700")
b += line(OX + K * 40, OY - K * 30, OX + K * 40, OY, "currentColor", 1.2, "5 4", .45)
b += line(OX + K * 40, OY - K * 30, OX, OY - K * 30, "currentColor", 1.2, "5 4", .45)
ra = 42
b += f'<path d="M{OX},{OY-ra} A{ra},{ra} 0 0,1 {OX+ra*0.8:.1f},{OY-ra*0.6:.1f}" fill="none" stroke="currentColor" stroke-width="1.4"/>'
b += text(OX + 6, OY - ra - 10, "53°", "currentColor", 14, "start", "700")
fig5 = wrap("0 0 440 240",
            "Hai từ trường thành phần vuông góc: 30 microtesla hướng bắc và 40 microtesla hướng đông, tổng hợp 50 microtesla lệch 53 độ",
            b, "Hình 6. Kim chỉ theo vectơ tổng hợp $B = 50\\ \\mu\\text{T}$, lệch $53^\\circ$.")

# ------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3 + fig3b, fig4, fig5), 1):
    moc = f"<!--FIG{n}-->"
    assert moc in src, f"thiếu mốc FIG{n}"
    src = src.replace(moc, f)
open("theory.html", "w", encoding="utf8").write(margin_figs(src))
print("ok", len(src), "bytes")
