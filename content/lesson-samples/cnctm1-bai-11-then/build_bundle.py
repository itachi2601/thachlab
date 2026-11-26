#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho CNCTM 1 – Bài 11 (Gia công then – then hoa).
Dùng: python3 build_figs.py && python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
Nguồn ý: giáo trình CNCTM của bộ môn (Chương 11). Số đo rãnh 10,12/10,15/10,11 và bài toán mẫu là ví dụ tự soạn.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Kiểm tra nhanh — Gia công then, then hoa",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Mối ghép nào truyền được mômen xoắn lớn nhất và cho chi tiết trượt dọc trục?",
         "options": ["Then bằng", "Then bán nguyệt", "Then vát", "Then hoa"],
         "answer": 3,
         "explanation": "Then hoa truyền mômen lớn nhất, định tâm tốt, cho phép di trượt dọc trục."},
        {"type": MC,
         "question": "Phay rãnh then bằng KÍN (giữa trục) trên máy phay vạn năng, dùng dao nào?",
         "options": ["Dao phay đĩa ba mặt răng", "Dao phay ngón (khoan lỗ mồi trước nếu là dao thường)",
                     "Dao phay lăn", "Dao chuốt"],
         "answer": 1,
         "explanation": "Rãnh kín chỉ làm được bằng dao phay ngón; dao ngón thường không có lưỡi mặt đầu nên phải khoan mồi."},
        {"type": MC,
         "question": "Nhược điểm của phay rãnh then bằng dao phay đĩa là:",
         "options": ["Năng suất thấp", "Không làm được rãnh suốt",
                     "Rãnh bị rộng hơn bề rộng dao (từ 0,1 mm) do trục gá biến dạng, dao đảo", "Phải khoan lỗ mồi"],
         "answer": 2,
         "explanation": "Dao đĩa năng suất cao nhưng rãnh rộng ra do trục gá dao biến dạng, dao mài, gá không chính xác."},
        {"type": MC,
         "question": "Dao phay ngón hai lưỡi chuyên dùng phay rãnh then kín không cần khoan mồi vì:",
         "options": ["Dao quay rất nhanh", "Dao có lưỡi cắt ở mặt đầu, ăn sâu từng lớp 0,2–0,4 mm",
                     "Phôi được nung nóng", "Rãnh rộng hơn dao"],
         "answer": 1,
         "explanation": "Lưỡi mặt đầu cho dao tự ăn xuống; dao chạy dọc rãnh, mỗi hành trình ăn sâu 0,2–0,4 mm."},
        {"type": MC,
         "question": "Phay chép hình trục then hoa 6 răng trên đầu phân độ. Sau mỗi rãnh quay phôi:",
         "options": ["6°", "36°", "60°", "90°"],
         "answer": 2,
         "explanation": "Góc phân độ = 360° / z = 360° / 6 = 60°."},
        {"type": MC,
         "question": "Gia công then hoa trên trục bằng phay lăn (bao hình) khác phay chép hình ở chỗ:",
         "options": ["Phải dùng đầu phân độ sau mỗi rãnh", "Cắt liên tục, không cần phân độ, năng suất cao hơn",
                     "Chỉ dùng cho đơn chiếc", "Không cần máy chuyên dùng"],
         "answer": 1,
         "explanation": "Phay lăn: dao và phôi quay ăn khớp liên tục, không phân độ; dùng cho loạt lớn."},
        {"type": MC,
         "question": "Làm rãnh then trong lỗ bánh răng, sản xuất hàng loạt lớn, nên dùng:",
         "options": ["Xọc theo dấu", "Bào ngang", "Chuốt", "Phay đĩa"],
         "answer": 2,
         "explanation": "Chuốt năng suất và chính xác cao, dao đắt nên hợp loạt lớn; xọc, bào cho đơn chiếc, loạt nhỏ."},
        {"type": MC,
         "question": "Trục then hoa định tâm theo đường kính ngoài D, đã tôi. Nguyên công cuối là:",
         "options": ["Mài D trên máy mài tròn ngoài", "Mài định hình mặt bên và d",
                     "Chuốt nóng D", "Phay lăn lại"],
         "answer": 0,
         "explanation": "Mặt định tâm là D thì mài D như mài trụ trơn trên máy mài tròn ngoài; chuốt nóng là cách sửa D của lỗ."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Công nghệ chế tạo máy 1", "lesson_title": "Bài 11. Gia công then – then hoa"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Mối ghép then · phay rãnh then · then hoa chép hình, bao hình · rãnh trong lỗ · định tâm",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự lý thuyết,", len(exam["questions"]), "câu")

