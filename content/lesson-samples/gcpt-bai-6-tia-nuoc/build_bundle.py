#!/usr/bin/env python3
"""Đóng gói bundle.json cho GCPT – Bài 6 (tia nước). Dùng: python3 build_figs.py && python3 build_bundle.py"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Gia công bằng tia nước",
    "duration_minutes": 5,
    "questions": [
        {"type": MC, "question": "Tác nhân chính bóc vật liệu của AWJ là:",
         "options": ["Nước thuần", "Hạt mài do tia nước mang", "Nhiệt của tia", "Dòng điện"],
         "answer": 1, "explanation": "AWJ: nước kéo hạt mài vào ống tập trung; hạt mài va đập là phần bóc chính."},
        {"type": MC, "question": "Độ côn của vết cắt AWJ là:",
         "options": ["Miệng vào hẹp hơn đáy", "Đáy hẹp hơn miệng vào", "Hai mặt song song tuyệt đối", "Chỉ có khi cắt nước thuần"],
         "answer": 1, "explanation": "Tia mất năng lượng và loe khi đi sâu nên đáy vết cắt hẹp hơn miệng."},
        {"type": MC, "question": "Khuyết tật nào KHÔNG đặc trưng của gia công tia nước?",
         "options": ["Vệt trễ ở đáy", "Độ côn", "Vùng ảnh hưởng nhiệt (HAZ) lớn", "Hạt mài găm vào vật liệu mềm"],
         "answer": 2, "explanation": "Tia nước cắt nguội, không có HAZ đáng kể."},
        {"type": MC, "question": "Tấm thép dày 1 mm, số lượng lớn, dung sai vừa. Nên chọn:",
         "options": ["Phay cao tốc", "AWJ", "WJM", "Laser"],
         "answer": 3, "explanation": "Tấm mỏng không sợ nhiệt: laser nhanh và rẻ hơn AWJ."},
    ],
}
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Các phương pháp gia công phi truyền thống",
               "lesson_title": "Bài 6. Gia công bằng tia nước và tia nước mài (WJM, AWJ)"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Nguyên lý · WJM, AWJ · độ côn, vệt trễ · chọn / không chọn · tự luận mẫu",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự,", len(exam["questions"]), "câu")
