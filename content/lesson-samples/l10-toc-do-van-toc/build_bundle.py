#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Tốc độ và vận tốc",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Xe máy đi từ nhà tới trường 6 km hết 15 phút. Lúc qua cổng trường, tốc kế chỉ 20 km/h. Phát biểu đúng là:",
         "options": ["Tốc độ trung bình cả đường là 20 km/h",
                     "Suốt đường, tốc kế luôn chỉ 24 km/h",
                     "Xe chuyển động đều, vì tốc kế lúc nào cũng có số",
                     "Tốc độ trung bình 24 km/h; tốc độ tức thời lúc qua cổng 20 km/h"],
         "answer": 3,
         "explanation": "15 phút = 0,25 h nên tốc độ trung bình = 6 : 0,25 = 24 km/h. Số 20 km/h trên tốc kế là tốc độ tức thời tại lúc qua cổng."},
        {"type": MC,
         "question": "Một bạn chạy đúng 2 vòng sân 400 m hết 160 s, về đúng chỗ xuất phát. Kết luận đúng:",
         "options": ["Tốc độ trung bình 5 m/s; vận tốc trung bình bằng 0",
                     "Tốc độ trung bình bằng 0; vận tốc trung bình 5 m/s",
                     "Cả hai đều bằng 5 m/s",
                     "Cả hai đều bằng 2,5 m/s"],
         "answer": 0,
         "explanation": "Quãng đường 800 m nên tốc độ trung bình = 800 : 160 = 5 m/s. Về chỗ cũ nên độ dịch chuyển bằng 0, vận tốc trung bình bằng 0."},
        {"type": MC,
         "question": "Xe đi nửa đầu quãng đường với 40 km/h, nửa sau với 60 km/h. Tốc độ trung bình cả quãng là:",
         "options": ["50 km/h", "48 km/h", "100 km/h", "52 km/h"],
         "answer": 1,
         "explanation": "Lấy cả quãng 120 km: t1 = 60 : 40 = 1,5 h; t2 = 60 : 60 = 1 h; tốc độ trung bình = 120 : 2,5 = 48 km/h. 50 km/h là trung bình cộng, chỉ đúng khi hai đoạn đi cùng thời gian."},
        {"type": MC,
         "question": "Một người bơi ngược dòng với 1,5 m/s so với nước; nước chảy 2 m/s so với bờ. So với bờ, người đó:",
         "options": ["Tiến lên ngược dòng với 3,5 m/s",
                     "Tiến lên ngược dòng với 0,5 m/s",
                     "Đứng yên, vì đang bơi hết sức",
                     "Bị trôi theo chiều dòng nước với 0,5 m/s"],
         "answer": 3,
         "explanation": "Hai vận tốc ngược chiều: v13 = |1,5 − 2| = 0,5 m/s, chiều theo vận tốc lớn hơn là dòng nước, nên người bị trôi lùi."},
        {"type": MC,
         "question": "Ca nô chạy 4 m/s so với nước, mũi luôn vuông góc bờ; sông rộng 120 m; nước chảy 5 m/s so với bờ. Thời gian ca nô sang sông là:",
         "options": ["Khoảng 18,7 s", "24 s", "30 s", "Ca nô không sang được"],
         "answer": 2,
         "explanation": "Chỉ thành phần vuông góc bờ (4 m/s, so với nước) đưa ca nô sang: t = 120 : 4 = 30 s. Dòng nước dọc bờ chỉ làm ca nô cập bến xa hơn (5 · 30 = 150 m). 18,7 s là chia nhầm cho √41 ≈ 6,4 m/s; 24 s là chia nhầm cho 5 m/s."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 5. Tốc độ và vận tốc"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Tốc độ trung bình, tốc độ tức thời; vận tốc; tính tương đối và công thức cộng vận tốc",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
