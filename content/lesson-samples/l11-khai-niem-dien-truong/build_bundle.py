"""Đóng gói theory.html + 5 câu tự kiểm tra thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_bundle.py
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent

EXAM = {
    "title": "Luyện tập — Khái niệm điện trường",
    "duration_minutes": 10,
    "questions": [
        {
            "type": "multiple_choice",
            "question": "Tại điểm M, điện trường hướng về phía đông. Đặt một electron tại M thì lực điện tác dụng lên electron hướng",
            "options": [
                "về phía đông, cùng hướng điện trường.",
                "về phía tây, ngược hướng điện trường.",
                "về phía bắc, vuông góc với điện trường.",
                "không có hướng, vì lực bằng 0.",
            ],
            "answer": 1,
            "explanation": "$\\vec F=q\\vec E$. Electron có $q\\lt 0$ nên lực ngược chiều $\\vec E$, tức hướng về phía tây. Lực luôn cùng phương với $\\vec E$ nên không thể vuông góc.",
        },
        {
            "type": "multiple_choice",
            "question": "Điện tích điểm $Q$ gây ra tại M cách nó 10 cm điện trường $3{,}6\\cdot10^4$ V/m. Tại N cách $Q$ 30 cm, cường độ điện trường là",
            "options": ["$1{,}2\\cdot10^4$ V/m", "$3{,}6\\cdot10^4$ V/m", "$4\\cdot10^3$ V/m", "$1{,}08\\cdot10^5$ V/m"],
            "answer": 2,
            "explanation": "$E$ tỉ lệ nghịch với $r^2$. $r$ gấp 3 nên $E$ giảm 9 lần: $3{,}6\\cdot10^4/9=4\\cdot10^3$ V/m. Chỉ chia cho 3 là quên bình phương.",
        },
        {
            "type": "multiple_choice",
            "question": "Phát biểu nào về đường sức điện của điện trường tĩnh là SAI?",
            "options": [
                "Đường sức điện là đường cong khép kín.",
                "Các đường sức điện không cắt nhau.",
                "Chỗ đường sức mau thì điện trường mạnh.",
                "Đường sức đi ra từ điện tích dương, kết thúc ở điện tích âm.",
            ],
            "answer": 0,
            "explanation": "Đường sức của điện trường tĩnh không khép kín: bắt đầu ở điện tích dương (hoặc vô cực) và kết thúc ở điện tích âm (hoặc vô cực). Ba phát biểu còn lại đều đúng.",
        },
        {
            "type": "multiple_choice",
            "question": "Tại M, điện tích thử $q$ chịu lực điện $F$. Thay bằng điện tích thử $3q$ đặt đúng chỗ đó thì",
            "options": [
                "lực không đổi, cường độ điện trường tại M giảm 3 lần.",
                "lực tăng 3 lần, cường độ điện trường tại M tăng 3 lần.",
                "lực tăng 9 lần, cường độ điện trường tại M không đổi.",
                "lực tăng 3 lần, cường độ điện trường tại M không đổi.",
            ],
            "answer": 3,
            "explanation": "Cường độ điện trường tại M do điện tích nguồn và vị trí quyết định, không phụ thuộc điện tích thử. $F=|q|E$ nên lực tăng 3 lần. $E=F/q$ chỉ là cách đo $E$.",
        },
        {
            "type": "multiple_choice",
            "question": "Trong không khí, $q_1=+12$ nC tại A, $q_2=-16$ nC tại B, $AB=6$ cm. Cường độ điện trường tổng hợp tại trung điểm M của AB là",
            "options": ["$4\\cdot10^4$ V/m", "$2{,}8\\cdot10^5$ V/m", "$2\\cdot10^5$ V/m", "$0$"],
            "answer": 1,
            "explanation": "$r=3$ cm: $E_1=9\\cdot10^9\\cdot\\dfrac{12\\cdot10^{-9}}{0{,}03^2}=1{,}2\\cdot10^5$ V/m, $E_2=1{,}6\\cdot10^5$ V/m. $\\vec E_1$ hướng ra xa A (về B), $\\vec E_2$ hướng về B: cùng chiều nên $E=2{,}8\\cdot10^5$ V/m.",
        },
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 11", "lesson_title": "Bài 17. Khái niệm điện trường"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Điện trường, cường độ điện trường và nguyên lí chồng chất điện trường",
    "theory_html": (HERE / "theory.html").read_text(encoding="utf8"),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}

(HERE / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf8")
print("ok", len(bundle["theory_html"]), "bytes theory")
