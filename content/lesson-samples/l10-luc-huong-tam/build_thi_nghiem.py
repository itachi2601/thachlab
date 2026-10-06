"""Sinh 4 file content/thi-nghiem/tn-l10-huongtam-0N.json cho bài 32 (lesson 77). Số liệu mẫu tính từ chính
mo_hinh của từng file (không gõ tay). Chạy: python3 build_thi_nghiem.py. Sửa số/chữ ở đây rồi chạy lại,
đừng sửa tay JSON (sẽ bị ghi đè)."""
import json, math, pathlib

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parents[1] / "thi-nghiem"
BASE = {"mon": "vat-ly", "lop": 10, "bai": "Bài 32. Lực hướng tâm và gia tốc hướng tâm", "lesson_id": 77,
        "nguon_trong_bai": "content/lesson-samples/l10-luc-huong-tam/theory.html"}


def r2(x, n=2):
    return round(x + 0.0, n)


# 01 — ô tô qua khúc cua phẳng (mở bài + bài toán mẫu)
m1, R1, k1, g1 = 1200, 50, 0.5, 10
F_max = k1 * m1 * g1
rows1 = [[v, r2(v * 3.6, 1), r2(v * v / R1), r2(m1 * v * v / R1, 0), "không" if m1 * v * v / R1 <= F_max else "có"]
         for v in (5, 10, 15, 17)]
tn1 = {**BASE, "id": "tn-l10-huongtam-01", "ten": "Ô tô qua khúc cua phẳng: ma sát nghỉ làm lực hướng tâm",
       "loai": "vi_du", "muc_do": "trung_binh",
       "kien_thuc": ["huong_tam.a_v2_chia_r", "huong_tam.vai_tro_ma_sat_nghi", "huong_tam.toc_do_toi_da_qua_cua"],
       "muc_tieu": "Thấy xe tốc độ không đổi qua cua vẫn có gia tốc hướng vào tâm; tính lực hướng tâm cần có và tốc độ tối đa trước khi trượt.",
       "dung_cu": [{"ten": "Mô hình/ảnh nhìn từ trên của khúc cua tròn, ô tô đồ chơi", "so_luong": 1}],
       "cac_buoc": {
           "lam": ["Cho xe 1200 kg chạy đều qua khúc cua phẳng bán kính 50 m với tốc độ 5; 10; 15; 17 m/s.",
                   "Tính a_ht = v²/r và F_ht = m·v²/r; so với ma sát nghỉ lớn nhất 0,5·m·g = 6000 N."],
           "quan_sat": ["Kim tốc độ đứng yên nhưng hướng vận tốc đổi liên tục.",
                        "F_ht cần có tăng theo v²: 600 N → 2400 N → 5400 N → 6936 N; ở 17 m/s vượt 6000 N."],
           "rut_ra": ["Ma sát nghỉ giữa lốp và mặt đường đóng vai lực hướng tâm.",
                      "Tốc độ tối đa v_max = √(F_max·r/m) ≈ 15,8 m/s ≈ 57 km/h; nhanh hơn thì xe trượt khỏi đường cong."]},
       "tham_so": [
           {"ky_hieu": "m", "ten": "Khối lượng xe", "don_vi": "kg", "kieu": "co_dinh", "gia_tri": m1},
           {"ky_hieu": "r", "ten": "Bán kính khúc cua", "don_vi": "m", "kieu": "dieu_chinh", "min": 20, "max": 200, "mac_dinh": R1, "buoc": 5},
           {"ky_hieu": "v", "ten": "Tốc độ xe", "don_vi": "m/s", "kieu": "dieu_chinh", "min": 2, "max": 25, "mac_dinh": 10, "buoc": 1},
           {"ky_hieu": "k", "ten": "Tỉ số ma sát nghỉ lớn nhất / trọng lượng", "don_vi": "", "kieu": "dieu_chinh", "min": 0.1, "max": 0.8, "mac_dinh": k1, "buoc": 0.02},
           {"ky_hieu": "a_ht", "ten": "Gia tốc hướng tâm", "don_vi": "m/s²", "kieu": "tinh_ra"},
           {"ky_hieu": "F_ht", "ten": "Lực hướng tâm cần có", "don_vi": "N", "kieu": "tinh_ra"}],
       "mo_hinh": {"phuong_trinh": ["a_ht = v² / r", "F_ht = m·v² / r", "F_max = k·m·g", "trượt nếu F_ht > F_max",
                                    "v_max = √(k·g·r)"],
                   "gia_thiet": ["đường nằm ngang, P và N triệt tiêu", "xe coi là chất điểm, chạy đều", "g = 10 m/s²"]},
       "so_lieu_mau": {"cot": ["v (m/s)", "v (km/h)", "a_ht (m/s²)", "F_ht (N)", "trượt?"], "hang": rows1,
                       "ghi_chu": "Số liệu tính từ mô hình (minh hoạ), m = 1200 kg, r = 50 m, k = 0,5. Bài toán mẫu dùng hàng v = 10 m/s; biến thể trời mưa k = 0,16 cho F_max = 1920 N, v_max ≈ 8,9 m/s."},
       "ket_qua_ky_vong": f"F_ht tăng theo v²; xe trượt khi v > √(k·g·r) ≈ {math.sqrt(k1 * g1 * R1):.1f} m/s, không phụ thuộc khối lượng xe.",
       "hien_tuong_hay_sai": ["Cho rằng tốc độ không đổi thì không có gia tốc.",
                              "Vẽ thêm một 'lực hướng tâm' bên cạnh ma sát (đếm một lực hai lần).",
                              "Thế thẳng km/h vào v²/r, không đổi ra m/s."],
       "goi_y_mo_phong": {"loai": "2d_dong_hoc+so_do_luc", "y_tuong": "Xe nhìn từ trên chạy trên cung tròn; thanh trượt v, r, k; mũi tên v (tiếp tuyến), F_ms và a_ht (vào tâm) cập nhật; vượt F_max thì xe trượt theo hướng gần tiếp tuyến.",
                          "diem_nhan": "Hỏi trước: tăng tốc độ gấp đôi thì lực cần có gấp mấy (4, không phải 2)."}}

# 02 — đồng xu trên bàn xoay
m2, r2_, k2, g2 = 0.0075, 0.10, 0.3, 10
rows2 = []
for n in (20, 30, 45, 60):
    w = 2 * math.pi * n / 60
    a = w * w * r2_
    rows2.append([n, r2(w), r2(a), "không" if a <= k2 * g2 else "có"])
tn2 = {**BASE, "id": "tn-l10-huongtam-02", "ten": "Đồng xu trên bàn xoay: ma sát nghỉ giữ xu đi vòng",
       "loai": "thi_nghiem", "muc_do": "co_ban",
       "kien_thuc": ["huong_tam.vai_tro_ma_sat_nghi", "huong_tam.a_omega2_r"],
       "muc_tieu": "Thấy lực giữ vật trên vòng tròn là ma sát nghỉ; quay đủ nhanh thì ma sát nghỉ không đủ và vật trượt.",
       "dung_cu": [{"ten": "Bàn xoay (loại xoay bánh kem) hoặc đĩa quay", "so_luong": 1},
                   {"ten": "Đồng xu", "so_luong": 1}],
       "cac_buoc": {"lam": ["Đặt đồng xu cách tâm đĩa khoảng 10 cm.", "Quay chậm rồi tăng dần tốc độ quay."],
                    "quan_sat": ["Lúc đầu xu quay theo đĩa, không trượt.", "Quay đủ nhanh thì xu trượt ra khỏi vòng tròn."],
                    "rut_ra": ["Ma sát nghỉ của đĩa đóng vai lực hướng tâm.",
                               "Khi m·ω²·r cần lớn hơn ma sát nghỉ lớn nhất, xu trượt."]},
       "tham_so": [
           {"ky_hieu": "r", "ten": "Khoảng cách xu tới tâm", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.03, "max": 0.3, "mac_dinh": r2_, "buoc": 0.01},
           {"ky_hieu": "n", "ten": "Tốc độ quay", "don_vi": "vòng/phút", "kieu": "dieu_chinh", "min": 10, "max": 90, "mac_dinh": 30, "buoc": 5},
           {"ky_hieu": "k", "ten": "Tỉ số ma sát nghỉ lớn nhất / trọng lượng", "don_vi": "", "kieu": "co_dinh", "gia_tri": k2},
           {"ky_hieu": "a_ht", "ten": "Gia tốc hướng tâm cần có", "don_vi": "m/s²", "kieu": "tinh_ra"}],
       "mo_hinh": {"phuong_trinh": ["ω = 2π·n / 60", "a_ht = ω²·r", "trượt nếu ω²·r > k·g", "r_max = k·g / ω²"],
                   "gia_thiet": ["đĩa nằm ngang, quay đều", "k = 0,3 (giả định)", "g = 10 m/s²", "khối lượng xu không ảnh hưởng ngưỡng trượt"]},
       "so_lieu_mau": {"cot": ["n (vòng/phút)", "ω (rad/s)", "a_ht (m/s²)", "trượt?"], "hang": rows2,
                       "ghi_chu": "Số liệu tính từ mô hình (minh hoạ), r = 10 cm, k = 0,3: ngưỡng a = 3 m/s², ứng với khoảng 52 vòng/phút."},
       "ket_qua_ky_vong": f"Xu trượt khi ω > √(k·g/r) ≈ {math.sqrt(k2 * g2 / r2_):.2f} rad/s (≈ {math.sqrt(k2 * g2 / r2_) * 60 / (2 * math.pi):.0f} vòng/phút) với r = 10 cm.",
       "hien_tuong_hay_sai": ["Cho rằng xu trượt vì 'lực li tâm' đẩy ra; thật ra ma sát nghỉ không đủ làm lực hướng tâm.",
                              "Cho rằng xu bay ra theo bán kính; thật ra nó rời đi gần theo tiếp tuyến."],
       "goi_y_mo_phong": {"loai": "2d_dong_hoc+so_do_luc", "y_tuong": "Đĩa nhìn từ trên, thanh trượt n và r; vẽ ma sát nghỉ chĩa vào tâm, thanh đo 'ma sát cần có / ma sát lớn nhất'; vượt 100 % thì xu trượt.",
                          "diem_nhan": "Cho đặt hai xu ở hai bán kính, hỏi trước xu nào trượt trước."}}

# 03 — nút cao su quay trên đầu ống (thí nghiệm đo)
m3, R3, g3 = 0.050, 0.50, 9.8
rows3 = []
for M, t10 in ((0.10, 10.2), (0.20, 7.0), (0.30, 5.7)):
    T = t10 / 10
    v = 2 * math.pi * R3 / T
    F = m3 * v * v / R3
    rows3.append([M, r2(M * g3), t10, r2(v), r2(F)])
for M, Mg, t10, v, F in rows3:   # kiểm: mọi hàng lệch < 4 % và nằm trong sai số bấm giờ 2·0,2/t10
    dev = abs(F / Mg - 1)
    assert dev < 0.04 and dev < 2 * 0.2 / t10, (M, dev)
tn3 = {**BASE, "id": "tn-l10-huongtam-03", "ten": "Nút cao su quay trên đầu ống: kiểm F = m·v²/r",
       "loai": "thi_nghiem", "muc_do": "trung_binh",
       "kien_thuc": ["huong_tam.f_bang_m_v2_chia_r", "huong_tam.vai_tro_luc_cang"],
       "muc_tieu": "Đo thời gian 10 vòng để tính m·v²/r và so với lực căng dây Mg đã biết.",
       "dung_cu": [{"ten": "Nút cao su 0,050 kg buộc đầu dây", "so_luong": 1},
                   {"ten": "Ống nhựa cứng (thân bút bi to) để luồn dây", "so_luong": 1},
                   {"ten": "Bộ quả nặng 0,10 kg", "so_luong": 3},
                   {"ten": "Kẹp giấy đánh dấu trên dây", "so_luong": 1},
                   {"ten": "Đồng hồ bấm giây (phản xạ tay ±0,2 s)", "so_luong": 1},
                   {"ten": "Thước dây", "so_luong": 1}],
       "cac_buoc": {"lam": ["Luồn dây qua ống, buộc nút cao su ở đầu trên, treo quả nặng M ở đầu dưới.",
                            "Đặt kẹp sao cho bán kính quỹ đạo r = 0,50 m (từ trục ống tới nút).",
                            "Quay nút thành vòng tròn nằm ngang, giữ kẹp đứng yên ngay dưới ống; bấm thời gian t10 của 10 vòng.",
                            "Làm với M = 0,10; 0,20; 0,30 kg."],
                    "quan_sat": ["Quả nặng càng lớn, phải quay càng nhanh thì kẹp mới đứng yên: t10 = 10,2 s; 7,0 s; 5,7 s.",
                                 "m·v²/r ≈ 0,95; 2,01; 3,04 N so với Mg = 0,98; 1,96; 2,94 N."],
                    "rut_ra": ["Lực căng dây Mg đóng vai lực hướng tâm.",
                               "m·v²/r khớp Mg trong khoảng 4 %, cỡ sai số bấm giờ: F_ht = m·v²/r được xác nhận."]},
       "tham_so": [
           {"ky_hieu": "m", "ten": "Khối lượng nút cao su", "don_vi": "kg", "kieu": "co_dinh", "gia_tri": m3},
           {"ky_hieu": "r", "ten": "Bán kính quỹ đạo", "don_vi": "m", "kieu": "co_dinh", "gia_tri": R3},
           {"ky_hieu": "M", "ten": "Khối lượng quả nặng", "don_vi": "kg", "kieu": "dieu_chinh", "min": 0.05, "max": 0.5, "mac_dinh": 0.1, "buoc": 0.05},
           {"ky_hieu": "t10", "ten": "Thời gian 10 vòng", "don_vi": "s", "kieu": "do_duoc", "sai_so_do": 0.2},
           {"ky_hieu": "F_ht", "ten": "m·v²/r tính từ số đo", "don_vi": "N", "kieu": "tinh_ra"}],
       "mo_hinh": {"phuong_trinh": ["T = t10 / 10", "v = 2π·r / T", "F_ht = m·v² / r", "F_ht = M·g (lý thuyết)",
                                    "t10 = 10·2π·√(m·r / (M·g))"],
                   "gia_thiet": ["dây nằm ngang, bỏ qua trọng lượng nút làm dây chùng", "bỏ qua ma sát dây với miệng ống",
                                 "g = 9,8 m/s²", "kẹp đứng yên nên r không đổi"]},
       "so_lieu_mau": {"cot": ["M (kg)", "Mg (N)", "t10 (s)", "v (m/s)", "m·v²/r (N)"], "hang": rows3,
                       "ghi_chu": "Số liệu minh hoạ (chưa phải số đo thật): t10 lệch ngẫu nhiên quanh mô hình (10,04; 7,10; 5,79 s), mỗi hàng lệch dưới 4 %, nằm trong sai số bấm giờ 2·0,2/t10. Bài chỉ hiện các cột Mg, t10, m·v²/r."},
       "ket_qua_ky_vong": "m·v²/r ≈ Mg ở cả ba lần đo; sai số tương đối lớn nhất ở lần quay nhanh nhất (t10 ngắn nhất, ≈ 7 %).",
       "hien_tuong_hay_sai": ["Cho rằng quay nhanh thì nút 'bị kéo ra' nên kẹp tụt lên; thật ra cần lực hướng tâm lớn hơn, quả nặng không đủ giữ.",
                              "Đo r từ tay chứ không từ trục ống."],
       "sai_so_thuong_gap": ["Bấm giờ ±0,2 s; F ~ 1/T² nên sai số tương đối của F gấp đôi của t.",
                             "Dây không nằm ngang hẳn (nút có trọng lượng) và dây cọ miệng ống."],
       "an_toan": "Quay ở nơi rộng, không ai đứng trong vòng quay; buộc chặt nút cao su.",
       "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu", "y_tuong": "Nút quay quanh ống (nhìn nghiêng), thanh trượt M; đồng hồ đếm 10 vòng có nhiễu ±0,2 s; bảng tự thêm hàng Mg – t10 – m·v²/r.",
                          "diem_nhan": "Hỏi trước: M gấp 4 thì t10 giảm mấy lần (2, vì t ~ 1/√M)."}}

# 04 — viên bi trong vòng có chỗ hở
tn4 = {**BASE, "id": "tn-l10-huongtam-04", "ten": "Viên bi trong vòng có chỗ hở: mất lực hướng tâm thì đi theo tiếp tuyến",
       "loai": "thi_nghiem", "muc_do": "co_ban",
       "kien_thuc": ["huong_tam.khong_co_luc_li_tam", "huong_tam.bay_theo_tiep_tuyen"],
       "muc_tieu": "Thấy vật mất lực hướng tâm thì đi thẳng theo tiếp tuyến, không bật ra theo bán kính.",
       "dung_cu": [{"ten": "Nắp hộp tròn có thành (đường kính ~20 cm), cắt bỏ một đoạn thành ~1/6 vòng", "so_luong": 1},
                   {"ten": "Viên bi", "so_luong": 1}],
       "cac_buoc": {"lam": ["Đặt nắp hộp trên bàn phẳng.", "Búng viên bi chạy vòng sát thành, hướng về phía chỗ hở."],
                    "quan_sat": ["Tới chỗ hở, bi lăn thẳng theo tiếp tuyến tại điểm thành kết thúc.",
                                 "Bi không bật ra theo bán kính."],
                    "rut_ra": ["Thành vòng đẩy bi vào tâm, đóng vai lực hướng tâm.",
                               "Mất lực đó, bi đi thẳng theo quán tính."]},
       "tham_so": [
           {"ky_hieu": "R", "ten": "Bán kính vòng", "don_vi": "m", "kieu": "co_dinh", "gia_tri": 0.10},
           {"ky_hieu": "v", "ten": "Tốc độ bi", "don_vi": "m/s", "kieu": "dieu_chinh", "min": 0.2, "max": 1.5, "mac_dinh": 0.6, "buoc": 0.1},
           {"ky_hieu": "goc_ho", "ten": "Vị trí bắt đầu chỗ hở", "don_vi": "độ", "kieu": "dieu_chinh", "min": 0, "max": 330, "mac_dinh": 0, "buoc": 30},
           {"ky_hieu": "N", "ten": "Lực thành đẩy bi", "don_vi": "N", "kieu": "tinh_ra"}],
       "mo_hinh": {"phuong_trinh": ["trên thành: N = m·v² / R, hướng vào tâm",
                                    "ở chỗ hở: N = 0, bi chuyển động thẳng đều theo tiếp tuyến tại điểm rời thành"],
                   "gia_thiet": ["bỏ qua ma sát lăn trong thời gian quan sát", "bi coi là chất điểm"]},
       "so_lieu_mau": {"cot": ["v (m/s)", "N (N) với m = 0,02 kg"],
                       "hang": [[v, r2(0.02 * v * v / 0.10, 3)] for v in (0.4, 0.6, 0.8)],
                       "ghi_chu": "Số liệu tính từ mô hình (minh hoạ); thí nghiệm này định tính, bài không hiện bảng."},
       "ket_qua_ky_vong": "Quỹ đạo sau chỗ hở là đường thẳng tiếp tuyến với vòng tại điểm rời thành.",
       "hien_tuong_hay_sai": ["Dự đoán bi bật thẳng ra ngoài theo bán kính vì 'lực li tâm'.",
                              "Dự đoán bi tiếp tục đi cong một đoạn sau khi rời thành."],
       "goi_y_mo_phong": {"loai": "2d_dong_hoc", "y_tuong": "Nhìn từ trên, kéo chỗ hở tới vị trí bất kỳ; bi rời thành đi thẳng; vẽ mờ đường 'bán kính' để so.",
                          "diem_nhan": "Cho học sinh vẽ dự đoán đường đi trước khi bấm chạy."}}

for d in (tn1, tn2, tn3, tn4):
    (OUT / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf8")
    print("ghi", d["id"])
print("bảng TN3:", rows3)
