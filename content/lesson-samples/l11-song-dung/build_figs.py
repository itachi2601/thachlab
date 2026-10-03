"""Sinh 4 hình SVG cho bài Sóng dừng (Vật lí 11) và thay các mốc <!--FIGn--> trong theory.src.html.
Chạy: python3 build_figs.py   (từ thư mục bài)
"""
import math
from svg_lib import *

def poly(pts, c, w=2.2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline fill="none" stroke="{c}" stroke-width="{w}"{d} opacity="{op}" points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>'

def dot(x, y, r=4.5, c="currentColor"): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'

def seg(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'

def sine(x0, x1, y0, amp, period, step=4):
    return [(x, y0 - amp * math.sin(2 * math.pi * (x - x0) / period)) for x in range(int(x0), int(x1) + 1, step)]

# ---------------- Hình 1: dây đàn buông (1 bó) và bấm phím (2 bó ngắn hơn)
b = ""
# (a) dây buông, hai đầu cố định, 1 bó
b += text(20, 16, "Dây buông: đoạn rung dài, 1 bó — nốt thấp", "currentColor", 12, "start")
b += seg(30, 32, 30, 92, "currentColor", 3) + seg(410, 32, 410, 92, "currentColor", 3)
b += poly(sine(30, 410, 62, 36, 760), GRN, 2.6)
b += poly(sine(30, 410, 62, -36, 760), GRN, 1.6, "5 4", .5)
b += dot(30, 62, 4) + dot(410, 62, 4)
b += text(20, 112, "đầu cố định", "currentColor", 11, "start", "400")
# (b) bấm phím ở giữa: đoạn rung còn một nửa, 2 bó
b += text(20, 136, "Bấm phím giữa dây: đoạn rung còn một nửa, 2 bó — nốt cao hơn", "currentColor", 12, "start")
b += poly(sine(30, 250, 182, 34, 220), GRN, 2.6)
b += poly(sine(30, 250, 182, -34, 220), GRN, 1.6, "5 4", .5)
b += seg(30, 152, 30, 212, "currentColor", 3)
b += seg(250, 152, 250, 212, "currentColor", 2.5)
b += seg(250, 182, 410, 182, "currentColor", 1.4, "3 3", .35)
b += dot(30, 182, 4) + dot(250, 182, 5, ORG)
b += text(258, 174, "ngón bấm", ORG, 11, "start", "700")
b += text(330, 204, "không rung", "currentColor", 11, "middle", "400")
fig1 = wrap("0 0 440 226",
            "Dây đàn buông rung thành 1 bó; bấm phím cho đoạn rung ngắn còn một nửa thì có 2 bó và nốt cao hơn",
            b,
            "Hình 1. Bấm phím làm đoạn dây rung <strong>ngắn lại</strong>: cùng sợi dây, sóng dừng chuyển từ 1 bó sang 2 bó, nên tần số tăng, nốt cao hơn.")
fig1 = fig1.replace('<figure class="fig" data-tl="1">',
                    '<figure class="fig" data-tl="1" data-exp="tn-l11-songdung-04">', 1)

# ---------------- Hình 2: nút, bụng và khoảng cách
axis, amp, x0, x1, per = 120, 50, 20, 420, 200
b = ""
b += seg(x0, axis - amp, x1, axis - amp, "currentColor", 1, "3 3", .3)
b += seg(x0, axis + amp, x1, axis + amp, "currentColor", 1, "3 3", .3)
b += seg(x0, axis, x1, axis, "currentColor", 1, "", .3)
b += poly(sine(x0, x1, axis, amp, per), BLUE, 2.6)
for k in range(9):
    x = x0 + k * (per // 4)
    if k % 2 == 0:
        b += dot(x, axis, 4.5)
    else:
        b += dot(x, axis - amp if (k // 2) % 2 == 0 else axis + amp, 5, ORG)
# khoảng cách
b += seg(x0, 50, x0, 56, "currentColor", 1.4) + seg(x0 + per // 4, 50, x0 + per // 4, 56, "currentColor", 1.4) + seg(x0, 53, x0 + per // 4, 53, "currentColor", 1.4)
b += text(x0 + per // 8, 44, "λ/4", "currentColor", 11, "middle", "700")
b += seg(x0, 196, x0, 202, "currentColor", 1.4) + seg(x0 + per // 2, 196, x0 + per // 2, 202, "currentColor", 1.4) + seg(x0, 199, x0 + per // 2, 199, "currentColor", 1.4)
b += text(x0 + per // 4, 190, "λ/2", "currentColor", 11, "middle", "700")
b += dot(24, 222, 5) + text(34, 226, "nút: biên độ 0", "currentColor", 11, "start", "400")
b += dot(200, 222, 5, ORG) + text(210, 226, "bụng: biên độ 2A", ORG, 11, "start", "400")
fig2 = wrap("0 0 440 236",
            "Sóng dừng trên dây hai đầu cố định: các nút đứng yên và các bụng dao động mạnh nhất xen kẽ, cách nhau λ/2 và λ/4",
            b,
            "Hình 2. Sóng dừng: <strong>nút</strong> (chấm đen) đứng yên, <strong>bụng</strong> (chấm cam) dao động mạnh nhất. Hai nút liên tiếp cách nhau λ/2; nút và bụng liền kề cách nhau λ/4.")

# ---------------- Hình 3: hai trường hợp điều kiện
b = ""
# (a) hai đầu cố định, 3 bó
b += text(20, 16, "Hai đầu cố định: 3 bó · 4 nút · 3 bụng", "currentColor", 12, "start")
b += seg(20, 32, 420, 32, "currentColor", 1, "3 3", .3) + seg(20, 112, 420, 112, "currentColor", 1, "3 3", .3)
b += poly(sine(20, 420, 72, 40, 266.7), GRN, 2.4)
b += seg(20, 47, 20, 97, "currentColor", 3) + seg(420, 47, 420, 97, "currentColor", 3)
for k in range(4):
    b += dot(20 + k * 133.3, 72, 4.5)
for k in range(3):
    b += dot(20 + 66.7 + k * 133.3, 32 if k % 2 == 0 else 112, 5, ORG)
b += text(20, 130, "l = 3·λ/2", GRN, 11, "start", "700")
# (b) một đầu cố định, một đầu tự do, l = 3λ/4
b += text(20, 158, "Một đầu cố định, một đầu tự do: 2 nút · 2 bụng", "currentColor", 12, "start")
b += seg(20, 174, 420, 174, "currentColor", 1, "3 3", .3) + seg(20, 254, 420, 254, "currentColor", 1, "3 3", .3)
b += poly(sine(20, 420, 214, 40, 533.3), RED, 2.4)
b += seg(20, 189, 20, 239, "currentColor", 3)
b += dot(20, 214, 4.5) + dot(286.7, 214, 4.5) + dot(153.3, 174, 5, ORG) + dot(420, 254, 5, ORG)
b += seg(430, 164, 430, 292, "currentColor", 2.4, "", .6)
b += f'<circle cx="420" cy="254" r="9" fill="none" stroke="{ORG}" stroke-width="2"/>'
b += text(300, 296, "đầu tự do (bụng)", ORG, 11, "middle", "400")
b += text(20, 272, "l = 3·λ/4", RED, 11, "start", "700")
fig3 = wrap("0 0 440 304",
            "Hai trường hợp sóng dừng: hai đầu cố định chiều dài bằng số nguyên lần λ/2; một đầu tự do chiều dài bằng số lẻ lần λ/4",
            b,
            "Hình 3. Trên: hai đầu cố định, dây có 3 bó (l = 3·λ/2). Dưới: một đầu cố định, một đầu tự do, đầu tự do là bụng (l = 3·λ/4, tức k = 1 trong l = (2k+1)·λ/4).")

# ---------------- Hình 4: đường bao biên độ
axis, amp, x0, x1, per = 130, 50, 20, 420, 200
b = defs("f4")
b += poly(sine(x0, x1, axis, amp, per), BLUE, 2.4)
b += poly(sine(x0, x1, axis, -amp, per), BLUE, 1.6, "5 4", .55)
b += seg(x0, axis, x1, axis, "currentColor", 1.2, "", .45)
for k in range(5):
    b += dot(x0 + k * (per // 2), axis, 4.5)
b += dot(70, axis - amp, 5, ORG) + dot(170, axis + amp, 5, ORG)
b += arrow("f4", "o", 70, axis, 70, axis - amp + 2, 2)
b += text(78, axis - 30, "2A", ORG, 12, "start", "700")
b += arrow("f4", "o", 170, axis, 170, axis - amp + 2, 2)
b += arrow("f4", "o", 170, axis, 170, axis + amp - 2, 2)
b += text(178, axis + 6, "4A", ORG, 12, "start", "700")
b += text(425, axis + 5, "x", "currentColor", 12, "start", "700")
b += seg(x0, 210, x0, 216, "currentColor", 1.4) + seg(x0 + per // 2, 210, x0 + per // 2, 216, "currentColor", 1.4) + seg(x0, 213, x0 + per // 2, 213, "currentColor", 1.4)
b += text(x0 + per // 4, 232, "λ/2", "currentColor", 11, "middle", "700")
b += text(x0, 20, "đường bao biên độ: mạnh nhất ở bụng, bằng 0 ở nút", "currentColor", 12, "start")
fig4 = wrap("0 0 440 240",
            "Đường bao biên độ của sóng dừng: bằng 0 tại nút, lớn nhất 2A tại bụng; bụng vung từ +2A tới −2A nên bề rộng là 4A",
            b,
            "Hình 4. Đường bao biên độ: tại nút biên độ bằng 0, tại bụng biên độ bằng 2A. Bụng vung từ +2A xuống −2A nên <strong>bề rộng</strong> vùng dao động của bụng là 4A.")

h = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, f"thiếu mốc FIG{n}"
    h = h.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(h)
print("ok", len(h), "bytes,", h.count('<figure class="fig"'), "hình")
