#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
Thứ tự phương án và đáp án giữ đúng như quiz trong theory.html.
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Động học của chuyển động tròn đều",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Một vật đi được cung dài 3,14 m trên đường tròn bán kính 2 m. Độ dịch chuyển góc của vật là:",
         "options": ["6,28 rad", "0,64 rad", "1,57 rad", "3,14 rad"],
         "answer": 2,
         "explanation": "θ = s/r = 3,14/2 = 1,57 rad (một phần tư vòng). 6,28 là nhân s·r; 0,64 là chia ngược r/s; 3,14 là quên chia cho bán kính."},
        {"type": MC,
         "question": "Kim phút của đồng hồ có tốc độ góc bằng:",
         "options": ["π/1800 rad/s", "π/30 rad/s", "π/21600 rad/s", "120π rad/s"],
         "answer": 0,
         "explanation": "Kim phút quay một vòng mất 3600 s nên ω = 2π/3600 = π/1800 rad/s. π/30 là của kim giây, π/21600 là của kim giờ, 120π là nhân thay vì chia."},
        {"type": MC,
         "question": "Ô tô chạy vòng xuyến với tốc độ không đổi 10 m/s. Sau một phần tư vòng, độ lớn của độ biến thiên vận tốc Δv = v₂ − v₁ (hiệu hai vectơ) là:",
         "options": ["0", "14,1 m/s", "20 m/s", "10 m/s"],
         "answer": 1,
         "explanation": "Sau một phần tư vòng hai vectơ vận tốc vuông góc, cùng độ lớn 10 m/s: |Δv| = √(10² + 10²) ≈ 14,1 m/s. Ra 0 là trừ hai tốc độ; 20 m/s ứng với nửa vòng."},
        {"type": MC,
         "question": "Cánh quạt trần quay đều. Điểm A ở đầu cánh cách trục 60 cm, điểm B cách trục 20 cm. So sánh nào đúng?",
         "options": ["ωA = ωB; vA = 3vB", "vA = vB; ωA = 3ωB", "ωA = 3ωB; vA = 3vB", "ωA = ωB; vA = vB"],
         "answer": 0,
         "explanation": "Cùng một cánh nên cùng ω; v = ωr tỉ lệ với r nên vA/vB = 60/20 = 3."},
        {"type": MC,
         "question": "Lồng vắt của một máy giặt quay 1500 vòng/phút. Tốc độ góc của lồng là:",
         "options": ["25 rad/s", "9425 rad/s", "157 rad/s", "0,25 rad/s"],
         "answer": 2,
         "explanation": "f = 1500/60 = 25 Hz, ω = 2πf = 50π ≈ 157 rad/s. 25 là f (quên nhân 2π); 9425 là quên chia 60; 0,25 là lật ngược phân số."},
        {"type": MC,
         "question": "Bánh xe đạp đường kính 60 cm quay 120 vòng/phút thì điểm trên vành có tốc độ khoảng 226 m/phút. Một xe đạp bánh nhỏ có bánh xe đường kính 30 cm muốn điểm trên vành có đúng tốc độ đó thì bánh xe phải quay:",
         "options": ["60 vòng/phút", "120 vòng/phút", "480 vòng/phút", "240 vòng/phút"],
         "answer": 3,
         "explanation": "v = ωr giữ nguyên mà r giảm một nửa thì ω phải gấp đôi: 240 vòng/phút (π·0,3·240 ≈ 226 m/phút)."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 31. Động học của chuyển động tròn đều"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Độ dịch chuyển góc, radian; tốc độ góc, chu kì, tần số; v = ωr; vectơ vận tốc tiếp tuyến",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
