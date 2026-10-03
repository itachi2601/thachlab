#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/.../validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Sóng dừng",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Bấm phím cho đoạn dây đàn rung ngắn lại, giữ nguyên sức căng dây. Tần số âm phát ra sẽ:",
         "options": ["Thấp hơn, vì dây ngắn dao động chậm hơn",
                     "Không đổi, vì vẫn là sợi dây đó",
                     "Cao hơn, vì dây ngắn thì tần số lớn hơn",
                     "Không đổi, vì tai người không phân biệt được"],
         "answer": 2,
         "explanation": "Tần số nhỏ nhất của sóng dừng trên dây hai đầu cố định là f0 = v/(2l) (nói chung f = k·v/(2l)). Sức căng giữ nguyên nên v không đổi; l giảm thì f tăng, tai nghe nốt cao hơn."},
        {"type": MC,
         "question": "Dây AB dài 1,2 m, hai đầu cố định, có sóng dừng với 3 bó sóng. Bước sóng trên dây là:",
         "options": ["1,2 m", "0,4 m", "0,6 m", "0,8 m"],
         "answer": 3,
         "explanation": "Ba bó thì l = 3λ/2, suy ra λ = 2l/3 = 2 × 1,2/3 = 0,8 m. Ra 0,4 m là lấy l/3 (mỗi bó dài λ/2 chứ không phải λ)."},
        {"type": MC,
         "question": "Sóng tới trên dây có biên độ A. Tại một bụng sóng, biên độ dao động và bề rộng vùng dao động của bụng lần lượt là:",
         "options": ["2A và 4A", "A và 2A", "2A và 2A", "4A và 4A"],
         "answer": 0,
         "explanation": "Hai sóng thành phần cùng pha ở bụng nên biên độ bằng 2A; bụng vung từ +2A xuống −2A nên bề rộng bằng 4A."},
        {"type": MC,
         "question": "Dây dài 0,6 m, một đầu cố định và một đầu tự do, tốc độ truyền sóng trên dây v = 12 m/s. Tần số nhỏ nhất để trên dây có sóng dừng là:",
         "options": ["2,5 Hz", "10 Hz", "5 Hz", "20 Hz"],
         "answer": 2,
         "explanation": "Một đầu tự do, tần số nhỏ nhất ứng với l = λ/4: λ = 4l = 2,4 m, f = v/λ = 12/2,4 = 5 Hz. Ra 10 Hz là dùng nhầm công thức của dây hai đầu cố định."},
        {"type": MC,
         "question": "Dây dài 60 cm, hai đầu cố định, có sóng dừng với 3 bó sóng. Trên dây có bao nhiêu nút sóng?",
         "options": ["3 nút", "4 nút", "5 nút", "6 nút"],
         "answer": 1,
         "explanation": "Hai đầu dây cũng là nút, nên k bó có k + 1 = 4 nút. Chọn 3 là quên hai đầu; chọn 6 là lấy 2 nút cho mỗi bó (2k) mà quên hai nút ở giữa do hai bó dùng chung."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 11", "lesson_title": "Sóng dừng"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Nút, bụng sóng và điều kiện có sóng dừng; tính bước sóng, tốc độ truyền sóng từ sóng dừng",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
