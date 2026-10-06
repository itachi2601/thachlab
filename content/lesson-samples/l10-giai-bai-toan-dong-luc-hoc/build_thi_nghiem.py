"""Sinh 3 file content/thi-nghiem/tn-l10-giaibt-dlh-0N.json cho bài 20 (lesson 65). Số liệu mẫu tính từ chính
mo_hinh của từng file (g = 10 m/s², thống nhất với cả bài). Chạy: python3 build_thi_nghiem.py (TRƯỚC build_figs.py —
build_figs đọc bảng số liệu của tn-02 để dựng bảng trong bài). Sửa số/chữ ở đây rồi chạy lại, đừng sửa tay JSON."""
import json, math, pathlib

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parents[1] / "thi-nghiem"
G = 10
BASE = {"mon": "vat-ly", "lop": 10,
        "bai": "Bài 20. Một số ví dụ về cách giải các bài toán thuộc phần động lực học", "lesson_id": 65,
        "nguon_trong_bai": "content/lesson-samples/l10-giai-bai-toan-dong-luc-hoc/theory.html"}


def r2(x, n=2):
    return round(x + 0.0, n)


# 01 — hai hộp trượt trên ván nghiêng (và cầu trượt mở bài)
al1, mu1, L1 = 30, 0.3, 1.0
a1 = G * (math.sin(math.radians(al1)) - mu1 * math.cos(math.radians(al1)))
assert math.tan(math.radians(al1)) > mu1          # hộp thật sự trượt
rows1 = [[m, r2(a1), r2(math.sqrt(2 * L1 / a1))] for m in (0.05, 0.10, 0.20, 0.40)]
assert len({(r[1], r[2]) for r in rows1}) == 1    # a, t không phụ thuộc m
tn1 = {**BASE, "id": "tn-l10-giaibt-dlh-01", "ten": "Hai hộp nhẹ và nặng trượt trên ván nghiêng",
       "loai": "thi_nghiem", "muc_do": "co_ban",
       "kien_thuc": ["dong_luc_hoc.quy_trinh_4_buoc", "dong_luc_hoc.mat_phang_nghieng", "ma_sat.ap_luc_mat_nghieng"],
       "muc_tieu": "Thấy hai vật cùng chất liệu đáy, khác khối lượng, trượt xuống dốc với cùng gia tốc; giải thích bằng a = g(sinα − μcosα).",
       "dung_cu": [{"ten": "Tấm ván phẳng dài khoảng 1 m, kê nghiêng khoảng 30°", "so_luong": 1},
                   {"ten": "Hộp bút nhựa giống nhau (một rỗng, một nhét đầy tẩy và bút)", "so_luong": 2}],
       "cac_buoc": {"lam": ["Kê tấm ván nghiêng khoảng 30°.",
                            "Đặt hai hộp cạnh nhau ở đầu ván, thả cùng lúc."],
                    "quan_sat": ["Hai hộp tới chân ván gần như cùng lúc dù một hộp nặng hơn nhiều."],
                    "rut_ra": ["Chiếu định luật II lên trục dọc dốc: mg·sinα − μ·mg·cosα = m·a, m giản ước.",
                               "Gia tốc trượt a = g(sinα − μcosα) không phụ thuộc khối lượng; hai bạn trên cầu trượt đôi cũng vậy."]},
       "tham_so": [
           {"ky_hieu": "alpha", "ten": "Góc nghiêng", "don_vi": "°", "kieu": "dieu_chinh", "min": 10, "max": 60, "mac_dinh": al1, "buoc": 1},
           {"ky_hieu": "mu", "ten": "Hệ số ma sát trượt", "don_vi": "", "kieu": "dieu_chinh", "min": 0, "max": 0.6, "mac_dinh": mu1, "buoc": 0.05},
           {"ky_hieu": "m", "ten": "Khối lượng hộp", "don_vi": "kg", "kieu": "dieu_chinh", "min": 0.05, "max": 0.5, "mac_dinh": 0.1, "buoc": 0.05},
           {"ky_hieu": "L", "ten": "Chiều dài ván", "don_vi": "m", "kieu": "co_dinh", "gia_tri": L1},
           {"ky_hieu": "a", "ten": "Gia tốc trượt", "don_vi": "m/s²", "kieu": "tinh_ra"},
           {"ky_hieu": "t", "ten": "Thời gian trượt hết ván", "don_vi": "s", "kieu": "tinh_ra"}],
       "mo_hinh": {"phuong_trinh": ["N = m·g·cosα", "a = g·(sinα − μ·cosα)", "t = √(2L/a)", "trượt nếu tanα > μ_n"],
                   "gia_thiet": ["hộp coi là chất điểm, thả từ nghỉ", "bỏ qua sức cản không khí",
                                 "μ = 0,3 (giả định, nhựa trên gỗ)", "g = 10 m/s²"]},
       "so_lieu_mau": {"cot": ["m (kg)", "a (m/s²)", "t (s)"], "hang": rows1,
                       "ghi_chu": "Số liệu tính từ mô hình (minh hoạ), α = 30°, μ = 0,3, L = 1 m: mọi khối lượng cho cùng a và t."},
       "ket_qua_ky_vong": f"a ≈ {a1:.2f} m/s², t ≈ {math.sqrt(2 * L1 / a1):.2f} s cho mọi khối lượng.",
       "hien_tuong_hay_sai": ["Dự đoán hộp nặng xuống nhanh hơn vì lực kéo xuống dốc lớn hơn.",
                              "Dự đoán hộp nhẹ xuống nhanh hơn vì ma sát nhỏ hơn.",
                              "Tính áp lực bằng mg thay vì mg·cosα."],
       "goi_y_mo_phong": {"loai": "2d_dong_hoc+so_do_luc",
                          "y_tuong": "Hai hộp khác khối lượng trên cùng một dốc; thanh trượt α, μ, m; mũi tên P, N, F_ms tỉ lệ độ lớn; đồng hồ đo thời gian tới chân dốc.",
                          "diem_nhan": "Cho học sinh chọn trước hộp nào tới trước rồi mới bấm thả."}}

# 02 — hệ xe lăn + quả nặng qua ròng rọc (thí nghiệm đo, có bảng)
m1, m2, mu2, s2 = 0.40, 0.10, 0.02, 0.80
a_li = m2 * G / (m1 + m2)                         # dự đoán bỏ ma sát
a_mh = (m2 * G - mu2 * m1 * G) / (m1 + m2)        # mô hình sinh số liệu (có lực cản nhỏ)
t_mh = math.sqrt(2 * s2 / a_mh)
TS = [0.93, 0.95, 0.92, 0.94, 0.93]              # t "đo" = t mô hình ± 0,02 s (minh hoạ)
assert all(abs(t - t_mh) <= 0.021 for t in TS), t_mh
rows2 = [[i + 1, t, r2(2 * s2 / t ** 2)] for i, t in enumerate(TS)]
a_tb = sum(r[2] for r in rows2) / len(rows2)
assert all(r[2] < a_li for r in rows2)            # mọi lần đều thấp hơn dự đoán (sai số hệ thống)
assert abs(a_tb - 1.83) < 0.01 and abs((a_li - a_tb) / a_li - 0.08) < 0.01
assert abs(0.5 * (a_li - a_tb) - 0.08) < 0.005     # lực cản ước tính ≈ 0,08 N
tn2 = {**BASE, "id": "tn-l10-giaibt-dlh-02", "ten": "Hệ xe lăn và quả nặng nối dây qua ròng rọc",
       "loai": "thi_nghiem", "muc_do": "trung_binh",
       "kien_thuc": ["dong_luc_hoc.quy_trinh_4_buoc", "dong_luc_hoc.he_vat_noi_day", "do_luong.sai_so_he_thong"],
       "muc_tieu": "Dự đoán gia tốc của hệ hai vật nối dây bằng định luật II viết cho từng vật, rồi đo để so; nhận ra sai số hệ thống do ma sát.",
       "dung_cu": [{"ten": "Xe lăn 0,40 kg và máng ngang", "so_luong": 1},
                   {"ten": "Ròng rọc nhẹ kẹp mép bàn, dây mảnh", "so_luong": 1},
                   {"ten": "Quả nặng 0,10 kg", "so_luong": 1},
                   {"ten": "Cổng quang điện và đồng hồ đo thời gian hiện số", "so_luong": 1},
                   {"ten": "Thước đo độ dài", "so_luong": 1}],
       "cac_buoc": {"lam": ["Nối xe lăn m1 = 0,40 kg với quả nặng m2 = 0,10 kg qua ròng rọc ở mép bàn.",
                            "Thả hệ từ nghỉ, đo thời gian t xe đi s = 0,80 m bằng cổng quang; làm 5 lần.",
                            "Tính a = 2s/t² cho từng lần."],
                    "quan_sat": ["t dao động quanh 0,93 s; a đo khoảng 1,77–1,89 m/s²."],
                    "rut_ra": ["Bỏ ma sát, 4 bước cho a = m2·g/(m1 + m2) = 2,0 m/s².",
                               "Cả 5 lần đều nhỏ hơn 2,0 m/s² (trung bình ≈ 1,83): sai số hệ thống do ma sát trục bánh và ròng rọc, lực cản cỡ 0,08 N.",
                               "Chênh nhau giữa các lần (±0,02 s) là sai số ngẫu nhiên khi thả tay."]},
       "tham_so": [
           {"ky_hieu": "m1", "ten": "Khối lượng xe", "don_vi": "kg", "kieu": "dieu_chinh", "min": 0.1, "max": 1.0, "mac_dinh": m1, "buoc": 0.05},
           {"ky_hieu": "m2", "ten": "Khối lượng quả nặng", "don_vi": "kg", "kieu": "dieu_chinh", "min": 0.02, "max": 0.5, "mac_dinh": m2, "buoc": 0.01},
           {"ky_hieu": "mu", "ten": "Hệ số cản quy đổi (ma sát trục, ròng rọc)", "don_vi": "", "kieu": "dieu_chinh", "min": 0, "max": 0.1, "mac_dinh": mu2, "buoc": 0.005},
           {"ky_hieu": "s", "ten": "Quãng đường đo", "don_vi": "m", "kieu": "co_dinh", "gia_tri": s2},
           {"ky_hieu": "t", "ten": "Thời gian đi hết s", "don_vi": "s", "kieu": "do_duoc", "sai_so_do": 0.02},
           {"ky_hieu": "a", "ten": "Gia tốc của hệ", "don_vi": "m/s²", "kieu": "tinh_ra"},
           {"ky_hieu": "T", "ten": "Lực căng dây", "don_vi": "N", "kieu": "tinh_ra"}],
       "mo_hinh": {"phuong_trinh": ["m1: T − μ·m1·g = m1·a", "m2: m2·g − T = m2·a",
                                    "a = (m2·g − μ·m1·g)/(m1 + m2)", "T = m2·(g − a)", "a_đo = 2s/t²"],
                   "gia_thiet": ["dây nhẹ, không dãn; ròng rọc nhẹ", "lực cản quy đổi thành μ·m1·g với μ = 0,02",
                                 "g = 10 m/s²", "thả từ nghỉ"]},
       "so_lieu_mau": {"cot": ["Lần", "t (s)", "a (m/s²)"], "hang": rows2,
                       "ghi_chu": f"Số liệu minh hoạ, không phải đo thật: t sinh từ mô hình a = {a_mh:.2f} m/s² (t ≈ {t_mh:.3f} s) cộng dao động ±0,02 s; dự đoán bỏ ma sát {a_li:.1f} m/s²."},
       "ket_qua_ky_vong": f"a đo trung bình ≈ {a_tb:.2f} m/s², thấp hơn dự đoán {a_li:.1f} m/s² khoảng {100 * (a_li - a_tb) / a_li:.0f} %; mọi lần đều thấp hơn.",
       "sai_so_thuong_gap": ["Ma sát trục bánh xe, ròng rọc (hệ thống, làm a nhỏ đi)",
                             "Dùng g = 10 thay vì 9,8 (dự đoán cao hơn khoảng 2 %)",
                             "Thả tay đẩy nhẹ hoặc giữ lại (ngẫu nhiên)"],
       "hien_tuong_hay_sai": ["Viết m2·g = (m1 + m2)·a nhưng quên ma sát, rồi cho rằng số đo 'sai'.",
                              "Chọn chiều dương của vật treo hướng lên, ra phương trình sai dấu.",
                              "Cho rằng lực căng dây bằng trọng lượng quả nặng (T = m2·g)."],
       "goi_y_mo_phong": {"loai": "2d_dong_hoc+so_do_luc+bang_so_lieu",
                          "y_tuong": "Xe trên bàn nối dây qua ròng rọc với quả nặng; thanh trượt m1, m2, μ; hiện T, a; cổng quang ghi t, tự lập bảng 5 lần có nhiễu.",
                          "diem_nhan": "So cột a đo với đường a lý thuyết bỏ ma sát: mọi điểm nằm dưới đường."}}

# 03 — kéo thùng sách bằng dây xiên (mặt ngang có ma sát)
m3, F3, mu3 = 20, 100, 0.2
rows3 = []
for al in (0, 15, 30, 45, 60):
    ra = math.radians(al)
    N = m3 * G - F3 * math.sin(ra)
    fms = mu3 * N
    rows3.append([al, r2(N, 1), r2(fms, 1), r2((F3 * math.cos(ra) - fms) / m3)])
assert rows3[2][1] == 150.0 and rows3[2][2] == 30.0   # khớp Câu 1 của bài
tn3 = {**BASE, "id": "tn-l10-giaibt-dlh-03", "ten": "Kéo thùng sách bằng dây xiên trên sàn có ma sát",
       "loai": "vi_du", "muc_do": "trung_binh",
       "kien_thuc": ["dong_luc_hoc.quy_trinh_4_buoc", "dong_luc_hoc.mat_ngang_ma_sat", "ma_sat.ap_luc_khac_mg"],
       "muc_tieu": "Áp 4 bước cho vật trên mặt ngang; thấy kéo xiên lên làm áp lực N = mg − F·sinα nhỏ hơn mg, nên ma sát giảm.",
       "dung_cu": [{"ten": "Thùng carton đựng sách, dây kéo, lực kế (nếu làm thật)", "so_luong": 1}],
       "cac_buoc": {"lam": ["Kéo thùng sách 20 kg trên sàn bằng lực ngang 80 N (μ = 0,3), rồi bằng lực 100 N xiên lên các góc khác nhau (μ = 0,2)."],
                    "quan_sat": ["Kéo ngang: N = 200 N, a = 1 m/s².",
                                 "Kéo xiên 30°: N = 150 N, ma sát 30 N."],
                    "rut_ra": ["Chiếu lên Oy để tìm N, không mặc định N = mg.",
                               "Chiếu lên Ox: F·cosα − μN = m·a."]},
       "tham_so": [
           {"ky_hieu": "m", "ten": "Khối lượng thùng", "don_vi": "kg", "kieu": "dieu_chinh", "min": 5, "max": 40, "mac_dinh": m3, "buoc": 1},
           {"ky_hieu": "F", "ten": "Lực kéo", "don_vi": "N", "kieu": "dieu_chinh", "min": 0, "max": 200, "mac_dinh": F3, "buoc": 5},
           {"ky_hieu": "alpha", "ten": "Góc dây so với sàn", "don_vi": "°", "kieu": "dieu_chinh", "min": 0, "max": 80, "mac_dinh": 30, "buoc": 1},
           {"ky_hieu": "mu", "ten": "Hệ số ma sát trượt", "don_vi": "", "kieu": "dieu_chinh", "min": 0, "max": 0.6, "mac_dinh": mu3, "buoc": 0.05},
           {"ky_hieu": "N", "ten": "Áp lực", "don_vi": "N", "kieu": "tinh_ra"},
           {"ky_hieu": "a", "ten": "Gia tốc", "don_vi": "m/s²", "kieu": "tinh_ra"}],
       "mo_hinh": {"phuong_trinh": ["N = m·g − F·sinα", "F_ms = μ·N", "a = (F·cosα − μ·N)/m"],
                   "gia_thiet": ["thùng trượt (đã thắng ma sát nghỉ)", "F·sinα < m·g (thùng không bị nhấc khỏi sàn)", "g = 10 m/s²"]},
       "so_lieu_mau": {"cot": ["α (°)", "N (N)", "F_ms (N)", "a (m/s²)"], "hang": rows3,
                       "ghi_chu": "Số liệu tính từ mô hình (minh hoạ), m = 20 kg, F = 100 N, μ = 0,2. Hàng α = 30° là Câu 1 trong bài."},
       "ket_qua_ky_vong": "N giảm khi α tăng; a lớn nhất quanh tanα = μ (α ≈ 11°), rồi giảm vì F·cosα giảm.",
       "hien_tuong_hay_sai": ["Coi N = mg khi dây kéo xiên.", "Cộng F·sinα vào N thay vì trừ.",
                              "Lấy F·cosα làm áp lực."],
       "goi_y_mo_phong": {"loai": "so_do_luc+do_thi",
                          "y_tuong": "Thùng trên sàn, xoay góc dây; mũi tên P, N, F, F_ms co giãn theo độ lớn; đồ thị a theo α.",
                          "diem_nhan": "Hỏi trước: kéo xiên lên có nhẹ tay hơn kéo ngang không?"}}

for d in (tn1, tn2, tn3):
    (OUT / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf8")
    print("ghi", d["id"])
print("bảng TN2:", rows2, "a_tb =", round(a_tb, 3))
print("bảng TN3:", rows3)
