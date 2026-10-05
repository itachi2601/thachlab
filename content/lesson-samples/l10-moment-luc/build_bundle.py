#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Moment lực. Cân bằng của vật rắn",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Đai ốc cần moment 36 N·m. Cầm cờ lê cách tâm 30 cm, ấn vuông góc cán. Lực cần dùng là:",
         "options": ["10,8 N", "1,2 N", "0,0083 N", "120 N"],
         "answer": 3,
         "explanation": "F = M/d = 36/0,30 = 120 N. Ra 10,8 N là nhân thay vì chia; ra 1,2 N là để nguyên 30 cm."},
        {"type": MC,
         "question": "Bập bênh có trục ở giữa, bỏ qua khối lượng ván. Bạn 30 kg ngồi cách trục 1,5 m. Bạn 45 kg phải ngồi bên kia cách trục bao xa để bập bênh cân bằng?",
         "options": ["1,0 m", "2,25 m", "1,5 m", "0,67 m"],
         "answer": 0,
         "explanation": "Quy tắc moment: 30g·1,5 = 45g·x nên x = 1,0 m. Người nặng hơn ngồi gần trục hơn."},
        {"type": MC,
         "question": "Lực 100 N đặt ở tay cầm cờ lê cách tâm đai ốc 0,25 m, hợp với cán góc 30°. Moment của lực là:",
         "options": ["25 N·m", "21,7 N·m", "12,5 N·m", "400 N·m"],
         "answer": 2,
         "explanation": "Cánh tay đòn là khoảng cách từ trục tới giá của lực: d = 0,25·sin30° = 0,125 m; M = 12,5 N·m. Ra 25 N·m là lấy khoảng cách tới điểm đặt."},
        {"type": MC,
         "question": "Đẩy mép cánh cửa rộng 0,8 m bằng lực 50 N, hướng dọc mặt cửa thẳng vào bản lề. Moment lực đối với trục bản lề là:",
         "options": ["40 N·m", "0", "62,5 N·m", "Lớn nhất có thể, vì lực đặt xa bản lề nhất"],
         "answer": 1,
         "explanation": "Giá của lực đi qua trục bản lề nên cánh tay đòn bằng 0, moment bằng 0: cửa không quay."},
        {"type": MC,
         "question": "Hai tay tác dụng ngẫu lực lên vô lăng, mỗi lực 20 N, hai giá cách nhau 0,36 m. Kết luận nào đúng?",
         "options": ["Hợp lực 40 N, moment 7,2 N·m", "Hợp lực bằng 0 nên vô lăng cân bằng, đứng yên",
                     "Hợp lực bằng 0, moment 3,6 N·m", "Hợp lực bằng 0, moment 7,2 N·m"],
         "answer": 3,
         "explanation": "Hai lực ngược chiều nên hợp lực bằng 0; M = F·d = 20·0,36 = 7,2 N·m, vô lăng quay. Tổng lực bằng 0 chưa đủ để cân bằng."},
        {"type": MC,
         "question": "Thanh thép đồng chất AB dài 1,2 m, nặng 40 N, kê trên giá đỡ O cách A 0,4 m, đang nằm ngang nhờ hộp 20 N treo ở A. Treo thêm vật 10 N ở B. Muốn thanh vẫn nằm ngang, ở A phải treo thêm:",
         "options": ["20 N", "10 N", "5 N", "Không cần, vì 10 N nhỏ hơn trọng lượng thanh"],
         "answer": 0,
         "explanation": "OB = 0,8 m; moment thêm 10·0,8 = 8 N·m. Ở A cần thêm 8/0,4 = 20 N."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 21. Moment lực. Cân bằng của vật rắn"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Moment lực và quy tắc moment; điều kiện cân bằng của vật rắn; ngẫu lực",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
