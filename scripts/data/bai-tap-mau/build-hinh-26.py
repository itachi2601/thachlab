"""Bài 26 · Bài 7. Bài tập về sự chuyển hoá năng lượng trong dao động điều hoà (Vật lí 11, chương 1 Dao động)
— dựng file scripts/data/bai-tap-mau/26.json từ đầu.   Chạy: python3 scripts/data/bai-tap-mau/build-hinh-26.py   (mẫu cấu trúc: build-hinh-57.py)

QUÉT DẠNG (bước 0, làm trong phiên 9/10/2026; lý thuyết bài 26 có 4 "họ" + bài toán mẫu; ngân hàng chưa tra được vì RLS):
  Bài 26 KHÔNG có chủ đề riêng trong question-topics.json; nội dung năng lượng nằm ở bài 24 → dùng YCCĐ con của bài 24:
  160 "Động năng, thế năng của vật dao động", 161 "Bảo toàn cơ năng trong dao động điều hoà".
  Không đưa vào: dao động tắt dần / cộng hưởng (bài 25; lý thuyết bài 26 KHÔNG dạy, luật 7 của bước quét).
  5 dạng, cấp không giảm (nhãn Dễ/Trung bình/Khó theo cấp 1/2-2/3-4):
    1 (cấp 1) Họ 1: W, Wt, Wđ, |v| tại li độ x                       · topic 160
    2 (cấp 2) Họ 2: Wđ = n·Wt → li độ, tốc độ                        · topic 160
    3 (cấp 2) Họ 3: đồ thị năng lượng theo li độ x → k, Wđ, |v|      · topic 160
    4 (cấp 3) Họ 4: con lắc đơn, góc lớn → W, v_max, v tại α         · topic 161
    5 (cấp 4) Họ 3 + 2: đồ thị Wđ, Wt theo t (dữ kiện ẩn) → W, T, k, A, v_max · topic 161
Quy ước theo lý thuyết bài 26: W = ½kA² · Wt = ½kx² · Wđ = W − Wt · Wđ = nWt → x = ±A/√(n+1) · năng lượng có chu kì T/2 ·
con lắc đơn h = l(1−cosα), v = √(2gl(cosα − cosα₀)); mốc thế năng luôn ở VTCB; đổi cm → m, g → kg trước khi thế."""
import json, math, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "26.json")
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
PI = math.pi
VIO = "#a78bfa"


def anim(attr, vals_str, dur):
    return f'<animate attributeName="{attr}" values="{vals_str}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'


# ───────────────────────── Con lắc lò xo nằm ngang (dạng 1, 2) ─────────────────────────
X0, YC = 214, 96                 # vị trí cân bằng (tâm vật) và trục lò xo


def spring_pts(xb, ncoil=7):
    xs, xe = 24.0, xb - 20.0
    pts = [(xs, YC), (xs + 10, YC)]
    n = 2 * ncoil
    for i in range(n):
        pts.append((xs + 10 + (xe - xs - 20) * (i + 0.5) / n, YC + (-8 if i % 2 == 0 else 8)))
    pts += [(xe - 10, YC), (xe, YC)]
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def block(xb, ghost=False):
    if ghost:
        return f'<rect x="{xb - 20:.1f}" y="76" width="40" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="4 3" opacity=".6"/>'
    return f'<rect x="{xb - 20:.1f}" y="76" width="40" height="40" rx="3" fill="{GRN}" fill-opacity=".35" stroke="currentColor" stroke-width="2"/>'


def wall_floor():
    return seg(24, 62, 24, 118, "currentColor", 3) + seg(16, 118, 410, 118, "currentColor", 2)


def ruler(s, A_cm, extra=()):
    y = 148
    b = seg(X0 - s * A_cm - 14, y, X0 + s * A_cm + 14, y, "currentColor", 1.6)
    ticks = [(-A_cm, f"−{A_cm}"), (0, "O"), (A_cm, f"{A_cm}")] + list(extra)
    for t, name in ticks:
        b += seg(X0 + s * t, y - 5, X0 + s * t, y + 5, "currentColor", 1.6) + lbl(X0 + s * t, y + 20, name, "currentColor", 12, "middle", "400")
    b += lbl(X0 + s * A_cm + 18, y + 4, "x (cm)", "currentColor", 12, "start", "700")
    return b


def spring_sim(p, A_cm, omega, slow, texts, ghost_x=None, extra_ticks=()):
    """Vật dao động x = A cos(ωt) tính thật; chạy MỘT chu kì, chậm `slow` lần."""
    s = 135.0 / A_cm
    nfr = 30
    T = 2 * PI / omega
    xs = [A_cm * math.cos(2 * PI * i / nfr) for i in range(nfr + 1)]
    xb = [X0 + s * x for x in xs]
    dur = T * slow
    pts_vals = ";".join(spring_pts(v) for v in xb)
    b = defs(p) + wall_floor() + ruler(s, A_cm, extra_ticks)
    b += f'<polyline fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round" points="{spring_pts(xb[0])}">{anim("points", pts_vals, dur)}</polyline>'
    if ghost_x is not None:
        gx = X0 + s * ghost_x
        b += seg(gx, 66, gx, 150, ORG, 1.6, "4 4") + block(gx, True)
    b += (f'<rect x="{xb[0] - 20:.1f}" y="76" width="40" height="40" rx="3" fill="{GRN}" fill-opacity=".35" stroke="currentColor" stroke-width="2">'
          f'{smil("x", [v - 20 for v in xb], dur)}</rect>')
    b += arrow(p, "g", X0, 178, X0 + 135, 178, 2) + arrow(p, "g", X0 + 135, 178, X0, 178, 2) + lbl(X0 + 70, 174, f"A = {A_cm} cm", GRN, 13, "middle", "700")
    for (x, y, t, c, anchor) in texts:
        b += lbl(x, y, t, c, 13, anchor, "700")
    return b, dur


def spring_static(p, A_cm, xmark, texts):
    s = 135.0 / A_cm
    gx = X0 + s * xmark
    b = defs(p) + wall_floor() + ruler(s, A_cm)
    b += f'<polyline fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round" points="{spring_pts(gx)}"/>' + block(gx)
    b += seg(X0, 134, gx, 134, ORG, 3) + lbl((X0 + gx) / 2, 130, "x", ORG, 13, "middle", "700") + dot(X0, 134, 3.5, "currentColor")
    b += arrow(p, "g", X0, 178, X0 + 135, 178, 2) + arrow(p, "g", X0 + 135, 178, X0, 178, 2) + lbl(X0 + 70, 174, f"A = {A_cm} cm", GRN, 13, "middle", "700")
    for (x, y, t, c, anchor) in texts:
        b += lbl(x, y, t, c, 12, anchor, "700")
    return b


# ───────────── Dạng 1: m = 0,4 kg, k = 40 N/m, A = 15 cm, x = −9 cm ─────────────
def d1(k):
    p = f"d1{k}"; VB = "0 0 420 196"
    if k == 0:
        om = math.sqrt(40 / 0.4)
        b, dur = spring_sim(p, 15, om, 3, [
            (60, 22, "m = 400 g · k = 40 N/m", "currentColor", "start"),
            (60, 42, "Thả nhẹ từ biên: A = 15 cm", "currentColor", "start"),
            (410, 22, "Cần tìm: W, Wt, Wđ, |v|", ORG, "end"),
            (410, 42, "tại li độ x = −9 cm", ORG, "end")], ghost_x=-9, extra_ticks=[(-9, "−9")])
        b += lbl(X0 - 81, 58, "x = −9 cm", ORG, 12, "middle", "700")
        return fig("d1-0", VB, "Vật 400 gam gắn lò xo nằm ngang dao động giữa hai biên cách vị trí cân bằng 15 cm; vạch cam đánh dấu li độ âm 9 cm", b,
                   "Mô phỏng: một chu kì dao động, chạy chậm 3 lần (T thật ≈ 0,63 s). Chuyển động tính theo x = A·cos(ωt).")
    b = spring_static(p, 15, -9, [
        (410, 22, "① W = ½kA²", "currentColor", "end"), (410, 40, "② Wt = ½kx² (dùng x, không dùng A)", ORG, "end"),
        (410, 58, "③ Wđ = W − Wt  ④ Wđ = ½mv²", BLUE, "end")])
    return fig("d1-2", VB, "Vật ở li độ âm 9 cm so với vị trí cân bằng; cơ năng tính theo biên độ, thế năng theo li độ", b, "Dữ kiện: W theo biên độ A, Wt theo li độ x. " + NOTE)


# ───────────── Dạng 2: m = 0,5 kg, k = 100 N/m, A = 10 cm, Wđ = 24 Wt ─────────────
def d2(k):
    p = f"d2{k}"; VB = "0 0 420 196"
    if k == 0:
        om = math.sqrt(100 / 0.5)
        b, dur = spring_sim(p, 10, om, 3, [
            (60, 22, "m = 500 g · k = 100 N/m", "currentColor", "start"),
            (60, 42, "Thả nhẹ từ biên: A = 10 cm", "currentColor", "start"),
            (410, 22, "Lúc Wđ = 24 Wt:", ORG, "end"),
            (410, 42, "x = ?   |v| = ?", ORG, "end")])
        return fig("d2-0", VB, "Vật 500 gam gắn lò xo nằm ngang dao động với biên độ 10 cm; cần tìm li độ và tốc độ lúc động năng gấp 24 lần thế năng", b,
                   "Mô phỏng: một chu kì dao động, chạy chậm 3 lần (T thật ≈ 0,44 s). Chuyển động tính theo x = A·cos(ωt).")
    # hình dữ kiện: thanh cơ năng chia phần
    x0, x1, y0 = 40, 380, 56
    w1 = (x1 - x0) / 25
    b = defs(p) + lbl(x0, 30, "Cơ năng W (không đổi)", "currentColor", 13, "start", "700")
    b += f'<rect x="{x0}" y="{y0}" width="{x1 - x0 - w1:.1f}" height="30" fill="{BLUE}" fill-opacity=".45" stroke="currentColor" stroke-width="1.8"/>'
    b += f'<rect x="{x1 - w1:.1f}" y="{y0}" width="{w1:.1f}" height="30" fill="{ORG}" fill-opacity=".75" stroke="currentColor" stroke-width="1.8"/>'
    b += lbl((x0 + x1 - w1) / 2, y0 + 20, "Wđ = 24 phần", "currentColor", 13, "middle", "700")
    b += seg(x1 - w1 / 2, y0 + 30, x1 - w1 / 2, y0 + 50, ORG, 1.8) + lbl(x1, y0 + 66, "Wt = 1 phần", ORG, 13, "end", "700")
    b += lbl(x0, 128, "W = Wđ + Wt = (n + 1) phần của Wt", "currentColor", 13, "start", "700")
    b += lbl(x0, 150, "Wt ∝ x²  →  tỉ số li độ = căn của tỉ số năng lượng", ORG, 13, "start", "700")
    return fig("d2-2", "0 0 420 166", "Thanh cơ năng chia thành hai phần: động năng gồm 24 phần, thế năng gồm một phần", b, "Dữ kiện: n phần động năng, 1 phần thế năng. " + NOTE)


# ───────────── Đồ thị năng lượng theo li độ (dạng 3): k = 20 N/m, m = 0,15 kg, A = 6 cm ─────────────
G3 = dict(ox=210, oy=190, sx=22.0, sy=3.4)     # px/cm, px/mJ


def px3(x): return G3["ox"] + G3["sx"] * x
def py3(e): return G3["oy"] - G3["sy"] * e


def graph3_base(p):
    b = defs(p)
    b += seg(px3(-7.2), G3["oy"], px3(7.2), G3["oy"], "currentColor", 1.8) + seg(G3["ox"], G3["oy"] + 4, G3["ox"], 28, "currentColor", 1.8)
    for t in (-6, 0, 6):
        b += seg(px3(t), G3["oy"] - 4, px3(t), G3["oy"] + 5, "currentColor", 1.6) + lbl(px3(t), G3["oy"] + 20, ("−" if t < 0 else "") + str(abs(t)), "currentColor", 12, "middle", "400")
    b += lbl(px3(7.2) + 4, G3["oy"] + 4, "x (cm)", "currentColor", 12, "start", "700") + lbl(G3["ox"] + 8, 30, "W (mJ)", "currentColor", 12, "start", "700")
    b += seg(px3(-6), py3(36), px3(6), py3(36), "currentColor", 1.6, "6 4", .8) + lbl(px3(-0.5), py3(36) - 6, "W = 36 mJ", "currentColor", 13, "end", "700")
    xs = [-6 + 12 * i / 60 for i in range(61)]
    b += poly([(px3(x), py3(x * x)) for x in xs], ORG, 2.6) + poly([(px3(x), py3(36 - x * x)) for x in xs], BLUE, 2.6)
    b += lbl(px3(-5.9), py3(36) + 18, "Wt", ORG, 14, "end", "700") + lbl(px3(-3.4), py3(36 - 3.4 ** 2) - 8, "Wđ", BLUE, 14, "end", "700")
    return b


def d3(k):
    p = f"d3{k}"; VB = "0 0 420 226"
    b = graph3_base(p)
    if k == 0:
        om = math.sqrt(20 / 0.15); T = 2 * PI / om; slow = 4; dur = T * slow; nfr = 48
        xs = [6 * math.cos(2 * PI * i / nfr) for i in range(nfr + 1)]
        b += (f'<line x1="{px3(xs[0]):.1f}" x2="{px3(xs[0]):.1f}" y1="{py3(36):.1f}" y2="{G3["oy"]}" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 4" opacity=".7">'
              f'{smil("x1", [px3(x) for x in xs], dur)}{smil("x2", [px3(x) for x in xs], dur)}</line>')
        b += (f'<circle cx="{px3(xs[0]):.1f}" cy="{py3(xs[0] ** 2):.1f}" r="5.5" fill="{ORG}" stroke="currentColor" stroke-width="1.5">{smil("cx", [px3(x) for x in xs], dur)}{smil("cy", [py3(x * x) for x in xs], dur)}</circle>')
        b += (f'<circle cx="{px3(xs[0]):.1f}" cy="{py3(36 - xs[0] ** 2):.1f}" r="5.5" fill="{BLUE}" stroke="currentColor" stroke-width="1.5">{smil("cx", [px3(x) for x in xs], dur)}{smil("cy", [py3(36 - x * x) for x in xs], dur)}</circle>')
        b += lbl(16, 22, "m = 150 g", "currentColor", 13, "start", "700") + lbl(16, 42, "Cần tìm: k; Wđ, |v| tại x = 3 cm", ORG, 13, "start", "700")
        return fig("d3-0", VB, "Đồ thị thế năng và động năng theo li độ của con lắc lò xo: hai parabol, cơ năng là đường ngang 36 mJ, li độ cực đại 6 cm", b,
                   "Mô phỏng: hai điểm chạy trên hai đồ thị khi vật dao động một chu kì (chạy chậm 4 lần, T thật ≈ 0,54 s). Điểm tính theo x = A·cos(ωt).")
    b += seg(px3(3), G3["oy"], px3(3), py3(9), "currentColor", 1.4, "4 4", .8) + dot(px3(3), py3(9), 5, ORG) + dot(px3(3), py3(27), 5, BLUE)
    b += lbl(px3(3), G3["oy"] + 34, "x = 3 cm", "currentColor", 12, "middle", "700")
    b += lbl(px3(3) + 10, py3(9) + 4, "Wt = ?", ORG, 13, "start", "700") + lbl(px3(3) + 10, py3(27) - 8, "Wđ = ?", BLUE, 13, "start", "700")
    b += lbl(16, 22, "① đọc A, W → k = 2W/A²", "currentColor", 12, "start", "700") + lbl(16, 40, "② Wt = ½kx², Wđ = W − Wt", "currentColor", 12, "start", "700")
    return fig("d3-2", VB, "Tại li độ 3 cm, thế năng và động năng là hai điểm trên hai đồ thị, tổng của chúng bằng cơ năng", b, "Dữ kiện: tại mỗi x, hai điểm trên đồ thị cộng lại bằng W. " + NOTE)


# ───────────── Dạng 4: con lắc đơn l = 0,9 m, m = 200 g, α₀ = 60°, g = 10 ─────────────
PX, PY, LP = 210, 28, 150.0     # chốt treo và chiều dài dây (px)
L4, G4, A0 = 0.9, 10.0, math.radians(60)


def pend_traj(tmax, nfr):
    """Tích phân θ'' = −(g/l) sinθ (RK4) từ α₀, thả nhẹ → θ(t) thật (không dùng xấp xỉ góc nhỏ)."""
    h = 0.0005; th, w = A0, 0.0; out = []; t = 0.0; nxt = 0
    steps = int(round(tmax / h))
    f = lambda th_, w_: (w_, -G4 / L4 * math.sin(th_))
    for i in range(steps + 1):
        if i >= nxt * steps / nfr:
            out.append(th); nxt += 1
        k1 = f(th, w); k2 = f(th + h / 2 * k1[0], w + h / 2 * k1[1]); k3 = f(th + h / 2 * k2[0], w + h / 2 * k2[1]); k4 = f(th + h * k3[0], w + h * k3[1])
        th += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); w += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
    return out[: nfr + 1]


def bob(th):
    return PX + LP * math.sin(th), PY + LP * math.cos(th)


def pend_period():
    h = 0.0005; th, w = A0, 0.0; t = 0.0; f = lambda a, b_: (b_, -G4 / L4 * math.sin(a))
    cross = 0
    while True:
        prev_w = w
        k1 = f(th, w); k2 = f(th + h / 2 * k1[0], w + h / 2 * k1[1]); k3 = f(th + h / 2 * k2[0], w + h / 2 * k2[1]); k4 = f(th + h * k3[0], w + h * k3[1])
        th += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); w += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]); t += h
        if (prev_w < 0 <= w) or (prev_w > 0 >= w):   # θ' đổi dấu: biên trái (lần 1), biên phải (lần 2 = hết một chu kì)
            cross += 1
            if cross == 2:
                return t


def pend_base(p, left_label=False):
    b = defs(p) + seg(PX - 40, PY - 4, PX + 40, PY - 4, "currentColor", 3)
    arc_pts = [bob(math.radians(a)) for a in range(-60, 61, 4)]
    b += poly(arc_pts, GRN, 1.6, "5 4", .8)
    b += seg(PX, PY, PX, PY + LP, "currentColor", 1.2, "5 4", .6)
    yb = PY + LP
    b += seg(PX - 80, yb, PX + 100, yb, "currentColor", 1.2, "6 4", .5) + (lbl(PX - 80, yb + 18, "mốc thế năng", "currentColor", 12, "start", "400") if left_label else lbl(PX + 104, yb + 4, "mốc thế năng", "currentColor", 12, "start", "400"))
    return b


def d4(k):
    p = f"d4{k}"; VB = "0 0 420 206"
    b = pend_base(p)
    gx, gy = bob(-math.radians(30))
    if k == 0:
        Tp = pend_period(); nfr = 60
        ths = pend_traj(Tp, nfr)
        X = [bob(t)[0] for t in ths]; Y = [bob(t)[1] for t in ths]
        b += seg(PX, PY, gx, gy, "currentColor", 1.4, "4 4", .6) + f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="9" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3 3" opacity=".6"/>'
        b += (f'<line x1="{PX}" y1="{PY}" x2="{X[0]:.1f}" y2="{Y[0]:.1f}" stroke="currentColor" stroke-width="2">{smil("x2", X, Tp)}{smil("y2", Y, Tp)}</line>')
        b += (f'<circle cx="{X[0]:.1f}" cy="{Y[0]:.1f}" r="10" fill="{GRN}" fill-opacity=".5" stroke="currentColor" stroke-width="2">{smil("cx", X, Tp)}{smil("cy", Y, Tp)}</circle>')
        b += arc(PX, PY, 44, -90, -30, RED) + lbl(PX + 26, PY + 78, "α₀ = 60°", RED, 12, "start", "700")
        b += lbl(gx - 16, gy + 4, "α = 30° → v = ?", ORG, 13, "end", "700")
        b += lbl(16, 56, "l = 0,9 m · m = 200 g", "currentColor", 13, "start", "700") + lbl(16, 76, "g = 10 m/s²", "currentColor", 13, "start", "700")
        b += lbl(410, 20, "Cần tìm: W, v tại VTCB,", ORG, 13, "end", "700") + lbl(410, 38, "v tại α = 30°", ORG, 13, "end", "700")
        return fig("d4-0", VB, "Con lắc đơn dài 0,9 mét thả nhẹ từ góc lệch 60 độ, dao động qua vị trí cân bằng; đường nét đứt cho vị trí khi dây lệch 30 độ", b,
                   f"Mô phỏng: một chu kì, đúng thời gian thật (≈ {Tp:.1f} s). Chuyển động giải số phương trình con lắc đơn, không xấp xỉ góc nhỏ.")
    bx, by = bob(A0)
    b = pend_base(p, True)
    b += seg(PX, PY, bx, by, "currentColor", 2) + f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="10" fill="{GRN}" fill-opacity=".5" stroke="currentColor" stroke-width="2"/>'
    b += arc(PX, PY, 44, -90, -30, RED) + lbl(PX + 20, PY + 62, "α₀", RED, 13, "start", "700")
    b += seg(PX, by, bx, by, ORG, 1.4, "4 4", .8)
    b += dim(p, "o", bx + 24, by, bx + 24, PY + LP, "h₀", bx + 32, (by + PY + LP) / 2 + 4)
    b += lbl(PX - 6, (PY + by) / 2 + 4, "l·cosα₀", "currentColor", 12, "end", "700")
    b += lbl(16, 20, "h₀ = l(1 − cosα₀)", ORG, 12, "start", "700") + lbl(16, 38, "góc lớn: dùng cos", "currentColor", 12, "start", "700")
    return fig("d4-2", VB, "Độ cao của vị trí biên so với mốc thế năng bằng chiều dài dây trừ phần chiếu của dây lên phương thẳng đứng", b, "Dữ kiện: h₀ = l(1 − cosα₀). " + NOTE)


# ───────────── Dạng 5: đồ thị Wt, Wđ theo thời gian — m = 0,2 kg, T = 0,4 s, W = 90 mJ ─────────────
G5 = dict(ox=62, oy=190, st=700.0, se=1.5)      # px/s, px/mJ
W5, T5 = 90.0, 0.4


def px5(t): return G5["ox"] + G5["st"] * t
def py5(e): return G5["oy"] - G5["se"] * e
def wt5(t): return W5 * math.cos(2 * PI * t / T5) ** 2
def wd5(t): return W5 * math.sin(2 * PI * t / T5) ** 2


def graph5_base(p):
    b = defs(p)
    b += seg(G5["ox"], G5["oy"], px5(0.455), G5["oy"], "currentColor", 1.8) + seg(G5["ox"], G5["oy"] + 4, G5["ox"], 30, "currentColor", 1.8)
    b += lbl(px5(0.455), G5["oy"] + 20, "t (s)", "currentColor", 12, "end", "700") + lbl(G5["ox"] + 8, 30, "W (mJ)", "currentColor", 12, "start", "700")
    b += lbl(G5["ox"] - 6, G5["oy"] + 16, "O", "currentColor", 12, "end", "700")
    ts = [0.4 * i / 100 for i in range(101)]
    b += poly([(px5(t), py5(wt5(t))) for t in ts], ORG, 2.6) + poly([(px5(t), py5(wd5(t))) for t in ts], BLUE, 2.6)
    # giao điểm cho trong đề: t = 0,05 s và 0,15 s, mức 45 mJ
    for tc in (0.05, 0.15):
        b += seg(px5(tc), py5(45), px5(tc), G5["oy"] + 4, "currentColor", 1.2, "4 4", .7) + dot(px5(tc), py5(45), 4.5, "currentColor")
        b += lbl(px5(tc), G5["oy"] + 20, fmt_vn(tc), "currentColor", 12, "middle", "700")
    b += seg(G5["ox"] - 4, py5(45), px5(0.15), py5(45), "currentColor", 1.2, "4 4", .7) + lbl(G5["ox"] - 8, py5(45) + 4, "45", "currentColor", 12, "end", "700")
    b += lbl(px5(0.012), py5(88) - 2, "Wt", ORG, 14, "start", "700") + lbl(px5(0.1), py5(90) - 6, "Wđ", BLUE, 14, "middle", "700")
    return b


def fmt_vn(x):
    return f"{x:.2f}".replace(".", ",")


def d5(k):
    p = f"d5{k}"; VB = "0 0 420 226"
    b = graph5_base(p)
    if k == 0:
        slow = 5; dur = T5 * slow; nfr = 48
        ts = [T5 * i / nfr for i in range(nfr + 1)]
        b += (f'<line x1="{px5(0):.1f}" x2="{px5(0):.1f}" y1="{py5(W5):.1f}" y2="{G5["oy"]}" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 4" opacity=".7">'
              f'{smil("x1", [px5(t) for t in ts], dur)}{smil("x2", [px5(t) for t in ts], dur)}</line>')
        b += (f'<circle cx="{px5(0):.1f}" cy="{py5(wt5(0)):.1f}" r="5.5" fill="{ORG}" stroke="currentColor" stroke-width="1.5">{smil("cx", [px5(t) for t in ts], dur)}{smil("cy", [py5(wt5(t)) for t in ts], dur)}</circle>')
        b += (f'<circle cx="{px5(0):.1f}" cy="{py5(wd5(0)):.1f}" r="5.5" fill="{BLUE}" stroke="currentColor" stroke-width="1.5">{smil("cx", [px5(t) for t in ts], dur)}{smil("cy", [py5(wd5(t)) for t in ts], dur)}</circle>')
        b += lbl(px5(0.2), 14, "m = 200 g · π² = 10", "currentColor", 13, "start", "700") + lbl(px5(0.2), 30, "Cần tìm: W, T, k, A, vmax", ORG, 13, "start", "700")
        return fig("d5-0", VB, "Đồ thị thế năng và động năng theo thời gian: hai đường ngược pha cắt nhau tại hai điểm liên tiếp ở mức 45 mJ, tại 0,05 giây và 0,15 giây", b,
                   "Mô phỏng: hai điểm chạy trên hai đồ thị trong một chu kì dao động (chạy chậm 5 lần, T thật là 0,4 s). Gốc thời gian lúc vật ở biên.")
    b += lbl(px5(0.2), 14, "Wđ = Wt tại giao điểm", "currentColor", 12, "start", "700") + lbl(px5(0.2), 30, "2 giao điểm liên tiếp cách nhau ?", ORG, 12, "start", "700")
    b += lbl(px5(0.2), 46, "→ T ?   ·   W ?", ORG, 12, "start", "700")
    return fig("d5-2", VB, "Hai điểm cắt nhau của đồ thị động năng và thế năng; ở mức này mỗi loại bằng một nửa cơ năng", b, "Dữ kiện: giao điểm có Wđ = Wt. " + NOTE)


BUILD = [d1, d2, d3, d4, d5]

# ───────────────────────── Đề ─────────────────────────
DANG = [
 dict(label="Dạng 1 · Dễ · Tính cơ năng, thế năng, động năng và tốc độ tại li độ x",
      topic="Động năng, thế năng của vật dao động",
      problem_html="<p>Một con lắc lò xo nằm ngang gồm vật nhỏ khối lượng $400\\ \\text{g}$ gắn vào lò xo nhẹ có độ cứng $40\\ \\text{N/m}$. Kéo vật khỏi vị trí cân bằng $15\\ \\text{cm}$ rồi thả nhẹ; vật dao động điều hoà. Bỏ qua ma sát. Xét lúc vật ở li độ $x=-9\\ \\text{cm}$ (bên trái vị trí cân bằng).</p>"
                   "<ol type=\"a\"><li>Tính cơ năng của con lắc.</li><li>Tính thế năng và động năng của vật tại li độ đó.</li><li>Tính tốc độ của vật tại li độ đó.</li></ol>"),
 dict(label="Dạng 2 · Trung bình · Động năng bằng n lần thế năng: tìm li độ và tốc độ",
      topic="Động năng, thế năng của vật dao động",
      problem_html="<p>Một con lắc lò xo nằm ngang gồm vật nhỏ khối lượng $500\\ \\text{g}$ gắn vào lò xo nhẹ có độ cứng $100\\ \\text{N/m}$, dao động điều hoà với biên độ $10\\ \\text{cm}$. Bỏ qua ma sát. Tại một thời điểm, động năng của vật bằng $24$ lần thế năng.</p>"
                   "<ol type=\"a\"><li>Tính cơ năng của con lắc.</li><li>Tìm li độ của vật tại thời điểm đó.</li><li>Tính tốc độ của vật tại thời điểm đó.</li></ol>"),
 dict(label="Dạng 3 · Trung bình · Đọc đồ thị năng lượng theo li độ: tìm độ cứng, động năng, tốc độ",
      topic="Động năng, thế năng của vật dao động",
      problem_html="<p>Một con lắc lò xo nằm ngang gồm vật nhỏ khối lượng $150\\ \\text{g}$ dao động điều hoà, bỏ qua ma sát. Hình vẽ là đồ thị thế năng $W_t$ và động năng $W_{\\text{đ}}$ của con lắc theo li độ $x$; đường nét đứt nằm ngang là cơ năng.</p>"
                   "<ol type=\"a\"><li>Đọc đồ thị để tìm độ cứng của lò xo.</li><li>Tính động năng và tốc độ của vật khi $x=3\\ \\text{cm}$.</li></ol>"),
 dict(label="Dạng 4 · Khó · Con lắc đơn góc lớn: cơ năng và tốc độ tại góc lệch bất kì",
      topic="Bảo toàn cơ năng trong dao động điều hoà",
      problem_html="<p>Một con lắc đơn gồm vật nhỏ khối lượng $200\\ \\text{g}$ treo vào sợi dây nhẹ, không dãn, dài $l=0{,}9\\ \\text{m}$. Kéo con lắc lệch khỏi phương thẳng đứng góc $\\alpha_0=60^\\circ$ rồi thả nhẹ. Bỏ qua mọi lực cản, lấy $g=10\\ \\text{m/s}^2$ và chọn mốc thế năng ở vị trí thấp nhất.</p>"
                   "<ol type=\"a\"><li>Tính cơ năng của con lắc.</li><li>Tính tốc độ của vật khi qua vị trí cân bằng.</li><li>Tính tốc độ của vật khi dây lệch góc $\\alpha=30^\\circ$ so với phương thẳng đứng.</li></ol>"),
 dict(label="Dạng 5 · Khó · Đồ thị năng lượng theo thời gian: tìm cơ năng, chu kì, độ cứng, biên độ",
      topic="Bảo toàn cơ năng trong dao động điều hoà",
      problem_html="<p>Một vật nhỏ khối lượng $200\\ \\text{g}$ dao động điều hoà trên lò xo nằm ngang, bỏ qua ma sát. Hình vẽ là đồ thị thế năng $W_t$ và động năng $W_{\\text{đ}}$ của vật theo thời gian $t$ (gốc thời gian lúc vật ở biên); hai đồ thị cắt nhau tại hai điểm liên tiếp như hình. Lấy $\\pi^2=10$.</p>"
                   "<ol type=\"a\"><li>Tính cơ năng và chu kì dao động.</li><li>Tính độ cứng của lò xo và biên độ dao động.</li><li>Tính tốc độ cực đại của vật.</li></ol>"),
]

# ───────────────────────── Bảng phân tích đề ─────────────────────────
ANALYSIS = [
 [("\"con lắc lò xo nằm ngang … $400$ g … $40$ N/m\"", "$m=0{,}4$ kg; $k=40$ N/m", "Cơ năng của con lắc lò xo: $W=\\dfrac{1}{2}kA^2$; đổi g → kg"),
  ("\"kéo vật khỏi vị trí cân bằng $15$ cm rồi thả nhẹ\"", "$A=0{,}15$ m", "Thả nhẹ từ biên: biên độ bằng đoạn đã kéo"),
  ("\"bỏ qua ma sát\"", "$W$ không đổi", "⚠ Bỏ qua ma sát thì $W$ không đổi; mốc thế năng ở VTCB; đổi cm → m trước khi bình phương"),
  ("\"li độ $x=-9$ cm\"", "$x=-0{,}09$ m", "$W_t=\\dfrac{1}{2}kx^2$ dùng $x$, không dùng $A$ (bình phương nên dấu $-$ mất)"),
  ("\"thế năng và động năng\"", "Cần $W_t$, $W_{\\text{đ}}$", "$W_{\\text{đ}}=W-W_t$"),
  ("\"tốc độ\"", "Cần $|v|$", "$W_{\\text{đ}}=\\dfrac{1}{2}mv^2$, nên $|v|=\\sqrt{\\dfrac{2W_{\\text{đ}}}{m}}$")],
 [("\"con lắc lò xo nằm ngang … $500$ g … $100$ N/m\"", "$m=0{,}5$ kg; $k=100$ N/m", "Cơ năng: $W=\\dfrac{1}{2}kA^2$; đổi g → kg"),
  ("\"biên độ $10$ cm\"", "$A=0{,}1$ m", "Đổi cm → m trước khi bình phương"),
  ("\"bỏ qua ma sát\"", "$W$ không đổi", "⚠ Mốc thế năng ở VTCB; $W=W_{\\text{đ}}+W_t$ không đổi suốt quá trình dao động"),
  ("\"động năng bằng $24$ lần thế năng\"", "$n=24$", "Họ 2: $W_{\\text{đ}}=nW_t$ nên $W=(n+1)W_t$"),
  ("\"li độ\"", "Cần $x$", "$W_t\\propto x^2$, nên $x=\\pm\\dfrac{A}{\\sqrt{n+1}}$ (phải lấy căn)"),
  ("\"tốc độ\"", "Cần $|v|$", "$W_{\\text{đ}}=\\dfrac{n}{n+1}W$ và $|v|=\\sqrt{\\dfrac{2W_{\\text{đ}}}{m}}$")],
 [("\"đồ thị thế năng $W_t$ và động năng $W_{\\text{đ}}$ theo li độ $x$\"", "Hai parabol; $W$ là đường ngang", "Theo $x$: $W_t$ parabol đáy ở VTCB; $W_{\\text{đ}}$ parabol úp"),
  ("\"khối lượng $150$ g\"", "$m=0{,}15$ kg", "Đổi g → kg"),
  ("\"bỏ qua ma sát\"", "$W$ không đổi (đường ngang)", "⚠ Chỉ khi bỏ qua ma sát thì $W$ là đường nằm ngang; mốc thế năng ở VTCB"),
  ("đọc đỉnh và hai đầu của đồ thị", "$W$ ở đường ngang; $A$ ở chỗ $W_{\\text{đ}}=0$", "Tại biên $x=\\pm A$: $W_t=W$, $W_{\\text{đ}}=0$; $W=\\dfrac{1}{2}kA^2$"),
  ("\"độ cứng của lò xo\"", "Cần $k$", "$k=\\dfrac{2W}{A^2}$"),
  ("\"khi $x=3$ cm\"", "$x=0{,}03$ m", "$W_t=\\dfrac{1}{2}kx^2$; $W_{\\text{đ}}=W-W_t$; $|v|=\\sqrt{\\dfrac{2W_{\\text{đ}}}{m}}$")],
 [("\"con lắc đơn … $200$ g … dài $0{,}9$ m\"", "$m=0{,}2$ kg; $l=0{,}9$ m", "Mốc thế năng ở vị trí thấp nhất (VTCB)"),
  ("\"kéo lệch $\\alpha_0=60^\\circ$ rồi thả nhẹ\"", "$\\alpha_0=60^\\circ$; $v=0$ ở biên", "Độ cao của biên: $h_0=l(1-\\cos\\alpha_0)$"),
  ("\"bỏ qua mọi lực cản, $g=10$ m/s²\"", "$W$ không đổi", "⚠ Góc $60^\\circ$ không nhỏ: dùng $\\cos$, không dùng $W\\approx\\dfrac{1}{2}mgl\\alpha_0^2$"),
  ("\"cơ năng\"", "Cần $W$", "$W=mgh_0=mgl(1-\\cos\\alpha_0)$"),
  ("\"khi qua vị trí cân bằng\"", "$\\alpha=0$", "$v_{max}=\\sqrt{2gl(1-\\cos\\alpha_0)}$"),
  ("\"khi dây lệch góc $\\alpha=30^\\circ$\"", "$\\alpha=30^\\circ$", "$v=\\sqrt{2gl(\\cos\\alpha-\\cos\\alpha_0)}$")],
 [("\"vật nhỏ khối lượng $200$ g … lò xo nằm ngang\"", "$m=0{,}2$ kg", "Đổi g → kg; $k=m\\omega^2$"),
  ("\"bỏ qua ma sát\"", "$W$ không đổi", "⚠ $W_t+W_{\\text{đ}}=W$ không đổi nên hai đồ thị bù nhau; mốc thế năng ở VTCB"),
  ("\"đồ thị $W_t$, $W_{\\text{đ}}$ theo $t$ (gốc thời gian lúc ở biên)\"", "Hai đường ngược pha", "Theo $t$: $W_t$, $W_{\\text{đ}}$ lên xuống quanh $\\dfrac{W}{2}$, chu kì $\\dfrac{T}{2}$"),
  ("\"cắt nhau tại hai điểm liên tiếp\"", "Mức $45$ mJ; $t=0{,}05$ s và $t=0{,}15$ s", "Giao điểm: $W_{\\text{đ}}=W_t=\\dfrac{W}{2}$; hai giao điểm liên tiếp cách $\\dfrac{T}{4}$"),
  ("\"lấy $\\pi^2=10$\"", "$\\pi^2=10$", "$\\omega=\\dfrac{2\\pi}{T}$ rồi $k=m\\omega^2$"),
  ("\"cơ năng, chu kì, độ cứng, biên độ, tốc độ cực đại\"", "Cần $W$, $T$, $k$, $A$, $v_{max}$", "$W=\\dfrac{1}{2}kA^2$; $v_{max}=\\sqrt{\\dfrac{2W}{m}}$")],
]

# ───────────────────────── Lời giải ─────────────────────────
R_LX = ["<strong>Khái niệm:</strong> cơ năng $W=W_{\\text{đ}}+W_t$, mốc thế năng ở VTCB.",
        "<strong>Định luật:</strong> không ma sát thì $W$ không đổi.",
        "$W=\\dfrac{1}{2}kA^2$ · $W_t=\\dfrac{1}{2}kx^2$ · $W_{\\text{đ}}=W-W_t$",
        "$W_{\\text{đ}}=\\dfrac{1}{2}mv^2$ nên $|v|=\\sqrt{\\dfrac{2W_{\\text{đ}}}{m}}$",
        "⚠ <strong>Điều kiện:</strong> bỏ qua ma sát; đổi cm → m, g → kg trước khi thế."]
R_N = ["<strong>Khái niệm:</strong> $W=W_{\\text{đ}}+W_t$ không đổi khi bỏ qua ma sát.",
       "<strong>Họ 2:</strong> $W_{\\text{đ}}=nW_t$ nên $W=(n+1)W_t$.",
       "$W_t=\\dfrac{1}{2}kx^2\\propto x^2$ nên $x=\\pm\\dfrac{A}{\\sqrt{n+1}}$ (lấy căn)",
       "$W_{\\text{đ}}=\\dfrac{n}{n+1}W$ · $|v|=\\sqrt{\\dfrac{2W_{\\text{đ}}}{m}}$",
       "⚠ <strong>Điều kiện:</strong> bỏ qua ma sát; mốc thế năng ở VTCB."]
R_X = ["<strong>Khái niệm:</strong> đồ thị theo $x$: $W_t$ parabol đáy ở VTCB, $W_{\\text{đ}}$ parabol úp, $W$ đường ngang.",
       "<strong>Định luật:</strong> tại mọi $x$: $W_t+W_{\\text{đ}}=W$.",
       "Tại biên $x=\\pm A$: $W_t=W$, $W_{\\text{đ}}=0$ · $W=\\dfrac{1}{2}kA^2$ nên $k=\\dfrac{2W}{A^2}$",
       "$W_t=\\dfrac{1}{2}kx^2$ · $W_{\\text{đ}}=W-W_t$ · $|v|=\\sqrt{\\dfrac{2W_{\\text{đ}}}{m}}$",
       "⚠ <strong>Điều kiện:</strong> bỏ qua ma sát; đổi mJ → J, cm → m."]
R_D = ["<strong>Khái niệm:</strong> mốc thế năng ở đáy; $W_t=mgh$ với $h=l(1-\\cos\\alpha)$.",
       "<strong>Định luật:</strong> bỏ qua lực cản thì $W=mgl(1-\\cos\\alpha_0)$ không đổi.",
       "$v=\\sqrt{2gl(\\cos\\alpha-\\cos\\alpha_0)}$ · $v_{max}=\\sqrt{2gl(1-\\cos\\alpha_0)}$",
       "⚠ <strong>Điều kiện:</strong> $W\\approx\\dfrac{1}{2}mgl\\alpha_0^2$ chỉ đúng góc nhỏ (dưới khoảng $10^\\circ$, tính bằng rad); $60^\\circ$ thì dùng $\\cos$."]
R_T = ["<strong>Khái niệm:</strong> theo $t$, $W_t$ và $W_{\\text{đ}}$ ngược pha, chu kì $\\dfrac{T}{2}$, lên xuống quanh $\\dfrac{W}{2}$.",
       "<strong>Giao điểm:</strong> $W_{\\text{đ}}=W_t=\\dfrac{W}{2}$; hai giao điểm liên tiếp cách $\\dfrac{T}{4}$.",
       "$\\omega=\\dfrac{2\\pi}{T}$ · $k=m\\omega^2$ · $W=\\dfrac{1}{2}kA^2$ · $v_{max}=\\sqrt{\\dfrac{2W}{m}}$",
       "⚠ <strong>Điều kiện:</strong> bỏ qua ma sát; đổi mJ → J, g → kg."]

SOLS = [
 sol(R_LX, [
  ("Cơ năng", [P("Đổi: $A=15\\ \\text{cm}=0{,}15\\ \\text{m}$; $m=400\\ \\text{g}=0{,}4\\ \\text{kg}$."), M(r"W=\dfrac{1}{2}kA^2=\dfrac{1}{2}\cdot40\cdot0{,}15^2"), A(r"W=0{,}45\ \text{J}")]),
  ("Thế năng và động năng tại $x$", [P("Thế năng dùng li độ ($x=-9\\ \\text{cm}=-0{,}09\\ \\text{m}$):"), M(r"W_t=\dfrac{1}{2}kx^2=\dfrac{1}{2}\cdot40\cdot0{,}09^2"), A(r"W_t=0{,}162\ \text{J}"),
                                      P("Động năng:"), M(r"W_{\text{đ}}=W-W_t=0{,}45-0{,}162"), A(r"W_{\text{đ}}=0{,}288\ \text{J}")]),
  ("Tốc độ", [M(r"W_{\text{đ}}=\dfrac{1}{2}mv^2\ \Rightarrow\ |v|=\sqrt{\dfrac{2W_{\text{đ}}}{m}}=\sqrt{\dfrac{2\cdot0{,}288}{0{,}4}}=\sqrt{1{,}44}"), A(r"|v|=1{,}2\ \text{m/s}")]),
  ("Kiểm tra", [P("$W_t+W_{\\text{đ}}=0{,}162+0{,}288=0{,}45\\ \\text{J}=W$ ✓"),
                P("$v_{max}=\\sqrt{\\dfrac{2W}{m}}=1{,}5\\ \\text{m/s}$ và $1{,}2\\lt1{,}5$ nên hợp lí."),
                P("Cách 2: $\\omega=\\sqrt{\\dfrac{k}{m}}=10\\ \\text{rad/s}$; $|v|=\\omega\\sqrt{A^2-x^2}=10\\cdot0{,}12=1{,}2\\ \\text{m/s}$ ✓")])],
  ["a) $W=0{,}45\\ \\text{J}$", "b) $W_t=0{,}162\\ \\text{J}$ · $W_{\\text{đ}}=0{,}288\\ \\text{J}$", "c) $|v|=1{,}2\\ \\text{m/s}$"],
  "Nhận dạng: đề cho <strong>biên độ</strong> và <strong>li độ</strong> rồi hỏi động năng hay tốc độ → $W$ theo $A$, $W_t$ theo $x$, lấy hiệu."),
 sol(R_N, [
  ("Cơ năng", [P("Đổi $A=10\\ \\text{cm}=0{,}1\\ \\text{m}$."), M(r"W=\dfrac{1}{2}kA^2=\dfrac{1}{2}\cdot100\cdot0{,}1^2"), A(r"W=0{,}5\ \text{J}")]),
  ("Li độ", [P("$W_{\\text{đ}}=24W_t$ nên cơ năng gồm $25$ phần, thế năng chiếm $1$ phần:"), M(r"W=W_{\text{đ}}+W_t=25W_t"),
             M(r"\dfrac{1}{2}kA^2=25\cdot\dfrac{1}{2}kx^2\ \Rightarrow\ x^2=\dfrac{A^2}{25}"), M(r"|x|=\dfrac{A}{5}=\dfrac{10}{5}"), A(r"x=\pm2\ \text{cm}")]),
  ("Tốc độ", [M(r"W_{\text{đ}}=\dfrac{24}{25}W=\dfrac{24}{25}\cdot0{,}5=0{,}48\ \text{J}"), M(r"|v|=\sqrt{\dfrac{2W_{\text{đ}}}{m}}=\sqrt{\dfrac{2\cdot0{,}48}{0{,}5}}=\sqrt{1{,}92}"), A(r"|v|\approx1{,}39\ \text{m/s}")]),
  ("Kiểm tra", [P("$W_t=\\dfrac{1}{2}\\cdot100\\cdot0{,}02^2=0{,}02\\ \\text{J}=\\dfrac{W}{25}$ ✓"),
                P("$v_{max}=\\sqrt{\\dfrac{2W}{m}}=\\sqrt{2}\\approx1{,}41\\ \\text{m/s}$ và $1{,}39\\lt1{,}41$: vật gần VTCB nên tốc độ gần cực đại ✓")])],
  ["a) $W=0{,}5\\ \\text{J}$", "b) $x=\\pm2\\ \\text{cm}$", "c) $|v|\\approx1{,}39\\ \\text{m/s}$"],
  "Nhận dạng: đề cho <strong>động năng gấp n lần thế năng</strong> → $W=(n+1)W_t$, chia $\\sqrt{n+1}$ (không chia $n$)."),
 sol(R_X, [
  ("Đọc đồ thị, tìm độ cứng", [P("Tại biên $W_{\\text{đ}}=0$ và $W_t=W$. Đọc đồ thị: $A=6\\ \\text{cm}=0{,}06\\ \\text{m}$; $W=36\\ \\text{mJ}=0{,}036\\ \\text{J}$."),
                                M(r"W=\dfrac{1}{2}kA^2\ \Rightarrow\ k=\dfrac{2W}{A^2}=\dfrac{2\cdot0{,}036}{0{,}06^2}"), A(r"k=20\ \text{N/m}")]),
  ("Động năng khi $x=3$ cm", [M(r"W_t=\dfrac{1}{2}kx^2=\dfrac{1}{2}\cdot20\cdot0{,}03^2=9\ \text{mJ}"), M(r"W_{\text{đ}}=W-W_t=36-9"), A(r"W_{\text{đ}}=27\ \text{mJ}=0{,}027\ \text{J}")]),
  ("Tốc độ", [M(r"|v|=\sqrt{\dfrac{2W_{\text{đ}}}{m}}=\sqrt{\dfrac{2\cdot0{,}027}{0{,}15}}=\sqrt{0{,}36}"), A(r"|v|=0{,}6\ \text{m/s}")]),
  ("Kiểm tra", [P("$W_t+W_{\\text{đ}}=9+27=36\\ \\text{mJ}=W$ ✓"),
                P("Cách 2: $\\omega=\\sqrt{\\dfrac{k}{m}}\\approx11{,}55\\ \\text{rad/s}$; $|v|=\\omega\\sqrt{A^2-x^2}\\approx11{,}55\\cdot0{,}052=0{,}6\\ \\text{m/s}$ ✓")])],
  ["a) $k=20\\ \\text{N/m}$", "b) $W_{\\text{đ}}=27\\ \\text{mJ}$ · $|v|=0{,}6\\ \\text{m/s}$"],
  "Nhận dạng: đề cho <strong>đồ thị năng lượng theo li độ</strong> → đọc $A$ (chỗ $W_{\\text{đ}}=0$) và $W$ (đỉnh), rồi $k=\\dfrac{2W}{A^2}$."),
 sol(R_D, [
  ("Độ cao của biên", [P("Mốc ở đáy; biên cao hơn đáy:"), M(r"h_0=l(1-\cos\alpha_0)=0{,}9\,(1-\cos60^\circ)=0{,}9\cdot0{,}5"), A(r"h_0=0{,}45\ \text{m}")]),
  ("Cơ năng", [P("Tại biên $v=0$ nên chỉ có thế năng ($m=0{,}2\\ \\text{kg}$):"), M(r"W=mgh_0=0{,}2\cdot10\cdot0{,}45"), A(r"W=0{,}9\ \text{J}")]),
  ("Tốc độ khi qua VTCB", [P("Ở đáy $W_t=0$ nên toàn bộ là động năng:"), M(r"\dfrac{1}{2}mv^2=W\ \Rightarrow\ v=\sqrt{\dfrac{2W}{m}}=\sqrt{\dfrac{2\cdot0{,}9}{0{,}2}}=\sqrt{9}"), A(r"v_{max}=3\ \text{m/s}")]),
  ("Tốc độ khi $\\alpha=30^\\circ$", [M(r"v=\sqrt{2gl(\cos\alpha-\cos\alpha_0)}=\sqrt{2\cdot10\cdot0{,}9\,(\cos30^\circ-\cos60^\circ)}"), M(r"v=\sqrt{18\cdot0{,}366}=\sqrt{6{,}59}"), A(r"v\approx2{,}57\ \text{m/s}")]),
  ("Kiểm tra", [P("Cách 2: $W_t=mgl(1-\\cos30^\\circ)=2\\cdot0{,}134\\cdot0{,}9\\approx0{,}241\\ \\text{J}$; $W_{\\text{đ}}=0{,}9-0{,}241=0{,}659\\ \\text{J}$; $v=\\sqrt{\\dfrac{2\\cdot0{,}659}{0{,}2}}\\approx2{,}57\\ \\text{m/s}$ ✓"),
                P("$2{,}57\\lt3$: gần biên thì chậm hơn ở đáy ✓"),
                P("Nếu dùng góc nhỏ: $\\dfrac{1}{2}mgl\\alpha_0^2=\\dfrac{1}{2}\\cdot0{,}2\\cdot10\\cdot0{,}9\\cdot1{,}047^2\\approx0{,}99\\ \\text{J}$, lệch $10\\%$ so với $0{,}9\\ \\text{J}$ nên không dùng được.")])],
  ["a) $W=0{,}9\\ \\text{J}$", "b) $v_{max}=3\\ \\text{m/s}$", "c) $v\\approx2{,}57\\ \\text{m/s}$"],
  "Nhận dạng: đề cho <strong>con lắc đơn, góc lệch lớn</strong> → mốc ở đáy, $h=l(1-\\cos\\alpha)$, tốc độ theo hiệu hai $\\cos$."),
 sol(R_T, [
  ("Cơ năng", [P("Tại giao điểm $W_{\\text{đ}}=W_t=45\\ \\text{mJ}$, mà $W=W_{\\text{đ}}+W_t$:"), M(r"W=45+45=90\ \text{mJ}"), A(r"W=0{,}09\ \text{J}")]),
  ("Chu kì", [P("Hai giao điểm liên tiếp ở $t=0{,}05\\ \\text{s}$ và $t=0{,}15\\ \\text{s}$ cách nhau $\\dfrac{T}{4}$:"), M(r"\dfrac{T}{4}=0{,}15-0{,}05=0{,}1\ \text{s}"), A(r"T=0{,}4\ \text{s}")]),
  ("Độ cứng", [M(r"\omega=\dfrac{2\pi}{T}=5\pi\ \text{rad/s}"), M(r"k=m\omega^2=0{,}2\cdot25\pi^2=0{,}2\cdot250"), A(r"k=50\ \text{N/m}")]),
  ("Biên độ", [M(r"W=\dfrac{1}{2}kA^2\ \Rightarrow\ A=\sqrt{\dfrac{2W}{k}}=\sqrt{\dfrac{2\cdot0{,}09}{50}}=\sqrt{0{,}0036}"), A(r"A=0{,}06\ \text{m}=6\ \text{cm}")]),
  ("Tốc độ cực đại", [P("Qua VTCB toàn bộ cơ năng là động năng:"), M(r"v_{max}=\sqrt{\dfrac{2W}{m}}=\sqrt{\dfrac{2\cdot0{,}09}{0{,}2}}=\sqrt{0{,}9}"), A(r"v_{max}\approx0{,}95\ \text{m/s}")]),
  ("Kiểm tra", [P("$\\omega A=5\\pi\\cdot0{,}06\\approx0{,}94\\ \\text{m/s}$, khớp (chênh nhỏ do $\\pi^2=10$ là xấp xỉ) ✓"),
                P("Đồ thị: $W_t$ cực đại $90\\ \\text{mJ}=W$ ở $t=0$ (vật ở biên) ✓")])],
  ["a) $W=0{,}09\\ \\text{J}$ · $T=0{,}4\\ \\text{s}$", "b) $k=50\\ \\text{N/m}$ · $A=6\\ \\text{cm}$", "c) $v_{max}\\approx0{,}95\\ \\text{m/s}$"],
  "Nhận dạng: đề cho <strong>đồ thị $W_{\\text{đ}}$, $W_t$ theo $t$</strong> → giao điểm cho $W=2\\cdot W_t$, hai giao điểm liên tiếp cho $T=4\\cdot$ khoảng cách."),
]

# ───────────────────────── Tự giải từng bước ─────────────────────────
STEPS = [
 dict(nhan_dang="Đề cho <b>biên độ</b> và <b>li độ</b> rồi hỏi <b>động năng</b> hay <b>tốc độ</b> → $W$ theo $A$, $W_t$ theo $x$, lấy hiệu.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Cơ năng", "Cơ năng $W$ của con lắc bằng bao nhiêu (J)?", 0.45, "J", 0.01,
       loi="Để nguyên $A=15$ (cm) rồi bình phương: ra số lớn gấp $10^4$ lần. Phải đổi $A=0{,}15$ m và $m=0{,}4$ kg trước."),
  buoc("Thế năng và động năng tại $x$", "Động năng tại $x=-9$ cm bằng bao nhiêu (J)?", 0.288, "J", 0.005,
       loi="Dùng $A$ thay cho $x$ trong $W_t$ thì $W_t=W$, $W_{\\text{đ}}=0$; hoặc lấy $W_{\\text{đ}}=\\dfrac{1}{2}kx^2$ (đó là thế năng).",
       ke=[("Tính $W_t=\\dfrac{1}{2}kx^2$ theo li độ rồi $W_{\\text{đ}}=W-W_t$", True),
           ("$W_{\\text{đ}}=\\dfrac{1}{2}kx^2$", "Đó là công thức thế năng; động năng là phần còn lại của cơ năng."),
           ("$W_t=\\dfrac{1}{2}kA^2$ rồi $W_{\\text{đ}}=W-W_t$", "Thế năng dùng li độ $x$; dùng $A$ thì $W_t=W$ và động năng thành $0$.")]),
  buoc("Tốc độ", "Tốc độ $|v|$ tại li độ đó bằng bao nhiêu (m/s)?", 1.2, "m/s", 0.02,
       loi="Dùng $W$ thay $W_{\\text{đ}}$ sẽ ra $v_{max}$; hoặc quên đổi $m=400$ g sang kg.",
       ke=[("Từ $W_{\\text{đ}}=\\dfrac{1}{2}mv^2$ suy ra $|v|=\\sqrt{\\dfrac{2W_{\\text{đ}}}{m}}$", True),
           ("$|v|=\\sqrt{\\dfrac{2W}{m}}$", "Đó là tốc độ cực đại ở VTCB; tại $x\\ne0$ một phần cơ năng đang là thế năng."),
           ("$|v|=\\sqrt{2W_{\\text{đ}}\\,m}$", "Từ $W_{\\text{đ}}=\\dfrac{1}{2}mv^2$ phải chia cho $m$, không nhân; đơn vị cũng không ra m/s.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Đề cho <b>động năng gấp n lần thế năng</b> → $W=(n+1)W_t$, nên chia cho $\\sqrt{n+1}$ chứ không chia cho $n$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Cơ năng", "Cơ năng $W$ bằng bao nhiêu (J)?", 0.5, "J", 0.01,
       loi="Quên đổi $A=10$ cm sang m trước khi bình phương, ra $W$ lớn gấp $10^4$ lần."),
  buoc("Li độ", "Li độ $|x|$ lúc đó bằng bao nhiêu (cm)?", 2, "cm", 0.03,
       loi="Chia $A$ cho $n$ hoặc quên lấy căn: $W_t\\propto x^2$ nên tỉ số li độ là căn của tỉ số năng lượng.",
       ke=[("$W=(n+1)W_t$ nên $|x|=\\dfrac{A}{\\sqrt{n+1}}$", True),
           ("$|x|=\\dfrac{A}{n+1}$", "Thiếu căn: $W_t\\propto x^2$, tỉ số năng lượng $\\dfrac{1}{n+1}$ ứng với tỉ số li độ $\\dfrac{1}{\\sqrt{n+1}}$."),
           ("$|x|=\\dfrac{A}{\\sqrt{n}}$", "Quên phần thế năng: cơ năng gồm $n+1$ phần ($n$ phần động và $1$ phần thế), không phải $n$ phần.")]),
  buoc("Tốc độ", "Tốc độ $|v|$ lúc đó bằng bao nhiêu (m/s)?", 1.39, "m/s", 0.02,
       loi="Dùng cả cơ năng cho động năng sẽ ra $v_{max}$; hoặc lấy $W_{\\text{đ}}=24W$ thay vì $\\dfrac{24}{25}W$.",
       ke=[("$W_{\\text{đ}}=\\dfrac{n}{n+1}W$ rồi $|v|=\\sqrt{\\dfrac{2W_{\\text{đ}}}{m}}$", True),
           ("$|v|=\\sqrt{\\dfrac{2W}{m}}$ vì cơ năng không đổi", "Cơ năng không đổi nhưng chỉ phần $W_{\\text{đ}}$ nằm trong động năng; công thức này cho $v_{max}$."),
           ("$|v|=\\sqrt{\\dfrac{2W_t}{m}}$", "$W_t$ là thế năng, không phải động năng.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Đề cho <b>đồ thị năng lượng theo li độ</b> → đọc $A$ (chỗ $W_{\\text{đ}}=0$) và $W$ (đỉnh), rồi $k=\\dfrac{2W}{A^2}$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Đọc đồ thị, tìm độ cứng", "Từ đồ thị, độ cứng $k$ của lò xo bằng bao nhiêu (N/m)?", 20, "N/m", 0.5,
       loi="Thế $A=6$ (cm) và $W=36$ (mJ) thẳng vào $k=\\dfrac{2W}{A^2}$: ra $2$ N/m sai vì chưa đổi sang m và J."),
  buoc("Động năng khi $x=3$ cm", "Động năng của vật khi $x=3$ cm bằng bao nhiêu (mJ)?", 27, "mJ", 0.5,
       loi="Lấy $W_{\\text{đ}}=\\dfrac{1}{2}kx^2=9$ mJ (đó là thế năng), hoặc đọc nhầm đường $W_t$ thay cho $W_{\\text{đ}}$.",
       ke=[("$W_t=\\dfrac{1}{2}kx^2$ rồi $W_{\\text{đ}}=W-W_t$", True),
           ("$W_{\\text{đ}}=\\dfrac{1}{2}kx^2$", "Đó là thế năng; tại $x$ động năng là phần còn lại của $W$."),
           ("$W_{\\text{đ}}=W\\cdot\\dfrac{x}{A}$", "Năng lượng tỉ lệ với bình phương li độ, không tỉ lệ bậc nhất.")]),
  buoc("Tốc độ", "Tốc độ $|v|$ khi $x=3$ cm bằng bao nhiêu (m/s)?", 0.6, "m/s", 0.01,
       loi="Quên đổi mJ sang J (ra $v$ lớn gấp $\\sqrt{1000}$ lần) hoặc quên đổi $m=150$ g sang kg.",
       ke=[("$|v|=\\sqrt{\\dfrac{2W_{\\text{đ}}}{m}}$ với $W_{\\text{đ}}$ đổi ra J", True),
           ("$|v|=\\sqrt{\\dfrac{2W}{m}}$", "Đó là $v_{max}$ ở VTCB, không phải tốc độ khi $x=3$ cm."),
           ("$|v|=\\dfrac{2W_{\\text{đ}}}{m}$", "Thiếu dấu căn: đó là $v^2$, đơn vị không phải m/s.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>con lắc đơn, góc lệch lớn</b> → mốc ở đáy, $h=l(1-\\cos\\alpha)$, tốc độ theo hiệu hai $\\cos$.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Độ cao của biên", "Biên cao hơn vị trí thấp nhất bao nhiêu mét?", 0.45, "m", 0.01,
       loi="Lấy $h_0=l\\cos\\alpha_0$ (đó là phần chiếu của dây) thay vì $l(1-\\cos\\alpha_0)$."),
  buoc("Cơ năng", "Cơ năng $W$ của con lắc bằng bao nhiêu (J)?", 0.9, "J", 0.02,
       loi="Quên đổi $m=200$ g sang kg, hoặc dùng $W\\approx\\dfrac{1}{2}mgl\\alpha_0^2$ với góc $60^\\circ$ (không phải góc nhỏ).",
       ke=[("Tại biên $v=0$ nên $W=W_t=mgh_0$", True),
           ("$W=\\dfrac{1}{2}mgl\\alpha_0^2$ với $\\alpha_0=60$", "Công thức góc nhỏ đòi $\\alpha_0$ bằng rad và dưới khoảng $10^\\circ$; $60^\\circ$ không thoả."),
           ("$W=mgl$", "Đó là thế năng ở độ cao $l$ so với đáy; biên chỉ cao $h_0=l(1-\\cos\\alpha_0)$.")]),
  buoc("Tốc độ khi qua VTCB", "Tốc độ khi qua VTCB bằng bao nhiêu (m/s)?", 3, "m/s", 0.05,
       loi="Quên lấy căn (giữ nguyên $v^2$) hoặc quên nhân đôi trong $\\dfrac{1}{2}mv^2=W$.",
       ke=[("Ở đáy $W_t=0$ nên $\\dfrac{1}{2}mv^2=W$", True),
           ("$mv=W$", "Đơn vị không phù hợp; động năng là $\\dfrac{1}{2}mv^2$."),
           ("$v=\\sqrt{2gl}$", "Ứng với biên cao $l$ so với đáy (thả từ phương ngang); ở đây biên chỉ cao $h_0$.")]),
  buoc("Tốc độ khi $\\alpha=30^\\circ$", "Tốc độ khi dây lệch $30^\\circ$ bằng bao nhiêu (m/s)?", 2.57, "m/s", 0.03,
       loi="Dùng $\\cos\\alpha_0-\\cos\\alpha$ (đảo dấu, ra số âm) hoặc viết $1-\\cos\\alpha$ thay cho hiệu hai $\\cos$.",
       ke=[("$v=\\sqrt{2gl(\\cos\\alpha-\\cos\\alpha_0)}$", True),
           ("$v=\\sqrt{2gl(1-\\cos\\alpha)}$", "Đó là tốc độ ở đáy khi thả từ góc $\\alpha$, không phải tốc độ tại góc $\\alpha$ khi thả từ $\\alpha_0$: phải dùng hiệu hai $\\cos$."),
           ("$v=\\sqrt{2gl(\\cos\\alpha_0-\\cos\\alpha)}$", "Đảo dấu: $\\cos30^\\circ\\gt\\cos60^\\circ$ nên biểu thức dưới căn sẽ âm.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>đồ thị $W_{\\text{đ}}$, $W_t$ theo thời gian</b> → giao điểm cho $W=2W_t$, hai giao điểm liên tiếp cho $T$.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Cơ năng", "Cơ năng $W$ bằng bao nhiêu (mJ)?", 90, "mJ", 1,
       loi="Lấy luôn $W=45$ mJ (đó chỉ là mỗi loại năng lượng tại giao điểm)."),
  buoc("Chu kì", "Chu kì dao động $T$ bằng bao nhiêu (s)?", 0.4, "s", 0.01,
       loi="Lấy khoảng cách hai giao điểm làm chu kì ($0{,}1$ s), hoặc làm chu kì năng lượng $\\dfrac{T}{2}$ thành $T$.",
       ke=[("Hai giao điểm liên tiếp cách $\\dfrac{T}{4}$", True),
           ("Hai giao điểm liên tiếp cách đúng một chu kì $T$", "Mỗi chu kì có $4$ giao điểm nên hai giao điểm liên tiếp cách $\\dfrac{T}{4}$."),
           ("Hai giao điểm liên tiếp cách $\\dfrac{T}{2}$", "$\\dfrac{T}{2}$ là chu kì của đồ thị năng lượng, không phải khoảng giữa hai giao điểm.")]),
  buoc("Độ cứng", "Độ cứng $k$ của lò xo bằng bao nhiêu (N/m)?", 50, "N/m", 1,
       loi="Quên $\\omega=\\dfrac{2\\pi}{T}$ hoặc quên bình phương $\\omega$; $m$ phải đổi ra kg.",
       ke=[("$\\omega=\\dfrac{2\\pi}{T}$ rồi $k=m\\omega^2$", True),
           ("$k=m\\omega=m\\dfrac{2\\pi}{T}$", "Thiếu bình phương: $\\omega=\\sqrt{\\dfrac{k}{m}}$ nên $k=m\\omega^2$."),
           ("$k=\\dfrac{4\\pi^2 T^2}{m}$", "Đảo ngược: từ $T=2\\pi\\sqrt{\\dfrac{m}{k}}$ suy ra $k=\\dfrac{4\\pi^2m}{T^2}$.")]),
  buoc("Biên độ", "Biên độ $A$ bằng bao nhiêu (cm)?", 6, "cm", 0.1,
       loi="Quên đổi $W=90$ mJ sang J, hoặc quên căn bậc hai trong $A=\\sqrt{\\dfrac{2W}{k}}$.",
       ke=[("$W=\\dfrac{1}{2}kA^2$ nên $A=\\sqrt{\\dfrac{2W}{k}}$", True),
           ("$A=\\dfrac{2W}{k}$", "Thiếu dấu căn: $W\\propto A^2$."),
           ("$A=\\sqrt{\\dfrac{W}{k}}$", "Thiếu hệ số $2$: $W=\\dfrac{1}{2}kA^2$.")]),
  buoc("Tốc độ cực đại", "Tốc độ cực đại $v_{max}$ bằng bao nhiêu (m/s)?", 0.95, "m/s", 0.02,
       loi="Dùng $A$ theo cm trong $\\omega A$ (kết quả lớn gấp $100$ lần) hoặc quên căn trong $\\sqrt{\\dfrac{2W}{m}}$.",
       ke=[("Qua VTCB toàn bộ cơ năng là động năng: $v_{max}=\\sqrt{\\dfrac{2W}{m}}$", True),
           ("$v_{max}=\\sqrt{\\dfrac{2W}{k}}$", "Đó là biên độ $A$ (đơn vị m), không phải tốc độ."),
           ("$v_{max}=\\dfrac{W}{m}$", "Thiếu hệ số $2$ và dấu căn: $\\dfrac{1}{2}mv_{max}^2=W$.")]),
  buoc("Kiểm tra")]),
]

d = {"lesson_id": 26, "lesson_title": "Bài 7. Bài tập về sự chuyển hoá năng lượng trong dao động điều hoà", "generated_at": "2026-10-09",
     "review": {"checked": True, "notes": "kiểm chéo 9/10: 5 dạng đúng, buoc[] khớp, hình ổn"},
     "dang_bai": [dict(form="bai_tap", solution_html="", **x) for x in DANG]}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
