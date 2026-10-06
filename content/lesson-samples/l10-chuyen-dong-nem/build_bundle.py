#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Chuyển động ném",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Từ cùng độ cao h, viên bi A được bắn ngang với v0 = 2 m/s, viên bi B được bắn ngang với v0 = 6 m/s (bỏ qua lực cản). Thời gian rơi của hai viên:",
         "options": ["B rơi lâu gấp ba lần, vì B bay xa gấp ba",
                     "A rơi lâu gấp ba lần, vì A bay chậm hơn",
                     "Chưa kết luận được, còn phải biết khối lượng hai viên",
                     "Bằng nhau, vì thời gian rơi chỉ do độ cao quyết định"],
         "answer": 3,
         "explanation": "t = √(2h/g) chỉ chứa h và g, không có v0 và không có khối lượng. Viên B chỉ bay xa hơn chứ không rơi lâu hơn."},
        {"type": MC,
         "question": "Một vật được ném ngang từ độ cao h. Muốn tầm xa tăng gấp đôi mà giữ nguyên v0, phải ném vật từ độ cao:",
         "options": ["2h", "4h", "h/2", "√2·h"],
         "answer": 1,
         "explanation": "L = v0·√(2h/g) nên L tỉ lệ với √h: muốn L gấp đôi thì h phải gấp bốn. Chọn 2h là quên dấu căn; chọn √2·h là làm ngược."},
        {"type": MC,
         "question": "Một vật ném ngang với v0 = 6 m/s từ độ cao 20 m, lấy g = 10 m/s². Độ lớn vận tốc khi chạm đất là:",
         "options": ["20 m/s", "26 m/s", "20,9 m/s", "22,9 m/s"],
         "answer": 2,
         "explanation": "vy = √(2gh) = √(2×10×20) = 20 m/s; v = √(v0² + vy²) = √(36 + 400) ≈ 20,9 m/s. Ra 20 m/s là quên v0; ra 26 m/s là cộng thẳng hai vận tốc vuông góc."},
        {"type": MC,
         "question": "Hai vật cùng được ném ngang từ độ cao 20 m, lấy g = 10 m/s². Vật A có v0 = 5 m/s, vật B có v0 = 20 m/s. Kết luận đúng là:",
         "options": ["A chạm đất trước B",
                     "B chạm đất trước A",
                     "Hai vật chạm đất cùng lúc, B bay xa gấp bốn lần A",
                     "Hai vật chạm đất cùng lúc và cùng tầm xa"],
         "answer": 2,
         "explanation": "t = √(2×20/10) = 2 s như nhau cho cả hai; tầm xa L = v0·t nên A được 10 m, B được 40 m — gấp bốn vì v0 gấp bốn."},
        {"type": MC,
         "question": "Một vật được ném ngang từ độ cao 5 m với v0 = 10 m/s, lấy g = 10 m/s². Tầm xa của vật là:",
         "options": ["5 m", "10 m", "20 m", "50 m"],
         "answer": 1,
         "explanation": "t = √(2×5/10) = 1 s, rồi L = v0·t = 10×1 = 10 m. Ra 50 m là quên dấu căn khi tính t (lấy t = 5 s); ra 5 m là lẫn tầm xa với độ cao."},
        {"type": MC,
         "question": "Hai quả bóng được đá từ mặt đất với cùng tốc độ, một quả hợp góc 30°, quả kia hợp góc 60° với phương ngang (bỏ qua lực cản). So sánh nào đúng?",
         "options": ["Quả 60° bay xa hơn vì lên cao hơn",
                     "Quả 30° bay xa hơn vì có thành phần ngang lớn hơn",
                     "Hai quả cùng tầm xa; quả 60° lên cao hơn và bay lâu hơn",
                     "Hai quả cùng thời gian bay và cùng tầm xa"],
         "answer": 2,
         "explanation": "L = v0²·sin2α/g mà sin60° = sin120° nên tầm xa bằng nhau (hai góc phụ nhau). Nhưng t = 2v0·sinα/g và H = v0²·sin²α/2g đều chứa sinα nên quả 60° bay lâu hơn và lên cao gấp ba."},
        {"type": MC,
         "question": "Vật ném xiên từ mặt đất với v0 = 20 m/s, góc 60° so với phương ngang. Tại điểm cao nhất, vận tốc của vật là:",
         "options": ["0", "10 m/s, nằm ngang", "17,3 m/s, nằm ngang", "20 m/s, nằm ngang"],
         "answer": 1,
         "explanation": "Ở đỉnh vy = 0 nhưng vx = v0·cos60° = 10 m/s ≠ 0. Ra 0 là nhầm vy = 0 với v = 0; ra 17,3 m/s là dùng sin60° thay cho cos60°."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Chuyển động ném"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Phân tích chuyển động ném ngang và ném xiên theo hai phương; thời gian bay, tầm cao, tầm xa và vận tốc của vật bị ném",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
