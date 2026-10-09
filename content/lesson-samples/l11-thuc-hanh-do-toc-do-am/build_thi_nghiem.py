#!/usr/bin/env python3
"""Sinh 3 file content/thi-nghiem/tn-l11-dotocdoam-NN.json từ mô hình vật lí (số liệu tính, không gõ tay).
Chạy lại được; ghi đè đúng 3 file của bài này. Số liệu 01 phải khớp bảng trong theory.src.html (5 lần đo)."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "content" / "thi-nghiem"
BAI = "Bài 15. Thực hành: Đo tốc độ truyền âm"
SRC = "content/lesson-samples/l11-thuc-hanh-do-toc-do-am/theory.html"
COMMON = {"mon": "vat-ly", "lop": 11, "bai": BAI, "lesson_id": 34, "nguon_trong_bai": SRC}

# ---------- mô hình ống cộng hưởng
F, T, E_CM, L_ONG = 500, 20, 0.5, 67.0
V = 331 + 0.6 * T                                    # 343 m/s
LAM = V / F * 100                                    # 68,6 cm
M1, M2 = LAM / 4 - E_CM, 3 * LAM / 4 - E_CM          # 16,65 ; 50,95 cm
assert abs(V - 343) < 1e-9 and abs(M1 - 16.65) < 1e-9 and abs(M2 - 50.95) < 1e-9
assert 5 * LAM / 4 - E_CM > L_ONG                    # ống 67 cm chỉ có hai vị trí cộng hưởng ở 500 Hz
L1 = [16.8, 16.7, 16.8, 16.6, 16.7]
L2 = [50.8, 50.9, 50.9, 50.8, 51.0]
for a in L1:
    assert abs(a - M1) <= 0.2 + 1e-9, a              # sai số đọc ±2 mm quanh mô hình
for b in L2:
    assert abs(b - M2) <= 0.2 + 1e-9, b
hang = []
for i, (a, b) in enumerate(zip(L1, L2), 1):
    lam = 2 * (b - a)
    hang.append([i, a, b, round(lam, 1), round(lam / 100 * F)])
vs = [h[4] for h in hang]
vtb = sum(vs) / 5
assert vs == [340, 342, 341, 342, 343] and abs(vtb - 341.6) < 1e-9
m1, m2 = sum(L1) / 5, sum(L2) / 5
d1, d2 = sum(abs(x - m1) for x in L1) / 5, sum(abs(x - m2) for x in L2) / 5
lam_tb = 2 * (m2 - m1)
rel = 2 * (d1 + d2) / lam_tb + 1 / F
dv = vtb * rel
assert abs(m1 - 16.72) < 1e-9 and abs(m2 - 50.88) < 1e-9 and abs(lam_tb - 68.32) < 1e-9 and abs(dv - 1.96) < 0.01

tn1 = {
    **COMMON,
    "id": "tn-l11-dotocdoam-01",
    "ten": "Đo tốc độ truyền âm trong không khí bằng ống cộng hưởng một đầu kín",
    "loai": "thi_nghiem", "muc_do": "trung_binh",
    "kien_thuc": ["am.toc_do_truyen_am", "song_dung.ong_mot_dau_kin", "am.xu_ly_so_lieu_sai_so"],
    "muc_tieu": "Đo hai chiều dài cột khí l1, l2 tại hai lần cộng hưởng liên tiếp ở tần số f đã biết, tính λ = 2(l2 − l1) và v = λf, viết v = v̄ ± Δv rồi so với giá trị tham khảo.",
    "dung_cu": [
        {"ten": "Máy phát tần số (tín hiệu sin) và loa điện động", "so_luong": 1, "ghi_chu": "đặt loa sát miệng ống; f = 500 ± 1 Hz"},
        {"ten": "Ống trụ trong suốt đường kính trong 16 mm, dài 670 mm, gắn thước (bộ của trường dùng ống 40 mm thì e lớn hơn, số liệu khác)", "so_luong": 1, "ghi_chu": "số 0 của thước ở miệng ống"},
        {"ten": "Bình nước nối ống mềm với đáy ống (hoặc pít-tông có vạch chuẩn)", "so_luong": 1, "ghi_chu": "mặt nước ở ống và ở bình luôn cùng độ cao"},
        {"ten": "Giá đỡ", "so_luong": 1},
    ],
    "cac_buoc": {
        "lam": [
            "Chỉnh máy phát f = 500 Hz, âm vừa đủ nghe; đặt loa sát miệng ống.",
            "Hạ từ từ bình nước, dừng ở chỗ nghe to nhất lần đầu, đọc l1 ngay tại mặt nước, mắt ngang mặt nước.",
            "Hạ tiếp tới lần to nhất thứ hai, đọc l2.",
            "Đưa nước về sát miệng ống, lặp lại để có đủ 5 lần đo.",
            "Tính λ = 2(l2 − l1), v = λf cho từng lần; lấy trung bình; tính Δλ = 2(Δl1 + Δl2), Δv/v = Δλ/λ + Δf/f.",
        ],
        "quan_sat": [
            "Trong ống dài 670 mm chỉ có hai vị trí nghe to nhất, cỡ 17 cm và 51 cm tính từ miệng ống.",
            "Năm lần đo cho l1, l2 lệch nhau vài mm; v các lần từ 340 đến 343 m/s.",
        ],
        "rut_ra": [
            "Hiệu l2 − l1 gần như không đổi; λ̄ = 68,32 cm, v̄ = 341,6 m/s.",
            f"Δv ≈ {dv:.1f} m/s nên v = 341,6 ± 2,0 m/s; giá trị tham khảo 343 m/s nằm trong khoảng 339,6 đến 343,6 m/s.",
        ],
    },
    "tham_so": [
        {"ky_hieu": "f", "ten": "Tần số máy phát", "don_vi": "Hz", "kieu": "dieu_chinh", "min": 200, "max": 1000, "mac_dinh": 500, "buoc": 50},
        {"ky_hieu": "t", "ten": "Nhiệt độ phòng", "don_vi": "°C", "kieu": "dieu_chinh", "min": 0, "max": 40, "mac_dinh": 20, "buoc": 1},
        {"ky_hieu": "e", "ten": "Hiệu chỉnh đầu hở", "don_vi": "cm", "kieu": "dieu_chinh", "min": 0, "max": 1.5, "mac_dinh": 0.5, "buoc": 0.1},
        {"ky_hieu": "L", "ten": "Chiều dài ống", "don_vi": "cm", "kieu": "co_dinh", "gia_tri": 67.0},
        {"ky_hieu": "l1", "ten": "Cột khí ở lần cộng hưởng thứ nhất", "don_vi": "cm", "kieu": "do_duoc", "sai_so_do": 0.2},
        {"ky_hieu": "l2", "ten": "Cột khí ở lần cộng hưởng thứ hai", "don_vi": "cm", "kieu": "do_duoc", "sai_so_do": 0.2},
        {"ky_hieu": "v", "ten": "Tốc độ truyền âm", "don_vi": "m/s", "kieu": "tinh_ra"},
        {"ky_hieu": "lambda", "ten": "Bước sóng", "don_vi": "cm", "kieu": "tinh_ra"},
    ],
    "mo_hinh": {
        "phuong_trinh": [
            "v = 331 + 0,6·t (m/s)",
            "λ = v/f",
            "l1 + e = λ/4 ; l2 + e = 3λ/4",
            "λ = 2(l2 − l1) ; v = λf",
            "Δλ = 2(Δl1 + Δl2) ; Δv/v = Δλ/λ + Δf/f",
        ],
        "gia_thiet": [
            "không khí khô, nhiệt độ đều trong ống",
            "e ≈ 0,6·bán kính ống = 0,5 cm với ống 16 mm, không đổi giữa hai lần cộng hưởng",
            "mặt bích hay loa sát miệng làm e lớn hơn 0,6r; sai số đọc ±2 mm quanh giá trị mô hình",
        ],
    },
    "so_lieu_mau": {
        "cot": ["Lần", "l1 (cm)", "l2 (cm)", "λ (cm)", "v (m/s)"],
        "hang": hang,
        "ghi_chu": "Số liệu minh hoạ sinh từ mô hình (v = 343 m/s, e = 0,5 cm, f = 500 Hz) cộng sai số đọc tới ±0,2 cm; không phải số đo thật.",
    },
    "ket_qua_ky_vong": f"l̄1 = 16,72 cm, l̄2 = 50,88 cm, λ̄ = 68,32 cm, v̄ = 341,6 m/s, Δv ≈ {dv:.1f} m/s; v = 341,6 ± 2,0 m/s, phù hợp 343 m/s.",
    "hien_tuong_hay_sai": [
        "Coi λ = 4·l1 (quên hiệu chỉnh đầu hở e): v lệch thấp khoảng 9 m/s.",
        "Nhầm khoảng cách hai lần cộng hưởng liên tiếp là λ thay vì λ/2.",
        "Cho rằng đổi tần số thì tốc độ truyền âm đổi theo.",
        "Đọc vạch ở mép bình hay đỉnh ống thay vì ở mặt nước.",
    ],
    "goi_y_mo_phong": {
        "loai": "2d_dong_hoc+do_thi+bang_so_lieu",
        "dieu_khien": ["f", "t", "e"],
        "dau_ra": ["cột khí cộng hưởng l1, l2", "đồ thị độ to theo l", "v tính từ hiệu l2 − l1"],
        "hinh_trong_bai": "Hình 2, 3, 4",
        "y_tuong": "Kéo mực nước trong ống; độ to lên cực đại tại l1, l2; hiện hiệu l2 − l1 = λ/2 và v = λf; cho đổi f, t, e.",
    },
}

# ---------- chai nước
V_CH = 343.0
cot = [12, 16, 20]
f_ch = [round(V_CH / (4 * (l + 0.5) / 100)) for l in cot]
assert f_ch[0] > f_ch[1] > f_ch[2]
tn2 = {
    **COMMON,
    "id": "tn-l11-dotocdoam-02",
    "ten": "Thổi ngang miệng chai: cột không khí ngắn thì tiếng cao",
    "loai": "vi_du", "muc_do": "co_ban",
    "kien_thuc": ["am.cong_huong_cot_khi", "am.do_cao_tan_so"],
    "muc_tieu": "Thấy mực nước (chiều dài cột không khí) quyết định cao độ tiếng kêu của chai.",
    "dung_cu": [
        {"ten": "Chai nhựa giống nhau", "so_luong": 3},
        {"ten": "Nước", "so_luong": 1, "ghi_chu": "rót nhiều, vừa, ít"},
    ],
    "cac_buoc": {
        "lam": ["Rót nước vào ba chai: A nhiều nhất, B vừa, C ít nhất.", "Thổi ngang miệng từng chai và nghe cao độ."],
        "quan_sat": ["Chai A kêu cao nhất, chai C thấp nhất."],
        "rut_ra": ["Cột không khí phía trên mặt nước càng ngắn thì tần số cộng hưởng càng lớn, nghe càng cao."],
    },
    "tham_so": [
        {"ky_hieu": "l", "ten": "Chiều dài cột không khí", "don_vi": "cm", "kieu": "dieu_chinh", "min": 8, "max": 24, "mac_dinh": 16, "buoc": 1},
        {"ky_hieu": "e", "ten": "Hiệu chỉnh đầu hở", "don_vi": "cm", "kieu": "co_dinh", "gia_tri": 0.5},
        {"ky_hieu": "f", "ten": "Tần số cộng hưởng gần đúng", "don_vi": "Hz", "kieu": "tinh_ra"},
    ],
    "mo_hinh": {
        "phuong_trinh": ["f = v/(4·(l + e))", "v = 343 m/s"],
        "gia_thiet": ["coi cột không khí trong chai như ống một đầu kín", "chai thật còn chịu ảnh hưởng của thể tích nên tần số thật thấp hơn, xu hướng vẫn đúng"],
    },
    "so_lieu_mau": {
        "cot": ["Chai", "l (cm)", "f (Hz)"],
        "hang": [["A", cot[0], f_ch[0]], ["B", cot[1], f_ch[1]], ["C", cot[2], f_ch[2]]],
        "ghi_chu": "Số minh hoạ tính từ mô hình ống một đầu kín, không phải số đo thật.",
    },
    "ket_qua_ky_vong": "Chai ít không khí (A) có f lớn nhất, nghe cao nhất; chai nhiều không khí (C) nghe thấp nhất.",
    "hien_tuong_hay_sai": ["Cho rằng chai nặng hơn thì tiếng thấp hơn.", "Nhầm cao độ (tần số) với độ to."],
    "goi_y_mo_phong": {
        "loai": "2d_dong_hoc+bang_so_lieu",
        "dieu_khien": ["l"],
        "dau_ra": ["tần số f", "nốt nghe được"],
        "hinh_trong_bai": "Hình 1",
        "y_tuong": "Kéo mặt nước trong chai lên xuống, nghe và đọc f.",
    },
}

# ---------- hai micro
d = [2.00, 4.00, 6.00]
dt_ms = [5.8, 11.7, 17.5]
vv = [round(x / (t / 1000), 1) for x, t in zip(d, dt_ms)]
assert all(abs(x - 343) < 3 for x in vv), vv
tn3 = {
    **COMMON,
    "id": "tn-l11-dotocdoam-03",
    "ten": "Đo tốc độ truyền âm bằng độ trễ giữa hai micro",
    "loai": "thi_nghiem", "muc_do": "co_ban",
    "kien_thuc": ["am.toc_do_truyen_am", "am.do_tre_hai_micro"],
    "muc_tieu": "Nhận biết phương án đo v = d/Δt từ độ trễ của tiếng động giữa hai micro nối cùng một máy ghi.",
    "dung_cu": [
        {"ten": "Hai micro nối chung một máy ghi (hoặc máy tính)", "so_luong": 2},
        {"ten": "Thước dây", "so_luong": 1},
    ],
    "cac_buoc": {
        "lam": ["Đặt hai micro thẳng hàng với nguồn, cách nhau d = 6,00 m.", "Vỗ tay một cái sát micro thứ nhất và ghi âm."],
        "quan_sat": ["Đồ thị âm thanh có hai gai; gai thứ hai trễ Δt = 17,5 ms so với gai thứ nhất."],
        "rut_ra": ["v = d/Δt = 6,00/0,0175 ≈ 343 m/s. Hai điện thoại riêng lẻ không dùng được vì đồng hồ không đồng bộ."],
    },
    "tham_so": [
        {"ky_hieu": "d", "ten": "Khoảng cách hai micro", "don_vi": "m", "kieu": "dieu_chinh", "min": 1, "max": 10, "mac_dinh": 6, "buoc": 0.5},
        {"ky_hieu": "t", "ten": "Nhiệt độ phòng", "don_vi": "°C", "kieu": "dieu_chinh", "min": 0, "max": 40, "mac_dinh": 20, "buoc": 1},
        {"ky_hieu": "dt", "ten": "Độ trễ giữa hai gai", "don_vi": "ms", "kieu": "do_duoc", "sai_so_do": 0.1},
        {"ky_hieu": "v", "ten": "Tốc độ truyền âm", "don_vi": "m/s", "kieu": "tinh_ra"},
    ],
    "mo_hinh": {
        "phuong_trinh": ["v = d/Δt", "v = 331 + 0,6·t (m/s)"],
        "gia_thiet": ["tiếng vỗ tay phát ra ở một điểm sát micro thứ nhất", "hai micro dùng chung một đồng hồ ghi"],
    },
    "so_lieu_mau": {
        "cot": ["d (m)", "Δt (ms)", "v (m/s)"],
        "hang": [[a, b, c] for a, b, c in zip(d, dt_ms, vv)],
        "ghi_chu": "Số minh hoạ sinh từ mô hình v = 343 m/s, độ trễ làm tròn 0,1 ms; không phải số đo thật.",
    },
    "ket_qua_ky_vong": "Với d = 6,00 m, Δt = 17,5 ms: v ≈ 343 m/s. d càng ngắn thì Δt càng bé, sai số tỉ đối của v càng lớn.",
    "hien_tuong_hay_sai": ["Dùng hai điện thoại riêng lẻ nên đồng hồ lệch nhau.", "Đặt hai micro không thẳng hàng với nguồn nên d sai."],
    "goi_y_mo_phong": {
        "loai": "do_thi+bang_so_lieu",
        "dieu_khien": ["d", "t"],
        "dau_ra": ["hai gai âm", "Δt", "v"],
        "hinh_trong_bai": "Hộp thí nghiệm mục II.6",
        "y_tuong": "Kéo micro thứ hai ra xa, gai thứ hai lùi dần; hiện v = d/Δt.",
    },
}

for tn in (tn1, tn2, tn3):
    (OUT / f"{tn['id']}.json").write_text(json.dumps(tn, ensure_ascii=False, indent=1), encoding="utf8")
print("ok", [t["id"] for t in (tn1, tn2, tn3)], hang, vv, f_ch)
