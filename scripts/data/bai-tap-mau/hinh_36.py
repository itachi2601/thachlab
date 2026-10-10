"""Hình cho bài tập mẫu Bài 17 "Khái niệm điện trường" (Vật lí 11), lesson_id 36.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Quy tắc: KHÔNG vẽ vectơ E (đáp án hoặc bước đáp án) ở bất kỳ hình nào. Vectơ duy nhất trong bài là lực F của Dạng 1 (dữ kiện của đề),
vẽ bằng vec_luc: độ dài = k·F, đầu V 30°. Dạng 2–6 mô phỏng bằng các vòng nét đứt mở rộng từ điện tích ("điện trường lan ra"),
không có chiều nên không lộ chiều E; bán kính vòng cuối khớp khoảng cách thật đến điểm xét trong hình."""
import math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from svg_lib import vec_luc, chevron

GREY = "#94a3b8"
COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN}
MINUS = "−"


def an(attr, vals, dur, nd=1):
    return (f'<animate attributeName="{attr}" values="{";".join(f"{v:.{nd}f}" for v in vals)}" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')


def vec_anim(c, tails, tips, step, w=3.0):
    """Vectơ lực chạy theo các mẫu (đuôi, ngọn) cách đều `step` giây: đường thẳng + đầu V 30° (path trượt theo)."""
    col = COL[c]
    ww = min(w, 2.8)
    n = len(tips)
    dur = step * (n - 1)
    lens = [math.hypot(t[0] - s[0], t[1] - s[1]) for s, t in zip(tails, tips)]
    L = max(5, min(3.4 * ww + 2, 0.6 * min(lens)))
    ds = [re.search(r'd="([^"]+)"', chevron(t[0], t[1], t[0] - s[0], t[1] - s[1], col, ww, L)).group(1) for s, t in zip(tails, tips)]
    line = (f'<line x1="{tails[0][0]:.1f}" y1="{tails[0][1]:.1f}" x2="{tips[0][0]:.1f}" y2="{tips[0][1]:.1f}" '
            f'stroke="{col}" stroke-width="{ww}">' + an("x2", [t[0] for t in tips], dur) + an("y2", [t[1] for t in tips], dur) + "</line>")
    path = (f'<path d="{ds[0]}" fill="none" stroke="{col}" stroke-width="{ww}" stroke-linejoin="miter" stroke-miterlimit="10" '
            f'stroke-linecap="butt"><animate attributeName="d" values="{";".join(ds)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/></path>')
    return line + path


def ramp(x, y, F, k, n=14, hold=6):
    """Ngọn vectơ (hướng sang phải) tăng từ 15 % tới đủ k·F, rồi giữ."""
    full = k * F
    tips = [(x + full * (0.15 + 0.85 * i / (n - 1)), y) for i in range(n)]
    tips += [tips[-1]] * hold
    assert abs(tips[-1][0] - x - full) < 0.05
    return tips


def ts(x, y, base, sb, tail="", c="currentColor", size=13, anchor="start", weight="700"):
    """Nhãn có chỉ số dưới: base_sb tail."""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{base}<tspan dy="4" font-size="{size - 3}">{sb}</tspan><tspan dy="-4">{tail}</tspan></text>')


def chg(x, y, sg, r=12):
    """Điện tích: vòng tròn + dấu. sg = "+", "-" hoặc "?" (chưa biết dấu, ghi chữ Q)."""
    c = RED if sg == "+" else BLUE if sg == "-" else GREY
    t = "+" if sg == "+" else MINUS if sg == "-" else "Q"
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="{c}" stroke-width="2.4"/>'
            + text(round(x, 1), round(y + (6 if sg != "?" else 5), 1), t, c, 18 if sg != "?" else 14, "middle", "700"))


def pdot(x, y, name, dy=24):
    return dot(x, y, 4.5, "currentColor") + lbl(x, y + dy, name, "currentColor", 13, "middle", "700")


def ring(cx, cy, R, Rmax, dur=3.2, n=16, r0=14):
    """Vòng nét đứt mở rộng từ r0 tới R với CÙNG tốc độ cho mọi vòng trong hình (vòng lớn nhất xong lúc `dur`), rồi dừng."""
    assert R > r0 and Rmax >= R
    v = (Rmax - r0) / dur
    vals = [min(R, r0 + v * dur * j / n) for j in range(n + 1)]
    assert abs(vals[-1] - R) < 0.05 or R < Rmax
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r0}" fill="none" stroke="{GREY}" stroke-width="1.6" stroke-dasharray="5 4">'
            + an("r", vals, dur) + "</circle>")


# ───────────── Dạng 1: q = +4,0 nC tại M chịu F = 6,0·10⁻⁵ N sang phải ─────────────
def d1(kk):
    M = (90, 90); k = 1.6; F = 60.0       # F tính bằng µN: 60 µN = 6,0·10⁻⁵ N
    t0 = (M[0] + 12, M[1])
    b = chg(*M, "+") + lbl(M[0], M[1] - 28, "q = +4,0 nC", RED, 13, "middle", "700") + lbl(M[0], M[1] + 36, "M", "currentColor", 13, "middle", "700")
    b += lbl(120, 66, "F = 6,0·10⁻⁵ N", ORG, 13, "start", "700") + lbl(262, 94, "E tại M = ?", "currentColor", 14, "start", "700")
    if kk == 0:
        tips = ramp(t0[0], t0[1], F, k)
        b += vec_anim("o", [t0] * len(tips), tips, 0.2)
        return fig("d1-0", "0 0 420 140", "Điện tích thử dương q đặt tại điểm M chịu một lực điện hướng sang phải", b,
                   "Mô phỏng: lực điện lên q tăng dần từ 15 % lên đủ giá trị của đề (khoảng 4 s), vẽ theo tỉ lệ 1 µN ứng với 1,6 px. Chưa vẽ vectơ cường độ điện trường.")
    s, _ = vec_luc("o", t0[0], t0[1], 1, 0, F, k)
    return fig("d1-2", "0 0 420 140", "Điện tích thử dương q tại điểm M chịu lực điện F hướng sang phải; cường độ điện trường tại M chưa biết", b + s,
               "Dữ kiện: lực điện lên q vẽ theo tỉ lệ 1 µN ứng với 1,6 px. Chưa vẽ vectơ cường độ điện trường.")


# ───────────── Dạng 2: Q = −5,0 nC, M cách Q 10 cm ─────────────
def d2(kk):
    Q = (60, 90); s = 12.0; r = 10.0
    M = (Q[0] + s * r, Q[1])
    b = seg(Q[0], Q[1], M[0], M[1], GREY, 1.2, "4 4", .8)
    if kk == 0:
        b += ring(Q[0], Q[1], s * r, s * r)
    b += chg(*Q, "-") + lbl(Q[0], Q[1] - 26, "Q", BLUE, 14, "middle", "700") + pdot(M[0], M[1], "M")
    b += dim("", "o", Q[0], 142, M[0], 142, "", 0, 0) + lbl((Q[0] + M[0]) / 2, 134, "r = 10 cm", ORG, 13, "middle", "700")
    b += lbl(232, 62, "Q = −5,0 nC", BLUE, 13, "start", "700") + lbl(232, 86, "Không khí", "currentColor", 13, "start", "600") + lbl(232, 110, "E tại M = ?", "currentColor", 14, "start", "700")
    if kk == 0:
        return fig("d2-0", "0 0 420 160", "Điện tích âm Q và điểm M cách Q mười xăng-ti-mét; các vòng nét đứt mở rộng từ Q tới M", b,
                   "Mô phỏng: điện trường “lan” ra từ Q, vòng nét đứt mở rộng tới điểm M (khoảng 3 s), vẽ theo tỉ lệ 1 cm ứng với 12 px. Vòng chỉ minh hoạ sự lan toả, không cho biết chiều hay độ lớn của E.")
    return fig("d2-2", "0 0 420 160", "Điện tích âm Q trong không khí và điểm M cách Q mười xăng-ti-mét", b,
               "Dữ kiện: vẽ theo tỉ lệ 1 cm ứng với 12 px. Chưa vẽ vectơ cường độ điện trường.")


# ───────────── Dạng 3: điện tích Q, A cách 15 cm có E = 1,6·10⁴ V/m; B cách 25 cm ─────────────
def d3(kk):
    Q = (50, 90); s = 10.0
    A = (Q[0] + 15 * s, Q[1]); B = (Q[0] + 25 * s, Q[1])
    b = seg(Q[0], Q[1], B[0] + 30, B[1], GREY, 1.2, "4 4", .8)
    if kk == 0:
        b += ring(Q[0], Q[1], 15 * s, 25 * s) + ring(Q[0], Q[1], 25 * s, 25 * s)
    b += chg(*Q, "?") + pdot(*A, "A", 22) + pdot(*B, "B", 22)
    b += ts(A[0], 60, "E", "A", " = 1,6·10⁴ V/m", ORG, 13, "middle") + ts(B[0] + 4, 82, "E", "B", " = ?", "currentColor", 13, "middle")
    b += dim("", "b", Q[0], 142, A[0], 142, "", 0, 0) + lbl((Q[0] + A[0]) / 2, 134, "15 cm", BLUE, 13, "middle", "700")
    b += dim("", "b", Q[0], 168, B[0], 168, "", 0, 0) + lbl((Q[0] + B[0]) / 2, 160, "25 cm", BLUE, 13, "middle", "700")
    if kk == 0:
        return fig("d3-0", "0 0 420 184", "Điện tích Q và hai điểm A, B nằm trên một đường thẳng qua Q, cách Q lần lượt mười lăm và hai mươi lăm xăng-ti-mét; các vòng nét đứt mở rộng từ Q", b,
                   "Mô phỏng: điện trường “lan” ra từ Q, hai vòng nét đứt mở rộng tới A rồi tới B (khoảng 3 s), vẽ theo tỉ lệ 1 cm ứng với 10 px. Vòng chỉ minh hoạ sự lan toả, không cho biết độ lớn của E.")
    return fig("d3-2", "0 0 420 184", "Điện tích Q và hai điểm A, B nằm trên một đường thẳng qua Q, cách Q lần lượt mười lăm và hai mươi lăm xăng-ti-mét", b,
               "Dữ kiện: vẽ theo tỉ lệ 1 cm ứng với 10 px. Dấu của Q chưa biết nên ghi chữ Q.")


# ───────────── Dạng 4: q1 = +8,0 nC tại A, q2 = −2,0 nC tại B, AB = 20 cm; M trung điểm; N cách B 10 cm ngoài AB ─────────────
def d4(kk):
    y = 90; s = 10.0
    A = (60, y); B = (60 + 20 * s, y); M = (60 + 10 * s, y); N = (B[0] + 10 * s, y)
    b = seg(20, y, 405, y, GREY, 1.2, "4 4", .8)
    if kk == 0:
        Rm = 30 * s
        b += ring(A[0], y, 10 * s, Rm) + ring(A[0], y, 30 * s, Rm) + ring(B[0], y, 10 * s, Rm)
    b += chg(*A, "+") + chg(*B, "-") + pdot(*M, "M", 22) + pdot(*N, "N", 22)
    b += ts(A[0], 56, "q", "1", " = +8,0 nC", RED, 13, "middle") + ts(B[0], 56, "q", "2", " = −2,0 nC", BLUE, 13, "middle")
    b += lbl(A[0], 124, "A", "currentColor", 13, "middle", "700") + lbl(B[0], 124, "B", "currentColor", 13, "middle", "700")
    b += dim("", "o", A[0], 160, B[0], 160, "", 0, 0) + lbl((A[0] + B[0]) / 2, 152, "AB = 20 cm", ORG, 13, "middle", "700")
    b += dim("", "o", B[0], 160, N[0], 160, "", 0, 0) + lbl((B[0] + N[0]) / 2, 152, "BN = 10 cm", ORG, 13, "middle", "700")
    if kk == 0:
        return fig("d4-0", "0 0 420 176", "Hai điện tích trái dấu tại A và B, điểm M ở giữa AB và điểm N ngoài đoạn AB về phía B; các vòng nét đứt mở rộng từ hai điện tích", b,
                   "Mô phỏng: điện trường “lan” ra từ cả hai điện tích, các vòng nét đứt mở rộng cùng tốc độ tới M và N (khoảng 3 s), vẽ theo tỉ lệ 1 cm ứng với 10 px. Vòng chỉ minh hoạ sự lan toả, không cho biết chiều hay độ lớn của E.")
    return fig("d4-2", "0 0 420 176", "Hai điện tích trái dấu tại A và B cách nhau hai mươi xăng-ti-mét, điểm M là trung điểm AB, điểm N nằm ngoài đoạn AB cách B mười xăng-ti-mét", b,
               "Dữ kiện: vẽ theo tỉ lệ 1 cm ứng với 10 px. Chưa vẽ vectơ cường độ điện trường nào.")


# ───────────── Dạng 5: q1 = +2,0 nC tại A, q2 = −4,8 nC tại B; C cách A 5,0 cm, cách B 12 cm (hình KHÔNG theo tỉ lệ) ─────────────
def d5(kk):
    A = (60, 66); C = (150, 150); B = (340, 112)
    rA = math.hypot(A[0] - C[0], A[1] - C[1]); rB = math.hypot(B[0] - C[0], B[1] - C[1])
    b = seg(A[0], A[1], C[0], C[1], "currentColor", 1.6, "", .8) + seg(C[0], C[1], B[0], B[1], "currentColor", 1.6, "", .8) + seg(A[0], A[1], B[0], B[1], GREY, 1.2, "4 4", .8)
    if kk == 0:
        Rm = max(rA, rB)
        b += ring(A[0], A[1], rA, Rm) + ring(B[0], B[1], rB, Rm)
    b += chg(*A, "+") + chg(*B, "-") + pdot(*C, "C", 22)
    b += ts(A[0] + 14, 34, "q", "1", " = +2,0 nC", RED, 13, "middle") + ts(B[0], 86, "q", "2", " = −4,8 nC", BLUE, 13, "middle")
    b += lbl(A[0] - 18, A[1] + 5, "A", "currentColor", 13, "end", "700") + lbl(B[0] + 18, B[1] + 5, "B", "currentColor", 13, "start", "700")
    b += lbl(94, 104, "5,0 cm", ORG, 13, "end", "700") + lbl(252, 160, "12 cm", ORG, 13, "middle", "700") + lbl(200, 78, "13 cm", ORG, 13, "middle", "700")
    if kk == 0:
        return fig("d5-0", "0 0 420 184", "Hai điện tích trái dấu tại A và B và điểm C; các vòng nét đứt mở rộng từ A và từ B tới C", b,
                   "Mô phỏng: điện trường “lan” ra từ A và B, hai vòng nét đứt mở rộng cùng tốc độ tới C (khoảng 3 s). Hình không vẽ theo tỉ lệ; độ dài các cạnh ghi trên hình. Vòng chỉ minh hoạ sự lan toả, không cho biết chiều hay độ lớn của E.")
    return fig("d5-2", "0 0 420 184", "Hai điện tích trái dấu tại A và B, điểm C cách A năm xăng-ti-mét và cách B mười hai xăng-ti-mét, AB bằng mười ba xăng-ti-mét", b,
               "Dữ kiện: hình không vẽ theo tỉ lệ; độ dài các cạnh ghi trên hình. Chưa vẽ vectơ cường độ điện trường nào.")


# ───────────── Dạng 6: q1 = +9,0 nC tại A, q2 = −4,0 nC tại B, AB = 10 cm; tìm M có E = 0 ─────────────
def d6(kk):
    y = 80; s = 6.0
    A = (180, y); B = (180 + 10 * s, y)
    b = seg(20, y, 400, y, GREY, 1.2, "4 4", .8)
    if kk == 0:
        b += ring(A[0], y, 18 * s, 18 * s) + ring(B[0], y, 18 * s, 18 * s)
    b += chg(*A, "+") + chg(*B, "-")
    b += ts(A[0] - 8, 44, "q", "1", " = +9,0 nC", RED, 13, "end") + ts(B[0] + 8, 44, "q", "2", " = −4,0 nC", BLUE, 13, "start")
    b += lbl(A[0], 112, "A", "currentColor", 13, "middle", "700") + lbl(B[0], 112, "B", "currentColor", 13, "middle", "700")
    b += dim("", "o", A[0], 142, B[0], 142, "", 0, 0) + lbl((A[0] + B[0]) / 2, 134, "AB = 10 cm", ORG, 13, "middle", "700")
    if kk == 0:
        return fig("d6-0", "0 0 420 160", "Hai điện tích trái dấu tại A và B cách nhau mười xăng-ti-mét trên một đường thẳng; các vòng nét đứt mở rộng từ hai điện tích", b,
                   "Mô phỏng: điện trường “lan” ra từ cả hai điện tích, hai vòng nét đứt mở rộng cùng tốc độ (khoảng 3 s), vẽ theo tỉ lệ 1 cm ứng với 6 px. Vòng chỉ minh hoạ sự lan toả, không đánh dấu điểm nào.")
    return fig("d6-2", "0 0 420 160", "Hai điện tích trái dấu tại A và B cách nhau mười xăng-ti-mét trên một đường thẳng", b,
               "Dữ kiện: vẽ theo tỉ lệ 1 cm ứng với 6 px. Điểm M cần tìm chưa được đánh dấu.")


BUILD = [d1, d2, d3, d4, d5, d6]
