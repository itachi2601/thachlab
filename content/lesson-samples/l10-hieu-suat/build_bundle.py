#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) từ theory.html. Chạy: python3 build_bundle.py"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Hiệu suất",
    "duration_minutes": 8,
    "questions": [
        {"type": MC, "question": "Một xe máy nhận năng lượng 2000 kJ từ xăng, trong đó 500 kJ thành công có ích để xe chạy. Năng lượng hao phí là:",
         "options": ["2500 kJ", "500 kJ", "4 kJ", "1500 kJ"], "answer": 3,
         "explanation": "W_hp = W_tp − W_ci = 2000 − 500 = 1500 kJ. Ra 2500 kJ là cộng hai số."},
        {"type": MC, "question": "Động cơ trục chính của máy CNC nhận 5,0 kW điện, trục quay nhận 4,0 kW cơ. Hiệu suất của động cơ là:",
         "options": ["80 %", "20 %", "125 %", "1,0 kW"], "answer": 0,
         "explanation": "H = P_ci/P_tp = 4,0/5,0 = 80 %. 20 % là tỉ lệ hao phí; 125 % là chia ngược; hiệu suất không có đơn vị watt."},
        {"type": MC, "question": "Máy X nhận 10 kW điện, H = 60 %. Máy Y nhận 4 kW điện, H = 80 %. Kết luận nào đúng?",
         "options": ["Y có P_ci lớn hơn", "X có H cao hơn",
                     "X có P_ci lớn hơn nhưng H thấp hơn", "Không so được: kW khác %"], "answer": 2,
         "explanation": "P_ci của X = 0,60·10 = 6,0 kW; của Y = 0,80·4 = 3,2 kW. Hiệu suất chỉ là tỉ lệ, chưa nói máy mạnh hay yếu."},
        {"type": MC, "question": "Một máy nhận 800 J, toả ra 200 J nhiệt hao phí, phần còn lại là cơ năng có ích. Hiệu suất của máy là:",
         "options": ["25 %", "75 %", "133 %", "600 J"], "answer": 1,
         "explanation": "W_ci = 800 − 200 = 600 J; H = 600/800 = 75 %. 25 % là lấy hao phí chia toàn phần; 133 % là 800/600."},
        {"type": MC, "question": "Động cơ điện H1 = 90 % truyền chuyển động qua hộp giảm tốc H2 = 80 %. Hiệu suất cả hệ là:",
         "options": ["85 %", "170 %", "90 %", "72 %"], "answer": 3,
         "explanation": "Nối tiếp thì nhân: H = 0,90·0,80 = 72 %."},
        {"type": MC, "question": "Tời điện (H = 60 %) nâng khối 300 kg lên cao 5 m trong 10 s (g = 10 m/s²). Công suất điện tời tiêu thụ là:",
         "options": ["2,5 kW", "1,25 kW", "1,5 kW", "0,9 kW"], "answer": 0,
         "explanation": "P_ci = 15000/10 = 1500 W; P_tp = P_ci/H = 1500/0,60 = 2500 W."},
    ],
}
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 27. Hiệu suất"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Năng lượng có ích và hao phí; hiệu suất theo năng lượng và công suất; hiệu suất khi ghép nhiều máy",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · {len(re.findall(r'<figure class=.fig.', theory))} hình")
