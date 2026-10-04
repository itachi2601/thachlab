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

# nhiệt lượng kế vỏ xốp (cột trái)
b += rect(24, 84, 112, 120, "rgba(148,163,184,.14)", "currentColor", 2.5)
b += rect(32, 92, 96, 104, "rgba(56,189,248,.14)", BLUE, 2)
b += line(32, 122, 128, 122, BLUE, 3)          # mặt nước
b += text(80, 108, "nước", BLUE, 12, "middle", "600")

# điện trở nhiệt trong bình
b += line(68, 122, 68, 184, RED, 4)
b += line(92, 122, 92, 184, RED, 4)
b += line(68, 184, 92, 184, RED, 4)
b += text(24, 310, "nhiệt lượng kế vỏ xốp + nắp, que khuấy", "currentColor", 10.5, "start", "600")
b += text(24, 290, "điện trở nhiệt trong bình", RED, 10, "start", "600")

# nhiệt kế cắm qua nắp
b += rect(100, 64, 14, 62, "rgba(148,163,184,.18)", "currentColor", 2, 6)
b += rect(103, 80, 8, 44, GRN, GRN, 0, 4)
b += f'<circle cx="107" cy="126" r="8" fill="rgba(52,211,153,.35)" stroke="{GRN}" stroke-width="2"/>'
b += text(122, 68, "nhiệt kế 0,1 °C", GRN, 10.5, "start", "700")

# dây nối sang oát kế
b += poly([(92, 184), (154, 184), (154, 236)], ORG, 2.2)
b += poly([(68, 184), (44, 250), (154, 250), (154, 268)], ORG, 2.2)

# cột phải: oát kế + bảng số liệu
b += text(196, 84, "oát kế", ORG, 11.5, "start", "700")
b += text(196, 100, "hiện P (W)", ORG, 10.5, "start", "600")
b += text(196, 116, "và thời gian τ (s)", ORG, 10.5, "start", "600")
b += rect(196, 130, 230, 190, "rgba(148,163,184,.10)", "currentColor", 2)
b += text(206, 152, "Ghi vào vở mỗi 20 s:", "currentColor", 11, "start", "700")
b += line(206, 162, 416, 162, "currentColor", 1, "", .5)
for i, s in enumerate(("τ (s)     t (°C)     P (W)", "0            25,0        500", "20          29,8        500",
                       "40          34,9        500", "60          39,7        500", "80          44,6        500",
                       "100        49,5        500")):
    b += text(206, 182 + i * 18, s, "currentColor", 10.5, "start", "500")
b += text(196, 342, "Cân điện tử đo m riêng, trước khi", "currentColor", 10.5, "start", "600")
b += text(196, 358, "đổ nước vào bình.", "currentColor", 10.5, "start", "600")

fig1 = wrap("0 0 440 370", "Sơ đồ bố trí thí nghiệm đo nhiệt lượng: nhiệt lượng kế có điện trở nhiệt và nhiệt kế, nối sang oát kế, số liệu ghi vào bảng",
            b, "Hình 1. Một phép đo nhiệt lượng cần bốn số: công suất P và thời gian τ (oát kế), khối lượng m (cân), độ tăng nhiệt độ Δt (nhiệt kế). Không có dụng cụ nào đọc thẳng nhiệt lượng.")

# ======================================================= Hình 2: đường cong đun nóng
b = defs("f2")
b += text(16, 22, "Đun 0,500 kg nước đá bằng bếp 500 W", "currentColor", 12.5, "start", "700")

OX, OY = 62, 214                 # gốc toạ độ
b += line(OX, OY, 428, OY, "currentColor", 2)
b += line(OX, OY, OX, 44, "currentColor", 2)
b += text(424, 234, "τ", "currentColor", 12, "end", "700")
b += text(28, 44, "t (°C)", "currentColor", 11.5, "start", "600")
b += text(40, OY + 5, "0", "currentColor", 11, "end", "600")
b += text(40, 106, "100", "currentColor", 11, "end", "600")
b += line(OX, 102, 424, 102, "currentColor", 1, "4 4", .4)

# toạ độ x của các mốc, tỉ lệ theo nhiệt lượng
X = [68, 72, 110, 155, 282, 400, 424]
Y0, Y100, YNEG = 206, 102, 224           # 0 °C, 100 °C, -10 °C
b += poly([(X[0], YNEG), (X[1], Y0), (X[2], Y0), (X[3], Y100), (X[4], Y100), (X[5], Y100), (X[6], Y100)],
          GRN, 2.8)
for x, y in ((X[0], YNEG), (X[1], Y0), (X[2], Y0), (X[3], Y100), (X[4], Y100), (X[5], Y100)):
    b += dot(x, y, 3.4, GRN)
b += line(OX - 4, YNEG, 428, YNEG, "currentColor", 1, "3 3", .35)
b += text(40, YNEG + 5, "−10", "currentColor", 10.5, "end", "600")

# nhãn từng giai đoạn
b += text(292, 74, "4. Hoá hơi ở 100 °C", RED, 11, "start", "700")
b += text(292, 88, "L = Pτ/m", RED, 10.5, "start", "600")
b += line(292, 92, 340, 100, RED, 1, "3 3", .8)
b += text(196, 148, "3. Nước 0 → 100 °C", BLUE, 11, "start", "700")
b += text(196, 162, "c = Pτ/(mΔt)", BLUE, 10.5, "start", "600")
b += line(196, 152, 140, 140, BLUE, 1, "3 3", .8)
b += text(112, 168, "2. Tan ở 0 °C", ORG, 11, "start", "700")
b += text(112, 182, "λ = Pτ/m", ORG, 10.5, "start", "600")
b += line(114, 186, 92, 202, ORG, 1, "3 3", .8)
b += text(16, 250, "Đoạn ngang = nhiệt dùng để chuyển thể, không làm nhiệt độ đổi.", "currentColor", 10.5, "start", "600")
fig2 = wrap("0 0 440 292", "Đường cong đun nóng của nước đá: nhiệt độ tăng, rồi đứng ở 0 độ C khi tan, tăng tiếp tới 100 độ C, rồi đứng ở 100 độ C khi sôi",
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
    y = 52 + i * 44
    b += text(16, y + 6, ten, "currentColor", 11, "start", "600")
    b += rect(150, y - 6, 210, 18, "rgba(148,163,184,.12)", "currentColor", 1, 4)
    b += rect(150, y - 6, max(3, 210 * phan / 100), 18, f"{col}55", col, 1.5, 4)
    b += text(398, y + 6, so, "currentColor", 10, "end", "600")
b += text(150, 238, "Cùng một khối nước đá 0,500 kg, bếp 500 W", "currentColor", 10.5, "start", "600")
b += text(150, 254, "→ riêng hoá hơi chiếm 3/4 tổng nhiệt", RED, 10.5, "start", "700")
fig3 = wrap("0 0 440 266", "Bốn thanh biểu diễn nhiệt cần cho bốn giai đoạn: hoá hơi chiếm 74 phần trăm, hoá hơi và tan chiếm phần lớn",
            b, "Hình 3. Cùng một khối nước đá 0,500 kg: hoá hơi chiếm 74% tổng nhiệt, còn giai đoạn đá nóng từ −10 °C lên 0 °C chỉ chiếm 0,7%. Đây là lí do cô đặc dung dịch rất tốn năng lượng.")

# ======================================================= Hình 4: ba đại lượng cần đo
b = defs("f4")
b += text(16, 22, "Ba đại lượng, cùng một cách đo", "currentColor", 12.5, "start", "700")

cards = (
    ("Nhiệt dung riêng", "J/(kg·K)", "c = Pτ / (m·Δt)", "đoạn nghiêng", BLUE),
    ("Nhiệt nóng chảy riêng", "J/kg", "λ = Pτ₁ / m", "đoạn ngang thứ nhất", ORG),
    ("Nhiệt hoá hơi riêng", "J/kg", "L = Pτ₂ / m", "đoạn ngang thứ hai", RED),
)
for i, (ten, dv, ct, mo, col) in enumerate(cards):
    x = 16 + i * 140
    b += rect(x, 40, 128, 138, f"{col}22", col, 2)
    b += text(x + 64, 64, ten, col, 11, "middle", "700")
    if i == 0:
        b += text(x + 64, 82, "Nhiệt dung riêng", "currentColor", 9.5, "middle", "500")
    b += text(x + 64, 104, ct, "currentColor", 11.5, "middle", "700")
    b += text(x + 64, 124, "đơn vị " + dv, "currentColor", 10, "middle", "600")
    b += text(x + 64, 146, mo, GRN, 10, "middle", "600")
    b += text(x + 64, 164, "τ của đoạn đó", "currentColor", 9.5, "middle", "500")
b += text(16, 202, "Điểm chung: đo P, τ, m rồi chia. Điểm khác: đọc số liệu ở đoạn nào của đồ thị.", "currentColor", 10.5, "start", "600")
b += text(16, 220, "Chú ý đơn vị: c có thêm K ở mẫu, λ và L thì không.", RED, 10.5, "start", "700")
fig4 = wrap("0 0 440 232", "Ba thẻ công thức cho ba đại lượng cần đo: nhiệt dung riêng, nhiệt nóng chảy riêng, nhiệt hoá hơi riêng",
            b, "Hình 4. Ba đại lượng của bài thực hành. Cùng cách đo (P, τ, m) nhưng đọc số liệu ở đoạn khác nhau của đồ thị, và đơn vị khác nhau: c có J/(kg·K), còn λ và L chỉ có J/kg.")

# ------------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
