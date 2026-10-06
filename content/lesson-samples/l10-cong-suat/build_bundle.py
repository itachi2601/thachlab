#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Bài 24. Công suất",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Thang máy nâng đều nhóm học sinh tổng khối lượng 200 kg lên cao 6 m trong 4 s (g = 10 m/s²). Công suất trung bình của lực nâng là:",
         "options": ["12 000 W", "300 W", "3 000 W", "48 000 W"],
         "answer": 2,
         "explanation": "Nâng đều: F = mg = 2 000 N; A = F·d = 12 000 J; P = A/t = 3 000 W. 12 000 là công (J), 300 W là quên g, 48 000 là nhân với t."},
        {"type": MC,
         "question": "Động cơ ghi 2 mã lực Pháp (CV), 1 CV = 736 W. Công suất của nó khoảng:",
         "options": ["1,47 kW", "368 W", "14,7 kW", "2 kW"],
         "answer": 0,
         "explanation": "2·736 = 1 472 W ≈ 1,47 kW. Ra 368 W là chia thay vì nhân; 14,7 kW lệch một bậc mười; 2 kW coi 1 CV bằng 1 kW."},
        {"type": MC,
         "question": "Ô tô chạy đều 72 km/h, lực kéo của động cơ 1 500 N. Công suất tức thời của động cơ là:",
         "options": ["108 kW", "75 W", "30 W", "30 kW"],
         "answer": 3,
         "explanation": "72 km/h = 20 m/s; P = F·v = 1 500·20 = 30 000 W = 30 kW. Ra 108 kW là chưa đổi km/h ra m/s; 75 W là chia F/v."},
        {"type": MC,
         "question": "Máy A có công suất 5 kW chạy 10 s. Máy B có công suất 1 kW chạy 100 s. Nhận xét nào đúng?",
         "options": ["Máy A có công suất lớn hơn nên cũng sinh công lớn hơn",
                     "Công suất A lớn hơn, nhưng công của B lớn hơn",
                     "Máy B sinh nhiều công hơn nên công suất của B cũng lớn hơn",
                     "Không so sánh được công suất vì hai máy chạy thời gian khác nhau"],
         "answer": 1,
         "explanation": "A_A = 5 000·10 = 50 000 J, A_B = 1 000·100 = 100 000 J. Công = công suất × thời gian nên công suất lớn chưa chắc công lớn."},
        {"type": MC,
         "question": "Bóng đèn ghi 100 W bật liên tục 10 giờ. Điện năng tiêu thụ là:",
         "options": ["1 kWh", "10 kWh", "1 000 kWh", "100 W"],
         "answer": 0,
         "explanation": "100 W·10 h = 1 000 Wh = 1 kWh (3,6·10^6 J). kWh là đơn vị công, không phải công suất."},
        {"type": MC,
         "question": "Xe máy chạy trên đường bằng, rồi gặp dốc dài. Người lái giảm số, xe chạy chậm lại. Lý do đúng:",
         "options": ["Giảm số làm động cơ phát công suất lớn hơn mức tối đa",
                     "Lên dốc thì công suất của động cơ tự động giảm đi",
                     "Công suất có hạn, P = Fv nên F lớn thì v nhỏ",
                     "Chạy chậm thì dốc kéo xe xuống yếu đi nên xe lên dễ hơn"],
         "answer": 2,
         "explanation": "Công suất tối đa gần như cố định; lên dốc cần lực kéo lớn hơn nên theo P = F·v vận tốc phải nhỏ lại."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 24. Công suất"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Công suất trung bình và tức thời; đơn vị W, kW, mã lực, kWh; P = F·v",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
