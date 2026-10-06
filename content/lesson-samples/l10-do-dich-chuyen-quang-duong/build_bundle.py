#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Độ dịch chuyển và quãng đường đi được",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Trên trục X (chiều dương sang phải), xe điều khiển từ xa đi từ x₁ = 70 cm tới 90 cm rồi lùi về x₂ = 40 cm. Độ dịch chuyển của xe là:",
         "options": ["30 cm", "70 cm", "−50 cm", "−30 cm"],
         "answer": 3,
         "explanation": "d = x₂ − x₁ = 40 − 70 = −30 cm (điểm cuối nằm về phía âm). 70 cm là quãng đường (20 + 50); 30 cm là quên dấu; −50 cm chỉ tính đoạn lùi cuối."},
        {"type": MC,
         "question": "Trường hợp nào độ lớn độ dịch chuyển bằng quãng đường đi được?",
         "options": ["Thang máy đi thẳng từ tầng 1 lên tầng 8, không dừng và không quay xuống",
                     "Vận động viên chạy đúng một vòng sân vận động 400 m",
                     "Xe đi thẳng từ A đến B rồi quay về A trên cùng con đường",
                     "Ô tô chạy theo đường đèo uốn lượn từ chân lên đỉnh dốc"],
         "answer": 0,
         "explanation": "Độ lớn d = s chỉ khi vật chuyển động thẳng và không đổi chiều. Chạy vòng kín hoặc đi rồi quay về cho d = 0; đường đèo cong cho d < s."},
        {"type": MC,
         "question": "Chọn trục Ox hướng từ Tây sang Đông. Một xe đi thẳng 5 km về phía Tây, không đổi chiều. Nhận xét đúng là:",
         "options": ["d = 5 km; s = −5 km", "d = −5 km; s = 5 km", "d = −5 km; s = −5 km", "d = 5 km; s = 5 km"],
         "answer": 1,
         "explanation": "Xe đi ngược chiều dương nên d = −5 km; quãng đường không bao giờ âm nên s = 5 km."},
        {"type": MC,
         "question": "Robot hút bụi đi thẳng 6 m về phía Bắc, rồi rẽ đi thẳng 8 m về phía Đông. Độ lớn độ dịch chuyển của robot là:",
         "options": ["14 m", "2 m", "10 m", "48 m"],
         "answer": 2,
         "explanation": "Hai đoạn vuông góc: d = √(6² + 8²) = 10 m. 14 m là quãng đường; 2 m chỉ đúng nếu hai đoạn ngược chiều."},
        {"type": MC,
         "question": "Một bạn đi xe đạp 1,2 km về phía Đông rồi quay lại 0,5 km về phía Tây trên cùng con đường, hết 6 phút. Độ lớn độ dịch chuyển và tốc độ trung bình là:",
         "options": ["1,3 km và 17 km/h", "1,7 km và 17 km/h", "0,7 km và 7 km/h", "0,7 km và 17 km/h"],
         "answer": 3,
         "explanation": "Cùng phương, ngược chiều: d = 1,2 − 0,5 = 0,7 km. Quãng đường s = 1,7 km, t = 0,1 h nên tốc độ trung bình = s/t = 17 km/h (dùng quãng đường, không dùng d)."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 4. Độ dịch chuyển và quãng đường đi được"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Chất điểm, hệ quy chiếu; độ dịch chuyển và quãng đường đi được; tốc độ trung bình",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
