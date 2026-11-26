#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho CNCTM 1 – Bài 7 Gia công mặt phẳng.
Dùng: python3 build_figs.py && python3 build_bundle.py  rồi
      npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
Nguồn ý: giáo trình CNCTM của bộ môn (Chương 7). Ví dụ thân máy, tấm dẫn hướng, xéc măng là ví dụ tự soạn.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Kiểm tra nhanh — Gia công mặt phẳng",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Nhóm nào KHÔNG thuộc bốn nhóm yêu cầu kỹ thuật của mặt phẳng?",
         "options": ["Độ phẳng, độ thẳng", "Độ song song, vuông góc với mặt khác",
                     "Độ nhám, độ cứng bề mặt", "Số vòng quay trục chính khi gia công"],
         "answer": 3,
         "explanation": "Bốn nhóm: kích thước, hình dáng, vị trí, bề mặt. Số vòng quay là chế độ cắt, không phải yêu cầu của chi tiết."},
        {"type": MC,
         "question": "Khi bào trên máy bào ngang, chuyển động chạy dao là:",
         "options": ["Dao tịnh tiến đi – về", "Bàn máy mang phôi dịch một bước sau mỗi hành trình kép",
                     "Dao quay tròn", "Phôi quay tròn"],
         "answer": 1,
         "explanation": "Bào ngang: dao đi – về là chuyển động chính; bàn máy nhích sau mỗi hành trình kép là chạy dao."},
        {"type": MC,
         "question": "Khi phay mặt phẳng, chuyển động chính là:",
         "options": ["Dao quay", "Phôi tịnh tiến dọc", "Phôi tịnh tiến ngang", "Bàn máy nâng lên"],
         "answer": 0,
         "explanation": "Phay: dao quay là chuyển động chính; phôi (bàn máy) tịnh tiến là chạy dao."},
        {"type": MC,
         "question": "Phay thuận có đặc điểm:",
         "options": ["Dao quay ngược chiều chạy dao, phoi mỏng → dày",
                     "Dao quay cùng chiều chạy dao, phoi dày → mỏng, cần máy ít rơ",
                     "Chỉ dùng để phay thô phôi đúc", "Dùng được trên mọi máy, kể cả máy đã rơ"],
         "answer": 1,
         "explanation": "Phay thuận: cùng chiều, phoi dày → mỏng, mặt nhẵn hơn; chỉ dùng khi băng trượt ít rơ."},
        {"type": MC,
         "question": "So với mài bằng mặt đầu đá, mài phẳng bằng lưng đá:",
         "options": ["Năng suất cao hơn vì tiếp xúc rộng", "Chính xác hơn vì tiếp xúc hẹp, dễ thoát nhiệt",
                     "Không cần tưới nguội", "Chỉ mài được gang"],
         "answer": 1,
         "explanation": "Lưng đá tiếp xúc hẹp: dễ thoát phoi, thoát nhiệt, tưới nguội → chính xác; năng suất thấp hơn."},
        {"type": MC,
         "question": "Mặt phẳng thép đã tôi cần cấp 7, Ra = 0,25 µm. Bước cuối hợp lý là:",
         "options": ["Phay tinh mỏng", "Bào tinh mỏng", "Mài tinh", "Mài tinh mỏng"],
         "answer": 3,
         "explanation": "Mài tinh mỏng đạt cấp 7–6, Ra 0,4–0,1; phay, bào tinh mỏng và mài tinh chỉ tới Ra 0,8."},
        {"type": MC,
         "question": "Cạo rà KHÔNG sửa được sai lệch nào?",
         "options": ["Mấp mô nhỏ trên bề mặt", "Độ nhám còn lớn",
                     "Mặt đế không song song với mặt trên", "Vài điểm cao cục bộ"],
         "answer": 2,
         "explanation": "Cạo chỉ hạ điểm cao, sửa sai lệch hình dáng nhỏ; không sửa được sai lệch vị trí (song song, vuông góc)."},
        {"type": MC,
         "question": "Mặt phẳng dài 800 mm, rộng 200 mm. Theo bảng lượng dư cạo, cần để lại khoảng:",
         "options": ["0,10 mm", "0,15 mm", "0,20 mm", "0,30 mm"],
         "answer": 2,
         "explanation": "Rộng 200 thuộc hàng 100–500; dài 800 thuộc cột 500–1000 → 0,20 mm."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Công nghệ chế tạo máy 1", "lesson_title": "Bài 7. Gia công mặt phẳng"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Bào, xọc · phay thuận, phay nghịch · chuốt · mài, mài nghiền · cạo rà · trình tự gia công",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự lý thuyết,", len(exam["questions"]), "câu")
