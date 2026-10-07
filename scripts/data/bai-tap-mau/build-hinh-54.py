"""Bài 54 · Chuyển động thẳng biến đổi đều — soạn 6 dạng, dựng mô phỏng + phân tích + lời giải, ghi scripts/data/bai-tap-mau/54.json.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-54.py   (đọc old/54.json; ghi đè 54.json, review.checked=False)"""
import json, math, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "54.json")
ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
PUR = "#a78bfa"

TOPICS = {t["id"]: t["name"] for t in json.load(open(os.path.join(ROOT, "scripts/data/question-topics.json"))) if t["lesson_id"] == 54}
T_CT, T_DT, T_PHANH = TOPICS[113], TOPICS[112], TOPICS[114]

# ───────────── helper dùng riêng cho bài 54 ─────────────
def vehicle(xf, gy, w=40, c="currentColor", wheels=2):
    """Xe/đoàn tàu nhìn nghiêng, mũi quay phải: mũi tại xf, bánh chạm đường y=gy."""
    s = f'<rect x="{xf - w:.1f}" y="{gy - 19:.1f}" width="{w}" height="13" rx="3" fill="none" stroke="{c}" stroke-width="2.2"/>'
    s += f'<path d="M{xf - w * 0.62:.1f},{gy - 19:.1f} l5,-8 h{w * 0.28:.1f} l5,8" fill="none" stroke="{c}" stroke-width="2.2"/>'
    for i in range(wheels):
        cx = xf - w + 9 + i * ((w - 18) / max(wheels - 1, 1))
        s += f'<circle cx="{cx:.1f}" cy="{gy - 4.5:.1f}" r="4.5" fill="none" stroke="{c}" stroke-width="2.2"/>'
    return s

def move_g(content, dxs, dur):
    vals = ";".join(f"{d:.2f} 0" for d in dxs)
    return (f'<g><animateTransform attributeName="transform" type="translate" values="{vals}" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>{content}</g>')

def varrow(p, c, xs, y, lens, dur):
    """Mũi tên vận tốc chạy theo xe (xs: x mũi xe theo mẫu; lens: độ dài mũi tên px theo mẫu)."""
    col = {"r": RED, "b": BLUE, "o": ORG, "g": GRN}[c]
    return (f'<line y1="{y}" y2="{y}" stroke="{col}" stroke-width="3" marker-end="url(#{p}-{c})" x1="{xs[0]:.1f}" x2="{xs[0] + lens[0]:.1f}">'
            f'{smil("x1", xs, dur)}{smil("x2", [x + l for x, l in zip(xs, lens)], dur)}</line>')

def ruler(x0, x1, y, step_px, labels, size=12):
    s = seg(x0 - 10, y, x1, y, "currentColor", 2)
    for i, lab in enumerate(labels):
        x = x0 + i * step_px
        s += seg(x, y, x, y + 6, "currentColor", 1.6) + lbl(x, y + 20, lab, "currentColor", size, "middle", "400")
    return s

def samp(f, T, n):
    return [f(T * i / n) for i in range(n + 1)]

# ───────────── Dạng 1: đoàn tàu tăng tốc, v0=20, a=0,5, t=30 ─────────────
def d1(k):
    p = f"d1{k}"; x0 = 30; sx = 0.36; gy = 100
    d = lambda t: 20 * t + 0.25 * t * t
    b = defs(p) + ruler(x0, 410, gy, 200 * sx, ["0", "200", "400", "600", "800 m"])
    if k == 0:
        n = 60; T = 30; dur = T / 3
        xs = [x0 + sx * d(T * i / n) for i in range(n + 1)]
        lens = [2 * (20 + 0.5 * T * i / n) for i in range(n + 1)]
        b += move_g(vehicle(x0, gy, 64, "currentColor", 3), [x - x0 for x in xs], dur)
        b += varrow(p, "r", xs, 62, lens, dur)
        b += lbl(x0 - 14, 46, "v₀ = 20 m/s", RED, 13, "start", "700") + lbl(212, 28, "a = 0,5 m/s²  (không đổi)", "currentColor", 13, "start", "400")
        b += lbl(212, 46, "sau t = 30 s:  v = ?  d = ?", ORG, 13, "start", "700")
        return fig("d1-0", "0 0 420 140", "Đoàn tàu đang chạy với vận tốc 20 m/s tăng tốc đều với gia tốc 0,5 m/s² trong 30 s; mũi tên vận tốc dài dần", b,
                   "Mô phỏng: tàu tăng tốc đều, mũi tên đỏ là vận tốc (chạy nhanh 3 lần, 10 s thay vì 30 s; bấm Chạy mô phỏng). Vị trí tính theo công thức.")
    xe = x0 + sx * d(30)
    b += vehicle(x0, gy, 64, "currentColor", 3) + vehicle(xe, gy, 64, GRN, 3)
    b += seg(x0, gy - 30, xe, gy - 30, "currentColor", 1.2, "4 4", .6)
    b += dim(p, "b", x0, gy - 40, xe, gy - 40, "d = v₀t + ½at²", (x0 + xe) / 2 - 52, gy - 48)
    b += arrow(p, "r", x0, 62, x0 + 40, 62, 3) + lbl(x0 + 46, 66, "v₀", RED, 13, "start", "700")
    b += arrow(p, "r", xe, 62, xe + 70, 62, 3) + lbl(xe + 10, 50, "v = v₀ + at", RED, 13, "start", "700")
    b += lbl(30, 28, "Chiều dương = chiều chạy của tàu", "currentColor", 12, "start", "400")
    return fig("d1-2", "0 0 420 140", "Vị trí đầu và cuối của đoàn tàu; độ dịch chuyển tính từ v₀, a, t và vận tốc cuối tính từ v₀ + at", b, "Dữ kiện: hai công thức cần dùng. " + NOTE)

# ───────────── Dạng 2: đồ thị v–t, (0;4) (6;16) (10;16) (14;0) ─────────────
GT0, GV0, KT, KV = 56, 196, 24.3, 7.5
def gx(t): return GT0 + KT * t
def gy_(v): return GV0 - KV * v
PTS2 = [(0, 4), (6, 16), (10, 16), (14, 0)]
def v2(t):
    if t <= 6: return 4 + 2 * t
    if t <= 10: return 16
    return 16 - 4 * (t - 10)

def graph_base(p):
    b = defs(p) + arrow(p, "g", GT0, GV0, 404, GV0, 2) + arrow(p, "g", GT0, GV0, GT0, 34, 2)
    b += lbl(412, GV0 - 8, "t (s)", GRN, 13, "end", "700") + lbl(GT0 + 8, 30, "v (m/s)", GRN, 13, "start", "700")
    for t in range(2, 15, 2):
        b += seg(gx(t), GV0, gx(t), GV0 + 5, "currentColor", 1.4) + lbl(gx(t), GV0 + 19, str(t), "currentColor", 12, "middle", "400")
    for v in (4, 8, 12, 16, 20):
        b += seg(GT0 - 5, gy_(v), GT0, gy_(v), "currentColor", 1.4) + lbl(GT0 - 8, gy_(v) + 4, str(v), "currentColor", 12, "end", "400")
    return b

def d2(k):
    p = f"d2{k}"; b = graph_base(p)
    line = poly([(gx(t), gy_(v)) for t, v in PTS2], RED, 2.6)
    if k == 0:
        b += line
        for t, v in PTS2:
            b += seg(gx(t), gy_(v), gx(t), GV0, "currentColor", 1, "3 4", .5) + seg(GT0, gy_(v), gx(t), gy_(v), "currentColor", 1, "3 4", .5) + dot(gx(t), gy_(v), 3.5, RED)
        n = 56; T = 14; dur = T / 2
        X = [gx(T * i / n) for i in range(n + 1)]; Y = [gy_(v2(T * i / n)) for i in range(n + 1)]
        b += (f'<line stroke="{ORG}" stroke-width="2" stroke-dasharray="4 4" x1="{X[0]:.1f}" x2="{X[0]:.1f}" y1="{Y[0]:.1f}" y2="{GV0}">'
              f'{smil("x1", X, dur)}{smil("x2", X, dur)}{smil("y1", Y, dur)}</line>')
        b += (f'<circle cx="{X[0]:.1f}" cy="{Y[0]:.1f}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">{smil("cx", X, dur)}{smil("cy", Y, dur)}</circle>')
        b += lbl(236, 70, "a = ?  (mỗi giai đoạn)", ORG, 13, "start", "700") + lbl(236, 90, "quãng đường 14 s = ?", ORG, 13, "start", "700")
        return fig("d2-0", "0 0 420 232", "Đồ thị vận tốc theo thời gian gồm ba đoạn: tăng đều từ 4 lên 16 m/s trong 6 s, giữ 16 m/s đến 10 s, giảm đều về 0 lúc 14 s; điểm chạy trên đồ thị", b,
                   "Đồ thị v – t của xe (đề cho); điểm xanh là xe tại từng thời điểm, đúng đồ thị (chạy nhanh 2 lần, 7 s; bấm Chạy mô phỏng).")
    b += (f'<polygon points="{gx(0):.1f},{GV0} {gx(0):.1f},{gy_(4):.1f} {gx(6):.1f},{gy_(16):.1f} {gx(6):.1f},{GV0}" fill="{ORG}" opacity=".28"/>'
          f'<polygon points="{gx(6):.1f},{GV0} {gx(6):.1f},{gy_(16):.1f} {gx(10):.1f},{gy_(16):.1f} {gx(10):.1f},{GV0}" fill="{BLUE}" opacity=".28"/>'
          f'<polygon points="{gx(10):.1f},{GV0} {gx(10):.1f},{gy_(16):.1f} {gx(14):.1f},{GV0}" fill="{GRN}" opacity=".28"/>')
    b += line
    b += lbl(gx(3), gy_(2.5), "hình thang", ORG, 12, "middle", "700") + lbl(gx(8), gy_(6), "chữ nhật", BLUE, 12, "middle", "700") + lbl(gx(11.6), gy_(3), "tam giác", GRN, 12, "middle", "700")
    b += seg(gx(0), gy_(4), gx(6), gy_(4), RED, 1.8, "5 4") + seg(gx(6), gy_(4), gx(6), gy_(16), RED, 1.8, "5 4")
    b += lbl(gx(3), gy_(4) - 6, "Δt", RED, 13, "middle", "700") + lbl(gx(6) + 6, gy_(10) + 4, "Δv", RED, 13, "start", "700")
    b += lbl(236, 60, "a = Δv / Δt  (độ dốc)", RED, 13, "start", "700") + lbl(236, 80, "d = diện tích dưới đồ thị", "currentColor", 13, "start", "700")
    return fig("d2-2", "0 0 420 232", "Đồ thị chia làm ba phần: hình thang, hình chữ nhật, tam giác; độ dốc từng đoạn cho gia tốc", b, "Dữ kiện: độ dốc cho a, diện tích cho d. " + NOTE)

# ───────────── Dạng 3: phanh, v0=15, vết phanh 37,5 m (a=−3, T=5) ─────────────
def d3(k):
    p = f"d3{k}"; x0 = 40; sx = 7.2; gy = 100
    d = lambda t: 15 * t - 1.5 * t * t
    xe = x0 + sx * 37.5
    b = defs(p) + seg(x0 - 20, gy, 410, gy, "currentColor", 2)
    if k == 0:
        n = 50; T = 5; dur = T * 2
        xs = [x0 + sx * d(T * i / n) for i in range(n + 1)]
        lens = [3.4 * (15 - 3 * T * i / n) + 0.01 for i in range(n + 1)]
        b += move_g(vehicle(x0, gy, 40, "currentColor", 2), [x - x0 for x in xs], dur)
        b += varrow(p, "r", xs, 60, lens, dur)
        b += dim(p, "b", x0, gy + 22, xe, gy + 22, "vết phanh 37,5 m", (x0 + xe) / 2 - 56, gy + 42)
        b += seg(xe, gy, xe, gy + 28, "currentColor", 1.2, "3 3", .6)
        b += lbl(x0 - 26, 44, "v₀ = 54 km/h", RED, 13, "start", "700") + lbl(262, 44, "a = ?   t phanh = ?", ORG, 13, "start", "700")
        return fig("d3-0", "0 0 420 156", "Xe máy chạy 54 km/h phanh gấp, để lại vết phanh dài 37,5 m rồi dừng; mũi tên vận tốc ngắn dần", b,
                   "Mô phỏng: xe phanh đều tới dừng (chạy chậm 2 lần; bấm Chạy mô phỏng). Quãng đường tính theo công thức.")
    b += vehicle(x0, gy, 40, "currentColor", 2) + vehicle(xe, gy, 40, GRN, 2)
    b += arrow(p, "r", x0, 60, x0 + 50, 60, 3) + lbl(x0 + 56, 64, "v₀ = 15 m/s", RED, 13, "start", "700")
    b += lbl(xe - 36, 56, "v = 0", GRN, 13, "start", "700")
    b += dim(p, "b", x0, gy + 22, xe, gy + 22, "d = 37,5 m", (x0 + xe) / 2 - 40, gy + 42)
    b += lbl(230, 28, "v² − v₀² = 2ad  (không có t)", ORG, 13, "start", "700")
    return fig("d3-2", "0 0 420 156", "Xe từ vận tốc v₀ dừng sau quãng đường d; công thức không chứa thời gian nối v₀, v, a và d", b, "Dữ kiện: đổi 54 km/h sang m/s trước khi thế. " + NOTE)

# ───────────── Dạng 4: giây thứ n, v0=3, a=2 ─────────────
def d4(k):
    p = f"d4{k}"; x0 = 30; sx = 3.7; gy = 96
    x = lambda t: x0 + sx * (3 * t + t * t)
    b = defs(p) + seg(x0 - 14, gy, 400, gy, "currentColor", 2)
    for t in range(0, 9 if k else 6):
        b += dot(x(t), gy, 3.5, "currentColor") + lbl(x(t), gy + 20, str(t), "currentColor", 12, "middle", "400")
    b += lbl(402, gy + 20, "t (s)", "currentColor", 12, "end", "400")
    def bracket(t1, t2, y, c, txt, ly):
        return (seg(x(t1), y, x(t2), y, c, 3) + seg(x(t1), y - 5, x(t1), y + 5, c, 2) + seg(x(t2), y - 5, x(t2), y + 5, c, 2)
                + lbl((x(t1) + x(t2)) / 2, ly, txt, c, 13, "middle", "700"))
    if k == 0:
        n = 64; T = 8; dur = T
        X = [x(T * i / n) for i in range(n + 1)]
        b += bracket(4, 5, 70, ORG, "giây thứ 5: 12 m", 54) + lbl(x(7.5), 54, "giây thứ 8: ? m", RED, 13, "middle", "700")
        b += lbl(x0 - 6, 28, "v₀ = 3 m/s, nhanh dần đều, a = ?", "currentColor", 13, "start", "700")
        b += f'<circle cx="{X[0]:.1f}" cy="{gy - 9}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">{smil("cx", X, dur)}</circle>'
        return fig("d4-0", "0 0 420 128", "Vật chuyển động nhanh dần đều từ vận tốc 3 m/s; các chấm đánh dấu vị trí sau mỗi giây; giây thứ 5 đi được 12 m, cần tìm quãng đường giây thứ 8", b,
                   "Mô phỏng: vật chạy dọc thước, chấm đánh dấu từng giây (đúng thời gian thật, 8 s; bấm Chạy mô phỏng). Vị trí tính theo công thức.")
    b += bracket(4, 5, 70, ORG, "s₅ − s₄", 54) + bracket(7, 8, 70, RED, "s₈ − s₇", 54)
    b += lbl(x0 - 6, 16, "giây thứ n = khoảng từ (n − 1) đến n", "currentColor", 13, "start", "700")
    b += lbl(x0 - 6, 34, "Δsₙ = sₙ − sₙ₋₁", ORG, 13, "start", "700")
    return fig("d4-2", "0 0 420 128", "Giây thứ 5 là khoảng từ giây 4 đến giây 5, quãng đường trong giây đó bằng hiệu hai quãng đường s5 và s4", b, "Dữ kiện: quãng đường giây thứ n là hiệu hai quãng đường tích luỹ. " + NOTE)

# ───────────── Dạng 5: dốc 64 m (8 s) rồi mặt ngang 32 m dừng ─────────────
KK = 4.0; ANG = math.radians(28)
A5 = (24, 36); B5 = (A5[0] + KK * 64 * math.cos(ANG), A5[1] + KK * 64 * math.sin(ANG)); C5 = (B5[0] + KK * 32, B5[1])
def s5(t):
    if t <= 8: return t * t
    u = t - 8; return 64 + 16 * u - 2 * u * u
def pos5(s):
    if s <= 64:
        return (A5[0] + KK * s * math.cos(ANG) + 6 * math.sin(ANG), A5[1] + KK * s * math.sin(ANG) - 6 * math.cos(ANG))
    return (B5[0] + KK * (s - 64), B5[1] - 6)

def d5(k):
    p = f"d5{k}"
    b = defs(p) + poly([A5, B5, C5], "currentColor", 2.6) + dot(*A5, 3.5) + dot(*B5, 3.5) + dot(*C5, 3.5)
    b += lbl(A5[0] - 4, A5[1] - 8, "A", "currentColor", 13, "start", "700") + lbl(B5[0] - 4, B5[1] + 20, "B", "currentColor", 13, "start", "700") + lbl(C5[0] + 2, C5[1] + 20, "C", "currentColor", 13, "start", "700")
    if k == 0:
        n = 72; T = 12; dur = T / 2
        P = [pos5(s5(T * i / n)) for i in range(n + 1)]
        b += lbl(150, 40, "dốc AB dài 64 m, thả từ nghỉ", "currentColor", 13, "start", "700") + lbl(150, 58, "đến chân dốc B sau 8 s", "currentColor", 13, "start", "700")
        b += dim(p, "b", B5[0], B5[1] + 30, C5[0], C5[1] + 30, "BC = 32 m, dừng ở C", B5[0] - 4, B5[1] + 52)
        b += lbl(250, 96, "a₁, v_B, a₂, t₂ = ?", ORG, 13, "start", "700")
        b += (f'<circle cx="{P[0][0]:.1f}" cy="{P[0][1]:.1f}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">'
              f'{smil("cx", [q[0] for q in P], dur)}{smil("cy", [q[1] for q in P], dur)}</circle>')
        return fig("d5-0", "0 0 420 212", "Quả cầu lăn từ nghỉ xuống dốc dài 64 m trong 8 s rồi lăn trên mặt ngang 32 m thì dừng", b,
                   "Mô phỏng: quả cầu lăn xuống dốc rồi dừng trên mặt ngang (chạy nhanh 2 lần, 6 s; bấm Chạy mô phỏng). Vị trí tính theo công thức.")
    b += poly([A5, B5], ORG, 4) + poly([B5, C5], BLUE, 4) + dot(*B5, 4.5, "currentColor")
    b += lbl(150, 38, "① dốc: v_A = 0 → v_B", ORG, 13, "start", "700") + lbl(150, 58, "d₁ = 64 m, t₁ = 8 s", ORG, 13, "start", "400")
    b += lbl(256, 118, "② ngang: v_B → v_C = 0", BLUE, 13, "start", "700") + lbl(256, 136, "d₂ = 32 m", BLUE, 13, "start", "400")
    b += lbl(24, 120, "v_B: cuối ① = đầu ②", RED, 13, "start", "700")
    return fig("d5-2", "0 0 420 212", "Hai giai đoạn: xuống dốc từ A đến B rồi trượt trên mặt ngang từ B đến C; vận tốc tại B là cầu nối", b, "Dữ kiện: vận tốc tại B nối hai giai đoạn. " + NOTE)

# ───────────── Dạng 6: ô tô lên dốc – xe đạp xuống dốc, dốc 570 m ─────────────
F6 = (30, 196); T6 = (380, 100)
def pos6(x):
    f = x / 570; ux, uy = (T6[0] - F6[0]), (T6[1] - F6[1]); L = math.hypot(ux, uy); ux, uy = ux / L, uy / L
    return (F6[0] + (T6[0] - F6[0]) * f + uy * 9, F6[1] + (T6[1] - F6[1]) * f - ux * 9)

def d6(k):
    p = f"d6{k}"
    b = defs(p) + seg(*F6, *T6, "currentColor", 2.6) + dot(*F6, 3.5) + dot(*T6, 3.5)
    b += lbl(F6[0] - 14, F6[1] + 20, "chân dốc", "currentColor", 12, "start", "400") + lbl(T6[0] - 18, T6[1] - 10, "đỉnh dốc", "currentColor", 12, "end", "400")
    if k == 0:
        n = 60; T = 15; dur = T / 3
        x1 = lambda t: 20 * t - 0.2 * t * t; x2 = lambda t: 570 - 2 * t - 0.1 * t * t
        P1 = [pos6(x1(T * i / n)) for i in range(n + 1)]; P2 = [pos6(x2(T * i / n)) for i in range(n + 1)]
        b += lbl(16, 30, "ô tô lên dốc: v₀ = 20 m/s, chậm dần a = 0,4 m/s²", BLUE, 13, "start", "700")
        b += lbl(16, 52, "xe đạp xuống dốc: v₀ = 2 m/s, nhanh dần a = 0,2 m/s²", ORG, 13, "start", "700")
        b += lbl(214, 178, "dốc dài 570 m", "currentColor", 13, "start", "700") + lbl(214, 214, "gặp nhau lúc t = ?  tại x = ?", RED, 13, "start", "700")
        for P, c in ((P1, BLUE), (P2, ORG)):
            b += (f'<circle cx="{P[0][0]:.1f}" cy="{P[0][1]:.1f}" r="6" fill="{c}" stroke="currentColor" stroke-width="1.5">'
                  f'{smil("cx", [q[0] for q in P], dur)}{smil("cy", [q[1] for q in P], dur)}</circle>')
        return fig("d6-0", "0 0 420 232", "Ô tô lên dốc từ chân dốc và xe đạp xuống dốc từ đỉnh dốc dài 570 m, hai xe đi ngược chiều nhau", b,
                   "Mô phỏng 15 s đầu của hai xe (chạy nhanh 3 lần, 5 s; bấm Chạy mô phỏng), chưa tới chỗ gặp. Vị trí tính theo công thức.")
    e = lambda f: (F6[0] + (T6[0] - F6[0]) * f, F6[1] + (T6[1] - F6[1]) * f)
    q = (F6[0], F6[1] + 12); r_ = (T6[0], T6[1] + 12)
    b += arrow(p, "g", F6[0] + 70, F6[1] + 18, F6[0] + 160, F6[1] + 18 - 90 * (96 / 350), 2) + lbl(F6[0] + 166, F6[1] + 2, "chiều dương (x)", GRN, 13, "start", "700")
    b += lbl(16, 30, "O: x = 0 ;  xe đạp: x₀₂ = 570 m", "currentColor", 13, "start", "700")
    b += lbl(16, 52, "ô tô: v₀ > 0 → chậm dần ⇒ a₁ < 0", BLUE, 13, "start", "700")
    b += lbl(16, 74, "xe đạp: v₀ < 0 → nhanh dần ⇒ a₂ < 0", ORG, 13, "start", "700")
    b += lbl(214, 214, "gặp nhau: x₁ = x₂", RED, 13, "start", "700")
    return fig("d6-2", "0 0 420 232", "Chọn gốc ở chân dốc, chiều dương lên dốc: ô tô có vận tốc dương, xe đạp có vận tốc âm và gia tốc cùng dấu vận tốc", b, "Dữ kiện: dấu của v₀ và a theo chiều dương đã chọn. " + NOTE)

BUILD = [d1, d2, d3, d4, d5, d6]

# ───────────── Phân tích đề ─────────────
ANALYSIS = [
 [("\"đang chạy với vận tốc 20 m/s\"", "$v_0=20\\ \\text{m/s}$", "Vận tốc đầu; chọn chiều dương theo chiều chạy"),
  ("\"tăng tốc với gia tốc $0{,}5\\ \\text{m/s}^2$\"", "$a=+0{,}5\\ \\text{m/s}^2$ (cùng dấu $v_0$)", "$a\\cdot v\\gt0$: nhanh dần đều"),
  ("\"trong 30 s\"", "$t=30$ s", "⚠ $a$ không đổi suốt $t$ nên dùng được $v=v_0+at$ và $d=v_0t+\\dfrac12at^2$"),
  ("\"vận tốc … sau 30 s\"", "Cần $v$", "$v=v_0+at$"),
  ("\"quãng đường đi được\"", "Cần $s$; tàu không đổi chiều", "$d=v_0t+\\dfrac12at^2$; $s=d$")],
 [("\"đồ thị $v$–$t$ … 4 m/s … 6 s … 16 m/s\"", "$(0;4)$ và $(6;16)$", "Độ dốc đoạn thẳng là gia tốc: $a=\\dfrac{\\Delta v}{\\Delta t}$"),
  ("\"giữ nguyên … đến $t=10$ s\"", "$(6;16)$ và $(10;16)$", "Nhìn độ dốc đoạn này để suy ra loại chuyển động"),
  ("\"giảm đều đến dừng lúc $t=14$ s\"", "$(10;16)$ và $(14;0)$", "⚠ $v$ không đổi dấu nên $s=d$; nhìn độ dốc đoạn này để suy ra loại chuyển động"),
  ("\"gia tốc ở từng giai đoạn\"", "Cần $a_1,a_2,a_3$", "Tính độ dốc từng đoạn, nhìn dấu $a$ so với $v$"),
  ("\"quãng đường … trong 14 s\"", "Cần $s$", "Diện tích dưới đồ thị: hình thang + hình chữ nhật + tam giác")],
 [("\"đang chạy 54 km/h\"", "$v_0=54$ km/h", "Đổi sang m/s trước khi thế: chia $3{,}6$"),
  ("\"phanh … để lại vết phanh dài 37,5 m\"", "$d=37{,}5$ m (xe chạy thẳng một chiều)", "Không cho và không hỏi $t$: dùng $v^2-v_0^2=2ad$"),
  ("\"dừng lại\"", "$v=0$; $a\\lt0$", "⚠ Chậm dần đều: $a$ ngược dấu $v_0$; xe dừng thì đứng yên, không chạy lùi"),
  ("\"tính gia tốc và thời gian phanh\"", "Cần $a$, $t_d$", "$a=\\dfrac{v^2-v_0^2}{2d}$; $t_d=\\dfrac{v-v_0}{a}$"),
  ("\"vận tốc sau 2 s\"", "Cần $v$ tại $t=2$ s", "$v=v_0+at$ (khi $t\\lt t_d$)"),
  ("\"quãng đường trong 7 s kể từ lúc phanh\"", "Cần $s$ tại $t=7$ s", "So $t$ của đề với thời gian xe còn chuyển động được")],
 [("\"vận tốc ban đầu 3 m/s\"", "$v_0=3$ m/s", "Chiều dương theo chiều chuyển động"),
  ("\"nhanh dần đều\"", "$a$ chưa biết, không đổi", "⚠ $a$ không đổi nên dùng $s_t=v_0t+\\dfrac12at^2$ cho mọi $t$"),
  ("\"trong giây thứ 5 đi được 12 m\"", "Khoảng $t$ từ $4$ s đến $5$ s: $\\Delta s_5=12$ m", "$\\Delta s_n=s_n-s_{n-1}$ (giây thứ $n$ là khoảng $n-1\\to n$)"),
  ("\"gia tốc\"", "Cần $a$", "Lập phương trình ẩn $a$ từ $\\Delta s_5=s_5-s_4$"),
  ("\"quãng đường trong giây thứ 8\"", "Cần $\\Delta s_8$", "$\\Delta s_8=s_8-s_7$")],
 [("\"lăn từ nghỉ xuống dốc dài 64 m trong 8 s\"", "$v_A=0$; $d_1=64$ m; $t_1=8$ s", "Giai đoạn ①: $d_1=\\dfrac12a_1t_1^2$"),
  ("\"vận tốc ở chân dốc\"", "Cần $v_B$", "$v_B=v_A+a_1t_1$ ($v_B$ nối hai giai đoạn)"),
  ("\"lăn tiếp trên mặt ngang 32 m thì dừng\"", "$v_B$ là vận tốc đầu; $v_C=0$; $d_2=32$ m", "⚠ Giai đoạn ② có gia tốc riêng $a_2$: dùng $v_C^2-v_B^2=2a_2d_2$"),
  ("\"gia tốc … thời gian trên mặt ngang\"", "Cần $a_2$, $t_2$", "$a_2=\\dfrac{v_C^2-v_B^2}{2d_2}$; $t_2=\\dfrac{v_C-v_B}{a_2}$"),
  ("\"vận tốc trung bình trên cả quãng đường\"", "Tổng quãng, tổng thời gian", "$v_{tb}=\\dfrac{d_1+d_2}{t_1+t_2}$")],
 [("\"ô tô lên dốc … 20 m/s … chậm dần đều, gia tốc 0,4\"", "$x_{01}=0$; cần xác định dấu $v_{01}$, $a_1$", "$x_1=x_{01}+v_{01}t+\\dfrac12a_1t^2$"),
  ("\"xe đạp xuống dốc … 2 m/s … nhanh dần đều, gia tốc 0,2\"", "$x_{02}=570$ m; cần xác định dấu $v_{02}$, $a_2$", "⚠ Chọn MỘT chiều dương cho cả hai xe; dấu của $v_{02}$ và $a_2$ đọc theo chiều đó"),
  ("\"cùng lúc … dốc dài 570 m\"", "Một gốc toạ độ, một gốc thời gian; $x_{02}=570$", "⚠ Nghiệm $t$ phải dương và xe còn chuyển động theo chiều cũ"),
  ("\"xác định vị trí hai xe gặp nhau\"", "Cần $t$, $x$", "Gặp nhau: $x_1=x_2$ → phương trình bậc hai theo $t$"),
  ("\"vận tốc mỗi xe lúc gặp nhau\"", "Cần $v_1$, $v_2$", "$v=v_0+at$ cho từng xe, giữ dấu")],
]

# ───────────── Lời giải ─────────────
RECALL1 = ["<strong>Khái niệm:</strong> chuyển động thẳng biến đổi đều, $a$ không đổi; $a\\cdot v\\gt0$ nhanh dần, $a\\cdot v\\lt0$ chậm dần.",
           "<strong>Vận tốc:</strong> $v=v_0+at$",
           "<strong>Độ dịch chuyển:</strong> $d=v_0t+\\dfrac12at^2=\\dfrac{v_0+v}{2}\\,t$",
           "⚠ <strong>Điều kiện:</strong> $a$ không đổi suốt $t$; chọn chiều dương theo chiều chuyển động."]
RECALL2 = ["<strong>Khái niệm:</strong> trên đồ thị $v$–$t$, độ dốc là gia tốc: $a=\\dfrac{\\Delta v}{\\Delta t}$.",
           "<strong>Quan hệ:</strong> diện tích giữa đồ thị và trục $t$ là độ dịch chuyển $d$.",
           "Hình thang: $S=\\dfrac{\\text{đáy}_1+\\text{đáy}_2}{2}\\cdot\\text{cao}$; tam giác: $S=\\dfrac12\\cdot\\text{đáy}\\cdot\\text{cao}$.",
           "⚠ <strong>Điều kiện:</strong> $v$ không đổi dấu thì quãng đường $s=d$."]
RECALL3 = ["<strong>Khái niệm:</strong> phanh tới dừng: $v=0$, $a$ ngược dấu $v_0$ (chậm dần đều).",
           "Không cho và không hỏi $t$: $v^2-v_0^2=2ad$.",
           "Cần $t$: $v=v_0+at$.",
           "⚠ <strong>Điều kiện:</strong> xe dừng thì đứng yên; $t\\gt t_d$ thì $s=\\dfrac{v_0^2}{2|a|}$."]
RECALL4 = ["<strong>Khái niệm:</strong> giây thứ $n$ là khoảng thời gian từ $t=n-1$ đến $t=n$.",
           "<strong>Công thức:</strong> $s_t=v_0t+\\dfrac12at^2$.",
           "Quãng đường trong giây thứ $n$: $\\Delta s_n=s_n-s_{n-1}$.",
           "⚠ <strong>Điều kiện:</strong> $a$ không đổi; chiều dương theo chiều chuyển động."]
RECALL5 = ["<strong>Khái niệm:</strong> mỗi giai đoạn có gia tốc riêng; vận tốc cuối giai đoạn ① là vận tốc đầu giai đoạn ②.",
           "$d=v_0t+\\dfrac12at^2$ · $v=v_0+at$ · $v^2-v_0^2=2ad$",
           "Vận tốc trung bình: $v_{tb}=\\dfrac{\\text{tổng quãng đường}}{\\text{tổng thời gian}}$",
           "⚠ <strong>Điều kiện:</strong> chọn chiều dương theo chiều chuyển động cho cả hai giai đoạn."]
RECALL6 = ["<strong>Khái niệm:</strong> phương trình chuyển động $x=x_0+v_0t+\\dfrac12at^2$; dấu của $x_0,v_0,a$ đọc theo chiều dương.",
           "Gặp nhau: $x_1=x_2$. Vận tốc: $v=v_0+at$.",
           "⚠ <strong>Điều kiện:</strong> MỘT gốc toạ độ, MỘT chiều dương, MỘT gốc thời gian cho cả hai xe.",
           "Nghiệm $t$ phải dương và xe còn chuyển động theo chiều ban đầu."]

SOLS = [
 sol(RECALL1, [
  ("Chọn chiều dương và đọc dữ kiện", [P("Chiều dương theo chiều chạy của tàu:"), M(r"v_0=20\ \text{m/s}\qquad a=+0{,}5\ \text{m/s}^2\qquad t=30\ \text{s}"), P("$a$ cùng dấu $v_0$ nên tàu chạy nhanh dần đều.")]),
  ("Vận tốc sau 30 s", [M(r"v=v_0+at"), M(r"v=20+0{,}5\cdot30"), A(r"v=35\ \text{m/s}")]),
  ("Quãng đường", [M(r"d=v_0t+\dfrac{1}{2}at^2"), M(r"d=20\cdot30+\dfrac{1}{2}\cdot0{,}5\cdot30^2=600+225"), A(r"d=825\ \text{m}"), P("Tàu không đổi chiều nên $s=d$.")]),
  ("Kiểm tra", [P("Bằng vận tốc trung bình:"), M(r"d=\dfrac{v_0+v}{2}\,t=\dfrac{20+35}{2}\cdot30=825\ \text{m}"), P("$v\\gt v_0$ đúng với chuyển động nhanh dần. Đơn vị: m/s² · s = m/s ✓")])],
  ["a) $v=35\\ \\text{m/s}$", "b) $s=825\\ \\text{m}$"],
  "Nhận dạng: đề cho <strong>$v_0$, $a$, $t$</strong> và hỏi $v$ hoặc quãng đường → $v=v_0+at$ rồi $d=v_0t+\\tfrac12at^2$."),
 sol(RECALL2, [
  ("Đọc đồ thị theo ba giai đoạn", [P("① $0\\to6$ s: $v$ từ $4$ lên $16$ m/s. ② $6\\to10$ s: $v=16$ m/s. ③ $10\\to14$ s: $v$ từ $16$ về $0$.")]),
  ("Gia tốc từng giai đoạn", [M(r"a_1=\dfrac{16-4}{6-0}=+2\ \text{m/s}^2"), P("$a_1\\cdot v\\gt0$: nhanh dần đều."), M(r"a_2=\dfrac{16-16}{10-6}=0"), P("Thẳng đều."),
                              M(r"a_3=\dfrac{0-16}{14-10}=-4\ \text{m/s}^2"), P("$a_3\\lt0$ còn $v\\gt0$: chậm dần đều.")]),
  ("Quãng đường bằng diện tích", [P("$v$ không đổi dấu nên $s=d$."), M(r"d_1=\dfrac{4+16}{2}\cdot6=60\ \text{m}"), M(r"d_2=16\cdot4=64\ \text{m}"), M(r"d_3=\dfrac{1}{2}\cdot4\cdot16=32\ \text{m}"),
                                  M(r"s=60+64+32"), A(r"s=156\ \text{m}")]),
  ("Kiểm tra", [P("Giai đoạn ① bằng công thức:"), M(r"d_1=v_0t+\dfrac{1}{2}at^2=4\cdot6+\dfrac{1}{2}\cdot2\cdot6^2=60\ \text{m}"), P("Trùng với diện tích hình thang ✓")])],
  ["a) $a_1=+2$ · $a_2=0$ · $a_3=-4\\ \\text{m/s}^2$", "b) $s=156\\ \\text{m}$"],
  "Nhận dạng: đề cho <strong>đồ thị $v$–$t$</strong> → độ dốc là $a$, diện tích là $d$."),
 sol(RECALL3, [
  ("Đổi đơn vị và đọc dữ kiện", [M(r"v_0=54\ \text{km/h}=\dfrac{54}{3{,}6}=15\ \text{m/s}"), P("Chiều dương theo chiều chạy; dừng lại nên $v=0$; $d=37{,}5$ m.")]),
  ("Gia tốc", [P("Đề không cho và không hỏi $t$:"), M(r"v^2-v_0^2=2ad"), M(r"a=\dfrac{v^2-v_0^2}{2d}=\dfrac{0-15^2}{2\cdot37{,}5}"), A(r"a=-3\ \text{m/s}^2"), P("$a\\lt0$ ngược dấu $v_0$: chậm dần ✓")]),
  ("Thời gian phanh", [M(r"t_d=\dfrac{v-v_0}{a}=\dfrac{0-15}{-3}"), A(r"t_d=5\ \text{s}")]),
  ("Vận tốc sau 2 s", [P("$2\\ \\text{s}\\lt t_d$ nên xe còn chuyển động:"), M(r"v=v_0+at=15+(-3)\cdot2"), A(r"v=9\ \text{m/s}")]),
  ("Quãng đường trong 7 s", [P("$7\\ \\text{s}\\gt t_d=5\\ \\text{s}$: xe đã dừng ở giây thứ 5 và đứng yên, không chạy lùi."), M(r"s=\dfrac{v_0^2}{2|a|}=\dfrac{15^2}{2\cdot3}"), A(r"s=37{,}5\ \text{m}"),
                            P("Thế thẳng $t=7$ s sẽ ra $15\\cdot7-1{,}5\\cdot7^2=31{,}5$ m: sai, vì như xe quay đầu chạy lùi.")])],
  ["a) $a=-3\\ \\text{m/s}^2$ · $t_d=5\\ \\text{s}$", "b) $v=9\\ \\text{m/s}$", "c) $s=37{,}5\\ \\text{m}$"],
  "Nhận dạng: <strong>phanh tới dừng</strong> → tính lúc dừng $t_d$ trước, rồi so $t$ của đề với $t_d$."),
 sol(RECALL4, [
  ("Đọc dữ kiện", [P("Chiều dương theo chiều chuyển động: $v_0=3$ m/s. Giây thứ 5 là khoảng từ $t=4$ s đến $t=5$ s, $\\Delta s_5=12$ m.")]),
  ("Quãng đường đi trong 5 s và 4 s", [M(r"s_5=3\cdot5+\dfrac{1}{2}a\cdot5^2=15+12{,}5a"), M(r"s_4=3\cdot4+\dfrac{1}{2}a\cdot4^2=12+8a")]),
  ("Lập phương trình tìm $a$", [M(r"\Delta s_5=s_5-s_4=3+4{,}5a=12"), M(r"a=\dfrac{12-3}{4{,}5}"), A(r"a=2\ \text{m/s}^2")]),
  ("Quãng đường trong giây thứ 8", [M(r"s_8=3\cdot8+\dfrac{1}{2}\cdot2\cdot8^2=24+64=88\ \text{m}"), M(r"s_7=3\cdot7+\dfrac{1}{2}\cdot2\cdot7^2=21+49=70\ \text{m}"), M(r"\Delta s_8=s_8-s_7=88-70"), A(r"\Delta s_8=18\ \text{m}")]),
  ("Kiểm tra", [P("Công thức gọn cho giây thứ $n$:"), M(r"\Delta s_n=v_0+a\left(n-\dfrac{1}{2}\right)"), M(r"\Delta s_5=3+2\cdot4{,}5=12\ \text{m}\ \checkmark"), M(r"\Delta s_8=3+2\cdot7{,}5=18\ \text{m}\ \checkmark"),
                P("Nhanh dần nên giây sau đi xa hơn giây trước ($12\\lt18$) ✓")])],
  ["a) $a=2\\ \\text{m/s}^2$", "b) $\\Delta s_8=18\\ \\text{m}$"],
  "Nhận dạng: đề hỏi <strong>quãng đường trong giây thứ $n$</strong> → hiệu hai quãng đường tích luỹ $s_n-s_{n-1}$."),
 sol(RECALL5, [
  ("Giai đoạn ①: xuống dốc", [P("Chiều dương theo chiều lăn; $v_A=0$, $d_1=64$ m, $t_1=8$ s:"), M(r"d_1=\dfrac{1}{2}a_1t_1^2"), M(r"a_1=\dfrac{2d_1}{t_1^2}=\dfrac{2\cdot64}{8^2}"), A(r"a_1=2\ \text{m/s}^2")]),
  ("Vận tốc ở chân dốc", [M(r"v_B=v_A+a_1t_1=0+2\cdot8"), A(r"v_B=16\ \text{m/s}")]),
  ("Giai đoạn ②: mặt ngang", [P("$v_B$ là vận tốc đầu; dừng nên $v_C=0$; $d_2=32$ m:"), M(r"v_C^2-v_B^2=2a_2d_2"), M(r"a_2=\dfrac{0-16^2}{2\cdot32}"), A(r"a_2=-4\ \text{m/s}^2"),
                              M(r"t_2=\dfrac{v_C-v_B}{a_2}=\dfrac{0-16}{-4}"), A(r"t_2=4\ \text{s}")]),
  ("Vận tốc trung bình cả hành trình", [P("Tổng quãng đường $64+32=96$ m; tổng thời gian $8+4=12$ s:"), M(r"v_{tb}=\dfrac{d_1+d_2}{t_1+t_2}=\dfrac{96}{12}"), A(r"v_{tb}=8\ \text{m/s}")]),
  ("Kiểm tra", [P("Mỗi giai đoạn biến đổi đều nên vận tốc trung bình bằng trung bình cộng hai đầu:"), M(r"\dfrac{0+16}{2}=8\ \text{m/s}\ \ (\text{dốc})"), M(r"\dfrac{16+0}{2}=8\ \text{m/s}\ \ (\text{ngang})"), P("Cả hai bằng $8$ m/s nên cả hành trình cũng $8$ m/s ✓")])],
  ["a) $a_1=2\\ \\text{m/s}^2$ · $v_B=16\\ \\text{m/s}$", "b) $a_2=-4\\ \\text{m/s}^2$ · $t_2=4\\ \\text{s}$", "c) $v_{tb}=8\\ \\text{m/s}$"],
  "Nhận dạng: chuyển động <strong>nhiều giai đoạn</strong> → làm từng giai đoạn, lấy vận tốc cuối làm vận tốc đầu giai đoạn sau."),
 sol(RECALL6, [
  ("Chọn hệ quy chiếu", [P("Gốc toạ độ O ở chân dốc, chiều dương hướng lên đỉnh dốc, gốc thời gian lúc hai xe xuất phát.")]),
  ("Ô tô (lên dốc)", [P("$x_{01}=0$; $v_{01}=+20$ m/s; chậm dần nên $a_1$ ngược dấu $v_{01}$: $a_1=-0{,}4\\ \\text{m/s}^2$."), M(r"x_1=20t-0{,}2t^2")]),
  ("Xe đạp (xuống dốc)", [P("$x_{02}=570$ m; xuống dốc là ngược chiều dương nên $v_{02}=-2$ m/s; nhanh dần nên $a_2$ cùng dấu $v_{02}$: $a_2=-0{,}2\\ \\text{m/s}^2$."), M(r"x_2=570-2t-0{,}1t^2")]),
  ("Thời điểm gặp nhau", [M(r"x_1=x_2"), M(r"20t-0{,}2t^2=570-2t-0{,}1t^2"), M(r"t^2-220t+5700=0"), P("Nghiệm $t=30$ s hoặc $t=190$ s."),
                          P("Ô tô chỉ chuyển động theo chiều cũ tới lúc $v=0$, tức $t=\\dfrac{20}{0{,}4}=50$ s; $t=190$ s vô lí nên loại."), A(r"t=30\ \text{s}")]),
  ("Vị trí gặp nhau", [M(r"x=20\cdot30-0{,}2\cdot30^2=600-180"), A(r"x=420\ \text{m}\ \ (\text{cách chân dốc})"), P("Kiểm tra bằng xe đạp: $570-2\\cdot30-0{,}1\\cdot30^2=420$ m ✓")]),
  ("Vận tốc mỗi xe lúc gặp", [M(r"v_1=20-0{,}4\cdot30=8\ \text{m/s}"), M(r"v_2=-2-0{,}2\cdot30=-8\ \text{m/s}"), P("Dấu trừ: xe đạp đang đi xuống dốc, tốc độ $8$ m/s.")])],
  ["a) $t=30\\ \\text{s}$, cách chân dốc $420\\ \\text{m}$", "b) ô tô $8\\ \\text{m/s}$ lên dốc; xe đạp $8\\ \\text{m/s}$ xuống dốc"],
  "Nhận dạng: <strong>hai xe cùng xuất phát</strong>, hỏi lúc/nơi gặp → một hệ quy chiếu, hai phương trình $x(t)$, giải $x_1=x_2$."),
]

# ───────────── Dạng bài (đề chữ) ─────────────
DANG = [
 dict(label="Dạng 1 · Dễ · Tăng tốc đều: tìm vận tốc và quãng đường", topic=T_CT,
      problem_html="<p>Một đoàn tàu đang chạy với vận tốc $20\\ \\text{m/s}$ thì tăng tốc đều với gia tốc $0{,}5\\ \\text{m/s}^2$ trong $30\\ \\text{s}$.</p>"
                   "<ol type=\"a\"><li>Tính vận tốc của tàu sau $30\\ \\text{s}$ đó.</li><li>Tính quãng đường tàu đi được trong thời gian này.</li></ol>"),
 dict(label="Dạng 2 · Dễ · Đọc đồ thị vận tốc – thời gian: gia tốc và quãng đường", topic=T_DT,
      problem_html="<p>Một xe chuyển động thẳng theo một chiều, đồ thị vận tốc – thời gian như hình dưới đây: lúc $t=0$ có $v=4\\ \\text{m/s}$, tăng đều đến $16\\ \\text{m/s}$ lúc $t=6\\ \\text{s}$, giữ nguyên "
                   "đến $t=10\\ \\text{s}$, rồi giảm đều đến dừng lại lúc $t=14\\ \\text{s}$.</p>"
                   "<ol type=\"a\"><li>Tính gia tốc ở từng giai đoạn và cho biết xe nhanh dần, chậm dần hay chuyển động đều.</li><li>Tính quãng đường xe đi được trong $14\\ \\text{s}$.</li></ol>"),
 dict(label="Dạng 3 · Trung bình · Phanh tới dừng: gia tốc, thời gian phanh, quãng đường", topic=T_PHANH,
      problem_html="<p>Một xe máy đang chạy với tốc độ $54\\ \\text{km/h}$ thì phanh gấp và dừng lại sau khi để lại vết phanh dài $37{,}5\\ \\text{m}$. Coi chuyển động khi phanh là chậm dần đều.</p>"
                   "<ol type=\"a\"><li>Tính gia tốc và thời gian phanh.</li><li>Tính vận tốc của xe sau $2\\ \\text{s}$ kể từ lúc bắt đầu phanh.</li><li>Tính quãng đường xe đi được trong $7\\ \\text{s}$ kể từ lúc bắt đầu phanh.</li></ol>"),
 dict(label="Dạng 4 · Trung bình · Quãng đường trong giây thứ n", topic=T_CT,
      problem_html="<p>Một vật chuyển động thẳng nhanh dần đều với vận tốc ban đầu $3\\ \\text{m/s}$. Trong giây thứ $5$ (kể từ lúc bắt đầu chuyển động) vật đi được $12\\ \\text{m}$.</p>"
                   "<ol type=\"a\"><li>Tính gia tốc của vật.</li><li>Tính quãng đường vật đi được trong giây thứ $8$.</li></ol>"),
 dict(label="Dạng 5 · Khó · Chuyển động hai giai đoạn: dốc rồi mặt ngang", topic=T_CT,
      problem_html="<p>Một quả cầu bắt đầu lăn từ nghỉ ở đỉnh A của dốc dài $64\\ \\text{m}$ và đến chân dốc B sau $8\\ \\text{s}$. Sau đó nó lăn tiếp trên mặt ngang, đi thêm $32\\ \\text{m}$ từ B đến C thì dừng. "
                   "Coi mỗi giai đoạn là chuyển động biến đổi đều.</p>"
                   "<ol type=\"a\"><li>Tính gia tốc trên dốc và vận tốc của quả cầu ở chân dốc B.</li><li>Tính gia tốc và thời gian lăn trên mặt ngang BC.</li><li>Tính vận tốc trung bình của quả cầu trên cả hành trình AC (quả cầu không đổi chiều nên tốc độ trung bình bằng độ lớn vận tốc trung bình).</li></ol>"),
 dict(label="Dạng 6 · Khó · Hai xe ngược chiều trên dốc: lúc và nơi gặp nhau", topic=T_PHANH,
      problem_html="<p>Một ô tô qua chân dốc với vận tốc $20\\ \\text{m/s}$ và lên dốc, chuyển động chậm dần đều với gia tốc có độ lớn $0{,}4\\ \\text{m/s}^2$. Cùng lúc đó, một xe đạp ở đỉnh dốc có vận tốc $2\\ \\text{m/s}$ "
                   "bắt đầu xuống dốc, chuyển động nhanh dần đều với gia tốc có độ lớn $0{,}2\\ \\text{m/s}^2$. Dốc dài $570\\ \\text{m}$.</p>"
                   "<ol type=\"a\"><li>Sau bao lâu hai xe gặp nhau và chỗ gặp cách chân dốc bao xa?</li><li>Tính vận tốc của mỗi xe lúc gặp nhau.</li></ol>"),
]

# ───────────── Tự luận: ví dụ cũ chưa biên tập (xếp dễ → khó) ─────────────
OLD = json.load(open(os.path.join(HERE, "old/54.json")))["questions"]
USED = {2, 3, 16, 17, 18}   # ví dụ 3, 4, 17, 18, 19 đã biên tập thành dạng 1, 3, 6, 5, 4
ORDER = [0, 1, 13, 4, 9, 10, 11, 12, 19, 7, 6, 8, 14, 5, 15, 20, 21]
assert not (set(ORDER) & USED) and len(set(ORDER) | USED) == len(OLD)
MUC = {0: "Dễ", 1: "Dễ", 13: "Dễ", 4: "Trung bình", 9: "Trung bình", 10: "Trung bình", 11: "Trung bình", 12: "Trung bình", 19: "Trung bình",
       7: "Trung bình", 6: "Trung bình", 8: "Khó", 14: "Khó", 5: "Khó", 15: "Khó", 20: "Nâng cao", 21: "Nâng cao"}
TU_LUAN = tu_luan_tu(OLD, ORDER, MUC)
for a_, b_ in ((r"\Delta t}5=", r"\Delta t}=5="), ("5^{5}", "5^{2}"), ("m/h = 10", "36 km/h = 10")):
    assert TU_LUAN["body_html"].count(a_) == 1, a_
    TU_LUAN["body_html"] = TU_LUAN["body_html"].replace(a_, b_)

write(J, 54, "Bài 9. Chuyển động thẳng biến đổi đều", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
