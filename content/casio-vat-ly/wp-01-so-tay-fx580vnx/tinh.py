"""Tính đáp số cho 20 bài luyện của WP-01. Mọi đáp số trong bai-luyen.md phải khớp in ra ở đây.
Chạy: python3 tinh.py  (không cần thư viện ngoài)"""
import math, cmath
from math import pi, sqrt, log, exp, cos, atan2, degrees

R = {}
# --- SOLVE ---
R["S1_t"] = 2 / 15                                   # 4cos(5πt−π/3)=2, t>0 nhỏ nhất
R["S2_t"] = (0.3*880*100 + 0.5*4180*20) / (0.3*880 + 0.5*4180)
R["S3_t"] = 5.27 * math.log2(1/0.3)
# --- CALC ---
g = 9.8
R["C1_T"] = [2*pi*sqrt(l/g) for l in (0.8, 1.0, 1.2)]
R["C2_P"] = [200**2*r/(r*r + 40**2) for r in (20, 40, 60, 80)]
# --- TABLE ---
L, C, Rr, U = 0.1, 25e-6, 50, 100
def I(f):
    w = 2*pi*f
    return U / sqrt(Rr**2 + (w*L - 1/(w*C))**2)
R["T1_f0"] = 1/(2*pi*sqrt(L*C))
R["T1_I5"] = {f: I(f) for f in range(80, 125, 5)}
R["T1_best5"] = max(R["T1_I5"], key=R["T1_I5"].get)
f05 = [80 + 0.5*k for k in range(0, 81)]
R["T1_best05"] = max(f05, key=I)
R["T1_Imax"] = I(R["T1_best05"])
R["T2_n"] = sum(1 for k in range(-6, 7) if abs(2*k) < 10.5)
R["T3_x"] = 4*0.45*2/1.0                              # mm, D=2 m, a=1 mm, i1=0,9 mm
# --- SỐ PHỨC ---
z1 = cmath.rect(3, pi/3); z2 = cmath.rect(4, -pi/6)
R["X1"] = (abs(z1+z2), cmath.phase(z1+z2), degrees(cmath.phase(z1+z2)))
Z = 30 + 40j
Ic = cmath.rect(100, 0)/Z
R["X2"] = (abs(Ic), cmath.phase(Ic), abs(Ic)*sqrt(2))
Zb = cmath.rect(200, pi/6)/cmath.rect(2, -pi/6)
R["X3"] = (abs(Zb), Zb.real, Zb.imag, Zb.imag/(100*pi))
x2 = cmath.rect(6, pi/3) - cmath.rect(4, pi/6)
R["X4"] = (abs(x2), cmath.phase(x2), degrees(cmath.phase(x2)))
# --- VECTƠ ---
q = 1.6e-19; v = (2e5, 3e5, 0); B = (0, 0, 0.5)
cr = (v[1]*B[2]-v[2]*B[1], v[2]*B[0]-v[0]*B[2], v[0]*B[1]-v[1]*B[0])
F = tuple(q*c for c in cr)
R["V1"] = (F, sqrt(sum(c*c for c in F)))
Fv = (4, -3, 2); d = (2, 1, 5)
dot = sum(a*b for a, b in zip(Fv, d))
R["V2"] = (dot, degrees(math.acos(dot/sqrt(29*30))))
# --- THỐNG KÊ ---
gs = [9.78, 9.83, 9.80, 9.86, 9.81]
m = sum(gs)/5
R["St1"] = (m, sqrt(sum((x-m)**2 for x in gs)/5), sqrt(sum((x-m)**2 for x in gs)/4))
ll = [0.30, 0.50, 0.70, 0.90, 1.10]; T2 = [1.22, 2.01, 2.78, 3.60, 4.37]
def lin(x, y):
    n = len(x); mx = sum(x)/n; my = sum(y)/n
    b = sum((a-mx)*(c-my) for a, c in zip(x, y))/sum((a-mx)**2 for a in x)
    a = my - b*mx
    r = sum((p-mx)*(c-my) for p, c in zip(x, y))/sqrt(sum((p-mx)**2 for p in x)*sum((c-my)**2 for c in y))
    return a, b, r
a, b, r = lin(ll, T2)
R["St2"] = (a, b, r, 4*pi**2/b)
tt = [0, 2, 4, 6, 8]; N = [1000, 640, 410, 262, 168]
a2, b2, r2 = lin(tt, [log(n) for n in N])
R["St3"] = (exp(a2), b2, r2, log(2)/(-b2))
# --- HẰNG SỐ / ĐƠN VỊ ---
h, c, e = 6.62607015e-34, 299792458, 1.602176634e-19
eps = h*c/500e-9
R["K1"] = (eps, eps/e)
dm = 2*1.0073 + 2*1.0087 - 4.0015
R["K2"] = (dm, dm*931.5, dm*931.5/4)
V = 2*8.314*300/1.013e5
R["K3"] = (V, V*1000)
for k, v_ in R.items():
    print(k, v_)
