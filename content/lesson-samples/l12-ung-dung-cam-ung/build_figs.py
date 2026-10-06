"""Sinh 4 hình SVG cho bài "Bài 15. Một số ứng dụng của cảm ứng điện từ" (Vật lí 12)
và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html.
Chạy từ thư mục này: python3 build_figs.py
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *  # noqa: E402


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1, cap=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    k = f' stroke-linecap="{cap}"' if cap else ""
    o = f' opacity="{op}"' if op != 1 else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d}{k}{o}/>'


def dot(x, y, r=3.5, c="currentColor"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def rect(x, y, w, h, fill="none", stroke="currentColor", sw=2, rx=0, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def ell(cx, cy, rx, ry, c, w=2.4):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{c}" stroke-width="{w}"/>'


def path(d, c, w=2, dash="", marker=""):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#{marker})"' if marker else ""
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}"{ds}{m}/>'


def cross(x, y, r=7, c="currentColor", op=.75):
    """Ký hiệu ⊗ (từ trường hướng vào trang) vẽ bằng nét, không dùng ký tự."""
    k = r * 0.707
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{c}" stroke-width="1.6" opacity="{op}"/>'
            f'<line x1="{x-k:.1f}" y1="{y-k:.1f}" x2="{x+k:.1f}" y2="{y+k:.1f}" stroke="{c}" stroke-width="1.6" opacity="{op}"/>'
            f'<line x1="{x-k:.1f}" y1="{y+k:.1f}" x2="{x+k:.1f}" y2="{y-k:.1f}" stroke="{c}" stroke-width="1.6" opacity="{op}"/>')


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


# ======================================================= Hình 1: pickup guitar (1 dây thép · 2 nam châm · 3 cuộn dây)
b = defs("f1")
b += text(16, 28, "1  dây thép", "currentColor", 14, "start", "600")
b += line(104, 32, 150, 44, "currentColor", 1.3, "", .8)
b += dot(150, 44, 3, "currentColor")
b += line(150, 46, 410, 46, "currentColor", 5, cap="round")
b += arrow("f1", "o", 330, 68, 330, 28, 2.4)
b += arrow("f1", "o", 352, 28, 352, 68, 2.4)
b += text(366, 86, "rung", ORG, 13, "start", "600")
b += rect(150, 86, 120, 118, "none", "currentColor", 2.5, 10)              # cuộn dây
b += rect(186, 104, 48, 82, "none", RED, 2.5)                              # nam châm
b += text(210, 128, "N", RED, 16, "middle", "600")
b += text(210, 172, "S", BLUE, 16, "middle", "600")
b += path("M196 104 Q150 74 168 46", RED, 1.8, "5 4")
b += path("M224 104 Q270 74 252 46", RED, 1.8, "5 4")
b += text(16, 118, "2  nam châm", RED, 14, "start", "600")
b += line(108, 114, 190, 118, RED, 1.3, "", .85)
b += dot(190, 118, 3, RED)
b += text(16, 146, "3  cuộn dây", "currentColor", 14, "start", "600")
b += line(108, 142, 150, 150, "currentColor", 1.3, "", .8)
b += dot(150, 150, 3, "currentColor")
b += arrow("f1", "g", 270, 150, 404, 150, 2)
b += text(278, 172, "vào tăng âm", "currentColor", 13, "start", "600")
b += text(16, 214, "Đường đứt: từ thông qua cuộn", RED, 13, "start", "600")
fig1 = wrap("0 0 430 230", "Đàn guitar điện: dây thép (1) rung phía trên nam châm (2) nằm trong cuộn dây (3), cuộn nối vào máy tăng âm",
            b, "Hình 1. Dây thép (1) bị nam châm (2) từ hoá. Dây rung thì từ thông qua cuộn dây (3) đổi, dòng cảm ứng cùng tần số với dây đi vào máy tăng âm.",
            "tn-l12-udcamung-01")

# ======================================================= Hình 2: sạc không dây
b = defs("f2")
b += rect(28, 16, 230, 78, "none", "currentColor", 2.2, 10)
b += text(40, 36, "điện thoại", "currentColor", 13, "start", "600")
b += ell(78, 62, 30, 16, BLUE)
b += text(118, 58, "cuộn máy", BLUE, 13, "start", "600")
b += text(118, 78, "nối với pin", BLUE, 13, "start", "600")
b += text(140, 118, "không chạm dây", "currentColor", 13, "start", "600")
b += rect(28, 132, 230, 96, "none", "currentColor", 2.2, 10)
b += ell(78, 180, 36, 18, RED)
b += text(124, 172, "cuộn đế sạc", RED, 13, "start", "600")
b += text(124, 194, "điện xoay chiều", RED, 13, "start", "600")
for x in (62, 78, 94):
    b += line(x, 78, x, 162, BLUE, 1.6, "4 4")
b += text(278, 48, "thứ cấp", BLUE, 15, "start", "600")
b += text(278, 70, "nhận suất", "currentColor", 13, "start", "600")
b += text(278, 90, "điện động", "currentColor", 13, "start", "600")
b += text(278, 168, "sơ cấp", RED, 15, "start", "600")
b += text(278, 190, "gây từ thông", "currentColor", 13, "start", "600")
b += text(278, 210, "biến thiên", "currentColor", 13, "start", "600")
fig2 = wrap("0 0 430 246", "Đế sạc và điện thoại: hai cuộn đặt sát, từ thông biến thiên đi từ cuộn sơ cấp sang cuộn thứ cấp",
            b, "Hình 2. Sạc không dây là một biến áp có khe hở: cuộn đế chạy điện xoay chiều, cuộn trong máy nhận suất điện động.",
            "tn-l12-udcamung-02")

# ======================================================= Hình 3: tấm đặc và tấm có rãnh, B vuông góc mặt tấm
b = defs("f3")
b += text(16, 22, "Từ trường B vuông góc mặt tấm, hướng vào trang (dấu ×)", "currentColor", 12.5, "start", "600")
for x0, nhan, nhan2, col in ((16, "tấm đặc", "tắt nhanh", ORG), (226, "tấm có rãnh", "tắt chậm", GRN)):
    b += rect(x0, 34, 188, 150, "none", "currentColor", 1.4, 10, "5 4")        # vùng từ trường
    for cx in (x0 + 18, x0 + 94, x0 + 170):
        for cy in (50, 108, 168):
            b += cross(cx, cy, 7, "currentColor", .55)
    b += rect(x0 + 40, 56, 108, 100, "rgba(148,163,184,.14)", "currentColor", 2.4, 4)   # tấm nhôm
b += path("M127 76.6 A34 34 0 1 1 104 72.5", ORG, 2.6, "", "f3-o")                  # vòng Foucault (tấm đặc)
for x in (276, 308, 340):                                                          # rãnh xẻ ở tấm bên phải
    b += rect(x + 2, 62, 8, 88, "none", "currentColor", 1.6, 2)
b += text(16, 206, "tấm đặc", "currentColor", 14, "start", "600")
b += text(16, 226, "vòng Foucault kín, tắt nhanh", ORG, 13, "start", "600")
b += text(226, 206, "tấm có rãnh", "currentColor", 14, "start", "600")
b += text(226, 226, "rãnh cắt vòng, tắt chậm", GRN, 13, "start", "600")
fig3 = wrap("0 0 430 238", "Tấm nhôm đặc và tấm nhôm xẻ rãnh dao động trong từ trường vuông góc với mặt tấm, hướng vào trang",
            b, "Hình 3. Từ trường B vuông góc với mặt tấm (dấu ×: hướng vào trang) nên từ thông qua tấm đổi khi tấm dao động. Tấm đặc có vòng Foucault kín nên bị hãm mạnh; rãnh cắt vòng đó, tấm đung đưa lâu hơn.",
            "tn-l12-udcamung-04")

# ======================================================= Hình 4: mặt cắt bếp từ
b = defs("f4")
b += path("M70 36 L70 108 L250 108 L250 36", "currentColor", 2.6)
b += path("M58 128 L58 44 L262 44 L262 128 Z", "currentColor", 2)
b += text(160, 78, "nước", "currentColor", 14, "middle", "600")
b += ell(160, 118, 48, 8, ORG)
b += path("M196 114 A20 6 0 0 1 188 122", ORG, 2, "", "f4-o")
b += text(270, 118, "đáy nóng", ORG, 13, "start", "600")
b += line(24, 148, 300, 148, BLUE, 4, cap="round")
b += text(308, 152, "kính", BLUE, 13, "start", "600")
b += ell(160, 190, 56, 18, RED, 2.6)
b += text(230, 186, "cuộn bếp", RED, 13, "start", "600")
b += text(230, 206, "xoay chiều", RED, 13, "start", "600")
b += text(16, 228, "Nhiệt ở đáy nồi, không ở mặt kính", "currentColor", 13, "start", "600")
fig4 = wrap("0 0 430 244", "Mặt cắt bếp từ: cuộn dưới mặt kính, dòng Foucault trong đáy nồi",
            b, "Hình 4. Cuộn bếp tạo từ thông biến thiên. Bài toán mẫu gộp mọi dòng xoáy ở đáy nồi thành một vòng tương đương.",
            "tn-l12-udcamung-05")

# ------------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
