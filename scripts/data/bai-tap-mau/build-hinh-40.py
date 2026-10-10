"""Bài tập mẫu Bài 21 "Tụ điện" (Vật lí 11, Chương 3) — lesson_id 40. 5 dạng (quét: ket-qua/40.quet-dang.json).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-40.py   (idempotent) → 40.json (review.checked=false cho tới khi kiểm chéo)."""
import json, os, sys, math, re as _re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

# CẢNH BÁO 10/10: có phiên song song cũng đang làm bài 40 (40.json + hinh_40.py) → mặc định KHÔNG ghi đè 40.json; chọn bản nào thì mv sang 40.json.
J = os.path.join(HERE, os.environ.get("BTM_OUT", "40.v2.json"))
TOP_A = "Điện dung, ghép tụ nối tiếp và song song"
TOP_B = "Năng lượng của tụ điện"

# ═════════════ TỰ GIẢI LẠI SỐ LIỆU (độc lập với lời giải) ═════════════
def close(a, b, tol=1e-9): return abs(a - b) <= tol * max(1.0, abs(b))
K9 = 9e9 * 4 * math.pi
# Dạng 1
C1_ = 330e-6
assert close(C1_ * 12, 3.96e-3) and close(C1_ * 25, 8.25e-3) and 12 < 25
# Dạng 2
C2_ = 200e-6; Q2 = C2_ * 300; W2_ = 0.5 * Q2 * 300; W2b = 0.5 * C2_ * 150 ** 2
assert close(Q2, 0.06) and close(W2_, 9.0) and close(0.5 * C2_ * 300 ** 2, 9.0) and close(W2b, 2.25) and close(W2_ / W2b, 4.0)
# Dạng 3
S3 = 0.30 ** 2; d3 = 2.0e-3
Cair = S3 / (K9 * d3); Cdi = 4 * S3 / (K9 * d3); Um = 3e6 * d3
assert close(S3, 0.09) and abs(Cair - 3.979e-10) < 1e-13 and abs(Cdi - 1.5915e-9) < 1e-12 and close(Um, 6000.0)
assert abs(0.04 / (K9 * 1e-3) * (0.09 / 0.04) / 2 - Cair) < 1e-13          # đối chiếu với tụ 354 pF trong lý thuyết
# Dạng 4
c1, c2, c3, U4 = 5.0, 20.0, 6.0, 15.0
c12 = c1 * c2 / (c1 + c2); cb = c12 + c3; q12 = c12 * U4; u1 = q12 / c1; u2 = q12 / c2; q3 = c3 * U4
assert close(c12, 4) and close(cb, 10) and close(q12, 60) and close(u1, 12) and close(u2, 3) and close(q3, 90) and close(u1 + u2, U4)
assert close(q12 + q3, cb * U4) and close(0.5 * c1 * u1 ** 2 + 0.5 * c2 * u2 ** 2 + 0.5 * c3 * U4 ** 2, 0.5 * cb * U4 ** 2)
# Dạng 5 (đơn vị pF, V → nC, μJ)
a1, a2, U5, eps = 600.0, 1200.0, 300.0, 2.0
Cb = a1 * a2 / (a1 + a2); Qn = Cb * U5 / 1000                       # nC
a1n = eps * a1; Cb2 = a1n * a2 / (a1n + a2)
U2 = Qn * 1000 / Cb2; W0 = 0.5 * Cb * U5 ** 2 * 1e-6; Wn = (Qn * 1e-9) ** 2 / (2 * Cb2 * 1e-12) * 1e6; Wc = 0.5 * Cb2 * U5 ** 2 * 1e-6
assert close(Cb, 400) and close(Qn, 120) and close(a1n, 1200) and close(Cb2, 600) and close(U2, 200)
assert close(W0, 18) and close(Wn, 12) and close(Wc, 27) and close(0.5 * Cb2 * U2 ** 2 * 1e-6, Wn)
assert close(Qn * 1000 / a1n + Qn * 1000 / a2, U2)                    # U₁′ + U₂′ = U′
assert close(Qn * 1000 / a1 + Qn * 1000 / a2, U5)                     # trước khi lấp: U₁ + U₂ = U

# ═════════════ TIỆN ÍCH VẼ ═════════════
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"

def rich(s, size=13):
    parts = _re.split(r"_([A-Za-z0-9]+)", s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        out += f'<tspan dy="4" font-size="{size - 3}">{parts[i]}</tspan>'
        if parts[i + 1]:
            out += f'<tspan dy="-4">{parts[i + 1]}</tspan>'
    return out

def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)

def R(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0, op=1):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" '
            f'stroke-width="{sw}" opacity="{op}"/>')

def box_t(x, y, w, h, lines, c="currentColor", size=13):
    b = R(x, y, w, h, c, 2, rx=6)
    n = len(lines)
    for i, s in enumerate(lines):
        b += txt(x + w / 2, y + h / 2 + 5 - (n - 1) * 8 + i * 16, s, c, size, "middle")
    return b

def anim(attr, vals, kts, T):
    v = ";".join(f"{x:.1f}" if isinstance(x, float) else str(x) for x in vals)
    k = ";".join(f"{t:.4f}" for t in kts)
    return f'<animate attributeName="{attr}" values="{v}" keyTimes="{k}" dur="{T:.2f}s" begin="indefinite" fill="freeze"/>'

def W(*pts):                      # dây dẫn
    return poly(list(pts), "currentColor", 2)

def cap_h(x, y, half=16, gap=10):  # tụ vẽ hai bản nằm ngang
    return seg(x - half, y - gap / 2, x + half, y - gap / 2, "currentColor", 3) + seg(x - half, y + gap / 2, x + half, y + gap / 2, "currentColor", 3)

def cap_v(x, y, half=22, gap=20):  # tụ vẽ hai bản thẳng đứng
    return seg(x - gap / 2, y - half, x - gap / 2, y + half, "currentColor", 3) + seg(x + gap / 2, y - half, x + gap / 2, y + half, "currentColor", 3)

def battery_v(x, y):               # nguồn: cực dương ở trên (vạch dài)
    return seg(x - 14, y - 6, x + 14, y - 6, "currentColor", 2.4) + seg(x - 8, y + 6, x + 8, y + 6, "currentColor", 4.5)

def sign(ch, x, y, col, t0, t1, T, size=15):
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{col}" font-size="{size}" font-weight="700" text-anchor="middle" opacity="0">{ch}'
            f'{anim("opacity", [0, 0, 1, 1], [0, t0 / T, t1 / T, 1], T)}</text>')

def lever(x0, y0, x1c, y1c, x1o, y1o, times, vals_closed, T):
    """Khoá K: tay đòn quay quanh (x0,y0); mở ở (x1o,y1o), đóng ở (x1c,y1c). vals_closed[i]=1 nếu đóng tại times[i]."""
    kt = [0] + [t / T for t in times] + [1]
    st = [vals_closed[0]] + list(vals_closed) + [vals_closed[-1]]
    ax = [x1c if s else x1o for s in st]; ay = [y1c if s else y1o for s in st]
    return (f'<line x1="{x0}" y1="{y0}" x2="{x1o}" y2="{y1o}" stroke="currentColor" stroke-width="2.4">'
            f'{anim("x2", [float(v) for v in ax], kt, T)}{anim("y2", [float(v) for v in ay], kt, T)}</line>')

# ═════════════ DẠNG 1 · vỏ tụ, Q = CU (mô phỏng: nạp tụ hoá qua khoá K) ═════════════
def circuit1(animated):
    T = 5.0
    b = W((50, 40), (130, 40)) + W((170, 40), (300, 40), (300, 100)) + W((300, 116), (300, 190), (50, 190), (50, 110)) + W((50, 40), (50, 98))
    b += battery_v(50, 104) + txt(66, 108, "U = 12 V", "currentColor", 13)
    b += cap_h(300, 108, 20, 16)
    b += f'<circle cx="130" cy="40" r="3.2" fill="currentColor"/><circle cx="170" cy="40" r="3.2" fill="currentColor"/>'
    if animated:
        b += lever(130, 40, 170, 40, 166, 22, [0.4, 0.9], [0, 1], T)
    else:
        b += seg(130, 40, 170, 40, "currentColor", 2.4)
    b += txt(150, 62, "K", "currentColor", 13, "middle")
    b += txt(332, 104, "330 μF – 25 V", "currentColor", 13) + txt(332, 124, "Q = ?", ORG, 13)
    if animated:
        for x, t0 in ((284, 1.0), (316, 1.0)):
            b += sign("+", x, 98, RED, t0, t0 + 0.8, T)
        for x, t0 in ((284, 1.0), (316, 1.0)):
            b += sign("−", x, 136, BLUE, t0 + 0.8, t0 + 1.6, T)
    # thang hiệu điện thế (11 px / V)
    k = 11.0; x0 = 50
    b += txt(x0, 206, "hiệu điện thế giữa hai bản", "currentColor", 12, "start", "400")
    b += R(x0, 212, 30 * k, 12, "currentColor", 1.6, op=.7)
    fw = 12 * k
    if animated:
        b += f'<rect x="{x0}" y="212" width="0" height="12" fill="{BLUE}" fill-opacity=".45">{anim("width", [0.0, 0.0, fw, fw], [0, 1.0 / T, 3.0 / T, 1], T)}</rect>'
    else:
        b += f'<rect x="{x0}" y="212" width="{fw}" height="12" fill="{BLUE}" fill-opacity=".45"/>'
    b += seg(x0 + fw, 224, x0 + fw, 234, BLUE, 2.4) + txt(x0 + fw, 250, "12 V", BLUE, 12, "middle")
    b += seg(x0 + 25 * k, 208, x0 + 25 * k, 234, RED, 2.8) + txt(x0 + 25 * k, 250, "25 V (giới hạn)", RED, 12, "middle")
    return b

def d1(kk):
    if kk == 0:
        return fig("d1-0", "0 0 420 258", "Tụ hoá nối với nguồn qua khoá K: đóng K thì hai bản tích điện, thanh hiệu điện thế đầy dần tới vạch 12 V",
                   circuit1(True),
                   "Mô phỏng: đóng khoá K, hai bản của tụ tích điện trái dấu và thanh hiệu điện thế dừng ở giá trị của nguồn. "
                   "Tốc độ phát chỉ để minh hoạ, thực tế tụ nạp xong rất nhanh. " + NOTE)
    return fig("d1-2", "0 0 420 258", "Tụ hoá ghi 330 μF – 25 V nối với nguồn 12 V, điện tích cần tìm",
               circuit1(False),
               "Dữ kiện: hai số ghi trên vỏ tụ và hiệu điện thế nguồn; điện tích của tụ cần tìm. " + NOTE)

# ═════════════ DẠNG 2 · năng lượng tụ (mô phỏng: đồ thị Q–U, vùng tô lớn dần khi nạp) ═════════════
def d2(kk):
    p = f"d2{kk}"
    if kk == 0:
        T = 6.0; ox, oy = 60, 200; kx = 0.9; Hq = 130
        ex, ey = ox + 300 * kx, oy - Hq
        b = f'<clipPath id="{p}c"><rect x="{ox}" y="30" width="0" height="180">{anim("width", [0.0, 0.0, 300 * kx, 300 * kx], [0, 0.5 / T, 5.0 / T, 1], T)}</rect></clipPath>'
        b += f'<g clip-path="url(#{p}c)"><polygon points="{ox},{oy} {ex:.1f},{oy} {ex:.1f},{ey:.1f}" fill="{BLUE}" fill-opacity=".28"/></g>'
        b += arrow(p, "g", ox, oy, 392, oy, 2) + arrow(p, "g", ox, oy, ox, 28, 2)
        b += txt(386, 222, "U (V)", GRN, 13, "end") + txt(70, 40, "Q", GRN, 13)
        for v in (150, 300):
            x = ox + v * kx
            b += seg(x, oy, x, oy + 8, "currentColor", 2) + txt(x, 224, f"{v} V", "currentColor", 12, "middle", "400")
        b += poly([(ox, oy), (ex, ey)], GRN, 2.4)
        b += txt(ex + 8, ey + 4, "Q = ?", ORG, 13)
        b += f'<circle cx="{ox}" cy="{oy}" r="5.5" fill="{RED}" stroke="currentColor" stroke-width="1.5">{anim("cx", [float(ox), float(ox), ex, ex], [0, 0.5 / T, 5.0 / T, 1], T)}{anim("cy", [float(oy), float(oy), ey, ey], [0, 0.5 / T, 5.0 / T, 1], T)}</circle>'
        b += R(86, 54, 14, 12, BLUE, 1.6, BLUE, 0, .35) + txt(106, 65, "vùng tô: W = ?", BLUE, 13)
        return fig("d2-0", "0 0 420 232", "Đồ thị Q theo U của tụ 200 μF, điểm đỏ chạy từ gốc tới 300 V và vùng dưới đường được tô dần",
                   b, "Mô phỏng: nạp tụ tới 300 V, điểm đỏ chạy dọc đường Q–U và vùng tô lớn dần. Tốc độ phát chỉ để minh hoạ, không phải thời gian nạp thật. " + NOTE)
    b = box_t(14, 16, 130, 44, ["C = 200 μF"], "currentColor", 14)
    b += arrow(p, "b", 144, 38, 188, 38, 2.2) + box_t(188, 16, 218, 44, ["nạp tới U = 300 V"], "currentColor", 14)
    b += box_t(188, 84, 218, 44, ["pin yếu: U′ = 150 V"], "currentColor", 14)
    b += arrow(p, "b", 297, 60, 297, 84, 2.2)
    b += txt(14, 166, "Cần tìm:", "currentColor", 13) + txt(14, 188, "Q = ?   W = ?   W′ = ?", ORG, 13) + txt(14, 210, "W giảm bao nhiêu lần ?", ORG, 13)
    return fig("d2-2", "0 0 420 222", "Tụ điện dung 200 μF nạp tới 300 V rồi chỉ nạp tới 150 V, cần tìm điện tích và năng lượng",
               b, "Dữ kiện: điện dung và hai mức hiệu điện thế nạp; điện tích, năng lượng và số lần giảm cần tìm. " + NOTE)

# ═════════════ DẠNG 3 · tụ phẳng (mô phỏng: tấm điện môi trượt vào khe giữa hai bản) ═════════════
def plates(slab):
    b = R(100, 70, 220, 8, "currentColor", 2) + R(100, 130, 220, 8, "currentColor", 2)
    b += dim("d3", "o", 80, 79, 80, 129, "d = 2,0 mm", 72, 108, "end")
    b += txt(210, 56, "bản vuông, cạnh 30 cm", "currentColor", 13, "middle")
    return b

def d3(kk):
    p = f"d3{kk}"
    if kk == 0:
        T = 6.0
        b = plates(True)
        kt = [0, 0.5 / T, 4.5 / T, 1]
        b += (f'<g transform="translate(330 0)"><animateTransform attributeName="transform" type="translate" '
              f'values="330 0;330 0;0 0;0 0" keyTimes="{";".join(f"{t:.4f}" for t in kt)}" dur="{T:.2f}s" begin="indefinite" fill="freeze"/>'
              f'{R(101, 80, 218, 48, BLUE, 2, BLUE, 0, .22)}{txt(210, 109, "điện môi ε = 4", BLUE, 14, "middle")}</g>')
        b += txt(210, 160, "ban đầu: không khí (ε = 1)", "currentColor", 12, "middle", "400") + txt(210, 192, "C = ?", ORG, 14, "middle")
        return fig("d3-0", "0 0 420 206", "Tấm điện môi trượt vào khe giữa hai bản của tụ phẳng", b,
                   "Mô phỏng: tấm điện môi trượt vào, lấp đầy khe giữa hai bản (S và d giữ nguyên). Tốc độ phát chỉ để minh hoạ. " + NOTE)
    b = plates(False)
    b += txt(210, 160, "giữa hai bản: không khí (ε = 1)", "currentColor", 12, "middle", "400")
    b += txt(14, 186, "E_max = 3·10⁶ V/m (không khí)", "currentColor", 12, "start", "400")
    b += txt(14, 206, "Cần tìm: C ; C′ khi ε = 4 ; U_max", ORG, 13)
    return fig("d3-2", "0 0 420 214", "Tụ phẳng hai bản vuông cạnh 30 cm cách nhau 2,0 mm trong không khí, cần tìm điện dung và hiệu điện thế tối đa", b,
               "Dữ kiện: cạnh bản, khoảng cách, điện môi và điện trường giới hạn của không khí; ba đại lượng cần tìm ghi dưới hình. " + NOTE)

# ═════════════ DẠNG 4 · bộ tụ hỗn hợp (mô phỏng: nạp bộ tụ, dấu điện tích hiện dần) ═════════════
def circuit4(animated):
    T = 5.0
    b = W((40, 40), (310, 40)) + W((40, 200), (310, 200)) + W((40, 40), (40, 100)) + W((40, 112), (40, 200))
    b += battery_v(40, 106) + txt(56, 110, "U = 15 V", "currentColor", 13)
    b += W((150, 40), (150, 71)) + cap_h(150, 76, 16, 10) + W((150, 81), (150, 113)) + cap_h(150, 118, 16, 10) + W((150, 123), (150, 200))
    b += W((310, 40), (310, 108)) + cap_h(310, 113, 16, 10) + W((310, 118), (310, 200))
    for x, y in ((150, 40), (150, 200), (310, 40), (310, 200)):
        b += f'<circle cx="{x}" cy="{y}" r="3.2" fill="currentColor"/>'
    b += txt(172, 80, "C_1 = 5 μF", "currentColor", 13) + txt(172, 122, "C_2 = 20 μF", "currentColor", 13) + txt(332, 117, "C_3 = 6 μF", "currentColor", 13)
    if animated:
        pairs = [(130, 66, 130, 96, 1.0), (130, 111, 130, 141, 1.8), (292, 103, 292, 133, 2.6)]
        for xp, yp, xm, ym, t0 in pairs:
            b += sign("+", xp, yp, RED, t0, t0 + 0.7, T) + sign("−", xm, ym, BLUE, t0, t0 + 0.7, T)
    return b

def d4(kk):
    p = f"d4{kk}"
    if kk == 0:
        return fig("d4-0", "0 0 420 214", "Nạp bộ tụ gồm hai nhánh song song, các tụ lần lượt tích điện trái dấu trên hai bản", circuit4(True),
                   "Mô phỏng: các tụ trong bộ lần lượt tích điện, dấu + và − hiện ở hai bản mỗi tụ. Tốc độ phát chỉ để minh hoạ. " + NOTE)
    b = circuit4(False)
    b += txt(40, 226, "Cần tìm: C bộ ; Q và U của từng tụ", ORG, 13)
    return fig("d4-2", "0 0 420 236", "Tụ C₁ nối tiếp C₂ thành một nhánh, nhánh đó song song với C₃, nối vào nguồn 15 V", b,
               "Dữ kiện: ba điện dung và hiệu điện thế nguồn; điện dung bộ, điện tích và hiệu điện thế từng tụ cần tìm. " + NOTE)

# ═════════════ DẠNG 5 · ghép nối tiếp, ngắt nguồn, lấp điện môi (mô phỏng: nối nguồn → ngắt → điện môi trượt vào C₁) ═════════════
def circuit5(animated):
    T = 9.0
    b = W((50, 50), (140, 50)) + W((160, 50), (260, 50)) + W((280, 50), (370, 50), (370, 190), (230, 190))
    b += W((180, 190), (50, 190), (50, 122)) + W((50, 50), (50, 98))
    b += battery_v(50, 110) + txt(58, 156, "U = 300 V", "currentColor", 13)
    b += cap_v(150, 50, 22, 20) + cap_v(270, 50, 22, 20)
    b += f'<circle cx="180" cy="190" r="3.2" fill="currentColor"/><circle cx="230" cy="190" r="3.2" fill="currentColor"/>'
    if animated:
        b += lever(180, 190, 230, 190, 226, 170, [0.5, 1.0, 4.0, 4.6], [0, 1, 1, 0], T)
        b += txt(205, 214, "K", "currentColor", 13, "middle")
        for ch, x, col, t0 in (("+", 131, RED, 1.2), ("−", 170, BLUE, 1.2), ("+", 251, RED, 1.2), ("−", 290, BLUE, 1.2)):
            b += sign(ch, x, 32, col, t0, t0 + 0.8, T)
        kt = [0, 5.5 / T, 7.5 / T, 1]
        b += (f'<g transform="translate(0 -80)"><animateTransform attributeName="transform" type="translate" values="0 -80;0 -80;0 0;0 0" '
              f'keyTimes="{";".join(f"{t:.4f}" for t in kt)}" dur="{T:.2f}s" begin="indefinite" fill="freeze"/>'
              f'{R(141, 29, 18, 42, BLUE, 1.6, BLUE, 0, .3)}{txt(150, 20, "ε = 2", BLUE, 12, "middle")}</g>')
        b += (f'<text x="205" y="238" font-size="13" font-weight="700" text-anchor="middle" fill="currentColor" opacity="0">còn nối nguồn'
              f'{anim("opacity", [0, 0, 1, 1, 0, 0], [0, 1.0 / T, 1.4 / T, 3.8 / T, 4.2 / T, 1], T)}</text>')
        b += (f'<text x="205" y="238" font-size="13" font-weight="700" text-anchor="middle" fill="{ORG}" opacity="0">đã ngắt nguồn'
              f'{anim("opacity", [0, 0, 1, 1], [0, 4.6 / T, 5.0 / T, 1], T)}</text>')
    else:
        b += seg(180, 190, 230, 190, "currentColor", 2.4) + txt(205, 214, "K", "currentColor", 13, "middle")
    b += txt(150, 106, "C_1 = 600 pF", "currentColor", 13, "middle") + txt(150, 124, "(không khí)", "currentColor", 12, "middle", "400")
    b += txt(270, 106, "C_2 = 1200 pF", "currentColor", 13, "middle")
    return b

def d5(kk):
    if kk == 0:
        return fig("d5-0", "0 0 420 246", "Bộ hai tụ nối tiếp được nạp, ngắt khỏi nguồn, rồi tấm điện môi trượt vào giữa hai bản của tụ C₁", circuit5(True),
                   "Mô phỏng: nạp bộ tụ, mở khoá K ngắt nguồn, rồi tấm điện môi trượt vào khe của C₁. Tốc độ phát chỉ để minh hoạ. " + NOTE)
    b = circuit5(False) + txt(50, 238, "Cần tìm: C bộ ; Q mỗi tụ ; U′ ; W′ ; W″", ORG, 13)
    return fig("d5-2", "0 0 420 246", "Hai tụ C₁ = 600 pF và C₂ = 1200 pF nối tiếp vào nguồn 300 V, cần tìm điện dung, điện tích, hiệu điện thế và năng lượng", b,
               "Dữ kiện: hai điện dung, hiệu điện thế nguồn và hằng số điện môi lấp vào C₁; các đại lượng cần tìm ghi dưới hình. " + NOTE)

BUILD = [d1, d2, d3, d4, d5]

# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Số ghi trên vỏ tụ và điện tích: Q = CU, đổi μF ra F", topic=TOP_A,
      problem_html=r"""<p>Trên vỏ một tụ hoá có ghi “330 μF – 25 V”. Nối tụ vào nguồn điện một chiều có hiệu điện thế $U=12$ V cho tới khi nạp xong.</p><ol type="a"><li>Tính điện tích của tụ.</li><li>Tính điện tích lớn nhất mà tụ có thể tích được mà không bị đánh thủng.</li></ol>"""),
 dict(label="Dạng 2 · Dễ · Năng lượng của tụ khi đổi hiệu điện thế nạp", topic=TOP_B,
      problem_html=r"""<p>Tụ điện của một đèn flash rời có điện dung $200\ \mu\text{F}$. Mạch tăng áp nạp tụ tới hiệu điện thế $300$ V, rồi tụ phóng điện qua bóng đèn khi chụp.</p><ol type="a"><li>Tính điện tích và năng lượng của tụ sau khi nạp xong.</li><li>Khi pin yếu, mạch chỉ nạp được tụ tới $150$ V. Tính năng lượng của tụ lúc đó và cho biết năng lượng giảm bao nhiêu lần so với câu a.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Tụ phẳng: điện dung theo cấu tạo và hiệu điện thế không đánh thủng", topic=TOP_A,
      problem_html=r"""<p>Một tụ phẳng gồm hai bản kim loại hình vuông cạnh $30$ cm, đặt đối diện nhau và cách nhau $2{,}0$ mm trong không khí ($\varepsilon=1$). Điện trường lớn nhất mà không khí chịu được là $E_{\max}=3\cdot10^{6}$ V/m.</p><ol type="a"><li>Tính điện dung của tụ.</li><li>Lấp đầy khoảng giữa hai bản bằng một tấm điện môi có $\varepsilon=4$. Tính điện dung của tụ lúc này.</li><li>Tính hiệu điện thế lớn nhất có thể đặt vào tụ không khí ban đầu mà không bị đánh thủng.</li></ol>"""),
 dict(label="Dạng 4 · Trung bình · Bộ tụ ghép hỗn hợp nối tiếp và song song", topic=TOP_A,
      problem_html=r"""<p>Ba tụ điện chưa tích điện có $C_1=5\ \mu\text{F}$, $C_2=20\ \mu\text{F}$ và $C_3=6\ \mu\text{F}$. Tụ $C_1$ ghép nối tiếp với tụ $C_2$ thành một nhánh, nhánh này ghép song song với tụ $C_3$. Hai đầu bộ tụ được nối vào nguồn có $U=15$ V.</p><ol type="a"><li>Tính điện dung của bộ tụ.</li><li>Tính điện tích và hiệu điện thế của từng tụ.</li></ol>"""),
 dict(label="Dạng 5 · Khó · Bộ tụ nối tiếp: ngắt nguồn hay còn nối nguồn khi đổi điện dung", topic=TOP_B,
      problem_html=r"""<p>Hai tụ chưa tích điện có $C_1=600\ \text{pF}$ (tụ phẳng, giữa hai bản là không khí) và $C_2=1200\ \text{pF}$ ghép nối tiếp rồi nối vào nguồn có $U=300$ V cho tới khi nạp xong.</p><ol type="a"><li>Tính điện dung của bộ và điện tích của mỗi tụ.</li></ol><p>Sau đó ngắt bộ tụ khỏi nguồn, rồi lấp đầy khoảng giữa hai bản của $C_1$ bằng điện môi có $\varepsilon=2$.</p><ol type="a" start="2"><li>Tính hiệu điện thế giữa hai đầu bộ tụ và năng lượng của bộ tụ lúc này.</li><li>Nếu lấp điện môi vào $C_1$ mà bộ tụ vẫn nối với nguồn $300$ V thì năng lượng của bộ tụ là bao nhiêu?</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (⚠ chỉ nêu điều kiện; cột 3 không ghi công thức/kết luận) ═════════════
ANALYSIS = [
 [(r'"vỏ một tụ hoá có ghi 330 μF – 25 V"', r"$330\ \mu\text{F}$ ; $25$ V", r"⚠ Hai số trên vỏ có vai trò khác nhau: một số là đặc trưng của tụ, một số là giới hạn không được vượt"),
  (r'"nối tụ vào nguồn một chiều $U=12$ V"', r"$U=12$ V", r"Tụ chịu hiệu điện thế của nguồn ; so với giới hạn ghi trên vỏ"),
  (r'"cho tới khi nạp xong"', r"Tụ đã tích đầy điện", r"Hiệu điện thế giữa hai bản khi đó so với nguồn"),
  (r'"tính điện tích của tụ"', r"Cần: $Q$", r"Quan hệ giữa điện tích, điện dung và hiệu điện thế ; ước số của fara"),
  (r'"điện tích lớn nhất … không bị đánh thủng"', r"Cần: $Q_{\max}$", r"Hiệu điện thế lớn nhất tụ chịu được ; đánh thủng là gì")],
 [(r'"tụ điện … điện dung $200\ \mu\text{F}$"', r"$C=200\ \mu\text{F}$", r"⚠ Điện dung do cấu tạo tụ quyết định, không đổi khi đổi hiệu điện thế nạp"),
  (r'"nạp tụ tới hiệu điện thế $300$ V"', r"$U=300$ V", r"Quan hệ giữa $Q$, $C$, $U$"),
  (r'"tính điện tích và năng lượng của tụ"', r"Cần: $Q$, $W$", r"Năng lượng của tụ nằm ở đâu ; các dạng công thức của năng lượng"),
  (r'"chỉ nạp được tụ tới $150$ V"', r"$U'=150$ V", r"$C$ giữ nguyên, hiệu điện thế nạp đổi: các đại lượng khác đổi thế nào"),
  (r'"giảm bao nhiêu lần so với câu a"', r"Cần: tỉ số hai năng lượng", r"So sánh bằng tỉ số, không bằng hiệu")],
 [(r'"hai bản … hình vuông cạnh $30$ cm"', r"$a=30$ cm", r"Diện tích phần đối diện của hai bản ; đổi cm sang m"),
  (r'"cách nhau $2{,}0$ mm trong không khí ($\varepsilon=1$)"', r"$d=2{,}0$ mm ; $\varepsilon=1$", r"⚠ Công thức tụ phẳng dùng khoảng cách tính bằng mét"),
  (r'"điện trường lớn nhất … $E_{\max}=3\cdot10^{6}$ V/m"', r"$E_{\max}=3\cdot10^{6}$ V/m", r"⚠ Điện trường vượt giá trị này thì không khí bị đánh thủng ; điện trường giữa hai bản là đều"),
  (r'"tính điện dung của tụ"', r"Cần: $C$", r"Điện dung phụ thuộc những yếu tố cấu tạo nào"),
  (r'"lấp đầy … tấm điện môi có $\varepsilon=4$"', r"$\varepsilon=4$ ; $S$, $d$ giữ nguyên", r"Điện môi ảnh hưởng thế nào tới điện dung"),
  (r'"hiệu điện thế lớn nhất … không bị đánh thủng"', r"Cần: $U_{\max}$", r"Liên hệ giữa điện trường đều, hiệu điện thế và khoảng cách hai bản")],
 [(r'"ba tụ điện chưa tích điện … $5$, $20$, $6\ \mu\text{F}$"', r"$C_1=5\ \mu\text{F}$ ; $C_2=20\ \mu\text{F}$ ; $C_3=6\ \mu\text{F}$ ; $Q_0=0$", r"⚠ Công thức ghép tụ dùng được khi các tụ chưa tích điện trước lúc ghép"),
  (r'"$C_1$ ghép nối tiếp với $C_2$ thành một nhánh"', r"Nhánh gồm $C_1$ và $C_2$", r"Đại lượng chung của các tụ nối tiếp ; cách tính điện dung của nhánh"),
  (r'"nhánh này ghép song song với $C_3$"', r"Nhánh $\parallel$ $C_3$", r"Đại lượng chung của hai nhánh song song ; cách tính điện dung khi song song"),
  (r'"hai đầu bộ tụ nối vào nguồn $U=15$ V"', r"$U=15$ V đặt vào cả bộ", r"Hiệu điện thế đặt vào mỗi nhánh song song"),
  (r'"tính điện dung của bộ tụ"', r"Cần: $C_{\text{bộ}}$", r"Hai bước ghép: trong nhánh trước, rồi giữa hai nhánh"),
  (r'"điện tích và hiệu điện thế của từng tụ"', r"Cần: $Q_1,Q_2,Q_3$ ; $U_1,U_2,U_3$", r"Cách chia điện tích và hiệu điện thế trong từng kiểu ghép")],
 [(r'"hai tụ chưa tích điện … $C_1=600$ pF (tụ phẳng, không khí) và $C_2=1200$ pF"', r"$C_1=600$ pF ; $C_2=1200$ pF ; $Q_0=0$", r"⚠ Công thức ghép tụ dùng được khi các tụ chưa tích điện trước lúc ghép"),
  (r'"ghép nối tiếp rồi nối vào nguồn $U=300$ V … nạp xong"', r"$U=300$ V đặt vào cả bộ", r"Đại lượng chung của các tụ nối tiếp ; các tụ chia nhau hiệu điện thế nguồn"),
  (r'"điện dung của bộ và điện tích của mỗi tụ"', r"Cần: $C_{\text{bộ}}$, $Q_1$, $Q_2$", r"Cách tính điện dung khi nối tiếp ; quan hệ giữa $Q$, $C$, $U$"),
  (r'"ngắt bộ tụ khỏi nguồn"', r"Bộ tụ bị cô lập", r"⚠ Đại lượng nào còn bị nguồn giữ cố định, đại lượng nào không còn"),
  (r'"lấp đầy khoảng giữa hai bản của $C_1$ … $\varepsilon=2$"', r"$\varepsilon=2$, chỉ ở $C_1$", r"Điện môi làm đổi điện dung của tụ nào ; điện dung bộ đổi theo thế nào"),
  (r'"hiệu điện thế giữa hai đầu bộ tụ và năng lượng"', r"Cần: $U'$, $W'$", r"Các dạng công thức của năng lượng ; chọn dạng theo đại lượng đã biết"),
  (r'"bộ tụ vẫn nối với nguồn $300$ V … năng lượng"', r"$U$ do nguồn giữ ; cần: $W''$", r"Khi còn nối nguồn thì đại lượng nào giữ nguyên")],
]

# ═════════════ LỜI GIẢI ═════════════
R1 = [r"<strong>Khái niệm:</strong> điện dung $C=\dfrac{Q}{U}$, với $Q$ là độ lớn điện tích trên mỗi bản.",
      r"<strong>Công thức:</strong> $Q=CU$ ; đổi ước số $1\ \mu\text{F}=10^{-6}\ \text{F}$.",
      r"Vỏ tụ ghi điện dung và hiệu điện thế tối đa $U_{\max}$.",
      r"⚠ <strong>Điều kiện:</strong> hiệu điện thế đặt vào không vượt $U_{\max}$, nếu không tụ bị đánh thủng."]
R2 = [r"<strong>Khái niệm:</strong> tụ tích điện thì có điện trường giữa hai bản, điện trường đó dự trữ năng lượng.",
      r"<strong>Công thức:</strong> $W=\tfrac12QU=\tfrac12CU^2=\dfrac{Q^2}{2C}$ ; $Q=CU$.",
      r"Biết $C$ và $U$ thì dùng $\tfrac12CU^2$.",
      r"⚠ <strong>Điều kiện:</strong> $C$ do cấu tạo quyết định nên không đổi khi đổi hiệu điện thế nạp."]
R3 = [r"<strong>Khái niệm:</strong> điện dung của tụ phẳng do cấu tạo quyết định ($S$, $d$, $\varepsilon$), không phụ thuộc $Q$ và $U$.",
      r"<strong>Công thức:</strong> $C=\dfrac{\varepsilon S}{9\cdot10^{9}\cdot4\pi d}$ ; điện trường giữa hai bản là đều: $E=\dfrac{U}{d}$.",
      r"$S$ là diện tích phần đối diện của hai bản (m²) ; $d$ là khoảng cách hai bản (m).",
      r"⚠ <strong>Điều kiện:</strong> không bị đánh thủng khi $E\le E_{\max}$, tức $U\le E_{\max}\,d$."]
R4 = [r"<strong>Nối tiếp:</strong> $Q$ chung ; $U=U_1+U_2$ ; $\dfrac1C=\dfrac1{C_1}+\dfrac1{C_2}$.",
      r"<strong>Song song:</strong> $U$ chung ; $Q=Q_1+Q_2$ ; $C=C_1+C_2$.",
      r"<strong>Công thức:</strong> $Q=CU$ cho từng tụ hoặc từng nhánh.",
      r"⚠ <strong>Điều kiện:</strong> các tụ chưa tích điện trước lúc ghép."]
R5 = [r"<strong>Nối tiếp:</strong> $Q$ chung ; $\dfrac1C=\dfrac1{C_1}+\dfrac1{C_2}$ ; $Q=CU$.",
      r"Lấp điện môi $\varepsilon$ vào một tụ phẳng làm điện dung của riêng tụ đó gấp $\varepsilon$ lần.",
      r"<strong>Năng lượng:</strong> $W=\tfrac12CU^2=\dfrac{Q^2}{2C}$.",
      r"⚠ <strong>Điều kiện:</strong> còn nối nguồn thì $U$ giữ nguyên ; đã ngắt nguồn thì $Q$ giữ nguyên, $U=\dfrac QC$ đổi theo $C$."]

SOLS = [
 sol(R1, [
  ("Đọc số ghi trên vỏ tụ",
   [P(r"Số có đơn vị fara là điện dung, số có đơn vị vôn là hiệu điện thế tối đa:"),
    M(r"C=330\ \mu\text{F}=330\cdot10^{-6}\ \text{F}=3{,}30\cdot10^{-4}\ \text{F}"), M(r"U_{\max}=25\ \text{V}")]),
  ("Điện tích ở 12 V",
   [P("Nạp xong thì hiệu điện thế giữa hai bản bằng hiệu điện thế của nguồn:"), M(r"Q=CU"), M(r"Q=3{,}30\cdot10^{-4}\cdot12"),
    A(r"Q\approx3{,}96\cdot10^{-3}\ \text{C}=3{,}96\ \text{mC}")]),
  ("Điện tích lớn nhất",
   [P(r"Tụ chịu được hiệu điện thế tối đa $25$ V nên điện tích lớn nhất ứng với $U_{\max}$:"), M(r"Q_{\max}=CU_{\max}"), M(r"Q_{\max}=3{,}30\cdot10^{-4}\cdot25"),
    A(r"Q_{\max}\approx8{,}25\cdot10^{-3}\ \text{C}=8{,}25\ \text{mC}")]),
  ("Kiểm tra",
   [P(r"$12\ \text{V}\lt25\ \text{V}$ nên tụ không bị đánh thủng ✓."),
    P(r"$Q_{\max}\gt Q$ vì $U_{\max}\gt U$ ✓."),
    P(r"Điện dung cỡ $10^{-4}$ F nằm trong khoảng $10^{-12}$ đến $10^{-3}$ F của tụ thường gặp ✓.")])],
  [r"a) $Q\approx3{,}96\ \text{mC}$", r"b) $Q_{\max}\approx8{,}25\ \text{mC}$"],
  r"Nhận dạng: đề cho <strong>số ghi trên vỏ tụ</strong> và hỏi <strong>điện tích</strong> → đổi $\mu$F ra F rồi dùng $Q=CU$ ; hỏi <strong>lớn nhất</strong> thì thế $U_{\max}$."),
 sol(R2, [
  ("Điện tích ở 300 V",
   [P(r"Đổi $200\ \mu\text{F}=2{,}00\cdot10^{-4}\ \text{F}$ rồi dùng $Q=CU$:"), M(r"Q=2{,}00\cdot10^{-4}\cdot300"), A(r"Q=0{,}060\ \text{C}=60\ \text{mC}")]),
  ("Năng lượng ở 300 V",
   [P(r"Đã biết $Q$ và $U$ nên dùng dạng $\tfrac12QU$:"), M(r"W=\tfrac12QU"), M(r"W=\tfrac12\cdot0{,}060\cdot300"), A(r"W=9{,}0\ \text{J}")]),
  ("Năng lượng ở 150 V",
   [P(r"$C$ không đổi, chỉ $U$ đổi nên dùng $\tfrac12CU'^2$:"), M(r"W'=\tfrac12CU'^2"), M(r"W'=\tfrac12\cdot2{,}00\cdot10^{-4}\cdot150^2"), A(r"W'=2{,}25\ \text{J}")]),
  ("Số lần giảm",
   [P("So sánh hai năng lượng bằng tỉ số:"), M(r"\dfrac{W}{W'}=\dfrac{9{,}0}{2{,}25}"), A(r"\dfrac{W}{W'}=4")]),
  ("Kiểm tra",
   [P(r"Dạng khác: $\tfrac12CU^2=\tfrac12\cdot2{,}00\cdot10^{-4}\cdot300^2=9{,}0\ \text{J}$ ✓ khớp $\tfrac12QU$."),
    P(r"$U$ giảm $2$ lần mà $W\propto U^2$ nên $W$ giảm $2^2=4$ lần ✓, không phải $2$ lần."),
    P(r"Cỡ vài jun đến chục jun hợp với tụ đèn flash (ví dụ trong bài: $6{,}75$ J) ✓.")])],
  [r"a) $Q=60\ \text{mC}$ ; $W=9{,}0\ \text{J}$", r"b) $W'=2{,}25\ \text{J}$ ; giảm $4$ lần"],
  r"Nhận dạng: đề cho <strong>C không đổi, đổi hiệu điện thế nạp</strong> và hỏi <strong>năng lượng</strong> → $W=\tfrac12CU^2$, $W$ tỉ lệ $U^2$."),
 sol(R3, [
  ("Đổi đơn vị, tính diện tích S",
   [P("Đổi cạnh và khoảng cách ra mét:"), M(r"a=30\ \text{cm}=0{,}30\ \text{m}"), M(r"d=2{,}0\ \text{mm}=2{,}0\cdot10^{-3}\ \text{m}"),
    P(r"Bản hình vuông nên $S=a^2$:"), M(r"S=0{,}30^2"), A(r"S=0{,}090\ \text{m}^2")]),
  ("Điện dung tụ không khí",
   [M(r"C=\dfrac{\varepsilon S}{9\cdot10^{9}\cdot4\pi d}"), M(r"C=\dfrac{1\cdot0{,}090}{9\cdot10^{9}\cdot4\pi\cdot2{,}0\cdot10^{-3}}"),
    A(r"C\approx3{,}98\cdot10^{-10}\ \text{F}=398\ \text{pF}")]),
  ("Điện dung khi lấp điện môi",
   [P(r"$S$ và $d$ giữ nguyên, chỉ $\varepsilon$ đổi từ $1$ lên $4$:"), M(r"C'=\dfrac{4\cdot0{,}090}{9\cdot10^{9}\cdot4\pi\cdot2{,}0\cdot10^{-3}}"),
    A(r"C'\approx1{,}59\cdot10^{-9}\ \text{F}=1{,}59\ \text{nF}")]),
  ("Hiệu điện thế tối đa",
   [P(r"Điện trường đều $E=\dfrac Ud$. Không bị đánh thủng khi $E\le E_{\max}$:"), M(r"U_{\max}=E_{\max}\,d"), M(r"U_{\max}=3\cdot10^{6}\cdot2{,}0\cdot10^{-3}"),
    A(r"U_{\max}=6{,}0\cdot10^{3}\ \text{V}=6{,}0\ \text{kV}")]),
  ("Kiểm tra",
   [P(r"$\dfrac{C'}{C}=\dfrac{1{,}59\ \text{nF}}{0{,}398\ \text{nF}}=4=\varepsilon$ ✓."),
    P(r"So với tụ trong bài ($S=0{,}04\ \text{m}^2$, $d=1$ mm cho $354$ pF): $S$ gấp $2{,}25$ lần, $d$ gấp $2$ lần nên $C\approx354\cdot\dfrac{2{,}25}{2}\approx398$ pF ✓."),
    P(r"$C$ không phụ thuộc $Q$ và $U$: đổi nguồn không làm $C$ đổi ✓.")])],
  [r"a) $C\approx398\ \text{pF}$", r"b) $C'\approx1{,}59\ \text{nF}$", r"c) $U_{\max}=6{,}0\ \text{kV}$"],
  r"Nhận dạng: đề cho <strong>kích thước bản, khoảng cách, điện môi</strong> → $C=\dfrac{\varepsilon S}{9\cdot10^{9}\cdot4\pi d}$ ; hỏi <strong>không bị đánh thủng</strong> → $U_{\max}=E_{\max}d$."),
 sol(R4, [
  ("Điện dung nhánh nối tiếp",
   [P(r"$C_1$ nối tiếp $C_2$ nên cộng nghịch đảo:"), M(r"\dfrac1{C_{12}}=\dfrac1{C_1}+\dfrac1{C_2}"), M(r"C_{12}=\dfrac{C_1C_2}{C_1+C_2}=\dfrac{5\cdot20}{5+20}"),
    A(r"C_{12}=4\ \mu\text{F}")]),
  ("Điện dung cả bộ",
   [P(r"Nhánh $C_{12}$ song song với $C_3$ nên cộng thẳng:"), M(r"C=C_{12}+C_3=4+6"), A(r"C=10\ \mu\text{F}")]),
  ("Điện tích tụ C₁",
   [P("Nhánh nối tiếp mắc trực tiếp vào hai đầu nguồn nên chịu cả $15$ V:"), M(r"Q_{12}=C_{12}U=4\cdot15"),
    P(r"Nối tiếp thì $Q$ chung:"), A(r"Q_1=Q_2=60\ \mu\text{C}")]),
  ("Hiệu điện thế trong nhánh",
   [P(r"Với mỗi tụ dùng $U=\dfrac QC$:"), M(r"U_1=\dfrac{Q_1}{C_1}=\dfrac{60}{5}"), M(r"U_2=\dfrac{Q_2}{C_2}=\dfrac{60}{20}"), A(r"U_1=12\ \text{V}\ ;\ U_2=3\ \text{V}")]),
  ("Tụ C₃",
   [P(r"$C_3$ chung hai đầu bộ nên chịu cả $15$ V:"), M(r"U_3=U=15\ \text{V}"), M(r"Q_3=C_3U_3=6\cdot15"), A(r"Q_3=90\ \mu\text{C}")]),
  ("Kiểm tra",
   [P(r"$U_1+U_2=12+3=15\ \text{V}=U$ ✓."),
    P(r"$Q_{12}+Q_3=60+90=150\ \mu\text{C}=C\,U=10\cdot15$ ✓."),
    P(r"Tụ nhỏ hơn ($5\ \mu\text{F}$) chịu hiệu điện thế lớn hơn ($12$ V so với $3$ V) ✓ đúng với nối tiếp.")])],
  [r"a) $C=10\ \mu\text{F}$", r"b) $Q_1=Q_2=60\ \mu\text{C}$ ; $U_1=12$ V ; $U_2=3$ V", r"$Q_3=90\ \mu\text{C}$ ; $U_3=15$ V"],
  r"Nhận dạng: đề cho <strong>nối tiếp và song song</strong>, hỏi <strong>Q, U từng tụ</strong> → tính $C$ bộ từ trong ra ngoài, rồi đi ngược lại, chia theo $Q$ chung hoặc $U$ chung."),
 sol(R5, [
  ("Điện dung của bộ",
   [M(r"C=\dfrac{C_1C_2}{C_1+C_2}=\dfrac{600\cdot1200}{600+1200}"), A(r"C=400\ \text{pF}")]),
  ("Điện tích mỗi tụ",
   [P("Nối tiếp nên điện tích hai tụ bằng nhau và bằng điện tích của cả bộ:"), M(r"Q=CU=400\cdot10^{-12}\cdot300"),
    A(r"Q_1=Q_2=1{,}20\cdot10^{-7}\ \text{C}=120\ \text{nC}")]),
  ("Đại lượng giữ nguyên khi ngắt nguồn",
   [P("Ngắt nguồn thì hai bản ngoài cùng của bộ bị cô lập, không còn điện tích nào đi vào hay đi ra:"),
    A(r"T:Điện tích $Q=120$ nC giữ nguyên. Hiệu điện thế hai đầu bộ không còn bị nguồn giữ, nó đổi theo điện dung: $U'=\dfrac{Q}{C'}$.")]),
  ("Điện dung mới của bộ",
   [P(r"Chỉ $C_1$ có điện môi nên chỉ $C_1$ gấp $\varepsilon$ lần:"), M(r"C_1'=\varepsilon C_1=2\cdot600=1200\ \text{pF}"),
    P("Hai tụ vẫn nối tiếp:"), M(r"C'=\dfrac{C_1'C_2}{C_1'+C_2}=\dfrac{1200\cdot1200}{1200+1200}"), A(r"C'=600\ \text{pF}")]),
  ("Hiệu điện thế sau khi lấp điện môi",
   [P(r"$Q$ giữ nguyên, điện dung đổi thành $C'$:"), M(r"U'=\dfrac{Q}{C'}=\dfrac{1{,}20\cdot10^{-7}}{600\cdot10^{-12}}"), A(r"U'=200\ \text{V}")]),
  ("Năng lượng sau khi lấp điện môi",
   [P(r"Biết $Q$ và $C'$ nên dùng dạng $\dfrac{Q^2}{2C'}$:"), M(r"W'=\dfrac{Q^2}{2C'}=\dfrac{(1{,}20\cdot10^{-7})^2}{2\cdot600\cdot10^{-12}}"),
    A(r"W'=1{,}2\cdot10^{-5}\ \text{J}=12\ \mu\text{J}")]),
  ("Lấp điện môi khi vẫn nối nguồn",
   [P(r"Nguồn giữ hiệu điện thế hai đầu bộ ở $300$ V, điện dung mới vẫn là $C'$:"), M(r"W''=\tfrac12C'U^2=\tfrac12\cdot600\cdot10^{-12}\cdot300^2"),
    A(r"W''=2{,}7\cdot10^{-5}\ \text{J}=27\ \mu\text{J}")]),
  ("Kiểm tra",
   [P(r"Năng lượng ban đầu: $\tfrac12CU^2=\tfrac12\cdot400\cdot10^{-12}\cdot300^2=18\ \mu\text{J}$."),
    P(r"Ngắt nguồn: $W'=12\ \mu\text{J}\lt18\ \mu\text{J}$ ✓ điện trường kéo tấm điện môi vào nên năng lượng giảm."),
    P(r"Còn nối nguồn: $W''=27\ \mu\text{J}\gt18\ \mu\text{J}$ ✓ nguồn bơm thêm điện tích nên năng lượng tăng."),
    P(r"Sau lấp điện môi: $\dfrac{Q}{C_1'}+\dfrac{Q}{C_2}=100+100=200\ \text{V}=U'$ ✓.")])],
  [r"a) $C=400\ \text{pF}$ ; $Q_1=Q_2=120\ \text{nC}$", r"b) $U'=200\ \text{V}$ ; $W'=12\ \mu\text{J}$", r"c) $W''=27\ \mu\text{J}$"],
  r"Nhận dạng: đề có <strong>ngắt nguồn</strong> hoặc <strong>vẫn nối nguồn</strong> khi đổi tụ → xác định $Q$ giữ hay $U$ giữ trước, rồi chọn công thức năng lượng."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>số ghi trên vỏ tụ</b> và hỏi <b>điện tích</b> → đổi μF ra F rồi dùng <b>Q = CU</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Đọc số ghi trên vỏ tụ", r"Hai số $330\ \mu\text{F}$ và $25$ V ghi trên vỏ tụ cho biết gì?",
       loi=r"Lấy số vôn ghi trên vỏ làm hiệu điện thế đang đặt vào tụ ở câu a.",
       lua_chon=[(r"Điện dung của tụ và hiệu điện thế tối đa được đặt vào", True),
                 (r"Điện tích của tụ và hiệu điện thế luôn đặt vào tụ", r"Số có đơn vị μF là điện dung, không phải điện tích ; còn số vôn là giới hạn chứ không phải giá trị đang đặt vào."),
                 (r"Hiệu điện thế của tụ và điện tích tối đa", r"Fara đo điện dung, vôn đo hiệu điện thế ; điện tích đo bằng culông, vỏ tụ không ghi.")]),
  buoc("Điện tích ở 12 V", r"Điện tích của tụ khi nối nguồn $12$ V, theo đơn vị mC ($10^{-3}$ C)?", 3.96, "mC", 0.04,
       loi=r"Quên đổi μF ra F (ra điện tích cỡ nghìn culông), hoặc thế 25 V thay cho hiệu điện thế của nguồn.",
       ke=[(r"Đổi μF ra F rồi dùng $Q=CU$ với $U$ là hiệu điện thế của nguồn", True),
           (r"Dùng $Q=CU$ với $U$ là số vôn ghi trên vỏ", r"Số vôn trên vỏ là giới hạn chịu được ; hiệu điện thế đặt vào tụ ở câu a là của nguồn."),
           (r"Dùng $C=\dfrac QU$ để tìm điện dung", r"Điện dung đã cho trên vỏ tụ ; đại lượng cần tìm là điện tích.")]),
  buoc("Điện tích lớn nhất", r"Điện tích lớn nhất của tụ không bị đánh thủng, theo đơn vị mC?", 8.25, "mC", 0.08,
       loi=r"Dùng cùng một hiệu điện thế cho cả hai câu, hoặc cộng điện tích của hai bản (nhân đôi).",
       ke=[(r"Đặt hiệu điện thế lớn nhất tụ chịu được vào $Q=CU$", True),
           (r"Nhân đôi điện tích ở câu a vì tụ có hai bản", r"Điện tích của tụ là độ lớn trên một bản, không cộng hai bản."),
           (r"Lấy $Q_{\max}=\dfrac{U_{\max}}{C}$", r"Quan hệ là $Q=CU$ ; phép chia như vậy sai đơn vị.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>C không đổi, đổi hiệu điện thế nạp</b> và hỏi <b>năng lượng</b> → dùng <b>W = ½CU²</b>, W tỉ lệ U².",
  cap_do=1, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Điện tích ở 300 V", r"Điện tích của tụ sau khi nạp tới $300$ V, theo đơn vị mC?", 60, "mC", 0.6,
       loi=r"Quên đổi μF ra F, hoặc nhân với 150 V (hiệu điện thế của câu b)."),
  buoc("Năng lượng ở 300 V", r"Năng lượng của tụ sau khi nạp tới $300$ V, theo jun?", 9.0, "J", 0.1,
       loi=r"Quên hệ số một nửa (tính $QU$), hoặc dùng $\tfrac12CU$ thiếu bình phương.",
       ke=[(r"Biết $Q$ và $U$ nên dùng $W=\tfrac12QU$", True),
           (r"Dùng $W=QU$ vì $Q$ và $U$ đã biết", r"Lúc nạp $U$ tăng dần từ 0, năng lượng là diện tích tam giác dưới đường $Q$–$U$ nên có hệ số một nửa."),
           (r"Dùng $W=\tfrac12CU$ với $C$ và $U$ đã biết", r"Thiếu bình phương: $\tfrac12CU$ có đơn vị culông, không phải jun ; phải là $\tfrac12CU^2$.")]),
  buoc("Năng lượng ở 150 V", r"Năng lượng của tụ khi chỉ nạp tới $150$ V, theo jun?", 2.25, "J", 0.03,
       loi=r"Giữ nguyên điện tích như ở câu a, hoặc chia năng lượng cho 2 vì hiệu điện thế giảm một nửa.",
       ke=[(r"$C$ không đổi, thế $U'$ vào $W'=\tfrac12CU'^2$", True),
           (r"Giữ $Q$ như câu a, thế vào $W'=\tfrac12QU'$", r"$Q=CU$ nên khi $U$ giảm thì $Q$ cũng giảm ; $Q$ không còn như trước."),
           (r"Chia năng lượng ở câu a cho 2 vì $U$ giảm một nửa", r"$W$ tỉ lệ $U^2$ nên không giảm theo tỉ lệ của $U$.")]),
  buoc("Số lần giảm", r"Năng lượng của tụ giảm bao nhiêu lần so với câu a?", 4, "lần", 0.05,
       loi=r"Kết luận năng lượng giảm 2 lần như hiệu điện thế, quên rằng $W$ tỉ lệ $U^2$.",
       ke=[(r"Lấy năng lượng ở câu a chia năng lượng lúc pin yếu", True),
           (r"Lấy tỉ số hai hiệu điện thế", r"Đó là tỉ số hiệu điện thế, không phải tỉ số năng lượng."),
           (r"Lấy hiệu hai năng lượng", r"Hiệu cho biết lượng giảm bằng jun, không phải giảm bao nhiêu lần.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>S, d, ε</b> hoặc <b>không bị đánh thủng</b> → dùng <b>C = εS/(9·10⁹·4πd)</b> và <b>U_max = E_max·d</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Đổi đơn vị, tính diện tích S", r"Diện tích $S$ của mỗi bản theo đơn vị m²?", 0.09, "m²", 0.001,
       loi=r"Lấy cạnh làm diện tích, hoặc bình phương 30 mà không đổi cm sang m."),
  buoc("Điện dung tụ không khí", r"Điện dung của tụ không khí theo đơn vị pF?", 398, "pF", 4,
       loi=r"Để khoảng cách theo mm trong công thức (sai một nghìn lần), hoặc tìm $C$ bằng $\dfrac QU$ trong khi đề không cho $Q$, $U$.",
       ke=[(r"Thế $S$, $d$ đã đổi ra mét và $\varepsilon=1$ vào công thức tụ phẳng", True),
           (r"Dùng $C=\dfrac QU$", r"Đề không cho $Q$ hay $U$, và $C$ do cấu tạo quyết định nên dùng công thức theo $S$, $d$, $\varepsilon$."),
           (r"Thế $d$ theo mm vào công thức mà không đổi ra mét", r"Công thức cần $d$ tính bằng mét ; để mm thì kết quả sai một nghìn lần.")]),
  buoc("Điện dung khi lấp điện môi", r"Điện dung của tụ khi lấp đầy điện môi theo đơn vị nF?", 1.59, "nF", 0.02,
       loi=r"Cho rằng $C$ không đổi vì $C$ không phụ thuộc $Q$, $U$ (quên $C$ có phụ thuộc $\varepsilon$), hoặc chia cho $\varepsilon$ thay vì nhân.",
       ke=[(r"$S$, $d$ giữ nguyên, chỉ $\varepsilon$ đổi: tính lại $C$ theo công thức tụ phẳng", True),
           (r"Giữ nguyên $C$ vì $C$ không phụ thuộc $Q$ và $U$", r"$C$ đúng là không phụ thuộc $Q$, $U$, nhưng có phụ thuộc $\varepsilon$ của điện môi."),
           (r"Chia $C$ cho $\varepsilon$ vì điện môi cản điện trường", r"$\varepsilon$ nằm ở tử số của công thức: $\varepsilon$ lớn thì $C$ lớn, không giảm.")]),
  buoc("Hiệu điện thế tối đa", r"Hiệu điện thế lớn nhất đặt vào tụ không khí mà không bị đánh thủng, theo đơn vị kV?", 6.0, "kV", 0.05,
       loi=r"Lấy $E_{\max}$ chia cho $d$, hoặc coi $E_{\max}$ chính là hiệu điện thế tối đa.",
       ke=[(r"Điện trường đều $E=\dfrac Ud$, không đánh thủng khi $E\le E_{\max}$: $U_{\max}=E_{\max}d$", True),
           (r"Lấy $U_{\max}=\dfrac{E_{\max}}{d}$", r"$E=\dfrac Ud$ suy ra $U=Ed$ ; phép chia này không ra đơn vị vôn."),
           (r"Coi $E_{\max}$ là hiệu điện thế tối đa", r"$E_{\max}$ đo bằng V/m là cường độ điện trường, phải nhân với $d$ mới ra vôn.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>nối tiếp, song song</b> và hỏi <b>Q, U từng tụ</b> → tính <b>C bộ</b> trước, rồi chia theo <b>Q chung / U chung</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Điện dung nhánh nối tiếp", r"Điện dung của nhánh gồm $C_1$ nối tiếp $C_2$ theo đơn vị μF?", 4, "μF", 0.04,
       loi=r"Cộng thẳng hai điện dung (công thức của song song), ra số lớn hơn cả hai tụ."),
  buoc("Điện dung cả bộ", r"Điện dung của cả bộ tụ theo đơn vị μF?", 10, "μF", 0.1,
       loi=r"Coi nhánh nối tiếp với $C_3$ (cộng nghịch đảo) thay vì song song.",
       ke=[(r"Nhánh song song với $C_3$ nên cộng thẳng điện dung nhánh với $C_3$", True),
           (r"Nối tiếp nhánh với $C_3$ nên cộng nghịch đảo", r"Đề nói nhánh ghép song song với $C_3$, nên không cộng nghịch đảo."),
           (r"Cộng nghịch đảo cả ba tụ như nối tiếp", r"Chỉ $C_1$ và $C_2$ nối tiếp ; $C_3$ nằm ở nhánh song song.")]),
  buoc("Điện tích tụ C₁", r"Điện tích của tụ $C_1$ theo đơn vị μC?", 60, "μC", 0.6,
       loi=r"Lấy điện tích của cả bộ gán cho $C_1$, hoặc chia đôi hiệu điện thế nguồn cho hai nhánh.",
       ke=[(r"Nhánh và $C_3$ chung hai đầu bộ nên cả nhánh chịu $U$ của nguồn: lấy $Q=C_{12}U$ rồi áp cho $C_1$", True),
           (r"Lấy $Q=C_{\text{bộ}}U$ của cả bộ rồi gán cho $C_1$", r"$C_{\text{bộ}}U$ là tổng điện tích của cả bộ, gồm cả phần của $C_3$."),
           (r"Chia đôi hiệu điện thế nguồn cho hai nhánh", r"Hai nhánh song song nên mỗi nhánh chịu trọn hiệu điện thế nguồn.")]),
  buoc("Hiệu điện thế trong nhánh", r"Hiệu điện thế trên tụ $C_2$ theo đơn vị V?", 3, "V", 0.03,
       loi=r"Chia đều hiệu điện thế nguồn cho hai tụ nối tiếp, hoặc cho $U_2$ bằng cả hiệu điện thế nguồn.",
       ke=[(r"$C_1$ và $C_2$ nối tiếp nên $Q$ chung: $U_2=\dfrac{Q}{C_2}$", True),
           (r"Chia đều hiệu điện thế nguồn cho hai tụ", r"Nối tiếp thì $Q$ chung, $U$ chia theo nghịch đảo $C$ chứ không chia đều."),
           (r"Cho $U_2$ bằng hiệu điện thế nguồn vì song song với nguồn", r"Chỉ cả nhánh chịu hiệu điện thế nguồn ; hai tụ trong nhánh nối tiếp chia nhau hiệu điện thế ấy.")]),
  buoc("Tụ C₃", r"Điện tích của tụ $C_3$ theo đơn vị μC?", 90, "μC", 0.9,
       loi=r"Cho $Q_3$ bằng $Q_1$ vì cùng nằm trong bộ, hoặc lấy $U_3$ bằng hiệu của nguồn và $U_1$.",
       ke=[(r"$C_3$ chung hai đầu bộ nên $U_3=U$, rồi $Q_3=C_3U_3$", True),
           (r"Cho $Q_3$ bằng $Q_1$ vì cùng nằm trong bộ", r"$Q$ chung chỉ với tụ nối tiếp ; $C_3$ ở nhánh song song nên có điện tích riêng."),
           (r"Lấy $U_3=U-U_1$", r"Phép trừ chỉ dùng trong nhánh nối tiếp ; $C_3$ song song nên $U_3$ bằng $U$ của nguồn.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>ngắt nguồn</b> hay <b>vẫn nối nguồn</b> → xét <b>Q giữ</b> hay <b>U giữ</b> trước, rồi chọn công thức năng lượng.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Điện dung của bộ", r"Điện dung của bộ hai tụ nối tiếp theo đơn vị pF?", 400, "pF", 4,
       loi=r"Cộng thẳng hai điện dung (công thức của song song)."),
  buoc("Điện tích mỗi tụ", r"Điện tích của mỗi tụ khi nối nguồn, theo đơn vị nC?", 120, "nC", 1.2,
       loi=r"Cho mỗi tụ chịu trọn hiệu điện thế nguồn, hoặc chia điện tích của bộ làm đôi cho hai tụ.",
       ke=[(r"Nối tiếp nên $Q$ chung và bằng $Q$ của bộ: $Q=C_{\text{bộ}}U$", True),
           (r"Tính $Q_1=C_1U$ và $Q_2=C_2U$ vì mỗi tụ chịu cả hiệu điện thế nguồn", r"Nối tiếp thì hai tụ chia nhau hiệu điện thế nguồn, mỗi tụ không chịu trọn $U$."),
           (r"Chia điện tích của bộ làm đôi cho hai tụ", r"Nối tiếp thì $Q$ bằng nhau trên mỗi tụ, không chia nhỏ ra.")]),
  buoc("Đại lượng giữ nguyên khi ngắt nguồn", r"Sau khi ngắt khỏi nguồn rồi lấp điện môi, đại lượng nào của bộ giữ nguyên?",
       loi=r"Cho rằng hiệu điện thế vẫn bằng hiệu điện thế nguồn dù đã ngắt nguồn.",
       lua_chon=[(r"Điện tích $Q$ trên mỗi bản", True),
                 (r"Hiệu điện thế hai đầu bộ", r"Không còn nguồn giữ hiệu điện thế ; điện dung đổi thì $U=\dfrac QC$ đổi theo."),
                 (r"Điện dung của bộ", r"Lấp điện môi vào $C_1$ làm điện dung của $C_1$ và của bộ đổi.")],
       ke=[(r"Hỏi trước: đã ngắt nguồn thì đại lượng nào không còn đổi được", True),
           (r"Dùng luôn hiệu điện thế của nguồn cho bộ", r"Đã ngắt nguồn thì hiệu điện thế hai đầu bộ không còn bị nguồn giữ."),
           (r"Tính ngay năng lượng với điện dung cũ", r"Điện dung đã đổi vì $C_1$ thay đổi.")]),
  buoc("Điện dung mới của bộ", r"Điện dung của bộ sau khi lấp điện môi vào $C_1$, theo đơn vị pF?", 600, "pF", 6,
       loi=r"Nhân cả điện dung bộ với ε (quên chỉ C₁ có điện môi), hoặc cộng thẳng hai điện dung.",
       ke=[(r"Chỉ $C_1$ gấp $\varepsilon$ lần, rồi tính lại ghép nối tiếp", True),
           (r"Nhân điện dung bộ cũ với $\varepsilon$", r"Chỉ $C_1$ có điện môi, $C_2$ không đổi nên điện dung bộ không gấp $\varepsilon$ lần."),
           (r"Cộng thẳng $C_1'$ và $C_2$", r"Hai tụ vẫn nối tiếp, phải cộng nghịch đảo.")]),
  buoc("Hiệu điện thế sau khi lấp điện môi", r"Hiệu điện thế giữa hai đầu bộ sau khi lấp điện môi, theo đơn vị V?", 200, "V", 2,
       loi=r"Giữ hiệu điện thế bằng của nguồn, hoặc chia $Q$ cho điện dung cũ.",
       ke=[(r"$Q$ giữ nguyên nên $U'=\dfrac{Q}{C'}$ với $C'$ mới", True),
           (r"Cho $U'$ bằng hiệu điện thế của nguồn", r"Đã ngắt nguồn nên $U'$ không còn bị nguồn giữ."),
           (r"Tính $U'=\dfrac QC$ với $C$ cũ", r"Phải dùng điện dung mới sau khi lấp điện môi.")]),
  buoc("Năng lượng sau khi lấp điện môi", r"Năng lượng của bộ sau khi lấp điện môi (đã ngắt nguồn), theo đơn vị μJ?", 12, "μJ", 0.12,
       loi=r"Dùng hiệu điện thế của nguồn trong công thức năng lượng, hoặc cho rằng năng lượng không đổi vì Q không đổi.",
       ke=[(r"Biết $Q$ và $C'$ nên dùng $W'=\dfrac{Q^2}{2C'}$", True),
           (r"Dùng $W'=\dfrac{C'U^2}{2}$ với $U$ là hiệu điện thế nguồn", r"Hiệu điện thế hai đầu bộ lúc này là $U'$, không phải của nguồn."),
           (r"Giữ $W'=W$ vì $Q$ không đổi", r"$Q$ không đổi nhưng $C$ đổi nên $W=\dfrac{Q^2}{2C}$ đổi theo.")]),
  buoc("Lấp điện môi khi vẫn nối nguồn", r"Năng lượng của bộ khi lấp điện môi mà vẫn nối nguồn, theo đơn vị μJ?", 27, "μJ", 0.3,
       loi=r"Dùng lại cách của câu b (giữ Q) dù bộ vẫn nối nguồn, hoặc quên đổi sang điện dung mới.",
       ke=[(r"Vẫn nối nguồn nên $U$ giữ nguyên: $W''=\tfrac12C'U^2$", True),
           (r"Dùng $Q$ cũ: $W''=\dfrac{Q^2}{2C'}$ như câu b", r"Còn nối nguồn thì nguồn bơm thêm điện tích ; $Q$ không còn giữ nguyên, $U$ mới là đại lượng giữ."),
           (r"Dùng điện dung cũ: $W''=\tfrac12C\,U^2$", r"Điện môi đã làm điện dung đổi ; phải dùng $C'$.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ GHI FILE ═════════════
write(J, 40, "Bài 21. Tụ điện", DANG, BUILD, ANALYSIS, SOLS, None)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo độc lập (kiem-code) — nháp Opus chỉ dùng làm tham khảo, đã viết lại theo quét dạng 5 cấp 1,1,2,2,3"}
raw = json.dumps(d, ensure_ascii=False, indent=1)
bad = [c for c in raw if ord(c) < 32 and c not in "\n"]
assert not bad, f"ký tự điều khiển trong JSON: {bad[:5]}"
assert raw.count("marker-end") == 0
open(J, "w").write(raw)
print("ghi", J, len(raw), "byte")
