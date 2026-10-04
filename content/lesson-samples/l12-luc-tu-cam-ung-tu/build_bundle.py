"""Đóng gói theory.html + 5 câu lấy từ quiz trong bài thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_bundle.py
"""
import json

EXAM = {
    "title": "Luyện tập — Lực từ. Cảm ứng từ",
    "duration_minutes": 10,
    "questions": [
        {
            "type": "multiple_choice",
            "question": "Một đoạn dây dẫn mang dòng điện đặt vuông góc với đường sức từ. Lực từ tác dụng lên đoạn dây có phương",
            "options": [
                "trùng với phương của đoạn dây.",
                "trùng với phương của đường sức từ.",
                "vuông góc với cả đoạn dây và đường sức từ.",
                "hợp với đoạn dây một góc 45°.",
            ],
            "answer": 2,
            "explanation": "Lực từ có phương vuông góc với đoạn dây dẫn mang dòng điện và vuông góc với đường sức từ, tức vuông góc với mặt phẳng chứa vectơ cảm ứng từ và đoạn dây. Nếu lực nằm dọc theo dây thì nó chỉ kéo căng dây, không thể làm dây lệch khỏi vị trí cân bằng như thí nghiệm cho thấy.",
        },
        {
            "type": "multiple_choice",
            "question": "Đoạn dây dài 10 cm mang dòng điện 2 A đặt vuông góc với đường sức từ, tại chỗ có cảm ứng từ B = 0,05 T. Lực từ tác dụng lên đoạn dây bằng",
            "options": ["0,01 N.", "0,1 N.", "0,005 N.", "0,02 N."],
            "answer": 0,
            "explanation": "Dây vuông góc đường sức nên F = BIl = 0,05 × 2 × 0,10 = 0,01 N. Phải đổi 10 cm = 0,10 m trước khi thay số; các phương án sai ứng với việc quên đổi đơn vị (l = 1 m, 5 cm hoặc 20 cm).",
        },
        {
            "type": "multiple_choice",
            "question": "Phát biểu nào sau đây đúng về vectơ cảm ứng từ tại một điểm trong từ trường?",
            "options": [
                "Có phương trùng với phương của dòng điện đặt tại điểm đó.",
                "Có chiều từ cực Bắc sang cực Nam của nam châm thử nằm cân bằng tại điểm đó.",
                "Có chiều từ cực Nam sang cực Bắc của nam châm thử nằm cân bằng tại điểm đó.",
                "Có độ lớn tăng theo cường độ dòng điện của đoạn dây thử đặt tại điểm đó.",
            ],
            "answer": 2,
            "explanation": "Cảm ứng từ là đại lượng vectơ đặc trưng cho từ trường về mặt tác dụng lực: phương là phương của nam châm thử nằm cân bằng, chiều từ cực Nam sang cực Bắc của nam châm thử, độ lớn B = F/(Il·sinα). Độ lớn này là đặc tính có sẵn của từ trường tại điểm đó nên không phụ thuộc vào dòng điện thử.",
        },
        {
            "type": "multiple_choice",
            "question": "Một ống dây dài có 1000 vòng dây trên mỗi mét, mang dòng điện 1 A. Cảm ứng từ trong lòng ống dây bằng",
            "options": ["1,26·10⁻³ T.", "12,6·10⁻³ T.", "0,126·10⁻³ T.", "1,26·10⁻⁵ T."],
            "answer": 0,
            "explanation": "B = 4π·10⁻⁷·n·I = 4π·10⁻⁷ × 1000 × 1 ≈ 1,26·10⁻³ T = 1,26 mT. Trong lòng ống dây dài, cảm ứng từ chỉ phụ thuộc số vòng trên một mét và cường độ dòng điện, không phụ thuộc bán kính ống.",
        },
        {
            "type": "multiple_choice",
            "question": "Đặt một đoạn dây dài 5 cm mang dòng 2 A vuông góc với đường sức từ, lực từ đo được 0,01 N. Nếu tăng cường độ dòng điện lên 4 A (giữ nguyên dây và vị trí) thì cảm ứng từ tại điểm đó",
            "options": [
                "tăng gấp đôi, thành 0,2 T.",
                "không đổi, vẫn bằng 0,1 T.",
                "giảm một nửa, còn 0,05 T.",
                "không xác định được vì thiếu chiều dài đoạn dây.",
            ],
            "answer": 1,
            "explanation": "Từ dữ kiện đầu: B = F/(Il) = 0,01/(2 × 0,05) = 0,1 T. Khi tăng dòng thử lên 4 A thì lực từ tăng thành 0,02 N nhưng cảm ứng từ tại điểm đó vẫn là 0,1 T — đó là tính chất của từ trường, không phải của đoạn dây thử.",
        },
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 12", "lesson_title": "Bài 10. Lực từ. Cảm ứng từ"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Lực từ, cảm ứng từ và quy tắc bàn tay trái",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}

with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("ok", len(bundle["theory_html"]), "bytes theory")
