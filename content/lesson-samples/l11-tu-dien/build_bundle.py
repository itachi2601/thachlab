#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/.../validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Tụ điện",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Một tụ đang nối nguồn 6 V. Đổi sang nguồn 12 V thì điện dung của tụ:",
         "options": ["Giảm một nửa", "Không đổi", "Tăng gấp đôi", "Tăng gấp bốn"],
         "answer": 1,
         "explanation": "Điện dung chỉ phụ thuộc cấu tạo tụ (S, d, ε), không phụ thuộc U. Đổi nguồn chỉ làm Q = CU gấp đôi."},
        {"type": MC,
         "question": "Cùng một tụ, nạp ở hiệu điện thế gấp đôi thì năng lượng của tụ:",
         "options": ["Tăng 4 lần", "Tăng 2 lần", "Không đổi", "Giảm 2 lần"],
         "answer": 0,
         "explanation": "W = ½CU², C không đổi nên U gấp 2 thì W gấp 4. Ra 2 lần là quên rằng Q cũng tăng theo U."},
        {"type": MC,
         "question": "Hai tụ 4 μF và 12 μF ghép nối tiếp. Điện dung của bộ là:",
         "options": ["16 μF", "8 μF", "4 μF", "3 μF"],
         "answer": 3,
         "explanation": "Nối tiếp: C = C1·C2/(C1 + C2) = 48/16 = 3 μF, nhỏ hơn tụ nhỏ nhất. 16 μF là công thức song song."},
        {"type": MC,
         "question": "Tụ phẳng nạp xong thì ngắt khỏi nguồn, rồi kéo hai bản ra xa gấp đôi. Hiệu điện thế giữa hai bản:",
         "options": ["Tăng gấp đôi", "Không đổi", "Giảm một nửa", "Tăng gấp bốn"],
         "answer": 0,
         "explanation": "Ngắt nguồn nên Q giữ nguyên; d gấp đôi thì C giảm một nửa, U = Q/C gấp đôi."},
        {"type": MC,
         "question": "Hai tụ C1 = 2 μF và C2 = 6 μF ghép nối tiếp vào nguồn 16 V. Hiệu điện thế trên tụ C1 là:",
         "options": ["4 V", "8 V", "12 V", "16 V"],
         "answer": 2,
         "explanation": "C = 12/8 = 1,5 μF; Q = 1,5·16 = 24 μC chung cho hai tụ; U1 = 24/2 = 12 V, U2 = 4 V. Tụ nhỏ chịu hiệu điện thế lớn."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 11", "lesson_title": "Bài 21. Tụ điện"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Điện dung, ghép tụ nối tiếp và song song; năng lượng của tụ điện",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
