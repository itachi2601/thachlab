"""Bài tập mẫu Bài 16 "Lực tương tác giữa hai điện tích" (Vật lí 11) — lesson_id 35. 5 dạng (quét: ket-qua/35.quet-dang.json).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-35.py   (idempotent) → 35.json (review.checked=false cho tới khi kiểm chéo).
Ví dụ cũ (old/35.json, 4 mục): VD1 → Dạng 2 (đổi số), VD2 (tìm điện tích từ lực) → ý b Dạng 2; VD2, 3, 4 vào tự luận."""
import json, os, sys, math, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

J = os.path.join(HERE, "35.json")
TOP_BAI = "Lực tương tác giữa hai điện tích"
TOP_CL = "Định luật Coulomb"
TOP_CB = "Cân bằng của điện tích chịu nhiều lực"
GREY = "#94a3b8"
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
K = 9e9
E = 1.6e-19

# ═════════════ TỰ GIẢI LẠI SỐ LIỆU (độc lập với lời giải) ═════════════
def near(a, b, tol=1e-9): return abs(a - b) <= tol * max(1, abs(b))
# Dạng 1
_q1, _q2 = -8.0e-9, 2.0e-9
_qp = (_q1 + _q2) / 2
assert near(_qp, -3.0e-9) and near(_q1 + _q2, -6.0e-9)
_dq = abs(_qp - _q1)
assert near(_dq, 5.0e-9) and near(abs(_qp - _q2), 5.0e-9)
_n = _dq / E
assert abs(_n / 1e10 - 3.125) < 1e-9
# Dạng 2
_F2a = K * abs(3.0e-6 * -5.0e-6) / 0.30 ** 2
assert near(_F2a, 1.5)
_q2b = 0.10 * math.sqrt(0.90 / K)
assert near(_q2b, 1.0e-6)
assert near(K * (1.0e-6) ** 2 / 0.10 ** 2, 0.90)
# Dạng 3
_F0 = 4.0e-3; _eps = 4.0; _r0 = 0.060
_Fa = _F0 / _eps
assert near(_Fa, 1.0e-3)
_rb = _r0 / math.sqrt(_eps)
assert near(_rb, 0.030)
assert near(K * 1.0 / (_eps * _rb ** 2) / (K * 1.0 / _r0 ** 2), 1.0)       # lực trong dầu ở r' bằng F0
_Fc = _F0 * 3 * (_r0 / 0.030) ** 2
assert near(_Fc, 48e-3)
# Dạng 4 (không phụ thuộc q0)
_q1, _q2, _AB, _q0 = 36e-9, -4e-9, 0.090, 2e-9
_ratio = math.sqrt(abs(_q1) / abs(_q2))
assert near(_ratio, 3.0)
_r2 = _AB / (_ratio - 1); _r1 = _ratio * _r2          # ngoài đoạn, phía B: r1 - r2 = AB
assert near(_r2, 0.045) and near(_r1, 0.135)
assert near(abs(_q1) / _r1 ** 2, abs(_q2) / _r2 ** 2)
_F1c = K * abs(_q1 * _q0) / _r1 ** 2; _F2c = K * abs(_q2 * _q0) / _r2 ** 2
assert near(_F1c, _F2c) and abs(_F1c / 1e-5 - 3.5556) < 1e-3
# các miền khác không cân bằng (dò cả đường thẳng): đúng một nghiệm
def _net(s):
    d1, d2 = s, s - _AB
    f1 = K * _q1 * _q0 / d1 ** 2 * (1 if d1 > 0 else -1)
    f2 = K * _q2 * _q0 / d2 ** 2 * (1 if d2 > 0 else -1)
    return f1 + f2
_prev = None; _zeros = []
for i in range(-3000, 6000):
    s = i / 10000 + 1e-7
    if abs(s) < 1e-3 or abs(s - _AB) < 1e-3: _prev = None; continue
    v = _net(s)
    if _prev is not None and (_prev[1] > 0) != (v > 0): _zeros.append(round(s, 3))
    _prev = (s, v)
assert len(_zeros) == 1 and abs(_zeros[0] - 0.135) < 2e-3, _zeros
# đổi dấu q0 thì vị trí không đổi (cả hai lực đảo chiều)
assert near(K * abs(_q1 * -2e-9) / _r1 ** 2, K * abs(_q2 * -2e-9) / _r2 ** 2)
# Dạng 5
_qa, _qb, _qc = 4.0e-9, -12e-9, 2.0e-9
_F1 = K * abs(_qa * _qc) / 0.030 ** 2; _F2 = K * abs(_qb * _qc) / 0.060 ** 2
assert near(_F1, 8.0e-5) and near(_F2, 6.0e-5)
_R = math.hypot(_F1, _F2)
assert near(_R, 1.0e-4)
_phi = math.degrees(math.atan2(_F2, _F1))
assert abs(_phi - 36.87) < 0.01
# phương án sai (để lựa chọn nhiễu khác đáp án đúng)
assert abs(math.degrees(math.atan2(_F1, _F2)) - 53.13) < 0.01 and abs(_F1 + _F2 - 1.4e-4) < 1e-12 and abs(_F1 - _F2 - 2e-5) < 1e-12
assert abs(K * abs(_qa * _qc) / (0.03 ** 2 + 0.06 ** 2) / 1e-5 - 1.6) < 1e-6        # dùng r = AB nhầm
assert abs(math.degrees(math.acos(_F2 / _F1)) - 41.41) < 0.01

# ═════════════ TIỆN ÍCH VẼ ═════════════
def T(x, y, s, c="currentColor", size=13, anchor="middle", w="700"):
    return lbl(x, y, s, c, size, anchor, w)

def anim(attr, vals, kts, dur):
    v = ";".join(f"{x:.1f}" if isinstance(x, float) else str(x) for x in vals)
    k = ";".join(f"{t:.4f}" for t in kts)
    return f'<animate attributeName="{attr}" values="{v}" keyTimes="{k}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'

def move(vals, kts, dur):
    v = ";".join(f"{a:.1f} {b:.1f}" for a, b in vals)
    k = ";".join(f"{t:.4f}" for t in kts)
    return (f'<animateTransform attributeName="transform" type="translate" values="{v}" keyTimes="{k}" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')

def colr(sign): return RED if sign == "+" else BLUE if sign == "−" else GREY

def qb(x, y, r, sign, size=18):
    """Quả cầu tích điện: nền màu theo dấu + dấu bên trong."""
    c = colr(sign)
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" fill-opacity=".35" stroke="{c}" stroke-width="2.2"/>'
            + T(x, y + size * 0.36, sign, c, size))

def R(x, y, w, h, c="currentColor", sw=2, fill="none", op=1, rx=0):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" '
            f'stroke-width="{sw}" opacity="{op}"/>')

def right_angle(x, y, ux, uy, vx, vy, s=11):
    """Dấu vuông góc tại (x,y); u, v là hai hướng đơn vị của hai cạnh."""
    return (f'<path d="M{x + ux * s:.1f},{y + uy * s:.1f} L{x + (ux + vx) * s:.1f},{y + (uy + vy) * s:.1f} L{x + vx * s:.1f},{y + vy * s:.1f}" '
            f'fill="none" stroke="currentColor" stroke-width="1.6"/>')

# ═════════════ HÌNH ═════════════
def d1(kk):
    p = f"d1{kk}"
    if kk == 0:
        Tt = 7.0
        xa, xb, y, r = 80, 340, 118, 22
        dx = (xb - xa) / 2 - r                                   # mỗi quả đi 108 px để chạm nhau ở giữa
        kt = [0, .10, .40, .55, .85, 1]
        mv = lambda s: move([(0, 0), (0, 0), (s * dx, 0), (s * dx, 0), (0, 0), (0, 0)], kt, Tt)
        fade_out = anim("opacity", [1, 1, 0, 0], [0, .35, .40, 1], Tt)
        fade_in = anim("opacity", [0, 0, 1, 1], [0, .85, .90, 1], Tt)
        b = f'<line x1="30" y1="{y + r + 3}" x2="390" y2="{y + r + 3}" stroke="currentColor" stroke-width="2.4"/>'
        b += T(210, 190, "mặt bàn cách điện", GREY, 12, "middle", "400")
        for xc, sg, nm, sv in ((xa, "−", "q₁ = −8,0 nC", -1), (xb, "+", "q₂ = +2,0 nC", 1)):
            c = colr(sg)
            b += f'<g>{mv(sv)}'
            b += (f'<circle cx="{xc}" cy="{y}" r="{r}" fill="{c}" fill-opacity=".35" stroke="{c}" stroke-width="2.2">'
                  f'{anim("fill", [c, c, GREY, GREY], [0, .35, .40, 1], Tt)}{anim("stroke", [c, c, GREY, GREY], [0, .35, .40, 1], Tt)}</circle>')
            b += f'<g>{fade_out}{T(xc, y + 6.5, sg, c, 18)}</g>'
            b += f'<g opacity="0">{fade_in}{T(xc, y + 6, "?", "currentColor", 18)}</g>'
            b += '</g>'
            b += f'<g>{fade_out}{T(xc, 62, nm, c, 14)}</g>'
            b += f'<g opacity="0">{fade_in}{T(xc, 62, "q′ = ?", "currentColor", 14)}</g>'
        return fig("d1-0", "0 0 420 200", "Hai quả cầu giống nhau chạm vào nhau rồi tách ra, trở lại vị trí cũ", b,
                   "Mô phỏng: hai quả cầu chạm nhau rồi tách ra, đặt lại chỗ cũ (7 s). Màu quả cầu cho biết dấu điện tích lúc đầu. " + NOTE)
    b = qb(100, 80, 26, "−", 22) + qb(320, 80, 26, "+", 22)
    b += T(100, 38, "q₁ = −8,0 nC", BLUE, 14) + T(320, 38, "q₂ = +2,0 nC", RED, 14)
    b += arrow("", "o", 140, 80, 180, 80, 2.2) + arrow("", "o", 280, 80, 240, 80, 2.2)
    b += T(210, 66, "chạm nhau", "currentColor", 13) + T(210, 100, "rồi tách ra", "currentColor", 13)
    b += T(210, 150, "Sau khi tách: q′ = ? (mỗi quả)", ORG, 14)
    b += T(210, 176, "Êlectron đã chuyển: n = ? hạt", ORG, 14)
    return fig("d1-2", "0 0 420 196", "Hai quả cầu giống nhau mang q₁ và q₂, chạm nhau rồi tách ra", b,
               "Dữ kiện của đề; dấu “?” là đại lượng cần tìm. " + NOTE)

def d2(kk):
    p = f"d2{kk}"
    xa, xb, y, r = 100, 300, 92, 20
    def scale(y0):
        s = f'<line x1="{xa}" y1="{y0}" x2="{xb}" y2="{y0}" stroke="currentColor" stroke-width="2"/>'
        for i, cm in enumerate((0, 10, 20, 30)):
            xx = xa + (xb - xa) * cm / 30
            s += f'<line x1="{xx:.1f}" y1="{y0 - 5}" x2="{xx:.1f}" y2="{y0 + 5}" stroke="currentColor" stroke-width="1.6"/>'
            s += T(xx, y0 + 22, str(cm), "currentColor", 12, "middle", "400")
        return s + T(xb + 14, y0 + 22, "cm", "currentColor", 12, "start", "400")
    if kk == 0:
        Tt = 4.0
        b = scale(150) + T(xa, 46, "q₁ = +3,0 μC", RED, 14) + T(xb, 46, "q₂ = −5,0 μC", BLUE, 14)
        b += qb(xa, y, r, "+")
        b += f'<g>{move([(90, 0), (90, 0), (0, 0)], [0, .1, 1], Tt)}{qb(xb, y, r, "−")}</g>'
        b += f'<g opacity="0">{anim("opacity", [0, 0, 1], [0, .85, 1], Tt)}{T((xa + xb) / 2, y + 6, "F = ?", ORG, 15)}</g>'
        b += T(xa, 190, "r = 30 cm", "currentColor", 12, "start", "400")
        return fig("d2-0", "0 0 420 200", "Quả cầu thứ hai được đặt cách quả thứ nhất 30 cm trên thước", b,
                   "Mô phỏng: đặt quả cầu thứ hai cách quả thứ nhất 30 cm, đo giữa hai tâm trên thước (4 s). " + NOTE)
    b = qb(xa, y, r, "+") + qb(xb, y, r, "−")
    b += T(xa, 46, "q₁ = +3,0 μC", RED, 14) + T(xb, 46, "q₂ = −5,0 μC", BLUE, 14)
    b += dim(p, "g", xa, 140, xb, 140, "r = 30 cm", 210, 132, "middle")
    b += T(210, y + 6, "F = ?", ORG, 15)
    b += T(210, 182, "Ý b: hai điện tích bằng nhau, r = 10 cm, F = 0,90 N, |q| = ?", ORG, 13)
    return fig("d2-2", "0 0 420 196", "Hai điện tích điểm đặt cách nhau 30 cm trong không khí", b, "Dữ kiện của đề ý a; dấu “?” là đại lượng cần tìm. " + NOTE)

def d3(kk):
    p = f"d3{kk}"
    xa, xb, y, r = 110, 310, 140, 18
    if kk == 0:
        Tt = 5.0
        tank = R(24, 44, 372, 140, "currentColor", 2.4)
        oil = (f'<rect x="26" y="182" width="368" height="0" fill="{BLUE}" fill-opacity=".22">'
               f'{anim("y", [182, 182, 64, 64], [0, .1, .8, 1], Tt)}{anim("height", [0, 0, 118, 118], [0, .1, .8, 1], Tt)}</rect>')
        b = tank + oil
        for xc, sg in ((xa, "+"), (xb, "−")):
            b += f'<line x1="{xc}" y1="{y + r}" x2="{xc}" y2="184" stroke="currentColor" stroke-width="2.2"/>' + qb(xc, y, r, sg, 17)
        b += dim(p, "g", xa, 206, xb, 206, "r = 6,0 cm", 210, 224, "middle")
        b += f'<g>{anim("opacity", [1, 1, 0, 0], [0, .75, .85, 1], Tt)}{T(210, 30, "không khí: F₀ = 4,0 mN", "currentColor", 14)}</g>'
        b += f'<g opacity="0">{anim("opacity", [0, 0, 1, 1], [0, .75, .85, 1], Tt)}{T(210, 30, "trong dầu (ε = 4,0): F′ = ?", ORG, 14)}</g>'
        return fig("d3-0", "0 0 420 232", "Dầu dâng lên ngập cả hai quả cầu, khoảng cách giữa chúng không đổi", b,
                   "Mô phỏng: đổ dầu vào bể đến khi ngập cả hai quả cầu, khoảng cách không đổi (5 s). " + NOTE)
    b = ""
    for xc, sg in ((xa, "+"), (xb, "−")):
        b += qb(xc, 62, r, sg, 17)
    b += dim(p, "g", xa, 98, xb, 98, "r = 6,0 cm", 210, 92, "middle")
    b += T(210, 30, "không khí: F₀ = 4,0 mN", "currentColor", 14)
    b += T(24, 140, "a) dầu ε = 4,0, giữ r = 6,0 cm: F′ = ?", ORG, 13, "start")
    b += T(24, 164, "b) trong dầu, F = 4,0 mN: r′ = ?", ORG, 13, "start")
    b += T(24, 188, "c) không khí, q₁ gấp 3, r = 3,0 cm: F″ = ?", ORG, 13, "start")
    return fig("d3-2", "0 0 420 204", "Hai điện tích điểm cách nhau 6,0 cm trong không khí hút nhau với lực 4,0 mN", b, "Dữ kiện của đề; dấu “?” là đại lượng cần tìm. " + NOTE)

def d4_dyn():
    """Thả q₀ ở trung điểm AB: tích phân chuyển động thật dọc thanh (q₀ = +2 nC, m = 0,10 g)."""
    m = 1.0e-4; s = 0.045; v = 0.0; t = 0.0; dt = 1e-5; stop = _AB - 0.015
    def acc(s): return K * _q0 * (_q1 / s ** 2 + abs(_q2) / (_AB - s) ** 2) / m
    ts, ss = [0.0], [s]
    while s < stop:
        a = acc(s); v += a * dt; s += v * dt; t += dt
        if int(round(t / dt)) % 50 == 0: ts.append(t); ss.append(s)
    ts.append(t); ss.append(s)
    # lấy mẫu đều theo thời gian
    N = 30; out = []
    j = 0
    for i in range(N + 1):
        tt = t * i / N
        while j < len(ts) - 2 and ts[j + 1] < tt: j += 1
        f = (tt - ts[j]) / max(ts[j + 1] - ts[j], 1e-12); f = min(max(f, 0), 1)
        out.append(ss[j] + f * (ss[j + 1] - ss[j]))
    return t, out
_T4, _S4 = d4_dyn()

def d4(kk):
    p = f"d4{kk}"
    sc = 18.0                                                   # px/cm
    xa = 40; xb = xa + 9 * sc; y = 118
    rod = f'<line x1="14" y1="{y}" x2="406" y2="{y}" stroke="currentColor" stroke-width="3"/>'
    ends = qb(xa, y, 13, "+", 17) + qb(xb, y, 11, "−", 17)
    lab = T(xa + 10, 66, "q₁ = +36 nC", RED, 14) + T(xb + 10, 66, "q₂ = −4,0 nC", BLUE, 14) + T(xa, 50, "A", "currentColor", 13) + T(xb, 50, "B", "currentColor", 13)
    if kk == 0:
        dur = 3.2; slow = dur / _T4
        pts = [(sc * 100 * (s_ - 0.045), 0) for s_ in _S4]
        x0 = xa + sc * 4.5
        vals = ";".join(f"{a:.1f} 0" for a, _ in pts)
        mv = (f'<animateTransform attributeName="transform" type="translate" values="{vals}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')
        b = rod + ends + lab
        b += f'<g>{mv}{qb(x0, y, 8, "+", 13)}{T(x0, y - 20, "q₀ = +2,0 nC", RED, 13)}</g>'
        b += dim(p, "g", xa, 162, xb, 162, "AB = 9,0 cm", (xa + xb) / 2, 184, "middle")
        return fig("d4-0", "0 0 420 196", "Hạt q₀ thả ở trung điểm của AB trượt dọc thanh theo lực điện", b,
                   f"Mô phỏng: thả q₀ ở trung điểm AB (chỉ là một vị trí thử, không phải vị trí cần tìm); q₀ trượt dọc thanh theo lực điện thật, khối lượng giả định 0,10 g. Chạy chậm {slow:.0f} lần. " + NOTE)
    b = rod + ends + lab
    b += dim(p, "g", xa, 162, xb, 162, "AB = 9,0 cm", (xa + xb) / 2, 184, "middle")
    b += T(300, 108, "q₀ = +2,0 nC (trượt được)", "currentColor", 12, "middle", "400")
    b += T(210, 22, "Cần tìm: vị trí C để hợp lực lên q₀ bằng 0", ORG, 13)
    return fig("d4-2", "0 0 420 196", "Hai điện tích cố định A và B trên một thanh thẳng, hạt q₀ trượt được dọc thanh", b, "Dữ kiện của đề; vị trí C là đại lượng cần tìm. " + NOTE)

def d5(kk):
    p = f"d5{kk}"
    C = (170, 150); A = (170, 90); B = (290, 150)
    tri = (f'<line x1="{C[0]}" y1="{C[1]}" x2="{A[0]}" y2="{A[1]}" stroke="{GREY}" stroke-width="1.8" stroke-dasharray="6 4"/>'
           f'<line x1="{C[0]}" y1="{C[1]}" x2="{B[0]}" y2="{B[1]}" stroke="{GREY}" stroke-width="1.8" stroke-dasharray="6 4"/>')
    tri += right_angle(C[0], C[1], 0, -1, 1, 0)
    fixed = qb(*A, 12, "+", 16) + qb(*B, 12, "−", 16)
    fixed += T(A[0], 62, "A: q₁ = +4,0 nC", RED, 13) + T(B[0] + 14, B[1] + 5, "B: q₂ = −12 nC", BLUE, 13, "start")
    fixed += T(A[0] + 8, 125, "3,0 cm", "currentColor", 12, "start", "400") + T(230, 172, "6,0 cm", "currentColor", 12, "middle", "400")
    if kk == 0:
        Tt = 4.0
        b = tri + fixed
        b += f'<g>{move([(-100, 48), (-100, 48), (0, 0)], [0, .1, 1], Tt)}{qb(C[0], C[1], 9, "+", 14)}</g>'
        b += T(C[0] - 12, 176, "C: q₀ = +2,0 nC", RED, 13, "end")
        return fig("d5-0", "0 0 420 200", "Hạt q₀ được đưa tới điểm C, nơi CA vuông góc CB", b,
                   "Mô phỏng: đưa q₀ tới điểm C bằng giá cách điện (4 s); CA vuông góc CB. " + NOTE)
    b = tri + fixed + qb(C[0], C[1], 9, "+", 14) + T(C[0] - 12, 176, "C: q₀ = +2,0 nC", RED, 13, "end")
    b += T(360, 40, "lực lên q₀: ?", ORG, 13, "end")
    return fig("d5-2", "0 0 420 200", "Ba điện tích đặt ở A, B, C với CA vuông góc CB", b, "Dữ kiện của đề; dấu “?” là đại lượng cần tìm. " + NOTE)

BUILD = [d1, d2, d3, d4, d5]

# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Hai quả cầu giống nhau chạm rồi tách: điện tích mỗi quả và số êlectron chuyển", topic=TOP_BAI,
      problem_html=r"""<p>Hai quả cầu kim loại nhỏ giống hệt nhau, đặt trên mặt bàn cách điện, mang điện tích $q_1=-8{,}0$ nC và $q_2=+2{,}0$ nC. Cho hai quả chạm nhau rồi tách ra. Bỏ qua điện tích mất đi vào không khí. Lấy $|e|=1{,}6\cdot10^{-19}$ C.</p><ol type="a"><li>Tính điện tích của mỗi quả sau khi tách.</li><li>Êlectron đã chuyển từ quả nào sang quả nào? Tính số êlectron chuyển.</li></ol>"""),
 dict(label="Dạng 2 · Dễ · Định luật Coulomb: tính lực, xét hút hay đẩy, tìm điện tích từ lực", topic=TOP_CL,
      problem_html=r"""<p>Trong không khí, hai điện tích điểm $q_1=+3{,}0\ \mu$C và $q_2=-5{,}0\ \mu$C có tâm cách nhau $30$ cm.</p><ol type="a"><li>Tính độ lớn lực tương tác giữa hai điện tích. Hai điện tích hút hay đẩy nhau?</li><li>Một cặp điện tích điểm khác, hai điện tích có độ lớn bằng nhau, đặt trong không khí cách nhau $10$ cm, đẩy nhau với lực $0{,}90$ N. Tính độ lớn mỗi điện tích.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Lực Coulomb khi đổi môi trường, khoảng cách, điện tích", topic=TOP_CL,
      problem_html=r"""<p>Hai điện tích điểm đặt trong không khí, cách nhau $6{,}0$ cm, hút nhau với lực $F_0=4{,}0$ mN.</p><ol type="a"><li>Nhúng cả hai vào dầu có hằng số điện môi $\varepsilon=4{,}0$, giữ nguyên khoảng cách $6{,}0$ cm. Tính lực tương tác khi đó.</li><li>Vẫn trong dầu, phải đặt hai điện tích cách nhau bao nhiêu để lực lại bằng $4{,}0$ mN?</li><li>Quay về tình huống ban đầu (không khí, các điện tích ban đầu), tăng độ lớn $q_1$ lên $3$ lần và giảm khoảng cách xuống $3{,}0$ cm. Tính lực tương tác khi đó.</li></ol>"""),
 dict(label="Dạng 4 · Trung bình · Tìm vị trí để điện tích nằm cân bằng trên đường nối hai điện tích", topic=TOP_CB,
      problem_html=r"""<p>Trên một thanh nhựa thẳng nằm ngang, đủ dài về hai phía, trong không khí, gắn cố định hai hạt tích điện $q_1=+36$ nC tại A và $q_2=-4{,}0$ nC tại B, với $AB=9{,}0$ cm. Một hạt nhỏ mang điện tích $q_0=+2{,}0$ nC xâu vào thanh, trượt được không ma sát dọc thanh.</p><ol type="a"><li>Đặt $q_0$ ở điểm C nào trên thanh để hợp lực điện lên nó bằng $0$? Tìm $CA$ và $CB$.</li><li>Tính lực do $q_1$ và lực do $q_2$ tác dụng lên $q_0$ tại C, để kiểm tra kết quả.</li><li>Thay $q_0$ bằng hạt mang điện tích $-2{,}0$ nC. Vị trí cân bằng có thay đổi không?</li></ol>"""),
 dict(label="Dạng 5 · Khó · Tổng hợp lực điện của hai điện tích lên một điện tích: độ lớn và hướng", topic=TOP_CB,
      problem_html=r"""<p>Trong không khí, ba điện tích điểm đặt tại ba điểm A, B, C: $q_1=+4{,}0$ nC tại A, $q_2=-12$ nC tại B, $q_0=+2{,}0$ nC tại C. Biết $CA=3{,}0$ cm, $CB=6{,}0$ cm và $CA$ vuông góc với $CB$.</p><ol type="a"><li>Tính độ lớn lực $F_1$ do $q_1$ và lực $F_2$ do $q_2$ tác dụng lên $q_0$.</li><li>Tính độ lớn hợp lực tác dụng lên $q_0$.</li><li>Tính góc giữa hợp lực và lực $\vec F_1$.</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (⚠ chỉ nêu điều kiện; cột 3 không ghi kết luận) ═════════════
ANALYSIS = [
 [(r'"hai quả cầu kim loại nhỏ giống hệt nhau"', r"Hai quả giống hệt nhau", r"⚠ Điều kiện chỉ áp dụng khi hệ cô lập và hai quả giống hệt nhau (cùng kích thước, cùng chất)"),
  (r'"$q_1=-8{,}0$ nC và $q_2=+2{,}0$ nC"', r"$q_1=-8{,}0\cdot10^{-9}$ C ; $q_2=+2{,}0\cdot10^{-9}$ C", r"Điện tích là đại lượng có dấu ; đổi nC sang C"),
  (r'"chạm nhau rồi tách ra"', r"Hai quả tiếp xúc rồi tách", r"Định luật bảo toàn điện tích : đại lượng nào của hệ không đổi ? Điện tích phân bố lại thế nào giữa hai quả giống hệt nhau ?"),
  (r'"bỏ qua điện tích mất đi vào không khí"', r"Hệ cô lập", r"Hệ cô lập là hệ không trao đổi điện tích với bên ngoài"),
  (r'"tính điện tích của mỗi quả sau khi tách"', r"Cần: $q'$ của mỗi quả", r"Cách tính điện tích mỗi quả từ $q_1$ và $q_2$"),
  (r'"êlectron đã chuyển từ quả nào sang quả nào … số êlectron"', r"$|e|=1{,}6\cdot10^{-19}$ C ; cần: số êlectron", r"Điện tích của một vật liên hệ thế nào với số êlectron thừa hoặc thiếu ; êlectron dịch chuyển làm điện tích mỗi quả thay đổi bao nhiêu")],
 [(r'"không khí"', r"$\varepsilon\approx1$", r"⚠ Công thức dùng cho điện tích điểm đứng yên ; $q$ tính bằng C, $r$ tính bằng m"),
  (r'"$q_1=+3{,}0\ \mu$C và $q_2=-5{,}0\ \mu$C"', r"$q_1=+3{,}0\cdot10^{-6}$ C ; $q_2=-5{,}0\cdot10^{-6}$ C", r"Đổi $\mu$C sang C ; dấu hai điện tích cho biết hút hay đẩy"),
  (r'"tâm cách nhau $30$ cm"', r"$r=0{,}30$ m", r"Đổi cm sang m rồi mới bình phương"),
  (r'"tính độ lớn lực tương tác"', r"Cần: $F$", r"Định luật Coulomb : lực phụ thuộc điện tích và khoảng cách thế nào"),
  (r'"hút hay đẩy nhau"', r"Cần: loại lực", r"Quan hệ giữa dấu hai điện tích và loại lực"),
  (r'"hai điện tích có độ lớn bằng nhau … cách nhau $10$ cm … đẩy nhau với lực $0{,}90$ N"', r"$|q|$ giống nhau ; $r=0{,}10$ m ; $F=0{,}90$ N", r"Hai điện tích có độ lớn như nhau thì tích $|q_1q_2|$ viết lại thế nào"),
  (r'"tính độ lớn mỗi điện tích"', r"Cần: $|q|$", r"Biến đổi công thức Coulomb để tìm điện tích")],
 [(r'"hai điện tích điểm … trong không khí"', r"Điện tích điểm ; $\varepsilon\approx1$", r"⚠ Mỗi lần chỉ đổi những đại lượng đề nêu ; các đại lượng còn lại giữ nguyên"),
  (r'"cách nhau $6{,}0$ cm … hút nhau với lực $F_0=4{,}0$ mN"', r"$r_0=0{,}060$ m ; $F_0=4{,}0\cdot10^{-3}$ N", r"Tình huống mốc để so sánh"),
  (r'"nhúng … vào dầu có $\varepsilon=4{,}0$, giữ nguyên khoảng cách"', r"$\varepsilon=4{,}0$ ; $r$ không đổi", r"Hằng số điện môi ảnh hưởng đến lực thế nào"),
  (r'"phải đặt cách nhau bao nhiêu để lực lại bằng $4{,}0$ mN"', r"Cần: $r'$ ; $F'=F_0$", r"Lực phụ thuộc $r$ theo quy luật nào ; điều gì bù lại ảnh hưởng của $\varepsilon$"),
  (r'"tăng độ lớn $q_1$ lên $3$ lần"', r"$q_1''=3q_1$", r"Lực phụ thuộc tích $|q_1q_2|$ thế nào"),
  (r'"giảm khoảng cách xuống $3{,}0$ cm"', r"$r''=0{,}030$ m ; môi trường: không khí", r"Lực phụ thuộc $r$ thế nào ; so sánh với tình huống mốc ($r_0=6{,}0$ cm)")],
 [(r'"gắn cố định hai hạt tích điện … $q_1=+36$ nC tại A, $q_2=-4{,}0$ nC tại B"', r"$q_1=+36\cdot10^{-9}$ C ; $q_2=-4{,}0\cdot10^{-9}$ C", r"⚠ $q_1$, $q_2$ cố định ; mỗi điện tích tác dụng lên $q_0$ một lực riêng, lực do hai điện tích cộng lại"),
  (r'"$AB=9{,}0$ cm"', r"$AB=0{,}090$ m", r"Khoảng cách giữa hai điện tích cố định"),
  (r'"hạt nhỏ $q_0=+2{,}0$ nC … trượt được không ma sát dọc thanh"', r"$q_0=+2{,}0\cdot10^{-9}$ C", r"Hai lực điện lên $q_0$ nằm trên cùng một đường thẳng (thanh)"),
  (r'"hợp lực điện lên nó bằng $0$"', r"Điều kiện cân bằng", r"Hai lực thành phần phải thoả những điều kiện nào về phương, chiều, độ lớn"),
  (r'"đặt $q_0$ ở điểm C nào … tìm $CA$ và $CB$"', r"Cần: $CA=r_1$, $CB=r_2$", r"Quan hệ giữa dấu hai điện tích và miền chứa C ; quan hệ giữa $r_1$, $r_2$ và $AB$"),
  (r'"tính lực do $q_1$ và lực do $q_2$ … để kiểm tra"', r"Cần: $F_{10}$, $F_{20}$", r"Công thức Coulomb với khoảng cách từ mỗi điện tích đến $q_0$"),
  (r'"thay $q_0$ bằng hạt mang điện tích $-2{,}0$ nC"', r"$q_0'=-2{,}0\cdot10^{-9}$ C", r"Vị trí cân bằng có phụ thuộc dấu và độ lớn của $q_0$ không")],
 [(r'"ba điện tích điểm … trong không khí"', r"Điện tích điểm ; $\varepsilon\approx1$", r"⚠ Điện tích điểm đứng yên ; lực điện là đại lượng có hướng"),
  (r'"$q_1=+4{,}0$ nC tại A, $q_2=-12$ nC tại B, $q_0=+2{,}0$ nC tại C"', r"$q_1=4{,}0\cdot10^{-9}$ C ; $q_2=-12\cdot10^{-9}$ C ; $q_0=2{,}0\cdot10^{-9}$ C", r"Đổi nC sang C ; dấu cho biết hút hay đẩy"),
  (r'"$CA=3{,}0$ cm, $CB=6{,}0$ cm"', r"$r_1=0{,}030$ m ; $r_2=0{,}060$ m", r"Khoảng cách từ mỗi điện tích đến $q_0$ ; đổi cm sang m"),
  (r'"$CA$ vuông góc với $CB$"', r"Hai đường thẳng CA, CB vuông góc", r"Hai đường CA, CB vuông góc : hai lực lên $q_0$ có phương thế nào"),
  (r'"tính độ lớn lực $F_1$ do $q_1$ và lực $F_2$ do $q_2$"', r"Cần: $F_1$, $F_2$", r"Lực mỗi điện tích tác dụng lên $q_0$ phụ thuộc những đại lượng nào"),
  (r'"tính độ lớn hợp lực"', r"Cần: $F$", r"Hai điện tích cùng tác dụng lên $q_0$ thì lực tổng cộng được xác định thế nào"),
  (r'"tính góc giữa hợp lực và lực $\vec F_1$"', r"Cần: góc $\varphi$", r"Hợp lực và hai lực thành phần tạo thành hình gì ; góc cần tìm nằm ở đâu trong hình đó")],
]

# ═════════════ LỜI GIẢI ═════════════
R1 = [r"<strong>Khái niệm:</strong> hệ cô lập là hệ không trao đổi điện tích với bên ngoài ; tổng đại số điện tích của hệ không đổi.",
      r"<strong>Định luật:</strong> hai quả cầu giống hệt nhau chạm nhau rồi tách ra thì điện tích chia đều.",
      r"<strong>Công thức:</strong> $q'=\dfrac{q_1+q_2}{2}$ (cộng có dấu) ; $|q|=n|e|$, $|e|=1{,}6\cdot10^{-19}$ C.",
      r"⚠ <strong>Điều kiện:</strong> hai quả giống hệt nhau và hệ cô lập ; cộng đại số (giữ dấu), không cộng độ lớn."]
R2 = [r"<strong>Khái niệm:</strong> lực hút hay đẩy giữa hai điện tích điểm đứng yên gọi là lực Coulomb ; cùng dấu thì đẩy, trái dấu thì hút.",
      r"<strong>Định luật:</strong> lực tỉ lệ thuận với $|q_1q_2|$, tỉ lệ nghịch với $r^2$.",
      r"<strong>Công thức:</strong> $F=k\dfrac{|q_1q_2|}{r^2}$ trong không khí, $k=9\cdot10^9\ \text{N·m}^2/\text{C}^2$.",
      r"⚠ <strong>Điều kiện:</strong> điện tích điểm đứng yên ; $q$ tính bằng C, $r$ tính bằng m."]
R3 = [r"<strong>Khái niệm:</strong> điện môi làm lực giảm $\varepsilon$ lần so với chân không (không khí) ở cùng khoảng cách.",
      r"<strong>Công thức:</strong> $F=k\dfrac{|q_1q_2|}{\varepsilon r^2}$ : $F\sim|q_1q_2|$, $F\sim\dfrac{1}{r^2}$, $F\sim\dfrac{1}{\varepsilon}$.",
      r"Gặp bài đổi nhiều đại lượng : lập tỉ số với tình huống mốc, không cần tính lại từ đầu.",
      r"⚠ <strong>Điều kiện:</strong> điện tích điểm đứng yên ; mỗi bước chỉ đổi những đại lượng đề nêu, giữ nguyên phần còn lại."]
R4 = [r"<strong>Khái niệm:</strong> $q_0$ cân bằng khi hợp lực lên nó bằng $0$ : $\vec F_{10}+\vec F_{20}=\vec 0$.",
      r"<strong>Định luật:</strong> hai lực cùng phương, ngược chiều, bằng độ lớn. Cùng dấu : C ở giữa A và B. Trái dấu : C ngoài đoạn AB, gần điện tích nhỏ hơn.",
      r"<strong>Công thức:</strong> $\dfrac{r_1}{r_2}=\sqrt{\dfrac{|q_1|}{|q_2|}}$ ; ở giữa : $r_1+r_2=AB$ ; ở ngoài : $|r_1-r_2|=AB$ ; $F=k\dfrac{|q_1q_0|}{r^2}$.",
      r"⚠ <strong>Điều kiện:</strong> $q_1$, $q_2$ cố định ; vị trí cân bằng không phụ thuộc dấu và độ lớn của $q_0$ ($q_0\neq0$)."]
R5 = [r"<strong>Khái niệm:</strong> lực điện là vectơ ; chiều theo dấu : cùng dấu đẩy, trái dấu hút.",
      r"<strong>Định luật:</strong> $\vec F=\vec F_1+\vec F_2$ (hình bình hành) ; $F_1=k\dfrac{|q_1q_0|}{r_1^2}$, $F_2=k\dfrac{|q_2q_0|}{r_2^2}$.",
      r"<strong>Công thức:</strong> hai lực vuông góc : $F=\sqrt{F_1^2+F_2^2}$ ; góc $\varphi$ giữa $\vec F$ và $\vec F_1$ : $\tan\varphi=\dfrac{F_2}{F_1}$.",
      r"⚠ <strong>Điều kiện:</strong> chọn công thức hợp lực theo góc giữa hai <em>lực</em> (xét chiều từng lực), không đoán theo hình."]

SOLS = [
 sol(R1, [
  ("Tổng đại số điện tích",
   [P(r"Hệ cô lập nên tổng đại số điện tích không đổi sau khi tách. Cộng có dấu:"),
    M(r"q_1+q_2=(-8{,}0)+(+2{,}0)"), A(r"q_1+q_2=-6{,}0\ \text{nC}")]),
  ("Chia đều cho hai quả",
   [P("Hai quả giống hệt nhau nên mỗi quả mang một nửa tổng:"),
    M(r"q'=\dfrac{q_1+q_2}{2}=\dfrac{-6{,}0}{2}"), A(r"q'=-3{,}0\ \text{nC (mỗi quả)}")]),
  ("Điện tích dịch chuyển",
   [P(r"Quả 1 đi từ $-8{,}0$ nC đến $-3{,}0$ nC ; quả 2 đi từ $+2{,}0$ nC đến $-3{,}0$ nC. Độ biến thiên của mỗi quả:"),
    M(r"|\Delta q|=|q'-q_1|=|-3{,}0-(-8{,}0)|"), A(r"|\Delta q|=5{,}0\ \text{nC}"),
    P(r"Quả 1 giảm lượng điện âm nên mất êlectron ; quả 2 nhận đúng lượng đó. Êlectron chuyển từ quả 1 sang quả 2.")]),
  ("Số êlectron chuyển",
   [P(r"Điện tích dịch chuyển là bội của $|e|$:"),
    M(r"n=\dfrac{|\Delta q|}{|e|}"), M(r"n=\dfrac{5{,}0\cdot10^{-9}}{1{,}6\cdot10^{-19}}"), A(r"n\approx3{,}1\cdot10^{10}\ \text{êlectron}")]),
  ("Kiểm tra",
   [P(r"Tổng sau khi tách $2\cdot(-3{,}0)=-6{,}0$ nC bằng tổng ban đầu ✓."),
    P(r"Hai quả cùng dấu âm sau khi tách, nên nếu đặt gần nhau sẽ đẩy nhau."),
    P(r"Cộng độ lớn $8{,}0+2{,}0$ rồi chia đôi sẽ cho điện tích có độ lớn lớn hơn mọi quả ban đầu — vô lí vì hệ cô lập.")])],
  [r"a) $q'=-3{,}0$ nC (mỗi quả)", r"b) êlectron chuyển từ quả 1 sang quả 2 ; $n\approx3{,}1\cdot10^{10}$ hạt"],
  r"Nhận dạng: đề cho <strong>hai quả cầu giống hệt nhau chạm nhau rồi tách</strong> → cộng đại số hai điện tích rồi chia đôi ; số êlectron chuyển = $|\Delta q|/|e|$."),
 sol(R2, [
  ("Đổi sang đơn vị SI",
   [P(r"Đổi điện tích sang C và khoảng cách sang m:"),
    M(r"q_1=3{,}0\cdot10^{-6}\ \text{C},\quad q_2=-5{,}0\cdot10^{-6}\ \text{C},\quad r=0{,}30\ \text{m}"),
    M(r"r^2=(0{,}30)^2"), A(r"r^2=0{,}090\ \text{m}^2")]),
  ("Độ lớn lực",
   [P(r"Dùng công thức Coulomb với độ lớn của tích hai điện tích:"),
    M(r"F=k\dfrac{|q_1q_2|}{r^2}"), M(r"F=9\cdot10^{9}\cdot\dfrac{3{,}0\cdot10^{-6}\cdot5{,}0\cdot10^{-6}}{0{,}090}"),
    A(r"F=1{,}5\ \text{N}")]),
  ("Hút hay đẩy",
   [P(r"Dấu quyết định loại lực, không phụ thuộc điện tích nào lớn hơn:"),
    M(r"q_1q_2\lt0"), A(r"T:Hai điện tích <strong>hút</strong> nhau (trái dấu).")]),
  ("Tìm điện tích từ lực",
   [P(r"Hai điện tích bằng nhau nên $|q_1q_2|=q^2$. Rút $|q|$ từ công thức Coulomb:"),
    M(r"F=k\dfrac{q^2}{r^2}\ \Rightarrow\ |q|=r\sqrt{\dfrac{F}{k}}"),
    M(r"|q|=0{,}10\cdot\sqrt{\dfrac{0{,}90}{9\cdot10^{9}}}=0{,}10\cdot\sqrt{10^{-10}}"),
    A(r"|q|=1{,}0\cdot10^{-6}\ \text{C}=1{,}0\ \mu\text{C}")]),
  ("Kiểm tra",
   [P(r"Lực $1{,}5$ N ở khoảng cách $30$ cm với điện tích cỡ $\mu$C : hợp lí (cỡ mấy N)."),
    P(r"Thế ngược ý b : $9\cdot10^{9}\cdot\dfrac{(10^{-6})^2}{0{,}10^2}=0{,}90$ N ✓ khớp đề.")])],
  [r"a) $F=1{,}5$ N ; hút", r"b) $|q|=1{,}0\ \mu$C"],
  r"Nhận dạng: đề hỏi <strong>độ lớn lực giữa hai điện tích</strong> hoặc <strong>tìm điện tích từ lực</strong> → $F=k|q_1q_2|/r^2$ sau khi đổi sang SI ; dấu chỉ để biết hút hay đẩy."),
 sol(R3, [
  ("Đổi môi trường",
   [P(r"Điện môi làm lực giảm $\varepsilon$ lần, $r$ và điện tích không đổi:"),
    M(r"F'=\dfrac{F_0}{\varepsilon}=\dfrac{4{,}0}{4{,}0}"), A(r"F'=1{,}0\ \text{mN}")]),
  ("Bù lại bằng khoảng cách",
   [P(r"Trong dầu cần lực bằng $F_0$. Lực tỉ lệ nghịch với $\varepsilon r'^2$ nên:"),
    M(r"\dfrac{k|q_1q_2|}{\varepsilon r'^2}=\dfrac{k|q_1q_2|}{r_0^2}\ \Rightarrow\ \varepsilon r'^2=r_0^2"),
    M(r"r'=\dfrac{r_0}{\sqrt{\varepsilon}}=\dfrac{6{,}0}{\sqrt{4{,}0}}"), A(r"r'=3{,}0\ \text{cm}")]),
  ("Đổi điện tích và khoảng cách",
   [P(r"Lập tỉ số với tình huống mốc (không khí, $F_0$, $r_0$):"),
    M(r"\dfrac{F''}{F_0}=\dfrac{|q_1''q_2|}{|q_1q_2|}\cdot\dfrac{r_0^2}{r''^2}=3\cdot\left(\dfrac{6{,}0}{3{,}0}\right)^2"),
    M(r"F''=4{,}0\cdot3\cdot4"), A(r"F''=48\ \text{mN}")]),
  ("Kiểm tra",
   [P(r"Ý a : lực giảm khi có điện môi ✓."),
    P(r"Ý b : trong dầu phải lại gần mới đủ lực ✓."),
    P(r"Ý c : $q$ tăng, $r$ giảm thì lực tăng ✓.")])],
  [r"a) $F'=1{,}0$ mN", r"b) $r'=3{,}0$ cm", r"c) $F''=48$ mN"],
  r"Nhận dạng: đề cho <strong>đổi môi trường, điện tích hoặc khoảng cách</strong> → lập tỉ số với tình huống mốc : $F\sim|q_1q_2|/(\varepsilon r^2)$."),
 sol(R4, [
  ("Chọn miền chứa C",
   [P(r"Xét lực của $q_1$ và $q_2$ lên $q_0$ ở ba miền của đường thẳng AB."),
    P(r"Giữa A và B : $q_1$ đẩy $q_0$, $q_2$ hút $q_0$, hai lực cùng chiều nên không triệt tiêu."),
    P(r"Ngoài, phía A : gần $q_1$ có độ lớn lớn hơn nên $F_{10}\gt F_{20}$ ở mọi điểm."),
    A(r"T:Chỉ còn miền <strong>ngoài đoạn AB, phía B</strong> (gần điện tích nhỏ hơn).")]),
  ("Lập tỉ số khoảng cách",
   [P(r"Hợp lực bằng $0$ thì hai lực bằng độ lớn. Đặt $r_1=CA$, $r_2=CB$:"),
    M(r"k\dfrac{|q_1q_0|}{r_1^2}=k\dfrac{|q_2q_0|}{r_2^2}\ \Rightarrow\ \dfrac{r_1}{r_2}=\sqrt{\dfrac{|q_1|}{|q_2|}}"),
    M(r"\dfrac{r_1}{r_2}=\sqrt{\dfrac{36}{4{,}0}}"), A(r"\dfrac{r_1}{r_2}=3{,}0")]),
  ("Tính khoảng cách",
   [P(r"C ngoài đoạn AB, phía B nên $r_1-r_2=AB$:"),
    M(r"3{,}0\,r_2-r_2=9{,}0"), A(r"CB=r_2=4{,}5\ \text{cm}"), A(r"CA=r_1=13{,}5\ \text{cm}")]),
  ("Kiểm tra bằng lực",
   [P(r"Tính lực do $q_1$ tại C ($r_1=0{,}135$ m):"),
    M(r"F_{10}=9\cdot10^{9}\cdot\dfrac{36\cdot10^{-9}\cdot2{,}0\cdot10^{-9}}{0{,}135^2}"), A(r"F_{10}\approx3{,}56\cdot10^{-5}\ \text{N}"),
    P(r"Lực do $q_2$ ($r_2=0{,}045$ m):"),
    M(r"F_{20}=9\cdot10^{9}\cdot\dfrac{4{,}0\cdot10^{-9}\cdot2{,}0\cdot10^{-9}}{0{,}045^2}"), A(r"F_{20}\approx3{,}56\cdot10^{-5}\ \text{N}"),
    P(r"Hai lực bằng nhau ; $q_1$ đẩy ra xa A, $q_2$ hút về B nên ngược chiều ✓.")]),
  ("Đổi dấu của $q_0$",
   [P(r"Đổi dấu $q_0$ thì cả hai lực đổi chiều cùng lúc, vẫn ngược chiều và bằng độ lớn. $q_0$ chỉ xuất hiện ở hai vế và giản ước :"),
    A(r"T:Vị trí cân bằng <strong>không đổi</strong> (CB = 4,5 cm).")])],
  [r"a) C ngoài đoạn AB, phía B : $CB=4{,}5$ cm, $CA=13{,}5$ cm", r"b) $F_{10}=F_{20}\approx3{,}56\cdot10^{-5}$ N", r"c) không đổi"],
  r"Nhận dạng: đề hỏi <strong>vị trí để điện tích đứng yên</strong> hoặc <strong>hợp lực bằng 0</strong> → $F_1=F_2$, ngược chiều ; cùng dấu : giữa, trái dấu : ngoài, gần điện tích nhỏ."),
 sol(R5, [
  ("Lực do $q_1$",
   [P(r"$q_1$ và $q_0$ cùng dấu nên $q_1$ đẩy $q_0$ ra xa A, dọc đường AC. Độ lớn ($r_1=0{,}030$ m):"),
    M(r"F_1=k\dfrac{|q_1q_0|}{r_1^2}"), M(r"F_1=9\cdot10^{9}\cdot\dfrac{4{,}0\cdot10^{-9}\cdot2{,}0\cdot10^{-9}}{0{,}030^2}"),
    A(r"F_1=8{,}0\cdot10^{-5}\ \text{N}")]),
  ("Lực do $q_2$",
   [P(r"$q_2$ và $q_0$ trái dấu nên $q_2$ hút $q_0$ về B, dọc đường CB. Độ lớn ($r_2=0{,}060$ m):"),
    M(r"F_2=9\cdot10^{9}\cdot\dfrac{12\cdot10^{-9}\cdot2{,}0\cdot10^{-9}}{0{,}060^2}"),
    A(r"F_2=6{,}0\cdot10^{-5}\ \text{N}")]),
  ("Góc giữa hai lực",
   [P(r"$\vec F_1$ nằm trên đường AC, $\vec F_2$ nằm trên đường CB. Hai đường vuông góc, dù mỗi lực hướng về phía nào:"),
    A(r"T:Góc giữa $\vec F_1$ và $\vec F_2$ bằng <strong>$90^\circ$</strong>.")]),
  ("Độ lớn hợp lực",
   [P(r"Hai lực vuông góc nên:"),
    M(r"F=\sqrt{F_1^2+F_2^2}"), M(r"F=\sqrt{(8{,}0\cdot10^{-5})^2+(6{,}0\cdot10^{-5})^2}"), A(r"F=1{,}0\cdot10^{-4}\ \text{N}")]),
  ("Hướng của hợp lực",
   [P(r"Gọi $\varphi$ là góc giữa $\vec F$ và $\vec F_1$. Trong tam giác lực vuông, $F_2$ là cạnh đối, $F_1$ là cạnh kề:"),
    M(r"\tan\varphi=\dfrac{F_2}{F_1}=\dfrac{6{,}0}{8{,}0}=0{,}75"), A(r"\varphi\approx37^\circ"),
    P(r"Hợp lực lệch khỏi phương xa A về phía B.")]),
  ("Kiểm tra",
   [P(r"$F=1{,}0\cdot10^{-4}$ N lớn hơn từng lực thành phần và nhỏ hơn tổng $F_1+F_2=1{,}4\cdot10^{-4}$ N ✓."),
    P(r"Thử lại: $\cos\varphi=F_1/F=0{,}80$ ứng với $\varphi\approx37^\circ$ ✓.")])],
  [r"a) $F_1=8{,}0\cdot10^{-5}$ N ; $F_2=6{,}0\cdot10^{-5}$ N", r"b) $F=1{,}0\cdot10^{-4}$ N", r"c) $\varphi\approx37^\circ$"],
  r"Nhận dạng: đề hỏi <strong>hợp lực của hai điện tích lên một điện tích</strong> → tính từng lực bằng Coulomb, xác định chiều theo dấu, rồi cộng vectơ theo góc giữa hai lực."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>hai quả cầu giống hệt nhau chạm nhau rồi tách</b> → nghĩ tới <b>cộng đại số rồi chia đôi</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Tổng đại số điện tích", r"Tổng đại số $q_1+q_2$ bằng bao nhiêu nC?", -6.0, "nC", 0.05,
       loi=r"Cộng độ lớn của hai điện tích, bỏ qua dấu âm của $q_1$, hoặc trừ hai điện tích cho nhau."),
  buoc("Chia đều cho hai quả", r"Điện tích $q'$ của mỗi quả sau khi tách bằng bao nhiêu nC?", -3.0, "nC", 0.05,
       loi=r"Coi mỗi quả giữ nguyên điện tích cũ, hoặc chia đôi tổng độ lớn rồi gắn dấu của quả lớn hơn mà không cộng có dấu.",
       ke=[(r"Chia đôi tổng đại số vì hai quả giống hệt nhau", True),
           (r"Giữ nguyên điện tích mỗi quả vì hệ cô lập", r"Hệ cô lập chỉ giữ tổng điện tích không đổi ; khi chạm, điện tích phân bố lại đều giữa hai quả giống hệt nhau."),
           (r"Lấy hiệu hai điện tích rồi chia đôi", r"Điện tích được bảo toàn khi cộng có dấu, không phải khi trừ ; hiệu không phải đại lượng bảo toàn.")]),
  buoc("Điện tích dịch chuyển", r"Điện tích của quả 1 đã thay đổi một lượng $|\Delta q|$ bằng bao nhiêu nC?", 5.0, "nC", 0.05,
       loi=r"Dùng tổng điện tích của hệ, hoặc dùng điện tích còn lại của một quả, thay cho độ biến thiên của quả đó.",
       ke=[(r"Lấy độ chênh giữa điện tích sau và trước của quả 1", True),
           (r"Lấy tổng đại số của hệ làm lượng điện tích chuyển", r"Tổng của hệ không đổi trước và sau, nó không cho biết lượng đã chuyển qua."),
           (r"Lấy điện tích còn lại $q'$ của mỗi quả", r"$q'$ là điện tích sau khi tách, không phải phần đã dịch chuyển.")]),
  buoc("Số êlectron chuyển", r"Số êlectron chuyển, theo đơn vị $10^{10}$ hạt, là bao nhiêu?", 3.125, "×10¹⁰ hạt", 0.03,
       loi=r"Nhân $|\Delta q|$ với $|e|$ thay vì chia, hoặc để nguyên đơn vị nC khi chia cho $|e|$ tính bằng C.",
       ke=[(r"Chia $|\Delta q|$ (đổi ra C) cho $|e|$", True),
           (r"Nhân $|\Delta q|$ với $|e|$", r"$|q|=n|e|$ nên $n$ là thương của hai số, không phải tích."),
           (r"Chia điện tích còn lại $|q'|$ cho $|e|$", r"Đó là số êlectron thừa còn lại trên quả, không phải số đã chuyển qua.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>độ lớn lực giữa hai điện tích</b> hoặc <b>tìm điện tích từ lực</b> → nghĩ tới <b>F = k|q₁q₂|/r²</b> sau khi đổi SI.",
  cap_do=1, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Đổi sang đơn vị SI", r"Bình phương khoảng cách $r^2$ bằng bao nhiêu $\text{m}^2$?", 0.09, "m²", 0.001,
       loi=r"Thế luôn $r=30$ (cm) vào công thức, hoặc quên bình phương sau khi đổi sang m."),
  buoc("Độ lớn lực", r"Độ lớn lực tương tác giữa hai điện tích bằng bao nhiêu N?", 1.5, "N", 0.02,
       loi=r"Thế $q$ theo $\mu$C thay vì C, hoặc dùng tổng $q_1+q_2$ thay cho tích $q_1q_2$.",
       ke=[(r"Dùng $F=k\dfrac{|q_1q_2|}{r^2}$ với $q$, $r$ đã đổi sang SI", True),
           (r"Dùng $F=k\dfrac{|q_1+q_2|}{r^2}$", r"Lực tỉ lệ với tích $|q_1q_2|$, không phải với tổng hai điện tích."),
           (r"Dùng $F=k\dfrac{|q_1q_2|}{r}$", r"Lực tỉ lệ nghịch với bình phương khoảng cách, không phải với $r$.")]),
  buoc("Hút hay đẩy", "Hai điện tích hút hay đẩy nhau?",
       loi=r"Dựa vào điện tích nào có độ lớn lớn hơn để kết luận, trong khi loại lực chỉ phụ thuộc dấu của hai điện tích.",
       lua_chon=[(r"Hút, vì $q_1q_2\lt0$ (trái dấu)", True),
                 (r"Đẩy, vì $|q_2|\gt|q_1|$", r"Loại lực không phụ thuộc điện tích nào lớn hơn, chỉ phụ thuộc hai điện tích cùng dấu hay trái dấu."),
                 (r"Hút, vì hai điện tích có độ lớn khác nhau", r"Hai điện tích khác độ lớn mà cùng dấu vẫn đẩy nhau ; chỉ dấu mới quyết định loại lực.")],
       ke=[(r"Xét dấu của tích $q_1q_2$", True),
           (r"So sánh $|q_1|$ với $|q_2|$", r"Độ lớn các điện tích chỉ ảnh hưởng độ lớn lực, không quyết định hút hay đẩy."),
           (r"Tính lại lực với $r$ khác", r"Đổi $r$ chỉ đổi độ lớn lực, loại lực vẫn vậy.")]),
  buoc("Tìm điện tích từ lực", r"Độ lớn mỗi điện tích ở ý b, theo $\mu$C, bằng bao nhiêu?", 1.0, "μC", 0.02,
       loi=r"Quên lấy căn bậc hai vì tích hai điện tích bằng nhau là $q^2$, hoặc dùng $r=10$ cm không đổi sang m.",
       ke=[(r"Viết $F=k\dfrac{q^2}{r^2}$ rồi rút $|q|=r\sqrt{F/k}$", True),
           (r"Rút $|q|=\dfrac{F r^2}{k}$, không lấy căn", r"Hai điện tích bằng nhau nên tích là $q^2$ ; muốn có $|q|$ phải lấy căn bậc hai."),
           (r"Rút $|q|=\dfrac{k r^2}{F}$", r"Lực tỉ lệ thuận với $q^2$ nên $F$ nằm ở tử số của $q^2$, không phải ở mẫu.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>nhúng vào dầu</b>, <b>đổi khoảng cách</b> hay <b>tăng điện tích</b> → nghĩ tới <b>so sánh tỉ lệ</b> F ∝ |q₁q₂|/(εr²).",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Đổi môi trường", r"Lực khi nhúng vào dầu, giữ nguyên khoảng cách, bằng bao nhiêu mN?", 1.0, "mN", 0.02,
       loi=r"Nhân lực với $\varepsilon$ (hiểu ngược), hoặc quên rằng điện môi làm lực giảm."),
  buoc("Bù lại bằng khoảng cách", r"Để lực trong dầu bằng $4{,}0$ mN, hai điện tích phải cách nhau bao nhiêu cm?", 3.0, "cm", 0.05,
       loi=r"Chia thẳng $r$ cho $\varepsilon$ mà không lập phương trình lực, quên rằng $r$ nằm trong bình phương.",
       ke=[(r"Cho lực trong dầu bằng $F_0$ rồi giải $\dfrac{k|q_1q_2|}{\varepsilon r'^2}=F_0$ tìm $r'$", True),
           (r"Chia $r$ cho $\varepsilon$ : $r'=r/\varepsilon$", r"Lực tỉ lệ nghịch với $r^2$ chứ không phải $r$ ; phải lập phương trình lực rồi giải, không chia thẳng."),
           (r"Nhân $r$ với $\varepsilon$ để lực tăng lại", r"Tăng $r$ làm lực giảm thêm ; muốn lực tăng lại phải đưa hai điện tích lại gần.")]),
  buoc("Đổi điện tích và khoảng cách", r"Lực ở ý c bằng bao nhiêu mN?", 48, "mN", 0.5,
       loi=r"Coi lực tỉ lệ nghịch với $r$ thay vì $r^2$, hoặc lấy lực trong dầu (đã tính ở ý a) làm mốc.",
       ke=[(r"Lập tỉ số với tình huống ban đầu : $F\sim|q_1q_2|/r^2$", True),
           (r"Nhân lực với 3 rồi với 2, vì $r$ giảm một nửa", r"Lực tỉ lệ nghịch với bình phương khoảng cách, không phải với khoảng cách."),
           (r"Lấy lực trong dầu làm mốc rồi đổi tiếp", r"Đề đã đưa về không khí nên mốc là $F_0$ ban đầu, không còn $\varepsilon$.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>vị trí để điện tích đứng yên</b> hoặc <b>hợp lực bằng 0</b> → nghĩ tới <b>F₁ = F₂ ngược chiều</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Chọn miền chứa C", "C nằm ở miền nào của đường thẳng AB?",
       loi=r"Đặt C giữa A và B vì thấy hai điện tích ở hai đầu, hoặc đặt gần điện tích có độ lớn lớn hơn.",
       lua_chon=[(r"Giữa A và B", r"Ở giữa, $q_1$ đẩy $q_0$ còn $q_2$ hút $q_0$ cùng về một phía, hai lực cùng chiều nên không triệt tiêu."),
                 (r"Ngoài đoạn AB, phía A", r"Phía A gần điện tích có độ lớn lớn hơn nên lực của $q_1$ luôn trội hơn lực của $q_2$."),
                 (r"Ngoài đoạn AB, phía B", True)]),
  buoc("Lập tỉ số khoảng cách", r"Tỉ số $r_1/r_2$ (với $r_1=CA$, $r_2=CB$) bằng bao nhiêu?", 3.0, "", 0.03,
       loi=r"Lấy luôn tỉ số hai điện tích làm tỉ số khoảng cách, quên lấy căn bậc hai.",
       ke=[(r"Cho $F_{10}=F_{20}$ : $\dfrac{|q_1|}{r_1^2}=\dfrac{|q_2|}{r_2^2}$", True),
           (r"Cho $\dfrac{|q_1|}{r_1}=\dfrac{|q_2|}{r_2}$", r"Lực tỉ lệ nghịch với bình phương khoảng cách, không phải với khoảng cách."),
           (r"Cho $|q_1|r_1^2=|q_2|r_2^2$", r"Điện tích lớn hơn phải ở xa hơn, tức $|q|/r^2$ bằng nhau, không phải $|q|r^2$ bằng nhau.")]),
  buoc("Tính khoảng cách", r"Khoảng cách $CB$ bằng bao nhiêu cm?", 4.5, "cm", 0.05,
       loi=r"Dùng $r_1+r_2=AB$ (điều kiện của C nằm giữa) cho trường hợp C ở ngoài đoạn.",
       ke=[(r"Dùng $r_1-r_2=AB$ vì C ở ngoài đoạn, phía B", True),
           (r"Dùng $r_1+r_2=AB$", r"Đó là điều kiện khi C nằm giữa A và B, mà C đã được xác định ở ngoài đoạn."),
           (r"Dùng $r_1-r_2=AB$ nhưng thay tỉ số khoảng cách bằng tỉ số điện tích", r"Tỉ số khoảng cách phải lấy từ bước trước ; tỉ số điện tích là một đại lượng khác.")]),
  buoc("Kiểm tra bằng lực", r"Lực do $q_1$ tác dụng lên $q_0$ tại C, theo đơn vị $10^{-5}$ N, bằng bao nhiêu?", 3.56, "×10⁻⁵ N", 0.05,
       loi=r"Lấy $r=AB$ thay vì khoảng cách $CA$ từ $q_1$ đến $q_0$, hoặc để $r$ bằng cm khi thế vào công thức.",
       ke=[(r"Dùng $F_{10}=k\dfrac{|q_1q_0|}{CA^2}$ với $CA$ đổi ra m", True),
           (r"Dùng $AB$ làm khoảng cách", r"$AB$ là khoảng cách giữa hai điện tích cố định, không phải từ $q_1$ đến $q_0$."),
           (r"Dùng $CB$ làm khoảng cách", r"$CB$ là khoảng cách từ $q_2$ đến $q_0$, không phải từ $q_1$.")]),
  buoc("Đổi dấu của $q_0$", r"Thay $q_0$ bằng $-2{,}0$ nC thì vị trí cân bằng thay đổi thế nào?",
       loi=r"Nghĩ rằng đổi dấu $q_0$ thì hai lực đổi chỗ cho nhau, hoặc rằng dấu của $q_0$ quyết định vị trí.",
       lua_chon=[(r"Không đổi, vì cả hai lực cùng đổi chiều, vẫn ngược chiều và bằng độ lớn", True),
                 (r"Chuyển sang phía A", r"Đổi dấu $q_0$ đảo cả hai lực cùng lúc, nên quan hệ ngược chiều và bằng độ lớn vẫn giữ nguyên."),
                 (r"Không còn vị trí cân bằng", r"$q_0$ giản ước khỏi điều kiện $F_{10}=F_{20}$, nên vị trí vẫn tồn tại."),],
       ke=[(r"Xét xem $q_0$ có còn trong điều kiện $F_{10}=F_{20}$ sau khi giản ước không", True),
           (r"Tính lại từ đầu với $q_0=-2{,}0$ nC", r"Không cần : $q_0$ xuất hiện ở cả hai vế nên đổi dấu hay độ lớn đều không ảnh hưởng."),
           (r"Đổi chỗ vai trò của $q_1$ và $q_2$", r"$q_1$, $q_2$ là hai điện tích cố định, không đổi vai trò khi đổi dấu $q_0$.")])]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>hợp lực của hai điện tích lên một điện tích</b> → nghĩ tới <b>tính từng lực Coulomb, xét chiều</b>, rồi cộng vectơ.",
  cap_do=3, fading="giau_het", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Lực do $q_1$", r"Độ lớn $F_1$ do $q_1$ tác dụng lên $q_0$, theo đơn vị $10^{-5}$ N?", 8.0, "×10⁻⁵ N", 0.1,
       loi=r"Dùng khoảng cách $AB$ thay cho $CA$, hoặc để $r$ bằng cm khi thế vào công thức."),
  buoc("Lực do $q_2$", r"Độ lớn $F_2$ do $q_2$ tác dụng lên $q_0$, theo đơn vị $10^{-5}$ N?", 6.0, "×10⁻⁵ N", 0.1,
       loi=r"Dùng khoảng cách $CA$ cho cả hai lực, hoặc bỏ dấu âm của $q_2$ làm đảo luôn cả chiều lực.",
       ke=[(r"Dùng $F_2=k\dfrac{|q_2q_0|}{CB^2}$ với $CB$ đổi ra m", True),
           (r"Dùng $F_2=k\dfrac{|q_2q_0|}{CA^2}$", r"Mỗi lực dùng khoảng cách từ chính điện tích đó đến $q_0$ ; $q_2$ ở B nên dùng $CB$."),
           (r"Dùng $F_2=k\dfrac{q_2q_0}{CB^2}$ rồi coi kết quả âm là lực nhỏ hơn", r"Dấu của $q_2q_0$ chỉ cho biết hút hay đẩy, độ lớn lực luôn dương : dùng $|q_2q_0|$.")]),
  buoc("Góc giữa hai lực", r"Góc giữa $\vec F_1$ và $\vec F_2$ bằng bao nhiêu?",
       loi=r"Cho rằng $q_1$ và $q_2$ trái dấu nên hai lực ngược chiều, hoặc cộng độ lớn $F_1+F_2$ mà không xét góc.",
       lua_chon=[(r"$90^\circ$, vì hai lực nằm trên hai đường thẳng CA và CB vuông góc", True),
                 (r"$180^\circ$, vì $q_1$ và $q_2$ trái dấu", r"Dấu chỉ cho biết chiều của mỗi lực dọc đường nối nó với $q_0$ ; hai đường nối này vẫn vuông góc."),
                 (r"$0^\circ$, vì $q_1$ và $q_0$ cùng dấu", r"Một lực đẩy, một lực hút, và chúng nằm trên hai đường vuông góc nên không cùng chiều.")],
       ke=[(r"Xác định phương của mỗi lực rồi xét góc giữa chúng", True),
           (r"Cộng ngay hai độ lớn $F_1+F_2$", r"Chỉ cộng độ lớn được khi hai lực cùng chiều ; ở đây hai lực lệch nhau một góc."),
           (r"Trừ hai độ lớn $|F_1-F_2|$", r"Chỉ trừ được khi hai lực ngược chiều ; chưa biết góc thì chưa chọn được công thức.")]),
  buoc("Độ lớn hợp lực", r"Độ lớn hợp lực, theo đơn vị $10^{-4}$ N, bằng bao nhiêu?", 1.0, "×10⁻⁴ N", 0.02,
       loi=r"Cộng thẳng hai độ lớn, hoặc lấy hiệu hai độ lớn, thay vì dùng căn của tổng bình phương.",
       ke=[(r"Dùng $F=\sqrt{F_1^2+F_2^2}$ vì hai lực vuông góc", True),
           (r"Dùng $F=F_1+F_2$", r"Chỉ đúng khi hai lực cùng chiều ; ở đây chúng vuông góc nên hợp lực nhỏ hơn tổng độ lớn."),
           (r"Dùng $F=|F_1-F_2|$", r"Chỉ đúng khi hai lực ngược chiều ; hai lực vuông góc thì không triệt tiêu một phần như vậy.")]),
  buoc("Hướng của hợp lực", r"Góc $\varphi$ giữa hợp lực và $\vec F_1$ bằng bao nhiêu độ?", 36.9, "độ", 0.5,
       loi=r"Lấy tỉ số ngược $F_1/F_2$ nên ra góc với $\vec F_2$, hoặc dùng $\cos\varphi=F_2/F_1$.",
       ke=[(r"Dùng $\tan\varphi=\dfrac{F_2}{F_1}$ vì $F_2$ là cạnh đối của $\varphi$", True),
           (r"Dùng $\tan\varphi=\dfrac{F_1}{F_2}$", r"Tỉ số này cho góc giữa hợp lực và $\vec F_2$, không phải $\vec F_1$."),
           (r"Dùng $\cos\varphi=\dfrac{F_2}{F_1}$", r"$\cos\varphi=F_1/F$ (cạnh kề trên cạnh huyền) ; $F_2$ là cạnh đối nên không đi với cosin.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ GHI FILE ═════════════
OLD = json.load(open(os.path.join(HERE, "old/35.json")))["questions"]
TU_LUAN = tu_luan_tu(OLD, [1, 3, 2], {1: "Dễ", 3: "Trung bình", 2: "Khó"})
TU_LUAN["body_html"] = re.sub(r"\$[^$]*\$", lambda m: m.group(0).replace("&gt;", r"\gt ").replace("&lt;", r"\lt ").replace(">", r"\gt ").replace("<", r"\lt "), TU_LUAN["body_html"])
write(J, 35, "Bài 16. Lực tương tác giữa hai điện tích", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code) — đã tự giải lại bằng Python 10/10/2026"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
