#!/usr/bin/env python3
"""CĐ14 (bài 158) — Gương phẳng, bóng tối và nửa tối: tính mọi số liệu dùng trong nguon.md.

Chạy: python3 content/hsg9/cd14-guong-phang-bong-toi/tinh.py
Quy ước: góc tới/góc phản xạ đo với PHÁP TUYẾN; góc hướng đo ngược chiều kim đồng hồ từ trục Ox nằm ngang.
Mọi kết quả kiểm bằng hình học véc-tơ (phản xạ thật), không chỉ thay công thức.
"""
import math

d2r, r2d = math.radians, math.degrees


def unit(deg):
    return (math.cos(d2r(deg)), math.sin(d2r(deg)))


def reflect_dir(v, mirror_deg):
    """Phản xạ véc-tơ hướng v trên gương có phương mirror_deg."""
    m = unit(mirror_deg)
    dot = v[0] * m[0] + v[1] * m[1]
    return (2 * dot * m[0] - v[0], 2 * dot * m[1] - v[1])


def ang(v):
    return r2d(math.atan2(v[1], v[0])) % 360


def angle_between(u, v):
    c = (u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v))
    return r2d(math.acos(max(-1, min(1, c))))


def hr(t):
    print("\n" + "=" * 8 + " " + t + " " + "=" * 8)


# ---------------------------------------------------------------- D1
hr("D1 Phản xạ, đặt gương, gương quay")
# (a) Tia nắng chếch xuống, hợp phương ngang 50°, đi từ trái sang phải; muốn tia phản xạ thẳng đứng xuống giếng.
inc = unit(-50)              # hướng truyền của tia tới
out = unit(-90)              # hướng truyền của tia phản xạ
# pháp tuyến song song với (out - inc); gương vuông góc pháp tuyến
n = (out[0] - inc[0], out[1] - inc[1])
mirror = (ang(n) + 90) % 180
i_a = angle_between((-inc[0], -inc[1]), n) if False else None
SIR = angle_between((-inc[0], -inc[1]), out)   # góc giữa tia tới và tia phản xạ (tại I)
i_a = SIR / 2
mir_h = min(mirror, 180 - mirror)
assert abs(ang(reflect_dir(inc, mirror)) - 270) < 1e-9
print(f"(a) góc SIR = {SIR:.1f}°, góc tới i = {i_a:.1f}°, gương hợp phương ngang {mir_h:.1f}° (phương gương {mirror:.1f}°)")
# (b) cùng tia nắng, muốn hắt thẳng đứng LÊN trần
out_b = unit(90)
n_b = (out_b[0] - inc[0], out_b[1] - inc[1])
mirror_b = (ang(n_b) + 90) % 180
SIR_b = angle_between((-inc[0], -inc[1]), out_b)
assert abs(ang(reflect_dir(inc, mirror_b)) - 90) < 1e-9
print(f"(b) hắt lên: góc SIR = {SIR_b:.1f}°, i = {SIR_b/2:.1f}°, gương hợp phương ngang {min(mirror_b,180-mirror_b):.1f}°")
# (c) Laser chiếu vào gương, tia phản xạ đập VUÔNG GÓC vào tường cách điểm tới 4,0 m; quay gương 3°.
D_tuong, quay = 4.0, 3.0
# kiểm 2α bằng véc-tơ: tia tới cố định hướng 200°, gương phương 10° → quay 3°
v0 = unit(200)
r1, r2 = reflect_dir(v0, 10), reflect_dir(v0, 13)
print(f"(c) kiểm véc-tơ: gương quay {quay}° → tia phản xạ quay {angle_between(r1, r2):.4f}°")
x = D_tuong * math.tan(d2r(2 * quay))
print(f"(c) vệt sáng dịch {x:.3f} m ≈ {x*100:.0f} cm; nếu (sai) nghĩ quay 3° → {D_tuong*math.tan(d2r(quay))*100:.0f} cm")
# (d) muốn vệt sáng dịch 70 cm thì quay gương bao nhiêu
phi = r2d(math.atan(0.70 / D_tuong))
print(f"(d) vệt dịch 70 cm → tia quay {phi:.2f}°, gương quay {phi/2:.2f}°")

# ---------------------------------------------------------------- D2
hr("D2 Bóng người dưới đèn đường (nguồn điểm)")
H, h, v = 4.5, 1.5, 1.2     # đèn cao 4,5 m; người 1,5 m; đi xa đèn 1,2 m/s
for x0 in (2.0, 5.0):
    l = h * x0 / (H - h)
    print(f"người cách chân đèn {x0} m → bóng dài {l:.2f} m, đỉnh bóng cách chân đèn {x0+l:.2f} m")
v_dinh = v * H / (H - h)
v_dai = v * h / (H - h)
print(f"tốc độ đỉnh bóng = {v_dinh:.2f} m/s; bóng dài thêm {v_dai:.2f} m mỗi giây")
# kiểm bằng sai phân
x1, x2 = 3.0, 3.0 + v * 1.0
tip = lambda x_: x_ + h * x_ / (H - h)
assert abs((tip(x2) - tip(x1)) - v_dinh) < 1e-9
# (c) có tường thẳng đứng cách chân đèn 9 m: bóng leo lên tường khi đỉnh bóng chạm tường
x_cham = 9.0 * (H - h) / H
print(f"(c) tường cách đèn 9 m: bóng bắt đầu lên tường khi người cách đèn {x_cham:.2f} m")
x_n = 7.5
y_tuong = H - (H - h) * 9.0 / x_n  # đường từ đèn qua đỉnh đầu, tới x = 9
print(f"(c) người cách đèn {x_n} m: bóng trên tường cao {y_tuong:.2f} m (phần trên sàn dài {9.0-x_n:.2f} m)")
# kiểm tam giác đồng dạng: đường qua (0,H) và (x_n,h)
slope = (h - H) / x_n
assert abs((H + slope * 9.0) - y_tuong) < 1e-12
# (d) hai đèn: đèn thứ hai cao 4,5 m cách đèn thứ nhất 12 m; người đứng giữa cách đèn 1 là 4 m
x_p = 4.0
l1 = h * x_p / (H - h)
l2 = h * (12 - x_p) / (H - h)
print(f"(d) hai đèn cách 12 m, người cách đèn 1 {x_p} m: bóng do đèn 1 dài {l1:.2f} m, do đèn 2 dài {l2:.2f} m")

# ---------------------------------------------------------------- D3
hr("D3 Bóng với nguồn rộng: vùng tối, nửa tối")
D, d, a, L = 20.0, 30.0, 60.0, 180.0   # cm: đèn đĩa D, đĩa chắn d, nguồn–vật a, nguồn–màn L


def shadow(D, d, a, L):
    # tia cùng mép: (D/2 at 0) -> (d/2 at a)
    y_toi = D / 2 + (d / 2 - D / 2) * L / a
    y_ngoai = -D / 2 + (d / 2 + D / 2) * L / a
    return 2 * y_toi, 2 * y_ngoai


dp = d * L / a
dt, dn = shadow(D, d, a, L)
print(f"nguồn điểm: bóng {dp:.0f} cm; nguồn rộng: vùng tối {dt:.0f} cm, mép ngoài nửa tối {dn:.0f} cm, vành rộng {(dn-dt)/2:.0f} cm")
print(f"diện tích vùng tối / diện tích đĩa chắn = {(dt/d)**2:.3f}")
# (c) thay đĩa chắn d2 = 12 cm (nhỏ hơn nguồn)
d2 = 12.0
L0 = a * D / (D - d2)
print(f"(c) d2 = {d2:.0f} cm: vùng tối biến mất khi L = {L0:.0f} cm")
dt2, dn2 = shadow(D, d2, a, L)
print(f"(c) tại L = {L:.0f} cm: 'vùng tối' tính ra {dt2:.0f} cm (<0: không còn vùng tối; đĩa giữa {abs(dt2):.0f} cm thấy vành sáng của nguồn), mép ngoài nửa tối {dn2:.0f} cm")
dt3, dn3 = shadow(D, d2, a, 120.0)
print(f"(c) tại L = 120 cm: vùng tối {dt3:.1f} cm, mép ngoài nửa tối {dn3:.1f} cm")
# (d) dịch màn để vùng tối có đường kính 60 cm (d = 30)
L45 = (60 / 2 - D / 2) * a / (d / 2 - D / 2)
print(f"(d) vùng tối 60 cm khi L = {L45:.0f} cm; lúc đó mép ngoài nửa tối {shadow(D,d,a,L45)[1]:.0f} cm")
# kiểm bằng giao điểm đường thẳng tổng quát
def line_y(p, q, x):
    return p[1] + (q[1] - p[1]) * (x - p[0]) / (q[0] - p[0])
assert abs(2 * line_y((0, D/2), (a, d/2), L) - dt) < 1e-9
assert abs(2 * line_y((0, -D/2), (a, d/2), L) - dn) < 1e-9
# bóng nắng (tia song song): cột cờ
h_coc, l_coc, l_cot = 1.2, 0.8, 7.4
print(f"bóng nắng: cọc 1,2 m bóng 0,8 m; cột bóng 7,4 m → cột cao {h_coc*l_cot/l_coc:.2f} m")

# ---------------------------------------------------------------- D4
hr("D4 Ảnh khi vật/gương dịch chuyển")
d0, v_ng = 3.0, 1.2
print(f"(a) người cách gương {d0} m → cách ảnh {2*d0:.1f} m; đi tới gương {v_ng} m/s: ảnh lại gần người {2*v_ng:.1f} m/s; sau 1,5 s cách ảnh {2*(d0-v_ng*1.5):.1f} m")
v_g = 0.4
print(f"(b) người đứng yên, gương lùi ra xa {v_g} m/s (vuông góc mặt gương): ảnh đi xa {2*v_g:.1f} m/s so với đất; sau 2 s người–ảnh {2*(d0+v_g*2):.1f} m")
# (c) người đi theo phương hợp với mặt gương 60°, tốc độ 1,2 m/s
beta, vv = 60.0, 1.2
# gương là trục Ox (y=0), người ở y>0, đi về phía gương
vel = (vv * math.cos(d2r(beta)), -vv * math.sin(d2r(beta)))
vel_img = (vel[0], -vel[1])
rel = math.hypot(vel[0] - vel_img[0], vel[1] - vel_img[1])
print(f"(c) đi hợp mặt gương {beta:.0f}°, {vv} m/s: ảnh chuyển động {math.hypot(*vel_img):.2f} m/s so với đất; người–ảnh lại gần nhau {rel:.3f} m/s (= 2v·sin60° = {2*vv*math.sin(d2r(beta)):.3f})")
print(f"    góc giữa vận tốc người và vận tốc ảnh = {angle_between(vel, vel_img):.0f}°")
# (d) người đứng yên cách gương 3 m, gương quay 15° quanh trục thẳng đứng đi qua chân đường vuông góc → ảnh dời trên cung tròn
R = d0
q = 15.0
# ảnh quay góc 2q quanh trục, bán kính 3 m
chord = 2 * R * math.sin(d2r(2 * q) / 2)
print(f"(d) gương quay {q:.0f}° quanh trục qua chân H: ảnh quay {2*q:.0f}° quanh H trên đường tròn bán kính {R} m, dời {chord:.3f} m (dây cung)")
# kiểm: ảnh của điểm (0,3) qua đường thẳng qua gốc phương q
def mirror_pt(p, deg):
    m = unit(deg)
    dot = p[0] * m[0] + p[1] * m[1]
    return (2 * dot * m[0] - p[0], 2 * dot * m[1] - p[1])
P = (0.0, 3.0)
I0, I1 = mirror_pt(P, 0), mirror_pt(P, q)
assert abs(math.dist(I0, I1) - chord) < 1e-9

# ---------------------------------------------------------------- D5
hr("D5 Vùng nhìn thấy, gương thấy toàn thân")
h_ng, mat_dinh = 1.70, 0.12
mat = h_ng - mat_dinh
PQ = h_ng / 2
Q = mat / 2
P = (mat + h_ng) / 2
print(f"(a) người {h_ng} m, mắt cao {mat:.2f} m: gương tối thiểu {PQ:.3f} m; mép dưới {Q:.2f} m; mép trên {P:.2f} m (kiểm {P-Q:.3f})")
print(f"    nếu (sai) lấy mép dưới = h/2 = {h_ng/2:.3f} m thì lệch {h_ng/2-Q:.3f} m (= nửa khoảng mắt–đỉnh)")
g_cao, g_duoi = 0.60, 0.95
g_tren = g_duoi + g_cao
y_thap = 2 * g_duoi - mat
y_cao = 2 * g_tren - mat
print(f"(b) gương {g_cao} m, mép dưới {g_duoi} m (mép trên {g_tren:.2f}): thấy từ độ cao {y_thap:.2f} m tới {min(y_cao,h_ng):.2f} m (không thấy chân, không thấy đỉnh đầu)")
# (c) vùng nhìn thấy trên tường đối diện: gương rộng 40 cm treo tường; mắt trên trục, cách gương 30 cm; tường đối diện cách gương 2,0 m
w, dm, Lw = 0.40, 0.30, 2.0
band = w * (dm + Lw) / dm
print(f"(c) gương rộng {w} m, mắt cách {dm} m, tường đối diện cách gương {Lw} m: thấy dải tường rộng {band:.3f} m")
dm2 = 0.60
band2 = w * (dm2 + Lw) / dm2
print(f"    lùi mắt ra cách gương {dm2} m: dải còn {band2:.3f} m (lại gần thấy nhiều hơn)")
# kiểm bằng giao điểm: O' tại (0,-dm); mép (±w/2, 0); tường y = Lw
xw = (w / 2) * (Lw + dm) / dm
assert abs(2 * xw - band) < 1e-12
# (d) mắt lệch trục: mắt cách gương 0,5 m, lệch sang phải mép phải gương 0,3 m (x=0,5); điểm S trên tường đối diện (cách gương 2 m), x_S = ? có thấy không
O = (0.5, 0.5)  # (x ngang, khoảng cách tới gương)
Op = (O[0], -O[1])
for xs in (-1.5, -3.4):
    S = (xs, Lw)
    # giao O'S với gương y=0
    t = (0 - Op[1]) / (S[1] - Op[1])
    xi = Op[0] + t * (S[0] - Op[0])
    print(f"(d) mắt (x=0,5; cách 0,5 m), S trên tường x={xs}: O'S cắt gương tại x={xi:.3f} → {'thấy' if abs(xi)<=w/2 else 'không thấy'}")
x_trai = Op[0] + (-w/2 - Op[0]) * (Lw - Op[1]) / (0 - Op[1])
x_phai = Op[0] + (w/2 - Op[0]) * (Lw - Op[1]) / (0 - Op[1])
print(f"    dải thấy được trên tường: x từ {min(x_trai,x_phai):.2f} m đến {max(x_trai,x_phai):.2f} m")

# ---------------------------------------------------------------- D6
hr("D6 Tia qua điểm cho trước, đường ngắn nhất")
a_A, b_B, s = 30.0, 50.0, 60.0   # cm: A cách gương 30, B cách gương 50, hai chân cách nhau 60
SB = math.hypot(s, a_A + b_B)
xI = s * a_A / (a_A + b_B)
print(f"(a) đường ngắn nhất A→gương→B = {SB:.0f} cm; điểm tới I cách chân của A {xI:.1f} cm")
iI = r2d(math.atan(xI / a_A))
print(f"    góc tới tại I = {iI:.2f}° (tan i = {xI/a_A:.3f})")
# kiểm: đường đi qua điểm khác dài hơn
f = lambda x_: math.hypot(x_, a_A) + math.hypot(s - x_, b_B)
assert all(f(xI) < f(xI + e) for e in (-5, -1, 1, 5))
print(f"    so sánh: I lệch 10 cm → {f(xI+10):.2f} cm; I ở trung điểm 30 cm → {f(30):.2f} cm")
# (b) bài người lấy nước: lều A cách sông 30 m, nhà B cách sông 50 m, chân cách nhau 60 m, đi 1,25 m/s
vn = 1.25
print(f"(b) quãng đường ngắn nhất 100 m, thời gian {SB/vn:.0f} s (cùng số với (a) nếu đổi cm → m)")
# (c) hai gương vuông góc: tia từ A phản xạ trên G1 rồi G2 rồi tới B. Góc vuông tại O gốc; G1 là trục Ox (y=0, x>0), G2 là trục Oy.
A = (40.0, 20.0)
B = (10.0, 50.0)
A1 = (A[0], -A[1])          # ảnh A qua G1 (Ox)
A12 = (-A1[0], A1[1])       # ảnh A1 qua G2 (Oy)
L_c = math.dist(A12, B)
# điểm tới trên G2: giao A12-B với x=0; trên G1: giao A1-J với y=0
tJ = (0 - A12[0]) / (B[0] - A12[0])
J = (0.0, A12[1] + tJ * (B[1] - A12[1]))
tI = (0 - A1[1]) / (J[1] - A1[1])
Ipt = (A1[0] + tI * (J[0] - A1[0]), 0.0)
print(f"(c) hai gương vuông góc, A(40;20), B(10;50) cm: tia A→G1(Ox)→G2(Oy)→B dài {L_c:.2f} cm; I trên Ox tại x={Ipt[0]:.2f}; J trên Oy tại y={J[1]:.2f}")
assert Ipt[0] > 0 and J[1] > 0
chk = math.dist(A, Ipt) + math.dist(Ipt, J) + math.dist(J, B)
assert abs(chk - L_c) < 1e-9
# kiểm định luật phản xạ tại I và J
v1 = (Ipt[0] - A[0], Ipt[1] - A[1]); v2 = (J[0] - Ipt[0], J[1] - Ipt[1]); v3 = (B[0] - J[0], B[1] - J[1])
assert angle_between(reflect_dir(v1, 0), v2) < 1e-6 and angle_between(reflect_dir(v2, 90), v3) < 1e-6
print(f"    tổng đường ({chk:.2f}) khớp; góc(tia tới AI, tia ló JB) = {angle_between(v1, v3):.1f}° → hai gương vuông góc: tia ló luôn song song ngược chiều tia tới")

# ---------------------------------------------------------------- D7
hr("D7 Hai gương hợp góc")


def count_images(alpha, theta):
    """Đếm ảnh của điểm ở góc theta (0<theta<alpha) trong góc giữa gương G1 (phương 0°) và G2 (phương alpha).
    Dựng chuỗi ảnh xen kẽ; dừng khi ảnh nằm sau cả hai gương (trong góc đối đỉnh [180, 180+alpha])."""
    imgs = set()
    for first in (1, 2):
        th, which = theta, first
        while True:
            th = (-th) % 360 if which == 1 else (2 * alpha - th) % 360
            imgs.add(round(th, 6))
            if 180 - 1e-9 <= th <= 180 + alpha + 1e-9:
                break
            which = 2 if which == 1 else 1
            if len(imgs) > 100:
                break
    return len(imgs)


for al in (90, 72, 60, 45, 120, 100):
    on = count_images(al, al / 2)
    off = count_images(al, al / 3)
    print(f"α={al}°: 360/α={360/al:.2f}; vật trên phân giác {on} ảnh; vật lệch phân giác (θ=α/3) {off} ảnh")

# (b) tia sáng: α = 72°, i1 = 25°
al, i1 = 72.0, 25.0


def trace_wedge(alpha, i1, nmax=20):
    """Tia tới G1 (phương 0°, gốc O) tại I1=(1,0) với góc tới i1, đi về phía O. Trả về list góc tới và hướng cuối."""
    # tia tới đến từ trên, hướng truyền hợp với pháp tuyến (0,-1)... tia hướng về phía O (x giảm)
    v_in = (-math.sin(d2r(i1)), -math.cos(d2r(i1)))
    p = (1.0, 0.0)
    v = reflect_dir(v_in, 0)
    incid = [i1]
    cur = 1
    for _ in range(nmax):
        nxt = 2 if cur == 1 else 1
        mdeg = alpha if nxt == 2 else 0.0
        m = unit(mdeg)
        # giao tia p + t v với đường thẳng qua O phương m: cross(m, p + t v) = 0
        cr = lambda a_, b_: a_[0] * b_[1] - a_[1] * b_[0]
        den = cr(m, v)
        if abs(den) < 1e-12:
            break
        t = -cr(m, p) / den
        if t <= 1e-9:
            break
        q = (p[0] + t * v[0], p[1] + t * v[1])
        if q[0] * m[0] + q[1] * m[1] < 0:   # cắt phần kéo dài, không phải gương
            break
        nrm = (-m[1], m[0])
        ii = angle_between((-v[0], -v[1]), nrm)
        ii = min(ii, 180 - ii)
        incid.append(ii)
        v = reflect_dir(v, mdeg)
        p, cur = q, nxt
    return incid, v_in, v


inc_list, vin, vout = trace_wedge(al, i1)
print(f"(b) α={al:.0f}°, i1={i1:.0f}°: các góc tới lần lượt {[round(x,2) for x in inc_list]}")
print(f"    góc giữa tia ló và tia tới = {angle_between(vin, vout):.2f}° (2α = {2*al:.0f}°); góc lệch tổng 360−2α = {360-2*al:.0f}°")
for al_, i_ in ((60, 20), (60, 70), (120, 10), (100, 30)):
    il, vi, vo = trace_wedge(al_, i_)
    print(f"    kiểm α={al_}°, i1={i_}°: góc tới {[round(x,1) for x in il]}, số lần phản xạ {len(il)}, góc(tia ló, tia tới) = {angle_between(vi, vo):.1f}°")
# (c) tia quay ngược lại đường cũ sau khi tới vuông góc gương ở lần phản xạ thứ 3: góc giữa tia và mặt gương γ tăng α mỗi lần:
#     γ1 + 2α = 90°. Điều kiện để tia tới đi vào từ miệng góc mà không bị G2 chắn: γ1 = 90° − i1 < α.
i1c = 70.0
al_c = (90 - (90 - i1c)) / 2
assert (90 - i1c) < al_c
print(f"(c) i1 = {i1c:.0f}°: muốn tia tới vuông góc gương ở lần thứ 3 → α = {al_c:.0f}°")
il, vi, vo = trace_wedge(al_c, i1c)
print(f"    kiểm: góc tới {[round(x,3) for x in il]}; góc(tia ló, tia tới) = {angle_between(vi, vo):.3f}° (180 = quay ngược)")
print(f"    tổng số lần phản xạ trước khi ra = {len(il)}")
# (d) hai gương song song cách 20 cm, S cách G1 6 cm: khoảng cách các ảnh qua G1 tới G1
a_s, e = 6.0, 20.0
# trục x: G1 tại x=0, G2 tại x=20, S tại x=6
S = a_s
chain1, x, w_ = [], S, 1
for k in range(4):
    x = -x if w_ == 1 else 2 * e - x
    chain1.append(x); w_ = 3 - w_
chain2, x, w_ = [], S, 2
for k in range(4):
    x = -x if w_ == 1 else 2 * e - x
    chain2.append(x); w_ = 3 - w_
print(f"(d) gương song song cách {e:.0f} cm, S cách G1 {a_s:.0f} cm (x=0 là G1):")
print(f"    chuỗi bắt đầu từ G1: {chain1}; chuỗi bắt đầu từ G2: {chain2}")
print(f"    khoảng cách S1 (ảnh đầu qua G1) – S2 (ảnh đầu qua G2) = {abs(chain1[0]-chain2[0]):.0f} cm (= 2·khoảng cách hai gương)")

# ---------------------------------------------------------------- Tự luận (số liệu gợi ý)
hr("Tự luận — số liệu gợi ý")
# TL1 hắt nắng chiếu ngang vào hang: tia nắng hợp ngang 36° (chếch xuống); muốn phản xạ nằm ngang đi tiếp sang phải
inc = unit(-36); out = unit(0)
SIRt = angle_between((-inc[0], -inc[1]), out)
mt = (ang((out[0]-inc[0], out[1]-inc[1])) + 90) % 180
print(f"TL1 nắng 36°, hắt ngang cùng chiều: SIR={SIRt:.0f}°, i={SIRt/2:.0f}°, gương hợp ngang {min(mt,180-mt):.0f}°")
out = unit(180)
SIRt = angle_between((-inc[0], -inc[1]), out)
mt = (ang((out[0]-inc[0], out[1]-inc[1])) + 90) % 180
print(f"    hắt ngang ngược lại: SIR={SIRt:.0f}°, i={SIRt/2:.0f}°, gương hợp ngang {min(mt,180-mt):.0f}°")
# TL2 bóng cây cột đèn trên tường: cọc 1,0 m bóng 1,25 m; cột cao? cột cách tường 6 m, bóng trên sàn 6 m tới tường, phần trên tường 1,6 m
h_coc, l_coc = 1.0, 1.25
tan_phi = h_coc / l_coc
hc = 6.0 * tan_phi + 1.6
print(f"TL2 bóng nắng chạm tường: cọc 1,0 m bóng 1,25 m; cột cách tường 6 m, bóng lên tường 1,6 m → cột cao {hc:.2f} m")
# TL3 người dưới đèn đi từ chân đèn: đèn H, người 1,6 m; sau 4 s đi 1 m/s bóng dài 2,0 m → H?
h3, x3, l3 = 1.6, 4.0, 2.0
H3 = h3 * (x3 + l3) / l3
print(f"TL3 người 1,6 m đi 4 m từ chân đèn, bóng dài 2,0 m → đèn cao {H3:.2f} m; tốc độ đỉnh bóng nếu đi 1 m/s: {1*H3/(H3-h3):.2f} m/s")
# TL4 cọc và đèn: hai lần đo bóng (đèn cao chưa biết, khoảng cách chưa biết) — người 1,5 m: đứng A bóng 1,0 m; lùi xa thêm 2,0 m bóng 1,8 m
hh, l1, l2, dx = 1.5, 1.0, 1.8, 2.0
# l = h x/(H-h) → l2 - l1 = h dx/(H-h)
Hh = hh + hh * dx / (l2 - l1)
x_A = l1 * (Hh - hh) / hh
print(f"TL4 bóng 1,0 m rồi lùi 2,0 m bóng 1,8 m (người 1,5 m) → đèn cao {Hh:.2f} m, vị trí đầu cách chân đèn {x_A:.2f} m")
# TL5 gương vuông góc / số ảnh α = 30°
print(f"TL5 α=30°: {count_images(30, 15)} ảnh (phân giác), {count_images(30, 7)} ảnh (lệch); α=40°: {count_images(40, 20)} / {count_images(40, 13)}")
# TL6 ống kính tiềm vọng: hai gương song song nghiêng 45°, ống cao 0,8 m; vật cách gương trên 20 m → ảnh cuối cách mắt?
print("TL6 tiềm vọng: ảnh cuối cách gương dưới = 20 + 0,8 = 20,8 m (ảnh qua G1 làm vật cho G2); ảnh cùng chiều vật")
# TL7 vận tốc ảnh: gương quay đều 2 vòng/phút, tia phản xạ quét trên tường cách 5 m: tốc độ góc tia phản xạ
n_g = 2 / 60
w_r = 2 * 2 * math.pi * n_g
print(f"TL7 gương quay 2 vòng/phút → tia phản xạ quay {2*n_g*60:.0f} vòng/phút; khi vệt sáng ở chân đường vuông góc trên tường cách 5 m, vệt chạy {w_r*5:.2f} m/s")
# TL8 nguồn rộng: đèn tuýp dài 1,2 m treo ngang cách sàn 2,4 m; thước dài 0,3 m song song đèn, cách sàn 0,8 m, ngay dưới tâm đèn → bóng trên sàn
Lt, Hd, lt, ht = 1.2, 2.4, 0.3, 0.8
# toạ độ dọc đèn, độ cao: nguồn từ -0,6..0,6 ở y=2,4; thước -0,15..0,15 ở y=0,8; sàn y=0
k = Hd / (Hd - ht)   # tỉ số khoảng cách từ nguồn: sàn / thước
y_toi = Lt/2 + (lt/2 - Lt/2) * k
y_ng = -Lt/2 + (lt/2 + Lt/2) * k
print(f"TL8 đèn tuýp 1,2 m cao 2,4 m, thước 0,3 m cao 0,8 m: 'vùng tối' {2*y_toi:.2f} m (<0 → không có vùng tối), mép ngoài nửa tối {2*y_ng:.2f} m")
ht2 = 0.2
k2 = Hd / (Hd - ht2)
print(f"    hạ thước xuống cao 0,2 m: vùng tối {2*(Lt/2 + (lt/2-Lt/2)*k2):.3f} m, nửa tối {2*(-Lt/2+(lt/2+Lt/2)*k2):.3f} m")
h_lim = Hd * (1 - Lt / (Lt - lt) * 0) if False else None
# độ cao lớn nhất của thước để còn vùng tối trên sàn: L = a D/(D-d) với L=Hd → a = Hd (D-d)/D
a_lim = Hd * (Lt - lt) / Lt
print(f"    còn vùng tối khi khoảng cách đèn–thước ≥ {a_lim:.2f} m, tức thước cao ≤ {Hd-a_lim:.2f} m")

# ---------------------------------------------------------------- Luyện tập
hr("Luyện tập — số liệu")
print("P1: tia tới hợp mặt gương 25° → i = 65°, góc giữa tia tới và tia phản xạ = 130°; nhiễu 50° (2×25), 65° (i), 25°")
print(f"P2: hai gương 45°, vật bất kì → {count_images(45, 10)} ảnh; nhiễu 8 (đếm vật), 6, vô số")
print("P3: tia tới cố định, quay gương 12° → tia phản xạ quay 24°; nhiễu 12°, 6°, 48°")
print("P4 (khái niệm): vùng nửa tối = chỉ nhận ánh sáng từ một phần nguồn")
# PII-1: người cao 1,60 m (mắt 1,50 m) cách gương 2 m
print("PII-1: người 1,60 m, mắt 1,50 m, cách gương 2 m: a) ảnh cách người 4 m (Đ) b) gương tối thiểu 0,80 m (Đ) c) mép dưới 0,80 m (S, đúng 0,75) d) lùi xa thì cần gương cao hơn (S)")
# PII-2: đèn đĩa D=10 cm, đĩa chắn 20 cm cách đèn 40 cm, màn cách đèn 120 cm
dtt, dnn = shadow(10, 20, 40, 100)
print(f"PII-2: D=10, d=20, a=40, L=100: vùng tối {dtt:.0f} cm, mép ngoài nửa tối {dnn:.0f} cm; nguồn điểm bóng {20*100/40:.0f} cm; vành nửa tối rộng {(dnn-dtt)/2:.0f} cm")
# PIII-1: đèn đường 3,6 m, người 1,6 m đi 1,0 m/s → tốc độ đỉnh bóng
print(f"PIII-1: H=4,0, h=1,6, v=1,2 → đỉnh bóng {1.2*4.0/(4.0-1.6):.2f} m/s; bóng dài thêm {1.2*1.6/(4.0-1.6):.2f} m/s; nhiễu 1,2 (tốc độ người)")
# PIII-2: hai gương α, tia ló song song ngược chiều? hoặc vệt sáng: laser, tường 2,5 m, quay gương 4°
xx = 2.5 * math.tan(d2r(8))
print(f"PIII-2: tường 2,5 m, quay gương 4° → vệt dịch {xx*100:.1f} cm ≈ {round(xx*100)} cm; nhiễu 17 cm (quên 2α)")
print(f"         (nhiễu: {2.5*math.tan(d2r(4))*100:.1f} cm)")
