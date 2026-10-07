"""Sinh 5 hình SVG cho bài "Bài 9. Khái niệm từ trường" (Vật lí 12) và thay các mốc
<!--FIGn--> trong theory.src.html -> theory.html. Chạy từ thư mục này: python3 build_figs.py
"""
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
b += text(72, 91, "N", RED, 12, "middle", "700")
b += text(72, 199, "S", BLUE, 12, "middle", "700")
b += text(84, 238, "la bàn trong máy", "currentColor", 10, "start", "500")
b += text(150, 132, "kim chỉ bắc", RED, 12, "start", "700")
b += text(150, 158, "dù xoay máy", "currentColor", 11, "start", "500")
b += line(150, 140, 268, 140, RED, 2.4)
b += arrow("f1", "r", 268, 140, 300, 140, 2.6)
b += rect(316, 62, 108, 84, "rgba(52,211,153,.14)", GRN, 1.8, 10)
b += text(370, 92, "cạnh cửa sắt", GRN, 12, "middle", "700")
b += text(370, 112, "kim lệch hẳn", GRN, 11, "middle", "500")
b += text(370, 132, "khỏi hướng bắc", GRN, 11, "middle", "500")
b += line(300, 140, 316, 122, "currentColor", 1.2, "5 4", .7)
fig1 = wrap("0 0 440 252",
            "Điện thoại có la bàn: kim chỉ về phía bắc dù xoay máy; đặt cạnh cửa sắt thì kim lệch hẳn",
            b, "Hình 1. La bàn chỉ một phía; gần cửa sắt thì kim lệch.")

# ------------------------------------------- Hình 2: hút – đẩy giữa hai nam châm
b = defs("f2")
b += text(14, 22, "a) Khác tên: hút nhau", "currentColor", 12, "start", "700")
b += rect(24, 44, 78, 42, "rgba(248,113,113,.16)", RED, 2, 6)
b += rect(102, 44, 78, 42, "rgba(56,189,248,.16)", BLUE, 2, 6)
b += text(63, 71, "N", RED, 15, "middle", "700")
b += text(141, 71, "S", BLUE, 15, "middle", "700")
b += arrow("f2", "r", 84, 65, 106, 65, 2.4)
b += arrow("f2", "b", 120, 65, 98, 65, 2.4)
b += text(24, 106, "hút", GRN, 11, "start", "700")
b += text(230, 22, "b) Cùng tên: đẩy nhau", "currentColor", 12, "start", "700")
b += rect(240, 44, 78, 42, "rgba(248,113,113,.16)", RED, 2, 6)
b += rect(318, 44, 78, 42, "rgba(248,113,113,.16)", RED, 2, 6)
b += text(279, 71, "N", RED, 15, "middle", "700")
b += text(357, 71, "N", RED, 15, "middle", "700")
b += arrow("f2", "r", 316, 65, 292, 65, 2.4)
b += arrow("f2", "r", 320, 65, 344, 65, 2.4)
b += text(240, 106, "đẩy", RED, 11, "start", "700")
b += line(14, 122, 426, 122, "currentColor", 1.2, "6 5", .35)
b += text(14, 150, "Dòng điện cũng có từ tính", "currentColor", 11, "start", "700")
fig2 = wrap("0 0 440 168",
            "Hai nam châm: khác tên hút nhau, cùng tên đẩy nhau; dòng điện cũng có tương tác từ",
            b, "Hình 2. Khác cực hút, cùng cực đẩy; dòng điện cũng có từ tính.")

# ------------------------------------------- Hình 3: bốn khung đường sức từ
b = defs("f3")
# a) thanh nam châm — N bên trái, S bên phải
b += text(14, 20, "a) Thanh nam châm", "currentColor", 11, "start", "700")
b += rect(44, 72, 68, 30, "rgba(248,113,113,.18)", RED, 2, 4)
b += rect(112, 72, 68, 30, "rgba(56,189,248,.18)", BLUE, 2, 4)
b += text(78, 93, "N", RED, 13, "middle", "700")
b += text(146, 93, "S", BLUE, 13, "middle", "700")
b += f'<path d="M78,72 C78,42 146,42 146,72" fill="none" stroke="{RED}" stroke-width="1.8" stroke-dasharray="6 4"/>'
b += f'<path d="M78,102 C78,132 146,132 146,102" fill="none" stroke="{RED}" stroke-width="1.8" stroke-dasharray="6 4"/>'
b += f'<path d="M44,87 C14,87 20,34 112,34 C204,34 210,87 180,87" fill="none" stroke="{RED}" stroke-width="1.8" stroke-dasharray="6 4"/>'
b += f'<path d="M44,87 C14,87 20,140 112,140 C204,140 210,87 180,87" fill="none" stroke="{RED}" stroke-width="1.8" stroke-dasharray="6 4"/>'
b += chevron(118, 49, 18.0, -1.0, RED, 1.8, 10)
b += chevron(126, 124, 18.0, -1.0, RED, 1.8, 10)
b += chevron(124, 34, 24.0, 0.0, RED, 1.8, 10)
b += chevron(124, 140, 24.0, 0.0, RED, 1.8, 10)
def _bz(P, t):
    u = 1 - t
    return tuple(u**3*P[0][k] + 3*u*u*t*P[1][k] + 3*u*t*t*P[2][k] + t**3*P[3][k] for k in (0, 1))
for P in (((112, 34), (204, 34), (210, 87), (180, 87)), ((112, 140), (204, 140), (210, 87), (180, 87))):
    a, c = _bz(P, 0.66), _bz(P, 0.74)
    b += chevron(round(c[0], 1), round(c[1], 1), c[0] - a[0], c[1] - a[1], RED, 1.8, 10)
b += text(14, 166, "ra ở bắc, vào ở nam", "currentColor", 10, "start", "500")
# b) nam châm chữ U — N bên trái, S bên phải (đường sức giữa hai cực đi từ N sang S)
b += text(232, 20, "b) Chữ U", "currentColor", 11, "start", "700")
b += f'<path d="M244,50 L244,64 Q244,84 264,84 L316,84 Q336,84 336,64 L336,50" fill="none" stroke="currentColor" stroke-width="5"/>'
b += text(242, 44, "N", RED, 12, "start", "700")
b += text(338, 44, "S", BLUE, 12, "end", "700")
for y in (52, 64, 76):
    b += field_line(268, y, 312, y, BLUE, 1.8, "5 3", 7)
b += text(232, 114, "song song, cách đều", GRN, 10, "start", "600")
b += text(232, 129, "→ từ trường đều", GRN, 10, "start", "600")
# c) từ phổ mạt sắt
b += text(14, 186, "c) Từ phổ", "currentColor", 11, "start", "700")
b += rect(18, 196, 136, 62, "rgba(148,163,184,.08)", "currentColor", 1.2, 6)
b += f'<path d="M24,202 C54,252 112,252 148,198" fill="none" stroke="{GRN}" stroke-width="1.6" stroke-dasharray="2 3"/>'
b += f'<path d="M20,218 C50,256 116,256 152,194" fill="none" stroke="{GRN}" stroke-width="1.6" stroke-dasharray="2 3"/>'
b += f'<path d="M20,238 C50,262 116,262 152,198" fill="none" stroke="{GRN}" stroke-width="1.6" stroke-dasharray="2 3"/>'
b += f'<ellipse cx="86" cy="226" rx="6" ry="15" fill="{RED}" stroke="currentColor" stroke-width="1"/>'
b += text(86, 274, "ảnh thật", "currentColor", 10, "middle", "500")
# d) đường vẽ theo quy ước
b += text(232, 186, "d) Đường quy ước", "currentColor", 11, "start", "700")
b += rect(236, 196, 190, 62, "rgba(148,163,184,.08)", "currentColor", 1.2, 6)
b += f'<path d="M248,254 C280,198 384,198 414,254" fill="none" stroke="{RED}" stroke-width="1.6" stroke-dasharray="6 4"/>'
b += f'<path d="M250,242 C288,204 374,204 412,242" fill="none" stroke="{RED}" stroke-width="1.6" stroke-dasharray="6 4"/>'
b += f'<path d="M256,208 L408,208" fill="none" stroke="{RED}" stroke-width="1.6" stroke-dasharray="6 4"/>'
b += chevron(308, 215, 30.0, -9.0, RED, 1.8, 10)
b += chevron(366, 208, 22.0, 0.0, RED, 1.8, 10)
b += text(236, 274, "mũi tên chỉ chiều", "currentColor", 10, "start", "500")
b += text(236, 286, "không cắt nhau", "currentColor", 10, "start", "500")
fig3 = wrap("0 0 440 296",
            "Bốn khung: đường sức từ của thanh nam châm, của nam châm chữ U (từ trường đều), từ phổ mạt sắt và đường sức vẽ theo quy ước",
            b, "Hình 3.<br>a) Đường sức thanh nam châm: ra ở bắc, vào ở nam, khép kín.<br>b) Chữ U: từ trường đều.<br>"
               "c) Từ phổ.<br>d) Đường vẽ theo quy ước.")

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
            b, "Hình 4. Gần bắc địa lí là <strong>cực từ nam</strong>, nên cực bắc của kim bị hút về đó.")

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
b += text(264, 216, "B3 = 40 µT", RED, 12, "middle", "700")
b += arrow("f5", "b", 224, 196, 304, 136, 3)
b += text(312, 130, "B = 50 µT", BLUE, 12, "start", "700")
b += line(304, 136, 304, 196, "currentColor", 1.2, "5 4", .45)
b += line(304, 136, 224, 136, "currentColor", 1.2, "5 4", .45)
b += f'<path d="M224,151 A45,45 0 0,1 260,169" fill="none" stroke="currentColor" stroke-width="1.4"/>'
b += text(250, 146, "53°", "currentColor", 12, "start", "700")
b += text(44, 250, "Kim chỉ theo vectơ tổng hợp.", "currentColor", 11, "start", "600")
fig5 = wrap("0 0 440 268",
            "Hai từ trường thành phần vuông góc: 30 microtesla hướng bắc và 40 microtesla hướng đông, tổng hợp 50 microtesla lệch 53 độ",
            b, "Hình 5. Kim chỉ theo vectơ tổng hợp $B = 50\\ \\mu\\text{T}$, lệch $53^\\circ$.")

# ------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4, fig5), 1):
    moc = f"<!--FIG{n}-->"
    assert moc in src, f"thiếu mốc FIG{n}"
    src = src.replace(moc, f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
