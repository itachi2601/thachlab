#!/usr/bin/env python3
"""CĐ07 Thấu kính mỏng & kính lúp (bài 156) — tính mọi số liệu dùng trong nguon.md.
Quy ước: d > 0 (vật thật); d' > 0 ảnh thật, d' < 0 ảnh ảo; f > 0 hội tụ, f < 0 phân kì.
Công thức: 1/f = 1/d + 1/d';  |h'|/h = |d'|/d;  d' > 0 => ngược chiều, d' < 0 => cùng chiều.
Chạy: python3 tinh.py
"""
from fractions import Fraction as Fr
from math import sqrt, isclose


def anh(f, d):
    """Trả về d' (Fraction) hoặc None nếu ảnh ở vô cực."""
    f, d = Fr(f), Fr(d)
    inv = 1 / f - 1 / d
    return None if inv == 0 else 1 / inv


def k_abs(d, dp):
    return abs(Fr(dp)) / Fr(d)


def fmt(x, nd=2):
    if x is None:
        return "vô cực"
    x = Fr(x)
    if x.denominator == 1:
        return str(x.numerator)
    return f"{float(x):.{nd}f} (= {x})"


def tinhchat(dp):
    return "ảnh thật, ngược chiều" if dp > 0 else "ảnh ảo, cùng chiều"


def bai(ten, f, d, h):
    dp = anh(f, d)
    k = k_abs(d, dp)
    L = d + dp  # khoảng cách vật–ảnh (ảnh ảo: d + d' = d − |d'|, lấy trị tuyệt đối)
    print(f"  {ten}: f={f}, d={d}, h={h} -> d'={fmt(dp)}, |k|={fmt(k)}, h'={fmt(k*h)}, "
          f"{tinhchat(dp)}, vật–ảnh={fmt(abs(L))}")
    return dp, k


def hr(t):
    print("\n" + "=" * 8 + " " + t)


# ---------------- Lý thuyết ----------------
hr("LÝ THUYẾT — ví dụ kiểm quy ước dấu, bảng dịch chuyển f = 12")
bai("HT ảnh thật", 12, 20, 1)
bai("HT ảnh ảo", 12, 8, 1)
bai("PK", -12, 12, 3)
print("  Bảng f = 12 cm (d -> d', |k|, L = d + d'):")
for d in [60, 36, 24, 18, 16, 14, 13]:
    dp = anh(12, d)
    print(f"    d={d:>3}  d'={float(dp):6.2f}  |k|={float(k_abs(d, dp)):5.2f}  L={float(d+dp):6.2f}")
print("  L nhỏ nhất = 4f = 48 tại d = d' = 24 (bảng xác nhận).")

# ---------------- D1 ----------------
hr("D1 dựng ảnh trên giấy ô ly (1 ô = 2 cm)")
dp, k = bai("a) HT", 8, 12, 2)
print(f"     ô lưới: f=4 ô, d=6 ô, d'={fmt(dp/2)} ô, h=1 ô, h'={fmt(k*2/2)} ô")
dp, k = bai("b) PK (bài ngược)", -12, 24, 3)
# B(-24,3), B'(-8,1): BB' cắt trục chính tại O
xB, yB, xBp, yBp = -24, 3, float(dp), float(k * 3)
xO = xB + (0 - yB) * (xBp - xB) / (yBp - yB)
# tia song song từ B tới I(0,3); đường kéo dài tia ló đi qua B' và F'
xF = 0 + (0 - 3) * (xBp - 0) / (yBp - 3)
print(f"     B({xB},{yB}), B'({xBp},{yBp}) -> O tại x={xO}, F' tại x={xF} (cùng phía vật => PK, |f|=12)")

# ---------------- D2 ----------------
hr("D2 công thức + chứng minh: HT ảnh ảo, PK")
bai("a) HT", 20, 15, 1)
bai("b) PK", -30, 15, Fr(3, 2))

# ---------------- D3 ----------------
hr("D3 bài toán ngược nhiều trường hợp, f = 12")
# a) ảnh cao gấp 3: thật d' = 3d ; ảo d' = -3d
for name, s in [("thật", 3), ("ảo", -3)]:
    # 1/12 = 1/d + 1/(s d) = (s+1)/(s d) -> d = 12 (s+1)/s
    d = Fr(12) * (s + 1) / s
    dp = s * d
    assert anh(12, d) == dp
    print(f"  a) ảnh {name} gấp 3: d={fmt(d)}, d'={fmt(dp)}, vật–ảnh={fmt(abs(d+dp))}")
# b) ảnh cách vật 50 cm
L = 50
# thật: d + d' = L -> d^2 - L d + L f = 0
disc = L * L - 4 * L * 12
r = sqrt(disc)
for d in [(L - r) / 2, (L + r) / 2]:
    print(f"  b) ảnh thật: d={d:g}, d'={L-d:g}")
# ảo: |d'| - d = L, d' = -(d + L): 1/f = 1/d - 1/(d+L) = L/(d(d+L)) -> d^2 + L d - L f = 0
disc2 = L * L + 4 * L * 12
d = (-L + sqrt(disc2)) / 2
print(f"  b) ảnh ảo: d={d:g}, d'={-(d+L):g}  (kiểm: d' theo công thức = {float(anh(12, Fr(d))):g})")

# ---------------- D4 ----------------
hr("D4 dịch chuyển vật–ảnh, f = 15")
prev = None
for d in [45, 30, 20]:
    dp = anh(15, d)
    print(f"  d={d}: d'={fmt(dp)}, L={fmt(d+dp)}, |k|={fmt(k_abs(d, dp))}")
print("  45->30: vật dịch 15 cm về phía TK, ảnh dịch ra xa TK 7,5 cm; L giảm 67,5 -> 60 (=4f).")
print("  30->20: vật dịch 10 cm, ảnh dịch ra xa 30 cm; L tăng 60 -> 80.")
# c) bài ngược: vật lại gần 5 cm, ảnh dịch 10 cm, ảnh mới cao gấp 2 ảnh cũ
# k = f/(d-f) -> (d1-f) = 2 (d1-5-f) -> d1 - f = 10 ; d2' - d1' = f^2/10 = 10 -> f = 10
f = 10
d1, d2 = f + 10, f + 5
d1p, d2p = anh(f, d1), anh(f, d2)
print(f"  c) f={f}, d1={d1}, d1'={fmt(d1p)}, d2={d2}, d2'={fmt(d2p)}, ảnh dịch {fmt(d2p-d1p)}, "
      f"k2/k1={fmt(k_abs(d2, d2p)/k_abs(d1, d1p))}")

# ---------------- D5 ----------------
hr("D5 đo tiêu cự: Bessel + 2f–2f")
L, l, h = 125, 75, 2
f = Fr(L * L - l * l, 4 * L)
print(f"  a) f=(L²-ℓ²)/(4L) = {fmt(f)}")
d1, d2 = Fr(L - l, 2), Fr(L + l, 2)
for d in (d1, d2):
    dp = L - d
    assert anh(f, d) == dp
    print(f"     d={fmt(d)}, d'={fmt(dp)}, h'={fmt(k_abs(d, dp)*h)}")
h1, h2 = k_abs(d1, L - d1) * h, k_abs(d2, L - d2) * h
print(f"     h1'·h2' = {fmt(h1*h2)} = h² -> h = {sqrt(h1*h2):g} (đo chiều cao vật không cần thước đặt vào vật)")
print(f"  b) L nhỏ nhất = 4f = {fmt(4*f)}; L = 70 < 80 -> không có vị trí nào cho ảnh rõ")
Ls = [79.5, 80.6, 80.2]
Ltb = sum(Ls) / 3
dL = sum(abs(x - Ltb) for x in Ls) / 3
print(f"  c) 2f–2f: L = {Ls}, L_tb = {Ltb:.2f}, ΔL_tb = {dL:.2f} -> f = {Ltb/4:.2f} ± {dL/4:.2f} cm "
      f"(làm tròn f = {Ltb/4:.1f} ± {max(dL/4, 0.1):.1f})")
# độ nhạy Bessel không dùng đạo hàm: đổi L hoặc ℓ thêm 1 cm
fL = Fr((L + 1) ** 2 - l * l, 4 * (L + 1))
fl = Fr(L * L - (l + 1) ** 2, 4 * L)
print(f"     L tăng 1 cm -> f = {float(fL):.3f} (đổi {float(fL-f):+.3f}); ℓ tăng 1 cm -> f = {float(fl):.3f} "
      f"(đổi {float(fl-f):+.3f}) => đo L cẩn thận hơn")

# ---------------- D6 ----------------
hr("D6 kính lúp ghi 5×, kính sát mắt")
G = 5
f = Fr(25, G)
print(f"  f = 25/G = {fmt(f)} cm")
for name, Cc, Cv in [("mắt tốt", 25, None), ("mắt cận", 12, 50)]:
    dcc = 1 / (1 / f + Fr(1, Cc))  # ảnh ảo tại Cc: d' = -Cc
    dcv = f if Cv is None else 1 / (1 / f + Fr(1, Cv))
    print(f"  {name}: Cc={Cc}, Cv={Cv or 'vô cực'} -> d từ {fmt(dcc)} đến {fmt(dcv)} cm, "
          f"khoảng xê dịch {fmt(dcv-dcc)} cm; ngắm chừng Cc: |k| = {fmt(Fr(Cc)/dcc)}")
print(f"  mắt tốt ngắm chừng vô cực: G = 25/f = {G}; vật 0,4 mm ngắm Cc -> ảnh {float(Fr(25)/(1/(1/f+Fr(1,25)))*Fr(4,10)):.1f} mm")

# ---------------- D7 ----------------
hr("D7 hệ hai thấu kính, TK1 f1 = 20, d1 = 30, h = 2")
d1p = anh(20, 30)
k1 = k_abs(30, d1p)
print(f"  TK1: d1'={fmt(d1p)}, |k1|={fmt(k1)}, ảnh trung gian thật, ngược chiều, cao {fmt(k1*2)}")
# a) TK2 PK f2 = -20, a = 80
a = 80
d2 = a - d1p
d2p = anh(-20, d2)
k2 = k_abs(d2, d2p)
print(f"  a) a={a}: d2={fmt(d2)}, d2'={fmt(d2p)} (ảo, cách TK1 {fmt(a+d2p)}), |k|={fmt(k1*k2)}, "
      f"h'={fmt(k1*k2*2)}, ngược chiều vật (1 lần ảnh thật)")
# b) ghép sát
inv = Fr(1, 20) + Fr(1, -20)
print(f"  b) ghép sát: 1/f = {inv} -> hệ như tấm kính phẳng; kiểm từng TK: d2 = -60 (vật ảo) -> d2' = {fmt(anh(-20, -60))} = ảnh trùng vật")
# c) TK2 HT f2 = 20, tìm a để ảnh cuối thật, cao gấp 2 vật
# |k2| = 20/(d2-20) = 1 -> d2 = 40
d2 = 40
a = d1p + d2
print(f"  c) d2={d2}, a={fmt(a)}, d2'={fmt(anh(20, d2))}, |k|={fmt(k1*k_abs(d2, anh(20, d2)))}, ảnh thật, cùng chiều vật")

# ---------------- Tự luận ----------------
hr("TỰ LUẬN")
bai("TL1 HT", 6, 9, 1)
bai("TL2 PK", -10, 40, 5)
f = 4
dcc = 1 / (1 / Fr(f) + Fr(1, 25))
print(f"  TL3 kính lúp f=4: G={fmt(Fr(25, f))}; d từ {fmt(dcc)} đến 4; vật 0,5 mm ngắm Cc -> ảnh {float(Fr(25)/dcc*Fr(1,2)):.3f} mm")
print("  TL4 chứng minh PK: |d'| = d|f|/(d+|f|) < |f| và < d; |k| = |f|/(d+|f|) < 1 (đại số, không số)")
bai("TL5 điểm sáng trên trục", 10, 25, 1)
f, L = 18, 81
r = sqrt(L * L - 4 * L * f)
print(f"  TL6 f={f}, L={L}: Δ = {L*L-4*L*f}, d = {(L-r)/2:g} hoặc {(L+r)/2:g}; L_min = {4*f}")
# TL7: Bessel, L = 72, hai ảnh 9 cm và 1 cm
L, H1, H2 = 72, 9, 1
h = sqrt(H1 * H2)
kk = H1 / h  # = d'/d ở vị trí gần vật
d = L / (1 + kk)
dp = L - d
f = d * dp / L
print(f"  TL7 L={L}, ảnh {H1} và {H2} cm -> h={h:g}, d={d:g}, d'={dp:g}, f={f:g}, ℓ={dp-d:g}; "
      f"kiểm (L²-ℓ²)/(4L)={(L*L-(dp-d)**2)/(4*L):g}")
# TL8: hệ HT–HT
d1p = anh(10, 15)
d2 = 40 - d1p
d2p = anh(15, d2)
print(f"  TL8 f1=10, f2=15, a=40, d1=15: d1'={fmt(d1p)}, d2={fmt(d2)}, d2'={fmt(d2p)} "
      f"(ảo, cách TK1 {fmt(40+d2p)}), |k|={fmt(k_abs(15, d1p)*k_abs(d2, d2p))}, h=1 -> h'={fmt(k_abs(15, d1p)*k_abs(d2, d2p))}, ngược chiều")

# ---------------- Luyện tập ----------------
hr("LUYỆN TẬP")
dp = anh(15, 10)
print(f"  I.2 HT f=15, d=10: d'={fmt(dp)} -> ảo, cùng chiều, cách TK 30 cm")
print(f"  I.3 L=72: f_max = L/4 = {72/4:g}")
print(f"  I.4 kính 2,5×: f = {25/2.5:g} cm; ngắm chừng vô cực đặt vật tại d = f = 10 cm")
dp = anh(-20, 30)
print(f"  II.1 PK f=-20, d=30, h=5: d'={fmt(dp)}, h'={fmt(k_abs(30, dp)*5)}; d=60 -> d'={fmt(anh(-20, 60))} (ảnh ra xa TK, tiến về F')")
L, f = 100, 21
r = sqrt(L * L - 4 * L * f)
print(f"  II.2 L={L}, f={f}: ℓ={r:g}, d={(L-r)/2:g}/{(L+r)/2:g}, |k| gần vật = {((L+r)/2)/((L-r)/2):.3f}; 4f={4*f}")
dp = anh(20, 25)
print(f"  III.1 HT f=20, d=25: d'={fmt(dp)}, vật–ảnh = {fmt(25+dp)}")
fs = 1 / (Fr(1, 30) + Fr(1, 20))
print(f"  III.2 ghép sát 30 & 20: f={fmt(fs)}; d=18 -> d'={fmt(anh(fs, 18))}")

# ---------------- Kiểm số docx ----------------
hr("KIỂM SỐ DOCX (đáp án mục E, G, H)")
chk = [(12, 36, 18), (20, 30, 60), (15, 10, -30), (-15, 30, -10), (10, 15, 30), (10, 8, -40), (16, 20, 80)]
for f, d, want in chk:
    assert anh(f, d) == want, (f, d)
assert Fr(100**2 - 60**2, 400) == 16 and Fr(90**2 - 30**2, 360) == 20
assert anh(-20, 30) == -12
assert anh(20, 60) == 30 and anh(20, 40) == 40                      # E6
assert 1 / (Fr(1, 30) + Fr(1, 15)) == 10                             # E10
assert anh(15, 30) == 30 and anh(20, 60 - 30) == 60                  # E11 / G4a
assert anh(20, 30) == 60 and Fr(1, 35) + Fr(1, 55) != Fr(1, 20)      # E12
assert anh(15, 20) == 60 and 20 + 60 == 80                           # G1 (k=3, L=80)
assert anh(10, 15) == 30 and anh(10, 20) == 20                       # G2
assert anh(10, 20) == 20 and anh(12, 6) == -12 and anh(-12, 36) == -9  # H3, H4, H5
assert 1 / (Fr(1, 30) + Fr(1, 60)) == 20 and Fr(80, 4) == 20         # H9, H8
assert anh(12, 18) == 36 and anh(15, 10) == -30 and anh(-15, 30) == -10  # ví dụ mục C
assert anh(10, 30) == 15 and anh(10, 12) == 60 and Fr(45**2 - 15**2, 180) == 10
assert 1 / (1 / Fr(5) + Fr(1, 20)) == 4                              # Dạng 8b
print("  E1–E12, G1–G4, H3–H9, ví dụ mục C: khớp")
print("\nOK — mọi assert qua.")
