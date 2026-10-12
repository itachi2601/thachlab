#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts <bundle.json>
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Năng lượng của dòng điện và công suất điện",
    "duration_minutes": 10,
    "questions": [
        {"type": MC, "question": "Đo công suất bóng đèn 6 V – 3 W bằng ampe kế có độ chia 0,01 A và vôn kế. Để các giá trị U·I đáng tin hơn, nên làm gì?",
         "options": ["Đo lặp vài lần ở mỗi U, lấy trung bình I", "Thay ampe kế loại 10 A, độ chia 0,2 A", "Tính U : I thay cho U · I cho gọn", "Tăng U lên 9 V để dòng lớn, dễ đọc"],
         "answer": 0, "explanation": "Đo lặp rồi lấy trung bình làm sai lệch ngẫu nhiên khi đọc kim nhỏ đi. Độ chia 0,2 A quá thô; U : I là điện trở; 9 V vượt định mức làm đèn dễ cháy."},
        {"type": MC, "question": "Bóng đèn ghi 220 V – 60 W đang sáng bình thường. Cường độ dòng điện qua đèn là",
         "options": ["13 200 A", "3,67 A", "0,00027 A", "0,27 A"],
         "answer": 3, "explanation": "Sáng bình thường nên U = 220 V, P = 60 W; I = P/U = 60/220 ≈ 0,27 A. Ra 3,67 A là chia ngược U/P."},
        {"type": MC, "question": "Chỉ bật một máy sấy tóc trong 30 phút, công tơ tăng thêm 0,6 số. Công suất của máy sấy là",
         "options": ["0,3 W", "1 200 W", "1,2 W", "20 W"],
         "answer": 1, "explanation": "0,6 số = 0,6 kWh, t = 0,5 h; P = A/t = 1,2 kW = 1 200 W. Ra 20 W là chia cho 30 phút thay vì 0,5 giờ."},
        {"type": MC, "question": "Nhãn một máy điều hoà ghi 1 000 W. Câu nào đúng?",
         "options": ["Mỗi tháng máy tiêu thụ đúng 1 000 W điện", "Chạy đúng công suất 1 giờ, máy tiêu thụ 1 kWh", "Chạy đúng công suất 1 giờ, máy tiêu thụ 1 000 kWh", "Bật càng lâu thì công suất của máy càng tăng"],
         "answer": 1, "explanation": "1 000 W là công suất; một giờ tiêu thụ A = 1 kW · 1 h = 1 kWh. Oát đo công suất, kWh đo điện năng."},
        {"type": MC, "question": "Quạt trần 75 W chạy đúng công suất trong 2 giờ. Điện năng tiêu thụ tính ra jun là",
         "options": ["150 J", "9 000 J", "0,15 J", "5,4·10⁵ J"],
         "answer": 3, "explanation": "t = 2 h = 7 200 s; A = 75 · 7 200 = 540 000 J. Ra 150 là Wh, ra 9 000 là dùng phút, 0,15 là kWh."},
        {"type": MC, "question": "Hai bóng đèn sợi đốt Đ1 (220 V – 40 W) và Đ2 (220 V – 100 W) mắc nối tiếp vào 220 V. Coi điện trở mỗi đèn không đổi. Đèn nào sáng hơn?",
         "options": ["Đèn Đ1 (40 W)", "Đèn Đ2 (100 W)", "Hai đèn sáng như nhau", "Cả hai đèn đều tắt"],
         "answer": 0, "explanation": "R1 = 220²/40 = 1 210 Ω, R2 = 484 Ω. Nối tiếp cùng I, P = I²R nên đèn có R lớn hơn (Đ1) sáng hơn."},
        {"type": MC, "question": "Một tủ lạnh có công suất trung bình 120 W, chạy suốt 24 giờ mỗi ngày. Giá điện 2 000 đồng cho mỗi kWh (giá minh hoạ). Tiền điện của tủ lạnh trong 30 ngày là",
         "options": ["172 800 000 đồng", "7 200 đồng", "172 800 đồng", "5 760 đồng"],
         "answer": 2, "explanation": "A = 0,12 kW · 24 h · 30 = 86,4 kWh; tiền = 86,4 · 2 000 = 172 800 đồng. Quên đổi W ra kW thì gấp một nghìn lần."},
    ],
}
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "KHTN 9", "lesson_title": "Bài 13. Năng lượng của dòng điện và công suất điện"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Điện năng; công suất điện P = UI và số ghi trên thiết bị; điện năng tiêu thụ A = UIt, kWh và tiền điện; P = I²R = U²/R",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
