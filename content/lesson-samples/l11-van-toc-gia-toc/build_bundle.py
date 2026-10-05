#!/usr/bin/env python3
"""Đóng gói bundle.json từ theory.html. Chạy: python3 build_bundle.py"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Kiểm tra nhanh — Vận tốc, gia tốc trong dao động điều hoà",
    "duration_minutes": 8,
    "difficulty": "trung-binh",
    "questions": [
        {"type": MC,
         "question": "Pha ban đầu bằng 0, x = A cos(ωt). Tại t = T/4, vận tốc bằng bao nhiêu?",
         "options": ["+Aω", "0", "−Aω", "−Aω²"],
         "answer": 2,
         "explanation": "ωt = π/2 nên v = −Aω sin(π/2) = −Aω. Lúc này li độ bằng 0, vận tốc đang âm nhất."},
        {"type": MC,
         "question": "Giá trị đại số a_max = +Aω² đạt tại đâu?",
         "options": ["Biên dương", "VTCB, đang đi chiều dương", "VTCB, đang đi chiều âm", "Biên âm"],
         "answer": 3,
         "explanation": "a = −ω²x nên a dương nhất khi x = −A, tức biên âm. Biên dương là a_min. Tại VTCB thì a = 0."},
        {"type": MC,
         "question": "Vật đi từ vị trí cân bằng ra biên dương. Câu nào đúng?",
         "options": ["a cùng chiều v, nhanh dần đều",
                     "a cùng chiều v, nhanh dần không đều",
                     "a ngược chiều v, chậm dần không đều",
                     "a = 0 trên cả đoạn vì tốc độ đang giảm"],
         "answer": 2,
         "explanation": "Ra biên dương thì v > 0 và a = −ω²x < 0, ngược chiều, chậm dần. |a| đổi theo x nên không đều."},
        {"type": MC,
         "question": "Con lắc có A = 2 cm, f = 5 Hz. Tốc độ cực đại của vật là bao nhiêu?",
         "options": ["10 cm/s", "20π cm/s", "5 cm/s", "2 cm/s"],
         "answer": 1,
         "explanation": "ω = 2πf = 10π rad/s, v_max = Aω = 20π cm/s. Không lấy A·f và không lẫn với tốc độ truyền sóng."},
        {"type": MC,
         "question": "A = 4 cm, ω = 10 rad/s. Độ lớn vận tốc tại x = 2 cm là bao nhiêu?",
         "options": ["20√3 cm/s", "40 cm/s", "20 cm/s", "10√3 cm/s"],
         "answer": 0,
         "explanation": "|v| = ω√(A²−x²) = 10√12 = 20√3 cm/s. 40 cm/s là Aω tại vị trí cân bằng."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 11", "lesson_title": "Bài 3. Vận tốc, gia tốc trong dao động điều hoà"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Công thức vận tốc, gia tốc theo li độ; Quan hệ pha giữa x, v, a; Hệ thức độc lập với thời gian",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print("bundle.json: %.1f KB · %d câu · %d hình" % (
    out.stat().st_size / 1024, len(exam["questions"]), len(re.findall(r"<figure class=.fig.", theory))))
