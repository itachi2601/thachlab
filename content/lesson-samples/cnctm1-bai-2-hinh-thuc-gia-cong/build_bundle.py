#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho CNCTM 1 – Bài 2.
Dùng: python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
Nguồn ý: giáo trình CNCTM của bộ môn (Chương 2). Ví dụ bu lông, chốt C45, bánh răng 20Cr là ví dụ tự soạn.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Kiểm tra nhanh — Các hình thức gia công cơ khí",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Gia công tinh khác gia công thô chủ yếu ở chỗ:",
         "options": ["Dùng máy khác loại", "Lấy đi lớp kim loại mỏng để hình dáng, kích thước giống bản vẽ",
                     "Lấy đi phần lớn lượng dư", "Không tạo ra phoi"],
         "answer": 1,
         "explanation": "Thô lấy phần lớn lượng dư cho gần giống; tinh lấy lớp mỏng cho giống với yêu cầu, đạt cấp 7–6."},
        {"type": MC,
         "question": "Bề mặt nào nhẵn nhất?",
         "options": ["Ra 20 µm", "Ra 6,3 µm", "Ra 1,25 µm", "Ra 0,32 µm"],
         "answer": 3,
         "explanation": "Ra là độ nhám: giá trị càng nhỏ, bề mặt càng nhẵn."},
        {"type": MC,
         "question": "Cán ren, cán lăn, nong lỗ dựa trên hiện tượng:",
         "options": ["Biến dạng dẻo của kim loại", "Nóng chảy cục bộ do tia lửa điện",
                     "Khuếch tán nguyên tố vào lớp mặt", "Cắt đứt lớp kim loại thành phoi"],
         "answer": 0,
         "explanation": "Gia công không phoi dùng biến dạng dẻo, tạo lớp biến cứng chịu mòn trên bề mặt."},
        {"type": MC,
         "question": "Ủ, thường hoá và tôi khác nhau chủ yếu ở:",
         "options": ["Giai đoạn nung nóng", "Thời gian giữ nhiệt", "Tốc độ làm nguội", "Loại lò dùng để nung"],
         "answer": 2,
         "explanation": "Ủ nguội cùng lò, thường hoá nguội trong không khí, tôi nguội nhanh trong nước/dầu."},
        {"type": MC,
         "question": "Trong quy trình gia công trục có tôi, nguyên công tôi thường đặt:",
         "options": ["Trước tiện thô", "Giữa tiện thô và tiện tinh", "Sau gia công tinh, trước mài", "Sau mài tinh"],
         "answer": 2,
         "explanation": "Cắt gọt khi thép còn mềm; tôi xong có thể biến dạng nên mài sau cùng để sửa và đạt chính xác."},
        {"type": MC,
         "question": "Thép C45 (0,45 %C) cần tôi. Nhiệt độ tôi được chọn theo:",
         "options": ["A1 + (30 ÷ 50) °C", "A3 + (30 ÷ 50) °C", "Acm + (20 ÷ 30) °C", "150 ÷ 200 °C"],
         "answer": 1,
         "explanation": "Thép ≤ 0,8 %C tôi ở A3 + (30 ÷ 50) °C; thép > 0,8 %C mới dùng A1."},
        {"type": MC,
         "question": "Bánh răng thép 20Cr (0,2 %C) cần mặt răng cứng 58 HRC, lõi dẻo. Chọn:",
         "options": ["Tôi trực tiếp rồi ram cao", "Thấm cacbon, rồi tôi và ram thấp",
                     "Ủ hoàn toàn", "Thường hoá"],
         "answer": 1,
         "explanation": "Thép ít cacbon tôi không đủ cứng; thấm C cho lớp mặt rồi tôi + ram, lõi vẫn dẻo."},
        {"type": MC,
         "question": "Đặc điểm nào là của gia công phi truyền thống?",
         "options": ["Dụng cụ phải cứng hơn chi tiết", "Chỉ gia công được vật liệu mềm",
                     "Dụng cụ không cần cứng hơn chi tiết, làm được hình phức tạp, siêu nhỏ",
                     "Luôn tạo ra phoi dây dài"],
         "answer": 2,
         "explanation": "Dùng năng lượng cơ, nhiệt, hoá thay lưỡi cắt nên gia công được thép đã tôi, hợp kim cứng."},
    ],
}


bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Công nghệ chế tạo máy 1", "lesson_title": "Bài 2. Các hình thức gia công cơ khí"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Gia công có phoi · không phoi · nhiệt luyện, hoá nhiệt luyện · gia công phi truyền thống",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự lý thuyết,", len(exam["questions"]), "câu")

