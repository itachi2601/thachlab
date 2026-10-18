"""Đáp số WP-06 (dao động & sóng điện từ, sóng ánh sáng). Chạy: python3 tinh.py
Mọi số trong bai-luyen.md, mini-test.md, ky-thuat.md (kể cả mục Bẫy) phải lấy từ đây.
Đề cho c = 3.10^8 m/s khi cần."""
import math
from math import pi, sqrt, sin, asin, degrees, radians, tan, floor
c = 3e8
R = {}
def rnd(d): return {a: (round(b, 7) if isinstance(b, float) else b) for a, b in d.items()}
# Q1
L, C, Q0 = 2e-3, 0.5e-6, 2e-6
w = 1/sqrt(L*C)
R["Q1"] = dict(T=2*pi/w, f=w/(2*pi), w=w, I0=w*Q0, U0=Q0/C, W=Q0**2/(2*C))
# Q2
f2 = 90e6; lam2 = c/f2; L2 = 1e-6
R["Q2"] = dict(lam=lam2, C_pF=1/((2*pi*f2)**2*L2)*1e12)
# Q3
lam, a, D = 0.6e-6, 1e-3, 2.0
i3 = lam*D/a
R["Q3"] = dict(i_mm=i3*1e3, sang3=3*i3*1e3, toi3=2.5*i3*1e3)
# Q4
R["Q4"] = dict(r=degrees(asin(sin(radians(40))/1.5)), igh=degrees(asin(1/1.5)))
# Q5
L5, C5 = 0.4e-3, 0.9e-6
T5 = 2*pi*sqrt(L5*C5)
R["Q5"] = dict(T=T5, t_half=T5/6, t_eq=T5/8)
# Q6
L6, Cmin, Cmax = 2e-6, 10e-12, 250e-12
lam_f = lambda C_: 2*pi*c*sqrt(L6*C_)
C25 = (25/(2*pi*c))**2/L6
R["Q6"] = dict(lmin=lam_f(Cmin), lmax=lam_f(Cmax), C25_pF=C25*1e12, theta=180*(C25-Cmin)/(Cmax-Cmin))
# Q7
a7, D7, l7, Lf = 0.8e-3, 1.6, 0.5e-6, 21.5e-3
i7 = l7*D7/a7
Ns = 2*floor(Lf/(2*i7))+1
Nt = 2*sum(1 for k in range(0, 100) if (k+.5)*i7 <= Lf/2)
R["Q7"] = dict(i_mm=i7*1e3, Ns=Ns, Nt=Nt)
# Q8
l1, l2, a8, D8 = 0.48e-6, 0.64e-6, 1.2e-3, 1.8
i1, i2 = l1*D8/a8, l2*D8/a8
xt = 4*i1
nt = 2*floor(15e-3/xt)+1
R["Q8"] = dict(i1=i1*1e3, i2=i2*1e3, xt_mm=xt*1e3, k_ratio=l2/l1, ntrung=nt, x_check=3*i2*1e3)
# Q9
a9, di, dD = 1.5e-3, 0.3e-3, 0.75
lam9 = a9*di/dD
R["Q9"] = dict(lam_um=lam9*1e6, D=0.9e-3*a9/lam9)
# Q10
A, nd, nt_ = radians(6), 1.642, 1.685
Dd, Dt = (nd-1)*A, (nt_-1)*A
R["Q10"] = dict(Dd=degrees(Dd), Dt=degrees(Dt), diff=degrees(Dt-Dd), width_mm=2*(tan(Dt)-tan(Dd))*1e3, width_small=2*(Dt-Dd)*1e3)
# Q11
f1, f2b, L11 = 12e3, 16e3, 1e-3
C1, C2 = 1/((2*pi*f1)**2*L11), 1/((2*pi*f2b)**2*L11)
Cs, Cp = C1*C2/(C1+C2), C1+C2
fs = 1/(2*pi*sqrt(L11*Cs)); fp = 1/(2*pi*sqrt(L11*Cp))
R["Q11"] = dict(C1_uF=C1*1e6, C2_uF=C2*1e6, fs=fs, fp=fp, fs_f=sqrt(f1**2+f2b**2), fp_f=f1*f2b/sqrt(f1**2+f2b**2))
# Q12
a12, D12, x12 = 1e-3, 2.0, 7.0e-3
sang = [(k, a12*x12/(k*D12)*1e6) for k in range(1, 50) if 0.38 <= a12*x12/(k*D12)*1e6 <= 0.76]
toi = [(k, a12*x12/((k+.5)*D12)*1e6) for k in range(0, 50) if 0.38 <= a12*x12/((k+.5)*D12)*1e6 <= 0.76]
R["Q12"] = dict(sang=[(k, round(v, 4)) for k, v in sang], toi=[(k, round(v, 4)) for k, v in toi])
# mini-test
Lm, Cm = 8e-3, 2e-9
fm = 1/(2*pi*sqrt(Lm*Cm))
R["M1"] = dict(f=fm, lam=c/fm, I0=5*sqrt(Cm/Lm))
im = 0.55e-6*1/0.5e-3
R["M2"] = dict(i_mm=im*1e3, d=4.5*im*1e3)
sr = 4/3*sin(radians(40))
R["M3"] = dict(sinr=sr, r=degrees(asin(sr)), igh=degrees(asin(3/4)))
R["M4"] = dict(C_pF=(30/(2*pi*c))**2/5e-6*1e12)
for k, v in R.items(): print(k, rnd(v) if isinstance(v, dict) else v)
# số phụ cho mục Bẫy
print("BAY Q2 dùng c=3.108 trái:", 3e8/90e6, "| Q3 vân tối thứ 3 nếu nhầm 3i:", 3*i3*1e3)
