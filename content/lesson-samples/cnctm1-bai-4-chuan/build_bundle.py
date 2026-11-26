#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho CNCTM 1 – Bài 4.
Dùng: python3 build_figs.py && python3 build_bundle.py
      rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts <bundle.json>
Nguồn ý: giáo trình CNCTM của bộ môn (Chương 4). Ví dụ trục bậc lệch tâm, hộp bút, bài toán 35/65 theo dạng giáo trình; số liệu đổi tự soạn.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Kiểm tra nhanh — Chuẩn",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Trong gá đặt chi tiết, thứ tự đúng là:",
         "options": ["Kẹp chặt rồi định vị", "Định vị rồi kẹp chặt",
                     "Định vị và kẹp chặt là một việc", "Chỉ cần kẹp chặt thật mạnh"],
         "answer": 1,
         "explanation": "Định vị xác định vị trí so với dao trước; kẹp chặt giữ nguyên vị trí đó, chống lực cắt."},
        {"type": MC,
         "question": "Rà gá thường dùng khi:",
         "options": ["Sản xuất đơn chiếc, loạt nhỏ", "Sản xuất hàng khối",
                     "Thợ chưa có tay nghề", "Phôi đã rất chính xác và cần gá thật nhanh"],
         "answer": 0,
         "explanation": "Rà gá tốn thời gian, phụ thuộc tay nghề nhưng không cần đồ gá riêng → hợp đơn chiếc, loạt nhỏ."},
        {"type": MC,
         "question": "Hai lỗ tâm ở hai đầu trục dùng để gá khi tiện, mài là:",
         "options": ["Chuẩn thô", "Chuẩn tinh chính", "Chuẩn ảo", "Chuẩn tinh phụ"],
         "answer": 3,
         "explanation": "Lỗ tâm đã gia công nên là chuẩn tinh; chỉ để gá, không tham gia lắp → tinh phụ."},
        {"type": MC,
         "question": "Đỉnh nón của bánh răng côn dùng để ghi kích thước trên bản vẽ là:",
         "options": ["Chuẩn thiết kế thực", "Chuẩn gia công", "Chuẩn thiết kế ảo", "Chuẩn lắp ráp"],
         "answer": 2,
         "explanation": "Đỉnh nón là điểm không có thật trên chi tiết → chuẩn thiết kế ảo."},
        {"type": MC,
         "question": "Định vị chi tiết hình hộp, mặt có 3 điểm tì (mặt định vị chính) nên là:",
         "options": ["Mặt nhỏ nhất", "Mặt dài và hẹp nhất", "Mặt có ba via", "Mặt lớn nhất"],
         "answer": 3,
         "explanation": "Ba điểm cần đặt xa nhau cho vững → chọn mặt lớn nhất."},
        {"type": MC,
         "question": "Chốt trụ dài lồng vào lỗ, đồng thời mặt đầu tì lên mặt phẳng 3 điểm. Đây là:",
         "options": ["Siêu định vị — hai bậc quay bị khử hai lần", "Định vị hoàn toàn",
                     "Định vị không hoàn toàn", "Cách gá tốt nhất cho chi tiết dạng bạc"],
         "answer": 0,
         "explanation": "Chốt dài và mặt tì 3 điểm cùng khử hai bậc quay → siêu định vị, dễ kênh chi tiết hoặc cong chốt."},
        {"type": MC,
         "question": "Kích thước 40 ± 0,15 có gốc không trùng chuẩn định vị; phương pháp có ω = 0,1 mm. Sai số chuẩn cho phép là:",
         "options": ["0,05 mm", "0,2 mm", "0,3 mm", "0,15 mm"],
         "answer": 1,
         "explanation": "[εc] = δ − ω = 0,3 − 0,1 = 0,2 mm."},
        {"type": MC,
         "question": "Nguyên tắc nào nói về chuẩn thô?",
         "options": ["Ưu tiên chuẩn tinh chính", "Chọn chuẩn thống nhất cho mọi nguyên công",
                     "Chỉ dùng một lần trong cả quá trình gia công", "Chuẩn định vị trùng gốc kích thước"],
         "answer": 2,
         "explanation": "Mặt thô sần, méo: dùng lại sẽ cho vị trí khác → chuẩn thô chỉ dùng một lần. Ba ý còn lại là nguyên tắc chuẩn tinh."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Công nghệ chế tạo máy 1", "lesson_title": "Bài 4. Chuẩn"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Gá đặt · các loại chuẩn · nguyên tắc 6 điểm · sai số chuẩn · chọn chuẩn thô, chuẩn tinh",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự lý thuyết,", len(exam["questions"]), "câu")
