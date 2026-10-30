"""Sinh 4 hình SVG cho bài "Bài 17. Hiện tượng phóng xạ" (Vật lí 12) và thay các mốc
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
# hộp chì thành dày (khung ngoài 22..132 x 46..136, thành 10 px), khe hở thành phải ở y 82..102
b += '<path d="M132,82 V46 H22 V136 H132 V102 H122 V126 H32 V56 H122 V82 Z" fill="rgba(148,163,184,.55)" stroke="currentColor" stroke-width="1.6"/>'
b += rect(52, 78, 46, 28, "rgba(248,113,113,.35)", RED, 2, 5)                     # mẫu quặng
b += text(146, 124, "khe", "currentColor", 14, "start", "600")
b += line(140, 112, 132, 103, "currentColor", 1.2)
b += text(77, 156, "mẫu trong hộp chì", "currentColor", 14, "middle", "600")
b += arrow("f1", "r", 100, 92, 206, 92, 2.4, "6 4")                              # tia ra thẳng qua khe
b += text(142, 78, "tia α, β, γ", RED, 14, "start", "700")
b += rect(210, 66, 92, 52, "rgba(56,189,248,.15)", BLUE, 2, 10)                   # ống đếm
b += text(256, 88, "ống đếm", BLUE, 14, "middle", "700")
b += text(256, 107, "Geiger", BLUE, 14, "middle", "700")
b += line(302, 92, 322, 92, "currentColor", 2)                                       # dây nối
b += rect(322, 66, 110, 52, "rgba(148,163,184,.14)", "currentColor", 2, 8)           # bộ đếm
b += text(377, 88, "bộ đếm", "currentColor", 14, "middle", "700")
b += text(377, 107, "≈ 500/phút", "currentColor", 14, "middle", "600")
fig1 = wrap("0 0 440 168",
            "Mẫu quặng phóng xạ trong hộp chì thành dày có một khe hở; tia thoát qua khe vào ống đếm Geiger nối với bộ đếm, khoảng 500 xung mỗi phút",
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
b += arrow("f2", "g", 74, 129, 380, 129, 2.4)
b += text(388, 133, "γ", GRN, 14, "start", "700")
# đường cong Bezier bậc 2; đầu V đặt theo tiếp tuyến tại điểm cuối (P2 − P1)
b += path("M70,129 Q220,129 318,68", BLUE, 2.4)
b += chevron(318, 68, 318 - 220, 68 - 129, BLUE, 2.4, 10)
b += text(328, 90, "β⁻", BLUE, 14, "start", "700")
b += path("M70,129 Q240,129 318,166", RED, 2.4)
b += chevron(318, 166, 318 - 240, 166 - 129, RED, 2.4, 10)
b += text(328, 176, "α", RED, 14, "start", "700")
b += arrow("f2", "o", 110, 72, 110, 114, 2.4)
b += text(122, 98, "E", ORG, 14, "start", "700")
b += text(14, 254, "α (+2e) lệch về bản âm", RED, 14, "start", "600")
b += text(14, 274, "β⁻ (−e) lệch về bản dương", BLUE, 14, "start", "600")
b += text(14, 294, "γ không mang điện: đi thẳng", GRN, 14, "start", "600")
fig2 = wrap("0 0 440 304",
            "Ba chùm tia alpha, beta trừ và gamma bay vào điện trường đều: alpha lệch xuống bản âm, beta trừ lệch lên bản dương, gamma bay thẳng",
            b, "Hình 2. γ không mang điện nên bay thẳng; β⁻ nhẹ hơn α nhiều nên lệch gắt hơn.")

# ------------------------------------------------- Hình 3: ảnh OpenStax (đợt 2, 27/10/2026)
fig3 = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l12-phong-xa/hinh-phan-ra-theo-chu-ki.webp" '
        'alt="Đồ thị số hạt nhân giảm một nửa sau mỗi chu kì bán rã" '
        'loading="lazy" width="750" height="597" style="max-width:100%;height:auto"><figcaption>'
        'Hình 3. Mỗi T còn một nửa.<br>Nhãn: t<sub>1/2</sub> = T<br>Number of nuclides = số hạt nhân<br>Time in multiples of t<sub>1/2</sub> = thời gian tính theo số chu kì<br>'
        '<small>Hình: OpenStax, College Physics 2e, Hình 31.19 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small>'
        '</figcaption></figure>')

# ------------------------------------------------- Hình 4: dịch chuyển ô trong bảng tuần hoàn
b = defs("f4")
b += text(14, 22, "Hạt nhân con dịch chuyển trong bảng tuần hoàn", "currentColor", 14, "start", "700")
Z0, X0, PITCH, W, H = 89, 50, 62, 58, 36                       # 5 ô Z = 89..93
HANG = ((40, 3, 1, "α", "α: lùi 2 ô", RED, "r"),            # mẹ Z=92 → con Z=90
        (116, 1, 2, "β⁻", "β⁻: tiến 1 ô", BLUE, "b"),       # mẹ Z=90 → con Z=91
        (192, 2, 1, "β⁺", "β⁺: lùi 1 ô", ORG, "o"))          # mẹ Z=91 → con Z=90
for y, ip, ic, ten, nhan, col, mk in HANG:
    b += text(14, y + 24, ten, col, 15, "start", "700")
    for i in range(5):
        x = X0 + PITCH * i
        if i == ip:
            b += rect(x, y, W, H, "rgba(248,113,113,.30)", RED, 2, 4)
            mau = RED
        elif i == ic:
            b += rect(x, y, W, H, "rgba(52,211,153,.30)", GRN, 2, 4)
            mau = GRN
        else:
            b += rect(x, y, W, H, "rgba(148,163,184,.08)", "currentColor", 1.2, 4)
            mau = "currentColor"
        b += text(x + W / 2, y + 24, str(Z0 + i), mau, 15, "middle", "700")
    cx = lambda i: X0 + PITCH * i + W / 2
    b += arrow("f4", mk, cx(ip), y + 50, cx(ic), y + 50, 2.4)
    b += text(428, y + 55, nhan, col, 14, "end", "700")
b += text(14, 270, "Số trong ô là Z (số proton)", "currentColor", 14, "start", "600")
b += rect(14, 280, 16, 14, "rgba(248,113,113,.30)", RED, 2, 3)
b += text(38, 292, "hạt nhân mẹ", "currentColor", 14, "start", "600")
b += rect(150, 280, 16, 14, "rgba(52,211,153,.30)", GRN, 2, 3)
b += text(174, 292, "hạt nhân con", "currentColor", 14, "start", "600")
fig4 = wrap("0 0 440 304",
            "Ba hàng ô nguyên tố: phân rã alpha làm con lùi 2 ô, phân rã beta trừ làm con tiến 1 ô, phân rã beta cộng làm con lùi 1 ô",
            b, "Hình 4. Chỗ dịch chuyển của hạt nhân con: α lùi 2 ô, β⁻ tiến 1 ô, β⁺ lùi 1 ô; tia γ không đổi ô.")

# ------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(margin_figs(src))
print("ok", len(src), "bytes")
