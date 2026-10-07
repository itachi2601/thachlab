#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Thực hành đo tiêu cự của thấu kính hội tụ",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Hứng ảnh của một cột đèn đặt cách thấu kính 1 m. Ảnh nét nhất khi màn cách tâm thấu kính 15,2 cm. Tiêu cự gần nhất với:",
         "options": ["f ≈ 15,2 cm, vì ảnh luôn ở tiêu điểm", "f ≈ 7,6 cm, vì ảnh cách kính 2f", "f ≈ 115,2 cm, vì f = d + d'", "f ≈ 13,2 cm, vì 1/f = 1/d + 1/d'"],
         "answer": 3,
         "explanation": "Cột đèn cách 1 m chưa phải rất xa: 1/f = 1/100 + 1/15,2 ≈ 0,0758 nên f ≈ 13,2 cm. Coi d' = f sẽ lệch rõ."},
        {"type": MC,
         "question": "Đo cách 2 năm lần được f = 10,0; 9,9; 10,1; 9,8; 10,1 cm. Lấy f̄ = 10,0 cm. Lần nào có f lệch xa f̄ nhất?",
         "options": ["Lần có f = 9,8 cm (d = 30,0 cm)", "Lần có f = 10,0 cm (d = 15,0 cm)", "Lần có f = 10,1 cm (d = 25,0 cm)", "Lần có f = 10,1 cm (d = 40,0 cm)"],
         "answer": 0,
         "explanation": "|9,8 − 10,0| = 0,2 cm là lệch lớn nhất; các lần khác lệch 0 hoặc 0,1 cm. Sai số lấy bằng độ lệch lớn nhất: f = 10,0 ± 0,2 cm."},
        {"type": MC,
         "question": "Ảnh nét, cao đúng bằng vật, khoảng cách vật – màn L = 48,0 cm. Tiêu cự là:",
         "options": ["f = 24,0 cm", "f = 96,0 cm", "f = 12,0 cm", "f = 48,0 cm"],
         "answer": 2,
         "explanation": "Ảnh bằng vật thì d = d' = 2f nên L = 4f, f = 48,0/4 = 12,0 cm. 24,0 cm là d (hay d') chứ không phải f."},
        {"type": MC,
         "question": "Thật ra d = d' = 20,0 cm (tới tâm). Giá đỡ dày 2,0 cm; nhóm đo từ vật tới mặt trước giá và từ mặt sau giá tới màn, được d = d' = 19,0 cm. Nhóm tính ra:",
         "options": ["f = 9,5 cm, nhỏ hơn thật", "f = 10,0 cm, đúng như thật", "f = 10,5 cm, lớn hơn thật", "f = 19,0 cm, bằng d"],
         "answer": 0,
         "explanation": "f = 19,0·19,0/(19,0 + 19,0) = 9,5 cm. d và d' hụt cùng phía nên cùng làm f nhỏ đi, không bù nhau."},
        {"type": MC,
         "question": "Dịch màn thấy ảnh còn nét khi màn ở từ 19,4 cm đến 20,6 cm; ngoài khoảng đó thì nhoè. Nên ghi d' bằng:",
         "options": ["19,4 cm, chỗ ảnh vừa hết nhoè", "20,6 cm, chỗ ảnh vừa bắt đầu nhoè", "40,0 cm, tổng của hai đầu mút", "20,0 cm, trung điểm khoảng nét"],
         "answer": 3,
         "explanation": "(19,4 + 20,6)/2 = 20,0 cm. Ảnh nét là cả một đoạn nên ghi trung điểm; độ rộng 1,2 cm gợi ý về sai số của d'."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "KHTN 9", "lesson_title": "Bài 9. Thực hành đo tiêu cự của thấu kính hội tụ"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Ba cách đo tiêu cự thấu kính hội tụ; xử lí số liệu và sai số; vẽ sơ đồ tỉ lệ để giải bài tập",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
