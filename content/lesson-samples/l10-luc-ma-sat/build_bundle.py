#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Lực ma sát",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Em đẩy ngang một thùng bằng lực 50 N nhưng thùng chưa nhúc nhích. Lực ma sát sàn tác dụng lên thùng là:",
         "options": ["Bằng 0, vì thùng chưa chuyển động", "Đúng 50 N, ngược chiều lực đẩy",
                     "Bằng μmg, tính theo công thức ma sát", "Lớn hơn 50 N, nên thùng mới đứng yên"],
         "answer": 1,
         "explanation": "Thùng đứng yên nên hợp lực bằng 0: ma sát nghỉ cân bằng đúng lực đẩy, 50 N. Công thức μN chỉ dùng cho vật đang trượt."},
        {"type": MC,
         "question": "Hộp đang trượt đều trên bàn. Dựng đứng hộp cho diện tích tiếp xúc còn 1/3, kéo cùng tốc độ. Lực ma sát trượt:",
         "options": ["Giảm còn 1/3", "Tăng gấp 3", "Gần như không đổi", "Bằng 0"],
         "answer": 2,
         "explanation": "F = μN: vật liệu và áp lực không đổi nên ma sát trượt không đổi; nó không phụ thuộc diện tích tiếp xúc."},
        {"type": MC,
         "question": "Kéo vật 3 kg trên sàn ngang bằng lực 20 N chếch lên 30° so với phương ngang, g = 9,8 m/s². Áp lực của vật lên sàn là:",
         "options": ["29,4 N", "39,4 N", "12,1 N", "19,4 N"],
         "answer": 3,
         "explanation": "N = mg − F sin30° = 29,4 − 10 = 19,4 N. Lực kéo chếch lên đỡ bớt một phần trọng lượng."},
        {"type": MC,
         "question": "Tủ 40 kg có lực ma sát nghỉ cực đại 200 N. Em đẩy ngang 120 N, tủ đứng yên. Lực ma sát sàn tác dụng lên tủ là:",
         "options": ["120 N", "200 N", "80 N", "0 N"],
         "answer": 0,
         "explanation": "Tủ đứng yên nên ma sát nghỉ cân bằng lực đẩy: 120 N. 200 N chỉ là giá trị cực đại."},
        {"type": MC,
         "question": "Quyển sách 0,5 kg đang trượt xuống mặt bàn nghiêng 30°, hệ số ma sát trượt 0,3, g = 9,8 m/s². Lực ma sát trượt bằng khoảng:",
         "options": ["1,47 N", "0,74 N", "1,27 N", "2,45 N"],
         "answer": 2,
         "explanation": "Trên mặt nghiêng N = mg cos30° ≈ 4,24 N, nên F = 0,3 · 4,24 ≈ 1,27 N. Ra 1,47 N là dùng nhầm N = mg."},
        {"type": MC,
         "question": "Khi em bước đi, lực ma sát do mặt đường tác dụng lên bàn chân đang đạp đất hướng:",
         "options": ["Ra sau, vì ma sát luôn cản chuyển động", "Thẳng đứng lên trên",
                     "Không có, vì chân không trượt", "Tới trước, cùng chiều em đi"],
         "answer": 3,
         "explanation": "Chân có xu hướng trượt ra sau nên ma sát nghỉ của đất lên chân hướng tới trước; chính lực này giúp em đi."},
        {"type": MC,
         "question": "Đẩy thùng 55 kg trên sàn ngang bằng lực ngang 220 N, hệ số ma sát trượt 0,35, g = 9,8 m/s². Gia tốc của thùng khoảng:",
         "options": ["0,57 m/s²", "4,0 m/s²", "7,4 m/s²", "3,4 m/s²"],
         "answer": 0,
         "explanation": "F_ms = 0,35 · 55 · 9,8 ≈ 188,7 N; a = (220 − 188,7)/55 ≈ 0,57 m/s². Ra 4,0 m/s² là quên ma sát."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 18. Lực ma sát"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Ma sát nghỉ, ma sát trượt, ma sát lăn; F = μN và áp lực trên mặt ngang, kéo chếch, mặt nghiêng; bài toán có ma sát",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
