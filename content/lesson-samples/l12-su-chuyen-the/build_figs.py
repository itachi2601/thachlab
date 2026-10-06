"""Sinh 4 hình SVG cho bài "Sự chuyển thể" (Vật lí 12) và thay các mốc <!--FIGn-->
trong theory.src.html -> theory.html. Chạy từ thư mục này:  python3 build_figs.py"""
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


def circle(x, y, r=7, c="currentColor", w=2):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{c}" stroke-width="{w}"/>'


def poly(pts, c, w=2, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline fill="none" stroke="{c}" stroke-width="{w}"{d} points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>'


def dbl_h(x1, x2, y, c, w=1.6):
    b = line(x1, y, x2, y, c, w)
    b += f'<path d="M{x1+7},{y-4} L{x1},{y} L{x1+7},{y+4}" fill="none" stroke="{c}" stroke-width="{w}"/>'
    b += f'<path d="M{x2-7},{y-4} L{x2},{y} L{x2-7},{y+4}" fill="none" stroke="{c}" stroke-width="{w}"/>'
    return b


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


# ---------------------------------------------------------------- Hình 1: li nước đá
b = defs("f1")
b += '<path d="M150 58 L150 182 Q150 196 166 196 L254 196 Q270 196 270 182 L270 58" fill="none" stroke="currentColor" stroke-width="2.5"/>'
b += '<path d="M152 128 L152 182 Q152 194 166 194 L254 194 Q268 194 268 182 L268 128 Z" fill="rgba(56,189,248,.16)" stroke="none"/>'
for x, y, w, h in ((166, 142, 28, 24), (200, 136, 30, 28), (234, 144, 26, 22)):
    b += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="rgba(56,189,248,.4)" stroke="{BLUE}" stroke-width="1.6"/>'
b += text(160, 234, "đá đang tan", BLUE, 12, "start", "700")
b += line(218, 74, 218, 158, "currentColor", 2.5) + dot(218, 158, 5, RED)
b += text(228, 82, "nhiệt kế", GRN, 12)
b += text(228, 100, "chỉ 0 °C", GRN, 14, "start", "700")
b += f'<ellipse cx="146" cy="150" rx="4" ry="6" fill="{BLUE}"/>'
b += f'<ellipse cx="143" cy="172" rx="3.4" ry="5" fill="{BLUE}"/>'
b += text(14, 146, "hơi nước", BLUE, 12) + text(14, 162, "ngưng tụ", BLUE, 12)
b += arrow("f1", "r", 372, 176, 276, 176, 3)
b += text(276, 166, "nhiệt từ không khí vào", RED, 11)
fig1 = wrap("0 0 420 250", "Li nước đá đang tan: nhiệt kế chỉ 0 °C, ngoài thành li có nước ngưng tụ",
            b, "Hình 1. Đá tan dần mà nhiệt kế vẫn đứng ở 0 °C, dù không khí nóng vẫn truyền nhiệt vào li. Nước ngoài thành li là hơi nước trong không khí <em>ngưng tụ</em> khi gặp mặt lạnh.")

# ---------------------------------------------------------------- Hình 2: ba thể
b = defs("f2")
panels = (
    (12, "RẮN", RED, "gần nhau, trật tự",
     [(47, 75), (77, 75), (107, 75), (47, 105), (77, 105), (107, 105), (47, 135), (77, 135), (107, 135)]),
    (152, "LỎNG", BLUE, "kém trật tự",
     [(178, 72), (209, 64), (238, 78), (188, 100), (219, 96), (243, 112), (180, 132), (211, 134), (239, 142)]),
    (292, "KHÍ", GRN, "rất xa, hỗn loạn",
     [(316, 66), (378, 54), (328, 120), (392, 124), (356, 158)]),
)
for px, ten, col, mota, chấm in panels:
    b += f'<rect x="{px}" y="34" width="130" height="142" rx="8" fill="rgba(148,163,184,.08)" stroke="currentColor" stroke-width="1.5"/>'
    b += text(px + 65, 24, ten, col, 14, "middle", "700")
    for x, y in chấm:
        b += circle(x, y)
    b += text(px + 65, 196, mota, "currentColor", 11, "middle", "500")
# mũi tên chuyển động cho thể khí
b += arrow("f2", "g", 322, 78, 358, 70, 1.6, "4 3")
b += arrow("f2", "g", 334, 132, 372, 128, 1.6, "4 3")
b += arrow("f2", "g", 362, 150, 396, 132, 1.6, "4 3")
fig2 = wrap("0 0 440 212", "Ba thể của chất: rắn sắp xếp trật tự và ở gần nhau, lỏng kém trật tự, khí rất xa nhau và chuyển động hỗn loạn",
            b, "Hình 2. Cùng là các phân tử, khác nhau ở <strong>khoảng cách</strong> và <strong>mức trật tự</strong>: rắn gần – trật tự, lỏng kém trật tự, khí rất xa – hỗn loạn.")

# ---------------------------------------------------------------- Hình 3: vòng chuyển thể
b = defs("f3")


def hop(x, y, w, h, ten, col):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="rgba(148,163,184,.1)" stroke="{col}" stroke-width="2"/>'
    s += text(x + w / 2, y + h / 2 + 6, ten, col, 15, "middle", "700")
    return s


b += hop(30, 50, 120, 46, "RẮN", RED)
b += hop(290, 50, 120, 46, "LỎNG", BLUE)
b += hop(160, 180, 120, 46, "KHÍ", GRN)
b += arrow("f3", "r", 154, 62, 286, 62, 2.6)
b += text(220, 44, "nóng chảy", RED, 12, "middle", "700")
b += arrow("f3", "b", 286, 86, 154, 86, 2.6)
b += text(220, 106, "đông đặc", BLUE, 12, "middle", "700")
b += arrow("f3", "o", 372, 100, 268, 178, 2.6)
b += text(150, 148, "hoá hơi", ORG, 12, "start", "700")
b += arrow("f3", "b", 292, 178, 392, 100, 2.6)
b += text(298, 214, "ngưng tụ", BLUE, 12, "start", "700")
b += f'<path d="M92 98 C 92 158, 112 202, 156 203" fill="none" stroke="{ORG}" stroke-width="2.2" stroke-dasharray="5 4" marker-end="url(#f3-o)"/>'
b += text(14, 240, "thăng hoa ⇄ ngưng kết (bỏ qua thể lỏng)", ORG, 11, "start", "500")
fig3 = wrap("0 0 440 254", "Vòng chuyển thể: nóng chảy, đông đặc, hoá hơi, ngưng tụ, thăng hoa và ngưng kết",
            b, "Hình 3. Bốn quá trình chính đi thành hai cặp ngược chiều. Nét đứt là hai quá trình ít gặp: <strong>thăng hoa</strong> (rắn → hơi) và <strong>ngưng kết</strong> (hơi → rắn).")

# ---------------------------------------------------------------- Hình 4: đồ thị nhiệt độ – thời gian
b = defs("f4")
b += line(50, 30, 50, 210, "currentColor", 2)      # trục tung
b += line(50, 210, 420, 210, "currentColor", 2)    # trục hoành
b += text(20, 24, "T (°C)", "currentColor", 12)
b += text(360, 230, "t (phút)", "currentColor", 12)
b += line(50, 120, 420, 120, GRN, 1.2, "5 4", .8)
b += text(24, 124, "0", GRN, 12, "start", "700")
b += poly([(60, 150), (140, 120), (250, 120), (400, 60)], BLUE, 2.6)
b += line(140, 120, 140, 150, RED, 1.2, "4 3", .9)
b += line(250, 120, 250, 150, RED, 1.2, "4 3", .9)
b += dbl_h(140, 250, 152, RED, 1.6)
b += text(195, 170, "thời gian nóng chảy", RED, 11, "middle", "700")
b += text(56, 198, "a: rắn nóng lên", RED, 11)
b += text(150, 94, "b: đang nóng chảy", BLUE, 11, "start", "700")
b += text(150, 110, "nhiệt độ không đổi", BLUE, 11, "start", "500")
b += text(292, 58, "c: lỏng nóng lên", GRN, 11, "start", "700")
b += dot(140, 120, 4, RED) + dot(250, 120, 4, RED)
fig4 = wrap("0 0 440 244", "Đồ thị nhiệt độ theo thời gian khi đun nước đá: đoạn dốc lên, đoạn nằm ngang ở 0 °C, rồi dốc lên tiếp",
            b, "Hình 4. Đồ thị nhiệt độ – thời gian. Đoạn <strong>nằm ngang</strong> ở 0 °C là lúc nước đá đang nóng chảy: nhiệt độ không đổi, độ dài đoạn cho biết thời gian nóng chảy.")

# ---------------------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
