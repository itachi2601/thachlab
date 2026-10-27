"""Sinh 4 hình SVG cho bài "Bài 15. Một số ứng dụng của cảm ứng điện từ" (Vật lí 12)
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


# ------------------------------------------------- Hình 1: bếp từ cắt dọc
def dbl(x1, y1, x2, y2, c, w=1.8):
    """Đường sức biến thiên: nét đứt, đầu mũi tên ở CẢ HAI đầu (B đổi chiều theo thời gian)."""
    return field_line(x1, y1, x2, y2, c, w, "6 4", 10) + chevron(x1, y1, x1 - x2, y1 - y2, c, w, 10)


b = defs("f1")
b += text(14, 20, "Bếp từ: nhiệt sinh ngay trong đáy nồi", "currentColor", 14, "start", "700")
b += rect(130, 50, 180, 54, "rgba(56,189,248,.18)", "none", 0, 0)          # nước trong nồi
b += text(170, 72, "nước", BLUE, 14, "start", "600")
b += rect(120, 44, 10, 66, "rgba(251,146,60,.20)", ORG, 2, 3)              # thành nồi trái
b += rect(310, 44, 10, 66, "rgba(251,146,60,.20)", ORG, 2, 3)              # thành nồi phải
b += rect(120, 104, 200, 16, "rgba(251,146,60,.30)", ORG, 2)               # đáy nồi
b += text(326, 116, "đáy nồi gang", ORG, 14, "start", "600")
b += rect(60, 124, 320, 9, "rgba(148,163,184,.28)", "currentColor", 1.2, 3)  # mặt kính
b += text(14, 150, "mặt kính", "currentColor", 14)
b += text(14, 166, "(cách điện)", "currentColor", 14)
for i in range(8):                                                         # mặt cắt cuộn dây: dây ra/vào mặt giấy
    x = 167.5 + i * 15
    b += f'<circle cx="{x}" cy="150" r="6" fill="none" stroke="{RED}" stroke-width="2"/>'
    if i < 4:
        b += line(x - 3.5, 146.5, x + 3.5, 153.5, RED, 1.6) + line(x - 3.5, 153.5, x + 3.5, 146.5, RED, 1.6)
    else:
        b += dot(x, 150, 2.2, RED)
b += text(296, 160, "cuộn dây", RED, 14, "start", "700")
b += text(296, 176, "dòng xoay chiều", RED, 14, "start", "600")
for x in (190, 220, 250):                                                  # B(t): mũi tên hai đầu
    b += dbl(x, 138, x, 100, BLUE)
b += text(262, 94, "B(t)", BLUE, 14, "start", "700")
for ry in (86, 46):                                                        # vòng Foucault đồng tâm phủ đáy nồi
    b += f'<ellipse cx="220" cy="112" rx="{ry}" ry="6" fill="none" stroke="{GRN}" stroke-width="1.8" stroke-dasharray="5 4"/>'
    b += chevron(220 + ry, 112, 0, 1, GRN, 1.8, 7)
    b += chevron(220 - ry, 112, 0, -1, GRN, 1.8, 7)
for x in (142, 298):                                                       # nhiệt vào nước
    b += arrow("f1", "r", x, 100, x, 82, 2)
b += text(14, 200, "từ trường biến thiên xuyên qua mặt kính", BLUE, 14)
b += text(14, 220, "dòng Foucault: vòng tròn đồng tâm trong đáy nồi", GRN, 14)
b += text(14, 240, "dòng đó toả nhiệt (Joule) làm nồi nóng lên", RED, 14)
fig1 = wrap("0 0 440 252",
            "Mặt cắt bếp từ: cuộn dây dưới mặt kính tạo từ trường biến thiên xuyên vào đáy nồi gang, sinh dòng Foucault dạng vòng đồng tâm và toả nhiệt trong đáy nồi",
            b, "Hình 1. Từ trường biến thiên xuyên qua mặt kính, sinh dòng Foucault toả nhiệt "
               "ngay trong đáy nồi gang.")

# ------------------------------------------------- Hình 2: đàn ghi ta điện
b = defs("f2")
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
            b, "Hình 2. Bộ cảm ứng: dây thép dao động trên nam châm, cuộn dây cho dòng cảm ứng "
               "cùng tần số ra loa.")

# ------------------------------------------------- Hình 3: sạc không dây (2 ô)
b = defs("f3")
b += text(12, 20, "a) Hai cuộn rời nhau", "currentColor", 11, "start", "700")
b += rect(30, 36, 142, 62, "rgba(56,189,248,.12)", BLUE, 2, 8)             # thân điện thoại
b += text(38, 54, "điện thoại", "currentColor", 11, "start", "600")
b += coil(46, 84, 8, 9, 9, RED, 2)                                         # cuộn thứ cấp
b += text(126, 74, "cuộn", RED, 11, "start", "600")
b += text(126, 86, "thứ cấp", RED, 11, "start", "600")
b += rect(30, 150, 142, 26, "rgba(148,163,184,.16)", "currentColor", 2, 6)  # đế sạc
b += coil(46, 160, 8, 9, 8, RED, 2)                                        # cuộn sơ cấp
b += text(30, 192, "đế sạc: cuộn sơ cấp", "currentColor", 11)
for x in (70, 100, 130):                                                   # từ trường giữa hai cuộn
    b += arrow("f3", "b", x, 148, x, 100, 1.6, "4 3")
b += text(12, 222, "~ xoay chiều → từ trường → dòng cảm ứng", RED, 11)
b += text(228, 20, "b) Điện áp giảm theo khoảng cách", "currentColor", 11, "start", "700")
b += line(280, 205, 280, 56, "currentColor", 2)
b += line(280, 205, 424, 205, "currentColor", 2)
b += text(286, 48, "U (V)", "currentColor", 11, "start", "600")
b += text(424, 236, "d (cm)", "currentColor", 11, "end", "600")
b += line(280, 66, 420, 66, GRN, 1.4, "6 5")
b += text(302, 62, "lí tưởng 9,0 V", GRN, 11, "start", "600")
for d, u in ((0, 8.4), (1, 7.1), (2, 5.9), (3, 4.8), (4, 3.9)):
    x = 280 + d * 35
    y = 205 - int(u * 15.47)
    b += dot(x, y)
    b += text(x, 220, str(d), "currentColor", 11, "middle", "600")
pts = " ".join(f"{280 + d * 35},{205 - int(u * 15.47)}" for d, u in ((0, 8.4), (1, 7.1), (2, 5.9), (3, 4.8), (4, 3.9)))
b += f'<polyline points="{pts}" fill="none" stroke="{GRN}" stroke-width="2.2"/>'
fig3 = wrap("0 0 440 240",
            "Sạc không dây: hai cuộn dây rời nhau ghép qua từ trường, và đồ thị điện áp cuộn thứ cấp giảm dần khi tăng khoảng cách",
            b, "Hình 3. Sạc không dây = máy biến áp không lõi: hai cuộn rời ghép qua từ trường; "
               "số đo luôn thấp hơn lí tưởng 9,0 V.")

# ------------------------------------------------- Hình 4: tấm Foucault (nhìn thẳng mặt tấm, B vuông góc mặt tấm)
def field_dots(cx, cy, r):
    """Vùng nam châm: từ trường vuông góc mặt tấm, hướng ra phía người xem (chấm)."""
    o = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="rgba(56,189,248,.10)" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="5 4"/>'
    for dx in (-14, 0, 14):
        for dy in (-14, 0, 14):
            if dx * dx + dy * dy <= (r - 8) ** 2:
                o += dot(cx + dx, cy + dy, 2.4, BLUE)
    return o


def eddy(cx, cy, rx, ry, L=9):
    """Vòng dòng Foucault: bên trái đi xuống (trong vùng từ trường), bên phải đi lên."""
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{GRN}" stroke-width="2" stroke-dasharray="5 4"/>'
            + chevron(cx - rx, cy, 0, 1, GRN, 2, L) + chevron(cx + rx, cy, 0, -1, GRN, 2, L))


b = defs("f4")
b += text(12, 20, "a) Tấm liền khối", "currentColor", 14, "start", "700")
b += line(110, 30, 110, 52, "currentColor", 1.5)                           # dây treo
b += rect(50, 52, 120, 110, "rgba(148,163,184,.22)", "currentColor", 2, 3)
b += field_dots(110, 112, 30)
b += eddy(126, 112, 34, 30)
b += arrow("f4", "o", 60, 182, 150, 182, 2.4)                              # vận tốc tấm
b += text(12, 212, "tấm chuyển động sang phải", ORG, 14)
b += text(12, 230, "chấm: B vuông góc mặt tấm", BLUE, 14)
b += text(12, 248, "vòng dòng khép kín lớn", GRN, 14)
b += text(12, 266, "→ hãm mạnh", GRN, 14)
b += text(12, 284, "qua 6 lần · tắt 3,8 s", GRN, 14, "start", "700")
b += text(232, 20, "b) Tấm có rãnh xẻ", "currentColor", 14, "start", "700")
b += line(330, 30, 330, 52, "currentColor", 1.5)
x0, w, g, n = 272, 20, 4, 5                                                # tấm xẻ rãnh: dạng chiếc lược
b += rect(x0, 52, n * w + (n - 1) * g, 50, "rgba(148,163,184,.22)", "currentColor", 2, 3)   # thanh ngang phía trên
for i in range(n):
    b += rect(x0 + i * (w + g), 102, w, 60, "rgba(148,163,184,.22)", "currentColor", 2, 2)  # các răng, giữa có rãnh
b += field_dots(330, 112, 30)
for i in (1, 2, 3):
    b += eddy(x0 + i * (w + g) + w / 2, 132, 7, 20, 6)
b += arrow("f4", "o", 282, 182, 372, 182, 2.4)
b += text(232, 212, "cùng khối lượng,", "currentColor", 14)
b += text(232, 230, "cùng từ trường", "currentColor", 14)
b += text(232, 248, "rãnh cắt đường dòng", GRN, 14)
b += text(232, 266, "→ dòng nhỏ → hãm yếu", GRN, 14)
b += text(232, 284, "qua 21 lần · tắt 13,3 s", GRN, 14, "start", "700")
fig4 = wrap("0 0 440 296",
            "Hai tấm nhôm dao động qua vùng từ trường vuông góc mặt tấm: tấm liền khối có dòng Foucault khép kín lớn nên tắt nhanh, tấm có rãnh xẻ bị cắt đường dòng nên dao động lâu hơn",
            b, "Hình 4. Cùng khối lượng, cùng từ trường: tấm liền khối tắt nhanh, tấm có rãnh xẻ lâu hơn.")

# ------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
