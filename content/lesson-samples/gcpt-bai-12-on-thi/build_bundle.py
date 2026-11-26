#!/usr/bin/env python3
"""Đóng gói bundle.json cho GCPT – Bài 12 (Ôn thi). Chạy: python3 build_figs.py && python3 build_bundle.py
Cấu trúc đề và thang điểm là dạng mẫu để luyện; đề thật theo thông báo của giảng viên."""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {"title": "Kiểm tra nhanh — Ôn thi tự luận", "duration_minutes": 8, "questions": [
    {"type": MC, "question": "Câu \"Giải thích vì sao cắt dây cắt được thép đã tôi\": bài nào được nhiều điểm hơn?",
     "options": ["Bài chỉ nêu cắt dây là phương pháp phi truyền thống", "Hai bài như nhau", "Bài nêu phóng điện sinh nhiệt làm chảy, bay hơi kim loại nên độ cứng không cản", "Bài dùng đúng thuật ngữ nhưng không giải thích"],
     "answer": 2, "explanation": "Đề hỏi vì sao thì cần chuỗi nguyên nhân – cơ chế – kết quả."},
    {"type": MC, "question": "Vì sao chi tiết cắt bằng EDM có thể giảm độ bền mỏi?",
     "options": ["Kim loại chảy nguội nhanh thành lớp tái đúc giòn, có thể vi nứt và ứng suất dư", "Vì EDM là phương pháp phi truyền thống", "Vì EDM làm bề mặt rất nhẵn", "Vì điện cực bị mòn"],
     "answer": 0, "explanation": "Lớp tái đúc cứng, giòn, vi nứt là nơi khởi đầu hỏng mỏi."},
    {"type": MC, "question": "Bài chọn đúng WEDM, nêu đủ lý do, nhưng không nói vì sao không chọn phay hay laser. Thiếu phần nào của khung Chọn – Vì – Loại – Lưu?",
     "options": ["Chọn", "Vì", "Lưu", "Loại"], "answer": 3,
     "explanation": "Câu chọn công nghệ đòi nêu cả các công nghệ không chọn và lý do loại."},
    {"type": MC, "question": "Tấm gốm đổi thành thép đã tôi, vẫn 20 lỗ vuông 3 × 3 mm. Công nghệ nào phù hợp nhất?",
     "options": ["Siêu âm", "EDM chìm với điện cực vuông", "Cắt plasma", "Tia nước"], "answer": 1,
     "explanation": "Thép dẫn điện nên nhóm phóng điện dùng được; điện cực vuông in lỗ vuông."},
]}
bundle = {"schema": "thachlab.lesson-bundle/v1",
          "target": {"class_name": "Các phương pháp gia công phi truyền thống", "lesson_title": "Bài 12. Ôn thi tự luận"},
          "theory_title": "Lý thuyết trọng tâm",
          "theory_subtitle": "Cấu trúc đề · khung câu chọn công nghệ · 3 đề mẫu có đáp án · lỗi hay mắc",
          "theory_html": theory, "worked_examples": [], "exam": exam, "raster_images": []}
(HERE / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi bundle.json", len(exam["questions"]), "câu")
