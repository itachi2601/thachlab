#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Khối lượng riêng. Áp suất chất lỏng",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Cưa một khối sắt đặc thành hai nửa bằng nhau. So với cả khối, mỗi nửa có:",
         "options": ["Khối lượng giảm một nửa, ρ giữ nguyên", "Khối lượng và ρ cùng giảm một nửa",
                     "Khối lượng giữ nguyên, ρ giảm một nửa", "Khối lượng giảm một nửa, ρ tăng gấp đôi"],
         "answer": 0,
         "explanation": "m và V cùng giảm một nửa nên ρ = m/V không đổi: khối lượng riêng là đặc trưng của chất."},
        {"type": MC,
         "question": "Viên gạch 2 kg, kích thước 20 cm × 10 cm × 5 cm, đặt đứng trên mặt 10 cm × 5 cm, g = 10 m/s². Áp suất gạch gây ra trên mặt sàn là:",
         "options": ["0,4 Pa", "400 Pa", "1000 Pa", "4000 Pa"],
         "answer": 3,
         "explanation": "F = mg = 20 N; S = 50 cm² = 5·10⁻³ m²; p = F/S = 4000 Pa. 0,4 Pa là chưa đổi cm² ra m²; 400 Pa là quên nhân g; 1000 Pa là dùng mặt 20 × 10."},
        {"type": MC,
         "question": "Vòi nước tầng 1 và tầng 5 của một chung cư cùng nối với bồn trên mái; vòi tầng 1 thấp hơn vòi tầng 5 là 12 m. Khi khoá cả hai vòi, áp suất nước ở vòi tầng 1 lớn hơn ở vòi tầng 5 một lượng (g = 10 m/s²):",
         "options": ["1,2·10⁴ Pa", "1,2·10⁵ Pa", "120 Pa", "0 Pa"],
         "answer": 1,
         "explanation": "Δp = ρgΔh = 1000·10·12 = 1,2·10⁵ Pa. 1,2·10⁴ là quên g; 120 là dùng ρ = 1 g/cm³ chưa đổi; 0 là quên vòi tầng 1 sâu hơn."},
        {"type": MC,
         "question": "Bình hẹp chứa 0,5 lít nước, mực nước cao 30 cm. Bình rộng chứa 5 lít nước, mực nước cao 20 cm. Áp suất do nước gây ra ở đáy:",
         "options": ["Ở bình hẹp lớn hơn", "Ở bình rộng lớn hơn", "Ở hai bình bằng nhau", "Chưa so được khi chưa biết diện tích đáy"],
         "answer": 0,
         "explanation": "p = ρgh chỉ phụ thuộc độ sâu: 3000 Pa ở bình hẹp, 2000 Pa ở bình rộng. Lượng nước và diện tích đáy không có mặt trong công thức áp suất."},
        {"type": MC,
         "question": "Thợ lặn ở độ sâu 15 m trong hồ nước ngọt. Áp suất khí quyển 1,0·10⁵ Pa, g = 10 m/s². Áp suất tuyệt đối tại chỗ thợ lặn là:",
         "options": ["1,5·10⁵ Pa", "1,6·10⁵ Pa", "2,5·10⁵ Pa", "1,5·10⁴ Pa"],
         "answer": 2,
         "explanation": "p = pₐ + ρgh = 1,0·10⁵ + 1,5·10⁵ = 2,5·10⁵ Pa. 1,5·10⁵ là quên pₐ; 1,6·10⁵ là nhớ nhầm 1 atm = 10⁴ Pa; 1,5·10⁴ là quên g."},
        {"type": MC,
         "question": "Chai dầu ăn có ρ = 0,92 g/cm³, cột dầu cao 50 cm, g = 10 m/s². Áp suất do dầu gây ra ở đáy chai là:",
         "options": ["4,6 Pa", "460 Pa", "460 000 Pa", "4600 Pa"],
         "answer": 3,
         "explanation": "ρ = 920 kg/m³, h = 0,5 m: p = 920·10·0,5 = 4600 Pa. Các phương án khác là quên đổi ρ hoặc h (hoặc cả hai) về SI."},
        {"type": MC,
         "question": "Bình loe miệng (miệng rộng hơn đáy) có diện tích đáy 0,02 m², chứa 9 kg nước, mực nước cao 30 cm, g = 10 m/s². Áp lực của nước lên đáy bình là:",
         "options": ["90 N", "60 N", "6000 N", "3000 N"],
         "answer": 1,
         "explanation": "p = ρgh = 3000 Pa; F = pS = 60 N, nhỏ hơn trọng lượng nước 90 N vì phần nước ở chỗ loe tựa lên thành bình."},
    ],
}

# đối chiếu đáp án bundle với tl-ok trong theory.html (bỏ câu dự đoán đầu bài)
quiz = re.findall(r'<div class="tl-quiz">(.*?)<div class="tl-fb', theory, re.S)[1:]
assert len(quiz) == len(exam["questions"]), (len(quiz), len(exam["questions"]))
for q, item in zip(quiz, exam["questions"]):
    kinds = re.findall(r'class="tl-opt (tl-ok|tl-no)"', q)
    assert kinds.index("tl-ok") == item["answer"], item["question"]

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 34. Khối lượng riêng. Áp suất chất lỏng"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "ρ = m/V; p = F/S; p = pₐ + ρgh chỉ phụ thuộc độ sâu; bình thông nhau; lực đẩy Archimedes",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
