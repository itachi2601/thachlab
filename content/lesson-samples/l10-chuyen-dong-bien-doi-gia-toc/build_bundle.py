#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Chuyển động biến đổi. Gia tốc",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Đoàn tàu rời ga có gia tốc 0,5 m/s². Câu nào đúng?",
         "options": ["Mỗi giây tàu đi được 0,5 m",
                     "Tàu luôn chạy với vận tốc 0,5 m/s",
                     "Cứ sau 0,5 s, vận tốc tàu tăng thêm 1 m/s",
                     "Mỗi giây, vận tốc tàu tăng thêm 0,5 m/s"],
         "answer": 3,
         "explanation": "m/s² là \"m/s mỗi giây\": gia tốc 0,5 m/s² nghĩa là mỗi giây vận tốc tăng 0,5 m/s. Sau 0,5 s vận tốc chỉ tăng 0,25 m/s."},
        {"type": MC,
         "question": "Đồ thị v–t của một xe là đoạn thẳng đi từ v = 4 m/s lúc t = 0 lên v = 10 m/s lúc t = 3 s. Gia tốc và tính chất chuyển động:",
         "options": ["a = 2 m/s², nhanh dần đều",
                     "a ≈ 3,3 m/s², nhanh dần đều",
                     "a = 2 m/s², chậm dần đều",
                     "a = 0,5 m/s², nhanh dần đều"],
         "answer": 0,
         "explanation": "Độ dốc = (10 − 4)/(3 − 0) = 2 m/s²; đồ thị đi lên nên nhanh dần đều. 3,3 là quên trừ vận tốc đầu; 0,5 là chia ngược Δt/Δv."},
        {"type": MC,
         "question": "Một xe đang chạy chậm dần đều. Chọn chiều dương ngược chiều chuyển động của xe. Dấu của v và a là:",
         "options": ["v > 0, a < 0", "v < 0, a > 0", "v < 0, a < 0", "v > 0, a > 0"],
         "answer": 1,
         "explanation": "Xe đi ngược chiều dương nên v < 0. Chậm dần thì a ngược chiều v, tức a > 0. Chậm dần hay nhanh dần xét dấu tích a·v, không xét riêng dấu a."},
        {"type": MC,
         "question": "Xe chạy qua khúc cua tròn, đồng hồ tốc độ luôn chỉ 40 km/h. Xe có gia tốc không?",
         "options": ["Không, vì tốc độ không đổi",
                     "Có, gia tốc hướng theo chiều chuyển động",
                     "Không, vì mỗi giây xe đi được quãng đường như nhau",
                     "Có, vì hướng của vận tốc thay đổi"],
         "answer": 3,
         "explanation": "Vận tốc là vectơ; đổi hướng là đổi vận tốc nên có gia tốc. Gia tốc này hướng vào phía trong cua, không theo chiều chuyển động (nếu theo chiều chuyển động thì xe phải nhanh dần)."},
        {"type": MC,
         "question": "Xe máy rời vạch dừng, chuyển động nhanh dần đều, sau 4 s đạt 36 km/h. Gia tốc của xe là:",
         "options": ["9 m/s²", "0,4 m/s²", "2,5 m/s²", "10 m/s²"],
         "answer": 2,
         "explanation": "36 km/h = 10 m/s; a = (10 − 0)/4 = 2,5 m/s². 9 m/s² là quên đổi km/h; 0,4 là chia ngược; 10 là lấy vận tốc làm gia tốc."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 8. Chuyển động biến đổi. Gia tốc"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Chuyển động biến đổi; gia tốc — định nghĩa, đơn vị, ý nghĩa; nhanh dần, chậm dần; đồ thị vận tốc – thời gian",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
