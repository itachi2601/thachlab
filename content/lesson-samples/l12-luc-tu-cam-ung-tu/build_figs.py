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


# Màu thân nam châm chữ U (mặt trước / mặt trên / mặt bên tối hơn) và hai cực
EDGE = "#1e293b"
G_FR, G_TOP, G_SIDE = "#cbd5e1", "#e2e8f0", "#94a3b8"
N_FR, N_TOP, N_SIDE = "#dc2626", "#f87171", "#b91c1c"
S_FR, S_TOP, S_SIDE = "#2563eb", "#60a5fa", "#1e40af"


def poly(pts, fill, sw=1.5):
    d = " ".join(f"{x:g},{y:g}" for x, y in pts)
    return f'<polygon points="{d}" fill="{fill}" stroke="{EDGE}" stroke-width="{sw}" stroke-linejoin="round"/>'


def pathf(d, fill, sw=1.5, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{EDGE}" stroke-width="{sw}" stroke-linejoin="round"{extra}/>'


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


# ------------------------------------------------- Hình 1: dây dẫn trong khe nam châm chữ U
# Nam châm chữ U nằm ngang, miệng khe quay về phía người xem, gông ở phía sau (chiếu xiên: z sâu → (+0,6z, −0,3z)).
# Cánh trên đầu cực N (y 50–86), cánh dưới đầu cực S (y 174–210); khe y 86–174; B hướng xuống N → S.
# I sang phải (+x), B xuống (−y) ⇒ F = Il × B hướng vào mặt phẳng hình vẽ (⊗). Phần dây trong khe x 90–290, trung điểm x = 190.
b = defs("f1")
b += poly([(138, 62), (338, 62), (338, 150), (138, 150)], G_TOP)                      # vách gông (đáy khe)
b += poly([(114, 162), (314, 162), (338, 150), (138, 150)], G_TOP)                    # mặt trên cánh dưới, phần xám
b += poly([(90, 174), (290, 174), (314, 162), (114, 162)], S_TOP)                     # mặt trên cánh dưới, đầu cực S
b += poly([(114, 38), (314, 38), (341.6, 24.2), (141.6, 24.2)], G_TOP)                # mặt trên cánh trên, phần xám
b += poly([(90, 50), (290, 50), (314, 38), (114, 38)], N_TOP)                         # mặt trên cánh trên, đầu cực N
b += pathf("M290,50 L341.6,24.2 Q356,17 356,41 L356,153 Q356,177 341.6,184.2 L290,210 "
           "L290,174 L338,150 L338,62 L290,86 Z", G_SIDE)                             # mặt bên: hình chữ U, góc bo
b += poly([(290, 50), (314, 38), (314, 74), (290, 86)], N_SIDE)
b += poly([(290, 174), (314, 162), (314, 198), (290, 210)], S_SIDE)
b += pathf("M90,50 H290 V86 H90 Z", N_FR) + text(190, 75, "N", "#ffffff", 20, "middle", "800")
b += pathf("M90,174 H290 V210 H90 Z", S_FR) + text(190, 199, "S", "#ffffff", 20, "middle", "800")
b += field_line(140, 92, 140, 148, BLUE, 2.4)                                   # đường sức B (N → S)
b += field_line(240, 92, 240, 148, BLUE, 2.4)
b += text(150, 110, "B", "#1d4ed8", 15, "start", "700")
b += line(16, 130, 404, 130, "#ffffff", 9)                                      # viền trắng: dây đi PHÍA TRƯỚC gông
b += line(16, 130, 404, 130, "currentColor", 3.5)                               # dây dẫn
b += arrow("f1", "o", 26, 130, 76, 130, 3)
b += text(46, 118, "I", "#c2410c", 15, "middle", "700")
b += f'<circle cx="190" cy="130" r="16" fill="#ffffff" stroke="none"/>'
b += vao(190, 130, 14, RED)                                                     # lực từ F (vào trong)
b += text(210, 122, "F", "#b91c1c", 15, "start", "700")
fig1 = wrap("0 0 420 230", "Đoạn dây mang dòng điện đặt giữa hai cực nam châm chữ U, đường sức từ hướng xuống, lực từ hướng vuông góc vào trong mặt phẳng hình vẽ",
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
# Nam châm chữ U đứng trên cân, nhìn chính diện, chiều sâu chiếu xiên (+22, −14).
# Cánh trái đầu cực N, cánh phải đầu cực S (đầu cực y 70–164); B nằm ngang N → S.
# Dây MN là thanh đồng nằm dọc trục nhìn (M phía sau, N phía trước): dòng M → N hướng ra (⊙).
# I ra (+z), B sang phải (+x) ⇒ F = Il × B hướng lên. F và F' (dây đẩy nam châm) cùng độ lớn → cùng dài 50 px.
U = ("M110,70 L170,70 L170,190 Q170,204 184,204 L256,204 Q270,204 270,190 L270,70 L330,70 "
     "L330,232 Q330,262 300,262 L140,262 Q110,262 110,232 Z")
b += rect(90, 264, 260, 40, "rgba(148,163,184,.12)", "currentColor", 2, 6)      # cân
b += rect(186, 273, 68, 22, "none", "currentColor", 1.5, 3)
b += text(220, 290, "cân", "currentColor", 14, "middle", "700")
b += pathf(U, G_SIDE, 1.5, ' transform="translate(22,-14)"')                   # mặt sau (chiều sâu)
b += poly([(330, 164), (352, 150), (352, 218), (330, 232)], G_SIDE)             # mặt bên cánh phải
b += poly([(330, 70), (352, 56), (352, 150), (330, 164)], S_SIDE)
b += poly([(170, 164), (192, 150), (192, 190), (170, 204)], G_SIDE)             # mặt trong cánh trái (nhìn thấy)
b += poly([(170, 70), (192, 56), (192, 150), (170, 164)], N_SIDE)
b += poly([(170, 204), (270, 204), (292, 190), (192, 190)], G_TOP)              # mặt trên gông (đáy khe)
b += poly([(110, 70), (170, 70), (192, 56), (132, 56)], N_TOP)                  # mặt trên hai đầu cực
b += poly([(270, 70), (330, 70), (352, 56), (292, 56)], S_TOP)
b += pathf(U, G_FR)                                                             # mặt trước thân chữ U
b += pathf("M110,70 H170 V164 H110 Z", N_FR) + text(140, 124, "N", "#ffffff", 20, "middle", "800")
b += pathf("M270,70 H330 V164 H270 Z", S_FR) + text(300, 124, "S", "#ffffff", 20, "middle", "800")
b += field_line(196, 148, 264, 148, BLUE, 2.4)                                  # đường sức nét đứt N → S
b += field_line(196, 162, 264, 162, BLUE, 2.4)
b += text(230, 182, "B", "#1d4ed8", 15, "middle", "700")
# dây MN: thanh đồng từ M (sau, 247,87) tới N (trước, 193,121)
b += '<line x1="247" y1="87" x2="203" y2="114.7" stroke="#92400e" stroke-width="8" stroke-linecap="round"/>'
b += '<line x1="246" y1="85" x2="204" y2="111.7" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round"/>'
b += chevron(214, 108, -27, 17, "#ffffff", 7) + chevron(214, 108, -27, 17, "#c2410c", 3)   # viền trắng cho nổi trên dây                                       # dòng điện M → N
b += text(206, 98, "I", "#c2410c", 15, "middle", "700")
b += text(200, 134, "đầu N", "currentColor", 14, "start", "700")
b += text(254, 84, "M", "currentColor", 14, "start", "700")
b += arrow("f3", "r", 226, 92, 226, 42, 3)                                     # F lên dây (50 px)
b += text(236, 52, "F", "#b91c1c", 15, "start", "700")
b += arrow("f3", "r", 220, 208, 220, 258, 3)                                    # F' dây đẩy nam châm (50 px)
b += text(230, 244, "F′", "#b91c1c", 15, "start", "700")
b += text(16, 24, "dây MN giữ cố định", "currentColor", 14, "start", "600")
b += text(16, 46, "dòng M → N: hướng ra (⊙)", "#c2410c", 14, "start", "700")
fig3 = wrap("0 0 440 312", "Nam châm chữ U đặt trên cân, cực N bên trái, cực S bên phải, đường sức nằm ngang từ N sang S; dây MN giữ cố định nằm ngang trong khe, dòng điện hướng ra phía người xem; lực từ lên dây hướng lên, lực dây đẩy nam châm hướng xuống",
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
