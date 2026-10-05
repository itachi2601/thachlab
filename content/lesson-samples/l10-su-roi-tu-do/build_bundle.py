#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Sự rơi tự do",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Hòn đá được thả rơi tự do tại nơi có g = 9,8 m/s². Sau 3 s, vận tốc và quãng đường đã rơi là:",
         "options": ["29,4 m/s và 88,2 m", "29,4 m/s và 14,7 m", "9,8 m/s và 44,1 m", "29,4 m/s và 44,1 m"],
         "answer": 3,
         "explanation": "v = gt = 9,8·3 = 29,4 m/s; s = ½gt² = ½·9,8·9 = 44,1 m. 88,2 m là quên hệ số ½; 14,7 m là quên bình phương t; 9,8 m/s là lấy g làm vận tốc."},
        {"type": MC,
         "question": "Trên Mặt Trăng (không có không khí), thả cùng lúc một cái búa và một chiếc lông chim từ cùng độ cao. Kết quả:",
         "options": ["Búa chạm đất trước, vì nặng hơn mấy chục lần",
                     "Hai vật chạm đất cùng lúc",
                     "Lông chim lơ lửng, vì trên Mặt Trăng không có trọng lực",
                     "Lông chim chạm đất sau, nhưng chênh ít hơn trên Trái Đất"],
         "answer": 1,
         "explanation": "Không có không khí thì không có lực cản: cả hai rơi tự do với cùng gia tốc rơi của Mặt Trăng (≈ 1,6 m/s²). Rơi nhanh hay chậm do lực cản, không do khối lượng."},
        {"type": MC,
         "question": "Vật rơi tự do tại nơi có g = 9,8 m/s². Quãng đường vật rơi trong giây thứ 2 là:",
         "options": ["19,6 m", "4,9 m", "14,7 m", "9,8 m"],
         "answer": 2,
         "explanation": "Giây thứ 2 là từ t = 1 s đến t = 2 s: s₂ − s₁ = 19,6 − 4,9 = 14,7 m. 19,6 m là cả 2 giây đầu; 4,9 m là giây thứ nhất."},
        {"type": MC,
         "question": "Thả viên bi từ độ cao h, bi chạm đất sau 0,6 s. Thả từ độ cao 4h tại cùng nơi, thời gian rơi là:",
         "options": ["1,2 s", "2,4 s", "9,6 s", "0,85 s"],
         "answer": 0,
         "explanation": "t = √(2h/g): độ cao gấp 4 thì thời gian gấp √4 = 2, được 1,2 s. 2,4 s là coi t tỉ lệ thuận với h; 0,85 s là nhân √2 (khi độ cao gấp 2)."},
        {"type": MC,
         "question": "Một vật rơi tự do, chạm đất với vận tốc 25 m/s. Lấy g = 10 m/s². Vật được thả từ độ cao:",
         "options": ["62,5 m", "2,5 m", "1,25 m", "31,25 m"],
         "answer": 3,
         "explanation": "v² = 2gh nên h = 25²/(2·10) = 31,25 m. 62,5 m là quên số 2 ở mẫu; 2,5 là thời gian rơi v/g; 1,25 là v/(2g), quên bình phương v."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 10. Sự rơi tự do"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Rơi trong không khí và rơi tự do; đặc điểm; công thức tính thời gian, quãng đường, vận tốc; gia tốc rơi tự do",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
