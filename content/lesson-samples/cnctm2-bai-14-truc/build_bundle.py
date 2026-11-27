#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho CNCTM 2 – Bài 14 (Công nghệ gia công chi tiết dạng trục).
Dùng: python3 build_figs.py && python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
Nguồn ý: giáo trình CNCTM 2 của bộ môn (Chương 14). Bài toán mẫu và số liệu đồng hồ so là ví dụ tự soạn.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Kiểm tra nhanh — Công nghệ gia công chi tiết dạng trục",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Trục trơn Ø40 mm, dài 120 mm thuộc loại nào?",
         "options": ["Trục trơn ngắn", "Trục trơn thường", "Trục trơn dài", "Trục bậc"],
         "answer": 0,
         "explanation": "L/d = 120/40 = 3 < 4 nên là trục trơn ngắn."},
        {"type": MC,
         "question": "Chuẩn tinh thống nhất khi gia công chi tiết dạng trục là:",
         "options": ["Mặt trụ ngoài lớn nhất", "Một mặt đầu và một cổ trục", "Hai lỗ tâm", "Rãnh then"],
         "answer": 2,
         "explanation": "Hai lỗ tâm dùng được cho hầu hết nguyên công thô, bán tinh, tinh, giữ các cổ trục đồng tâm."},
        {"type": MC,
         "question": "Gá trục trên hai mũi tâm, mũi tâm trái là mũi cứng, dao điều chỉnh sẵn. Sai số chuẩn xuất hiện ở kích thước nào?",
         "options": ["Đường kính các cổ trục", "Chiều dài các bậc tính từ mặt đầu",
                     "Cả đường kính lẫn chiều dài", "Không có sai số chuẩn nào"],
         "answer": 1,
         "explanation": "Chuẩn định vị trùng chuẩn đo cho đường kính; nhưng lỗ tâm nông sâu khác nhau làm chiều dài bậc thay đổi."},
        {"type": MC,
         "question": "Tiện trục trên hai mũi tâm ở 1000 vòng/phút. Mũi tâm sau nên là:",
         "options": ["Mũi tâm cố định", "Mũi tâm có khía nhám", "Mũi tâm tuỳ động có lò xo", "Mũi tâm quay"],
         "answer": 3,
         "explanation": "Trên 500 vòng/phút mũi tâm cố định bị cháy, phải dùng mũi tâm quay. Mũi tâm tuỳ động chỉ giải quyết sai số chiều dài, không giải quyết nhiệt."},
        {"type": MC,
         "question": "Làm một trục bậc thay thế (đơn chiếc), bậc chênh đường kính lớn. Phôi hợp lý là:",
         "options": ["Dập nóng trên máy dập", "Đúc trong khuôn kim loại", "Rèn tự do", "Chồn trên máy chồn ngang"],
         "answer": 2,
         "explanation": "Đơn chiếc, loạt nhỏ: rèn tự do (khuôn đơn giản, máy búa); dập, chồn, đúc khuôn chỉ kinh tế khi sản lượng lớn."},
        {"type": MC,
         "question": "Sau nhiệt luyện, trước khi mài tinh cổ trục trên hai mũi tâm cần:",
         "options": ["Phay rãnh then", "Sửa lỗ tâm", "Khoan lại lỗ tâm mới", "Tiện tinh lại cổ trục"],
         "answer": 1,
         "explanation": "Lỗ tâm bị ôxy hoá, cháy khi nhiệt luyện; độ chính xác cổ trục mài phụ thuộc lỗ tâm."},
        {"type": MC,
         "question": "Theo quy tắc mốc 80 mm trong giáo trình, mài cổ trục dài 200 mm trên máy mài tròn ngoài dùng cách nào?",
         "options": ["Tiến ngang, đá rộng hơn cổ", "Mài vô tâm tiến ngang", "Đá định hình tiến ngang", "Tiến dọc"],
         "answer": 3,
         "explanation": "Đoạn dài hơn 80 mm (dài hơn bề rộng đá) phải mài tiến dọc."},
        {"type": MC,
         "question": "Quay trục một vòng trên hai mũi tâm, đồng hồ so chỉ lớn nhất +0,010 mm, nhỏ nhất −0,004 mm. Độ đảo hướng tâm là:",
         "options": ["0,014 mm", "0,006 mm", "0,010 mm", "0,007 mm"],
         "answer": 0,
         "explanation": "Độ đảo = 0,010 − (−0,004) = 0,014 mm."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Công nghệ chế tạo máy 2", "lesson_title": "Bài 14. Công nghệ gia công chi tiết dạng trục"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Phân loại L/d · yêu cầu kỹ thuật · phôi · hai lỗ tâm · Tâm – Tiện – Phay – Tôi – Mài · kiểm độ đảo",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự lý thuyết,", len(exam["questions"]), "câu")
