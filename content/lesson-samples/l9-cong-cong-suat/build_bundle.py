#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts <bundle.json>
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Công và công suất",
    "duration_minutes": 10,
    "questions": [
        {"type": MC, "question": "Kéo đều khối gỗ bằng lực kế độ chia 0,1 N, ba lần cùng quãng đường mà công tính ra lệch nhau. Muốn giá trị công đáng tin hơn, nên làm gì?",
         "options": ["Giật mạnh lực kế cho kim chỉ số lớn, dễ đọc", "Kéo thật đều, đo nhiều lần rồi lấy trung bình", "Thay lực kế có độ chia 1 N cho kim ít rung", "Đo quãng đường bằng gang tay cho nhanh"],
         "answer": 1, "explanation": "Kéo đều thì lực kéo bằng lực cản; lấy trung bình làm sai lệch ngẫu nhiên nhỏ đi. Giật mạnh làm vật tăng tốc, độ chia 1 N quá thô, gang tay sai số lớn."},
        {"type": MC, "question": "Một công nhân đẩy xe hàng với lực 200 N theo phương ngang, xe đi được 15 m theo hướng đẩy. Công của lực đẩy là",
         "options": ["3 kJ", "13,3 J", "215 J", "3 000 kJ"],
         "answer": 0, "explanation": "A = F·s = 200 · 15 = 3 000 J = 3 kJ. 13,3 là chia F/s; 215 là cộng; 3 000 kJ ghi sai đơn vị."},
        {"type": MC, "question": "Minh xách bao gạo 10 kg (trọng lượng 100 N) lên cao 6 m hết 20 s. Công suất của Minh khi đưa bao gạo lên là",
         "options": ["12 000 W", "3 W", "0,033 W", "30 W"],
         "answer": 3, "explanation": "A = 100 · 6 = 600 J; P = 600/20 = 30 W. 3 W là lấy 10 kg làm lực; 12 000 W là nhân A·t."},
        {"type": MC, "question": "Một bạn xách cặp nặng 30 N, đi đều 50 m trên sân nằm ngang; lực tay giữ cặp hướng thẳng lên. Công của lực tay giữ cặp là",
         "options": ["1 500 J", "80 J", "0,6 J", "0 J"],
         "answer": 3, "explanation": "Dịch chuyển nằm ngang vuông góc với lực tay hướng lên nên lực tay không thực hiện công: A = 0."},
        {"type": MC, "question": "Máy bơm X có công suất 2 kW, máy bơm Y có công suất 1 kW. Câu nào đúng?",
         "options": ["Máy X lúc nào cũng thực hiện công nhiều hơn máy Y", "Làm cùng một công, máy X cần thời gian gấp đôi máy Y", "Trong cùng thời gian, máy X thực hiện công gấp đôi máy Y", "Chạy càng lâu thì công suất của máy X càng tăng"],
         "answer": 2, "explanation": "A = P·t: cùng thời gian thì công tỉ lệ với công suất. Công suất không tăng theo thời gian chạy."},
        {"type": MC, "question": "Thang máy đưa một người nặng 600 N đi đều từ tầng 1 lên tầng 5 trong 20 s, mỗi tầng cao 3 m. Chỉ tính công nâng người, công suất của thang máy là",
         "options": ["360 W", "450 W", "90 W", "144 000 W"],
         "answer": 0, "explanation": "Tầng 1 lên tầng 5 là 4 khoảng tầng: h = 12 m; A = 7 200 J; P = 360 W. 450 W là đếm 5 tầng."},
        {"type": MC, "question": "Một ô tô chạy đều với tốc độ 72 km/h, lực kéo của động cơ là 2 000 N. Công suất của động cơ là",
         "options": ["144 kW", "40 kW", "100 W", "27,8 W"],
         "answer": 1, "explanation": "v = 72 km/h = 20 m/s; P = F·v = 2 000 · 20 = 40 000 W = 40 kW. 144 kW là quên đổi km/h ra m/s."},
    ],
}
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "KHTN 9", "lesson_title": "Bài 4. Công và công suất"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Công cơ học A = F·s và điều kiện có công; đơn vị năng lượng J, cal, kWh; công suất P = A/t, P = F·v; đơn vị W, kW, HP",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
