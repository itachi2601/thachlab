#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho CNCTM 1 – Bài 3.
Dùng: python3 build_figs.py && python3 build_bundle.py
      rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts <bundle.json>
Nguồn ý: giáo trình CNCTM của bộ môn (Chương 3). Ví dụ thanh truyền, ống lót, khối D 100×100×280, trục Ø45→Ø40 là ví dụ tự soạn.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Kiểm tra nhanh — Phôi và lượng dư",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Chi tiết bằng gang xám nên dùng loại phôi nào?",
         "options": ["Phôi cán", "Phôi rèn tự do", "Phôi đúc", "Phôi rèn khuôn"],
         "answer": 2,
         "explanation": "Gang xám giòn, không rèn hay cán được → chỉ làm phôi bằng đúc."},
        {"type": MC,
         "question": "So với phôi cán, phôi rèn có ưu điểm chính là:",
         "options": ["Hạt kim loại nhỏ mịn, cơ tính tốt, hình dáng gần chi tiết hơn",
                     "Chiều dài không hạn chế", "Không cần nung nóng", "Luôn rẻ hơn"],
         "answer": 0,
         "explanation": "Biến dạng dẻo làm hạt mịn, bền chặt; rèn cho hình dáng gần chi tiết nên lượng dư nhỏ hơn."},
        {"type": MC,
         "question": "Rèn khuôn hở khác rèn khuôn kín ở chỗ:",
         "options": ["Không cần nung phôi", "Có vành biên quanh mặt phân khuôn, phải cắt bỏ",
                     "Phôi ban đầu phải đúng thể tích", "Lực rèn lớn hơn nhiều, dễ hỏng khuôn"],
         "answer": 1,
         "explanation": "Khuôn hở để kim loại thừa tràn ra thành vành biên nên phôi không cần đúng thể tích; khuôn kín thì ngược lại."},
        {"type": MC,
         "question": "Ống, xi lanh, sơ mi bằng gang, sản xuất loạt lớn, thường đúc bằng:",
         "options": ["Khuôn cát, làm khuôn bằng tay", "Đúc áp lực buồng nóng", "Đúc mẫu chảy", "Đúc ly tâm"],
         "answer": 3,
         "explanation": "Lực ly tâm ép kim loại ra thành khuôn, tạo vật rỗng không cần lõi, tổ chức mịn chặt."},
        {"type": MC,
         "question": "Chi tiết nặng 2,4 kg làm từ phôi nặng 4 kg. Nhận xét nào đúng?",
         "options": ["K = 0,6 < 0,7 → nên xem lại cách làm phôi", "K = 1,67 → phôi tốt",
                     "K = 0,6 → phôi đạt yêu cầu", "K = 0,4 → phôi đạt yêu cầu"],
         "answer": 0,
         "explanation": "K = Mct/Mph = 2,4/4 = 0,6, nhỏ hơn 0,7 nên cần xem lại phương pháp chế tạo phôi."},
        {"type": MC,
         "question": "Trục tiện từ Ø36 xuống Ø33. Lượng dư mỗi phía của bước này là:",
         "options": ["3 mm", "1,5 mm", "6 mm", "0,75 mm"],
         "answer": 1,
         "explanation": "Trục: 2Z = d1 − d2 = 36 − 33 = 3 mm → Z = 1,5 mm."},
        {"type": MC,
         "question": "Lượng dư tổng cộng Z₀ bằng:",
         "options": ["Lượng dư của bước tinh cuối cùng", "Lượng dư của bước thô đầu tiên",
                     "Hiệu kích thước hai bước liền nhau", "Tổng các lượng dư trung gian"],
         "answer": 3,
         "explanation": "Z₀ = ΣZi, cũng bằng khoảng cách từ mặt phôi tới mặt chi tiết."},
        {"type": MC,
         "question": "Gia công phá trong chuẩn bị phôi nhằm:",
         "options": ["Đạt độ nhám thấp ngay từ đầu", "Khoan lỗ tâm hai đầu trục",
                     "Bóc lớp vỏ rỗ, dính cát, biến cứng của phôi", "Nắn thẳng phôi thanh bị cong"],
         "answer": 2,
         "explanation": "Gia công phá bóc vỏ xấu; máy cần công suất lớn, cứng vững, không cần chính xác."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Công nghệ chế tạo máy 1", "lesson_title": "Bài 3. Phôi và lượng dư gia công"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Phôi cán · rèn · đúc · chọn phôi · lượng dư trung gian, tổng cộng · chuẩn bị phôi",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự lý thuyết,", len(exam["questions"]), "câu")
