#!/usr/bin/env python3
"""Đóng gói bundle.json từ theory.html. Chạy trong thư mục bài: python3 build_bundle.py"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Mô tả dao động điều hoà",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Tần số góc ω = 10π rad/s. Chu kì bằng bao nhiêu?",
         "options": ["10π s", "5 s", "0,1 s", "0,2 s"],
         "answer": 3,
         "explanation": "T = 2π/ω = 2π/(10π) = 0,2 s. Giá trị 5 là tần số f = ω/(2π) = 5 Hz, không phải chu kì. 0,1 s là thiếu số 2 (tính π/ω)."},
        {"type": MC,
         "question": "Vật dao động theo x = A cos(ωt − π/2). Lúc t = 0 vật ở đâu?",
         "options": ["Ở vị trí cân bằng, sắp sang phía x dương",
                     "Ở biên dương, sắp về vị trí cân bằng",
                     "Ở vị trí cân bằng, sắp sang phía x âm",
                     "Ở biên âm, sắp về vị trí cân bằng"],
         "answer": 0,
         "explanation": "cos(−π/2) = 0 nên vật ở vị trí cân bằng. Pha tăng một chút thì góc tiến về 0, côsin thành dương, li độ tăng."},
        {"type": MC,
         "question": "Trên đồ thị x–t, hai đỉnh dương liên tiếp cách 0,4 s và đỉnh cao 3 cm. Kết luận nào đúng?",
         "options": ["Bước sóng bằng 0,4 m",
                     "Tần số bằng 0,4 Hz",
                     "Chu kì bằng 0,4 s và biên độ bằng 3 cm",
                     "Biên độ bằng 0,4 cm và chu kì bằng 3 s"],
         "answer": 2,
         "explanation": "Hai đỉnh dương liên tiếp cách nhau đúng chu kì T = 0,4 s. Độ cao đỉnh là biên độ A = 3 cm. Tần số là 1/0,4 = 2,5 Hz."},
        {"type": MC,
         "question": "Hai dao động cùng chu kì. Em đổi mốc t = 0. Điều nào đúng?",
         "options": ["Pha ban đầu mỗi vật đổi; độ lệch pha không đổi",
                     "Độ lệch pha đổi; pha ban đầu không đổi",
                     "Cả pha ban đầu và độ lệch pha đều đổi",
                     "Không đại lượng nào đổi, vì cùng chu kì"],
         "answer": 0,
         "explanation": "Đổi mốc muộn τ thì mỗi pha ban đầu cộng thêm ωτ. Hiệu hai pha không đổi, nên độ lệch pha giữ nguyên."},
        {"type": MC,
         "question": "So với x1 = 4 cos(2πt) cm, dao động x2 = 4 cos(2πt − π/2) cm là:",
         "options": ["Sớm pha π/2",
                     "Đồng pha, vì cùng biên độ",
                     "Trễ pha π/2",
                     "Ngược pha"],
         "answer": 2,
         "explanation": "φ2 = −π/2 nhỏ hơn φ1 = 0 nên dao động 2 trễ pha π/2. Cùng biên độ không suy ra đồng pha. Ngược pha phải lệch π."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 11", "lesson_title": "Bài 2. Mô tả dao động điều hoà"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Các đại lượng đặc trưng, pha ban đầu và độ lệch pha giữa hai dao động cùng chu kì",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
