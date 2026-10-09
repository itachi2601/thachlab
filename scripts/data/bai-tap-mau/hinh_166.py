"""Hình + mô phỏng cho bài tạm 166 (Chuyên đề 02 · Động năng, thế năng, cơ năng) — HSG KHTN 9.
Mọi chuyển động TÍNH THẬT từ công thức (g = 10 m/s²), mẫu cách đều thời gian, nội suy tuyến tính (SMIL, chạy MỘT lần khi bấm).
Màu năng lượng: Wđ đỏ · Wt cam · nhiệt xanh lá. Không ghi đáp số lên hình."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

GR = 10.0          # g của chuyên đề (khác G = 9.8 trong hinh.py)
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
C_WD, C_WT, C_Q = RED, ORG, GRN


def ebar(x, y, w, h, series, dur):
    """Thanh năng lượng xếp chồng, các đoạn đổi độ dài theo thời gian. series = [(màu, [phần trăm tại từng mẫu])], tổng ≤ 1."""
    n = len(series[0][1]); cum = [0.0] * n; out = ""
    for col, fr in series:
        xs = [x + w * c for c in cum]; ws = [w * f for f in fr]
        out += (f'<rect x="{xs[0]:.1f}" y="{y}" width="{ws[0]:.1f}" height="{h}" fill="{col}" opacity="0.9">'
                f'{smil("x", xs, dur)}{smil("width", ws, dur)}</rect>')
        cum = [a + b for a, b in zip(cum, fr)]
    return out + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="currentColor" stroke-width="1.6"/>'


def legend(x, y, items, gap=60):
    out = ""
    for i, (c, t) in enumerate(items):
        out += f'<rect x="{x + i * gap}" y="{y}" width="11" height="11" fill="{c}"/>' + lbl(x + i * gap + 15, y + 10, t, "currentColor", 12, "start", "600")
    return out


def mover(content, dxs, dys, dur):
    vals = ";".join(f"{a:.1f} {b:.1f}" for a, b in zip(dxs, dys))
    return (f'<g><animateTransform attributeName="transform" type="translate" values="{vals}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'
            f'{content}</g>')


def static_bar(x, y, w, h, parts):
    out = ""; cx = x
    for col, f in parts:
        out += f'<rect x="{cx:.1f}" y="{y}" width="{w * f:.1f}" height="{h}" fill="{col}" opacity="0.9"/>'; cx += w * f
    return out + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="currentColor" stroke-width="1.6"/>'


def lerp_pts(a, b, n):
    return [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(n + 1)]


# ───────────── Dạng 1: drone bay ngang, hai mốc thế năng ─────────────
def d1(k):
    p = f"d1{k}"; s = 14; gy = 205; roof = gy - 3 * s; y0 = gy - 8 * s
    b = defs(p) + ground(gy) + f'<rect x="44" y="{roof}" width="352" height="{gy - roof}" fill="none" stroke="currentColor" stroke-width="2"/>'
    b += lbl(220, gy - 12, "sân thượng", "currentColor", 12, "middle", "400") + lbl(16, 230, "mặt đất", "currentColor", 12, "start", "400")
    b += dim(p, "o", 22, y0, 22, gy, "", 0, 0) + lbl(28, (y0 + roof) / 2 + 4, "h = 8 m", ORG, 13, "start", "700")

    def drone(x):
        return (f'<rect x="{x - 10}" y="{y0 - 4}" width="20" height="8" rx="2" fill="none" stroke="currentColor" stroke-width="2.2"/>'
                + seg(x - 15, y0 - 8, x - 5, y0 - 8, "currentColor", 2.2) + seg(x + 5, y0 - 8, x + 15, y0 - 8, "currentColor", 2.2))
    if k == 0:
        x0 = 70; dx = 5 * 4 * s          # 5 m/s trong 4 s
        b += seg(x0, y0, x0 + dx, y0, GRN, 2.4, "6 4")
        grp = drone(x0) + arrow(p, "r", x0 + 18, y0, x0 + 62, y0, 3) + lbl(x0, y0 - 30, "m = 400 g", "currentColor", 12, "middle", "700") + lbl(x0, y0 - 16, "v = 18 km/h", RED, 12, "middle", "700")
        n = 40
        b += mover(grp, [dx * i / n for i in range(n + 1)], [0] * (n + 1), 4.0)
        b += lbl(250, 22, "a) mốc: mặt đất", "currentColor", 13, "start", "400") + lbl(250, 40, "b) mốc: mặt sân thượng", "currentColor", 13, "start", "400")
        return fig("d1-0", "0 0 420 238", "Drone bay ngang ở độ cao 8 m so với mặt đất, phía trên sân thượng cao 3 m", b,
                   "Mô phỏng: drone bay ngang đều (đúng thời gian thật, 4 s; bấm Chạy mô phỏng). " + NOTE)
    b += drone(200) + arrow(p, "r", 218, y0, 262, y0, 3) + lbl(200, y0 - 16, "v = 18 km/h", RED, 12, "middle", "700")
    b += seg(44, roof, 396, roof, BLUE, 1.6, "5 4") + lbl(398, roof - 5, "mốc b", BLUE, 12, "end", "700")
    b += seg(44, gy, 396, gy, BLUE, 1.6, "5 4") + lbl(388, gy - 5, "mốc a", BLUE, 12, "end", "700")
    b += dim(p, "g", 330, y0 + 4, 330, roof, "", 0, 0) + lbl(336, (y0 + roof) / 2 + 4, "h′ = ?", GRN, 13, "start", "700")
    return fig("d1-1", "0 0 420 238", "Hai mốc thế năng: mặt đất và mặt sân thượng; độ cao của drone đo từ từng mốc", b,
               "Dữ kiện: cùng một vị trí, độ cao h khác nhau theo mốc. " + NOTE)


# ───────────── Dạng 2: ném thẳng đứng lên, v0 = 10 m/s ─────────────
def d2(k):
    p = f"d2{k}"; gy = 200; s = 24
    b = defs(p) + ground(gy, 16, 150)
    if k == 0:
        T = 2.0; n = 40; ts = [T * i / n for i in range(n + 1)]
        pts = [(105, gy - 6 - s * (10 * t - 5 * t * t)) for t in ts]
        wd = [(1 - t) ** 2 for t in ts]; wt = [1 - f for f in wd]
        b += arrow(p, "r", 60, gy - 6, 60, gy - 56, 3) + lbl(16, 132, "v₀ = 10 m/s", RED, 13, "start", "700")
        b += lbl(16, 24, "m = 2 kg", "currentColor", 13, "start", "400") + lbl(16, 42, "bỏ qua lực cản", "currentColor", 13, "start", "400")
        b += lbl(118, 78, "h_max = ?", ORG, 13, "start", "700")
        b += lbl(200, 56, "cơ năng W (không đổi)", "currentColor", 12, "start", "400")
        b += ebar(200, 62, 190, 24, [(C_WD, wd), (C_WT, wt)], T) + legend(200, 94, [(C_WD, "Wđ"), (C_WT, "Wt")])
        b += ball(pts, 0, T / n)
        return fig("d2-0", "0 0 420 220", "Vật ném thẳng đứng lên từ mặt đất; thanh năng lượng cho thấy động năng chuyển dần thành thế năng rồi ngược lại", b,
                   "Mô phỏng: vật đi lên rồi rơi xuống (đúng thời gian thật, 2 s). Thanh bên phải chỉ tỉ lệ Wđ và Wt, tổng không đổi. " + NOTE)
    for i, (yy, wdf, txt) in enumerate([(184, 1.0, "lúc ném: Wt = 0"), (124, 0.62, "ở giữa: có cả Wđ và Wt"), (64, 0.0, "điểm cao nhất: v = 0")]):
        b += dot(70, yy, 5.5, GRN) + static_bar(130, yy - 12, 150, 22, [(C_WD, wdf), (C_WT, 1 - wdf)]) + lbl(290, yy + 4, txt, "currentColor", 12, "start", "400")
    b += seg(70, 190, 70, 60, "currentColor", 1.4, "5 4", .6) + legend(130, 20, [(C_WD, "Wđ"), (C_WT, "Wt")])
    return fig("d2-1", "0 0 420 220", "Ba vị trí của vật: lúc ném chỉ có động năng, ở giữa có cả hai, ở điểm cao nhất chỉ có thế năng", b,
               "Dữ kiện: tổng Wđ + Wt luôn bằng cơ năng. " + NOTE)


# ───────────── Dạng 3: trượt dốc không ma sát, l = 8 m, h = 3,2 m ─────────────
def d3(k):
    p = f"d3{k}"; l, h = 8.0, 3.2; hor = math.sqrt(l * l - h * h); s = 41; gy = 190
    A = (50, gy - h * s); B = (A[0] + hor * s, gy)
    b = defs(p) + ground(gy, 16, 410) + poly([A, B], "currentColor", 2.6)
    b += lbl(A[0] - 12, A[1] - 4, "A", "currentColor", 14, "end", "700") + lbl(B[0] + 8, B[1] - 8, "B", "currentColor", 14, "start", "700")
    b += dim(p, "o", 34, A[1], 34, gy, "", 0, 0) + lbl(40, (A[1] + gy) / 2 + 30, "h = 3,2 m", ORG, 13, "start", "700")
    mid = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2); b += lbl(mid[0] + 10, mid[1] - 8, "l = 8 m", BLUE, 13, "start", "700")
    if k == 0:
        T = 2.0; n = 40; ss = [2 * (T * i / n) ** 2 for i in range(n + 1)]       # a = g·sinα = 4 m/s²
        pts = [(A[0] + (B[0] - A[0]) * q / l, A[1] + (B[1] - A[1]) * q / l) for q in ss]
        wd = [q / l for q in ss]; wt = [1 - f for f in wd]
        b += lbl(96, 28, "m = 1,5 kg", "currentColor", 13, "start", "400") + lbl(96, 46, "bỏ qua ma sát", "currentColor", 13, "start", "400")
        b += lbl(B[0] + 12, B[1] - 52, "v_B = ?", RED, 13, "start", "700")
        b += lbl(240, 22, "cơ năng W (không đổi)", "currentColor", 12, "start", "400")
        b += ebar(240, 28, 160, 22, [(C_WD, wd), (C_WT, wt)], T) + legend(240, 58, [(C_WD, "Wđ"), (C_WT, "Wt")])
        b += ball(pts, 0, T / n)
        return fig("d3-0", "0 0 420 212", "Vật trượt không ma sát từ đỉnh dốc A xuống chân dốc B; thanh năng lượng cho thấy thế năng chuyển thành động năng", b,
                   "Mô phỏng: vật trượt xuống (đúng thời gian thật, 2 s). Quỹ đạo tính theo gia tốc g·sinα. " + NOTE)
    b += lbl(A[0] + 14, A[1] - 8, "A: v = 0, chỉ có Wt", "currentColor", 12, "start", "700")
    b += lbl(B[0] + 12, B[1] - 30, "B: Wt = 0", "currentColor", 12, "start", "700")
    b += lbl(250, 30, "Tìm M trên dốc", GRN, 13, "start", "700") + lbl(250, 48, "sao cho Wđ = Wt", GRN, 13, "start", "700")
    return fig("d3-1", "0 0 420 212", "Dốc AB với độ cao và chiều dài; cần tìm điểm M trên dốc mà động năng bằng thế năng", b,
               "Dữ kiện: mốc thế năng tại chân dốc B. " + NOTE)


# ───────────── Dạng 4: dốc có ma sát, l = 10, h = 6, cosα = 0,8, μ = 0,35 ─────────────
def d4(k):
    p = f"d4{k}"; l, h, hor = 10.0, 6.0, 8.0; s = 30; gy = 215
    A = (60, gy - h * s); B = (A[0] + hor * s, gy)
    b = defs(p) + ground(gy, 16, 410) + poly([A, B], "currentColor", 2.6)
    b += lbl(A[0] - 12, A[1] - 4, "A", "currentColor", 14, "end", "700") + lbl(B[0] + 8, B[1] - 8, "B", "currentColor", 14, "start", "700")
    ang = math.degrees(math.atan2(h, hor))
    b += arc(B[0], B[1], 34, 180 - ang, 180, RED, 1.8) + lbl(B[0] - 50, B[1] - 8, "α", RED, 13, "end", "700")
    if k == 0:
        mu, g_ = 0.35, GR; a = g_ * (h / l - mu * hor / l)        # 3,2 m/s²
        T = math.sqrt(2 * l / a); n = 40; ts = [T * i / n for i in range(n + 1)]
        ss = [0.5 * a * t * t for t in ts]; m = 2.0; W1 = m * g_ * h
        pts = [(A[0] + (B[0] - A[0]) * q / l, A[1] + (B[1] - A[1]) * q / l) for q in ss]
        wt = [1 - q / l for q in ss]; wd = [0.5 * m * (2 * a * q) / W1 for q in ss]; qq = [mu * m * g_ * (hor / l) * q / W1 for q in ss]
        b += dim(p, "o", 40, A[1], 40, gy, "", 0, 0) + lbl(46, (A[1] + gy) / 2 + 36, "h = 6 m", ORG, 13, "start", "700")
        b += lbl(112, 24, "m = 2 kg", "currentColor", 13, "start", "400") + lbl(112, 42, "μ = 0,35", "currentColor", 13, "start", "400") + lbl(112, 60, "cos α = 0,8", "currentColor", 13, "start", "400")
        b += lbl(205, 112, "l = 10 m", BLUE, 13, "start", "700") + lbl(B[0] + 12, B[1] - 40, "v_B = ?", RED, 13, "start", "700")
        b += lbl(250, 22, "năng lượng ban đầu W₁", "currentColor", 12, "start", "400")
        b += ebar(250, 28, 150, 22, [(C_WD, wd), (C_WT, wt), (C_Q, qq)], T) + legend(250, 58, [(C_WD, "Wđ"), (C_WT, "Wt"), (C_Q, "nhiệt")], 52)
        b += ball(pts, 0, T / n)
        return fig("d4-0", "0 0 420 238", "Vật trượt có ma sát từ đỉnh dốc xuống chân dốc; thanh năng lượng có thêm phần nhiệt toả ra tăng dần", b,
                   f"Mô phỏng: vật trượt xuống (đúng thời gian thật, {T:.1f} s). Thanh bên phải: phần nhiệt tăng dần, Wđ + Wt + nhiệt = W₁. " + NOTE)
    # hình lực trên dốc: vật tại giữa dốc
    t_ = ((B[0] - A[0]) / math.hypot(B[0] - A[0], B[1] - A[1]), (B[1] - A[1]) / math.hypot(B[0] - A[0], B[1] - A[1]))   # đơn vị dọc dốc (xuống)
    nrm = (-t_[1], t_[0])        # pháp tuyến hướng vào mặt dốc? chọn ra khỏi mặt dốc (lên trên-phải)
    if nrm[1] > 0: nrm = (-nrm[0], -nrm[1])
    M = (A[0] + 0.45 * (B[0] - A[0]), A[1] + 0.45 * (B[1] - A[1])); Mo = (M[0] + nrm[0] * 6, M[1] + nrm[1] * 6)
    b += dot(*Mo, 6, GRN)
    # tỉ lệ thật (k = 3 px/N): P = mg = 20 N, N = P·cos α = 16 N, F_ms = μN = 5,6 N
    K = 3
    b += vec_luc("o", Mo[0], Mo[1], 0, 1, 20, K, 3)[0] + lbl(Mo[0] + 10, Mo[1] + 20 * K - 6, "P", ORG, 13, "start", "700")
    b += vec_luc("b", Mo[0], Mo[1], nrm[0], nrm[1], 16, K, 3)[0] + lbl(Mo[0] + nrm[0] * 16 * K - 4, Mo[1] + nrm[1] * 16 * K - 6, "N", BLUE, 13, "end", "700")
    b += vec_luc("r", Mo[0], Mo[1], -t_[0], -t_[1], 5.6, K, 3)[0] + lbl(Mo[0] - t_[0] * 5.6 * K - 8, Mo[1] - t_[1] * 5.6 * K + 18, "F_ms", RED, 13, "end", "700")
    b += lbl(250, 24, "N = P·cos α", BLUE, 13, "start", "700") + lbl(250, 44, "F_ms = μ·N", RED, 13, "start", "700") + lbl(250, 64, "A_ms = F_ms·l", "currentColor", 13, "start", "700")
    return fig("d4-1", "0 0 420 238", "Các lực tác dụng lên vật trên dốc: trọng lực, phản lực vuông góc với dốc và lực ma sát dọc dốc hướng lên", b,
               "Dữ kiện: lực ma sát song song với dốc, áp lực vuông góc với dốc. " + NOTE)


# ───────────── Dạng 5: xích đu / con lắc đơn, l = 4,5 m, cosα0 = 0,9 ─────────────
def pendulum_series(theta0, l, g, n):
    w2 = g / l
    T = 2 * math.pi * math.sqrt(l / g) * (1 + theta0 ** 2 / 16 + 11 * theta0 ** 4 / 3072)
    th, om, t, dt = -theta0, 0.0, 0.0, 1e-3
    out = [th]; nxt = T / n
    f = lambda th_, om_: (om_, -w2 * math.sin(th_))
    while len(out) <= n:
        k1 = f(th, om); k2 = f(th + dt / 2 * k1[0], om + dt / 2 * k1[1]); k3 = f(th + dt / 2 * k2[0], om + dt / 2 * k2[1]); k4 = f(th + dt * k3[0], om + dt * k3[1])
        th += dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); om += dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]); t += dt
        if t >= nxt * len(out): out.append(th)
    return T, out


def d5(k):
    p = f"d5{k}"; l = 4.5; c0 = 0.9; th0 = math.acos(c0); s = 37.8; P = (150, 26); L = l * s
    O = (P[0], P[1] + L); h_px = L * (1 - c0)
    b = defs(p) + seg(P[0] - 40, P[1], P[0] + 40, P[1], "currentColor", 3)
    b += seg(40, O[1], 250, O[1], BLUE, 1.5, "5 4") + (lbl(250, O[1] + 4, "O: mốc Wt = 0", BLUE, 12, "start", "700") if k == 0 else lbl(250, O[1] + 4, "mốc", BLUE, 12, "start", "700"))
    ya = P[1] + L * c0
    if k == 0:
        n = 84; T, th = pendulum_series(th0, l, GR, n)
        pts = [(P[0] + L * math.sin(a), P[1] + L * math.cos(a)) for a in th]
        wt = [(1 - math.cos(a)) / (1 - c0) for a in th]; wd = [max(0.0, 1 - f_) for f_ in wt]
        arc_pts_ = [(P[0] + L * math.sin(-th0 + 2 * th0 * i / 40), P[1] + L * math.cos(-th0 + 2 * th0 * i / 40)) for i in range(41)]
        b += poly(arc_pts_, GRN, 2, "6 4", .9)
        b += seg(30, ya, pts[0][0], ya, "currentColor", 1.2, "4 4", .6) + dim(p, "o", 60, ya, 60, O[1], "", 0, 0) + lbl(50, ya + 6, "h = ?", ORG, 13, "end", "700")
        b += lbl(16, 56, "l = 4,5 m", BLUE, 13, "start", "700") + lbl(16, 74, "m = 25 kg", "currentColor", 13, "start", "400") + lbl(16, 92, "cos α₀ = 0,9", "currentColor", 13, "start", "400")
        b += lbl(250, 40, "cơ năng W (không đổi)", "currentColor", 12, "start", "400")
        b += ebar(250, 46, 150, 22, [(C_WD, wd), (C_WT, wt)], T) + legend(250, 76, [(C_WD, "Wđ"), (C_WT, "Wt")])
        dur = T
        b += (f'<line x1="{P[0]}" y1="{P[1]}" x2="{pts[0][0]:.1f}" y2="{pts[0][1]:.1f}" stroke="currentColor" stroke-width="2">'
              f'{smil("x2", [q[0] for q in pts], dur)}{smil("y2", [q[1] for q in pts], dur)}</line>')
        b += (f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="7" fill="{GRN}" stroke="currentColor" stroke-width="1.5">'
              f'{smil("cx", [q[0] for q in pts], dur)}{smil("cy", [q[1] for q in pts], dur)}</circle>')
        b += lbl(O[0], O[1] + 22, "O", "currentColor", 13, "middle", "700")
        return fig("d5-0", "0 0 420 232", "Xích đu được kéo lệch rồi thả, dao động qua lại quanh vị trí cân bằng O; thanh năng lượng đổi qua lại giữa động năng và thế năng", b,
                   f"Mô phỏng: một chu kì dao động (đúng thời gian thật, {T:.1f} s). Chuyển động tính từ phương trình con lắc. " + NOTE)
    a0 = th0; bob = (P[0] - L * math.sin(a0), P[1] + L * math.cos(a0))
    b += seg(*P, *bob, "currentColor", 2) + seg(P[0], P[1], P[0], O[1], "currentColor", 1.2, "4 4", .6) + dot(*bob, 7, GRN)
    b += arc(P[0], P[1], 46, 270 - math.degrees(a0), 270, RED, 1.8) + lbl(P[0] - 18, P[1] + 70, "α₀", RED, 13, "end", "700")
    b += seg(bob[0], bob[1], P[0] + 40, bob[1], "currentColor", 1.2, "4 4", .6)
    b += dim(p, "o", P[0] + 30, bob[1], P[0] + 30, O[1], "", 0, 0) + lbl(P[0] + 36, (bob[1] + O[1]) / 2 + 12, "h = ?", ORG, 13, "start", "700")
    b += lbl(250, 60, "biên: v = 0, Wt cực đại", "currentColor", 12, "start", "400") + lbl(250, 78, "O: Wt = 0, Wđ cực đại", "currentColor", 12, "start", "400")
    b += lbl(O[0], O[1] + 22, "O", "currentColor", 13, "middle", "700")
    return fig("d5-1", "0 0 420 232", "Con lắc kéo lệch góc alpha 0 so với phương thẳng đứng; cần tìm độ cao h của vật so với vị trí cân bằng O", b,
               "Dữ kiện: h đo từ vị trí cân bằng O, không phải từ điểm treo. " + NOTE)


# ───────────── Dạng 6: đồ thị năng lượng của vật rơi tự do (H = 20 m, m = 0,5 kg) ─────────────
def graph_hw(ox, oy, wpx, hpx, p, labels=True, lines=True):
    out = arrow(p, "g", ox, oy, ox + wpx + 14, oy, 2) + arrow(p, "g", ox, oy, ox, oy - hpx - 14, 2)
    if lines:
        out += seg(ox, oy - hpx, ox + wpx, oy - hpx, "currentColor", 1.6, "5 4", .8)            # W
        out += seg(ox, oy, ox + wpx, oy - hpx, C_WT, 2.6) + seg(ox, oy - hpx, ox + wpx, oy, C_WD, 2.6)
    if labels:
        out += lbl(ox - 6, oy + 14, "0", "currentColor", 12, "end", "400") + lbl(ox + wpx, oy + 16, "H", "currentColor", 12, "middle", "700")
    return out


def d6(k):
    p = f"d6{k}"
    if k == 0:
        H = 20.0; T = 2.0; n = 40; ts = [T * i / n for i in range(n + 1)]; hs = [H - 5 * t * t for t in ts]
        gx, gyb, wp, hp = 190, 196, 190, 130
        b = defs(p) + graph_hw(gx, gyb, wp, hp, p, True, False)
        b += lbl(gx + wp / 2, gyb + 34, "độ cao h (m)", "currentColor", 12, "middle", "400") + lbl(gx, 26, "năng lượng (J)", "currentColor", 12, "start", "400")
        # cột vật rơi
        cx = 105; sc = 7.0; top = 44
        b += ground(gyb, 16, 140)
        pts = [(cx, gyb - 6 - sc * h_) for h_ in hs]
        b += dim(p, "o", 30, gyb - 6, 30, gyb - 6 - sc * H, "", 0, 0) + lbl(36, 126, "H = 20 m", ORG, 13, "start", "700")
        b += lbl(16, 22, "m = 0,5 kg", "currentColor", 13, "start", "400")
        xW = [gx + wp * h_ / H for h_ in hs]
        yT = [gyb - hp * h_ / H for h_ in hs]; yD = [gyb - hp * (1 - h_ / H) for h_ in hs]
        b += (f'<circle cx="{xW[0]:.1f}" cy="{yT[0]:.1f}" r="5" fill="{C_WT}" stroke="currentColor" stroke-width="1.4">{smil("cx", xW, T)}{smil("cy", yT, T)}</circle>')
        b += (f'<circle cx="{xW[0]:.1f}" cy="{yD[0]:.1f}" r="5" fill="{C_WD}" stroke="currentColor" stroke-width="1.4">{smil("cx", xW, T)}{smil("cy", yD, T)}</circle>')
        b += ball(pts, 0, T / n)
        return fig("d6-0", "0 0 420 240", "Vật rơi tự do từ độ cao 20 m; hai chấm trên hệ trục cho thấy thế năng và động năng ứng với độ cao của vật", b,
                   "Mô phỏng: vật rơi (đúng thời gian thật, 2 s); chấm cam là Wt, chấm đỏ là Wđ (ứng với độ cao của vật). Trục năng lượng chưa ghi số. " + NOTE)
    b = defs(p) + graph_hw(40, 190, 150, 120, p, True, False)
    b += lbl(115, 222, "độ cao h", "currentColor", 12, "middle", "400") + lbl(40, 40, "năng lượng", "currentColor", 12, "start", "400")
    b += lbl(70, 110, "Wt, Wđ theo h = ?", GRN, 12, "start", "700")
    ox, oy = 250, 190
    b += arrow(p, "g", ox, oy, ox + 150, oy, 2) + arrow(p, "g", ox, oy, ox, oy - 134, 2)
    b += lbl(ox + 75, oy + 32, "v²", "currentColor", 12, "middle", "700") + lbl(ox, 40, "Wđ", C_WD, 13, "start", "700") + lbl(ox + 40, oy - 60, "Wđ theo v² = ?", GRN, 12, "start", "700")
    return fig("d6-1", "0 0 420 240", "Bên trái: hệ trục năng lượng theo độ cao; bên phải: hệ trục động năng theo bình phương vận tốc", b,
               "Dữ kiện: hai hệ trục cần vẽ đồ thị. " + NOTE)


# ───────────── Dạng 7: dốc – mặt ngang có ma sát – dốc ─────────────
def sim7(hA=3.2, mu=0.4, BC=3.5, L3=5.0, ang=30.0):
    g = GR; sa = math.sin(math.radians(ang)); L1 = hA / sa; tot = L1 + BC + L3
    s, u, t, dt = 0.0, 0.0, 0.0, 2e-5; rec = []; nxt = 0.0; stopped = None
    def acc(s_, u_):
        if s_ < L1: return g * sa
        if s_ < L1 + BC: return -mu * g * (1 if u_ > 0 else -1)
        return -g * sa
    while True:
        if t >= nxt - 1e-12:
            rec.append((t, s, u)); nxt += 0.1
        if stopped is not None and t - stopped > 0.5: break
        if stopped is None:
            a = acc(s, u); un = u + a * dt
            if L1 <= s < L1 + BC and u != 0 and un * u <= 0:
                un = 0.0; stopped = t
            u = un; s += u * dt; t += dt
            if t > 40: break
        else:
            t += dt * 500
    return rec, L1, stopped


def d7(k):
    p = f"d7{k}"; hA, BCm, ang = 3.2, 3.5, 30.0; sc = 26; yb = 150
    L1 = hA / math.sin(math.radians(ang)); x1 = L1 * math.cos(math.radians(ang)) * sc; x2 = BCm * sc; x3 = 5.0 * math.cos(math.radians(ang)) * sc; y3 = 5.0 * math.sin(math.radians(ang)) * sc
    A = (40, yb - hA * sc); B = (A[0] + x1, yb); C = (B[0] + x2, yb); D = (C[0] + x3, yb - y3)
    b = defs(p) + poly([A, B, C, D], "currentColor", 2.6)
    for nm, q, dx, dy in (("A", A, -12, -4), ("B", B, -4, 20), ("C", C, 4, 20), ("D", D, 8, 4)):
        b += lbl(q[0] + dx, q[1] + dy, nm, "currentColor", 14, "end" if nm == "A" else "start", "700")
    b += dim(p, "o", 26, A[1], 26, yb, "", 0, 0) + lbl(32, (A[1] + yb) / 2 + 40, "h_A = 3,2 m", ORG, 13, "start", "700")
    b += dim(p, "b", B[0], yb + 24, C[0], yb + 24, "BC = 3,5 m", (B[0] + C[0]) / 2 - 38, yb + 42) + lbl((B[0] + C[0]) / 2, yb - 10, "μ = 0,4", RED, 13, "middle", "700")
    b += lbl(16, 214, "m = 1,5 kg · AB, CD không ma sát", "currentColor", 12, "start", "400") if k == 0 else ""
    if k == 0:
        rec, L1_, stopped = sim7(hA=hA, mu=0.4, BC=BCm)
        def xy(q):
            if q <= L1_: f = q / L1_; return (A[0] + (B[0] - A[0]) * f, A[1] + (B[1] - A[1]) * f)
            if q <= L1_ + BCm: return (B[0] + (q - L1_) * sc, yb)
            f = (q - L1_ - BCm) / 5.0; return (C[0] + (D[0] - C[0]) * f, C[1] + (D[1] - C[1]) * f)
        pts = [xy(r[1]) for r in rec]; n = len(rec)
        W1 = GR * hA; wd = []; wt = []; qq = []
        for _, q, u in rec:
            hh = (L1_ - q) * 0.5 if q < L1_ else (0 if q <= L1_ + BCm else (q - L1_ - BCm) * 0.5)
            e_d = 0.5 * u * u; e_t = GR * hh
            wd.append(e_d / W1); wt.append(e_t / W1); qq.append(max(0.0, 1 - (e_d + e_t) / W1))
        T = 0.1 * (n - 1)
        b += lbl(130, 22, "cơ năng ban đầu W_A", "currentColor", 12, "start", "400")
        b += ebar(130, 28, 200, 20, [(C_WD, wd), (C_WT, wt), (C_Q, qq)], T) + legend(130, 56, [(C_WD, "Wđ"), (C_WT, "Wt"), (C_Q, "nhiệt")], 56)
        b += ball(pts, 0, 0.1)
        return fig("d7-0", "0 0 420 224", "Vật trượt từ A qua B, C lên dốc CD rồi quay lại, qua lại nhiều lần trên đoạn BC có ma sát cho tới khi dừng", b,
                   f"Mô phỏng: chuyển động tính thật cho tới khi dừng (đúng thời gian thật, {T:.0f} s). Thanh bên phải: nhiệt tăng mỗi lần qua BC. " + NOTE)
    b += lbl(130, 30, "AB: W không đổi", "currentColor", 12, "start", "400") + lbl(130, 48, "BC: W giảm F_ms·BC mỗi lượt", RED, 12, "start", "700") + lbl(130, 66, "CD: W không đổi", "currentColor", 12, "start", "400")
    b += lbl(D[0] - 6, D[1] - 14, "h_max = ?", ORG, 13, "end", "700")
    return fig("d7-1", "0 0 420 224", "Ba đoạn đường: dốc AB không ma sát, mặt ngang BC có ma sát, dốc CD không ma sát", b,
               "Dữ kiện: cơ năng chỉ giảm ở đoạn BC. " + NOTE)
