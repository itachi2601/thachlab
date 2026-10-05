#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Cơ năng và định luật bảo toàn cơ năng",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Quả bóng 0,5 kg bay ở độ cao 4 m so với mặt đất với tốc độ 6 m/s. Mốc thế năng ở mặt đất, g = 10 m/s². Cơ năng của bóng là:",
         "options": ["38 J", "11 J", "29 J", "20 J"],
         "answer": 2,
         "explanation": "Wđ = ½·0,5·36 = 9 J; Wt = 0,5·10·4 = 20 J; W = 29 J. Ra 38 J là quên hệ số ½; 20 J là chỉ tính thế năng."},
        {"type": MC,
         "question": "Thả hòn bi không vận tốc đầu ở đỉnh máng nhẵn cao 0,45 m. Bỏ qua ma sát, g = 10 m/s². Tốc độ bi ở chân máng là:",
         "options": ["3 m/s", "9 m/s", "2,1 m/s", "Không tính được vì thiếu khối lượng"],
         "answer": 0,
         "explanation": "mgh = ½mv² nên v = √(2·10·0,45) = 3 m/s; khối lượng triệt tiêu."},
        {"type": MC,
         "question": "Xe trượt cỏ cùng em bé 20 kg trượt không vận tốc đầu từ đỉnh dốc cao 5 m, tới chân dốc với 8 m/s. g = 10 m/s². Tổng công của ma sát và lực cản là:",
         "options": ["360 J", "1640 J", "−640 J", "−360 J"],
         "answer": 3,
         "explanation": "W1 = 1000 J, W2 = 640 J; A_c = W2 − W1 = −360 J. Công âm: cơ năng giảm."},
        {"type": MC,
         "question": "Trường hợp nào cơ năng của vật được bảo toàn?",
         "options": ["Người nhảy dù rơi với tốc độ không đổi", "Hòn đá ném xiên, bỏ qua sức cản không khí",
                     "Thùng hàng được thang máy kéo lên đều", "Xe đạp bóp phanh, lết trên đường ngang"],
         "answer": 1,
         "explanation": "Chỉ hòn đá (bỏ qua cản) chịu riêng trọng lực. Nhảy dù rơi đều: lực cản sinh công âm; thang máy: lực kéo sinh công dương; phanh: ma sát."},
        {"type": MC,
         "question": "Con lắc đơn dao động, bỏ qua lực cản, mốc thế năng ở vị trí thấp nhất. Phát biểu nào đúng?",
         "options": ["Động năng không đổi, vì cơ năng được bảo toàn", "Ở vị trí cao nhất, cơ năng bằng 0 vì vật dừng lại",
                     "Cơ năng lớn nhất ở vị trí thấp nhất, vì tốc độ lớn nhất", "Động năng lớn nhất ở vị trí thấp nhất, vì ở đó thế năng nhỏ nhất"],
         "answer": 3,
         "explanation": "Cơ năng bảo toàn là giữ tổng; ở vị trí thấp nhất Wt = 0 nên động năng lớn nhất."},
        {"type": MC,
         "question": "Từ ban công cao 15 m, ném bóng thẳng đứng lên với 10 m/s. Bỏ qua lực cản, g = 10 m/s². Tốc độ bóng khi chạm đất là:",
         "options": ["17,3 m/s", "10 m/s", "20 m/s", "Chưa tính được, vì còn tuỳ mốc thế năng"],
         "answer": 2,
         "explanation": "v² = 10² + 2·10·15 = 400, v = 20 m/s; tốc độ không phụ thuộc mốc đã chọn."},
        {"type": MC,
         "question": "Lan và ván 50 kg thả không vận tốc đầu từ mép lòng chảo cao 3,2 m so với đáy, bỏ qua ma sát. Ở độ cao nào so với đáy thì động năng bằng thế năng?",
         "options": ["1,6 m", "0,8 m", "2,4 m", "2,26 m"],
         "answer": 0,
         "explanation": "W = Wđ + Wt = 2Wt nên z = 3,2/2 = 1,6 m."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 26. Cơ năng và định luật bảo toàn cơ năng"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Cơ năng; định luật bảo toàn cơ năng; biến thiên cơ năng khi có ma sát, lực cản",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
