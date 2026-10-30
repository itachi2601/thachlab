"""Sinh 3 hình SVG cho bài Bài tập về sóng (Vật lí 11) và thay mốc <!--FIGn--> trong theory.src.html.
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

# ---------- Hình 1: bản đồ 4 họ (chữ ≥ 14, mỗi từ khoá một dòng ngắn)
b = ""
cards = [
    (8, 8, BLUE, "A. Sóng cơ, điện từ", ("n ngọn, cách nhau d", "cường độ sóng", "tần số, bước sóng")),
    (224, 8, RED, "B. Giao thoa sóng cơ", ("hai nguồn A, B", "cực đại, cực tiểu", "trên đoạn AB")),
    (8, 134, ORG, "C. Khe Young", ("a, D, khoảng vân", "vân sáng, vân tối", "trùng vân")),
    (224, 134, GRN, "D. Sóng dừng", ("dây, nút, bụng", "đầu cố định", "đầu tự do")),
]
for x, y, c, t, lines in cards:
    b += f'<rect x="{x}" y="{y}" width="208" height="116" rx="10" fill="none" stroke="{c}" stroke-width="2.4"/>'
    b += text(x + 14, y + 28, t, c, 15, "start", "700")
    for i, l in enumerate(lines):
        b += text(x + 14, y + 56 + 22 * i, l, "currentColor", 14, "start", "400")
fig1 = wrap("0 0 440 258", "Bản đồ bốn họ bài tập sóng và từ khoá trong đề giúp nhận ra từng họ",
            b, "Hình 1. Bốn họ gom 15 dạng: nhìn <strong>từ khoá trong đề</strong> là biết dùng công thức nào.")

# ---------- Hình 2: AB = 4λ, 7 cực đại, 8 cực tiểu
# Trên AB: d2 - d1 = AB - 2x  =>  cực đại x = (2 - k/2)λ, cực tiểu x = (2 - (k+½)/2)λ
x0, px, y = 40, 90, 84   # px / lambda
b = ""
b += seg(x0, y, x0 + 4 * px, y, "currentColor", 1.4, "", .5)
b += seg(x0, y - 22, x0, y + 22, "currentColor", 3) + seg(x0 + 4 * px, y - 22, x0 + 4 * px, y + 22, "currentColor", 3)
b += text(x0, y + 44, "A", "currentColor", 15, "middle", "700") + text(x0 + 4 * px, y + 44, "B", "currentColor", 15, "middle", "700")
for k in range(-3, 4):
    b += dot(x0 + (2 - k / 2) * px, y, 6, RED)
for k in range(-4, 4):
    b += dot(x0 + (2 - (k + .5) / 2) * px, y, 4.5, BLUE)
# khoảng cách hai cực đại liền kề = λ/2 (k = 0 và k = -1)
xa, xb, yb = x0 + 2 * px, x0 + 2.5 * px, y - 26
b += seg(xa, yb, xb, yb, "currentColor", 1.6) + seg(xa, yb - 6, xa, yb + 6, "currentColor", 1.6) + seg(xb, yb - 6, xb, yb + 6, "currentColor", 1.6)
b += text((xa + xb) / 2, yb - 10, "λ/2", "currentColor", 14, "middle", "700")
b += text(x0, 24, "Hai nguồn cùng pha, AB = 4λ", "currentColor", 15, "start", "700")
b += dot(20, 160, 6, RED) + text(34, 165, "cực đại: 7 điểm, k = −3 … 3", RED, 14, "start", "700")
b += dot(20, 188, 4.5, BLUE) + text(34, 193, "cực tiểu: 8 điểm, k + ½ = −3,5 … 3,5", BLUE, 14, "start", "700")
fig2 = wrap("0 0 440 206", "Trên đoạn AB bằng 4 bước sóng, hai nguồn cùng pha: 7 cực đại và 8 cực tiểu xen kẽ, hai cực đại liền kề cách nhau nửa bước sóng, A và B không phải điểm đếm",
            b, "Hình 2. Với $AB=4\\lambda$: cực đại xen kẽ cực tiểu, hai cực đại liền kề cách nhau $\\tfrac{\\lambda}{2}$. A, B <strong>không được đếm</strong>.")
fig2 = fig2.replace('<figure class="fig" data-tl="1">', '<figure class="fig" data-tl="1" data-exp="tn-l11-baitapsong-02">', 1)

# ---------- Hình 3: một đầu cố định, một đầu tự do, L = 5λ/4 (n = 2)
L, lam, ya, amp = 360, 288, 104, 44
x0 = 24
b = ""
env = [(x0 + x, ya - amp * math.sin(2 * math.pi * x / lam)) for x in range(0, L + 1, 4)]
env2 = [(x, 2 * ya - y) for x, y in env]
b += seg(x0, ya, x0 + L + 20, ya, "currentColor", 1, "", .35)
b += poly(env, GRN, 2.6) + poly(env2, GRN, 1.8, "5 4", .55)
b += seg(x0, ya - 50, x0, ya + 50, "currentColor", 3.5)
for x in (0, lam / 2, lam):                      # nút: sin(2πx/λ) = 0
    b += dot(x0 + x, ya, 5)
for x in (lam / 4, 3 * lam / 4, 5 * lam / 4):    # bụng: |sin| = 1, lấy điểm trên nét liền
    b += dot(x0 + x, ya - amp * math.sin(2 * math.pi * x / lam), 5.5, ORG)
b += f'<circle cx="{x0+L}" cy="{ya-amp}" r="9" fill="none" stroke="{ORG}" stroke-width="2"/>'
b += text(x0, 30, "Đầu cố định (nút)", "currentColor", 14, "start", "700")
b += text(x0 + L - 4, 30, "Đầu tự do (bụng)", ORG, 14, "end", "700")
b += text(x0, 180, "L = 5λ/4 = (2n + 1)·λ/4 với n = 2", GRN, 15, "start", "700")
b += dot(x0 + 6, 203, 5) + text(x0 + 20, 208, "nút: 3 điểm, kể cả đầu cố định", "currentColor", 14, "start", "400")
b += dot(x0 + 6, 229, 5.5, ORG) + text(x0 + 20, 234, "bụng: 3 điểm, kể cả đầu tự do", "currentColor", 14, "start", "400")
fig3 = wrap("0 0 440 246", "Sóng dừng trên dây một đầu cố định một đầu tự do với L bằng năm phần tư bước sóng: 3 nút và 3 bụng",
            b, "Hình 3. Một đầu cố định (nút), một đầu tự do (bụng): $L=(2n+1)\\tfrac{\\lambda}{4}$. Hình vẽ $n=2$ nên có $n+1=3$ bụng và 3 nút.")
fig3 = fig3.replace('<figure class="fig" data-tl="1">', '<figure class="fig" data-tl="1" data-exp="tn-l11-baitapsong-04">', 1)

h = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3), 1):
    assert f"<!--FIG{n}-->" in h
    h = h.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(h)
print("ok", len(h), "bytes,", h.count('<figure class="fig"'), "hình")
