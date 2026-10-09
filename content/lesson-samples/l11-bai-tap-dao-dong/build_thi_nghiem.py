"""Ghi 3 file thí nghiệm của Bài 4. Bài tập về dao động điều hoà (VL11, lesson 23) vào content/thi-nghiem/.
Số liệu mẫu TÍNH bằng script từ mô hình khai trong file + sai số dụng cụ; assert khớp với bảng trong theory.src.html.
Chạy: python3 build_thi_nghiem.py"""
import json, math, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parents[1] / "thi-nghiem"
G = 9.8
CHUNG = {"mon": "vat-ly", "lop": 11, "bai": "Bài 4. Bài tập về dao động điều hoà", "lesson_id": 23,
         "nguon_trong_bai": "content/lesson-samples/l11-bai-tap-dao-dong/theory.html"}
SRC = (HERE / "theory.src.html").read_text(encoding="utf8")

# ---------- 01: đo chu kì chùm chìa khoá bằng đồng hồ điện thoại (10 dao động × 5 lần)
L = 0.36
T_MO_HINH = 2 * math.pi * math.sqrt(L / G)                 # 1,2043 s
LECH_TAY = [0.08, -0.11, 0.14, -0.15, -0.01]               # sai lệch phản xạ tay (s), |.| ≤ 0,2 s
T10 = [round(10 * T_MO_HINH + d, 2) for d in LECH_TAY]
assert T10 == [12.12, 11.93, 12.18, 11.89, 12.03], T10
for v in T10:
    assert f"<td>{str(v).replace('.', ',')}</td>" in SRC
tb = sum(T10) / len(T10)
T_TB = tb / 10
dT = (max(T10) - min(T10)) / 2 / 10
assert abs(tb - 12.03) < 1e-9 and abs(T_TB - 1.203) < 1e-9 and abs(dT - 0.0145) < 1e-9
assert abs(T_TB - T_MO_HINH) < dT                          # lệch so với mô hình nằm trong sai số
W = 2 * math.pi / T_TB
assert abs(W - 5.2229) < 1e-3 and abs(5.0 * W - 26.11) < 0.01
tn1 = dict(CHUNG, **{
    "id": "tn-l11-baitapdaodong-01",
    "ten": "Đo chu kì chùm chìa khoá treo dây bằng đồng hồ điện thoại",
    "loai": "thi_nghiem", "muc_do": "co_ban",
    "kien_thuc": ["daodong.chu_ki_tan_so", "daodong.van_toc_cuc_dai", "do_luong.sai_so_ngau_nhien"],
    "muc_tieu": "Đo T bằng cách bấm giờ 10 dao động, lặp 5 lần; ghi kết quả T ± ΔT, rồi tính ω = 2π/T và v_max = Aω.",
    "dung_cu": [
        {"ten": "Chùm chìa khoá", "so_luong": 1},
        {"ten": "Sợi dây mảnh dài 36 cm", "so_luong": 1},
        {"ten": "Điện thoại có đồng hồ bấm giờ", "so_luong": 1},
        {"ten": "Thước kẻ (đo độ kéo lệch)", "so_luong": 1},
    ],
    "cac_buoc": {
        "lam": ["Buộc chùm chìa khoá vào dây dài 36 cm, treo lên mép bàn.",
                "Kéo lệch A = 5,0 cm rồi thả nhẹ.",
                "Bấm giờ 10 dao động (t10), lặp 5 lần."],
        "quan_sat": ["t10 (s): 12,12; 11,93; 12,18; 11,89; 12,03."],
        "rut_ra": ["t10 trung bình 12,03 s, T = 1,203 s.",
                   "Sai số t10 = (12,18 − 11,89)/2 ≈ 0,15 s nên ΔT ≈ 0,015 s ≈ 0,02 s: T = 1,20 ± 0,02 s.",
                   "ω = 2π/T ≈ 5,22 rad/s; v_max = Aω ≈ 26 cm/s."],
    },
    "tham_so": [
        {"ky_hieu": "L", "ten": "Chiều dài dây", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.2, "max": 1.0, "mac_dinh": L, "buoc": 0.02},
        {"ky_hieu": "A", "ten": "Độ kéo lệch (biên độ)", "don_vi": "cm", "kieu": "dieu_chinh", "min": 2, "max": 8, "mac_dinh": 5, "buoc": 1},
        {"ky_hieu": "g", "ten": "Gia tốc trọng trường", "don_vi": "m/s²", "kieu": "co_dinh", "gia_tri": G},
        {"ky_hieu": "t10", "ten": "Thời gian 10 dao động", "don_vi": "s", "kieu": "do_duoc", "sai_so_do": 0.2},
        {"ky_hieu": "T", "ten": "Chu kì", "don_vi": "s", "kieu": "tinh_ra"},
        {"ky_hieu": "v_max", "ten": "Tốc độ cực đại", "don_vi": "cm/s", "kieu": "tinh_ra"},
    ],
    "mo_hinh": {
        "phuong_trinh": ["T = 2π·√(L/g)", "t10 = 10·T + sai lệch bấm tay", "ω = 2π/T", "v_max = A·ω"],
        "gia_thiet": ["góc lệch nhỏ (5 cm trên dây 36 cm, khoảng 8°)", "bỏ qua cản không khí trong 10 dao động",
                      "sai lệch bấm tay ngẫu nhiên, cỡ 0,1–0,2 s mỗi lần"],
    },
    "so_lieu_mau": {
        "cot": ["Lần", "t10 (s)"],
        "hang": [[i + 1, v] for i, v in enumerate(T10)],
        "ghi_chu": "Số minh hoạ: 10·T tính từ T = 2π√(L/g) cộng sai lệch bấm tay giả định, không phải số đo thật.",
    },
    "ket_qua_ky_vong": "T = 1,20 ± 0,02 s (mô hình 1,204 s); ω ≈ 5,22 rad/s; v_max ≈ 26 cm/s với A = 5,0 cm.",
    "sai_so_thuong_gap": ["Phản xạ tay khi bấm bắt đầu/kết thúc: 0,1–0,2 s mỗi lần.",
                          "Đếm nhầm số dao động (đếm 'một' ngay lúc thả)."],
    "hien_tuong_hay_sai": ["Chia giá trị t10 cho 10 nhưng quên chia sai số cho 10.",
                           "Bấm từ biên này sang biên kia rồi gọi là một chu kì.",
                           "Lấy khoảng chênh lớn nhất làm sai số mà quên chia đôi."],
    "goi_y_mo_phong": {
        "loai": "2d_dong_hoc+bang_so_lieu",
        "dieu_khien": ["L", "A"],
        "dau_ra": ["con lắc đung đưa", "đồng hồ bấm giờ có độ trễ ngẫu nhiên", "bảng t10 và T ± ΔT"],
        "y_tuong": "Cho học sinh bấm nút bắt đầu/dừng thật; so sai số khi đo 1 dao động và 10 dao động.",
    },
})

# ---------- 02: vật tự vẽ đồ thị x–t lên băng giấy
V_GIAY, A_CM, T_S = 20.0, 3.0, 0.80
DINH_DAY, DINH_DINH = 2 * A_CM, V_GIAY * T_S
assert DINH_DAY == 6.0 and abs(DINH_DINH - 16.0) < 1e-9
tn2 = dict(CHUNG, **{
    "id": "tn-l11-baitapdaodong-02",
    "ten": "Vật dao động tự vẽ đồ thị li độ – thời gian lên băng giấy",
    "loai": "vi_du", "muc_do": "co_ban",
    "kien_thuc": ["daodong.do_thi_li_do_thoi_gian", "daodong.bien_do", "daodong.chu_ki_tan_so"],
    "muc_tieu": "Đọc biên độ và chu kì từ đồ thị thật: đỉnh–đáy = 2A, hai đỉnh liền kề cách nhau đúng một chu kì.",
    "dung_cu": [
        {"ten": "Lò xo + quả nặng treo trên giá", "so_luong": 1},
        {"ten": "Bút dạ gắn vào quả nặng", "so_luong": 1},
        {"ten": "Băng giấy dài", "so_luong": 1},
        {"ten": "Thước", "so_luong": 1},
    ],
    "cac_buoc": {
        "lam": ["Gắn bút dạ vào quả nặng treo lò xo, đầu bút chạm băng giấy.",
                "Cho quả nặng dao động; một bạn kéo đều băng giấy ngang qua đầu bút, tốc độ 20 cm/s."],
        "quan_sat": ["Nét bút là đường hình sin.", "Đỉnh cao nhất cách đáy thấp nhất 6,0 cm; hai đỉnh liền kề cách nhau 16,0 cm."],
        "rut_ra": ["A = 6,0/2 = 3,0 cm.", "T = 16/20 = 0,80 s."],
    },
    "tham_so": [
        {"ky_hieu": "A", "ten": "Biên độ", "don_vi": "cm", "kieu": "dieu_chinh", "min": 1, "max": 5, "mac_dinh": A_CM, "buoc": 0.5},
        {"ky_hieu": "T", "ten": "Chu kì", "don_vi": "s", "kieu": "dieu_chinh", "min": 0.4, "max": 2, "mac_dinh": T_S, "buoc": 0.1},
        {"ky_hieu": "u", "ten": "Tốc độ kéo giấy", "don_vi": "cm/s", "kieu": "dieu_chinh", "min": 5, "max": 40, "mac_dinh": V_GIAY, "buoc": 5},
        {"ky_hieu": "h", "ten": "Khoảng đỉnh–đáy theo phương dao động", "don_vi": "cm", "kieu": "do_duoc", "sai_so_do": 0.1},
        {"ky_hieu": "d", "ten": "Khoảng giữa hai đỉnh liền kề trên giấy", "don_vi": "cm", "kieu": "do_duoc", "sai_so_do": 0.1},
    ],
    "mo_hinh": {
        "phuong_trinh": ["x = A·cos(2π·t/T)", "vị trí dọc giấy s = u·t", "h = 2A", "d = u·T"],
        "gia_thiet": ["kéo giấy đều", "bỏ qua ma sát đầu bút làm giảm biên độ"],
    },
    "so_lieu_mau": {
        "cot": ["u (cm/s)", "h (cm)", "d (cm)", "A (cm)", "T (s)"],
        "hang": [[V_GIAY, DINH_DAY, DINH_DINH, A_CM, T_S]],
        "ghi_chu": "Số minh hoạ tính từ mô hình, không phải số đo thật.",
    },
    "ket_qua_ky_vong": "A = 3,0 cm; T = 0,80 s.",
    "hien_tuong_hay_sai": ["Đọc khoảng đỉnh–đáy là A (thực ra là 2A).",
                           "Lấy khoảng từ đỉnh tới đáy liền kề làm chu kì (thực ra là T/2)."],
    "goi_y_mo_phong": {
        "loai": "2d_dong_hoc+do_thi",
        "dieu_khien": ["A", "T", "u"],
        "dau_ra": ["vật dao động", "băng giấy chạy, nét bút vẽ dần đồ thị"],
        "hinh_trong_bai": "Hình 2",
        "y_tuong": "Tăng tốc độ kéo giấy thì đồ thị giãn ngang nhưng A và T không đổi.",
    },
})

# ---------- 03: quay chậm 240 khung/s, đếm khung O → A/2 và A/2 → A
T3, A3, FPS = 0.80, 4.0, 240
OM = 2 * math.pi / T3
k1 = math.asin(0.5) / OM * FPS                 # O → A/2 : T/12
k2 = (math.pi / 2 - math.asin(0.5)) / OM * FPS # A/2 → A : T/6
assert abs(k1 - 16) < 1e-9 and abs(k2 - 32) < 1e-9
DEM = [(16, 32), (17, 31), (16, 33)]           # ±1 khung do chọn khung bắt đầu/kết thúc
for a, c in DEM:
    assert abs(a - k1) <= 1 + 1e-9 and abs(c - k2) <= 1 + 1e-9
    assert f"<td>{a} khung</td><td>{c} khung</td>" in SRC
tn3 = dict(CHUNG, **{
    "id": "tn-l11-baitapdaodong-03",
    "ten": "Quay chậm con lắc lò xo: nửa quãng đường không phải nửa thời gian",
    "loai": "thi_nghiem", "muc_do": "trung_binh",
    "kien_thuc": ["daodong.vong_tron_luong_giac", "daodong.thoi_gian_giua_hai_vi_tri"],
    "muc_tieu": "Đếm khung hình quay chậm để thấy O → A/2 mất T/12, A/2 → A mất T/6.",
    "dung_cu": [
        {"ten": "Con lắc lò xo nằm ngang trên ray (T ≈ 0,80 s)", "so_luong": 1},
        {"ten": "Băng dính màu đánh dấu O, 2 cm, 4 cm", "so_luong": 1},
        {"ten": "Điện thoại quay chậm 240 khung/s", "so_luong": 1},
    ],
    "cac_buoc": {
        "lam": ["Dán băng dính ở O, ở 2 cm và 4 cm. Kéo vật ra 4,0 cm rồi thả.",
                "Quay chậm 240 khung/s; xem lại, đếm số khung vật đi O → 2 cm và 2 → 4 cm. Làm 3 lần."],
        "quan_sat": ["O → 2 cm: 16, 17, 16 khung.", "2 → 4 cm: 32, 31, 33 khung."],
        "rut_ra": ["Nửa đường gần O mất khoảng 16 khung ≈ 0,067 s = T/12.",
                   "Nửa đường gần biên mất khoảng 32 khung ≈ 0,133 s = T/6.",
                   "Nửa quãng đường không phải nửa thời gian: gần biên vật đi chậm."],
    },
    "tham_so": [
        {"ky_hieu": "T", "ten": "Chu kì", "don_vi": "s", "kieu": "dieu_chinh", "min": 0.4, "max": 2, "mac_dinh": T3, "buoc": 0.1},
        {"ky_hieu": "A", "ten": "Biên độ", "don_vi": "cm", "kieu": "dieu_chinh", "min": 2, "max": 8, "mac_dinh": A3, "buoc": 1},
        {"ky_hieu": "fps", "ten": "Số khung hình mỗi giây", "don_vi": "khung/s", "kieu": "co_dinh", "gia_tri": FPS},
        {"ky_hieu": "n1", "ten": "Số khung O → A/2", "don_vi": "khung", "kieu": "do_duoc", "sai_so_do": 1},
        {"ky_hieu": "n2", "ten": "Số khung A/2 → A", "don_vi": "khung", "kieu": "do_duoc", "sai_so_do": 1},
    ],
    "mo_hinh": {
        "phuong_trinh": ["x = A·sin(ωt) tính từ lúc qua O", "ω = 2π/T",
                         "t(O→A/2) = arcsin(1/2)/ω = T/12", "t(A/2→A) = (π/2 − π/6)/ω = T/6", "n = t·fps"],
        "gia_thiet": ["bỏ qua ma sát trên ray", "sai số ±1 khung do chọn khung bắt đầu/kết thúc"],
    },
    "so_lieu_mau": {
        "cot": ["Lần", "O → 2 cm (khung)", "2 → 4 cm (khung)"],
        "hang": [[i + 1, a, c] for i, (a, c) in enumerate(DEM)],
        "ghi_chu": "Số minh hoạ: mô hình cho 16 và 32 khung, cộng/trừ 1 khung do chọn khung; không phải số đo thật.",
    },
    "ket_qua_ky_vong": "O → 2 cm ≈ 16 khung (T/12); 2 → 4 cm ≈ 32 khung (T/6).",
    "hien_tuong_hay_sai": ["Nghĩ nửa quãng đường O → A mất nửa thời gian T/4, tức T/8.",
                           "Nhầm T/6 là thời gian O → A/2."],
    "goi_y_mo_phong": {
        "loai": "2d_dong_hoc+do_thi",
        "dieu_khien": ["T", "A"],
        "dau_ra": ["vật chạy chậm từng khung", "bộ đếm khung ở mỗi mốc", "điểm M quay trên vòng tròn pha"],
        "hinh_trong_bai": "Hình 3",
        "y_tuong": "Chạy song song vật trên ray và điểm M trên vòng tròn; tô màu cung 30° và 60°.",
    },
})

for tn in (tn1, tn2, tn3):
    p = OUT / f"{tn['id']}.json"
    p.write_text(json.dumps(tn, ensure_ascii=False, indent=1), encoding="utf8")
    assert f'data-exp="{tn["id"]}"' in SRC, tn["id"]
    print("ghi", p.name)
