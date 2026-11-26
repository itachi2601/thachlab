#!/usr/bin/env python3
"""Đóng gói bundle.json cho GCPT – Bài 3 Cắt dây WEDM. Chạy: python3 build_figs.py && python3 build_bundle.py"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {"title": "Kiểm tra nhanh — Cắt dây WEDM", "duration_minutes": 5, "questions": [
    {"type": MC, "question": "Vì sao dây trong WEDM chạy liên tục từ cuộn cấp sang cuộn thu?",
     "options": ["Để dây cắt bằng lực nhanh hơn", "Để đoạn dây mòn rời vùng cắt, luôn có dây mới nên khe cắt ổn định",
                 "Để làm mát phôi", "Để tạo góc côn"], "answer": 1,
     "explanation": "Tia lửa làm mòn dây; chạy liên tục giữ đường kính dây tại vùng cắt ổn định."},
    {"type": MC, "question": "Dây d = 0,25 mm, khe g = 0,02 mm mỗi bên. Bề rộng khe cắt W là:",
     "options": ["0,25 mm", "0,27 mm", "0,29 mm", "0,31 mm"], "answer": 2, "explanation": "W = d + 2g = 0,25 + 0,04 = 0,29 mm."},
    {"type": MC, "question": "Cần khoét hốc vuông đáy kín trong thép tôi. Nên chọn:",
     "options": ["WEDM", "EDM chìm", "Cắt dây rồi hàn đáy", "Tia nước"], "answer": 1,
     "explanation": "Dây đi xuyên suốt, không chừa đáy. Hốc kín đáy dùng EDM chìm với điện cực tạo hình."},
    {"type": MC, "question": "Mục đích chính của các lượt cắt tinh (skim cut) là:",
     "options": ["Cắt nhanh hơn lượt thô", "Bóc lớp mỏng cho mặt mịn, chính xác, sửa lệch do ứng suất dư", "Làm dây bền hơn", "Tạo lỗ mồi"], "answer": 1,
     "explanation": "Lượt tinh dùng dòng nhỏ, bóc lớp mỏng; không nhanh hơn lượt thô."},
]}
bundle = {"schema": "thachlab.lesson-bundle/v1",
          "target": {"class_name": "Các phương pháp gia công phi truyền thống", "lesson_title": "Bài 3. Cắt dây (WEDM)"},
          "theory_title": "Lý thuyết trọng tâm",
          "theory_subtitle": "Dây – nước – bàn · khe cắt · cắt thô và cắt tinh · cắt côn · so với EDM chìm",
          "theory_html": theory, "worked_examples": [], "exam": exam, "raster_images": []}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự,", len(exam["questions"]), "câu")
