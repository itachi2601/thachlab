#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho CNCTM 2 – Bài 19 (Công nghệ lắp ráp, phần 1).
Dùng: python3 build_figs.py && python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
Nguồn ý: giáo trình CNCTM của bộ môn (Chương 19). Các bài số là ví dụ tự soạn, đã tính lại bằng python.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Kiểm tra nhanh — Công nghệ lắp ráp (phần 1)",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Mối lắp bằng đinh tán thuộc loại nào?",
         "options": ["Cố định, tháo được", "Cố định, không tháo được", "Di động, tháo được", "Di động, không tháo được"],
         "answer": 1,
         "explanation": "Các chi tiết không chuyển động tương đối với nhau và không tháo ra được mà không phá mối lắp: cố định, không tháo được (như hàn, ép, dán)."},
        {"type": MC,
         "question": "Trong chuỗi kích thước lắp ráp, khâu khép kín là:",
         "options": ["Khâu có kích thước nhỏ nhất", "Khâu có dung sai nhỏ nhất",
                     "Khâu hình thành sau cùng khi lắp, không gia công trực tiếp", "Khâu được chọn để cạo sửa"],
         "answer": 2,
         "explanation": "Khâu khép kín (ví dụ khe hở dọc trục) là kết quả của các khâu thành phần, chỉ có khi lắp xong."},
        {"type": MC,
         "question": "Khâu tăng là khâu mà khi nó tăng (các khâu khác giữ nguyên) thì:",
         "options": ["Khâu khép kín tăng", "Khâu khép kín giảm", "Khâu khép kín không đổi", "Các khâu khác tăng theo"],
         "answer": 0,
         "explanation": "Định nghĩa khâu tăng: tăng nó thì khâu khép kín tăng; khâu giảm thì ngược lại."},
        {"type": MC,
         "question": "Lỗ thân dài 50 (+0,08; 0) mm, bạc nằm trong lỗ dài 49,9 (0; −0,04) mm. Khe hở dọc trục lớn nhất là:",
         "options": ["0,10 mm", "0,14 mm", "0,18 mm", "0,22 mm"],
         "answer": 3,
         "explanation": "Lỗ lớn nhất trừ bạc nhỏ nhất: 50,08 − 49,86 = 0,22 mm. Khe hở nhỏ nhất 50,00 − 49,90 = 0,10 mm."},
        {"type": MC,
         "question": "Chuỗi lắp ráp có 6 khâu (kể cả khâu khép kín), dung sai khâu khép kín 0,15 mm. Lắp lẫn hoàn toàn, dung sai trung bình mỗi khâu thành phần là:",
         "options": ["0,025 mm", "0,03 mm", "0,15 mm", "0,9 mm"],
         "answer": 1,
         "explanation": "T_ct = T_Δ/(n − 1) = 0,15/5 = 0,03 mm. Chia cho 6 (0,025) là tính nhầm cả khâu khép kín."},
        {"type": MC,
         "question": "Lắp chọn theo nhóm, chia dung sai chế tạo thành 4 nhóm thì dung sai lắp ghép của mỗi nhóm:",
         "options": ["Không đổi", "Nhỏ đi 2 lần", "Nhỏ đi 4 lần", "Lớn lên 4 lần"],
         "answer": 2,
         "explanation": "Chia n nhóm thì dung sai lắp ghép mỗi nhóm nhỏ đi n lần."},
        {"type": MC,
         "question": "Điểm khác cơ bản giữa lắp điều chỉnh và lắp sửa là:",
         "options": ["Lắp điều chỉnh không cần khâu bồi thường",
                     "Lắp điều chỉnh chỉ dùng cho hàng khối", "Lắp sửa không cần mở rộng dung sai",
                     "Lắp điều chỉnh đổi vị trí hoặc thay khâu bồi thường (vòng đệm, bạc chặn) thay vì cạo bớt kim loại"],
         "answer": 3,
         "explanation": "Cả hai đều dùng khâu bồi thường; lắp sửa lấy bớt kim loại, lắp điều chỉnh đổi vị trí hoặc kích thước khâu bồi thường."},
        {"type": MC,
         "question": "Điều kiện bắt buộc với chi tiết khi lắp ráp theo dây chuyền là:",
         "options": ["Chi tiết phải lắp lẫn hoàn toàn, không sửa, không chỉnh tại chỗ",
                     "Chi tiết phải được chọn lắp từng chiếc", "Mỗi vị trí do một thợ vạn năng lắp trọn sản phẩm",
                     "Sản phẩm đứng yên tại một chỗ"],
         "answer": 0,
         "explanation": "Dây chuyền chạy theo nhịp nên phải loại trừ điều chỉnh, sửa chữa tại các vị trí lắp: chi tiết lắp lẫn hoàn toàn."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Công nghệ chế tạo máy 2", "lesson_title": "Bài 19. Công nghệ lắp ráp (phần 1)"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Mối lắp · tổ chức lắp · chuỗi kích thước · lắp lẫn, chọn, sửa, điều chỉnh",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự lý thuyết,", len(exam["questions"]), "câu")
