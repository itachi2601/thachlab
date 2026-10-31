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
b += text(16, 22, "Bố trí một phép đo nhiệt lượng", "currentColor", 15, "start", "700")
b += text(16, 46, "nhiệt kế (độ chia 0,1 °C)", GRN, 14, "start", "700")
b += text(80, 68, "que khuấy", "currentColor", 14, "start", "600")

# nhiệt lượng kế vỏ xốp: nắp + thân + nước (mặt nước y = 136)
b += rect(20, 112, 176, 140, "rgba(148,163,184,.14)", "currentColor", 2.5, 8)
b += rect(28, 120, 160, 124, "rgba(56,189,248,.14)", BLUE, 2, 6)
b += line(28, 136, 188, 136, BLUE, 3)
b += rect(14, 100, 188, 12, "rgba(148,163,184,.45)", "currentColor", 2, 4)
b += text(140, 166, "nước", BLUE, 14, "middle", "700")

# nhiệt kế (bầu ngập trong nước) và que khuấy, cùng cắm qua nắp
b += rect(36, 58, 14, 150, "rgba(148,163,184,.18)", "currentColor", 2, 6)
b += rect(39, 150, 8, 58, GRN, GRN, 0, 3)
b += f'<circle cx="43" cy="214" r="8" fill="rgba(52,211,153,.45)" stroke="{GRN}" stroke-width="2"/>'
b += line(70, 60, 70, 232, "currentColor", 2.5)
b += line(60, 232, 80, 232, "currentColor", 3)

# dây điện trở: cuộn ở đáy, hai chân đi lên qua nắp
zz = [(104, 226)] + [(110 + 12 * i, 219 if i % 2 == 0 else 233) for i in range(6)] + [(176, 226)]
b += poly(zz, RED, 3)
b += line(104, 226, 104, 80, RED, 3)
b += line(176, 226, 176, 92, RED, 3)
b += text(140, 206, "điện trở", RED, 14, "middle", "700")

# mạch kín: điện trở -> oát kế -> nguồn điện -> điện trở
b += poly([(176, 92), (214, 92), (214, 300)], ORG, 2.4)
b += poly([(104, 80), (222, 80), (222, 278), (372, 278), (372, 300)], ORG, 2.4)
b += rect(154, 300, 120, 74, "rgba(251,146,60,.14)", ORG, 2, 8)
b += text(214, 322, "oát kế", ORG, 14, "middle", "700")
b += text(214, 342, "P = 150 W", ORG, 14, "middle", "600")
b += text(214, 362, "đo thời gian τ", ORG, 14, "middle", "600")
b += line(274, 337, 316, 337, ORG, 2.4)
b += rect(316, 300, 112, 74, "rgba(148,163,184,.14)", "currentColor", 2, 8)
b += text(372, 332, "nguồn điện", "currentColor", 14, "middle", "700")
b += text(372, 352, "nối ổ cắm", "currentColor", 14, "middle", "600")

b += text(16, 274, "nhiệt lượng kế", "currentColor", 14, "start", "700")
b += text(16, 292, "vỏ xốp, có nắp", "currentColor", 14, "start", "600")

# bảng số liệu (cột bên phải)
b += rect(232, 100, 204, 150, "rgba(148,163,184,.10)", "currentColor", 2)
b += text(244, 122, "Ghi vào vở mỗi 100 s", "currentColor", 14, "start", "700")
b += line(244, 130, 424, 130, "currentColor", 1, "", .5)
CX = (290, 382)
for x, h in zip(CX, ("τ (s)", "t (°C)")):
    b += text(x, 150, h, "currentColor", 14, "middle", "700")
for r, row in enumerate((("0", "28,0"), ("100", "45,8"), ("200", "63,5"), ("300", "81,3"))):
    for x, v in zip(CX, row):
        b += text(x, 174 + r * 20, v, "currentColor", 14, "middle", "500")

# cân điện tử
b += rect(16, 312, 124, 62, "rgba(148,163,184,.14)", "currentColor", 2, 8)
b += text(78, 336, "cân điện tử", "currentColor", 14, "middle", "700")
b += text(78, 358, "m = 0,200 kg", "currentColor", 14, "middle", "600")
b += text(16, 402, "Cân nước trước khi đổ vào bình.", "currentColor", 14, "start", "600")

fig1 = wrap("0 0 440 414", "Sơ đồ bố trí thí nghiệm đo nhiệt lượng: nhiệt lượng kế vỏ xốp có nắp chứa nước, dây điện trở ở đáy, nhiệt kế và que khuấy cắm qua nắp; hai chân dây điện trở nối kín với oát kế và nguồn điện; cân điện tử đo khối lượng nước; số liệu nhiệt độ ghi vào bảng mỗi 100 giây",
            b, "Hình 1. Bốn số cần đo: P và τ (oát kế), m (cân), Δt (nhiệt kế). Không dụng cụ nào đọc thẳng nhiệt lượng.")

# ======================================================= Hình 2: đường cong đun nóng
# Trục τ tuyến tính theo thời gian thật: 0,500 kg đá −10 °C, bếp 500 W.
# Thời gian từng giai đoạn: 10 500/500 = 21 s; 167 000/500 = 334 s; 210 000/500 = 420 s; 1 130 000/500 = 2 260 s.
b = defs("f2")
b += text(16, 22, "Đun 0,500 kg nước đá bằng bếp 500 W", "currentColor", 15, "start", "700")

OX, SX = 64, 0.112                # 0,112 px mỗi giây
def xt(tau):
    return OX + SX * tau
def yt(t):                        # 1,7 px mỗi °C
    return 262 - 1.7 * t
YA = yt(-10)                      # trục τ đặt ở mức −10 °C
b += line(OX, YA, 424, YA, "currentColor", 2)
b += chevron(428, YA, 1, 0, "currentColor", 2, 10)
b += line(OX, YA, OX, 44, "currentColor", 2)
b += chevron(OX, 40, 0, -1, "currentColor", 2, 10)
b += text(14, 48, "t (°C)", "currentColor", 14, "start", "700")
b += text(56, yt(100) + 5, "100", "currentColor", 14, "end", "600")
b += text(56, yt(0) + 5, "0", "currentColor", 14, "end", "600")
b += text(56, YA + 5, "−10", "currentColor", 14, "end", "600")
for tk in (1000, 2000, 3000):
    b += line(xt(tk), YA, xt(tk), YA + 6, "currentColor", 2)
    b += text(xt(tk), YA + 22, str(tk), "currentColor", 14, "middle", "600")
b += text(436, YA + 42, "τ (s)", "currentColor", 14, "end", "700")
b += line(OX, yt(100), 420, yt(100), "currentColor", 1, "4 4", .4)
b += line(OX, yt(0), 420, yt(0), "currentColor", 1, "4 4", .4)

cum = [0, 21, 355, 775, 3035]
pts = [(round(xt(cum[0]), 1), YA), (round(xt(cum[1]), 1), yt(0)), (round(xt(cum[2]), 1), yt(0)),
       (round(xt(cum[3]), 1), yt(100)), (round(xt(cum[4]), 1), yt(100))]
b += poly(pts, GRN, 2.8)
for x, y in pts:
    b += dot(x, y, 3.2, GRN)

# nhãn từng giai đoạn (đường dẫn nét đứt không cắt đường cong)
b += text(250, 62, "4. Hoá hơi ở 100 °C", RED, 14, "start", "700")
b += text(250, 80, "L = Pτ/m", RED, 14, "start", "600")
b += text(170, 170, "3. Nước 0 → 100 °C", BLUE, 14, "start", "700")
b += text(170, 188, "c = Pτ/(mΔt)", BLUE, 14, "start", "600")
b += line(165, 165, 134, 165, BLUE, 1.2, "3 3", .9)
b += text(74, 54, "2. Tan ở 0 °C", ORG, 14, "start", "700")
b += text(74, 72, "λ = Pτ/m", ORG, 14, "start", "600")
b += line(86, 78, 86, 257, ORG, 1.2, "3 3", .9)
b += text(74, YA + 42, "1. Đá −10 → 0 °C", BLUE, 14, "start", "700")
b += line(70, YA + 29, 65, YA + 4, BLUE, 1.2, "3 3", .9)
b += text(16, YA + 70, "Đoạn ngang: nhiệt dùng để chuyển thể,", "currentColor", 14, "start", "600")
b += text(16, YA + 90, "nhiệt độ không đổi.", "currentColor", 14, "start", "600")
fig2 = wrap(f"0 0 440 {YA + 102:.0f}", "Đường cong đun nóng 0,5 kg nước đá bằng bếp 500 W, trục thời gian theo tỉ lệ thật: nhiệt độ tăng từ −10 lên 0 độ C trong 21 giây, đứng ở 0 độ C 334 giây khi tan, tăng tới 100 độ C trong 420 giây, rồi đứng ở 100 độ C 2260 giây khi sôi",
            b, "Hình 2. Đường cong đun nóng: hai đoạn nằm ngang ứng với hai lần chuyển thể, tan ở 0 °C và sôi ở 100 °C.")

# ======================================================= Hình 3: bốn giai đoạn, tỉ lệ nhiệt
b = defs("f3")
b += text(16, 22, "Nhiệt chia thế nào giữa bốn giai đoạn", "currentColor", 15, "start", "700")

stages = (
    ("Đá −10 → 0 °C", 0.7, BLUE, "10 500 J (0,7%)"),
    ("Tan hoàn toàn ở 0 °C", 11.0, ORG, "167 000 J (11,0%)"),
    ("Nước 0 → 100 °C", 13.8, BLUE, "210 000 J (13,8%)"),
    ("Hoá hơi ở 100 °C", 74.5, RED, "1 130 000 J (74,5%)"),
)
for i, (ten, phan, col, so) in enumerate(stages):
    y = 54 + i * 54
    b += text(16, y, ten, "currentColor", 14, "start", "600")
    b += text(424, y, so, "currentColor", 14, "end", "600")
    b += rect(16, y + 9, 408, 18, "rgba(148,163,184,.12)", "currentColor", 1, 4)
    b += rect(16, y + 9, max(3, 408 * phan / 100), 18, f"{col}55", col, 1.5, 4)
b += text(16, 286, "Cùng một khối nước đá 0,500 kg, bếp 500 W:", "currentColor", 14, "start", "600")
b += text(16, 306, "riêng hoá hơi chiếm gần 3/4 tổng nhiệt.", RED, 14, "start", "700")
fig3 = wrap("0 0 440 318", "Bốn thanh biểu diễn nhiệt cần cho bốn giai đoạn: hoá hơi chiếm khoảng 74 phần trăm",
            b, "Hình 3. Cùng 0,500 kg nước đá: hoá hơi chiếm 74% tổng nhiệt, đá nóng từ −10 °C lên 0 °C chỉ chiếm 0,7%.")

# ======================================================= Hình 4: ba đại lượng cần đo
b = defs("f4")
b += text(16, 22, "Ba đại lượng, cùng một cách đo", "currentColor", 15, "start", "700")
SUB = '<tspan baseline-shift="sub" font-size="14">{}</tspan>'
cards = (
    ("Nhiệt dung riêng", "c = Pτ/(m·Δt)", "đơn vị J/(kg·K)", "τ: thời gian đoạn nghiêng", BLUE),
    ("Nhiệt nóng chảy riêng", "λ = Pτ" + SUB.format("1") + "/m", "đơn vị J/kg",
     "τ" + SUB.format("1") + ": thời gian đoạn ngang thứ nhất", ORG),
    ("Nhiệt hoá hơi riêng", "L = Pτ" + SUB.format("2") + "/m", "đơn vị J/kg",
     "τ" + SUB.format("2") + ": thời gian đoạn ngang thứ hai", RED),
)
for i, (ten, ct, dv, mo, col) in enumerate(cards):
    y0 = 38 + i * 94
    b += rect(16, y0, 408, 84, f"{col}22", col, 2)
    b += text(30, y0 + 26, ten, col, 14, "start", "700")
    b += text(410, y0 + 26, ct, "currentColor", 15, "end", "700")
    b += text(30, y0 + 50, dv, "currentColor", 14, "start", "600")
    b += text(30, y0 + 72, mo, "currentColor", 14, "start", "600")
b += text(16, 344, "Điểm chung: đo P, τ, m rồi chia.", "currentColor", 14, "start", "600")
b += text(16, 364, "Điểm khác: đọc ở đoạn nào của đồ thị.", "currentColor", 14, "start", "600")
b += text(16, 388, "Chú ý đơn vị: c có thêm K ở mẫu, λ và L thì không.", RED, 14, "start", "700")
fig4 = wrap("0 0 440 400", "Ba thẻ công thức cho ba đại lượng cần đo: nhiệt dung riêng, nhiệt nóng chảy riêng, nhiệt hoá hơi riêng",
            b, "Hình 4. Cùng cách đo P, τ, m nhưng đọc ở đoạn khác nhau của đồ thị; c có đơn vị J/(kg·K), λ và L chỉ J/kg.")

# ------------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
