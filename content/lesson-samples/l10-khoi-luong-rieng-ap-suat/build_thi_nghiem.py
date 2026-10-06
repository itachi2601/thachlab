"""Sinh 5 file content/thi-nghiem/tn-l10-klr-apsuat-0N.json cho Bài 34 (lesson 79). Số liệu mẫu tính từ chính
mo_hinh của từng file (không gõ tay). Chạy: python3 build_thi_nghiem.py (TRƯỚC build_figs.py — build_figs đọc
bảng của tn-01). Sửa số/chữ ở đây rồi chạy lại, đừng sửa tay JSON (sẽ bị ghi đè).
Có tự kiểm cấu trúc theo cùng quy tắc của thi_nghiem.py (không ghi index.json)."""
import json, math, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parents[1] / "thi-nghiem"
BASE = {"mon": "vat-ly", "lop": 10, "bai": "Bài 34. Khối lượng riêng. Áp suất chất lỏng", "lesson_id": 79,
        "nguon_trong_bai": "content/lesson-samples/l10-khoi-luong-rieng-ap-suat/theory.html"}
G = 10


def r(x, n=2):
    return round(x + 0.0, n)


# 01 — đo khối lượng riêng của nhôm bằng cân + bình chia độ (bảng số liệu có sai số)
RHO_AL = 2.70                       # g/cm³
DO_CHIA_V, DO_CHIA_M = 1.0, 0.1     # cm³, g
# (m đọc trên cân, V đọc trên bình chia độ) — số minh hoạ, lệch quanh m = 2,70·V trong giới hạn đọc ±0,5 cm³
DO = [(21.1, 8), (40.9, 15), (67.2, 25), (99.7, 37)]
rows1 = [[m, V, r(m / V, 2)] for m, V in DO]
for m, V in DO:   # mỗi hàng phải nằm trong giới hạn sai số dụng cụ: |ρ − 2,70|/2,70 ≤ ΔV/V + Δm/m
    assert abs(m / V - RHO_AL) / RHO_AL <= (DO_CHIA_V / 2) / V + (DO_CHIA_M / 2) / m + 1e-9, (m, V)
tn1 = {**BASE, "id": "tn-l10-klr-apsuat-01", "ten": "Đo khối lượng riêng của nhôm bằng cân và bình chia độ",
       "loai": "thi_nghiem", "muc_do": "co_ban",
       "kien_thuc": ["khoi_luong_rieng.rho_bang_m_chia_v", "khoi_luong_rieng.dac_trung_cho_chat"],
       "muc_tieu": "Đo m và V của bốn khối nhôm to nhỏ khác nhau, thấy ρ = m/V gần như không đổi; đọc bảng và nhận ra sai số đọc thể tích lớn nhất ở khối nhỏ.",
       "dung_cu": [{"ten": "Cân điện tử (độ chia 0,1 g)", "so_luong": 1},
                   {"ten": "Bình chia độ 100 cm³ (độ chia 1 cm³)", "so_luong": 1},
                   {"ten": "Khối nhôm to nhỏ khác nhau, buộc chỉ", "so_luong": 4}],
       "cac_buoc": {
           "lam": ["Cân từng khối nhôm, ghi m.",
                   "Đọc mực nước trong bình chia độ, thả khối nhôm chìm hẳn, đọc lại mực nước; V = mực sau − mực trước.",
                   "Tính ρ = m/V cho từng khối."],
           "quan_sat": ["Bốn khối có m và V rất khác nhau nhưng ρ đều gần 2,7 g/cm³.",
                        "Khối nhỏ nhất (8 cm³) cho ρ lệch nhiều nhất so với 2,70 g/cm³."],
           "rut_ra": ["Khối lượng riêng là đặc trưng của chất, không phụ thuộc vật to hay nhỏ.",
                      "Sai số chủ yếu do đọc vạch bình chia độ (±0,5 cm³); V càng nhỏ, sai số tương đối càng lớn."]},
       "tham_so": [
           {"ky_hieu": "rho", "ten": "Khối lượng riêng của nhôm", "don_vi": "g/cm³", "kieu": "co_dinh", "gia_tri": RHO_AL},
           {"ky_hieu": "V", "ten": "Thể tích khối nhôm", "don_vi": "cm³", "kieu": "dieu_chinh", "min": 5, "max": 60, "mac_dinh": 25, "buoc": 1},
           {"ky_hieu": "m", "ten": "Khối lượng đọc trên cân", "don_vi": "g", "kieu": "do_duoc", "sai_so_do": DO_CHIA_M / 2},
           {"ky_hieu": "V_doc", "ten": "Thể tích đọc trên bình chia độ", "don_vi": "cm³", "kieu": "do_duoc", "sai_so_do": DO_CHIA_V / 2},
           {"ky_hieu": "rho_do", "ten": "Khối lượng riêng tính được", "don_vi": "g/cm³", "kieu": "tinh_ra"}],
       "mo_hinh": {"phuong_trinh": ["m = rho·V", "rho_do = m / V_doc",
                                    "sai số tương đối của rho_do ≈ ΔV/V + Δm/m (ΔV = 0,5 cm³, Δm = 0,05 g)"],
                   "gia_thiet": ["nhôm đặc, không có lỗ rỗng", "khối chìm hẳn, không mang theo bọt khí",
                                 "thể tích sợi chỉ bỏ qua"]},
       "so_lieu_mau": {"cot": ["m (g)", "V (cm³)", "ρ = m/V (g/cm³)"], "hang": rows1,
                       "ghi_chu": "Số liệu minh hoạ (chưa phải số đo thật), lệch quanh ρ = 2,70 g/cm³ trong giới hạn đọc ±0,5 cm³ của bình chia độ."},
       "ket_qua_ky_vong": "ρ của mọi khối ≈ 2,7 g/cm³ = 2700 kg/m³; độ lệch giảm dần khi khối to lên.",
       "sai_so_thuong_gap": ["Đọc vạch bình chia độ ±0,5 cm³, nặng nhất ở khối nhỏ.",
                             "Bọt khí bám vào khối làm V đọc lớn hơn thật, ρ ra nhỏ hơn.",
                             "Nhìn vạch không ngang tầm mắt (đọc mép cong của mặt nước)."],
       "hien_tuong_hay_sai": ["Nghĩ khối to thì khối lượng riêng lớn hơn.",
                              "Lấy mực nước sau làm V mà không trừ mực trước.",
                              "Đổi g/cm³ ra kg/m³ bằng cách nhân 1000 nhầm thành chia 1000."],
       "goi_y_mo_phong": {"loai": "bang_so_lieu+do_thi", "y_tuong": "Kéo khối nhôm thả vào bình chia độ, mực nước dâng; đọc vạch có nhiễu ±0,5 cm³; bảng tự thêm hàng m – V – ρ; đồ thị m theo V là đường thẳng qua gốc, hệ số góc = ρ.",
                          "diem_nhan": "Hỏi trước: khối to gấp 4 thì ρ gấp mấy (vẫn 1)."}}

# 02 — bút chì ép giữa hai ngón tay: cùng lực, khác diện tích
F2 = 5.0                                 # N
S_NHON, S_BANG = 0.5e-6, 30e-6           # m² (0,5 mm² và 30 mm²)
rows2 = [[f, r(f / S_NHON / 1e6, 1), r(f / S_BANG / 1e6, 3)] for f in (2.0, 5.0, 8.0)]
tn2 = {**BASE, "id": "tn-l10-klr-apsuat-02", "ten": "Bút chì ép giữa hai ngón tay: cùng áp lực, khác áp suất",
       "loai": "thi_nghiem", "muc_do": "co_ban",
       "kien_thuc": ["ap_suat.p_bang_f_chia_s", "ap_suat.ap_luc_vuong_goc"],
       "muc_tieu": "Cảm nhận cùng một áp lực mà diện tích bị ép nhỏ thì áp suất lớn.",
       "dung_cu": [{"ten": "Bút chì đã gọt, một đầu nhọn một đầu bằng", "so_luong": 1}],
       "cac_buoc": {"lam": ["Kẹp bút chì giữa ngón cái (đầu bằng) và ngón trỏ (đầu nhọn), giữ bút nằm yên.", "Ép nhẹ hai ngón vào nhau."],
                    "quan_sat": ["Ngón chạm đầu nhọn đau hơn hẳn, da lõm sâu hơn."],
                    "rut_ra": ["Bút đứng yên nên hai ngón chịu áp lực bằng nhau.",
                               "Đầu nhọn có diện tích nhỏ nên áp suất lớn hơn nhiều: p = F/S."]},
       "tham_so": [
           {"ky_hieu": "F", "ten": "Áp lực của bút lên mỗi ngón", "don_vi": "N", "kieu": "dieu_chinh", "min": 1, "max": 10, "mac_dinh": F2, "buoc": 0.5},
           {"ky_hieu": "S_nhon", "ten": "Diện tích đầu nhọn", "don_vi": "mm²", "kieu": "dieu_chinh", "min": 0.2, "max": 2, "mac_dinh": 0.5, "buoc": 0.1},
           {"ky_hieu": "S_bang", "ten": "Diện tích đầu bằng", "don_vi": "mm²", "kieu": "co_dinh", "gia_tri": 30},
           {"ky_hieu": "p", "ten": "Áp suất lên ngón tay", "don_vi": "MPa", "kieu": "tinh_ra"}],
       "mo_hinh": {"phuong_trinh": ["p_nhon = F / S_nhon", "p_bang = F / S_bang", "F như nhau ở hai đầu (bút cân bằng)"],
                   "gia_thiet": ["bỏ qua trọng lượng bút", "lực phân bố đều trên mặt tiếp xúc"]},
       "so_lieu_mau": {"cot": ["F (N)", "p đầu nhọn (MPa)", "p đầu bằng (MPa)"], "hang": rows2,
                       "ghi_chu": "Số liệu tính từ mô hình (minh hoạ), S nhọn = 0,5 mm², S bằng = 30 mm²; tỉ số áp suất luôn bằng 60."},
       "ket_qua_ky_vong": "Cùng F, áp suất ở đầu nhọn lớn gấp S_bang/S_nhon = 60 lần.",
       "hien_tuong_hay_sai": ["Nghĩ đầu nhọn đau hơn vì bút đẩy mạnh hơn về phía đó.",
                              "Lẫn áp lực (N) với áp suất (Pa)."],
       "an_toan": "Ép nhẹ, không dùng bút gọt quá nhọn.",
       "goi_y_mo_phong": {"loai": "so_do_luc", "y_tuong": "Bút nằm ngang giữa hai ngón; hai mũi tên F bằng nhau; vùng tiếp xúc tô màu theo áp suất; thanh trượt F và S_nhon.",
                          "diem_nhan": "Hỏi trước: ngón nào chịu lực lớn hơn (bằng nhau)."}}

# 03 — chai nhựa đục lỗ: áp suất tăng theo độ sâu, như nhau theo mọi phương
RHO_N = 1000
H3 = [0.05, 0.10, 0.15]                      # độ sâu ba lỗ dưới mặt nước (m)
rows3 = [[r(h * 100, 0), r(RHO_N * G * h, 0), r(math.sqrt(2 * G * h), 2)] for h in H3]
tn3 = {**BASE, "id": "tn-l10-klr-apsuat-03", "ten": "Chai nhựa đục lỗ: áp suất nước tăng theo độ sâu, như nhau theo mọi phương",
       "loai": "thi_nghiem", "muc_do": "co_ban",
       "kien_thuc": ["ap_suat_chat_long.tang_theo_do_sau", "ap_suat_chat_long.moi_phuong"],
       "muc_tieu": "Thấy tia nước ở lỗ sâu hơn phun mạnh hơn, và các lỗ cùng độ sâu phun mạnh như nhau theo mọi hướng.",
       "dung_cu": [{"ten": "Chai nhựa 1,5 lít", "so_luong": 2}, {"ten": "Đinh nung nóng để đục lỗ", "so_luong": 1},
                   {"ten": "Khay hứng nước", "so_luong": 1}],
       "cac_buoc": {"lam": ["Chai 1: đục 3 lỗ thẳng hàng dọc thân, ở ba độ cao khác nhau.",
                            "Chai 2: đục 4 lỗ quanh thân, cùng một độ cao.",
                            "Bịt lỗ, đổ đầy nước, rồi mở cùng lúc."],
                    "quan_sat": ["Chai 1: tia ở lỗ thấp nhất (sâu nhất) phun mạnh nhất.",
                                 "Chai 2: bốn tia phun mạnh như nhau về bốn phía."],
                    "rut_ra": ["Áp suất nước tăng theo độ sâu.",
                               "Ở cùng độ sâu, nước ép như nhau theo mọi phương."]},
       "tham_so": [
           {"ky_hieu": "h", "ten": "Độ sâu của lỗ dưới mặt nước", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.02, "max": 0.25, "mac_dinh": 0.10, "buoc": 0.01},
           {"ky_hieu": "rho", "ten": "Khối lượng riêng nước", "don_vi": "kg/m³", "kieu": "co_dinh", "gia_tri": RHO_N},
           {"ky_hieu": "p_du", "ten": "Áp suất dư tại lỗ", "don_vi": "Pa", "kieu": "tinh_ra"},
           {"ky_hieu": "v", "ten": "Tốc độ tia nước ra khỏi lỗ", "don_vi": "m/s", "kieu": "tinh_ra"}],
       "mo_hinh": {"phuong_trinh": ["p_du = rho·g·h", "v = √(2·g·h) (định luật Torricelli, ngoài chương trình)"],
                   "gia_thiet": ["lỗ nhỏ so với chai", "mực nước coi như không đổi trong lúc quan sát", "g = 10 m/s²"]},
       "so_lieu_mau": {"cot": ["h (cm)", "p dư (Pa)", "v (m/s)"], "hang": rows3,
                       "ghi_chu": "Số liệu tính từ mô hình (minh hoạ); bài chỉ dùng định tính."},
       "ket_qua_ky_vong": "Lỗ sâu hơn có áp suất dư lớn hơn nên tia ra nhanh hơn; các lỗ cùng độ sâu như nhau.",
       "hien_tuong_hay_sai": ["Nghĩ nước chỉ ép xuống đáy, không ép ngang lên thành chai.",
                              "Nghĩ lỗ trên cao phun mạnh hơn vì 'nước ở trên đầy hơn'."],
       "goi_y_mo_phong": {"loai": "2d_dong_hoc", "y_tuong": "Chai nhìn ngang, kéo vị trí lỗ lên xuống; tia nước là parabol với tốc độ ra √(2gh); mực nước tụt dần.",
                          "diem_nhan": "Cho học sinh đoán lỗ nào phun mạnh nhất trước khi mở nút."}}

# 04 — ống chữ U: nước + dầu hoả không hoà tan
RHO_D = 800
rows4 = []
for hd in (4, 6, 8, 10):                      # cm cột dầu
    hn = RHO_D * hd / RHO_N
    rows4.append([hd, r(hn, 1), r(hd - hn, 1)])
assert all(abs(RHO_D * a - RHO_N * b) < 1e-9 for a, b, _ in rows4)
tn4 = {**BASE, "id": "tn-l10-klr-apsuat-04", "ten": "Ống chữ U chứa nước và dầu: so cột chất lỏng ở hai nhánh",
       "loai": "thi_nghiem", "muc_do": "trung_binh",
       "kien_thuc": ["binh_thong_nhau.cung_muc_ngang_cung_ap_suat", "binh_thong_nhau.rho1h1_bang_rho2h2"],
       "muc_tieu": "Thấy cột dầu nhẹ hơn phải cao hơn cột nước mới cân bằng: ρ₁h₁ = ρ₂h₂ tính từ mức ngang của mặt phân cách.",
       "dung_cu": [{"ten": "Ống nhựa trong suốt uốn chữ U (hoặc ống mềm gắn lên bảng)", "so_luong": 1},
                   {"ten": "Nước, dầu hoả (ρ ≈ 800 kg/m³)", "so_luong": 1}, {"ten": "Thước có vạch cm", "so_luong": 1}],
       "cac_buoc": {"lam": ["Đổ nước vào ống: mực nước hai nhánh ngang nhau.",
                            "Rót từ từ dầu vào nhánh trái tới khi cột dầu cao 10 cm.",
                            "Đo chiều cao cột nước bên phải tính từ mức ngang của mặt phân cách dầu–nước."],
                    "quan_sat": ["Mặt dầu bên trái cao hơn mặt nước bên phải.", "Cột nước bên phải khoảng 8 cm."],
                    "rut_ra": ["Hai điểm cùng mức ngang trong cùng một chất lỏng (nước) có cùng áp suất.",
                               "ρ_dầu·h_dầu = ρ_nước·h_nước: chất lỏng nhẹ hơn cần cột cao hơn."]},
       "tham_so": [
           {"ky_hieu": "h_d", "ten": "Chiều cao cột dầu", "don_vi": "cm", "kieu": "dieu_chinh", "min": 2, "max": 20, "mac_dinh": 10, "buoc": 1},
           {"ky_hieu": "rho_d", "ten": "Khối lượng riêng chất lỏng rót thêm", "don_vi": "kg/m³", "kieu": "dieu_chinh", "min": 600, "max": 950, "mac_dinh": RHO_D, "buoc": 10},
           {"ky_hieu": "rho_n", "ten": "Khối lượng riêng nước", "don_vi": "kg/m³", "kieu": "co_dinh", "gia_tri": RHO_N},
           {"ky_hieu": "h_n", "ten": "Cột nước bên kia, tính từ mức mặt phân cách", "don_vi": "cm", "kieu": "tinh_ra"},
           {"ky_hieu": "chenh", "ten": "Độ chênh hai mặt thoáng", "don_vi": "cm", "kieu": "tinh_ra"}],
       "mo_hinh": {"phuong_trinh": ["p_A = p_a + rho_d·g·h_d", "p_B = p_a + rho_n·g·h_n", "p_A = p_B ⇒ h_n = rho_d·h_d / rho_n",
                                    "chenh = h_d − h_n"],
                   "gia_thiet": ["dầu và nước không hoà tan", "ống đủ hẹp, hai nhánh cùng tiết diện", "chất lỏng đứng yên"]},
       "so_lieu_mau": {"cot": ["h dầu (cm)", "h nước (cm)", "chênh (cm)"], "hang": rows4,
                       "ghi_chu": "Số liệu tính từ mô hình (minh hoạ), ρ dầu = 800 kg/m³. Hình 3 trong bài dùng hàng 10 cm."},
       "ket_qua_ky_vong": "h_nước = 0,8·h_dầu; mặt dầu cao hơn mặt nước 0,2·h_dầu.",
       "hien_tuong_hay_sai": ["Nghĩ hai mặt thoáng vẫn ngang nhau như khi chỉ có nước.",
                              "So áp suất ở hai điểm cùng mức nhưng một điểm nằm trong dầu, một điểm trong nước.",
                              "Đo h_nước từ đáy ống thay vì từ mức mặt phân cách."],
       "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu", "y_tuong": "Ống chữ U nhìn ngang; thanh trượt lượng dầu rót vào; hai mặt thoáng tự cân bằng; đường ngang A–B nhấp nháy.",
                          "diem_nhan": "Hỏi trước: mặt dầu cao hơn, thấp hơn hay ngang mặt nước bên kia."}}

# 05 — bể cá (bài toán mẫu)
A5, B5, H5, HM, PA = 0.60, 0.40, 0.50, 0.20, 1.0e5
rows5 = []
for h in (0.10, 0.30, 0.50):
    rows5.append([r(h * 100, 0), r(RHO_N * G * h, 0), r(PA + RHO_N * G * h, 0)])
tn5 = {**BASE, "id": "tn-l10-klr-apsuat-05", "ten": "Bể cá: áp suất và áp lực của nước lên đáy",
       "loai": "vi_du", "muc_do": "trung_binh",
       "kien_thuc": ["ap_suat_chat_long.p_bang_pa_cong_rho_g_h", "ap_suat_chat_long.ap_luc_day_bang_p_nhan_s",
                     "khoi_luong_rieng.rho_bang_m_chia_v"],
       "muc_tieu": "Tính khối lượng nước, áp suất do nước và áp suất toàn phần ở đáy, áp lực lên đáy, áp suất tại một điểm giữa bể.",
       "dung_cu": [{"ten": "Bể cá thành thẳng đứng, đáy 60 cm × 40 cm", "so_luong": 1}],
       "cac_buoc": {"lam": ["Đổ nước cao 50 cm.", "Tính áp suất tại đáy và tại điểm M cách đáy 20 cm."],
                    "quan_sat": ["Áp suất do nước ở đáy 5000 Pa; tại M (sâu 30 cm) 3000 Pa."],
                    "rut_ra": ["Độ sâu đo từ mặt thoáng xuống, không đo từ đáy lên.",
                               "Thành thẳng đứng: áp lực của nước lên đáy bằng trọng lượng nước (1200 N)."]},
       "tham_so": [
           {"ky_hieu": "h", "ten": "Mực nước", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.1, "max": 0.6, "mac_dinh": H5, "buoc": 0.05},
           {"ky_hieu": "S", "ten": "Diện tích đáy", "don_vi": "m²", "kieu": "co_dinh", "gia_tri": r(A5 * B5, 2)},
           {"ky_hieu": "p_a", "ten": "Áp suất khí quyển", "don_vi": "Pa", "kieu": "co_dinh", "gia_tri": PA},
           {"ky_hieu": "p_nuoc", "ten": "Áp suất do nước ở đáy", "don_vi": "Pa", "kieu": "tinh_ra"},
           {"ky_hieu": "F", "ten": "Áp lực của nước lên đáy", "don_vi": "N", "kieu": "tinh_ra"}],
       "mo_hinh": {"phuong_trinh": ["m = rho·S·h", "p_nuoc = rho·g·h", "p = p_a + rho·g·h", "F = p_nuoc·S"],
                   "gia_thiet": ["nước đứng yên", "g = 10 m/s²", "áp suất khí quyển ép lên mặt nước và dưới đáy bể như nhau"]},
       "so_lieu_mau": {"cot": ["độ sâu (cm)", "p do nước (Pa)", "p toàn phần (Pa)"], "hang": rows5,
                       "ghi_chu": "Tính từ mô hình; hàng 30 cm là điểm M, hàng 50 cm là đáy bể của bài toán mẫu."},
       "ket_qua_ky_vong": "m = 120 kg; p đáy do nước 5000 Pa, toàn phần 1,05·10⁵ Pa; F = 1200 N; p tại M (do nước) 3000 Pa.",
       "hien_tuong_hay_sai": ["Lấy 20 cm (khoảng cách tới đáy) làm độ sâu của M.",
                              "Cộng áp suất khí quyển khi đề chỉ hỏi áp suất do nước.",
                              "Thế h = 50 (cm) vào ρgh."],
       "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu", "y_tuong": "Bể nhìn ngang, kéo điểm M lên xuống; đồng hồ hiện áp suất dư và toàn phần; thanh trượt mực nước.",
                          "diem_nhan": "Hỏi trước: điểm M cách đáy 20 cm thì độ sâu là bao nhiêu."}}

# ---------- tự kiểm như thi_nghiem.py ----------
BAT_BUOC = ["id", "ten", "loai", "muc_do", "mon", "lop", "bai", "kien_thuc", "muc_tieu", "dung_cu", "cac_buoc",
            "tham_so", "mo_hinh", "so_lieu_mau", "ket_qua_ky_vong", "hien_tuong_hay_sai", "goi_y_mo_phong"]
for d in (tn1, tn2, tn3, tn4, tn5):
    for k in BAT_BUOC:
        assert k in d, (d["id"], k)
    assert d["loai"] in {"thi_nghiem", "vi_du"} and d["muc_do"] in {"co_ban", "trung_binh", "nang_cao"}
    assert all(re.fullmatch(r"[a-z0-9_]+\.[a-z0-9_]+", k) for k in d["kien_thuc"]), d["id"]
    assert all(d["cac_buoc"][k] for k in ("lam", "quan_sat", "rut_ra"))
    assert any(t["kieu"] == "dieu_chinh" for t in d["tham_so"])
    kys = [t["ky_hieu"] for t in d["tham_so"]]
    assert len(kys) == len(set(kys)), d["id"]
    for t in d["tham_so"]:
        if t["kieu"] == "dieu_chinh":
            assert t["min"] <= t["mac_dinh"] <= t["max"], (d["id"], t)
        if t["kieu"] == "co_dinh":
            assert "gia_tri" in t
    assert all(len(h) == len(d["so_lieu_mau"]["cot"]) for h in d["so_lieu_mau"]["hang"])
    assert d["goi_y_mo_phong"]["loai"].split("+")[0] in {"2d_dong_hoc", "so_do_luc", "do_thi", "bang_so_lieu"}
    (OUT / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf8")
    print("ghi", d["id"])
print("bảng TN1:", rows1)
print("bảng TN4:", rows4)
