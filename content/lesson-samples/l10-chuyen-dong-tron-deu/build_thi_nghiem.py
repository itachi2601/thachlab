"""Ghi 4 file thí nghiệm/ví dụ của Bài 31 (lesson 76) vào content/thi-nghiem/ và cung cấp số liệu đo cho build_figs.py.
Một nguồn số liệu: bảng trong theory.html và so_lieu_mau trong JSON cùng tính từ các hàm dưới đây.
Chạy: python3 build_thi_nghiem.py   (từ thư mục bài) — sửa số/chữ ở đây rồi build lại, đừng sửa tay JSON.
"""
import json, math, pathlib

HERE = pathlib.Path(__file__).resolve().parent
DIR = HERE.parents[1] / "thi-nghiem"
BAI = "Bài 31. Động học của chuyển động tròn đều"
NGUON = "content/lesson-samples/l10-chuyen-dong-tron-deu/theory.html"

# Thí nghiệm đo: thời gian đĩa xoay lò vi sóng quay 3 vòng, 5 lần đo (số liệu minh hoạ quanh T0 = 10,0 s)
T0 = 10.0
N_VONG = 3
R_BANG_DINH = 0.14  # m
DO_3_VONG = [30.2, 29.8, 30.1, 30.4, 29.9]


def xu_li_do():
    tb = sum(DO_3_VONG) / len(DO_3_VONG)
    T = tb / N_VONG
    lech = [abs(x - tb) for x in DO_3_VONG]
    m = max(lech)
    lan = [str(i) for i, d in enumerate(lech, 1) if abs(d - m) < 1e-6]   # so tập cực đại có dung sai
    return {"tb": tb, "T": T, "f": 1 / T, "w": 2 * math.pi / T, "v": 2 * math.pi * R_BANG_DINH / T,
            "lech_nhat": " và ".join(lan)}


def vn(x, nd):
    return f"{x:.{nd}f}".replace(".", ",")


def r(x, n=3):
    return round(x, n)


def chung(id_, ten, loai, muc_do, kien_thuc):
    return {"mon": "vat-ly", "lop": 10, "bai": BAI, "lesson_id": 76, "nguon_trong_bai": NGUON,
            "id": id_, "ten": ten, "loai": loai, "muc_do": muc_do, "kien_thuc": kien_thuc}


def tn01():
    d = chung("tn-l10-trondeu-01", "Đội hình xoay trên sân băng: cùng tốc độ góc, khác tốc độ", "vi_du", "co_ban",
              ["trondeu.toc_do_goc", "trondeu.v_bang_omega_r"])
    T = 5.0
    d.update({
        "muc_tieu": "Phân biệt tốc độ góc (chung cho cả hàng) với tốc độ (tăng theo khoảng cách tới tâm) qua một đội hình xoay trên sân băng.",
        "dung_cu": [{"ten": "Nhóm 4 người trượt băng nắm tay thành hàng ngang", "so_luong": 1},
                    {"ten": "Đồng hồ bấm giây", "so_luong": 1}],
        "cac_buoc": {
            "lam": ["Người đầu hàng đứng trụ ở tâm, cả hàng nắm tay giữ thẳng rồi xoay quanh người trụ.",
                    "Bấm giờ thời gian cả hàng quay một vòng; đo khoảng cách từng người tới người trụ."],
            "quan_sat": ["Cả hàng luôn thẳng: mọi người quay hết một vòng cùng lúc.",
                         "Người ngoài cùng phải đạp chân liên tục, người gần tâm gần như chỉ xoay người."],
            "rut_ra": ["Mọi người có cùng tốc độ góc ω = 2π/T.",
                       "Tốc độ v = ωr tỉ lệ với khoảng cách tới tâm: người ngoài cùng nhanh nhất."]},
        "tham_so": [
            {"ky_hieu": "T", "ten": "Thời gian cả hàng quay một vòng", "don_vi": "s", "kieu": "dieu_chinh",
             "min": 3, "max": 10, "mac_dinh": T, "buoc": 0.5},
            {"ky_hieu": "r", "ten": "Khoảng cách từ người đang xét tới tâm", "don_vi": "m", "kieu": "dieu_chinh",
             "min": 0, "max": 8, "mac_dinh": 6, "buoc": 0.5},
            {"ky_hieu": "omega", "ten": "Tốc độ góc chung của cả hàng", "don_vi": "rad/s", "kieu": "tinh_ra"},
            {"ky_hieu": "v", "ten": "Tốc độ của người cách tâm r", "don_vi": "m/s", "kieu": "tinh_ra"}],
        "mo_hinh": {"phuong_trinh": ["omega = 2·pi/T", "v = omega·r", "v = 2·pi·r/T"],
                    "gia_thiet": ["hàng người giữ thẳng như một vật rắn", "cả hàng quay đều quanh người trụ"]},
        "so_lieu_mau": {"cot": ["r (m)", "ω (rad/s)", "v (m/s)", "v (km/h)"],
                        "hang": [[x, r(2 * math.pi / T), r(2 * math.pi * x / T, 2), r(2 * math.pi * x / T * 3.6, 1)]
                                 for x in (0, 2, 4, 6)],
                        "ghi_chu": "Số liệu minh hoạ tính từ mô hình với T = 5 s; chưa phải số đo thật."},
        "ket_qua_ky_vong": "Mọi người cùng ω ≈ 1,26 rad/s; người cách tâm 6 m chạy khoảng 7,5 m/s (≈ 27 km/h).",
        "hien_tuong_hay_sai": ["Nghĩ nắm tay nhau thì mọi người cùng tốc độ.",
                               "Nghĩ người ngoài cùng quay hết một vòng nhanh hơn (khác chu kì).",
                               "Nghĩ người gần trục chạy nhanh hơn."],
        "an_toan": "Chỉ làm khi có huấn luyện viên; người ngoài cùng là người trượt vững nhất.",
        "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu",
                           "y_tuong": "Hàng chấm tròn quay quanh tâm nhìn từ trên; thanh trượt T và chọn người; mỗi người để lại vệt cung trong cùng Δt, bảng ω và v tự cập nhật.",
                           "diem_nhan": "Cùng Δt mọi vệt quét cùng góc nhưng vệt ngoài dài gấp nhiều lần vệt trong."},
    })
    return d


def tn02():
    d = chung("tn-l10-trondeu-02", "Một radian dài bao nhiêu: quấn sợi chỉ dài bằng bán kính quanh nắp nồi", "thi_nghiem",
              "co_ban", ["trondeu.radian"])
    hang = []
    for rr, do in ((8.0, 56), (10.0, 58), (12.5, 57)):
        hang.append([rr, rr, r(math.degrees(1.0), 1), do])
    d.update({
        "muc_tieu": "Thấy được 1 rad là góc chắn cung dài bằng bán kính, khoảng 57°, không phụ thuộc cỡ đường tròn.",
        "dung_cu": [{"ten": "Nắp nồi hoặc đĩa tròn các cỡ", "so_luong": 3},
                    {"ten": "Sợi chỉ, kéo, thước kẻ", "so_luong": 1},
                    {"ten": "Thước đo độ, bút dạ", "so_luong": 1}],
        "cac_buoc": {
            "lam": ["Đo bán kính r của nắp; cắt sợi chỉ dài đúng bằng r.",
                    "Quấn sát sợi chỉ theo vành nắp từ điểm A, đánh dấu điểm cuối B; nối A, B với tâm O.",
                    "Đo góc AOB bằng thước đo độ; làm lại với hai nắp cỡ khác."],
            "quan_sat": ["Góc AOB đo được khoảng 57° ở cả ba nắp."],
            "rut_ra": ["1 rad là góc ở tâm chắn cung dài bằng bán kính: θ = s/r.",
                       "Cả vòng dài 2πr nên ứng với 2π rad, tức 180° = π rad."]},
        "tham_so": [
            {"ky_hieu": "r", "ten": "Bán kính nắp", "don_vi": "cm", "kieu": "dieu_chinh", "min": 5, "max": 15,
             "mac_dinh": 10, "buoc": 0.5},
            {"ky_hieu": "s", "ten": "Độ dài sợi chỉ quấn theo vành", "don_vi": "cm", "kieu": "dieu_chinh", "min": 1,
             "max": 30, "mac_dinh": 10, "buoc": 0.5},
            {"ky_hieu": "theta", "ten": "Góc ở tâm chắn cung", "don_vi": "rad", "kieu": "tinh_ra"},
            {"ky_hieu": "theta_do", "ten": "Góc đo bằng thước đo độ", "don_vi": "°", "kieu": "do_duoc", "sai_so_do": 1}],
        "mo_hinh": {"phuong_trinh": ["theta = s/r (rad)", "theta_do = theta·180/pi"],
                    "gia_thiet": ["sợi chỉ không giãn, quấn sát vành", "vành nắp là đường tròn"]},
        "so_lieu_mau": {"cot": ["r (cm)", "s (cm)", "θ lí thuyết (°)", "θ đo (°)"], "hang": hang,
                        "ghi_chu": "Cột θ đo là số minh hoạ (lệch ±1° do quấn chỉ và đọc thước đo độ); chưa phải số đo thật."},
        "ket_qua_ky_vong": "Góc chắn cung dài bằng bán kính luôn xấp xỉ 57,3° = 1 rad với mọi cỡ nắp.",
        "hien_tuong_hay_sai": ["Nghĩ nắp to thì 1 rad lớn hơn.", "Nhầm 1 rad với 1°.",
                               "Dùng θ = s·r hoặc r/s thay vì s/r."],
        "sai_so_thuong_gap": "Sợi chỉ quấn không sát vành hoặc bị giãn; xác định tâm nắp lệch; đọc thước đo độ lệch 1°.",
        "goi_y_mo_phong": {"loai": "2d_dong_hoc",
                           "y_tuong": "Kéo độ dài cung s trên đường tròn bán kính r; góc θ = s/r hiện cả rad và độ.",
                           "diem_nhan": "Đặt s = r ở mọi r: góc luôn 57,3°."},
    })
    return d


def tn03():
    kq = xu_li_do()
    d = chung("tn-l10-trondeu-03", "Đo chu kì quay của đĩa xoay lò vi sóng, suy ra tần số và tốc độ góc", "thi_nghiem",
              "trung_binh", ["trondeu.chu_ki_tan_so", "trondeu.toc_do_goc"])
    d.update({
        "muc_tieu": "Đo thời gian nhiều vòng để tìm chu kì T, suy ra f và ω; nhận xét sai số do bấm đồng hồ bằng tay.",
        "dung_cu": [{"ten": "Lò vi sóng có đĩa xoay, cốc nước nhỏ đặt giữa đĩa", "so_luong": 1},
                    {"ten": "Băng dính màu", "so_luong": 1},
                    {"ten": "Đồng hồ bấm giây (điện thoại)", "so_luong": 1},
                    {"ten": "Thước kẻ", "so_luong": 1}],
        "cac_buoc": {
            "lam": ["Dán băng dính lên mép đĩa xoay, cách tâm 14,0 cm; đặt cốc nước nhỏ giữa đĩa.",
                    "Bật lò, bấm đồng hồ đo thời gian đĩa quay 3 vòng; làm 5 lần."],
            "quan_sat": [f"Thời gian 3 vòng: {'; '.join(vn(x, 1) for x in DO_3_VONG)} s."],
            "rut_ra": [f"T ≈ {vn(kq['T'], 2)} s, f ≈ {vn(kq['f'], 3)} Hz, ω ≈ {vn(kq['w'], 3)} rad/s.",
                       "Đo nhiều vòng rồi chia giúp giảm sai số do phản xạ tay khi bấm đồng hồ."]},
        "tham_so": [
            {"ky_hieu": "T0", "ten": "Chu kì thật của đĩa xoay", "don_vi": "s", "kieu": "dieu_chinh", "min": 8,
             "max": 12, "mac_dinh": T0, "buoc": 0.5},
            {"ky_hieu": "r", "ten": "Khoảng cách băng dính tới tâm", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.05,
             "max": 0.15, "mac_dinh": R_BANG_DINH, "buoc": 0.01},
            {"ky_hieu": "n", "ten": "Số vòng đếm mỗi lần đo", "don_vi": "vòng", "kieu": "co_dinh", "gia_tri": N_VONG},
            {"ky_hieu": "dt", "ten": "Thời gian n vòng đo bằng đồng hồ", "don_vi": "s", "kieu": "do_duoc",
             "sai_so_do": 0.2},
            {"ky_hieu": "T", "ten": "Chu kì suy ra", "don_vi": "s", "kieu": "tinh_ra"},
            {"ky_hieu": "f", "ten": "Tần số", "don_vi": "Hz", "kieu": "tinh_ra"},
            {"ky_hieu": "omega", "ten": "Tốc độ góc", "don_vi": "rad/s", "kieu": "tinh_ra"}],
        "mo_hinh": {"phuong_trinh": ["T = dt/n", "f = 1/T", "omega = 2·pi/T", "v = omega·r"],
                    "gia_thiet": ["đĩa quay đều", "sai số chủ yếu do phản xạ tay khi bấm (cỡ 0,2 s mỗi lần)"]},
        "so_lieu_mau": {"cot": ["Lần", "Thời gian 3 vòng (s)", "T = dt/3 (s)"],
                        "hang": [[i, x, r(x / N_VONG)] for i, x in enumerate(DO_3_VONG, 1)],
                        "ghi_chu": f"Số liệu minh hoạ quanh T0 = {T0} s (đĩa lò vi sóng thường 5–6 vòng/phút); trung bình {kq['tb']:.2f} s → T = {kq['T']:.3f} s, ω = {kq['w']:.3f} rad/s, tốc độ băng dính v = {kq['v']:.4f} m/s. Chưa phải số đo thật."},
        "ket_qua_ky_vong": "T ≈ 10 s, f ≈ 0,1 Hz, ω ≈ 0,63 rad/s; các lần đo 3 vòng lệch nhau dưới 0,4 s.",
        "hien_tuong_hay_sai": ["Đo một vòng rồi lấy luôn làm T (sai số tay lớn).",
                               "Quên chia cho số vòng khi tính T.",
                               "Nhầm f với ω (quên nhân 2π)."],
        "sai_so_thuong_gap": "Phản xạ tay khi bấm bắt đầu/kết thúc; khó nhận đúng lúc băng dính qua mốc; đĩa có thể khựng nhẹ khi bánh xe lăn qua chỗ gồ.",
        "an_toan": "Không bật lò khi trống: luôn đặt cốc nước bên trong; không cho kim loại vào lò.",
        "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu",
                           "y_tuong": "Đĩa quay nhìn từ trên với mốc băng dính; học sinh bấm nút bắt đầu/dừng như đồng hồ, mô phỏng cộng thêm độ trễ phản xạ ngẫu nhiên; bảng tự tính T, f, ω.",
                           "diem_nhan": "So sai số khi đếm 1 vòng và 10 vòng."},
    })
    return d


def tn04():
    n, D = 180, 0.66
    d = chung("tn-l10-trondeu-04", "Giọt nước văng khỏi bánh xe đạp: bay theo phương tiếp tuyến", "vi_du", "co_ban",
              ["trondeu.van_toc_tiep_tuyen"])
    d.update({
        "muc_tieu": "Thấy vectơ vận tốc trong chuyển động tròn nằm theo tiếp tuyến: vật rời đường tròn thì bay thẳng theo tiếp tuyến.",
        "dung_cu": [{"ten": "Xe đạp (bánh Ø660 mm) dựng ngược trên yên và tay lái", "so_luong": 1},
                    {"ten": "Bình xịt nước nhỏ", "so_luong": 1},
                    {"ten": "Tấm bìa cứng chắn phía sau để thấy vệt nước", "so_luong": 1}],
        "cac_buoc": {
            "lam": ["Xịt nước lên lốp rồi quay bánh xe bằng tay; người xem đứng lệch sang bên, tránh mặt phẳng bánh."],
            "quan_sat": ["Giọt nước bắn thành vệt thẳng, sát vành bánh, không bắn theo bán kính ra ngoài."],
            "rut_ra": ["Giọt nước rời bánh thì giữ vận tốc ở chỗ rời: phương tiếp tuyến, chiều theo chiều quay."]},
        "tham_so": [
            {"ky_hieu": "n", "ten": "Tốc độ quay của bánh xe", "don_vi": "vòng/phút", "kieu": "dieu_chinh", "min": 60,
             "max": 300, "mac_dinh": n, "buoc": 10},
            {"ky_hieu": "D", "ten": "Đường kính bánh xe", "don_vi": "m", "kieu": "co_dinh", "gia_tri": D},
            {"ky_hieu": "omega", "ten": "Tốc độ góc của bánh xe", "don_vi": "rad/s", "kieu": "tinh_ra"},
            {"ky_hieu": "v", "ten": "Tốc độ giọt nước lúc rời vành bánh", "don_vi": "m/s", "kieu": "tinh_ra"}],
        "mo_hinh": {"phuong_trinh": ["omega = 2·pi·n/60", "v = omega·D/2", "hướng v: tiếp tuyến, vuông góc bán kính tại điểm rời"],
                    "gia_thiet": ["bỏ qua trọng lực và lực cản trong đoạn bay ngắn ngay sau khi rời bánh"]},
        "so_lieu_mau": {"cot": ["n (vòng/phút)", "ω (rad/s)", "v (m/s)"],
                        "hang": [[x, r(2 * math.pi * x / 60, 1), r(2 * math.pi * x / 60 * D / 2, 1)] for x in (60, 180, 300)],
                        "ghi_chu": "Số liệu tính từ mô hình với bánh Ø660 mm; 180 vòng/phút là tốc độ quay bằng tay khá nhanh."},
        "ket_qua_ky_vong": "Giọt nước rời bánh với tốc độ khoảng 6 m/s theo đúng phương tiếp tuyến tại điểm tiếp xúc.",
        "hien_tuong_hay_sai": ["Nghĩ giọt nước bắn theo bán kính, ra xa tâm.",
                               "Nghĩ giọt nước còn cong theo vành bánh một đoạn rồi mới bay thẳng.",
                               "Lấy đúng phương tiếp tuyến nhưng ngược chiều quay."],
        "an_toan": "Đứng lệch sang bên, không đưa tay vào nan hoa khi bánh đang quay.",
        "goi_y_mo_phong": {"loai": "2d_dong_hoc",
                           "y_tuong": "Bánh xe quay, chọn điểm trên vành; giọt nước rời bánh vẽ vệt thẳng; bật/tắt mũi tên vận tốc tiếp tuyến.",
                           "diem_nhan": "Cho học sinh đoán hướng tia lửa trước khi giọt nước rời bánh ở điểm thấp nhất."},
    })
    return d


def ghi_tat_ca():
    for d in (tn01(), tn02(), tn03(), tn04()):
        (DIR / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf8")
        print("ghi", d["id"])


if __name__ == "__main__":
    ghi_tat_ca()
    print(xu_li_do())
