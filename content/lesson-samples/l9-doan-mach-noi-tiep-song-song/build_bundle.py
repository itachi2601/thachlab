#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts <bundle.json>
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Đoạn mạch nối tiếp, song song",
    "duration_minutes": 10,
    "questions": [
        {"type": MC, "question": "Mắc R₁ = 10 Ω nối tiếp R₂ = 20 Ω, đo bằng vôn kế có độ chia 0,1 V. Một lần đo được U₁ = 2,0 V, U₂ = 4,0 V nhưng U giữa A và B là 6,1 V. Lí do hợp lí nhất là",
         "options": ["Đọc kim vôn kế có thể lệch tới nửa vạch chia", "Vôn kế đo U giữa A và B đã bị mắc nối tiếp vào mạch", "Điện trở R₁ nóng lên nên tăng khi nguồn lớn", "Dòng điện qua R₂ nhỏ hơn dòng điện qua R₁"],
         "answer": 0, "explanation": "Mỗi lần đọc lệch tới 0,05 V; ba số đọc có thể lệch tới 0,15 V. Dù R₁ đổi thế nào, U₁ + U₂ vẫn bằng U giữa A và B; nối tiếp thì dòng như nhau."},
        {"type": MC, "question": "Mắc R₁ = 6 Ω song song R₂ = 12 Ω vào nguồn 12 V. Ampe kế ở mạch chính chỉ",
         "options": ["0,67 A", "1,5 A", "2 A", "3 A"],
         "answer": 3, "explanation": "Mỗi nhánh nhận đủ 12 V: I₁ = 2 A, I₂ = 1 A, I = 3 A. Ra 0,67 A là cộng R như nối tiếp; 1,5 A là chia đôi U."},
        {"type": MC, "question": "Đoạn mạch AB gồm R₁ = 2 Ω nối tiếp với cụm (R₂ = 6 Ω song song R₃ = 6 Ω). Điện trở tương đương của đoạn mạch là",
         "options": ["14 Ω", "1,2 Ω", "5 Ω", "3,4 Ω"],
         "answer": 2, "explanation": "Cụm R₂, R₃ song song: 6·6/(6 + 6) = 3 Ω; R tương đương = 2 + 3 = 5 Ω. 14 Ω là coi cả ba nối tiếp, 1,2 Ω là coi cả ba song song."},
        {"type": MC, "question": "Ba bóng đèn giống nhau mắc nối tiếp. Ampe kế đặt trước bóng thứ nhất chỉ 0,3 A. Ampe kế đặt sau bóng thứ ba chỉ",
         "options": ["0,3 A", "0,1 A", "0,9 A", "0 A"],
         "answer": 0, "explanation": "Nối tiếp chỉ có một đường đi, cường độ dòng điện như nhau ở mọi chỗ. Bị chia ra là hiệu điện thế, không phải dòng điện."},
        {"type": MC, "question": "Mắc R₁ = 20 Ω song song R₂ = 30 Ω. Điện trở tương đương là",
         "options": ["50 Ω", "25 Ω", "0,083 Ω", "12 Ω"],
         "answer": 3, "explanation": "R tương đương = 20·30/(20 + 30) = 12 Ω. Ra 0,083 Ω là quên lật ngược (đó mới là 1 chia R tương đương)."},
        {"type": MC, "question": "Hai bóng đèn 220 V mắc song song vào điện lưới 220 V. Bóng 1 đứt dây tóc. Bóng 2 sẽ",
         "options": ["tắt theo, vì mạch điện bị hở", "vẫn sáng như cũ", "sáng hơn, vì nhận thêm dòng của bóng 1", "sáng yếu đi, vì dòng mạch chính giảm"],
         "answer": 1, "explanation": "Nhánh bóng 2 vẫn nhận đủ 220 V nên dòng qua nó không đổi; chỉ dòng mạch chính giảm."},
        {"type": MC, "question": "Đoạn mạch AB gồm R₁ = 3 Ω nối tiếp với cụm (R₂ = 6 Ω song song R₃ = 3 Ω), U giữa A và B là 10 V. Cường độ dòng điện qua R₂ là",
         "options": ["1,33 A", "1,0 A", "0,67 A", "2,0 A"],
         "answer": 2, "explanation": "Cụm song song 2 Ω, R tương đương 5 Ω, I = 2 A, U của cụm = 4 V, I₂ = 4/6 ≈ 0,67 A. 1,33 A là dòng qua R₃; 2,0 A là dòng mạch chính."},
    ],
}
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "KHTN 9", "lesson_title": "Bài 12. Đoạn mạch nối tiếp, song song"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Đoạn mạch nối tiếp, song song: cường độ dòng điện, hiệu điện thế, điện trở tương đương; tính U, I trong mạch hỗn hợp",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
