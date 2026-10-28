"""Sinh 5 hình SVG cho bài "Bài 9. Khái niệm từ trường" (Vật lí 12) và thay các mốc
<!--FIGn--> trong theory.src.html -> theory.html. Chạy từ thư mục này: python3 build_figs.py
"""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *  # noqa: E402


# ------------------------------------------- đường sức nam châm thanh: TÍNH bằng Biot-Savart
# Nam châm thanh = ống dây hữu hạn (dài 5a, bán kính a) — mô hình chuẩn của vật liệu từ hoá đều; B trong lõi hướng về cực N (bên trái).
_A, _HL = 1.0, 2.5
_Z = np.linspace(-_HL, _HL, 51)
_P = np.linspace(0, 2 * np.pi, 120, endpoint=False)


_CX, _SX = np.cos(_P), np.sin(_P)
_DL = np.stack([-_SX, _CX, np.zeros_like(_CX)], 1) * (2 * np.pi / len(_P)) * _A
_R = np.stack([np.repeat(_A * _CX[None, :], len(_Z), 0), np.repeat(_A * _SX[None, :], len(_Z), 0),
               np.repeat(_Z[:, None], len(_P), 1)], 2).reshape(-1, 3)
_DLALL = np.tile(_DL, (len(_Z), 1))


def _B(x, z):
    d = np.array([x, 0.0, z]) - _R
    c = np.cross(_DLALL, d) / (np.linalg.norm(d, axis=1) ** 3 + 1e-9)[:, None]
    return -c[:, 0].sum(), -c[:, 2].sum()


def duong_suc(x0, h=0.03, maxn=1500):
    """Đường sức đi qua điểm (z=0, x=x0), theo chiều B; trả về mảng (z, x) khép kín (trong lõi: về N; ngoài: từ N sang S)."""
    def f(x, z):
        a, b = _B(x, z)
        n = np.hypot(a, b) + 1e-12
        return a / n, b / n
    x, z = x0, 0.0
    pts = [(z, x)]
    for i in range(maxn):
        k1 = f(x, z); k2 = f(x + h / 2 * k1[0], z + h / 2 * k1[1])
        k3 = f(x + h / 2 * k2[0], z + h / 2 * k2[1]); k4 = f(x + h * k3[0], z + h * k3[1])
        x += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        z += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        pts.append((z, x))
        if i > 40 and np.hypot(z, x - x0) < h * 1.2:
            break
        if abs(x) > 12 or abs(z) > 14:
            break
    return np.array(pts)


def _px(L, cx, cy, s):
    return [(cx + s * z, cy + s * x) for z, x in L]   # z -> sang phải (N bên trái), x -> xuống dưới (hình)


def _chev_tai(P, i, c, w=1.8, L=10):
    i = max(1, min(i, len(P) - 2))
    return chevron(P[i][0], P[i][1], P[i + 1][0] - P[i - 1][0], P[i + 1][1] - P[i - 1][1], c, w, L)


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

# ------------------------------------------- Hình 3 (OpenStax, đầu hàm) + Hình 4: ba khung đường sức còn lại (SVG)
b = defs("f3")
# b) nam châm chữ U — N bên trái, S bên phải (đường sức giữa hai cực đi từ N sang S)
b += '<g transform="translate(-218,0)">'
b += text(232, 20, "i) Chữ U", "currentColor", 14, "start", "700")
b += f'<path d="M244,50 L244,64 Q244,84 264,84 L316,84 Q336,84 336,64 L336,50" fill="none" stroke="currentColor" stroke-width="5"/>'
b += text(242, 44, "N", RED, 14, "start", "700")
b += text(338, 44, "S", BLUE, 14, "end", "700")
for y in (52, 64, 76):
    b += field_line(268, y, 312, y, BLUE, 1.8, "5 3", 7)
b += text(232, 116, "song song, cách đều", GRN, 14, "start", "600")
b += text(232, 133, "→ từ trường đều", GRN, 14, "start", "600")
b += "</g>"
# c) từ phổ mạt sắt
b += '<g transform="translate(218,-150)">'
b += text(14, 186, "ii) Từ phổ", "currentColor", 14, "start", "700")
b += rect(18, 196, 136, 62, "rgba(148,163,184,.08)", "currentColor", 1.2, 6)
F = 'fill="none" stroke="{}" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="0.1 5"'.format(GRN)
b += rect(60, 223, 52, 10, "rgba(248,113,113,.2)", "currentColor", 1.2, 2)
for k in (0, 1):
    h = 18 + 8 * k
    b += f'<path d="M60,228 C{36-8*k},228 {36-8*k},{228-h} 86,{228-h} C{136+8*k},{228-h} {136+8*k},228 112,228" {F}/>'
    b += f'<path d="M60,228 C{36-8*k},228 {36-8*k},{228+h} 86,{228+h} C{136+8*k},{228+h} {136+8*k},228 112,228" {F}/>'
b += f'<path d="M58,228 L24,228" {F}/>'
b += f'<path d="M114,228 L148,228" {F}/>'
b += text(86, 276, "mạt sắt dày ở hai cực", "currentColor", 14, "middle", "500")
b += "</g>"
b += '<g transform="translate(-118,18)">'
# d) đường vẽ theo quy ước
b += text(232, 186, "iii) Đường quy ước", "currentColor", 14, "start", "700")
b += rect(236, 196, 190, 62, "rgba(148,163,184,.08)", "currentColor", 1.2, 6)
b += f'<path d="M248,254 C280,198 384,198 414,254" fill="none" stroke="{RED}" stroke-width="1.6" stroke-dasharray="6 4"/>'
b += f'<path d="M250,242 C288,204 374,204 412,242" fill="none" stroke="{RED}" stroke-width="1.6" stroke-dasharray="6 4"/>'
b += f'<path d="M256,208 L408,208" fill="none" stroke="{RED}" stroke-width="1.6" stroke-dasharray="6 4"/>'
b += chevron(308, 215, 30.0, -9.0, RED, 1.8, 10)
b += chevron(366, 208, 22.0, 0.0, RED, 1.8, 10)
b += text(236, 276, "mũi tên chỉ chiều", "currentColor", 14, "start", "500")
b += text(236, 294, "không cắt nhau", "currentColor", 14, "start", "500")
b += "</g>"
fig3b = wrap("0 0 440 322",
            "Ba khung: đường sức từ của nam châm chữ U (từ trường đều), từ phổ mạt sắt và đường sức vẽ theo quy ước",
            b, "Hình 4.<br>i) Chữ U: từ trường đều.<br>ii) Từ phổ.<br>iii) Đường quy ước.")
fig3 = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l12-khai-niem-tu-truong/hinh-duong-suc-thanh-nam-cham.webp" '
        'alt="Thanh nam châm thẳng: a) kim la bàn đặt quanh nam châm chỉ theo từ trường; b) và c) đường sức đi ra ở cực bắc, vào ở cực nam, đường c khép kín qua thân nam châm" '
        'loading="lazy" width="1000" height="344" style="display:block;margin:0 auto;max-width:100%;height:auto;border-radius:8px">'
        '<figcaption>Hình 3. Đường sức khép kín.<br>'
        
        '<small>Hình: OpenStax, <em>College Physics 2e</em>, Hình 22.14 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>')

# ------------------------------------------- Hình 4: từ trường Trái Đất
b = defs("f4")
CX = 190
b += f'<circle cx="{CX}" cy="150" r="96" fill="rgba(56,189,248,.10)" stroke="currentColor" stroke-width="2"/>'
b += line(CX, 54, CX, 246, "currentColor", 1.2, "6 5", .5)
b += text(CX, 34, "Bắc", "currentColor", 12, "middle", "700")
b += text(CX, 276, "Nam", "currentColor", 12, "middle", "700")
b += line(CX, 62, CX, 238, "currentColor", 4)
b += f'<path d="M{CX},62 L{CX-8},78 L{CX+8},78 z" fill="{BLUE}"/>'
b += f'<path d="M{CX},238 L{CX-8},222 L{CX+8},222 z" fill="{RED}"/>'
b += text(CX + 12, 98, "cực từ", BLUE, 12, "start", "700")
b += text(CX + 12, 113, "nam", BLUE, 12, "start", "700")
b += text(CX - 12, 200, "cực từ", RED, 12, "end", "700")
b += text(CX - 12, 215, "bắc", RED, 12, "end", "700")
for dx in (150, 230):
    for sg in (1, -1):
        b += f'<path d="M{CX},238 C{CX+sg*dx},262 {CX+sg*dx},38 {CX},62" fill="none" stroke="{GRN}" stroke-width="1.8" stroke-dasharray="6 4"/>'
        xm = CX + sg * dx * 0.75
        b += chevron(xm, 138, 0, -1, GRN, 1.8, 10)
b += f'<g transform="translate(408,150) rotate(-80)"><rect x="-20" y="-7" width="40" height="14" rx="7" fill="{RED}"/><rect x="-20" y="-7" width="20" height="14" rx="7" fill="{BLUE}"/><path d="M20,0 L6,-7 L6,7 z" fill="{RED}"/></g>'
b += text(408, 108, "kim la bàn", "currentColor", 12, "middle", "700")
b += text(408, 196, "nằm theo", GRN, 12, "middle", "600")
b += text(408, 211, "đường sức", GRN, 12, "middle", "600")
b += line(390, 150, CX + 230 * 0.75 + 4, 150, GRN, 1.4, "5 4", .8)
b += text(14, 18, "đường sức", GRN, 12, "start", "600")
b += text(14, 33, "vào cực từ nam", GRN, 12, "start", "600")
fig4 = wrap("0 0 440 296",
            "Trái Đất như một nam châm khổng lồ: gần bắc địa lí là cực từ nam, đường sức đi vào đó; kim la bàn nằm theo đường sức",
            b, "Hình 5. Gần bắc địa lí là <strong>cực từ nam</strong>, nên cực bắc của kim bị hút về đó.")

# ------------------------------------------- Hình 5: hai từ trường vuông góc
b = defs("f5")
b += line(44, 196, 404, 196, "currentColor", 1.6)
b += line(224, 196, 224, 40, "currentColor", 1.6)
b += text(400, 214, "đông", "currentColor", 11, "end", "600")
b += text(224, 32, "bắc", "currentColor", 11, "middle", "600")
b += f'<circle cx="224" cy="196" r="7" fill="currentColor"/>'
# tỉ lệ chung 2 px cho mỗi µT: 30 µT → 60 px, 40 µT → 80 px, 50 µT → 100 px lệch 53° so với bắc
b += arrow("f5", "g", 224, 196, 224, 136, 3)
b += text(216, 140, "Bđ = 30 µT", GRN, 12, "end", "700")
b += arrow("f5", "r", 224, 196, 304, 196, 3)
b += text(264, 216, "B1 = 40 µT", RED, 12, "middle", "700")
b += arrow("f5", "b", 224, 196, 304, 136, 3)
b += text(312, 130, "B = 50 µT", BLUE, 12, "start", "700")
b += line(304, 136, 304, 196, "currentColor", 1.2, "5 4", .45)
b += line(304, 136, 224, 136, "currentColor", 1.2, "5 4", .45)
b += f'<path d="M224,151 A45,45 0 0,1 260,169" fill="none" stroke="currentColor" stroke-width="1.4"/>'
b += text(250, 146, "53°", "currentColor", 12, "start", "700")
b += text(44, 250, "Kim chỉ theo vectơ tổng hợp.", "currentColor", 11, "start", "600")
fig5 = wrap("0 0 440 268",
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
