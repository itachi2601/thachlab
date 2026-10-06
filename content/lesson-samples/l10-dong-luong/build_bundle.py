#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Động lượng",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Bạn nhỏ 30 kg lướt 4 m/s, người lớn 60 kg lướt 2 m/s trên băng (bỏ qua ma sát). Muốn mỗi người dừng hẳn trong cùng 1 s, phải đẩy ai mạnh hơn?",
         "options": ["Bạn nhỏ, vì lướt nhanh gấp đôi", "Người lớn, vì nặng gấp đôi", "Mạnh như nhau", "Không so sánh được khi chưa biết lực"],
         "answer": 2,
         "explanation": "Hai người có cùng động lượng 30·4 = 60·2 = 120 kg·m/s, nên cần cùng xung lượng F·Δt; cùng Δt thì cùng lực."},
        {"type": MC,
         "question": "Hành khách 60 kg ngồi yên trên tàu đang chạy thẳng đều 15 m/s. Động lượng của hành khách đối với toa tàu và đối với sân ga lần lượt là:",
         "options": ["0 và 900 kg·m/s", "900 và 900 kg·m/s", "0 và 0 kg·m/s", "900 và 0 kg·m/s"],
         "answer": 0,
         "explanation": "So với toa v = 0 nên p = 0; so với sân ga v = 15 m/s nên p = 900 kg·m/s. Động lượng phụ thuộc hệ quy chiếu."},
        {"type": MC,
         "question": "Vật 2 kg đứng yên trên mặt ngang không ma sát, chịu lực ngang 50 N trong 0,2 s. Tốc độ của vật ngay sau đó là:",
         "options": ["10 m/s", "20 m/s", "125 m/s", "5 m/s"],
         "answer": 3,
         "explanation": "Δp = F·Δt = 10 kg·m/s; v = Δp/m = 5 m/s. Ra 10 m/s là quên chia cho m."},
        {"type": MC,
         "question": "Bóng tennis 0,06 kg rơi chạm sàn với tốc độ 5 m/s, nảy thẳng lên với tốc độ 4 m/s. Độ lớn độ biến thiên động lượng của bóng là:",
         "options": ["0,06 kg·m/s", "0,54 kg·m/s", "0,30 kg·m/s", "0,24 kg·m/s"],
         "answer": 1,
         "explanation": "Chọn chiều dương hướng lên: Δp = 0,06·(4 − (−5)) = 0,54 kg·m/s. Ra 0,06 là quên hai vận tốc ngược chiều."},
        {"type": MC,
         "question": "Bạn Lan 40 kg lướt 3 m/s về hướng đông, bạn Minh 50 kg lướt 3,2 m/s về hướng bắc. Độ lớn động lượng của hệ hai bạn là:",
         "options": ["280 kg·m/s", "40 kg·m/s", "200 kg·m/s", "0 kg·m/s"],
         "answer": 2,
         "explanation": "p1 = 120, p2 = 160, hai vector vuông góc: p = √(120² + 160²) = 200 kg·m/s."},
        {"type": MC,
         "question": "Nhảy từ bậc cao xuống, em gập gối khi chạm đất. Việc gập gối có tác dụng:",
         "options": ["Kéo dài thời gian dừng, lực lên chân nhỏ", "Giảm độ biến thiên động lượng của người",
                     "Giảm tốc độ của người ngay lúc chạm đất", "Tăng xung lượng để người dừng nhanh hơn"],
         "answer": 0,
         "explanation": "Δp không đổi (từ tốc độ chạm đất về 0); gập gối kéo dài Δt nên F = Δp/Δt nhỏ đi."},
        {"type": MC,
         "question": "Ô tô 1 200 kg đang chạy 15 m/s thì phanh, dừng hẳn sau 3,0 s. Độ lớn lực hãm trung bình là:",
         "options": ["18 000 N", "54 000 N", "5 N", "6 000 N"],
         "answer": 3,
         "explanation": "|Δp| = 1 200·15 = 18 000 kg·m/s; F = 18 000/3 = 6 000 N. Ra 18 000 N là quên chia Δt."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 28. Động lượng"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Động lượng p = mv, động lượng của hệ, xung lượng của lực; độ biến thiên động lượng Δp = FΔt và dạng tổng quát định luật II Newton",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
