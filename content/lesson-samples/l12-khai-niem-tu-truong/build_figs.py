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


def _bar(cx, cy, hl, hw=7):
    return (f'<rect x="{cx-hl}" y="{cy-hw}" width="{hl}" height="{2*hw}" fill="{RED}" stroke="currentColor" stroke-width="1.2"/>'
            f'<rect x="{cx}" y="{cy-hw}" width="{hl}" height="{2*hw}" fill="{BLUE}" stroke="currentColor" stroke-width="1.2"/>')


b = defs("f3")
# i) nam châm chữ U: N trái (đỏ), S phải (xanh); đường sức giữa hai cực thẳng, song song, cách đều, chiều N → S
b += text(14, 20, "i) Chữ U", "currentColor", 14, "start", "700")
b += f'<path d="M44,44 L44,100 Q44,124 68,124 L142,124 Q166,124 166,100 L166,44" fill="none" stroke="currentColor" stroke-width="14" opacity=".35"/>'
b += rect(36, 44, 16, 38, RED, "currentColor", 1.2, 2)
b += rect(158, 44, 16, 38, BLUE, "currentColor", 1.2, 2)
b += text(44, 38, "N", RED, 14, "middle", "700")
b += text(166, 38, "S", BLUE, 14, "middle", "700")
for y in (51, 63, 75):
    b += field_line(56, y, 154, y, GRN, 1.8, "5 3", 9)
b += text(14, 148, "song song, cách đều", GRN, 14, "start", "600")
b += text(14, 167, "→ từ trường đều", GRN, 14, "start", "600")
# ii) từ phổ: mạt sắt rắc quanh thanh nam châm, xếp theo đường sức (vạch ngắn, không mũi tên)
b += text(232, 20, "ii) Từ phổ", "currentColor", 14, "start", "700")
b += f'<clipPath id="f3-c2"><rect x="230" y="36" width="200" height="98" rx="6"/></clipPath>'
b += rect(230, 36, 200, 98, "rgba(148,163,184,.08)", "currentColor", 1.2, 6)
g = ""
for Q, _, _ in _bar_lines(330, 85, 12, (25, 45, 65, 85, 105, 125, 145)):
    g += _poly(Q, "currentColor", 2.2, "2 4", .7)
g += f'<line x1="230" y1="85" x2="430" y2="85" stroke="currentColor" stroke-width="2.2" stroke-dasharray="2 4" opacity=".7"/>'
b += f'<g clip-path="url(#f3-c2)">{g}</g>' + _bar(330, 85, 29)
b += text(232, 156, "mạt sắt dày ở hai cực", "currentColor", 14, "start", "500")
# iii) đường sức vẽ theo quy ước: nét đứt, có chiều (ra ở N, vào ở S), không cắt nhau
b += text(14, 200, "iii) Đường sức quy ước", "currentColor", 14, "start", "700")
b += f'<clipPath id="f3-c3"><rect x="14" y="212" width="266" height="112" rx="6"/></clipPath>'
b += rect(14, 212, 266, 112, "rgba(148,163,184,.08)", "currentColor", 1.2, 6)
g = ""
for Q, tip, dr in _bar_lines(147, 268, 15, (35, 70, 115)):
    g += _poly(Q, GRN, 1.8, "6 4") + chevron(tip[0], tip[1], dr[0], dr[1], GRN, 1.8, 9)
g += field_line(110, 268, 24, 268, GRN, 1.8, "6 4", 9)      # trục, bên trái N: B hướng ra xa N
g += field_line(276, 268, 186, 268, GRN, 1.8, "6 4", 9)     # trục, bên phải S: B hướng vào S
b += f'<g clip-path="url(#f3-c3)">{g}</g>' + _bar(147, 268, 36)
b += text(129, 273, "N", "#fff", 14, "middle", "700") + text(165, 273, "S", "#fff", 14, "middle", "700")
b += text(292, 246, "ra ở N, vào ở S", "currentColor", 14, "start", "500")
b += text(292, 272, "không cắt nhau", "currentColor", 14, "start", "500")
b += text(292, 298, "gần cực: mau", "currentColor", 14, "start", "500")
fig3b = wrap("0 0 440 336",
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
for L in (1.35 * RE, 2.1 * RE, 3.4 * RE):
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
b += f'<text x="{OX-8}" y="{OY-K*30+6}" fill="{GRN}" font-size="14" font-weight="700" text-anchor="end">B<tspan font-size="14" baseline-shift="sub">đ</tspan> = 30 µT</text>'
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
