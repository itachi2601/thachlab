#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho CNCTM 1 – Bài 8 Gia công mặt ngoài tròn xoay.
Dùng: python3 build_figs.py && python3 build_bundle.py  rồi
      npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
Nguồn ý: giáo trình CNCTM của bộ môn (Chương 8). Ví dụ trục Ø20 phình giữa, cổ trục C45, chốt Ø10 là ví dụ tự soạn.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Kiểm tra nhanh — Gia công mặt ngoài tròn xoay",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Khi tiện trụ ngoài, chuyển động chính và chuyển động chạy dao là gì?",
         "options": ["Dao quay; phôi tịnh tiến dọc", "Phôi tịnh tiến; dao quay",
                     "Phôi quay; dao tịnh tiến dọc trục", "Dao và phôi cùng quay"],
         "answer": 2,
         "explanation": "Tiện: phôi quay là chuyển động chính; bàn xe dao mang dao chạy dọc trục là chạy dao."},
        {"type": MC,
         "question": "Trục thép Ø20 dài 500 mm chống tâm hai đầu, tiện xong giữa trục to hơn hai đầu. Cách khắc phục phù hợp nhất?",
         "options": ["Thêm luynét đỡ giữa trục", "Tăng tốc độ cắt",
                     "Đổi sang mâm cặp 3 chấu, bỏ mũi tâm", "Tăng lượng chạy dao"],
         "answer": 0,
         "explanation": "Trục dài, mảnh võng dưới lực cắt nên giữa bị cắt ít. Luynét đỡ giữa trục làm trục cứng vững."},
        {"type": MC,
         "question": "Phôi đúc hình hộp có một mặt trụ cần tiện đồng tâm cao với lỗ sẵn có. Nên gá bằng gì?",
         "options": ["Mâm cặp 3 chấu tự định tâm", "Ống kẹp đàn hồi",
                     "Hai mũi tâm và tốc kẹp", "Mâm cặp 4 chấu, rà bằng đồng hồ so"],
         "answer": 3,
         "explanation": "Bốn chấu chỉnh riêng từng chấu nên kẹp được phôi không tròn và rà được tâm."},
        {"type": MC,
         "question": "So với cắt từng lớp, cắt từng đoạn khi tiện trục bậc có đặc điểm gì?",
         "options": ["Lực cắt nhỏ hơn, chính xác hơn", "Năng suất cao hơn nhưng lực cắt lớn, kém cứng vững",
                     "Không dùng được trên máy tiện thường", "Chỉ dùng cho tiện tinh"],
         "answer": 1,
         "explanation": "Cắt từng đoạn ăn sâu, xong từng bậc nên nhanh, nhưng lực cắt lớn."},
        {"type": MC,
         "question": "Vì sao phải sửa lỗ tâm trước khi mài tinh một trục đã tôi?",
         "options": ["Để trục nhẹ hơn", "Vì lỗ tâm là chuẩn định vị khi mài có tâm, bị hỏng khi nhiệt luyện",
                     "Vì mài vô tâm cần lỗ tâm", "Để đá mài ít mòn"],
         "answer": 1,
         "explanation": "Mài có tâm định vị bằng hai lỗ tâm; lỗ tâm bị ô xi hoá, cháy khi tôi nên phải sửa lại."},
        {"type": MC,
         "question": "Khi mài vô tâm, chi tiết được định vị bằng gì?",
         "options": ["Hai lỗ tâm", "Mâm cặp 3 chấu", "Mặt đầu tì vào ụ động", "Chính mặt trụ đang được mài"],
         "answer": 3,
         "explanation": "Chi tiết tựa lên thanh đỡ và đá dẫn bằng chính mặt trụ đang mài; không dùng lỗ tâm."},
        {"type": MC,
         "question": "Đánh bóng một trục đang bị côn 0,03 mm thì kết quả là gì?",
         "options": ["Mặt nhẵn hơn nhưng vẫn côn", "Hết côn, nhẵn hơn",
                     "Hết côn, độ nhám không đổi", "Trục nhỏ đi khoảng 0,03 mm"],
         "answer": 0,
         "explanation": "Đánh bóng chỉ bóc lớp khoảng 5 µm, không sửa được hình dáng; muốn hết côn phải mài lại."},
        {"type": MC,
         "question": "Cổ trục thép đã tôi cần cấp 6, Ra 0,15 µm. Bước gia công cuối phù hợp là gì?",
         "options": ["Tiện tinh mỏng", "Mài tinh", "Mài tinh mỏng", "Đánh bóng"],
         "answer": 2,
         "explanation": "Mài tinh mỏng đạt cấp 7–6, Ra 0,2–0,1; 0,15 nằm trong khoảng này. Thép đã tôi khó tiện."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Công nghệ chế tạo máy 1", "lesson_title": "Bài 8. Gia công mặt ngoài tròn xoay"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Tiện trụ ngoài · gá phôi · mài có tâm, vô tâm · gia công tinh nhẵn · trình tự gia công",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự lý thuyết,", len(exam["questions"]), "câu")
