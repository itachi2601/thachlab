#!/usr/bin/env python3
"""Sinh 3 file content/thi-nghiem/tn-l11-dotansoam-NN.json từ mô hình (số liệu tính bằng script, không gõ tay)."""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "content" / "thi-nghiem"
BAI = "Bài 10. Thực hành: Đo tần số của sóng âm"
NGUON = "content/lesson-samples/l11-thuc-hanh-do-tan-so-am/theory.html"
BASE = {"mon": "vat-ly", "lop": 11, "bai": BAI, "lesson_id": 29, "nguon_trong_bai": NGUON}


def fmt(x, nd=1):
    return round(x, nd)


def save(d):
    p = OUT / f"{d['id']}.json"
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf8")
    print("ghi", p.name)


# ---------- 01: dao động kí, 5 lần đo, N = 4, k = 1 ms/ô, f0 = 440 Hz
F0, K, N = 440.0, 1.0, 4
L_TRUE = N * (1000 / F0) / K                     # 9,09 ô
L_READ = [9.1, 9.0, 9.2, 9.1, 9.0]                # đọc tới 0,1 ô, lệch ≤ 0,1 ô quanh giá trị thật
assert all(abs(l - L_TRUE) <= 0.12 for l in L_READ), L_READ
FS = [N / (l * K * 1e-3) for l in L_READ]
FBAR = sum(FS) / 5
DF = [abs(f - FBAR) for f in FS]
DFM = sum(DF) / 5
assert [fmt(f) for f in FS] == [439.6, 444.4, 434.8, 439.6, 444.4] and fmt(FBAR) == 440.6 and fmt(DFM) == 3.1
save({**BASE, "id": "tn-l11-dotansoam-01",
      "ten": "Đo tần số của âm thoa bằng dao động kí và micro",
      "loai": "thi_nghiem", "muc_do": "co_ban",
      "kien_thuc": ["amthanh.tan_so_chu_ki", "amthanh.doc_dao_dong_ki", "amthanh.sai_so_nhieu_lan_do"],
      "muc_tieu": "Đo tần số của âm thoa 440 Hz: đọc bề rộng L của N chu kì liên tiếp trên màn dao động kí, tính T rồi f, lặp 5 lần, tính f trung bình, sai số tuyệt đối trung bình và viết f = f̄ ± Δf.",
      "dung_cu": [{"ten": "Âm thoa 440 Hz có hộp cộng hưởng", "so_luong": 1, "ghi_chu": "kèm búa cao su"},
                  {"ten": "Micro", "so_luong": 1},
                  {"ten": "Dao động kí có núm TIME/DIV và VOLT/DIV", "so_luong": 1},
                  {"ten": "Dây tín hiệu nối micro vào CH1", "so_luong": 1}],
      "cac_buoc": {
          "lam": ["Nối micro vào CH1 của dao động kí.",
                  "Gõ âm thoa vào búa cao su, đặt sát micro (khoảng 2 cm).",
                  "Chỉnh VOLT/DIV cho sóng cao cỡ 4 ô, TIME/DIV ở 1 ms/ô, chỉnh TRIGGER cho hình đứng yên.",
                  "Đo bề rộng L của N = 4 chu kì liên tiếp, đọc tới 0,1 ô.",
                  "Gõ lại âm thoa và đo như vậy, tổng cộng 5 lần."],
          "quan_sat": ["L quanh 9,1 ô, từ 9,0 đến 9,2 ô.", "Sóng nhỏ dần sau mỗi lần gõ."],
          "rut_ra": ["Mỗi lần cho f = N/(L·k) hơi khác nhau; f trung bình ≈ 440,6 Hz, Δf̄ ≈ 3,1 Hz.",
                     "Sai số dụng cụ: 0,1 ô tương ứng ≈ 4,8 Hz; Δf = Δf̄ + Δf_dc ≈ 3,1 + 4,8 ≈ 8 Hz.", "Kết quả f = 441 ± 8 Hz, khoảng 433–449 Hz chứa giá trị ghi trên âm thoa (440 Hz)."]},
      "tham_so": [
          {"ky_hieu": "f", "ten": "Tần số của nguồn âm", "don_vi": "Hz", "kieu": "dieu_chinh", "min": 200, "max": 1000, "mac_dinh": 440, "buoc": 10},
          {"ky_hieu": "k", "ten": "Độ chia thời gian TIME/DIV", "don_vi": "ms/ô", "kieu": "dieu_chinh", "min": 0.1, "max": 5, "mac_dinh": 1, "buoc": 0.1},
          {"ky_hieu": "N", "ten": "Số chu kì liên tiếp được đo", "don_vi": "", "kieu": "dieu_chinh", "min": 1, "max": 8, "mac_dinh": 4, "buoc": 1},
          {"ky_hieu": "L", "ten": "Bề rộng N chu kì trên màn", "don_vi": "ô", "kieu": "do_duoc", "sai_so_do": 0.1},
          {"ky_hieu": "T", "ten": "Chu kì", "don_vi": "ms", "kieu": "tinh_ra"},
          {"ky_hieu": "f_do", "ten": "Tần số tính được", "don_vi": "Hz", "kieu": "tinh_ra"}],
      "mo_hinh": {"phuong_trinh": ["L_that = N·(1000/f)/k (ô)", "L_doc = L_that + sai số ngẫu nhiên trong ±0,1 ô, làm tròn 0,1 ô",
                                   "T = L·k/N (ms)", "f = 1000/T (Hz)", "Δf_i = |f_i − f̄|, Δf = trung bình các Δf_i + Δf_dc (Δf_dc = f̄·0,1/L)"],
                  "gia_thiet": ["âm đơn, biên độ không đổi trong lúc đọc", "độ chia thời gian chính xác (núm hiệu chỉnh ở vị trí chuẩn)"]},
      "so_lieu_mau": {"cot": ["Lần", "L (ô)", "f (Hz)"],
                      "hang": [[i + 1, L_READ[i], fmt(FS[i])] for i in range(5)],
                      "ghi_chu": "Số minh hoạ, sinh từ mô hình với N = 4, k = 1 ms/ô, f = 440 Hz và sai số đọc màn ±0,1 ô; không phải số đo thật. f̄ ≈ 440,6 Hz; Δf̄ ≈ 3,1 Hz; Δf_dc ≈ 4,8 Hz; Δf ≈ 8 Hz; δ ≈ 1,8 %."},
      "ket_qua_ky_vong": "f = 441 ± 8 Hz (sai số tỉ đối ≈ 1,8 %), phù hợp nhãn 440 Hz của âm thoa.",
      "hien_tuong_hay_sai": ["Đếm đỉnh thay vì đếm chu kì (n đỉnh chỉ cho n − 1 chu kì).", "Quên đổi ms ra s trước khi lật ngược.",
                             "Lấy cả bề rộng L làm một chu kì, quên chia cho N."],
      "sai_so_thuong_gap": ["đọc ô lệch cỡ 0,1 ô (ngẫu nhiên)", "núm hiệu chỉnh TIME/DIV chưa về vị trí chuẩn (hệ thống)", "âm thoa tắt dần, sóng nhỏ"],
      "goi_y_mo_phong": {"loai": "do_thi+bang_so_lieu", "dieu_khien": ["f", "k", "N"], "dau_ra": ["màn dao động kí 10 ô", "bảng L và f", "f̄ ± Δf"],
                         "hinh_trong_bai": "Hình 3", "y_tuong": "Kéo hai vạch ngắm trên màn để đọc L; bấm Đo lại thì thêm một hàng lệch ngẫu nhiên ±0,1 ô."}})

# ---------- 02: điện thoại ghi âm, đếm N = 10 chu kì
T10 = [22.6, 22.8, 22.7]
F10 = [10 / (t * 1e-3) for t in T10]
assert [fmt(f) for f in F10] == [442.5, 438.6, 440.5], [fmt(f) for f in F10]
save({**BASE, "id": "tn-l11-dotansoam-02",
      "ten": "Đo tần số bằng điện thoại: ghi âm rồi đếm chu kì trên dạng sóng",
      "loai": "thi_nghiem", "muc_do": "co_ban",
      "kien_thuc": ["amthanh.tan_so_chu_ki", "amthanh.dem_chu_ki_dang_song"],
      "muc_tieu": "Đo tần số âm thoa 440 Hz không cần dao động kí: ghi âm, phóng to dạng sóng, đếm N = 10 chu kì liên tiếp và đọc thời gian t của đoạn đó.",
      "dung_cu": [{"ten": "Âm thoa 440 Hz", "so_luong": 1}, {"ten": "Điện thoại có ứng dụng ghi âm hiển thị dạng sóng", "so_luong": 1}],
      "cac_buoc": {"lam": ["Ghi âm âm thoa vài giây.", "Mở dạng sóng, phóng to, chọn đoạn có N = 10 chu kì liên tiếp và đọc thời gian t của đoạn.", "Chọn ba đoạn khác nhau."],
                   "quan_sat": ["t = 22,6; 22,8; 22,7 ms (số minh hoạ)."],
                   "rut_ra": ["f = N/t ra 442,5; 438,6; 440,5 Hz, trung bình khoảng 440,5 Hz."]},
      "tham_so": [{"ky_hieu": "f", "ten": "Tần số của nguồn âm", "don_vi": "Hz", "kieu": "dieu_chinh", "min": 200, "max": 1000, "mac_dinh": 440, "buoc": 10},
                  {"ky_hieu": "N", "ten": "Số chu kì được đếm", "don_vi": "", "kieu": "dieu_chinh", "min": 2, "max": 20, "mac_dinh": 10, "buoc": 1},
                  {"ky_hieu": "t", "ten": "Thời gian của đoạn đếm", "don_vi": "ms", "kieu": "do_duoc", "sai_so_do": 0.1},
                  {"ky_hieu": "f_do", "ten": "Tần số tính được", "don_vi": "Hz", "kieu": "tinh_ra"}],
      "mo_hinh": {"phuong_trinh": ["t_that = N·1000/f (ms)", "f = N/t"], "gia_thiet": ["âm đơn", "đếm đúng N chu kì (n đỉnh là n − 1 chu kì)"]},
      "so_lieu_mau": {"cot": ["Lần", "t (ms)", "f (Hz)"], "hang": [[i + 1, T10[i], fmt(F10[i])] for i in range(3)],
                      "ghi_chu": "Số minh hoạ sinh từ mô hình f = 440 Hz với sai số đọc thời gian cỡ 0,1 ms; không phải số đo thật."},
      "ket_qua_ky_vong": "f ≈ 440,5 Hz, cùng nguyên lý với dao động kí.",
      "hien_tuong_hay_sai": ["Đếm 10 đỉnh thành 10 chu kì.", "Quên đổi ms ra s."],
      "goi_y_mo_phong": {"loai": "do_thi+bang_so_lieu", "dieu_khien": ["f", "N"], "dau_ra": ["dạng sóng phóng to", "t của đoạn đếm", "f"],
                         "hinh_trong_bai": None, "y_tuong": "Kéo hai mốc đầu và cuối đoạn, hiện t và f = N/t."}})

# ---------- 03: hai âm khác tần số trên cùng thang thời gian (Hình 4)
save({**BASE, "id": "tn-l11-dotansoam-03",
      "ten": "So sánh hai âm đơn 440 Hz và 880 Hz trên cùng thang thời gian",
      "loai": "vi_du", "muc_do": "co_ban",
      "kien_thuc": ["amthanh.tan_so_do_cao", "amthanh.bien_do_do_to"],
      "muc_tieu": "Thấy tần số lớn gấp đôi thì trong cùng khoảng thời gian có số chu kì gấp đôi, âm cao hơn; còn biên độ chỉ đổi độ to.",
      "dung_cu": [{"ten": "Máy phát tần số và loa", "so_luong": 1}, {"ten": "Micro và dao động kí", "so_luong": 1}],
      "cac_buoc": {"lam": ["Phát âm 440 Hz, ghi lại số chu kì trong 9 ms trên màn.", "Đổi sang 880 Hz, giữ nguyên TIME/DIV và biên độ."],
                   "quan_sat": ["Trong 9 ms: gần 4 chu kì ở 440 Hz, gần 8 chu kì ở 880 Hz.", "Chiều cao sóng không đổi, tai nghe thấy âm cao hơn."],
                   "rut_ra": ["f gấp đôi thì T giảm một nửa, số chu kì trong cùng thời gian gấp đôi.", "Biên độ quyết định độ to, tần số quyết định độ cao."]},
      "tham_so": [{"ky_hieu": "f", "ten": "Tần số", "don_vi": "Hz", "kieu": "dieu_chinh", "min": 200, "max": 2000, "mac_dinh": 440, "buoc": 10},
                  {"ky_hieu": "A", "ten": "Biên độ (độ to)", "don_vi": "ô", "kieu": "dieu_chinh", "min": 0.5, "max": 3, "mac_dinh": 1, "buoc": 0.5},
                  {"ky_hieu": "T", "ten": "Chu kì", "don_vi": "ms", "kieu": "tinh_ra"}],
      "mo_hinh": {"phuong_trinh": ["u(t) = A·sin(2π·f·t)", "T = 1000/f (ms)", "số chu kì trong 9 ms = f·9·10⁻³"], "gia_thiet": ["âm đơn"]},
      "so_lieu_mau": {"cot": ["f (Hz)", "T (ms)", "Số chu kì trong 9 ms"],
                      "hang": [[440, fmt(1000 / 440, 2), fmt(440 * 9e-3, 2)], [880, fmt(1000 / 880, 2), fmt(880 * 9e-3, 2)]],
                      "ghi_chu": "Tính từ mô hình, không phải số đo thật."},
      "ket_qua_ky_vong": "880 Hz có số chu kì gấp đôi 440 Hz trong cùng 9 ms.",
      "hien_tuong_hay_sai": ["Cho rằng nhiều đỉnh hơn nghĩa là to hơn.", "Lấy chiều cao sóng làm tần số."],
      "goi_y_mo_phong": {"loai": "do_thi", "dieu_khien": ["f", "A"], "dau_ra": ["hai đồ thị sin cùng trục thời gian", "phát âm thật bằng Web Audio"],
                         "hinh_trong_bai": "Hình 4", "y_tuong": "Hai thanh trượt f và A; đổi A không đổi số chu kì, đổi f không đổi chiều cao."}})
