"""Đáp số WP-03 (dao động cơ). Mọi số trong bai-luyen.md / mini-test.md phải khớp in ra ở đây.
Chạy: python3 tinh.py  (chỉ dùng thư viện chuẩn)"""
import math, cmath
from math import pi, sqrt, cos, sin, radians, degrees, acos
R = {}
# D1 lò xo
k, m, A = 50, 0.2, 0.06
w = sqrt(k/m)
R["D1"] = dict(w=w, T=2*pi/w, f=w/(2*pi), vmax=w*A, amax=w*w*A, E=0.5*k*A*A)
# D2 con lắc đơn
l, g, a0 = 0.75, 9.81, radians(8)
R["D2"] = dict(T=2*pi*sqrt(l/g), vmax=sqrt(2*g*l*(1-cos(a0))), vmax_approx=sqrt(g*l)*a0)
# D3
t = 0.25; ph = 4*pi*t + pi/6
R["D3"] = dict(x=5*cos(ph), v=-5*4*pi*sin(ph), a=-(4*pi)**2*5*cos(ph))
# D4
z = cmath.rect(8, pi/6) + cmath.rect(8, pi/2)
R["D4"] = dict(A=abs(z), phi=cmath.phase(z), phi_deg=degrees(cmath.phase(z)))
# D5 SOLVE: x=10cos(wt+pi/3) = -5sqrt3, T=0.6
w5 = 2*pi/0.6
R["D5"] = dict(w=w5, t=(5*pi/6 - pi/3)/w5)
# D6 quãng đường x=6cos(4πt−π/3) từ 0 đến 1,375 s
def path(f_v, t1, n=2000000):
    dt = t1/n; s = 0.0
    for i in range(n):
        s += abs(f_v((i+0.5)*dt))*dt
    return s
v6 = lambda t: -6*4*pi*sin(4*pi*t - pi/3)
R["D6"] = dict(s=path(v6, 1.375), T=0.5)
# D7 treo thẳng đứng
m7, k7, g7 = 0.25, 100, 9.8
dl = m7*g7/k7
R["D7"] = dict(dl=dl, T=2*pi*sqrt(m7/k7),
               A2=(k7*(dl+0.02), k7*max(dl-0.02, 0)),
               A5=(k7*(dl+0.05), 0.0))
# D8 đồng hồ quả lắc
al, dT = 1.2e-5, 30
ratio = sqrt(1+al*dT)
R["D8"] = dict(ratio=ratio, lost=86400*(1-1/ratio))
# D9 năng lượng
m9, k9, A9, x9 = 0.1, 40, 0.05, 0.03
W = 0.5*k9*A9**2; Wt = 0.5*k9*x9**2; Wd = W-Wt
R["D9"] = dict(W=W, Wt=Wt, Wd=Wd, v=sqrt(2*Wd/m9), x_wd3wt=A9/2)
# D10 con lắc đơn góc lớn
m10, l10, g10, a010, a10 = 0.1, 1.0, 9.8, radians(60), radians(30)
R["D10"] = dict(v=sqrt(2*g10*l10*(cos(a10)-cos(a010))), tau=m10*g10*(3*cos(a10)-2*cos(a010)))
# D11 tắt dần
k11, m11, mu, g11, A11 = 100, 0.2, 0.05, 10, 0.10
dA = 2*mu*m11*g11/k11; x0 = mu*m11*g11/k11; w11 = sqrt(k11/m11)
Nh = A11/dA
R["D11"] = dict(dA=dA, S=k11*A11**2/(2*mu*m11*g11), v1=w11*(A11-x0), Nhalf=Nh, t=Nh*pi/w11, T=2*pi/w11)
# D12 A nhỏ nhất
A12f = lambda X: sqrt(36 + X*X + 12*X*cos(radians(150)))
best = min((i/10 for i in range(0, 101)), key=A12f)
z12 = cmath.rect(6, pi/3) + cmath.rect(-6*cos(radians(150)), -pi/2)
R["D12"] = dict(A2=-6*cos(radians(150)), Amin=A12f(-6*cos(radians(150))), best_step01=best, Abest=A12f(best), phi=cmath.phase(z12))
# ---- mini-test ----
vmax, amax = 0.2*pi, 4*pi**2
w_m1 = amax/vmax
R["M1"] = dict(w=w_m1, A=vmax/w_m1, T=2*pi/w_m1)
l2 = 0.44/0.44; l1 = l2*1.44
R["M2"] = dict(l1=l1, l2=l2, T1=2*pi*sqrt(l1/9.8), T2=2*pi*sqrt(l2/9.8))
T3, g3 = 0.4, 9.8
dl3 = g3*T3**2/(4*pi**2); A3 = dl3/2
R["M3"] = dict(dl=dl3, A=A3, vmax=2*pi/T3*A3, ratio=(dl3+A3)/(dl3-A3))
z4 = cmath.rect(4, pi/6) + cmath.rect(3, -pi/3)
A4, p4 = abs(z4), cmath.phase(z4)
cands = [(-p4 + math.acos(0.5) + 2*pi*n)/(2*pi) for n in range(-1, 3)] + [(-p4 - math.acos(0.5) + 2*pi*n)/(2*pi) for n in range(-1, 3)]
R["M4"] = dict(A=A4, phi=p4, t=min(c for c in cands if c > 1e-9))
for k_, v_ in R.items():
    print(k_, {a: (round(b, 6) if isinstance(b, float) else b) for a, b in v_.items()})
