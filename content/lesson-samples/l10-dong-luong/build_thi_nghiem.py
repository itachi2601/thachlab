"""Ghi 3 file thí nghiệm của bài 'Động lượng' (lesson 73) vào content/thi-nghiem/.
Số liệu mẫu TÍNH bằng script từ chính mô hình khai trong file (không gõ tay).
Chạy: python3 build_thi_nghiem.py (trước build_figs.py — build_figs đọc lại tn-01 để đối chiếu bảng)."""
import json, math, pathlib

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parents[1] / "thi-nghiem"
G = 9.8
CHUNG = {"mon": "vat-ly", "lop": 10, "bai": "Bài 28. Động lượng", "lesson_id": 73,
         "nguon_trong_bai": "content/lesson-samples/l10-dong-luong/theory.html"}

# ---------- 01: xe trên ray đệm khí bật vào đệm lò xo, đo Δp bằng cổng quang, xung lượng bằng cảm biến lực ----------
M1 = 0.250
CHAY = [(0.40, -0.32, 0.176), (0.60, -0.49, 0.268), (0.80, -0.63, 0.352), (1.00, -0.81, 0.445)]  # v1, v2 (cổng quang), số đọc cảm biến
hang1 = []
for v1, v2, s in CHAY:
    dp = M1 * (v2 - v1)
    assert abs(abs(dp) - s) / abs(dp) < 0.03, (v1, v2, s)      # chênh < 3 %: trong sai số dụng cụ
    hang1.append([v1, v2, s])
tn1 = dict(CHUNG, **{
    "id": "tn-l10-dongluong-01",
    "ten": "Đo độ biến thiên động lượng và xung lượng khi xe bật vào đệm lò xo",
    "loai": "thi_nghiem", "muc_do": "trung_binh",
    "kien_thuc": ["dongluong.do_bien_thien_dong_luong", "dongluong.xung_luong", "dongluong.dinh_ly_xung_luong"],
    "muc_tieu": "Xe 0,250 kg chạy trên ray đệm khí, bật ngược lại khi va vào đệm lò xo gắn cảm biến lực; so sánh Δp tính từ hai lần đo tốc độ với xung lượng cảm biến ghi được, thấy Δp = F·Δt.",
    "dung_cu": [
        {"ten": "Ray đệm khí kèm bơm khí", "so_luong": 1},
        {"ten": "Xe trượt 0,250 kg có tấm chắn sáng", "so_luong": 1},
        {"ten": "Cổng quang điện + đồng hồ đo thời gian hiện số", "so_luong": 1},
        {"ten": "Cảm biến lực nối máy tính, đầu gắn đệm lò xo (nếu trường có)", "so_luong": 1},
    ],
    "cac_buoc": {
        "lam": [
            "Đặt cổng quang gần đầu ray có đệm lò xo gắn cảm biến lực. Chọn chiều dương là chiều xe chạy tới đệm.",
            "Đẩy xe cho chạy tới đệm; cổng quang đo tốc độ v1 lúc tới và v2 lúc bật ngược lại.",
            "Cảm biến lực vẽ đồ thị F theo t; phần mềm tính diện tích dưới đồ thị (xung lượng).",
            "Lặp lại 4 lần với tốc độ đẩy tăng dần.",
        ],
        "quan_sat": [
            "v2 luôn ngược dấu v1 và nhỏ hơn về độ lớn (xe bật lại chậm hơn).",
            "Xung lượng đo được tăng theo tốc độ đẩy: 0,176; 0,268; 0,352; 0,445 N·s.",
        ],
        "rut_ra": [
            "Độ lớn m(v2 − v1) khớp xung lượng cảm biến trong khoảng 1,5–2,2 %: Δp = F·Δt.",
            "Δp và xung lượng của đệm cùng hướng: ngược chiều xe chạy tới.",
        ],
    },
    "tham_so": [
        {"ky_hieu": "v1", "ten": "Tốc độ xe lúc chạy tới đệm", "don_vi": "m/s", "kieu": "dieu_chinh", "min": 0.2, "max": 1.2, "mac_dinh": 0.6, "buoc": 0.1},
        {"ky_hieu": "e", "ten": "Tỉ số tốc độ bật lại / tốc độ tới của đệm lò xo", "don_vi": "", "kieu": "dieu_chinh", "min": 0.0, "max": 1.0, "mac_dinh": 0.8, "buoc": 0.05},
        {"ky_hieu": "m", "ten": "Khối lượng xe", "don_vi": "kg", "kieu": "co_dinh", "gia_tri": M1},
        {"ky_hieu": "v2", "ten": "Vận tốc xe lúc bật lại (âm)", "don_vi": "m/s", "kieu": "do_duoc", "sai_so_do": 0.01},
        {"ky_hieu": "J", "ten": "Xung lượng cảm biến ghi được", "don_vi": "N·s", "kieu": "do_duoc", "sai_so_do": "2 %"},
        {"ky_hieu": "dp", "ten": "Độ biến thiên động lượng m(v2 − v1)", "don_vi": "kg·m/s", "kieu": "tinh_ra"},
    ],
    "mo_hinh": {
        "phuong_trinh": ["v2 = −e·v1", "Δp = m·(v2 − v1)", "J = ∫F dt = Δp (bỏ qua ma sát trên ray)"],
        "gia_thiet": ["ray nằm ngang, đệm khí làm ma sát không đáng kể", "chỉ lực đệm tác dụng theo phương ngang trong lúc va chạm"],
    },
    "so_lieu_mau": {
        "cot": ["v1 (m/s)", "v2 (m/s)", "Xung lượng cảm biến (N·s)"],
        "hang": hang1,
        "ghi_chu": "Số liệu minh hoạ, không phải số đo thật: v2 ứng với e ≈ 0,79–0,82; Δp = m(v2 − v1) cho 0,180; 0,2725; 0,3575; 0,4525 kg·m/s; số cảm biến nhỏ hơn đều 1,5–2,2 % (cảm biến lấy mẫu sót phần đầu, cuối của xung).",
    },
    "ket_qua_ky_vong": "|Δp| khớp xung lượng cảm biến, chênh dưới 2,5 %; cả 4 lần cảm biến đều nhỏ hơn một chút (sai số hệ thống).",
    "hien_tuong_hay_sai": [
        "Tính Δp bằng hiệu tốc độ 0,40 − 0,32 (quên v2 ngược chiều), ra 0,02 kg·m/s.",
        "Cho rằng xe bật lại nên lực của đệm cùng chiều xe chạy tới.",
    ],
    "sai_so_thuong_gap": [
        "Cổng quang ±0,01 m/s cho mỗi tốc độ, nên Δp sai cỡ ±0,005 kg·m/s.",
        "Cảm biến lực ±2 %, lấy mẫu thưa làm sót phần đầu và cuối của xung.",
    ],
    "goi_y_mo_phong": {
        "loai": "2d_dong_hoc+do_thi+bang_so_lieu",
        "y_tuong": "Thanh trượt v1 và e; xe chạy tới đệm, đồ thị F(t) hiện vùng tô màu bằng Δp; vector p trước, p sau và Δp vẽ cạnh nhau.",
        "diem_nhan": "Hỏi trước: xe tới 0,40 m/s, bật lại 0,32 m/s — Δp bằng 0,02 hay 0,18 kg·m/s?",
    },
})

# ---------- 02: bi lăn từ máng nghiêng va vào khúc gỗ ----------
CAU_HINH = [(0.050, 0.10), (0.050, 0.20), (0.100, 0.10), (0.100, 0.20)]   # m (kg), h (m)
hang2 = []
for m, h in CAU_HINH:
    v = math.sqrt(10 * G * h / 7)        # bi đặc lăn không trượt
    hang2.append([m, h, round(v, 2), round(m * v, 3)])
tn2 = dict(CHUNG, **{
    "id": "tn-l10-dongluong-02",
    "ten": "Bi lăn từ máng nghiêng va vào khúc gỗ",
    "loai": "thi_nghiem", "muc_do": "co_ban",
    "kien_thuc": ["dongluong.dinh_nghia", "dongluong.phu_thuoc_m_va_v"],
    "muc_tieu": "Thấy khả năng truyền chuyển động của viên bi cho khúc gỗ tăng khi bi nặng hơn hoặc lăn nhanh hơn: dẫn tới đại lượng p = mv.",
    "dung_cu": [
        {"ten": "Máng nghiêng có vạch độ cao", "so_luong": 1},
        {"ten": "Bi thép 50 g và 100 g", "so_luong": 2},
        {"ten": "Khúc gỗ nhỏ đặt ở chân máng", "so_luong": 1},
        {"ten": "Thước đo độ dịch chuyển", "so_luong": 1},
    ],
    "cac_buoc": {
        "lam": [
            "Thả bi 50 g từ độ cao 10 cm rồi 20 cm; đo quãng khúc gỗ bị đẩy đi.",
            "Đổi sang bi 100 g, thả lại từ 10 cm và 20 cm.",
        ],
        "quan_sat": [
            "Cùng bi, thả cao hơn (bi tới nhanh hơn) thì khúc gỗ đi xa hơn.",
            "Cùng độ cao, bi nặng hơn thì khúc gỗ đi xa hơn.",
        ],
        "rut_ra": [
            "Khả năng truyền chuyển động phụ thuộc cả khối lượng lẫn vận tốc: gộp thành p = mv.",
        ],
    },
    "tham_so": [
        {"ky_hieu": "m", "ten": "Khối lượng bi", "don_vi": "kg", "kieu": "dieu_chinh", "min": 0.02, "max": 0.2, "mac_dinh": 0.05, "buoc": 0.01},
        {"ky_hieu": "h", "ten": "Độ cao thả bi", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.05, "max": 0.3, "mac_dinh": 0.1, "buoc": 0.05},
        {"ky_hieu": "g", "ten": "Gia tốc trọng trường", "don_vi": "m/s²", "kieu": "co_dinh", "gia_tri": G},
        {"ky_hieu": "v", "ten": "Tốc độ bi ở chân máng", "don_vi": "m/s", "kieu": "tinh_ra"},
        {"ky_hieu": "p", "ten": "Động lượng bi ngay trước va chạm", "don_vi": "kg·m/s", "kieu": "tinh_ra"},
    ],
    "mo_hinh": {
        "phuong_trinh": ["v = √(10·g·h/7) (bi đặc lăn không trượt)", "p = m·v"],
        "gia_thiet": ["bi lăn không trượt, bỏ qua ma sát lăn", "khúc gỗ giống nhau ở mọi lần thả"],
    },
    "so_lieu_mau": {
        "cot": ["m (kg)", "h (m)", "v (m/s)", "p (kg·m/s)"],
        "hang": hang2,
        "ghi_chu": "Số tính từ mô hình, không phải số đo; thí nghiệm trên lớp chỉ cần so sánh quãng đi của khúc gỗ (định tính).",
    },
    "ket_qua_ky_vong": "Khúc gỗ đi xa nhất khi bi 100 g thả từ 20 cm (p lớn nhất), gần nhất khi bi 50 g thả từ 10 cm.",
    "hien_tuong_hay_sai": [
        "Cho rằng chỉ tốc độ quyết định (bi nào nhanh hơn thì đẩy mạnh hơn).",
        "Cho rằng bi nặng gấp đôi thì lăn xuống nhanh gấp đôi.",
    ],
    "goi_y_mo_phong": {
        "loai": "2d_dong_hoc+bang_so_lieu",
        "y_tuong": "Hai thanh trượt m và h; bi lăn xuống va khúc gỗ, hiện p của bi và quãng khúc gỗ đi.",
        "diem_nhan": "Hỏi trước: bi 50 g thả 20 cm hay bi 100 g thả 10 cm đẩy khúc gỗ xa hơn?",
    },
})

# ---------- 03: ví dụ — đỡ cùng một Δp bằng mặt cứng và mặt mềm (đồ thị F–t) ----------
DP3, T_CUNG, T_MEM = 0.45, 0.010, 0.040        # N·s, s
F_cung = math.pi * DP3 / (2 * T_CUNG)          # xung nửa hình sin: diện tích = 2·Fmax·T/π
F_mem = math.pi * DP3 / (2 * T_MEM)
tn3 = dict(CHUNG, **{
    "id": "tn-l10-dongluong-03",
    "ten": "Cùng độ biến thiên động lượng: mặt cứng và mặt mềm",
    "loai": "vi_du", "muc_do": "trung_binh",
    "kien_thuc": ["dongluong.dinh_ly_xung_luong", "dongluong.keo_dai_thoi_gian_giam_luc"],
    "muc_tieu": "Một vật dừng lại với cùng Δp trên mặt cứng (Δt ngắn) và mặt mềm (Δt dài): diện tích dưới đồ thị F–t bằng nhau, lực cực đại trên mặt mềm nhỏ hơn nhiều.",
    "dung_cu": [
        {"ten": "Quả bóng hoặc túi cát nhỏ", "so_luong": 1},
        {"ten": "Mặt bàn cứng và tấm đệm xốp", "so_luong": 1},
        {"ten": "Cảm biến lực (tuỳ chọn) để vẽ đồ thị F–t", "so_luong": 1},
    ],
    "cac_buoc": {
        "lam": ["Thả cùng một túi cát từ cùng độ cao xuống mặt cứng rồi xuống tấm đệm xốp (nếu có cảm biến lực thì đặt dưới mặt đỡ)."],
        "quan_sat": ["Trên mặt cứng: tiếng 'bộp' gọn, đồ thị F–t là xung hẹp và cao. Trên đệm: lún sâu, đồ thị thấp và rộng."],
        "rut_ra": ["Δp như nhau nên diện tích dưới hai đồ thị bằng nhau; kéo dài Δt thì lực trung bình giảm."],
    },
    "tham_so": [
        {"ky_hieu": "dt", "ten": "Thời gian va chạm", "don_vi": "s", "kieu": "dieu_chinh", "min": 0.005, "max": 0.2, "mac_dinh": 0.04, "buoc": 0.005},
        {"ky_hieu": "dp", "ten": "Độ lớn độ biến thiên động lượng", "don_vi": "kg·m/s", "kieu": "co_dinh", "gia_tri": DP3},
        {"ky_hieu": "F_tb", "ten": "Lực trung bình", "don_vi": "N", "kieu": "tinh_ra"},
        {"ky_hieu": "F_max", "ten": "Lực cực đại (xung nửa hình sin)", "don_vi": "N", "kieu": "tinh_ra"},
    ],
    "mo_hinh": {
        "phuong_trinh": ["F_tb = Δp/Δt", "F(t) = F_max·sin(πt/Δt), 0 ≤ t ≤ Δt", "F_max = π·Δp/(2·Δt)"],
        "gia_thiet": ["bỏ qua trọng lực so với lực va chạm", "dạng xung nửa hình sin chỉ để vẽ minh hoạ"],
    },
    "so_lieu_mau": {
        "cot": ["Δt (s)", "F_tb (N)", "F_max (N)"],
        "hang": [[T_CUNG, round(DP3 / T_CUNG, 1), round(F_cung, 1)], [T_MEM, round(DP3 / T_MEM, 2), round(F_mem, 1)]],
        "ghi_chu": "Số minh hoạ cho Δp = 0,45 kg·m/s; hai dòng ứng với hai đồ thị của Hình 3 trong bài.",
    },
    "ket_qua_ky_vong": "Kéo Δt dài gấp 4 thì lực trung bình và lực cực đại đều nhỏ đi 4 lần; Δp không đổi.",
    "hien_tuong_hay_sai": [
        "Cho rằng đệm mềm làm giảm độ biến thiên động lượng.",
        "Cho rằng đệm mềm làm vật dừng 'nhẹ nhàng' vì xung lượng nhỏ hơn.",
    ],
    "goi_y_mo_phong": {
        "loai": "do_thi+bang_so_lieu",
        "y_tuong": "Thanh trượt Δt; vẽ xung F(t) với diện tích cố định bằng Δp, đọc F_tb và F_max.",
        "diem_nhan": "Hỏi trước: đổi sang đệm mềm thì diện tích dưới đồ thị tăng, giảm hay giữ nguyên?",
    },
})

for d in (tn1, tn2, tn3):
    (OUT / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf8")
    print("ghi", d["id"])
