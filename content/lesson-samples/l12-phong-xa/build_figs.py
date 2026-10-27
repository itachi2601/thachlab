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
b += text(14, 24, "Một nguồn phóng xạ và ống đếm", "currentColor", 14, "start", "700")
b += '<path d="M124,84 V52 H24 V128 H124 V100" fill="rgba(148,163,184,.14)" stroke="currentColor" stroke-width="2.4"/>'                   # hộp chì, mở khe bên phải
b += text(140, 118, "khe", "currentColor", 14, "middle", "600")
b += rect(50, 76, 48, 28, "rgba(248,113,113,.35)", RED, 2, 5)                     # mẫu quặng
b += text(74, 148, "mẫu trong hộp chì", "currentColor", 14, "middle", "600")
b += arrow("f1", "r", 106, 92, 202, 84, 2.2, "6 4")
b += text(164, 66, "tia α, β, γ", RED, 14, "middle", "700")
b += rect(210, 56, 92, 48, "rgba(56,189,248,.15)", BLUE, 2, 10)                   # ống đếm
b += text(256, 77, "ống đếm", BLUE, 14, "middle", "700")
b += text(256, 96, "Geiger", BLUE, 14, "middle", "700")
b += line(302, 80, 326, 80, "currentColor", 2)                                       # dây nối
b += rect(326, 56, 110, 48, "rgba(148,163,184,.14)", "currentColor", 2, 8)           # bộ đếm
b += text(381, 77, "bộ đếm", "currentColor", 14, "middle", "700")
b += text(381, 96, "≈ 500/phút", "currentColor", 14, "middle", "600")
fig1 = wrap("0 0 440 200",
            "Mẫu quặng phóng xạ trong hộp chì có một khe hở; tia thoát qua khe vào ống đếm Geiger nối với bộ đếm, khoảng 500 xung mỗi phút",
            b, "Hình 1. Tia thoát qua khe hộp chì vào ống đếm Geiger, bộ đếm ghi xung.")

# ------------------------------------------------- Hình 2: ba chùm tia trong điện trường
b = defs("f2")
b += text(14, 20, "Ba chùm tia trong điện trường đều", "currentColor", 14, "start", "700")
b += rect(70, 48, 260, 10, "rgba(148,163,184,.22)", "currentColor", 1.2, 2)        # bản dương
b += text(74, 42, "+ bản dương", "currentColor", 14, "start", "600")
b += rect(70, 200, 260, 10, "rgba(148,163,184,.22)", "currentColor", 1.2, 2)       # bản âm
b += text(74, 228, "− bản âm", "currentColor", 14, "start", "600")
b += dot(26, 129, 7, "currentColor")
b += text(26, 152, "nguồn", "currentColor", 14, "middle", "600")
b += line(33, 129, 70, 129, "currentColor", 2)
b += arrow("f2", "g", 74, 129, 380, 129, 2.2)
b += text(388, 133, "γ", GRN, 14, "start", "700")
b += path("M70,129 Q220,129 318,68", BLUE, 2.4, "f2-b")
b += text(334, 62, "β⁻", BLUE, 14, "start", "700")
b += path("M70,129 Q240,129 318,166", RED, 2.4, "f2-r")
b += text(334, 172, "α", RED, 14, "start", "700")
b += arrow("f2", "o", 110, 72, 110, 114, 2.4)
b += text(122, 98, "E", "currentColor", 14, "start", "700")
b += text(14, 252, "α lệch về bản âm · β⁻ lệch về bản dương", "currentColor", 14, "start", "600")
b += text(14, 272, "γ đi thẳng", "currentColor", 14, "start", "600")
fig2 = wrap("0 0 440 284",
            "Ba chùm tia alpha, beta trừ và gamma bay vào điện trường đều: alpha lệch xuống bản âm, beta trừ lệch lên bản dương, gamma bay thẳng",
            b, "Hình 2. γ không mang điện nên bay thẳng; β⁻ nhẹ hơn α nhiều nên lệch gắt hơn.")

# ------------------------------------------------- Hình 3: ảnh OpenStax (đợt 2, 27/10/2026)
fig3 = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l12-phong-xa/hinh-phan-ra-theo-chu-ki.webp" '
        'alt="Đồ thị số hạt nhân giảm một nửa sau mỗi chu kì bán rã" '
        'loading="lazy" width="750" height="597" style="max-width:100%;height:auto"><figcaption>'
        'Hình 3. Mỗi T còn một nửa. Nhãn: t<sub>1/2</sub> = T; Time = thời gian.<br>'
        '<small>Hình: OpenStax, College Physics 2e, Hình 31.19 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small>'
        '</figcaption></figure>')

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
