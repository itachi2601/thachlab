"""Sinh 4 hình SVG cho bài "Bài 10. Lực từ. Cảm ứng từ" (Vật lí 12) và thay các mốc
<!--FIGn--> trong theory.src.html -> theory.html. Chạy từ thư mục này: python3 build_figs.py

Quy ước màu dùng chung cả bài: đỏ = lực từ F · cam = dòng điện I · xanh dương = cảm ứng từ B
(chỉ dùng chữ và nét bằng currentColor cho vật thể).
"""
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


def rect(x, y, w, h, fill, stroke="currentColor", sw=2, rx=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def vao(x, y, r=14, c=BLUE):
    """Kí hiệu ⊗: vectơ hướng vào trong mặt phẳng hình vẽ."""
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{c}" stroke-width="2.5"/>'
            f'<line x1="{x - r * 0.7:.0f}" y1="{y - r * 0.7:.0f}" x2="{x + r * 0.7:.0f}" y2="{y + r * 0.7:.0f}" stroke="{c}" stroke-width="2.5"/>'
            f'<line x1="{x + r * 0.7:.0f}" y1="{y - r * 0.7:.0f}" x2="{x - r * 0.7:.0f}" y2="{y + r * 0.7:.0f}" stroke="{c}" stroke-width="2.5"/>')


def ellipse(cx, cy, rx, ry, c=BLUE, w=2, fill="none"):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{c}" stroke-width="{w}"/>'


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


# ------------------------------------------------- Hình 1: dây dẫn trong khe nam châm chữ U
b = defs("f1")
b += rect(96, 30, 228, 30, "rgba(148,163,184,.16)", "currentColor", 2, 8)       # cực N
b += rect(96, 190, 228, 30, "rgba(148,163,184,.16)", "currentColor", 2, 8)      # cực S
b += text(210, 52, "N", "currentColor", 16, "middle", "700")
b += text(210, 212, "S", "currentColor", 16, "middle", "700")
b += field_line(150, 68, 150, 184, BLUE, 2.2)                                   # đường sức B
b += field_line(300, 68, 300, 184, BLUE, 2.2)
b += text(160, 88, "B", BLUE, 14, "start", "700")
b += line(30, 120, 390, 120, "currentColor", 3.5)                               # dây dẫn
b += arrow("f1", "o", 58, 120, 108, 120, 3)
b += text(78, 108, "I", ORG, 14, "middle", "700")
b += vao(210, 120, 14, RED)                                                     # lực từ F (vào trong)
b += text(232, 116, "F", RED, 14, "start", "700")
fig1 = wrap("0 0 420 260", "Đoạn dây mang dòng điện đặt giữa hai cực nam châm chữ U, đường sức từ hướng xuống, lực từ hướng vuông góc vào trong mặt phẳng hình vẽ",
            b, "Hình 1. Dây trong khe nam châm: B hướng xuống, F hướng vào mặt phẳng hình vẽ (⊗).")

# ------------------------------------------------- Hình 2: quy tắc bàn tay trái
# Lòng bàn tay hướng về người xem, bốn ngón sang phải, ngón cái thẳng lên (vuông góc 90°).
b = defs("f2")
b += (
    '<path d="M120,278'
    ' C78,276 46,250 46,214 L46,168'
    ' C46,148 78,136 100,128'
    ' C92,80 108,36 132,26'
    ' C156,16 170,40 160,72'
    ' C152,100 158,114 176,118'
    ' L332,118 A16,16 0 0 1 332,150'
    ' L200,150 L176,150 L176,164 L200,164'
    ' L364,164 A16,16 0 0 1 364,196'
    ' L200,196 L176,196 L176,210 L200,210'
    ' L326,210 A15,15 0 0 1 326,240'
    ' L200,240 L176,240 L176,252 L200,252'
    ' L300,252 A13,13 0 0 1 300,278'
    ' L120,278 Z"'
    ' fill="rgba(148,163,184,.16)" stroke="currentColor" stroke-width="2.5"'
    ' stroke-linejoin="round" stroke-linecap="round"/>'
)
b += vao(118, 208, 15, BLUE)                                                    # B xuyên vào lòng bàn tay
b += text(146, 214, "B", BLUE, 16, "start", "700")
b += arrow("f2", "r", 138, 100, 138, -26, 3.2)                                   # F: dọc ngón cái, hướng lên
b += text(150, -10, "F", RED, 16, "start", "700")
b += arrow("f2", "o", 46, 300, 386, 300, 3.2)                                   # I: cổ tay → đầu ngón
b += text(398, 306, "I", ORG, 16, "start", "700")
b += text(216, 324, "cổ tay → ngón tay", ORG, 15, "middle", "600")
fig2 = wrap("0 -36 460 376", "Bàn tay trái duỗi thẳng, lòng bàn tay hướng về phía người xem: đường sức từ xuyên vào lòng bàn tay, chiều từ cổ tay đến ngón tay theo dòng điện, ngón cái chỉ chiều lực từ",
            b, "Hình 2. Quy tắc bàn tay trái.")

# ------------------------------------------------- Hình 3: cân dòng điện (bố trí đề 2025 câu II.2)
# Nhìn chính diện: cực N trái, cực S phải, B nằm ngang N → S; dây MN nhìn đầu, dòng M (sau) → N (trước) = ⊙.
# F lên dây hướng lên; phản lực F' dây đẩy nam châm hướng xuống → cân tăng.
b = defs("f3")
# Cặp lực – phản lực F và F' cùng độ lớn → vẽ cùng dài 50 px.
b += rect(100, 252, 240, 40, "rgba(148,163,184,.10)", "currentColor", 2, 6)     # cân
b += rect(186, 261, 68, 22, "none", "currentColor", 1.5, 3)
b += text(220, 278, "cân", "currentColor", 14, "middle", "700")
b += rect(130, 190, 180, 60, "rgba(148,163,184,.16)", "currentColor", 2, 6)     # đế nam châm chữ U
b += rect(130, 80, 52, 110, "rgba(148,163,184,.16)", "currentColor", 2, 6)      # cực N
b += rect(258, 80, 52, 110, "rgba(148,163,184,.16)", "currentColor", 2, 6)      # cực S
b += text(156, 142, "N", "currentColor", 18, "middle", "700")
b += text(284, 142, "S", "currentColor", 18, "middle", "700")
b += field_line(186, 98, 254, 98, BLUE, 2.2)                                    # đường sức nét đứt N → S
b += field_line(186, 176, 254, 176, BLUE, 2.2)
b += text(190, 122, "B", BLUE, 14, "start", "700")
b += f'<circle cx="220" cy="140" r="11" fill="none" stroke="{ORG}" stroke-width="2.5"/>' + dot(220, 140, 3.5, ORG)   # ⊙ dòng ra
b += text(236, 146, "I", ORG, 15, "start", "700")
b += arrow("f3", "r", 220, 126, 220, 76, 3)                                     # F lên dây (50 px)
b += text(230, 80, "F", RED, 15, "start", "700")
b += arrow("f3", "r", 220, 196, 220, 246, 3)                                    # F' dây đẩy nam châm (50 px)
b += text(230, 230, "F′", RED, 15, "start", "700")
b += text(16, 28, "dây MN giữ cố định", "currentColor", 14, "start", "600")
b += text(16, 50, "dòng M → N: hướng ra (⊙)", ORG, 14, "start", "600")
fig3 = wrap("0 0 440 304", "Nam châm chữ U đặt trên cân, cực N bên trái, cực S bên phải, đường sức nằm ngang từ N sang S; dây MN giữ cố định nằm ngang trong khe, dòng điện hướng ra phía người xem; lực từ lên dây hướng lên, lực dây đẩy nam châm hướng xuống",
            b, "Hình 3. Cân dòng điện.")

# ------------------------------------------------- Hình 4a/4b/4c: ảnh OpenStax College Physics 2e (đợt 2, 27/10/2026)
# Chèn trực tiếp Hình 22.37, 22.38, 22.39 (CC BY-NC-SA 4.0), không vẽ lại.
def raster(file, alt, cap, w, h, hinh):
    return (f'<figure class="fig" data-tl="1"><img src="{P}{file}" alt="{alt}" loading="lazy" width="{w}" height="{h}">'
            f'<figcaption>{cap}<br><small>Hình: OpenStax, College Physics 2e, Hình {hinh} — CC BY‑NC‑SA 4.0 — '
            f'openstax.org/books/college-physics-2e</small></figcaption></figure>')


P = "/assets/openstax/l12-luc-tu-cam-ung-tu/"
fig4a = raster("hinh-day-thang-duong-suc-tron.webp",
               "Dây thẳng đứng mang dòng điện I hướng lên; các đường sức từ là những đường tròn đồng tâm quanh dây, nằm trong mặt phẳng ngang, mũi tên ngược chiều kim đồng hồ nhìn từ trên xuống; các kim la bàn xếp dọc theo đường tròn",
               "Hình 4a. Dây thẳng: đường sức tròn.",
               624, 440, "22.37a")
fig4b = raster("hinh-vong-day-duong-suc.webp",
               "Vòng dây tròn nhìn nghiêng mang dòng điện I; đường sức từ đi lên qua lòng vòng dây, vòng ra ngoài rồi quay xuống, giống đường sức của nam châm thẳng",
               "Hình 4b. Vòng dây: đường sức xuyên qua vòng.",
               360, 525, "22.38b")
fig4c = raster("hinh-ong-day-duong-suc.webp",
               "Mặt cắt ống dây dài: dòng điện đi vào trang ở hàng vòng trên (dấu X) và đi ra khỏi trang ở hàng vòng dưới (dấu chấm); trong lòng ống các đường sức xanh song song, cách đều, đi từ cực S sang cực N; bên ngoài khép kín như nam châm thẳng",
               "Hình 4c. Ống dây: trong lòng ống đường sức song song, cách đều.<br>"
               "I<sub>in</sub> = dòng vào trang (⊗).<br>I<sub>out</sub> = dòng ra (⊙).",
               425, 440, "22.39b")

# ------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in (("1", fig1), ("2", fig2), ("3", fig3), ("4A", fig4a), ("4B", fig4b), ("4C", fig4c)):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(margin_figs(src))
print("ok", len(src), "bytes")
