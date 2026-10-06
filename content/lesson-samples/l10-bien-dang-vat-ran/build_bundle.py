#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Biến dạng của vật rắn",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Trường hợp nào vật chịu biến dạng nén?",
         "options": ["Dây cáp treo buồng thang máy", "Dây chun buộc tóc đang bị kéo căng",
                     "Chân ghế khi em ngồi lên", "Dây đàn guitar đã lên dây"],
         "answer": 2,
         "explanation": "Chân ghế bị người đè xuống ở đầu trên và sàn đẩy lên ở đầu dưới: cặp lực hướng vào trong vật. Ba trường hợp còn lại đều bị kéo ra ở hai đầu (biến dạng kéo)."},
        {"type": MC,
         "question": "Kéo móc một lực kế bằng lực 3 N thì lò xo bên trong dãn 6 cm. Độ cứng của lò xo là:",
         "options": ["0,5 N/m", "18 N/m", "2 N/m", "50 N/m"],
         "answer": 3,
         "explanation": "k = F/|Δl| = 3/0,06 = 50 N/m. Ra 0,5 là chưa đổi cm ra m; ra 18 là nhân F với Δl; ra 2 là chia ngược."},
        {"type": MC,
         "question": "Lò xo dài tự nhiên 30 cm, độ cứng 100 N/m. Ép hai đầu cho lò xo còn dài 26 cm. Độ lớn lực đàn hồi là:",
         "options": ["4 N", "26 N", "400 N", "30 N"],
         "answer": 0,
         "explanation": "|Δl| = 30 − 26 = 4 cm = 0,04 m; F = 100·0,04 = 4 N. 26 N và 30 N là lấy chiều dài thay cho độ biến dạng; 400 N là quên đổi cm ra m."},
        {"type": MC,
         "question": "Treo vật 2 N, một lò xo dãn 4 cm. Đổi sang vật 3 N (vẫn trong giới hạn đàn hồi). Nhận định đúng là:",
         "options": ["k tăng 1,5 lần, lò xo vẫn dãn 4 cm", "k giảm, vì lò xo đã bị kéo dãn từ trước",
                     "k không đổi, lò xo dãn thêm 3 cm nữa", "k không đổi, lò xo dãn 6 cm"],
         "answer": 3,
         "explanation": "k = 2/0,04 = 50 N/m là của lò xo, không đổi theo lực. Với 3 N: |Δl| = 3/50 = 0,06 m = 6 cm, tức chỉ thêm 2 cm so với lúc treo 2 N."},
        {"type": MC,
         "question": "Một lò xo có k = 100 N/m, chỉ còn đàn hồi khi lực kéo không quá 5 N. Bạn Bình treo vật 8 N rồi tính độ dãn 8/100 = 0,08 m. Nhận xét đúng là:",
         "options": ["Đúng, F = k|Δl| dùng được với mọi lực kéo", "Sai: 8 N vượt giới hạn đàn hồi",
                     "Sai, phải tính 100/8 = 12,5 cm", "Đúng, miễn là lò xo được treo thẳng đứng"],
         "answer": 1,
         "explanation": "Định luật Hooke chỉ đúng trong giới hạn đàn hồi. Quá 5 N, lực không còn tỉ lệ với độ dãn và thôi lực lò xo không về chiều dài cũ."},
        {"type": MC,
         "question": "Lò xo k = 80 N/m, dài tự nhiên 20 cm, treo thẳng đứng. Móc vật 400 g, g = 10 m/s². Khi vật đứng yên, lò xo dài:",
         "options": ["25 cm", "5 cm", "15 cm", "20,05 cm"],
         "answer": 0,
         "explanation": "F = mg = 4 N; |Δl| = 4/80 = 0,05 m = 5 cm; lò xo dãn nên l = 20 + 5 = 25 cm. 5 cm là chưa cộng l0; 15 cm là trừ như lò xo nén; 20,05 cm là cộng mét vào xentimét."},
    ],
}

# đối chiếu đáp án bundle với tl-ok trong theory.html (bỏ câu dự đoán q1)
quiz = re.findall(r'<div class="tl-quiz">(.*?)<div class="tl-fb', theory, re.S)[1:]
assert len(quiz) == len(exam["questions"])
for q, item in zip(quiz, exam["questions"]):
    kinds = re.findall(r'class="tl-opt (tl-ok|tl-no)"', q)
    assert kinds.index("tl-ok") == item["answer"], item["question"]

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 33. Biến dạng của vật rắn"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Biến dạng kéo, nén; đàn hồi và dẻo; định luật Hooke F = k|Δl| trong giới hạn đàn hồi",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
