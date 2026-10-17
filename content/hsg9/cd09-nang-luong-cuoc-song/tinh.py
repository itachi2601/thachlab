#!/usr/bin/env python3
"""CĐ09 Năng lượng với cuộc sống (lesson 163) — tính mọi số liệu dùng trong nguon.md.
Chạy: python3 tinh.py  (in kết quả; chép sang nguon.md). Số liệu tự đặt, KHÔNG lấy ví dụ docx."""
import math

KWH = 3.6e6          # J
G = 10               # m/s^2
D_NUOC = 1000        # kg/m^3  -> trọng lượng riêng d = 10D = 1e4 N/m^3
Q_THAN = 2.7e7       # J/kg (đề cho)
K_THAN = 2.5         # kg CO2 / kg than (đề cho)
NGAY = 86400
NAM = 365 * NGAY


def p(title, **kw):
    print(f"  {title}: " + ", ".join(f"{k}={v:.6g}" for k, v in kw.items()))


print("=" * 70)
print("BÀI TẬP MẪU")
print("=" * 70)

# ---------- D1 Chuỗi hiệu suất nhà máy nhiệt điện ----------
print("D1 nhiệt điện than, chuỗi 3 cấp")
H1, H2, H3 = 0.90, 0.42, 0.96
H = H1 * H2 * H3
Pd = 330e6
Pnl = Pd / H
Php = Pnl - Pd
p("H tổng", H=H)
p("công suất nhiên liệu (MW)", Pnl=Pnl / 1e6, Php=Php / 1e6)
loss1 = Pnl * (1 - H1)
loss2 = Pnl * H1 * (1 - H2)
loss3 = Pnl * H1 * H2 * (1 - H3)
p("hao phí từng cấp (MW)", lo_hoi=loss1 / 1e6, tuabin=loss2 / 1e6, may_phat=loss3 / 1e6,
  tong=(loss1 + loss2 + loss3) / 1e6)
ms = Pnl / Q_THAN
p("than", kg_s=ms, tan_gio=ms * 3600 / 1e3, tan_ngay=ms * NGAY / 1e3)
p("CO2 (tấn/ngày)", co2=ms * NGAY * K_THAN / 1e3)
H2b = 0.45
Hb = H1 * H2b * H3
ms_b = Pd / Hb / Q_THAN
p("nâng H2 lên 0,45", H_moi=Hb, than_tan_ngay=ms_b * NGAY / 1e3,
  tiet_kiem_tan_ngay=(ms - ms_b) * NGAY / 1e3, tiet_kiem_pct=(1 - ms_b / ms) * 100)
A_D1_ngay_MWh = Pd * 24 / 1e6
p("điện năng 1 ngày (MWh)", A=A_D1_ngay_MWh)

# ---------- D2 Thuỷ điện ----------
print("D2 thuỷ điện")
h, L = 95, 250
Ht, Hm = 0.92, 0.96
Htd = Ht * Hm
Pn = 10 * D_NUOC * L * h
p("mùa mưa", H=Htd, Pn_MW=Pn / 1e6, Pd_MW=Htd * Pn / 1e6)
Pd_mua = Htd * Pn
h2, L2 = 80, 160
Pd_kho = Htd * 10 * D_NUOC * L2 * h2
p("mùa khô h=80, L=160", Pd_MW=Pd_kho / 1e6, ti_le=Pd_kho / Pd_mua)
L_can = 150e6 / (Htd * 1e4 * 80)
p("L cần cho 150 MW khi h=80", L=L_can)
A_mua = Pd_mua * NGAY
than_tk = A_mua / H / Q_THAN       # thay cho nhà máy D1 (H = 0,36288)
p("1 ngày mùa mưa", A_MWh=A_mua / KWH / 1e3, V_m3=L * NGAY,
  than_thay_tan=than_tk / 1e3, co2_tranh_tan=than_tk * K_THAN / 1e3)

# ---------- D3 Pin Mặt Trời cho một gia đình ----------
print("D3 pin Mặt Trời gia đình")
A_thang, ngay = 375, 30
A_ngay = A_thang / ngay
S_tam, H_pin, I, t_d, H_bt = 2.0, 0.20, 1000, 4.0, 0.95
P_tam = H_pin * I * S_tam                    # W đỉnh mỗi tấm (chưa biến tần)
A_tam = P_tam * t_d * H_bt / 1000            # kWh/ngày mỗi tấm sau biến tần
n = A_ngay / A_tam
n_tam = math.ceil(n)
p("mỗi tấm", P_dinh_W=P_tam, A_kWh_ngay=A_tam)
p("số tấm", A_ngay=A_ngay, n=n, n_lam_tron=n_tam, P_he_kWp=n_tam * P_tam / 1000)
n_quen_bt = A_ngay / (P_tam * t_d / 1000)
p("bẫy quên biến tần", n=n_quen_bt, lam_tron=math.ceil(n_quen_bt))
n_12h = A_ngay / (P_tam * 12 * H_bt / 1000)
p("bẫy lấy 12 h trời sáng", n=n_12h)
S_mai = 14
n_mai = int(S_mai // S_tam)
A_mai = n_mai * A_tam
p("mái 14 m2", n_tam=n_mai, A_ngay=A_mai, thieu_ngay=A_ngay - A_mai, thieu_thang=(A_ngay - A_mai) * 30)
gia = 2800
von = 67.5e6   # 9 tấm × 7,5 triệu
tk_thang = A_thang * gia
p("hoàn vốn 9 tấm, 67,5 triệu, giá 2800", tiet_kiem_thang=tk_thang, thang=von / tk_thang, nam=von / tk_thang / 12)

# ---------- D4 Điện gió ----------
print("D4 điện gió")
d_q, Dkk, v_dm, P_dm = 80, 1.2, 12, 2.0e6
S = math.pi * d_q ** 2 / 4
Pgio = 0.5 * Dkk * S * v_dm ** 3
p("tại 12 m/s", S=S, Pgio_MW=Pgio / 1e6, H=P_dm / Pgio)


def P_tb(v):
    if v < 3 or v > 25:
        return 0.0
    if v >= v_dm:
        return P_dm
    return P_dm * (v / v_dm) ** 3


bang = [(4, 2), (8, 6), (6, 9), (4, 12), (2, 15)]   # (giờ, v m/s)
A = 0
for gio, v in bang:
    A += gio * P_tb(v)
    p(f"{gio} h ở {v} m/s", P_MW=P_tb(v) / 1e6, A_MWh=gio * P_tb(v) / 1e6)
A_MWh = A / 1e6
p("tổng ngày", A_MWh=A_MWh, he_so_cong_suat=A_MWh / (P_dm / 1e6 * 24))
p("bẫy 15 m/s dùng v^3", P_MW=P_dm * (15 / 12) ** 3 / 1e6)
n_tb = A_D1_ngay_MWh / A_MWh
p("số tuabin thay nhà máy D1", n=n_tb, lam_tron=math.ceil(n_tb))

# ---------- D5 Xe máy xăng vs xe máy điện ----------
print("D5 xe xăng vs xe điện (40 km/ngày)")
F, s = 70, 40e3
A_ich = F * s
H_xang, q_xang, D_xang, k_xang, gia_xang = 0.15, 4.6e7, 0.70, 3.2, 24000
Qx = A_ich / H_xang
mx = Qx / q_xang
Vx = mx / D_xang
p("xe xăng", A_ich=A_ich, Q=Qx, m_kg=mx, V_L=Vx, tien=Vx * gia_xang, co2_kg=mx * k_xang)
H_dc, H_sac, gia_dien, ke = 0.80, 0.90, 3000, 0.65
H_xd = H_dc * H_sac
A_luoi = A_ich / H_xd
p("xe điện", H=H_xd, A_J=A_luoi, A_kWh=A_luoi / KWH, tien=A_luoi / KWH * gia_dien,
  co2_kg=A_luoi / KWH * ke)
p("tỉ số", tien_xang_tren_dien=(Vx * gia_xang) / (A_luoi / KWH * gia_dien),
  co2_xang_tren_dien=(mx * k_xang) / (A_luoi / KWH * ke))
# nếu toàn bộ điện từ nhà máy than D1 (bỏ qua truyền tải)
H_chuoi = H * H_xd
m_than = A_ich / H_chuoi / Q_THAN
p("điện từ nhà máy than D1", H_than_den_banh=H_chuoi, than_kg=m_than, co2_kg=m_than * K_THAN,
  ke_tuong_duong=K_THAN / (H * Q_THAN / KWH))
p("1 năm (365 ngày)", tien_xang=Vx * gia_xang * 365, tien_dien=A_luoi / KWH * gia_dien * 365,
  chenh=(Vx * gia_xang - A_luoi / KWH * gia_dien) * 365)

print("=" * 70)
print("TỰ LUẬN")
print("=" * 70)
# TL2 Mặt Trời -> Trái Đất
I0, R = 1360, 6.4e6
P_td = I0 * math.pi * R ** 2
P_nguoi = 2.0e13
p("TL2", P_td=P_td, ti_so=P_td / P_nguoi, giay_cho_1_nam=NAM / (P_td / P_nguoi),
  phut=NAM / (P_td / P_nguoi) / 60, sai_4piR2=I0 * 4 * math.pi * R ** 2,
  hap_thu_tb_Wm2=0.7 * I0 / 4)
# TL3 thay đèn ở trường -> than ở nhà máy
dA = 120 * (0.040 - 0.018) * 8 * 22
m3 = dA * KWH / 0.36 / Q_THAN
p("TL3", dA_kWh_thang=dA, than_kg=m3, co2_kg=m3 * K_THAN, tien=dA * 2900, dA_nam_9thang=dA * 9)
# TL4 thuỷ điện tích năng
V, hh, Hb_, Hp_ = 3.6e6, 300, 0.85, 0.88
Wt = 1e4 * V * hh
p("TL4", Wt_J=Wt, Wt_MWh=Wt / KWH / 1e3, A_bom_MWh=Wt / Hb_ / KWH / 1e3,
  A_phat_MWh=Wt * Hp_ / KWH / 1e3, H_chu_trinh=Hb_ * Hp_,
  P_phat_6h_MW=Wt * Hp_ / (6 * 3600) / 1e6, L_6h=V / (6 * 3600))
# TL5 hạt nhân vs than
P5, H5 = 1e9, 0.33
E_nl = P5 * NAM / H5
q_U = 8.2e10   # J/g U-235 (đề cho)
mU = E_nl / q_U
m_than5 = P5 * NAM / 0.36 / Q_THAN
p("TL5", A_dien_J=P5 * NAM, E_nl=E_nl, U_kg=mU / 1e3, than_trieu_tan=m_than5 / 1e9,
  co2_trieu_tan=m_than5 * K_THAN / 1e9, ti_le_khoi_luong=m_than5 / (mU / 1e3),
  q_ratio=q_U * 1e3 / Q_THAN)
# TL6 hệ lai gió – Mặt Trời – acquy – diesel cho đảo
E_can = 200 * 5.0
Pdm6, vdm6 = 100, 12
Pw = lambda v: Pdm6 * (v / vdm6) ** 3
A_gio = 10 * Pw(6) + 14 * Pw(9)
G_can = E_can / (0.6 + 0.4 * 0.85)
a_m2 = 0.19 * 1000 * 4.5 * 0.95 / 1000
A_pin = G_can - A_gio
p("TL6", E_can=E_can, P6=Pw(6), P9=Pw(9), A_gio=A_gio, G_can=G_can, A_pin=A_pin,
  kWh_m2=a_m2, S_m2=A_pin / a_m2)
Qd = E_can * KWH / 0.35
md = Qd / 4.4e7
p("TL6 diesel 1 ngày", m_kg=md, V_L=md / 0.84, co2_kg=md * 3.2)

print("=" * 70)
print("LUYỆN TẬP")
print("=" * 70)
p("I.2 chuỗi", H=0.90 * 0.40 * 0.95, tb_cong=(0.9 + 0.4 + 0.95) / 3)
p("I.3 gió 10->8", con_lai=(8 / 10) ** 3, giam_pct=(1 - (8 / 10) ** 3) * 100, bay_binh_phuong=(1 - 0.64) * 100)
Pn1 = 1e4 * 100 * 60
p("II.1 thuỷ điện", Pn_MW=Pn1 / 1e6, Pd_MW=0.85 * Pn1 / 1e6, V_1h=100 * 3600)
Q1t = 1000 * Q_THAN
p("II.2 1 tấn than", Q=Q1t, kWh_khong_H=Q1t / KWH, kWh_H35=Q1t * 0.35 / KWH, co2_tan=K_THAN)
a_tam3 = 0.2 * 1000 * 1.8 * 4.5 / 1000
p("III.1 pin", kWh_tam=a_tam3, n=9 / a_tam3, lam_tron=math.ceil(9 / a_tam3))
p("III.2 nhiệt điện", Pnl_MW=450 / 0.375, tan_gio=450e6 / 0.375 * 3600 / 2.4e7 / 1e3)
p("U-235 so với than (1 g vs kg)", kg_than_tuong_duong_1g_U=8.2e10 / Q_THAN)
