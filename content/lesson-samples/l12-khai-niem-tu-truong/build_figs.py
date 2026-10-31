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
# Đường sức thanh nam châm: mô hình hai "từ tích" ở hai đầu (N bên trái, S bên phải), TÍNH bằng RK4.
# Toạ độ toán (z sang phải, x lên trên); B ngoài nam châm đi từ N sang S.
def _B2(z, x, d=2.0):
    bz = bx = 0.0
    for zc, q in ((-d, 1.0), (d, -1.0)):
        dz, dx = z - zc, x
        r3 = (dz * dz + dx * dx) ** 1.5 + 1e-12
        bz += q * dz / r3; bx += q * dx / r3
    return bz, bx


def duong_suc2(phi, d=2.0, h=0.02, maxn=6000, lim=30.0):
    """Đường sức rời cực N (z=-d) theo góc phi (độ, đo từ +z, x>0); dừng khi tới cực S hoặc ra xa."""
    import math as m
    e = 0.12
    z, x = -d + e * m.cos(m.radians(phi)), e * m.sin(m.radians(phi))
    pts = [(z, x)]
    def f(z, x):
        a, b = _B2(z, x, d); n = m.hypot(a, b) + 1e-12
        return a / n, b / n
    for _ in range(maxn):
        k1 = f(z, x); k2 = f(z + h / 2 * k1[0], x + h / 2 * k1[1])
        k3 = f(z + h / 2 * k2[0], x + h / 2 * k2[1]); k4 = f(z + h * k3[0], x + h * k3[1])
        z += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); x += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        pts.append((z, x))
        if m.hypot(z - d, x) < e or abs(z) > lim or abs(x) > lim:
            break
    return pts


def _bar_lines(cx, cy, s, phis, mirror=True):
    """Trả danh sách polyline (toạ độ màn hình) + điểm cao nhất kèm hướng B tại đó."""
    out = []
    for phi in phis:
        P = duong_suc2(phi)
        for sg in ((1, -1) if mirror else (1,)):
            Q = [(cx + s * z, cy - sg * s * x) for z, x in P]
            i = min(range(len(Q)), key=lambda k: Q[k][1]) if sg == 1 else max(range(len(Q)), key=lambda k: Q[k][1])
            i = max(1, min(i, len(Q) - 2))
            out.append((Q, Q[i], (Q[i + 1][0] - Q[i - 1][0], Q[i + 1][1] - Q[i - 1][1])))
    return out


def _poly(Q, c, w, dash, op=1):
    K = [Q[0]]
    for p in Q[1:-1]:                      # thưa điểm: cách nhau ≥ 4 px cho HTML gọn
        if (p[0] - K[-1][0]) ** 2 + (p[1] - K[-1][1]) ** 2 >= 16:
            K.append(p)
    K.append(Q[-1])
    d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in K)
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-dasharray="{dash}" opacity="{op}" stroke-linecap="round"/>'


UM_BODY, UM_DARK, UM_EDGE = "#cbd5e1", "#94a3b8", "#334155"   # cùng bảng màu nam châm chữ U (bài 11 u_magnet)
UM_N = ("#dc2626", "#f87171", "#b91c1c")      # mặt trước, mặt trên, mặt bên
UM_S = ("#2563eb", "#60a5fa", "#1e40af")


def bar_magnet(cx, cy, L, H, d=(10, -7), fs=17, sw=2, n_left=True):
    """Nam châm thẳng nhìn chính diện hơi xiên (chiều sâu dời d=(dx, dy) lên-phải); tâm mặt trước (cx, cy),
    dài L, cao H. Nửa trái N đỏ, nửa phải S xanh (n_left=False thì đảo); chữ trắng 800 cỡ fs. Trả SVG."""
    dx, dy = d
    x0, x1, y0, y1, xm = cx - L / 2, cx + L / 2, cy - H / 2, cy + H / 2, cx
    CL, CR = (UM_N, UM_S) if n_left else (UM_S, UM_N)
    P = lambda pts, f: f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="{f}" stroke="{UM_EDGE}" stroke-width="{sw}" stroke-linejoin="round"/>'
    o = P([(x0, y0), (xm, y0), (xm + dx, y0 + dy), (x0 + dx, y0 + dy)], CL[1])          # mặt trên nửa trái
    o += P([(xm, y0), (x1, y0), (x1 + dx, y0 + dy), (xm + dx, y0 + dy)], CR[1])         # mặt trên nửa phải
    o += P([(x1, y0), (x1 + dx, y0 + dy), (x1 + dx, y1 + dy), (x1, y1)], CR[2])         # mặt bên phải
    o += (f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{L/2:.1f}" height="{H:.1f}" fill="{CL[0]}" stroke="{UM_EDGE}" stroke-width="{sw}"/>'
          f'<rect x="{xm:.1f}" y="{y0:.1f}" width="{L/2:.1f}" height="{H:.1f}" fill="{CR[0]}" stroke="{UM_EDGE}" stroke-width="{sw}"/>')
    lt, rt = ("N", "S") if n_left else ("S", "N")
    o += text(round(x0 + L / 4, 1), round(cy + fs * .36, 1), lt, "#fff", fs, "middle", "800")
    o += text(round(x1 - L / 4, 1), round(cy + fs * .36, 1), rt, "#fff", fs, "middle", "800")
    return o


# Bộ đường sức chung cho khung ii và iii (mô hình hai từ tích ở ±2 đơn vị, 30 px/đơn vị → cách nhau 120 px,
# sát hai đầu thân dài 128 px). Góc rời cực N: đường càng gần trục càng mau ở hai cực.
BAR_L, BAR_H, BAR_D, BAR_S, BAR_PHI = 128, 26, (8, -6), 30, (40, 52, 64, 76)


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


def _bo_duong(cx, cy, kieu):
    """kieu='mat_sat': vạch ngắn xám (từ phổ); 'quy_uoc': nét đứt xanh lục + đầu V giữa đường (chiều N → S)."""
    g = ""
    for k, (Q, tip, dr) in enumerate(_bar_lines(cx, cy, BAR_S, BAR_PHI)):
        if kieu == "mat_sat":
            g += _poly(Q, "currentColor", 2.4, "3 4", .75)
        else:
            # đầu V so le theo x (0, −26, +22, −44 px quanh tâm; đường trong cùng ở đỉnh cho xa mặt trên thân) để không dồn thành một cột; đặt đúng điểm trên đường
            xt = cx + (0, -26, 22, -44)[k // 2]
            i = min((j for j in range(1, len(Q) - 1) if (Q[j][1] - cy) * (tip[1] - cy) > 0), key=lambda j: abs(Q[j][0] - xt))
            g += _poly(Q, GRN, 1.8, "6 4") + chevron(Q[i][0], Q[i][1], Q[i + 1][0] - Q[i - 1][0], Q[i + 1][1] - Q[i - 1][1], GRN, 1.8, 9)
    xl, xr = cx - BAR_L / 2, cx + BAR_L / 2 + BAR_D[0]
    if kieu == "mat_sat":
        g += f'<line x1="0" y1="{cy}" x2="{xl-4}" y2="{cy}" stroke="currentColor" stroke-width="2.4" stroke-dasharray="3 4" opacity=".75"/>'
        g += f'<line x1="{xr+4}" y1="{cy}" x2="440" y2="{cy}" stroke="currentColor" stroke-width="2.4" stroke-dasharray="3 4" opacity=".75"/>'
    else:
        g += field_line(xl - 4, cy, cx - 133, cy, GRN, 1.8, "6 4", 9)      # trục bên trái: ra xa N
        g += field_line(cx + 133, cy, xr + 4, cy, GRN, 1.8, "6 4", 9)      # trục bên phải: đi vào S
    return g


# ii) từ phổ: mạt sắt xếp dọc đúng bộ đường của khung iii
b += text(14, 162, "ii) Từ phổ (mạt sắt)", "currentColor", 14, "start", "700")
b += f'<clipPath id="f3-c2"><rect x="14" y="172" width="276" height="186" rx="6"/></clipPath>'
b += rect(14, 172, 276, 186, "rgba(148,163,184,.08)", "currentColor", 1.2, 6)
b += f'<g clip-path="url(#f3-c2)">{_bo_duong(152, 265, "mat_sat")}</g>' + bar_magnet(152, 265, BAR_L, BAR_H, BAR_D)
b += text(302, 258, "mạt sắt dày", "currentColor", 14, "start", "600")
b += text(302, 278, "ở hai cực", "currentColor", 14, "start", "600")
# iii) đường sức vẽ theo quy ước: cùng bộ đường, nét đứt, có chiều
b += text(14, 382, "iii) Đường sức quy ước", "currentColor", 14, "start", "700")
b += f'<clipPath id="f3-c3"><rect x="14" y="392" width="276" height="186" rx="6"/></clipPath>'
b += rect(14, 392, 276, 186, "rgba(148,163,184,.08)", "currentColor", 1.2, 6)
b += f'<g clip-path="url(#f3-c3)">{_bo_duong(152, 485, "quy_uoc")}</g>' + bar_magnet(152, 485, BAR_L, BAR_H, BAR_D)
b += text(302, 446, "ra ở N, vào ở S", "currentColor", 14, "start", "600")
b += text(302, 470, "khép kín", "currentColor", 14, "start", "600")
b += text(302, 494, "không cắt nhau", "currentColor", 14, "start", "600")
b += text(302, 518, "gần cực: mau", "currentColor", 14, "start", "600")
fig3b = wrap("0 0 440 592",
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
