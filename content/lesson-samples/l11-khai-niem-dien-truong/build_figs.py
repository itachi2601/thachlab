"""Sinh 4 hình SVG cho "Bài 17. Khái niệm điện trường" (Vật lí 11) và thay các mốc
<!--FIGn--> trong theory.src.html -> theory.html. Chạy từ thư mục này: python3 build_figs.py
Hình được kiểm bằng toạ độ (assert) để mũi tên đúng chiều vật lí và hình bình hành khép kín.
"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from svg_lib import *  # noqa: E402,F403


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" '
            f'stroke-width="{w}"{d} opacity="{op}"/>')


def arr(p, c, x1, y1, x2, y2, w=2.5):
    return arrow(p, c, f"{x1:.1f}", f"{y1:.1f}", f"{x2:.1f}", f"{y2:.1f}", w)


def charge(x, y, sign, r=14):
    col = RED if sign > 0 else BLUE
    s = f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" fill-opacity="0.25" stroke="{col}" stroke-width="2"/>'
    s += line(x - 7, y, x + 7, y, "currentColor", 2.4)
    if sign > 0:
        s += line(x, y - 7, x, y + 7, "currentColor", 2.4)
    return s


def sub(base, idx, x, y, c="currentColor", size=14, anchor="start", weight="700", rest=""):
    """Nhãn có chỉ số dưới, không dùng KaTeX trong SVG; rest = phần chữ sau chỉ số."""
    tail = f'<tspan font-size="{size - 1}">{rest}</tspan>' if rest else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}">{base}<tspan baseline-shift="sub" font-size="{size - 4}">{idx}</tspan>{tail}</text>')


def unit(dx, dy):
    n = math.hypot(dx, dy)
    return dx / n, dy / n


# ------------------------------------------------ Hình 1: vectơ E quanh Q > 0 và Q < 0
b = defs("f1")
R, L = 60, 34  # điểm xét cách Q 60 px, mũi tên E dài 34 px (cùng r nên cùng độ lớn)
for cx, sign in ((110, 1), (330, -1)):
    cy = 112
    b += charge(cx, cy, sign)
    for k in range(8):
        t = k * math.pi / 4
        ux, uy = math.cos(t), math.sin(t)
        px, py = cx + R * ux, cy + R * uy
        b += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3" fill="currentColor"/>'
        if sign > 0:   # dương: E hướng RA xa Q
            x2, y2 = px + L * ux, py + L * uy
        else:          # âm: E hướng VỀ phía Q
            x2, y2 = px - L * ux, py - L * uy
        # kiểm chiều: đầu mũi tên xa Q hơn gốc với Q>0, gần Q hơn với Q<0
        d0, d1 = math.hypot(px - cx, py - cy), math.hypot(x2 - cx, y2 - cy)
        assert (d1 > d0) if sign > 0 else (d1 < d0 and d1 > 14 + 8)
        b += arr("f1", "r", px, py, x2, y2)
    b += text(cx + R + 4, cy - 10, "M", "currentColor", 12, "start", "700")
b += text(110, 228, "Q &gt; 0: E hướng ra xa Q", RED, 13, "middle", "700")
b += text(330, 228, "Q &lt; 0: E hướng về Q", BLUE, 13, "middle", "700")
fig1 = wrap("0 0 440 240", "Vectơ cường độ điện trường tại các điểm cách đều điện tích: hướng ra xa điện tích dương, hướng về điện tích âm",
            b, "Hình 1. Các điểm cách đều Q có E bằng nhau về độ lớn. Q dương: E hướng ra xa Q; Q âm: E hướng về Q.")

# ------------------------------------------------ Hình 2: đường sức điện tích dương / âm
b = defs("f2")
for cx, sign in ((110, 1), (330, -1)):
    cy = 108
    b += charge(cx, cy, sign)
    for k in range(8):
        t = k * math.pi / 4 + math.pi / 8
        ux, uy = math.cos(t), math.sin(t)
        b += line(cx + 18 * ux, cy + 18 * uy, cx + 96 * ux, cy + 96 * uy, "currentColor", 1.6, "", 0.75)
        r_a, r_b = (50, 66) if sign > 0 else (66, 50)  # dương: mũi chỉ ra; âm: mũi chỉ vào
        assert (r_b > r_a) == (sign > 0)
        b += arr("f2", "r", cx + r_a * ux, cy + r_a * uy, cx + r_b * ux, cy + r_b * uy, 2.2)
b += text(110, 226, "Dương: đường sức đi ra", RED, 13, "middle", "700")
b += text(330, 226, "Âm: đường sức đi vào", BLUE, 13, "middle", "700")
fig2 = wrap("0 0 440 238", "Đường sức điện của điện tích dương hướng ra ngoài, của điện tích âm hướng vào trong",
            b, "Hình 2. Đường sức của một điện tích: ra từ điện tích dương tới vô cực, từ vô cực về điện tích âm. Gần điện tích đường sức mau: điện trường mạnh.")

# ------------------------------------------------ Hình 3: quy tắc hình bình hành
b = defs("f3")
M = (120.0, 196.0)
E1 = (170.0, -30.0)
E2 = (60.0, -140.0)
T1 = (M[0] + E1[0], M[1] + E1[1])
T2 = (M[0] + E2[0], M[1] + E2[1])
T = (M[0] + E1[0] + E2[0], M[1] + E1[1] + E2[1])
# hình bình hành: T1->T song song, bằng E2; T2->T song song, bằng E1
assert (T[0] - T1[0], T[1] - T1[1]) == E2 and (T[0] - T2[0], T[1] - T2[1]) == E1
b += line(*T1, *T, BLUE, 1.6, "5 4", 0.8) + line(*T2, *T, RED, 1.6, "5 4", 0.8)
b += arr("f3", "r", *M, *T1, 3) + arr("f3", "b", *M, *T2, 3) + arr("f3", "g", *M, *T, 3.2)
t1, t2 = math.atan2(E1[1], E1[0]), math.atan2(E2[1], E2[0])
ra = 34
p1 = (M[0] + ra * math.cos(t1), M[1] + ra * math.sin(t1))
p2 = (M[0] + ra * math.cos(t2), M[1] + ra * math.sin(t2))
b += f'<path d="M{p1[0]:.1f},{p1[1]:.1f} A{ra},{ra} 0 0 0 {p2[0]:.1f},{p2[1]:.1f}" fill="none" stroke="currentColor" stroke-width="1.5"/>'
tm = (t1 + t2) / 2
tm2 = t1 + 0.28 * (t2 - t1)
b += text(M[0] + 44 * math.cos(tm2), M[1] + 44 * math.sin(tm2) + 4, "α", "currentColor", 14, "middle", "700")
b += f'<circle cx="{M[0]}" cy="{M[1]}" r="4" fill="currentColor"/>' + text(M[0] - 8, M[1] + 16, "M", "currentColor", 13, "end", "700")
b += sub("E", "1", T1[0] + 6, T1[1] + 18, RED)
b += sub("E", "2", T2[0] - 10, T2[1] + 2, BLUE, 14, "end")
b += text(T[0] + 8, T[1] + 6, "E", GRN, 15, "start", "700")
b += text(14, 22, "E = E₁ + E₂ (cộng vectơ)", "currentColor", 12, "start", "600")
fig3 = wrap("0 0 440 220", "Quy tắc hình bình hành: vectơ E tổng hợp là đường chéo của hình bình hành dựng trên E1 và E2",
            b, "Hình 3. Quy tắc hình bình hành: E (lục) là đường chéo dựng trên E₁ (đỏ) và E₂ (xanh), α là góc giữa hai vectơ.")

# ------------------------------------------------ Hình 4: bài toán mẫu (MA = 3 cm, MB = 4 cm, AB = 5 cm)
b = defs("f4")
S = 28.0                     # px mỗi cm
A = (160.0, 196.0)
B = (A[0] + 5 * S, A[1])
M = (A[0] + 1.8 * S, A[1] - 2.4 * S)   # chân đường cao cách A 9/5 cm, cao 12/5 cm
assert abs(math.dist(M, A) - 3 * S) < 1e-6 and abs(math.dist(M, B) - 4 * S) < 1e-6
uA = unit(A[0] - M[0], A[1] - M[1])      # M -> A
uB = unit(B[0] - M[0], B[1] - M[1])      # M -> B
assert abs(uA[0] * uB[0] + uA[1] * uB[1]) < 1e-9   # vuông góc tại M
K = 80.0 / 1e5               # px trên mỗi V/m
E1v, E2v = 1.2e5, 9e4
# q1 > 0 tại A: E1 hướng RA XA A (ngược M->A); q2 < 0 tại B: E2 hướng VỀ B (cùng M->B)
d1 = (-uA[0], -uA[1])
d2 = uB
T1 = (M[0] + K * E1v * d1[0], M[1] + K * E1v * d1[1])
T2 = (M[0] + K * E2v * d2[0], M[1] + K * E2v * d2[1])
T = (T1[0] + T2[0] - M[0], T1[1] + T2[1] - M[1])
assert math.dist(T1, A) > math.dist(M, A)          # E1 đi ra xa A
assert math.dist(T2, B) < math.dist(M, B)          # E2 đi về phía B
assert abs(math.dist(M, T) - K * 1.5e5) < 1e-6     # |E| = 1,5.10^5 V/m
b += line(*A, *B, "currentColor", 1.4, "4 4", 0.6) + line(*A, *M, "currentColor", 1.4, "4 4", 0.6) + line(*M, *B, "currentColor", 1.4, "4 4", 0.6)
c1 = (M[0] + 10 * uA[0], M[1] + 10 * uA[1])
c3 = (M[0] + 10 * uB[0], M[1] + 10 * uB[1])
c2 = (c1[0] + 10 * uB[0], c1[1] + 10 * uB[1])
b += f'<polyline fill="none" stroke="currentColor" stroke-width="1.3" points="{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {c3[0]:.1f},{c3[1]:.1f}"/>'
b += line(*T1, *T, BLUE, 1.5, "5 4", 0.8) + line(*T2, *T, RED, 1.5, "5 4", 0.8)
b += arr("f4", "r", *M, *T1, 3) + arr("f4", "b", *M, *T2, 3) + arr("f4", "g", *M, *T, 3.2)
b += charge(A[0], A[1], 1, 11) + charge(B[0], B[1], -1, 11)
b += f'<circle cx="{M[0]:.1f}" cy="{M[1]:.1f}" r="4" fill="currentColor"/>'
b += text(M[0] - 10, M[1] - 4, "M", "currentColor", 14, "end", "700")
b += text(A[0], A[1] + 30, "A", "currentColor", 14, "middle", "700") + text(B[0], B[1] + 30, "B", "currentColor", 14, "middle", "700")
b += sub("q", "1", A[0], A[1] + 48, RED, 13, "middle", rest=" = +12 nC")
b += sub("q", "2", B[0], B[1] + 48, BLUE, 13, "middle", rest=" = −16 nC")
b += text((A[0] + B[0]) / 2, A[1] + 18, "5 cm", "currentColor", 11, "middle", "400")
mA = ((A[0] + M[0]) / 2, (A[1] + M[1]) / 2)
b += text(mA[0] - 8, mA[1] + 4, "3 cm", "currentColor", 11, "end", "400")
b += text(B[0] - 4, B[1] - 20, "4 cm", "currentColor", 11, "start", "400")
b += sub("E", "1", T1[0] + 8, T1[1] + 6, RED)
b += sub("E", "2", 224, 176, BLUE)
b += text(T[0] + 8, T[1] + 6, "E", GRN, 15, "start", "700")
fig4 = wrap("0 36 440 222", "Bài toán mẫu: q1 dương tại A, q2 âm tại B, tam giác AMB vuông tại M; E1 hướng ra xa A, E2 hướng về B, E là đường chéo hình chữ nhật",
            b, "Hình 4. Tam giác AMB vuông tại M nên E₁ ⊥ E₂. E₁ (đỏ) ra xa A vì q₁ &gt; 0; E₂ (xanh) hướng về B vì q₂ &lt; 0; E (lục) là đường chéo.")

here = pathlib.Path(__file__).resolve().parent
h = (here / "theory.src.html").read_text(encoding="utf8")
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert h.count(f"<!--FIG{n}-->") == 1, n
    h = h.replace(f"<!--FIG{n}-->", f)
(here / "theory.html").write_text(h, encoding="utf8")
print("ok", len(h))
