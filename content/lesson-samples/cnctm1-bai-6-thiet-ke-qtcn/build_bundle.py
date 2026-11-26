#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho CNCTM 1 – Bài 6.
Dùng: python3 build_figs.py && python3 build_bundle.py  rồi
      npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
Nguồn ý: giáo trình CNCTM của bộ môn (Chương 6). Bài toán chọn phôi trục bậc, bạc trượt, hộp số là ví dụ tự soạn.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Kiểm tra nhanh — Thiết kế quy trình công nghệ",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Trong các tài liệu ban đầu để thiết kế quy trình công nghệ, tài liệu nào không thể thiếu trong mọi trường hợp?",
         "options": ["Sổ tay định mức thời gian", "Bản vẽ phôi", "Bản vẽ chi tiết", "Catalog máy"],
         "answer": 2,
         "explanation": "Đơn chiếc có thể bỏ định mức, tra lượng dư thay bản vẽ phôi; bản vẽ chi tiết thì lúc nào cũng phải có."},
        {"type": MC,
         "question": "Chi tiết nặng 1,8 kg, phôi nặng 2,4 kg. Hệ số sử dụng vật liệu K bằng:",
         "options": ["0,60", "0,75", "1,33", "0,80"],
         "answer": 1,
         "explanation": "K = Mct / Mph = 1,8 / 2,4 = 0,75."},
        {"type": MC,
         "question": "Bước nào có tính chất quyết định chất lượng của quy trình công nghệ?",
         "options": ["Vạch thứ tự nguyên công", "Định cấp bậc thợ", "Viết phiếu công nghệ", "Chọn dụng cụ đo"],
         "answer": 0,
         "explanation": "Thứ tự nguyên công hợp lý vừa bảo đảm độ chính xác vừa nâng năng suất."},
        {"type": MC,
         "question": "Phát biểu nào đúng về chuẩn thô?",
         "options": ["Dùng cho mọi nguyên công để đỡ tốn công", "Dùng ở nguyên công cuối cùng",
                     "Chỉ dùng khi mài", "Chỉ dùng một lần ở nguyên công đầu tiên"],
         "answer": 3,
         "explanation": "Mặt phôi xù xì, gá lại mỗi lần tỳ một chỗ khác; các nguyên công sau phải dùng mặt đã gia công làm chuẩn."},
        {"type": MC,
         "question": "Phân tán nguyên công thích hợp với:",
         "options": ["Sản xuất đơn chiếc trên máy vạn năng", "Sản xuất hàng loạt, dây chuyền với máy chuyên dùng",
                     "Xưởng sửa chữa", "Mọi trường hợp như nhau"],
         "answer": 1,
         "explanation": "Mỗi máy một vài bước, chỉnh sẵn, thợ chuyên một việc → năng suất cao khi sản lượng lớn."},
        {"type": MC,
         "question": "Gá ba chi tiết trên bàn máy phay, dao cắt cả ba đồng thời và xong cùng lúc. Đó là cách gá:",
         "options": ["Tuần tự", "Song song – tuần tự", "Song song", "Phân tán"],
         "answer": 2,
         "explanation": "Song song: các chi tiết gia công đồng thời và hoàn thành cùng một lúc."},
        {"type": MC,
         "question": "Phiếu nào ghi khái quát theo từng nguyên công, không ghi các bước cụ thể?",
         "options": ["Biểu 1 – tiến trình công nghệ", "Biểu 2 – quy trình công nghệ",
                     "Biểu 3 – chỉ dẫn nguyên công", "Biểu 4 – bảng kê dụng cụ"],
         "answer": 0,
         "explanation": "Biểu 1 đơn giản, chỉ ghi theo nguyên công; Biểu 2 ghi tỉ mỉ từng bước; Biểu 3 mỗi nguyên công một tờ có sơ đồ."},
        {"type": MC,
         "question": "Sơ đồ nguyên công KHÔNG cần thể hiện nội dung nào?",
         "options": ["Ký hiệu định vị, kẹp chặt", "Dao và vị trí của dao", "Kích thước cần đạt ở nguyên công đó",
                     "Giá thành của cả chi tiết"],
         "answer": 3,
         "explanation": "Sơ đồ nguyên công gồm hình chiếu rõ nhất, định vị – kẹp chặt, dao và vị trí, kích thước cần đạt."},
    ],
}


bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Công nghệ chế tạo máy 1", "lesson_title": "Bài 6. Thiết kế quy trình công nghệ"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Yêu cầu QTCN · tài liệu ban đầu · 12 bước · hệ số K · tập trung, phân tán · phiếu và sơ đồ nguyên công",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự lý thuyết,", len(exam["questions"]), "câu")
