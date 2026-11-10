"""Sinh 3 hình SVG cho bài "Bài 18. An toàn phóng xạ" (Vật lí 12) và thay các mốc
<!--FIGn--> trong theory.src.html -> theory.html. Chạy từ thư mục này: python3 build_figs.py
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *  # noqa: E402


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def dot(x, y, r=4, c="currentColor"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def rect(x, y, w, h, fill, stroke="currentColor", sw=2, rx=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


# ------------------------------------------------------- Hình 1: cảnh xạ trị áp sát
# Chữ 13–14 (viewBox 440 thu còn ~390 px ở màn 375 → chữ ≥ 11,5 px). Người vẽ riêng (không dùng person():
# hàm đó có lưỡi giày trượt). Ba nguyên tắc = ba nhãn: tấm chắn chì, khoảng cách 3 m, đồng hồ "ở ít phút".
b = defs("f1")
b += line(14, 196, 426, 196, "currentColor", 2, "", 0.9)                       # sàn
b += rect(16, 166, 104, 26, "rgba(148,163,184,.18)", "currentColor", 2, 4)     # bệnh nhân
b += text(68, 184, "bệnh nhân", "currentColor", 13, "middle", "600")
b += f'<circle cx="68" cy="158" r="7" fill="{ORG}"/>'                          # nguồn
b += text(14, 122, "nguồn Ir-192", ORG, 14, "start", "700")
b += line(44, 128, 62, 151, ORG, 1.2, "4 3", 0.9)
for y2 in (114, 150, 186):                                                     # chùm tia gamma
    b += arrow("f1", "o", 78, 158, 234, y2, 2.4)
b += text(118, 100, "tia gamma", ORG, 14, "start", "700")
b += rect(240, 100, 16, 96, "rgba(148,163,184,.45)", "currentColor", 2, 3)     # tấm chắn chì
b += text(248, 90, "tấm chắn chì", "currentColor", 14, "middle", "700")
# người: đầu, thân, tay, chân
px = 340
b += f'<circle cx="{px}" cy="114" r="10" fill="none" stroke="currentColor" stroke-width="2.5"/>'
b += line(px, 124, px, 156, "currentColor", 2.5)
b += line(px, 132, px - 12, 154, "currentColor", 2.5)
b += line(px, 132, px + 12, 154, "currentColor", 2.5)
b += line(px, 156, px - 11, 195, "currentColor", 2.5)
b += line(px, 156, px + 11, 195, "currentColor", 2.5)
b += rect(350, 127, 13, 11, "rgba(52,211,153,.45)", GRN, 1.6, 2)              # liều kế: huy hiệu cạnh ngực, không chạm tay (tay ở y 127–138 có x ≤ 343)
b += text(368, 137, "liều kế", GRN, 14, "start", "700")
# đồng hồ: ở ít phút
b += f'<circle cx="412" cy="162" r="13" fill="none" stroke="{BLUE}" stroke-width="2"/>'
b += line(412, 162, 412, 153, BLUE, 2) + line(412, 162, 419, 165, BLUE, 2)
b += text(432, 192, "ở ít phút", BLUE, 14, "end", "700")
b += line(68, 214, 340, 214, "currentColor", 1.2, "5 4", 0.8)                  # khoảng cách
b += line(68, 208, 68, 220, "currentColor", 1.2)
b += line(340, 208, 340, 220, "currentColor", 1.2)
b += text(204, 234, "khoảng cách 3 m", "currentColor", 14, "middle", "700")
fig1 = wrap("0 72 440 172",
            "Sơ đồ xạ trị áp sát trong bệnh viện: nguồn đặt sát khối u, tấm chắn chì ở giữa, kỹ thuật viên đứng xa 3 m, ở ít phút, đeo liều kế",
            b, "Hình 1. Xạ trị áp sát: nguồn sát khối u; người đứng xa, sau tấm chắn chì, ở ít phút và đeo liều kế — đủ ba nguyên tắc an toàn.")

# ------------------------------------------------------- Hình 2: thang liều quen thuộc (lôgarit)
# Toạ độ: x(v) = 112 + 72·log10(v) → 0,1→40 · 1→112 · 2,4→139 · 7→173 · 20→206 · 4000→371 · 10000→400.
import math


def xl(v):
    return 112 + 72 * math.log10(v)


AX = 110
b = defs("f2")
b += text(14, 20, "liều (mSv), thang lôgarit", "currentColor", 13, "start", "600")
b += (f'<rect x="{xl(20):.0f}" y="{AX-12}" width="{426-xl(20):.0f}" height="24" rx="4" fill="rgba(248,113,113,.13)" '
      f'stroke="{RED}" stroke-width="1" stroke-dasharray="4 3"/>')
b += line(30, AX, 426, AX, "currentColor", 2)
for v, lab in ((0.1, "0,1"), (1, "1"), (10, "10"), (100, "100"), (1000, "1000"), (10000, "10000")):
    x = round(xl(v))
    b += line(x, AX - 6, x, AX + 6, "currentColor", 1.4)
    b += text(x, AX + 30, lab, "currentColor", 13, "middle", "600")
# các mốc liều: (giá trị, nhãn, màu, hàng, neo)
for v, lab, col, hang, anc in ((0.1, "X-quang ngực 0,1", BLUE, "tren", "start"),
                               (2.4, "phông 2,4/năm", GRN, "duoi", "end"),
                               (7, "chụp CT 7", ORG, "tren", "start"),
                               (20, "giới hạn nghề 20/năm", RED, "duoi", "start"),
                               (4000, "gây chết 4000", RED, "tren", "end")):
    x = round(xl(v))
    b += dot(x, AX, 4, col)
    if hang == "tren":
        b += line(x, AX - 8, x, 58, col, 1.2, "4 3", 0.85)
        tx = {"start": x - 8, "end": 432}[anc]
        b += text(tx, 50, lab, col, 14, anc, "700")
    else:
        b += line(x, AX + 8, x, 154, col, 1.2, "4 3", 0.85)
        tx = x + 4 if anc == "end" else x - 6
        b += text(tx, 170, lab, col, 14, anc, "700")
b += text(432, 196, "vùng đỏ: vượt giới hạn nghề", RED, 13, "end", "700")
b += text(14, 220, "mỗi vạch gấp 10 lần vạch trước", "currentColor", 13, "start", "500")
fig2 = wrap("0 0 440 230",
            "Thang liều lôgarit với các mốc: chụp X-quang ngực, phông tự nhiên, chụp CT, giới hạn nghề nghiệp và liều gây chết",
            b, "Hình 2. Thang liều lôgarit, từ X-quang ngực 0,1 mSv tới liều gây chết khoảng 4 000 mSv.")

# ------------------------------------------------------- Hình 3: suất liều giảm theo bình phương khoảng cách
b = defs("f3")


def xt(d):
    return 56 + (d - 0.8) * 148.3


b += line(56, 190, 420, 190, "currentColor", 2)
b += line(56, 190, 56, 40, "currentColor", 2)
b += text(6, 16, "suất liều tương đối (%)", "currentColor", 14, "start", "600")
b += text(420, 228, "d (m)", "currentColor", 14, "end", "600")
for pct in (0, 25, 50, 75, 100):
    y = 190 - 1.5 * pct
    b += line(50, y, 56, y, "currentColor", 1.4)
    b += text(44, y + 5, str(pct), "currentColor", 14, "end", "600")
for d in (1, 1.5, 2, 2.5, 3):
    b += line(xt(d), 190, xt(d), 196, "currentColor", 1.4)
for d in (1, 2, 3):
    b += text(xt(d), 212, str(d), "currentColor", 14, "middle", "600")
pts = []
d = 1.0
while d <= 3.201:
    pts.append(f"{xt(d):.1f},{190 - 150 / (d * d):.1f}")
    d += 0.05
b += f'<polyline fill="none" stroke="{GRN}" stroke-width="2.4" points="{" ".join(pts)}"/>'
for d, lab in ((1, "100%"), (1.5, "44%"), (2, "25%"), (3, "11%")):
    b += dot(xt(d), 190 - 150 / (d * d), 4, GRN)
    b += text(xt(d) + 7, 190 - 150 / (d * d) - 4, lab, GRN, 14, "start", "700")
b += line(xt(1), 44, xt(2), 44, "currentColor", 1.2, "5 4", 0.8)
b += line(xt(2), 44, xt(2), 148, "currentColor", 1.2, "5 4", 0.8)
b += text(150, 36, "d gấp đôi → suất liều còn 1/4", "currentColor", 14, "start", "600")
fig3 = wrap("0 0 440 236",
            "Đồ thị suất liều còn lại theo khoảng cách: giảm nhanh theo bình phương khoảng cách, ở 2 m còn 25 phần trăm",
            b, "Hình 3. Suất liều giảm theo bình phương khoảng cách: ở 2 m còn 25%, ở 3 m còn 11%.")

# ------------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
if "<!--FIG" in src:
    raise SystemExit("còn mốc FIG chưa thay")
print("ok", len(src), "bytes")
