#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Thực hành: Xác định động lượng trước và sau va chạm",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Hai xe đứng yên trên băng đệm khí, lò xo nén ở giữa. Xe 2 nặng gấp đôi xe 1. Cắt dây. Điều gì xảy ra?",
         "options": ["Hai xe chạy nhanh bằng nhau, vì lực lò xo lên hai xe bằng nhau",
                     "Xe 2 nặng hơn nên chạy nhanh hơn, vì có nhiều \"đà\" hơn",
                     "Xe 1 chạy nhanh gấp đôi xe 2, hai xe đi ngược chiều",
                     "Hai xe vẫn đứng yên, vì hai lực triệt tiêu nhau"],
         "answer": 2,
         "explanation": "Trước khi cắt tổng p = 0; sau khi cắt vẫn 0 nên m1·v1 = m2·v2 về độ lớn. m2 = 2·m1 thì v1 = 2·v2. Lực bằng nhau nhưng khối lượng khác nhau thì gia tốc khác nhau; hai lực đặt lên hai vật khác nhau nên không triệt tiêu lên từng xe."},
        {"type": MC,
         "question": "Lần 3: m1 = 0,405 kg, tấm cản quang rộng 5,00 cm, t1 = 0,105 s. Động lượng p trước va chạm là:",
         "options": ["19,3 kg·m/s", "0,382 kg·m/s", "0,0021 kg·m/s", "0,193 kg·m/s"],
         "answer": 3,
         "explanation": "v1 = 0,0500/0,105 ≈ 0,476 m/s; p = 0,405·0,476 ≈ 0,193 kg·m/s. 19,3: chưa đổi cm sang m. 0,382: dùng cả hai khối lượng trong khi xe 2 đứng yên. 0,0021: tính v = s·t thay vì s/t."},
        {"type": MC,
         "question": "Hai xe đẩy nhau, m1 = 0,300 kg, m2 = 0,150 kg. Xe 2 qua cổng 2 hết t2' = 0,150 s. Thời gian t1' của xe 1 qua cổng 1 gần nhất với (bỏ qua mất mát):",
         "options": ["0,300 s", "0,075 s", "0,150 s", "0,450 s"],
         "answer": 0,
         "explanation": "Hai động lượng bằng nhau về độ lớn: m1·s/t1' = m2·s/t2', nên t1' = t2'·m1/m2 = 0,150·2 = 0,300 s. Xe nặng hơn đi chậm hơn nên mất nhiều thời gian hơn để qua cổng."},
        {"type": MC,
         "question": "Xe 1 (0,250 kg) đi sang trái với 0,400 m/s, xe 2 (0,500 kg) đi sang phải với 0,200 m/s. Chọn chiều dương hướng sang TRÁI. Tổng động lượng sau p' là:",
         "options": ["+0,200 kg·m/s", "0 kg·m/s", "−0,200 kg·m/s", "+0,100 kg·m/s"],
         "answer": 1,
         "explanation": "Chiều dương sang trái: p1' = +0,250·0,400 = +0,100; p2' = −0,500·0,200 = −0,100. Tổng bằng 0. Hai phương án ±0,200 cộng hai độ lớn; +0,100 chỉ lấy xe 1."},
        {"type": MC,
         "question": "Va chạm mềm: m1 = 0,205 kg, m2 = 0,398 kg, hai xe dính nhau qua cổng 2 với v' = 0,170 m/s. Động lượng p' là:",
         "options": ["0,0349 kg·m/s", "0,170 kg·m/s", "0,103 kg·m/s", "0,0677 kg·m/s"],
         "answer": 2,
         "explanation": "p' = (0,205 + 0,398)·0,170 = 0,603·0,170 ≈ 0,103 kg·m/s. 0,0349 chỉ tính xe 1, 0,0677 chỉ tính xe 2; 0,170 lấy tốc độ làm động lượng."},
        {"type": MC,
         "question": "Một nhóm khác làm ba lần va chạm mềm, đều có p' < p, δ = 2,1 %; 2,3 %; 2,0 % và ε ≈ 2,5 % mỗi lần. Kết luận phù hợp nhất:",
         "options": ["Định luật sai, vì cả ba lần đều cho p' không bằng p chính xác",
                     "Thí nghiệm hỏng, phải làm lại cho tới khi p' = p đúng từng chữ số",
                     "Sai số ngẫu nhiên, nên lấy trung bình ba lần thì p' sẽ bằng p",
                     "Phù hợp trong sai số; lệch cùng phía gợi ý sai số hệ thống"],
         "answer": 3,
         "explanation": "Nhóm này có δ < ε ở cả ba lần nên không bác bỏ được bảo toàn. Ba lần cùng một phía là dấu hiệu sai số hệ thống (như ngoại lực nhỏ), không phải ngẫu nhiên; lệch cùng phía thì lấy trung bình không làm mất lệch."},
        {"type": MC,
         "question": "Va chạm mềm: thêm gia trọng để cả hai xe nặng gấp đôi, vẫn đẩy xe 1 sao cho t1 như cũ. Thời gian t1' của cặp xe qua cổng 2 thay đổi thế nào (bỏ qua mất mát)?",
         "options": ["Giảm một nửa, vì xe nặng hơn thì có nhiều đà hơn",
                     "Không đổi, vì v' chỉ phụ thuộc tỉ số m1 : m2",
                     "Gấp đôi, vì khối lượng của cặp xe tăng gấp đôi",
                     "Gấp bốn, vì cả p lẫn m cùng gấp đôi"],
         "answer": 1,
         "explanation": "v' = m1/(m1+m2)·v1: nhân đôi cả m1 và m2 thì tỉ số không đổi, v' không đổi, t1' = s/v' không đổi."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 30. Thực hành: Xác định động lượng của vật trước và sau va chạm"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Đo tốc độ bằng cổng quang; động lượng trước và sau va chạm mềm, hai xe đẩy nhau; độ lệch, sai số và nguyên nhân hệ không kín hoàn toàn",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
