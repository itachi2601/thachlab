"""Đáp số WP-04 (sóng cơ, giao thoa, sóng dừng, sóng âm). Chạy: python3 tinh.py"""
import math
from math import pi, sqrt, cos, sin, acos, log10, floor
R = {}
# W1
f, v = 10, 200.0   # cm/s
lam = v/f
dphi = 2*pi*25/lam
R["W1"] = dict(lam=lam, dphi=dphi, dphi_mod=dphi % (2*pi), u=3*cos(20*pi*0.04 - dphi))
# W2
P, r = 0.5, 10
I = P/(4*pi*r*r); L = 10*log10(I/1e-12)
R["W2"] = dict(I=I, L=L, L20=10*log10(P/(4*pi*400)/1e-12), dL=20*log10(2))
# W3
l = 0.9; lam3 = 2*l/3
R["W3"] = dict(lam=lam3, v=lam3*50, f1=lam3*50/(2*l))
# W4
A4, f4, v4 = 0.002, 25, 0.5
R["W4"] = dict(lam=v4/f4, vmax=2*pi*f4*A4, ratio=2*pi*f4*A4/v4)
# W5 cùng pha AB=19 lam=3.2
def count(AB, lam, same):
    mx = mn = 0
    for k in range(-100, 100):
        d = (k if same else k+0.5)*lam      # cực đại
        if abs(d) < AB: mx += 1
        d = ((k+0.5) if same else k)*lam    # cực tiểu
        if abs(d) < AB: mn += 1
    return mx, mn
R["W5"] = dict(lam=0.8/25*100, n=count(19, 3.2, True))
R["W6"] = dict(n=count(17.5, 3.2, False))
# W7 hình vuông cạnh 10, lam=1.2 : d2-d1 trên CD thuộc (-4.142,4.142)
dm = 10*sqrt(2) - 10
mx7 = sum(1 for k in range(-20, 21) if abs(k*1.2) < dm)
mn7 = sum(1 for k in range(-20, 21) if abs((k+.5)*1.2) < dm)
R["W7"] = dict(dm=dm, mx=mx7, mn=mn7)
# W8 đầu cố định - đầu tự do
l8, v8 = 0.75, 60
f1 = v8/(4*l8)
fl = [(2*n+1)*f1 for n in range(0, 20) if 150 <= (2*n+1)*f1 <= 250]
R["W8"] = dict(f1=f1, fs=fl, bung=[(int(f/f1)+1)//2 for f in fl])
# W9
R["W9"] = dict(A=4*abs(sin(2*pi*5/60)), d=60/4)
# W10
AB, lamk, k = 20, 3, 6
R["W10"] = dict(kmax=floor(AB/lamk), x=(AB**2 - (k*lamk)**2)/(2*k*lamk))
# W11 tỉ lệ thời gian |u_M|<=2 với A_M=2√3, T=0.2
c = 2/(2*sqrt(3))
frac = 1 - 2*acos(c)/pi
N = 2000000
cnt = sum(1 for i in range(N) if abs(2*sqrt(3)*cos(2*pi*(i+.5)/N)) <= 2)
R["W11"] = dict(frac=frac, t=frac*0.2, num=cnt/N)
# W12
rA = 1.0; rB = 10.0; rM = 5.5
LM = 60 - 20*log10(rM)
R["W12"] = dict(LM=LM, LM2=LM+10*log10(2))
# mini-test
R["M1"] = dict(f=2.0, lam=2*pi/(0.02*pi), v=2*100, vmax=4*pi*6)
R["M2"] = dict(n=count(12, 1.5, True))
l3 = 0.6; lam_m3 = 4*l3/7
R["M3"] = dict(lam=lam_m3, v=lam_m3*70)
I4 = 1e-12*10**7
R["M4"] = dict(r=2*10**((70-50)/20), I=I4, P=4*pi*4*I4)
for k_, v_ in R.items():
    print(k_, {a: (round(b, 6) if isinstance(b, float) else b) for a, b in v_.items()})
