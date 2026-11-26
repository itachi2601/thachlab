#!/usr/bin/env python3
"""Đóng gói bundle.json cho GCPT – Bài 7 (siêu âm). Dùng: python3 build_figs.py && python3 build_bundle.py"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Gia công siêu âm",
    "duration_minutes": 5,
    "questions": [
        {"type": MC, "question": "Trong USM, thứ trực tiếp bóc vật liệu khỏi phôi là:",
         "options": ["Hạt mài trong bùn bị dụng cụ rung đập vào phôi", "Cạnh sắc của dụng cụ", "Sóng siêu âm làm nóng chảy phôi", "Dòng điện giữa dụng cụ và phôi"],
         "answer": 0, "explanation": "Dụng cụ chỉ truyền dao động; hạt mài cứng mới là lưỡi cắt thật."},
        {"type": MC, "question": "Vật liệu nào hợp nhất với USM?",
         "options": ["Nhôm tấm", "Đồng đỏ", "Kính, gốm alumina", "Cao su"],
         "answer": 2, "explanation": "USM hợp vật liệu giòn; kim loại dẻo và cao su hấp thụ dao động, bóc rất chậm."},
        {"type": MC, "question": "Dụng cụ USM hình vuông thì lỗ khoét ra:",
         "options": ["Tròn", "Vuông, lớn hơn dụng cụ một chút", "Nhỏ hơn dụng cụ", "Hình tuỳ ý"],
         "answer": 1, "explanation": "Lỗ là bản sao của dụng cụ; hạt mài đập cả thành bên nên rộng hơn một chút."},
        {"type": MC, "question": "Lỗ nhỏ sâu trên thép đã tôi (dẫn điện). Nên chọn:",
         "options": ["USM", "AWJ", "Phay dao thép gió", "EDM"],
         "answer": 3, "explanation": "Phôi dẫn điện: EDM nhanh hơn, làm được lỗ nhỏ sâu. USM dành cho vật liệu không dẫn điện."},
    ],
}
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Các phương pháp gia công phi truyền thống",
               "lesson_title": "Bài 7. Gia công siêu âm (USM)"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Nguyên lý · cơ chế bóc · tỷ lệ tạo hình · RUM · chọn / không chọn · tự luận mẫu",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự,", len(exam["questions"]), "câu")
