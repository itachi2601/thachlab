"""Sinh 4 hình SVG cho bài "Sự chuyển thể" (Vật lí 12) và thay các mốc <!--FIGn-->
trong theory.src.html -> theory.html. Chạy từ thư mục này:  python3 build_figs.py"""
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
# thành li + nước (mặt nước y=110); đá nổi, nhô lên khỏi mặt nước
b += '<path d="M150 50 L150 186 Q150 200 166 200 L254 200 Q270 200 270 186 L270 50" fill="none" stroke="currentColor" stroke-width="2.5"/>'
b += '<path d="M152 110 L152 186 Q152 198 166 198 L254 198 Q268 198 268 186 L268 110 Z" fill="rgba(56,189,248,.16)" stroke="none"/>'
b += line(152, 110, 203, 110, BLUE, 1.4) + line(217, 110, 268, 110, BLUE, 1.4)
for x, y, w, h in ((158, 107, 30, 26), (228, 107, 32, 24)):  # ngập ~87 %
    b += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="rgba(56,189,248,.4)" stroke="{BLUE}" stroke-width="1.6"/>'
b += line(114, 90, 156, 110, BLUE, 1.2)
b += text(14, 92, "đá đang tan", BLUE, 14, "start", "700")
# nhiệt kế: ống thẳng, bầu nằm trong nước giữa hai viên đá
b += f'<rect x="204" y="14" width="12" height="150" rx="6" fill="none" stroke="currentColor" stroke-width="2"/>'
b += line(210, 120, 210, 166, RED, 4) + dot(210, 172, 8, RED)
b += text(226, 22, "nhiệt kế", GRN, 14)
b += text(226, 40, "chỉ ? °C", GRN, 16, "start", "700")
# giọt nước ngưng tụ bám ngoài thành li
b += f'<ellipse cx="144" cy="140" rx="4" ry="6" fill="{BLUE}"/>'
b += f'<ellipse cx="143" cy="164" rx="3.4" ry="5" fill="{BLUE}"/>'
b += line(96, 152, 136, 146, BLUE, 1.2)
b += text(14, 148, "hơi nước", BLUE, 14) + text(14, 166, "ngưng tụ", BLUE, 14)
b += arrow("f1", "r", 404, 174, 278, 174, 2.8)
b += text(290, 140, "nhiệt từ", RED, 14) + text(290, 158, "không khí vào", RED, 14)
fig1 = wrap("0 0 420 214", "Li nước đá đang tan có cắm nhiệt kế, ngoài thành li có nước ngưng tụ",
            b, "Hình 1. Không khí nóng truyền nhiệt vào li đá đang tan: nhiệt kế chỉ bao nhiêu? Nước ngoài thành li là hơi nước <em>ngưng tụ</em> khi gặp mặt lạnh.")

# ---------------------------------------------------------------- Hình 2: ảnh OpenStax 14.7 (đợt 2, 27/10/2026)
fig2 = ('<p>Hình 2 đặt ba thể cạnh nhau ở mức phân tử.<sup class="tl-fn"><a href="#tl-fn-1">1</a></sup></p>\n\n'
        '<figure class="fig" data-tl="1"><img src="/assets/openstax/l12-su-chuyen-the/hinh-ba-the-mo-hinh.webp" '
        'alt="Mô hình phân tử của chất rắn, chất lỏng và chất khí, kèm chiều nóng chảy, đông đặc, sôi, ngưng tụ" '
        'loading="lazy" width="875" height="864"><figcaption>Hình 2. Cùng là các phân tử, khác nhau ở <strong>khoảng cách</strong> và <strong>mức trật tự</strong>.<br>'
        'Rắn: phân tử dao động quanh vị trí cố định, nối bằng "lò xo" liên kết.<br>Lỏng: phân tử chuyển động tự do hơn.<br>Khí: phân tử rất xa nhau, bay thẳng.</figcaption></figure>\n'
        '<ol class="tl-fns"><li id="tl-fn-1"><strong>Nhãn trong hình:</strong> Solid = rắn · Liquid = lỏng · Gas = khí · Limits of motion = giới hạn dao động · '
        'Energy input = nhận năng lượng · Energy output = toả năng lượng · Melt = nóng chảy · Freeze = đông đặc · Boil = sôi (hoá hơi) · Condense = ngưng tụ.<br>'
        'Hình: OpenStax, College Physics 2e, Hình 14.7 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</li></ol>')

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
b += text(220, 44, "nóng chảy", RED, 14, "middle", "700")
b += arrow("f3", "b", 286, 86, 154, 86, 2.6)
b += text(220, 106, "đông đặc", BLUE, 14, "middle", "700")
b += arrow("f3", "o", 372, 100, 268, 178, 2.6)
b += text(314, 132, "hoá hơi", ORG, 14, "end", "700")
b += arrow("f3", "b", 292, 178, 392, 100, 2.6)
b += text(344, 170, "ngưng tụ", BLUE, 14, "start", "700")
# thăng hoa (rắn -> khí) và ngưng kết (khí -> rắn): hai nét đứt song song, mỗi chiều một mũi tên chevron
b += f'<path d="M90 98 C 88 170, 108 218, 154 218" fill="none" stroke="{ORG}" stroke-width="2.2" stroke-dasharray="5 4"/>'
b += chevron(158, 218, 44, 0, ORG, 2.2, 9)
b += text(82, 150, "thăng hoa", ORG, 14, "end", "700")
b += f'<path d="M158 203 C 132 200, 114 160, 116 102" fill="none" stroke="{BLUE}" stroke-width="2.2" stroke-dasharray="5 4"/>'
b += chevron(116, 98, 0, -70, BLUE, 2.2, 9)
b += text(136, 166, "ngưng kết", BLUE, 14, "start", "700")
fig3 = wrap("0 0 440 254", "Vòng chuyển thể: nóng chảy, đông đặc, hoá hơi, ngưng tụ, thăng hoa và ngưng kết",
            b, "Hình 3. Bốn quá trình chính đi thành hai cặp ngược chiều. Nét đứt là hai quá trình ít gặp: <strong>thăng hoa</strong> (rắn → hơi) và <strong>ngưng kết</strong> (hơi → rắn).")

# ---------------------------------------------------------------- Hình 4: đồ thị nhiệt độ – thời gian
# c(nước đá) ≈ 2100, c(nước) ≈ 4180 J/(kg.K): cùng công suất, đoạn rắn dốc gấp ~2 đoạn lỏng (1,0 so với 0,5)
b = defs("f4")
b += line(50, 215, 50, 24, "currentColor", 2) + chevron(50, 22, 0, -1, "currentColor", 2, 10)
b += line(50, 215, 424, 215, "currentColor", 2) + chevron(426, 215, 1, 0, "currentColor", 2, 10)
b += text(60, 26, "T (°C)", "currentColor", 14)
b += text(426, 240, "t (phút)", "currentColor", 14, "end")
b += line(50, 125, 420, 125, GRN, 1.2, "5 4", .8)
b += text(40, 130, "0", GRN, 14, "end", "700")
b += poly([(60, 185), (120, 125), (250, 125), (400, 50)], BLUE, 2.6)
b += line(120, 125, 120, 152, RED, 1.2, "4 3", .9)
b += line(250, 125, 250, 152, RED, 1.2, "4 3", .9)
b += dbl_h(120, 250, 152, RED, 1.6)
b += text(185, 174, "thời gian nóng chảy", RED, 14, "middle", "700")
b += text(72, 202, "a: rắn nóng lên", RED, 14, "start", "700")
b += text(125, 92, "b: đang nóng chảy", BLUE, 14, "start", "700")
b += text(125, 110, "nhiệt độ không đổi", BLUE, 14, "start", "500")
b += text(236, 56, "c: lỏng nóng lên", GRN, 14, "start", "700")
b += dot(120, 125, 4, RED) + dot(250, 125, 4, RED)
fig4 = wrap("0 0 440 250", "Đồ thị nhiệt độ theo thời gian khi đun nước đá: đoạn dốc lên, đoạn nằm ngang ở 0 °C, rồi dốc lên tiếp",
            b, "Hình 4. Đồ thị nhiệt độ – thời gian khi đun nước đá.")

# ---------------------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(margin_figs(src))
print("ok", len(src), "bytes")
