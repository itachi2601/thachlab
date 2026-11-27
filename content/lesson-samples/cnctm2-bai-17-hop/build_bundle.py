#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho CNCTM 2 – Bài 17 (Công nghệ gia công chi tiết dạng hộp).
Dùng: python3 build_figs.py && python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
Nguồn ý: giáo trình CNCTM 2 của bộ môn (Chương 17). Số liệu bài toán mẫu là ví dụ tự soạn.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Kiểm tra nhanh — Gia công chi tiết dạng hộp",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Hộp giảm tốc hai nửa (thân và nắp ghép, lỗ ổ nằm ở mặt ghép) thuộc loại:",
         "options": ["Hộp rời", "Hộp liền", "Không phải chi tiết dạng hộp", "Chi tiết dạng càng"],
         "answer": 0,
         "explanation": "Hộp rời có hệ lỗ chủ yếu nằm ở hai nửa thân hộp, như hộp giảm tốc hai nửa, gối đỡ hai nửa."},
        {"type": MC,
         "question": "Theo giáo trình, dung sai độ đồng tâm của các lỗ trong hộp bằng:",
         "options": ["Dung sai đường kính lỗ lớn nhất",
                     "1/2 dung sai đường kính lỗ nhỏ nhất",
                     "Dung sai khoảng cách tâm",
                     "0,5 ÷ 0,7 dung sai đường kính lỗ"],
         "answer": 1,
         "explanation": "Đồng tâm bằng 1/2 dung sai đường kính lỗ nhỏ nhất; 0,5 ÷ 0,7 dung sai đường kính là sai số hình dạng lỗ."},
        {"type": MC,
         "question": "Phôi hộp đúc phải được khử ứng suất dư trước khi cắt gọt vì:",
         "options": ["Gang đúc quá cứng, khó cắt",
                     "Để giảm lượng dư gia công",
                     "Hộp đúc nguội không đều, có ứng suất dư gây biến dạng",
                     "Để tăng độ cứng bề mặt lỗ"],
         "answer": 2,
         "explanation": "Hộp đúc nguội không đều gây biến dạng nhiệt và ứng suất dư; không khử thì hộp biến dạng sau gia công."},
        {"type": MC,
         "question": "Hộp cỡ vừa và nhỏ, sản xuất loạt lớn, thường dùng chuẩn tinh thống nhất là:",
         "options": ["Ba mặt phẳng", "Dấu vạch trên phôi", "Hai mặt đầu của lỗ chính", "Một mặt phẳng và hai lỗ"],
         "answer": 3,
         "explanation": "Một mặt phẳng + hai lỗ dùng cho hộp vừa và nhỏ; ba mặt phẳng dùng cho hộp lớn; vạch dấu cho đơn chiếc, sửa chữa."},
        {"type": MC,
         "question": "Hai lỗ chuẩn trên mặt phẳng chuẩn của hộp nên bố trí:",
         "options": ["Sát nhau ở giữa mặt", "Trùng với hai lỗ ổ trục",
                     "Chéo góc, ở vị trí xa nhau nhất", "Ở mặt bên, vuông góc mặt chuẩn"],
         "answer": 2,
         "explanation": "Hai lỗ chuẩn đặt chéo góc, xa nhất, gia công chính xác; chúng chỉ có mục đích công nghệ."},
        {"type": MC,
         "question": "Nguyên công nào làm SAU CÙNG trước khi tổng kiểm tra chi tiết hộp?",
         "options": ["Gia công mặt phẳng chuẩn", "Gia công các lỗ kẹp chặt",
                     "Gia công thô các lỗ lắp ghép", "Gia công chính xác các lỗ lắp ghép"],
         "answer": 3,
         "explanation": "Thứ tự: mặt chuẩn, lỗ chuẩn → mặt còn lại → lỗ lắp ghép thô, bán tinh → lỗ kẹp chặt → lỗ lắp ghép chính xác → tổng kiểm tra."},
        {"type": MC,
         "question": "Doa lỗ dài trên máy doa ngang, trục doa cần được dẫn hướng:",
         "options": ["Chỉ phía trước", "Cả phía trước và phía sau", "Chỉ phía sau", "Không cần dẫn hướng"],
         "answer": 1,
         "explanation": "Lỗ ngắn dẫn hướng phía trước hoặc phía sau; lỗ dài cần dẫn hướng cả trước và sau."},
        {"type": MC,
         "question": "Đút trục kiểm Ø50 và Ø40 vừa khít vào hai lỗ, đo kích thước ngoài hai trục được M = 145,00 mm. Khoảng cách tâm hai lỗ là:",
         "options": ["100,00 mm", "95,00 mm", "120,00 mm", "145,00 mm"],
         "answer": 0,
         "explanation": "A = M − (d₁ + d₂)/2 = 145 − 45 = 100 mm."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Công nghệ chế tạo máy 2", "lesson_title": "Bài 17. Công nghệ gia công chi tiết dạng hộp"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Hộp liền, hộp rời · yêu cầu hệ lỗ · phôi đúc · chuẩn mặt phẳng + hai lỗ · thứ tự nguyên công · kiểm tra",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự lý thuyết,", len(exam["questions"]), "câu")
