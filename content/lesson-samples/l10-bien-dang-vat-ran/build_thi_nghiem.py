"""Sinh 4 file content/thi-nghiem/tn-l10-biendang-0N.json cho bài 33 (lesson 78). Số liệu mẫu tính từ chính
mo_hinh của từng file (không gõ tay) và đối chiếu với bảng trong theory.html. Chạy: python3 build_thi_nghiem.py
(sau build_figs.py). Sửa số/chữ ở đây rồi chạy lại, đừng sửa tay JSON (sẽ bị ghi đè)."""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parents[1] / "thi-nghiem"
BASE = {"mon": "vat-ly", "lop": 10, "bai": "Bài 33. Biến dạng của vật rắn", "lesson_id": 78,
        "nguon_trong_bai": "content/lesson-samples/l10-bien-dang-vat-ran/theory.html"}


def r2(x, n=2):
    return round(x + 0.0, n)


# 01 — lò xo bút bi: đàn hồi và dẻo
k1, Fgh1 = 200.0, 4.0
rows1 = []
for F in (1.0, 2.0, 3.0, 6.0):
    if F <= Fgh1:
        rows1.append([F, r2(F / k1 * 100, 1), "về đúng chiều dài cũ"])
    else:
        rows1.append([F, "không còn tỉ lệ", "dài hẳn ra, không về"])
tn1 = {**BASE, "id": "tn-l10-biendang-01", "ten": "Lò xo bút bi: biến dạng đàn hồi và biến dạng dẻo",
       "loai": "thi_nghiem", "muc_do": "co_ban",
       "kien_thuc": ["bien_dang.dan_hoi_va_deo", "bien_dang.gioi_han_dan_hoi"],
       "muc_tieu": "Thấy cùng một lò xo: lực nhỏ cho biến dạng đàn hồi (thôi lực thì về), lực vượt giới hạn đàn hồi cho biến dạng dẻo (không về).",
       "dung_cu": [{"ten": "Lò xo lấy từ bút bi bấm", "so_luong": 1}],
       "cac_buoc": {"lam": ["Kéo nhẹ hai đầu lò xo rồi thả.", "Kéo thật mạnh cho lò xo duỗi hẳn ra rồi thả."],
                    "quan_sat": ["Kéo nhẹ: lò xo co về đúng chiều dài cũ.",
                                 "Kéo mạnh: lò xo dài ra hẳn, các vòng thưa mãi, không co về."],
                    "rut_ra": ["Lực nhỏ: biến dạng đàn hồi.",
                               "Lực vượt giới hạn đàn hồi: biến dạng dẻo, lò xo hỏng."]},
       "tham_so": [
           {"ky_hieu": "F", "ten": "Lực kéo", "don_vi": "N", "kieu": "dieu_chinh", "min": 0, "max": 8, "mac_dinh": 2, "buoc": 0.5},
           {"ky_hieu": "k", "ten": "Độ cứng (trong giới hạn đàn hồi)", "don_vi": "N/m", "kieu": "co_dinh", "gia_tri": k1},
           {"ky_hieu": "F_gh", "ten": "Lực ứng với giới hạn đàn hồi", "don_vi": "N", "kieu": "co_dinh", "gia_tri": Fgh1},
           {"ky_hieu": "dl", "ten": "Độ dãn", "don_vi": "cm", "kieu": "tinh_ra"}],
       "mo_hinh": {"phuong_trinh": ["nếu F ≤ F_gh: Δl = F / k, thôi lực thì Δl dư = 0",
                                    "nếu F > F_gh: không còn tỉ lệ, thôi lực còn độ dãn dư > 0"],
                   "gia_thiet": ["k = 200 N/m, F_gh = 4 N là số minh hoạ cho lò xo bút bi", "kéo dọc trục lò xo"]},
       "so_lieu_mau": {"cot": ["F (N)", "Δl khi đang kéo (cm)", "sau khi thả"], "hang": rows1,
                       "ghi_chu": "Số liệu minh hoạ tính từ mô hình; thí nghiệm định tính, bài không hiện bảng."},
       "ket_qua_ky_vong": "Trong giới hạn đàn hồi lò xo về đúng chiều dài cũ; vượt giới hạn thì còn độ dãn dư.",
       "hien_tuong_hay_sai": ["Cho rằng lò xo kéo mạnh tới đâu cũng co về được.",
                              "Cho rằng biến dạng dẻo chỉ xảy ra với vật mềm như đất nặn."],
       "goi_y_mo_phong": {"loai": "2d_dong_hoc", "y_tuong": "Lò xo nằm ngang, thanh trượt F; thả tay thì lò xo co về; vượt F_gh thì vòng giãn thưa vĩnh viễn và nút 'Làm lại' mới khôi phục.",
                          "diem_nhan": "Hỏi trước: kéo 6 N rồi thả, lò xo có về chiều dài cũ không?"}}

# 02 — đo độ cứng k bằng quả nặng (thí nghiệm đo, khớp bảng trong bài)
g2, k2, l0_2, m_1 = 9.8, 25.0, 10.0, 0.050
L_DO = [11.9, 13.9, 15.9, 17.9, 19.8]
rows2 = []
for i, l in enumerate(L_DO, 1):
    F = r2(i * m_1 * g2)
    dl = r2(l - l0_2, 1)
    assert abs(dl - F / k2 * 100) <= 0.1 + 1e-9
    rows2.append([r2(i * m_1 * 1000, 0), F, l, dl, r2(F / (dl / 100), 1)])
k_tb = sum(r[4] for r in rows2) / len(rows2)
theory = (HERE / "theory.html").read_text(encoding="utf8")
for _, F, l, dl, _k in rows2:   # bảng trong bài phải khớp từng hàng
    cell = f"<tr><td>${str(F).replace('.', '{,}')}$</td><td>${str(l).replace('.', '{,}')}$</td><td>${str(dl).replace('.', '{,}')}$</td></tr>"
    assert cell in theory, cell
tn2 = {**BASE, "id": "tn-l10-biendang-02", "ten": "Treo quả nặng vào lò xo: đo độ cứng k",
       "loai": "thi_nghiem", "muc_do": "trung_binh",
       "kien_thuc": ["hooke.f_bang_k_delta_l", "hooke.do_cung_k", "hooke.do_thi_f_delta_l"],
       "muc_tieu": "Đo chiều dài lò xo khi treo 1–5 quả nặng 50 g, tính F/|Δl| để thấy lực đàn hồi tỉ lệ độ dãn và tìm k.",
       "dung_cu": [{"ten": "Lò xo xoắn nhẹ", "so_luong": 1},
                   {"ten": "Quả nặng 50 g có móc", "so_luong": 5},
                   {"ten": "Giá treo + thước mm đặt dọc lò xo", "so_luong": 1}],
       "cac_buoc": {"lam": ["Treo lò xo cạnh thước, đọc chiều dài tự nhiên l0 = 10,0 cm.",
                            "Lần lượt móc 1, 2, 3, 4, 5 quả nặng 50 g; chờ đứng yên rồi đọc chiều dài l."],
                    "quan_sat": ["Mỗi quả nặng thêm, lò xo dài thêm gần như đều nhau, khoảng 2 cm.",
                                 f"F/|Δl| ≈ {'; '.join(str(r[4]).replace('.', ',') for r in rows2)} N/m."],
                    "rut_ra": ["Vật đứng yên: lực đàn hồi cân bằng trọng lượng, F = mg.",
                               f"F/|Δl| gần như không đổi, trung bình k ≈ {str(round(k_tb, 1)).replace('.', ',')} N/m; hàng đầu lệch nhiều nhất vì độ dãn nhỏ nhất nên sai số đọc thước tương đối lớn nhất."]},
       "tham_so": [
           {"ky_hieu": "m", "ten": "Tổng khối lượng treo", "don_vi": "kg", "kieu": "dieu_chinh", "min": 0, "max": 0.3, "mac_dinh": 0.1, "buoc": 0.05},
           {"ky_hieu": "k", "ten": "Độ cứng lò xo", "don_vi": "N/m", "kieu": "dieu_chinh", "min": 10, "max": 100, "mac_dinh": k2, "buoc": 5},
           {"ky_hieu": "l0", "ten": "Chiều dài tự nhiên", "don_vi": "cm", "kieu": "co_dinh", "gia_tri": l0_2},
           {"ky_hieu": "l", "ten": "Chiều dài đọc trên thước", "don_vi": "cm", "kieu": "do_duoc", "sai_so_do": 0.1},
           {"ky_hieu": "F", "ten": "Lực đàn hồi = trọng lượng", "don_vi": "N", "kieu": "tinh_ra"}],
       "mo_hinh": {"phuong_trinh": ["F = m·g", "|Δl| = F / k", "l = l0 + |Δl|", "k = F / |Δl|"],
                   "gia_thiet": ["g = 9,8 m/s²", "lò xo nhẹ, trong giới hạn đàn hồi", "đọc thước ±0,1 cm"]},
       "so_lieu_mau": {"cot": ["m (g)", "F (N)", "l (cm)", "Δl (cm)", "F/Δl (N/m)"], "hang": rows2,
                       "ghi_chu": "Số liệu minh hoạ (chưa phải số đo thật): l lệch mô hình k = 25 N/m không quá 0,1 cm (sai số đọc thước). Bài hiện các cột F, l, Δl; học sinh tự tính F/Δl."},
       "ket_qua_ky_vong": f"F/|Δl| gần như không đổi, k ≈ {k_tb:.1f} N/m; các điểm (Δl, F) nằm trên một đường thẳng qua gốc.",
       "hien_tuong_hay_sai": ["Tính F/l (chiều dài) thay cho F/Δl nên tỉ số giảm dần.",
                              "Quên đổi cm ra m nên k nhỏ đi 100 lần.",
                              "Cho rằng k tăng khi treo thêm quả nặng."],
       "sai_so_thuong_gap": ["Đọc thước ±0,1 cm: sai số tương đối lớn nhất ở lần dãn ít nhất.",
                             "Đọc khi quả nặng còn dao động lên xuống."],
       "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu+do_thi", "y_tuong": "Lò xo treo cạnh thước; kéo thả quả nặng vào móc; bảng tự thêm hàng F – l – Δl có nhiễu ±0,1 cm; đồ thị F theo Δl vẽ dần từng chấm.",
                          "diem_nhan": "Hỏi trước: treo 4 quả thì dài bao nhiêu (≈ 17,8 cm, không phải 4 × 11,9)."}}

# 03 — hai lò xo khác độ cứng, cùng quả nặng
g3, m3, kA, kB = 9.8, 0.100, 50.0, 25.0
FA = m3 * g3
rows3 = [["lò xo dây to", kA, r2(FA / kA * 100)], ["lò xo dây mảnh", kB, r2(FA / kB * 100)]]
assert rows3[0][2] < rows3[1][2]
tn3 = {**BASE, "id": "tn-l10-biendang-03", "ten": "Hai lò xo, cùng một quả nặng: k là của từng lò xo",
       "loai": "thi_nghiem", "muc_do": "co_ban",
       "kien_thuc": ["hooke.do_cung_k", "hooke.k_khong_phu_thuoc_luc"],
       "muc_tieu": "Thấy cùng một lực, lò xo cứng dãn ít, lò xo mềm dãn nhiều; k thuộc về lò xo chứ không đổi theo lực.",
       "dung_cu": [{"ten": "Lò xo dây to và lò xo dây mảnh", "so_luong": 2},
                   {"ten": "Quả nặng 100 g", "so_luong": 1},
                   {"ten": "Giá treo + thước", "so_luong": 1}],
       "cac_buoc": {"lam": ["Treo quả nặng 100 g vào lò xo dây to, đọc độ dãn.", "Chuyển quả nặng sang lò xo dây mảnh, đọc độ dãn."],
                    "quan_sat": [f"Lò xo dây to dãn khoảng {rows3[0][2]} cm, lò xo dây mảnh dãn khoảng {rows3[1][2]} cm."],
                    "rut_ra": ["Cùng lực, độ dãn khác nhau vì k khác nhau.",
                               "Muốn đổi k phải đổi lò xo (vật liệu, độ dày dây, kích thước), không phải đổi lực."]},
       "tham_so": [
           {"ky_hieu": "F", "ten": "Lực kéo chung", "don_vi": "N", "kieu": "dieu_chinh", "min": 0, "max": 3, "mac_dinh": 1, "buoc": 0.1},
           {"ky_hieu": "k1", "ten": "Độ cứng lò xo dây to", "don_vi": "N/m", "kieu": "dieu_chinh", "min": 10, "max": 100, "mac_dinh": kA, "buoc": 5},
           {"ky_hieu": "k2", "ten": "Độ cứng lò xo dây mảnh", "don_vi": "N/m", "kieu": "dieu_chinh", "min": 10, "max": 100, "mac_dinh": kB, "buoc": 5},
           {"ky_hieu": "dl", "ten": "Độ dãn mỗi lò xo", "don_vi": "cm", "kieu": "tinh_ra"}],
       "mo_hinh": {"phuong_trinh": ["|Δl1| = F / k1", "|Δl2| = F / k2", "đồ thị F theo Δl: hai đường thẳng qua gốc, độ dốc k1, k2"],
                   "gia_thiet": ["g = 9,8 m/s²", "k1 = 50 N/m, k2 = 25 N/m là số minh hoạ", "trong giới hạn đàn hồi"]},
       "so_lieu_mau": {"cot": ["lò xo", "k (N/m)", "Δl với 100 g (cm)"], "hang": rows3,
                       "ghi_chu": "Số liệu minh hoạ tính từ mô hình. Hình 5 của bài dùng cùng hai độ cứng, đọc ở F = 1 N: 2 cm và 4 cm."},
       "ket_qua_ky_vong": "Cùng lực, độ dãn tỉ lệ nghịch với k; mỗi lò xo có một đường thẳng F–Δl riêng.",
       "hien_tuong_hay_sai": ["Cho rằng kéo mạnh hơn thì k lớn hơn.", "Cho rằng lò xo dài hơn thì luôn cứng hơn."],
       "goi_y_mo_phong": {"loai": "do_thi+2d_dong_hoc", "y_tuong": "Hai lò xo treo cạnh nhau, cùng thanh trượt F; đồ thị F–Δl vẽ hai đường; kéo F lên thì điểm chạy dọc đường thẳng, độ dốc không đổi.",
                          "diem_nhan": "Hỏi trước: tăng F gấp đôi thì độ dốc (k) có đổi không?"}}

# 04 — cân treo: lò xo treo túi cam (mở bài)
g4, l0_4, m4 = 10.0, 20.0, 0.200
k4 = m4 * g4 / ((22.0 - l0_4) / 100)
assert abs(k4 - 100) < 1e-9
rows4 = [[n, r2(n * m4 * 1000, 0), r2(l0_4 + n * m4 * g4 / k4 * 100, 1)] for n in (0, 1, 2, 3)]
assert rows4[1][2] == 22.0 and rows4[2][2] == 24.0
tn4 = {**BASE, "id": "tn-l10-biendang-04", "ten": "Cân treo ở chợ: lò xo dài thêm tỉ lệ khối lượng treo",
       "loai": "vi_du", "muc_do": "co_ban",
       "kien_thuc": ["hooke.f_bang_k_delta_l", "hooke.delta_l_khac_l"],
       "muc_tieu": "Thấy cái tỉ lệ với khối lượng treo là độ dãn Δl, không phải chiều dài l của lò xo.",
       "dung_cu": [{"ten": "Lò xo treo + túi 200 g (hoặc cân treo đồ chơi)", "so_luong": 1}],
       "cac_buoc": {"lam": ["Đo chiều dài lò xo khi chưa treo (20 cm).", "Treo 1 túi 200 g, đo lại (22 cm).", "Dự đoán rồi đo khi treo 2 túi."],
                    "quan_sat": ["2 túi: lò xo dài 24 cm, không phải 44 cm."],
                    "rut_ra": ["Độ dãn tỉ lệ khối lượng treo: 1 túi dãn 2 cm, 2 túi dãn 4 cm.",
                               "Cân treo chia vạch đều theo độ dãn."]},
       "tham_so": [
           {"ky_hieu": "n", "ten": "Số túi 200 g", "don_vi": "", "kieu": "dieu_chinh", "min": 0, "max": 5, "mac_dinh": 1, "buoc": 1},
           {"ky_hieu": "k", "ten": "Độ cứng", "don_vi": "N/m", "kieu": "co_dinh", "gia_tri": k4},
           {"ky_hieu": "l0", "ten": "Chiều dài tự nhiên", "don_vi": "cm", "kieu": "co_dinh", "gia_tri": l0_4},
           {"ky_hieu": "l", "ten": "Chiều dài khi treo", "don_vi": "cm", "kieu": "tinh_ra"}],
       "mo_hinh": {"phuong_trinh": ["F = n·m·g", "|Δl| = F / k", "l = l0 + |Δl|"],
                   "gia_thiet": ["g = 10 m/s²", "lò xo nhẹ, trong giới hạn đàn hồi"]},
       "so_lieu_mau": {"cot": ["số túi", "m (g)", "l (cm)"], "hang": rows4,
                       "ghi_chu": "Số liệu minh hoạ tính từ mô hình; khớp câu dự đoán ở mục I (đáp án 24 cm)."},
       "ket_qua_ky_vong": "Chiều dài tăng đều 2 cm mỗi túi: l = 20 + 2n (cm).",
       "hien_tuong_hay_sai": ["Gấp đôi cả chiều dài (44 cm) thay vì gấp đôi độ dãn.", "Gấp đôi chiều dài tự nhiên (40 cm)."],
       "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu", "y_tuong": "Kéo từng túi vào móc lò xo, thước bên cạnh; ẩn chiều dài lò xo cho tới khi học sinh nhập dự đoán.",
                          "diem_nhan": "Bắt nhập dự đoán chiều dài khi treo 2 túi trước khi cho thả."}}

for d in (tn1, tn2, tn3, tn4):
    (OUT / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf8")
    print("ghi", d["id"])
print("bảng TN2:", rows2, "k_tb =", round(k_tb, 2))
assert re.search(r'data-exp="tn-l10-biendang-0[1-4]"', theory)
