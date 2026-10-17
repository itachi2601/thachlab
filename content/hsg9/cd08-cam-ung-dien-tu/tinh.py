#!/usr/bin/env python3
"""CĐ08 Cảm ứng điện từ & dòng xoay chiều (bài 152) — tính mọi số liệu dùng trong nguon.md.
Chạy: python3 tinh.py   (chỉ in, không ghi file)
Quy ước: R là điện trở TỔNG cả hai dây; P là công suất ở ĐẦU đường dây; U là hiệu điện thế ở đầu đường dây.
"""
from math import sqrt, pi

RHO_CU, RHO_AL = 1.7e-8, 2.8e-8      # Ω·m
D_CU, D_AL = 8900, 2700              # kg/m³


def line(P, U, R):
    I = P / U
    Php = I * I * R
    return I, Php, 1 - Php / P, I * R, U - I * R


def show(title, **kw):
    print(f"\n== {title}")
    for k, v in kw.items():
        print(f"   {k:<28} = {v:.6g}" if isinstance(v, float) else f"   {k:<28} = {v}")


# ---------------- BÀI TẬP MẪU ----------------
# D2 máy phát: f = n.p
p = 6
n_s = 50 / p
show("D2a thuỷ điện p=6, f=50 Hz", n_vong_s=n_s, n_vong_phut=n_s * 60)
show("D2b rôto chậm còn 480 vòng/phút", f=480 / 60 * p)
v, d_num, p_dyn = 18 / 3.6, 0.02, 2   # xe 18 km/h, núm dinamô đường kính 2 cm, 4 cực = 2 cặp
n_dyn = v / (pi * d_num)
show("D2c dinamô xe đạp", v_m_s=v, n_num_vong_s=n_dyn, f=n_dyn * p_dyn,
     f_neu_nham_p4=n_dyn * 4, so_lan_doi_chieu_moi_s_luoi50=100)

# D3 máy biến áp hạ áp
N1, U1, U2 = 1650, 220, 12
N2 = N1 * U2 / U1
P_tai = 2 * 24
show("D3 máy biến áp 220->12 V", N2=N2, I2=P_tai / U2, I1_li_tuong=P_tai / U1,
     I1_H94=P_tai / (0.94 * U1), U_quan_nguoc=U1 * N1 / N2, N_dau_6V=N1 * 6 / U1)

# D4 hao phí cơ bản
P, U, R = 600e3, 15e3, 24
I, Php, H, dU, Utt = line(P, U, R)
show("D4a P=600 kW, U=15 kV, R=24 Ω", I=I, Php_W=Php, H=H, dU=dU, Utt=Utt)
I, Php2, H2, _, _ = line(P, 60e3, R)
show("D4b U=60 kV (k=4)", I=I, Php_W=Php2, H=H2, giam_lan=Php / Php2)
Umin = sqrt(P * P * R / (0.01 * P))
show("D4c Php<=1%P", Umin_V=Umin, k_min=Umin / U)
show("D4d thay vì tăng U 4 lần, giảm R", R_can=R / 16, tiet_dien_gap=16.0)

# D5 dây nhôm + chọn tỉ số máy tăng áp + tiết diện
l, S, P, U0 = 20e3, 70e-6, 2e6, 6e3
R = RHO_AL * 2 * l / S
I, Php, H, dU, Utt = line(P, U0, R)
show("D5a dây nhôm 2x20 km, S=70 mm², truyền thẳng 6 kV", R=R, I=I, Php_W=Php, ty_le_hp=Php / P, dU=dU, Utt=Utt)
Umin = sqrt(P * R / 0.02)
show("D5b Php<=2%", Umin_V=Umin, k=Umin / U0, N2_khi_N1_300=300 * Umin / U0)
I, Php, H, dU, Utt = line(P, Umin, R)
show("D5c ở 40 kV", I=I, Php_W=Php, H=H, dU=dU, Utt=Utt, ti_so_ha_ap_ve_400V=Utt / 400)
Rmax = 0.02 * P * 22e3 ** 2 / P ** 2
Smin = RHO_AL * 2 * l / Rmax
show("D5d giữ 22 kV, chọn S", Rmax=Rmax, Smin_mm2=Smin * 1e6, gap_70=Smin * 1e6 / 70)

# D6 công suất nơi tiêu thụ không đổi
R, U, Ptt = 10, 10e3, 1.6e6
# R I^2 - U I + Ptt = 0
disc = U * U - 4 * R * Ptt
Ia, Ib = (U - sqrt(disc)) / (2 * R), (U + sqrt(disc)) / (2 * R)
for Ix in (Ia, Ib):
    show(f"D6a nghiệm I={Ix:g} A", P_dau=U * Ix, Php=R * Ix * Ix, H=1 - R * Ix / U, dU=R * Ix, Utt=U - R * Ix)
H1, H2 = 0.8, 0.95
k = sqrt(H1 * (1 - H1) / (H2 * (1 - H2)))
P2 = Ptt / H2
I2 = sqrt((P2 - Ptt) / R)
show("D6b Ptt không đổi, H 80%->95%", k=k, U2=U * k, P2=P2, I2=I2, U2_kiem=P2 / I2)
show("D6c bẫy: coi P đầu dây không đổi", k_sai=sqrt((1 - H1) / (1 - H2)))

# ---------------- TỰ LUẬN ----------------
show("TL3 biến áp nhiều đầu ra N1=1100, 220 V",
     **{f"N_{u}V": 1100 * u / 220 for u in (3, 6, 9, 12)},
     noi_60_30_cung_chieu_V=220 * 90 / 1100, noi_60_30_nguoc_chieu_V=220 * 30 / 1100)
P1max = 220 * 0.5
show("TL4 cầu chì sơ cấp 0,5 A, đèn 11 V-20 W", N2=2000 * 11 / 220, P1max=P1max, so_den=int(P1max // 20),
     I2_5den=5 * 20 / 11, I1_5den=5 * 20 / 220)
I, Php, H, _, _ = line(300e3, 6e3, 8)
I_, Php_, H_, _, _ = line(300e3, 30e3, 8)
show("TL5 P=300 kW, R=8 Ω", I_6kV=I, Php_6kV=Php, A_ngay_kWh=Php * 24 / 1e3,
     Php_30kV=Php_, A_ngay_30kV=Php_ * 24 / 1e3, tiet_kiem_kWh=(Php - Php_) * 24 / 1e3)
show("TL6 đồng vs nhôm cùng khối lượng, cùng chiều dài", R_Al_chia_R_Cu=(RHO_AL * D_AL) / (RHO_CU * D_CU),
     S_Al_chia_S_Cu=D_CU / D_AL)
dA, t, U1v, U2v = 216e3, 24, 6000, 5700
Php = dA / t
I = Php / (U1v - U2v)
R = (U1v - U2v) / I
P = U1v * I
show("TL7 hai vôn kế + hai công tơ", Php_W=Php, I=I, R=R, P=P, H=1 - Php / P,
     U_can_cho_1pc=sqrt(P * R / 0.01), k=sqrt(P * R / 0.01) / U1v)
P, U0, kt, R = 200e3, 1e3, 10, 20
I, Php, H, dU, Utt = line(P, U0 * kt, R)
show("TL8 hệ hai máy biến áp", U_tang=U0 * kt, I=I, Php=Php, H=H, dU=dU, U_vao_ha_ap=Utt,
     ti_so_ha_ap=Utt / 220, P_tieu_thu=P - Php, I_neu_khong_tang_ap=P / U0, dU_neu_khong=P / U0 * R)

# ---------------- LUYỆN TẬP ----------------
show("LT I.3", U2=220 * 60 / 1200)
show("LT II.1 p=4, 750 vòng/phút", f=750 / 60 * 4, doi_chieu_moi_s=2 * 750 / 60 * 4, n_neu_2cap=50 / 2 * 60)
I, Php, H, dU, Utt = line(500e3, 25e3, 50)
show("LT II.2 P=500 kW, U=25 kV, R=50 Ω", I=I, Php=Php, H=H, dU=dU, Utt=Utt, Php_50kV=line(500e3, 50e3, 50)[1])
show("LT III.1", U2=220 * 48 / 880, I2=2.5, I1=(220 * 48 / 880) * 2.5 / 220)
show("LT III.2 P=1 MW, R=10 Ω, Php<=4%", Umin_kV=sqrt(1e6 * 10 / 0.04) / 1e3)

# ---------------- KIỂM LẠI SỐ DOCX (mục Sai sót) ----------------
I = 11e3 / 4400
show("docx G2: ΔU bị bỏ qua", I=I, dU=I * 4, U_vao_ha_ap=4400 - I * 4, U3_dung=(4400 - I * 4) / 20)
