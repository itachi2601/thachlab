"""Bài 33 · Bài 14. Bài tập về sóng (Vật lí 11, chương 2 Sóng) — dựng file scripts/data/bai-tap-mau/33.json từ đầu.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-33.py        (mẫu cấu trúc: build-hinh-57.py)
Quy ước theo lý thuyết bài 33: λ = vT = v/f · n ngọn liên tiếp → (n−1)λ · Δφ = 2πd/λ · cùng pha: cực đại d₂−d₁ = kλ, cực tiểu (k+½)λ ·
Young i = λD/a, N_s = 2[L/2i]+1, N_t = 2[L/2i+0,5] · sóng dừng hai đầu cố định L = nλ/2, một đầu kín L = (2n+1)λ/4.
6 dạng, xếp dễ → kết hợp:
  1 đọc hình dạng sóng (λ, T, v) · 2 độ lệch pha · 3 giao thoa hai nguồn cùng pha · 4 khe Young · 5 sóng dừng hai đầu cố định · 6 ống một đầu kín."""
import json, math, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "33.json")
OLD = json.load(open(os.path.join(HERE, "old/33.json")))["questions"]
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
PI = math.pi
VIO = "#a78bfa"


def wave_d(f, x0, x1, step, px, py):
    n = int(round((x1 - x0) / step))
    return "M" + " L".join(f"{px(x0 + i * step):.1f},{py(f(x0 + i * step)):.1f}" for i in range(n + 1))


def wpath(d, c=GRN, w=2.6, dash=""):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"{ds}/>'


def trans(dx, dur):
    return f'<animateTransform attributeName="transform" type="translate" values="0 0;{dx:.1f} 0" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'


def dotanim(cx, cy_vals, dur, c, r=5.5):
    return (f'<circle cx="{cx:.1f}" cy="{cy_vals[0]:.1f}" r="{r}" fill="{c}" stroke="currentColor" stroke-width="1.5">'
            f'{smil("cy", cy_vals, dur)}</circle>')


def clip(p, x, y, w, h):
    return f'<clipPath id="{p}c"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>'


def fmt(x, nd=1):
    s = f"{x:.{nd}f}".replace(".", ",")
    return s.rstrip("0").rstrip(",") if "," in s else s


# ═════════════ Dạng 1 · đọc hình dạng sóng: λ = 12 cm, A = 3 cm, f = 4 Hz ═════════════
L1, A1, F1 = 12.0, 3.0, 4.0
X0_1, SX1, YC1, SY1 = 44, 8, 108, 22


def px1(x): return X0_1 + SX1 * x
def py1(u): return YC1 - SY1 * u
def u1(x, t=0.0): return A1 * math.cos(2 * PI * ((x - 3) / L1 - t * F1))


def frame1():
    b = ""
    for xc in range(0, 46, 3):
        b += seg(px1(xc), 22, px1(xc), 196, "currentColor", 1, "", .13) + seg(px1(xc), 196, px1(xc), 201, "currentColor", 1.4)
        b += lbl(px1(xc), 214, str(xc), "currentColor", 12, "middle", "400")
    for uu in (3, 0, -3):
        b += seg(X0_1, py1(uu), X0_1 + SX1 * 45, py1(uu), "currentColor", 1, "" if uu else "5 4", .3 if uu else .5)
        b += lbl(X0_1 - 6, py1(uu) + 4, ("−" if uu < 0 else "") + str(abs(uu)), "currentColor", 12, "end", "400")
    b += seg(X0_1, 22, X0_1, 196, "currentColor", 1.6) + seg(X0_1, 196, X0_1 + SX1 * 45, 196, "currentColor", 1.6)
    b += lbl(X0_1 + 6, 14, "u (cm)", "currentColor", 12, "start", "700") + lbl(X0_1 + SX1 * 45, 230, "x (cm)", "currentColor", 12, "end", "700")
    return b


def d1(k):
    p = f"d1{k}"; VB = "0 0 420 234"
    b = defs(p) + clip(p, X0_1, 18, SX1 * 45, 180) + frame1()
    if k == 0:
        T_slow = 2.0; ncyc = 2; dur = T_slow * ncyc          # T thật = 0,25 s, chạy chậm 8 lần
        xs = -L1 * ncyc
        path = wpath(wave_d(u1, xs, 45, 0.75, px1, py1))
        b += f'<g clip-path="url(#{p}c)"><g>{trans(SX1 * L1 * ncyc, dur)}{path}</g></g>'
        xP = 21
        vals = [py1(u1(xP, i / 16 * 0.25)) for i in range(16 * ncyc + 1)]
        b += dotanim(px1(xP), vals, dur, ORG)
        b += arrow(p, "r", 236, 30, 292, 30, 3) + lbl(298, 34, "chiều truyền sóng", RED, 12, "start", "700")
        return fig("d1-0", VB, "Đồ thị li độ theo toạ độ của sợi dây có bốn đỉnh sóng liên tiếp, sóng lan sang phải", b,
                   "Mô phỏng: sóng lan sang phải (chạy chậm 8 lần, 2 chu kì), điểm P chỉ dao động lên xuống. Đồ thị tính theo công thức.")
    b += wpath(wave_d(u1, 0, 45, 0.75, px1, py1))
    for j in range(4):
        xc = 3 + L1 * j
        b += dot(px1(xc), py1(A1), 4.5, ORG) + lbl(px1(xc), py1(A1) + 24, str(j + 1), ORG, 13, "middle", "700")
    b += dim(p, "o", px1(3), 26, px1(39), 26, "", 0, 0) + lbl(px1(21), 22, "x₄ − x₁", ORG, 13, "middle", "700")
    b += lbl(px1(21), 190, "4 đỉnh liên tiếp: mấy khoảng?", "currentColor", 12, "middle", "700")
    return fig("d1-2", VB, "Bốn đỉnh sóng được đánh số 1 đến 4; khoảng cách từ đỉnh 1 đến đỉnh 4 nằm giữa các đỉnh", b, "Dữ kiện: đỉnh 1 ở x = 3 cm, đỉnh 4 ở x = 39 cm. " + NOTE)


# ═════════════ Dạng 2 · độ lệch pha: f = 20 Hz, v = 4,0 m/s, MN = 0,45 m ═════════════
F2, V2, XM, XN = 20.0, 4.0, 0.10, 0.55
LAM2 = V2 / F2
X0_2, SX2, YC2, A2PX = 30, 360, 108, 44


def px2(x): return X0_2 + SX2 * x
def py2(u): return YC2 - A2PX * u
def u2(x, t=0.0): return math.cos(2 * PI * (x / LAM2 - t * F2))


def frame2():
    b = ""
    for i in range(0, 11):
        xc = i / 10
        b += seg(px2(xc), 22, px2(xc), 196, "currentColor", 1, "", .13) + seg(px2(xc), 196, px2(xc), 201, "currentColor", 1.4)
        b += lbl(px2(xc), 214, fmt(xc), "currentColor", 12, "middle", "400")
    b += seg(X0_2, py2(0), px2(1.0), py2(0), "currentColor", 1, "5 4", .5)
    b += seg(X0_2, 22, X0_2, 196, "currentColor", 1.6) + seg(X0_2, 196, px2(1.0), 196, "currentColor", 1.6)
    b += lbl(X0_2 - 6, 24, "u", "currentColor", 13, "end", "700") + lbl(px2(1.0), 230, "x (m)", "currentColor", 12, "end", "700")
    return b


def d2(k):
    p = f"d2{k}"; VB = "0 0 420 234"
    b = defs(p) + clip(p, X0_2, 18, SX2 * 1.0, 180) + frame2()
    if k == 0:
        ncyc = 3; T_slow = 1.0; dur = T_slow * ncyc          # T thật = 0,05 s, chạy chậm 20 lần
        path = wpath(wave_d(u2, -LAM2 * ncyc, 1.0, LAM2 / 16, px2, py2))
        b += f'<g clip-path="url(#{p}c)"><g>{trans(SX2 * LAM2 * ncyc, dur)}{path}</g></g>'
        for xc, col, nm in ((XM, RED, "M"), (XN, BLUE, "N")):
            b += seg(px2(xc), 38, px2(xc), 196, col, 1.4, "4 4", .8) + lbl(px2(xc), 14, nm, col, 13, "middle", "700")
            vals = [py2(u2(xc, i / 16 * (1 / F2))) for i in range(16 * ncyc + 1)]
            b += dotanim(px2(xc), vals, dur, col)
        b += dim(p, "o", px2(XM), 44, px2(XN), 44, "", 0, 0) + lbl((px2(XM) + px2(XN)) / 2, 38, "MN = 0,45 m", ORG, 13, "middle", "700")
        b += arrow(p, "r", px2(0.78), 170, px2(0.93), 170, 3) + lbl(px2(0.78) - 4, 176, "chiều truyền", RED, 12, "end", "700")
        return fig("d2-0", VB, "Sóng hình sin trên sợi dây, hai điểm M và N cách nhau 0,45 m theo phương truyền sóng", b,
                   "Mô phỏng: sóng lan sang phải (chạy chậm 20 lần, 3 chu kì), M và N dao động lên xuống tại chỗ. Tính theo công thức.")
    b += wpath(wave_d(u2, 0, 1.0, LAM2 / 16, px2, py2))
    for xc, col, nm in ((XM, RED, "M"), (XN, BLUE, "N")):
        b += seg(px2(xc), 38, px2(xc), 196, col, 1.4, "4 4", .8) + lbl(px2(xc), 14, nm, col, 13, "middle", "700") + dot(px2(xc), py2(u2(xc)), 5, col)
    b += dim(p, "o", px2(XM), 44, px2(XN), 44, "", 0, 0) + lbl((px2(XM) + px2(XN)) / 2, 38, "d = MN", ORG, 13, "middle", "700")
    b += lbl(px2(0.55), 176, "λ = v / f  →  Δφ = 2πd / λ", "currentColor", 13, "middle", "700")
    return fig("d2-2", VB, "M và N trên phương truyền sóng cách nhau d; độ lệch pha tính theo d chia bước sóng", b, "Dữ kiện: d đo dọc phương truyền sóng. " + NOTE)


# ═════════════ Dạng 3 · giao thoa: AB = 12 cm, f = 25 Hz, v = 0,50 m/s (λ = 2 cm), MA = 15, MB = 8 ═════════════
PXCM3 = 14
A3 = (70, 150); B3 = (70 + 12 * PXCM3, 150)
_mx = (15 ** 2 - 8 ** 2 + 12 ** 2) / 24
M3 = (A3[0] + _mx * PXCM3, A3[1] - math.sqrt(15 ** 2 - _mx ** 2) * PXCM3)


def ring(c, cx, cy, j, n, lam_px, dur):
    R = (n - j) * lam_px
    if j == 0:
        v, kt = f"0;{R:.1f}", ""
    else:
        v, kt = f"0;0;{R:.1f}", f' keyTimes="0;{j / n:.3f};1"'
    return (f'<circle cx="{cx}" cy="{cy}" r="0" fill="none" stroke="{c}" stroke-width="1.5" opacity=".55">'
            f'<animate attributeName="r" values="{v}"{kt} dur="{dur:.2f}s" begin="indefinite" fill="freeze"/></circle>')


def d3(k):
    p = f"d3{k}"; VB = "0 0 420 198"
    b = defs(p) + clip(p, 0, 0, 420, 198)
    if k == 0:
        n = 8; lam_px = 2 * PXCM3; T_slow = 0.6; dur = n * T_slow          # T thật = 0,04 s, chạy chậm 15 lần
        rings = "".join(ring(BLUE, A3[0], A3[1], j, n, lam_px, dur) + ring(ORG, B3[0], B3[1], j, n, lam_px, dur) for j in range(n))
        b += f'<g clip-path="url(#{p}c)">{rings}</g>'
    b += seg(*A3, *M3, BLUE, 2, "6 4") + seg(*B3, *M3, ORG, 2, "6 4") + seg(*A3, *B3, "currentColor", 2.2)
    b += dot(*A3, 5.5, BLUE) + dot(*B3, 5.5, ORG) + dot(*M3, 5.5, "currentColor")
    b += lbl(A3[0] - 8, A3[1] + 18, "A", BLUE, 14, "end", "700") + lbl(B3[0] + 6, B3[1] + 18, "B", ORG, 14, "start", "700") + lbl(M3[0] + 10, M3[1] + 4, "M", "currentColor", 14, "start", "700")
    b += lbl((A3[0] + M3[0]) / 2 - 6, (A3[1] + M3[1]) / 2 - 4, "15 cm", BLUE, 13, "end", "700") if k == 0 else lbl((A3[0] + M3[0]) / 2 - 6, (A3[1] + M3[1]) / 2 - 4, "d₁", BLUE, 14, "end", "700")
    b += lbl((B3[0] + M3[0]) / 2 + 8, (B3[1] + M3[1]) / 2 + 22, "8 cm", ORG, 13, "start", "700") if k == 0 else lbl((B3[0] + M3[0]) / 2 + 8, (B3[1] + M3[1]) / 2 + 22, "d₂", ORG, 14, "start", "700")
    b += dim(p, "g", A3[0], 176, B3[0], 176, "AB = 12 cm" if k == 0 else "AB", (A3[0] + B3[0]) / 2 - 36 if k == 0 else (A3[0] + B3[0]) / 2 - 10, 193)
    if k == 0:
        return fig("d3-0", VB, "Hai nguồn A và B tạo các vòng sóng tròn lan rộng trên mặt nước, điểm M cách A 15 cm và cách B 8 cm", b,
                   "Mô phỏng: hai nguồn cùng pha, các vòng sóng lan ra (chạy chậm 15 lần). Bán kính vòng tính theo v và t.")
    b += lbl(14, 30, "|d₁ − d₂| / λ ?", "currentColor", 13, "start", "700") + lbl(14, 52, "k nguyên trong (−AB/λ; AB/λ)", "currentColor", 12, "start", "700")
    return fig("d3-2", VB, "M cách A một đoạn d1 và cách B một đoạn d2; cần so hiệu d1 trừ d2 với bước sóng và đếm giá trị k trên AB", b, "Dữ kiện: d₁, d₂ của M và AB. " + NOTE)


# ═════════════ Dạng 4 · khe Young: a = 0,5 mm, D = 1,5 m, λ = 0,60 µm → i = 1,8 mm; L = 17 mm; P ở 6,3 mm ═════════════
I4 = 50.0; X04 = 210.0; YB4 = 120


def d4(k):
    p = f"d4{k}"; VB = "0 0 420 214"
    if k == 0:
        Ifn = lambda x: math.cos(PI * x / I4) ** 2
        xs = list(range(40, 381, 4))
        pts = [(x, YB4 - 58 * Ifn(x - X04)) for x in xs]
        stops = "".join(f'<stop offset="{(x - 40) / 340 * 100:.1f}%" stop-color="{ORG}" stop-opacity="{Ifn(x - X04):.2f}"/>' for x in range(40, 381, 10))
        b = defs(p) + f'<linearGradient id="{p}g" x1="0" x2="1" y1="0" y2="0">{stops}</linearGradient>'
        b += seg(40, YB4, 380, YB4, "currentColor", 1.4) + lbl(380, YB4 + 16, "x", "currentColor", 12, "end", "700") + lbl(44, 24, "độ sáng I", "currentColor", 12, "start", "700")
        b += poly(pts, GRN, 2.4) + f'<rect x="40" y="138" width="340" height="26" fill="url(#{p}g)" stroke="currentColor" stroke-width="1.2"/>'
        b += lbl(X04, 184, "vân trung tâm", "currentColor", 12, "middle", "700")
        b += seg(X04, YB4 - 58, X04, 196, ORG, 1, "3 4", .6) + seg(X04 + I4, YB4 - 58, X04 + I4, 196, ORG, 1, "3 4", .6)
        b += dim(p, "o", X04, 198, X04 + I4, 198, "i = ?", X04 + I4 / 2 - 14, 212)
        b += lbl(44, 44, "Cận cảnh vùng quanh vân trung tâm", "currentColor", 12, "start", "400")
        b += ball([(x, YB4 - 58 * Ifn(x - X04)) for x in range(52, 369, 8)], 0, 4.0 / 40)
        return fig("d4-0", VB, "Cường độ sáng trên màn của thí nghiệm Young: các vân sáng và vân tối xen kẽ đối xứng quanh vân trung tâm", b,
                   "Mô phỏng: điểm quét dọc màn theo độ sáng tính từ công thức, vùng quanh vân trung tâm (chạy 4 s). Không phải cả trường giao thoa.")
    b = defs(p)
    b += f'<rect x="30" y="86" width="360" height="30" fill="none" stroke="currentColor" stroke-width="2"/>'
    b += seg(210, 80, 210, 122, "currentColor", 1.6, "4 4") + lbl(210, 74, "O", "currentColor", 13, "middle", "700")
    b += dim(p, "b", 30, 140, 390, 140, "L (trường giao thoa)", 210 - 66, 160)
    b += dim(p, "o", 210, 52, 210 + 38.1, 52, "", 0, 0) + lbl(210 + 19, 46, "i", ORG, 14, "middle", "700")
    b += lbl(30, 186, "N_s = 2[L / 2i] + 1", RED, 13, "start", "700") + lbl(30, 206, "N_t = 2[L / 2i + 0,5]", BLUE, 13, "start", "700")
    b += lbl(260, 186, "[ ] = phần nguyên", "currentColor", 12, "start", "400")
    return fig("d4-2", "0 0 420 214", "Trường giao thoa có bề rộng L đối xứng qua vân trung tâm O, khoảng vân i là đơn vị để đếm vân", b, "Dữ kiện: số vân tính theo L chia cho 2i. " + NOTE)


# ═════════════ Dạng 5 · sóng dừng hai đầu cố định: L = 0,60 m, 3 bụng, f = 150 Hz ═════════════
XA5, XB5, YC5, AMP5 = 50, 370, 92, 54


def d5(k):
    p = f"d5{k}"; VB = "0 0 420 196" if k == 0 else "0 0 420 214"
    n = 3
    sh = lambda x: -AMP5 * math.sin(n * PI * (x - XA5) / (XB5 - XA5))
    pts = [(x, YC5 + sh(x)) for x in range(XA5, XB5 + 1, 4)]
    b = defs(p)
    b += seg(XA5, YC5 - 22, XA5, YC5 + 22, "currentColor", 4) + seg(XB5, YC5 - 22, XB5, YC5 + 22, "currentColor", 4)
    b += lbl(XA5 - 8, YC5 + 42, "A", "currentColor", 14, "end", "700") + lbl(XB5 + 8, YC5 + 42, "B", "currentColor", 14, "start", "700")
    b += seg(XA5, YC5, XB5, YC5, "currentColor", 1, "5 4", .4)
    yd = 160 if k == 0 else 184
    b += dim(p, "g", XA5, yd, XB5, yd, "L = 0,60 m" if k == 0 else "L", (XA5 + XB5) / 2 - (30 if k == 0 else 6), yd + 20)
    if k == 0:
        ncyc = 3; T_slow = 1.0; dur = T_slow * ncyc          # T thật ≈ 6,7 ms, chạy chậm 150 lần
        vals = ";".join(f"1 {math.cos(2 * PI * i / 16):.3f}" for i in range(16 * ncyc + 1))
        b += poly(pts, GRN, 1.2, "4 4", .45) + poly([(x, YC5 - sh(x) + 0) for x, _ in pts], GRN, 1.2, "4 4", .45)
        b += (f'<g transform="translate(0,{YC5})"><g><animateTransform attributeName="transform" type="scale" values="{vals}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'
              + wpath(wave_d(lambda x: sh(x), XA5, XB5, 4, lambda x: x, lambda y: y), GRN, 3) + '</g></g>')
        return fig("d5-0", VB, "Sợi dây AB hai đầu cố định có sóng dừng với ba múi sóng, các điểm giữa dao động lên xuống còn hai đầu đứng yên", b,
                   "Mô phỏng: sóng dừng trên dây (chạy chậm 150 lần, 3 chu kì). Hình dạng tính theo công thức.")
    b += poly(pts, GRN, 2.8)
    for j in range(n + 1):
        xn = XA5 + (XB5 - XA5) * j / n
        b += dot(xn, YC5, 5, ORG)
    for j in range(n):
        xb = XA5 + (XB5 - XA5) * (j + 0.5) / n
        b += lbl(xb, YC5 + (-AMP5 - 8 if j % 2 == 0 else AMP5 + 18), "bụng", BLUE, 12, "middle", "700")
    b += lbl(XA5 - 20, 12, "chấm cam: nút (cả hai đầu)", ORG, 12, "start", "700")
    b += lbl(XB5 + 20, 12, "L = n · λ/2", "currentColor", 13, "end", "700")
    return fig("d5-2", VB, "Sóng dừng với các nút đánh dấu chấm cam, mỗi múi sóng dài nửa bước sóng, hai đầu cố định đều là nút", b, "Dữ kiện: hai đầu là nút; một múi = λ/2. " + NOTE)


# ═════════════ Dạng 6 · ống một đầu kín: 1020 Hz và 1700 Hz liên tiếp, v = 340 m/s → f₁ = 340 Hz, L = 0,25 m ═════════════
XC6, XO6, YT6 = 60, 360, 100
H6 = 34


def d6(k):
    p = f"d6{k}"; VB = "0 0 420 200"
    b = defs(p)
    b += f'<rect x="{XC6}" y="{YT6 - H6}" width="{XO6 - XC6}" height="{2 * H6}" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    b += seg(XC6, YT6 - H6, XC6, YT6 + H6, "currentColor", 6)
    b += lbl(XC6, YT6 - H6 - 12, "đầu kín", "currentColor", 13, "middle", "700") + lbl(XO6, YT6 - H6 - 12, "đầu hở", "currentColor", 13, "middle", "700")
    b += dim(p, "g", XC6, 164, XO6, 164, "L = ?" if k == 0 else "L", (XC6 + XO6) / 2 - 20, 186)
    if k == 0:
        ncol = 10; ncyc = 2; T_slow = 1.0; dur = ncyc * T_slow          # âm cơ bản 340 Hz, chạy chậm 340 lần
        for j in range(ncol):
            xj = XC6 + (j + 0.5) * (XO6 - XC6) / ncol
            amp = 16 * math.sin(PI / 2 * (xj - XC6) / (XO6 - XC6))
            vals = ";".join(f"{amp * (math.cos(2 * PI * i / 16) - 1):.1f} 0" for i in range(16 * ncyc + 1))
            g = "".join(dot(xj + amp, YT6 + dy, 3.4, GRN) for dy in (-20, 0, 20))
            b += f'<g><animateTransform attributeName="transform" type="translate" values="{vals}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>{g}</g>'
        return fig("d6-0", VB, "Ống hình trụ một đầu bịt kín một đầu hở, các lớp không khí dao động dọc theo ống khi có sóng dừng", b,
                   "Mô phỏng: các lớp không khí dao động trong ống ở âm cơ bản (chạy chậm 340 lần, 2 chu kì). Biên độ tính theo công thức.")
    env = [(x, YT6 - H6 * 0.9 * math.sin(PI / 2 * (x - XC6) / (XO6 - XC6))) for x in range(XC6, XO6 + 1, 6)]
    b += poly(env, GRN, 2, "5 4") + poly([(x, 2 * YT6 - y) for x, y in env], GRN, 2, "5 4")
    b += dot(XC6, YT6, 5, ORG) + lbl(XC6 + 10, YT6 + 28, "nút", ORG, 12, "start", "700")
    b += dot(XO6, YT6, 5, BLUE) + lbl(XO6 - 8, YT6 + 4, "bụng", BLUE, 12, "end", "700")
    b += lbl(XC6, 22, "cơ bản: L = λ/4", "currentColor", 13, "start", "700") + lbl(XO6, 22, "f_m = m·f₁, m lẻ", "currentColor", 13, "end", "700")
    return fig("d6-2", VB, "Ống một đầu kín là nút, đầu hở là bụng; ở âm cơ bản chiều dài ống bằng một phần tư bước sóng", b, "Dữ kiện: đầu kín là nút, đầu hở là bụng. " + NOTE)


BUILD = [d1, d2, d3, d4, d5, d6]

# ───────────────────────── Đề + bảng phân tích ─────────────────────────
DANG = [
 dict(label="Dạng 1 · Dễ · Đọc hình dạng sóng: bước sóng, chu kì, tốc độ truyền sóng",
      topic="Bước sóng, chu kì, tần số, tốc độ truyền sóng",
      problem_html="<p>Một sóng hình sin truyền trên sợi dây đàn hồi theo chiều dương của trục Ox với tần số $f=4\\ \\text{Hz}$. Hình vẽ là hình dạng của một đoạn dây tại một thời điểm, trục $u$ là li độ, trục $x$ là toạ độ dọc theo dây; hình cho thấy bốn đỉnh sóng liên tiếp.</p>"
                   "<ol type=\"a\"><li>Đọc hình để tính bước sóng $\\lambda$.</li><li>Tính chu kì $T$.</li><li>Tính tốc độ truyền sóng $v$ theo đơn vị m/s.</li></ol>"),
 dict(label="Dạng 2 · Trung bình · Độ lệch pha giữa hai điểm trên phương truyền sóng",
      topic="Phương trình sóng và đồ thị sóng",
      problem_html="<p>Trên một sợi dây đàn hồi rất dài có sóng hình sin lan truyền với tần số $f=20\\ \\text{Hz}$, tốc độ truyền sóng $v=4{,}0\\ \\text{m/s}$. Hai điểm M và N nằm trên dây, cách nhau $MN=0{,}45\\ \\text{m}$ theo phương truyền sóng (hình vẽ).</p>"
                   "<ol type=\"a\"><li>Tính bước sóng $\\lambda$.</li><li>Tính độ lệch pha giữa dao động tại M và tại N.</li><li>M và N dao động cùng pha, ngược pha, vuông pha hay không đặc biệt?</li></ol>"),
 dict(label="Dạng 3 · Khó · Giao thoa hai nguồn cùng pha: loại điểm M và đếm cực đại, cực tiểu trên AB",
      topic="Xác định số điểm cực đại, cực tiểu trên đoạn thẳng",
      problem_html="<p>Trên mặt nước có hai nguồn kết hợp A và B dao động cùng pha, cùng tần số $f=25\\ \\text{Hz}$, cách nhau $AB=12\\ \\text{cm}$. Tốc độ truyền sóng là $v=0{,}50\\ \\text{m/s}$. Điểm M cách A là $15\\ \\text{cm}$ và cách B là $8\\ \\text{cm}$.</p>"
                   "<ol type=\"a\"><li>Tính bước sóng $\\lambda$.</li><li>M nằm trên cực đại hay cực tiểu giao thoa?</li><li>Trên đoạn AB có bao nhiêu điểm dao động với biên độ cực đại, bao nhiêu điểm với biên độ cực tiểu?</li></ol>"),
 dict(label="Dạng 4 · Khó · Khe Young: khoảng vân, đếm vân sáng, vân tối",
      topic="Giao thoa ánh sáng qua khe Young",
      problem_html="<p>Trong thí nghiệm Young về giao thoa ánh sáng, hai khe cách nhau $a=0{,}50\\ \\text{mm}$, màn cách hai khe $D=1{,}5\\ \\text{m}$, ánh sáng đơn sắc có bước sóng $\\lambda=0{,}60\\ \\mu\\text{m}$. Trường giao thoa trên màn rộng $L=17\\ \\text{mm}$, đối xứng qua vân sáng trung tâm.</p>"
                   "<ol type=\"a\"><li>Tính khoảng vân $i$.</li><li>Trên trường giao thoa có bao nhiêu vân sáng, bao nhiêu vân tối?</li><li>Điểm P cách vân sáng trung tâm $6{,}3\\ \\text{mm}$ là vân sáng hay vân tối?</li></ol>"),
 dict(label="Dạng 5 · Khó · Sóng dừng trên dây hai đầu cố định: bước sóng, tốc độ, số nút, tần số mới",
      topic="Tính bước sóng, tốc độ truyền sóng từ sóng dừng",
      problem_html="<p>Sợi dây đàn hồi AB dài $L=0{,}60\\ \\text{m}$ căng ngang, hai đầu A, B cố định (coi là nút). Kích thích dây với tần số $f=150\\ \\text{Hz}$ thì trên dây có sóng dừng như hình vẽ.</p>"
                   "<ol type=\"a\"><li>Tính bước sóng và tốc độ truyền sóng trên dây.</li><li>Trên dây có bao nhiêu nút (kể cả A và B)?</li><li>Giữ nguyên dây và lực căng, phải đổi tần số thành bao nhiêu để trên dây có 4 bụng sóng?</li></ol>"),
 dict(label="Dạng 6 · Khó · Sóng dừng trong ống một đầu kín: hai tần số cộng hưởng liên tiếp",
      topic="Nút, bụng sóng và điều kiện có sóng dừng",
      problem_html="<p>Một ống sáo hình trụ một đầu bịt kín, một đầu hở. Khi thổi vào miệng ống, không khí trong ống cộng hưởng ở hai tần số liên tiếp là $1020\\ \\text{Hz}$ và $1700\\ \\text{Hz}$. Tốc độ truyền âm trong không khí là $340\\ \\text{m/s}$.</p>"
                   "<ol type=\"a\"><li>Tìm tần số âm cơ bản của ống.</li><li>Tìm chiều dài ống.</li><li>Ở tần số $1700\\ \\text{Hz}$, trong ống có mấy bụng sóng (kể cả đầu hở)?</li></ol>"),
]

DK_PHA = "⚠ Chỉ áp dụng cho hai điểm cùng nằm trên một phương truyền sóng"
ANALYSIS = [
 [("\"sóng hình sin … theo chiều dương trục Ox với tần số $f=4$ Hz\"", "$f=4$ Hz", "Sóng hình sin: $T=\\dfrac{1}{f}$ · $v=\\lambda f$"),
  ("\"hình cho thấy bốn đỉnh sóng liên tiếp\" (đỉnh đầu ở $x=3$ cm, đỉnh cuối ở $x=39$ cm)", "$x_1=3$ cm; $x_4=39$ cm; $n=4$ đỉnh", "⚠ $n$ đỉnh liên tiếp chỉ có $n-1$ khoảng, mỗi khoảng là một bước sóng"),
  ("\"tính bước sóng $\\lambda$\"", "Cần $\\lambda$", "$x_4-x_1=(n-1)\\lambda$"),
  ("\"tính chu kì $T$\"", "Cần $T$", "$T=\\dfrac{1}{f}$"),
  ("\"tốc độ truyền sóng theo đơn vị m/s\"", "Cần $v$ (m/s)", "⚠ $v=\\lambda f$ — đổi $\\lambda$ sang m trước khi nhân")],
 [("\"sóng hình sin … $f=20$ Hz, $v=4{,}0$ m/s\"", "$f=20$ Hz; $v=4{,}0$ m/s", "$\\lambda=\\dfrac{v}{f}$"),
  ("\"M, N cách nhau $0{,}45$ m theo phương truyền sóng\"", "$d=MN=0{,}45$ m", DK_PHA + "; $\\Delta\\varphi=\\dfrac{2\\pi d}{\\lambda}$"),
  ("\"tính độ lệch pha\"", "Cần $\\Delta\\varphi$", "$\\Delta\\varphi=\\dfrac{2\\pi d}{\\lambda}$ (N ở xa nguồn hơn nên trễ pha hơn M)"),
  ("\"cùng pha, ngược pha, vuông pha hay không đặc biệt?\"", "Cần phân loại", "⚠ Bỏ các bội của $2\\pi$ rồi so phần dư: cùng pha $2k\\pi$ · ngược pha $(2k+1)\\pi$ · vuông pha $(2k+1)\\dfrac{\\pi}{2}$")],
 [("\"hai nguồn kết hợp A và B dao động cùng pha\"", "Cùng pha", "⚠ Cực đại $d_2-d_1=k\\lambda$ · cực tiểu $(k+\\tfrac12)\\lambda$ — chỉ đúng khi hai nguồn cùng pha"),
  ("\"$f=25$ Hz\", \"$v=0{,}50$ m/s\"", "$f=25$ Hz; $v=50$ cm/s", "$\\lambda=\\dfrac{v}{f}$ (cùng đơn vị cm)"),
  ("\"M cách A là 15 cm và cách B là 8 cm\"", "$d_1=15$ cm; $d_2=8$ cm", "Xét $\\dfrac{|d_1-d_2|}{\\lambda}$: nguyên → cực đại; bán nguyên → cực tiểu"),
  ("\"$AB=12$ cm\"", "$AB=12$ cm", "Cực đại: $-\\dfrac{AB}{\\lambda}\\lt k\\lt\\dfrac{AB}{\\lambda}$"),
  ("\"bao nhiêu điểm cực đại, cực tiểu trên đoạn AB\"", "Cần $N_{max}$, $N_{min}$", "⚠ Không tính A, B (dấu $\\lt$, không phải $\\le$); cực tiểu thay $k$ bằng $k+\\tfrac12$")],
 [("\"hai khe cách nhau $a=0{,}50$ mm, màn cách $D=1{,}5$ m, $\\lambda=0{,}60\\ \\mu$m\"", "$a=0{,}50$ mm; $D=1{,}5$ m; $\\lambda=0{,}60\\ \\mu$m", "$i=\\dfrac{\\lambda D}{a}$"),
  ("\"tính khoảng vân $i$\"", "Cần $i$", "⚠ Đổi $\\lambda$, $a$, $D$ về cùng hệ đơn vị (m) trước khi tính"),
  ("\"trường giao thoa rộng $L=17$ mm, đối xứng qua vân trung tâm\"", "$L=17$ mm", "⚠ Công thức đếm chỉ đúng khi trường đối xứng qua vân trung tâm"),
  ("\"bao nhiêu vân sáng, bao nhiêu vân tối\"", "Cần $N_s$, $N_t$", "$N_s=2\\left[\\dfrac{L}{2i}\\right]+1$ · $N_t=2\\left[\\dfrac{L}{2i}+0{,}5\\right]$ ($[\\ ]$ là phần nguyên)"),
  ("\"điểm P cách vân trung tâm $6{,}3$ mm\"", "$x_P=6{,}3$ mm", "Xét $\\dfrac{x_P}{i}$: nguyên → vân sáng; bán nguyên → vân tối")],
 [("\"AB dài $L=0{,}60$ m, hai đầu cố định (coi là nút)\"", "$L=0{,}60$ m; hai nút ở A, B", "⚠ Hai đầu cố định: $L=n\\dfrac{\\lambda}{2}$ ($n$ bụng, $n+1$ nút)"),
  ("\"sóng dừng như hình vẽ\" (ba múi sóng)", "$n=3$ bụng", "Mỗi múi sóng dài $\\dfrac{\\lambda}{2}$, giữa hai nút liên tiếp có một bụng"),
  ("\"$f=150$ Hz\"", "$f=150$ Hz", "$v=\\lambda f$"),
  ("\"bao nhiêu nút (kể cả A và B)\"", "Cần số nút", "$n$ bụng → $n+1$ nút"),
  ("\"giữ nguyên dây và lực căng\"", "$v$ không đổi", "⚠ $v$ chỉ phụ thuộc dây và lực căng; đổi $f$ thì đổi $\\lambda$"),
  ("\"đổi tần số … để có 4 bụng\"", "Cần $f'$", "$\\lambda'=\\dfrac{2L}{4}$ rồi $f'=\\dfrac{v}{\\lambda'}$")],
 [("\"ống một đầu bịt kín, một đầu hở\"", "Đầu kín là nút, đầu hở là bụng", "⚠ $L=(2n+1)\\dfrac{\\lambda}{4}$ · $f_m=m f_1$ chỉ với $m$ lẻ · $f_1=\\dfrac{v}{4L}$"),
  ("\"hai tần số liên tiếp là $1020$ Hz và $1700$ Hz\"", "$f_a=1020$ Hz; $f_b=1700$ Hz (kề nhau)", "Hai tần số kề nhau ứng với hai $m$ lẻ kề nhau (hơn kém 2): hiệu bằng $2f_1$"),
  ("\"tốc độ truyền âm $340$ m/s\"", "$v=340$ m/s", "$f_1=\\dfrac{v}{4L}$ → $L=\\dfrac{v}{4f_1}$"),
  ("\"tìm tần số âm cơ bản; tìm chiều dài ống\"", "Cần $f_1$, $L$", "$f_b-f_a=2f_1$"),
  ("\"ở $1700$ Hz có mấy bụng (kể cả đầu hở)\"", "Cần số bụng", "$m=\\dfrac{f}{f_1}$; $m=2n+1$ → $n+1$ bụng, $n+1$ nút")],
]

# ───────────────────────── Lời giải ─────────────────────────
R1 = ["<strong>Khái niệm:</strong> bước sóng $\\lambda$ là khoảng cách hai đỉnh sóng liên tiếp (quãng sóng truyền trong một chu kì).",
      "<strong>Công thức:</strong> $T=\\dfrac{1}{f}$ · $v=\\dfrac{\\lambda}{T}=\\lambda f$",
      "⚠ <strong>Điều kiện:</strong> $n$ đỉnh liên tiếp có $n-1$ khoảng; $\\lambda$ và $v$ cùng hệ đơn vị."]
R2 = ["<strong>Khái niệm:</strong> hai điểm trên phương truyền sóng dao động cùng tần số; điểm xa nguồn hơn trễ pha hơn.",
      "<strong>Công thức:</strong> $\\lambda=\\dfrac{v}{f}$ · $\\Delta\\varphi=\\dfrac{2\\pi d}{\\lambda}$",
      "Cùng pha $\\Delta\\varphi=2k\\pi$ · ngược pha $(2k+1)\\pi$ · vuông pha $(2k+1)\\dfrac{\\pi}{2}$",
      "⚠ <strong>Điều kiện:</strong> $d$ đo dọc phương truyền sóng, cùng đơn vị với $\\lambda$."]
R3 = ["<strong>Khái niệm:</strong> hai nguồn kết hợp, cùng pha; $d_1$, $d_2$ là khoảng cách từ điểm đang xét tới nguồn 1 và 2.",
      "<strong>Công thức:</strong> $\\lambda=\\dfrac{v}{f}$ · cực đại $d_2-d_1=k\\lambda$ · cực tiểu $d_2-d_1=(k+\\tfrac12)\\lambda$",
      "Đếm trên AB: $-\\dfrac{AB}{\\lambda}\\lt k\\lt\\dfrac{AB}{\\lambda}$ (cực tiểu: thay $k$ bằng $k+\\tfrac12$).",
      "⚠ <strong>Điều kiện:</strong> hai nguồn cùng pha; không tính hai nguồn A, B nên dùng dấu $\\lt$."]
R4 = ["<strong>Khái niệm:</strong> khoảng vân $i$ là khoảng cách hai vân sáng (hoặc hai vân tối) liên tiếp.",
      "<strong>Công thức:</strong> $i=\\dfrac{\\lambda D}{a}$ · vân sáng $x=ki$ · vân tối $x=(k+\\tfrac12)i$",
      "Đếm trên trường $L$: $N_s=2\\left[\\dfrac{L}{2i}\\right]+1$ · $N_t=2\\left[\\dfrac{L}{2i}+0{,}5\\right]$",
      "⚠ <strong>Điều kiện:</strong> trường đối xứng qua vân trung tâm; $[\\ ]$ là phần nguyên (bỏ phần lẻ, không làm tròn)."]
R5 = ["<strong>Khái niệm:</strong> sóng dừng hai đầu cố định: hai đầu là nút, giữa hai nút liên tiếp có một bụng.",
      "<strong>Công thức:</strong> $L=n\\dfrac{\\lambda}{2}$ ($n$ bụng, $n+1$ nút) · $v=\\lambda f$",
      "⚠ <strong>Điều kiện:</strong> $v$ chỉ phụ thuộc dây và lực căng — đổi $f$ thì $v$ giữ nguyên, $\\lambda$ đổi."]
R6 = ["<strong>Khái niệm:</strong> ống một đầu kín, một đầu hở: đầu kín là nút, đầu hở là bụng.",
      "<strong>Công thức:</strong> $L=(2n+1)\\dfrac{\\lambda}{4}$ · $f_m=m f_1$ với $m$ lẻ · $f_1=\\dfrac{v}{4L}$",
      "Với $m=2n+1$ có $n+1$ bụng và $n+1$ nút (kể cả hai đầu).",
      "⚠ <strong>Điều kiện:</strong> chỉ có họa âm bậc lẻ; hai cộng hưởng liên tiếp hơn kém $2f_1$."]

SOLS = [
 sol(R1, [
  ("Bước sóng từ hình", [P("Đọc hình: đỉnh thứ nhất ở $x_1=3$ cm, đỉnh thứ tư ở $x_4=39$ cm."), P("Bốn đỉnh liên tiếp chỉ có 3 khoảng, mỗi khoảng là một bước sóng:"), M(r"x_4-x_1=3\lambda"), M(r"\lambda=\dfrac{39-3}{3}"), A(r"\lambda=12\ \text{cm}")]),
  ("Chu kì", [M(r"T=\dfrac{1}{f}=\dfrac{1}{4}"), A(r"T=0{,}25\ \text{s}")]),
  ("Tốc độ truyền sóng", [P("Đổi $\\lambda=12$ cm $=0{,}12$ m rồi nhân với $f$:"), M(r"v=\lambda f=0{,}12\cdot4"), A(r"v=0{,}48\ \text{m/s}")]),
  ("Kiểm tra", [P("Cách khác: $v=\\dfrac{\\lambda}{T}=\\dfrac{0{,}12}{0{,}25}=0{,}48$ m/s ✓."), P("Đơn vị: m · Hz = m/s ✓.")])],
  ["a) $\\lambda=12\\ \\text{cm}$", "b) $T=0{,}25\\ \\text{s}$", "c) $v=0{,}48\\ \\text{m/s}$"],
  "Nhận dạng: đề cho <strong>hình dạng sóng</strong> kèm tần số → đọc $\\lambda$ từ khoảng cách các đỉnh (nhớ $n$ đỉnh = $n-1$ khoảng), rồi $v=\\lambda f$."),
 sol(R2, [
  ("Bước sóng", [M(r"\lambda=\dfrac{v}{f}=\dfrac{4{,}0}{20}"), A(r"\lambda=0{,}20\ \text{m}")]),
  ("Độ lệch pha", [P("M, N cùng nằm trên phương truyền sóng, $d=0{,}45$ m:"), M(r"\Delta\varphi=\dfrac{2\pi d}{\lambda}=\dfrac{2\pi\cdot0{,}45}{0{,}20}"), A(r"\Delta\varphi=4{,}5\pi\ \text{rad}")]),
  ("Phân loại", [P("Bỏ hai chu kì đầy đủ ($4\\pi$):"), M(r"\Delta\varphi=4\pi+\dfrac{\pi}{2}"), A("T:M và N <strong>vuông pha</strong> (lệch nhau một phần tư chu kì)."), P("Cách nhanh: $d=2{,}25\\lambda=2\\lambda+\\dfrac{\\lambda}{4}$.")]),
  ("Kiểm tra", [P("Phần lẻ $0{,}25\\lambda$ ứng với $\\dfrac{\\pi}{2}$ ✓ ($\\lambda$ ứng với $2\\pi$)."), P("Đơn vị: $d$ và $\\lambda$ cùng m nên $\\dfrac{d}{\\lambda}$ không có đơn vị ✓.")])],
  ["a) $\\lambda=0{,}20\\ \\text{m}$", "b) $\\Delta\\varphi=4{,}5\\pi\\ \\text{rad}$", "c) M và N vuông pha"],
  "Nhận dạng: đề cho <strong>khoảng cách giữa hai điểm trên phương truyền</strong> → tính $\\dfrac{d}{\\lambda}$, bỏ phần nguyên chu kì, so phần dư với $\\dfrac{\\pi}{2}$, $\\pi$."),
 sol(R3, [
  ("Bước sóng", [P("Đổi $v=0{,}50$ m/s $=50$ cm/s:"), M(r"\lambda=\dfrac{v}{f}=\dfrac{50}{25}"), A(r"\lambda=2\ \text{cm}")]),
  ("Hiệu đường đi của M", [P("Hai nguồn cùng pha, xét hiệu đường đi chia $\\lambda$:"), M(r"\dfrac{|d_1-d_2|}{\lambda}=\dfrac{15-8}{2}"), A(r"\dfrac{|d_1-d_2|}{\lambda}=3{,}5")]),
  ("Loại điểm M", [P("$3{,}5=3+\\tfrac12$ là số bán nguyên:"), M(r"d_1-d_2=3{,}5\lambda=\left(3+\tfrac12\right)\lambda"), A("T:M nằm trên <strong>cực tiểu</strong> giao thoa.")]),
  ("Số cực đại trên AB", [M(r"\dfrac{AB}{\lambda}=\dfrac{12}{2}=6"), M(r"-6\lt k\lt6"), P("$k=-5,-4,\\dots,5$ (loại $\\pm6$ vì ứng với A và B):"), A(r"N_{max}=11")]),
  ("Số cực tiểu trên AB", [M(r"-6\lt k+\tfrac12\lt6\ \Rightarrow\ -6{,}5\lt k\lt5{,}5"), P("$k=-6,-5,\\dots,5$:"), A(r"N_{min}=12")]),
  ("Kiểm tra", [P("Cực đại và cực tiểu xen kẽ: 11 cực đại tạo 12 khoảng, mỗi khoảng chứa một cực tiểu ✓."), P("Đơn vị: $d_1$, $d_2$, $\\lambda$ cùng cm ✓.")])],
  ["a) $\\lambda=2\\ \\text{cm}$", "b) M thuộc cực tiểu", "c) 11 cực đại và 12 cực tiểu trên AB"],
  "Nhận dạng: đề hỏi <strong>cực đại, cực tiểu giữa hai nguồn</strong> → tính $\\dfrac{AB}{\\lambda}$, đếm $k$ nguyên (không tính A, B)."),
 sol(R4, [
  ("Khoảng vân", [P("Đổi về mét: $\\lambda=0{,}60\\cdot10^{-6}$ m, $a=0{,}50\\cdot10^{-3}$ m."), M(r"i=\dfrac{\lambda D}{a}=\dfrac{0{,}60\cdot10^{-6}\cdot1{,}5}{0{,}50\cdot10^{-3}}"), A(r"i=1{,}8\ \text{mm}")]),
  ("Số vân sáng", [M(r"\dfrac{L}{2i}=\dfrac{17}{2\cdot1{,}8}\approx4{,}72"), P("Lấy phần nguyên (bỏ phần lẻ): $[4{,}72]=4$."), M(r"N_s=2\cdot4+1"), A(r"N_s=9")]),
  ("Số vân tối", [M(r"\dfrac{L}{2i}+0{,}5\approx5{,}22\ \Rightarrow\ [5{,}22]=5"), M(r"N_t=2\cdot5"), A(r"N_t=10")]),
  ("Vị trí của P theo khoảng vân", [M(r"\dfrac{x_P}{i}=\dfrac{6{,}3}{1{,}8}"), A(r"\dfrac{x_P}{i}=3{,}5")]),
  ("Loại vân tại P", [P("$3{,}5=3+\\tfrac12$ là số bán nguyên:"), M(r"x_P=\left(3+\tfrac12\right)i"), A("T:P là <strong>vân tối</strong> (ứng với $k=3$).")]),
  ("Kiểm tra", [P("Vân sáng bậc 4 ở $7{,}2$ mm (trong $\\pm8{,}5$ mm), bậc 5 ở $9$ mm (ngoài) nên 9 vân sáng ✓."), P("Vân sáng lẻ vì có vân trung tâm, vân tối chẵn vì đối xứng ✓.")])],
  ["a) $i=1{,}8\\ \\text{mm}$", "b) $N_s=9$ · $N_t=10$", "c) P là vân tối"],
  "Nhận dạng: đề hỏi <strong>số vân trên trường giao thoa</strong> → tính $i$, rồi $\\dfrac{L}{2i}$ và lấy phần nguyên (không làm tròn)."),
 sol(R5, [
  ("Bước sóng", [P("Hình cho 3 bụng ($n=3$):"), M(r"L=n\dfrac{\lambda}{2}\ \Rightarrow\ \lambda=\dfrac{2L}{n}=\dfrac{2\cdot0{,}60}{3}"), A(r"\lambda=0{,}40\ \text{m}")]),
  ("Tốc độ truyền sóng", [M(r"v=\lambda f=0{,}40\cdot150"), A(r"v=60\ \text{m/s}")]),
  ("Số nút", [P("Hai đầu cũng là nút, $n$ bụng thì có $n+1$ nút:"), M(r"n+1=3+1"), A("T:Có <strong>4 nút</strong> (kể cả A và B).")]),
  ("Tần số cho 4 bụng", [P("$v$ không đổi, $n'=4$:"), M(r"\lambda'=\dfrac{2L}{n'}=\dfrac{2\cdot0{,}60}{4}=0{,}30\ \text{m}"), M(r"f'=\dfrac{v}{\lambda'}=\dfrac{60}{0{,}30}"), A(r"f'=200\ \text{Hz}")]),
  ("Kiểm tra", [P("$f_n=n\\,f_1$ với $f_1=\\dfrac{v}{2L}=50$ Hz: $3f_1=150$ Hz và $4f_1=200$ Hz ✓."), P("Thêm một bụng thì tần số tăng đúng $f_1=50$ Hz ✓.")])],
  ["a) $\\lambda=0{,}40\\ \\text{m}$ · $v=60\\ \\text{m/s}$", "b) 4 nút", "c) $f'=200\\ \\text{Hz}$"],
  "Nhận dạng: đề cho <strong>dây hai đầu cố định, có hình hoặc số bụng</strong> → $L=n\\dfrac{\\lambda}{2}$, $v=\\lambda f$, nút = bụng + 1."),
 sol(R6, [
  ("Âm cơ bản", [P("Hai tần số kề nhau ứng với hai họa âm lẻ liên tiếp, hơn kém $2f_1$:"), M(r"f_b-f_a=2f_1"), M(r"f_1=\dfrac{1700-1020}{2}"), A(r"f_1=340\ \text{Hz}")]),
  ("Chiều dài ống", [P("Ống một đầu kín: $f_1=\\dfrac{v}{4L}$."), M(r"L=\dfrac{v}{4f_1}=\dfrac{340}{4\cdot340}"), A(r"L=0{,}25\ \text{m}")]),
  ("Bậc của tần số $1700$ Hz", [M(r"m=\dfrac{f}{f_1}=\dfrac{1700}{340}"), A(r"m=5"), P("Số lẻ ✓ (ống một đầu kín chỉ có bậc lẻ).")]),
  ("Số bụng", [P("$m=2n+1=5$ nên $n=2$:"), M(r"n+1=2+1"), A("T:Có <strong>3 bụng</strong> (kể cả đầu hở) và 3 nút (kể cả đầu kín).")]),
  ("Kiểm tra", [P("$\\lambda=\\dfrac{v}{f}=\\dfrac{340}{1700}=0{,}20$ m; $L=5\\cdot\\dfrac{\\lambda}{4}=0{,}25$ m ✓."), P("$1020=3f_1$ và $1700=5f_1$ nên đúng là hai họa âm lẻ kề nhau ✓.")])],
  ["a) $f_1=340\\ \\text{Hz}$", "b) $L=0{,}25\\ \\text{m}$", "c) 3 bụng ($m=5$)"],
  "Nhận dạng: đề cho <strong>hai tần số cộng hưởng liên tiếp</strong> của ống hoặc dây → lấy hiệu để tìm $f_1$ (ống một đầu kín: hiệu $=2f_1$)."),
]

# ───────────────────────── Tự giải từng bước (9/10/2026) ─────────────────────────
STEPS = [
 dict(nhan_dang="Thấy <b>hình dạng sóng</b> kèm tần số → đọc $\\lambda$ từ các đỉnh ($n$ đỉnh = $n-1$ khoảng), rồi $v=\\lambda f$.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Bước sóng từ hình", "Bước sóng $\\lambda$ bằng bao nhiêu cm?", 12, "cm", 0.3,
       loi="Chia khoảng cách cho 4 (số đỉnh) ra $9$ cm; 4 đỉnh liên tiếp chỉ có 3 khoảng, mỗi khoảng là một $\\lambda$."),
  buoc("Chu kì", "Chu kì $T$ bằng bao nhiêu giây?", 0.25, "s", 0.005,
       loi="Lấy $T=f=4$ hoặc quên rằng chu kì là nghịch đảo của tần số: $T=\\dfrac{1}{f}$.",
       ke=[("$T=\\dfrac{1}{f}$", True),
           ("$T=f$", "Tần số là số dao động trong 1 s, chu kì là thời gian một dao động nên hai đại lượng nghịch đảo nhau."),
           ("$T=\\dfrac{\\lambda}{f}$", "Thương $\\dfrac{\\lambda}{f}$ có đơn vị m·s, không phải giây; $\\lambda$ không liên quan trực tiếp tới $T$.")]),
  buoc("Tốc độ truyền sóng", "Tốc độ truyền sóng $v$ bằng bao nhiêu m/s?", 0.48, "m/s", 0.01,
       loi="Nhân $12\\cdot4$ ra $48$ nhưng đó là cm/s; đề hỏi m/s nên phải đổi $\\lambda$ sang m trước.",
       ke=[("$v=\\lambda f$ với $\\lambda$ đổi sang m", True),
           ("$v=\\dfrac{\\lambda}{f}$", "Đơn vị m·s, không phải m/s; $v=\\dfrac{\\lambda}{T}=\\lambda f$."),
           ("$v=A\\cdot f$ với $A$ là biên độ đọc trên trục $u$", "Biên độ là độ lệch lớn nhất theo phương vuông góc dây, không phải quãng sóng truyền trong một chu kì; phải dùng $\\lambda$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Đề cho <b>khoảng cách giữa hai điểm trên phương truyền</b> → tính $\\dfrac{d}{\\lambda}$, bỏ phần chu kì đầy đủ, so phần dư với $\\dfrac{\\pi}{2}$, $\\pi$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Bước sóng", "Bước sóng $\\lambda$ bằng bao nhiêu mét?", 0.2, "m", 0.005,
       loi="Nhân thay vì chia ($\\lambda=vf=80$ m) hoặc lấy $\\lambda=\\dfrac{f}{v}$; bước sóng là quãng đường sóng đi trong một chu kì nên $\\lambda=\\dfrac{v}{f}$."),
  buoc("Độ lệch pha", "Độ lệch pha $\\Delta\\varphi$ bằng bao nhiêu lần $\\pi$ (rad)?", 4.5, "π rad", 0.05,
       loi="Quên nhân 2 (dùng $\\dfrac{\\pi d}{\\lambda}$) ra một nửa giá trị đúng; hoặc đảo $\\dfrac{\\lambda}{d}$ — quãng đường dài hơn thì trễ pha nhiều hơn.",
       ke=[("$\\Delta\\varphi=\\dfrac{2\\pi d}{\\lambda}$", True),
           ("$\\Delta\\varphi=\\dfrac{2\\pi\\lambda}{d}$", "Tỉ số bị đảo: $d$ càng lớn thì độ trễ pha càng lớn, nên $d$ phải ở tử số."),
           ("$\\Delta\\varphi=\\dfrac{d}{\\lambda}$ (rad)", "Tỉ số $\\dfrac{d}{\\lambda}$ chỉ là số bước sóng; một bước sóng ứng với $2\\pi$ rad, phải nhân $2\\pi$.")]),
  buoc("Phân loại", "M, N dao động thế nào?", loi="Thấy $\\Delta\\varphi$ vượt $\\pi$ thì kết luận ngược pha, hoặc bỏ cả phần lẻ rồi kết luận cùng pha; phải bỏ bội của $2\\pi$ rồi so phần dư.",
       lua_chon=[("Vuông pha", True),
                 ("Ngược pha, vì $\\Delta\\varphi$ lớn hơn $\\pi$", "Ngược pha là hơn kém $\\pi$ cộng bội của $2\\pi$, không phải lớn hơn $\\pi$."),
                 ("Cùng pha, vì $d$ lớn hơn $2\\lambda$", "Cùng pha cần $d$ đúng bằng số nguyên lần $\\lambda$; ở đây còn dư một phần $\\lambda$.")],
       ke=[("Bỏ các bội của $2\\pi$, so phần dư với $\\pi$, $\\dfrac{\\pi}{2}$", True),
           ("So thẳng $\\Delta\\varphi$ với $\\pi$: lớn hơn $\\pi$ là ngược pha", "Hơn kém $\\pi$ cộng bội $2\\pi$ mới là ngược pha; phải bỏ bội $2\\pi$ trước."),
           ("Chỉ xét $d$ có nguyên $\\lambda$ hay không", "Phần lẻ của $\\dfrac{d}{\\lambda}$ mới cho biết loại pha; số nguyên lần $\\lambda$ chỉ bỏ đi.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Đề hỏi <b>cực đại, cực tiểu</b> giữa hai nguồn cùng pha → tính $\\dfrac{AB}{\\lambda}$, đếm $k$ nguyên, không tính A, B.",
  cap_do=3, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Bước sóng", "Bước sóng $\\lambda$ bằng bao nhiêu cm?", 2, "cm", 0.05,
       loi="Không đổi $v=0{,}50$ m/s sang cm/s nên chia ra $0{,}02$; $\\lambda$ phải cùng đơn vị với $AB$ và $d$."),
  buoc("Hiệu đường đi của M", "$\\dfrac{|d_1-d_2|}{\\lambda}$ bằng bao nhiêu?", 3.5, None, 0.05,
       loi="Lấy tổng $d_1+d_2$ thay vì hiệu, hoặc chia $d_1$ cho $\\lambda$ riêng.",
       ke=[("Lấy $|d_1-d_2|$ rồi chia cho $\\lambda$", True),
           ("Lấy $d_1+d_2$ rồi chia cho $\\lambda$", "Điều kiện giao thoa dựa trên hiệu đường đi, không phải tổng."),
           ("Chia riêng $\\dfrac{d_1}{\\lambda}$ và $\\dfrac{d_2}{\\lambda}$ rồi xét từng số", "Chỉ hiệu hai quãng đường quyết định hai sóng gặp nhau cùng pha hay ngược pha.")]),
  buoc("Loại điểm M", "M thuộc loại điểm nào?", loi="Thấy hiệu đường đi lớn nên kết luận cực đại; cực đại cần hiệu đường là số nguyên lần $\\lambda$, số bán nguyên là cực tiểu.",
       lua_chon=[("Cực tiểu (hiệu đường đi là số bán nguyên lần $\\lambda$)", True),
                 ("Cực đại, vì hiệu đường đi lớn", "Cực đại cần hiệu đường là số nguyên lần $\\lambda$, không phải số lớn."),
                 ("Điểm có biên độ trung gian, không đặc biệt", "Số bán nguyên lần $\\lambda$ chính là điều kiện cực tiểu nên M đặc biệt.")],
       ke=[("Xét số nguyên hay bán nguyên (hai nguồn cùng pha)", True),
           ("Xét số nguyên hay bán nguyên (hai nguồn ngược pha)", "Đề cho hai nguồn cùng pha; điều kiện ngược pha sẽ đổi chỗ cực đại và cực tiểu."),
           ("So $|d_1-d_2|$ với $AB$", "So với $AB$ chỉ cho biết M có tồn tại hay không, không cho biết M là cực đại hay cực tiểu.")]),
  buoc("Số cực đại trên AB", "Số điểm cực đại trên đoạn AB là bao nhiêu?", 11, None, 0,
       loi="Đếm cả hai nguồn ($k=\\pm6$) ra 13, hoặc lấy $\\dfrac{AB}{\\lambda}=6$ làm số cực đại; $k$ chạy cả hai phía của $k=0$.",
       ke=[("Đếm $k$ nguyên thoả $-\\dfrac{AB}{\\lambda}\\lt k\\lt\\dfrac{AB}{\\lambda}$", True),
           ("Đếm $k$ nguyên thoả $-\\dfrac{AB}{\\lambda}\\le k\\le\\dfrac{AB}{\\lambda}$", "A và B là nguồn, không phải điểm cực đại; $k=\\pm\\dfrac{AB}{\\lambda}$ rơi đúng tại hai nguồn nên phải loại."),
           ("Lấy $N=\\dfrac{AB}{\\lambda}$", "Số $k$ nguyên phải đếm cả $k$ âm, $k=0$ và $k$ dương, không bằng $\\dfrac{AB}{\\lambda}$.")]),
  buoc("Số cực tiểu trên AB", "Số điểm cực tiểu trên đoạn AB là bao nhiêu?", 12, None, 0,
       loi="Đếm sai số cực tiểu vì nhầm với số cực đại; cực tiểu ứng với $k+\\tfrac{1}{2}$, không phải $k$ nguyên.",
       ke=[("Đếm $k$ nguyên thoả $-\\dfrac{AB}{\\lambda}\\lt k+\\tfrac{1}{2}\\lt\\dfrac{AB}{\\lambda}$", True),
           ("Lấy số cực tiểu bằng số cực đại", "Cực đại và cực tiểu xen kẽ: giữa hai cực đại liên tiếp có một cực tiểu, lại còn cực tiểu ở hai phía ngoài cùng, nên hai số không bằng nhau."),
           ("Lấy số cực đại trừ 1", "Cực tiểu ứng với $k+\\tfrac{1}{2}$, phải đếm riêng theo điều kiện này chứ không suy từ số cực đại.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Đề hỏi <b>số vân sáng, vân tối trên trường giao thoa</b> → tính $i$, rồi $\\dfrac{L}{2i}$ và lấy phần nguyên, không làm tròn.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Khoảng vân", "Khoảng vân $i$ bằng bao nhiêu mm?", 1.8, "mm", 0.02,
       loi="Không đổi $\\mu$m và mm về mét nên ra $i$ lệch 10 hoặc 1000 lần; hoặc đảo $\\dfrac{a}{\\lambda D}$."),
  buoc("Số vân sáng", "Số vân sáng trên trường giao thoa là bao nhiêu?", 9, None, 0,
       loi="Làm tròn $4{,}72$ lên 5 ra 11 vân sáng, hoặc quên vân trung tâm ($2\\cdot4=8$); vân sáng luôn lẻ.",
       ke=[("Lấy phần nguyên của $\\dfrac{L}{2i}$ rồi $N_s=2[\\,\\cdot\\,]+1$", True),
           ("Làm tròn $\\dfrac{L}{2i}$ lên rồi $N_s=2[\\,\\cdot\\,]+1$", "Phải bỏ phần lẻ: vân bậc 5 nằm ở $9$ mm, ngoài mép $\\pm8{,}5$ mm nên không đếm."),
           ("$N_s=2[\\,\\dfrac{L}{2i}\\,]$", "Quên vân sáng trung tâm: trường đối xứng nên số vân sáng luôn lẻ.")]),
  buoc("Số vân tối", "Số vân tối trên trường giao thoa là bao nhiêu?", 10, None, 0,
       loi="Lấy $N_t=N_s$ hoặc $N_s-1$; vân tối nằm giữa hai vân sáng và trường đối xứng nên số vân tối luôn chẵn.",
       ke=[("$N_t=2\\left[\\dfrac{L}{2i}+0{,}5\\right]$", True),
           ("$N_t=N_s$", "Trường đối xứng qua vân trung tâm (là vân sáng) nên vân tối luôn thành cặp: số chẵn."),
           ("$N_t=N_s-1$", "Số vân tối phải tính riêng bằng phần nguyên của $\\dfrac{L}{2i}+0{,}5$; ở đây còn nhiều hơn số vân sáng.")]),
  buoc("Vân tại P", "$\\dfrac{x_P}{i}$ bằng bao nhiêu?", 3.5, None, 0.05,
       loi="Chia $x_P$ cho $\\lambda$ hoặc cho $L$; vân sáng/tối xét theo tỉ số với khoảng vân $i$.",
       ke=[("Lấy $\\dfrac{x_P}{i}$: nguyên → sáng, bán nguyên → tối", True),
           ("Lấy $\\dfrac{x_P}{\\lambda}$", "Vị trí vân tính theo khoảng vân $i$, không theo bước sóng."),
           ("So $x_P$ với $\\dfrac{L}{2}$", "Chỉ cho biết P có nằm trong trường hay không, không cho biết sáng hay tối.")]),
  buoc("Loại vân tại P", "P là vân gì?", loi="Thấy $3{,}5$ gần 4 nên chọn vân sáng bậc 4; số bán nguyên mới là vân tối.",
       lua_chon=[("Vân tối ($k=3$)", True),
                 ("Vân sáng bậc 4", "Vân sáng cần $\\dfrac{x}{i}$ nguyên; $3{,}5$ không nguyên."),
                 ("Vân sáng bậc 3", "Vân sáng cần $\\dfrac{x}{i}$ nguyên; $3{,}5$ không nguyên.")],
       ke=[("So $\\dfrac{x_P}{i}$ với số nguyên hay bán nguyên", True),
           ("So $x_P$ với $\\lambda$", "Khoảng vân $i$ mới là đơn vị đo vị trí vân."),
           ("Làm tròn $\\dfrac{x_P}{i}$ rồi kết luận vân sáng", "Làm tròn làm mất phần $\\tfrac12$ quyết định vân tối.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Đề cho <b>dây hai đầu cố định có hình hoặc số bụng</b> → $L=n\\dfrac{\\lambda}{2}$, $v=\\lambda f$, số nút $=n+1$.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Bước sóng", "Bước sóng $\\lambda$ bằng bao nhiêu mét?", 0.4, "m", 0.01,
       loi="Dùng $L=n\\lambda$ (thiếu $\\dfrac{1}{2}$) ra $0{,}20$ m; mỗi múi sóng chỉ dài $\\dfrac{\\lambda}{2}$."),
  buoc("Tốc độ truyền sóng", "Tốc độ truyền sóng $v$ bằng bao nhiêu m/s?", 60, "m/s", 1,
       loi="Tính $v=\\dfrac{\\lambda}{f}$ hoặc lấy $v=2Lf$ (đúng chỉ khi dây rung ở âm cơ bản $n=1$).",
       ke=[("$v=\\lambda f$ với $\\lambda$ vừa tìm", True),
           ("$v=2Lf$", "Công thức này chỉ đúng với một múi sóng ($n=1$); dây đang có 3 múi."),
           ("$v=\\dfrac{\\lambda}{f}$", "Thương này có đơn vị m·s, không phải m/s.")]),
  buoc("Số nút", "Trên dây có bao nhiêu nút, kể cả A và B?", 4, None, 0,
       loi="Đếm 3 nút bằng số bụng, hoặc chỉ đếm nút giữa dây (2 nút) quên hai đầu; hai đầu cố định cũng là nút.",
       ke=[("Số nút $=n+1$ vì hai đầu cũng là nút", True),
           ("Số nút bằng số bụng", "Giữa hai nút liên tiếp có một bụng nên nút nhiều hơn bụng 1 khi hai đầu đều là nút."),
           ("Số nút $=n-1$ (chỉ nút giữa dây)", "Câu hỏi tính cả A và B, hai đầu cố định là nút.")]),
  buoc("Tần số cho 4 bụng", "Tần số $f'$ để dây có 4 bụng bằng bao nhiêu Hz?", 200, "Hz", 2,
       loi="Giữ $\\lambda$ cũ hoặc đổi cả $v$; lực căng không đổi thì $v$ không đổi, chỉ $\\lambda$ đổi theo số bụng.",
       ke=[("Giữ $v$, tính $\\lambda'=\\dfrac{2L}{4}$ rồi $f'=\\dfrac{v}{\\lambda'}$", True),
           ("Giữ $\\lambda$ cũ, tính $f'=\\dfrac{v}{\\lambda}\\cdot4$", "Thêm bụng thì $\\lambda$ phải thu nhỏ; không giữ nguyên $\\lambda$."),
           ("Giữ $f$ cũ, đổi $v$ để có 4 bụng", "Đề giữ nguyên dây và lực căng nên $v$ không đổi, chỉ tần số đổi được.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Đề cho <b>hai tần số cộng hưởng liên tiếp</b> của ống một đầu kín → hiệu $=2f_1$; $f_m=mf_1$ với $m$ lẻ.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Âm cơ bản", "Tần số âm cơ bản $f_1$ bằng bao nhiêu Hz?", 340, "Hz", 3,
       loi="Lấy hiệu hai tần số bằng $f_1$ như dây hai đầu cố định; ống một đầu kín chỉ có bậc lẻ nên hai cộng hưởng kề nhau hơn kém $2f_1$."),
  buoc("Chiều dài ống", "Chiều dài ống $L$ bằng bao nhiêu mét?", 0.25, "m", 0.005,
       loi="Dùng $f_1=\\dfrac{v}{2L}$ của dây hai đầu cố định ra gấp đôi; ống một đầu kín có $L=\\dfrac{\\lambda}{4}$ ở âm cơ bản.",
       ke=[("$L=\\dfrac{v}{4f_1}$ vì ở âm cơ bản $L=\\dfrac{\\lambda}{4}$", True),
           ("$L=\\dfrac{v}{2f_1}$", "Công thức đó dành cho dây hai đầu cố định (hoặc ống hai đầu hở), $L=\\dfrac{\\lambda}{2}$."),
           ("$L=\\dfrac{v}{f_1}$", "Ống không dài bằng cả một bước sóng ở âm cơ bản; chỉ bằng một phần tư.")]),
  buoc("Bậc của tần số $1700$ Hz", "Tần số $1700$ Hz là họa âm bậc $m$ bằng bao nhiêu?", 5, None, 0,
       loi="Chia cho $2f_1$ ra $2{,}5$ (không nguyên), hoặc nghĩ họa âm bậc chẵn; ống một đầu kín chỉ có bậc lẻ.",
       ke=[("$m=\\dfrac{f}{f_1}$, phải ra số lẻ", True),
           ("$m=\\dfrac{f}{2f_1}$", "Ra số bán nguyên, không phải bậc lẻ; $f_m=m\\,f_1$ nên chia cho $f_1$."),
           ("$m=2n$ vì ống có $n$ bụng", "Đầu kín là nút, đầu hở là bụng nên chỉ có $m=2n+1$ lẻ.")]),
  buoc("Số bụng", "Trong ống có mấy bụng sóng, kể cả đầu hở?", 3, None, 0,
       loi="Lấy số bụng bằng $m$ (ra 5) hoặc $\\dfrac{m}{2}$; với $m=2n+1$ có $n+1$ bụng.",
       ke=[("$m=2n+1$ thì có $n+1$ bụng", True),
           ("Số bụng bằng $m$", "Mỗi bụng ứng với nửa bước sóng, còn $m$ đếm số phần tư bước sóng; hai khái niệm khác nhau."),
           ("Số bụng bằng $\\dfrac{m}{2}$ làm tròn xuống", "Đầu hở là bụng và không được bỏ; phải dùng $n+1$ với $m=2n+1$.")]),
  buoc("Kiểm tra")]),
]


# ───────────────────────── Tự luận: ví dụ cũ còn đúng, chưa biên tập thành dạng ─────────────────────────
def old_pairs(i):
    parts = re.split(r'<p class="text-base leading-relaxed my-2"><strong class="font-bold">Đề:</strong>', OLD[i]["body_html"])[1:]
    out = []
    for p_ in parts:
        de, loi = p_.split('<p class="text-base leading-relaxed my-2"><strong class="font-bold">Lời giải:</strong>')
        de = re.sub(r"^\s*Ví dụ \d+\.\s*", "", de.strip().removesuffix("</p>").strip())
        loi = loi.strip().removesuffix("</p>").strip()
        out.append((de, loi))
    return out


def lt(h):
    """Trong $…$ mọi `<`/`>` viết \\lt/\\gt (kể cả `<k`, vì trình duyệt coi `<k` là thẻ HTML → mất cả đoạn)."""
    return re.sub(r"\$[^$]*\$", lambda m: m.group(0).replace("<", "\\lt ").replace(">", "\\gt "), h)


# (dạng cũ, ví dụ) xếp dễ → khó. Bỏ: D1 ví dụ 1 (dao động, không phải sóng), D3 ví dụ 1 (đáp số cũ 3,4 m/s sai, tính lại 3,2 m/s),
# D14 ví dụ 1 (âm cơ bản 12 Hz hạ âm) và ví dụ 4 (LaTeX hỏng, đề mơ hồ). D1 ví dụ 3, D3 ví dụ 2... đã có dạng mới tương ứng.
TL = [("Dễ", 4, 0), ("Dễ", 4, 1), ("Dễ", 3, 0), ("Dễ", 3, 1), ("Dễ", 5, 0), ("Dễ", 5, 1), ("Dễ", 1, 0), ("Dễ", 1, 1),
      ("Dễ", 0, 2), ("Dễ", 8, 0), ("Dễ", 8, 1), ("Dễ", 8, 2), ("Trung bình", 2, 1), ("Trung bình", 7, 0), ("Trung bình", 7, 1),
      ("Trung bình", 12, 0), ("Trung bình", 13, 1), ("Trung bình", 13, 2), ("Trung bình", 14, 0), ("Trung bình", 14, 1),
      ("Khó", 12, 1), ("Khó", 9, 0), ("Khó", 9, 1), ("Khó", 10, 0), ("Khó", 10, 1), ("Khó", 6, 0), ("Khó", 6, 1), ("Khó", 11, 0), ("Khó", 11, 1)]


def tu_luan_33():
    parts = []
    for k, (muc, i, j) in enumerate(TL, 1):
        de, loi = old_pairs(i)[j]
        parts.append(f"<h4>Bài {k} · {muc}</h4><p>{lt(de)}</p><details><summary>Hướng dẫn giải</summary><p>{lt(loi)}</p></details>")
    return dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
                body_html="<p>Các bài còn lại của bài học, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>" + "".join(parts))


d = {"lesson_id": 33, "lesson_title": "Bài 14. Bài tập về sóng", "generated_at": "2026-10-09",
     "review": {"checked": False, "notes": "chờ kiểm chéo"},
     "dang_bai": [dict(form="bai_tap", solution_html="", **x) for x in DANG],
     "tu_luan": tu_luan_33()}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
