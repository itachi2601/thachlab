"""Đóng gói theory.html + 5 câu tự kiểm tra thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_bundle.py
"""
import json

EXAM = {
    "title": "Luyện tập — Áp suất và động năng của phân tử khí",
    "duration_minutes": 10,
    "questions": [
        {
            "type": "multiple_choice",
            "question": "Một phân tử khí khối lượng m bay vuông góc vào thành bình với tốc độ v, va chạm hoàn toàn đàn hồi rồi bật ngược trở lại với cùng tốc độ. Độ lớn độ biến thiên động lượng của phân tử là",
            "options": ["0, vì tốc độ của phân tử không đổi.", "mv.", "2mv.", "mv/2."],
            "answer": 2,
            "explanation": "Động lượng là vectơ: nó đổi chiều từ +mv thành −mv khi bật ngược, nên độ lớn biến thiên là |−mv − (+mv)| = 2mv. Tốc độ không đổi nhưng hướng vận tốc đổi chiều, vì vậy không thể kết luận là 0.",
        },
        {
            "type": "multiple_choice",
            "question": "Ở 27 °C, động năng tịnh tiến trung bình của một phân tử khí xấp xỉ",
            "options": [
                "6,2·10⁻²¹ J.",
                "4,1·10⁻²¹ J.",
                "5,6·10⁻²² J.",
                "Không xác định được, vì còn cần biết khối lượng phân tử.",
            ],
            "answer": 0,
            "explanation": "Đổi sang Kelvin: T = 27 + 273 = 300 K. Động năng tịnh tiến trung bình chỉ phụ thuộc nhiệt độ: E_d = (3/2)kT = 1,5 × 1,38·10⁻²³ × 300 ≈ 6,2·10⁻²¹ J. Phương án 4,1·10⁻²¹ J là quên hệ số 3/2; 5,6·10⁻²² J là dùng số 27 như thể đó là nhiệt độ Kelvin.",
        },
        {
            "type": "multiple_choice",
            "question": "Hai bình kín cùng thể tích, mỗi bình chứa cùng số phân tử và cùng ở 27 °C; bình 1 là H₂, bình 2 là O₂. So sánh áp suất khí trong hai bình:",
            "options": [
                "Bình O₂ lớn hơn vì phân tử O₂ nặng hơn.",
                "Bình H₂ lớn hơn vì phân tử H₂ chuyển động nhanh hơn.",
                "Hai bình bằng nhau, vì cùng N, cùng V, cùng T nên tích m·v² của hai khí bằng nhau.",
                "Không so sánh được vì hai khí có khối lượng phân tử khác nhau.",
            ],
            "answer": 2,
            "explanation": "Ở cùng nhiệt độ, mọi chất khí có cùng động năng tịnh tiến trung bình E_d = (1/2)m·v², nghĩa là tích m·v² bằng nhau. Với cùng N và cùng V thì p = (1/3)μ·m·v² bằng nhau: phân tử H₂ nhẹ nên bay nhanh hơn, vừa đủ bù cho khối lượng nhỏ hơn.",
        },
        {
            "type": "multiple_choice",
            "question": "Bình kín dung tích 3,0 lít chứa 0,20 mol khí nitơ. Mật độ phân tử trong bình là",
            "options": ["4,0·10²⁵ m⁻³", "4,0·10²² m⁻³", "6,0·10²³ m⁻³", "0,067 m⁻³"],
            "answer": 0,
            "explanation": "μ = N/V = nN_A/V = (0,20 × 6,02·10²³)/(3,0·10⁻³) ≈ 4,0·10²⁵ m⁻³. Phương án 4,0·10²² m⁻³ là quên đổi 3,0 lít = 3,0·10⁻³ m³; 0,067 m⁻³ là lấy số mol chia thể tích thay vì số phân tử chia thể tích.",
        },
        {
            "type": "multiple_choice",
            "question": "Cũng bình khí đó, nung từ 27 °C lên 327 °C (thể tích không đổi). Động năng tịnh tiến trung bình của phân tử",
            "options": [
                "Tăng 2 lần, vì nhiệt độ tuyệt đối tăng từ 300 K lên 600 K.",
                "Tăng 12,1 lần, vì 327 : 27 = 12,1.",
                "Không đổi, vì thể tích bình không đổi.",
                "Tăng 4 lần, vì động năng tỉ lệ với bình phương nhiệt độ.",
            ],
            "answer": 0,
            "explanation": "Phải đổi sang Kelvin: T₁ = 300 K, T₂ = 600 K, tỉ số T₂/T₁ = 2. Vì E_d = (3/2)kT tỉ lệ thuận với nhiệt độ tuyệt đối nên động năng tăng đúng 2 lần. Lấy tỉ số hai giá trị Celsius (327 : 27) hoặc nhớ nhầm thành T² đều cho kết quả sai.",
        },
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 12", "lesson_title": "Bài 8. Áp suất - động năng của phân tử khí"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Áp suất do va chạm, động năng theo nhiệt độ",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}

with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("ok", len(bundle["theory_html"]), "bytes theory")
