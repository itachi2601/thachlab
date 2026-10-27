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
b += line(218, 20, 218, 158, "currentColor", 2.5) + dot(218, 158, 5, RED)
b += text(228, 24, "nhiệt kế", GRN, 12)
b += text(228, 42, "chỉ ? °C", GRN, 14, "start", "700")
b += f'<ellipse cx="146" cy="150" rx="4" ry="6" fill="{BLUE}"/>'
b += f'<ellipse cx="143" cy="172" rx="3.4" ry="5" fill="{BLUE}"/>'
b += text(14, 146, "hơi nước", BLUE, 12) + text(14, 162, "ngưng tụ", BLUE, 12)
b += arrow("f1", "r", 372, 176, 276, 176, 3)
b += text(276, 166, "nhiệt từ không khí vào", RED, 11)
fig1 = wrap("0 0 420 250", "Li nước đá đang tan có cắm nhiệt kế, ngoài thành li có nước ngưng tụ",
            b, "Hình 1. Không khí nóng truyền nhiệt vào li đá đang tan: nhiệt kế chỉ bao nhiêu? Nước ngoài thành li là hơi nước <em>ngưng tụ</em> khi gặp mặt lạnh.")

# ---------------------------------------------------------------- Hình 2: ảnh OpenStax 14.7 (đợt 2, 27/10/2026)
fig2 = ('<p>Hình 2 đặt ba thể cạnh nhau ở mức phân tử.<sup class="tl-fn"><a href="#tl-fn-1">1</a></sup></p>\n\n'
        '<figure class="fig" data-tl="1"><img src="/assets/openstax/l12-su-chuyen-the/hinh-ba-the-mo-hinh.webp" '
        'alt="Mô hình phân tử của chất rắn, chất lỏng và chất khí, kèm chiều nóng chảy, đông đặc, sôi, ngưng tụ" '
        'loading="lazy" width="875" height="864"><figcaption>Hình 2. Cùng là các phân tử, khác nhau ở <strong>khoảng cách</strong> và <strong>mức trật tự</strong>.<br>'
        'Rắn: phân tử dao động quanh vị trí cố định, nối bằng "lò xo" liên kết. Lỏng: phân tử chuyển động tự do hơn. Khí: phân tử rất xa nhau, bay thẳng.</figcaption></figure>\n'
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
            b, "Hình 4. Đồ thị nhiệt độ – thời gian khi đun nước đá.")

# ---------------------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
