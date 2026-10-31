"""Sinh 4 hình SVG cho bài "Bài 15. Một số ứng dụng của cảm ứng điện từ" (Vật lí 12)
và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html.
Chạy từ thư mục này: python3 build_figs.py
"""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *  # noqa: E402


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def dot(x, y, r=4, c=GRN):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def rect(x, y, w, h, fill, stroke="currentColor", sw=2, rx=6):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def coil(x0, y0, n=8, step=13, amp=11, c=RED, w=2.2):
    """Cuộn dây vẽ bằng đường zic-zac ngang."""
    pts = []
    for i in range(n + 1):
        y = y0 if i % 2 == 0 else y0 + amp
        pts.append(f"{x0 + i * step},{y}")
    return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{c}" stroke-width="{w}"/>'


def loop(cx, cy, rx, ry, c=GRN):
    """Vòng dòng khép kín."""
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{c}" '
            f'stroke-width="1.8" stroke-dasharray="5 4"/>')


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


# ------------------------------------------------- FIG1 (Hình 4 trong bài): bếp từ cắt dọc — vẽ lại 31/10/2026
def dbl(x1, y1, x2, y2, c, w=1.8):
    """Đường sức biến thiên: nét đứt, đầu mũi tên ở CẢ HAI đầu (B đổi chiều theo thời gian)."""
    return field_line(x1, y1, x2, y2, c, w, "6 4", 10) + chevron(x1, y1, x1 - x2, y1 - y2, c, w, 10)


def ring(cx, cy, rx, ry, t_deg, c=GRN):
    """Vòng dòng Foucault (elip nằm ngang) + đầu V tại góc t; chiều: nửa trước (dưới) chạy sang PHẢI."""
    t = math.radians(t_deg)
    x, y = cx + rx * math.cos(t), cy + ry * math.sin(t)
    dx, dy = rx * math.sin(t), -ry * math.cos(t)
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{c}" stroke-width="2" stroke-dasharray="5 4"/>'
            + chevron(round(x, 1), round(y, 1), dx, dy, c, 2, 9))


b = text(14, 20, "Bếp từ: nhiệt sinh ngay trong đáy nồi", "currentColor", 14, "start", "700")
b += rect(120, 48, 200, 56, "rgba(56,189,248,.16)", "none", 0, 0)          # nước
b += rect(110, 40, 10, 96, "rgba(251,146,60,.20)", ORG, 2, 3)              # thành nồi trái
b += rect(320, 40, 10, 96, "rgba(251,146,60,.20)", ORG, 2, 3)              # thành nồi phải
b += rect(110, 104, 220, 32, "rgba(251,146,60,.28)", ORG, 2, 3)            # đáy nồi dày
b += text(220, 66, "nước", BLUE, 14, "middle", "600")
for x in (146, 294):                                                       # nhiệt từ đáy nồi vào nước
    b += arrow("", "r", x, 102, x, 78, 2.4)
    b += text(x, 72, "nhiệt", RED, 14, "middle", "600")
b += text(336, 126, "đáy nồi gang", ORG, 14, "start", "600")
b += rect(60, 140, 320, 10, "rgba(148,163,184,.28)", "currentColor", 1.2, 3)  # mặt kính
b += text(14, 176, "mặt kính", "currentColor", 14)
b += text(14, 194, "(cách điện)", "currentColor", 14)
# Cuộn dây phẳng cắt dọc: nửa trái dòng đi vào (⊗), nửa phải đi ra (⊙) — tại thời điểm vẽ.
for i in range(8):
    x = 167.5 + i * 15
    b += f'<circle cx="{x}" cy="178" r="6" fill="none" stroke="{RED}" stroke-width="2"/>'
    if i < 4:
        b += line(x - 3.5, 174.5, x + 3.5, 181.5, RED, 1.6) + line(x - 3.5, 181.5, x + 3.5, 174.5, RED, 1.6)
    else:
        b += dot(x, 178, 2.2, RED)
b += text(292, 184, "cuộn dây", RED, 14, "start", "700")
b += text(292, 202, "dòng xoay chiều", RED, 14, "start", "600")
for x in (170, 220, 270):                                                  # B(t): nét đứt, mũi hai đầu, xuyên kính vào đáy nồi
    b += dbl(x, 168, x, 90, BLUE)
b += text(282, 164, "B(t)", BLUE, 14, "start", "700")
# Dòng Foucault: chiều ngược dòng trong cuộn dây (Lenz, lúc dòng cuộn dây đang tăng):
# cuộn dây nửa trước chạy sang trái (⊗ trái = vào, ⊙ phải = ra) → vòng Foucault nửa trước chạy sang phải.
b += ring(220, 120, 92, 11, 108)
b += ring(220, 120, 46, 6, 66)
b += text(14, 236, "từ trường B(t) đổi chiều liên tục, xuyên qua kính", BLUE, 14)
b += text(14, 256, "dòng Foucault: vòng khép kín trong đáy nồi", GRN, 14)
b += text(14, 276, "dòng đó toả nhiệt Joule: nồi nóng, nước sôi", RED, 14)
fig1 = wrap("0 0 440 288",
            "Mặt cắt bếp từ: cuộn dây dưới mặt kính tạo từ trường biến thiên xuyên vào đáy nồi gang, sinh dòng Foucault dạng vòng khép kín trong đáy nồi và toả nhiệt vào nước",
            b, "Hình 4. Từ trường biến thiên xuyên qua mặt kính, sinh dòng Foucault toả nhiệt "
               "ngay trong đáy nồi gang.")

# ------------------------------------------------- FIG2 (Hình 1 trong bài): đàn ghi ta điện
b = ""
b += text(12, 20, "Đàn ghi ta điện: dao động thành dòng điện", "currentColor", 14, "start", "700")
b += line(30, 64, 250, 64, "currentColor", 2.5)                            # dây thép
b += arrow("f2", "r", 44, 76, 44, 50, 1.8)
b += arrow("f2", "r", 60, 50, 60, 76, 1.8)
b += text(268, 56, "dây thép dao động", RED, 14, "start", "600")
b += rect(130, 92, 40, 30, "rgba(248,113,113,.22)", RED, 2, 2)             # nam châm: cực N sát dây
b += rect(130, 122, 40, 30, "rgba(56,189,248,.22)", BLUE, 2, 2)
b += text(150, 112, "N", RED, 14, "middle", "700")
b += text(150, 144, "S", BLUE, 14, "middle", "700")
for i in range(3):                                                         # cuộn dây quấn ở giữa nam châm, tránh chữ N, S
    y = 118.5 + i * 4.5
    b += f'<ellipse cx="150" cy="{y}" rx="26" ry="2.8" fill="none" stroke="{RED}" stroke-width="2"/>'
b += field_path("M138,92 C70,-30 20,200 130,148", (130, 148), (1, -.3), BLUE)    # đường sức từ cực N ra, cắt dây, về cực S từ ngoài cuộn
b += field_path("M162,92 C230,-30 280,200 170,148", (170, 148), (-1, -.3), BLUE)
b += field_line(150, 90, 150, 38, BLUE, 1.8)                                      # đường sức qua dây
b += text(268, 100, "nam châm: trục dọc", "currentColor", 14, "start", "600")
b += text(268, 118, "cực N sát dây", "currentColor", 14, "start", "600")
b += text(268, 136, "cuộn quanh nam châm", RED, 14, "start", "600")
b += text(268, 80, "từ trường qua dây", BLUE, 14, "start", "600")
b += line(124, 127, 112, 127, RED, 2) + line(112, 127, 112, 196, RED, 2) + line(112, 196, 270, 196, RED, 2)    # hai đầu cuộn dây nối ra máy
b += line(176, 118.5, 196, 118.5, RED, 2) + line(196, 118.5, 196, 178, RED, 2) + line(196, 178, 270, 178, RED, 2)
b += rect(270, 168, 160, 38, "rgba(148,163,184,.16)", "currentColor", 2, 6)
b += text(350, 192, "máy tăng âm → loa", "currentColor", 14, "middle", "600")
b += arrow("f2", "r", 224, 178, 254, 178, 2.2)
b += text(12, 226, "dây dao động: từ thông qua cuộn biến thiên", RED, 14)
b += text(12, 244, "cuộn dây cho dòng cảm ứng cùng tần số dây", RED, 14)
fig2 = wrap("0 0 440 258",
            "Sơ đồ đàn ghi ta điện: nam châm trục dọc có một cực sát dây thép, cuộn dây quấn quanh nam châm, hai đầu cuộn nối ra máy tăng âm và loa; dây dao động làm từ thông qua cuộn biến thiên nên có dòng cảm ứng cùng tần số",
            b, "Hình 1. Bộ cảm ứng: dây thép dao động trên nam châm, cuộn dây cho dòng cảm ứng "
               "cùng tần số ra loa.")

# ------------------------------------------------- FIG3 (Hình 2 trong bài): sạc không dây — vẽ lại 31/10/2026 (2 ô xếp dọc, chữ ≥ 14)
def flat_coil(cx, cy, c=RED):
    """Cuộn dây phẳng nhìn nghiêng: ba elip đồng tâm."""
    return "".join(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{c}" stroke-width="2"/>'
                   for rx, ry in ((62, 9), (44, 6.5), (26, 4)))


b = text(12, 20, "a) Hai cuộn dây rời nhau", "currentColor", 14, "start", "700")
b += rect(60, 34, 220, 66, "rgba(56,189,248,.12)", BLUE, 2, 8)             # thân điện thoại
b += text(72, 56, "điện thoại", "currentColor", 14, "start", "600")
b += flat_coil(170, 82)                                                    # cuộn thứ cấp
b += text(292, 72, "cuộn thứ cấp", RED, 14, "start", "700")
b += text(292, 90, "(nối pin)", "currentColor", 14, "start", "600")
b += rect(60, 150, 220, 40, "rgba(148,163,184,.16)", "currentColor", 2, 6)  # đế sạc
b += flat_coil(170, 168)                                                   # cuộn sơ cấp
b += text(292, 164, "cuộn sơ cấp", RED, 14, "start", "700")
b += text(292, 182, "(đế sạc, nối", "currentColor", 14, "start", "600")
b += text(292, 200, "xoay chiều)", "currentColor", 14, "start", "600")
for x in (128, 170, 212):                                                  # B(t) giữa hai cuộn: nét đứt, mũi hai đầu
    b += dbl(x, 156, x, 96, BLUE)
b += text(220, 132, "B(t)", BLUE, 14, "start", "700")
# ô b: đồ thị U2 theo d; trục tuyến tính: 75 px/cm, 16 px/V, gốc (70, 430)
X0, Y0, KX, KY = 70, 430, 75, 16
b += text(12, 240, "b) Điện áp thứ cấp theo khoảng cách", "currentColor", 14, "start", "700")
b += line(X0, Y0, X0, 266, "currentColor", 2) + chevron(X0, 262, 0, -1, "currentColor", 2, 9)
b += line(X0, Y0, 404, Y0, "currentColor", 2) + chevron(408, Y0, 1, 0, "currentColor", 2, 9)
b += text(80, 270, "U (V)", "currentColor", 14, "start", "700")
for u in (3, 6, 9):
    y = Y0 - u * KY
    b += line(X0 - 5, y, X0, y, "currentColor", 2) + text(X0 - 9, y + 5, str(u), "currentColor", 14, "end", "600")
b += text(X0 - 9, Y0 + 5, "0", "currentColor", 14, "end", "600")
b += line(X0, Y0 - 9 * KY, 392, Y0 - 9 * KY, GRN, 1.6, "6 5")
b += text(392, Y0 - 9 * KY - 8, "lí tưởng 9,0 V", GRN, 14, "end", "700")
DATA = ((0, 8.4), (1, 7.1), (2, 5.9), (3, 4.8), (4, 3.9))
for dd, u in DATA:
    x, y = X0 + dd * KX, Y0 - u * KY
    b += dot(x, round(y, 1), 4.5)
    b += line(x, Y0, x, Y0 + 5, "currentColor", 2) + text(x, Y0 + 22, str(dd), "currentColor", 14, "middle", "600")
pts = " ".join(f"{X0 + dd * KX},{Y0 - u * KY:.1f}" for dd, u in DATA)
b += f'<polyline points="{pts}" fill="none" stroke="{GRN}" stroke-width="2.4"/>'
b += text(236, 368, "số đo", GRN, 14, "start", "700")
b += text(428, 470, "d (cm)", "currentColor", 14, "end", "700")
fig3 = wrap("0 0 440 480",
            "Sạc không dây: cuộn sơ cấp trong đế sạc và cuộn thứ cấp trong điện thoại rời nhau, ghép qua từ trường biến thiên; đồ thị điện áp cuộn thứ cấp giảm từ 8,4 V xuống 3,9 V khi khoảng cách tăng từ 0 đến 4 cm, luôn dưới mức lí tưởng 9,0 V",
            b, "Hình 2. Sạc không dây = máy biến áp không lõi: hai cuộn rời ghép qua từ trường; "
               "số đo luôn thấp hơn lí tưởng 9,0 V.")

# ------------------------------------------------- FIG4 (Hình 3 trong bài): ảnh OpenStax College Physics 2e, Hình 23.12 (đợt 2, 27/10/2026)
fig4 = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l12-ung-dung-cam-ung-dien-tu/hinh-tam-foucault-lien-khoi-ranh-xe.webp" '
        'alt="Ba tấm kim loại treo dao động giữa hai cực nam châm: a) tấm liền khối có dòng Foucault khép kín, b) tấm xẻ rãnh, c) tấm không dẫn điện" '
        'loading="lazy" width="1000" height="653"><figcaption>'
        'Hình 3. a) liền khối: hãm mạnh; b) xẻ rãnh: hãm ít; c) không dẫn điện: không hãm.<br>'
        'Pivot = trục treo; v = vận tốc.<br>'
        '<small>Hình: OpenStax, College Physics 2e, Hình 23.12 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small>'
        '</figcaption></figure>')

# ------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(margin_figs(src))
print("ok", len(src), "bytes")
