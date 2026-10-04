#!/usr/bin/env python3
"""Đóng gói bundle.json từ theory.html. Chạy: python3 build_bundle.py"""
import json, pathlib, re
HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {"title": "Kiểm tra nhanh — Bài tập về sóng", "duration_minutes": 8, "questions": [
 {"type": MC, "question": "Đề cho khoảng cách giữa 5 ngọn sóng liên tiếp là 2 m. Bước sóng bằng:",
  "options": ["0,4 m", "0,5 m", "1 m", "2 m"], "answer": 1,
  "explanation": "5 ngọn liên tiếp có 4 khoảng, mỗi khoảng là một bước sóng: 4λ = 2 m nên λ = 0,5 m. Ra 0,4 m là chia cho số ngọn thay vì số ngọn trừ 1."},
 {"type": MC, "question": "Hai điểm trên cùng phương truyền sóng cách nhau 1,5λ. Hai điểm đó dao động:",
  "options": ["cùng pha", "ngược pha", "vuông pha", "lệch pha 3π/2 nên không đặc biệt"], "answer": 1,
  "explanation": "Δφ = 2π·1,5λ/λ = 3π, tức hơn kém π một số chẵn lần π, nên ngược pha (d = (k + 1/2)λ với k = 1)."},
 {"type": MC, "question": "Dây dài 0,9 m, một đầu cố định, một đầu tự do, λ = 1,2 m. Số bụng sóng trên dây là:",
  "options": ["1", "2", "3", "4"], "answer": 1,
  "explanation": "L = 0,9 = 3·λ/4, tức 2n + 1 = 3, n = 1, nên có n + 1 = 2 bụng (một bụng ở đầu tự do)."},
 {"type": MC, "question": "Khe Young có i = 2 mm, trường giao thoa đối xứng rộng L = 15 mm. Số vân sáng trên trường là:",
  "options": ["6", "7", "8", "9"], "answer": 1,
  "explanation": "L/(2i) = 3,75, lấy phần nguyên 3, N_s = 2·3 + 1 = 7 (vân trung tâm và 3 vân mỗi bên). Vân sáng luôn là số lẻ."},
 {"type": MC, "question": "Hai nguồn ngược pha cách nhau 20 cm, λ = 2 cm. Số cực đại và số cực tiểu trên đoạn nối hai nguồn là:",
  "options": ["19 cực đại, 20 cực tiểu", "20 cực đại, 19 cực tiểu", "19 cực đại, 19 cực tiểu", "20 cực đại, 20 cực tiểu"], "answer": 1,
  "explanation": "Nguồn ngược pha thì cực đại lấy k + 1/2 trong (−10; 10) được 20 điểm, cực tiểu lấy k được 19 điểm. Hai loại đổi chỗ so với nguồn cùng pha."}]}
bundle = {"schema": "thachlab.lesson-bundle/v1",
 "target": {"class_name": "Vật lí 11", "lesson_title": "Bài 14. Bài tập về sóng"},
 "theory_title": "Lý thuyết trọng tâm",
 "theory_subtitle": "Gọi đúng họ bài tập, công thức chủ chốt và ba cái bẫy của chương Sóng",
 "theory_html": theory, "worked_examples": [], "exam": exam, "raster_images": []}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB")
