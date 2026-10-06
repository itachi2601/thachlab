"""Sinh 3 mục kho thí nghiệm (content/thi-nghiem/) và bundle.json. Chạy sau build.py."""
import json, math, pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
r = lambda v: round(v + 0.0, 2)
base = {"mon": "vat-ly", "lop": 11, "bai": "Bài 1. Dao động điều hoà", "lesson_id": 20,
        "nguon_trong_bai": "content/lesson-samples/l11-dao-dong-dieu-hoa/theory.html"}
def tp(k, ten, dv, kieu, **kw): return {"ky_hieu": k, "ten": ten, "don_vi": dv, "kieu": kieu, **kw}

def x_cm(A, w, ph, t): return r(A * math.cos(w * t + ph))

tn1 = {**base, "id": "tn-l11-daodongdieuhoa-01", "ten": "Con lắc lò xo: dao động quanh vị trí cân bằng", "loai": "thi_nghiem", "muc_do": "co_ban",
 "kien_thuc": ["daodong.dao_dong_co", "daodong.vi_tri_can_bang"],
 "muc_tieu": "Thấy vật dao động qua lại hai bên vị trí cân bằng (chỗ vật đứng yên ban đầu) khi kéo lệch rồi thả.",
 "dung_cu": [{"ten": "Lò xo", "so_luong": 1}, {"ten": "Vật nặng (quả cân)", "so_luong": 1}, {"ten": "Giá đỡ hoặc đường ray ngang", "so_luong": 1}],
 "cac_buoc": {"lam": ["Cho vật đứng yên trên lò xo, đánh dấu vị trí đó.", "Kéo vật lệch ra rồi thả tay."],
              "quan_sat": ["Vật đi qua lại hai bên vị trí đánh dấu.", "Biên độ giảm dần rất chậm do ma sát."],
              "rut_ra": ["Vị trí đánh dấu là vị trí cân bằng.", "Dao động cơ là chuyển động qua lại quanh vị trí cân bằng."]},
 "tham_so": [tp("A", "Độ kéo lệch ban đầu (biên độ)", "cm", "dieu_chinh", min=2, max=10, mac_dinh=5, buoc=1),
             tp("T", "Chu kì", "s", "dieu_chinh", min=0.5, max=3, mac_dinh=1, buoc=0.5),
             tp("x", "Li độ tại thời điểm t", "cm", "tinh_ra")],
 "mo_hinh": {"phuong_trinh": ["x = A·cos(2π·t/T)"], "gia_thiet": ["bỏ qua ma sát, biên độ không đổi", "thả tay lúc t = 0 ở biên dương"]},
 "so_lieu_mau": {"cot": ["A (cm)", "T (s)", "t (s)", "x (cm)"],
                 "hang": [[5, 1, t, x_cm(5, 2 * math.pi / 1, 0, t)] for t in (0, 0.25, 0.5, 0.75, 1)],
                 "ghi_chu": "Tính từ mô hình, không phải số đo thật."},
 "ket_qua_ky_vong": "Với A = 5 cm, T = 1 s: x = 5 cm lúc t = 0, 0 lúc t = 0,25 s, −5 cm lúc t = 0,5 s.",
 "hien_tuong_hay_sai": ["Cho rằng vị trí cân bằng là vị trí lò xo không biến dạng (khi treo thẳng đứng thì không phải).", "Nhầm li độ với quãng đường đã đi."],
 "goi_y_mo_phong": {"loai": "2d_dong_hoc+do_thi", "dieu_khien": ["A", "T"], "dau_ra": ["vật chạy qua lại", "điểm chạy trên đồ thị x–t"], "hinh_trong_bai": "Hình 1",
                    "y_tuong": "Kéo vật bằng chuột, thả ra; hiện nhãn −A, O, +A trên trục."}}

tn2 = {**base, "id": "tn-l11-daodongdieuhoa-02", "ten": "Cây bút trên vật dao động tự vẽ đồ thị li độ – thời gian", "loai": "thi_nghiem", "muc_do": "co_ban",
 "kien_thuc": ["daodong.do_thi_sin", "daodong.bien_do", "daodong.chu_ki"],
 "muc_tieu": "Thấy đồ thị li độ theo thời gian của dao động điều hoà có dạng hình sin; đọc được biên độ A và chu kì T.",
 "dung_cu": [{"ten": "Con lắc lò xo", "so_luong": 1}, {"ten": "Bút dạ gắn lên vật nặng", "so_luong": 1}, {"ten": "Tờ giấy dài kéo đều", "so_luong": 1, "ghi_chu": "kéo đều tay hoặc dùng băng giấy chạy bằng động cơ"}],
 "cac_buoc": {"lam": ["Gắn bút lên vật, đầu bút chạm giấy.", "Cho vật dao động, kéo giấy chạy đều vuông góc phương dao động."],
              "quan_sat": ["Nét bút là đường lượn sóng đều đặn.", "Khoảng cách theo chiều dọc từ trục đến đỉnh là A; khoảng cách giữa hai đỉnh liền kề ứng với T."],
              "rut_ra": ["Đồ thị li độ – thời gian có dạng hình sin.", "A là giá trị lớn nhất của li độ; T là thời gian một dao động."]},
 "tham_so": [tp("A", "Biên độ", "cm", "dieu_chinh", min=2, max=10, mac_dinh=5, buoc=1),
             tp("T", "Chu kì", "s", "dieu_chinh", min=0.5, max=4, mac_dinh=2, buoc=0.5),
             tp("phi", "Pha ban đầu", "rad", "dieu_chinh", min=0, max=6.28, mac_dinh=0, buoc=0.1),
             tp("x", "Li độ", "cm", "tinh_ra")],
 "mo_hinh": {"phuong_trinh": ["x = A·cos(2π·t/T + phi)"], "gia_thiet": ["giấy chạy đều nên trục ngang tỉ lệ với thời gian", "bỏ qua tắt dần"]},
 "so_lieu_mau": {"cot": ["A (cm)", "T (s)", "phi (rad)", "t (s)", "x (cm)"],
                 "hang": [[5, 2, 0, t, x_cm(5, math.pi, 0, t)] for t in (0, 0.5, 1, 1.5, 2)],
                 "ghi_chu": "Tính từ mô hình, không phải số đo thật."},
 "ket_qua_ky_vong": "Với A = 5 cm, T = 2 s, phi = 0: x = 5, 0, −5, 0, 5 cm tại t = 0; 0,5; 1; 1,5; 2 s.",
 "hien_tuong_hay_sai": ["Cho rằng biên độ có thể âm.", "Đọc chu kì là khoảng cách từ đỉnh đến đáy (đó chỉ là nửa chu kì)."],
 "goi_y_mo_phong": {"loai": "do_thi+bang_so_lieu", "dieu_khien": ["A", "T", "phi"], "dau_ra": ["đường x–t vẽ dần theo thời gian", "nhãn A, −A, T"], "hinh_trong_bai": "Hình 2",
                    "y_tuong": "Kéo thanh trượt phi để đường cong dịch ngang; hiện chấm đỏ tại t = 0."}}

w = 2
tn3 = {**base, "id": "tn-l11-daodongdieuhoa-03", "ten": "Bóng của van xe đạp: hình chiếu của chuyển động tròn đều", "loai": "vi_du", "muc_do": "co_ban",
 "kien_thuc": ["daodong.phuong_trinh", "daodong.hinh_chieu_tron_deu"],
 "muc_tieu": "Thấy hình chiếu của chuyển động tròn đều lên một đường thẳng là dao động điều hoà; nối ω với tốc độ góc, A với bán kính.",
 "dung_cu": [{"ten": "Bánh xe đạp dựng thẳng đứng, quay đều", "so_luong": 1}, {"ten": "Đèn pin chiếu từ phía trước", "so_luong": 1}, {"ten": "Tường hoặc màn hứng bóng", "so_luong": 1}],
 "cac_buoc": {"lam": ["Quay bánh xe đều, chiếu đèn pin để bóng van xe rơi lên tường."],
              "quan_sat": ["Van xe chạy vòng tròn.", "Bóng của van chạy qua lại trên một đường thẳng, chậm lại ở hai đầu."],
              "rut_ra": ["Bóng (hình chiếu) dao động điều hoà.", "Biên độ bằng bán kính, tần số góc bằng tốc độ góc của bánh xe."]},
 "tham_so": [tp("A", "Bán kính đường tròn (biên độ)", "cm", "dieu_chinh", min=2, max=10, mac_dinh=10, buoc=1),
             tp("omega", "Tốc độ góc (tần số góc)", "rad/s", "dieu_chinh", min=1, max=10, mac_dinh=2, buoc=0.5),
             tp("phi", "Góc ban đầu của M (pha ban đầu)", "rad", "dieu_chinh", min=0, max=6.28, mac_dinh=0, buoc=0.1),
             tp("x", "Li độ của hình chiếu Q", "cm", "tinh_ra")],
 "mo_hinh": {"phuong_trinh": ["x = A·cos(omega·t + phi)"], "gia_thiet": ["M quay đều", "đèn chiếu song song, lên đường kính nằm ngang"]},
 "so_lieu_mau": {"cot": ["A (cm)", "omega (rad/s)", "phi (rad)", "t (s)", "x (cm)"],
                 "hang": [[10, w, 0, t, x_cm(10, w, 0, t)] for t in (0, 1, 2, 3)],
                 "ghi_chu": "Tính từ mô hình (góc theo rad), không phải số đo thật."},
 "ket_qua_ky_vong": "Với A = 10 cm, omega = 2 rad/s, phi = 0: x = 10; −4,16; −6,54; 9,60 cm tại t = 0; 1; 2; 3 s.",
 "hien_tuong_hay_sai": ["Cho rằng bóng chuyển động đều như van xe (thực ra chậm ở biên, nhanh ở giữa).", "Nhầm ω của dao động với tần số vòng/giây."],
 "goi_y_mo_phong": {"loai": "2d_dong_hoc+do_thi", "dieu_khien": ["A", "omega", "phi"], "dau_ra": ["M quay đều, Q chạy trên trục x", "đồ thị x–t song song"], "hinh_trong_bai": "Hình 3",
                    "y_tuong": "Hai khung cạnh nhau: vòng tròn bên trái, đồ thị x–t bên phải, điểm Q nối bằng đường nét đứt."}}

for tn in (tn1, tn2, tn3):
    p = ROOT / "content/thi-nghiem" / f"{tn['id']}.json"
    p.write_text(json.dumps(tn, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

def q(question, opts, ans, expl): return {"type": "multiple_choice", "question": question, "options": opts, "answer": ans, "explanation": expl}
exam = {"title": "Luyện tập — Dao động điều hoà", "duration_minutes": 10, "questions": [
  q("Vật dao động theo $x = 4\\cos(\\pi t)$ cm. Khi vật ở biên phía âm, li độ bằng:", ["4 cm", "−4 cm", "0", "8 cm"], 1, "Li độ là vị trí so với VTCB: biên phía âm có x = −A = −4 cm."),
  q("Biên độ của dao động $x = -3\\cos(2t)$ cm là:", ["−3 cm", "3 cm", "6 cm", "2 cm"], 1, "Biên độ luôn dương; −cos α = cos(α + π)."),
  q("Vật dao động theo $x = 10\\cos(2\\pi t)$ cm. Lúc $t = 0{,}25$ s, li độ bằng:", ["10 cm", "−10 cm", "0", "5 cm"], 2, "Pha = 2π·0,25 = π/2, nên x = 10cos(π/2) = 0."),
  q("Vật dao động theo $x = 6\\cos(5\\pi t + \\pi/2)$ cm. Lúc $t = 0{,}1$ s, li độ bằng:", ["6 cm", "0", "−6 cm", "3 cm"], 2, "Pha = 5π·0,1 + π/2 = π, nên x = 6cosπ = −6 cm."),
  q("Dao động $x = 5\\cos(2\\pi t + \\pi/3)$ cm có li độ lúc t = 0 là:", ["5 cm", "2,5 cm", "0", "4,33 cm"], 1, "x(0) = 5cos(π/3) = 2,5 cm."),
]}
import re
bundle = {"schema": "thachlab.lesson-bundle/v1", "target": {"class_name": "Vật lí 11", "lesson_title": "Bài 1. Dao động điều hoà"},
          "theory_title": "Lý thuyết trọng tâm", "theory_subtitle": "Từ cái đu đến phương trình dao động điều hoà",
          "theory_html": (HERE / "theory.html").read_text(encoding="utf-8"), "worked_examples": [], "exam": exam, "raster_images": []}
(HERE / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ok")
