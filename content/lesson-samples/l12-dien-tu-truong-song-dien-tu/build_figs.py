"""Sinh 4 hình SVG cho bài "Bài 16. Điện từ trường. Mô hình sóng điện từ" (Vật lí 12)
và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html.
Chạy từ thư mục này: python3 build_figs.py
"""
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *  # noqa: E402


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def rect(x, y, w, h, fill="rgba(148,163,184,.10)", stroke="currentColor", sw=2, rx=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def arc(cx, cy, r, a1, a2, c="currentColor", w=2, op=1):
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    x2, y2 = cx + r * math.cos(math.radians(a2)), cy + r * math.sin(math.radians(a2))
    return (f'<path d="M {x1:.1f},{y1:.1f} A {r},{r} 0 0 1 {x2:.1f},{y2:.1f}" fill="none" '
            f'stroke="{c}" stroke-width="{w}" opacity="{op}"/>')


def poly(pts, c, w=2.4, op=1):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polyline fill="none" stroke="{c}" stroke-width="{w}" opacity="{op}" points="{p}"/>'


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


# ------------------------------------------------- Hình 1: tiếng rè trong xưởng
b = defs("f1")
b += text(14, 22, "Không có dây nối, radio vẫn rè", "currentColor", 12.5, "start", "700")
b += rect(14, 62, 96, 74)
b += text(62, 92, "máy hàn", "currentColor", 12, "middle", "700")
b += text(62, 110, "dòng xoay chiều", "currentColor", 9.5, "middle", "600")
b += text(62, 124, "biến thiên", "currentColor", 9.5, "middle", "600")
for r, op in ((26, .95), (44, .7), (62, .45)):
    b += arc(125, 100, r, -52, 52, BLUE, 2.2, op)
b += rect(250, 64, 88, 72)
b += text(294, 96, "radio", "currentColor", 12, "middle", "700")
b += text(294, 114, "chạy pin", "currentColor", 9.5, "middle", "600")
b += text(294, 128, "cách 2 m", "currentColor", 9.5, "middle", "600")
b += line(294, 64, 282, 30, "currentColor", 2.4)
b += text(14, 168, "Dòng biến thiên sinh điện từ trường,", BLUE, 11, "start", "600")
b += text(14, 184, "trường lan tới ăng ten radio thành tín hiệu nhiễu.", BLUE, 11, "start", "600")
fig1 = wrap("0 0 420 198", "Máy hàn chạy dòng xoay chiều đặt cạnh một radio chạy pin: sóng điện từ lan từ máy hàn tới ăng ten radio",
            b, "Hình 1. Máy hàn chạy dòng xoay chiều: điện từ trường lan tới ăng ten radio cách hai mét.",
            exp="tn-l12-dttruong-03")

# ------------------------------------------------- Hình 2: điện trường xoáy
b = defs("f2")
b += text(14, 22, "Điện trường xoáy bao quanh đường sức từ", "currentColor", 12.5, "start", "700")
b += f'<ellipse cx="210" cy="118" rx="96" ry="56" fill="none" stroke="{BLUE}" stroke-width="2.6"/>'
b += line(210, 52, 210, 184, RED, 3)
b += f'<path d="M210,56 L204,68 L216,68 z" fill="{RED}"/>'
b += arrow("f2", "b", 176, 62, 244, 62, 2.4)
b += arrow("f2", "b", 244, 174, 176, 174, 2.4)
b += text(222, 46, "đường sức từ biến thiên (B)", RED, 10.5, "start", "600")
b += text(22, 214, "đường sức điện trường xoáy: đường cong kín bao quanh đường cảm ứng từ", BLUE, 10.5, "start", "600")
fig2 = wrap("0 0 420 226", "Đường sức từ thẳng đứng có một mũi tên ở đầu trên chỉ chiều, bao quanh là một đường cong kín của điện trường xoáy với hai mũi tên chỉ chiều",
            b, "Hình 2. Từ trường biến thiên sinh điện trường xoáy; đường sức điện trường xoáy là đường cong kín bao quanh các đường cảm ứng từ.")

# ------------------------------------------------- Hình 3: sóng điện từ
b = defs("f3")
b += text(14, 20, "Sóng điện từ: sóng ngang, E và B cùng pha", "currentColor", 12.5, "start", "700")
b += text(210, 92, "phương truyền sóng", "currentColor", 10.5, "middle", "600")
AX, AMP, LAM = 146, 42, 185.0
b += line(30, AX, 404, AX, "currentColor", 2)
b += '<path d="M404,140 L415,146 L404,152 z" fill="currentColor"/>'
e_pts, b_pts = [], []
x = 30.0
while x <= 404:
    s = math.sin(2 * math.pi * (x - 30) / LAM)
    e_pts.append((x, AX - AMP * s))
    bb = 40 * s
    b_pts.append((x + 0.28 * bb, AX + 0.55 * bb))
    x += 2
b += poly(b_pts, BLUE, 2.4)
b += poly(e_pts, RED, 2.6)
x0 = 30 + LAM / 4
b += arrow("f3", "r", x0, AX, x0, AX - AMP, 2.6)
b += arrow("f3", "b", x0, AX, x0 + 0.28 * 40, AX + 0.55 * 40, 2.6)
b += text(x0, AX - AMP - 10, "E", RED, 12.5, "middle", "700")
b += text(x0 + 26, AX + 34, "B", BLUE, 12.5, "start", "700")
b += text(14, 216, "E vuông góc với B, cả hai cùng vuông góc với phương truyền", "currentColor", 10.5, "start", "600")
b += text(14, 232, "E và B cùng pha: hai đường cong cùng cắt trục tại một chỗ", "currentColor", 10.5, "start", "600")
fig3 = wrap("0 0 420 243", "Sóng điện từ lan truyền theo trục ngang: vectơ E dao động thẳng đứng, vectơ B dao động theo phương xiên, hai đường cong cùng pha",
            b, "Hình 3. Sóng điện từ là sóng ngang: E vuông góc với B, cả hai vuông góc phương truyền và luôn cùng pha.")

# ------------------------------------------------- Hình 4: thang sóng điện từ
b = defs("f4")
b += text(14, 18, "Thang sóng điện từ", "currentColor", 12.5, "start", "700")
b += text(406, 18, "bước sóng giảm dần", "currentColor", 10.5, "end", "600")
edges = [30, 125, 180, 225, 280, 335, 400]
names = ["sóng vô tuyến", "hồng ngoại", "ánh sáng nhìn thấy", "tử ngoại", "tia X", "tia gamma"]
for i in range(6):
    x1, x2 = edges[i], edges[i + 1]
    col = BLUE if i == 0 else "currentColor"
    fill = "rgba(56,189,248,.20)" if i == 0 else "rgba(148,163,184,.14)"
    b += rect(x1, 82, x2 - x1, 22, fill, col, 1.6, 3)
cen = [(edges[i] + edges[i + 1]) / 2 for i in range(6)]
for i in (0, 2, 4):
    col = BLUE if i == 0 else "currentColor"
    b += line(cen[i], 56, cen[i], 82, "currentColor", 1, "3 3", .55)
    b += text(cen[i], 50, names[i], col, 10.5, "middle", "700")
for i in (1, 3, 5):
    b += line(cen[i], 72, cen[i], 82, "currentColor", 1, "3 3", .55)
    b += text(cen[i], 66, names[i], "currentColor", 10.5, "middle", "700")
b += text(14, 126, "Ranh giới các vùng: 1 mm · 0,76 μm · 0,38 μm · 10 nm · 0,01 nm", "currentColor", 10, "start", "600")
b += text(14, 144, "Sơ đồ bậc thang: độ rộng các vùng không theo tỉ lệ bước sóng", "currentColor", 10, "start", "600")
b += text(14, 164, "mọi vùng đều là sóng điện từ, truyền trong chân không với cùng tốc độ c", "currentColor", 10.5, "start", "600")
b += text(14, 180, "bước sóng càng nhỏ thì tần số và năng lượng càng lớn", "currentColor", 10.5, "start", "600")
fig4 = wrap("0 0 420 194", "Thang sóng điện từ vẽ theo sơ đồ bậc thang, độ rộng các vùng không theo tỉ lệ bước sóng: sáu vùng xếp theo bước sóng giảm dần gồm vô tuyến, hồng ngoại, ánh sáng nhìn thấy, tử ngoại, tia X, tia gamma",
            b, "Hình 4. Thang sóng điện từ: sáu vùng xếp theo bước sóng giảm dần (sơ đồ bậc thang, độ rộng các vùng không theo tỉ lệ); vùng tô xanh là sóng vô tuyến.",
            exp="tn-l12-dttruong-04")

# ------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
