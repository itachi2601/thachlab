#!/usr/bin/env python3
"""Sinh bundle.json cho bài "Bài 6. Định luật Boyle. Định luật Charles" (lesson_id 7).
Chạy từ gốc repo: python3 content/lesson-samples/l12-boyle-charles/build_bundle.py
theory_html lấy nguyên văn từ theory.html; exam lấy 5 câu trắc nghiệm trong bài.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent

QUESTIONS = [
    {
        "type": "multiple_choice",
        "question": "Trạng thái của một lượng khí xác định được xác định bằng ba thông số trạng thái nào?",
        "options": [
            "Áp suất, thể tích, nhiệt độ.",
            "Khối lượng, thể tích, nhiệt độ.",
            "Áp suất, khối lượng, nhiệt độ.",
            "Áp suất, thể tích, khối lượng.",
        ],
        "answer": 0,
        "explanation": "Ba thông số trạng thái là áp suất p, thể tích V và nhiệt độ T. Nếu trong một quá trình biến đổi trạng thái có đúng một thông số không đổi thì đó là đẳng quá trình (đẳng nhiệt, đẳng áp hoặc đẳng tích).",
    },
    {
        "type": "multiple_choice",
        "question": "Ống thuỷ tinh hở phía trên, bên trong có cột thuỷ ngân cao 50 mm; áp suất khí quyển là 760 mmHg. Áp suất của khí bị nhốt ở đáy ống là",
        "options": ["710 mmHg.", "810 mmHg.", "760 mmHg.", "50 mmHg."],
        "answer": 1,
        "explanation": "Ống hở phía trên nên khí quyển và cột thuỷ ngân cùng đè xuống khí bị nhốt: p = p0 + h = 760 + 50 = 810 mmHg. Chỉ khi ống hở phía dưới mới lấy p = p0 − h.",
    },
    {
        "type": "multiple_choice",
        "question": "Một lượng khí ở áp suất 1,0 atm và thể tích 3,0 lít. Nén đẳng nhiệt cho thể tích còn 1,5 lít thì áp suất của khí là",
        "options": ["0,5 atm.", "1,5 atm.", "2,0 atm.", "3,0 atm."],
        "answer": 2,
        "explanation": "Định luật Boyle: p1V1 = p2V2, suy ra p2 = (1,0 × 3,0)/1,5 = 2,0 atm. Thể tích giảm 2 lần thì áp suất tăng 2 lần.",
    },
    {
        "type": "multiple_choice",
        "question": "Trong hệ toạ độ (p, V), đường đẳng nhiệt của một lượng khí xác định có dạng",
        "options": [
            "một đường thẳng đi qua gốc toạ độ.",
            "một nhánh hypebol.",
            "một đường thẳng song song với trục thể tích.",
            "một cung tròn.",
        ],
        "answer": 1,
        "explanation": "pV = hằng số nên p tỉ lệ nghịch với V: đường biểu diễn là một nhánh hypebol. Đường thẳng đi qua gốc toạ độ trên đồ thị (V, T) mới là đường đẳng áp.",
    },
    {
        "type": "multiple_choice",
        "question": "Một lượng khí ở 27 °C có thể tích 1,0 lít, áp suất giữ không đổi. Nung nóng khí tới 87 °C thì thể tích của nó là",
        "options": ["3,2 lít.", "1,2 lít.", "1,0 lít.", "0,8 lít."],
        "answer": 1,
        "explanation": "Định luật Charles: V2 = V1·T2/T1 với nhiệt độ tuyệt đối T1 = 27 + 273 = 300 K và T2 = 87 + 273 = 360 K, nên V2 = 1,0 × 360/300 = 1,2 lít. Lấy tỉ số 87/27 ≈ 3,2 là lỗi dùng nhầm thang Celsius.",
    },
]

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {
        "class_name": "Vật lí 12",
        "chapter_title": "Chương 2: Khí lí tưởng",
        "lesson_title": "Bài 6. Định luật Boyle. Định luật Charles",
    },
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Đẳng nhiệt – Đẳng áp: hai định luật, hai đường đồ thị",
    "theory_html": (HERE / "theory.html").read_text(encoding="utf8"),
    "worked_examples": [],
    "exam": {
        "title": "Luyện tập — Định luật Boyle và định luật Charles",
        "topic": "Khí lí tưởng",
        "difficulty": "de",
        "duration_minutes": 10,
        "questions": QUESTIONS,
    },
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
print("ok", out, len(bundle["theory_html"]), "bytes theory_html ·", len(QUESTIONS), "câu")
