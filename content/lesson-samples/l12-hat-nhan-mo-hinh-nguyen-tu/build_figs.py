"""Sinh 4 hình SVG cho bài "Bài 14. Hạt nhân và mô hình nguyên tử" (Vật lí 12)
và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html.
Chạy từ thư mục này: python3 build_figs.py
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


# ---------------------------------------------- Hình 1: thí nghiệm lá vàng (ảnh OpenStax, đợt 2 27/10/2026)
fig1 = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l12-hat-nhan-mo-hinh-nguyen-tu/hinh-tan-xa-alpha.webp" '
        'alt="Thí nghiệm lá vàng: nguồn hạt alpha bắn vào lá vàng đặt giữa màn hình trụ; bên phải, hầu hết hạt xuyên thẳng qua các nguyên tử, vài hạt lệch hoặc bật ngược khi gặp hạt nhân" '
        'loading="lazy" width="1000" height="481"><figcaption>Hình 1. Thí nghiệm lá vàng: hạt alpha xuyên qua phần trống, chỉ hạt sát hạt nhân mới lệch mạnh hoặc bật ngược. Bên phải là hình phóng to các nguyên tử trong lá vàng.<br>'
        'Nhãn: Source of α particles = nguồn hạt α; Gold foil = lá vàng; Screen = màn dò; Atoms = nguyên tử; Nuclei = hạt nhân; 10<sup>−10</sup> m = đường kính nguyên tử; 10<sup>−15</sup> m = đường kính hạt nhân.<br>'
        '<small>Hình: OpenStax, College Physics 2e, Hình 30.10 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>')

# ---------------------------------------------- FIG2 (hiện là Hình 4 — mốc FIG2 nằm sau FIG3, FIG4 trong bài): ba mô hình nguyên tử
b = defs("f2")
for x, t in ((66, "Thomson 1904"), (202, "Rutherford 1911"), (352, "Bohr 1913")):
    b += text(x, 22, t, "currentColor", 14, "middle", "700")
# Thomson: quả cầu đặc
b += f'<circle cx="66" cy="112" r="56" fill="rgba(251,146,60,.16)" stroke="{ORG}" stroke-width="1.8"/>'
for dx, dy in ((-26, -26), (26, -26), (0, 0), (-26, 26), (26, 26)):
    b += dot(66 + dx, 112 + dy, 4, BLUE)
b += text(66, 192, "cầu dương đặc", "currentColor", 14, "middle", "500")
b += text(66, 210, "êlectron rải rác", "currentColor", 14, "middle", "500")
# Rutherford
b += f'<circle cx="202" cy="112" r="56" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 5" opacity="0.5"/>'
b += dot(202, 112, 13, RED)
b += text(202, 117, "+", "currentColor", 14, "middle", "700")
b += f'<ellipse cx="202" cy="112" rx="42" ry="42" fill="none" stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="4 4"/>'
b += dot(160, 112, 4, BLUE) + dot(244, 112, 4, BLUE)
b += text(202, 192, "hạt nhân nhỏ, nặng", "currentColor", 14, "middle", "500")
b += text(202, 210, "êlectron quay", "currentColor", 14, "middle", "500")
b += text(202, 228, "quanh hạt nhân", "currentColor", 14, "middle", "500")
# Bohr
b += dot(352, 112, 13, RED)
b += text(352, 117, "+", "currentColor", 14, "middle", "700")
b += f'<circle cx="352" cy="112" r="24" fill="none" stroke="{BLUE}" stroke-width="1.8"/>'
b += f'<circle cx="352" cy="112" r="46" fill="none" stroke="{BLUE}" stroke-width="1.8"/>'
b += dot(328, 112, 4.5, BLUE) + dot(352, 66, 4.5, BLUE)
b += text(352, 192, "quỹ đạo cho phép,", "currentColor", 14, "middle", "500")
b += text(352, 210, "năng lượng xác định", "currentColor", 14, "middle", "500")
b += text(16, 258, "Nguyên tử gần như trống: hạt nhân chiếm", "currentColor", 14, "start", "500")
b += text(16, 276, "cỡ một phần mười nghìn tỉ thể tích", "currentColor", 14, "start", "500")
b += text(16, 296, "Hạt nhân vẽ phóng to, không đúng tỉ lệ", "currentColor", 14, "start", "500")
fig2 = wrap2("0 0 440 306", "Ba mô hình nguyên tử đặt cạnh nhau: Thomson cầu đặc, Rutherford có hạt nhân nhỏ ở giữa, Bohr thêm các quỹ đạo cho phép",
             b, "Hình 4. Ba mô hình nguyên tử: Thomson bị thí nghiệm lá vàng bác bỏ; Rutherford có hạt nhân nhỏ, nặng; Bohr thêm các quỹ đạo xác định.")

# ---------------------------------------------- FIG3 (hiện là Hình 2 — đứng thứ hai trong bài): kí hiệu hạt nhân
# Vẽ lại 30/10/2026: chữ ≥ 14 (đọc được ở 375 px), bỏ khoảng trống đầu hình, ví dụ trong khung.
b = defs("f3")
b += text(14, 24, "Đọc kí hiệu hạt nhân", "currentColor", 15, "start", "700")
# kí hiệu lớn ở giữa-phải
b += text(252, 122, "Cu", "currentColor", 56, "start", "700")
b += text(246, 94, "65", RED, 30, "end", "700")
b += text(246, 146, "29", BLUE, 30, "end", "700")
# nhãn trái + mũi tên chỉ vào hai chỉ số
b += text(14, 84, "A = số nuclôn", RED, 15, "start", "700")
b += text(14, 103, "prôtôn + nơtron", RED, 14, "start", "500")
b += arrow("f3", "r", 150, 84, 200, 84, 2)
b += text(14, 136, "Z = số prôtôn", BLUE, 15, "start", "700")
b += text(14, 155, "điện tích hạt nhân", BLUE, 14, "start", "500")
b += arrow("f3", "b", 150, 136, 200, 136, 2)
# nhãn phải: kí hiệu hoá học
b += text(352, 104, "kí hiệu", "currentColor", 14, "start", "500")
b += text(352, 122, "hoá học X", "currentColor", 14, "start", "500")
# ví dụ trong khung
b += rect(10, 178, 420, 84, "rgba(148,163,184,.10)", "currentColor", 1.2, 8)
b += text(22, 200, "Ví dụ: hạt nhân đồng có 29 prôtôn, 65 nuclôn", "currentColor", 14, "start", "600")
b += text(22, 222, "Số nơtron N = A − Z = 65 − 29 = 36", "currentColor", 14, "start", "600")
b += text(22, 246, "Cùng Z = 29, khác N: hai đồng vị của đồng", "currentColor", 14, "start", "600")
fig3 = wrap2("0 0 440 272", "Kí hiệu hạt nhân đồng: chỉ số trên là số nuclôn A bằng 65, chỉ số dưới là số prôtôn Z bằng 29, nên có 36 nơtron",
             b, "Hình 2. Kí hiệu hạt nhân $^A_Z X$: $A$ là số nuclôn, $Z$ là số prôtôn.")

# ---------------------------------------------- FIG4 (hiện là Hình 3): vạch quang phổ của hai đồng vị hiđrô
# Vẽ lại 30/10/2026: ở thang 400–700 nm độ lệch 0,18 nm chỉ ~0,2 px (không thấy) → thêm khung phóng to quanh Hα.
# Bước sóng (trong không khí): Hβ 486,13 / Dβ 486,00; Hα 656,28 / Dα 656,10 nm.
b = defs("f4")
b += text(14, 22, "Hai đồng vị hiđrô, hai bộ vạch quang phổ", "currentColor", 15, "start", "700")
b += text(14, 42, "đơteri D có thêm 1 nơtron trong hạt nhân", "currentColor", 14, "start", "500")
X = lambda wl: 80 + (wl - 400) * 340 / 300          # thang tổng quát: 400 nm → 80, 700 nm → 420
b += text(14, 86, "λ (nm)", "currentColor", 14, "start", "600")
b += line(80, 80, 420, 80, "currentColor", 1.6, "", .6)
for wl in (400, 500, 600, 700):
    b += line(X(wl), 76, X(wl), 84, "currentColor", 1.4, "", .8)
    b += text(X(wl), 70, f"{wl}", "currentColor", 14, "middle", "500")
for y, nhan, (wb, wa) in ((112, "H", (486.13, 656.28)), (148, "D", (486.00, 656.10))):
    b += text(62, y + 5, nhan, "currentColor", 16, "end", "700")
    b += line(80, y, 420, y, "currentColor", 1, "", .3)
    b += line(round(X(wb), 1), y - 12, round(X(wb), 1), y + 12, BLUE, 3)
    b += line(round(X(wa), 1), y - 12, round(X(wa), 1), y + 12, RED, 3)
# khung đánh dấu vùng phóng to (quanh Hα) + hai đường nối xuống khung dưới
xa = X(656.2)
b += f'<rect x="{xa-16:.1f}" y="94" width="32" height="72" rx="4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity=".7"/>'
b += line(round(xa - 16, 1), 166, 20, 190, "currentColor", 1, "4 3", .45)
b += line(round(xa + 16, 1), 166, 420, 190, "currentColor", 1, "4 3", .45)
b += rect(20, 190, 400, 126, "rgba(148,163,184,.08)", "currentColor", 1.2, 8)
b += text(32, 210, "Phóng to quanh vạch đỏ Hα", "currentColor", 14, "start", "700")
Z = lambda wl: 100 + (wl - 656.0) * 700          # thang phóng to: 656,0 → 100; 656,4 → 380 (700 px/nm)
xh, xd = Z(656.28), Z(656.10)                    # 296 và 170
b += text(xh, 234, "H: 656,28", RED, 14, "middle", "700")
b += text(xd, 234, "D: 656,10", RED, 14, "middle", "700")
b += line(xh, 242, xh, 282, RED, 3) + line(xd, 242, xd, 282, RED, 3)
b += arrow("f4", "o", xh - 6, 268, xd + 6, 268, 2)
b += text((xh + xd) / 2, 260, "lệch ≈ 0,18 nm", ORG, 14, "middle", "700")
b += line(100, 288, 380, 288, "currentColor", 1.4, "", .6)
for k in range(5):
    wl = 656.0 + k / 10
    b += line(Z(wl), 284, Z(wl), 292, "currentColor", 1.2, "", .8)
    b += text(Z(wl), 308, f"{wl:.1f}".replace(".", ","), "currentColor", 13, "middle", "500")
b += text(14, 338, "D nặng hơn: vạch dịch về phía bước sóng ngắn hơn", "currentColor", 14, "start", "600")
fig4 = wrap2("0 0 440 348", "Hai bộ vạch quang phổ của hiđrô và đơteri gần như trùng nhau; phóng to quanh vạch đỏ thấy vạch đơteri 656,10 nm nằm lệch 0,18 nm về phía bước sóng ngắn hơn vạch hiđrô 656,28 nm",
             b, "Hình 3. Hai đồng vị hiđrô cho hai bộ vạch quang phổ gần như trùng nhau; phóng to mới thấy vạch của đơteri dịch về phía bước sóng ngắn hơn.")

# ---------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(margin_figs(src))
print("ok", len(src), "bytes")
