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
b = defs("f1")
b += text(14, 22, "Đứng xa · sau tấm chắn · bấm nút từ xa", "currentColor", 12, "start", "700")
b += line(16, 206, 424, 206, "currentColor", 2, "", 0.9)
b += rect(26, 176, 96, 24, "rgba(148,163,184,.18)", "currentColor", 2, 4)      # bệnh nhân
b += text(74, 192, "bệnh nhân", "currentColor", 10, "middle", "600")
b += f'<circle cx="74" cy="170" r="7" fill="{ORG}"/>'                          # nguồn
b += text(30, 146, "nguồn Ir-192", ORG, 11, "start", "700")
b += line(48, 152, 68, 164, ORG, 1.2, "4 3", 0.9)
for x2, y2 in ((244, 124), (244, 158), (244, 192)):                            # chùm tia gamma
    b += arrow("f1", "o", 84, 170, x2, y2, 2.4)
b += text(112, 112, "tia gamma", ORG, 11, "start", "700")
b += rect(250, 108, 16, 96, "rgba(148,163,184,.45)", "currentColor", 2, 3)     # tấm chắn chì
b += text(258, 100, "tấm chắn chì", "currentColor", 11, "middle", "700")
b += person(340, 206, 0.72)                                                    # người
b += rect(331, 146, 16, 10, "rgba(52,211,153,.35)", GRN, 1.5, 2)               # liều kế
b += text(352, 155, "liều kế", GRN, 10, "start", "600")
b += line(74, 224, 340, 224, "currentColor", 1.2, "5 4", 0.8)                  # khoảng cách
b += line(74, 218, 74, 230, "currentColor", 1.2)
b += line(340, 218, 340, 230, "currentColor", 1.2)
b += text(207, 240, "khoảng cách 3 m", "currentColor", 10, "middle", "600")
fig1 = wrap("0 0 440 250",
            "Sơ đồ xạ trị áp sát trong bệnh viện: nguồn đặt sát khối u, tấm chắn chì ở giữa, kỹ thuật viên đứng xa đeo liều kế",
            b, "Hình 1. Xạ trị áp sát: nguồn sát khối u, người đứng xa sau tấm chắn chì, đeo liều kế — đủ ba nguyên tắc an toàn.")

# ------------------------------------------------------- Hình 2: thang liều quen thuộc (lôgarit)
b = defs("f2")
b += text(20, 30, "liều (mSv, thang lôgarit)", "currentColor", 10, "start", "600")
b += line(30, 140, 420, 140, "currentColor", 2)
b += (f'<rect x="201" y="126" width="219" height="28" rx="4" fill="rgba(248,113,113,.13)" '
      f'stroke="{RED}" stroke-width="1" stroke-dasharray="4 3"/>')
b += text(285, 120, "vùng vượt giới hạn nghề", RED, 10, "middle", "700")
for x, lab in ((45, "0,1"), (113, "1"), (181, "10"), (249, "100"), (317, "1000"), (385, "10000")):
    b += line(x, 134, x, 146, "currentColor", 1.4)
    b += text(x, 162, lab, "currentColor", 9, "middle", "600")
# các mốc liều: (x, nhãn, màu, hàng)
for x, lab, col, hang in ((45, "X-quang ngực 0,1", BLUE, "tren"),
                          (139, "phông tự nhiên 2,4", GRN, "duoi"),
                          (170, "chụp CT 7", ORG, "tren"),
                          (201, "giới hạn nghề 20", RED, "duoi"),
                          (358, "gây chết 4000", RED, "tren")):
    b += dot(x, 140, 3.5, col)
    if hang == "tren":
        b += line(x, 128, x, 102, col, 1.2, "4 3", 0.85)
        if x == 358:
            b += text(428, 96, lab, col, 10, "end", "700")
        else:
            b += text(x - 9, 96, lab, col, 10, "start", "700")
    else:
        b += line(x, 152, x, 186, col, 1.2, "4 3", 0.85)
        if x == 139:
            b += text(x - 17, 200, lab, col, 10, "end", "700")
        else:
            b += text(x + 9, 200, lab, col, 10, "start", "700")
b += text(20, 228, "hai vạch liền nhau cách nhau 10 lần", "currentColor", 9, "start", "500")
fig2 = wrap("0 0 440 240",
            "Thang liều lôgarit với các mốc: chụp X-quang ngực, phông tự nhiên, chụp CT, giới hạn nghề nghiệp và liều gây chết",
            b, "Hình 2. Thang liều lôgarit: X-quang ngực 0,1 mSv · phông tự nhiên 2,4 mSv/năm · chụp CT 7 mSv · giới hạn nghề nghiệp 20 mSv/năm.")

# ------------------------------------------------------- Hình 3: suất liều giảm theo bình phương khoảng cách
b = defs("f3")


def xt(d):
    return 56 + (d - 0.8) * 148.3


b += line(56, 190, 420, 190, "currentColor", 2)
b += line(56, 190, 56, 40, "currentColor", 2)
b += text(44, 26, "H (%)", "currentColor", 11, "end", "600")
b += text(420, 226, "d (m)", "currentColor", 11, "end", "600")
for pct in (0, 25, 50, 75, 100):
    y = 190 - 1.5 * pct
    b += line(50, y, 56, y, "currentColor", 1.4)
    b += text(44, y + 3.5, str(pct), "currentColor", 9, "end", "600")
for d in (1, 1.5, 2, 2.5, 3):
    b += line(xt(d), 190, xt(d), 196, "currentColor", 1.4)
for d in (1, 2, 3):
    b += text(xt(d), 208, str(d), "currentColor", 10, "middle", "600")
pts = []
d = 1.0
while d <= 3.201:
    pts.append(f"{xt(d):.1f},{190 - 150 / (d * d):.1f}")
    d += 0.05
b += f'<polyline fill="none" stroke="{GRN}" stroke-width="2.4" points="{" ".join(pts)}"/>'
for d, lab in ((1, "100%"), (1.5, "44%"), (2, "25%"), (3, "11%")):
    b += dot(xt(d), 190 - 150 / (d * d), 4, GRN)
    b += text(xt(d) + 7, 190 - 150 / (d * d) - 4, lab, GRN, 11, "start", "700")
b += line(xt(1), 44, xt(2), 44, "currentColor", 1.2, "5 4", 0.8)
b += line(xt(2), 44, xt(2), 148, "currentColor", 1.2, "5 4", 0.8)
b += text(150, 34, "d gấp đôi → H còn 1/4", "currentColor", 10, "start", "600")
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
