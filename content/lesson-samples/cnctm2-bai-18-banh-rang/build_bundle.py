#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho CNCTM 2 – Bài 18 (Công nghệ gia công chi tiết bánh răng).
Dùng: python3 build_figs.py && python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
Nguồn ý: giáo trình CNCTM 2 của bộ môn (Chương 18). Bài toán mẫu Z32 dựa theo ví dụ trong giáo trình, số liệu đã tính lại.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Kiểm tra nhanh — Công nghệ gia công chi tiết bánh răng",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Bánh răng trụ dạng đĩa (l/d < 1) khi cắt răng lấy mặt nào làm chuẩn chính?",
         "options": ["Mặt lỗ, khử 4 bậc tự do", "Mặt ngoài, khử 4 bậc tự do",
                     "Hai lỗ tâm", "Mặt đầu, khử 3 bậc tự do"],
         "answer": 3,
         "explanation": "l/d < 1 (loại III, IV): mặt đầu là chuẩn chính khử 3 bậc, mặt lỗ khử 2 bậc."},
        {"type": MC,
         "question": "Theo giáo trình, mặt lỗ bánh răng cần đạt cấp chính xác:",
         "options": ["Cấp 3, 4", "Cấp 6, 7", "Cấp 9, 10", "Cấp 11, 12"],
         "answer": 1,
         "explanation": "Mặt lỗ bánh răng và cổ trục của trục răng gia công đạt cấp chính xác 6, 7."},
        {"type": MC,
         "question": "Bánh răng thép Ø40 mm. Phôi thường dùng là:",
         "options": ["Thép cán", "Rèn tự do", "Rèn khuôn hở", "Gang đúc"],
         "answer": 0,
         "explanation": "Bánh răng đường kính nhỏ đến 60 mm chế tạo từ phôi thép cán."},
        {"type": MC,
         "question": "Vì sao lỗ và mặt đầu bánh răng nên gia công trong một lần gá?",
         "options": ["Để rút ngắn thời gian tôi", "Để cắt răng nhanh hơn",
                     "Để giữ độ vuông góc giữa mặt đầu và lỗ", "Để tiết kiệm phôi"],
         "answer": 2,
         "explanation": "Hai mặt làm cùng lần gá thì sai số gá không chen vào độ vuông góc giữa chúng."},
        {"type": MC,
         "question": "Ba giai đoạn gia công cơ của bánh răng theo đúng thứ tự là:",
         "options": ["Cắt răng → tạo chuẩn → tinh", "Tạo chuẩn → tinh → cắt răng",
                     "Tạo chuẩn → cắt răng → tinh sau nhiệt luyện", "Nhiệt luyện → tạo chuẩn → cắt răng"],
         "answer": 2,
         "explanation": "Giai đoạn 1 tạo chuẩn (lỗ, mặt đầu), giai đoạn 2 cắt răng, giai đoạn 3 gia công tinh sau nhiệt luyện."},
        {"type": MC,
         "question": "Sau khi tôi, mài lỗ bánh răng thì định vị theo:",
         "options": ["Mặt ngoài phôi chưa gia công", "Hai lỗ tâm",
                     "Lỗ vừa tôi", "Vành răng, qua con lăn đặt vào rãnh răng"],
         "answer": 3,
         "explanation": "Mài lỗ theo vòng chia (con lăn trong rãnh răng) và mặt đầu, để lỗ đồng tâm lại với răng."},
        {"type": MC,
         "question": "Sản xuất loạt, phôi đã cắt sẵn từng đoạn, cỡ trung bình, đủ thiết bị làm trục gá. Cách gá giữ đồng tâm và năng suất cao, không phí phôi là:",
         "options": ["Gia công toàn bộ trong một lần gá từ phôi cán",
                     "Lần 1 làm lỗ và một mặt đầu, lần 2 lên trục gá",
                     "Lần 1 mặt ngoài, lần 2 kẹp mâm ba chấu làm lỗ", "Gá hai mũi tâm từ đầu"],
         "answer": 1,
         "explanation": "Hai lần gá dùng trục gá: đồng tâm và năng suất cao, không phí phôi; phải làm trục gá chuyên dùng."},
        {"type": MC,
         "question": "Trục răng (bánh răng liền trục) khi mài răng dùng chuẩn nào?",
         "options": ["Cổ trục", "Mặt đầu bánh răng", "Lỗ then hoa", "Mặt đỉnh răng"],
         "answer": 0,
         "explanation": "Lỗ tâm dùng để tiện và cắt răng; mài răng dùng cổ trục vì đó là chuẩn lắp ráp."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Công nghệ chế tạo máy 2", "lesson_title": "Bài 18. Công nghệ gia công chi tiết bánh răng"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Loại theo l/d · yêu cầu kỹ thuật · phôi · chuẩn lỗ + mặt đầu · Chuẩn – Răng – Tinh · kiểm tra",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự lý thuyết,", len(exam["questions"]), "câu")
