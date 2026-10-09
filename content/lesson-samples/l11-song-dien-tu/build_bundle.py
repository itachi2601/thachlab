#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Sóng điện từ",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Sóng từ vệ tinh truyền thẳng đứng xuống mặt đất. Tại một điểm, vectơ E nằm ngang theo hướng Đông – Tây. Vectơ B tại đó nằm theo phương:",
         "options": ["Bắc – Nam", "Đông – Tây", "Thẳng đứng", "Một phương nằm ngang bất kì"],
         "answer": 0,
         "explanation": "B vuông góc với phương truyền (thẳng đứng) nên nằm ngang, và vuông góc với E (Đông – Tây) nên theo hướng Bắc – Nam."},
        {"type": MC,
         "question": "Trong lò vi sóng (f = 2,45 GHz), hai vệt chảy liền nhau trên thanh sô-cô-la cách nhau nửa bước sóng. Đo được khoảng cách trung bình d = 6,10 cm. Tốc độ sóng điện từ tính được là:",
         "options": ["1,49·10⁸ m/s", "2,99·10⁸ m/s", "2,99·10¹⁰ m/s", "4,98·10⁻¹¹ m/s"],
         "answer": 1,
         "explanation": "λ = 2d = 0,122 m; c = λf = 0,122 × 2,45·10⁹ ≈ 2,99·10⁸ m/s. Lấy λ = d ra 1,49·10⁸; để λ bằng cm ra 2,99·10¹⁰."},
        {"type": MC,
         "question": "Một bức xạ có tần số 1,0·10¹⁵ Hz trong chân không. Nó thuộc vùng:",
         "options": ["Hồng ngoại", "Ánh sáng nhìn thấy", "Sóng vô tuyến", "Tử ngoại"],
         "answer": 3,
         "explanation": "λ = c/f = 3·10⁸/10¹⁵ = 3·10⁻⁷ m = 300 nm, ngắn hơn ánh sáng tím (380 nm): vùng tử ngoại."},
        {"type": MC,
         "question": "Sóng đài FM và tia X cùng đi trong chân không. So sánh tốc độ của chúng:",
         "options": ["Bằng nhau", "Tia X nhanh hơn vì tần số lớn hơn", "Sóng FM nhanh hơn vì mỗi bước sóng dài hơn", "Tia X nhanh hơn vì đâm xuyên mạnh hơn"],
         "answer": 0,
         "explanation": "Trong chân không mọi sóng điện từ có cùng tốc độ c = 3·10⁸ m/s; f lớn thì λ nhỏ, tích λf vẫn là c."},
        {"type": MC,
         "question": "Một đài phát thanh AM phát sóng tần số 600 kHz. Bước sóng của đài là:",
         "options": ["0,5 m", "2·10⁻³ m", "500 m", "1,8·10¹⁴ m"],
         "answer": 2,
         "explanation": "f = 6·10⁵ Hz; λ = c/f = 3·10⁸/6·10⁵ = 500 m. Nhầm kHz với MHz ra 0,5 m."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 11", "lesson_title": "Bài 11. Sóng điện từ"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Đặc điểm sóng điện từ · λ = c/f · thang sóng điện từ · ứng dụng trong truyền thông",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
