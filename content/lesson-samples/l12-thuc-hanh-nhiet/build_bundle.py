"""Đóng gói theory.html + 6 câu tự kiểm tra thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_bundle.py
"""
import json

EXAM = {
    "title": "Luyện tập — Ba phép đo nhiệt trong bài thực hành",
    "duration_minutes": 10,
    "questions": [
        {
            "type": "multiple_choice",
            "question": "Trong bài thực hành đo nhiệt dung riêng của nước, nhiệt lượng bếp đã truyền cho nước được xác định bằng cách nào?",
            "options": [
                "Lấy công suất ghi trên oát kế nhân với thời gian đun: Q = P·τ.",
                "Đọc trực tiếp trên nhiệt kế rồi nhân với khối lượng nước.",
                "Lấy hiệu nhiệt độ cuối và nhiệt độ đầu nhân với khối lượng nước.",
                "Lấy nhiệt độ cuối chia cho thời gian đun.",
            ],
            "answer": 0,
            "explanation": "Không có dụng cụ đo thẳng nhiệt lượng, nên phải suy ra từ công suất và thời gian: Q = P·τ. Nhiệt độ chỉ dùng để tính Δt, còn khối lượng để quy về 1 kg.",
        },
        {
            "type": "multiple_choice",
            "question": "Trên đồ thị nhiệt độ – thời gian của một chất đang được đun, đoạn nằm ngang cho biết",
            "options": [
                "bếp đã ngừng truyền nhiệt cho chất.",
                "chất đang chuyển thể: nhiệt vào dùng để phá liên kết nên nhiệt độ không đổi.",
                "nhiệt kế bị hỏng, cần thay nhiệt kế khác.",
                "chất đang nguội đi vì nhiệt thoát ra môi trường.",
            ],
            "answer": 1,
            "explanation": "Đoạn nằm ngang là lúc nóng chảy hoặc sôi. Nhiệt vẫn vào liên tục nhưng dùng để phá liên kết giữa các phân tử, không làm nhiệt độ tăng — đây thường là giai đoạn tốn nhiều nhiệt nhất.",
        },
        {
            "type": "multiple_choice",
            "question": "Bếp 150 W đun 0,200 kg nước; trong 300 s nhiệt độ nước tăng 60 °C. Nhiệt dung riêng đo được là",
            "options": ["1,25 J/(kg·K).", "3 750 J/(kg·K).", "18 000 J/(kg·K).", "45 000 J/(kg·K)."],
            "answer": 1,
            "explanation": "c = P·τ/(m·Δt) = (150 × 300)/(0,200 × 60) = 45 000/12 = 3 750 J/(kg·K). Kết quả thấp hơn 4 180 khoảng 10% vì một phần nhiệt đã mất ra môi trường — sai số hệ thống.",
        },
        {
            "type": "multiple_choice",
            "question": "Đun 0,100 kg nước đá đang tan bằng bếp 100 W; sau 334 s thì đá tan hoàn toàn. Nhiệt nóng chảy riêng đo được là",
            "options": ["3,34 × 10³ J/kg.", "3,34 × 10⁴ J/kg.", "3,34 × 10⁵ J/kg.", "3,34 × 10⁶ J/kg."],
            "answer": 2,
            "explanation": "λ = P·τ/m = (100 × 334)/0,100 = 33 400/0,100 = 3,34 × 10⁵ J/kg. Đúng bậc với giá trị tra bảng của nước đá.",
        },
        {
            "type": "multiple_choice",
            "question": "Một bạn tính nhiệt dung riêng theo công thức c = (500 × 120)/(500 × 40) với P tính bằng W, τ bằng s, m bằng g và Δt bằng K, rồi ra 3,0 J/(kg·K). Lỗi nằm ở đâu?",
            "options": [
                "Phải đổi thời gian 120 s thành 2 phút.",
                "Phải đổi khối lượng 500 g thành 0,500 kg.",
                "Phải đổi 40 K thành 313 K.",
                "Không có lỗi, 3,0 J/(kg·K) là kết quả đúng.",
            ],
            "answer": 1,
            "explanation": "Khối lượng trong công thức phải tính bằng kilôgam: c = (500 × 120)/(0,500 × 40) = 3 000 J/(kg·K). Để gam thì kết quả nhỏ đi 1 000 lần. Δt là một khoảng nhiệt độ nên 40 K = 40 °C, không cộng 273.",
        },
        {
            "type": "multiple_choice",
            "question": "Hai cách tính nhiệt dung riêng (theo từng mốc số liệu và theo độ dốc đồ thị) cho hai kết quả lệch nhau 4%. Kết luận đúng là",
            "options": [
                "Một trong hai cách chắc chắn sai, phải chọn cách cho kết quả gần 4 180 hơn.",
                "Phải bỏ cả hai kết quả và làm lại thí nghiệm.",
                "Hai kết quả gần nhau trong phạm vi sai số; cần nêu nguyên nhân chênh lệch, thường là mất nhiệt ra môi trường.",
                "Phải lấy trung bình cộng của hai kết quả làm kết quả cuối cùng.",
            ],
            "answer": 2,
            "explanation": "Cả hai cách đều đúng trong phạm vi sai số; việc phải làm là giải thích chênh lệch (mất nhiệt, nhiệt kế chạm thành bình, lệch thời điểm bấm đồng hồ), chứ không phải chọn số đẹp hơn.",
        },
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 12",
               "lesson_title": "Bài 4. Thực hành đo nhiệt dung riêng, nhiệt nóng chảy riêng, nhiệt hoá hơi riêng"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Ba phép đo nhiệt trong bài thực hành",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}

with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("ok", len(bundle["theory_html"]), "bytes theory")
