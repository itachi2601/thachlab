"""Bài tập mẫu Bài 17 "Khái niệm điện trường" (Vật lí 11) — lesson_id 36. 5 dạng (quét: ket-qua/36.quet-dang.json).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-36.py   (idempotent) → 36.json (review.checked=false cho tới khi kiểm chéo)."""
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "36.json")
TOP_A = "Cường độ điện trường của điện tích điểm"
TOP_B = "Nguyên lí chồng chất điện trường"
GREY = "#94a3b8"
NOTE = "Hình minh hoạ."

# ═════════════ TỰ GIẢI LẠI SỐ LIỆU (độc lập với lời giải) ═════════════
k = 9e9
nC = 1e-9
# D1
_E = 6e-4 / (4 * nC); _F2 = 2 * nC * _E
assert abs(_E - 1.5e5) < 1e-6 and abs(_F2 - 3e-4) < 1e-12 and abs(_F2 / 6e-4 - 0.5) < 1e-12
# D2
_E2 = k * 6 * nC / 0.03 ** 2; _F = 2 * nC * _E2
assert abs(_E2 - 6e4) < 1e-6 and abs(_F - 1.2e-4) < 1e-12
# D3
_EM = k * 8 * nC / (2 * 0.04 ** 2); _EN = k * 8 * nC / (2 * 0.12 ** 2); _rP = math.sqrt(k * 8 * nC / (2 * 900))
assert abs(_EM - 22500) < 1e-6 and abs(_EN - 2500) < 1e-6 and abs(_EM / 9 - _EN) < 1e-6 and abs(_rP - 0.2) < 1e-12
assert abs(0.04 * math.sqrt(_EM / 900) - 0.2) < 1e-12
# D4
_E1 = k * 9 * nC / 0.06 ** 2; _E2m = k * 4 * nC / 0.02 ** 2
assert abs(_E1 - 22500) < 1e-6 and abs(_E2m - 90000) < 1e-6 and abs(_E2m - _E1 - 67500) < 1e-6
_E1i = k * 9 * nC / 0.02 ** 2; _E2i = k * 4 * nC / 0.02 ** 2
assert abs(_E1i + _E2i - 292500) < 1e-6
# D5 (vectơ thật bằng toạ độ: A(-4,0), B(4,0), M(0,3) cm)
import cmath
A_, B_, M_ = (-0.04, 0.0), (0.04, 0.0), (0.0, 0.03)
def Evec(Q, P, M):
    dx, dy = M[0] - P[0], M[1] - P[1]; r = math.hypot(dx, dy)
    return (k * Q * nC / r ** 2 * dx / r, k * Q * nC / r ** 2 * dy / r), r
(e1x, e1y), rMA = Evec(5, A_, M_); (e2x, e2y), rMB = Evec(5, B_, M_)
assert abs(rMA - 0.05) < 1e-12 and abs(math.hypot(e1x, e1y) - 18000) < 1e-6
Ex, Ey = e1x + e2x, e1y + e2y
assert abs(Ex) < 1e-9 and abs(Ey - 21600) < 1e-6          # hướng +y: ra xa AB
cosh = 3 / 5
assert abs(2 * 18000 * cosh - 21600) < 1e-9
_ang = 2 * math.degrees(math.acos(cosh))                  # α giữa hai vectơ
assert 106 < _ang < 107                                     # không vuông: 3-4-5 chỉ vuông ở H
assert abs(math.hypot(rMA, rMB) - 0.0707) < 1e-3 and abs(rMA ** 2 + rMB ** 2 - 0.08 ** 2) > 1e-3
_Fq = 2 * nC * 21600
assert abs(_Fq - 4.32e-5) < 1e-12
(h1x, h2x) = (k * 5 * nC / 0.04 ** 2, -k * 5 * nC / 0.04 ** 2)
assert abs(h1x + h2x) < 1e-9                                # tại H hai vectơ triệt tiêu
# các cách sai phải cho kết quả KHÁC đáp số đúng
assert abs(2 * 18000 - 21600) > 1 and abs(math.hypot(18000, 18000) - 21600) > 1 and abs(2 * 18000 * 0.8 - 21600) > 1
assert abs(k * 5 * nC / 0.03 ** 2 - 18000) > 1 and abs(k * 5 * nC / 0.04 ** 2 - 18000) > 1
assert abs(_EM / 3 - _EN) > 1 and abs(_EM * 3 - _EN) > 1
assert abs(k * 8 * nC / 0.04 ** 2 - _EM) > 1         # quên ε
assert abs(_E2m + _E1 - 67500) > 1                    # cộng số ở D4
assert abs(_E2m - _E1 - 292500) > 1

# ═════════════ TIỆN ÍCH VẼ ═════════════
import re as _re
def rich(s, size=13):
    """`E_M` hoặc `q₁` → chỉ số dưới thật (tspan hạ dòng rồi trả lại)."""
    s = s.replace("₁", "_1").replace("₂", "_2")
    parts = _re.split(r"_([A-Za-z0-9]+)", s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        out += f'<tspan dy="4" font-size="{size - 3}">{parts[i]}</tspan>'
        if parts[i + 1]:
            out += f'<tspan dy="-4">{parts[i + 1]}</tspan>'
        else:
            out += '<tspan dy="-4"></tspan>'
    return out

def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)

def chg(x, y, sign, r=12):
    """Điện tích điểm: vòng tròn + dấu + / −."""
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="currentColor" fill-opacity=".10" stroke="currentColor" stroke-width="2"/>'
            + txt(x, y + 5, "+" if sign > 0 else "−", "currentColor", 16, "middle", "700"))

def pt(x, y, name, dx=8, dy=-8, anchor="start"):
    return dot(x, y, 3.5) + txt(x + dx, y + dy, name, "currentColor", 13, anchor, "700")

def ring(cx, cy, r0, r1, dur, c=GREY, dash="6 4", w=2, clip=""):
    """Mặt sóng điện trường lan từ điện tích: vòng tròn nở ra từ r0 tới r1, chạy MỘT lần khi bấm, KHÔNG có chiều."""
    cp = f' clip-path="url(#{clip})"' if clip else ""
    return (f'<circle cx="{cx}" cy="{cy}" r="{r0}" fill="none" stroke="{c}" stroke-width="{w}" stroke-dasharray="{dash}"{cp}>'
            f'<animate attributeName="r" values="{r0};{r1}" dur="{dur}s" begin="indefinite" fill="freeze"/></circle>')

def slide(dx, dur, inner):
    return (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;{dx} 0" dur="{dur}s" '
            f'begin="indefinite" fill="freeze"/>{inner}</g>')

def compass(cx, cy, hx, hy):
    b = seg(cx - hx, cy, cx + hx, cy, GREY, 1.2, "4 4") + seg(cx, cy - hy, cx, cy + hy, GREY, 1.2, "4 4")
    b += txt(cx, cy - hy - 6, "Bắc", GREY, 12, "middle", "600") + txt(cx, cy + hy + 14, "Nam", GREY, 12, "middle", "600")
    b += txt(cx + hx + 6, cy + 4, "Đông", GREY, 12, "start", "600") + txt(cx - hx - 6, cy + 4, "Tây", GREY, 12, "end", "600")
    return b

# ═════════════ HÌNH CÁC DẠNG ═════════════
# Dạng 1 · điện tích thử q1 (âm) chịu lực hướng bắc; đổi sang q2 (dương) tại đúng M. Vectơ lực dài k·F (k = 1e5 px/N).
def d1(kk):
    M = (210, 128); KF = 1e5
    F1 = 6e-4
    fa, tip = vec_luc("r", M[0], M[1] - 14, 0, -1, F1, KF, 3)
    q1 = chg(M[0], M[1], -1) + fa + txt(M[0] + 10, M[1] - 40, "F₁", RED, 14) + txt(M[0], M[1] + 32, "q₁ = −4 nC", "currentColor", 13, "middle")
    b = compass(M[0], M[1], 170, 100) + dot(M[0], M[1], 2.5)
    b += txt(M[0] - 16, M[1] - 12, "M", "currentColor", 13, "end", "700")
    if kk == 0:
        q2 = chg(M[0] + 140, M[1], +1) + txt(M[0] + 140, M[1] + 32, "q₂ = +2 nC", "currentColor", 13, "middle")
        # q₁ rời M sang trái (mang theo vectơ lực), q₂ từ phải vào đúng M
        b += slide(-120, 3.0, q1) + slide(-140, 3.0, q2)
        b += txt(M[0], 212, "Tại M:  E = ?    F₂ = ?", ORG, 14, "middle")
        return fig("d1-0", "0 0 420 230", "Điện tích thử âm rời điểm M mang theo vectơ lực hướng bắc, điện tích thử dương tiến vào đúng điểm M", b,
                   "Mô phỏng: bỏ q₁ đi, đặt q₂ vào đúng M (chạy 3 s). Lực đã đo trên q₁ vẽ theo thang 1 N ứng với 100 000 px; vẽ ngắn hơn so với thật. " + NOTE)
    b += q1 + txt(M[0], 212, "Tại M:  E = ?", ORG, 14, "middle")
    return fig("d1-2", "0 0 420 230", "Điện tích thử q1 âm tại M chịu lực hướng bắc; cần tìm cường độ điện trường tại M", b,
               "Dữ kiện: q₁ = −4 nC tại M, chịu lực F₁ = 6·10⁻⁴ N hướng bắc (vẽ theo tỉ lệ độ dài lực). " + NOTE)


# Dạng 2 · điện tích điểm Q = −6 nC, M cách 3 cm (1 cm = 40 px). Mặt sóng điện trường nở tới M, không có chiều.
def d2(kk):
    Q = (140, 130); s = 40; r = 3 * s; M = (Q[0] + r, Q[1])
    b = ""
    if kk == 0:
        b += ring(Q[0], Q[1], 10, r, 3.0, GRN)
    b += chg(*Q, -1) + txt(Q[0], Q[1] - 22, "Q = −6 nC", "currentColor", 13, "middle")
    b += pt(M[0], M[1], "M", 8, -8)
    if kk == 2:
        b += dim("", "o", Q[0], 215, M[0], 215, "r = 3 cm", (Q[0] + M[0]) / 2 - 24, 238)
        b += seg(Q[0], 210, Q[0], 220, ORG, 1.5) + seg(M[0], 210, M[0], 220, ORG, 1.5)
    else:
        b += txt(300, 90, "r = QM = 3 cm", ORG, 14)
    b += txt(404, 30, "không khí", GREY, 13, "end", "400")
    if kk == 0:
        return fig("d2-0", "0 0 420 255", "Mặt sóng điện trường lan ra từ điện tích điểm Q tới điểm M cách Q 3 cm", b,
                   "Mô phỏng: điện trường của Q lan ra tới M (vòng nét đứt mở rộng, chạy 3 s). Vòng chỉ cho thấy khoảng cách, chưa cho biết chiều. " + NOTE)
    b += txt(300, 90, "Tại M:  E = ?", ORG, 14) + txt(300, 114, "Đặt q = +2 nC tại M:", "currentColor", 13, "start", "400") + txt(300, 134, "F = ?", RED, 14)
    return fig("d2-2", "0 0 420 255", "Điện tích điểm Q âm trong không khí, điểm M cách Q 3 cm; cần tìm cường độ điện trường tại M và lực lên điện tích thử", b,
               "Dữ kiện: Q = −6 nC, r = QM = 3 cm. " + NOTE)


# Dạng 3 · Q = +8 nC trong dầu ε = 2; M cách 4 cm, N cách 12 cm (1 cm = 10 px).
def d3(kk):
    Q = (140, 130); s = 10; M = (Q[0] + 4 * s, Q[1]); N = (Q[0] + 12 * s, Q[1])
    b = f'<rect x="16" y="8" width="388" height="244" rx="10" fill="none" stroke="{GREY}" stroke-width="1.5" stroke-dasharray="5 4"/>'
    b += txt(396, 30, "dầu, ε = 2", GREY, 13, "end", "600")
    if kk == 0:
        b += ring(Q[0], Q[1], 10, 12 * s, 3.0, GRN)
    b += chg(*Q, +1) + txt(Q[0], Q[1] - 22, "Q = +8 nC", "currentColor", 13, "middle")
    b += pt(M[0], M[1], "M", 0, -10, "middle") + pt(N[0], N[1], "N", 0, -10, "middle")
    if kk == 2:
        b += dim("", "o", Q[0], 178, M[0], 178, "4 cm", (Q[0] + M[0]) / 2 - 14, 198)
        b += dim("", "o", Q[0], 215, N[0], 215, "12 cm", (Q[0] + N[0]) / 2 - 18, 236)
    if kk == 0:
        b += txt(284, 56, "QM = 4 cm", ORG, 14) + txt(284, 78, "QN = 12 cm", ORG, 14) + txt(284, 104, "E_M = ?   E_N = ?", ORG, 14)
        b += txt(284, 128, "P: E_P = 900 V/m", ORG, 14) + txt(284, 150, "QP = ?", ORG, 14)
        return fig("d3-0", "0 0 420 260", "Mặt sóng điện trường lan ra từ điện tích điểm Q trong dầu, đi qua M rồi N", b,
                   "Mô phỏng: điện trường của Q lan ra qua M rồi tới N (chạy 3 s); khoảng cách vẽ đúng tỉ lệ 1 cm : 10 px. " + NOTE)
    b += txt(236, 52, "Cần tìm:  E_M ,  E_N", ORG, 14) + txt(236, 76, "Điểm P: E_P = 900 V/m", "currentColor", 13, "start", "700") + txt(236, 100, "QP = ?", ORG, 14)
    return fig("d3-2", "0 0 420 260", "Điện tích điểm Q trong dầu, hai điểm M và N trên cùng một tia cách Q 4 cm và 12 cm; cần tìm E tại M, N và khoảng cách tới điểm P", b,
               "Dữ kiện: Q = +8 nC, ε = 2 ; QM = 4 cm, QN = 12 cm ; khoảng cách vẽ đúng tỉ lệ 1 cm : 10 px. " + NOTE)


# Dạng 4 · A(+9 nC) – B(−4 nC), AB = 4 cm, M ngoài đoạn AB về phía B cách B 2 cm; I là trung điểm AB (1 cm = 20 px).
def d4(kk):
    cy = 135; s = 20; A = (150, cy); B = (A[0] + 4 * s, cy); M = (B[0] + 2 * s, cy); I = ((A[0] + B[0]) / 2, cy)
    b = ""
    if kk == 0:
        b += ring(A[0], cy, 10, 6 * s, 3.0, RED) + ring(B[0], cy, 10, 2 * s, 3.0 * 2 / 6, BLUE)
    b += seg(A[0] - 120, cy, M[0] + 100, cy, GREY, 1, "3 3")
    b += chg(*A, +1) + txt(A[0], cy - 22, "A: q₁ = +9 nC" if kk == 2 else "A", "currentColor", 13, "middle")
    b += chg(*B, -1) + txt(B[0] + (10 if kk == 2 else 0), cy - (50 if kk == 2 else 22), "B: q₂ = −4 nC" if kk == 2 else "B", "currentColor", 13, "middle")
    b += pt(*M, "M", 8, -10)
    if kk == 2:
        b += pt(I[0], I[1], "I", 0, -10, "middle")
    if kk == 2:
        b += dim("", "o", A[0], cy + 100, B[0], cy + 100, "AB = 4 cm", (A[0] + B[0]) / 2 - 30, cy + 122)
        b += dim("", "g", B[0], cy + 62, M[0], cy + 62, "BM = 2 cm", B[0] + 40 - 30, cy + 84)
    else:
        b += txt(296, 36, "A: q₁ = +9 nC", "currentColor", 13) + txt(296, 58, "B: q₂ = −4 nC", "currentColor", 13)
        b += txt(296, 84, "AB = 4 cm", ORG, 13) + txt(296, 106, "BM = 2 cm", GRN, 13)
    if kk == 0:
        return fig("d4-0", "0 0 420 270", "Điện trường của hai điện tích điểm A và B lan ra cùng tới điểm M ngoài đoạn AB", b,
                   "Mô phỏng: điện trường của A (vòng đỏ) và của B (vòng xanh) cùng lan tới M (chạy 3 s); hai vòng tới M cùng lúc. Vòng không có chiều. Khoảng cách vẽ đúng tỉ lệ 1 cm : 20 px. " + NOTE)
    b += txt(310, 40, "Tại M:  E = ?", ORG, 14) + txt(310, 62, "Tại I:  E = ?", ORG, 14)
    return fig("d4-2", "0 0 420 270", "Hai điện tích điểm A dương và B âm cách nhau 4 cm, điểm M ngoài đoạn AB cách B 2 cm và trung điểm I của AB", b,
               "Dữ kiện: q₁ = +9 nC tại A, q₂ = −4 nC tại B ; AB = 4 cm, BM = 2 cm ; I là trung điểm AB. " + NOTE)


# Dạng 5 · hai quả cầu +5 nC tại A, B (AB = 8 cm); M trên trung trực, MH = 3 cm (1 cm = 22 px).
def d5(kk):
    s = 22; H = (210, 190); A = (H[0] - 4 * s, H[1]); B = (H[0] + 4 * s, H[1]); M = (H[0], H[1] - 3 * s)
    b = seg(H[0], H[1], H[0], 38, GREY, 1.3, "5 4")
    b += seg(A[0], A[1], B[0], B[1], GREY, 1, "3 3")
    if kk == 0:
        rr = 5 * s
        b += f'<defs><clipPath id="d5c"><rect x="0" y="0" width="420" height="{H[1]}"/></clipPath></defs>'
        b += ring(A[0], A[1], 10, rr, 3.0, GRN, clip="d5c") + ring(B[0], B[1], 10, rr, 3.0, GRN, clip="d5c")
    b += chg(*A, +1) + txt(A[0], A[1] + 32, "A: +5 nC", "currentColor", 13, "middle")
    b += chg(*B, +1) + txt(B[0], B[1] + 32, "B: +5 nC", "currentColor", 13, "middle")
    b += pt(*M, "M", 10, 4) + pt(*H, "H", 8, -8)
    b += dim("", "o", A[0], 245, B[0], 245, "AB = 8 cm", H[0] - 32, 266)
    b += arrow("", "g", H[0] - 36, H[1], H[0] - 36, M[1], 1.8) + arrow("", "g", H[0] - 36, M[1], H[0] - 36, H[1], 1.8) + txt(H[0] - 44, (H[1] + M[1]) / 2 + 4, "MH = 3 cm", GRN, 13, "end", "700")
    if kk == 2:
        b += chg(M[0] + 56, M[1] + 0, -1, 9) + txt(M[0] + 74, M[1] + 5, "q = −2 nC (câu b)", "currentColor", 12, "start", "600")
        b += txt(M[0] + 16, M[1] - 24, "E = ?", ORG, 14)
    if kk == 0:
        return fig("d5-0", "0 0 420 275", "Điện trường của hai quả cầu cùng dấu cùng lan tới điểm M trên đường trung trực của AB", b,
                   "Mô phỏng: điện trường của A và của B cùng lan tới M (hai nửa vòng phía trên AB, chạy 3 s); vòng không có chiều. Hình không theo tỉ lệ. " + NOTE)
    return fig("d5-2", "0 0 420 275", "Hai quả cầu cùng dấu tại A và B, điểm M trên đường trung trực của AB cách trung điểm H 3 cm; cần tìm E tại M và lực lên điện tích đặt tại M", b,
               "Dữ kiện: Q = +5 nC tại A và tại B ; AB = 8 cm ; M trên đường trung trực của AB, MH = 3 cm. " + NOTE)


BUILD = [d1, d2, d3, d4, d5]

# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Từ lực đo được trên điện tích thử tìm E, rồi đổi điện tích thử", topic=TOP_A,
      problem_html=r"""<p>Tại điểm M trong một điện trường, đặt điện tích thử $q_1=-4$ nC thì nó chịu lực điện $6\cdot10^{-4}$ N hướng về phía bắc.</p>
<p>a) Tính độ lớn và nêu hướng của cường độ điện trường tại M.</p>
<p>b) Bỏ $q_1$ đi, đặt đúng vào M điện tích thử $q_2=+2$ nC. Tính lực điện lên $q_2$ và nêu hướng.</p>"""),
 dict(label="Dạng 2 · Dễ · Điện trường của một điện tích điểm: độ lớn, chiều theo dấu Q, lực lên điện tích thử", topic=TOP_A,
      problem_html=r"""<p>Một điện tích điểm $Q=-6$ nC đặt cố định trong không khí. Điểm M cách Q một đoạn 3 cm.</p>
<p>a) Tính cường độ điện trường tại M và nêu hướng.</p>
<p>b) Đặt tại M một điện tích thử $q=+2$ nC. Tính lực điện lên $q$ và nêu hướng.</p>"""),
 dict(label="Dạng 3 · Trung bình · Điện trường trong điện môi: đổi đơn vị, tỉ lệ theo khoảng cách", topic=TOP_A,
      problem_html=r"""<p>Một điện tích điểm $Q=+8$ nC đặt cố định trong dầu có hằng số điện môi $\varepsilon=2$. Điểm M cách Q 4 cm, điểm N nằm trên tia QM và cách Q 12 cm.</p>
<p>a) Tính cường độ điện trường tại M.</p>
<p>b) Tính cường độ điện trường tại N.</p>
<p>c) Điểm P nằm trên tia QM có cường độ điện trường $900$ V/m. Tính khoảng cách từ P đến Q.</p>"""),
 dict(label="Dạng 4 · Trung bình · Chồng chất điện trường của hai điện tích: hai vectơ cùng phương", topic=TOP_B,
      problem_html=r"""<p>Trong không khí, đặt $q_1=+9$ nC tại A và $q_2=-4$ nC tại B, với $AB=4$ cm.</p>
<p>a) Điểm M nằm trên đường thẳng AB, ngoài đoạn AB, về phía B và cách B 2 cm. Tính cường độ điện trường tổng hợp tại M và nêu hướng.</p>
<p>b) Tính cường độ điện trường tổng hợp tại trung điểm I của AB.</p>"""),
 dict(label="Dạng 5 · Khó · Hai điện tích bằng nhau, điểm trên trung trực: tìm góc, tổng hợp, tính lực", topic=TOP_B,
      problem_html=r"""<p>Trong không khí, hai quả cầu nhỏ cùng tích điện $Q=+5$ nC được giữ cố định tại A và B, $AB=8$ cm. Điểm M nằm trên đường trung trực của AB, cách trung điểm H của AB một đoạn 3 cm (A, B, H, M cùng nằm trong một mặt phẳng).</p>
<p>a) Tính cường độ điện trường tổng hợp tại M và nêu hướng.</p>
<p>b) Đặt tại M một quả cầu nhỏ tích điện $q=-2$ nC. Tính lực điện lên quả cầu này và nêu hướng.</p>
<p>c) Nếu quả cầu $q$ nằm đúng ở H thì lực điện tổng hợp lên nó bằng bao nhiêu?</p>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (⚠ chỉ nêu điều kiện; cột 3 không ghi kết luận/hướng/phép tính) ═════════════
ANALYSIS = [
 [(r'"điện tích thử $q_1=-4$ nC"', r"$q_1=-4$ nC (điện tích âm)", r"Đổi nC sang C ; dấu của $q$ liên quan thế nào tới chiều lực ?"),
  (r'"chịu lực điện $6\cdot10^{-4}$ N hướng về phía bắc"', r"$F_1=6\cdot10^{-4}$ N ; hướng bắc", r"Định nghĩa cường độ điện trường qua lực lên điện tích thử"),
  (r'"Tính độ lớn và nêu hướng của cường độ điện trường tại M"', r"Cần: $E$ (độ lớn), hướng của $\vec E$", r"Liên hệ giữa $E$, $F$, $q$ ; quan hệ chiều của $\vec F$ và $\vec E$ theo dấu $q$"),
  (r'"Bỏ $q_1$ đi, đặt đúng vào M điện tích thử $q_2=+2$ nC"', r"$q_2=+2$ nC (điện tích dương), vẫn là điểm M", r"⚠ Điện trường tại M do đâu mà có, và điện tích thử cần thoả điều kiện gì ?"),
  (r'"Tính lực điện lên $q_2$ và nêu hướng"', r"Cần: $F_2$ (độ lớn), hướng", r"Lực điện lên điện tích đặt trong điện trường ; chiều lực theo dấu $q_2$")],
 [(r'"điện tích điểm $Q=-6$ nC … trong không khí"', r"$Q=-6$ nC (âm) ; $\varepsilon\approx1$", r"Điểm đặt, phương, chiều, độ lớn của $\vec E$ do điện tích điểm gây ra ; chiều phụ thuộc dấu của $Q$"),
  (r'"Điểm M cách Q một đoạn 3 cm"', r"$r=3$ cm", r"⚠ $r$ là khoảng cách từ điện tích nguồn tới điểm xét, tính bằng m"),
  (r'"Tính cường độ điện trường tại M và nêu hướng"', r"Cần: $E_M$, hướng của $\vec E_M$", r"Công thức độ lớn $E$ của điện tích điểm ; quy ước chiều theo dấu $Q$"),
  (r'"Đặt tại M một điện tích thử $q=+2$ nC"', r"$q=+2$ nC (điện tích dương)", r"Lực điện lên điện tích đặt tại điểm đã biết $\vec E$"),
  (r'"Tính lực điện lên $q$ và nêu hướng"', r"Cần: $F$, hướng của $\vec F$", r"Liên hệ $F$ với $E$ và $|q|$ ; chiều lực theo dấu $q$")],
 [(r'"$Q=+8$ nC … trong dầu có hằng số điện môi $\varepsilon=2$"', r"$Q=+8$ nC ; $\varepsilon=2$", r"⚠ Môi trường không phải chân không : hằng số điện môi có mặt trong công thức $E$ của điện tích điểm"),
  (r'"Điểm M cách Q 4 cm"', r"$r_M=4$ cm", r"Đổi cm sang m trước khi thế vào công thức"),
  (r'"điểm N nằm trên tia QM và cách Q 12 cm"', r"$r_N=12$ cm", r"$E$ tại N so với $E$ tại M thế nào, khi cùng nguồn và cùng môi trường ?"),
  (r'"Tính cường độ điện trường tại M" ; "tại N"', r"Cần: $E_M$, $E_N$", r"Công thức độ lớn $E$ ; cách $E$ phụ thuộc khoảng cách $r$"),
  (r'"Điểm P … có cường độ điện trường $900$ V/m"', r"$E_P=900$ V/m", r"Từ $E$ cho trước suy ra khoảng cách : cùng nguồn, cùng môi trường như M"),
  (r'"Tính khoảng cách từ P đến Q"', r"Cần: $r_P$", r"Cách $E$ phụ thuộc $r$, dùng ngược chiều từ $E$ ra $r$")],
 [(r'"$q_1=+9$ nC tại A và $q_2=-4$ nC tại B, với $AB=4$ cm"', r"$q_1=+9$ nC ; $q_2=-4$ nC ; $AB=4$ cm", r"⚠ Mỗi điện tích gây ra một vectơ $\vec E$ riêng ; chiều của từng vectơ theo dấu điện tích gây ra nó"),
  (r'"M … ngoài đoạn AB, về phía B và cách B 2 cm"', r"$BM=2$ cm ; M nằm trên đường thẳng AB", r"Khoảng cách từ M tới mỗi điện tích tính từ đúng điện tích đó, không lấy chung một giá trị"),
  (r'"cường độ điện trường tổng hợp tại M và nêu hướng"', r"Cần: $E_M$, hướng", r"Nguyên lí chồng chất điện trường"),
  (r'"trung điểm I của AB"', r"$AI=IB=2$ cm", r"Khoảng cách từ I tới mỗi điện tích"),
  (r'"cường độ điện trường tổng hợp tại trung điểm I"', r"Cần: $E_I$", r"Nguyên lí chồng chất điện trường")],
 [(r'"hai quả cầu nhỏ cùng tích điện $Q=+5$ nC … tại A và B"', r"$Q=+5$ nC mỗi quả ; hai quả cầu coi là điện tích điểm", r"⚠ Điện tích điểm đứng yên trong không khí ; mỗi quả cầu gây ra một vectơ $\vec E$ riêng tại M"),
  (r'"$AB=8$ cm"', r"$AB=8$ cm", r"Khoảng cách giữa hai quả cầu khác khoảng cách từ mỗi quả cầu tới M"),
  (r'"M nằm trên đường trung trực của AB, cách trung điểm H … 3 cm"', r"$MH=3$ cm ; $MH\perp AB$ tại H", r"Tính chất đường trung trực"),
  (r'"cường độ điện trường tổng hợp tại M và nêu hướng"', r"Cần: $E_M$, hướng", r"Nguyên lí chồng chất ; cộng hai vectơ hợp góc bất kì"),
  (r'"quả cầu nhỏ tích điện $q=-2$ nC … lực điện"', r"$q=-2$ nC (âm) ; cần: $F$, hướng", r"Lực điện lên điện tích trong điện trường tổng hợp ; chiều lực theo dấu $q$"),
  (r'"nếu quả cầu $q$ nằm đúng ở H"', r"H là trung điểm AB", r"Điện trường tổng hợp tại H")],
]

# ═════════════ LỜI GIẢI ═════════════
R1 = [r"<strong>Khái niệm:</strong> cường độ điện trường $\vec E$ đặc trưng cho điện trường về tác dụng lực tại một điểm.",
      r"<strong>Định nghĩa:</strong> $\vec E=\dfrac{\vec F}{q}$ ; độ lớn $E=\dfrac{F}{|q|}$ ; $F=|q|E$.",
      r"$q\gt0$ : $\vec F$ cùng chiều $\vec E$ ; $q\lt0$ : $\vec F$ ngược chiều $\vec E$.",
      r"⚠ <strong>Điều kiện:</strong> $\vec E$ tại M do nguồn quyết định, không đổi khi thay điện tích thử ; đổi nC sang C trước khi thế."]
R2 = [r"<strong>Khái niệm:</strong> điện tích điểm $Q$ gây ra điện trường quanh nó ; $\vec E$ tại một điểm có phương là đường nối điểm đó với $Q$.",
      r"<strong>Công thức:</strong> $E=k\dfrac{|Q|}{\varepsilon r^2}$ với $k=9\cdot10^{9}\ \text{N·m}^2/\text{C}^2$ ; $F=|q|E$.",
      r"<strong>Chiều:</strong> $Q\gt0$ hướng ra xa $Q$ ; $Q\lt0$ hướng về phía $Q$ ; điện tích thử dương chịu lực cùng chiều $\vec E$.",
      r"⚠ <strong>Điều kiện:</strong> $r$ tính bằng m ; thế $|Q|$ vào công thức, dấu của $Q$ chỉ dùng để chọn chiều."]
R3 = [r"<strong>Công thức:</strong> $E=k\dfrac{|Q|}{\varepsilon r^2}$ ; cùng $Q$ và cùng môi trường thì $E$ tỉ lệ $\dfrac{1}{r^2}$.",
      r"<strong>Mẹo:</strong> $r$ gấp $n$ lần thì $E$ giảm $n^2$ lần.",
      r"⚠ <strong>Điều kiện:</strong> $\varepsilon$ nằm ở mẫu số ; đổi cm sang m trước khi thế ; khi so sánh hai điểm phải cùng $Q$ và cùng $\varepsilon$."]
R4 = [r"<strong>Nguyên lí chồng chất:</strong> $\vec E=\vec E_1+\vec E_2$ (cộng vectơ).",
      r"<strong>Mỗi điện tích:</strong> $E_i=k\dfrac{|q_i|}{r_i^2}$ ; $q_i\gt0$ hướng ra xa, $q_i\lt0$ hướng về phía điện tích.",
      r"<strong>Hai vectơ cùng phương:</strong> cùng chiều thì $E=E_1+E_2$ ; ngược chiều thì $E=|E_1-E_2|$.",
      r"⚠ <strong>Điều kiện:</strong> $r_i$ là khoảng cách từ <em>chính điện tích đó</em> tới điểm xét ; phải xét chiều từng vectơ trước khi cộng."]
R5 = [r"<strong>Nguyên lí chồng chất:</strong> $\vec E=\vec E_1+\vec E_2$ ; $E_i=k\dfrac{|Q_i|}{r_i^2}$.",
      r"<strong>Hai vectơ bằng nhau, hợp góc $\alpha$:</strong> $E=2E_1\cos\dfrac{\alpha}{2}$.",
      r"<strong>Lực điện:</strong> $F=|q|E$ ; $q\lt0$ thì $\vec F$ ngược chiều $\vec E$.",
      r"⚠ <strong>Điều kiện:</strong> $r_i$ là khoảng cách từ quả cầu tới M, không phải $MH$ hay $AB$ ; chỉ khi biết góc giữa hai vectơ mới cộng được, bộ ba cạnh 3–4–5 không tự cho góc vuông ở M."]

def _split(R):
    out = []
    for it in R:
        parts = it.split(" ; ")
        out.append(parts[0]); out += parts[1:]
    return out
R1, R2, R3, R4, R5 = map(_split, (R1, R2, R3, R4, R5))
ANALYSIS = [[(c, d_, k_.replace(" ; ", "<br>")) for c, d_, k_ in blk] for blk in ANALYSIS]

SOLS = [
 sol(R1, [
  ("Độ lớn của E tại M",
   [P(r"Đổi $|q_1|=4\ \text{nC}=4\cdot10^{-9}\ \text{C}$ rồi dùng định nghĩa:"), M(r"E=\dfrac{F_1}{|q_1|}"), M(r"E=\dfrac{6\cdot10^{-4}}{4\cdot10^{-9}}"),
    A(r"E=1{,}5\cdot10^{5}\ \text{V/m}")]),
  ("Hướng của E tại M",
   [P(r"$q_1\lt0$ nên $\vec F_1$ ngược chiều $\vec E$."), P(r"$\vec F_1$ hướng bắc, vậy:"), A(r"T:$\vec E$ tại M hướng về phía <strong>nam</strong>.")]),
  ("Lực điện lên q₂",
   [P(r"$\vec E$ tại M không đổi khi đổi điện tích thử. Đổi $q_2=2\cdot10^{-9}\ \text{C}$:"), M(r"F_2=|q_2|\,E"), M(r"F_2=2\cdot10^{-9}\cdot1{,}5\cdot10^{5}"),
    A(r"F_2=3\cdot10^{-4}\ \text{N}")]),
  ("Hướng của lực lên q₂",
   [P(r"$q_2\gt0$ nên $\vec F_2$ cùng chiều $\vec E$."), A(r"T:$\vec F_2$ hướng về phía <strong>nam</strong>.")]),
  ("Kiểm tra",
   [P(r"$|q_2|=\dfrac12|q_1|$ nên $F_2=\dfrac12F_1$ ✓."), P(r"Đơn vị $\text{N/C}=\text{V/m}$ ✓."),
    P(r"Hai điện tích trái dấu đặt cùng chỗ chịu lực ngược chiều nhau ✓ ($\vec F_1$ bắc, $\vec F_2$ nam).")])],
  [r"a) $E=1{,}5\cdot10^{5}$ V/m, hướng nam", r"b) $F_2=3\cdot10^{-4}$ N, hướng nam"],
  r"Nhận dạng: đề cho <strong>lực đo được trên một điện tích thử</strong> rồi hỏi $E$ hoặc lực khi đổi điện tích thử → $E=\dfrac{F}{|q|}$, chiều theo dấu $q$, $\vec E$ giữ nguyên."),

 sol(R2, [
  ("Độ lớn của E tại M",
   [P(r"Đổi $r=3\ \text{cm}=0{,}03\ \text{m}$ ; $|Q|=6\cdot10^{-9}\ \text{C}$ ; không khí $\varepsilon\approx1$."), M(r"E=k\dfrac{|Q|}{\varepsilon r^2}"),
    M(r"E=9\cdot10^{9}\cdot\dfrac{6\cdot10^{-9}}{1\cdot0{,}03^2}"), A(r"E=6\cdot10^{4}\ \text{V/m}")]),
  ("Hướng của E tại M",
   [P(r"$Q\lt0$ nên $\vec E$ nằm trên đường nối M với Q và hướng về phía $Q$."), A(r"T:$\vec E_M$ hướng <strong>từ M về Q</strong>.")]),
  ("Lực điện lên điện tích thử",
   [P(r"Đổi $q=2\cdot10^{-9}\ \text{C}$ ; dùng $E$ vừa tính:"), M(r"F=|q|\,E"), M(r"F=2\cdot10^{-9}\cdot6\cdot10^{4}"), A(r"F=1{,}2\cdot10^{-4}\ \text{N}")]),
  ("Hướng của lực",
   [P(r"$q\gt0$ nên $\vec F$ cùng chiều $\vec E$."), A(r"T:$\vec F$ hướng <strong>về phía Q</strong> (hai điện tích trái dấu hút nhau).")]),
  ("Kiểm tra",
   [P(r"Kiểm bằng định luật Culông : $F=k\dfrac{|Q||q|}{r^2}=9\cdot10^{9}\cdot\dfrac{6\cdot10^{-9}\cdot2\cdot10^{-9}}{0{,}03^2}=1{,}2\cdot10^{-4}\ \text{N}$ ✓."),
    P(r"Nếu thế $r=3$ (cm) vào công thức sẽ ra $E$ sai $10^{4}$ lần : luôn đổi sang m.")])],
  [r"a) $E=6\cdot10^{4}$ V/m, hướng từ M về Q", r"b) $F=1{,}2\cdot10^{-4}$ N, hướng về phía Q"],
  r"Nhận dạng: đề cho <strong>điện tích điểm Q và khoảng cách r</strong> → $E=k\dfrac{|Q|}{\varepsilon r^2}$ ; chiều theo dấu $Q$ (dương ra, âm vào)."),

 sol(R3, [
  ("Cường độ điện trường tại M",
   [P(r"Đổi $r_M=4\ \text{cm}=0{,}04\ \text{m}$ ; $|Q|=8\cdot10^{-9}\ \text{C}$ ; $\varepsilon=2$."), M(r"E_M=k\dfrac{|Q|}{\varepsilon r_M^2}"),
    M(r"E_M=9\cdot10^{9}\cdot\dfrac{8\cdot10^{-9}}{2\cdot0{,}04^2}"), A(r"E_M=2{,}25\cdot10^{4}\ \text{V/m}")]),
  ("Cường độ điện trường tại N",
   [P(r"Cùng $Q$, cùng môi trường ; $r_N=12\ \text{cm}=3r_M$ nên $E$ giảm $3^2$ lần:"), M(r"\dfrac{E_N}{E_M}=\left(\dfrac{r_M}{r_N}\right)^2=\dfrac{1}{9}"),
    M(r"E_N=\dfrac{2{,}25\cdot10^{4}}{9}"), A(r"E_N=2{,}5\cdot10^{3}\ \text{V/m}")]),
  ("Khoảng cách từ P đến Q",
   [P(r"Cùng $Q$, cùng môi trường ; so sánh P với M :"), M(r"\dfrac{E_M}{E_P}=\left(\dfrac{r_P}{r_M}\right)^2"),
    M(r"\dfrac{r_P}{r_M}=\sqrt{\dfrac{2{,}25\cdot10^{4}}{900}}=5"), M(r"r_P=5\cdot4\ \text{cm}"), A(r"r_P=20\ \text{cm}=0{,}20\ \text{m}")]),
  ("Kiểm tra",
   [P(r"Tính trực tiếp : $E_N=9\cdot10^{9}\cdot\dfrac{8\cdot10^{-9}}{2\cdot0{,}12^2}=2{,}5\cdot10^{3}\ \text{V/m}$ ✓."),
    P(r"Từ $E_P$ : $r_P=\sqrt{\dfrac{k|Q|}{\varepsilon E_P}}=\sqrt{\dfrac{72}{2\cdot900}}=0{,}20\ \text{m}$ ✓."),
    P(r"$E_P\lt E_N$ nên P phải xa Q hơn N ($20\ \text{cm}\gt12\ \text{cm}$) ✓.")])],
  [r"a) $E_M=2{,}25\cdot10^{4}$ V/m", r"b) $E_N=2{,}5\cdot10^{3}$ V/m", r"c) $r_P=20$ cm"],
  r"Nhận dạng: đề <strong>so sánh E ở hai khoảng cách</strong> hoặc cho $E$ rồi hỏi $r$ → dùng tỉ lệ $E\sim\dfrac{1}{r^2}$ cùng nguồn, cùng môi trường."),

 sol(R4, [
  ("Điện trường do q₁ tại M",
   [P(r"M cách A : $AM=AB+BM=6\ \text{cm}=0{,}06\ \text{m}$."), M(r"E_1=k\dfrac{|q_1|}{AM^2}=9\cdot10^{9}\cdot\dfrac{9\cdot10^{-9}}{0{,}06^2}"),
    A(r"E_1=2{,}25\cdot10^{4}\ \text{V/m}")]),
  ("Điện trường do q₂ tại M",
   [P(r"M cách B : $BM=2\ \text{cm}=0{,}02\ \text{m}$."), M(r"E_2=k\dfrac{|q_2|}{BM^2}=9\cdot10^{9}\cdot\dfrac{4\cdot10^{-9}}{0{,}02^2}"),
    A(r"E_2=9\cdot10^{4}\ \text{V/m}")]),
  ("Chiều hai vectơ tại M",
   [P(r"$q_1\gt0$ : $\vec E_1$ hướng ra xa A, tức hướng từ A về phía M."), P(r"$q_2\lt0$ : $\vec E_2$ hướng về B, tức hướng từ M về phía A."),
    A(r"T:Hai vectơ nằm trên đường thẳng AB và <strong>ngược chiều</strong> nhau.")]),
  ("Tổng hợp tại M",
   [P(r"Ngược chiều nên lấy hiệu hai độ lớn, chiều theo vectơ lớn hơn ($\vec E_2$):"), M(r"E_M=E_2-E_1=9\cdot10^{4}-2{,}25\cdot10^{4}"),
    A(r"E_M=6{,}75\cdot10^{4}\ \text{V/m}"), A(r"T:Hướng <strong>từ M về B</strong>.")]),
  ("Tổng hợp tại trung điểm I",
   [P(r"$AI=IB=0{,}02\ \text{m}$ :"), M(r"E_1=9\cdot10^{9}\cdot\dfrac{9\cdot10^{-9}}{0{,}02^2}=2{,}025\cdot10^{5}\ \text{V/m}"),
    M(r"E_2=9\cdot10^{9}\cdot\dfrac{4\cdot10^{-9}}{0{,}02^2}=9\cdot10^{4}\ \text{V/m}"),
    P(r"I nằm giữa hai điện tích trái dấu : $\vec E_1$ (ra xa A) và $\vec E_2$ (về B) cùng hướng từ A sang B, nên cộng độ lớn:"),
    M(r"E_I=E_1+E_2"), A(r"E_I=2{,}925\cdot10^{5}\ \text{V/m}")]),
  ("Kiểm tra",
   [P(r"Ở M (ngoài đoạn) hai vectơ ngược chiều, $E_M$ nhỏ hơn $E_2$ ✓ ; ở I (giữa) cùng chiều, $E_I$ lớn hơn từng thành phần ✓."),
    P(r"Cộng số có dấu $E_1+(-E_2)$ mà không vẽ hình dễ đảo kết quả giữa hai trường hợp này.")])],
  [r"a) $E_M=6{,}75\cdot10^{4}$ V/m, hướng từ M về B", r"b) $E_I=2{,}925\cdot10^{5}$ V/m, hướng từ A sang B"],
  r"Nhận dạng: đề cho <strong>hai điện tích và một điểm trên đường nối</strong> → tính từng $E_i$, vẽ chiều, rồi cộng (cùng chiều) hay trừ (ngược chiều)."),

 sol(R5, [
  ("Khoảng cách từ M đến mỗi quả cầu",
   [P(r"Tam giác MHA vuông tại H, $AH=\dfrac{AB}{2}=4\ \text{cm}$, $MH=3\ \text{cm}$ :"), M(r"MA=\sqrt{AH^2+MH^2}=\sqrt{4^2+3^2}"),
    A(r"MA=MB=5\ \text{cm}=0{,}05\ \text{m}")]),
  ("Điện trường do mỗi quả cầu tại M",
   [P(r"Hai quả cầu cùng $Q$, cùng khoảng cách tới M nên $E_1=E_2$ :"), M(r"E_1=k\dfrac{Q}{MA^2}=9\cdot10^{9}\cdot\dfrac{5\cdot10^{-9}}{0{,}05^2}"),
    A(r"E_1=E_2=1{,}8\cdot10^{4}\ \text{V/m}")]),
  ("Góc giữa hai vectơ",
   [P(r"$\vec E_1$ hướng ra xa A, $\vec E_2$ hướng ra xa B. Đường phân giác của góc giữa chúng là đường trung trực HM."),
    P(r"Nửa góc $\dfrac{\alpha}{2}$ bằng góc $\widehat{AMH}$ (đối đỉnh), cạnh kề là $MH$ :"), M(r"\cos\dfrac{\alpha}{2}=\dfrac{MH}{MA}=\dfrac{3}{5}"),
    M(r"\dfrac{\alpha}{2}=\arccos0{,}6\approx53{,}13^\circ"), A(r"\alpha\approx106{,}3^\circ")]),
  ("Điện trường tổng hợp tại M",
   [P(r"Hai vectơ bằng nhau, hợp góc $\alpha$ :"), M(r"E=2E_1\cos\dfrac{\alpha}{2}"), M(r"E=2\cdot1{,}8\cdot10^{4}\cdot\cos53{,}13^\circ=2\cdot1{,}8\cdot10^{4}\cdot0{,}6"),
    A(r"E=2{,}16\cdot10^{4}\ \text{V/m}"), A(r"T:$\vec E$ nằm trên đường trung trực, hướng <strong>từ H ra M</strong> (ra xa AB).")]),
  ("Lực điện lên quả cầu q tại M",
   [P(r"Đổi $|q|=2\cdot10^{-9}\ \text{C}$ :"), M(r"F=|q|\,E=2\cdot10^{-9}\cdot2{,}16\cdot10^{4}"), A(r"F=4{,}32\cdot10^{-5}\ \text{N}"),
    P(r"$q\lt0$ nên $\vec F$ ngược chiều $\vec E$ :"), A(r"T:$\vec F$ hướng <strong>từ M về H</strong>.")]),
  ("Lực điện khi quả cầu ở H",
   [P(r"H cách A và B cùng $4\ \text{cm}$ nên hai vectơ bằng nhau về độ lớn ; H nằm giữa hai điện tích dương nên hai vectơ ngược chiều."),
    M(r"\vec E_H=\vec E_1+\vec E_2=\vec 0"), A(r"F_H=0")]),
  ("Kiểm tra",
   [P(r"Kiểm bằng toạ độ : A$(-4;0)$, B$(4;0)$, M$(0;3)$ cm ; hai thành phần ngang của $\vec E_1,\vec E_2$ triệt tiêu, còn lại thành phần dọc $2\cdot1{,}8\cdot10^{4}\cdot0{,}6$ ✓."),
    P(r"Nếu coi $\vec E_1\perp\vec E_2$ sẽ ra $E=\sqrt{2}E_1\approx2{,}55\cdot10^{4}$ V/m — sai, vì góc vuông của bộ 3–4–5 nằm ở H, không ở M.")])],
  [r"a) $E=2{,}16\cdot10^{4}$ V/m, hướng từ H ra M (ra xa AB)", r"b) $F=4{,}32\cdot10^{-5}$ N, hướng từ M về H", r"c) $F_H=0$"],
  r"Nhận dạng: đề cho <strong>hai điện tích bằng nhau và điểm trên đường trung trực</strong> → tự tìm góc từ hình học, $E=2E_1\cos\dfrac{\alpha}{2}$, rồi $F=|q|E$."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>lực đo được trên điện tích thử</b> rồi <b>đổi điện tích thử</b> → <b>E = F/|q|</b>, chiều theo dấu q, E giữ nguyên.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Độ lớn của E tại M", r"Cường độ điện trường tại M bằng bao nhiêu (theo đơn vị $10^{5}\ \text{V/m}$)?", 1.5, "×10⁵ V/m", 0.02,
       loi=r"Quên đổi nC sang C nên $E$ sai $10^{9}$ lần, hoặc nhân $F$ với $|q|$ thay vì chia."),
  buoc("Hướng của E tại M", r"Hướng của $\vec E$ tại M so với hướng của $\vec F_1$ là gì?",
       loi=r"Lấy $\vec E$ cùng hướng với lực, quên rằng $q_1$ âm.",
       lua_chon=[(r"Ngược hướng $\vec F_1$ (hướng nam), vì $q_1\lt0$", True),
                 (r"Cùng hướng $\vec F_1$ (hướng bắc)", r"Chỉ đúng với điện tích thử dương ; $q_1$ âm nên lực ngược chiều $\vec E$."),
                 (r"Vuông góc với $\vec F_1$", r"Từ $\vec F=q\vec E$, lực luôn cùng phương với $\vec E$.")],
       ke=[(r"Xét dấu của $q_1$ để biết $\vec E$ cùng hay ngược chiều $\vec F_1$", True),
           (r"Lấy $\vec E$ cùng chiều $\vec F_1$ vì lực và cường độ điện trường luôn cùng hướng", r"Chỉ đúng khi điện tích thử dương."),
           (r"Coi $\vec E$ vuông góc $\vec F_1$ vì là hai đại lượng khác nhau", r"$\vec F=q\vec E$ nên hai vectơ luôn cùng phương.")]),
  buoc("Lực điện lên q₂", r"Lực điện lên $q_2$ bằng bao nhiêu (theo đơn vị $10^{-4}\ \text{N}$)?", 3, "×10⁻⁴ N", 0.05,
       loi=r"Cho rằng $E$ đổi theo điện tích thử, hoặc lấy luôn lực mới bằng lực cũ.",
       ke=[(r"Giữ nguyên $E$ tại M, tính $F_2=|q_2|E$", True),
           (r"Lấy $F_2=F_1$ vì cùng điểm M", r"Cùng điểm thì $E$ bằng nhau, còn lực tỉ lệ với $|q|$ mà $|q_2|$ khác $|q_1|$."),
           (r"Tính lại $E$ bằng $F/|q_2|$ rồi mới tìm lực", r"Chưa biết $F_2$ nên không tính được ; $E$ tại M do nguồn quyết định, không đổi.")]),
  buoc("Hướng của lực lên q₂", r"Lực điện lên $q_2$ hướng thế nào so với $\vec E$ tại M?",
       loi=r"Lấy hướng lực lên $q_2$ trùng hướng $\vec F_1$ vì cùng một điểm.",
       lua_chon=[(r"Cùng hướng $\vec E$ (hướng nam), vì $q_2\gt0$", True),
                 (r"Cùng hướng $\vec F_1$ (hướng bắc)", r"$\vec F_1$ tác dụng lên điện tích âm ; điện tích dương chịu lực ngược chiều với nó."),
                 (r"Ngược hướng $\vec E$", r"Chỉ điện tích âm chịu lực ngược chiều $\vec E$.")],
       ke=[(r"Xét dấu $q_2$ để so chiều $\vec F_2$ với $\vec E$", True),
           (r"Lấy $\vec F_2$ cùng chiều $\vec F_1$ vì cùng điểm M", r"Lực phụ thuộc dấu điện tích thử, không chỉ vào điểm đặt."),
           (r"Không cần xét, vì độ lớn đã đủ", r"Đề hỏi cả hướng.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>điện tích điểm Q và khoảng cách r</b> → <b>E = k|Q|/(εr²)</b>, chiều ra (Q dương) hoặc vào (Q âm).",
  cap_do=1, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Độ lớn của E tại M", r"Cường độ điện trường tại M bằng bao nhiêu (theo đơn vị $10^{4}\ \text{V/m}$)?", 6, "×10⁴ V/m", 0.1,
       loi=r"Thế $r=3$ (cm) thay vì $0{,}03$ m, hoặc thế $Q$ âm vào công thức rồi ra $E$ âm."),
  buoc("Hướng của E tại M", r"$\vec E$ tại M hướng thế nào?",
       loi=r"Vẽ $\vec E$ hướng ra xa $Q$ vì quên rằng $Q$ âm.",
       lua_chon=[(r"Hướng về phía Q, vì $Q\lt0$", True),
                 (r"Hướng ra xa Q", r"Chỉ đúng với điện tích nguồn dương."),
                 (r"Vuông góc với đường nối M và Q", r"$\vec E$ của điện tích điểm nằm trên đường nối điểm đó với $Q$.")],
       ke=[(r"Xét dấu của $Q$ : âm thì hướng vào, dương thì hướng ra", True),
           (r"Lấy dấu của $Q$ đưa vào công thức để $E$ mang dấu", r"Công thức cho độ lớn ; dấu của $Q$ chỉ dùng để chọn chiều."),
           (r"Cho $\vec E$ luôn hướng ra xa điện tích nguồn", r"Chỉ đúng với $Q$ dương.")]),
  buoc("Lực điện lên điện tích thử", r"Lực điện lên $q$ bằng bao nhiêu (theo đơn vị $10^{-4}\ \text{N}$)?", 1.2, "×10⁻⁴ N", 0.02,
       loi=r"Thế điện tích nguồn $Q$ thay cho $q$ khi nhân với $E$, hoặc chia thay vì nhân.",
       ke=[(r"Dùng $E$ vừa tính : $F=|q|E$", True),
           (r"Lấy $F=\dfrac{E}{|q|}$", r"Đó là $E=\dfrac{F}{|q|}$ lật ngược ; lực bằng $|q|E$."),
           (r"Lấy $F=|Q|\,E$", r"$Q$ đã nằm trong $E$ rồi ; lực lên $q$ phải nhân với chính điện tích $q$.")]),
  buoc("Hướng của lực", r"Lực điện lên $q$ hướng thế nào?",
       loi=r"Cho lực hướng ra xa $Q$, quên rằng $\vec E$ ở đây hướng vào.",
       lua_chon=[(r"Về phía Q, cùng chiều $\vec E$ vì $q\gt0$", True),
                 (r"Ra xa Q", r"$q\gt0$ chịu lực cùng chiều $\vec E$, mà $\vec E$ hướng vào Q nên lực cũng hướng vào."),
                 (r"Không có lực vì M chưa có điện tích thử", r"Điện trường có ở M dù chưa đặt gì ; đặt $q$ vào là có lực.")],
       ke=[(r"Lấy chiều của $\vec E$ vừa tìm rồi xét dấu $q$", True),
           (r"Lấy chiều ra xa $Q$ cho mọi trường hợp", r"Chiều lực phụ thuộc dấu của cả $Q$ và $q$."),
           (r"Bỏ qua chiều vì độ lớn là đủ", r"Đề hỏi cả hướng.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>so sánh E ở hai khoảng cách</b> hoặc <b>cho E, hỏi r</b> → nghĩ tới <b>E tỉ lệ 1/r²</b> cùng nguồn, cùng môi trường.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Cường độ điện trường tại M", r"Cường độ điện trường tại M bằng bao nhiêu (theo đơn vị $10^{4}\ \text{V/m}$)?", 2.25, "×10⁴ V/m", 0.03,
       loi=r"Quên chia cho $\varepsilon$, thế $r$ theo cm, hoặc quên bình phương $r$."),
  buoc("Cường độ điện trường tại N", r"Cường độ điện trường tại N bằng bao nhiêu (theo đơn vị $10^{3}\ \text{V/m}$)?", 2.5, "×10³ V/m", 0.05,
       loi=r"Áp dụng sai quy luật phụ thuộc của $E$ theo $r$.",
       ke=[(r"$r$ gấp 3 lần nên $E$ giảm $3^2$ lần", True),
           (r"$r$ gấp 3 lần nên $E$ giảm 3 lần", r"$E$ tỉ lệ $\dfrac{1}{r^2}$ chứ không phải $\dfrac{1}{r}$."),
           (r"N ở xa hơn nên nhân $E_M$ với 3", r"Xa điện tích hơn thì điện trường yếu đi, không mạnh lên.")]),
  buoc("Khoảng cách từ P đến Q", r"Khoảng cách từ P đến Q bằng bao nhiêu (theo đơn vị cm)?", 20, "cm", 0.5,
       loi=r"Suy tỉ số $r$ từ tỉ số $E$ sai cách.",
       ke=[(r"Lập $\dfrac{E_M}{E_P}=\left(\dfrac{r_P}{r_M}\right)^2$ rồi lấy căn", True),
           (r"Lập $\dfrac{E_M}{E_P}=\dfrac{r_P}{r_M}$ (tỉ số thẳng)", r"$E$ tỉ lệ nghịch với bình phương $r$, nên tỉ số $E$ bằng bình phương tỉ số $r$."),
           (r"Lập $\dfrac{r_P}{r_M}=\left(\dfrac{E_P}{E_M}\right)^2$ (đảo tỉ số)", r"$E_P$ nhỏ hơn $E_M$ nên P phải xa Q hơn M ; cách này cho P gần hơn.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>hai điện tích và điểm trên đường nối chúng</b> → tính từng <b>E</b>, xét <b>chiều</b>, rồi cộng hoặc trừ.",
  cap_do=2, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Điện trường do q₁ tại M", r"Điện trường do $q_1$ gây ra tại M bằng bao nhiêu (theo đơn vị $10^{4}\ \text{V/m}$)?", 2.25, "×10⁴ V/m", 0.03,
       loi=r"Lấy $r=AB=4$ cm thay vì khoảng cách từ A tới M."),
  buoc("Điện trường do q₂ tại M", r"Điện trường do $q_2$ gây ra tại M bằng bao nhiêu (theo đơn vị $10^{4}\ \text{V/m}$)?", 9, "×10⁴ V/m", 0.1,
       loi=r"Dùng nhầm $r=AM$ cho cả hai điện tích.",
       ke=[(r"Tính riêng với khoảng cách từ B tới M", True),
           (r"Dùng luôn khoảng cách từ A tới M cho cả hai", r"Mỗi điện tích có khoảng cách riêng tới M ; $q_2$ ở B nên dùng $BM$."),
           (r"Cộng $q_1$ và $q_2$ rồi tính một lần", r"Điện trường tổng không bằng điện trường của tổng điện tích ; phải tính riêng từng vectơ.")]),
  buoc("Chiều hai vectơ tại M", r"Hai vectơ $\vec E_1$ và $\vec E_2$ tại M có chiều thế nào với nhau?",
       loi=r"Suy chiều chỉ từ dấu hai điện tích, bỏ qua vị trí của M.",
       lua_chon=[(r"Ngược chiều nhau", True),
                 (r"Cùng chiều, vì hai điện tích trái dấu", r"Hai điện tích trái dấu chỉ cho hai vectơ cùng chiều khi điểm xét nằm giữa chúng ; M nằm ngoài đoạn AB."),
                 (r"Vuông góc với nhau", r"M nằm trên đường thẳng AB nên cả hai vectơ đều nằm trên đường thẳng ấy.")],
       ke=[(r"Vẽ chiều từng vectơ theo dấu điện tích gây ra nó", True),
           (r"Cộng ngay hai độ lớn", r"Chỉ cộng độ lớn khi hai vectơ cùng chiều ; chưa xét chiều thì chưa biết."),
           (r"Lấy chiều theo dấu của điện tích lớn hơn", r"Mỗi vectơ có chiều theo dấu điện tích gây ra nó.")]),
  buoc("Tổng hợp tại M", r"Cường độ điện trường tổng hợp tại M bằng bao nhiêu (theo đơn vị $10^{4}\ \text{V/m}$)?", 6.75, "×10⁴ V/m", 0.08,
       loi=r"Cộng hai độ lớn bất kể chiều, hoặc lấy hiệu rồi nêu sai hướng.",
       ke=[(r"Hai vectơ ngược chiều : lấy hiệu độ lớn, chiều theo vectơ lớn hơn", True),
           (r"Cộng hai độ lớn", r"Chỉ cộng khi cùng chiều."),
           (r"Lấy $\sqrt{E_1^2+E_2^2}$", r"Công thức này chỉ dùng khi hai vectơ vuông góc.")]),
  buoc("Tổng hợp tại trung điểm I", r"Cường độ điện trường tổng hợp tại I bằng bao nhiêu (theo đơn vị $10^{5}\ \text{V/m}$)?", 2.925, "×10⁵ V/m", 0.03,
       loi=r"Dùng lại cách tổng hợp ở câu a mà không xét lại chiều ở I.",
       ke=[(r"Tính lại $E_1$, $E_2$ với khoảng cách mới, xét chiều rồi cộng", True),
           (r"Dùng lại kết quả ở M vì cùng nằm trên AB", r"$E$ phụ thuộc khoảng cách tới từng điện tích nên mỗi điểm một giá trị."),
           (r"Lấy hiệu hai độ lớn như ở M", r"I nằm giữa hai điện tích trái dấu nên hai vectơ cùng chiều, không ngược chiều.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>hai điện tích bằng nhau</b>, điểm trên <b>đường trung trực</b> → tìm <b>góc</b>, <b>E = 2E₁cos(α/2)</b>, rồi <b>F = |q|E</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Khoảng cách từ M đến mỗi quả cầu", r"Khoảng cách MA bằng bao nhiêu (theo đơn vị cm)?", 5, "cm", 0.05,
       loi=r"Lấy $r=MH$ hoặc $r=AH$, tức khoảng cách tới điểm sai."),
  buoc("Điện trường do mỗi quả cầu tại M", r"Điện trường do một quả cầu gây ra tại M bằng bao nhiêu (theo đơn vị $10^{4}\ \text{V/m}$)?", 1.8, "×10⁴ V/m", 0.02,
       loi=r"Thế khoảng cách tới H hoặc độ dài AB thay vì khoảng cách từ quả cầu tới M.",
       ke=[(r"Thế khoảng cách từ quả cầu tới M vừa tìm vào $E=k\dfrac{|Q|}{r^2}$", True),
           (r"Thế $r=MH$ vì M gần H nhất", r"$r$ là khoảng cách từ điện tích nguồn tới điểm xét, tức từ quả cầu tới M."),
           (r"Thế $r=AB$", r"$AB$ là khoảng cách giữa hai quả cầu, không phải khoảng cách từ quả cầu tới M.")]),
  buoc("Góc giữa hai vectơ", r"Góc $\alpha$ giữa $\vec E_1$ và $\vec E_2$ bằng bao nhiêu độ?", 106.3, "độ", 0.3,
       loi=r"Coi $\alpha=90^\circ$ vì thấy bộ ba cạnh quen thuộc, hoặc lấy $\alpha$ bằng nửa góc cần tìm.",
       ke=[(r"Vẽ hai vectơ ; nửa góc giữa chúng là $\widehat{AMH}$ trong tam giác vuông MHA", True),
           (r"Coi $\alpha=90^\circ$ vì bộ ba cạnh quen thuộc", r"Góc vuông của bộ ba cạnh nằm ở H trong tam giác MHA ; góc AMB không vuông."),
           (r"Lấy $\alpha$ bằng góc $\widehat{AMH}$", r"Đường trung trực chia đôi góc giữa hai vectơ, nên $\alpha$ gấp đôi $\widehat{AMH}$.")]),
  buoc("Điện trường tổng hợp tại M", r"Cường độ điện trường tổng hợp tại M bằng bao nhiêu (theo đơn vị $10^{4}\ \text{V/m}$)?", 2.16, "×10⁴ V/m", 0.03,
       loi=r"Cộng thẳng hai độ lớn, hoặc dùng $\sqrt{E_1^2+E_2^2}$ như khi hai vectơ vuông góc.",
       ke=[(r"Hai vectơ bằng nhau : $E=2E_1\cos\dfrac{\alpha}{2}$", True),
           (r"Hai vectơ bằng nhau : $E=2E_1\cos\alpha$", r"Dùng nguyên góc $\alpha$ thay cho nửa góc ; với $\alpha\gt90^\circ$ còn cho $E$ âm."),
           (r"Hai vectơ bằng nhau : $E=2E_1\sin\dfrac{\alpha}{2}$", r"Nhầm $\cos$ với $\sin$ : nửa góc kề với phân giác nên dùng $\cos$.")]),
  buoc("Lực điện lên quả cầu q tại M", r"Lực điện lên quả cầu $q$ bằng bao nhiêu (theo đơn vị $10^{-5}\ \text{N}$)?", 4.32, "×10⁻⁵ N", 0.05,
       loi=r"Dùng điện trường của một quả cầu thay vì điện trường tổng hợp, hoặc cho lực cùng chiều $\vec E$.",
       ke=[(r"Dùng $E$ tổng hợp : $F=|q|E$, chiều ngược $\vec E$ vì $q\lt0$", True),
           (r"Dùng $F=k\dfrac{|Q||q|}{MH^2}$ với một quả cầu", r"Hai quả cầu cùng tác dụng lực và khoảng cách tới M là $MA$, không phải $MH$."),
           (r"Dùng $F=|q|E$ nhưng lấy cùng chiều $\vec E$", r"$q$ âm chịu lực ngược chiều $\vec E$.")]),
  buoc("Lực điện khi quả cầu ở H", r"Lực điện tổng hợp lên quả cầu $q$ khi nó ở đúng H là gì?",
       loi=r"Cho rằng H gần cả hai quả cầu nên lực lớn nhất, quên xét chiều hai vectơ.",
       lua_chon=[(r"Bằng 0, vì hai vectơ triệt tiêu", True),
                 (r"Lớn nhất, vì H gần cả hai quả cầu", r"Gần hơn thì từng vectơ lớn hơn, nhưng hai vectơ ngược chiều và bằng nhau nên triệt tiêu."),
                 (r"Bằng $2|q|E_1$, vì hai vectơ cộng lại", r"Tại H hai vectơ ngược chiều (H nằm giữa hai điện tích cùng dấu) nên không cộng.")],
       ke=[(r"Xét độ lớn và chiều của hai vectơ tại H", True),
           (r"Dùng lại góc $\alpha$ ở M", r"Vị trí H khác M nên góc giữa hai vectơ khác."),
           (r"Dùng lại kết quả của M vì cùng trên trung trực", r"$E$ phụ thuộc vị trí điểm xét ; mỗi điểm một giá trị.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ GHI FILE ═════════════
write(J, 36, "Bài 17. Khái niệm điện trường", DANG, BUILD, ANALYSIS, SOLS, None)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code) — đã tự giải lại bằng Python 10/10/2026"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
