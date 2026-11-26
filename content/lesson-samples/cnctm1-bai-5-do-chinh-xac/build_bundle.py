#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho CNCTM 1 – Bài 5.
Dùng: python3 build_figs.py && python3 build_bundle.py  rồi
      npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
Nguồn ý: giáo trình CNCTM của bộ môn (Chương 5). Bài toán mòn dao, piston, ống mỏng là ví dụ tự soạn;
U0 = 12 µm/km (thép 45 – T15K6) là trị số tra bảng, ghi rõ "tra bảng" trong bài.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Kiểm tra nhanh — Độ chính xác gia công",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Độ đồng tâm giữa lỗ Ø22 và mặt ngoài Ø38 của bạc trượt thuộc yếu tố nào của độ chính xác gia công?",
         "options": ["Kích thước (Cỡ)", "Hình dáng (Dáng)", "Vị trí tương quan (Vị)", "Chất lượng bề mặt (Mặt)"],
         "answer": 2,
         "explanation": "Đồng tâm, song song, vuông góc là vị trí tương quan giữa các bề mặt."},
        {"type": MC,
         "question": "Tiện với lượng chạy dao S = 0,2 mm/vòng, bán kính mũi dao r = 1 mm. Chiều cao nhấp nhô Rz khoảng:",
         "options": ["0,5 µm", "5 µm", "25 µm", "50 µm"],
         "answer": 1,
         "explanation": "Rz ≈ S²/(8r) = 0,04/8 = 0,005 mm = 5 µm."},
        {"type": MC,
         "question": "Tiện thép cacbon, vùng tốc độ cắt nào cho mặt nhám nhất do lẹo dao?",
         "options": ["Khoảng 15 – 20 m/phút", "Khoảng 2 – 5 m/phút", "Khoảng 100 – 120 m/phút", "Khoảng 200 m/phút trở lên"],
         "answer": 0,
         "explanation": "Lẹo dao hình thành mạnh nhất quanh 15 – 20 m/phút; tăng tốc độ cắt vượt vùng này mặt nhẵn hơn."},
        {"type": MC,
         "question": "Phương pháp tự động đạt kích thước KHÁC cắt thử ở điểm nào?",
         "options": ["Chính xác nhờ tay nghề người thợ", "Mòn dao không ảnh hưởng tới kích thước",
                     "Dùng cho đơn chiếc, sửa chữa", "Dao được chỉnh sẵn một lần, năng suất cao"],
         "answer": 3,
         "explanation": "Tự động đạt kích thước chỉnh dao sẵn theo đồ gá, năng suất cao nhưng mòn dao có ảnh hưởng; ba ý còn lại là của cắt thử."},
        {"type": MC,
         "question": "Mũi dao tiện mòn theo phương hướng kính một lượng U. Đường kính chi tiết thay đổi thế nào?",
         "options": ["Tăng một lượng 2U", "Giảm một lượng U", "Tăng một lượng U/2", "Không đổi"],
         "answer": 0,
         "explanation": "Mũi dao lùi ra U thì bán kính tăng U, đường kính tăng 2U."},
        {"type": MC,
         "question": "Trục mảnh gá chống tâm hai đầu, tiện xong thường có dạng:",
         "options": ["Loa kèn, đầu phải to", "Côn đều", "Tang trống, giữa to", "Ô van"],
         "answer": 2,
         "explanation": "Chỗ võng nhiều nhất là giữa trục nên giữa bị cắt ít nhất, to nhất."},
        {"type": MC,
         "question": "Đồ gá dùng để gia công chi tiết phải có độ chính xác thế nào?",
         "options": ["Thấp hơn chi tiết một cấp", "Bằng chi tiết", "Cao hơn chi tiết ít nhất một cấp", "Không cần quan tâm"],
         "answer": 2,
         "explanation": "Sai số của đồ gá chép vào chi tiết, nên đồ gá phải chính xác hơn ít nhất một cấp."},
        {"type": MC,
         "question": "Loạt 100 trục, dung sai 50,00 – 50,30 mm; có 3 trục nằm trong khoảng 50,30 – 50,35 mm, còn lại trong dung sai. Nhận xét đúng:",
         "options": ["3 % phế phẩm không sửa được", "3 % phế phẩm sửa được vì còn dư kích thước",
                     "Không có phế phẩm", "97 % phế phẩm"],
         "answer": 1,
         "explanation": "Trục lớn hơn giới hạn trên còn dư vật liệu, tiện lại được; trục nhỏ hơn giới hạn dưới mới là phế phẩm không sửa được."},
    ],
}


bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Công nghệ chế tạo máy 1", "lesson_title": "Bài 5. Độ chính xác gia công"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Cỡ – Dáng – Vị – Mặt · độ nhám · cắt thử, chỉnh sẵn · sai số do máy, dao, biến dạng · đường cong phân bố",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự lý thuyết,", len(exam["questions"]), "câu")
