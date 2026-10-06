"""Sinh 4 hình SVG cho bài "Bài 2. Thang nhiệt độ" (Vật lí 12) và thay các mốc
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


def dot(x, y, r=5, c="currentColor"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def rect(x, y, w, h, fill, stroke="currentColor", sw=2, rx=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def hop(x, y, w, h, s, c, size=12):
    """Hộp chữ nhật có chữ canh giữa."""
    return rect(x, y, w, h, "rgba(148,163,184,.10)") + text(x + w / 2, y + h / 2 + 4, s, c, size, "middle", "700")


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


# ------------------------------------------------------- Hình 1: một nhiệt độ, ba con số
b = defs("f1")
b += text(16, 26, "Ba thang đo, một nhiệt độ", "currentColor", 13, "start", "700")
b += rect(196, 46, 30, 132, "rgba(148,163,184,.14)", "currentColor", 2.5, 15)           # ống nhiệt kế
b += rect(205, 86, 12, 96, RED, RED, 0, 6)                                               # cột chất lỏng
b += f'<circle cx="211" cy="190" r="17" fill="rgba(248,113,113,.35)" stroke="{RED}" stroke-width="2"/>'
b += f'<circle cx="211" cy="190" r="11" fill="{RED}"/>'
for y, col, so, ten in ((52, GRN, "38,5 °C", "thang Celsius"),
                        (110, BLUE, "311,5 K", "thang Kelvin"),
                        (168, RED, "101,3 °F", "thang Fahrenheit")):
    b += rect(14, y, 140, 42, f"rgba(148,163,184,.10)", col, 1.6, 8)
    b += text(24, y + 22, so, col, 14, "start", "700")
    b += text(24, y + 37, ten, col, 11, "start", "500")
    b += line(156, y + 21, 208, 90, "currentColor", 1.2, "5 4", .7)
b += text(240, 84, "cùng một mức", "currentColor", 11, "start", "600")
b += text(240, 100, "nhiệt độ", "currentColor", 11, "start", "600")
fig1 = wrap("0 0 420 240", "Một nhiệt kế với ba nhãn nhiệt độ theo ba thang đo cho cùng một mức nhiệt độ",
            b, "Hình 1. Ba thang đo, một nhiệt độ: 38,5 °C = 311,5 K = 101,3 °F — chỉ khác cách chia thang.")

# ------------------------------------------------------- Hình 2: cân bằng nhiệt
b = defs("f2")
b += text(14, 24, "a) Vừa tiếp xúc", "currentColor", 12, "start", "700")
b += rect(30, 50, 80, 64, "rgba(248,113,113,.18)", RED, 2)
b += rect(110, 50, 80, 64, "rgba(56,189,248,.18)", BLUE, 2)
b += text(70, 72, "A", RED, 15, "middle", "700") + text(150, 72, "B", BLUE, 15, "middle", "700")
b += text(70, 134, "80 °C", RED, 12, "middle", "700") + text(150, 134, "20 °C", BLUE, 12, "middle", "700")
b += arrow("f2", "r", 74, 100, 146, 100, 2.6)
b += text(110, 168, "nhiệt năng truyền A → B", RED, 11, "middle", "700")
b += text(240, 24, "b) Một lúc sau", "currentColor", 12, "start", "700")
b += rect(250, 50, 80, 64, "rgba(52,211,153,.18)", GRN, 2)
b += rect(330, 50, 80, 64, "rgba(52,211,153,.18)", GRN, 2)
b += text(290, 72, "A", GRN, 15, "middle", "700") + text(370, 72, "B", GRN, 15, "middle", "700")
b += text(290, 134, "50 °C", GRN, 12, "middle", "700") + text(370, 134, "50 °C", GRN, 12, "middle", "700")
b += text(330, 168, "cân bằng nhiệt — hết truyền", GRN, 11, "middle", "700")
fig2 = wrap("0 0 440 186", "Hai vật A nóng và B lạnh tiếp xúc nhau: nhiệt năng truyền từ A sang B cho tới khi hai vật cùng nhiệt độ",
            b, "Hình 2. Hai vật tiếp xúc: nhiệt năng truyền từ vật nóng hơn sang vật lạnh hơn cho tới khi hai nhiệt độ bằng nhau — lúc đó hai vật ở trạng thái cân bằng nhiệt.")

# ------------------------------------------------------- Hình 4 (mốc FIG3): ba thang đo
b = defs("f3")
b += text(100, 24, "Celsius", RED, 13, "middle", "700")
b += text(230, 24, "Kelvin", BLUE, 13, "middle", "700")
b += text(360, 24, "Fahrenheit", ORG, 13, "middle", "700")
b += line(40, 74, 422, 74, "currentColor", 1.2, "6 5", .35)
b += line(40, 190, 422, 190, "currentColor", 1.2, "6 5", .35)
for x, col in ((100, RED), (230, BLUE), (360, ORG)):
    b += line(x, 44, x, 214, "currentColor", 2)
    b += line(x - 8, 74, x + 8, 74, col, 3)
    b += line(x - 8, 190, x + 8, 190, col, 3)
b += text(88, 66, "100 °C", RED, 12, "end", "700") + text(88, 182, "0 °C", RED, 12, "end", "700")
b += text(218, 66, "373 K", BLUE, 12, "end", "700") + text(218, 182, "273 K", BLUE, 12, "end", "700")
b += text(348, 66, "212 °F", ORG, 12, "end", "700") + text(348, 182, "32 °F", ORG, 12, "end", "700")
b += text(88, 138, "100 khoảng", GRN, 11, "end", "600")
b += text(218, 138, "100 khoảng", GRN, 11, "end", "600")
b += text(348, 138, "180 khoảng", ORG, 11, "end", "600")
b += text(16, 238, "mốc dưới: nước đá đang tan · mốc trên: hơi nước đang sôi", "currentColor", 11)
fig3 = wrap("0 0 440 250", "Ba thang nhiệt độ đặt cạnh nhau: Celsius 0 đến 100, Kelvin 273 đến 373, Fahrenheit 32 đến 212",
            b, "Hình 4. Ba thang đo cùng hai mốc nước: Celsius 0 °C – 100 °C chia 100 khoảng, Kelvin 273 K – 373 K cũng 100 khoảng, Fahrenheit 32 °F – 212 °F chia 180 khoảng.")

# ------------------------------------------------------- Hình 3 (mốc FIG4): ngoại suy về 0 K
b = defs("f4")
b += line(70, 205, 420, 205, "currentColor", 2)
b += line(70, 205, 70, 40, "currentColor", 2)
b += text(412, 240, "t (°C)", "currentColor", 12, "end", "600")
b += text(24, 40, "p (kPa)", "currentColor", 12, "start", "600")
b += line(95, 205, 307, 91, GRN, 2, "6 5", .9)
b += f'<polyline fill="none" stroke="{GRN}" stroke-width="2.6" points="307,91 384.5,49"/>'
pts = ((307, 91), (326, 80), (346, 70), (365, 59), (384, 49))
for x, y in pts:
    b += dot(x, y, 4, GRN)
b += line(95, 205, 95, 62, RED, 1.2, "5 4", .8)
b += text(100, 50, "0 K", GRN, 12, "start", "700")
b += text(95, 224, "-273", RED, 12, "middle", "700")
b += text(307, 224, "0", "currentColor", 12, "middle", "600")
b += text(384, 224, "100", "currentColor", 12, "middle", "600")
b += text(150, 62, "kéo dài đường thẳng", GRN, 11, "start", "600")
b += text(150, 80, "→ cắt trục ở -273 °C", GRN, 11, "start", "600")
fig4 = wrap("0 0 440 250", "Đồ thị áp suất khí theo nhiệt độ Celsius: các điểm nằm trên một đường thẳng, kéo dài cắt trục hoành ở -273 °C",
            b, "Hình 3. Áp suất một lượng khí không đổi tăng đều theo nhiệt độ. Kéo dài đường biểu diễn, nó cắt trục nhiệt độ ở −273 °C — đó là gốc 0 K của thang Kelvin.")

# ------------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
