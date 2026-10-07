#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts <bundle.json>
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Kính lúp. Bài tập thấu kính",
    "duration_minutes": 10,
    "questions": [
        {"type": MC, "question": "Đặt kính lúp sát một con tem rồi nâng kính dần lên, mắt luôn nhìn qua kính. Hình con tem thấy qua kính thay đổi thế nào?",
         "options": ["To dần mãi và luôn cùng chiều với con tem", "To dần, rồi nhoè đi, rồi lộn ngược", "Nhỏ dần đi ngay từ lúc bắt đầu nâng", "Giữ nguyên kích thước, chỉ nét hơn lên"],
         "answer": 1, "explanation": "Con tem còn trong khoảng tiêu cự: ảnh ảo cùng chiều, to dần. Qua tiêu điểm: ảnh nhoè rồi lật ngược (ảnh thật)."},
        {"type": MC, "question": "Một kính lúp có tiêu cự f = 2,5 cm. Số bội giác của kính là:",
         "options": ["10", "0,1", "62,5", "22,5"],
         "answer": 0, "explanation": "G = 25/f = 25/2,5 = 10. Ra 0,1 là chia ngược f/25; ra 62,5 là nhân."},
        {"type": MC, "question": "Đặt kính lúp sát trang bản đồ rồi dịch ra xa; tới một lúc tên phố nhoè hẳn. Nên làm gì?",
         "options": ["Đưa mắt ra thật xa kính cho dễ nhìn", "Tiếp tục dịch kính ra xa trang bản đồ", "Dịch kính lại gần bản đồ một chút", "Đổi kính tiêu cự ngắn hơn, giữ nguyên chỗ đặt"],
         "answer": 2, "explanation": "Nhoè hẳn là bản đồ đã tới gần tiêu điểm; lùi kính lại để bản đồ nằm trong tiêu cự thì ảnh ảo rõ, to trở lại. Đổi kính tiêu cự ngắn hơn mà giữ chỗ cũ thì bản đồ càng nằm ngoài tiêu cự."},
        {"type": MC, "question": "Kính lúp có f = 8 cm. Đặt một bông hoa cách kính 20 cm rồi hứng ảnh trên tờ giấy. Ảnh là:",
         "options": ["Ảnh ảo, cùng chiều, lớn hơn bông hoa", "Ảnh ảo, cùng chiều, nhỏ hơn bông hoa", "Ảnh thật, ngược chiều, lớn hơn bông hoa", "Ảnh thật, ngược chiều, nhỏ hơn bông hoa"],
         "answer": 3, "explanation": "d = 20 cm > 2f = 16 cm nên ảnh thật, ngược chiều, nhỏ hơn vật. Kính lúp chỉ cho ảnh ảo khi vật trong tiêu cự."},
        {"type": MC, "question": "Khi dựng ảnh qua kính lúp, đoạn nối từ thấu kính về ảnh B' phải vẽ thế nào?",
         "options": ["Nét liền, vì ảnh ảo trông rất rõ", "Nét đứt, vì ánh sáng không đi qua đó", "Nét liền, vì ánh sáng quay ngược về B'", "Nét đứt, vì đó là tia sáng yếu hơn"],
         "answer": 1, "explanation": "Đoạn về B' là đường kéo dài ngược của tia ló, không có ánh sáng đi qua, nên vẽ nét đứt."},
        {"type": MC, "question": "Kính M có f = 4 cm, kính N có f = 10 cm. Muốn soi rõ gân trên cánh một con muỗi, nên chọn:",
         "options": ["Kính N, vì tiêu cự dài thì phóng to nhiều hơn", "Kính nào cũng được, vì cả hai đều là kính lúp", "Kính M, vì có G = 6,25 lớn hơn", "Kính N, vì có G = 2,5 lớn hơn"],
         "answer": 2, "explanation": "G = 25/f: G_M = 6,25, G_N = 2,5. Tiêu cự ngắn hơn thì phóng to nhiều hơn."},
        {"type": MC, "question": "Thấu kính hội tụ f = 12 cm, vật cao 2 cm đặt vuông góc trục chính, cách thấu kính 24 cm. Ảnh là:",
         "options": ["Cao 2 cm, ảnh thật, ngược chiều", "Cao 4 cm, ảnh thật, ngược chiều", "Cao 1 cm, ảnh thật, ngược chiều", "Cao 2 cm, ảnh ảo, cùng chiều"],
         "answer": 0, "explanation": "1/d' = 1/12 − 1/24 = 1/24, d' = 24 cm; k = |d'|/d = 1, h' = 2 cm; d' > 0 nên ảnh thật, ngược chiều."},
        {"type": MC, "question": "Kính lúp ghi 4x. Đặt một con tem cách kính 5 cm. Ảnh của con tem:",
         "options": ["Cách kính 25 cm, là ảnh thật", "Cách kính 2,8 cm, là ảnh ảo", "Cách kính 6,25 cm, là ảnh ảo", "Cách kính 25 cm, là ảnh ảo"],
         "answer": 3, "explanation": "f = 25/4 = 6,25 cm; 1/d' = 1/6,25 − 1/5 = −0,04, d' = −25 cm: ảnh ảo, cùng phía con tem, cách kính 25 cm."},
    ],
}
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "KHTN 9", "lesson_title": "Bài 10. Kính lúp. Bài tập thấu kính"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Cấu tạo, số bội giác và cách dùng kính lúp; ba dạng bài tập thấu kính hội tụ",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}
# đối chiếu đáp án bundle với tl-ok trong bài
oks = re.findall(r'id="tl88-q(\d)([a-d])"><label for="tl88-q\d[a-d]" class="tl-opt tl-ok"', theory)
assert [("abcd".index(c)) for _, c in sorted(oks)] == [q["answer"] for q in exam["questions"]], oks
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
