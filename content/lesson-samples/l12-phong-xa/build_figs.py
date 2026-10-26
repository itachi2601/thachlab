"""Sinh 4 hình SVG cho bài "Bài 17. Hiện tượng phóng xạ" (Vật lí 12) và thay các mốc
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


def dot(x, y, r=4, c="currentColor"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def rect(x, y, w, h, fill, stroke="currentColor", sw=2, rx=8, op=1):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>')


def path(d, c, w=2.4, marker=""):
    m = f' marker-end="url(#{marker})"' if marker else ""
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}"{m}/>'


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">'
            f'{body}</svg><figcaption>{cap}</figcaption></figure>')


# ------------------------------------------------- Hình 1: nguồn phóng xạ và ống đếm
b = defs("f1")
b += text(14, 24, "Một nguồn phóng xạ và ống đếm", "currentColor", 12.5, "start", "700")
b += rect(24, 52, 100, 76, "rgba(148,163,184,.14)", "currentColor", 2, 8)          # hộp chì
b += rect(50, 76, 48, 28, "rgba(248,113,113,.35)", RED, 2, 5)                     # mẫu quặng
b += text(74, 148, "mẫu trong hộp chì", "currentColor", 10.5, "middle", "600")
b += arrow("f1", "r", 106, 92, 202, 82, 2.2, "6 4")
b += text(164, 66, "tia α, β, γ", RED, 11, "middle", "700")
b += rect(210, 56, 92, 48, "rgba(56,189,248,.15)", BLUE, 2, 10)                   # ống đếm
b += text(256, 78, "ống đếm", BLUE, 11, "middle", "700")
b += text(256, 93, "Geiger", BLUE, 11, "middle", "700")
b += text(256, 124, "≈ 500 xung/phút", "currentColor", 11, "middle", "600")
fig1 = wrap("0 0 440 200",
            "Mẫu quặng phóng xạ trong hộp chì bắn tia vào ống đếm Geiger, máy đếm khoảng 500 xung mỗi phút",
            b, "Hình 1. Mẫu phóng xạ trong hộp chì bắn tia sang ống đếm Geiger.")

# ------------------------------------------------- Hình 2: ba chùm tia trong điện trường
b = defs("f2")
b += text(14, 20, "Ba chùm tia trong điện trường đều", "currentColor", 12.5, "start", "700")
b += rect(70, 48, 260, 10, "rgba(148,163,184,.22)", "currentColor", 1.2, 2)        # bản dương
b += text(74, 42, "+ bản dương", "currentColor", 10.5, "start", "600")
b += rect(70, 200, 260, 10, "rgba(148,163,184,.22)", "currentColor", 1.2, 2)       # bản âm
b += text(74, 228, "− bản âm", "currentColor", 10.5, "start", "600")
b += dot(26, 129, 7, "currentColor")
b += text(26, 152, "nguồn", "currentColor", 10.5, "middle", "600")
b += line(33, 129, 70, 129, "currentColor", 2)
b += arrow("f2", "g", 74, 129, 380, 129, 2.2)
b += text(388, 133, "γ", GRN, 13, "start", "700")
b += path("M70,129 Q220,129 318,68", BLUE, 2.4, "f2-b")
b += text(334, 62, "β⁻", BLUE, 13, "start", "700")
b += path("M70,129 Q220,129 318,190", RED, 2.4, "f2-r")
b += text(334, 196, "α", RED, 13, "start", "700")
b += text(14, 254, "α, β⁺ lệch về bản âm · β⁻ lệch về bản dương · γ đi thẳng", "currentColor", 11, "start", "600")
fig2 = wrap("0 0 440 270",
            "Ba chùm tia alpha, beta trừ và gamma bay vào điện trường đều: alpha lệch xuống bản âm, beta trừ lệch lên bản dương, gamma bay thẳng",
            b, "Hình 2. γ không mang điện nên bay thẳng; β⁺ nhẹ hơn α nên lệch nhiều hơn.")

# ------------------------------------------------- Hình 3: đường cong phân rã
X0, DX = 70, 85
Y0, DY = 190, 130


def rx(n):
    return X0 + DX * n


def ry(n):
    return Y0 - DY * (2 ** (-n))


b = defs("f3")
b += text(14, 22, "Số hạt nhân giảm một nửa sau mỗi chu kì T", "currentColor", 12.5, "start", "700")
b += line(X0, Y0, 410, Y0, "currentColor", 2)
b += line(X0, Y0, X0, 44, "currentColor", 2)
b += text(58, 40, "N", "currentColor", 12, "end", "700")
b += text(432, 207, "t", "currentColor", 12, "middle", "700")
pts = []
n = 0.0
while n <= 4.001:
    pts.append(f"{rx(n):.1f},{ry(n):.1f}")
    n += 0.2
b += f'<polyline fill="none" stroke="{GRN}" stroke-width="2.6" points="{" ".join(pts)}"/>'
for k in (1, 2, 3):
    b += line(rx(k), Y0, rx(k), ry(k), "currentColor", 1, "4 4", .35)
    b += line(X0, ry(k), rx(k), ry(k), "currentColor", 1, "4 4", .35)
for k in range(5):
    b += dot(rx(k), ry(k), 4, GRN)
for k, nhan in ((0, "N₀"), (1, "N₀/2"), (2, "N₀/4"), (3, "N₀/8")):
    b += text(64, ry(k) + 4, nhan, GRN, 10.5, "end", "700")
for k, nhan in ((0, "0"), (1, "T"), (2, "2T"), (3, "3T"), (4, "4T")):
    b += text(rx(k), 206, nhan, "currentColor", 11.5, "middle", "600")
b += text(248, 140, "mỗi T lại còn một nửa", GRN, 11, "start", "600")
# ảnh động bấm mới chạy: 16 hạt nhân phân rã NGẪU NHIÊN từng hạt (không biết hạt nào trước),
# nhưng cứ hết một T thì còn đúng một nửa (16 → 8 → 4 → 2 → 1); chấm chạy trên đường cong cùng nhịp.
import random
NA = 91
TS = [i / (NA - 1) for i in range(NA)]
def nT(t):
    return 4 * min(t / .9, 1.0)
rnd = random.Random(17)
thu_tu = list(range(16)); rnd.shuffle(thu_tu)
luc_ra = {}
i = 0
for k, so in ((1, 8), (2, 4), (3, 2), (4, 1)):
    for _ in range(so):
        luc_ra[thu_tu[i]] = rnd.uniform(k - 1 + .08, k - .08); i += 1
for j in range(16):
    gx, gy = 342 + 18 * (j % 4), 40 + 18 * (j // 4)
    tr = luc_ra.get(j, 99)
    b += (f'<circle cx="{gx}" cy="{gy}" r="6" fill="{GRN}">'
          + anim("opacity", [1.0 if nT(t) < tr else .15 for t in TS]) + '</circle>')
b += text(369, 117, "1 chấm = 1 hạt nhân", "currentColor", 10.5, "middle", "500")
b += (f'<g opacity="0">{anim("opacity", [1.0] * (NA - 1) + [0.0])}<g>'
      + anim_move([(rx(nT(t)) - X0, ry(nT(t)) - ry(0)) for t in TS])
      + f'<circle cx="{X0}" cy="{ry(0):.1f}" r="6" fill="none" stroke="{ORG}" stroke-width="3"/></g></g>')
fig3 = wrap("0 0 440 240",
            "Đường cong phân rã: số hạt nhân giảm còn một nửa sau mỗi chu kì bán rã T",
            b, "Hình 3. Sau mỗi khoảng T, số hạt nhân giảm một nửa.")
fig3 = nut_chay(fig3)

# ------------------------------------------------- Hình 4: dịch chuyển ô trong bảng tuần hoàn
b = defs("f4")
b += text(14, 22, "Hạt nhân con dịch chuyển trong bảng tuần hoàn", "currentColor", 12.5, "start", "700")
Z0 = 88
HANG = ((44, 4, 2, "α", "α: lùi 2 ô", RED, "f4-r"),
        (114, 2, 3, "β⁻", "β⁻: tiến 1 ô", BLUE, "f4-b"),
        (184, 3, 2, "β⁺", "β⁺: lùi 1 ô", ORG, "f4-o"))
for y, ip, ic, ten, nhan, col, mk in HANG:
    b += text(14, y + 21, ten, col, 12.5, "start", "700")
    for i in range(6):
        x = 40 + 48 * i
        if i == ip:
            b += rect(x, y, 44, 32, "rgba(248,113,113,.30)", RED, 2, 4)
            mau = RED
        elif i == ic:
            b += rect(x, y, 44, 32, "rgba(52,211,153,.30)", GRN, 2, 4)
            mau = GRN
        else:
            b += rect(x, y, 44, 32, "rgba(148,163,184,.08)", "currentColor", 1.2, 4)
            mau = "currentColor"
        b += text(x + 22, y + 21, str(Z0 + i), mau, 10.5, "middle", "600")
    b += arrow("f4", mk[-1], 40 + 48 * ip + 22, y + 44, 40 + 48 * ic + 22, y + 44, 2.2)
    b += text(262, y + 48, nhan, col, 11, "start", "700")
b += text(14, 256, "con số trong ô là Z (số proton); ô đỏ là hạt nhân mẹ, ô xanh là hạt nhân con", "currentColor", 10.5, "start", "500")
fig4 = wrap("0 0 440 265",
            "Ba hàng ô nguyên tố: phân rã alpha làm con lùi 2 ô, phân rã beta trừ làm con tiến 1 ô, phân rã beta cộng làm con lùi 1 ô",
            b, "Hình 4. Chỗ dịch chuyển của hạt nhân con: α lùi 2 ô, β⁻ tiến 1 ô, β⁺ lùi 1 ô; tia γ không đổi ô.")

# ------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
