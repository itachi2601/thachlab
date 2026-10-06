#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Đồ thị độ dịch chuyển – thời gian",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Một bạn trượt thẳng 25 m theo chiều dương rồi quay lại 15 m trên cùng đường. Quãng đường s và độ dịch chuyển d là:",
         "options": ["s = 10 m; d = 40 m", "s = 40 m; d = 10 m", "s = 40 m; d = 40 m", "s = 10 m; d = 10 m"],
         "answer": 1,
         "explanation": "Quãng đường cộng mọi đoạn: 25 + 15 = 40 m. Độ dịch chuyển so điểm cuối với điểm đầu: 25 − 15 = 10 m."},
        {"type": MC,
         "question": "Đồ thị độ dịch chuyển – thời gian của một xe là đường thẳng đi qua hai điểm (0 s; 14 m) và (4 s; 2 m). Vận tốc của xe là:",
         "options": ["3 m/s", "−3,5 m/s", "−3 m/s", "0,5 m/s"],
         "answer": 2,
         "explanation": "v = Δd/Δt = (2 − 14)/(4 − 0) = −3 m/s. Dấu trừ: xe đi ngược chiều dương. 3 m/s là quên dấu; −3,5 và 0,5 là chia một giá trị d cho t thay vì lấy hiệu."},
        {"type": MC,
         "question": "Đồ thị d–t của một người gồm: đoạn 1 xiên lên, dốc ít; đoạn 2 nằm ngang; đoạn 3 xiên xuống, dốc hơn đoạn 1. Mô tả đúng là:",
         "options": ["Đi lên dốc, đi trên đường bằng, rồi xuống dốc",
                     "Đi chậm, đi đều, rồi đi nhanh, cùng một chiều",
                     "Đi nhanh ra xa, đứng lại, rồi quay về chậm hơn",
                     "Đi chậm ra xa, đứng lại, rồi quay về nhanh hơn"],
         "answer": 3,
         "explanation": "Dốc ít, dương: ra xa chậm. Nằm ngang: đứng yên. Dốc nhiều, âm: quay về nhanh. Đồ thị không phải hình dạng con đường."},
        {"type": MC,
         "question": "Một người đi ra 5 m, đứng 3 s, rồi về đúng chỗ xuất phát. Cho cả lượt:",
         "options": ["d = 0; s = 10 m", "d = 10 m; s = 10 m", "d = 0; s = 0", "d = 5 m; s = 10 m"],
         "answer": 0,
         "explanation": "Điểm cuối trùng điểm đầu nên d = 0; quãng đường cộng từng đoạn: 5 + 0 + 5 = 10 m."},
        {"type": MC,
         "question": "Xe đồ chơi có đồ thị d–t qua O(0;0), A(4 s; 8 m), B(6 s; 8 m), C(10 s; 0), chiều dương từ vạch mốc ra cọc cờ. Nếu chọn chiều dương từ cọc cờ về vạch mốc (gốc vẫn ở vạch mốc) thì vận tốc đoạn BC và độ dịch chuyển lúc t = 4 s là:",
         "options": ["v = −2 m/s; d = 8 m", "v = 2 m/s; d = 8 m", "v = 2 m/s; d = −8 m", "v = −2 m/s; d = −8 m"],
         "answer": 2,
         "explanation": "Đổi chiều dương thì mọi đại lượng có hướng đổi dấu: d lúc 4 s từ 8 m thành −8 m; đoạn BC xe chạy về vạch mốc, nay là chiều dương, v = 2 m/s."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 7. Đồ thị độ dịch chuyển - thời gian"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Vẽ đồ thị d–t từ bảng số liệu; độ dốc là vận tốc; đọc đồ thị để mô tả chuyển động",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
