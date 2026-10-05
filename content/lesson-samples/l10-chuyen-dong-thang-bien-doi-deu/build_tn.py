"""Sinh 3 file thí nghiệm/ví dụ cho bài 'Chuyển động thẳng biến đổi đều' (lesson 54) vào content/thi-nghiem/.
Mọi số liệu mẫu TÍNH từ chính mo_hinh của file (không gõ tay), rồi in ra để chép vào bảng trong theory.src.html.
Chạy: python3 build_tn.py"""
import json, math, pathlib

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parents[1] / "thi-nghiem"
BAI = "Bài 9. Chuyển động thẳng biến đổi đều"
SRC = "content/lesson-samples/l10-chuyen-dong-thang-bien-doi-deu/theory.html"


def base(n, ten, loai, muc_do, kt):
    return {"mon": "vat-ly", "lop": 10, "bai": BAI, "lesson_id": 54, "nguon_trong_bai": SRC,
            "id": f"tn-l10-ctbdd-{n:02d}", "ten": ten, "loai": loai, "muc_do": muc_do, "kien_thuc": kt}


def vn(x, nd=2):
    from decimal import Decimal, ROUND_HALF_UP
    q = Decimal(1).scaleb(-nd)
    return str(Decimal(repr(x)).quantize(q, rounding=ROUND_HALF_UP)).replace(".", ",")


# ---------- 01: xe lăn trên máng nghiêng, cổng quang điện (đo v theo t)
A, D = 0.50, 0.020                       # gia tốc mô hình (m/s²), bề rộng tấm chắn sáng (m)
S_POS = [0.10, 0.20, 0.40, 0.60]         # vị trí đặt cổng quang (m)
TAU_DOC = [0.064, 0.045, 0.032, 0.026]   # số đọc thời gian chắn sáng (đồng hồ chia 0,001 s)
T_DOC = [0.635, 0.892, 1.262, 1.551]     # số đọc t từ lúc thả
rows1 = []
for s, td, taud in zip(S_POS, T_DOC, TAU_DOC):
    t = math.sqrt(2 * s / A)
    v = A * t
    tau = D / v
    assert abs(td - t) < 0.005 and abs(taud - tau) <= 0.0011, (s, t, tau)   # nhiễu ≤ 1 vạch
    vdo = D / taud
    rows1.append([s, round(t, 4), round(tau, 4), td, taud, round(vdo, 4), round(vdo / td, 4)])
d1 = base(1, "Đo vận tốc xe lăn trên máng nghiêng bằng cổng quang điện: v tỉ lệ với t", "thi_nghiem", "trung_binh",
          ["ctbdd.v_bang_v0_cong_at", "ctbdd.do_thi_v_t", "ctbdd.gia_toc_khong_doi"])
d1.update({
    "muc_tieu": "Thả xe lăn từ nghỉ trên máng nghiêng, đo vận tốc tại 4 vị trí bằng cổng quang điện; thấy v tỉ lệ với t (đồ thị v–t là đường thẳng qua gốc), tính được a ≈ 0,5 m/s² và nhận xét sai số.",
    "dung_cu": [{"ten": "Máng nhôm dài ~1 m, kê nghiêng một góc nhỏ", "so_luong": 1},
                {"ten": "Xe lăn có gắn tấm chắn sáng rộng 2,00 cm", "so_luong": 1},
                {"ten": "Cổng quang điện", "so_luong": 2},
                {"ten": "Đồng hồ đo thời gian hiện số (chia 0,001 s)", "so_luong": 1},
                {"ten": "Thước mét", "so_luong": 1}],
    "cac_buoc": {
        "lam": ["Đặt cổng quang thứ nhất ngay chỗ thả xe để bấm giờ lúc xe bắt đầu chạy.",
                "Đặt cổng quang thứ hai lần lượt cách chỗ thả 10, 20, 40, 60 cm (4 lần đo); mỗi lần thả xe từ nghỉ.",
                "Đọc t (từ lúc thả tới cổng thứ hai) và τ (thời gian tấm chắn đi qua cổng thứ hai); tính v = d/τ."],
        "quan_sat": ["t càng lớn thì τ càng nhỏ, tức xe càng nhanh.",
                     "Thương v/t gần như không đổi, khoảng 0,49–0,50 m/s²."],
        "rut_ra": ["v tỉ lệ thuận với t: v = at với a không đổi — chuyển động nhanh dần đều.",
                   "Đồ thị v–t là đường thẳng qua gốc; độ dốc là a."]},
    "tham_so": [
        {"ky_hieu": "a", "ten": "Gia tốc của xe (do độ nghiêng máng)", "don_vi": "m/s²", "kieu": "dieu_chinh",
         "min": 0.2, "max": 1.0, "mac_dinh": 0.5, "buoc": 0.1},
        {"ky_hieu": "s", "ten": "Khoảng cách từ chỗ thả tới cổng quang", "don_vi": "m", "kieu": "dieu_chinh",
         "min": 0.1, "max": 0.8, "mac_dinh": 0.4, "buoc": 0.05},
        {"ky_hieu": "d", "ten": "Bề rộng tấm chắn sáng", "don_vi": "m", "kieu": "co_dinh", "gia_tri": D},
        {"ky_hieu": "t", "ten": "Thời gian từ lúc thả tới cổng", "don_vi": "s", "kieu": "do_duoc", "sai_so_do": 0.001},
        {"ky_hieu": "tau", "ten": "Thời gian chắn sáng", "don_vi": "s", "kieu": "do_duoc", "sai_so_do": 0.001},
        {"ky_hieu": "v", "ten": "Vận tốc tại cổng, v = d/τ", "don_vi": "m/s", "kieu": "tinh_ra"}],
    "mo_hinh": {"phuong_trinh": ["t = √(2s/a)", "v = a·t", "τ = d/v", "v (đo) = d/τ (đọc)"],
                "gia_thiet": ["thả từ nghỉ (v0 = 0)", "a không đổi dọc máng (bỏ qua ma sát thay đổi)",
                              "v = d/τ coi là vận tốc tức thời vì τ rất nhỏ", "a = 0,5 m/s² là giá trị minh hoạ"]},
    "so_lieu_mau": {"cot": ["s (m)", "t tính (s)", "τ tính (s)", "t đọc (s)", "τ đọc (s)", "v = d/τ (m/s)", "v/t (m/s²)"],
                    "hang": rows1,
                    "ghi_chu": "Số minh hoạ tính từ mô hình a = 0,5 m/s², d = 2,00 cm; số đọc lệch không quá 1 vạch (0,001 s) so với số tính."},
    "ket_qua_ky_vong": "v/t ≈ 0,49–0,50 m/s² ở cả 4 lần đo; hàng cuối có sai số tương đối của τ lớn nhất (0,001/0,026 ≈ 4 %).",
    "hien_tuong_hay_sai": ["Tưởng v = s/t (vận tốc trung bình cả đoạn) là vận tốc tại cổng — ra đúng một nửa.",
                           "Không thả xe từ nghỉ (đẩy nhẹ) nên đồ thị không qua gốc."],
    "sai_so_thuong_gap": "τ chỉ có 2 chữ số có nghĩa khi xe nhanh; v = d/τ là vận tốc trung bình khi đi qua cổng; bề rộng tấm chắn đo bằng thước có sai số.",
    "an_toan": "Chặn cuối máng để xe không lao xuống sàn.",
    "goi_y_mo_phong": {"loai": "2d_dong_hoc+do_thi+bang_so_lieu",
                       "y_tuong": "Kéo thanh trượt độ nghiêng (a) và vị trí cổng; xe lăn xuống, đồng hồ hiện t và τ; chấm điểm (t, v) lên đồ thị.",
                       "diem_nhan": "Cho học sinh dự đoán: đặt cổng xa gấp đôi thì v có gấp đôi không? (không — v ∝ √s, gấp đôi t mới gấp đôi v)."}})

# ---------- 02: quãng phanh theo tốc độ
AP = 5.0
rows2 = []
for kmh in (36, 54, 72, 90):
    v0 = kmh / 3.6
    rows2.append([kmh, round(v0, 2), round(v0 ** 2 / (2 * AP), 2), round(v0 / AP, 2)])
d2 = base(2, "Quãng đường phanh của xe tỉ lệ với bình phương tốc độ", "vi_du", "co_ban",
          ["ctbdd.cong_thuc_doc_lap_thoi_gian", "ctbdd.quang_phanh"])
d2.update({
    "muc_tieu": "Dùng v² − v0² = 2ad cho xe phanh tới dừng: quãng phanh d = v0²/(2|a|) — tốc độ gấp đôi thì quãng phanh gấp bốn.",
    "dung_cu": [{"ten": "Ô tô/xe máy trên đường khô (tình huống, không làm thật)", "so_luong": 1}],
    "cac_buoc": {"lam": ["Cho xe chạy ở 36, 54, 72, 90 km/h rồi phanh với cùng gia tốc 5 m/s² (giả định) tới khi dừng."],
                 "quan_sat": ["Quãng phanh 10; 22,5; 40; 62,5 m."],
                 "rut_ra": ["Quãng phanh tỉ lệ với v0²: gấp đôi tốc độ thì gấp bốn quãng phanh."]},
    "tham_so": [{"ky_hieu": "v0", "ten": "Tốc độ lúc bắt đầu phanh", "don_vi": "m/s", "kieu": "dieu_chinh",
                 "min": 5, "max": 30, "mac_dinh": 20, "buoc": 1},
                {"ky_hieu": "a", "ten": "Độ lớn gia tốc khi phanh", "don_vi": "m/s²", "kieu": "dieu_chinh",
                 "min": 2, "max": 8, "mac_dinh": 5, "buoc": 0.5},
                {"ky_hieu": "d", "ten": "Quãng phanh", "don_vi": "m", "kieu": "tinh_ra"},
                {"ky_hieu": "t", "ten": "Thời gian phanh", "don_vi": "s", "kieu": "tinh_ra"}],
    "mo_hinh": {"phuong_trinh": ["d = v0²/(2a)", "t = v0/a"],
                "gia_thiet": ["gia tốc phanh không đổi 5 m/s² (giả định, đường khô)", "chưa tính thời gian phản xạ của người lái"]},
    "so_lieu_mau": {"cot": ["v0 (km/h)", "v0 (m/s)", "d (m)", "t (s)"], "hang": rows2,
                    "ghi_chu": "Số minh hoạ tính từ mô hình."},
    "ket_qua_ky_vong": "72 km/h phanh mất 40 m, gấp 4 lần 10 m ở 36 km/h.",
    "hien_tuong_hay_sai": ["Nghĩ tốc độ gấp đôi thì quãng phanh gấp đôi.", "Quên đổi km/h sang m/s."],
    "goi_y_mo_phong": {"loai": "2d_dong_hoc+do_thi",
                       "y_tuong": "Hai làn xe chạy song song ở hai tốc độ, cùng phanh; vẽ vạch dừng và đồ thị v–t (tam giác) của mỗi xe.",
                       "diem_nhan": "Diện tích tam giác dưới đồ thị v–t gấp 4 khi chiều cao (v0) và đáy (t) cùng gấp đôi."}})

# ---------- 03: ô tô đuổi xe máy (bài toán mẫu)
rows3 = []
for t in (0, 2.5, 5, 7.5, 10):
    xo, xm = 0.5 * 2 * t * t, 10 * t
    rows3.append([t, xo, xm, xm - xo])
d3 = base(3, "Ô tô khởi hành ở đèn xanh đuổi theo xe máy chạy đều", "vi_du", "trung_binh",
          ["ctbdd.phuong_trinh_toa_do", "ctbdd.bai_toan_gap_nhau", "ctbdd.do_thi_v_t"])
d3.update({
    "muc_tieu": "Lập phương trình toạ độ của hai xe trên cùng một trục, giải x1 = x2 để tìm lúc và chỗ gặp; đọc đồ thị v–t để thấy khoảng cách lớn nhất khi hai xe cùng vận tốc.",
    "dung_cu": [{"ten": "Ô tô và xe máy ở ngã tư (tình huống)", "so_luong": 1}],
    "cac_buoc": {"lam": ["Đèn xanh: ô tô khởi hành từ vạch dừng với a = 2 m/s²; cùng lúc xe máy chạy đều 10 m/s đi qua vạch."],
                 "quan_sat": ["Ban đầu xe máy bỏ xa; tới t = 5 s hai xe cùng vận tốc, khoảng cách lớn nhất 25 m; t = 10 s ô tô đuổi kịp tại 100 m."],
                 "rut_ra": ["Gặp nhau khi x1 = x2 (cùng gốc toạ độ, cùng gốc thời gian).", "Cùng vận tốc không phải là gặp nhau."]},
    "tham_so": [{"ky_hieu": "a", "ten": "Gia tốc ô tô", "don_vi": "m/s²", "kieu": "dieu_chinh", "min": 1, "max": 4, "mac_dinh": 2, "buoc": 0.5},
                {"ky_hieu": "v2", "ten": "Vận tốc xe máy", "don_vi": "m/s", "kieu": "dieu_chinh", "min": 5, "max": 15, "mac_dinh": 10, "buoc": 1},
                {"ky_hieu": "t_gap", "ten": "Thời điểm gặp", "don_vi": "s", "kieu": "tinh_ra"},
                {"ky_hieu": "x_gap", "ten": "Vị trí gặp", "don_vi": "m", "kieu": "tinh_ra"}],
    "mo_hinh": {"phuong_trinh": ["x1 = ½·a·t²", "x2 = v2·t", "t_gap = 2·v2/a", "x_gap = v2·t_gap",
                                 "khoảng cách = v2·t − ½at², lớn nhất tại t = v2/a"],
                "gia_thiet": ["gốc toạ độ ở vạch dừng, chiều dương theo chiều chuyển động, gốc thời gian lúc đèn xanh", "hai xe coi là chất điểm"]},
    "so_lieu_mau": {"cot": ["t (s)", "x ô tô (m)", "x xe máy (m)", "khoảng cách (m)"], "hang": rows3,
                    "ghi_chu": "Tính từ mô hình với a = 2 m/s², v2 = 10 m/s."},
    "ket_qua_ky_vong": "Gặp nhau sau 10 s, cách vạch dừng 100 m; lúc đó ô tô có v = 20 m/s.",
    "hien_tuong_hay_sai": ["Tưởng hai đường v–t cắt nhau (t = 5 s) là lúc gặp nhau.", "Đặt hai gốc toạ độ khác nhau cho hai xe."],
    "goi_y_mo_phong": {"loai": "2d_dong_hoc+do_thi",
                       "y_tuong": "Hai xe chạy trên cùng một đường, bên dưới vẽ đồng thời đồ thị v–t và x–t; tô diện tích giữa hai đường v–t.",
                       "diem_nhan": "Cho dừng hình ở t = 5 s và hỏi: hai xe gặp nhau chưa?"}})

for d in (d1, d2, d3):
    (OUT / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
    print("ghi", d["id"])
print("Bảng 01 (t | v | v/t):")
for r in rows1:
    print(f"  {vn(r[3], 3)} | {vn(r[5])} | {vn(r[6])}   (τ đọc {vn(r[4], 3)})")
print("Bảng 02:", [(r[0], vn(r[1], 0), vn(r[2], 1), vn(r[3], 0)) for r in rows2])
print("Bảng 03:", rows3)
