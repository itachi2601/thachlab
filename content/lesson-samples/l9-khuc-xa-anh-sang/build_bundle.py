#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts <bundle.json>
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Khúc xạ ánh sáng",
    "duration_minutes": 8,
    "questions": [
        {"type": MC, "question": "Chiếu tia sáng vuông góc với mặt nước (góc tới bằng 0°). Tia sáng đi vào nước thế nào?",
         "options": ["Gãy khúc, lệch về một bên", "Bị hắt ngược lên hết", "Đi thẳng, không đổi phương", "Toả ra nhiều hướng trong nước"],
         "answer": 2, "explanation": "i = 0° thì r = 0°: tia đi thẳng theo pháp tuyến. Chỉ khi truyền xiên góc tia mới gãy khúc."},
        {"type": MC, "question": "Ánh sáng đi trong một khối nhựa trong suốt với tốc độ 1,5·10⁸ m/s (c = 3·10⁸ m/s). Chiết suất của khối nhựa là:",
         "options": ["2", "0,5", "4,5", "1,5"],
         "answer": 0, "explanation": "n = c/v = 3·10⁸ / 1,5·10⁸ = 2. Ra 0,5 là chia ngược v/c; chiết suất không thể nhỏ hơn 1."},
        {"type": MC, "question": "Tia sáng đi từ không khí vào thuỷ tinh (n = 1,5) với góc tới 60°. Góc khúc xạ gần bằng:",
         "options": ["40°", "60°", "Không có tia khúc xạ", "35,3°"],
         "answer": 3, "explanation": "sin 60° = 1,5·sin r nên sin r ≈ 0,577, r ≈ 35,3°. Ra 40° là chia góc 60 : 1,5 thay vì chia sin."},
        {"type": MC, "question": "Ánh sáng đi từ nước (n = 1,33) ra không khí với góc tới 40°. Góc khúc xạ gần bằng:",
         "options": ["28,9°", "40°", "58,7°", "50°"],
         "answer": 2, "explanation": "1,33·sin 40° = sin r nên sin r ≈ 0,855, r ≈ 58,7° > 40°: ra môi trường kém chiết quang thì lệch xa pháp tuyến."},
        {"type": MC, "question": "Tia sáng từ không khí chiếu xuống, hợp với mặt nước (n = 1,33) một góc 60°. Góc khúc xạ gần bằng:",
         "options": ["40,6°", "22,1°", "30°", "67,9°"],
         "answer": 1, "explanation": "Góc tới i = 90° − 60° = 30°; sin r = sin 30° / 1,33 ≈ 0,376, r ≈ 22,1°. Ra 40,6° là coi 60° là góc tới."},
        {"type": MC, "question": "Đứng trên bờ, em thấy một con cá trong hồ nước trong. Con cá thật nằm ở đâu so với chỗ em nhìn thấy?",
         "options": ["Đúng chỗ nhìn thấy", "Nông hơn chỗ nhìn thấy", "Gần bờ hơn chỗ nhìn thấy", "Sâu hơn chỗ nhìn thấy"],
         "answer": 3, "explanation": "Mắt chỉ thấy ảnh của cá; ảnh nằm cao hơn và gần mắt hơn cá thật, nên cá thật ở sâu hơn."},
        {"type": MC, "question": "Tia sáng đi từ thuỷ tinh (n = 1,5) ra không khí với góc tới 30°. Góc khúc xạ gần bằng:",
         "options": ["48,6°", "19,5°", "30°", "45°"],
         "answer": 0, "explanation": "1,5·sin 30° = sin r nên sin r = 0,75, r ≈ 48,6°. Ra 45° là nhân góc 30·1,5 thay vì nhân sin."},
    ],
}
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "KHTN 9", "lesson_title": "Bài 5. Khúc xạ ánh sáng"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Hiện tượng khúc xạ, đường truyền tia sáng; chiết suất và định luật khúc xạ ánh sáng",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
