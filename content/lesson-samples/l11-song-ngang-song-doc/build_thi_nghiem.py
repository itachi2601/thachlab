"""Ghi 3 file thí nghiệm của bài 'Sóng ngang, sóng dọc, sự truyền năng lượng của sóng cơ' (lesson 28) vào content/thi-nghiem/.
Số liệu mẫu TÍNH bằng script từ mô hình khai trong file (không gõ tay).
Chạy: python3 build_thi_nghiem.py (trước build_figs.py — build_figs đọc lại tn-03 để dựng bảng trong bài)."""
import json, math, pathlib

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parents[1] / "thi-nghiem"
CHUNG = {"mon": "vat-ly", "lop": 11, "bai": "Bài 9. Sóng ngang, sóng dọc, sự truyền năng lượng của sóng cơ", "lesson_id": 28,
         "nguon_trong_bai": "content/lesson-samples/l11-song-ngang-song-doc/theory.html"}

# ---------- 01: dây nhảy + dải băng màu — sóng ngang (định tính) ----------
tn1 = dict(CHUNG, **{
    "id": "tn-l11-songngangdoc-01",
    "ten": "Sóng ngang trên dây nhảy: dải băng màu chỉ lên xuống",
    "loai": "thi_nghiem", "muc_do": "co_ban",
    "kien_thuc": ["song.song_ngang", "song.phan_tu_dao_dong_tai_cho"],
    "muc_tieu": "Thấy phương dao động của một điểm trên dây vuông góc với phương truyền sóng, và điểm đó không chạy theo sóng.",
    "dung_cu": [
        {"ten": "Dây nhảy dài 4–6 m", "so_luong": 1},
        {"ten": "Dải băng màu buộc giữa dây", "so_luong": 1},
        {"ten": "Cột bóng rổ hoặc chân bàn để buộc đầu dây", "so_luong": 1},
    ],
    "cac_buoc": {
        "lam": ["Buộc một đầu dây vào cột, kéo căng ngang.", "Buộc dải băng màu ở giữa dây.",
                "Vẩy đầu dây lên xuống một cái thật nhanh."],
        "quan_sat": ["Một 'cái bướu' chạy dọc dây tới cột.", "Dải băng chỉ nhảy lên rồi rơi về chỗ cũ, không chạy theo bướu."],
        "rut_ra": ["Phương truyền nằm ngang dọc dây, phương dao động thẳng đứng: vuông góc nhau — sóng ngang.",
                   "Phần tử dây chỉ dao động tại chỗ; thứ chạy đi là trạng thái dao động và năng lượng."],
    },
    "tham_so": [
        {"ky_hieu": "A", "ten": "Biên độ cú vẩy", "don_vi": "cm", "kieu": "dieu_chinh", "min": 5, "max": 30, "mac_dinh": 15, "buoc": 5},
        {"ky_hieu": "v", "ten": "Tốc độ truyền sóng trên dây", "don_vi": "m/s", "kieu": "dieu_chinh", "min": 2, "max": 10, "mac_dinh": 5, "buoc": 1},
        {"ky_hieu": "x_b", "ten": "Vị trí dải băng", "don_vi": "m", "kieu": "co_dinh", "gia_tri": 2.5},
        {"ky_hieu": "u_b", "ten": "Li độ dải băng theo thời gian", "don_vi": "cm", "kieu": "tinh_ra"},
    ],
    "mo_hinh": {
        "phuong_trinh": ["u(x, t) = A·exp(−((x − v·t)/w)²) (xung dạng chuông, bề rộng w ≈ 0,4 m)",
                         "u_b(t) = u(x_b, t): dải băng chỉ lên xuống, hoành độ không đổi"],
        "gia_thiet": ["bỏ qua tắt dần và phản xạ ở cột", "dây đồng chất, căng đều"],
    },
    "so_lieu_mau": {
        "cot": ["t (s)", "Vị trí đỉnh xung (m)", "Li độ dải băng (cm)"],
        "hang": [[t, round(5.0 * t, 2), round(15 * math.exp(-((2.5 - 5.0 * t) / 0.4) ** 2), 1)] for t in (0.0, 0.4, 0.5, 0.6, 0.8)],
        "ghi_chu": "Tính từ mô hình với A = 15 cm, v = 5 m/s, w = 0,4 m; số minh hoạ, không phải số đo thật.",
    },
    "ket_qua_ky_vong": "Dải băng lên tới 15 cm đúng lúc đỉnh xung đi qua (t = 0,5 s) rồi về 0; hoành độ dải băng giữ nguyên 2,5 m.",
    "hien_tuong_hay_sai": ["Tưởng dải băng bị cuốn theo 'cái bướu' tới cột.",
                           "Gọi là sóng ngang vì dây nằm ngang (đúng ra vì dao động vuông góc phương truyền)."],
    "goi_y_mo_phong": {"loai": "2d_dong_hoc", "dieu_khien": ["A", "v"], "dau_ra": ["xung chạy trên dây", "dải băng lên xuống tại chỗ"],
                       "hinh_trong_bai": "Hình 2",
                       "y_tuong": "Hỏi trước: dải băng có tới được cột không? Rồi cho chạy, vẽ vệt hoành độ dải băng (một đường thẳng đứng)."},
})

# ---------- 02: lò xo slinky — sóng dọc, vùng nén – dãn (định tính) ----------
tn2 = dict(CHUNG, **{
    "id": "tn-l11-songngangdoc-02",
    "ten": "Sóng dọc trên lò xo slinky: vùng nén – dãn chạy, vòng đánh dấu tiến – lùi tại chỗ",
    "loai": "thi_nghiem", "muc_do": "co_ban",
    "kien_thuc": ["song.song_doc", "song.vung_nen_dan", "song.phan_tu_dao_dong_tai_cho"],
    "muc_tieu": "Thấy các vòng lò xo dao động dọc theo phương truyền, sóng lan đi thành chuỗi vùng nén và vùng dãn.",
    "dung_cu": [
        {"ten": "Lò xo slinky (lò xo ống mềm, dài)", "so_luong": 1},
        {"ten": "Băng dính màu", "so_luong": 1},
        {"ten": "Sàn nhẵn hoặc mặt bàn dài", "so_luong": 1},
    ],
    "cac_buoc": {
        "lam": ["Hai bạn giữ hai đầu lò xo trên sàn, kéo dãn dài khoảng 4 m.", "Dán băng dính màu vào một vòng ở giữa.",
                "Một bạn đẩy – kéo đầu lò xo dọc theo trục, đều tay."],
        "quan_sat": ["Chỗ các vòng sít nhau (nén) và chỗ thưa ra (dãn) chạy dọc lò xo tới đầu kia.",
                     "Vòng có băng màu chỉ tiến – lùi quanh chỗ cũ."],
        "rut_ra": ["Vòng dao động dọc theo phương truyền: sóng dọc.", "Lực đàn hồi giữa các vòng làm chỗ nén – dãn lan đi."],
    },
    "tham_so": [
        {"ky_hieu": "f", "ten": "Tần số đẩy – kéo", "don_vi": "Hz", "kieu": "dieu_chinh", "min": 1, "max": 5, "mac_dinh": 2, "buoc": 0.5},
        {"ky_hieu": "a", "ten": "Biên độ đẩy – kéo", "don_vi": "cm", "kieu": "dieu_chinh", "min": 2, "max": 10, "mac_dinh": 5, "buoc": 1},
        {"ky_hieu": "v", "ten": "Tốc độ sóng dọc trên lò xo", "don_vi": "m/s", "kieu": "co_dinh", "gia_tri": 7.0},
        {"ky_hieu": "λ", "ten": "Khoảng cách hai vùng nén liên tiếp", "don_vi": "m", "kieu": "tinh_ra"},
    ],
    "mo_hinh": {
        "phuong_trinh": ["u(x, t) = a·cos(2πf·(t − x/v)) — u là độ lệch DỌC trục của vòng ở vị trí cân bằng x",
                         "λ = v/f", "vùng nén: u = 0 và ∂u/∂x < 0; vùng dãn: u = 0 và ∂u/∂x > 0"],
        "gia_thiet": ["bỏ qua ma sát với sàn và tắt dần", "a·2π/λ < 1 để các vòng không chạm nhau"],
    },
    "so_lieu_mau": {
        "cot": ["f (Hz)", "λ = v/f (m)", "Nén – dãn gần nhất (m)"],
        "hang": [[f, round(7.0 / f, 2), round(7.0 / f / 2, 2)] for f in (1.0, 2.0, 3.5, 5.0)],
        "ghi_chu": "Tính từ mô hình với v = 7,0 m/s (khớp tn-l11-songngangdoc-03); số minh hoạ.",
    },
    "ket_qua_ky_vong": "Đẩy – kéo nhanh gấp đôi thì các vùng nén sít lại gần nhau gấp đôi (λ giảm một nửa); vòng đánh dấu chỉ tiến – lùi ±a.",
    "hien_tuong_hay_sai": ["Tưởng vùng nén ứng với đỉnh đồ thị u – x (thực ra ở điểm u = 0, đồ thị đi xuống).",
                           "Tưởng vòng đánh dấu bị đẩy dần tới đầu kia lò xo."],
    "goi_y_mo_phong": {"loai": "2d_dong_hoc+do_thi", "dieu_khien": ["f", "a"],
                       "dau_ra": ["các vòng lò xo dao động dọc trục", "đồ thị u – x đặt ngay trên lò xo"],
                       "hinh_trong_bai": "Hình 3, Hình 4",
                       "y_tuong": "Bật/tắt đồ thị u – x phía trên lò xo; đường gióng từ các điểm u = 0 xuống chỗ vòng sít và thưa."},
})

# ---------- 03: đo tốc độ xung trên lò xo bằng bấm giờ đi – về (có bảng) ----------
L = 4.00          # m, khoảng cách hai tay
V_MO_HINH = 7.0   # m/s
T_THAT = 2 * L / V_MO_HINH   # 1,143 s
# Sai số bấm tay (phản xạ ~0,1 s đầu + cuối): độ lệch minh hoạ cộng vào T_THAT, làm tròn theo độ chia 0,01 s.
LECH = [0.037, -0.053, 0.067, -0.013, 0.017]
T_DO = [round(T_THAT + e, 2) for e in LECH]
assert T_DO == [1.18, 1.09, 1.21, 1.13, 1.16], T_DO
assert all(abs(t - T_THAT) <= 0.1 for t in T_DO)
TB = sum(T_DO) / len(T_DO)
V_DO = 2 * L / TB
tn3 = dict(CHUNG, **{
    "id": "tn-l11-songngangdoc-03",
    "ten": "Đo tốc độ xung dọc trên lò xo slinky bằng bấm giờ xung đi – về",
    "loai": "thi_nghiem", "muc_do": "trung_binh",
    "kien_thuc": ["song.toc_do_truyen_song", "song.song_doc", "do_luong.sai_so_ngau_nhien"],
    "muc_tieu": "Đo thời gian xung nén chạy đi – về trên lò xo căng 4,00 m, 5 lần, tính tốc độ truyền sóng và nhận xét sai số do bấm tay.",
    "dung_cu": [
        {"ten": "Lò xo slinky", "so_luong": 1},
        {"ten": "Thước cuộn (độ chia 1 cm)", "so_luong": 1},
        {"ten": "Đồng hồ bấm giây (điện thoại, độ chia 0,01 s)", "so_luong": 1},
    ],
    "cac_buoc": {
        "lam": ["Căng lò xo giữa tay bạn A và bạn B, cách nhau L = 4,00 m.",
                "Bạn A đẩy mạnh một cái tạo một xung nén, đồng thời bấm đồng hồ.",
                "Xung chạy tới tay B, dội lại; xung về tới tay A thì bấm dừng.",
                "Làm 5 lần."],
        "quan_sat": ["Xung đi hết 2L = 8,00 m trong khoảng 1,1 – 1,2 s.",
                     "Năm lần đo lệch nhau vài phần trăm."],
        "rut_ra": ["v = 2L / t_tb = 8,00 / " + f"{TB:.3f}".replace(".", ",") + " ≈ " + f"{V_DO:.1f}".replace(".", ",") + " m/s.",
                   "Sai số chủ yếu do phản xạ tay khi bấm đồng hồ; đo đi – về làm sai số tỉ đối giảm một nửa so với đo một lượt."],
    },
    "tham_so": [
        {"ky_hieu": "L", "ten": "Khoảng cách hai tay", "don_vi": "m", "kieu": "co_dinh", "gia_tri": L},
        {"ky_hieu": "v", "ten": "Tốc độ sóng dọc trên lò xo (mô hình)", "don_vi": "m/s", "kieu": "dieu_chinh", "min": 4, "max": 10, "mac_dinh": V_MO_HINH, "buoc": 0.5},
        {"ky_hieu": "t", "ten": "Thời gian xung đi – về", "don_vi": "s", "kieu": "do_duoc", "sai_so_do": 0.1},
        {"ky_hieu": "v_do", "ten": "Tốc độ tính từ số đo", "don_vi": "m/s", "kieu": "tinh_ra"},
    ],
    "mo_hinh": {
        "phuong_trinh": ["t = 2L/v", "v_do = 2L/t_tb"],
        "gia_thiet": ["xung không đổi tốc độ khi phản xạ ở tay B", "sai số bấm tay ngẫu nhiên trong khoảng ±0,1 s"],
    },
    "so_lieu_mau": {
        "cot": ["Lần đo", "t đi – về (s)"],
        "hang": [[i + 1, t] for i, t in enumerate(T_DO)],
        "ghi_chu": f"Số minh hoạ, không phải số đo thật: t thật = 2L/v = {T_THAT:.3f} s với v = 7,0 m/s, cộng độ lệch bấm tay ≤ 0,07 s; trung bình {TB:.3f} s, v ≈ {V_DO:.2f} m/s.",
    },
    "ket_qua_ky_vong": f"t_tb = {TB:.3f} s; v ≈ {V_DO:.1f} m/s, lệch dưới 1 % so với mô hình 7,0 m/s.",
    "hien_tuong_hay_sai": ["Chia L cho t (quên xung đã đi cả lượt về), ra v nhỏ đi một nửa.",
                           "Tưởng vòng lò xo chạy theo xung tới tay B rồi về."],
    "sai_so_thuong_gap": ["Phản xạ tay khi bấm đồng hồ ~0,1 s ở cả lúc bắt đầu và lúc dừng.",
                          "Khó thấy đúng lúc xung về tới tay; xung yếu dần sau khi dội."],
    "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu", "dieu_khien": ["v"],
                       "dau_ra": ["xung chạy đi – về", "bảng 5 lần đo có nhiễu bấm tay"],
                       "y_tuong": "Cho học sinh tự bấm nút 'Bắt đầu'/'Dừng' theo mắt, ghi 5 lần, so trung bình với giá trị mô hình.",
                       "diem_nhan": "Hỏi trước: tính v bằng L/t hay 2L/t?"},
})

for d in (tn1, tn2, tn3):
    (OUT / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf8")
    print("ghi", d["id"])
