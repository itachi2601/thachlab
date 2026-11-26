#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho GCPT – Bài 1 Tổng quan. Chạy: python3 build_figs.py && python3 build_bundle.py"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {"title": "Kiểm tra nhanh — Tổng quan gia công phi truyền thống", "duration_minutes": 5, "questions": [
    {"type": MC, "question": "Gia công phi truyền thống khác truyền thống chủ yếu ở điểm nào?",
     "options": ["Chạy nhanh hơn nhiều", "Bóc vật liệu không chủ yếu bằng lực cắt của dao cứng hơn phôi",
                 "Chỉ dùng cho kim loại mềm", "Không cần máy CNC"], "answer": 1,
     "explanation": "Cơ chế bóc là điện, nhiệt, hoá, siêu âm hoặc dòng chảy; dụng cụ không cần cứng hơn phôi. Tốc độ thường thấp hơn."},
    {"type": MC, "question": "Nhóm nào sau đây KHÔNG phải một trong ba nhóm theo dạng năng lượng?",
     "options": ["Cơ", "Điện – nhiệt", "Hoá – điện hoá", "Cắt bằng lưỡi dao tiện"], "answer": 3,
     "explanation": "Tiện bằng dao là gia công truyền thống (lực cắt)."},
    {"type": MC, "question": "Câu chọn công nghệ trong đề thi cần đủ ý nào?",
     "options": ["Chỉ tên công nghệ", "Tên công nghệ và ưu điểm",
                 "Chọn gì, vì sao, điều kiện chính, vì sao loại phương án khác", "Định nghĩa công nghệ"], "answer": 2,
     "explanation": "Phải có cả lý do chọn và lý do loại phương án khác."},
]}
bundle = {"schema": "thachlab.lesson-bundle/v1",
          "target": {"class_name": "Các phương pháp gia công phi truyền thống", "lesson_title": "Bài 1. Tổng quan gia công phi truyền thống"},
          "theory_title": "Lý thuyết trọng tâm",
          "theory_subtitle": "Vì sao cần phi truyền thống · ba nhóm theo năng lượng · cách học và cách thi môn",
          "theory_html": theory, "worked_examples": [], "exam": exam, "raster_images": []}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự,", len(exam["questions"]), "câu")
