"""Đáp số WP-05 (điện xoay chiều). Chạy: python3 tinh.py  (thư viện chuẩn)
Mọi số trong bai-luyen.md, mini-test.md, ky-thuat.md (kể cả ở mục Bẫy) phải lấy từ đây."""
import math, cmath
from math import pi, sqrt, cos, sin, atan2, degrees, log10, floor
R = {}
def rnd(d): return {a: (round(b, 6) if isinstance(b, float) else b) for a, b in d.items()}
# E1
w = 100*pi; L1 = 0.4/pi; C1 = 250e-6/(3*pi)
ZL, ZC = w*L1, 1/(w*C1); Rr, U = 60, 200
Z = sqrt(Rr**2+(ZL-ZC)**2); I = U/Z
R["E1"] = dict(ZL=ZL, ZC=ZC, Z=Z, I=I, cosphi=Rr/Z, P=I*I*Rr, UR=I*Rr, UL=I*ZL, UC=I*ZC, phi_deg=degrees(atan2(ZL-ZC, Rr)))
# E2
L2, C2, R2, U2 = 0.5, 20e-6, 25, 100
f0 = 1/(2*pi*sqrt(L2*C2)); ZC0 = 1/(2*pi*f0*C2)
R["E2"] = dict(f0=f0, I=U2/R2, P=U2**2/R2, ZL=2*pi*f0*L2, UC=U2/R2*ZC0)
# E3
P3, U3, r3, c3 = 100e3, 10e3, 10, 0.9
dP = P3**2*r3/(U3**2*c3**2)
R["E3"] = dict(dP=dP, H=1-dP/P3, dP2=dP/4, H2=1-dP/4/P3)
# E4
U1, N1, N2 = 220, 1100, 60
U2o = U1*N2/N1; RL = 4; I2 = U2o/RL; P2 = U2o*I2
R["E4"] = dict(U2=U2o, I2=I2, P2=P2, P1=P2/0.9, I1=P2/0.9/U1)
# E5
Rr5, ZL5, ZC5, U5 = 40, 130, 60, 120
Z5 = complex(Rr5, ZL5-ZC5); I5 = U5*sqrt(2)/Z5
R["E5"] = dict(Z=abs(Z5), I0=abs(I5), I=abs(I5)/sqrt(2), phi_i=cmath.phase(I5), phi_u_minus_i=cmath.phase(Z5),
               uL_amp=abs(I5)*ZL5, uL_phase=cmath.phase(I5)+pi/2, uC_amp=abs(I5)*ZC5, uC_phase=cmath.phase(I5)-pi/2)
# E6
r6, ZL6, ZC6, U6 = 10, 70, 30, 120
d6 = ZL6-ZC6
Ptot = lambda Rx: U6**2*(Rx+r6)/((Rx+r6)**2+d6**2)
PR = lambda Rx: U6**2*Rx/((Rx+r6)**2+d6**2)
Rp = d6-r6; RpR = sqrt(r6**2+d6**2)
bestR = max((i/100 for i in range(0, 20001)), key=PR)
R["E6"] = dict(R_Ptot=Rp, Pmax=Ptot(Rp), R_PR=RpR, PRmax=PR(RpR), bestR_num=bestR, formula=U6**2/(2*(RpR+r6)))
# E7
R7, ZL7, U7 = 30, 40, 100
ZC7 = (R7**2+ZL7**2)/ZL7
UCf = lambda zc: U7*zc/sqrt(R7**2+(ZL7-zc)**2)
bz = max((i/100 for i in range(1, 20000)), key=UCf)
R["E7"] = dict(ZC=ZC7, UCmax=U7*sqrt(R7**2+ZL7**2)/R7, num=(bz, UCf(bz)), C_uF=1e6/(100*pi*ZC7))
# E8
R8, ZC8, U8 = 40, 30, 100
ZL8 = (R8**2+ZC8**2)/ZC8
ULf = lambda zl: U8*zl/sqrt(R8**2+(zl-ZC8)**2)
bl = max((i/100 for i in range(1, 30000)), key=ULf)
R["E8"] = dict(ZL=ZL8, ULmax=U8*sqrt(R8**2+ZC8**2)/R8, num=(bl, ULf(bl)), L=ZL8/(100*pi))
# E9
L9, C9, R9, U9 = 0.1, 20e-6, 20, 100
w9 = sqrt(1/(L9*C9) - R9**2/(2*L9**2))
UC9 = lambda ww: U9/(ww*C9)/sqrt(R9**2+(ww*L9-1/(ww*C9))**2)
bw = max((i/10 for i in range(100, 20000)), key=UC9)
R["E9"] = dict(w=w9, f=w9/(2*pi), UCmax=UC9(w9), UCmax_form=U9*2*L9/(R9*sqrt(4*L9*C9-R9**2*C9**2)), num=(bw, UC9(bw)), cond=(R9**2, 2*L9/C9), U_at_res=U9/R9*sqrt(L9/C9))
# E10
Zt = cmath.rect(200/sqrt(2), 0) / cmath.rect(2/sqrt(2), pi/4)   # hiệu dụng
Zx = Zt + 100j
R["E10"] = dict(Ztot=(Zt.real, Zt.imag, abs(Zt)), Zx=(Zx.real, Zx.imag), L=Zx.imag/(100*pi))
# E11
R11, L11, U11 = 30, 0.2, 60
f1, f2 = 40, 90
f0_ = sqrt(f1*f2)
C11 = 1/((2*pi*f0_)**2*L11)
def Zf(f): return sqrt(R11**2 + (2*pi*f*L11 - 1/(2*pi*f*C11))**2)
R["E11"] = dict(f0=f0_, C_uF=C11*1e6, Z1=Zf(f1), Z2=Zf(f2), I=U11/Zf(f1), cosphi=R11/Zf(f1),
                phi1=degrees(atan2(2*pi*f1*L11-1/(2*pi*f1*C11), R11)), phi2=degrees(atan2(2*pi*f2*L11-1/(2*pi*f2*C11), R11)))
# E12
ratio0 = 0.2; ratio1 = ratio0/4
n12 = 100*(1-ratio1)/(1-ratio0)
R["E12"] = dict(n=n12, floor=floor(n12))
# mini-test
ZLm, ZCm, Rm, Um = 50, 10, 30, 100
Zm = sqrt(Rm**2+(ZLm-ZCm)**2); Im = Um/Zm
R["M1"] = dict(Z=Zm, I=Im, P=Im*Im*Rm, cosphi=Rm/Zm, phi=degrees(atan2(ZLm-ZCm, Rm)))
Cm2 = 1/(100*pi*40)
R["M2"] = dict(C_uF=Cm2*1e6, I=120/20, P=120**2/20)
P4, U4, r4, c4 = 500e3, 50e3, 20, 0.8
I4 = P4/(U4*c4)
R["M3"] = dict(I=I4, dP=I4*I4*r4, H=1-I4*I4*r4/P4)
R4, ZC4, U4b = 20, 15, 80
ZL4 = (R4**2+ZC4**2)/ZC4
R["M4"] = dict(ZL=ZL4, ULmax=U4b*sqrt(R4**2+ZC4**2)/R4, L=ZL4/(100*pi))
for k, v in R.items(): print(k, rnd(v))
# --- số phụ dùng trong mục Bẫy ---
print("BAY E4 I1 sai:", 3*60/1100, "| E7 UC tại ZC=40:", 100*40/sqrt(30**2), "| E3 H2 %:", (1-dP/4/P3)*100)
