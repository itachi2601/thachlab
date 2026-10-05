#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Trọng lực và lực căng",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Một phôi thép 2 kg đưa từ xưởng (g = 9,8 m/s²) lên đỉnh núi (g = 9,7 m/s²). Nhận xét đúng là:",
         "options": ["Khối lượng và trọng lượng đều giảm",
                     "Khối lượng giảm, trọng lượng giữ nguyên 19,6 N",
                     "Cả hai giữ nguyên, vì vẫn là phôi đó",
                     "Khối lượng giữ nguyên 2 kg, trọng lượng giảm từ 19,6 N còn 19,4 N"],
         "answer": 3,
         "explanation": "Khối lượng là lượng chất, không đổi khi đổi chỗ. Trọng lượng P = mg đổi theo g: 2·9,8 = 19,6 N thành 2·9,7 = 19,4 N."},
        {"type": MC,
         "question": "Một nhà du hành có khối lượng 60 kg. Trên Mặt Trăng (g = 1,6 m/s²), số đo nào là đúng?",
         "options": ["Khối lượng 10 kg, trọng lượng 96 N",
                     "Khối lượng 60 kg, trọng lượng 588 N",
                     "Khối lượng 60 kg, trọng lượng 96 N",
                     "Khối lượng 9,6 kg, trọng lượng 60 N"],
         "answer": 2,
         "explanation": "Khối lượng vẫn 60 kg; P = 60·1,6 = 96 N. 588 N là dùng nhầm g của Trái Đất."},
        {"type": MC,
         "question": "Cầu trục nâng phôi 200 kg lên, nhanh dần với a = 0,5 m/s² (g = 10 m/s²). Lực căng của cáp là:",
         "options": ["2 000 N", "2 100 N", "1 900 N", "100 N"],
         "answer": 1,
         "explanation": "Chiều dương hướng lên: T − P = ma nên T = m(g + a) = 200·10,5 = 2 100 N. 2 000 N là coi T = P, 1 900 N là lấy nhầm g − a, 100 N chỉ là ma."},
        {"type": MC,
         "question": "Con lắc gồm quả cầu treo dưới sợi dây, đang ở vị trí lệch sang phải. Lực căng dây tác dụng lên quả cầu hướng:",
         "options": ["Thẳng đứng lên trên",
                     "Dọc dây, từ điểm treo xuống quả cầu",
                     "Nằm ngang, về vị trí cân bằng",
                     "Dọc dây, từ quả cầu về phía điểm treo"],
         "answer": 3,
         "explanation": "Lực căng đặt ở chỗ dây buộc vào quả cầu, nằm dọc dây và kéo quả cầu về phía dây (về điểm treo). Dây chỉ kéo, không đẩy."},
        {"type": MC,
         "question": "Khối A 2 kg trên bàn nằm ngang nhẵn nối bằng dây nhẹ không dãn qua ròng rọc nhẹ với vật B 0,5 kg treo thẳng đứng (g = 10 m/s²). Lực căng dây khi hệ chuyển động là:",
         "options": ["5 N", "4 N", "2 N", "10 N"],
         "answer": 1,
         "explanation": "a = m_B·g/(m_A + m_B) = 5/2,5 = 2 m/s²; T = m_A·a = 4 N. 5 N là coi T bằng trọng lượng B dù hệ đang có gia tốc; 2 N là lấy nhầm a làm T."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 17. Trọng lực và lực căng"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Trọng lực, trọng lượng và trọng tâm; lực căng dây — hệ vật nối dây, ròng rọc",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
