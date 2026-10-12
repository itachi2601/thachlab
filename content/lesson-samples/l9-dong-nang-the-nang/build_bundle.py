#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts <bundle.json>
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Động năng. Thế năng",
    "duration_minutes": 10,
    "questions": [
        {"type": MC, "question": "Chậu cây đứng yên trên lan can tầng 8. Chậu có năng lượng không?",
         "options": ["Không, vì chậu đang đứng yên", "Có, vì chậu đang ở trên cao", "Chưa có, chỉ có khi chậu bắt đầu rơi", "Có, và ở tầng 2 hay tầng 8 cũng như nhau"],
         "answer": 1, "explanation": "Vật ở trên cao so với mặt đất có thế năng, kể cả khi đứng yên. Ở càng cao thế năng càng lớn."},
        {"type": MC, "question": "Ô tô 1 tấn chạy 36 km/h. Động năng của ô tô là",
         "options": ["648 000 J", "5 000 J", "50 000 J", "100 000 J"],
         "answer": 2, "explanation": "v = 36 : 3,6 = 10 m/s; Wđ = ½·1 000·10² = 50 000 J. 648 000 J là quên đổi km/h; 5 000 J là quên bình phương; 100 000 J là quên ½."},
        {"type": MC, "question": "Quả cam 200 g treo trên cành, cao 3 m so với mặt đất. Chọn mốc ở mặt đất. Thế năng của quả cam là",
         "options": ["6 000 J", "0,6 J", "3 J", "6 J"],
         "answer": 3, "explanation": "P = 10·0,2 = 2 N; Wt = P·h = 2·3 = 6 J. 0,6 J là quên P = 10m; 6 000 J là để khối lượng bằng gam."},
        {"type": MC, "question": "Một xe máy tăng tốc từ 30 km/h lên 60 km/h. Động năng của xe",
         "options": ["tăng 2 lần", "tăng 4 lần", "không đổi, vì khối lượng không đổi", "tăng 8 lần"],
         "answer": 1, "explanation": "Wđ tỉ lệ với v²: tốc độ gấp 2 thì động năng gấp 2² = 4."},
        {"type": MC, "question": "Quyển sách 0,5 kg nằm trên mặt bàn cao 0,8 m so với sàn. Chọn mặt bàn làm mốc. Thế năng của quyển sách là",
         "options": ["0 J", "4 J", "0,4 J", "5 J"],
         "answer": 0, "explanation": "Sách nằm đúng ở mốc nên h = 0, Wt = 0. 4 J là khi chọn mốc ở sàn."},
        {"type": MC, "question": "Một hành khách ngồi yên trên toa tàu đang chạy. Lấy toa tàu làm mốc, động năng của hành khách",
         "options": ["lớn, vì tàu đang chạy nhanh", "chưa tính được vì thiếu khối lượng tàu", "bằng 0", "bằng thế năng của hành khách"],
         "answer": 2, "explanation": "So với toa tàu, khách đứng yên nên v = 0, Wđ = 0. So với sân ga thì khách có động năng."},
        {"type": MC, "question": "Quả bóng 0,5 kg đang bay ở độ cao 2 m so với mặt đất, tốc độ 4 m/s. Chọn mốc ở mặt đất. Động năng và thế năng của bóng lúc đó là",
         "options": ["Wđ = 1 J, Wt = 10 J", "Wđ = 8 J, Wt = 10 J", "Wđ = 4 J, Wt = 1 J", "Wđ = 4 J, Wt = 10 J"],
         "answer": 3, "explanation": "Wđ = ½·0,5·4² = 4 J; Wt = 10·0,5·2 = 10 J."},
    ],
}
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "KHTN 9", "lesson_title": "Bài 2. Động năng. Thế năng"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Động năng Wđ = ½mv²; thế năng trọng trường Wt = Ph = 10mh; mốc thế năng và vật làm mốc",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
