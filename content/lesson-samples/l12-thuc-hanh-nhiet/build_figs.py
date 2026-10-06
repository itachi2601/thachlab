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
b += text(16, 22, "Bố trí một phép đo nhiệt lượng", "currentColor", 12.5, "start", "700")

# nhiệt lượng kế vỏ xốp
b += text(16, 50, "nhiệt lượng kế vỏ xốp, có nắp", "currentColor", 11, "start", "600")
b += line(50, 56, 50, 84, "currentColor", 1.2, "3 3", .8)
b += rect(24, 84, 126, 120, "rgba(148,163,184,.14)", "currentColor", 2.5)
b += rect(32, 92, 110, 104, "rgba(56,189,248,.14)", BLUE, 2)
b += line(32, 122, 142, 122, BLUE, 3)          # mặt nước
b += text(60, 112, "nước", BLUE, 12, "start", "600")

# điện trở nhiệt: hai chân + đáy
b += line(56, 130, 56, 184, RED, 4)
b += line(80, 130, 80, 184, RED, 4)
b += line(56, 184, 80, 184, RED, 4)
b += text(88, 170, "điện trở", RED, 10.5, "start", "700")

# nhiệt kế
b += rect(112, 64, 14, 62, "rgba(148,163,184,.18)", "currentColor", 2, 6)
b += rect(115, 80, 8, 44, GRN, GRN, 0, 4)
b += f'<circle cx="119" cy="128" r="8" fill="rgba(52,211,153,.35)" stroke="{GRN}" stroke-width="2"/>'
b += text(134, 70, "nhiệt kế 0,1 °C", GRN, 11, "start", "700")

# bảng số liệu (cột bên phải)
b += rect(190, 90, 236, 140, "rgba(148,163,184,.10)", "currentColor", 2)
b += text(202, 112, "Ghi vào vở mỗi 100 s", "currentColor", 11.5, "start", "700")
b += line(202, 120, 414, 120, "currentColor", 1, "", .5)
CX = (232, 312, 388)
for x, h in zip(CX, ("τ (s)", "t (°C)", "P (W)")):
    b += text(x, 138, h, "currentColor", 11, "middle", "700")
for r, row in enumerate((("0", "28,0", "150"), ("100", "45,8", "150"), ("200", "63,5", "150"), ("300", "81,3", "150"))):
    for x, v in zip(CX, row):
        b += text(x, 160 + r * 18, v, "currentColor", 11, "middle", "500")

# dây nối điện trở -> oát kế
b += poly([(80, 184), (80, 254), (190, 254)], ORG, 2.4)
b += poly([(56, 184), (56, 278), (190, 278)], ORG, 2.4)
b += rect(190, 242, 112, 48, "rgba(251,146,60,.14)", ORG, 2, 8)
b += text(246, 262, "oát kế", ORG, 11.5, "middle", "700")
b += text(246, 280, "P = 150 W, đo τ", ORG, 10.5, "middle", "600")
# cân điện tử
b += rect(318, 242, 108, 48, "rgba(148,163,184,.14)", "currentColor", 2, 8)
b += text(372, 262, "cân điện tử", "currentColor", 11, "middle", "700")
b += text(372, 280, "m = 0,200 kg", "currentColor", 10.5, "middle", "600")
b += text(16, 316, "Cân nước trước khi đổ vào bình; oát kế cho P và τ.", "currentColor", 10.5, "start", "600")

fig1 = wrap("0 0 440 328", "Sơ đồ bố trí thí nghiệm đo nhiệt lượng: nhiệt lượng kế có điện trở nhiệt và nhiệt kế, điện trở nối với oát kế, cân điện tử đo khối lượng nước, số liệu ghi vào bảng",
            b, "Hình 1. Một phép đo nhiệt lượng cần bốn số: công suất P và thời gian τ (oát kế), khối lượng m (cân), độ tăng nhiệt độ Δt (nhiệt kế). Không có dụng cụ nào đọc thẳng nhiệt lượng.")

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
            b, "Hình 2. Đường cong đun nóng: hai đoạn nằm ngang là hai lần chuyển thể (tan ở 0 °C, sôi ở 100 °C). Nhìn độ dài đoạn ngang để thấy nhiệt chuyển thể lớn hơn nhiều so với nhiệt làm nóng.")

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
            b, "Hình 3. Cùng một khối nước đá 0,500 kg: hoá hơi chiếm 74% tổng nhiệt, còn giai đoạn đá nóng từ −10 °C lên 0 °C chỉ chiếm 0,7%. Đây là lí do cô đặc dung dịch rất tốn năng lượng.")

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
            b, "Hình 4. Ba đại lượng của bài thực hành. Cùng cách đo (P, τ, m) nhưng đọc số liệu ở đoạn khác nhau của đồ thị, và đơn vị khác nhau: c có J/(kg·K), còn λ và L chỉ có J/kg.")

# ------------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
