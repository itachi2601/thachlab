#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho CNCTM 1 – Bài 13 (Gia công mặt định hình).
Dùng: python3 build_figs.py && python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
Nguồn ý: giáo trình CNCTM của bộ môn (Chương 13). Bài toán mẫu, số liệu côn là ví dụ tự soạn.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Kiểm tra nhanh — Gia công mặt định hình",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Mặt cam đĩa thuộc loại mặt định hình nào?",
         "options": ["Mặt côn", "Mặt tròn xoay", "Mặt định hình đường thẳng", "Mặt định hình khối"],
         "answer": 2,
         "explanation": "Mặt định hình đường thẳng do một đường thẳng tịnh tiến trên một đường cong tạo nên, như cam đĩa, cam trống."},
        {"type": MC,
         "question": "Hai nguyên tắc gia công mặt định hình là:",
         "options": ["Tiện và phay", "Dùng dao định hình; điều khiển quỹ đạo dao",
                     "Gia công thô và gia công tinh", "Định hình và nhiệt luyện"],
         "answer": 1,
         "explanation": "Hoặc lưỡi dao có hình dạng giống mặt gia công, hoặc mũi dao đi theo quỹ đạo vạch ra mặt đó."},
        {"type": MC,
         "question": "Tiện côn bằng dao lưỡi rộng chỉ làm được mặt côn dài không quá:",
         "options": ["5 mm", "20 mm", "60 mm", "100 mm"],
         "answer": 1,
         "explanation": "Dao lưỡi rộng năng suất rất cao nhưng chỉ cho mặt côn dài đến 20 mm."},
        {"type": MC,
         "question": "Tiện côn góc 40° bằng cách quay con trượt trên, phải quay con trượt một góc:",
         "options": ["10°", "20°", "40°", "80°"],
         "answer": 1,
         "explanation": "Quay con trượt trên bằng nửa góc côn: 40° / 2 = 20°."},
        {"type": MC,
         "question": "Chi tiết dài L = 300 mm, đoạn côn l = 150 mm, D = 40 mm, d = 36 mm. Độ lệch ụ động h là:",
         "options": ["2 mm", "4 mm", "8 mm", "1 mm"],
         "answer": 1,
         "explanation": "h = L(D − d)/(2l) = 300 × 4 / 300 = 4 mm."},
        {"type": MC,
         "question": "Tiện côn bằng thước côn hiệu quả nhất với góc côn:",
         "options": ["Bất kỳ", "Từ 10 ÷ 12° trở xuống", "Từ 30° trở lên", "Chỉ đúng 60°"],
         "answer": 1,
         "explanation": "Thước côn dùng cho góc từ 10 ÷ 12° trở xuống, hiệu quả và năng suất nhất."},
        {"type": MC,
         "question": "Mặt côn đã tôi, góc côn 4°, cần chính xác cao. Gia công tinh bằng:",
         "options": ["Tiện bằng dao lưỡi rộng", "Mài tiến dọc, quay bàn máy mài",
                     "Phay chép hình", "Quay con trượt trên"],
         "answer": 1,
         "explanation": "Côn tôi cứng, chính xác cao thì mài; góc côn không quá 7° mài tiến dọc, quay bàn."},
        {"type": MC,
         "question": "Nhược điểm của dao định hình khi tiện mặt tròn xoay là:",
         "options": ["Mài lại thì prôfin thay đổi", "Quãng chạy dao rất dài",
                     "Giá chế tạo đắt, sản lượng phải nhiều mới kinh tế", "Chỉ dùng cho đơn chiếc"],
         "answer": 2,
         "explanation": "Dao định hình mài lại prôfin không đổi, tiến ngang nên quãng chạy dao ngắn; nhưng dao đắt, cần sản lượng lớn."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Công nghệ chế tạo máy 1", "lesson_title": "Bài 13. Gia công mặt định hình"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Bốn loại mặt · tiện côn · lệch ụ động, thước côn · mài côn · dao định hình, chép hình",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự lý thuyết,", len(exam["questions"]), "câu")

