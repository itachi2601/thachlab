#!/usr/bin/env python3
"""Đóng gói bundle.json từ theory.html. Chạy: python3 build_bundle.py"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {"title": "Kiểm tra nhanh — Bài tập năng lượng trong dao động điều hoà", "duration_minutes": 8, "questions": [
 {"type": MC, "question": "Lò xo k = 100 N/m, biên độ 5 cm. Động năng của vật tại li độ x = 3 cm là:",
  "options": ["0,045 J", "0,125 J", "0,080 J", "800 J"], "answer": 2,
  "explanation": "W = ½·100·0,05² = 0,125 J; Wt = ½·100·0,03² = 0,045 J; Wđ = W − Wt = 0,080 J. Ra 800 J là thế A, x bằng cm, quên đổi ra mét."},
 {"type": MC, "question": "Vật dao động với biên độ 9 cm. Động năng bằng 8 lần thế năng tại li độ:",
  "options": ["±3 cm", "±1 cm", "±3,18 cm", "±1,125 cm"], "answer": 0,
  "explanation": "Wđ = 8Wt thì W = 9Wt, x = ±A/√9 = ±3 cm. Ra ±1 cm là quên căn; ±3,18 cm là quên cộng 1 phần thế năng."},
 {"type": MC, "question": "Đồ thị thế năng theo thời gian của một vật dao động điều hoà lặp lại sau mỗi 0,25 s. Chu kì dao động của vật là:",
  "options": ["0,25 s", "0,125 s", "1,0 s", "0,5 s"], "answer": 3,
  "explanation": "Thế năng biến thiên với chu kì T/2 = 0,25 s, nên T = 0,5 s. Lấy luôn 0,25 s là nhầm chu kì năng lượng với chu kì dao động."},
 {"type": MC, "question": "Con lắc đơn dài 0,8 m, thả từ góc 45°, g = 10 m/s². Tốc độ khi qua vị trí cân bằng là:",
  "options": ["2,16 m/s", "3,36 m/s", "4,69 m/s", "127 m/s"], "answer": 0,
  "explanation": "v = √(2gl(1 − cos 45°)) = √(16·0,293) ≈ 2,16 m/s. 3,36 m/s là dùng cos α0 thay 1 − cos α0; 4,69 là quên lấy căn."},
 {"type": MC, "question": "Con lắc lò xo m = 100 g, k = 100 N/m, biên độ 4 cm (π² = 10). Tại vị trí thế năng bằng 3 lần động năng, tốc độ của vật là:",
  "options": ["1,10 m/s", "0,63 m/s", "0,32 m/s", "63 m/s"], "answer": 1,
  "explanation": "v_max = ωA = 10π·0,04 ≈ 1,26 m/s. Wđ = W/4 nên v = v_max/2 ≈ 0,63 m/s. 1,10 m/s là đọc ngược thành Wđ = 3Wt."}]}
bundle = {"schema": "thachlab.lesson-bundle/v1",
 "target": {"class_name": "Vật lí 11", "lesson_title": "Bài 7. Bài tập về sự chuyển hoá năng lượng trong dao động điều hoà"},
 "theory_title": "Lý thuyết trọng tâm",
 "theory_subtitle": "Bốn họ bài tập năng lượng dao động: công thức chủ chốt và ba cái bẫy",
 "theory_html": theory, "worked_examples": [], "exam": exam, "raster_images": []}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB")
