"""Đóng gói theory.html + 5 câu tự kiểm tra thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này:  python3 build_bundle.py"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent

EXAM = {
    "title": "Luyện tập — Đại cương về dòng điện xoay chiều",
    "duration_minutes": 10,
    "questions": [
        {"type": "multiple_choice",
         "question": "Ổ điện trong nhà ghi 220 V – 50 Hz. Điện áp cực đại giữa hai lỗ ổ điện xấp xỉ",
         "options": ["220 V.", "311 V.", "156 V.", "440 V."], "answer": 1,
         "explanation": "220 V là điện áp hiệu dụng. Điện áp cực đại U0 = U√2 = 220√2 ≈ 311 V."},
        {"type": "multiple_choice",
         "question": "Dòng điện i = 4cos(100πt − π/3) A. Phát biểu nào sau đây đúng?",
         "options": ["Tần số f = 100 Hz.", "Chu kì T = 0,2 s.", "Trong 1 s dòng điện đổi chiều 100 lần.", "Pha ban đầu là +π/3."], "answer": 2,
         "explanation": "ω = 100π nên f = ω/2π = 50 Hz, T = 0,02 s, số lần đổi chiều mỗi giây là 2f = 100. Pha ban đầu là −π/3."},
        {"type": "multiple_choice",
         "question": "Dòng xoay chiều có cường độ hiệu dụng 2 A và dòng không đổi 2 A cùng chạy qua một điện trở trong cùng thời gian. Nhiệt lượng toả ra",
         "options": ["bằng nhau.", "dòng xoay chiều toả nhiều hơn vì đỉnh là 2√2 A.", "dòng xoay chiều toả ít hơn vì giá trị trung bình bằng 0.", "không so sánh được."], "answer": 0,
         "explanation": "Cường độ hiệu dụng được định nghĩa theo tác dụng nhiệt: hai dòng này toả nhiệt bằng nhau."},
        {"type": "multiple_choice",
         "question": "Dòng i = 2cos(100πt) A chạy qua điện trở R = 10 Ω. Công suất toả nhiệt của R là",
         "options": ["0 W.", "40 W.", "20 W.", "28 W."], "answer": 2,
         "explanation": "I = I0/√2 = √2 A nên P = I²R = 2·10 = 20 W. Ra 40 W là dùng nhầm I0; ra 0 là dùng giá trị trung bình."},
        {"type": "multiple_choice",
         "question": "Khung dây đang quay đều trong từ trường đều. Tại lúc mặt khung vuông góc với vectơ cảm ứng từ, suất điện động trong khung",
         "options": ["cực đại vì từ thông cực đại.", "bằng không.", "bằng một nửa giá trị cực đại.", "bằng giá trị hiệu dụng."], "answer": 1,
         "explanation": "Từ thông và suất điện động vuông pha: từ thông cực đại thì e = −Φ' = 0."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 12", "lesson_title": "Bài 13. Đại cương về dòng điện xoay chiều"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Từ con số 220 V trên ổ điện",
    "theory_html": (HERE / "theory.html").read_text(encoding="utf-8"),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}
(HERE / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", len(bundle["theory_html"]))
