#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho CNCTM 2 – Bài 15 (Công nghệ gia công chi tiết dạng càng).
Dùng: python3 build_figs.py && python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
Nguồn ý: giáo trình CNCTM 2 của bộ môn (Chương 15). Bài toán mẫu và các số ví dụ là tự soạn.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Kiểm tra nhanh — Gia công chi tiết dạng càng",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Đặc điểm chính của chi tiết dạng càng là:",
         "options": ["Có một hay vài lỗ cơ bản, tâm song song hoặc tạo với nhau một góc",
                     "Là chi tiết tròn xoay dài, tỉ số chiều dài trên đường kính lớn",
                     "Là chi tiết hình hộp có nhiều vách và lỗ",
                     "Là chi tiết có vành răng ăn khớp"],
         "answer": 0,
         "explanation": "Càng có một hay vài lỗ cơ bản cần gia công chính xác, tâm song song hoặc lệch một góc."},
        {"type": MC,
         "question": "Theo giáo trình, dung sai độ vuông góc của tâm lỗ cơ bản so với mặt đầu thường trong khoảng:",
         "options": ["0,005 ÷ 0,01 mm trên 100 mm bán kính", "0,05 ÷ 0,1 mm trên 100 mm bán kính",
                     "0,5 ÷ 1 mm trên 100 mm bán kính", "0,05 ÷ 0,1 mm trên 100 mm chiều dài lỗ"],
         "answer": 1,
         "explanation": "Vuông góc tâm lỗ – mặt đầu: 0,05 ÷ 0,1 mm trên 100 mm bán kính."},
        {"type": MC,
         "question": "Càng làm việc với tải trọng không lớn, có thể chọn vật liệu:",
         "options": ["Thép hợp kim nhiệt luyện", "Gang xám", "Thép dụng cụ", "Hợp kim titan"],
         "answer": 1,
         "explanation": "Tải nhỏ dùng gang xám; tải lớn mới cần thép nhiệt luyện được."},
        {"type": MC,
         "question": "Chuẩn tinh thống nhất thường dùng khi gia công các mặt còn lại của càng là:",
         "options": ["Vành ngoài hai đầu càng", "Hai mặt bên của thân càng",
                     "Mặt đầu và hai lỗ cơ bản", "Mặt đầu và lỗ ren"],
         "answer": 2,
         "explanation": "Mặt đầu tì phiến tì (3 bậc), một lỗ lắp chốt trụ ngắn (2 bậc), lỗ kia lắp chốt trám (1 bậc)."},
        {"type": MC,
         "question": "Trong đường lối công nghệ chung của càng, nguyên công đầu tiên là:",
         "options": ["Gia công lỗ cơ bản", "Gia công lỗ ren, lỗ dầu", "Cân bằng trọng lượng", "Gia công mặt đầu"],
         "answer": 3,
         "explanation": "Mặt đầu làm chuẩn cho các nguyên công sau, nên gia công trước lỗ cơ bản."},
        {"type": MC,
         "question": "Sản xuất hàng loạt vừa và nhỏ, mặt đầu càng thường được gia công bằng:",
         "options": ["Phay hoặc tiện", "Chuốt", "Mài khôn", "Bào"],
         "answer": 0,
         "explanation": "Loạt vừa và nhỏ: phay hoặc tiện. Loạt lớn, phôi chính xác: mài hoặc chuốt. Bào ít dùng vì năng suất thấp."},
        {"type": MC,
         "question": "Gia công tất cả các lỗ cơ bản sau một lần gá (phương án 2), khối V ngắn di động khống chế:",
         "options": ["3 bậc tự do", "2 bậc tự do", "1 bậc tự do", "Không bậc nào, chỉ để kẹp"],
         "answer": 2,
         "explanation": "Mặt đầu 3 bậc, khối V ngắn cố định 2 bậc, khối V ngắn di động 1 bậc: đủ 6 bậc."},
        {"type": MC,
         "question": "Đồng hồ so tì mặt đầu cách tâm 40 mm, quay trục tâm một vòng kim lệch 0,03 mm. Độ không vuông góc quy ra trên 100 mm bán kính là:",
         "options": ["0,012 mm", "0,03 mm", "0,12 mm", "0,075 mm"],
         "answer": 3,
         "explanation": "0,03 × 100 / 40 = 0,075 mm trên 100 mm bán kính."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Công nghệ chế tạo máy 2", "lesson_title": "Bài 15. Công nghệ gia công chi tiết dạng càng"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Lỗ cơ bản · phôi · chuẩn mặt đầu + hai lỗ · thứ tự nguyên công · kiểm khoảng cách tâm, song song",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự lý thuyết,", len(exam["questions"]), "câu")
