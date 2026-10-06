#!/usr/bin/env python3
"""Sinh 3 file thí nghiệm/ví dụ của bài 'Độ dịch chuyển và quãng đường đi được' (lesson 49) vào content/thi-nghiem/.
Số liệu mẫu tính từ chính mo_hinh; cột "đo" (minh hoạ) được kiểm nằm trong sai số dụng cụ.
Chạy: python3 build_thi_nghiem.py   (build_figs.py đọc lại so_lieu_mau của tn-l10-dd-qd-01 để dựng bảng trong bài)"""
import json, math, pathlib

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parents[1] / "thi-nghiem"
B = "Bài 4. Độ dịch chuyển và quãng đường đi được"
SRC = "content/lesson-samples/l10-do-dich-chuyen-quang-duong/theory.html"
base = {"mon": "vat-ly", "lop": 10, "bai": B, "lesson_id": 49, "nguon_trong_bai": SRC}

# ---- 01: ray uốn — mô hình
r = 10
model = [("thẳng 30 cm", 30, 30), ("nửa vòng tròn r = 10 cm", math.pi * r, 2 * r * math.sin(math.pi / 2)),
         ("chữ L 30 cm + 40 cm", 70, math.hypot(30, 40)), ("trọn vòng tròn r = 10 cm", 2 * math.pi * r, 2 * r * math.sin(math.pi))]
S_DO = [30.2, 31.9, 70.6, 63.5]      # sợi chỉ, sai số ±1 cm (minh hoạ)
D_DO = [30.0, 20.1, 49.9, 0.0]       # thước, sai số ±0,2 cm (minh hoạ)
hang = [[n, round(s, 1), sd, round(abs(d), 1), dd] for (n, s, d), sd, dd in zip(model, S_DO, D_DO)]
for h, (n, s, d) in zip(hang, model):
    assert abs(h[2] - s) <= 1.0 + 1e-9 and abs(h[4] - abs(d)) <= 0.2 + 1e-9, h
    assert h[4] <= h[2], h            # d <= s
t1 = dict(base, **{
    "id": "tn-l10-dd-qd-01",
    "ten": "Xe đồ chơi chạy trên ray uốn: đo quãng đường bằng sợi chỉ, đo độ dịch chuyển bằng thước",
    "loai": "thi_nghiem", "muc_do": "co_ban",
    "kien_thuc": ["dong_hoc.quang_duong", "dong_hoc.do_dich_chuyen", "dong_hoc.so_sanh_d_s"],
    "muc_tieu": "Đo s và độ lớn d cho bốn hình dạng đường ray, thấy d = s chỉ khi đường thẳng không đổi chiều, còn lại d < s; đường khép kín cho d = 0.",
    "dung_cu": [{"ten": "Xe đồ chơi chạy pin", "so_luong": 1}, {"ten": "Đường ray nhựa uốn được, dài 80 cm", "so_luong": 1},
                {"ten": "Sợi chỉ không dãn", "so_luong": 1}, {"ten": "Thước thẳng 1 m, vạch chia 1 mm", "so_luong": 1},
                {"ten": "Băng dính đánh dấu điểm đầu, điểm cuối", "so_luong": 1}],
    "cac_buoc": {"lam": ["Uốn ray lần lượt thành 4 hình: thẳng 30 cm, nửa vòng tròn bán kính 10 cm, chữ L (30 cm rồi rẽ vuông góc 40 cm), trọn vòng tròn bán kính 10 cm.",
                         "Mỗi hình cho xe chạy một lần từ đầu tới cuối ray, dán băng dính ở điểm xuất phát và điểm dừng.",
                         "Đặt sợi chỉ sát dọc ray, kéo thẳng rồi đo bằng thước: được s. Đo đoạn thẳng nối điểm đầu – điểm cuối: được độ lớn d."],
                 "quan_sat": ["s đo: " + "; ".join(f"{x:.1f}".replace(".", ",") for x in S_DO) + " cm. d đo: "
                              + "; ".join(f"{x:.1f}".replace(".", ",") for x in D_DO) + " cm (số liệu minh hoạ).",
                              "Chỉ hình ray thẳng cho d ≈ s; vòng tròn kín cho d = 0 dù xe chạy hơn 60 cm."],
                 "rut_ra": ["Độ lớn độ dịch chuyển không lớn hơn quãng đường: d ≤ s.",
                            "d = s khi vật chuyển động thẳng, không đổi chiều."]},
    "tham_so": [{"ky_hieu": "r", "ten": "Bán kính ray tròn", "don_vi": "cm", "kieu": "dieu_chinh", "min": 5, "max": 20, "mac_dinh": 10, "buoc": 1},
                {"ky_hieu": "theta", "ten": "Góc cung tròn xe chạy", "don_vi": "rad", "kieu": "dieu_chinh", "min": 0, "max": 6.2832, "mac_dinh": 3.1416},
                {"ky_hieu": "s", "ten": "Quãng đường đo bằng sợi chỉ", "don_vi": "cm", "kieu": "do_duoc", "sai_so_do": 1.0},
                {"ky_hieu": "d", "ten": "Độ lớn độ dịch chuyển đo bằng thước", "don_vi": "cm", "kieu": "do_duoc", "sai_so_do": 0.2}],
    "mo_hinh": {"phuong_trinh": ["thẳng dài L: s = L, d = L", "cung tròn góc theta (rad): s = r·theta, d = 2r·sin(theta/2)",
                                 "chữ L hai cạnh a, b vuông góc: s = a + b, d = √(a² + b²)"],
                "gia_thiet": ["xe coi là chất điểm", "ray nằm trên mặt phẳng ngang", "s đo bằng chỉ lệch ≤ 1 cm, d đo bằng thước lệch ≤ 0,2 cm"]},
    "so_lieu_mau": {"cot": ["Hình ray", "s mô hình (cm)", "s đo (cm)", "d mô hình (cm)", "d đo (cm)"], "hang": hang,
                    "ghi_chu": "Số liệu minh hoạ: cột mô hình tính từ phương trình; cột đo lệch không quá sai số dụng cụ (sợi chỉ ±1 cm, thước ±0,2 cm)."},
    "ket_qua_ky_vong": "d = s ở ray thẳng; d < s ở ba hình còn lại; d = 0 ở vòng kín. Cột s đo lệch mô hình nhiều hơn cột d vì sợi chỉ khó đặt sát ray cong.",
    "hien_tuong_hay_sai": ["Tưởng d của vòng kín là chu vi 62,8 cm.", "Tưởng d của nửa vòng là nửa chu vi 31,4 cm thay vì đường kính 20 cm.",
                           "Cộng 30 + 40 = 70 cm làm độ dịch chuyển của hình chữ L."],
    "sai_so_thuong_gap": "Sợi chỉ không bám sát ray ở chỗ cong (thường làm s đo lớn hơn), băng dính đánh dấu lệch điểm dừng thật của xe.",
    "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu",
                       "y_tuong": "Kéo thanh trượt góc cung từ 0 đến 2π: xe chạy trên cung tròn, vệt cam là s, mũi tên xanh lá nối đầu–cuối là d; bảng cập nhật s, d.",
                       "diem_nhan": "Cho học sinh đoán d ở nửa vòng và trọn vòng trước khi kéo; d lớn nhất ở nửa vòng rồi giảm về 0."}})

# ---- 02: xe điều khiển trên trục X
def cnc(x1, xq, x2):
    return [x1, xq, x2, abs(xq - x1) + abs(x2 - xq), x2 - x1]
t2 = dict(base, **{
    "id": "tn-l10-dd-qd-02",
    "ten": "Xe điều khiển từ xa chạy tới rồi lùi trên trục X: d = x₂ − x₁ có dấu",
    "loai": "vi_du", "muc_do": "co_ban",
    "kien_thuc": ["dong_hoc.he_quy_chieu", "dong_hoc.do_dich_chuyen"],
    "muc_tieu": "Đọc toạ độ xe trên trục X dọc thước để tính quãng đường và độ dịch chuyển có dấu khi xe đổi chiều.",
    "dung_cu": [{"ten": "Xe đồ chơi điều khiển từ xa (chạy dọc thước dài)", "so_luong": 1}, {"ten": "Thước dán trên sàn, vạch chia cm", "so_luong": 1}],
    "cac_buoc": {"lam": ["Gốc O là đầu thước, trục X chiều dương sang phải.", "Xe đi từ x₁ = 20 cm tới x = 80 cm, rồi lùi về x₂ = 50 cm."],
                 "quan_sat": ["Vạch thước chỉ lần lượt 20 → 80 → 50 cm."],
                 "rut_ra": ["s = 60 + 30 = 90 cm.", "d = x₂ − x₁ = 30 cm, dương vì điểm cuối nằm bên phải điểm đầu."]},
    "tham_so": [{"ky_hieu": "x1", "ten": "Toạ độ đầu", "don_vi": "cm", "kieu": "dieu_chinh", "min": 0, "max": 100, "mac_dinh": 20},
                {"ky_hieu": "xq", "ten": "Toạ độ chỗ đổi chiều", "don_vi": "cm", "kieu": "dieu_chinh", "min": 0, "max": 100, "mac_dinh": 80},
                {"ky_hieu": "x2", "ten": "Toạ độ cuối", "don_vi": "cm", "kieu": "dieu_chinh", "min": 0, "max": 100, "mac_dinh": 50},
                {"ky_hieu": "s", "ten": "Quãng đường", "don_vi": "cm", "kieu": "tinh_ra"},
                {"ky_hieu": "d", "ten": "Độ dịch chuyển", "don_vi": "cm", "kieu": "tinh_ra"}],
    "mo_hinh": {"phuong_trinh": ["s = |xq − x1| + |x2 − xq|", "d = x2 − x1"],
                "gia_thiet": ["xe chỉ chạy dọc trục X", "đổi chiều đúng một lần tại xq"]},
    "so_lieu_mau": {"cot": ["x1 (cm)", "xq (cm)", "x2 (cm)", "s (cm)", "d (cm)"],
                    "hang": [cnc(20, 80, 50), cnc(70, 90, 40), cnc(10, 60, 60)],
                    "ghi_chu": "Hàng 1 là ví dụ trong bài (Hình 2), hàng 2 là câu tự kiểm tra (d âm), hàng 3 không đổi chiều nên d = s."},
    "ket_qua_ky_vong": "Khi đổi chiều, s > |d|; d mang dấu theo chiều dương đã chọn.",
    "hien_tuong_hay_sai": ["Lấy s làm d.", "Bỏ dấu âm của d khi điểm cuối ở bên trái điểm đầu.", "Tính d bằng đoạn lùi cuối cùng."],
    "goi_y_mo_phong": {"loai": "2d_dong_hoc+do_thi",
                       "y_tuong": "Kéo ba thanh x1, xq, x2; vệt cam phía trên trục là đường đi, mũi tên xanh lá dưới trục là d.",
                       "diem_nhan": "Đổi chiều dương của trục để thấy d đổi dấu, s không đổi."}})
assert t2["so_lieu_mau"]["hang"][0] == [20, 80, 50, 90, 30] and t2["so_lieu_mau"]["hang"][1][3:] == [70, -30]

# ---- 03: vòng sân băng (số liệu minh hoạ)
C, T1 = 60, 20
t3 = dict(base, **{
    "id": "tn-l10-dd-qd-03",
    "ten": "Một vòng sân băng: quãng đường 60 m, độ dịch chuyển bằng 0",
    "loai": "vi_du", "muc_do": "co_ban",
    "kien_thuc": ["dong_hoc.so_sanh_d_s", "dong_hoc.toc_do_trung_binh"],
    "muc_tieu": "Thấy quãng đường cộng dồn theo đường đi, còn độ dịch chuyển chỉ phụ thuộc điểm đầu và điểm cuối; vòng kín cho d = 0.",
    "dung_cu": [{"ten": "Sân băng (hoặc sân trường) có vòng chạy kín", "so_luong": 1}, {"ten": "Đồng hồ thể thao đo quãng đường", "so_luong": 1}],
    "cac_buoc": {"lam": ["Xuất phát ở cửa vào, trượt sát rào chắn đúng một vòng, dừng lại ở cửa vào. Bấm giờ."],
                 "quan_sat": ["Đồng hồ báo khoảng 60 m (minh hoạ), mất 20 s; điểm dừng trùng điểm xuất phát."],
                 "rut_ra": ["s = 60 m; d = 0.", "Tốc độ trung bình = s/t = 3 m/s, khác 0 dù d = 0."]},
    "tham_so": [{"ky_hieu": "C", "ten": "Chu vi vòng trượt", "don_vi": "m", "kieu": "dieu_chinh", "min": 30, "max": 120, "mac_dinh": 60},
                {"ky_hieu": "n", "ten": "Số vòng đã trượt", "don_vi": "vòng", "kieu": "dieu_chinh", "min": 0, "max": 2, "mac_dinh": 1, "buoc": 0.25},
                {"ky_hieu": "t", "ten": "Thời gian", "don_vi": "s", "kieu": "dieu_chinh", "min": 5, "max": 60, "mac_dinh": 20},
                {"ky_hieu": "s", "ten": "Quãng đường", "don_vi": "m", "kieu": "tinh_ra"},
                {"ky_hieu": "v_tb", "ten": "Tốc độ trung bình", "don_vi": "m/s", "kieu": "tinh_ra"}],
    "mo_hinh": {"phuong_trinh": ["s = C·n", "d = 0 khi n là số nguyên", "v_tb = s/t"],
                "gia_thiet": ["người trượt coi là chất điểm", "số liệu minh hoạ, tốc độ đều nên t tỉ lệ với n"]},
    "so_lieu_mau": {"cot": ["n (vòng)", "s (m)", "d (m)", "t (s)", "v_tb (m/s)"],
                    "hang": [[n, C * n, 0, T1 * n, C * n / (T1 * n)] for n in (1, 2)],
                    "ghi_chu": "Số liệu minh hoạ, chu vi 60 m, một vòng 20 s."},
    "ket_qua_ky_vong": "Sau số vòng nguyên, d = 0 nhưng s và tốc độ trung bình khác 0.",
    "hien_tuong_hay_sai": ["Nghĩ đồng hồ thể thao đo độ dịch chuyển.", "Nghĩ d = 0 thì tốc độ trung bình cũng bằng 0."],
    "goi_y_mo_phong": {"loai": "2d_dong_hoc",
                       "y_tuong": "Chấm tròn chạy quanh vòng bầu dục; vệt cam dài dần (s), mũi tên xanh lá từ điểm xuất phát tới vị trí hiện tại (d) dài ra rồi co về 0.",
                       "diem_nhan": "Dừng ở nửa vòng để hỏi: lúc nào d lớn nhất?"}})

for t in (t1, t2, t3):
    (OUT / f"{t['id']}.json").write_text(json.dumps(t, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print("ok 3 file thí nghiệm;", hang)
