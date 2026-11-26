#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho GCPT – Hướng dẫn thuyết trình nhóm. Chạy: python3 build_figs.py && python3 build_bundle.py"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {"title": "Kiểm tra nhanh — Thuyết trình nhóm", "duration_minutes": 5, "questions": [
    {"type": MC, "question": "Tiêu đề slide nào tốt nhất cho phần nguyên lý của nhóm EDM?",
     "options": ["Nguyên lý", "Nguyên lý EDM",
                 "Tia lửa điện làm nóng chảy từng điểm, nên phôi chỉ cần dẫn điện", "EDM là công nghệ hiện đại"],
     "answer": 2, "explanation": "Tiêu đề tốt là một câu khẳng định nói luôn ý của slide; thân slide là sơ đồ chứng minh."},
    {"type": MC, "question": "Trong 12 phút nói, hai phần nào nên được nhiều phút nhất?",
     "options": ["Mở bài và kết", "Nguyên lý và so sánh với phương pháp khác",
                 "Thiết bị và thông số", "Giới thiệu thành viên và mục lục"], "answer": 1,
     "explanation": "Nguyên lý (40%) và so sánh (20%) chiếm 60% điểm rubric nên được khoảng 5 trên 12 phút."},
    {"type": MC, "question": "Bị hỏi một câu nhóm chưa tìm hiểu, nên trả lời thế nào?",
     "options": ["Đoán đại một đáp án nghe hợp lý", "Im lặng chờ giảng viên chuyển câu",
                 "Nói thật là chưa có số liệu và nói nhóm sẽ tìm ở đâu", "Nói câu đó không thuộc bài nhóm"],
     "answer": 2, "explanation": "Trả lời trung thực kèm hướng tìm vẫn cho thấy nhóm hiểu vấn đề; đoán sai làm mất điểm phần đúng nguyên lý."},
]}
bundle = {"schema": "thachlab.lesson-bundle/v1",
          "target": {"class_name": "Các phương pháp gia công phi truyền thống", "lesson_title": "Hướng dẫn thuyết trình nhóm"},
          "theory_title": "Lý thuyết trọng tâm",
          "theory_subtitle": "Câu chốt · chia 12 phút theo rubric · slide một ý một hình · nói và hỏi đáp",
          "theory_html": theory, "worked_examples": [], "exam": exam, "raster_images": []}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự,", len(exam["questions"]), "câu")
