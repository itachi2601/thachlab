"""Ghi 3 file thí nghiệm của bài 'Sóng điện từ' (Vật lí 11, lesson 30) vào content/thi-nghiem/.
Số liệu mẫu TÍNH bằng script từ mô hình khai trong file (không gõ tay).
Chạy: python3 build_thi_nghiem.py (build_figs.py tự gọi trước khi dựng bảng trong bài)."""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parents[1] / "thi-nghiem"
CHUNG = {"mon": "vat-ly", "lop": 11, "bai": "Bài 11. Sóng điện từ", "lesson_id": 30,
         "nguon_trong_bai": "content/lesson-samples/l11-song-dien-tu/theory.html"}

# ---------- 01: điện thoại trong hộp giấy và hộp kim loại (định tính) ----------
tn1 = dict(CHUNG, **{
    "id": "tn-l11-songdientu-01",
    "ten": "Gọi vào điện thoại đặt trong hộp giấy và trong hộp kim loại",
    "loai": "thi_nghiem", "muc_do": "co_ban",
    "kien_thuc": ["songdientu.phan_xa_kim_loai", "songdientu.truyen_qua_vat_lieu"],
    "muc_tieu": "Thấy sóng điện từ đi qua giấy, bìa nhưng bị vỏ kim loại kín chặn lại (phản xạ) — vì sao thang máy hay mất sóng.",
    "dung_cu": [
        {"ten": "Điện thoại đang bật, có sóng", "so_luong": 2},
        {"ten": "Hộp giấy bìa có nắp", "so_luong": 1},
        {"ten": "Hộp bánh quy bằng sắt có nắp kín (hoặc 3 lớp giấy bạc bọc kín)", "so_luong": 1},
    ],
    "cac_buoc": {
        "lam": ["Đặt điện thoại A vào hộp giấy, đậy nắp; dùng điện thoại B gọi vào A.",
                "Chuyển A sang hộp sắt, đậy kín nắp; gọi lại."],
        "quan_sat": ["Hộp giấy: A vẫn đổ chuông.",
                     "Hộp sắt kín: thường nghe báo 'thuê bao tạm thời không liên lạc được'; hở nắp một khe thì có thể lại có sóng."],
        "rut_ra": ["Sóng điện từ đi qua giấy, bìa; vỏ kim loại kín phản xạ gần hết sóng.",
                   "Cabin thang máy bằng kim loại làm điện thoại mất sóng vì cùng lí do."],
    },
    "tham_so": [
        {"ky_hieu": "vat_lieu", "ten": "Vật liệu vỏ hộp (0 = giấy, 1 = kim loại)", "don_vi": "", "kieu": "dieu_chinh", "min": 0, "max": 1, "mac_dinh": 0, "buoc": 1},
        {"ky_hieu": "khe", "ten": "Bề rộng khe hở ở nắp", "don_vi": "cm", "kieu": "dieu_chinh", "min": 0, "max": 10, "mac_dinh": 0, "buoc": 1},
        {"ky_hieu": "co_song", "ten": "Điện thoại trong hộp nhận được cuộc gọi", "don_vi": "", "kieu": "tinh_ra"},
    ],
    "mo_hinh": {
        "phuong_trinh": ["vỏ giấy: sóng đi qua, co_song = 1",
                         "vỏ kim loại kín (khe = 0): sóng bị phản xạ, co_song = 0",
                         "khe hở cỡ vài cm trở lên (so với λ ≈ 16–33 cm của sóng điện thoại): một phần sóng lọt vào, co_song có thể = 1"],
        "gia_thiet": ["mô hình định tính; không tính cường độ", "trạm phát gần, sóng ngoài hộp đủ mạnh"],
    },
    "so_lieu_mau": {
        "cot": ["Vỏ hộp", "Khe hở", "Có đổ chuông?"],
        "hang": [["giấy bìa", "0 cm", "có"], ["hộp sắt", "0 cm", "không"], ["hộp sắt", "khoảng 5 cm", "có thể có"]],
        "ghi_chu": "Kết quả định tính điển hình; điện thoại đời mới, trạm phát rất gần có thể vẫn bắt được sóng yếu qua mép nắp.",
    },
    "ket_qua_ky_vong": "Hộp giấy: có sóng. Hộp sắt đậy kín: mất sóng.",
    "hien_tuong_hay_sai": ["Tưởng sóng điện thoại đi theo không khí nên hộp kín nào cũng chặn (hộp giấy kín vẫn có sóng).",
                           "Tưởng mất sóng trong thang máy vì 'ở trên cao' hoặc 'thiếu không khí'."],
    "an_toan": ["Không bọc giấy bạc quanh điện thoại đang sạc."],
    "goi_y_mo_phong": {"loai": "2d_dong_hoc", "dieu_khien": ["vat_lieu", "khe"],
                       "dau_ra": ["các vệt sóng từ trạm tới hộp", "vệt sóng dội lại ở vỏ kim loại", "biểu tượng cột sóng của điện thoại"],
                       "hinh_trong_bai": "Hình 1",
                       "y_tuong": "Hỏi trước: hộp giấy kín và hộp sắt kín, hộp nào chặn sóng? Rồi cho chạy."},
})

# ---------- 02: đo bước sóng vi sóng bằng lò vi sóng + thanh sô-cô-la (có bảng) ----------
C = 3.0e8
F = 2.45e9                     # Hz, tần số ghi trên lò
LAM = C / F * 100              # cm, 12,245
D_THAT = LAM / 2               # cm, 6,122
# Sai số đọc tâm vệt chảy (vệt rộng ~1 cm) — độ lệch minh hoạ cộng vào D_THAT, làm tròn theo độ chia thước 0,1 cm.
LECH = [-0.12, 0.08, -0.22, 0.18, -0.02]
D_DO = [round(D_THAT + e, 1) for e in LECH]
assert D_DO == [6.0, 6.2, 5.9, 6.3, 6.1], D_DO
assert all(abs(d - D_THAT) <= 0.3 for d in D_DO)
D_TB = sum(D_DO) / len(D_DO)
LAM_DO = 2 * D_TB
C_DO = LAM_DO / 100 * F
assert abs(D_TB - 6.10) < 1e-9 and abs(C_DO - 2.989e8) < 1e5
tn2 = dict(CHUNG, **{
    "id": "tn-l11-songdientu-02",
    "ten": "Đo bước sóng vi sóng trong lò vi sóng bằng thanh sô-cô-la, suy ra tốc độ sóng điện từ",
    "loai": "thi_nghiem", "muc_do": "trung_binh",
    "kien_thuc": ["songdientu.lambda_bang_c_chia_f", "songdientu.toc_do_c", "do_luong.sai_so_ngau_nhien"],
    "muc_tieu": "Đo khoảng cách hai vệt chảy liền nhau (bằng λ/2) trên thanh sô-cô-la, 5 lần; tính λ và c = λf với f = 2,45 GHz ghi trên lò; nhận xét sai số.",
    "dung_cu": [
        {"ten": "Lò vi sóng gia đình (ghi 2 450 MHz)", "so_luong": 1},
        {"ten": "Thanh sô-cô-la dài, đặt trên đĩa sứ", "so_luong": 5},
        {"ten": "Thước kẻ (độ chia 1 mm)", "so_luong": 1},
    ],
    "cac_buoc": {
        "lam": ["Nhấc đĩa xoay ra, úp một đĩa sứ lên trục để thức ăn KHÔNG quay.",
                "Đặt thanh sô-cô-la lên đĩa, quay khoảng 15–20 giây đến khi thấy vài vệt bắt đầu chảy.",
                "Đo khoảng cách d giữa tâm hai vệt chảy liền nhau.",
                "Làm 5 lần, mỗi lần một thanh mới."],
        "quan_sat": ["Sô-cô-la chảy thành từng vệt cách đều nhau, giữa các vệt vẫn còn cứng.",
                     "Năm lần đo d lệch nhau vài milimét."],
        "rut_ra": ["λ = 2·d_tb = " + f"{LAM_DO:.1f}".replace(".", ",") + " cm; c = λf ≈ " + f"{C_DO/1e8:.2f}".replace(".", ",") + "·10⁸ m/s, khớp 3·10⁸ m/s trong phạm vi sai số.",
                   "Sai số chủ yếu do vệt chảy rộng, khó xác định tâm; tần số thật của lò có thể lệch chút ít quanh 2,45 GHz."],
    },
    "tham_so": [
        {"ky_hieu": "f", "ten": "Tần số vi sóng của lò", "don_vi": "GHz", "kieu": "dieu_chinh", "min": 2.40, "max": 2.50, "mac_dinh": 2.45, "buoc": 0.01},
        {"ky_hieu": "c", "ten": "Tốc độ sóng điện từ trong không khí", "don_vi": "m/s", "kieu": "co_dinh", "gia_tri": C},
        {"ky_hieu": "d", "ten": "Khoảng cách tâm hai vệt chảy liền nhau", "don_vi": "cm", "kieu": "do_duoc", "sai_so_do": 0.3},
        {"ky_hieu": "c_do", "ten": "Tốc độ tính từ số đo", "don_vi": "m/s", "kieu": "tinh_ra"},
    ],
    "mo_hinh": {
        "phuong_trinh": ["λ = c/f", "trong lò có sóng dừng: chỗ nóng nhất (bụng) cách nhau d = λ/2", "c_do = 2·d_tb·f"],
        "gia_thiet": ["đĩa không xoay", "coi tốc độ vi sóng trong không khí bằng c", "sai số đọc tâm vệt ±0,3 cm"],
    },
    "so_lieu_mau": {
        "cot": ["Lần đo", "d (cm)"],
        "hang": [[i + 1, d] for i, d in enumerate(D_DO)],
        "ghi_chu": (f"Số minh hoạ, không phải số đo thật: d thật = λ/2 = {D_THAT:.3f} cm với f = 2,45 GHz, cộng độ lệch đọc tâm vệt ≤ 0,22 cm; "
                    f"trung bình {D_TB:.2f} cm, λ = {LAM_DO:.1f} cm, c ≈ {C_DO:.3e} m/s."),
    },
    "ket_qua_ky_vong": f"d_tb = {D_TB:.2f} cm; λ ≈ {LAM_DO:.1f} cm; c ≈ {C_DO/1e8:.2f}·10⁸ m/s (lệch {abs(C_DO-C)/C*100:.1f} % so với 3·10⁸ m/s).",
    "hien_tuong_hay_sai": ["Tính λ = d (quên hai vệt liền nhau chỉ cách λ/2), ra c nhỏ đi một nửa.",
                           "Để nguyên cm khi nhân với Hz, ra c lớn gấp 100 lần.",
                           "Nhầm vi sóng (sóng điện từ) với siêu âm (sóng âm)."],
    "sai_so_thuong_gap": ["Vệt chảy rộng khoảng 1 cm, khó xác định tâm.",
                          "Quay quá lâu thì các vệt loang vào nhau.",
                          "Tần số thật của lò có thể lệch chút ít quanh 2,45 GHz."],
    "an_toan": ["Không cho kim loại vào lò; không quay khi lò trống.", "Sô-cô-la nóng chảy có thể gây bỏng nhẹ."],
    "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu", "dieu_khien": ["f"],
                       "dau_ra": ["thanh sô-cô-la với các vệt chảy cách λ/2", "bảng 5 lần đo có nhiễu đọc tâm vệt"],
                       "hinh_trong_bai": "Hình 3",
                       "y_tuong": "Cho học sinh tự đặt thước đo d trên ảnh thanh sô-cô-la, ghi 5 lần, tính c.",
                       "diem_nhan": "Hỏi trước: λ bằng d hay 2d?"},
})

# ---------- 03: nhìn đèn điều khiển hồng ngoại qua camera điện thoại (định tính) ----------
tn3 = dict(CHUNG, **{
    "id": "tn-l11-songdientu-03",
    "ten": "Nhìn đèn hồng ngoại của điều khiển ti vi qua camera điện thoại",
    "loai": "thi_nghiem", "muc_do": "co_ban",
    "kien_thuc": ["songdientu.thang_song", "songdientu.hong_ngoai", "songdientu.anh_sang_nhin_thay_dai_hep"],
    "muc_tieu": "Thấy có bức xạ mắt không thấy nhưng cảm biến camera ghi được: hồng ngoại cùng bản chất với ánh sáng, chỉ khác bước sóng.",
    "dung_cu": [
        {"ten": "Điều khiển ti vi (đèn hồng ngoại ở đầu)", "so_luong": 1},
        {"ten": "Điện thoại có camera (nên dùng camera trước)", "so_luong": 1},
    ],
    "cac_buoc": {
        "lam": ["Chĩa đầu điều khiển vào mắt (cách xa), bấm giữ một nút.",
                "Chĩa đầu điều khiển vào camera điện thoại đang mở, bấm giữ cùng nút đó."],
        "quan_sat": ["Mắt thường: đầu điều khiển không sáng.",
                     "Trên màn hình điện thoại: đầu điều khiển nhấp nháy ánh tím trắng."],
        "rut_ra": ["Điều khiển phát hồng ngoại: sóng điện từ có λ dài hơn ánh sáng đỏ, mắt không thấy.",
                   "Ánh sáng nhìn thấy chỉ là một dải hẹp của thang sóng điện từ."],
    },
    "tham_so": [
        {"ky_hieu": "λ", "ten": "Bước sóng bức xạ của đèn", "don_vi": "nm", "kieu": "dieu_chinh", "min": 380, "max": 1100, "mac_dinh": 940, "buoc": 10},
        {"ky_hieu": "r", "ten": "Khoảng cách điều khiển – camera", "don_vi": "cm", "kieu": "dieu_chinh", "min": 5, "max": 300, "mac_dinh": 30, "buoc": 5},
        {"ky_hieu": "f", "ten": "Tần số tương ứng", "don_vi": "Hz", "kieu": "tinh_ra"},
    ],
    "mo_hinh": {
        "phuong_trinh": ["f = c/λ = 3·10⁸ / 940·10⁻⁹ ≈ 3,2·10¹⁴ Hz",
                         "mắt thấy 380 nm ≤ λ ≤ 760 nm; cảm biến camera nhạy tới khoảng 1 000 nm"],
        "gia_thiet": ["camera không có bộ lọc hồng ngoại quá mạnh (camera trước thường dễ thấy hơn)"],
    },
    "so_lieu_mau": {
        "cot": ["Bức xạ", "λ (nm)", "Mắt thấy?"],
        "hang": [["ánh sáng đỏ", 700, "có"], ["đèn điều khiển", 940, "không"], ["ánh sáng tím", 400, "có"]],
        "ghi_chu": "λ = 940 nm là giá trị điển hình của đèn LED hồng ngoại trong điều khiển ti vi.",
    },
    "ket_qua_ky_vong": "Mắt không thấy gì, camera thấy đầu điều khiển nhấp nháy.",
    "hien_tuong_hay_sai": ["Tưởng điều khiển ti vi dùng sóng âm hoặc sóng vô tuyến.",
                           "Tưởng ánh sáng nhìn thấy chiếm phần lớn thang sóng điện từ."],
    "goi_y_mo_phong": {"loai": "2d_dong_hoc", "dieu_khien": ["λ"],
                       "dau_ra": ["mắt thấy / không thấy", "camera thấy / không thấy"],
                       "hinh_trong_bai": "Hình 4",
                       "y_tuong": "Thanh trượt λ chạy dọc thang sóng; hai đèn báo 'mắt' và 'camera' sáng theo vùng nhạy."},
})

for d in (tn1, tn2, tn3):
    (OUT / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf8")
    print("ghi", d["id"])
