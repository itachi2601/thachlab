#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Chuyển động thẳng biến đổi đều",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Một xe máy phanh ở 36 km/h thì trượt 10 m rồi dừng. Cũng xe đó, cùng đường, phanh y như cũ ở 72 km/h thì trượt bao xa?",
         "options": ["20 m", "40 m", "10 m", "30 m"],
         "answer": 1,
         "explanation": "Phanh tới dừng: d = v0²/(2|a|), quãng phanh tỉ lệ với bình phương tốc độ. Tốc độ gấp đôi thì quãng phanh gấp 4: 4·10 = 40 m. 20 m là nghĩ quãng phanh tỉ lệ thuận với tốc độ."},
        {"type": MC,
         "question": "Ô tô đang chạy 10 m/s thì tăng tốc đều, sau 5 s đạt 20 m/s. Quãng đường đi được trong 5 s đó là:",
         "options": ["50 m", "100 m", "75 m", "25 m"],
         "answer": 2,
         "explanation": "Vận tốc trung bình (10 + 20)/2 = 15 m/s, nhân 5 s được 75 m. Hoặc a = 2 m/s², d = 10·5 + ½·2·5² = 75 m."},
        {"type": MC,
         "question": "Một xe chạy theo chiều âm của trục Ox với v = −10 m/s, gia tốc a = −2 m/s². Xe đang:",
         "options": ["Chậm dần đều, vì a < 0",
                     "Chậm dần đều, vì xe đi ngược chiều dương",
                     "Chuyển động thẳng đều, vì a không đổi",
                     "Nhanh dần đều, vì a cùng dấu v"],
         "answer": 3,
         "explanation": "a·v = (−2)(−10) = 20 > 0 nên nhanh dần đều. Dấu của a riêng nó chỉ cho biết chiều của gia tốc so với chiều dương."},
        {"type": MC,
         "question": "Ô tô đang chạy 10 m/s thì phanh, chậm dần đều với gia tốc có độ lớn 2 m/s². Quãng đường xe đi được trong 8 s kể từ lúc phanh là:",
         "options": ["16 m", "25 m", "80 m", "144 m"],
         "answer": 1,
         "explanation": "Xe dừng sau t = 10/2 = 5 s, đi được 10²/(2·2) = 25 m, rồi đứng yên. 16 m là thay thẳng t = 8 s vào công thức như thể xe chạy lùi."},
        {"type": MC,
         "question": "Ô tô khởi hành từ vạch dừng với a = 2 m/s²; cùng lúc xe máy chạy đều 10 m/s đi qua vạch, cùng chiều. Trước khi ô tô đuổi kịp, khoảng cách hai xe lớn nhất vào lúc nào?",
         "options": ["t = 0, khi vừa đèn xanh",
                     "t = 10 s, ngay trước khi gặp",
                     "Khoảng cách tăng đều, không có lúc nào lớn nhất",
                     "t = 5 s, khi hai xe cùng vận tốc"],
         "answer": 3,
         "explanation": "Khoảng cách 10t − t² lớn nhất tại t = 5 s (25 m), đúng lúc hai xe cùng vận tốc 10 m/s. Lúc t = 0 và t = 10 s khoảng cách bằng 0."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 9. Chuyển động thẳng biến đổi đều"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Gia tốc, đồ thị v–t, ba công thức của chuyển động thẳng biến đổi đều — hai xe gặp nhau, phanh gấp",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
