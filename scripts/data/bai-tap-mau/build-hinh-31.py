"""Bài 31 (Bài 12. Giao thoa sóng, Vật lí 11): 5 dạng bài tập mẫu + tự luận, mỗi dạng có mô phỏng dưới đề,
bảng phân tích, lời giải ngắt bước và buoc[] tự giải từng bước.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-31.py  → ghi scripts/data/bai-tap-mau/31.json
Quy ước (đúng lý thuyết bài): A, B cùng pha; d₁ = MA, d₂ = MB; cực đại d₂−d₁ = kλ; cực tiểu d₂−d₁ = (k+½)λ;
đếm trên AB không lấy hai đầu; khe Young i = λD/a, vân sáng x = k·i, vân tối x = (k+½)·i."""
import json, math, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "31.json")
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
SZ = 12


def anim(attr, vals, kts, dur):
    """<animate> có keyTimes: giữ nguyên giá trị đến lúc bắt đầu rồi chuyển. begin=indefinite, chạy một lần khi bấm."""
    v = ";".join(f"{x:.2f}" if isinstance(x, float) else str(x) for x in vals)
    k = ";".join(f"{t:.4f}" for t in kts)
    return f'<animate attributeName="{attr}" values="{v}" keyTimes="{k}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'


def appear(t0, t1, dur, lo=0.28):
    """Phần tử vẽ sẵn mờ (lo) — khi giảm chuyển động vẫn thấy — rồi sáng lên trong [t0, t1] (giây)."""
    t0 = min(t0, dur - 0.1); t1 = min(max(t1, t0 + 0.05), dur)
    return anim("opacity", [lo, lo, 1, 1], [0, t0 / dur, t1 / dur, 1], dur)


def rect(x, y, w, h, c, op=1, extra="", inner=""):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{c}" opacity="{op}"{extra}>{inner}</rect>'


def circ(x, y, r, c, op=1, inner="", stroke=True):
    s = ' stroke="currentColor" stroke-width="1.2"' if stroke else ""
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" opacity="{op}"{s}>{inner}</circle>'


def tri_pos(d1, d2, ab):
    """Toạ độ (x dọc AB tính từ A, y vuông góc AB) của M cách A d1, cách B d2 (cm)."""
    x = (d1 * d1 - d2 * d2 + ab * ab) / (2 * ab)
    return x, math.sqrt(d1 * d1 - x * x)


# ───────────── Dạng 1: M, N cực đại hay cực tiểu (f=25 Hz, v=50 cm/s, AB=20) ─────────────
def d1(k):
    p = f"d1{k}"; AB = 20.0; lam = 2.0
    M = tri_pos(16, 21, AB); N = tri_pos(18, 24, AB)
    if k == 0:
        s = 9.0; A = (50, 196); B = (A[0] + s * AB, 196)
        Mp = (A[0] + s * M[0], A[1] - s * M[1]); Np = (A[0] + s * N[0], A[1] - s * N[1])
        v, f = 50.0, 25.0; T = 1 / f; tend = 30.6 / v   # ảnh chụp khung cuối: bán kính sóng lớn nhất ≈ 30 cm
        slow = 5; dur = tend * slow
        b = defs(p) + f'<defs><clipPath id="{p}c"><rect x="16" y="14" width="260" height="{A[1] - 14}"/></clipPath></defs><g clip-path="url(#{p}c)">'
        for src, col in ((A, RED), (B, BLUE)):
            j = 0
            while j * T < tend:
                te = j * T; rend = v * (tend - te) * s
                kts = [0, te / tend, 1]
                b += (f'<circle cx="{src[0]}" cy="{src[1]}" r="0" fill="none" stroke="{col}" stroke-width="1.3" opacity=".55">'
                      f'{anim("r", [0.0, 0.0, rend], kts, dur)}</circle>')
                j += 1
        b += "</g>"
        b += seg(A[0], A[1], B[0], B[1], "currentColor", 1.4, "5 4", .7)
        b += circ(*A, 5, "currentColor") + circ(*B, 5, "currentColor")
        b += circ(*Mp, 5, ORG) + circ(*Np, 5, GRN)
        b += lbl(A[0], A[1] + 20, "A", "currentColor", 13, "middle", "700") + lbl(B[0], B[1] + 20, "B", "currentColor", 13, "middle", "700")
        b += lbl(Mp[0] + 9, Mp[1] + 4, "M", ORG, 13, "start", "700") + lbl(Np[0] - 9, Np[1] + 4, "N", GRN, 13, "end", "700")
        b += dim(p, "b", A[0], A[1] + 32, B[0], B[1] + 32, "AB = 20 cm", (A[0] + B[0]) / 2 - 36, A[1] + 50)
        b += lbl(286, 44, "A, B cùng pha", "currentColor", 13, "start", "700") + lbl(286, 68, "f = 25 Hz", RED, 13, "start", "700") + lbl(286, 92, "v = 50 cm/s", BLUE, 13, "start", "700")
        b += lbl(286, 132, "M, N là cực đại", ORG, 13, "start", "700") + lbl(286, 150, "hay cực tiểu?", ORG, 13, "start", "700")
        return fig("d1-0", "0 0 420 250", "Hai nguồn A và B cùng pha phát sóng tròn trên mặt nước, hai điểm M và N nằm phía trên đoạn AB", b,
                   "Mô phỏng: sóng tròn lan ra từ hai nguồn (chạy chậm 5 lần), ảnh dừng lại là mặt nước lúc sóng đã lan xa. Chỉ vẽ nửa mặt nước phía trên AB.")
    s = 5.5; b = defs(p)
    for ox, P_, d1_, d2_, nm, col in ((30, M, 16, 21, "M", ORG), (250, N, 18, 24, "N", GRN)):
        A = (ox, 160); B = (ox + s * AB, 160); Pp = (ox + s * P_[0], 160 - s * P_[1])
        b += seg(*A, *B, "currentColor", 2) + seg(*A, *Pp, RED, 2.2) + seg(*B, *Pp, BLUE, 2.2)
        b += circ(*A, 4, "currentColor") + circ(*B, 4, "currentColor") + circ(*Pp, 5, col)
        b += lbl(A[0], A[1] + 18, "A", "currentColor", 13, "middle", "700") + lbl(B[0], B[1] + 18, "B", "currentColor", 13, "middle", "700")
        b += lbl(Pp[0] + 9, Pp[1] - 4, nm, col, 13, "start", "700")
        b += lbl((A[0] + Pp[0]) / 2 - 5, (A[1] + Pp[1]) / 2 + 4, f"{d1_} cm", RED, SZ, "end", "700")
        b += lbl((B[0] + Pp[0]) / 2 + 9, (B[1] + Pp[1]) / 2 + 4, f"{d2_} cm", BLUE, SZ, "start", "700")
        b += lbl((A[0] + B[0]) / 2, A[1] + 38, "AB = 20 cm", "currentColor", SZ, "middle", "400")
    b += lbl(30, 22, "d₂ − d₁ = ?  rồi chia cho λ", "currentColor", 13, "start", "700")
    return fig("d1-2", "0 0 420 200", "Hai tam giác MAB và NAB với khoảng cách từ M và N tới hai nguồn", b,
               "Dữ kiện: đỏ là d₁ = khoảng cách tới A, xanh là d₂ = khoảng cách tới B. " + NOTE)


# ───────────── Dạng 2: đếm cực đại, cực tiểu trên AB (AB=12 cm, f=20 Hz, v=40 cm/s) ─────────────
def d2(k):
    p = f"d2{k}"
    if k == 0:
        lam = 72.0; AB = 3.25 * lam; A = (93, 100); B = (A[0] + AB, 100); c = (A[0] + B[0]) / 2
        dur = 5.0; pts = []
        for j in range(-3, 4): pts.append((abs(j * lam / 2), c + j * lam / 2, RED, "max"))
        for m in (-5, -3, -1, 1, 3, 5): pts.append((abs(m * lam / 4), c + m * lam / 4, BLUE, "min"))
        pts.sort(key=lambda t: t[0])
        b = defs(p) + seg(*A, *B, "currentColor", 2)
        for n, (_, x, col, _k) in enumerate(pts):
            t0 = 0.3 + n * 0.32
            b += circ(x, 100, 4.8, col, .28, appear(t0, t0 + .3, dur))
        b += circ(*A, 5, "currentColor") + circ(*B, 5, "currentColor")
        b += lbl(A[0], 128, "A", "currentColor", 13, "middle", "700") + lbl(B[0], 128, "B", "currentColor", 13, "middle", "700")
        b += lbl(c, 128, "trung điểm", "currentColor", SZ, "middle", "400")
        b += dim(p, "g", c, 76, c + lam / 2, 76, "λ/2", c + lam / 4 - 10, 66)
        b += circ(34, 24, 6, RED, 1) + lbl(46, 29, "cực đại", RED, 13, "start", "700") + circ(150, 24, 6, BLUE, 1) + lbl(162, 29, "cực tiểu", BLUE, 13, "start", "700")
        b += lbl(c, 166, "Hình mẫu AB = 3,25λ (số khác đề): 7 cực đại, 6 cực tiểu", "currentColor", SZ, "middle", "400")
        return fig("d2-0", "0 0 420 182", "Đoạn AB giữa hai nguồn cùng pha, các điểm cực đại và cực tiểu xuất hiện xen kẽ, cách nhau một phần tư bước sóng", b,
                   "Mô phỏng hình mẫu với AB = 3,25λ (khác số của đề): các điểm cực đại, cực tiểu hiện lần lượt từ trung điểm ra hai bên. Vị trí tính từ hiệu đường đi.")
    A = (40, 98); B = (300, 98); Mx = 140
    b = defs(p) + seg(*A, *B, "currentColor", 2.2) + circ(*A, 5, "currentColor") + circ(Mx, 98, 5, ORG) + circ(*B, 5, "currentColor")
    b += lbl(A[0], 80, "A", "currentColor", 13, "middle", "700") + lbl(B[0], 80, "B", "currentColor", 13, "middle", "700") + lbl(Mx, 80, "M", ORG, 13, "middle", "700")
    b += dim(p, "r", A[0], 120, Mx, 120, "d₁", (A[0] + Mx) / 2 - 6, 138) + dim(p, "b", Mx, 120, B[0], 120, "d₂", (Mx + B[0]) / 2 - 6, 138)
    b += dim(p, "g", A[0], 52, B[0], 52, "AB = 12 cm", (A[0] + B[0]) / 2 - 36, 42)
    b += lbl(40, 164, "M trên AB: d₁ + d₂ = AB, nên |d₂ − d₁| &lt; AB", "currentColor", 13, "start", "700")
    b += lbl(40, 184, "A, B là hai nguồn: không tính hai đầu", ORG, 13, "start", "700")
    return fig("d2-2", "0 0 420 196", "Điểm M bất kì trên đoạn AB, hai đoạn d1 và d2 cộng lại bằng AB", b, "Dữ kiện: M nằm trên AB nên d₁ + d₂ = AB. " + NOTE)


# ───────────── Dạng 3: bậc cực đại từ số dãy giữa M và trung trực (AB=24, MA=14, MB=26, f=10) ─────────────
def hyper_pts(kk, lam, half, ymax, side, cx, cy, n=24):
    """Đường cực đại bậc kk (|d₂−d₁| = kk·λ): side = -1 bên A (trái), +1 bên B (phải). Toạ độ màn hình, Oy lên."""
    a = kk * lam / 2; b2 = half * half - a * a
    out = []
    for i in range(n + 1):
        y = ymax * i / n
        x = a * math.sqrt(1 + y * y / b2) if kk else 0.0
        out.append((cx + side * x, cy - y))
    return out


def d3(k):
    p = f"d3{k}"
    if k == 0:
        lam = 40.0; half = 140.0; cx, cy = 200, 214; ymax = 168; dur = 5.0
        A = (cx - half, cy); B = (cx + half, cy)
        b = defs(p)
        order = [0, 1, 2, 3]
        for n_, kk in enumerate(order):
            t0 = 0.3 + n_ * 0.9
            for side in ((-1, 1) if kk else (1,)):
                col = "currentColor" if kk == 0 else RED
                dash = "6 4" if kk == 0 else ""
                d = hyper_pts(kk, lam, half, ymax, side, cx, cy)
                da = f' stroke-dasharray="{dash}"' if dash else ""
                path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in d)
                b += f'<path d="{path}" fill="none" stroke="{col}" stroke-width="2.2"{da} opacity=".28">{appear(t0, t0 + .6, dur)}</path>'
        # M trên bậc 3 bên A, độ cao 110
        a3 = 3 * lam / 2; b3 = math.sqrt(half * half - a3 * a3); yM = 110
        Mx = cx - a3 * math.sqrt(1 + yM * yM / (b3 * b3)); My = cy - yM
        b += circ(Mx, My, 6, ORG, .28, appear(3.9, 4.4, dur))
        b += seg(A[0], A[1], B[0], B[1], "currentColor", 1.4, "5 4", .6)
        b += circ(*A, 5, "currentColor") + circ(*B, 5, "currentColor")
        b += lbl(A[0], A[1] + 20, "A", "currentColor", 13, "middle", "700") + lbl(B[0], B[1] + 20, "B", "currentColor", 13, "middle", "700")
        b += lbl(Mx - 10, My + 4, "M", ORG, 13, "end", "700")
        for kk in (0, 1, 2, 3):
            a = kk * lam / 2; bb = math.sqrt(half * half - a * a); xt = cx - (a * math.sqrt(1 + ymax * ymax / (bb * bb)) if kk else 0)
            b += lbl(xt, cy - ymax - 8, f"k = {kk}", "currentColor" if kk == 0 else RED, SZ, "middle", "700")
        b += lbl(cx, 258, "Hình mẫu (số liệu khác đề): M ở một dãy cực đại", "currentColor", SZ, "middle", "400")
        return fig("d3-0", "0 0 420 268", "Các dãy cực đại dạng hypebol giữa hai nguồn cùng pha, đánh số bậc từ đường trung trực ra hai phía, điểm M nằm trên một dãy", b,
                   "Mô phỏng hình mẫu (số khác đề): các dãy cực đại tính từ d₂ − d₁ = kλ hiện lần lượt từ trung trực ra ngoài; M nằm trên dãy bậc 3.")
    s = 9.0; A = (40, 190); B = (A[0] + s * 24, 190)
    x, y = tri_pos(14, 26, 24.0); Mp = (A[0] + s * x, A[1] - s * y); tx = (A[0] + B[0]) / 2
    b = defs(p) + seg(*A, *B, "currentColor", 2) + seg(*A, *Mp, RED, 2.2) + seg(*B, *Mp, BLUE, 2.2)
    b += seg(tx, 190, tx, 34, "currentColor", 1.6, "6 4", .8)
    b += circ(*A, 4, "currentColor") + circ(*B, 4, "currentColor") + circ(*Mp, 5, ORG)
    b += lbl(A[0], A[1] + 18, "A", "currentColor", 13, "middle", "700") + lbl(B[0], B[1] + 18, "B", "currentColor", 13, "middle", "700")
    b += lbl(Mp[0] - 9, Mp[1] + 4, "M", ORG, 13, "end", "700")
    b += lbl((A[0] + Mp[0]) / 2 - 6, (A[1] + Mp[1]) / 2 + 4, "14 cm", RED, SZ, "end", "700")
    b += lbl((B[0] + Mp[0]) / 2 + 22, (B[1] + Mp[1]) / 2 - 10, "26 cm", BLUE, SZ, "start", "700")
    b += lbl(tx + 6, 46, "trung trực (k = 0)", "currentColor", SZ, "start", "400")
    b += lbl((A[0] + B[0]) / 2, 226, "AB = 24 cm", "currentColor", SZ, "middle", "400")
    b += lbl(296, 80, "Giữa M và trung trực", "currentColor", 13, "start", "700") + lbl(296, 98, "còn 3 dãy cực đại", "currentColor", 13, "start", "700")
    b += lbl(296, 130, "M thuộc bậc k = ?", ORG, 13, "start", "700")
    return fig("d3-2", "0 0 420 236", "Điểm M cách A 14 cm, cách B 26 cm, đường trung trực của AB vẽ nét đứt", b, "Dữ kiện: M không nằm trên đoạn AB, gần A hơn nên d₂ − d₁ dương. " + NOTE)


# ───────────── Dạng 4: khe Young, khoảng vân, vân sáng hay tối (a=0,8 mm, D=1,6 m, 7 vân = 6,0 mm) ─────────────
def d4(k):
    p = f"d4{k}"
    if k == 0:
        i_px = 14.0; cy = 110; dur = 4.2
        b = defs(p) + rect(16, 100, 44, 20, "none", 1, ' stroke="currentColor" stroke-width="2"')
        b += seg(60, cy, 150, cy, RED, 2.4)
        b += f'<polygon points="150,{cy} 330,24 330,196" fill="{RED}" opacity=".0">{anim("opacity", [0.0, 0.14], [0, 1], 1.0)}</polygon>'
        b += seg(150, 30, 150, 104, "currentColor", 3) + seg(150, 107, 150, 113, "currentColor", 3) + seg(150, 116, 150, 190, "currentColor", 3)
        b += seg(330, 24, 330, 196, "currentColor", 2)
        ks = sorted(range(-6, 7), key=lambda t: abs(t))
        for n_, kk in enumerate(ks):
            t0 = 0.8 + n_ * 0.22
            b += rect(332, cy + i_px * kk - 3.5, 22, 7, RED, .28, "", appear(t0, t0 + .3, dur))
        b += lbl(16, 92, "laser", "currentColor", SZ, "start", "700") + lbl(16, 140, "λ = ?", ORG, 13, "start", "700")
        b += lbl(150, 18, "hai khe  a = 0,8 mm", "currentColor", 13, "middle", "700")
        b += dim(p, "b", 150, 214, 330, 214, "D = 1,6 m", 240 - 34, 228)
        b += lbl(326, 14, "màn", "currentColor", SZ, "end", "400")
        b += lbl(326, 124, "vân trung tâm", "currentColor", SZ, "end", "400") + seg(328, cy, 332, cy, "currentColor", 1.2)
        b += lbl(358, 59, "vân sáng", RED, SZ, "start", "700")
        return fig("d4-0", "0 0 420 236", "Chùm laser đi qua hai khe hẹp rồi tạo các vân sáng tối xen kẽ trên màn", b,
                   "Mô phỏng: ánh sáng qua hai khe, các vân sáng hiện lần lượt từ vân trung tâm ra hai bên (vân vẽ theo i = λD/a của đề; khoảng cách a, D không vẽ đúng tỉ lệ).")
    b = defs(p)
    xs = [50 + 50 * kk for kk in range(7)]
    for x in xs: b += rect(x - 4, 36, 8, 30, RED, 1)
    b += lbl(xs[0], 28, "O", "currentColor", 13, "middle", "700")
    b += dim(p, "b", xs[0], 84, xs[-1], 84, "L = 6,0 mm", (xs[0] + xs[-1]) / 2 - 34, 102)
    b += lbl((xs[0] + xs[-1]) / 2, 124, "n vân liên tiếp → (n − 1) khoảng vân i", ORG, 13, "middle", "700")
    b += lbl(xs[0] + 25, 30, "i", ORG, 13, "start", "700")
    # thước đo vị trí M, N (thang khác hàng trên)
    sc = 40.0; O = (50, 168)
    b += seg(O[0], 168, O[0] + sc * 8.4, 168, "currentColor", 2)
    for nm, xv, col in (("O", 0, "currentColor"), ("M", 4.5, ORG), ("N", 7.0, GRN)):
        px = O[0] + sc * xv
        b += seg(px, 160, px, 176, col, 2.4) + lbl(px, 154, nm, col, 13, "middle", "700")
    b += dim(p, "o", O[0], 188, O[0] + sc * 4.5, 188, "OM = 4,5 mm", O[0] + sc * 2.25 - 36, 206)
    b += dim(p, "g", O[0], 216, O[0] + sc * 7.0, 216, "ON = 7,0 mm", O[0] + sc * 3.5 - 36, 234)
    return fig("d4-2", "0 0 420 244", "Hàng trên: bảy vân sáng liên tiếp, hàng dưới: vị trí hai điểm M và N đo từ vân trung tâm O", b,
               "Dữ kiện: hàng trên cho L và số vân; hàng dưới cho OM, ON (hai hàng khác thang). " + NOTE)


# ───────────── Dạng 5: hai bức xạ, vân trùng (a=1,2 mm, D=2 m, λ₁=0,60, λ₂=0,45 μm) ─────────────
def d5(k):
    p = f"d5{k}"
    if k == 0:
        i1 = 22.0; i2 = i1 * 6 / 5; x0 = 60.0; dur = 5.0
        y1, y2, y3 = 64, 114, 164
        b = defs(p)
        for kk in range(13):
            x = x0 + i1 * kk; t0 = 0.3 + (x - x0) / (12 * i1) * 3.2
            b += rect(x - 2.5, y1 - 14, 5, 28, GRN, .28, "", appear(t0, t0 + .25, dur))
        for kk in range(11):
            x = x0 + i2 * kk; t0 = 0.3 + (x - x0) / (12 * i1) * 3.2
            b += rect(x - 2.5, y2 - 14, 5, 28, ORG, .28, "", appear(t0, t0 + .25, dur))
        for kk in range(3):
            x = x0 + 6 * i1 * kk
            b += f'<line x1="{x:.1f}" y1="36" x2="{x:.1f}" y2="186" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 4" opacity=".15">{appear(3.6 + kk * .3, 4.1 + kk * .3, dur, .15)}</line>'
            b += rect(x - 4, y3 - 14, 8, 28, "currentColor", .28, "", appear(3.6 + kk * .3, 4.1 + kk * .3, dur))
        b += lbl(16, y1 + 5, "λ₁", GRN, 13, "start", "700") + lbl(16, y2 + 5, "λ₂", ORG, 13, "start", "700") + lbl(16, y3 + 4, "trùng", "currentColor", SZ, "start", "700")
        b += lbl(x0, 24, "O", "currentColor", 13, "middle", "700")
        b += lbl(250, 24, "Hình mẫu: λ₁ = 0,50 μm, λ₂ = 0,60 μm", "currentColor", SZ, "middle", "400")
        return fig("d5-0", "0 0 420 196", "Hai hệ vân sáng của hai bức xạ chồng lên nhau, có những vị trí hai vân sáng trùng nhau", b,
                   "Mô phỏng hình mẫu (số khác đề): hai hệ vân hiện từ vân trung tâm ra xa, vị trí trùng nhau đánh dấu ở hàng dưới cùng.")
    b = defs(p)
    for kk in range(8): b += rect(50 + 44 * kk - 3, 40, 6, 26, GRN, 1)
    for kk in range(10): b += rect(50 + 34 * kk - 3, 84, 6, 26, ORG, 1)
    b += seg(50, 30, 50, 120, "currentColor", 1.6, "4 4", .8)
    b += lbl(50, 22, "O (trùng)", "currentColor", SZ, "middle", "700")
    b += lbl(16, 58, "λ₁", GRN, 13, "start", "700") + lbl(16, 102, "λ₂", ORG, 13, "start", "700")
    b += lbl(50 + 22, 36, "i₁", GRN, 13, "middle", "700") + lbl(50 + 17, 126, "i₂", ORG, 13, "middle", "700")
    b += dim(p, "r", 50, 146, 150, 146, "x = ?", 74, 164)
    b += lbl(190, 152, "vân trùng: k₁·i₁ = k₂·i₂", "currentColor", 13, "start", "700")
    return fig("d5-2", "0 0 420 176", "Hai hàng vân sáng của hai bức xạ cùng xuất phát từ vân trung tâm O, vị trí trùng gần nhất cần tìm", b,
               "Dữ kiện: hai hệ vân có khoảng vân i₁, i₂ khác nhau, cùng gốc O. " + NOTE)


BUILD = [d1, d2, d3, d4, d5]

RD = ["<strong>Khái niệm:</strong> giao thoa, hai sóng gặp nhau tạo điểm mạnh và điểm yếu cố định.",
      "<strong>Định luật:</strong> hiệu đường đi $d_2-d_1$ quyết định hai sóng tới M cùng pha hay ngược pha.",
      "Cực đại: $d_2-d_1=k\\lambda$ · Cực tiểu: $d_2-d_1=(k+\\tfrac12)\\lambda$ ($k$ nguyên)",
      "Bước sóng: $\\lambda=\\dfrac{v}{f}$",
      "⚠ <strong>Điều kiện:</strong> hai nguồn kết hợp và <strong>cùng pha</strong>."]
RA = ["<strong>Khái niệm:</strong> trên AB hai sóng truyền ngược chiều, cực đại và cực tiểu nằm xen kẽ.",
      "Cực đại: $d_2-d_1=k\\lambda$ · Cực tiểu: $d_2-d_1=(k+\\tfrac12)\\lambda$",
      "M trên AB nên $|d_2-d_1|\\lt AB$ (hiệu hai cạnh nhỏ hơn cạnh thứ ba)",
      "Đếm: $-\\dfrac{AB}{\\lambda}\\lt k\\lt\\dfrac{AB}{\\lambda}$ (cực đại) · $-\\dfrac{AB}{\\lambda}-\\dfrac12\\lt k\\lt\\dfrac{AB}{\\lambda}-\\dfrac12$ (cực tiểu)",
      "⚠ <strong>Điều kiện:</strong> hai nguồn cùng pha; $k$ nguyên; <strong>không lấy hai đầu A, B</strong>."]
RB = ["<strong>Khái niệm:</strong> dãy cực đại bậc $k$ gồm các điểm có $d_2-d_1=k\\lambda$; đường trung trực là $k=0$.",
      "<strong>Định luật:</strong> hai nguồn cùng pha thì cực đại khi hai sóng tới M cùng pha.",
      "Cực đại: $d_2-d_1=k\\lambda$ · tốc độ sóng: $v=\\lambda f$",
      "Các dãy cực đại kế tiếp là $k=1,2,3,\\dots$ tính từ đường trung trực ra.",
      "⚠ <strong>Điều kiện:</strong> hai nguồn cùng pha; điểm M tồn tại khi $|d_2-d_1|\\lt AB$."]
RY = ["<strong>Khái niệm:</strong> hai khe cho hai chùm kết hợp; trên màn có vân sáng, vân tối xen kẽ.",
      "<strong>Công thức:</strong> khoảng vân $i=\\dfrac{\\lambda D}{a}$",
      "Vân sáng: $x=k\\,i$ · Vân tối: $x=(k+\\tfrac12)\\,i$ (đo từ vân trung tâm)",
      "⚠ <strong>Điều kiện:</strong> ánh sáng đơn sắc (một hệ vân); $a$, $D$, $\\lambda$, $i$ đổi về cùng hệ đơn vị."]
RY2 = ["<strong>Khái niệm:</strong> hai bức xạ cho hai hệ vân $i_1$, $i_2$ chồng lên nhau, cùng gốc ở vân trung tâm.",
       "<strong>Công thức:</strong> $i_1=\\dfrac{\\lambda_1D}{a}$ · $i_2=\\dfrac{\\lambda_2D}{a}$",
       "Trùng nhau khi $k_1i_1=k_2i_2$, tức $k_1\\lambda_1=k_2\\lambda_2$",
       "$\\dfrac{k_1}{k_2}=\\dfrac{\\lambda_2}{\\lambda_1}=\\dfrac{p}{q}$ (tối giản) nên $i_{tr}=p\\,i_1=q\\,i_2$",
       "⚠ <strong>Điều kiện:</strong> hai bức xạ đơn sắc, vân trung tâm trùng nhau."]

DANG = [
 dict(label="Dạng 1 · Dễ · Xét điểm là cực đại hay cực tiểu giao thoa", topic="Điều kiện giao thoa, cực đại và cực tiểu",
  problem_html=("<p>Trên mặt nước có hai nguồn A, B dao động cùng pha, cùng tần số $f=25\\ \\text{Hz}$, $AB=20\\ \\text{cm}$. Tốc độ truyền sóng trên mặt nước là $v=50\\ \\text{cm/s}$. "
                "Điểm M cách A $16\\ \\text{cm}$ và cách B $21\\ \\text{cm}$; điểm N cách A $18\\ \\text{cm}$ và cách B $24\\ \\text{cm}$.</p>"
                "<ol type=\"a\"><li>M là cực đại hay cực tiểu giao thoa?</li><li>N là cực đại hay cực tiểu giao thoa?</li></ol>")),
 dict(label="Dạng 2 · Trung bình · Đếm số cực đại, cực tiểu trên đoạn AB", topic="Xác định số điểm cực đại, cực tiểu trên đoạn thẳng",
  problem_html=("<p>Trên mặt nước có hai nguồn kết hợp A, B dao động cùng pha, tần số $f=20\\ \\text{Hz}$, cách nhau $AB=12\\ \\text{cm}$. Tốc độ truyền sóng là $v=40\\ \\text{cm/s}$. "
                "Trên đoạn thẳng AB có bao nhiêu điểm:</p>"
                "<ol type=\"a\"><li>dao động với biên độ cực đại?</li><li>đứng yên (cực tiểu)?</li></ol>")),
 dict(label="Dạng 3 · Trung bình · Biết số dãy cực đại giữa M và trung trực, tìm bước sóng và tốc độ", topic="Điều kiện giao thoa, cực đại và cực tiểu",
  problem_html=("<p>Trên mặt nước có hai nguồn A, B dao động cùng pha, cùng tần số $f=10\\ \\text{Hz}$, $AB=24\\ \\text{cm}$. Điểm M cách A $14\\ \\text{cm}$ và cách B $26\\ \\text{cm}$ dao động với biên độ cực đại. "
                "Giữa M và đường trung trực của AB còn có $3$ dãy cực đại khác (không kể đường trung trực).</p>"
                "<ol type=\"a\"><li>M thuộc dãy cực đại bậc mấy?</li><li>Tính bước sóng.</li><li>Tính tốc độ truyền sóng.</li></ol>")),
 dict(label="Dạng 4 · Trung bình · Khe Young: khoảng vân, bước sóng và vân sáng hay tối tại một điểm", topic="Giao thoa ánh sáng qua khe Young",
  problem_html=("<p>Trong thí nghiệm Young về giao thoa ánh sáng đơn sắc, hai khe cách nhau $a=0{,}8\\ \\text{mm}$, màn quan sát cách hai khe $D=1{,}6\\ \\text{m}$. "
                "Khoảng cách giữa $7$ vân sáng liên tiếp đo được là $6{,}0\\ \\text{mm}$. Điểm M và điểm N ở cùng một phía của vân trung tâm, cách vân trung tâm lần lượt $4{,}5\\ \\text{mm}$ và $7{,}0\\ \\text{mm}$.</p>"
                "<ol type=\"a\"><li>Tính khoảng vân $i$ và bước sóng $\\lambda$ của ánh sáng.</li><li>M và N là vân sáng hay vân tối?</li></ol>")),
 dict(label="Dạng 5 · Khó · Khe Young với hai bức xạ: vân sáng trùng nhau", topic="Giao thoa ánh sáng qua khe Young",
  problem_html=("<p>Trong thí nghiệm Young, hai khe cách nhau $a=1{,}2\\ \\text{mm}$, màn cách hai khe $D=2\\ \\text{m}$. Chiếu đồng thời hai bức xạ đơn sắc $\\lambda_1=0{,}60\\ \\mu\\text{m}$ và $\\lambda_2=0{,}45\\ \\mu\\text{m}$. "
                "Vân sáng trung tâm của hai bức xạ trùng nhau.</p>"
                "<ol type=\"a\"><li>Tính khoảng vân $i_1$ và $i_2$.</li>"
                "<li>Tìm khoảng cách từ vân trung tâm đến vân sáng gần nhất có màu giống vân trung tâm (vân sáng của hai bức xạ trùng nhau).</li>"
                "<li>Giữa hai vân trùng liên tiếp có bao nhiêu vân sáng của riêng bức xạ $\\lambda_2$?</li></ol>")),
]

ANALYSIS = [
 [("\"hai nguồn A, B dao động cùng pha\"", "Độ lệch pha hai nguồn bằng 0", "⚠ Điều kiện dùng $d_2-d_1=k\\lambda$ (cực đại) và $(k+\\tfrac12)\\lambda$ (cực tiểu)"),
  ("\"$f=25$ Hz\" và \"$v=50$ cm/s\"", "$f=25$ Hz; $v=50$ cm/s", "Bước sóng $\\lambda=\\dfrac{v}{f}$"),
  ("\"$AB=20$ cm\"", "$AB=20$ cm", "Không dùng để tính ở câu này"),
  ("\"M cách A 16 cm và cách B 21 cm\"", "$d_1=16$ cm; $d_2=21$ cm", "Hiệu đường đi $d_2-d_1$"),
  ("\"N cách A 18 cm và cách B 24 cm\"", "$d_1=18$ cm; $d_2=24$ cm", "Hiệu đường đi $d_2-d_1$"),
  ("\"cực đại hay cực tiểu\"", "Cần xét $\\dfrac{d_2-d_1}{\\lambda}$", "Nguyên → cực đại; nguyên + ½ → cực tiểu")],
 [("\"hai nguồn kết hợp A, B dao động cùng pha\"", "Độ lệch pha hai nguồn bằng 0", "⚠ Điều kiện dùng $d_2-d_1=k\\lambda$ (cực đại), $(k+\\tfrac12)\\lambda$ (cực tiểu)"),
  ("\"$f=20$ Hz\" và \"$v=40$ cm/s\"", "$f=20$ Hz; $v=40$ cm/s", "Bước sóng $\\lambda=\\dfrac{v}{f}$"),
  ("\"$AB=12$ cm\"", "$AB=12$ cm", "Điểm trên AB: $|d_2-d_1|\\lt AB$ nên $|k|\\lt\\dfrac{AB}{\\lambda}$"),
  ("\"trên đoạn thẳng AB\"", "A, B là hai nguồn", "⚠ Hai đầu A, B không phải điểm giao thoa: giữ dấu $\\lt$ chặt"),
  ("\"bao nhiêu điểm … cực đại\"", "Cần đếm số $k$ nguyên", "$-\\dfrac{AB}{\\lambda}\\lt k\\lt\\dfrac{AB}{\\lambda}$"),
  ("\"bao nhiêu điểm … cực tiểu\"", "Cần đếm số $k$ nguyên", "$-\\dfrac{AB}{\\lambda}-\\tfrac12\\lt k\\lt\\dfrac{AB}{\\lambda}-\\tfrac12$")],
 [("\"hai nguồn A, B dao động cùng pha\"", "Độ lệch pha hai nguồn bằng 0", "⚠ Điều kiện dùng cực đại $d_2-d_1=k\\lambda$ ($k$ nguyên)"),
  ("\"tần số $f=10$ Hz\"", "$f=10$ Hz", "$v=\\lambda f$"),
  ("\"$AB=24$ cm\"", "$AB=24$ cm", "Kiểm tra M tồn tại: $|d_2-d_1|\\lt AB$"),
  ("\"M cách A 14 cm và cách B 26 cm\"", "$d_1=14$ cm; $d_2=26$ cm", "Hiệu đường đi $d_2-d_1$"),
  ("\"M dao động với biên độ cực đại\"", "M nằm trên một dãy cực đại", "$d_2-d_1=k\\lambda$, $k$ là bậc của dãy"),
  ("\"giữa M và đường trung trực còn 3 dãy cực đại khác\"", "3 dãy ở giữa; trung trực là $k=0$", "Các dãy kế tiếp là $k=1,2,\\dots$ tính từ trung trực"),
  ("\"M thuộc dãy cực đại bậc mấy?\"", "Cần $k$", "Đếm từ trung trực $k=0$ ra tới dãy qua M"),
  ("\"tính bước sóng\" và \"tốc độ truyền sóng\"", "Cần $\\lambda$, $v$", "$\\lambda$ từ $d_2-d_1=k\\lambda$; $v=\\lambda f$")],
 [("\"ánh sáng đơn sắc\"", "Một bước sóng $\\lambda$, một hệ vân", "⚠ Khoảng vân $i=\\dfrac{\\lambda D}{a}$ chỉ dùng cho một bức xạ"),
  ("\"hai khe cách nhau $a=0{,}8$ mm\"", "$a=0{,}8$ mm", "$a$ là khoảng cách hai khe"),
  ("\"màn cách hai khe $D=1{,}6$ m\"", "$D=1{,}6$ m", "$D$ là khoảng cách từ khe đến màn"),
  ("\"khoảng cách giữa 7 vân sáng liên tiếp là 6,0 mm\"", "$n=7$ vân; $L=6{,}0$ mm", "⚠ $n$ vân sáng liên tiếp chỉ có $(n-1)$ khoảng vân $i$"),
  ("\"M và N … cách vân trung tâm 4,5 mm và 7,0 mm\"", "$x_M=4{,}5$ mm; $x_N=7{,}0$ mm", "Vân sáng $x=k\\,i$; vân tối $x=(k+\\tfrac12)\\,i$"),
  ("\"tính khoảng vân $i$ và bước sóng $\\lambda$\"", "Cần $i$, $\\lambda$", "$i$ từ $L$ và $n$; $\\lambda=\\dfrac{ia}{D}$"),
  ("\"M và N là vân sáng hay vân tối?\"", "Cần $\\dfrac{x}{i}$", "Nguyên → vân sáng; nguyên + ½ → vân tối")],
 [("\"hai khe cách nhau $a=1{,}2$ mm, màn cách hai khe $D=2$ m\"", "$a=1{,}2$ mm; $D=2$ m", "Mỗi bức xạ có $i=\\dfrac{\\lambda D}{a}$"),
  ("\"đồng thời hai bức xạ $\\lambda_1=0{,}60\\ \\mu$m và $\\lambda_2=0{,}45\\ \\mu$m\"", "$\\lambda_1$, $\\lambda_2$", "⚠ Hai hệ vân chồng lên nhau, mỗi hệ có khoảng vân $i_1$, $i_2$ riêng"),
  ("\"vân sáng trung tâm của hai bức xạ trùng nhau\"", "Cùng gốc $x=0$", "⚠ Cả hai hệ vân cùng tính từ vân trung tâm"),
  ("\"tính khoảng vân $i_1$ và $i_2$\"", "Cần $i_1$, $i_2$", "$i_1=\\dfrac{\\lambda_1D}{a}$ · $i_2=\\dfrac{\\lambda_2D}{a}$"),
  ("\"vân sáng gần nhất có màu giống vân trung tâm\"", "Vân trùng: $k_1i_1=k_2i_2$", "$\\dfrac{k_1}{k_2}=\\dfrac{\\lambda_2}{\\lambda_1}=\\dfrac{p}{q}$ (tối giản); $i_{tr}=p\\,i_1=q\\,i_2$"),
  ("\"giữa hai vân trùng liên tiếp … vân sáng của riêng $\\lambda_2$\"", "Hai vân trùng cách nhau $i_{tr}$", "Đếm các bậc $k_2$ nằm giữa, không kể hai vân trùng")],
]

SOLS = [
 sol(RD, [
  ("Bước sóng", [M(r"\lambda=\dfrac{v}{f}=\dfrac{50}{25}"), A(r"\lambda=2\ \text{cm}")]),
  ("Điểm M", [P("Hiệu đường đi:"), M(r"d_2-d_1=21-16=5\ \text{cm}"), P("Chia cho $\\lambda$:"), M(r"\dfrac{d_2-d_1}{\lambda}=\dfrac{5}{2}=2{,}5=2+\tfrac12")]),
  ("Điểm N", [M(r"d_2-d_1=24-18=6\ \text{cm}"), M(r"\dfrac{d_2-d_1}{\lambda}=\dfrac{6}{2}=3")]),
  ("Kết luận", [P("M: nguyên cộng $\\tfrac12$ nên hai sóng ngược pha."), P("N: số nguyên nên hai sóng cùng pha."), A("T:M là <strong>cực tiểu</strong> ($k=2$); N là <strong>cực đại</strong> ($k=3$).")]),
  ("Kiểm tra", [P("Hiệu đường đi tính bằng cm là $5$ và $6$ đều nguyên, nhưng điều kiện nguyên hay nửa nguyên là theo $\\lambda$, nên phải chia cho $\\lambda$."), P("$\\dfrac{d_2-d_1}{\\lambda}$ không có đơn vị ✓")])],
  ["a) M là cực tiểu ($k=2$)", "b) N là cực đại ($k=3$)"],
  "Nhận dạng: đề cho <strong>hai khoảng cách tới hai nguồn cùng pha</strong> và hỏi <strong>cực đại hay cực tiểu</strong> → lấy $d_2-d_1$ chia cho $\\lambda$."),
 sol(RA, [
  ("Bước sóng", [M(r"\lambda=\dfrac{v}{f}=\dfrac{40}{20}"), A(r"\lambda=2\ \text{cm}")]),
  ("Tỉ số $\\dfrac{AB}{\\lambda}$", [M(r"\dfrac{AB}{\lambda}=\dfrac{12}{2}"), A(r"\dfrac{AB}{\lambda}=6")]),
  ("Số cực đại", [M(r"-6\lt k\lt6"), P("$k$ nguyên, bỏ $k=\\pm6$ (ứng với đúng hai nguồn A, B):"), M(r"k=-5,-4,\dots,4,5"), A("T:Có <strong>11 cực đại</strong>.")]),
  ("Số cực tiểu", [M(r"-6-\dfrac12\lt k\lt6-\dfrac12"), M(r"-6{,}5\lt k\lt5{,}5"), M(r"k=-6,-5,\dots,4,5"), A("T:Có <strong>12 cực tiểu</strong>.")]),
  ("Kiểm tra", [P("11 cực đại có 10 khoảng, mỗi khoảng $\\dfrac{\\lambda}{2}=1\\ \\text{cm}$, tổng $10\\ \\text{cm}\\lt12\\ \\text{cm}$."), P("Mỗi đầu còn dư $1\\ \\text{cm}=\\dfrac{\\lambda}{2}$: cực đại kế tiếp trùng đúng nguồn A, B nên bị loại."), P("Giữa 11 cực đại có 10 cực tiểu, cộng 2 cực tiểu ở hai đầu: $10+2=12$ ✓")])],
  ["a) 11 điểm cực đại", "b) 12 điểm cực tiểu"],
  "Nhận dạng: đề hỏi <strong>số điểm cực đại, cực tiểu trên đoạn nối hai nguồn</strong> → tính $\\dfrac{AB}{\\lambda}$, đếm $k$ nguyên, bỏ hai đầu."),
 sol(RB, [
  ("Bậc của dãy cực đại qua M", [P("Trung trực là $k=0$. Giữa M và trung trực còn 3 dãy: $k=1,2,3$."), P("Dãy qua M là dãy kế tiếp:"), A(r"k=4")]),
  ("Hiệu đường đi", [M(r"d_2-d_1=MB-MA=26-14"), A(r"d_2-d_1=12\ \text{cm}")]),
  ("Bước sóng", [P("M là cực đại bậc $k$:"), M(r"d_2-d_1=k\lambda"), M(r"\lambda=\dfrac{d_2-d_1}{k}=\dfrac{12}{4}"), A(r"\lambda=3\ \text{cm}")]),
  ("Tốc độ truyền sóng", [M(r"v=\lambda f=3\cdot10"), A(r"v=30\ \text{cm/s}")]),
  ("Kiểm tra", [P("$d_2-d_1=12\\ \\text{cm}\\lt AB=24\\ \\text{cm}$ nên M tồn tại."), P("$\\dfrac{AB}{\\lambda}=8\\gt k=4$ nên dãy bậc 4 cắt được đoạn AB."), P("Đơn vị: cm · Hz = cm/s ✓")])],
  ["a) $k=4$", "b) $\\lambda=3\\ \\text{cm}$", "c) $v=30\\ \\text{cm/s}$"],
  "Nhận dạng: đề cho <strong>số dãy cực đại giữa M và trung trực</strong> → tính bậc, rồi dùng $d_2-d_1=k\\lambda$ để tìm $\\lambda$."),
 sol(RY, [
  ("Khoảng vân", [P("$7$ vân sáng liên tiếp có $6$ khoảng vân:"), M(r"i=\dfrac{L}{n-1}=\dfrac{6{,}0}{7-1}"), A(r"i=1{,}0\ \text{mm}")]),
  ("Bước sóng", [P("Từ $i=\\dfrac{\\lambda D}{a}$:"), M(r"\lambda=\dfrac{ia}{D}=\dfrac{1{,}0\cdot10^{-3}\cdot0{,}8\cdot10^{-3}}{1{,}6}"), A(r"\lambda=5\cdot10^{-7}\ \text{m}=0{,}5\ \mu\text{m}")]),
  ("Vị trí hai điểm so với khoảng vân", [M(r"\dfrac{x_M}{i}=\dfrac{4{,}5}{1{,}0}=4{,}5=4+\tfrac12"), M(r"\dfrac{x_N}{i}=\dfrac{7{,}0}{1{,}0}=7")]),
  ("Kết luận", [P("M: nguyên cộng $\\tfrac12$ nên là vân tối."), P("N: số nguyên nên là vân sáng."), A("T:M là <strong>vân tối</strong> ($k=4$); N là <strong>vân sáng bậc 7</strong>.")]),
  ("Kiểm tra", [P("$\\lambda=0{,}5\\ \\mu\\text{m}$ nằm trong vùng ánh sáng nhìn thấy ($0{,}38$ đến $0{,}76\\ \\mu\\text{m}$) ✓"), P("Chia cho $7$ thay vì $6$ sẽ ra $i\\approx0{,}86\\ \\text{mm}$ và $\\lambda\\approx0{,}43\\ \\mu\\text{m}$, vẫn nhìn thấy được nên chỉ kiểm vùng nhìn thấy chưa phát hiện được lỗi đếm khoảng vân.")])],
  ["a) $i=1{,}0\\ \\text{mm}$; $\\lambda=0{,}5\\ \\mu\\text{m}$", "b) M là vân tối ($k=4$); N là vân sáng bậc 7"],
  "Nhận dạng: đề cho <strong>n vân sáng liên tiếp</strong> và <strong>điểm cách vân trung tâm</strong> → $i=\\dfrac{L}{n-1}$, rồi xét $\\dfrac{x}{i}$."),
 sol(RY2, [
  ("Khoảng vân của từng bức xạ", [M(r"i_1=\dfrac{\lambda_1D}{a}=\dfrac{0{,}60\cdot10^{-6}\cdot2}{1{,}2\cdot10^{-3}}"), A(r"i_1=1{,}0\ \text{mm}"), M(r"i_2=\dfrac{\lambda_2D}{a}=\dfrac{0{,}45\cdot10^{-6}\cdot2}{1{,}2\cdot10^{-3}}"), A(r"i_2=0{,}75\ \text{mm}")]),
  ("Điều kiện hai vân sáng trùng", [P("Trùng khi cùng vị trí:"), M(r"k_1i_1=k_2i_2"), M(r"\dfrac{k_1}{k_2}=\dfrac{i_2}{i_1}=\dfrac{\lambda_2}{\lambda_1}=\dfrac{0{,}45}{0{,}60}=\dfrac{3}{4}"), P("Phân số tối giản, $k_1$ và $k_2$ nhỏ nhất khác $0$:"), A(r"k_1=3\ ;\ k_2=4")]),
  ("Khoảng cách tới vân trùng gần nhất", [M(r"i_{tr}=k_1i_1=3\cdot1{,}0"), A(r"i_{tr}=3{,}0\ \text{mm}"), P("Kiểm tra bằng bức xạ thứ hai:"), M(r"k_2i_2=4\cdot0{,}75=3{,}0\ \text{mm}")]),
  ("Vân sáng riêng giữa hai vân trùng", [P("Hai vân trùng liên tiếp ứng với $k_2=0$ và $k_2=4$. Giữa hai vân đó:"), M(r"k_2=1,2,3"), A("T:Có <strong>3 vân sáng</strong> của $\\lambda_2$ (và 2 vân sáng của $\\lambda_1$ với $k_1=1,2$).")]),
  ("Kiểm tra", [P("Giữa $0$ và $3{,}0\\ \\text{mm}$: $\\lambda_1$ có vân ở $1{,}0$ và $2{,}0\\ \\text{mm}$; $\\lambda_2$ có vân ở $0{,}75$; $1{,}5$ và $2{,}25\\ \\text{mm}$."), P("Không vị trí nào trùng nhau, đúng với phân số $\\dfrac{3}{4}$ đã tối giản ✓")])],
  ["a) $i_1=1{,}0\\ \\text{mm}$; $i_2=0{,}75\\ \\text{mm}$", "b) $3{,}0\\ \\text{mm}$ ($k_1=3$, $k_2=4$)", "c) 3 vân sáng của riêng $\\lambda_2$"],
  "Nhận dạng: đề chiếu <strong>hai bức xạ cùng lúc</strong> và hỏi <strong>vân trùng</strong> → $\\dfrac{k_1}{k_2}=\\dfrac{\\lambda_2}{\\lambda_1}$ tối giản, $i_{tr}=p\\,i_1$."),
]

STEPS = [
 dict(nhan_dang="Thấy <b>hai nguồn cùng pha</b> hỏi <b>cực đại hay cực tiểu</b> → lấy $\\dfrac{d_2-d_1}{\\lambda}$: nguyên là cực đại, nguyên + ½ là cực tiểu.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Bước sóng", "Bước sóng $\\lambda$ bằng bao nhiêu cm?", 2, "cm", 0.05, loi="Lấy $\\lambda=\\dfrac{f}{v}$ (lật tỉ số) hoặc quên đơn vị cm/s của $v$."),
  buoc("Điểm M", "Tỉ số $\\dfrac{d_2-d_1}{\\lambda}$ của điểm M bằng bao nhiêu?", 2.5, None, 0.05,
       loi="Chia nhầm $d_2$ hoặc $d_1$ cho $\\lambda$ thay vì hiệu $d_2-d_1$; hoặc thấy hiệu đường đi là số nguyên (cm) rồi kết luận cực đại mà chưa chia cho $\\lambda$.",
       ke=[("Lấy hiệu $d_2-d_1$ rồi chia cho $\\lambda$", True),
           ("Lấy tổng $d_1+d_2$ rồi chia cho $\\lambda$", "Điều kiện giao thoa dùng hiệu đường đi; tổng không cho biết hai sóng cùng pha hay ngược pha."),
           ("Chỉ xét hiệu $d_2-d_1$ là số nguyên hay không", "Hiệu tính bằng cm, còn nguyên hay nửa nguyên là so với $\\lambda$; phải chia cho $\\lambda$ trước.")]),
  buoc("Điểm N", "Tỉ số $\\dfrac{d_2-d_1}{\\lambda}$ của điểm N bằng bao nhiêu?", 3, None, 0.05, loi="Lấy $d_2-d_1=24+18$ (cộng thay vì trừ)."),
  buoc("Kết luận", "M và N là cực đại hay cực tiểu?",
       loi="Lẫn hai điều kiện: số nguyên mới là cực đại, nguyên cộng $\\tfrac12$ là cực tiểu.",
       lua_chon=[("M là cực tiểu, N là cực đại", True),
                 ("M là cực đại, N là cực tiểu", "Tỉ số của M là nguyên cộng $\\tfrac12$ nên cực tiểu; tỉ số của N là số nguyên nên cực đại. Đảo lại là lẫn hai điều kiện."),
                 ("Cả hai là cực đại vì hiệu đường đi tính bằng cm đều là số nguyên", "Phải so với $\\lambda$: hiệu đường đi của M bằng nguyên lần $\\lambda$ cộng $\\tfrac12\\lambda$, không phải nguyên lần $\\lambda$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Đề hỏi <b>số điểm cực đại, cực tiểu trên AB</b> → tính $\\dfrac{AB}{\\lambda}$, đếm $k$ nguyên, <b>bỏ hai đầu</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Bước sóng", "Bước sóng $\\lambda$ bằng bao nhiêu cm?", 2, "cm", 0.05, loi="Lấy $\\lambda=\\dfrac{f}{v}$ (lật tỉ số)."),
  buoc("Tỉ số $\\dfrac{AB}{\\lambda}$", "Tỉ số $\\dfrac{AB}{\\lambda}$ bằng bao nhiêu?", 6, None, 0.05, loi="Lật tỉ số thành $\\dfrac{\\lambda}{AB}$.",
       ke=[("Tính $\\dfrac{AB}{\\lambda}$ để lập khoảng giá trị của $k$", True),
           ("Tính $AB\\cdot\\lambda$", "Khoảng của $k$ lập từ $\\dfrac{AB}{\\lambda}$, không phải tích."),
           ("Tính hiệu đường đi tại trung điểm", "Trung điểm có $d_2-d_1=0$, không cho giới hạn của $k$.")]),
  buoc("Số cực đại", "Có bao nhiêu điểm cực đại trên đoạn AB?", 11, "điểm", 0,
       loi="Dùng dấu $\\le$, lấy cả $k=\\pm6$ ra 13 điểm; hai giá trị đó ứng với đúng vị trí hai nguồn.",
       ke=[("Giải $-\\dfrac{AB}{\\lambda}\\lt k\\lt\\dfrac{AB}{\\lambda}$, bỏ hai đầu (dấu $\\lt$ chặt)", True),
           ("Giải $-\\dfrac{AB}{\\lambda}\\le k\\le\\dfrac{AB}{\\lambda}$", "A và B là chính các nguồn, không phải điểm giao thoa trên đoạn; khi $\\dfrac{AB}{\\lambda}$ nguyên thì $k=\\pm\\dfrac{AB}{\\lambda}$ rơi đúng A, B nên phải loại."),
           ("Lấy số cực đại bằng $\\dfrac{AB}{\\lambda}$", "Đó chỉ là số bước sóng nằm trên AB; các cực đại cách nhau $\\dfrac{\\lambda}{2}$ và nằm cả hai phía trung điểm.")]),
  buoc("Số cực tiểu", "Có bao nhiêu điểm cực tiểu trên đoạn AB?", 12, "điểm", 0,
       loi="Dùng lại khoảng của cực đại nên ra cùng số với cực đại; quên khoảng của $k$ lệch đi $\\tfrac12$.",
       ke=[("Giải $-\\dfrac{AB}{\\lambda}-\\dfrac{1}{2}\\lt k\\lt\\dfrac{AB}{\\lambda}-\\dfrac{1}{2}$", True),
           ("Dùng lại $-\\dfrac{AB}{\\lambda}\\lt k\\lt\\dfrac{AB}{\\lambda}$ của cực đại", "Cực tiểu có hiệu đường đi $(k+\\tfrac12)\\lambda$ nên khoảng của $k$ lệch đi $\\tfrac12$."),
           ("Số cực tiểu luôn bằng số cực đại", "Hai khoảng của $k$ không trùng nhau nên số nguyên $k$ trong hai khoảng có thể khác nhau.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>còn n dãy cực đại giữa M và trung trực</b> → bậc của dãy qua M, rồi $d_2-d_1=k\\lambda$ để tìm $\\lambda$.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Bậc của dãy cực đại qua M", "Dãy cực đại qua M có bậc $k$ bằng bao nhiêu?", 4, None, 0,
       loi="Đếm đủ 3 dãy ở giữa rồi dừng, quên chính dãy qua M; hoặc tính cả đường trung trực vào số dãy ở giữa."),
  buoc("Hiệu đường đi", "Hiệu đường đi $d_2-d_1$ của M bằng bao nhiêu cm?", 12, "cm", 0.1,
       loi="Lấy $d_2-d_1=AB$ hoặc cộng $14+26$.",
       ke=[("Lấy $d_2-d_1=MB-MA$", True),
           ("Lấy $d_1+d_2$", "Tổng hai đoạn không cho độ lệch pha; điều kiện cực đại dùng hiệu."),
           ("Lấy $d_2-d_1=AB$", "Chỉ đúng khi M thẳng hàng với A, B và nằm ngoài đoạn AB; M ở vị trí tổng quát thì $d_2-d_1\\lt AB$.")]),
  buoc("Bước sóng", "Bước sóng $\\lambda$ bằng bao nhiêu cm?", 3, "cm", 0.05,
       loi="Lấy $\\lambda=d_2-d_1$ (chỉ đúng với dãy bậc 1) hoặc dùng $k+\\tfrac12$ của cực tiểu.",
       ke=[("$\\lambda=\\dfrac{d_2-d_1}{k}$ với $k$ là bậc của dãy cực đại", True),
           ("$\\lambda=d_2-d_1$ vì M là cực đại", "Chỉ đúng với dãy bậc 1; M ở bậc $k$ nên $d_2-d_1=k\\lambda$."),
           ("$\\lambda=\\dfrac{d_2-d_1}{k+\\tfrac12}$", "Đó là điều kiện của cực tiểu; M là cực đại nên là $k\\lambda$.")]),
  buoc("Tốc độ truyền sóng", "Tốc độ truyền sóng $v$ bằng bao nhiêu cm/s?", 30, "cm/s", 0.5,
       loi="Lấy $v=\\dfrac{\\lambda}{f}$ (ra đơn vị cm·s, không phải cm/s).",
       ke=[("$v=\\lambda f$", True),
           ("$v=\\dfrac{\\lambda}{f}$", "Đơn vị ra cm·s, không phải cm/s; đúng là $v=\\lambda f$."),
           ("$v=\\dfrac{d_2-d_1}{f}$", "Hiệu đường đi chưa phải bước sóng; phải qua $\\lambda=\\dfrac{d_2-d_1}{k}$ trước.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>n vân liên tiếp</b> và <b>điểm cách vân trung tâm</b> → $i=\\dfrac{L}{n-1}$, rồi xét $\\dfrac{x}{i}$ nguyên hay nửa nguyên.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Khoảng vân", "Khoảng vân $i$ bằng bao nhiêu mm?", 1, "mm", 0.02,
       loi="Chia cho số vân (7) thay vì số khoảng vân; $n$ vân liên tiếp chỉ có $n-1$ khoảng."),
  buoc("Bước sóng", "Bước sóng $\\lambda$ bằng bao nhiêu $\\mu$m?", 0.5, "μm", 0.01,
       loi="Lật công thức thành $\\lambda=\\dfrac{iD}{a}$ hoặc quên đổi mm, m sang cùng đơn vị.",
       ke=[("Từ $i=\\dfrac{\\lambda D}{a}$ suy ra $\\lambda=\\dfrac{ia}{D}$", True),
           ("$\\lambda=\\dfrac{iD}{a}$", "Lật tử mẫu: $\\lambda$ tỉ lệ thuận với $i$ và $a$, tỉ lệ nghịch với $D$."),
           ("$\\lambda=\\dfrac{aD}{i}$", "Sai chiều phụ thuộc: $i$ tăng thì $\\lambda$ phải tăng, không giảm.")]),
  buoc("Vị trí hai điểm so với khoảng vân", "Tỉ số $\\dfrac{x_M}{i}$ của điểm M bằng bao nhiêu?", 4.5, None, 0.05,
       loi="Chia vị trí cho $\\lambda$ hoặc cho $a$ thay vì khoảng vân $i$.",
       ke=[("Chia vị trí $x$ cho khoảng vân $i$ rồi xét nguyên hay nửa nguyên", True),
           ("Chia $x$ cho $a$", "$a$ là khoảng cách hai khe; vị trí vân tính theo khoảng vân $i$."),
           ("Chia $x$ cho $\\lambda$", "Vân sáng, vân tối quyết định bởi $\\dfrac{x}{i}$; $\\lambda$ chỉ dùng để tính $i$.")]),
  buoc("Kết luận", "M và N là vân sáng hay vân tối?",
       loi="Thấy số lẻ ở M (4,5) mà vẫn gọi là vân sáng, hoặc gọi số nguyên là vân tối.",
       lua_chon=[("M là vân tối, N là vân sáng bậc 7", True),
                 ("M là vân sáng, N là vân tối", "Tỉ số của M là nguyên cộng $\\tfrac12$ nên vân tối; tỉ số của N là số nguyên nên vân sáng."),
                 ("Cả hai là vân sáng vì cùng nằm một phía vân trung tâm", "Vân sáng hay tối phụ thuộc $\\dfrac{x}{i}$, không phụ thuộc phía của điểm.")],
       ke=[("So tỉ số $\\dfrac{x}{i}$ với số nguyên và nửa nguyên", True),
           ("So $x$ với $\\lambda$", "$x$ đo bằng mm, $\\lambda$ bằng $\\mu$m: không so sánh trực tiếp được."),
           ("So $x$ với $D$", "$D$ là khoảng cách tới màn, không quyết định vân sáng hay tối.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>hai bức xạ cùng lúc</b> và hỏi <b>vân trùng</b> → $\\dfrac{k_1}{k_2}=\\dfrac{\\lambda_2}{\\lambda_1}$ tối giản, $i_{tr}=p\\,i_1$.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Khoảng vân của từng bức xạ", "Khoảng vân $i_2$ của bức xạ $\\lambda_2$ bằng bao nhiêu mm?", 0.75, "mm", 0.01,
       loi="Đổi sai đơn vị ($\\mu$m sang m, mm sang m) nên lệch lũy thừa 10."),
  buoc("Điều kiện hai vân sáng trùng", "Giá trị nhỏ nhất khác $0$ của $k_1$ để hai vân sáng trùng nhau là bao nhiêu?", 3, None, 0,
       loi="Lật tỉ số thành $\\dfrac{k_1}{k_2}=\\dfrac{\\lambda_1}{\\lambda_2}$ (ra $k_1=4$), hoặc không rút gọn phân số.",
       ke=[("Vân trùng khi $k_1i_1=k_2i_2$ nên $\\dfrac{k_1}{k_2}=\\dfrac{\\lambda_2}{\\lambda_1}$, rồi rút gọn", True),
           ("$\\dfrac{k_1}{k_2}=\\dfrac{\\lambda_1}{\\lambda_2}$", "Lật tỉ số: từ $k_1\\lambda_1=k_2\\lambda_2$ suy ra $\\dfrac{k_1}{k_2}=\\dfrac{\\lambda_2}{\\lambda_1}$; bước sóng nhỏ hơn thì cần bậc cao hơn."),
           ("Khoảng vân trùng bằng $i_1+i_2$", "Hai hệ vân lặp lại theo bội của từng khoảng vân; chỗ trùng là bội chung, không phải tổng.")]),
  buoc("Khoảng cách tới vân trùng gần nhất", "Khoảng cách từ vân trung tâm đến vân trùng gần nhất bằng bao nhiêu mm?", 3, "mm", 0.05,
       loi="Lấy $i_{tr}=k_2i_1$ (nhân nhầm bậc) hoặc lấy trung bình cộng của $i_1$, $i_2$.",
       ke=[("$i_{tr}=p\\,i_1=q\\,i_2$ với $\\dfrac{p}{q}$ là phân số tối giản", True),
           ("$i_{tr}=\\dfrac{i_1+i_2}{2}$", "Vân trùng ứng với $k$ nguyên của cả hai bức xạ; trung bình cộng không đảm bảo điều đó."),
           ("Lấy vân sáng bậc 1 của bức xạ thứ hai", "Vân bậc 1 của bức xạ thứ hai không nằm đúng trên vân sáng nào của bức xạ thứ nhất.")]),
  buoc("Vân sáng riêng giữa hai vân trùng", "Giữa hai vân trùng liên tiếp có bao nhiêu vân sáng của riêng $\\lambda_2$?", 3, "vân", 0,
       loi="Đếm cả vân trùng ở hai đầu (ra 4 hoặc 5), hoặc lấy số khoảng vân thay vì số vân nằm giữa.",
       ke=[("Đếm các bậc $k_2=1,2,\\dots,q-1$ nằm giữa hai vân trùng", True),
           ("Đếm cả bậc $k_2=q$", "Bậc $q$ của $\\lambda_2$ trùng với vân sáng của $\\lambda_1$: đó là vân trùng, không phải vân riêng."),
           ("Lấy $\\dfrac{i_{tr}}{i_2}$ làm số vân", "Tỉ số cho số khoảng vân; số vân nằm giữa ít hơn số khoảng một đơn vị.")]),
  buoc("Kiểm tra")]),
]

# ───────────── Tự luận: ví dụ cũ chưa biên tập (giữ nguyên lời giải gốc) ─────────────
OLD = json.load(open(os.path.join(HERE, "old/31.json")))["questions"]
EX = []
for q in OLD:
    for part in re.split(r'(?=<p class="text-base leading-relaxed my-2"><strong class="font-bold">Ví dụ)', q["body_html"]):
        if "Ví dụ" in part: EX.append(part)
assert len(EX) == 6, len(EX)


def tl_item(h, k, muc):
    h = re.sub(r"Ví dụ \d+:?", f"Bài {k}.", h, count=1)
    h = re.sub(r"<(?![a-zA-Z/!?])", r"\\lt ", h)
    de, gi = h.split('<p class="text-base leading-relaxed my-2"><strong class="font-bold">Lời giải:</strong>', 1)
    return (f'<h4>Bài {k} · {muc}</h4>{de}<details><summary>Hướng dẫn giải</summary>'
            f'<p class="text-base leading-relaxed my-2"><strong class="font-bold">Lời giải:</strong>{gi}</details>')


# Ví dụ 2 → Dạng 3, Ví dụ 4 → Dạng 4, Ví dụ 6 → Dạng 5 (đã biên tập); còn Ví dụ 1, 3, 5.
TU_LUAN = dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
               body_html="<p>Các bài còn lại của bài học, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>"
               + tl_item(EX[0], 1, "Dễ") + tl_item(EX[2], 2, "Dễ") + tl_item(EX[4], 3, "Trung bình"))

if __name__ == "__main__":
    write(J, 31, "Bài 12. Giao thoa sóng", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
    inject(J, BUILD, ANALYSIS, SOLS, STEPS)
