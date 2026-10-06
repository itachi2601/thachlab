"""Đóng gói theory.html + 5 câu tự kiểm tra thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này:  python3 build_bundle.py
"""
import json

EXAM = {
    "title": "Luyện tập — Sự chuyển thể",
    "duration_minutes": 10,
    "questions": [
        {
            "type": "multiple_choice",
            "question": "Theo mô hình động học phân tử, tốc độ chuyển động của các phân tử phụ thuộc chủ yếu vào yếu tố nào?",
            "options": ["Áp suất của chất", "Nhiệt độ của vật", "Khối lượng riêng của chất", "Thể tích của chất"],
            "answer": 1,
            "explanation": "Các phân tử chuyển động không ngừng; nhiệt độ của vật càng cao thì tốc độ chuyển động trung bình của các phân tử càng lớn.",
        },
        {
            "type": "multiple_choice",
            "question": "Giữa hai phân tử, lực hút chiếm ưu thế trong trường hợp nào?",
            "options": ["Khi hai phân tử ở gần nhau", "Khi hai phân tử ở xa nhau", "Khi nhiệt độ tăng cao", "Lực hút luôn bằng lực đẩy"],
            "answer": 1,
            "explanation": "Khi các phân tử gần nhau thì lực đẩy chiếm ưu thế, khi xa nhau thì lực hút chiếm ưu thế — mẹo nhớ “gần đẩy, xa hút”.",
        },
        {
            "type": "multiple_choice",
            "question": "Đổ 50 ml rượu vào 50 ml nước, hỗn hợp thu được có thể tích",
            "options": ["bằng đúng 100 ml.", "lớn hơn 100 ml.", "nhỏ hơn 100 ml.", "không xác định được."],
            "answer": 2,
            "explanation": "Giữa các phân tử có khoảng cách nên phân tử rượu xen vào khoảng trống giữa các phân tử nước và ngược lại, làm thể tích hỗn hợp giảm.",
        },
        {
            "type": "multiple_choice",
            "question": "Một khối nước đá đang tan ở 0 °C, ta vẫn tiếp tục đun. Trong lúc đá đang tan:",
            "options": [
                "nhiệt độ tăng, nhiệt lượng truyền vào bằng 0.",
                "nhiệt độ không đổi, nhiệt lượng truyền vào vẫn khác 0.",
                "cả nhiệt độ và nhiệt lượng đều không đổi.",
                "cả nhiệt độ và nhiệt lượng đều tăng.",
            ],
            "answer": 1,
            "explanation": "Đang chuyển thể thì nhiệt độ không đổi, nhưng nhiệt lượng vẫn được truyền vào và dùng để phá vỡ liên kết trong mạng tinh thể.",
        },
        {
            "type": "multiple_choice",
            "question": "Sự bay hơi khác sự sôi ở điểm nào?",
            "options": [
                "Bay hơi chỉ xảy ra ở mặt thoáng; sôi xảy ra ở cả trong lòng lẫn bề mặt chất lỏng.",
                "Bay hơi xảy ra ở mọi nhiệt độ, còn sôi chỉ xảy ra đúng ở 100 °C với mọi chất lỏng.",
                "Bay hơi là quá trình ngược lại của sôi.",
                "Hai hiện tượng này giống hệt nhau.",
            ],
            "answer": 0,
            "explanation": "Bay hơi chỉ xảy ra ở mặt thoáng và ở mọi nhiệt độ; sôi xảy ra ở cả trong lòng lẫn mặt thoáng, tại một nhiệt độ sôi xác định phụ thuộc áp suất. 100 °C chỉ đúng cho nước ở áp suất tiêu chuẩn.",
        },
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 12", "lesson_title": "Bài 1. Sự chuyển thể"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Từ li nước đá để quên trên bàn",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}

with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("ok", len(bundle["theory_html"]), "bytes theory")
