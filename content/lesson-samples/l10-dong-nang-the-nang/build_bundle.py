#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Động năng, thế năng",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Vận động viên trượt băng 50 kg lướt với tốc độ 8 m/s. Động năng của người đó là",
         "options": ["200 J", "3200 J", "400 J", "1600 J"],
         "answer": 3,
         "explanation": "Wđ = ½·50·8² = 1600 J. Ra 200 J là quên bình phương; ra 3200 J là quên hệ số ½."},
        {"type": MC,
         "question": "Ô tô 1000 kg đang chạy 72 km/h thì phanh, lực hãm không đổi 5000 N. Quãng đường từ lúc phanh đến lúc dừng là",
         "options": ["40 m", "80 m", "518,4 m", "2 m"],
         "answer": 0,
         "explanation": "v = 20 m/s; định lí động năng: 0 − ½·1000·20² = −5000·s nên s = 40 m. Ra 518,4 m là chưa đổi km/h ra m/s."},
        {"type": MC,
         "question": "Toa tàu lượn 500 kg đi theo ray cong từ đỉnh cao 30 m xuống chỗ thấp cao 5 m so với mặt đất (g = 10 m/s²). Công của trọng lực là",
         "options": ["150 kJ", "125 kJ", "25 kJ", "−125 kJ"],
         "answer": 1,
         "explanation": "A = mg(z_đầu − z_cuối) = 500·10·25 = 125 000 J, không phụ thuộc hình dạng ray; đi xuống nên công dương."},
        {"type": MC,
         "question": "Vận động viên trượt băng tăng tốc từ 3 m/s lên 9 m/s. Động năng của người đó tăng",
         "options": ["3 lần", "81 lần", "9 lần", "6 lần"],
         "answer": 2,
         "explanation": "Động năng tỉ lệ với v²: tỉ số tốc độ 3, tỉ số động năng 3² = 9."},
        {"type": MC,
         "question": "Quả bóng 0,2 kg rơi từ ban công xuống sân thấp hơn 5 m. Chọn mốc thế năng tại ban công, g = 10 m/s². Thế năng của bóng ở sân và công của trọng lực khi rơi là",
         "options": ["Wt = −10 J; A = +10 J", "Wt = +10 J; A = +10 J", "Wt = −10 J; A = −10 J", "Wt = 0; A = 0"],
         "answer": 0,
         "explanation": "Sân dưới mốc nên z = −5 m, Wt = −10 J. Công = thế năng đầu − cuối = 0 − (−10) = +10 J, không phụ thuộc mốc."},
        {"type": MC,
         "question": "Kéo thùng hàng 40 kg từ nghỉ trên sàn ngang bằng lực 300 N nằm ngang, đi được 10 m; lực ma sát 100 N. Tốc độ của thùng lúc đó là",
         "options": ["12,2 m/s", "10 m/s", "14,1 m/s", "7,1 m/s"],
         "answer": 1,
         "explanation": "Tổng công = 3000 − 1000 = 2000 J = ½·40·v² nên v = 10 m/s. Ra 12,2 m/s là quên công âm của ma sát."},
        {"type": MC,
         "question": "Toa tàu lượn qua điểm B cao 3 m với tốc độ 20 m/s, leo lên đỉnh D cao 13 m so với mặt đất, bỏ qua ma sát (g = 10 m/s²). Tốc độ của toa tại D là",
         "options": ["24,5 m/s", "11,8 m/s", "17,3 m/s", "14,1 m/s"],
         "answer": 3,
         "explanation": "Toa lên 10 m: v_D² = 20² − 2·10·10 = 200, v_D ≈ 14,1 m/s. Ra 11,8 m/s là dùng cả 13 m thay vì hiệu độ cao."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 25. Động năng, thế năng"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Động năng và định lí động năng; thế năng trọng trường, mốc thế năng; công của trọng lực",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
