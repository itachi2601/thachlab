#!/usr/bin/env python3
"""Đóng gói bundle.json từ theory.html. Chạy: python3 build_bundle.py"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Động năng và thế năng",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Thế năng của con lắc lò xo (mốc tại vị trí cân bằng) đạt cực đại khi vật ở đâu?",
         "options": ["Ở vị trí cân bằng, vì lúc đó chuyển động mạnh nhất",
                     "Ở biên, x = ±A",
                     "Ở x = ±A/2",
                     "Ở chỗ động năng bằng thế năng"],
         "answer": 1,
         "explanation": "Et = (1/2)kx² lớn nhất khi |x| lớn nhất, tức x = ±A. Lúc đó vận tốc bằng không."},
        {"type": MC,
         "question": "Mỗi chu kì, động năng bằng thế năng bao nhiêu lần?",
         "options": ["1 lần, khi vật qua vị trí cân bằng",
                     "2 lần, vì chỉ có hai nghiệm x = ±A/√2",
                     "8 lần",
                     "4 lần"],
         "answer": 3,
         "explanation": "Có hai li độ ±A/√2, mỗi li độ vật đi qua hai lần. 2 × 2 = 4."},
        {"type": MC,
         "question": "Giữ độ cứng k và biên độ A, chỉ đổi khối lượng m. Cơ năng của con lắc lò xo (bỏ ma sát) thì sao?",
         "options": ["Không đổi, vì W = (1/2)kA²",
                     "Tăng nếu m tăng, vì W = (1/2)mv²",
                     "Giảm nếu m tăng, vì dao động chậm hơn",
                     "Bằng không cho đến khi thả tay"],
         "answer": 0,
         "explanation": "ω² = k/m nên mω² = k. W = (1/2)kA² không còn m."},
        {"type": MC,
         "question": "Chu kì biến thiên của thế năng và động năng là bao nhiêu?",
         "options": ["T, năng lượng lên xuống một lần mỗi dao động",
                     "T/2",
                     "T/4, vì mỗi chu kì có bốn lần động năng bằng thế năng",
                     "2T, vì năng lượng đổi chậm hơn li độ"],
         "answer": 1,
         "explanation": "Et cực đại ở cả hai biên, nên trong một chu kì của li độ thế năng lên đỉnh hai lần. Chu kì năng lượng là T/2, tần số góc 2ω."},
        {"type": MC,
         "question": "Cùng k, cùng m. Biên độ từ 8,0 cm giảm còn 6,0 cm. Vận tốc cực đại mới bằng vận tốc cực đại cũ nhân với:",
         "options": ["(6/8)² = 0,5625",
                     "1, vì tần số góc không phụ thuộc biên độ",
                     "8/6",
                     "6/8 = 0,75"],
         "answer": 3,
         "explanation": "v_max = ωA và ω không đổi, nên vận tốc cực đại tỉ lệ với A. Tỉ số (6/8)² là của cơ năng, không phải của vận tốc."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {
        "class_name": "Vật lí 11",
        "lesson_title": "Bài 5. Động năng. Thế năng. Sự chuyển hoá giữa động năng và thế năng trong dao động điều hoà",
    },
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Động năng · thế năng · cơ năng bảo toàn trong dao động điều hoà",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print("bundle.json: %.1f KB · %d câu · %d hình" % (
    out.stat().st_size / 1024, len(exam["questions"]), len(re.findall(r"<figure class=.fig.", theory))))
