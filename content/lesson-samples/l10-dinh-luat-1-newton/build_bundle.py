#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Định luật 1 Newton",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Ô tô chạy thẳng đều 60 km/h trên đường nằm ngang. Hợp lực tác dụng lên xe:",
         "options": ["Bằng 0",
                     "Hướng về phía trước, vì xe đang chạy về phía trước",
                     "Hướng về phía sau, vì xe chịu lực cản",
                     "Bằng lực kéo của động cơ"],
         "answer": 0,
         "explanation": "Thẳng đều nghĩa là vận tốc không đổi nên hợp lực bằng 0: lực kéo bằng lực cản, lực đỡ bằng trọng lực. Chọn 'về phía trước' là mắc lỗi 'chạy thì phải có lực theo chiều chạy'."},
        {"type": MC,
         "question": "Xe buýt đang chạy thẳng thì rẽ gấp sang trái. Hành khách đứng không vịn bị xô về phía nào?",
         "options": ["Phía trước", "Phía sau", "Bên trái", "Bên phải"],
         "answer": 3,
         "explanation": "Xe và chân đổi hướng sang trái, thân người giữ hướng chuyển động cũ do quán tính nên so với xe bị lệch sang phải. Phía trước là phanh gấp, phía sau là tăng tốc đột ngột."},
        {"type": MC,
         "question": "Hòn đá vừa rời tay, đang bay thẳng lên (bỏ qua lực cản không khí). Lực tác dụng lên hòn đá là:",
         "options": ["Lực ném hướng lên và trọng lực",
                     "Chỉ có trọng lực, hướng xuống",
                     "Lực ném lớn hơn trọng lực nên đá đi lên",
                     "Không có lực nào, vì đá đang bay tự do"],
         "answer": 1,
         "explanation": "Tay chỉ tác dụng lực khi còn chạm đá. Đá đi lên nhờ quán tính và chậm dần vì trọng lực ngược chiều chuyển động."},
        {"type": MC,
         "question": "Quyển sách nằm yên trên mặt bàn nằm ngang. Phát biểu nào đúng?",
         "options": ["Không có lực nào tác dụng lên sách",
                     "Chỉ có trọng lực, nhưng sách nhẹ nên không rơi",
                     "Có trọng lực và lực đỡ của bàn, hợp lực bằng 0",
                     "Lực đỡ của bàn lớn hơn trọng lực"],
         "answer": 2,
         "explanation": "Đứng yên là trạng thái cân bằng: có lực nhưng hợp lực bằng 0, không phải 'không có lực'."},
        {"type": MC,
         "question": "Xe tải 5 tấn chạy thẳng đều trên đường ngang với tốc độ 54 km/h, lực cản bằng 0,04 trọng lượng xe, g = 10 m/s². Lực kéo của động cơ là:",
         "options": ["50 000 N", "2160 N", "2000 N", "0 N"],
         "answer": 2,
         "explanation": "P = 50 000 N, Fc = 0,04P = 2000 N; thẳng đều nên Fk = Fc = 2000 N. 50 000 N là trọng lượng; 2160 N là lấy nhầm 0,04 × 54 000 (đưa tốc độ vào); 0 N là nhầm 'hợp lực bằng 0' thành 'lực kéo bằng 0'."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 14. Định luật 1 Newton"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Thí nghiệm Galilei, định luật 1 Newton, ý nghĩa của lực và quán tính trong đời sống",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
