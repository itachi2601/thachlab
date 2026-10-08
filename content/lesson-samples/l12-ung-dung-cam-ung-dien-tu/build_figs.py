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
b = defs("f1")
b += text(14, 20, "Bếp từ: nhiệt sinh ngay trong đáy nồi", "currentColor", 12, "start", "700")
b += rect(130, 50, 180, 54, "rgba(56,189,248,.18)", "none", 0, 0)          # nước trong nồi
b += text(140, 76, "nước", BLUE, 11, "start", "600")
b += rect(120, 44, 10, 66, "rgba(251,146,60,.20)", ORG, 2, 3)              # thành nồi trái
b += rect(310, 44, 10, 66, "rgba(251,146,60,.20)", ORG, 2, 3)              # thành nồi phải
b += rect(120, 104, 200, 16, "rgba(251,146,60,.30)", ORG, 2)               # đáy nồi
b += text(326, 116, "đáy nồi gang", ORG, 11, "start", "600")
b += rect(60, 124, 320, 9, "rgba(148,163,184,.28)", "currentColor", 1.2, 3)  # mặt kính
b += coil(160, 146, 9, 14, 12, RED, 2.4)                                   # cuộn dây
b += text(296, 156, "cuộn dây", RED, 11, "start", "700")
b += text(296, 169, "dòng xoay chiều", RED, 11, "start", "600")
for x in (170, 220, 270):                                                  # từ trường biến thiên
    b += arrow("f1", "b", x, 142, x, 102, 1.8, "5 4")
b += text(14, 150, "mặt kính (cách điện)", "currentColor", 11)
for cx in (170, 270):                                                      # dòng Foucault trong đáy nồi
    b += loop(cx, 112, 12, 7)
    b += arrow("f1", "g", cx - 8, 116, cx + 7, 116, 1.8)
for x in (205, 250):                                                       # nhiệt vào nước
    b += arrow("f1", "r", x, 100, x, 82, 2)
b += text(14, 196, "từ trường biến thiên xuyên qua mặt kính", BLUE, 11)
b += text(14, 214, "dòng Foucault sinh ra trong đáy nồi", GRN, 11)
b += text(14, 232, "dòng đó toả nhiệt (Joule) làm nồi nóng lên", RED, 11)
fig1 = wrap("0 0 440 250",
            "Mặt cắt bếp từ: cuộn dây dưới mặt kính tạo từ trường biến thiên xuyên vào đáy nồi gang, sinh dòng Foucault và toả nhiệt trong đáy nồi",
            b, "Hình 1. Từ trường biến thiên xuyên qua mặt kính, sinh dòng Foucault toả nhiệt "
               "ngay trong đáy nồi gang.")

# ------------------------------------------------- Hình 2: đàn ghi ta điện
b = defs("f2")
b += text(12, 20, "Đàn ghi ta điện: dao động thành dòng điện", "currentColor", 12, "start", "700")
b += line(40, 52, 400, 52, "currentColor", 2.5)                            # dây thép
b += arrow("f2", "r", 140, 66, 140, 38, 1.8)
b += arrow("f2", "r", 158, 38, 158, 66, 1.8)
b += text(164, 44, "dây thép dao động", RED, 11, "start", "600")
b += rect(196, 76, 64, 40, "rgba(148,163,184,.12)", "currentColor", 2)     # bộ cảm ứng
b += f'<ellipse cx="228" cy="96" rx="30" ry="15" fill="none" stroke="{RED}" stroke-width="1.6"/>'
b += f'<ellipse cx="228" cy="96" rx="30" ry="21" fill="none" stroke="{RED}" stroke-width="1.6"/>'
b += rect(206, 96, 44, 14, "rgba(248,113,113,.22)", RED, 1.4, 3)           # nam châm
b += text(214, 107, "N", RED, 11, "start", "700")
b += text(240, 107, "S", BLUE, 11, "start", "700")
b += line(140, 116, 194, 100, "currentColor", 1, "4 3", .8)
b += text(14, 122, "nam châm + cuộn dây", "currentColor", 11, "start", "600")
for x in (206, 228, 250):                                                  # từ trường lên dây
    b += arrow("f2", "b", x, 74, x, 58, 1.6, "4 3")
b += text(14, 100, "từ trường biến thiên", BLUE, 11)
b += arrow("f2", "r", 286, 96, 392, 96, 2.4)
b += text(290, 86, "dòng cảm ứng", RED, 11, "start", "700")
b += text(290, 116, "máy tăng âm → loa", "currentColor", 11, "start", "600")
pts = " ".join(f"{x},{160 - int(14 * __import__('math').sin((x - 30) / 110 * 6.283))}" for x in range(30, 251, 5))
b += f'<polyline points="{pts}" fill="none" stroke="{GRN}" stroke-width="2.2"/>'
b += text(258, 166, "ra loa: cùng tần số dây", "currentColor", 11)
fig2 = wrap("0 0 440 200",
            "Sơ đồ đàn ghi ta điện: dây thép dao động trên nam châm và cuộn dây cảm ứng, dòng điện cảm ứng cùng tần số đi ra máy tăng âm và loa",
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

# ------------------------------------------------- Hình 4: tấm Foucault
b = defs("f4")
b += text(12, 20, "a) Tấm liền khối", "currentColor", 11, "start", "700")
b += text(12, 36, "6 lần qua · tắt sau 3,8 s", GRN, 11, "start", "700")
b += line(60, 40, 150, 40, "currentColor", 2)
b += line(105, 40, 105, 58, "currentColor", 1.5)
b += rect(75, 58, 60, 80, "rgba(148,163,184,.22)", "currentColor", 2)
b += loop(105, 98, 20, 28)
b += arrow("f4", "g", 105, 124, 122, 118, 1.8)
b += rect(30, 76, 32, 44, "rgba(248,113,113,.22)", RED, 2, 4)
b += text(46, 102, "N", RED, 11, "middle", "700")
b += rect(148, 76, 32, 44, "rgba(56,189,248,.22)", BLUE, 2, 4)
b += text(164, 102, "S", BLUE, 11, "middle", "700")
b += text(14, 196, "dòng khép kín lớn", GRN, 11)
b += text(14, 214, "→ hãm mạnh", GRN, 11)
b += text(228, 20, "b) Tấm có rãnh xẻ", "currentColor", 11, "start", "700")
b += text(228, 36, "21 lần qua · tắt sau 13,3 s", GRN, 11, "start", "700")
b += line(270, 40, 370, 40, "currentColor", 2)
b += line(320, 40, 320, 58, "currentColor", 1.5)
for x in (290, 306, 322, 338):
    b += rect(x, 58, 12, 80, "rgba(148,163,184,.22)", "currentColor", 1.6, 2)
    b += loop(x + 6, 98, 5, 24)
b += text(228, 196, "rãnh cắt đường dòng", GRN, 11)
b += text(228, 214, "→ dòng nhỏ → hãm yếu", GRN, 11)
b += rect(246, 76, 30, 44, "rgba(248,113,113,.22)", RED, 2, 4)
b += text(261, 102, "N", RED, 11, "middle", "700")
b += rect(360, 76, 30, 44, "rgba(56,189,248,.22)", BLUE, 2, 4)
b += text(375, 102, "S", BLUE, 11, "middle", "700")
fig4 = wrap("0 0 440 224",
            "Hai tấm nhôm dao động giữa hai cực nam châm: tấm liền khối có dòng Foucault khép kín lớn nên tắt nhanh, tấm có rãnh xẻ bị cắt đường dòng nên dao động lâu hơn",
            b, "Hình 4. Cùng khối lượng, cùng từ trường: tấm liền khối tắt nhanh, tấm có rãnh xẻ lâu hơn.")

# ------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
