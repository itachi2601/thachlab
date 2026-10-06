#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Lực hướng tâm và gia tốc hướng tâm",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Ô tô qua một khúc cua tròn với tốc độ gấp đôi lúc trước (cùng bán kính). Gia tốc hướng tâm của xe:",
         "options": ["Không đổi, vì vẫn khúc cua ấy", "Tăng gấp đôi", "Giảm còn một nửa", "Tăng gấp bốn"],
         "answer": 3,
         "explanation": "a_ht = v²/r: v gấp 2 thì v² gấp 4, r giữ nguyên nên a_ht gấp 4. Chọn gấp đôi là quên bình phương của v."},
        {"type": MC,
         "question": "Vệ tinh chuyển động tròn đều quanh Trái Đất. Lực đóng vai lực hướng tâm của vệ tinh là:",
         "options": ["Lực đẩy của động cơ vệ tinh chĩa vào tâm", "Lực hấp dẫn của Trái Đất lên vệ tinh",
                     "Không lực nào, vệ tinh bay nhờ quán tính", "Hợp của lực hấp dẫn và lực li tâm"],
         "answer": 1,
         "explanation": "Lực đáng kể duy nhất lên vệ tinh là lực hấp dẫn, chĩa vào tâm Trái Đất; nó chính là lực hướng tâm. Chỉ có quán tính (hoặc hợp lực bằng 0) thì vệ tinh bay thẳng."},
        {"type": MC,
         "question": "Một cục tẩy nằm trên đĩa bàn xoay, quay đều cùng đĩa, không trượt. Các lực tác dụng lên cục tẩy là:",
         "options": ["Trọng lực, phản lực và ma sát nghỉ hướng vào tâm",
                     "Trọng lực, phản lực, ma sát nghỉ hướng vào tâm và lực hướng tâm",
                     "Trọng lực, phản lực và lực li tâm hướng ra ngoài",
                     "Trọng lực, phản lực và ma sát nghỉ theo chiều quay"],
         "answer": 0,
         "explanation": "Trọng lực và phản lực triệt tiêu; ma sát nghỉ hướng vào tâm đóng vai lực hướng tâm. Liệt kê thêm 'lực hướng tâm' là đếm ma sát hai lần."},
        {"type": MC,
         "question": "Xe rẽ trái gấp, người ngồi trong xe bị dồn vào cửa bên phải. Giải thích đúng là:",
         "options": ["Lực li tâm đẩy người văng ra phía ngoài khúc cua", "Ghế và cửa xe sinh ra lực kéo người sang phải",
                     "Người giữ hướng đi thẳng cũ, còn xe rẽ trái dồn vào", "Lực hướng tâm của xe khi rẽ hướng ra phía ngoài"],
         "answer": 2,
         "explanation": "Do quán tính người muốn đi thẳng; xe rẽ trái nên cửa phải 'đón' người rồi đẩy người vào trong. Không có vật nào gây ra 'lực li tâm'."},
        {"type": MC,
         "question": "Chiếc đĩa CD quay đều trong ổ đọc. Điểm A trên mặt đĩa cách tâm 4 cm, điểm B cách tâm 2 cm. So sánh gia tốc hướng tâm:",
         "options": ["a_A = a_B", "a_A = 2a_B", "a_A = a_B/2", "a_A = 4a_B"],
         "answer": 1,
         "explanation": "Hai điểm cùng một vật quay nên cùng ω; a = ω²r tỉ lệ thuận với r nên a_A = 2a_B. Dùng v²/r như thể v bằng nhau sẽ ra a_A = a_B/2 (sai vì v_A = 2v_B)."},
        {"type": MC,
         "question": "Ô tô 1000 kg chạy đều 72 km/h qua khúc cua phẳng bán kính 40 m. Lực ma sát nghỉ cần có để xe đi đúng đường cong là:",
         "options": ["10 000 N", "129 600 N", "500 N", "10 N"],
         "answer": 0,
         "explanation": "v = 20 m/s; F_ht = m·v²/r = 1000·400/40 = 10 000 N. 129 600 N là chưa đổi km/h ra m/s; 500 N là quên bình phương v; 10 N là quên nhân m."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 32. Lực hướng tâm và gia tốc hướng tâm"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Gia tốc hướng tâm a = v²/r = ω²r; lực hướng tâm là vai của một lực đã có; không có lực li tâm đẩy vật ra",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
