"""Sinh 4 hình SVG cho bài "Bài 14. Máy phát điện xoay chiều. Máy biến áp" (Vật lí 12)
và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html.
Chạy từ thư mục này: python3 build_figs.py
"""
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *  # noqa: E402


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1, cap="butt"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"'
            f'{d} opacity="{op}" stroke-linecap="{cap}"/>')


def rect(x, y, w, h, fill, stroke="currentColor", sw=2, rx=6):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>')


def hop(x, y, w, h, s, c, size=12, fill="rgba(148,163,184,.10)"):
    """Hộp chữ nhật có chữ canh giữa."""
    return rect(x, y, w, h, fill, c, 1.8) + text(x + w / 2, y + h / 2 + 4, s, c, size, "middle", "700")


def circ(cx, cy, r, c="currentColor", w=2.2, fill="none", dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{w}"{d}/>'


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">'
            f'{body}</svg><figcaption>{cap}</figcaption></figure>')


# ------------------------------------------------- Hình 1: bốn chặng từ tua-bin tới ổ cắm
b = defs("f1")
b += text(14, 24, "Từ tua-bin tới ổ cắm: bốn chặng đổi số", "currentColor", 13, "start", "700")
b += hop(12, 52, 74, 56, "máy phát", RED)
b += hop(104, 52, 74, 56, "tăng áp", ORG)
b += hop(262, 52, 74, 56, "hạ áp", BLUE)
b += hop(354, 52, 74, 56, "tải", GRN)
b += arrow("f1", "r", 88, 80, 102, 80, 2.4)
b += arrow("f1", "o", 180, 80, 196, 80, 2.4)
b += line(196, 80, 260, 80, ORG, 2.4, "7 5")
b += text(222, 44, "đường dây 500 kV", ORG, 11, "middle", "700")
b += arrow("f1", "b", 338, 80, 352, 80, 2.4)
b += text(49, 126, "tua-bin quay", "currentColor", 11, "middle", "600")
b += text(141, 126, "lên 500 kV", ORG, 11, "middle", "600")
b += text(299, 126, "về 220 V", BLUE, 11, "middle", "600")
b += text(391, 126, "trong nhà", "currentColor", 11, "middle", "600")
b += text(14, 158, "Hao phí trên đường dây: ΔP = R·P²/U²", RED, 12, "start", "700")
b += text(14, 178, "Tăng điện áp lên k lần thì hao phí giảm k² lần", "currentColor", 11, "start", "600")
fig1 = wrap("0 0 440 192",
            "Sơ đồ từ máy phát điện tới ổ cắm: máy phát, máy biến áp tăng áp, đường dây 500 kV, máy biến áp hạ áp và tải 220 V",
            b,
            "Hình 1. Bốn chặng: máy phát → tăng áp lên 500 kV → đường dây → hạ áp về 220 V.")

# ------------------------------------------------- Hình 2: hai cách bố trí máy phát một pha
b = defs("f2")
b += text(14, 38, "a) nam châm quay", RED, 12.5, "start", "700")
b += circ(110, 100, 50, "currentColor", 2.2)
b += rect(44, 84, 12, 32, "rgba(56,189,248,.18)", BLUE, 1.8, 3)
b += rect(164, 84, 12, 32, "rgba(56,189,248,.18)", BLUE, 1.8, 3)
b += line(86, 120, 110, 96, BLUE, 8, cap="round")
b += line(110, 96, 134, 72, RED, 8, cap="round")
b += text(142, 64, "N", RED, 13, "start", "700")
b += text(87, 137, "S", BLUE, 13, "start", "700")
b += f'<path d="M 162.6 124.5 A 58 58 0 0 1 134.5 152.6" fill="none" stroke="{GRN}" stroke-width="2.4" marker-end="url(#f2-g)"/>'
b += text(168, 136, "ω", GRN, 14, "start", "700")
b += text(14, 168, "cuộn dây đứng yên", BLUE, 11, "start", "600")
b += text(14, 186, "lấy điện trực tiếp", "currentColor", 11, "start", "600")
b += text(232, 36, "b) khung dây quay", BLUE, 12.5, "start", "700")
b += rect(236, 42, 72, 14, "rgba(248,113,113,.18)", RED, 1.8, 3)
b += text(272, 53, "N", RED, 12, "middle", "700")
b += rect(236, 134, 72, 14, "rgba(56,189,248,.18)", BLUE, 1.8, 3)
b += text(272, 145, "S", BLUE, 12, "middle", "700")
b += field_line(256, 60, 256, 126, "currentColor")
b += field_line(288, 60, 288, 126, "currentColor")
b += text(222, 72, "B", "currentColor", 13, "start", "700")
b += rect(244, 70, 48, 52, "rgba(56,189,248,.14)", BLUE, 2, 4)
b += f'<path d="M 236 80 A 16 16 0 0 0 236 112" fill="none" stroke="{GRN}" stroke-width="2.4" marker-end="url(#f2-g)"/>'
b += text(206, 100, "ω", GRN, 14, "start", "700")
b += circ(330, 94, 8, ORG, 2.2)
b += circ(350, 94, 8, ORG, 2.2)
b += line(292, 94, 322, 94, ORG, 2.2)
b += line(292, 112, 350, 112, ORG, 2.2)
b += line(350, 112, 350, 102, ORG, 2.2)
b += line(330, 86, 330, 74, ORG, 2.4)
b += line(358, 94, 370, 94, ORG, 2.4)
b += text(374, 98, "chổi quét", ORG, 11, "start", "600")
b += text(320, 70, "vành khuyên", ORG, 11, "start", "600")
b += text(240, 128, "khung dây", BLUE, 11, "end", "600")
b += text(362, 124, "ra mạch ngoài", "currentColor", 11, "start", "600")
fig2 = wrap("0 0 440 196",
            "Hai cách bố trí máy phát điện xoay chiều một pha: cho nam châm quay thì lấy điện trực tiếp; cho khung dây quay trong từ trường B với tốc độ góc ω thì phải dùng vành khuyên và chổi quét",
            b,
            "Hình 2. Hai cách bố trí: (a) nam châm quay — lấy điện trực tiếp; (b) khung dây quay với tốc độ góc ω trong từ trường B — cần vành khuyên và chổi quét để đưa điện ra mạch ngoài.")

# ------------------------------------------------- Hình 3: ba pha — ba cuộn dây và ba suất điện động
b = defs("f3")
b += text(14, 24, "ba cuộn dây lệch 120°", "currentColor", 12.5, "start", "700")
b += text(240, 24, "ba suất điện động lệch 120°", "currentColor", 12.5, "start", "700")
b += circ(110, 122, 60, "currentColor", 2)
for cx, cy, col, nhan in ((110, 52, RED, "1"), (49, 157, BLUE, "2"), (171, 157, ORG, "3")):
    b += rect(cx - 13, cy - 10, 26, 20, "rgba(148,163,184,.12)", col, 2, 3)
    b += text(cx, cy + 4, nhan, col, 12, "middle", "700")
b += line(92, 148, 110, 122, BLUE, 7, cap="round")
b += line(110, 122, 128, 96, RED, 7, cap="round")
b += text(134, 88, "N", RED, 12, "start", "700")
b += text(80, 164, "S", BLUE, 12, "start", "700")
b += f'<path d="M 147 132 A 37 37 0 0 0 144 106" fill="none" stroke="{GRN}" stroke-width="2.4" marker-end="url(#f3-g)"/>'
b += text(150, 99, "ω", GRN, 14, "start", "700")
b += text(14, 216, "stato: 3 cuộn giống nhau", "currentColor", 11, "start", "600")
b += text(14, 234, "rô-to: nam châm quay đều", "currentColor", 11, "start", "600")
# đồ thị ba đường hình sin lệch pha nhau 2π/3
X0, X1, Y0, A = 246, 428, 122, 44
b += line(240, Y0, 434, Y0, "currentColor", 1.4, "", .55)
b += line(X0, 60, X0, 184, "currentColor", 1.4, "", .55)
b += text(238, 56, "u", "currentColor", 12, "start", "700")
b += text(430, 148, "t", "currentColor", 12, "end", "700")
for phi, col in ((0.0, RED), (-2 * math.pi / 3, BLUE), (2 * math.pi / 3, ORG)):
    pts = []
    for k in range(0, 37):
        x = X0 + (X1 - X0) * k / 36
        theta = 2 * math.pi * k / 36
        y = Y0 - A * math.sin(theta + phi)
        pts.append(f"{x:.1f},{y:.1f}")
    b += f'<polyline fill="none" stroke="{col}" stroke-width="2.4" points="{" ".join(pts)}"/>'
b += text(246, 204, "u₁, u₂, u₃ lệch 1/3 chu kì", "currentColor", 11, "start", "600")
fig3 = wrap("0 0 440 244",
            "Máy phát ba pha: ba cuộn dây đặt lệch nhau 120 độ trên stato và ba suất điện động lệch pha nhau một phần ba chu kì",
            b,
            "Hình 3. Ba cuộn dây lệch 120° trên stato cho ba suất điện động lệch pha một phần ba chu kì.")

# ------------------------------------------------- Hình 4: máy biến áp
b = defs("f4")
b += text(14, 24, "Máy biến áp: hai cuộn dây trên một lõi kín", "currentColor", 13, "start", "700")
b += rect(140, 40, 160, 26, "rgba(148,163,184,.22)", "currentColor", 1.6, 4)
b += rect(140, 144, 160, 26, "rgba(148,163,184,.22)", "currentColor", 1.6, 4)
b += rect(140, 40, 26, 130, "rgba(148,163,184,.22)", "currentColor", 1.6, 4)
b += rect(274, 40, 26, 130, "rgba(148,163,184,.22)", "currentColor", 1.6, 4)
for cy in (72, 101, 130):
    b += circ(153, cy, 11, RED, 2.2)
    b += circ(287, cy, 11, BLUE, 2.2)
b += line(60, 76, 142, 76, RED, 2.2)
b += line(60, 126, 142, 126, RED, 2.2)
b += line(60, 76, 60, 89, RED, 2.2)
b += line(60, 113, 60, 126, RED, 2.2)
b += circ(60, 101, 12, RED, 2.2)
b += f'<path d="M 52 101 q4 -8 8 0 t8 0" fill="none" stroke="{RED}" stroke-width="2"/>'
b += line(298, 76, 380, 76, BLUE, 2.2)
b += line(298, 126, 380, 126, BLUE, 2.2)
b += line(380, 76, 380, 90, BLUE, 2.2)
b += line(380, 112, 380, 126, BLUE, 2.2)
b += rect(372, 90, 16, 22, "none", BLUE, 2.2, 2)
b += text(396, 105, "R", BLUE, 12, "start", "700")
b += field_line(160, 53, 280, 53, GRN, 2)
b += field_line(280, 157, 160, 157, GRN, 2)
b += f'<text x="220" y="84" fill="{GRN}" font-size="12" font-weight="700" text-anchor="middle">Φ<tspan dy="3" font-size="9">B</tspan></text>'
b += text(24, 60, "nguồn u₁", RED, 11.5, "start", "700")
b += text(374, 60, "tải u₂", BLUE, 11.5, "start", "700")
b += text(130, 96, "sơ cấp", RED, 11.5, "end", "700")
b += text(130, 114, "N₁", RED, 11.5, "end", "700")
b += text(310, 96, "thứ cấp", BLUE, 11.5, "start", "700")
b += text(310, 114, "N₂", BLUE, 11.5, "start", "700")
b += text(220, 102, "lõi thép", "currentColor", 11, "middle", "600")
b += text(220, 120, "ghép lá cách điện", "currentColor", 11, "middle", "600")
b += text(14, 190, "nguồn xoay chiều · U₁/U₂ = N₁/N₂ = I₂/I₁", "currentColor", 12, "start", "700")
b += text(14, 208, "không đổi tần số · không sinh thêm điện năng", "currentColor", 11, "start", "600")
fig4 = wrap("0 0 440 220",
            "Sơ đồ máy biến áp: cuộn sơ cấp và cuộn thứ cấp quấn trên một lõi thép kín ghép từ các lá mỏng cách điện",
            b,
            "Hình 4. Sơ đồ máy biến áp một pha; từ thông Φ<sub>B</sub> khép kín trong lõi.")

# ------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
