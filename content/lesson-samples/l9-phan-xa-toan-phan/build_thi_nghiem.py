"""Sinh 3 file content/thi-nghiem/tn-l9-pxtp-NN.json cho bài Phản xạ toàn phần (KHTN 9, lesson_id 84).
Số liệu mẫu tính từ chính mô hình (định luật khúc xạ) — khớp bảng trong theory.src.html."""
import json, math, pathlib

HERE = pathlib.Path(__file__).resolve().parent
KHO = HERE.parents[2] / "content" / "thi-nghiem"
def s(x): return math.sin(math.radians(x))
def asin_d(x): return math.degrees(math.asin(x))

BASE = {"mon": "vat-ly", "lop": 9, "bai": "Bài 6. Phản xạ toàn phần", "lesson_id": 84,
        "nguon_trong_bai": "content/lesson-samples/l9-phan-xa-toan-phan/theory.html"}

# ---------------------------------------------------------------- 01: khối bán trụ
n = 1.5
doc = {20: 31, 30: 49, 35: 60, 40: 74, 41: 80}          # số đọc minh hoạ (độ chia 1°)
hang = []
for i, rd in doc.items():
    rt = round(asin_d(n * s(i)), 1)
    assert abs(rd - rt) <= 0.7, (i, rd, rt)               # lệch < 1 vạch chia
    hang.append([i, rd, rt])
assert n * s(42) > 1
hang.append([42, "không còn", "không có"])
ith = asin_d(1 / n)
tn1 = {**BASE,
 "id": "tn-l9-pxtp-01",
 "ten": "Khối bán trụ thủy tinh: tăng góc tới tới khi tia khúc xạ biến mất",
 "loai": "thi_nghiem", "muc_do": "co_ban",
 "kien_thuc": ["pxtp.hien_tuong", "pxtp.goc_toi_han", "pxtp.dieu_kien"],
 "muc_tieu": "Thấy tia khúc xạ lệch xa pháp tuyến và mờ dần khi tăng góc tới, đi sát mặt phân cách ở góc tới hạn rồi biến mất; đọc bảng i–r và ước lượng góc tới hạn.",
 "dung_cu": [{"ten": "Bút laser (hoặc đèn chiếu chùm hẹp)", "so_luong": 1},
             {"ten": "Khối bán trụ thủy tinh/acrylic", "so_luong": 1},
             {"ten": "Vòng chia độ in trên tấm nhựa, độ chia 1°", "so_luong": 1}],
 "cac_buoc": {
  "lam": ["Đặt khối bán trụ trên vòng chia độ, mặt phẳng hướng lên, tâm trùng tâm vòng.",
          "Chiếu tia laser vào mặt cong, hướng vào tâm I (tia đi theo bán kính nên không gãy khi vào thủy tinh).",
          "Tăng dần góc tới i tại I, đọc góc khúc xạ r ở i = 20°, 30°, 35°, 40°, 41°, 42°."],
  "quan_sat": ["i nhỏ: có tia khúc xạ và tia phản xạ mờ.",
               "i tăng: tia khúc xạ lệch xa pháp tuyến, mờ dần; tia phản xạ sáng dần.",
               "Khoảng 42°: tia khúc xạ sát mặt phẳng; vượt quá chỉ còn tia phản xạ."],
  "rut_ra": ["Vượt góc tới hạn, ánh sáng bị phản xạ toàn phần.",
             f"Góc tới hạn nằm giữa 41° và 42°; tính đúng i_th = {ith:.1f}° (n = 1,5)."]},
 "tham_so": [
  {"ky_hieu": "n", "ten": "Chiết suất khối bán trụ", "don_vi": "", "kieu": "dieu_chinh", "min": 1.3, "max": 2.5, "mac_dinh": 1.5, "buoc": 0.01},
  {"ky_hieu": "i", "ten": "Góc tới tại tâm I", "don_vi": "°", "kieu": "dieu_chinh", "min": 0, "max": 89, "mac_dinh": 30, "buoc": 1},
  {"ky_hieu": "n_kk", "ten": "Chiết suất không khí", "don_vi": "", "kieu": "co_dinh", "gia_tri": 1.0},
  {"ky_hieu": "r", "ten": "Góc khúc xạ đọc trên vòng chia độ", "don_vi": "°", "kieu": "do_duoc", "sai_so_do": 1},
  {"ky_hieu": "i_th", "ten": "Góc tới hạn", "don_vi": "°", "kieu": "tinh_ra"}],
 "mo_hinh": {
  "phuong_trinh": ["n·sin i = n_kk·sin r (khi n·sin i ≤ 1)", "sin i_th = n_kk/n",
                   "i ≥ i_th: không có tia khúc xạ, phản xạ toàn phần (góc phản xạ = i)"],
  "gia_thiet": ["tia tới đi theo bán kính nên không khúc xạ ở mặt cong", "n_kk = 1", "bỏ qua bề rộng vệt laser"]},
 "so_lieu_mau": {"cot": ["i (°)", "r đọc (°)", "r tính (°)"], "hang": hang,
  "ghi_chu": f"Số liệu minh hoạ tính từ mô hình n = 1,5, số đọc làm tròn tới vạch 1° và lệch tối đa 0,6° so với tính; i_th = {ith:.2f}°."},
 "ket_qua_ky_vong": "r tăng nhanh dần khi i gần 42°; ở 42° không còn tia khúc xạ; i_th ≈ 41,8°.",
 "hien_tuong_hay_sai": ["Cho rằng tia khúc xạ luôn còn, chỉ lệch thêm.",
                        "Cho rằng khi có tia khúc xạ thì không có tia phản xạ.",
                        "Đo góc từ mặt phẳng thay vì từ pháp tuyến."],
 "sai_so_thuong_gap": "Gần góc tới hạn tia khúc xạ rất mờ và r đổi tới 5° khi i đổi 1°; vệt laser có bề rộng; chiếu lệch tâm I làm tia gãy ở mặt cong.",
 "an_toan": "Không chiếu laser vào mắt; dùng bút laser công suất thấp.",
 "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu",
  "y_tuong": "Khối bán trụ trên vòng chia độ, thanh trượt góc tới; độ sáng tia khúc xạ/phản xạ đổi theo i; bảng tự ghi r.",
  "diem_nhan": "Thanh trượt chiết suất: n lớn thì góc tới hạn nhỏ (kim cương 24,4°)."}}

# ---------------------------------------------------------------- 02: dòng nước dẫn sáng
chat = [("Nước", 1.33), ("Dầu ăn", 1.47)]
tn2 = {**BASE,
 "id": "tn-l9-pxtp-02",
 "ten": "Dòng nước dẫn ánh sáng (sợi quang bằng nước)",
 "loai": "thi_nghiem", "muc_do": "co_ban",
 "kien_thuc": ["pxtp.cap_quang", "pxtp.dieu_kien"],
 "muc_tieu": "Thấy ánh sáng laser đi cong theo dòng nước nhờ phản xạ toàn phần liên tiếp, giống ánh sáng trong sợi quang.",
 "dung_cu": [{"ten": "Chai nhựa trong, đục một lỗ nhỏ gần đáy", "so_luong": 1},
             {"ten": "Bút laser", "so_luong": 1},
             {"ten": "Chậu hứng nước", "so_luong": 1}],
 "cac_buoc": {
  "lam": ["Đổ đầy nước vào chai cho tia nước chảy ra chậu.", "Tắt đèn phòng; chiếu laser xuyên qua chai, thẳng vào lỗ, từ phía đối diện."],
  "quan_sat": ["Vệt sáng cong theo dòng nước.", "Chỗ dòng nước chạm chậu sáng lên một đốm."],
  "rut_ra": ["Nước chiết quang hơn không khí; ánh sáng phản xạ toàn phần nhiều lần trên mặt dòng nước nên đi cong theo nó."]},
 "tham_so": [
  {"ky_hieu": "n", "ten": "Chiết suất chất lỏng", "don_vi": "", "kieu": "dieu_chinh", "min": 1.3, "max": 1.6, "mac_dinh": 1.33, "buoc": 0.01},
  {"ky_hieu": "i", "ten": "Góc tới tại mặt dòng nước", "don_vi": "°", "kieu": "tinh_ra"},
  {"ky_hieu": "i_th", "ten": "Góc tới hạn chất lỏng – không khí", "don_vi": "°", "kieu": "tinh_ra"}],
 "mo_hinh": {"phuong_trinh": ["sin i_th = 1/n", "i ≥ i_th tại mọi điểm chạm thì ánh sáng không thoát ra"],
             "gia_thiet": ["dòng nước cong đều, không vỡ giọt", "bỏ qua hấp thụ của nước"]},
 "so_lieu_mau": {"cot": ["Chất lỏng", "n", "i_th (°)"],
  "hang": [[t, n_, round(asin_d(1 / n_), 1)] for t, n_ in chat],
  "ghi_chu": "Số liệu minh hoạ tính từ sin i_th = 1/n, không phải đo thật."},
 "ket_qua_ky_vong": "Ánh sáng đi theo dòng nước cong; đoạn dòng nước vỡ thành giọt thì ánh sáng tán ra.",
 "hien_tuong_hay_sai": ["Nghĩ ánh sáng tự 'uốn cong' trong nước.", "Nghĩ dòng nước phải thẳng thì mới dẫn được sáng."],
 "sai_so_thuong_gap": "Laser không nhắm đúng lỗ; phòng còn sáng nên khó thấy vệt; dòng nước rung làm vệt chập chờn.",
 "an_toan": "Không chiếu laser vào mắt; lau khô sàn sau thí nghiệm.",
 "goi_y_mo_phong": {"loai": "2d_dong_hoc",
  "y_tuong": "Chai, lỗ, dòng nước parabol; tia laser phản xạ zigzag trong dòng nước.",
  "diem_nhan": "Thanh trượt độ cao lỗ: dòng nước cong gắt hơn thì có chỗ góc tới < i_th, ánh sáng lọt ra."}}

# ---------------------------------------------------------------- 03: cốc nước thành gương
nn = 1.33
hang3 = []
for i in (30, 45, 50):
    x = nn * s(i)
    hang3.append([i, round(asin_d(x), 1) if x <= 1 else "không có", "ló ra" if x <= 1 else "phản xạ toàn phần"])
tn3 = {**BASE,
 "id": "tn-l9-pxtp-03",
 "ten": "Cốc nước thành gương: nhìn chếch từ dưới lên mặt nước",
 "loai": "thi_nghiem", "muc_do": "co_ban",
 "kien_thuc": ["pxtp.dieu_kien", "pxtp.chieu_truyen"],
 "muc_tieu": "Thấy mặt nước sáng bạc khi nhìn từ dưới chếch lên (nước → không khí, góc tới lớn) và không thấy khi nhìn từ trên xuống.",
 "dung_cu": [{"ten": "Cốc thủy tinh trong, thành thẳng", "so_luong": 1}, {"ten": "Nước", "so_luong": 1}],
 "cac_buoc": {
  "lam": ["Rót đầy nước vào cốc, nâng cốc cao hơn mắt, nhúng ngón tay vào nước.",
          "Nhìn chếch từ dưới lên mặt nước qua thành cốc; sau đó nhìn từ trên xuống."],
  "quan_sat": ["Nhìn từ dưới, chếch nhiều: mặt nước sáng bạc, thấy ảnh ngón tay lộn ngược.",
               "Nhìn từ trên xuống: mặt nước trong, không có lớp bạc."],
  "rut_ra": ["Lớp bạc chỉ có khi ánh sáng đi từ nước ra không khí với góc tới lớn: đúng hai điều kiện phản xạ toàn phần."]},
 "tham_so": [
  {"ky_hieu": "i", "ten": "Góc tới tại mặt nước", "don_vi": "°", "kieu": "dieu_chinh", "min": 0, "max": 89, "mac_dinh": 50, "buoc": 1},
  {"ky_hieu": "n", "ten": "Chiết suất nước", "don_vi": "", "kieu": "co_dinh", "gia_tri": nn},
  {"ky_hieu": "r", "ten": "Góc khúc xạ ra không khí", "don_vi": "°", "kieu": "tinh_ra"}],
 "mo_hinh": {"phuong_trinh": ["1,33·sin i = sin r (khi 1,33·sin i ≤ 1)", "sin i_th = 1/1,33, i_th ≈ 48,8°"],
             "gia_thiet": ["mặt nước phẳng", "thành cốc mỏng, bỏ qua khúc xạ qua thành cốc"]},
 "so_lieu_mau": {"cot": ["i (°)", "r (°)", "Kết quả"], "hang": hang3,
  "ghi_chu": "Số liệu minh hoạ tính từ định luật khúc xạ với n = 1,33, không phải đo thật."},
 "ket_qua_ky_vong": "Từ khoảng 49° trở lên mặt nước như gương khi nhìn từ dưới; nhìn từ trên xuống không bao giờ thấy.",
 "hien_tuong_hay_sai": ["Nghĩ mặt nước 'phản chiếu như gương' từ phía nào cũng như nhau.", "Nghĩ lớp bạc là do bọt khí bám mặt nước."],
 "sai_so_thuong_gap": "Cốc có hoa văn hoặc thành dày làm méo ảnh; mặt nước dao động.",
 "an_toan": "Cầm chắc cốc thủy tinh, tránh làm vỡ.",
 "goi_y_mo_phong": {"loai": "2d_dong_hoc",
  "y_tuong": "Mắt đặt dưới mặt nước, kéo hướng nhìn; khi i vượt 48,8° mặt nước chuyển sang phản chiếu đáy.",
  "diem_nhan": "Đặt mắt phía trên mặt nước: kéo mọi góc vẫn nhìn xuyên qua được."}}

for tn in (tn1, tn2, tn3):
    (KHO / f"{tn['id']}.json").write_text(json.dumps(tn, ensure_ascii=False, indent=1), encoding="utf8")
    print("ghi", tn["id"])
print(hang, hang3)
