#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho CNCTM 1 – Bài 1.
Dùng: python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
Nguồn ý: giáo trình CNCTM của bộ môn (Chương 1). Ví dụ chốt bậc, máy bơm là ví dụ tự soạn.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Kiểm tra nhanh — Những khái niệm cơ bản",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Việc nào sau đây KHÔNG thuộc quá trình công nghệ?",
         "options": ["Đúc phôi thân hộp số", "Phay rãnh then trên trục", "Vận chuyển phôi từ kho đến máy tiện", "Tôi bề mặt bánh răng"],
         "answer": 2,
         "explanation": "Vận chuyển không làm thay đổi hình dáng, kích thước hay tính chất của chi tiết → quá trình phụ."},
        {"type": MC,
         "question": "Quy trình công nghệ là:",
         "options": ["Mọi hoạt động của nhà máy để làm ra sản phẩm",
                     "Quá trình công nghệ hợp lý nhất đã được ghi thành văn kiện",
                     "Một lần định vị và kẹp chặt chi tiết",
                     "Tập hợp các động tác của công nhân đứng máy"],
         "answer": 1,
         "explanation": "Quy trình = quá trình công nghệ hợp lý nhất, ghi thành văn kiện (phiếu, bảng tiến trình)."},
        {"type": MC,
         "question": "Hai đặc trưng của một nguyên công là:",
         "options": ["Cùng dao và cùng chế độ cắt",
                     "Cùng chỗ làm việc và thực hiện liên tục",
                     "Cùng bề mặt và cùng một lần kẹp",
                     "Cùng vật liệu phôi và cùng bản vẽ"],
         "answer": 1,
         "explanation": "Nguyên công: một chỗ làm việc, làm liên tục trên cùng đối tượng gia công."},
        {"type": MC,
         "question": "Tiện mặt C cho cả loạt 100 chi tiết, sau đó trở đầu tiện mặt A cho cả loạt, đều trên cùng một máy. Số nguyên công là:",
         "options": ["1", "2", "100", "200"],
         "answer": 1,
         "explanation": "Công việc bị ngắt quãng (làm hết loạt mới trở đầu) nên mất tính liên tục → 2 nguyên công."},
        {"type": MC,
         "question": "Phay bánh răng 30 răng trên đầu phân độ, phôi không tháo ra giữa các răng. Mỗi lần chia răng là một:",
         "options": ["Nguyên công", "Lần gá", "Vị trí", "Đường chuyển dao"],
         "answer": 2,
         "explanation": "Phôi đổi chỗ so với dao mà không tháo ra → vị trí mới; số vị trí bằng số răng."},
        {"type": MC,
         "question": "Tiện thô một mặt trụ bằng 3 lần hớt cùng dao, cùng chế độ cắt, rồi tiện tinh mặt đó. Có:",
         "options": ["1 bước, 4 đường chuyển dao", "2 bước; bước thô có 3 đường chuyển dao", "4 bước", "3 bước, 1 đường chuyển dao"],
         "answer": 1,
         "explanation": "Thô → tinh đổi chế độ cắt nên là 2 bước; 3 lần hớt cùng chế độ cắt là 3 đường chuyển dao của bước thô."},
        {"type": MC,
         "question": "Một nhà máy sản xuất 1.500 hộp giảm tốc/năm, mỗi hộp có 2 trục (3 kg/trục), α = 4%, β = 6%. Sản lượng trục hằng năm là:",
         "options": ["1.500 chiếc", "1.650 chiếc", "3.000 chiếc", "3.300 chiếc"],
         "answer": 3,
         "explanation": "N = 1500 · 2 · (1 + 10/100) = 3300 chiếc/năm."},
        {"type": MC,
         "question": "Với N = 3.300 chiếc/năm và khối lượng 3 kg/chiếc, dạng sản xuất là:",
         "options": ["Hàng loạt nhỏ", "Hàng loạt vừa", "Hàng loạt lớn", "Hàng khối"],
         "answer": 1,
         "explanation": "3 kg < 4 kg → cột đầu; 3.300 nằm trong 500 – 5.000 → hàng loạt vừa."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Công nghệ chế tạo máy 1", "lesson_title": "Bài 1. Những khái niệm cơ bản"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Quá trình sản xuất · quá trình công nghệ · nguyên công, gá, vị trí, bước, đường chuyển dao · dạng sản xuất",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự lý thuyết,", len(exam["questions"]), "câu")
