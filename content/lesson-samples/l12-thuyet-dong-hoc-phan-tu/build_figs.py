"""Sinh 4 hình SVG cho bài "Bài 5. Thuyết động học phân tử chất khí" (Vật lí 12)
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


def poly(pts, c, w=2.6, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    s = " ".join(f"{x:g},{y:g}" for x, y in pts)
    return f'<polyline fill="none" stroke="{c}" stroke-width="{w}"{d} points="{s}"/>'


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


def trace_bounce(start, v, n_pts, box):
    """Đường đi va đập trong bình chữ nhật, đúng định luật phản xạ gương:
    gặp thành thì ĐẢO DẤU thành phần pháp tuyến và GIỮ NGUYÊN thành phần tiếp tuyến.
    Trả về danh sách các điểm chạm thành (điểm đầu cũng nằm trên thành)."""
    x0, x1, y0, y1 = box
    x, y = start
    vx, vy = v
    pts = [(round(x, 1), round(y, 1))]
    for _ in range(n_pts - 1):
        ts = []
        if vx > 0:
            ts.append(((x1 - x) / vx, "x"))
        elif vx < 0:
            ts.append(((x0 - x) / vx, "x"))
        if vy > 0:
            ts.append(((y1 - y) / vy, "y"))
        elif vy < 0:
            ts.append(((y0 - y) / vy, "y"))
        t, axis = min((c for c in ts if c[0] > 1e-9), key=lambda c: c[0])
        x, y = x + vx * t, y + vy * t
        if axis == "x":
            vx = -vx
        else:
            vy = -vy
        pts.append((round(x, 1), round(y, 1)))
    return pts


# ======================================================= Hình 1: vì sao hạt bụi nhảy múa
b = defs("f1")
b += text(14, 24, "Hạt khói bị phân tử khí đập lệch", "currentColor", 13, "start", "700")
b += rect(12, 36, 396, 190, "rgba(148,163,184,.08)", "currentColor", 1.6, 12)
# các phân tử khí
for x, y in ((70, 80), (120, 52), (300, 62), (350, 150), (86, 180), (330, 196)):
    b += dot(x, y, 5, BLUE)
# mũi tên va đập: dài ngắn khác nhau, không cân bằng
b += arrow("f1", "b", 76, 84, 186, 106, 2.2)
b += arrow("f1", "b", 124, 57, 196, 96, 2.2)
b += arrow("f1", "b", 296, 67, 226, 98, 2.2)
b += arrow("f1", "b", 344, 146, 232, 132, 2.2)
b += arrow("f1", "b", 92, 176, 192, 142, 2.2)
b += arrow("f1", "b", 324, 190, 230, 148, 2.2)
# hạt bụi
b += f'<circle cx="210" cy="120" r="20" fill="rgba(248,113,113,.28)" stroke="{RED}" stroke-width="2.5"/>'
b += dot(210, 120, 8, RED)
b += text(210, 172, "hạt khói", RED, 12.5, "middle", "700")
# hướng bị đẩy lệch (hợp lực không triệt tiêu)
b += arrow("f1", "o", 236, 124, 306, 124, 2.6)
b += text(272, 112, "hạt bị đẩy lệch", ORG, 11, "middle", "700")
b += text(16, 214, "chấm xanh: phân tử khí · mũi tên xanh: hướng va đập (dài ngắn khác nhau)", "currentColor", 10.5, "start", "500")
fig1 = wrap("0 0 420 240", "Hạt khói ở giữa bị nhiều phân tử khí va đập từ mọi phía với mức khác nhau, nên bị đẩy lệch",
            b, "Hình 1. Va đập từ mọi phía không cân bằng đẩy hạt khói lệch liên tục.")

# ======================================================= Hình 2: ba nội dung thuyết động học phân tử
b = defs("f2")
b += text(14, 26, "Ba điều phải nhớ của thuyết động học phân tử", "currentColor", 12.5, "start", "700")
# a) kích thước bé xíu so với khoảng cách
b += text(14, 52, "a) Kích thước bé xíu", "currentColor", 11.5, "start", "700")
b += dot(40, 78, 6, BLUE) + dot(150, 78, 6, BLUE)
b += line(48, 78, 142, 78, "currentColor", 1.4, "4 4", .7)
b += line(48, 72, 48, 84, "currentColor", 1.4, "", .7)
b += line(142, 72, 142, 84, "currentColor", 1.4, "", .7)
b += text(95, 68, "rất xa", "currentColor", 10.5, "middle", "600")
b += text(200, 74, "khoảng cách giữa các phân tử lớn hơn", "currentColor", 11, "start", "500")
b += text(200, 90, "kích thước mỗi phân tử rất nhiều", "currentColor", 11, "start", "500")
# b) hỗn loạn, nóng thì nhanh
b += text(14, 122, "b) Hỗn loạn, không ngừng", "currentColor", 11.5, "start", "700")
for x, y in ((40, 160), (92, 148), (146, 166), (62, 186)):
    b += dot(x, y, 5, ORG)
b += arrow("f2", "o", 46, 156, 74, 140, 1.8)
b += arrow("f2", "o", 98, 144, 120, 128, 1.8)
b += arrow("f2", "o", 152, 162, 176, 148, 1.8)
b += arrow("f2", "o", 68, 182, 96, 194, 1.8)
b += text(200, 152, "nhiệt độ càng cao", "currentColor", 11, "start", "500")
b += text(200, 168, "chuyển động càng nhanh", "currentColor", 11, "start", "500")
# c) va chạm vào thành bình gây áp suất
b += text(14, 222, "c) Va chạm vào thành bình gây áp suất", "currentColor", 11.5, "start", "700")
b += line(384, 238, 384, 300, "currentColor", 5)
b += text(378, 234, "thành bình", "currentColor", 10.5, "end", "500")
for x, y, yt in ((46, 258, 258), (110, 276, 272), (176, 246, 250)):
    b += dot(x, y, 5, BLUE)
b += arrow("f2", "b", 52, 258, 378, 258, 2)
b += arrow("f2", "b", 116, 276, 378, 272, 2)
b += arrow("f2", "b", 182, 246, 378, 250, 2)
fig2 = wrap("0 0 420 314", "Ba nội dung của thuyết động học phân tử chất khí: kích thước bé xíu, chuyển động hỗn loạn không ngừng, va chạm vào thành bình gây áp suất",
            b, "Hình 2. Ba nội dung: phân tử bé xíu so với khoảng cách · chuyển động hỗn loạn, nóng thì nhanh hơn · va chạm thành bình tạo áp suất.")

# ======================================================= Hình 3: mô hình khí lí tưởng
# Bình chứa x=14..194, y=40..180. Đường đi sinh bằng phản xạ gương (trace_bounce):
# mỗi lần gặp thành, thành phần pháp tuyến đổi dấu, thành phần tiếp tuyến giữ nguyên,
# nên hình vẽ đúng định luật phản xạ và không tự cắt nhau.
BOX = (14.0, 194.0, 40.0, 180.0)
PATH = trace_bounce((24.0, 180.0), (170.0, -34.0), 5, BOX)
assert all(abs(p[0] - BOX[0]) < .05 or abs(p[0] - BOX[1]) < .05
           or abs(p[1] - BOX[2]) < .05 or abs(p[1] - BOX[3]) < .05 for p in PATH), PATH
b = defs("f3")
b += text(14, 26, "Mô hình khí lí tưởng", "currentColor", 14, "start", "700")
b += rect(14, 40, 180, 140, "rgba(148,163,184,.08)", "currentColor", 2.4, 6)
b += poly(PATH, GRN, 2.6)
for x, y in PATH:  # chấm xanh ở MỌI điểm chạm thành, kể cả điểm đầu và điểm cuối
    b += dot(x, y, 3.8, GRN)
for i in (0, 2):  # đầu mũi tên chỉ chiều chuyển động ở giữa đoạn 1 và đoạn 3
    (xa, ya), (xb, yb) = PATH[i], PATH[i + 1]
    b += chevron((xa + xb) / 2 + (xb - xa) * .08, (ya + yb) / 2 + (yb - ya) * .08, xb - xa, yb - ya, GRN, 2.6, 11)
b += text(104, 202, "mỗi đoạn: bay thẳng đều", GRN, 14, "middle", "600")
# Khung phải: một lần va chạm với thành (theo ý OpenStax College Physics 2e, Hình 13.22):
# thành phần vuông góc với thành đổi chiều, thành phần song song giữ nguyên.
def vsub(x, y, base, sub, anchor="middle", c="currentColor", size=13):
    return (f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="700" font-style="italic" text-anchor="{anchor}">'
            f'{base}<tspan font-size="{size - 3}" dy="3">{sub}</tspan></text>')
WX, PY = 402, 118
b += text(214, 56, "Một lần va chạm với thành", "currentColor", 12.5, "start", "700")
b += line(WX, 66, WX, 172, "currentColor", 5)
b += arrow("f3", "g", 306, 158, WX - 3, PY + 2, 2.6)       # vận tốc tới
b += arrow("f3", "g", WX - 3, PY - 2, 306, 78, 2.6)        # vận tốc sau va chạm
b += line(306, 158, WX - 3, 158, "currentColor", 1.6, "5 4", .75)   # thành phần x tới
b += line(306, 158, 306, 78, "currentColor", 1.6, "5 4", .75)       # thành phần y (không đổi)
b += line(306, 118, WX - 3, 118, "currentColor", 1.6, "5 4", .75)   # thành phần x sau va chạm
b += chevron(WX - 3, 158, 1, 0, BLUE, 2.2, 9)
b += chevron(306, 118, -1, 0, ORG, 2.2, 9)
b += vsub(354, 174, "v", "x", "middle", BLUE)
b += vsub(354, 112, "v", "x", "middle", ORG)
b += vsub(298, 142, "v", "y", "end")
b += vsub(298, 100, "v", "y", "end")
b += vsub(214, 196, "v", "x", "start", BLUE, 12) + text(232, 196, "vuông góc thành: đảo chiều", BLUE, 12, "start", "600")
b += vsub(214, 214, "v", "y", "start", "currentColor", 12) + text(232, 214, "song song thành: giữ nguyên", "currentColor", 12, "start", "600")
fig3 = wrap("0 0 420 220", "Bình chứa với đường đi gấp khúc của phân tử khí lí tưởng: mỗi đoạn thẳng nối hai lần va chạm với thành bình, va chạm hoàn toàn đàn hồi nên bật ngược lại; bên phải là một lần va chạm với thành, vận tốc vuông góc đảo chiều còn vận tốc song song giữ nguyên",
            b, "Hình 3. Giữa hai va chạm, phân tử bay thẳng đều; chấm xanh là điểm gặp thành.<br>"
            "Bên phải: v<sub>x</sub> đảo chiều, v<sub>y</sub> giữ nguyên.<br>"
            "Vẽ lại theo OpenStax, College Physics 2e, Hình 13.22 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e")

# ======================================================= Hình 4: 1 mol khí ở điều kiện tiêu chuẩn
b = defs("f4")
b += text(14, 24, "1 mol khí ở điều kiện tiêu chuẩn", "currentColor", 12.5, "start", "700")
for x, ten, kl in ((14, "N₂", "28 g"), (148, "O₂", "32 g"), (282, "CO₂", "44 g")):
    b += rect(x, 44, 124, 116, "rgba(148,163,184,.08)", BLUE, 1.8, 10)
    b += text(x + 62, 76, ten, BLUE, 15, "middle", "700")
    b += text(x + 62, 108, "22,4 lít", ORG, 12.5, "middle", "700")
    b += text(x + 62, 140, kl, GRN, 12.5, "middle", "700")
b += text(14, 188, "Cùng thể tích · cùng số phân tử (6,02 × 10²³)", "currentColor", 11.5, "start", "600")
b += text(14, 206, "Khác khối lượng vì khối lượng mol khác nhau.", "currentColor", 11, "start", "500")
b += text(14, 222, "Thể tích mol không phải khối lượng mol.", "currentColor", 11, "start", "500")
fig4 = wrap("0 0 420 238", "Ba bình khí nitrogen, oxygen, carbon dioxide ở điều kiện tiêu chuẩn: mỗi bình 1 mol, cùng thể tích 22,4 lít, khối lượng khác nhau",
            b, "Hình 4. Ở điều kiện tiêu chuẩn, 1 mol khí nào cũng chiếm 22,4 lít và chứa 6,02 × 10²³ phân tử, nhưng khối lượng khác nhau.",
            exp="tn-l12-tdhphantu-03")

# ======================================================= thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
