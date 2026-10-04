#!/usr/bin/env python3
"""Đóng gói bundle.json từ theory.html. Chạy sau build_figs.py."""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Điện trường đều",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Giữa hai bản phẳng tích điện trái dấu (xa mép), điểm M sát bản dương, điểm N ở chính giữa. So sánh cường độ điện trường tại M và N.",
         "options": ["Tại M lớn hơn, vì M gần bản dương hơn",
                     "Tại N lớn hơn, vì N nhận điện trường của cả hai bản",
                     "Bằng nhau, cùng phương, cùng chiều",
                     "Bằng độ lớn nhưng ngược chiều nhau"],
         "answer": 2,
         "explanation": "Điện trường giữa hai bản là điện trường đều: vectơ E như nhau tại mọi điểm, không phụ thuộc gần hay xa bản."},
        {"type": MC,
         "question": "Hai bản cách nhau 4 mm, hiệu điện thế U = 12 V. Cường độ điện trường giữa hai bản là",
         "options": ["3 V/m", "0,048 V/m", "30 V/m", "3000 V/m"],
         "answer": 3,
         "explanation": "d = 4 mm = 0,004 m; E = U/d = 12/0,004 = 3000 V/m."},
        {"type": MC,
         "question": "Proton bay ngang vào giữa hai bản nằm ngang, bản trên tích điện âm, bản dưới tích điện dương. Bỏ qua trọng lực. Proton đi theo đường nào?",
         "options": ["Parabol, cong lên phía bản trên",
                     "Parabol, cong xuống phía bản dưới",
                     "Đường thẳng xiên lên phía bản trên",
                     "Đường thẳng, không lệch"],
         "answer": 0,
         "explanation": "E hướng từ bản dương (dưới) lên bản âm (trên). Proton dương chịu lực cùng chiều E, hướng lên; lực không đổi, vuông góc v0 nên quỹ đạo là parabol."},
        {"type": MC,
         "question": "Electron vừa ra khỏi vùng giữa hai bản, bên ngoài không có điện trường. Sau đó nó chuyển động thế nào?",
         "options": ["Tiếp tục cong theo parabol như cũ",
                     "Đi thẳng, theo hướng vận tốc lúc ra khỏi bản",
                     "Quay về đường bay ban đầu",
                     "Dừng lại vì không còn lực"],
         "answer": 1,
         "explanation": "Không còn lực điện nên electron chuyển động thẳng đều theo vận tốc tại mép bản (tiếp tuyến với parabol)."},
        {"type": MC,
         "question": "Electron bay vào chính giữa hai bản dài L = 5,0 cm, cách nhau d = 2,0 cm, U = 91 V, với v0 = 4,0·10^7 m/s song song hai bản (|e| = 1,6·10^-19 C, m = 9,1·10^-31 kg). Độ lệch khi ra khỏi bản là",
         "options": ["0,625 mm", "1,25 mm", "5,0 mm", "2,5 mm"],
         "answer": 0,
         "explanation": "a = |e|U/(md) = 8,0·10^14 m/s²; t = L/v0 = 1,25·10^-9 s; y = at²/2 = 6,25·10^-4 m = 0,625 mm (v0 gấp đôi so với 2,0·10^7 m/s thì y giảm 4 lần)."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 11", "lesson_title": "Bài 18. Điện trường đều"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Điện trường đều giữa hai bản song song và chuyển động của điện tích trong điện trường đều",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
