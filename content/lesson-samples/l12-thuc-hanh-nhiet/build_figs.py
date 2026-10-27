"""Sinh 4 hình SVG cho bài "Bài 4. Thực hành đo nhiệt dung riêng, nhiệt nóng chảy riêng,
nhiệt hoá hơi riêng" (Vật lí 12) và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html.
Chạy từ thư mục này: python3 build_figs.py
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *  # noqa: E402


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def dot(x, y, r=5, c="currentColor"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def rect(x, y, w, h, fill, stroke="currentColor", sw=2, rx=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def poly(pts, c, w=2.6, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    s = " ".join(f"{x},{y}" for x, y in pts)
    return f'<polyline fill="none" stroke="{c}" stroke-width="{w}"{d} points="{s}"/>'


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


# ======================================================= Hình 1: sơ đồ bố trí thí nghiệm
b = defs("f1")
b += text(16, 22, "Bố trí một phép đo nhiệt lượng", "currentColor", 14, "start", "700")

# nhiệt lượng kế vỏ xốp
b += text(16, 44, "nhiệt lượng kế vỏ xốp, có nắp", "currentColor", 14, "start", "600")
b += line(100, 52, 100, 100, "currentColor", 1.2, "3 3", .8)
b += rect(24, 100, 146, 120, "rgba(148,163,184,.14)", "currentColor", 2.5)
b += rect(32, 108, 130, 104, "rgba(56,189,248,.14)", BLUE, 2)
b += line(32, 138, 162, 138, BLUE, 3)          # mặt nước
b += text(60, 130, "nước", BLUE, 14, "start", "600")

# điện trở nhiệt: hai chân + đáy
b += line(56, 146, 56, 200, RED, 4)
b += line(80, 146, 80, 200, RED, 4)
b += line(56, 200, 80, 200, RED, 4)
b += text(88, 186, "điện trở", RED, 14, "start", "700")

# que khuấy
b += text(16, 70, "que khuấy", "currentColor", 14, "start", "600")
b += line(40, 80, 40, 190, "currentColor", 2.5)
b += line(32, 190, 48, 190, "currentColor", 3)
# nhiệt kế
b += rect(120, 82, 14, 62, "rgba(148,163,184,.18)", "currentColor", 2, 6)
b += rect(123, 98, 8, 44, GRN, GRN, 0, 4)
b += f'<circle cx="127" cy="146" r="8" fill="rgba(52,211,153,.35)" stroke="{GRN}" stroke-width="2"/>'
b += text(142, 76, "nhiệt kế 0,1 °C", GRN, 14, "start", "700")

# bảng số liệu (cột bên phải)
b += rect(190, 100, 246, 150, "rgba(148,163,184,.10)", "currentColor", 2)
b += text(202, 122, "Ghi vào vở mỗi 100 s", "currentColor", 14, "start", "700")
b += line(202, 130, 424, 130, "currentColor", 1, "", .5)
CX = (234, 318, 396)
for x, h in zip(CX, ("τ (s)", "t (°C)", "P (W)")):
    b += text(x, 150, h, "currentColor", 14, "middle", "700")
for r, row in enumerate((("0", "28,0", "150"), ("100", "45,8", "150"), ("200", "63,5", "150"), ("300", "81,3", "150"))):
    for x, v in zip(CX, row):
        b += text(x, 174 + r * 20, v, "currentColor", 14, "middle", "500")

# mạch kín: điện trở -> oát kế -> nguồn điện -> điện trở
b += poly([(80, 200), (80, 299), (186, 299)], ORG, 2.4)
b += poly([(56, 200), (56, 356), (381, 356), (381, 336)], ORG, 2.4)
b += rect(186, 262, 120, 74, "rgba(251,146,60,.14)", ORG, 2, 8)
b += text(246, 284, "oát kế", ORG, 14, "middle", "700")
b += text(246, 304, "P = 150 W", ORG, 14, "middle", "600")
b += text(246, 324, "đo thời gian τ", ORG, 14, "middle", "600")
b += line(306, 299, 326, 299, ORG, 2.4)
b += rect(326, 262, 110, 74, "rgba(148,163,184,.14)", "currentColor", 2, 8)
b += text(381, 294, "nguồn điện", "currentColor", 14, "middle", "700")
b += text(381, 314, "nối ổ cắm", "currentColor", 14, "middle", "600")
# cân điện tử
b += rect(16, 374, 160, 56, "rgba(148,163,184,.14)", "currentColor", 2, 8)
b += text(96, 396, "cân điện tử", "currentColor", 14, "middle", "700")
b += text(96, 416, "m = 0,200 kg", "currentColor", 14, "middle", "600")
b += text(190, 408, "Cân nước trước khi đổ vào bình.", "currentColor", 14, "start", "600")

fig1 = wrap("0 0 440 446", "Sơ đồ bố trí thí nghiệm đo nhiệt lượng: nhiệt lượng kế có điện trở nhiệt, nhiệt kế và que khuấy, điện trở nối kín với oát kế và nguồn điện, cân điện tử đo khối lượng nước, số liệu ghi vào bảng",
            b, "Hình 1. Bốn số cần đo: P và τ (oát kế), m (cân), Δt (nhiệt kế). Không dụng cụ nào đọc thẳng nhiệt lượng.")

# ======================================================= Hình 2: đường cong đun nóng
b = defs("f2")
b += text(16, 22, "Đun 0,500 kg nước đá bằng bếp 500 W", "currentColor", 12.5, "start", "700")

OX = 62
def yt(t):                       # trục nhiệt độ tuyến tính: 1,6 px mỗi °C
    return 250 - 1.6 * t
b += line(OX, yt(-10), 428, yt(-10), "currentColor", 2)      # trục τ đặt ở mức -10 °C
b += line(OX, yt(-10), OX, 46, "currentColor", 2)
b += text(428, 288, "τ", "currentColor", 12, "end", "700")
b += text(28, 44, "t (°C)", "currentColor", 11.5, "start", "600")
b += text(54, yt(0) + 4, "0", "currentColor", 11, "end", "600")
b += text(54, yt(100) + 4, "100", "currentColor", 11, "end", "600")
b += text(54, yt(-10) + 4, "−10", "currentColor", 11, "end", "600")
b += line(OX, yt(100), 424, yt(100), "currentColor", 1, "4 4", .4)
b += line(OX, yt(0), 424, yt(0), "currentColor", 1, "4 4", .4)

# mốc x tỉ lệ theo nhiệt lượng (≈ 10,5 : 167 : 210 : 1130 kJ, rút gọn đoạn sôi)
X = [68, 72, 110, 155, 400]
pts = [(X[0], yt(-10)), (X[1], yt(0)), (X[2], yt(0)), (X[3], yt(100)), (X[4], yt(100)), (424, yt(100))]
b += poly(pts, GRN, 2.8)
for x, y in pts[:5]:
    b += dot(x, y, 3.4, GRN)

# nhãn từng giai đoạn
b += text(262, 62, "4. Hoá hơi ở 100 °C", RED, 11.5, "start", "700")
b += text(262, 77, "L = Pτ/m", RED, 11, "start", "600")
b += line(300, 82, 320, yt(100) - 2, RED, 1, "3 3", .8)
b += text(196, 168, "3. Nước 0 → 100 °C", BLUE, 11.5, "start", "700")
b += text(196, 183, "c = Pτ/(mΔt)", BLUE, 11, "start", "600")
b += line(192, 166, 136, 166, BLUE, 1, "3 3", .8)
b += text(196, 222, "2. Tan ở 0 °C", ORG, 11.5, "start", "700")
b += text(196, 237, "λ = Pτ/m", ORG, 11, "start", "600")
b += line(192, 232, 116, 249, ORG, 1, "3 3", .8)
b += text(16, 310, "Đoạn ngang = nhiệt dùng để chuyển thể, không làm nhiệt độ đổi.", "currentColor", 10.5, "start", "600")
fig2 = wrap("0 0 440 322", "Đường cong đun nóng của nước đá: nhiệt độ tăng, rồi đứng ở 0 độ C khi tan, tăng tiếp tới 100 độ C, rồi đứng ở 100 độ C khi sôi",
            b, "Hình 2. Đường cong đun nóng: hai đoạn nằm ngang ứng với hai lần chuyển thể, tan ở 0 °C và sôi ở 100 °C.")

# ======================================================= Hình 3: bốn giai đoạn, tỉ lệ nhiệt
b = defs("f3")
b += text(16, 22, "Nhiệt chia thế nào giữa bốn giai đoạn", "currentColor", 12.5, "start", "700")

stages = (
    ("Đá −10 → 0 °C", 0.7, BLUE, "10 500 J · 0,7%"),
    ("Tan hoàn toàn ở 0 °C", 11.0, ORG, "167 000 J · 11,0%"),
    ("Nước 0 → 100 °C", 13.8, BLUE, "210 000 J · 13,8%"),
    ("Hoá hơi ở 100 °C", 74.5, RED, "1 130 000 J · 74,5%"),
)
for i, (ten, phan, col, so) in enumerate(stages):
    y = 52 + i * 50
    b += text(16, y, ten, "currentColor", 11.5, "start", "600")
    b += text(424, y, so, "currentColor", 11, "end", "600")
    b += rect(16, y + 8, 408, 16, "rgba(148,163,184,.12)", "currentColor", 1, 4)
    b += rect(16, y + 8, max(3, 408 * phan / 100), 16, f"{col}55", col, 1.5, 4)
b += text(16, 262, "Cùng một khối nước đá 0,500 kg, bếp 500 W", "currentColor", 11, "start", "600")
b += text(16, 280, "→ riêng hoá hơi chiếm 3/4 tổng nhiệt", RED, 11, "start", "700")
fig3 = wrap("0 0 440 292", "Bốn thanh biểu diễn nhiệt cần cho bốn giai đoạn: hoá hơi chiếm 74 phần trăm, hoá hơi và tan chiếm phần lớn",
            b, "Hình 3. Cùng 0,500 kg nước đá: hoá hơi chiếm 74% tổng nhiệt, đá nóng từ −10 °C lên 0 °C chỉ chiếm 0,7%.")

# ======================================================= Hình 4: ba đại lượng cần đo
b = defs("f4")
b += text(16, 22, "Ba đại lượng, cùng một cách đo", "currentColor", 12.5, "start", "700")

cards = (
    (("Nhiệt dung", "riêng"), "J/(kg·K)", "c = Pτ / (m·Δt)", "đoạn nghiêng", BLUE),
    (("Nhiệt nóng chảy", "riêng"), "J/kg", "λ = Pτ₁ / m", "đoạn ngang thứ nhất", ORG),
    (("Nhiệt hoá hơi", "riêng"), "J/kg", "L = Pτ₂ / m", "đoạn ngang thứ hai", RED),
)
for i, (ten, dv, ct, mo, col) in enumerate(cards):
    x = 16 + i * 140
    b += rect(x, 40, 128, 150, f"{col}22", col, 2)
    b += text(x + 64, 62, ten[0], col, 11, "middle", "700")
    b += text(x + 64, 77, ten[1], col, 11, "middle", "700")
    b += text(x + 64, 104, ct, "currentColor", 11.5, "middle", "700")
    b += text(x + 64, 126, "đơn vị " + dv, "currentColor", 10, "middle", "600")
    b += text(x + 64, 150, mo, GRN, 10, "middle", "600")
    b += text(x + 64, 170, "τ của đoạn đó", "currentColor", 9.5, "middle", "500")
b += text(16, 214, "Điểm chung: đo P, τ, m rồi chia. Điểm khác: đọc số liệu ở đoạn nào của đồ thị.", "currentColor", 10.5, "start", "600")
b += text(16, 232, "Chú ý đơn vị: c có thêm K ở mẫu, λ và L thì không.", RED, 10.5, "start", "700")
fig4 = wrap("0 0 440 244", "Ba thẻ công thức cho ba đại lượng cần đo: nhiệt dung riêng, nhiệt nóng chảy riêng, nhiệt hoá hơi riêng",
            b, "Hình 4. Cùng cách đo P, τ, m nhưng đọc ở đoạn khác nhau của đồ thị; c có đơn vị J/(kg·K), λ và L chỉ J/kg.")

# ------------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
