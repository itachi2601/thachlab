"""Sinh 2 file thí nghiệm content/thi-nghiem/tn-l11-baitapnangluong-0N.json cho Bài 7 (lesson 26).
Số liệu tính lại từ mô hình; bảng trong theory.src.html phải khớp (script tự kiểm).  Chạy: python3 build_thi_nghiem.py"""
import json, math, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(ROOT, "content", "thi-nghiem")
SLUG = "content/lesson-samples/l11-bai-tap-nang-luong-dao-dong/theory.html"
BAI = "Bài 7. Bài tập về sự chuyển hoá năng lượng trong dao động điều hoà"
g = 9.8

# ---- TN 01: W theo biên độ ----
m, dl = 0.250, 0.050
k = m * g / dl                      # 49 N/m
w = math.sqrt(k / m)                # 14 rad/s
AS = [1, 1.5, 2, 3, 4]              # cm, luôn < Δl = 5 cm để lò xo không bị nén
# tốc độ "đo" bằng video 240 hình/s: trung bình quanh VTCB nên nhỏ hơn v_max ~1,4 %; đọc làm tròn 0,5 cm/s
V_DO = [13.5, 20.5, 27.5, 41.5, 55.0]
hang = []
for A, v in zip(AS, V_DO):
    vmax = w * A                    # cm/s
    assert abs(v - 0.986 * vmax) <= 0.5, (A, v, vmax)   # sai lệch nằm trong độ phân giải đọc
    Wd = 0.5 * m * (v / 100) ** 2 * 1000                # mJ
    Wm = 0.5 * k * (A / 100) ** 2 * 1000
    assert Wd < Wm                                      # "Rút ra": số đo thấp hơn mô hình
    hang.append([A, v, round(Wd, 1), round(Wm, 2)])
ratios = [h[2] / h[0] ** 2 for h in hang]
assert all(2.25 < r < 2.45 for r in ratios), ratios      # W/A² ~ 2,3–2,4 mJ/cm²
assert max(AS) < dl * 100
assert abs(0.5 * k / 10 - 2.45) < 1e-9                   # ½k = 24,5 J/m² = 2,45 mJ/cm²

# đối chiếu bảng trong bài
src = open(os.path.join(HERE, "theory.src.html"), encoding="utf8").read()
tb = src.split('data-exp="tn-l11-baitapnangluong-01"')[1].split("</table>")[0]
rows = re.findall(r"<tr><td>([\d,]+)</td><td>([\d,]+)</td><td>([\d,]+)</td></tr>", tb)
assert [(float(a.replace(",", ".")), float(b.replace(",", ".")), float(c.replace(",", "."))) for a, b, c in rows] == \
       [(h[0], h[1], h[2]) for h in hang], rows

tn1 = {
 "mon": "vat-ly", "lop": 11, "bai": BAI, "lesson_id": 26, "nguon_trong_bai": SLUG,
 "id": "tn-l11-baitapnangluong-01",
 "ten": "Đo cơ năng con lắc lò xo theo biên độ (lò xo, thước, điện thoại quay chậm)",
 "loai": "thi_nghiem", "muc_do": "trung_binh",
 "kien_thuc": ["daodong.co_nang", "daodong.co_nang_ti_le_a_binh_phuong", "do_luong.sai_so_tuong_doi"],
 "muc_tieu": "Kiểm bằng số đo rằng cơ năng tỉ lệ bình phương biên độ, và thấy sai số tương đối của W gấp đôi sai số của A.",
 "dung_cu": [{"ten": "Lò xo", "so_luong": 1}, {"ten": "Quả nặng 250 g", "so_luong": 1},
             {"ten": "Giá treo", "so_luong": 1}, {"ten": "Thước thẳng có vạch mm", "so_luong": 1},
             {"ten": "Điện thoại quay chậm 240 hình/giây", "so_luong": 1}],
 "cac_buoc": {
  "lam": ["Treo quả nặng 250 g, đo độ dãn thêm 5,0 cm, tính k = mg/Δl = 49 N/m (g = 9,8 m/s²).",
          "Kéo xuống lần lượt A = 1; 1,5; 2; 3; 4 cm (nhỏ hơn Δl để lò xo luôn dãn; thước ±1 mm) rồi thả.",
          "Quay chậm 240 hình/giây, đo tốc độ khi vật qua vị trí cân bằng."],
  "quan_sat": ["Bảng 5 hàng: A, v_max đo, ½mv_max².",
               "Tỉ số W/A² gần như không đổi, khoảng 2,3–2,4 mJ/cm²."],
  "rut_ra": ["W tỉ lệ A²: biên gấp 3 (1 → 3 cm) thì năng lượng gấp khoảng 9.",
             "Số đo thấp hơn mô hình ½k = 2,45 mJ/cm² chừng 2–7% (video lấy tốc độ trung bình quanh VTCB, lực cản không khí).",
             "Hàng A = 1 cm kém tin cậy nhất: sai 1 mm là 10% của A, thành 20% của W; hàng 4 cm W chỉ sai cỡ 5% (A sai 2,5%)."]},
 "tham_so": [
  {"ky_hieu": "m", "ten": "Khối lượng quả nặng", "don_vi": "kg", "kieu": "co_dinh", "gia_tri": m},
  {"ky_hieu": "k", "ten": "Độ cứng lò xo", "don_vi": "N/m", "kieu": "tinh_ra"},
  {"ky_hieu": "A", "ten": "Biên độ", "don_vi": "cm", "kieu": "dieu_chinh", "min": 1, "max": 4, "mac_dinh": 2, "buoc": 0.5},
  {"ky_hieu": "v_max", "ten": "Tốc độ qua VTCB", "don_vi": "cm/s", "kieu": "do_duoc", "sai_so_do": 0.5},
  {"ky_hieu": "W", "ten": "Cơ năng", "don_vi": "mJ", "kieu": "tinh_ra"}],
 "mo_hinh": {
  "phuong_trinh": ["k = m·g/Δl", "ω = √(k/m)", "v_max = ω·A", "W = ½·k·A² = ½·m·v_max²",
                   "v_do ≈ 0,986·v_max (trung bình trên 10 khung quanh VTCB)"],
  "gia_thiet": ["A < Δl = 5 cm nên lò xo luôn dãn", "bỏ khối lượng lò xo", "mốc thế năng tại VTCB", "lực cản nhỏ trong một phần tư chu kì",
                "g = 9,8 m/s²"]},
 "so_lieu_mau": {"cot": ["A (cm)", "v_max đo (cm/s)", "½mv_max² (mJ)", "½kA² mô hình (mJ)"],
                 "hang": hang,
                 "ghi_chu": "Số minh hoạ: tính từ mô hình kèm sai số dụng cụ (đọc tốc độ ±0,5 cm/s), chưa phải số đo thật."},
 "ket_qua_ky_vong": "W/A² ≈ 2,3–2,4 mJ/cm², gần ½k = 2,45 mJ/cm²; A tăng 3 lần (1 → 3 cm) thì W tăng khoảng 9 lần.",
 "sai_so_thuong_gap": ["Đọc biên độ bằng mắt lệch 1 mm: sai số W gấp đôi sai số A.",
                       "Lấy tốc độ trung bình trên nhiều khung hình làm v_max nên W đo hơi nhỏ."],
 "hien_tuong_hay_sai": ["Nghĩ biên độ gấp 3 thì năng lượng gấp 3 (quên bình phương).",
                        "Thế A bằng cm vào ½kA² rồi ghi đơn vị J."],
 "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu", "dieu_khien": ["A"],
                    "dau_ra": ["vật dao động", "thanh W lớn dần theo A²", "bảng số đo"],
                    "y_tuong": "Kéo thanh A, vật dao động; cột W vẽ cạnh đường cong ½kA² để thấy W tăng theo bình phương."}}

# ---- TN 02: xích đu (ví dụ) ----
l, a0, M = 2.0, 30.0, 40.0
hh = l * (1 - math.cos(math.radians(a0)))
W2 = M * g * hh
v2 = math.sqrt(2 * g * hh)
assert round(hh, 2) == 0.27 and round(W2) == 105 and round(v2, 1) == 2.3
rows2 = []
for a in (10, 20, 30):
    h_ = l * (1 - math.cos(math.radians(a)))
    rows2.append([a, round(h_, 3), round(M * g * h_, 1), round(math.sqrt(2 * g * h_), 2)])
tn2 = {
 "mon": "vat-ly", "lop": 11, "bai": BAI, "lesson_id": 26, "nguon_trong_bai": SLUG,
 "id": "tn-l11-baitapnangluong-02",
 "ten": "Xích đu ở sân trường: cơ năng và tốc độ qua đáy",
 "loai": "vi_du", "muc_do": "co_ban",
 "kien_thuc": ["daodong.con_lac_don_co_nang", "daodong.bao_toan_co_nang"],
 "muc_tieu": "Tính độ cao biên h = l(1 − cos α0), cơ năng và tốc độ qua đáy của xích đu.",
 "dung_cu": [{"ten": "Xích đu dây dài 2,0 m", "so_luong": 1},
             {"ten": "Điện thoại có ứng dụng đo góc", "so_luong": 1}],
 "cac_buoc": {
  "lam": ["Bạn 40 kg ngồi xích đu dây 2,0 m; đẩy tới góc lệch lớn nhất 30° (đo bằng ứng dụng đo góc)."],
  "quan_sat": ["Ở biên đu dừng một thoáng; qua đáy nhanh nhất."],
  "rut_ra": ["h = 2,0(1 − cos 30°) ≈ 0,27 m; W = mgh ≈ 105 J; v qua đáy = √(2gh) ≈ 2,3 m/s."]},
 "tham_so": [
  {"ky_hieu": "l", "ten": "Chiều dài dây", "don_vi": "m", "kieu": "dieu_chinh", "min": 1.5, "max": 3, "mac_dinh": 2, "buoc": 0.1},
  {"ky_hieu": "α0", "ten": "Góc lệch lớn nhất", "don_vi": "độ", "kieu": "dieu_chinh", "min": 5, "max": 45, "mac_dinh": 30, "buoc": 5},
  {"ky_hieu": "m", "ten": "Khối lượng người", "don_vi": "kg", "kieu": "co_dinh", "gia_tri": M},
  {"ky_hieu": "v", "ten": "Tốc độ qua đáy", "don_vi": "m/s", "kieu": "tinh_ra"}],
 "mo_hinh": {"phuong_trinh": ["h = l·(1 − cos α0)", "W = m·g·h", "v = √(2·g·l·(cos α − cos α0))"],
             "gia_thiet": ["bỏ ma sát trong một lượt", "coi người + ghế là chất điểm ở đầu dây", "g = 9,8 m/s²"]},
 "so_lieu_mau": {"cot": ["α0 (độ)", "h (m)", "W (J)", "v qua đáy (m/s)"], "hang": rows2,
                 "ghi_chu": "Tính từ mô hình, không phải số đo thật."},
 "ket_qua_ky_vong": "α0 = 30°, l = 2,0 m, m = 40 kg: h ≈ 0,27 m, W ≈ 105 J, v ≈ 2,3 m/s.",
 "hien_tuong_hay_sai": ["Dùng cos α0 thay cho 1 − cos α0.",
                        "Thế góc bằng độ vào công thức góc nhỏ ½mglα0².",
                        "Nghĩ góc gấp đôi thì năng lượng gấp đôi."],
 "goi_y_mo_phong": {"loai": "2d_dong_hoc+do_thi", "dieu_khien": ["l", "α0"],
                    "dau_ra": ["xích đu đung đưa", "cột thế năng/động năng đổi chỗ", "số đo v qua đáy"],
                    "hinh_trong_bai": "Hình 4",
                    "y_tuong": "Kéo xích đu tới góc α0 rồi thả; hai cột Wt, Wđ đổi chỗ, tổng không đổi."}}

for d in (tn1, tn2):
    p = os.path.join(OUT, d["id"] + ".json")
    open(p, "w", encoding="utf8").write(json.dumps(d, ensure_ascii=False, indent=1))
    print("ghi", os.path.relpath(p, ROOT))
