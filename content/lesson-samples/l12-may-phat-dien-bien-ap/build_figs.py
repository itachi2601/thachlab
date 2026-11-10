"""Sinh 4 hình SVG cho bài "Bài 14. Máy phát điện xoay chiều. Máy biến áp" (Vật lí 12)
và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html.
Chạy từ thư mục này: python3 build_figs.py
"""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
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


def hop(x, y, w, h, s, c, size=14, fill="rgba(148,163,184,.10)"):
    """Hộp chữ nhật có chữ canh giữa."""
    return rect(x, y, w, h, fill, c, 1.8) + text(x + w / 2, y + h / 2 + 4, s, c, size, "middle", "700")


def circ(cx, cy, r, c="currentColor", w=2.2, fill="none", dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{w}"{d}/>'


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">'
            f'{body}</svg><figcaption>{cap}</figcaption></figure>')


def wrap_img(img, alt, w, h, cap, src):
    return (f'<figure class="fig" data-tl="1"><img src="/assets/openstax/l12-may-phat-dien-bien-ap/{img}.webp" alt="{alt}" '
            f'loading="lazy" width="{w}" height="{h}"><figcaption>{cap}<br><small>Hình: OpenStax, College Physics 2e, '
            f'Hình {src} — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>')


fig1 = wrap_img("hinh-he-thong-truyen-tai-d2",
    "Sơ đồ truyền tải điện: nhà máy phát điện, máy biến áp tăng áp, đường dây cao áp trên các cột tháp, trạm hạ áp, đường dây phân phối, máy biến áp hạ áp tới ngôi nhà",
    1000, 313,
    "Hình 1. Máy phát → tăng áp → đường dây cao áp → hạ áp → nhà em.<br>"
    "Số liệu trong ảnh là của sách; bài này dùng 500 kV và 220 V.<br>"
    "Nhãn: Power plant = nhà máy · Step-up = tăng áp · High-voltage transmission line = đường dây cao áp · Step-down = hạ áp · substation = trạm biến áp.",
    "23.26")

fig2 = wrap_img("hinh-may-phat-khung-quay-d2",
    "Máy phát điện xoay chiều một pha: khung dây quay quanh trục giữa hai cực N và S của nam châm, hai vành khuyên và hai chổi quét nối với bóng đèn, bên phải là đồ thị suất điện động hình sin theo thời gian",
    1000, 554,
    "Hình 2. Máy phát một pha: khung dây quay với tốc độ góc ω giữa hai cực N, S.<br>"
    "Mỗi đầu khung nối một vành khuyên riêng.<br>"
    "Chổi quét lấy điện ra bóng đèn.<br>"
    "Suất điện động biến thiên hình sin, T = 2π/ω.<br>"
    "Nhãn: Brushes = chổi quét · ℰ = suất điện động · ℰ₀ = giá trị cực đại · T = chu kì.",
    "23.21")

# ------------------------------------------------- Hình 3: ba pha — ba cuộn dây và ba suất điện động
b = ""
b += text(14, 24, "ba cuộn dây lệch 120°", "currentColor", 14, "start", "700")
b += text(240, 24, "ba suất điện động", "currentColor", 14, "start", "700")
b += circ(110, 122, 60, "currentColor", 2)
for cx, cy, col, nhan in ((110, 52, RED, "1"), (49, 157, BLUE, "2"), (171, 157, ORG, "3")):
    b += rect(cx - 13, cy - 10, 26, 20, "rgba(148,163,184,.12)", col, 2, 3)
    b += text(cx, cy + 4, nhan, col, 14, "middle", "700")
b += line(92, 148, 110, 122, BLUE, 7, cap="round")
b += line(110, 122, 128, 96, RED, 7, cap="round")
b += text(134, 88, "N", RED, 14, "start", "700")
b += text(80, 164, "S", BLUE, 14, "start", "700")
b += f'<path d="M 147 132 A 37 37 0 0 0 144 106" fill="none" stroke="{GRN}" stroke-width="2.4"/>'
# đầu V 30° tại (144,106): bán kính (34,-16) quay ngược chiều kim đồng hồ trên màn hình → tiếp tuyến (-16,-34)
b += chevron(144, 106, -16, -34, GRN, 2.4, 10)
b += text(124, 132, "ω", GRN, 14, "start", "700")
b += text(14, 214, "stato: 3 cuộn giống nhau", "currentColor", 14, "start", "600")
b += text(14, 234, "rô-to: nam châm quay đều", "currentColor", 14, "start", "600")
# đồ thị ba đường hình sin lệch pha nhau 2π/3
X0, X1, Y0, A = 246, 410, 122, 44
b += line(240, Y0, 432, Y0, "currentColor", 1.4, "", .55) + chevron(432, Y0, 1, 0, "currentColor", 1.4, 9)
b += line(X0, 58, X0, 184, "currentColor", 1.4, "", .55) + chevron(X0, 58, 0, -1, "currentColor", 1.4, 9)
b += text(228, 66, "e", "currentColor", 14, "start", "700")
b += text(434, 142, "t", "currentColor", 14, "end", "700")
for phi, col in ((0.0, RED), (-2 * math.pi / 3, BLUE), (2 * math.pi / 3, ORG)):
    pts = []
    for k in range(0, 37):
        x = X0 + (X1 - X0) * k / 36
        theta = 2 * math.pi * k / 36
        y = Y0 - A * math.sin(theta + phi)
        pts.append(f"{x:.1f},{y:.1f}")
    b += f'<polyline fill="none" stroke="{col}" stroke-width="2.4" points="{" ".join(pts)}"/>'
b += text(246, 204, "lệch nhau 1/3 chu kì", "currentColor", 14, "start", "600")
fig3 = wrap("0 0 440 244",
            "Máy phát ba pha: ba cuộn dây đặt lệch nhau 120 độ trên stato và ba suất điện động lệch pha nhau một phần ba chu kì",
            b,
            "Hình 3. Ba cuộn dây lệch 120° trên stato cho ba suất điện động lệch pha một phần ba chu kì.")

fig4 = wrap_img("hinh-may-bien-ap-d2",
    "Máy biến áp: hai cuộn dây quấn trên hai cạnh của một lõi thép kín ghép từ các lá mỏng, đường sức từ khép kín trong lõi; bên dưới là kí hiệu máy biến áp",
    660, 768,
    "Hình 4. Máy biến áp: hai cuộn dây quấn trên một lõi thép kín, đường sức từ (hồng) khép kín trong lõi.<br>"
    "Cuộn sơ cấp (bên trái) ít vòng, cuộn thứ cấp (bên phải) nhiều vòng hơn.<br>"
    "Điện áp tỉ lệ với số vòng.<br>"
    "Nhãn: V<sub>p</sub> = điện áp cuộn sơ cấp (tương ứng U₁) · V<sub>s</sub> = điện áp cuộn thứ cấp (U₂) · N<sub>p</sub> = số vòng cuộn sơ cấp (N₁) · Transformer symbol = kí hiệu máy biến áp.",
    "23.27")

# ------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(margin_figs(src))
print("ok", len(src), "bytes")
