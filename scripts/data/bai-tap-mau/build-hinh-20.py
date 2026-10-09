"""Bài 20 · Bài 1. Dao động điều hoà (Vật lí 11, chương 1 Dao động) — dựng scripts/data/bai-tap-mau/20.json từ đầu.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-20.py        (mẫu cấu trúc: build-hinh-57.py, hình đồ thị/sóng: build-hinh-33.py)

Quy ước theo lý thuyết bài 20: x = A·cos(ωt + φ), A > 0 · pha = ωt + φ, φ = pha lúc t = 0 · T = 2π/ω, f = 1/T (một vòng quay đều ứng với 2π rad) ·
đồ thị li độ – thời gian là đường hình sin (A: đỉnh; T: giữa hai đỉnh liên tiếp) · hình chiếu của chuyển động tròn đều: bán kính = A, tốc độ góc = ω,
φ = góc từ trục Ox tới OM lúc t = 0 (ngược chiều kim đồng hồ). KHÔNG dùng vận tốc/gia tốc/năng lượng (bài 22+).

Quét dạng (bước 0, làm trong đầu từ lý thuyết bài + ngân hàng; question_topics của bài nằm dưới lesson 21 "Mô tả dao động điều hoà":
154 Li độ, biên độ, chu kì, tần số, pha ban đầu — 184 câu bai_tap · 155 Viết phương trình dao động điều hoà — 77 · 156 Đọc đồ thị li độ – thời gian — 94):
  1 · cấp 1 · Đọc phương trình có số cụ thể: A, ω, φ, T, f, pha, li độ         · topic 154
  2 · cấp 2 · Phương trình có dấu trừ trước côsin: đưa về A > 0, tìm φ, li độ     · topic 154
  3 · cấp 2 · Đọc đồ thị li độ – thời gian: A, T (bẫy nửa chu kì), ω, φ, viết phương trình · topic 156
  4 · cấp 3 · Viết phương trình từ chiều dài quỹ đạo, số dao động và gốc thời gian ở biên · topic 155
  5 · cấp 4 · Hình chiếu của chuyển động tròn đều (đĩa quay vòng/phút): A, ω, φ, phương trình, li độ · topic 155
Bỏ: vận tốc, gia tốc, năng lượng, quãng đường, thời gian ngắn nhất (không có trong lý thuyết bài này, thuộc bài 21–24).
Ví dụ cũ (x = 5cos4πt: A, T, f) đã biên tập thành Dạng 1 nên không còn tự luận."""
import json, math, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "20.json")
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
PI = math.pi
PER = 24   # số mẫu mỗi chu kì (nội suy tuyến tính giữa các mẫu)


def fnum(x, nd=1):
    s = f"{x:.{nd}f}".replace(".", ",")
    if "," in s:
        s = s.rstrip("0").rstrip(",")
    return s.replace("-", "−")


def sec_dur(T, slow, ncyc):
    """(giây mỗi khoảng mẫu, tổng giây) khi chạy chậm `slow` lần trong `ncyc` chu kì."""
    return T * slow / PER, T * slow * ncyc


def times(T, ncyc):
    return [i * T / PER for i in range(PER * ncyc + 1)]


# ═════════════ Đường ray + khối trượt (dùng cho dạng 1, 2, 4) ═════════════
CX, RY = 210, 118


def rail(p, s, half, ticks=None, numbers=True, end_marks=None):
    b = seg(CX - s * half - 24, RY, CX + s * half + 24, RY, "currentColor", 2.4)
    b += lbl(CX + s * half + 24, RY - 8, "x (cm)", "currentColor", 12, "end", "700") if numbers else lbl(CX + s * half + 24, RY - 8, "x", "currentColor", 13, "end", "700")
    for u in (ticks or []):
        x = CX + s * u
        b += seg(x, RY, x, RY + 7, "currentColor", 1.6)
        b += lbl(x, RY + 24, "O" if u == 0 else fnum(u), "currentColor", 12, "middle", "700" if u == 0 else "400")
    if not ticks:
        b += seg(CX, RY, CX, RY + 7, "currentColor", 1.6) + lbl(CX, RY + 24, "O", "currentColor", 12, "middle", "700")
    for u in (end_marks or []):
        b += seg(CX + s * u, RY - 46, CX + s * u, RY + 7, "currentColor", 1.2, "4 4", .55)
    return b


def block(x0, color=GRN):
    return f'<rect x="{x0 - 14:.1f}" y="{RY - 24}" width="28" height="22" rx="3" fill="{color}" stroke="currentColor" stroke-width="1.6"/>'


def block_anim(xs_px, dur, color=GRN):
    return (f'<rect x="{xs_px[0] - 14:.1f}" y="{RY - 24}" width="28" height="22" rx="3" fill="{color}" stroke="currentColor" stroke-width="1.6">'
            + smil("x", [v - 14 for v in xs_px], dur) + "</rect>")


# ═════════════ Dạng 1 · x = 10cos(4πt + 2π/3) cm ═════════════
A1, W1, PH1 = 10.0, 4 * PI, 2 * PI / 3
T1 = 2 * PI / W1
S1 = 16


def x1(t): return A1 * math.cos(W1 * t + PH1)


def d1(k):
    p = f"d1{k}"; VB = "0 0 420 160"
    b = defs(p) + rail(p, S1, A1, [-10, -5, 0, 5, 10])
    if k == 0:
        ncyc = 2; step, dur = sec_dur(T1, 4, ncyc)
        xs = [CX + S1 * x1(t) for t in times(T1, ncyc)]
        dur = step * (len(xs) - 1)
        b += seg(xs[0], RY - 46, xs[0], RY - 28, "currentColor", 1.2, "4 4", .7) + lbl(xs[0], RY - 52, "t = 0", "currentColor", 12, "middle", "700")
        b += block_anim(xs, dur)
        b += lbl(18, 26, "x = 10cos(4πt + 2π/3) cm", "currentColor", 13, "start", "700")
        return fig("d1-0", VB, "Vật trượt qua lại trên trục Ox quanh vị trí cân bằng O, từ −10 cm đến +10 cm", b,
                   "Mô phỏng: vật dao động theo đúng phương trình đề cho (chạy chậm 4 lần, 2 chu kì; bấm Chạy mô phỏng). Tính theo công thức.")
    b += arrow(p, "o", CX, RY - 36, CX + S1 * A1, RY - 36, 2.4) + lbl(CX + S1 * A1 / 2, RY - 44, "A = ?", ORG, 13, "middle", "700")
    b += lbl(18, 26, "x = A cos(ωt + φ)", "currentColor", 13, "start", "700")
    b += lbl(18, 52, "Đề cho: số cụ thể thay cho A, ω, φ", "currentColor", 12, "start", "400")
    return fig("d1-2", VB, "Trục Ox với vị trí cân bằng O; biên độ A là khoảng từ O tới biên", b, "Dữ kiện: A là khoảng từ O tới biên; ω và φ đọc từ phương trình. " + NOTE)


# ═════════════ Dạng 2 · x = −6cos(5πt − π/3) cm ═════════════
A2, W2 = 6.0, 5 * PI
T2 = 2 * PI / W2
S2 = 24


def x2(t): return -A2 * math.cos(W2 * t - PI / 3)


def d2(k):
    p = f"d2{k}"
    if k == 0:
        VB = "0 0 420 160"
        b = defs(p) + rail(p, S2, A2, [-6, 0, 6])
        ncyc = 2; step, dur = sec_dur(T2, 4, ncyc)
        xs = [CX + S2 * x2(t) for t in times(T2, ncyc)]
        dur = step * (len(xs) - 1)
        b += seg(xs[0], RY - 46, xs[0], RY - 28, "currentColor", 1.2, "4 4", .7) + lbl(xs[0], RY - 52, "t = 0", "currentColor", 12, "middle", "700")
        b += block_anim(xs, dur)
        b += lbl(18, 26, "x = −6cos(5πt − π/3) cm", "currentColor", 13, "start", "700")
        return fig("d2-0", VB, "Vật trượt qua lại trên trục Ox giữa −6 cm và +6 cm", b,
                   "Mô phỏng: vật dao động theo đúng phương trình đề cho (chạy chậm 4 lần, 2 chu kì; bấm Chạy mô phỏng). Tính theo công thức.")
    # k = 2: hai đường cos α và −cos α, lệch nhau π (không mang số của đề)
    VB = "0 0 420 236"
    X0, Y0, SX, SY = 54, 128, 52, 52          # α từ 0 → 2π: 0 → 327 px
    b = defs(p)
    for a in (0, 0.5, 1, 1.5, 2):
        xx = X0 + SX * PI * a
        b += seg(xx, 56, xx, 200, "currentColor", 1, "", .13) + seg(xx, Y0 - 3, xx, Y0 + 3, "currentColor", 1.4)
        b += lbl(xx, 220, {0: "0", 0.5: "π/2", 1: "π", 1.5: "3π/2", 2: "2π"}[a], "currentColor", 12, "middle", "400")
    b += seg(X0, Y0, X0 + SX * 2 * PI + 14, Y0, "currentColor", 1.6) + seg(X0, 50, X0, 206, "currentColor", 1.6)
    b += lbl(X0 + SX * 2 * PI + 14, Y0 - 8, "α (rad)", "currentColor", 12, "end", "700") + lbl(X0 - 8, 46, "y", "currentColor", 12, "end", "700")
    pts_c = [(X0 + SX * a, Y0 - SY * math.cos(a)) for a in [i * 2 * PI / 96 for i in range(97)]]
    pts_m = [(X0 + SX * a, Y0 + SY * math.cos(a)) for a in [i * 2 * PI / 96 for i in range(97)]]
    b += poly(pts_c, GRN, 2.2, "6 4") + poly(pts_m, ORG, 2.8)
    b += dim(p, "r", X0, 34, X0 + SX * PI, 34, "", 0, 0) + lbl(X0 + SX * PI / 2, 28, "lệch π", RED, 13, "middle", "700")
    b += seg(X0, 34, X0, Y0 - SY, RED, 1, "3 3", .6) + seg(X0 + SX * PI, 34, X0 + SX * PI, Y0 - SY, RED, 1, "3 3", .6)
    b += lbl(X0 + 8, 196, "cos α", GRN, 13, "start", "700") + lbl(X0 + SX * 2 * PI - 6, 70, "−cos α = cos(α + π)", ORG, 13, "end", "700")
    return fig("d2-2", VB, "Hai đường côsin: đường cos α nét đứt và đường −cos α nét liền, đường này lệch pha π so với đường kia", b,
               "Dữ kiện: đổi dấu của côsin tương đương dịch pha π. " + NOTE)


# ═════════════ Dạng 3 · đồ thị x = 4cos(2πt + π) cm, T = 1 s ═════════════
A3, T3 = 4.0, 1.0
W3 = 2 * PI / T3
GX0, GY0, SXT, SYX = 56, 126, 150, 19


def gx(t): return GX0 + SXT * t
def gy(x): return GY0 - SYX * x
def x3(t): return A3 * math.cos(W3 * t + PI)


def frame3(p):
    b = defs(p)
    for i in range(0, 5):
        t = i / 2
        b += seg(gx(t), 40, gx(t), 206, "currentColor", 1, "", .14) + lbl(gx(t), 224, fnum(t), "currentColor", 12, "middle", "400")
    for u in (-4, 4):
        b += seg(GX0, gy(u), gx(2) + 6, gy(u), "currentColor", 1, "5 4", .3)
    for u in (-4, 0, 4):
        b += lbl(GX0 - 8, gy(u) + 4, fnum(u), "currentColor", 12, "end", "400")
    b += seg(GX0, GY0, gx(2) + 22, GY0, "currentColor", 1.6) + seg(GX0, 26, GX0, 206, "currentColor", 1.6)
    b += lbl(GX0 + 6, 20, "x (cm)", "currentColor", 12, "start", "700") + lbl(gx(2) + 22, 240, "t (s)", "currentColor", 12, "end", "700")
    return b


def curve3(c=GRN, w=2.6):
    pts = [(gx(t), gy(x3(t))) for t in [i / 96 * 2 for i in range(97)]]
    return poly(pts, c, w)


def d3(k):
    p = f"d3{k}"; VB = "0 0 420 244"
    b = frame3(p) + curve3()
    if k == 0:
        ncyc = 2; step, dur = sec_dur(T3, 2, ncyc)
        ts = times(T3, ncyc)
        X = [gx(t) for t in ts]; Y = [gy(x3(t)) for t in ts]
        dur = step * (len(ts) - 1)
        b += (f'<line x1="{X[0]:.1f}" y1="{Y[0]:.1f}" x2="{X[0]:.1f}" y2="{GY0}" stroke="{ORG}" stroke-width="1.6" stroke-dasharray="4 3">'
              + smil("x1", X, dur) + smil("x2", X, dur) + smil("y1", Y, dur) + "</line>")
        b += (f'<circle cx="{X[0]:.1f}" cy="{Y[0]:.1f}" r="5.5" fill="{ORG}" stroke="currentColor" stroke-width="1.5">'
              + smil("cx", X, dur) + smil("cy", Y, dur) + "</circle>")
        return fig("d3-0", VB, "Đồ thị li độ theo thời gian của một vật dao động điều hoà, đường hình sin xuất phát từ điểm thấp nhất", b,
                   "Mô phỏng: điểm cam chạy trên đồ thị, vạch đứng cho biết li độ tại từng thời điểm (chạy chậm 2 lần, 2 chu kì; bấm Chạy mô phỏng). Đồ thị tính theo công thức.")
    b += dim(p, "o", gx(0.5), 38, gx(1.5), 38, "", 0, 0) + lbl(gx(1.0), 30, "T = ?", ORG, 13, "middle", "700")
    b += seg(gx(0.5), 38, gx(0.5), gy(A3) - 2, ORG, 1, "3 3", .7) + seg(gx(1.5), 38, gx(1.5), gy(A3) - 2, ORG, 1, "3 3", .7)
    xa = gx(0.12)
    b += dim(p, "b", xa, GY0, xa, gy(A3), "", 0, 0) + lbl(xa - 6, (GY0 + gy(A3)) / 2 + 4, "A = ?", BLUE, 13, "end", "700")
    b += dot(gx(0), gy(x3(0)), 5, RED) + lbl(GX0 + 30, 199, "t = 0: x(0) = ?", RED, 13, "start", "700")
    return fig("d3-2", VB, "Đồ thị li độ theo thời gian với các chỗ cần đọc: biên độ A, chu kì T giữa hai đỉnh liên tiếp, li độ lúc t bằng 0", b,
               "Dữ kiện: A từ trục tới đỉnh; T giữa hai đỉnh liên tiếp; φ từ li độ lúc t = 0. " + NOTE)


# ═════════════ Dạng 4 · L = 16 cm, 30 dao động / 20 s, t = 0 ở biên âm ═════════════
A4, T4 = 8.0, 20 / 30
W4 = 2 * PI / T4
S4 = 20


def x4(t): return A4 * math.cos(W4 * t + PI)


def d4(k):
    p = f"d4{k}"; VB = "0 0 420 176"
    b = defs(p) + rail(p, S4, A4, None, numbers=False, end_marks=[-A4, A4])
    b += dim(p, "o", CX - S4 * A4, RY + 40, CX + S4 * A4, RY + 40, "L = 16 cm", CX - 36, RY + 58)
    if k == 0:
        ncyc = 2; step, dur = sec_dur(T4, 3, ncyc)
        xs = [CX + S4 * x4(t) for t in times(T4, ncyc)]
        dur = step * (len(xs) - 1)
        b += lbl(xs[0], RY - 52, "t = 0", "currentColor", 12, "middle", "700")
        b += block_anim(xs, dur)
        return fig("d4-0", VB, "Vật dao động trên đoạn thẳng dài 16 cm, bắt đầu từ biên bên trái", b,
                   "Mô phỏng: vật bắt đầu từ biên âm, dao động trên đoạn thẳng 16 cm (chạy chậm 3 lần, 2 chu kì; bấm Chạy mô phỏng). Tính theo công thức.")
    b += block(CX - S4 * A4, "none")
    b += arrow(p, "b", CX, RY - 36, CX + S4 * A4, RY - 36, 2.4) + lbl(CX + S4 * A4 / 2, RY - 44, "A = ?", BLUE, 13, "middle", "700")
    b += lbl(CX - S4 * A4, RY - 52, "t = 0", "currentColor", 12, "middle", "700")
    b += lbl(18, 26, "N dao động trong t giây", "currentColor", 13, "start", "700")
    return fig("d4-2", VB, "Đoạn thẳng dài 16 cm, vị trí cân bằng O ở giữa, biên độ A là nửa đoạn thẳng", b, "Dữ kiện: L = 2A; gốc thời gian lúc vật ở biên âm. " + NOTE)


# ═════════════ Dạng 5 · đĩa R = 12 cm, 150 vòng/phút, t = 0 ở điểm cao nhất ═════════════
R5, N5 = 12.0, 150
W5 = 2 * PI * N5 / 60
T5 = 2 * PI / W5
PH5 = PI / 2
OX, OY, RP = 150, 138, 100


def d5(k):
    p = f"d5{k}"; VB = "0 0 420 262"
    b = defs(p)
    b += f'<circle cx="{OX}" cy="{OY}" r="{RP}" fill="none" stroke="currentColor" stroke-width="1.8" opacity=".6"/>'
    b += arrow(p, "g", OX - RP - 22, OY, OX + RP + 40, OY, 2.2) + lbl(OX + RP + 42, OY - 8, "x", GRN, 13, "start", "700")
    b += dot(OX, OY, 3.5, "currentColor") + lbl(OX - 10, OY + 18, "O", "currentColor", 13, "end", "700")
    b += dim(p, "o", OX, OY, OX + RP * math.cos(math.radians(-40)), OY - RP * math.sin(math.radians(-40)), "", 0, 0)
    b += lbl(OX + RP * math.cos(math.radians(-40)) + 8, OY - RP * math.sin(math.radians(-40)) + 18, "R = 12 cm", ORG, 13, "start", "700")
    if k == 0:
        # cung mũi tên chiều quay (ngược chiều kim đồng hồ) bên ngoài đường tròn
        rr = RP + 14
        a0, a1 = 112, 158
        pa = (OX + rr * math.cos(math.radians(a0)), OY - rr * math.sin(math.radians(a0)))
        pb = (OX + rr * math.cos(math.radians(a1)), OY - rr * math.sin(math.radians(a1)))
        b += f'<path d="M{pa[0]:.1f},{pa[1]:.1f} A{rr},{rr} 0 0 0 {pb[0]:.1f},{pb[1]:.1f}" fill="none" stroke="{RED}" stroke-width="2.4"/>'
        tdx, tdy = -math.sin(math.radians(a1)), -math.cos(math.radians(a1))
        b += chevron(pb[0], pb[1], tdx, tdy, RED, 2.4, 11)
        b += lbl(6, 20, "150 vòng/phút", RED, 13, "start", "700")
        ncyc = 2; step, dur = sec_dur(T5, 4, ncyc)
        ts = times(T5, ncyc)
        th = [PH5 + W5 * t for t in ts]
        MX = [OX + RP * math.cos(a) for a in th]; MY = [OY - RP * math.sin(a) for a in th]
        dur = step * (len(ts) - 1)
        b += lbl(OX + 16, OY - RP - 8, "M lúc t = 0", ORG, 12, "start", "700")
        b += (f'<line x1="{OX}" y1="{OY}" x2="{MX[0]:.1f}" y2="{MY[0]:.1f}" stroke="{ORG}" stroke-width="2">' + smil("x2", MX, dur) + smil("y2", MY, dur) + "</line>")
        b += (f'<line x1="{MX[0]:.1f}" y1="{MY[0]:.1f}" x2="{MX[0]:.1f}" y2="{OY}" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 3" opacity=".8">'
              + smil("x1", MX, dur) + smil("x2", MX, dur) + smil("y1", MY, dur) + "</line>")
        b += (f'<circle cx="{MX[0]:.1f}" cy="{MY[0]:.1f}" r="6.5" fill="{ORG}" stroke="currentColor" stroke-width="1.5">' + smil("cx", MX, dur) + smil("cy", MY, dur) + "</circle>")
        b += (f'<circle cx="{MX[0]:.1f}" cy="{OY}" r="6.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">' + smil("cx", MX, dur) + "</circle>")
        b += lbl(OX, 254, "Q: hình chiếu của M", GRN, 12, "middle", "700")
        return fig("d5-0", VB, "Đĩa tròn bán kính 12 cm quay đều ngược chiều kim đồng hồ, điểm M ở mép đĩa, hình chiếu Q của M lên trục Ox nằm ngang chạy qua lại", b,
                   "Mô phỏng: M quay đều từ điểm cao nhất, Q là hình chiếu của M lên Ox (chạy chậm 4 lần, 2 vòng; bấm Chạy mô phỏng). Tính theo công thức.")
    b += arc(OX, OY, 34, 0, 90, RED, 2.2) + lbl(OX + 40, OY - 40, "φ = ?", RED, 13, "start", "700")
    b += seg(OX, OY, OX, OY - RP, ORG, 2.2) + dot(OX, OY - RP, 6.5, ORG) + lbl(OX + 12, OY - RP - 8, "M lúc t = 0", ORG, 12, "start", "700")
    b += lbl(6, 20, "φ: từ Ox tới OM lúc t = 0", "currentColor", 12, "start", "700")
    return fig("d5-2", VB, "Đĩa tròn tâm O với điểm M ở vị trí lúc t bằng 0, góc φ tính từ trục Ox tới bán kính OM", b,
               "Dữ kiện: A = R; φ là góc từ Ox tới OM lúc t = 0, đo ngược chiều kim đồng hồ. " + NOTE)


BUILD = [d1, d2, d3, d4, d5]

# ───────────────────────────── 5 dạng, xếp dễ → kết hợp ─────────────────────────────
DANG = [
 dict(label="Dạng 1 · Dễ · Đọc phương trình dao động điều hoà: biên độ, tần số góc, pha ban đầu, chu kì, li độ",
      topic="Li độ, biên độ, chu kì, tần số, pha ban đầu",
      problem_html=r'<p>Một vật dao động điều hoà theo phương trình $x=10\cos\left(4\pi t+\dfrac{2\pi}{3}\right)$, với $x$ tính bằng cm, $t$ tính bằng giây.</p>'
                   r'<ol type="a"><li>Xác định biên độ, tần số góc và pha ban đầu.</li><li>Tính chu kì và tần số.</li><li>Tính pha của dao động và li độ của vật lúc $t=0{,}25$ s.</li></ol>'),
 dict(label="Dạng 2 · Trung bình · Phương trình có dấu trừ trước côsin: đưa về biên độ dương, tìm pha ban đầu",
      topic="Li độ, biên độ, chu kì, tần số, pha ban đầu",
      problem_html=r'<p>Một vật dao động điều hoà theo phương trình $x=-6\cos\left(5\pi t-\dfrac{\pi}{3}\right)$, với $x$ tính bằng cm, $t$ tính bằng giây.</p>'
                   r'<ol type="a"><li>Biên độ của dao động bằng bao nhiêu?</li><li>Viết lại phương trình dưới dạng $x=A\cos(\omega t+\varphi)$ với $A\gt0$ và $-\pi\lt\varphi\le\pi$. Nêu pha ban đầu.</li><li>Tính li độ của vật lúc $t=0$ và lúc $t=0{,}2$ s.</li></ol>'),
 dict(label="Dạng 3 · Trung bình · Đọc đồ thị li độ – thời gian: biên độ, chu kì, tần số góc, pha ban đầu, phương trình",
      topic="Đọc đồ thị li độ – thời gian",
      problem_html=r'<p>Hình vẽ là đồ thị li độ $x$ (cm) theo thời gian $t$ (s) của một vật dao động điều hoà.</p>'
                   r'<ol type="a"><li>Đọc biên độ $A$ và chu kì $T$.</li><li>Tính tần số góc $\omega$.</li><li>Xác định pha ban đầu $\varphi$ (với $0\le\varphi\le\pi$) và viết phương trình dao động.</li></ol>'),
 dict(label="Dạng 4 · Khó · Viết phương trình từ chiều dài quỹ đạo, số dao động và gốc thời gian ở biên",
      topic="Viết phương trình dao động điều hoà",
      problem_html=r'<p>Một vật dao động điều hoà trên một đoạn thẳng dài $16$ cm. Trong $20$ s vật thực hiện $30$ dao động toàn phần. Chọn gốc toạ độ O ở vị trí cân bằng, chiều dương Ox hướng sang phải, gốc thời gian ($t=0$) lúc vật ở biên âm (hình vẽ).</p>'
                   r'<ol type="a"><li>Tìm biên độ và chu kì.</li><li>Tính tần số góc và viết phương trình dao động.</li><li>Tính li độ của vật lúc $t=\dfrac{1}{3}$ s.</li></ol>'),
 dict(label="Dạng 5 · Khó · Hình chiếu của chuyển động tròn đều: đĩa quay theo vòng/phút, viết phương trình của hình chiếu",
      topic="Viết phương trình dao động điều hoà",
      problem_html=r'<p>Một đĩa tròn bán kính $R=12$ cm quay đều quanh tâm O với tốc độ $150$ vòng/phút, ngược chiều kim đồng hồ. Điểm M ở mép đĩa; Q là hình chiếu của M lên trục Ox nằm ngang đi qua O (chiều dương sang phải). Lúc $t=0$, M ở điểm cao nhất của mép đĩa.</p>'
                   r'<ol type="a"><li>Đổi tốc độ quay ra rad/s. Q dao động điều hoà với biên độ và tần số góc bằng bao nhiêu?</li><li>Xác định pha ban đầu và viết phương trình dao động của Q.</li><li>Tính li độ của Q lúc $t=\dfrac{1}{30}$ s.</li></ol>'),
]

# ───────────────────────────── Bảng phân tích đề (không ghi đáp số) ─────────────────────────────
ANALYSIS = [
 [(r'"dao động điều hoà theo phương trình $x=10\cos(4\pi t+\frac{2\pi}{3})$"', r'Phương trình có số cụ thể; $x$ tính bằng cm, $t$ bằng s', r'Đối chiếu với $x=A\cos(\omega t+\varphi)$: $A$ đứng ngoài, $\omega$ nhân với $t$, $\varphi$ cộng riêng'),
  (r'"biên độ, tần số góc, pha ban đầu"', r'Cần $A$, $\omega$, $\varphi$', r'Đọc trực tiếp từ phương trình'),
  (r'ngầm: góc trong côsin', r'Đơn vị của $\omega t+\varphi$ là rad', r'⚠ Điều kiện: pha tính bằng rad (máy tính ở chế độ radian); $A\gt0$'),
  (r'"chu kì và tần số"', r'Cần $T$, $f$', r'$T=\dfrac{2\pi}{\omega}$ · $f=\dfrac{1}{T}$'),
  (r'"pha của dao động ... lúc $t=0{,}25$ s"', r'$t=0{,}25$ s', r'Pha $=\omega t+\varphi$'),
  (r'"li độ của vật lúc $t=0{,}25$ s"', r'Cần $x$', r'$x=A\cos(\text{pha})$')],
 [(r'"$x=-6\cos(5\pi t-\frac{\pi}{3})$"', r'Có dấu trừ đứng trước côsin', r'Dạng chuẩn $x=A\cos(\omega t+\varphi)$ đòi $A\gt0$'),
  (r'"viết lại ... với $A\gt0$ và $-\pi\lt\varphi\le\pi$"', r'Yêu cầu $A\gt0$; $-\pi\lt\varphi\le\pi$', r'⚠ Điều kiện: $A\gt0$, nên dấu trừ phải chuyển vào pha nhờ $-\cos\alpha=\cos(\alpha+\pi)$'),
  (r'"biên độ"', r'Cần $A$', r'$A$ là giá trị lớn nhất của li độ, luôn dương'),
  (r'"pha ban đầu"', r'Cần $\varphi$', r'Cộng $\pi$ vào pha hiện có rồi đưa về khoảng cho phép'),
  (r'"li độ ... lúc $t=0$ và $t=0{,}2$ s"', r'$t=0$; $t=0{,}2$ s', r'Thế $t$ vào phương trình (dạng gốc hay dạng chuẩn đều được); máy tính ở chế độ radian')],
 [(r'"đồ thị li độ $x$ (cm) theo thời gian $t$ (s)"', r'Đường hình sin; trục $x$ (cm), trục $t$ (s)', r'Đồ thị li độ – thời gian của dao động điều hoà là đường hình sin'),
  (r'ngầm: $T$ là khoảng cách giữa hai điểm cùng trạng thái', r'Hai đỉnh liên tiếp (hoặc hai đáy liên tiếp)', r'⚠ Điều kiện: $T$ là một chu kì đầy đủ; không lấy từ $t=0$ tới đỉnh đầu tiên khi đồ thị chưa xuất phát từ đỉnh'),
  (r'"biên độ $A$"', r'Cần $A$', r'Khoảng từ trục $t$ tới đỉnh'),
  (r'"chu kì $T$"', r'Cần $T$', r'Khoảng thời gian giữa hai đỉnh liên tiếp'),
  (r'"tần số góc $\omega$"', r'Cần $\omega$', r'$\omega=\dfrac{2\pi}{T}$'),
  (r'"pha ban đầu $\varphi$ ... viết phương trình"', r'Li độ lúc $t=0$ đọc trên đồ thị; $0\le\varphi\le\pi$', r'$x(0)=A\cos\varphi$ để tìm $\varphi$; rồi $x=A\cos(\omega t+\varphi)$')],
 [(r'"đoạn thẳng dài $16$ cm"', r'Chiều dài quỹ đạo $L=16$ cm', r'Vật đi từ $-A$ tới $+A$ nên $L=2A$'),
  (r'"gốc toạ độ O ở vị trí cân bằng"', r'O trùng vị trí cân bằng', r'⚠ Điều kiện: $x=A\cos(\omega t+\varphi)$ chỉ dùng khi gốc toạ độ ở vị trí cân bằng'),
  (r'"$30$ dao động toàn phần trong $20$ s"', r'$N=30$; $t=20$ s', r'Một dao động toàn phần $=$ một chu kì: $T=\dfrac{t}{N}$ · $\omega=\dfrac{2\pi}{T}$'),
  (r'"gốc thời gian lúc vật ở biên âm"', r'$x(0)=-A$', r'$x(0)=A\cos\varphi$ để tìm $\varphi$'),
  (r'"viết phương trình"', r'Cần $A$, $\omega$, $\varphi$', r'$x=A\cos(\omega t+\varphi)$'),
  (r'"li độ lúc $t=\frac{1}{3}$ s"', r'$t=\dfrac{1}{3}$ s', r'Thế $t$ vào phương trình vừa viết')],
 [(r'"đĩa bán kính $R=12$ cm quay đều, $150$ vòng/phút"', r'$R=12$ cm; $n=150$ vòng/phút', r'Chuyển động tròn đều: tốc độ góc $\omega$ tính bằng rad/s'),
  (r'ngầm: đơn vị của tốc độ quay', r'$1$ vòng $=2\pi$ rad; $1$ phút $=60$ s', r'⚠ Điều kiện: đổi vòng/phút ra rad/s trước khi dùng trong phương trình'),
  (r'"Q là hình chiếu của M lên trục Ox"', r'Q dao động điều hoà', r'Hình chiếu của chuyển động tròn đều: bán kính $=A$, tốc độ góc $=\omega$'),
  (r'"lúc $t=0$, M ở điểm cao nhất"', r'Vị trí của M lúc đầu', r'$\varphi$ là góc từ trục $Ox$ tới $OM$ lúc $t=0$ (ngược chiều kim đồng hồ)'),
  (r'"viết phương trình dao động của Q"', r'Cần $A$, $\omega$, $\varphi$', r'$x=A\cos(\omega t+\varphi)$'),
  (r'"li độ của Q lúc $t=\frac{1}{30}$ s"', r'$t=\dfrac{1}{30}$ s', r'Thế $t$ vào phương trình')],
]

# ───────────────────────────── Lời giải ─────────────────────────────
R1 = [r'<strong>Khái niệm:</strong> dao động điều hoà có li độ $x$ biến thiên theo hàm côsin của thời gian.',
      r'<strong>Phương trình:</strong> $x=A\cos(\omega t+\varphi)$ · $A\gt0$ (cm) · $\omega$ (rad/s)',
      r'Pha $=\omega t+\varphi$ · pha ban đầu $\varphi$ là pha lúc $t=0$',
      r'$T=\dfrac{2\pi}{\omega}$ (một vòng quay đều ứng với $2\pi$ rad) · $f=\dfrac{1}{T}$',
      r'⚠ <strong>Điều kiện:</strong> pha tính bằng rad; máy tính ở chế độ radian.']
R2 = [r'<strong>Khái niệm:</strong> dạng chuẩn $x=A\cos(\omega t+\varphi)$ đòi biên độ $A\gt0$.',
      r'<strong>Công thức:</strong> $-\cos\alpha=\cos(\alpha+\pi)$',
      r'Pha $=\omega t+\varphi$ · $x=A\cos(\text{pha})$',
      r'Chọn $\varphi$ trong khoảng $-\pi\lt\varphi\le\pi$ (cộng hoặc trừ $2\pi$ nếu cần).',
      r'⚠ <strong>Điều kiện:</strong> $A$ luôn dương; pha tính bằng rad.']
R3 = [r'<strong>Khái niệm:</strong> đồ thị li độ – thời gian là đường hình sin.',
      r'$A$: từ trục $t$ tới đỉnh · $T$: khoảng thời gian giữa hai đỉnh liên tiếp',
      r'$\omega=\dfrac{2\pi}{T}$ · $x(0)=A\cos\varphi$ (li độ lúc $t=0$)',
      r'$x=A\cos(\omega t+\varphi)$',
      r'⚠ <strong>Điều kiện:</strong> $T$ là một chu kì đầy đủ, không phải nửa chu kì.']
R4 = [r'<strong>Khái niệm:</strong> quỹ đạo là đoạn thẳng từ $-A$ tới $+A$, nên $L=2A$.',
      r'<strong>Công thức:</strong> $T=\dfrac{t}{N}$ ($N$ dao động toàn phần trong $t$ giây) · $\omega=\dfrac{2\pi}{T}$',
      r'$x(0)=A\cos\varphi$: vị trí lúc $t=0$ cho biết $\varphi$.',
      r'$x=A\cos(\omega t+\varphi)$',
      r'⚠ <strong>Điều kiện:</strong> gốc toạ độ O ở vị trí cân bằng; pha tính bằng rad.']
R5 = [r'<strong>Khái niệm:</strong> hình chiếu của chuyển động tròn đều lên một đường kính là dao động điều hoà.',
      r'Bán kính $R=A$ · tốc độ góc của M $=\omega$ của Q',
      r'$\varphi$ là góc từ trục $Ox$ tới $OM$ lúc $t=0$ (đo ngược chiều kim đồng hồ).',
      r'$1$ vòng $=2\pi$ rad · $1$ phút $=60$ s · $x=A\cos(\omega t+\varphi)$',
      r'⚠ <strong>Điều kiện:</strong> đĩa quay đều; đổi tốc độ quay ra rad/s.']

SOLS = [
 sol(R1, [
  ("Đối chiếu với dạng chuẩn", [P(r"So với $x=A\cos(\omega t+\varphi)$:"), M(r"A=10\ \text{cm}"), M(r"\omega=4\pi\ \text{rad/s}\approx12{,}57\ \text{rad/s}"), A(r"\varphi=\dfrac{2\pi}{3}\ \text{rad}\approx2{,}094\ \text{rad}")]),
  ("Chu kì và tần số", [M(r"T=\dfrac{2\pi}{\omega}=\dfrac{2\pi}{4\pi}"), A(r"T=0{,}5\ \text{s}"), M(r"f=\dfrac{1}{T}=\dfrac{1}{0{,}5}"), A(r"f=2\ \text{Hz}")]),
  ("Pha lúc t = 0,25 s", [P(r"Pha $=\omega t+\varphi$:"), M(r"4\pi\cdot0{,}25+\dfrac{2\pi}{3}=\pi+\dfrac{2\pi}{3}"), A(r"\text{pha}=\dfrac{5\pi}{3}\ \text{rad}\approx5{,}236\ \text{rad}")]),
  ("Li độ lúc t = 0,25 s", [M(r"x=10\cos\dfrac{5\pi}{3}=10\cdot\dfrac{1}{2}"), A(r"x=5\ \text{cm}")]),
  ("Kiểm tra", [P(r"$|x|=5\le A=10$ cm ✓"), P(r"$\cos\dfrac{5\pi}{3}=\cos\left(-\dfrac{\pi}{3}\right)=\dfrac{1}{2}$ ✓")])],
  [r"a) $A=10$ cm; $\omega=4\pi$ rad/s; $\varphi=\dfrac{2\pi}{3}$ rad", r"b) $T=0{,}5$ s; $f=2$ Hz", r"c) pha $=\dfrac{5\pi}{3}$ rad; $x=5$ cm"],
  "Nhận dạng: đề cho <strong>phương trình có số cụ thể</strong> → đối chiếu từng ký hiệu với $x=A\\cos(\\omega t+\\varphi)$, rồi $T=\\dfrac{2\\pi}{\\omega}$."),
 sol(R2, [
  ("Biên độ", [P("Biên độ là giá trị lớn nhất của li độ nên luôn dương; dấu trừ thuộc về pha."), A(r"A=6\ \text{cm}")]),
  ("Đưa dấu trừ vào pha", [P(r"Dùng $-\cos\alpha=\cos(\alpha+\pi)$ với $\alpha=5\pi t-\dfrac{\pi}{3}$:"),
                           M(r"x=-6\cos\left(5\pi t-\dfrac{\pi}{3}\right)=6\cos\left(5\pi t-\dfrac{\pi}{3}+\pi\right)"),
                           M(r"x=6\cos\left(5\pi t+\dfrac{2\pi}{3}\right)\ \text{cm}"), A(r"\varphi=\dfrac{2\pi}{3}\ \text{rad}")]),
  ("Li độ lúc t = 0", [M(r"x(0)=6\cos\dfrac{2\pi}{3}=6\cdot\left(-\dfrac{1}{2}\right)"), A(r"x(0)=-3\ \text{cm}")]),
  ("Li độ lúc t = 0,2 s", [M(r"\text{pha}=5\pi\cdot0{,}2+\dfrac{2\pi}{3}=\pi+\dfrac{2\pi}{3}=\dfrac{5\pi}{3}"), M(r"x=6\cos\dfrac{5\pi}{3}=6\cdot\dfrac{1}{2}"), A(r"x=3\ \text{cm}")]),
  ("Kiểm tra", [P(r"Dạng gốc, $t=0$: $-6\cos\left(-\dfrac{\pi}{3}\right)=-6\cdot\dfrac{1}{2}=-3$ cm ✓"), P(r"Dạng gốc, $t=0{,}2$ s: pha $=\dfrac{2\pi}{3}$, $-6\cos\dfrac{2\pi}{3}=3$ cm ✓")])],
  [r"a) $A=6$ cm", r"b) $x=6\cos\left(5\pi t+\dfrac{2\pi}{3}\right)$ cm; $\varphi=\dfrac{2\pi}{3}$ rad", r"c) $x(0)=-3$ cm; $x(0{,}2)=3$ cm"],
  "Nhận dạng: thấy <strong>dấu trừ đứng trước côsin</strong> → đưa vào pha bằng $-\\cos\\alpha=\\cos(\\alpha+\\pi)$ để có $A\\gt0$."),
 sol(R3, [
  ("Biên độ", [P(r"Đỉnh cao nhất cách trục $t$ bốn ô của trục $x$."), A(r"A=4\ \text{cm}")]),
  ("Chu kì", [P(r"Hai đỉnh liên tiếp ở $t=0{,}5$ s và $t=1{,}5$ s:"), M(r"T=1{,}5-0{,}5"), A(r"T=1\ \text{s}"),
              P(r"Đồ thị xuất phát từ đáy nên từ $t=0$ tới đỉnh đầu tiên ($0{,}5$ s) chỉ là nửa chu kì.")]),
  ("Tần số góc", [M(r"\omega=\dfrac{2\pi}{T}=\dfrac{2\pi}{1}"), A(r"\omega=2\pi\ \text{rad/s}\approx6{,}283\ \text{rad/s}")]),
  ("Pha ban đầu", [P(r"Lúc $t=0$ đồ thị ở đáy: $x(0)=-4$ cm."), M(r"x(0)=A\cos\varphi\ \Rightarrow\ \cos\varphi=\dfrac{-4}{4}=-1"), A(r"\varphi=\pi\ \text{rad}")]),
  ("Viết phương trình", [M(r"x=A\cos(\omega t+\varphi)"), A(r"x=4\cos(2\pi t+\pi)\ \text{cm}")]),
  ("Kiểm tra", [P(r"$t=0{,}5$ s: pha $=2\pi\cdot0{,}5+\pi=2\pi$, $x=4\cos2\pi=4$ cm, đúng đỉnh đầu tiên ✓"), P(r"$t=1$ s: pha $=3\pi$, $x=4\cos3\pi=-4$ cm, đúng đáy thứ hai ✓")])],
  [r"a) $A=4$ cm; $T=1$ s", r"b) $\omega=2\pi$ rad/s", r"c) $\varphi=\pi$ rad; $x=4\cos(2\pi t+\pi)$ cm"],
  "Nhận dạng: thấy <strong>đồ thị li độ – thời gian</strong> → $A$ từ đỉnh, $T$ giữa hai đỉnh liên tiếp, $\\varphi$ từ li độ lúc $t=0$."),
 sol(R4, [
  ("Biên độ", [M(r"L=2A\ \Rightarrow\ A=\dfrac{L}{2}=\dfrac{16}{2}"), A(r"A=8\ \text{cm}")]),
  ("Chu kì", [M(r"T=\dfrac{t}{N}=\dfrac{20}{30}"), A(r"T=\dfrac{2}{3}\ \text{s}\approx0{,}667\ \text{s}")]),
  ("Tần số góc", [M(r"\omega=\dfrac{2\pi}{T}=\dfrac{2\pi}{2/3}"), A(r"\omega=3\pi\ \text{rad/s}\approx9{,}425\ \text{rad/s}")]),
  ("Pha ban đầu và phương trình", [P(r"Lúc $t=0$ vật ở biên âm: $x(0)=-A$."), M(r"A\cos\varphi=-A\ \Rightarrow\ \cos\varphi=-1"), A(r"\varphi=\pi\ \text{rad}"), M(r"x=8\cos(3\pi t+\pi)\ \text{cm}")]),
  ("Li độ lúc t = 1/3 s", [M(r"\text{pha}=3\pi\cdot\dfrac{1}{3}+\pi=2\pi"), M(r"x=8\cos2\pi"), A(r"x=8\ \text{cm}")]),
  ("Kiểm tra", [P(r"$t=\dfrac{1}{3}$ s $=\dfrac{T}{2}$: sau nửa chu kì vật sang biên đối diện, $x=+A=8$ cm ✓")])],
  [r"a) $A=8$ cm; $T=\dfrac{2}{3}$ s", r"b) $\omega=3\pi$ rad/s; $x=8\cos(3\pi t+\pi)$ cm", r"c) $x=8$ cm"],
  "Nhận dạng: thấy <strong>chiều dài quỹ đạo</strong> và <strong>số dao động trong một khoảng thời gian</strong> → $A=\\dfrac{L}{2}$, $T=\\dfrac{t}{N}$, $\\varphi$ từ vị trí lúc $t=0$."),
 sol(R5, [
  ("Đổi tốc độ quay ra rad/s", [P(r"$150$ vòng/phút $=\dfrac{150}{60}=2{,}5$ vòng/s."), M(r"\omega=2\pi\cdot2{,}5"), A(r"\omega=5\pi\ \text{rad/s}\approx15{,}71\ \text{rad/s}")]),
  ("Biên độ", [P(r"Q chạy từ $-R$ tới $+R$ trên đường kính."), A(r"A=R=12\ \text{cm}")]),
  ("Pha ban đầu", [P(r"Lúc $t=0$, M ở điểm cao nhất nên $OM$ vuông góc với $Ox$, hướng lên."), A(r"\varphi=\dfrac{\pi}{2}\ \text{rad}")]),
  ("Viết phương trình", [M(r"x=A\cos(\omega t+\varphi)"), A(r"x=12\cos\left(5\pi t+\dfrac{\pi}{2}\right)\ \text{cm}")]),
  ("Li độ lúc t = 1/30 s", [M(r"\text{pha}=5\pi\cdot\dfrac{1}{30}+\dfrac{\pi}{2}=\dfrac{\pi}{6}+\dfrac{\pi}{2}=\dfrac{2\pi}{3}"), M(r"x=12\cos\dfrac{2\pi}{3}=12\cdot\left(-\dfrac{1}{2}\right)"), A(r"x=-6\ \text{cm}")]),
  ("Kiểm tra", [P(r"Sau $\dfrac{1}{30}$ s, M quay thêm $\dfrac{\pi}{6}=30^\circ$ từ điểm cao nhất sang trái, nên $OM$ hợp $Ox$ góc $120^\circ$."), P(r"Q nằm bên trái O: $x\lt0$ ✓; $|x|=12\cos60^\circ=6$ cm ✓")])],
  [r"a) $\omega=5\pi$ rad/s; $A=12$ cm", r"b) $\varphi=\dfrac{\pi}{2}$ rad; $x=12\cos\left(5\pi t+\dfrac{\pi}{2}\right)$ cm", r"c) $x=-6$ cm"],
  "Nhận dạng: thấy <strong>vật quay đều và hình chiếu lên một đường thẳng</strong> → $A=R$, $\\omega$ là tốc độ góc (rad/s), $\\varphi$ là góc ban đầu của $OM$."),
]

# ───────────────────────────── Tự giải từng bước ─────────────────────────────
STEPS = [
 dict(nhan_dang=r"Thấy <b>phương trình có số cụ thể</b> → đối chiếu từng ký hiệu với $x=A\cos(\omega t+\varphi)$, rồi $T=\dfrac{2\pi}{\omega}$.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Đối chiếu với dạng chuẩn", "Pha ban đầu φ của dao động bằng bao nhiêu rad?", 2.094, "rad", 0.02,
       loi=r"Nhầm $\varphi$ với hệ số đứng trước $t$ (đó là $\omega$); $\varphi$ là số hạng cộng riêng, không nhân với $t$."),
  buoc("Chu kì và tần số", "Chu kì T của dao động bằng bao nhiêu giây?", 0.5, "s", 0.01,
       loi=r"Lấy $T=\omega$ hoặc $T=\dfrac{\omega}{2\pi}$ (đó là tần số $f$); phải lấy $T=\dfrac{2\pi}{\omega}$.",
       ke=[(r"$T=\dfrac{2\pi}{\omega}$ vì một vòng ứng với $2\pi$ rad", True),
           (r"$T=\dfrac{\omega}{2\pi}$", "Đó là tần số $f$ (số dao động mỗi giây), không phải chu kì."),
           (r"$T=2\pi\omega$", "Đơn vị không ra giây: $T$ phải giảm khi $\\omega$ tăng, còn tích $2\\pi\\omega$ lại tăng theo $\\omega$.")]),
  buoc("Pha lúc t = 0,25 s", "Pha của dao động lúc t = 0,25 s bằng bao nhiêu rad?", 5.236, "rad", 0.02,
       loi=r"Lấy pha $=\varphi$ (đó chỉ là pha lúc $t=0$) hoặc nhân $\varphi$ với $t$; pha $=\omega t+\varphi$.",
       ke=[(r"pha $=\omega t+\varphi$ với $t=0{,}25$ s", True),
           (r"pha $=\varphi$ vì đó là pha của dao động", r"$\varphi$ chỉ là pha lúc $t=0$; ở thời điểm khác pha là $\omega t+\varphi$."),
           (r"pha $=\omega+\varphi t$", r"Nhầm vị trí: $t$ nhân với $\omega$, không nhân với $\varphi$.")]),
  buoc("Li độ lúc t = 0,25 s", "Li độ của vật lúc đó bằng bao nhiêu cm?", 5, "cm", 0.1,
       loi=r"Để máy tính ở chế độ độ (DEG) nên $\cos$ của số rad cho giá trị khác; phải chuyển sang chế độ radian.",
       ke=[(r"thay pha vừa tìm vào $x=A\cos(\text{pha})$", True),
           (r"thay $t=0{,}25$ vào $x=A\cos t$", r"Cung của côsin là pha $\omega t+\varphi$, không phải riêng $t$."),
           (r"lấy $x=A\cdot$ pha", r"Li độ là $A$ nhân với $\cos(\text{pha})$, không nhân với chính pha.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>dấu trừ đứng trước côsin</b> → đưa vào pha bằng $-\cos\alpha=\cos(\alpha+\pi)$ để có $A\gt0$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Biên độ", "Biên độ A của dao động bằng bao nhiêu cm?", 6, "cm", 0,
       loi=r"Đọc $A=-6$ vì thấy dấu trừ; biên độ là giá trị lớn nhất của li độ nên luôn dương, dấu trừ thuộc về pha."),
  buoc("Đưa dấu trừ vào pha", "Pha ban đầu φ (trong khoảng −π < φ ≤ π) của dao động là:",
       lua_chon=[(r"$\dfrac{2\pi}{3}$ rad", True),
                 (r"$-\dfrac{\pi}{3}$ rad", r"Giữ nguyên pha thì dấu trừ ngoài cùng vẫn còn, chưa đưa về $A\gt0$."),
                 (r"$\dfrac{\pi}{3}$ rad", r"Đổi dấu pha không bỏ được dấu trừ: $\cos$ là hàm chẵn nên $\cos(-\alpha)=\cos\alpha$.")],
       loi=r"Chỉ bỏ dấu trừ ngoài cùng mà không cộng $\pi$ vào pha nên đổi nghĩa phương trình.",
       ke=[(r"dùng $-\cos\alpha=\cos(\alpha+\pi)$ để đưa dấu trừ vào pha", True),
           (r"bỏ dấu trừ vì biên độ phải dương", r"Bỏ dấu trừ làm li độ đổi dấu ở mọi thời điểm, tức là một dao động khác."),
           (r"đổi $\cos$ thành $\sin$", r"Đổi hàm làm đổi pha theo cách khác và đề yêu cầu dạng côsin.")]),
  buoc("Li độ lúc t = 0", "Li độ của vật lúc t = 0 bằng bao nhiêu cm?", -3, "cm", 0.1,
       loi=r"Bỏ sót dấu trừ đứng trước $\cos$ hoặc tính sai dấu của $\cos$ nên ra kết quả ngược dấu.",
       ke=[(r"thay $t=0$ vào pha rồi lấy $A\cos(\text{pha})$", True),
           (r"lấy $x=A$ vì $t=0$ là lúc bắt đầu", r"Lúc $t=0$ vật chưa chắc ở biên; li độ phụ thuộc $\varphi$."),
           (r"lấy $x=0$ vì $t=0$", r"$t=0$ không có nghĩa là $x=0$; $x(0)=A\cos\varphi$.")]),
  buoc("Li độ lúc t = 0,2 s", "Li độ của vật lúc t = 0,2 s bằng bao nhiêu cm?", 3, "cm", 0.1,
       loi=r"Thế $t=0{,}2$ nhưng quên nhân $5\pi$ (lấy pha $0{,}2-\dfrac{\pi}{3}$), hoặc để máy ở chế độ độ.",
       ke=[(r"thay $t$ vào pha rồi lấy $A\cos(\text{pha})$ theo dạng chuẩn", True),
           (r"thay $t$ vào dạng chuẩn rồi nhân thêm dấu trừ lần nữa", r"Dạng chuẩn đã chứa dấu trừ trong pha; nhân thêm sẽ đảo dấu hai lần."),
           (r"lấy $x=-A$ vì có dấu trừ", r"Dấu trừ không giữ vật ở phía âm; li độ đổi dấu theo giá trị của $\cos(\text{pha})$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>đồ thị li độ – thời gian</b> → $A$ từ đỉnh, $T$ giữa hai đỉnh liên tiếp, $\varphi$ từ li độ lúc $t=0$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Biên độ", "Biên độ A đọc trên đồ thị bằng bao nhiêu cm?", 4, "cm", 0,
       loi=r"Đọc khoảng cách từ đỉnh tới đáy (gấp đôi biên độ) hoặc lấy giá trị âm ở đáy; biên độ là khoảng từ trục $t$ tới đỉnh."),
  buoc("Chu kì", "Chu kì T đọc trên đồ thị bằng bao nhiêu giây?", 1, "s", 0.02,
       loi=r"Lấy thời gian từ $t=0$ tới đỉnh đầu tiên; đồ thị xuất phát từ đáy nên đó chỉ là nửa chu kì.",
       ke=[("T là khoảng thời gian giữa hai đỉnh liên tiếp", True),
           (r"T là thời gian từ $t=0$ tới đỉnh đầu tiên", "Đồ thị xuất phát từ đáy, nên đoạn đó mới là nửa chu kì."),
           (r"T là giá trị lớn nhất của $t$ trên trục", "Đồ thị vẽ nhiều dao động; cả trục thời gian dài gấp nhiều lần chu kì.")]),
  buoc("Tần số góc", "Tần số góc ω bằng bao nhiêu rad/s?", 6.283, "rad/s", 0.05,
       loi=r"Dùng $\omega=\dfrac{1}{T}$ (đó là tần số $f$) hoặc quên nhân $2\pi$.",
       ke=[(r"$\omega=\dfrac{2\pi}{T}$", True),
           (r"$\omega=\dfrac{1}{T}$", r"Đó là tần số $f$; tần số góc là $\omega=2\pi f$."),
           (r"$\omega=\dfrac{T}{2\pi}$", r"Ngược: chu kì càng ngắn thì $\omega$ càng lớn, mà công thức này làm $\omega$ nhỏ đi.")]),
  buoc("Pha ban đầu", "Pha ban đầu φ (0 ≤ φ ≤ π) của dao động là:",
       lua_chon=[(r"$\pi$ rad", True),
                 (r"$0$ rad", r"Với $\varphi=0$: $x(0)=A\cos0=+A$, vật ở biên dương; đồ thị này xuất phát ở phía âm."),
                 (r"$\dfrac{\pi}{2}$ rad", r"Với $\varphi=\dfrac{\pi}{2}$: $x(0)=A\cos\dfrac{\pi}{2}=0$, đồ thị phải xuất phát từ trục $t$.")],
       loi=r"Chọn $\varphi$ không khớp li độ lúc $t=0$ đọc trên đồ thị; lập $x(0)=A\cos\varphi$ rồi so với điểm xuất phát.",
       ke=[(r"dùng $x(0)=A\cos\varphi$ và giá trị $x$ tại $t=0$ đọc trên đồ thị", True),
           (r"lấy $\varphi$ bằng góc của đường cong với trục $t$", r"$\varphi$ không phải góc hình học của đường cong; nó là pha tại $t=0$."),
           (r"lấy $\varphi=0$ vì đồ thị là đường hình sin", r"Đồ thị vẫn là đường hình sin dù $\varphi\ne0$; $\varphi$ phụ thuộc điểm xuất phát.")]),
  buoc("Viết phương trình", "Phương trình dao động là:",
       lua_chon=[(r"$x=4\cos(2\pi t+\pi)$ cm", True),
                 (r"$x=4\cos(\pi t+\pi)$ cm", r"Hệ số của $t$ phải là $\omega=\dfrac{2\pi}{T}$, không phải một nửa của nó."),
                 (r"$x=4\cos(2\pi t)$ cm", r"Thiếu pha ban đầu: phương trình này cho $x(0)=+4$ cm, còn đồ thị xuất phát ở phía âm.")],
       loi=r"Ghép sai $A$, $\omega$, $\varphi$ vào $x=A\cos(\omega t+\varphi)$: bỏ sót $\varphi$ hoặc thế $\omega$ nhầm.",
       ke=[(r"thế $A$, $\omega$, $\varphi$ vừa tìm vào $x=A\cos(\omega t+\varphi)$", True),
           (r"viết $x=A\sin(\omega t+\varphi)$ với cùng $\varphi$ vì đồ thị hình sin", r"$\varphi$ ở trên tìm theo côsin; thế vào hàm sin cho $x(0)=A\sin\pi=0$, sai với đồ thị."),
           (r"viết $x=A\cos(\omega t)+\varphi$", r"$\varphi$ nằm trong pha (cùng với $\omega t$), không cộng vào cả li độ.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>chiều dài quỹ đạo</b> và <b>số dao động trong một khoảng thời gian</b> → $A=\dfrac{L}{2}$, $T=\dfrac{t}{N}$, $\varphi$ từ vị trí lúc $t=0$.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Biên độ", "Biên độ A của dao động bằng bao nhiêu cm?", 8, "cm", 0,
       loi=r"Lấy $A$ bằng cả chiều dài quỹ đạo; vật đi từ $-A$ tới $+A$ nên quỹ đạo dài gấp đôi biên độ."),
  buoc("Chu kì", "Chu kì T của dao động bằng bao nhiêu giây?", 0.667, "s", 0.005,
       loi=r"Chia ngược (số dao động chia cho thời gian) ra tần số rồi coi là chu kì.",
       ke=[("T bằng thời gian chia cho số dao động", True),
           ("T bằng số dao động chia cho thời gian", "Đó là tần số f (dao động mỗi giây), không phải chu kì."),
           ("T bằng thời gian nhân với số dao động", "Tích này lớn hơn cả thời gian đo; một dao động không thể dài hơn toàn bộ thời gian đo.")]),
  buoc("Tần số góc", "Tần số góc ω bằng bao nhiêu rad/s?", 9.425, "rad/s", 0.05,
       loi=r"Dùng $\omega=\dfrac{1}{T}$ hoặc $\omega=\dfrac{2\pi}{20}$ (lấy cả thời gian đo thay vì một chu kì).",
       ke=[(r"$\omega=\dfrac{2\pi}{T}$ với $T$ vừa tìm", True),
           (r"$\omega=\dfrac{1}{T}$", r"Đó là tần số $f$ (Hz); $\omega$ còn phải nhân với $2\pi$."),
           (r"$\omega=\dfrac{2\pi}{N}$ với $N=30$", r"$N$ là số dao động trong cả $20$ s, không phải thời gian của một dao động.")]),
  buoc("Pha ban đầu và phương trình", "Gốc thời gian lúc vật ở biên âm. Pha ban đầu φ (0 ≤ φ ≤ π) là:",
       lua_chon=[(r"$\pi$ rad", True),
                 (r"$0$ rad", r"Với $\varphi=0$ thì $x(0)=+A$, vật ở biên dương, ngược với đề."),
                 (r"$\dfrac{\pi}{2}$ rad", r"Với $\varphi=\dfrac{\pi}{2}$ thì $x(0)=0$, vật ở vị trí cân bằng, không phải biên âm.")],
       loi=r"Lấy $\varphi=0$ vì $t=0$; pha ban đầu không tự bằng $0$, nó phụ thuộc vị trí xuất phát.",
       ke=[(r"giải $x(0)=A\cos\varphi=-A$ để tìm $\varphi$", True),
           (r"lấy $\varphi=0$ vì $t=0$", r"Pha ban đầu không tự bằng $0$: nó là pha lúc $t=0$ và phụ thuộc vị trí xuất phát."),
           (r"chọn $\varphi$ sao cho $x(0)=+A$ vì biên nào cũng viết $+A$", r"Biên âm có $x(0)=-A$, ứng với $\cos\varphi=-1$; đặt $+A$ là biên dương.")]),
  buoc("Li độ lúc t = 1/3 s", "Li độ của vật lúc t = 1/3 s bằng bao nhiêu cm?", 8, "cm", 0.1,
       loi=r"Bỏ $\varphi$ khỏi pha (lấy $x=8\cos3\pi t$), hoặc để máy ở chế độ độ.",
       ke=[(r"thay $t$ vào pha $3\pi t+\pi$ rồi lấy $A\cos(\text{pha})$", True),
           (r"dùng $x=A\cos(3\pi t)$ vì $\varphi$ chỉ là giá trị lúc đầu", r"$\varphi$ có mặt trong pha ở mọi thời điểm: pha $=\omega t+\varphi$."),
           (r"lấy $x=-A$ vì vật xuất phát từ biên âm", r"Vật chỉ ở biên âm lúc $t=0$; sau đó nó chuyển động nên li độ thay đổi.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>vật quay đều và hình chiếu lên một đường thẳng</b> → $A=R$, $\omega$ là tốc độ góc, $\varphi$ là góc ban đầu của $OM$.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Đổi tốc độ quay ra rad/s", "Tần số góc ω của Q (bằng tốc độ góc của M) bằng bao nhiêu rad/s?", 15.71, "rad/s", 0.05,
       loi=r"Quên đổi phút ra giây (chia $60$) hoặc quên nhân $2\pi$ cho mỗi vòng."),
  buoc("Biên độ", "Biên độ A của dao động của Q bằng bao nhiêu cm?", 12, "cm", 0,
       loi=r"Lấy $A$ bằng đường kính (đó là chiều dài quỹ đạo của Q) hoặc nhân bán kính với $\omega$.",
       ke=[(r"Q chạy từ $-R$ tới $+R$ nên $A=R$", True),
           (r"$A=2R$ vì Q đi hết đường kính", r"Đường kính là chiều dài quỹ đạo của Q; biên độ chỉ bằng nửa, tức $R$."),
           (r"$A=R\cdot\omega$", r"Tích $R\omega$ có đơn vị cm/s (tốc độ dài của M), không phải li độ cực đại.")]),
  buoc("Pha ban đầu", "Pha ban đầu φ của Q (−π < φ ≤ π) bằng:",
       lua_chon=[(r"$\dfrac{\pi}{2}$ rad", True),
                 (r"$0$ rad", r"$\varphi=0$ ứng với M ở bên phải O trên trục $Ox$, không phải điểm cao nhất."),
                 (r"$-\dfrac{\pi}{2}$ rad", r"Góc $-\dfrac{\pi}{2}$ ứng với M ở điểm thấp nhất, không phải điểm cao nhất.")],
       loi=r"Đo $\varphi$ từ phương thẳng đứng thay vì từ trục $Ox$, hoặc đo theo chiều kim đồng hồ.",
       ke=[(r"$\varphi$ là góc từ $Ox$ tới $OM$ lúc $t=0$, đo ngược chiều kim đồng hồ", True),
           (r"$\varphi$ là góc từ phương thẳng đứng tới $OM$", r"Góc $\varphi$ đo từ trục $Ox$ (nơi Q dao động), không đo từ phương thẳng đứng."),
           (r"$\varphi=0$ vì lúc $t=0$ đĩa mới bắt đầu quay", r"Pha ban đầu phụ thuộc vị trí của M lúc $t=0$, không tự bằng $0$.")]),
  buoc("Viết phương trình", "Phương trình dao động của Q là:",
       lua_chon=[(r"$x=12\cos\left(5\pi t+\dfrac{\pi}{2}\right)$ cm", True),
                 (r"$x=12\cos\left(150t+\dfrac{\pi}{2}\right)$ cm", r"$150$ là số vòng/phút; trong phương trình $\omega$ phải tính bằng rad/s."),
                 (r"$x=24\cos\left(5\pi t+\dfrac{\pi}{2}\right)$ cm", r"$24$ là đường kính; biên độ bằng bán kính.")],
       loi=r"Thế $\omega$ theo vòng/phút hoặc biên độ bằng đường kính khi ghép vào $x=A\cos(\omega t+\varphi)$.",
       ke=[(r"thế $A$, $\omega$, $\varphi$ vừa tìm vào $x=A\cos(\omega t+\varphi)$", True),
           (r"viết $x=R\cos(\omega t)$ vì M bắt đầu quay từ trục", r"M không bắt đầu từ trục $Ox$ mà từ điểm cao nhất, nên $\varphi\ne0$."),
           (r"viết $x=A\sin(\omega t)$ cho gọn", r"Với $\varphi=\dfrac{\pi}{2}$ thì $\cos\left(\omega t+\dfrac{\pi}{2}\right)=-\sin\omega t$, nên $A\sin\omega t$ ngược dấu li độ ở mọi thời điểm.")]),
  buoc("Li độ lúc t = 1/30 s", "Li độ của Q lúc t = 1/30 s bằng bao nhiêu cm?", -6, "cm", 0.1,
       loi=r"Bỏ $\varphi$ khỏi pha (lấy $x=12\cos5\pi t$) hoặc để máy ở chế độ độ.",
       ke=[(r"tính pha $5\pi t+\dfrac{\pi}{2}$ rồi lấy $A\cos(\text{pha})$", True),
           (r"lấy $x=A\cos(\omega t)$ vì $\varphi$ chỉ là góc lúc đầu", r"Pha luôn gồm cả $\varphi$: pha $=\omega t+\varphi$."),
           (r"lấy li độ bằng cung M đã quay được", r"Cung quay được đo trên đường tròn; li độ là hình chiếu của M lên $Ox$, phải lấy côsin.")]),
  buoc("Kiểm tra")]),
]

# ───────────────────────────── Ghi file ─────────────────────────────
write(J, 20, "Bài 1. Dao động điều hoà", DANG, BUILD, ANALYSIS, SOLS)
d = json.load(open(J))
d["generated_at"] = "2026-10-09"
d["review"] = {"checked": True, "notes": "Kiểm chéo độc lập 9/10/2026: 5 dạng giải lại bằng Python khớp đáp số và buoc[]; đã sửa nhãn y (dạng 2), lộ x(0)=-3 trên thước dạng 2, chữ chồng nhãn trục dạng 1, nhãn Q dạng 5, vi_sao hàm sin dạng 5, gợi dấu cos ở loi_hay_gap dạng 2."}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
