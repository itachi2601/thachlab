"""Sinh 4 hình SVG cho "Bài 17. Khái niệm điện trường" (Vật lí 11) và thay các mốc
<!--FIGn--> trong theory.src.html -> theory.html. Chạy từ thư mục này: python3 build_figs.py
Hình được kiểm bằng toạ độ (assert) để mũi tên đúng chiều vật lí và hình bình hành khép kín.
"""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *  # noqa: E402,F403


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" '
            f'stroke-width="{w}"{d} opacity="{op}"/>')


def arr(p, c, x1, y1, x2, y2, w=2.5):
    return arrow(p, c, round(x1, 1), round(y1, 1), round(x2, 1), round(y2, 1), w)


def charge(x, y, sign, r=14):
    col = RED if sign > 0 else BLUE
    s = f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" fill-opacity="0.25" stroke="{col}" stroke-width="2"/>'
    s += line(x - 7, y, x + 7, y, "currentColor", 2.4)
    if sign > 0:
        s += line(x, y - 7, x, y + 7, "currentColor", 2.4)
    return s


def sub(base, idx, x, y, c="currentColor", size=14, anchor="start", weight="700", rest=""):
    """Nhãn có chỉ số dưới, không dùng KaTeX trong SVG; rest = phần chữ sau chỉ số."""
    tail = f'<tspan font-size="{max(14, size - 1)}">{rest}</tspan>' if rest else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}">{base}<tspan baseline-shift="sub" font-size="{max(14, size - 3)}">{idx}</tspan>{tail}</text>')


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
    b += text(cx + R + 4, cy - 10, "M", "currentColor", 13, "start", "700")
b += text(110, 228, "Q &gt; 0: E hướng ra xa Q", RED, 13, "middle", "700")
b += text(330, 228, "Q &lt; 0: E hướng về Q", BLUE, 13, "middle", "700")
fig1 = wrap("0 0 440 240", "Vectơ cường độ điện trường tại các điểm cách đều điện tích: hướng ra xa điện tích dương, hướng về điện tích âm",
            b, "Hình 1. Các điểm cách đều Q có E bằng nhau về độ lớn. Q dương: E hướng ra xa Q; Q âm: E hướng về Q.")

# ------------------------------------------------ Hình 1: ảnh OpenStax College Physics 2e, Hình 18.19 (đợt 2, 28/10/2026) — thay SVG vẽ tay
fig1 = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l11-khai-niem-dien-truong/hinh-vecto-e-diem-tich.webp" '
        'alt="Điện trường của điện tích dương Q vẽ hai cách: (a) các mũi tên E hướng ra xa Q; (b) cùng trường đó vẽ bằng đường sức" '
        'loading="lazy" width="1000" height="512" style="max-width:100%;height:auto">'
        '<figcaption>Hình 1. Q &gt; 0: E ra xa Q.<br>(a) Mũi tên. (b) Đường sức.<br>Q &lt; 0: đảo chiều (Hình 2).<br>'
        '<small>Hình: OpenStax, College Physics 2e, Hình 18.19 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>')

# ------------------------------------------------ Hình 2: ảnh OpenStax College Physics 2e, Hình 18.20 (đợt 28/10/2026)
fig2 = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l11-khai-niem-dien-truong/hinh-duong-suc-diem.webp" '
        'alt="Đường sức của ba điện tích điểm: (a) điện tích dương, đường sức hướng ra; (b) điện tích âm cùng độ lớn, đường sức hướng vào; (c) điện tích âm lớn hơn, đường sức mau hơn" '
        'loading="lazy" width="1000" height="368" style="max-width:100%;height:auto">'
        '<figcaption>Hình 2. (a) Điện tích dương: đường sức đi ra.<br>'
        '(b) Điện tích âm: đường sức đi vào.<br>'
        '(c) Điện tích âm lớn hơn: đường sức mau hơn.<br>'
        '<small>Hình: OpenStax, College Physics 2e, Hình 18.20 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>')


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
b += sub("E", "2", T2[0] - 16, T2[1] + 8, BLUE, 14, "end")
b += text(T[0] + 8, T[1] + 6, "E", GRN, 15, "start", "700")
b += text(14, 22, "E = E₁ + E₂ (cộng vectơ)", "currentColor", 13, "start", "600")
fig3 = wrap("0 0 440 220", "Quy tắc hình bình hành: vectơ E tổng hợp là đường chéo của hình bình hành dựng trên E1 và E2",
            b, "Hình 3. Quy tắc hình bình hành: E (lục) là đường chéo dựng trên E₁ (đỏ) và E₂ (xanh), α là góc giữa hai vectơ.")

# ------------------------------------------------ Hình 3: ảnh OpenStax College Physics 2e, Hình 18.21 (đợt 2, 28/10/2026) — thay SVG vẽ tay
fig3 = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l11-khai-niem-dien-truong/hinh-chong-chat-e.webp" '
        'alt="Hai điện tích dương q1 và q2 gây ra tại gốc O các vectơ điện trường E1 và E2; E tổng là đường chéo của hình chữ nhật dựng trên E1, E2" '
        'loading="lazy" width="780" height="768" style="max-width:100%;height:auto">'
        '<figcaption>Hình 3. E=E₁+E₂ (đường chéo).<br>E₁⊥E₂: hình chữ nhật.<br>Sách ghi E<sub>tot</sub>=E, O=M.<br>Số trong hình: √(1,13²+0,56²) ≈ 1,26 (·10⁵ N/C), không phải 1,69.<br>'
        '<small>Hình: OpenStax, College Physics 2e, Hình 18.21 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>')

# ------------------------------------------------ Hình 4: bài toán mẫu (MA = 3 cm, MB = 4 cm, AB = 5 cm)
# Vẽ lại 31/10/2026: phóng to (36 px/cm), chữ ≥ 14, chỉ số 12, nhãn E1 không đè nét, caption mỗi ý một dòng.
b = ""  # đầu V 30° (chevron) của svg_lib, không cần marker
S = 36.0                     # px mỗi cm
A = (130.0, 222.0)
B = (A[0] + 5 * S, A[1])
M = (A[0] + 1.8 * S, A[1] - 2.4 * S)   # chân đường cao cách A 9/5 cm, cao 12/5 cm
assert abs(math.dist(M, A) - 3 * S) < 1e-6 and abs(math.dist(M, B) - 4 * S) < 1e-6
uA = unit(A[0] - M[0], A[1] - M[1])      # M -> A
uB = unit(B[0] - M[0], B[1] - M[1])      # M -> B
assert abs(uA[0] * uB[0] + uA[1] * uB[1]) < 1e-9   # vuông góc tại M
K = 80.0 / 1e5               # px trên mỗi V/m (cùng k cho E1, E2, E)
E1v, E2v = 1.2e5, 9e4
# q1 > 0 tại A: E1 hướng RA XA A (ngược M->A); q2 < 0 tại B: E2 hướng VỀ B (cùng M->B)
d1 = (-uA[0], -uA[1])
d2 = uB
T1 = (M[0] + K * E1v * d1[0], M[1] + K * E1v * d1[1])
T2 = (M[0] + K * E2v * d2[0], M[1] + K * E2v * d2[1])
T = (T1[0] + T2[0] - M[0], T1[1] + T2[1] - M[1])
assert math.dist(T1, A) > math.dist(M, A)          # E1 đi ra xa A
assert math.dist(T2, B) < math.dist(M, B)          # E2 đi về phía B
assert math.dist(T2, M) < math.dist(B, M) - 11     # ngọn E2 chưa chạm quả cầu B
assert abs(math.dist(M, T) - K * 1.5e5) < 1e-6     # |E| = 1,5.10^5 V/m
assert min(T1[1], T[1]) > 30 and T[0] < 420
rq = 12  # bán kính quả cầu: nét đứt dừng ở mép, không xuyên qua dấu +/−
b += line(A[0] + rq, A[1], B[0] - rq, B[1], "currentColor", 1.4, "4 4", 0.6)
b += line(A[0] - rq * uA[0], A[1] - rq * uA[1], *M, "currentColor", 1.4, "4 4", 0.6)
b += line(*M, B[0] - rq * uB[0], B[1] - rq * uB[1], "currentColor", 1.4, "4 4", 0.6)
c1 = (M[0] + 10 * uA[0], M[1] + 10 * uA[1])
c3 = (M[0] + 10 * uB[0], M[1] + 10 * uB[1])
c2 = (c1[0] + 10 * uB[0], c1[1] + 10 * uB[1])
b += f'<polyline fill="none" stroke="currentColor" stroke-width="1.3" points="{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {c3[0]:.1f},{c3[1]:.1f}"/>'
b += line(*T1, *T, BLUE, 1.5, "5 4", 0.8) + line(*T2, *T, RED, 1.5, "5 4", 0.8)
b += arr("f4", "r", *M, *T1, 2.8) + arr("f4", "b", *M, *T2, 2.8) + arr("f4", "g", *M, *T, 2.8)
b += charge(A[0], A[1], 1, 12) + charge(B[0], B[1], -1, 12)
b += f'<circle cx="{M[0]:.1f}" cy="{M[1]:.1f}" r="4" fill="currentColor"/>'
b += text(M[0] - 10, M[1] - 2, "M", "currentColor", 15, "end", "700")
b += text(A[0], A[1] + 32, "A", "currentColor", 15, "middle", "700") + text(B[0], B[1] + 32, "B", "currentColor", 15, "middle", "700")
b += sub("q", "1", A[0], A[1] + 52, RED, 14, "middle", rest=" = +12 nC")
b += sub("q", "2", B[0], B[1] + 52, BLUE, 14, "middle", rest=" = −16 nC")
b += text((A[0] + B[0]) / 2, A[1] + 20, "5 cm", "currentColor", 14, "middle", "400")
mA = ((A[0] + M[0]) / 2, (A[1] + M[1]) / 2)
b += text(mA[0] - 10, mA[1] - 4, "3 cm", "currentColor", 14, "end", "400")
pB = (M[0] + 0.8 * (B[0] - M[0]), M[1] + 0.8 * (B[1] - M[1]))
b += text(pB[0] + 10, pB[1] - 8, "4 cm", "currentColor", 14, "start", "400")
b += sub("E", "1", T1[0], T1[1] - 10, RED, 15, "middle")
mE2 = (M[0] + 0.5 * (T2[0] - M[0]), M[1] + 0.5 * (T2[1] - M[1]))
b += sub("E", "2", mE2[0] - 12, mE2[1] + 22, BLUE, 15, "middle")
b += text(T[0] + 8, T[1] + 6, "E", GRN, 16, "start", "700")
fig4 = wrap("0 18 440 270", "Bài toán mẫu: q1 dương tại A, q2 âm tại B, tam giác AMB vuông tại M; E1 hướng ra xa A, E2 hướng về B, E là đường chéo hình chữ nhật",
            b, "Hình 4. Tam giác AMB vuông tại M nên E₁ ⊥ E₂.<br>E₁ (đỏ) ra xa A vì q₁ &gt; 0.<br>E₂ (xanh) hướng về B vì q₂ &lt; 0.<br>E (lục) là đường chéo hình chữ nhật.")

here = pathlib.Path(__file__).resolve().parent
h = (here / "theory.src.html").read_text(encoding="utf8")
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert h.count(f"<!--FIG{n}-->") == 1, n
    h = h.replace(f"<!--FIG{n}-->", f)
(here / "theory.html").write_text(margin_figs(h), encoding="utf8")
print("ok", len(h))
