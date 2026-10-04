#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Thế năng điện",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Hai hạt sơn giống hệt nhau cùng rời đầu súng phun tĩnh điện, cùng bám vào một điểm N; một hạt bay thẳng, một hạt lượn cong. Chỉ xét lực điện, công của lực điện làm mỗi hạt dịch chuyển:",
         "options": ["Hạt bay cong lớn hơn, vì đi quãng dài hơn",
                     "Hạt bay thẳng lớn hơn, vì luôn đi đúng hướng lực",
                     "Bằng nhau",
                     "Hạt bay cong bằng 0"],
         "answer": 2,
         "explanation": "Công của lực điện không phụ thuộc hình dạng đường đi, chỉ phụ thuộc điểm đầu và điểm cuối. Hai hạt cùng điện tích, cùng đầu, cùng cuối nên công bằng nhau."},
        {"type": MC,
         "question": "Electron (q = −1,6·10⁻¹⁹ C) đi 2 cm ngược chiều đường sức trong điện trường đều E = 1000 V/m. Công của lực điện là:",
         "options": ["−3,2·10⁻¹⁸ J", "+3,2·10⁻¹⁸ J", "0", "+3,2·10⁻¹⁶ J"],
         "answer": 1,
         "explanation": "A = qEd với q < 0 và d = −0,02 m (ngược chiều đường sức): A = (−1,6·10⁻¹⁹)·1000·(−0,02) = +3,2·10⁻¹⁸ J. Ra số âm là bỏ sót một dấu; ra 10⁻¹⁶ là quên đổi cm ra m."},
        {"type": MC,
         "question": "Điện trường đều E = 2000 V/m. Proton đi đoạn MN dài 5 cm, MN hợp với chiều đường sức góc 60°. Công của lực điện là:",
         "options": ["1,6·10⁻¹⁷ J", "1,39·10⁻¹⁷ J", "8,0·10⁻¹⁸ J", "0"],
         "answer": 2,
         "explanation": "d là hình chiếu của MN lên đường sức: d = 5·cos60° = 2,5 cm. A = 1,6·10⁻¹⁹·2000·0,025 = 8,0·10⁻¹⁸ J. Lấy cả 5 cm ra 1,6·10⁻¹⁷ J; chiếu bằng sin ra 1,39·10⁻¹⁷ J."},
        {"type": MC,
         "question": "Một điện tích đi từ M đến N, lực điện sinh công A_MN = +2 mJ. Thế năng điện của điện tích:",
         "options": ["Giảm 2 mJ", "Tăng 2 mJ", "Không đổi", "Tăng hay giảm tuỳ mốc thế năng"],
         "answer": 0,
         "explanation": "A_MN = W_M − W_N = +2 mJ nên W_N nhỏ hơn W_M đúng 2 mJ: thế năng giảm 2 mJ. Đổi mốc làm đổi từng giá trị W nhưng không đổi hiệu W_M − W_N."},
        {"type": MC,
         "question": "Hai bản phẳng nằm ngang cách 4 cm, bản trên dương, E = 2000 V/m. Chọn mốc thế năng ở bản dương. Thế năng của electron (q = −1,6·10⁻¹⁹ C) tại điểm M cách bản âm 1 cm là:",
         "options": ["−3,2·10⁻¹⁸ J", "−9,6·10⁻¹⁸ J", "+3,2·10⁻¹⁸ J", "+9,6·10⁻¹⁸ J"],
         "answer": 3,
         "explanation": "W_M = công lực điện khi electron đi từ M lên bản dương: đi 3 cm ngược chiều đường sức, d = −0,03 m. W_M = (−1,6·10⁻¹⁹)·2000·(−0,03) = +9,6·10⁻¹⁸ J. Ra −3,2·10⁻¹⁸ J là vẫn dùng mốc bản âm."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 11", "lesson_title": "Bài 19. Thế năng điện"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Công của lực điện A = qEd, không phụ thuộc đường đi; thế năng điện, mốc thế năng và A = W_M − W_N",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
