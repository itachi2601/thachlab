#!/usr/bin/env python3
"""Đóng gói bundle.json từ theory.html (Bài 4. Bài tập về dao động điều hoà, lesson 23). Chạy: python3 build_bundle.py"""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {"title": "Kiểm tra nhanh — Bài tập về dao động điều hoà", "duration_minutes": 8, "questions": [
 {"type": MC, "question": "Vật dao động theo x = −6cos(5πt) cm. Biên độ và pha ban đầu là:",
  "options": ["A = −6 cm; φ = 0", "A = 6 cm; φ = π", "A = 6 cm; φ = 0", "A = 6 cm; φ = −π/2"], "answer": 1,
  "explanation": "−6cos(5πt) = 6cos(5πt + π). Biên độ luôn dương, dấu trừ chuyển vào pha thành +π. Kiểm tra: t = 0 thì x = −6 cm."},
 {"type": MC, "question": "Vật có A = 5 cm, ω = 10 rad/s. Khi vật ở x = −3 cm, tốc độ và gia tốc là:",
  "options": ["40 cm/s; −300 cm/s²", "20 cm/s; +300 cm/s²", "50 cm/s; 0", "40 cm/s; +300 cm/s²"], "answer": 3,
  "explanation": "|v| = ω√(A² − x²) = 10·√(25 − 9) = 40 cm/s. a = −ω²x = −100·(−3) = +300 cm/s²: gia tốc hướng về O."},
 {"type": MC, "question": "A = 4 cm. Lúc t = 0 vật ở x = −2 cm và đang đi về biên âm. Pha ban đầu là:",
  "options": ["−2π/3", "2π/3", "π/3", "−π/3"], "answer": 1,
  "explanation": "cos φ = −2/4 = −1/2 nên φ = ±2π/3. Đi về biên âm là v₀ < 0, mà v₀ = −Aω sin φ nên sin φ > 0: φ = 2π/3."},
 {"type": MC, "question": "Vật có T = 1,2 s. Thời gian ngắn nhất để vật đi từ x = −A/2 đến x = +A/2 là:",
  "options": ["0,1 s", "0,3 s", "0,4 s", "0,2 s"], "answer": 3,
  "explanation": "−A/2 → O mất T/12, O → +A/2 thêm T/12: tổng T/6 = 0,2 s (điểm M quét 60° trên vòng tròn pha)."},
 {"type": MC, "question": "Vật dao động theo x = 8cos(2πt + π/3) cm. Thời điểm vật qua vị trí cân bằng lần thứ hai là:",
  "options": ["7/12 s", "1/12 s", "5/12 s", "1/3 s"], "answer": 0,
  "explanation": "φ > 0 nên lúc t = 0 vật ở x = 4 cm, đang đi về O. Vật qua O khi pha bằng π/2 (lần 1) rồi 3π/2 (lần 2). M quét Δφ = 3π/2 − π/3 = 7π/6, Δt = (7π/6)/(2π) = 7/12 s. 1/12 s chỉ là lần thứ nhất."}]}
bundle = {"schema": "thachlab.lesson-bundle/v1",
 "target": {"class_name": "Vật lí 11", "lesson_title": "Bài 4. Bài tập về dao động điều hoà"},
 "theory_title": "Lý thuyết trọng tâm",
 "theory_subtitle": "Bốn họ bài tập dao động điều hoà, công thức chủ chốt và ba cái bẫy hay mất điểm",
 "theory_html": theory, "worked_examples": [], "exam": exam, "raster_images": []}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
assert json.loads(out.read_text(encoding="utf8"))["theory_html"] == theory
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB")
