"""Sinh 4 hình SVG cho bài "Bài 10. Lực từ. Cảm ứng từ" (Vật lí 12) và thay các mốc
<!--FIGn--> trong theory.src.html -> theory.html. Chạy từ thư mục này: python3 build_figs.py

Quy ước màu dùng chung cả bài: đỏ = lực từ F · cam = dòng điện I · xanh dương = cảm ứng từ B
(chỉ dùng chữ và nét bằng currentColor cho vật thể).
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
b += arrow("f2", "r", 138, 108, 138, 18, 3.2)                                   # F: dọc ngón cái, hướng lên
b += text(196, 40, "F", RED, 16, "start", "700")
b += arrow("f2", "o", 46, 300, 386, 300, 3.2)                                   # I: cổ tay → đầu ngón
b += text(398, 306, "I", ORG, 16, "start", "700")
b += text(216, 324, "cổ tay → ngón tay", ORG, 15, "middle", "600")
fig2 = wrap("0 0 460 340", "Bàn tay trái duỗi thẳng, lòng bàn tay hướng về phía người xem: đường sức từ xuyên vào lòng bàn tay, chiều từ cổ tay đến ngón tay theo dòng điện, ngón cái chỉ chiều lực từ",
            b, "Hình 2. Quy tắc bàn tay trái.")

# ------------------------------------------------- Hình 3: cân dòng điện (bố trí đề 2025 câu II.2)
# Nhìn chính diện: cực N trái, cực S phải, B nằm ngang N → S; dây MN nhìn đầu, dòng M (sau) → N (trước) = ⊙.
# F lên dây hướng lên; phản lực F' dây đẩy nam châm hướng xuống → cân tăng.
b = defs("f3")
b += rect(100, 214, 240, 34, "rgba(148,163,184,.10)", "currentColor", 2, 6)     # cân
b += rect(190, 222, 60, 18, "none", "currentColor", 1.5, 3)
b += text(220, 236, "cân", "currentColor", 12, "middle", "700")
b += rect(130, 178, 180, 34, "rgba(148,163,184,.16)", "currentColor", 2, 6)     # đế nam châm chữ U
b += rect(130, 70, 52, 108, "rgba(148,163,184,.16)", "currentColor", 2, 6)      # cực N
b += rect(258, 70, 52, 108, "rgba(148,163,184,.16)", "currentColor", 2, 6)      # cực S
b += text(156, 128, "N", "currentColor", 18, "middle", "700")
b += text(284, 128, "S", "currentColor", 18, "middle", "700")
b += field_line(186, 88, 254, 88, BLUE, 2.2)                                    # đường sức nét đứt N → S
b += field_line(186, 164, 254, 164, BLUE, 2.2)
b += text(240, 106, "B", BLUE, 14, "middle", "700")
b += f'<circle cx="220" cy="126" r="11" fill="none" stroke="{ORG}" stroke-width="2.5"/>' + dot(220, 126, 3.5, ORG)   # ⊙ dòng ra
b += text(235, 132, "I", ORG, 14, "start", "700")
b += arrow("f3", "r", 220, 112, 220, 40, 3)                                     # F lên dây
b += text(230, 48, "F", RED, 15, "start", "700")
b += arrow("f3", "r", 220, 182, 220, 210, 3)                                    # F' dây đẩy nam châm
b += text(230, 204, "F′", RED, 15, "start", "700")
b += text(20, 30, "dây MN giữ cố định", "currentColor", 12, "start", "600")
b += text(20, 48, "dòng M → N: hướng ra (⊙)", ORG, 12, "start", "600")
fig3 = wrap("0 0 440 260", "Nam châm chữ U đặt trên cân, cực N bên trái, cực S bên phải, đường sức nằm ngang từ N sang S; dây MN giữ cố định nằm ngang trong khe, dòng điện hướng ra phía người xem; lực từ lên dây hướng lên, lực dây đẩy nam châm hướng xuống",
            b, "Hình 3. Cân dòng điện.")

# ------------------------------------------------- Hình 4a/4b/4c: dây thẳng, vòng dây, ống dây (nhìn xiên, có che khuất)
# Nét liền ở phía trước đè lên; vật phía sau bị ngắt một khe chỗ vật trước đi qua (svg_lib: arc_pts...).
W, GAP = 4, 14   # bề dày dây; nửa khe che (độ)
VB = "0 0 440 250"

# 4a) dây thẳng: đường sức là đường tròn đồng tâm
b = defs("f4a")
cx = 220
levels = [(86, 100, 30), (158, 100, 30)]
ys = [22]
for g in sorted(cy + ry for cy, rx, ry in levels):
    ys += [g - 7, g + 7]                      # nửa trước đường sức đè lên dây -> ngắt dây
ys.append(236)
for i in range(0, len(ys), 2):
    b += line(cx, ys[i], cx, ys[i + 1], "currentColor", W)
b += chevron(cx, 24, 0, -1, ORG, 3.4, 15)
b += text(cx + 12, 34, "I", ORG, 16, "start", "700")
for cy, rx, ry in levels:
    b += pts_path(arc_pts(cx, cy, rx, ry, 180, 270 - GAP), BLUE, 2.2, "6 4")   # nửa sau: dây che
    b += pts_path(arc_pts(cx, cy, rx, ry, 270 + GAP, 360), BLUE, 2.2, "6 4")
    b += pts_path(arc_pts(cx, cy, rx, ry, 0, 180), BLUE, 2.2, "6 4")           # nửa trước
    x, y = ell_pt(cx, cy, rx, ry, 38)
    dx, dy = ell_tan(rx, ry, 38, -1)
    b += chevron(x, y, dx, dy, BLUE, 2.2)
b += text(cx + 106, 114, "B", BLUE, 16, "start", "700")
fig4a = wrap(VB, "Dây thẳng dài mang dòng điện hướng lên; đường sức từ là những đường tròn đồng tâm quanh dây, nửa phía sau bị dây che, nửa phía trước đi đè lên dây",
             b, "Hình 4a. Dây thẳng: đường sức là đường tròn đồng tâm quanh dây.")

# 4b) vòng dây: B xuyên qua tâm, vuông góc mặt phẳng vòng
b = defs("f4b")
cx, cy, rx, ry = 220, 130, 84, 34
top, bot = 22, 238
yf = cy + ry
b += line(cx, bot, cx, yf + 8, BLUE, 2.2, "6 4")                    # dây trước vòng đè lên đường sức -> ngắt
b += line(cx, yf - 8, cx, top + 4, BLUE, 2.2, "6 4")
b += chevron(cx, top, 0, -1, BLUE, 2.2)
b += chevron(cx, 70, 0, -1, BLUE, 2.2)
for sg in (1, -1):
    P = cubic((cx, top), (cx + sg * 190, top - 10), (cx + sg * 190, bot + 10), (cx, bot))
    b += pts_path(P, BLUE, 2.0, "6 4")
    b += chev_on(P, 30, BLUE)
b += pts_path(arc_pts(cx, cy, rx, ry, 180, 270 - GAP), "currentColor", W)   # nửa sau: đường sức đè lên -> ngắt dây
b += pts_path(arc_pts(cx, cy, rx, ry, 270 + GAP, 360), "currentColor", W)
b += pts_path(arc_pts(cx, cy, rx, ry, 0, 180), "currentColor", W)
for t in (35, 215):
    x, y = ell_pt(cx, cy, rx, ry, t)
    dx, dy = ell_tan(rx, ry, t, -1)
    b += chevron(x, y, dx, dy, ORG, 3.2, 14)
b += text(cx + rx + 10, cy + 30, "I", ORG, 16, "start", "700")
b += text(cx + 10, 60, "B", BLUE, 16, "start", "700")
fig4b = wrap(VB, "Vòng dây tròn nhìn xiên: đường sức từ xuyên qua tâm vuông góc mặt phẳng vòng dây rồi khép kín bên ngoài; chỗ đường sức đi trước thì dây bị ngắt, chỗ dây đi trước thì đường sức bị ngắt",
             b, "Hình 4b. Vòng dây: <strong>B</strong> xuyên qua tâm, vuông góc mặt phẳng vòng.")

# 4c) ống dây: từ trường đều trong lòng
b = defs("f4c")
cy = 130; rx, ry = 12, 44
xs = [110 + 40 * i for i in range(6)]
x0, x1 = xs[0] - 24, xs[-1] + rx + 34
import math
OFF = 20                                                                  # hai đường sức song song, cách trục đều nhau
tOff = math.degrees(math.asin(OFF / ry))                                   # góc elip tại độ cao ±OFF
for yy in (cy - OFF, cy, cy + OFF):
    ax = [x0]
    for x in xs:
        dxo = rx * math.cos(math.asin((yy - cy) / ry))
        ax += [x + dxo - 6, x + dxo + 6]                                   # nửa phải mỗi vòng ở phía trước, đè lên đường sức
    ax.append(x1)
    for i in range(0, len(ax), 2):
        b += line(ax[i], yy, ax[i + 1], yy, BLUE, 2.2, "6 4")
    b += chevron(x1, yy, 1, 0, BLUE, 2.2) + chevron(132, yy, 1, 0, BLUE, 2.2)
g = GAP * 1.3
for x in xs:
    # nửa trái ở phía sau: ba đường sức đè lên -> bỏ đoạn vòng nằm giữa ba đường sức
    h = tOff + 7
    b += pts_path(arc_pts(x, cy, rx, ry, 90, 180 - h, n=5), "currentColor", W)
    b += pts_path(arc_pts(x, cy, rx, ry, 180 + h, 270, n=5), "currentColor", W)
    b += pts_path(arc_pts(x, cy, rx, ry, -90, 90, n=14), "currentColor", W)
    if x in (xs[1], xs[4]):
        px, py = ell_pt(x, cy, rx, ry, 40)
        dx, dy = ell_tan(rx, ry, 40, 1)
        b += chevron(px, py, dx, dy, ORG, 3.2, 13)
for sg in (-1, 1):
    P = cubic((x1, cy), (x1 + 70, cy + sg * 100), (x0 - 70, cy + sg * 100), (x0, cy))
    b += pts_path(P, BLUE, 2.0, "6 4")
    b += chev_on(P, 30, BLUE)
b += text(x1 + 20, cy - 14, "B", BLUE, 16, "start", "700")
b += text(xs[1] + rx + 8, cy + 36, "I", ORG, 16, "start", "700")
fig4c = wrap(VB, "Ống dây dài nhìn xiên: bên trong lòng ống đường sức song song với trục, cách đều; bên ngoài khép kín như nam châm thẳng; nửa vòng phía trước đè lên đường sức, nửa phía sau bị đường sức che",
             b, "Hình 4c. Ống dây: trong lòng ống <strong>B</strong> đều, song song trục ống.")

# ------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in (("1", fig1), ("2", fig2), ("3", fig3), ("4A", fig4a), ("4B", fig4b), ("4C", fig4c)):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
