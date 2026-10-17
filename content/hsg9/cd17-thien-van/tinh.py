"""CĐ17 Thiên văn (bài 178) — mọi số liệu của nguon.md tính ở đây. Chạy: python3 tinh.py"""
from math import pi, degrees, radians, sin, cos, tan, atan, acos, sqrt

# ---- Quy ước số liệu (giá trị làm tròn phổ biến) ----
c = 3.0e5            # km/s
AU = 1.5e8           # km (khoảng cách TB Trái Đất – Mặt Trời)
D_S = 1.39e6         # km, đường kính Mặt Trời
D_E = 12_740         # km, đường kính Trái Đất (R = 6370)
R_E = D_E / 2
D_M = 3_470          # km, đường kính Mặt Trăng
d_M = 384_000        # km, Trái Đất – Mặt Trăng trung bình
d_per, d_apo = 363_000, 405_000   # km, gần nhất / xa nhất
T_tv = 27.32         # ngày, tháng thiên văn (sidereal)
Y = 365.25           # ngày
ly = c * Y * 86400   # km
TILT = 23.5          # độ
P = lambda *a: print(*a)

P("== Năm ánh sáng ==")
P(f"1 năm ánh sáng = {ly:.3e} km = {ly/AU:,.0f} AU")

P("\n== D1 / pha Mặt Trăng ==")
S = 1 / (1 / T_tv - 1 / Y)
P(f"tháng giao hội S = {S:.2f} ngày; 1/4 chu kì = {S/4:.2f} ngày; nửa = {S/2:.2f}")
P(f"Mặt Trăng mọc trễ mỗi ngày ≈ 24 h / S = {24*60/S:.0f} phút")

P("\n== D2 góc trông ==")
def goc(D, d): return degrees(D / d)
aS = goc(D_S, AU)
for ten, dd in [("TB", d_M), ("gần", d_per), ("xa", d_apo)]:
    aM = goc(D_M, dd - R_E)  # nhìn từ mặt đất, điểm dưới Mặt Trăng
    aM0 = goc(D_M, dd)
    P(f"Mặt Trăng {ten}: góc trông (tâm TĐ) {aM0:.3f}°, (mặt đất) {aM:.3f}°; Mặt Trời {aS:.3f}°; tỉ số {aM/aS:.3f}; tỉ lệ diện tích che (nếu nhỏ hơn) {min(1,(aM/aS)**2):.2f}")
P(f"Khoảng cách tối đa để Mặt Trăng che vừa Mặt Trời (từ mặt đất) = D_M*AU/D_S = {D_M*AU/D_S:,.0f} km")
P(f"Đồng xu 2 cm che vừa Mặt Trời khi cách mắt {2*AU/D_S:.0f} cm")

P("\n== D3 bóng Mặt Trăng (nhật thực) ==")
for ten, dd in [("gần", d_per), ("TB", d_M), ("xa", d_apo)]:
    a = AU - dd                         # Mặt Trời – Mặt Trăng (ngày trăng non)
    Lu = a * D_M / (D_S - D_M)          # chiều dài nón bóng tối
    x = dd - R_E                        # Mặt Trăng -> mặt đất (điểm gần nhất)
    du = D_M * (Lu - x) / Lu            # >0: đường kính vùng tối; <0: vùng hình khuyên (antumbra)
    dp = D_M + (D_S + D_M) * x / a      # đường kính vùng nửa tối
    P(f"{ten}: a={a:.4e}; L_toi={Lu:,.0f} km; khoảng tới mặt đất {x:,.0f} km; đường kính vùng {'tối' if du>0 else 'hình khuyên'} {abs(du):.0f} km; nửa tối {dp:,.0f} km")

P("\n== D3b bóng Trái Đất (nguyệt thực) ==")
LuE = AU * D_E / (D_S - D_E)
dUE = D_E * (LuE - d_M) / LuE
dPE = D_E + (D_S + D_E) * d_M / AU
P(f"nón bóng tối TĐ dài {LuE:,.0f} km = {LuE/d_M:.2f} lần d_M")
P(f"đường kính vùng tối tại quỹ đạo Mặt Trăng {dUE:,.0f} km = {dUE/D_M:.2f} D_M; nửa tối {dPE:,.0f} km")
v_rel = 2 * pi * d_M / (S * 86400)    # Mặt Trăng đi qua bóng (bóng đi theo TĐ) => dùng tháng giao hội
v_tv = 2 * pi * d_M / (T_tv * 86400)
P(f"v Mặt Trăng (quanh TĐ) {v_tv:.3f} km/s; so với bóng TĐ {v_rel:.3f} km/s")
t_tp = (dUE - D_M) / v_rel; t_all = (dUE + D_M) / v_rel
P(f"toàn phần dài nhất {t_tp/3600:.2f} h = {t_tp/60:.0f} min; từ lúc chạm tới lúc rời hẳn vùng tối {t_all/3600:.2f} h")

P("\n== D4 tháng giao hội ==")
w_tv, w_E = 360 / T_tv, 360 / Y
P(f"ω Mặt Trăng {w_tv:.3f}°/ngày, ω Trái Đất quanh MT {w_E:.4f}°/ngày, hiệu {w_tv-w_E:.4f}; S={360/(w_tv-w_E):.2f}")
P(f"sau 1 tháng thiên văn, TĐ đã đi {w_E*T_tv:.1f}°, Mặt Trăng cần thêm {w_E*T_tv/(w_tv-w_E):.2f} ngày")
sid = 1 / (1 / 24 + 1 / (Y * 24))   # ngày sao (giờ)
h = int(sid); m = (sid - h) * 60; s = (m - int(m)) * 60
P(f"ngày sao = {sid:.4f} h = {h} h {int(m)} min {s:.0f} s")
# Ví dụ khác cho luyện tập: tháng thiên văn 27,3 -> S
P(f"T_tv=27,3 → S={1/(1/27.3-1/365):.2f}")

P("\n== D5 góc cao Mặt Trời buổi trưa  h = 90 - |phi - delta| ==")
noi = {"Hà Nội": 21.0, "TP.HCM": 10.8, "Huế": 16.5}
for ten, phi in noi.items():
    for ngay, dl in [("xuân/thu phân", 0), ("hạ chí", TILT), ("đông chí", -TILT)]:
        hh = 90 - abs(phi - dl)
        bong = 1 / tan(radians(hh))
        huong = "Bắc" if dl < phi else ("Nam" if dl > phi else "không bóng")
        P(f"  {ten} φ={phi}°, {ngay}: h={hh:.1f}°, bóng cọc 1 m dài {bong:.3f} m, ngả về phía {huong}")
for ten, phi in noi.items():
    H = degrees(acos(-tan(radians(phi)) * tan(radians(TILT))))
    P(f"  {ten} hạ chí: ngày {2*H/15:.2f} h, chênh ngày-đêm {4*H/15-24:.2f} h (chưa kể khúc xạ khí quyển)")

P("\n== D5b Eratosthenes ==")
bong_B, khoang = 0.0875, 556
th = degrees(atan(bong_B))
R = khoang / radians(th)
P(f"BTM: cọc 1 m bóng {bong_B} m → {th:.2f}°; cung {khoang} km → chu vi {khoang*360/th:,.0f} km, R = {R:,.0f} km")
st = 0.1575  # km / stadion (giả thiết)
P(f"Tự luận (lịch sử): 7,2° và 5000 stadia × 157,5 m = {5000*st:.1f} km → chu vi {5000*st*360/7.2:,.0f} km, R = {5000*st/radians(7.2):,.0f} km")
th2 = degrees(atan(0.16))  # tự luận khác
P(f"Bóng 1 m dài 0,16 m → {th2:.2f}°")

P("\n== D6 Hệ Mặt Trời, Ngân Hà ==")
P(f"ánh sáng MT→TĐ {AU/c:.0f} s = {AU/c/60:.2f} min; TĐ→MTrăng {d_M/c:.2f} s")
for ten, a_au in [("Sao Hoả", 1.52), ("Sao Mộc", 5.2), ("Sao Thổ", 9.5), ("Sao Hải Vương", 30)]:
    P(f"  {ten} {a_au} AU: ánh sáng từ MT {a_au*AU/c/60:.1f} min = {a_au*AU/c/3600:.2f} h")
P(f"Sóng vô tuyến TĐ–Sao Hoả gần nhất (0,52 AU) {0.52*AU/c/60:.1f} min, xa nhất (2,52 AU) {2.52*AU/c/60:.1f} min")
vE = 2 * pi * AU / (Y * 86400)
P(f"tốc độ quỹ đạo TĐ {vE:.1f} km/s; quãng đường 1 ngày {2*pi*AU/Y:,.0f} km")
for ten, phi in [("xích đạo", 0)] + list(noi.items()):
    P(f"  tốc độ tự quay tại {ten}: {2*pi*R_E*cos(radians(phi))/86400*1000:.0f} m/s")
P(f"Proxima 4,24 ly = {4.24*ly:.3e} km = {4.24*ly/AU:,.0f} AU; tàu 17 km/s mất {4.24*ly/17/86400/Y:,.0f} năm")
r_gal, T_gal = 26_000, 230e6
v_gal = 2 * pi * r_gal * ly / (T_gal * Y * 86400)
P(f"Mặt Trời quanh tâm Ngân Hà (r=26 000 ly, T=230 triệu năm): v = {v_gal:.0f} km/s; tuổi HMT 4,6 tỉ năm ≈ {4.6e9/T_gal:.0f} vòng")
P(f"Ngân Hà đường kính 100 000 ly = {1e5*ly:.2e} km; ánh sáng băng qua mất 100 000 năm")
k = 1.39e6 * 1e5 / 14   # tỉ lệ: Mặt Trời = quả bóng 14 cm (cm)
P("Mô hình: Mặt Trời quả cầu 14 cm (tỉ lệ 1 : 1e10):")
P(f"  TĐ đường kính {D_E*1e5/1e10*10:.2f} mm cách {AU*1e5/1e10/100:.0f} m; Mặt Trăng {D_M*1e5/1e10*10:.2f} mm cách TĐ {d_M*1e5/1e10:.1f} cm; Hải Vương cách {30*AU*1e5/1e10/100:.0f} m; Proxima cách {4.24*ly*1e5/1e10/1e5:,.0f} km")

P("\n== Tự luận 8: Aristarchus (bóng TĐ = 2,6 lần Mặt Trăng) ==")
kk = 2.6
DM_est = D_E / (1 + kk)   # góc trông MT = Mặt Trăng, độ thu nhỏ nón tối = D_M
P(f"D_M ≈ D_E/(1+k) = {DM_est:,.0f} km (thật {D_M}); góc trông 0,52° → d = {DM_est/radians(0.52):,.0f} km")

P("\n== Luyện tập ==")
P(f"Hà Nội đông chí h = {90-abs(21-(-23.5)):.1f}°; TP.HCM hạ chí h = {90-abs(10.8-23.5):.1f}° (bóng về Nam)")
P(f"ánh sáng MT→TĐ = {AU/c/60:.1f} phút")
