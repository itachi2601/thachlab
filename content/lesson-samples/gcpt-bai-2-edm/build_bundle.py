#!/usr/bin/env python3
"""Đóng gói bundle.json cho GCPT – Bài 2 EDM chìm. Chạy: python3 build_figs.py && python3 build_bundle.py"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {"title": "Kiểm tra nhanh — EDM chìm", "duration_minutes": 5, "questions": [
    {"type": MC, "question": "Điều kiện bắt buộc về vật liệu để gia công bằng EDM là:",
     "options": ["Phải rất cứng", "Phải dẫn điện", "Phải mềm hơn điện cực", "Phải là kim loại màu"], "answer": 1,
     "explanation": "Cần đường dẫn điện để đánh thủng điện môi. Độ cứng không phải điều kiện."},
    {"type": MC, "question": "Tăng Ip và Ton thì thường:",
     "options": ["Bóc nhanh hơn, bề mặt nhám hơn", "Bóc chậm hơn, bề mặt mịn hơn", "Không đổi gì", "Điện cực hết mòn"], "answer": 0,
     "explanation": "Năng lượng mỗi xung lớn hơn: bóc nhiều hơn nhưng hố phóng điện to hơn, nhám hơn, lớp tái đúc dày hơn."},
    {"type": MC, "question": "Lớp tái đúc sau EDM có đặc điểm:",
     "options": ["Dẻo, không cần xử lý", "Giòn, có thể có vi nứt; chi tiết chịu mỏi nên bóc bỏ", "Cứng hơn và luôn có lợi", "Chỉ có ở gốm"], "answer": 1,
     "explanation": "Kim loại chảy rồi nguội rất nhanh nên giòn, ứng suất dư kéo, có vi nứt."},
    {"type": MC, "question": "Bóc 200 mm³ phôi, điện cực mòn 8 mm³. Tỉ số mòn là:",
     "options": ["4%", "25%", "96%", "0,4%"], "answer": 0, "explanation": "8 / 200 = 0,04 = 4%."},
]}
bundle = {"schema": "thachlab.lesson-bundle/v1",
          "target": {"class_name": "Các phương pháp gia công phi truyền thống", "lesson_title": "Bài 2. Gia công tia lửa điện (EDM)"},
          "theory_title": "Lý thuyết trọng tâm",
          "theory_subtitle": "Phóng điện · thông số xung Ip, Ton, Toff · điện cực và mòn · lớp tái đúc · chọn EDM khi nào",
          "theory_html": theory, "worked_examples": [], "exam": exam, "raster_images": []}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự,", len(exam["questions"]), "câu")
