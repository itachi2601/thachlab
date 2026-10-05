#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Năng lượng. Công cơ học",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Kéo vali bằng lực 50 N, dây hợp với phương ngang 60°, vali đi thẳng 20 m trên sàn ngang. Công của lực kéo là:",
         "options": ["1000 J", "866 J", "-500 J", "500 J"],
         "answer": 3,
         "explanation": "A = F·s·cosα = 50·20·cos60° = 500 J. Ra 1000 J là quên cosα; 866 J là dùng sin60°."},
        {"type": MC,
         "question": "Cần cẩu hạ kiện hàng thẳng đứng xuống, chậm đều. Công của lực căng dây cáp lên kiện hàng:",
         "options": ["Âm, vì lực hướng lên, kiện đi xuống", "Dương, vì dây cáp đang kéo giữ kiện hàng",
                     "Bằng 0, vì kiện hàng chuyển động thẳng đều", "Dương, vì kiện đi xuống cùng chiều với trọng lực"],
         "answer": 0,
         "explanation": "Lực căng hướng lên, độ dịch chuyển hướng xuống: α = 180°, công âm (công cản)."},
        {"type": MC,
         "question": "Em xách xô nước nặng 100 N, đi đều 10 m trên sàn nằm ngang, xô giữ ở độ cao không đổi. Công của lực tay lên xô là:",
         "options": ["1000 J", "-1000 J", "0", "10 J"],
         "answer": 2,
         "explanation": "Lực tay hướng thẳng lên, xô đi ngang: α = 90°, cosα = 0 nên A = 0 dù tay vẫn mỏi."},
        {"type": MC,
         "question": "Đứng trên giày trượt, em đẩy thành sân băng bằng lực 150 N và lùi ra xa được 2 m. Công của lực em đẩy lên thành sân là:",
         "options": ["300 J", "0", "-300 J", "75 J"],
         "answer": 1,
         "explanation": "Lực đặt lên thành sân, thành sân không dịch chuyển nên A = 0. Quãng 2 m là của em."},
        {"type": MC,
         "question": "Kéo thùng lên dốc nghiêng 30° bằng lực 200 N song song mặt dốc, thùng đi được 5 m dọc dốc. Công của lực kéo là:",
         "options": ["866 J", "500 J", "-1000 J", "1000 J"],
         "answer": 3,
         "explanation": "Lực cùng hướng đường đi nên α = 0°, A = 200·5 = 1000 J. Góc dốc không phải góc giữa lực và đường đi."},
        {"type": MC,
         "question": "Kéo ván trượt tổng 30 kg trên băng nằm ngang bằng dây chếch lên 30°, lực 40 N; hệ số ma sát trượt 0,05; g = 10 m/s². Ván đi 30 m. Công của lực ma sát là:",
         "options": ["-420 J", "-210 J", "420 J", "-450 J"],
         "answer": 0,
         "explanation": "N = 300 − 40·sin30° = 280 N; F_ms = 14 N; A_ms = −14·30 = −420 J. Ra −450 J là lấy N = mg."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 23. Năng lượng. Công cơ học"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Năng lượng: dạng, chuyển hoá, bảo toàn; công cơ học và dấu của công; công của trọng lực và lực ma sát",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
