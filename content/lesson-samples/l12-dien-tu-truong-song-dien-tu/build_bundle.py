"""Đóng gói theory.html + 5 câu tự kiểm tra thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_bundle.py
"""
import json

EXAM = {
    "title": "Luyện tập — Điện từ trường. Mô hình sóng điện từ",
    "duration_minutes": 10,
    "questions": [
        {
            "type": "multiple_choice",
            "question": "Đường sức của điện trường xoáy có đặc điểm gì?",
            "options": [
                "Là đường thẳng, đi từ điện tích dương sang điện tích âm.",
                "Là đường cong kín, bao quanh các đường cảm ứng từ.",
                "Là đường cong hở, nối hai điểm ở vô cùng.",
                "Là đường thẳng song song với các đường cảm ứng từ.",
            ],
            "answer": 1,
            "explanation": "Từ trường biến thiên theo thời gian sinh ra điện trường xoáy; đường sức của nó khép kín, bao quanh các đường cảm ứng từ và không có điểm đầu, điểm cuối. Đường sức không khép kín, đi từ điện tích dương sang điện tích âm là của điện trường tĩnh.",
        },
        {
            "type": "multiple_choice",
            "question": "Tụ điện mắc nối tiếp với bóng đèn trong mạch xoay chiều, đèn vẫn sáng. Vì sao?",
            "options": [
                "Vì các điện tích chạy xuyên qua lớp cách điện giữa hai bản tụ.",
                "Vì tụ điện biến dòng xoay chiều thành dòng một chiều chạy trong mạch.",
                "Vì điện trường biến thiên giữa hai bản tụ tương đương một dòng điện dịch.",
                "Vì tụ điện chỉ phóng điện một lần rồi ngắt mạch.",
            ],
            "answer": 2,
            "explanation": "Chất điện môi giữa hai bản tụ cách điện nên không có điện tích chạy qua. Khi tụ tích hoặc phóng điện, điện trường giữa hai bản biến thiên và tương đương một dòng điện gọi là dòng điện dịch; dòng điện dịch này gây ra từ trường có đường sức khép kín, nhờ đó mạch vẫn có dòng và đèn sáng liên tục.",
        },
        {
            "type": "multiple_choice",
            "question": "Tại một điểm có sóng điện từ truyền qua, nhận xét nào đúng?",
            "options": [
                "Hai vectơ E và B song song với nhau và cùng nằm trên phương truyền.",
                "Hai vectơ E và B lệch pha nhau π/2.",
                "Sóng điện từ không truyền được trong chân không.",
                "Hai vectơ E và B vuông góc với nhau, cùng vuông góc với phương truyền và cùng pha.",
            ],
            "answer": 3,
            "explanation": "Sóng điện từ là sóng ngang: vectơ cường độ điện trường E vuông góc với vectơ cảm ứng từ B, cả hai vuông góc với phương truyền sóng; E và B biến thiên điều hoà cùng pha (cùng đạt cực đại, cùng triệt tiêu). Sóng điện từ truyền được trong chân không với c = 3.10⁸ m/s.",
        },
        {
            "type": "multiple_choice",
            "question": "Khi điện trường E của một sóng điện từ triệt tiêu thì từ trường B thế nào?",
            "options": [
                "B cũng triệt tiêu, vì E và B cùng pha.",
                "B đạt cực đại, vì E và B lệch pha π/2.",
                "B đạt cực đại, vì năng lượng điện bằng 0 thì năng lượng từ cực đại.",
                "B luôn khác 0, vì từ trường của sóng không bao giờ triệt tiêu.",
            ],
            "answer": 0,
            "explanation": "Trong sóng điện từ, E và B luôn cùng pha nên cùng đạt cực đại và cùng triệt tiêu tại một thời điểm. Cách lí luận 'năng lượng điện chuyển hết thành năng lượng từ' chỉ đúng với mạch dao động kín, không dùng cho sóng điện từ đang lan truyền.",
        },
        {
            "type": "multiple_choice",
            "question": "Một đoạn cáp dẫn tín hiệu tần số 100 MHz với tốc độ truyền 2.10⁸ m/s. Bước sóng trong cáp là",
            "options": ["0,5 m.", "1,5 m.", "2 m.", "3 m."],
            "answer": 2,
            "explanation": "λ = v/f = 2.10⁸ / 10⁸ = 2 m. Phương án 3 m là lỗi quên đổi tốc độ — vẫn lấy c = 3.10⁸ m/s của chân không. Tần số không đổi khi sóng vào môi trường khác, chỉ tốc độ và bước sóng thay đổi.",
        },
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 12", "lesson_title": "Bài 16. Điện từ trường. Mô hình sóng điện từ"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Điện từ trường · sóng điện từ · thang sóng điện từ",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}

with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("ok", len(bundle["theory_html"]), "bytes theory ·", len(EXAM["questions"]), "câu luyện tập")
