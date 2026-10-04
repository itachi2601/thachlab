"""Đóng gói theory.html + 5 câu tự kiểm tra thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_bundle.py
"""
import json

EXAM = {
    "title": "Luyện tập — Phản ứng phân hạch, phản ứng nhiệt hạch và ứng dụng",
    "duration_minutes": 10,
    "questions": [
        {
            "type": "multiple_choice",
            "question": "Trong phản ứng phân hạch 235/92 U + 1/0 n → 144/56 Ba + 89/36 Kr + x·1/0 n, giá trị của x là",
            "options": ["x = 1.", "x = 2.", "x = 3.", "x = 4."],
            "answer": 2,
            "explanation": "Bảo toàn số nuclôn: 235 + 1 = 144 + 89 + x, suy ra x = 3. Kiểm tra điện tích: 92 + 0 = 56 + 36 + 0, khớp.",
        },
        {
            "type": "multiple_choice",
            "question": "Phân hạch U-235 toả năng lượng vì",
            "options": [
                "neutron bị hấp thụ và toàn bộ khối lượng của nó biến thành nhiệt.",
                "tổng khối lượng nghỉ của các mảnh vỡ nhỏ hơn khối lượng nghỉ ban đầu.",
                "hai hạt nhân urani kết hợp thành một hạt nhân nặng hơn.",
                "electron trong nguyên tử urani chuyển mức và phát ra ánh sáng.",
            ],
            "answer": 1,
            "explanation": "Năng lượng lấy từ phần khối lượng nghỉ hụt đi của cả phản ứng: W = (m_trước − m_sau)c². Hai mảnh vỡ bền hơn hạt nhân urani nên năng lượng liên kết riêng tăng và tổng khối lượng nghỉ giảm. Chuyển mức electron chỉ cho năng lượng cỡ vài êlectron vôn.",
        },
        {
            "type": "multiple_choice",
            "question": "Một lò phản ứng đang có hệ số nhân neutron k = 1,002. Phản ứng dây chuyền trong lò sẽ",
            "options": [
                "tắt dần, vì k còn nhỏ hơn 2.",
                "số neutron tăng dần theo từng thế hệ, vì k > 1.",
                "đứng yên không đổi, vì k xấp xỉ 1.",
                "dừng ngay, vì k khác đúng 1.",
            ],
            "answer": 1,
            "explanation": "k = 1,002 > 1 nên mỗi thế hệ có nhiều neutron hơn thế hệ trước một chút — số neutron tăng dần. Mốc so sánh của k là 1, không phải 2; muốn công suất không đổi phải giữ đúng k = 1 bằng thanh điều khiển.",
        },
        {
            "type": "multiple_choice",
            "question": "Điều kiện để phản ứng nhiệt hạch xảy ra là",
            "options": [
                "nhiệt độ cỡ 10⁸–10⁹ K, mật độ hạt nhân đủ lớn và duy trì đủ lâu.",
                "có neutron chậm bắn vào hạt nhân nhẹ.",
                "nhiệt độ phòng và áp suất thấp để hạt nhân dễ tiến lại gần nhau.",
                "chỉ cần đặt hai hạt nhân nhẹ sát nhau là đủ.",
            ],
            "answer": 0,
            "explanation": "Ba điều kiện phải đủ cùng lúc: nhiệt độ rất cao để thắng lực đẩy Cu-lông, mật độ lớn để va chạm đủ nhiều, thời gian giam đủ dài để năng lượng thu về lớn hơn năng lượng bỏ ra. Neutron chậm là cách mồi phân hạch, không phải nhiệt hạch.",
        },
        {
            "type": "multiple_choice",
            "question": "U-235 phân hạch toả trung bình 200 MeV. Số phân hạch cần thiết để toả ra năng lượng 1 J là",
            "options": ["3,1·10¹⁰.", "3,1·10¹³.", "1,25·10¹⁰.", "5,0·10¹²."],
            "answer": 0,
            "explanation": "1 MeV = 1,6·10⁻¹³ J nên 200 MeV = 3,2·10⁻¹¹ J. Số phân hạch cần: 1 ÷ 3,2·10⁻¹¹ ≈ 3,1·10¹⁰ hạt.",
        },
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {
        "class_name": "Vật lí 12",
        "lesson_title": "Bài 16. Phản ứng phân hạch, phản ứng nhiệt hạch và ứng dụng",
    },
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Phân hạch, dây chuyền, lò phản ứng và nhiệt hạch",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}

with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("ok", len(bundle["theory_html"]), "bytes theory")
