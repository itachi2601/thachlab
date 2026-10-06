"""Đóng gói theory.html + 5 câu tự kiểm tra thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_bundle.py
"""
import json

EXAM = {
    "title": "Luyện tập — Phương trình trạng thái của khí lí tưởng",
    "duration_minutes": 12,
    "questions": [
        {
            "type": "multiple_choice",
            "question": "Một lượng khí xác định chuyển từ trạng thái 1 sang trạng thái 2. Hệ thức nào luôn đúng?",
            "options": [
                "p₁V₁ = p₂V₂, vì p và V luôn tỉ lệ nghịch.",
                "p₁V₁/T₁ = p₂V₂/T₂.",
                "p₁/T₁ = p₂/T₂, vì p luôn tỉ lệ thuận với T.",
                "p₁T₁ = p₂T₂, vì p và T luôn tỉ lệ nghịch.",
            ],
            "answer": 1,
            "explanation": "Khi cả ba thông số cùng đổi thì chỉ phương trình trạng thái là chắc chắn đúng: p₁V₁/T₁ = p₂V₂/T₂ = hằng số. p₁V₁ = p₂V₂ chỉ đúng khi nhiệt độ không đổi (định luật Boyle); p₁/T₁ = p₂/T₂ chỉ đúng khi thể tích không đổi (quá trình đẳng tích). Hệ thức p₁T₁ = p₂T₂ không có cơ sở nào.",
        },
        {
            "type": "multiple_choice",
            "question": "Bình kín chứa khí ở 27 °C, áp suất 2,0.10⁵ Pa. Nung bình lên 87 °C. Áp suất khí lúc đó là",
            "options": [
                "6,4.10⁵ Pa.",
                "2,0.10⁵ Pa, không đổi.",
                "2,4.10⁵ Pa.",
                "1,7.10⁵ Pa.",
            ],
            "answer": 2,
            "explanation": "Bình kín nên đây là quá trình đẳng tích: p₂ = p₁·T₂/T₁ = 2,0.10⁵ × 360/300 = 2,4.10⁵ Pa (đổi 27 °C = 300 K, 87 °C = 360 K). Phương án 6,4.10⁵ Pa là lỗi lấy tỉ số nhiệt độ Celsius 87/27; 1,7.10⁵ Pa là lật ngược tỉ số; 2,0.10⁵ Pa là quên rằng nhiệt độ tăng thì áp suất phải tăng.",
        },
        {
            "type": "multiple_choice",
            "question": "Trong một quá trình biến đổi trạng thái mà thể tích của lượng khí không đổi, hệ thức nào đúng?",
            "options": [
                "p₁/T₁ = p₂/T₂.",
                "V₁/T₁ = V₂/T₂.",
                "p₁V₁ = p₂V₂.",
                "p₁T₁ = p₂T₂.",
            ],
            "answer": 0,
            "explanation": "V không đổi nên V triệt tiêu ở hai vế của phương trình trạng thái, chỉ còn p₁/T₁ = p₂/T₂ — đúng là quá trình đẳng tích (định luật Gay-Lussac). V₁/T₁ = V₂/T₂ ứng với p không đổi (Charles), còn p₁V₁ = p₂V₂ ứng với T không đổi (Boyle).",
        },
        {
            "type": "multiple_choice",
            "question": "Khí trong bình kín ở 27 °C có áp suất 3,0.10⁵ Pa. Hạ nhiệt độ xuống 0 °C thì áp suất là",
            "options": [
                "3,0.10⁵ Pa, không đổi vì bình vẫn kín.",
                "0 Pa, vì 0 °C ứng với 0 K.",
                "3,3.10⁵ Pa.",
                "2,73.10⁵ Pa.",
            ],
            "answer": 3,
            "explanation": "Quá trình đẳng tích: p₂ = p₁·T₂/T₁ = 3,0.10⁵ × 273/300 ≈ 2,73.10⁵ Pa. Hai điều phải nhớ: 0 °C = 273 K chứ không phải 0 K, và bình kín thì áp suất vẫn đổi khi nhiệt độ đổi. Phương án 3,3.10⁵ Pa là lật ngược tỉ số (300/273).",
        },
        {
            "type": "multiple_choice",
            "question": "Bình khí nén mini 4 lít để ngoài nắng: buổi sáng 27 °C, áp suất 5,0.10⁵ Pa; giữa trưa 47 °C, thể tích bình không đổi. Áp suất giữa trưa là",
            "options": [
                "8,7.10⁵ Pa.",
                "5,3.10⁵ Pa.",
                "4,7.10⁵ Pa.",
                "5,0.10⁵ Pa, không đổi.",
            ],
            "answer": 1,
            "explanation": "Đẳng tích: p₂ = p₁·T₂/T₁ = 5,0.10⁵ × 320/300 ≈ 5,3.10⁵ Pa (300 K và 320 K). Phương án 8,7.10⁵ Pa lấy tỉ số Celsius 47/27; 4,7.10⁵ Pa lật ngược tỉ số 300/320; 5,0.10⁵ Pa là quên rằng nhiệt độ tăng thì áp suất tăng.",
        },
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 12", "lesson_title": "Bài 7. Phương trình trạng thái của khí lí tưởng"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Ba thông số, một phương trình, ba định luật",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}

with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("ok", len(bundle["theory_html"]), "bytes theory")
