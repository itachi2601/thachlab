"""Sinh 4 hình SVG cho bài "Bài 14. Hạt nhân và mô hình nguyên tử" (Vật lí 12)
và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html.
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


def hop(x, y, w, h, s, c, size=12, fill="rgba(148,163,184,.10)"):
    """Hộp chữ nhật có chữ canh giữa."""
    return rect(x, y, w, h, fill) + text(x + w / 2, y + h / 2 + 4, s, c, size, "middle", "700")


def nuclon(x, y, r=9, kind="p"):
    """Một nuclôn: prôtôn đỏ có dấu +, nơtron xanh không dấu."""
    if kind == "p":
        return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="rgba(248,113,113,.30)" stroke="{RED}" stroke-width="2"/>'
                + text(x, y + 4, "+", RED, 11, "middle", "700"))
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="rgba(56,189,248,.28)" stroke="{BLUE}" stroke-width="2"/>')


def wrap2(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


# ---------------------------------------------- Hình 1: thí nghiệm lá vàng
b = defs("f1")
b += text(14, 24, "Chùm hạt alpha bắn vào lá vàng mỏng", "currentColor", 12, "start", "700")
b += rect(24, 78, 74, 96, "rgba(148,163,184,.10)", "currentColor", 2)
b += hop(36, 108, 50, 34, "nguồn", "currentColor", 10)
# lá vàng
b += rect(232, 62, 11, 128, "rgba(251,146,60,.35)", ORG, 2, 3)
b += text(237, 206, "lá vàng", ORG, 11, "middle", "700")
b += text(237, 220, "mỏng vài nghìn", ORG, 10, "middle", "500")
b += text(237, 232, "nguyên tử", ORG, 10, "middle", "500")
# ba tia: thẳng, lệch, bật ngược
b += arrow("f1", "g", 102, 126, 356, 126, 2.4)
b += text(300, 168, "hầu hết bay thẳng", GRN, 11, "start", "700")
# tia lệch: vào thẳng tới sát hạt nhân rồi gãy khúc lệch lên — không đi xuyên qua hạt nhân
b += (f'<path d="M102,126 L237,104 L404,52" fill="none" stroke="{ORG}" stroke-width="2.4"'
      f' marker-end="url(#f1-o)"/>')
b += text(404, 44, "lệch mạnh: vài hạt", ORG, 11, "end", "700")
b += arrow("f1", "r", 231, 100, 134, 58, 2.6)
b += text(126, 50, "bật ngược", RED, 11, "end", "700")
b += f'<circle cx="237" cy="104" r="7" fill="rgba(248,113,113,.35)" stroke="{RED}" stroke-width="2"/>'
b += text(24, 190, "Một chùm hạt, ba số phận", "currentColor", 10, "start", "500")
fig1 = wrap2("0 0 440 244", "Chùm hạt alpha bắn vào lá vàng: hầu hết bay thẳng, vài hạt lệch mạnh hoặc bật ngược lại",
             b, "Hình 1. Thí nghiệm lá vàng: hạt alpha xuyên qua phần trống bên trong nguyên tử; chỉ hạt đi sát hạt nhân mới bị lệch mạnh hoặc bật ngược.")

# ---------------------------------------------- Hình 2: ba mô hình nguyên tử
b = defs("f2")
for x, t in ((66, "Thomson 1904"), (202, "Rutherford 1911"), (352, "Bohr 1913")):
    b += text(x, 22, t, "currentColor", 11, "middle", "700")
# Thomson: quả cầu đặc
b += f'<circle cx="66" cy="112" r="56" fill="rgba(251,146,60,.16)" stroke="{ORG}" stroke-width="1.8"/>'
for dx, dy in ((-26, -26), (26, -26), (0, 0), (-26, 26), (26, 26)):
    b += dot(66 + dx, 112 + dy, 4, BLUE)
b += text(66, 196, "cầu dương đặc", "currentColor", 10, "middle", "500")
b += text(66, 210, "+ êlectron rải rác", "currentColor", 10, "middle", "500")
# Rutherford
b += f'<circle cx="202" cy="112" r="56" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 5" opacity="0.5"/>'
b += dot(202, 112, 13, RED)
b += text(202, 117, "+", "currentColor", 11, "middle", "700")
b += f'<ellipse cx="202" cy="112" rx="42" ry="42" fill="none" stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="4 4"/>'
b += dot(160, 112, 4, BLUE) + dot(244, 112, 4, BLUE)
b += text(202, 196, "hạt nhân nhỏ, nặng", "currentColor", 10, "middle", "500")
b += text(202, 210, "êlectron quay quanh", "currentColor", 10, "middle", "500")
# Bohr
b += dot(352, 112, 13, RED)
b += text(352, 117, "+", "currentColor", 11, "middle", "700")
b += f'<circle cx="352" cy="112" r="24" fill="none" stroke="{BLUE}" stroke-width="1.8"/>'
b += f'<circle cx="352" cy="112" r="46" fill="none" stroke="{BLUE}" stroke-width="1.8"/>'
b += dot(328, 112, 4.5, BLUE) + dot(352, 66, 4.5, BLUE)
b += text(352, 166, "quỹ đạo cho phép,", "currentColor", 10, "middle", "500")
b += text(352, 180, "có năng lượng xác định", "currentColor", 10, "middle", "500")
b += text(16, 238, "Nguyên tử gần như trống: hạt nhân chiếm một phần mười nghìn tỉ thể tích", "currentColor", 10, "start", "500")
fig2 = wrap2("0 0 440 250", "Ba mô hình nguyên tử đặt cạnh nhau: Thomson cầu đặc, Rutherford có hạt nhân nhỏ ở giữa, Bohr thêm các quỹ đạo cho phép",
             b, "Hình 2. Ba mô hình nguyên tử: Thomson (cầu dương đặc) bị thí nghiệm lá vàng bác bỏ; Rutherford có hạt nhân nhỏ, nặng, mang điện dương; Bohr thêm điều kiện êlectron chỉ ở các quỹ đạo xác định.")

# ---------------------------------------------- Hình 3: kí hiệu hạt nhân
b = defs("f3")
b += text(14, 26, "Đọc kí hiệu hạt nhân", "currentColor", 12, "start", "700")
b += text(210, 118, "Cu", "currentColor", 40, "start", "700")
b += text(204, 102, "65", RED, 24, "end", "700")
b += text(204, 140, "29", BLUE, 24, "end", "700")
b += text(232, 162, "kí hiệu hoá học", "currentColor", 10, "middle", "500")
b += arrow("f3", "r", 124, 94, 170, 94, 1.8)
b += text(14, 90, "A = số nuclôn", RED, 12, "start", "700")
b += text(14, 106, "= prôtôn + nơtron", RED, 10, "start", "500")
b += arrow("f3", "b", 124, 132, 170, 132, 1.8)
b += text(14, 128, "Z = số prôtôn", BLUE, 12, "start", "700")
b += text(14, 144, "= điện tích hạt nhân", BLUE, 10, "start", "500")
b += text(14, 212, "Ví dụ: Cu có 29 prôtôn, 65 nuclôn nên có 65 − 29 = 36 nơtron", "currentColor", 11, "start", "600")
b += text(14, 230, "Cùng 29 prôtôn mà khác số nơtron thì gọi là hai đồng vị", "currentColor", 11, "start", "600")
fig3 = wrap2("0 0 440 244", "Kí hiệu hạt nhân đồng: chỉ số trên là số nuclôn A, chỉ số dưới là số prôtôn Z",
             b, "Hình 3. Kí hiệu hạt nhân $^A_Z X$: trên là số nuclôn $A$, dưới là số prôtôn $Z$ (điện tích hạt nhân); $N = A - Z$.")

# ---------------------------------------------- Hình 4: vạch quang phổ của hai đồng vị hiđrô
b = defs("f4")
b += text(14, 20, "Hai đồng vị hiđrô, hai bộ vạch quang phổ", "currentColor", 12, "start", "700")
b += text(14, 36, "cùng một nguyên tố, cùng số prôtôn, khác số nơtron", "currentColor", 10, "start", "500")
b += text(258, 52, "bước sóng (nm)", "currentColor", 10, "middle", "600")
b += line(104, 90, 412, 90, "currentColor", 2, "", .5)
for wl in (400, 500, 600, 700):
    x = 104 + (wl - 400) * 308 / 300
    b += line(x, 86, x, 94, "currentColor", 1.4, "", .8)
    b += text(x, 78, f"{wl}", "currentColor", 10, "middle", "500")
# phổ hiđrô
b += text(96, 126, "H", RED, 15, "end", "700")
b += text(96, 142, "1 prôtôn", RED, 9, "end", "500")
b += line(104, 132, 412, 132, "currentColor", 1, "", .3)
for wl, nhan, c in ((486.1, "486,1", BLUE), (656.3, "656,3", RED)):
    x = 104 + (wl - 400) * 308 / 300
    b += line(x, 116, x, 148, c, 3)
    b += text(x, 164, nhan, c, 9, "middle", "600")
# phổ đơteri: hạt nhân nặng hơn nên vạch dịch về bước sóng NGẮN hơn (bên trái vạch H)
b += text(96, 210, "D", BLUE, 15, "end", "700")
b += text(96, 226, "1 p + 1 n", BLUE, 9, "end", "500")
b += line(104, 216, 412, 216, "currentColor", 1, "", .3)
for wl, nhan, c in ((486.0, "486,0", BLUE), (656.1, "656,1", RED)):
    x = 104 + (wl - 400) * 308 / 300
    b += line(x, 200, x, 232, c, 3)
    b += text(x, 248, nhan, c, 9, "middle", "600")
b += text(16, 268, "Vạch D lệch về phía bước sóng ngắn hơn: ~0,2 nm ở Hα, ~0,1 nm ở Hβ", "currentColor", 10, "start", "500")
fig4 = wrap2("0 0 440 278", "So sánh hai bộ vạch quang phổ của hiđrô và đơteri: các vạch nằm gần cùng vị trí, vạch của đơteri hơi dịch về phía bước sóng ngắn hơn",
             b, "Hình 4. Hai đồng vị hiđrô: hiđrô và đơteri cho hai bộ vạch quang phổ gần giống nhau, chỉ lệch chút ít — vạch của đơteri dịch về phía bước sóng ngắn hơn (0,2 nm ở Hα, 0,1 nm ở Hβ).")

# ---------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
