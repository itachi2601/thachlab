#!/usr/bin/env python3
"""CĐ06 (bài 151) — tính mọi số liệu dùng trong nguon.md. Chạy: python3 tinh.py
Quy ước: góc đo so với PHÁP TUYẾN; n_kk = 1; n_nước = 4/3; thuỷ tinh 1,5; c = 3e8 m/s.
"""
from math import sin, cos, tan, asin, atan, sqrt, radians as rad, degrees as deg

C = 3e8
NW = 4 / 3


def asind(x):
    return deg(asin(x))


def sind(a):
    return sin(rad(a))


def cosd(a):
    return cos(rad(a))


def tand(a):
    return tan(rad(a))


def p(label, val, fmt="{:.4f}"):
    print(f"  {label:<46} = {fmt.format(val)}")


def igh(n1, n2=1.0):
    return asind(n2 / n1)


# ---------------- Lý thuyết (số minh hoạ) ----------------
print("== Lý thuyết: bảng góc giới hạn / vận tốc")
for name, n in [("nước 4/3", NW), ("thuỷ tinh 1,5", 1.5), ("kim cương 2,42", 2.42)]:
    p(f"igh {name} -> kk (deg)", igh(n), "{:.1f}")
    p(f"v trong {name} (1e8 m/s)", C / n / 1e8, "{:.3f}")
p("igh thuỷ tinh 1,5 -> nước (deg)", igh(1.5, NW), "{:.1f}")
p("Mở bài: kk->nước i=50 => r (deg)", asind(sind(50) / NW), "{:.1f}")

# ---------------- D1 ----------------
print("== D1  Định luật khúc xạ, chiết suất, vận tốc")
i, r = 60, 36
n = sind(i) / sind(r)
p("sin60", sind(60)); p("sin36", sind(36))
p("n chất lỏng", n)
p("v (1e8 m/s)", C / n / 1e8, "{:.3f}")
r_b = asind(n * sind(30))
p("b) lỏng->kk i=30: sin r", n * sind(30)); p("b) r (deg)", r_b, "{:.1f}")
p("c) góc tia phản xạ - tia khúc xạ (i=60,r=36)", 180 - 60 - 36, "{:.0f}")
iB = deg(atan(n))
p("d) i để phản xạ ⊥ khúc xạ: tan i = n => i", iB, "{:.1f}")
p("d) r tương ứng = 90 - i", 90 - iB, "{:.1f}")
p("d) kiểm: sin i / sin r", sind(iB) / sind(90 - iB))

# ---------------- D2 ----------------
print("== D2  Độ sâu biểu kiến nhiều lớp (dầu 1,4 dày 14 cm trên nước 80 cm)")
nd, ed, ew = 1.4, 14, 80
p("a) h' đáy (cm)", ed / nd + ew / NW, "{:.2f}")
p("a) nâng lên (cm)", ed + ew - (ed / nd + ew / NW), "{:.2f}")
p("b) cá sâu 40 cm dưới mặt dầu-nước: h' (cm)", ed / nd + 40 / NW, "{:.2f}")
H = 150
dist = NW * (40 / NW + ed / nd + H / 1)
p("c) cá thấy đèn (cao 150 cm trên mặt dầu) cách cá (cm)", dist, "{:.1f}")
p("c) khoảng cách thật cá-đèn (cm)", 40 + ed + H, "{:.0f}")
p("c) đèn trông cao hơn mặt dầu (cm)", dist - 40 - ed, "{:.1f}")

# ---------------- D3 ----------------
print("== D3  Vùng sáng tròn, đĩa chắn")
g = igh(NW)
p("igh nước (deg)", g, "{:.2f}"); p("tan igh (=3/sqrt7)", tand(g)); p("3/sqrt(7)", 3 / sqrt(7))
p("a) h=0,9 m: R (m)", 0.9 * tand(g), "{:.3f}")
g16 = igh(1.6)
p("b) n=1,6: igh (deg)", g16, "{:.2f}"); p("b) tan igh", tand(g16))
p("b) R (m)", 0.9 * tand(g16), "{:.3f}")
p("c) đĩa r=0,5 m: h_max (m)", 0.5 / tand(g), "{:.3f}")
p("c) diện tích vùng sáng a) (m^2)", 3.141592653589793 * (0.9 * tand(g)) ** 2, "{:.2f}")

# ---------------- D4 ----------------
print("== D4  Bản mặt song song e=6 cm, n=1,5, i=60")
e, n, i = 6, 1.5, 60
r = asind(sind(i) / n)
p("sin r", sind(i) / n); p("r (deg)", r, "{:.2f}")
d = e * sind(i - r) / cosd(r)
p("độ dời ngang d (cm)", d, "{:.2f}")
p("đường đi trong kính IJ = e/cos r (cm)", e / cosd(r), "{:.2f}")
p("b) nhìn vuông góc: vật dịch lại gần e(1-1/n) (cm)", e * (1 - 1 / n), "{:.2f}")
for ii in (30, 45, 75):
    rr = asind(sind(ii) / n)
    p(f"   bảng: i={ii} -> d (cm)", e * sind(ii - rr) / cosd(rr), "{:.2f}")

# ---------------- D5 ----------------
print("== D5  Lăng kính A=30, tia vuông góc mặt AB; tán sắc")
A = 30
for name, n in [("đỏ 1,50", 1.50), ("tím 1,54", 1.54)]:
    r2 = asind(n * sind(A))
    D = r2 - A
    p(f"{name}: sin r2", n * sind(A)); p(f"{name}: r2 (deg)", r2, "{:.2f}"); p(f"{name}: D (deg)", D, "{:.2f}")
    p(f"{name}: tan D", tand(D))
Dd = asind(1.5 * sind(A)) - A
Dt = asind(1.54 * sind(A)) - A
p("góc giữa tia đỏ và tím (deg)", Dt - Dd, "{:.2f}")
L = 1.2
p("vệt màu trên màn ⊥ tia tới, cách 1,2 m (cm)", 100 * L * (tand(Dt) - tand(Dd)), "{:.1f}")
p("d) igh đỏ (deg)", igh(1.50), "{:.2f}"); p("d) igh tím (deg)", igh(1.54), "{:.2f}")
p("d) A=41: đỏ sin r2", 1.5 * sind(41)); p("d) A=41: đỏ r2", asind(1.5 * sind(41)), "{:.1f}")
p("d) A=41: tím n sinA (>1 => PXTP)", 1.54 * sind(41))

# ---------------- D6 ----------------
print("== D6  Lăng kính phản xạ toàn phần vuông cân, tia ⊥ mặt huyền")
p("n_min trong kk = sqrt2", sqrt(2))
p("n_min trong nước = (4/3)sqrt2", NW * sqrt(2))
p("thuỷ tinh 1,5 trong nước: igh (deg)", igh(1.5, NW), "{:.2f}")
s = 1.5 * sind(45) / NW
p("trong nước: sin r ló ở mặt bên", s); p("r ló (deg)", asind(s), "{:.1f}")
p("độ lệch của tia ló so với phương tới (deg) = r-45", asind(s) - 45, "{:.1f}")

# ---------------- D7 ----------------
print("== D7  Sợi quang lõi 1,60 / vỏ 1,50, dài 1 km")
n1, n2 = 1.60, 1.50
g = igh(n1, n2)
p("igh lõi-vỏ (deg)", g, "{:.2f}"); p("sin igh", n2 / n1)
r0 = 90 - g
p("r_max ở đầu sợi (deg)", r0, "{:.2f}")
sm = n1 * sind(r0)
p("sin i_max = n1 sin r_max", sm); p("sqrt(n1^2-n2^2)", sqrt(n1 ** 2 - n2 ** 2))
p("i_max (deg)", asind(sm), "{:.1f}")
Lf = 1000
t0 = Lf * n1 / C
t1 = Lf / (n2 / n1) * n1 / C
p("t tia dọc trục (µs)", t0 * 1e6, "{:.3f}"); p("t tia xiên nhất (µs)", t1 * 1e6, "{:.3f}")
p("chênh (ns)", (t1 - t0) * 1e9, "{:.0f}")
p("b') nếu đầu sợi đặt trong nước: sin i_max", sm / NW); p("i_max nước (deg)", asind(sm / NW), "{:.1f}")

# ---------------- Tự luận ----------------
print("== Tự luận")
p("TL1 cốc sâu 12 cm: h' (cm)", 12 / NW, "{:.1f}")
p("TL3 nước 3 m: t (ns)", 3 * NW / C * 1e9, "{:.1f}"); p("TL3 không khí 3 m: t (ns)", 3 / C * 1e9, "{:.1f}")
p("TL3 quãng đường kk tương đương (m)", 3 * NW, "{:.1f}")
# TL4 cá sâu 0,6 m, tia ló r với sin r = 0,8
si = 0.8 / NW
ii = asind(si); rr = asind(0.8)
dd = 0.6 * tand(ii)
p("TL4 sin i trong nước", si); p("TL4 i (deg)", ii, "{:.2f}"); p("TL4 r (deg)", rr, "{:.2f}")
p("TL4 d = 0,6 tan i (m)", dd, "{:.3f}"); p("TL4 h' = d/tan r (m)", dd / tand(rr), "{:.4f}")
p("TL4 so sánh h/n (m)", 0.6 / NW, "{:.3f}")
# TL5 bóng cọc: bể sâu 80 cm, cọc 1,2 m thẳng đứng chạm đáy, nắng i=60
above = 1.2 - 0.8
r5 = asind(sind(60) / NW)
p("TL5 r (deg)", r5, "{:.2f}")
p("TL5 bóng trên mặt nước (m)", above * tand(60), "{:.3f}")
p("TL5 thêm trong nước (m)", 0.8 * tand(r5), "{:.3f}")
p("TL5 bóng trên đáy (m)", above * tand(60) + 0.8 * tand(r5), "{:.3f}")
p("TL5 nếu bể cạn (m)", 1.2 * tand(60), "{:.3f}")
# TL6 bản mặt e=4 cm, n=1,6, i=45
r6 = asind(sind(45) / 1.6)
p("TL6 r (deg)", r6, "{:.2f}"); p("TL6 d (cm)", 4 * sind(45 - r6) / cosd(r6), "{:.2f}")
p("TL6 nhìn ⊥: dịch (cm)", 4 * (1 - 1 / 1.6), "{:.2f}")
# TL7 khối lập phương: n >= sqrt2
p("TL7 n_min", sqrt(2))
for n in (1.3, 1.5):
    rmax = asind(1 / n)
    p(f"TL7 n={n}: r_max (deg)", rmax, "{:.2f}"); p(f"TL7 n={n}: góc tới mặt bên min (deg)", 90 - rmax, "{:.2f}")
    p(f"TL7 n={n}: igh (deg)", igh(n), "{:.2f}")
# TL8 lăng kính tam giác đều n=1,5, tia ⊥ AB: theo dõi bằng vector
import math
def refl(v, nrm):
    k = v[0] * nrm[0] + v[1] * nrm[1]
    return (v[0] - 2 * k * nrm[0], v[1] - 2 * k * nrm[1])
Apt, Bpt, Cpt = (0, 0), (1, 0), (0.5, sqrt(3) / 2)   # AB nằm ngang
v = (0, 1)  # đi vào qua AB, vuông góc AB
# mặt AC: pháp tuyến đơn vị hướng ra ngoài
ac = (Cpt[0] - Apt[0], Cpt[1] - Apt[1]); nac = (-ac[1], ac[0]); L_ = math.hypot(*nac); nac = (nac[0] / L_, nac[1] / L_)
inc_ac = deg(math.acos(v[0] * nac[0] + v[1] * nac[1]))
p("TL8 góc tới ở AC (deg)", inc_ac, "{:.1f}")
v2 = refl(v, nac)
bc = (Cpt[0] - Bpt[0], Cpt[1] - Bpt[1]); nbc = (bc[1], -bc[0]); L_ = math.hypot(*nbc); nbc = (nbc[0] / L_, nbc[1] / L_)
inc_bc = deg(math.acos(max(-1, min(1, v2[0] * nbc[0] + v2[1] * nbc[1]))))
p("TL8 góc tới ở BC sau phản xạ (deg)", inc_bc, "{:.1f}")
dev = deg(math.acos(v[0] * v2[0] + v[1] * v2[1]))
p("TL8 góc giữa tia ló và tia tới (deg)", dev, "{:.1f}")
p("TL8 điều kiện PXTP ở AC: n >= 1/sin60", 1 / sind(60))

# ---------------- Luyện tập ----------------
print("== Luyện tập")
p("I.1 n=1,25: v (1e8)", C / 1.25 / 1e8, "{:.2f}")
p("I.2 n=1,25: igh (deg)", igh(1.25), "{:.1f}")
p("I.4 A=40,n=1,5 ⊥AB: sin r2", 1.5 * sind(40)); p("I.4 r2", asind(1.5 * sind(40)), "{:.1f}")
p("I.4 D", asind(1.5 * sind(40)) - 40, "{:.1f}")
p("I.4 nhiễu: igh 1,5", igh(1.5), "{:.1f}")
p("II.1 kim cương igh", igh(2.42), "{:.1f}")
p("II.2 bản kính 3 cm n 1,5 dịch (cm)", 3 * (1 - 1 / 1.5), "{:.1f}")
p("II.2 hồ 2 m: h' (m)", 2 / NW, "{:.2f}")
p("III.1 hồ 1,8 m: h' (m)", 1.8 / NW, "{:.2f}")
p("III.2 nguồn sâu 0,6 m: R (m)", 0.6 * tand(igh(NW)), "{:.3f}")
