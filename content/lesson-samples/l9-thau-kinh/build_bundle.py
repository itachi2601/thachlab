#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts <bundle.json>
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Thấu kính",
    "duration_minutes": 10,
    "questions": [
        {"type": MC, "question": "Kính lão có phần giữa dày hơn phần rìa. Hứng ánh nắng qua kính lên tờ giấy, dịch giấy ra xa dần. Có lúc trên giấy thấy:",
         "options": ["Một chấm sáng nhỏ, rất chói", "Một vùng tối hình tròn, viền rất rõ", "Vùng sáng loang rộng dần, không lúc nào thu nhỏ", "Chỉ có bóng của chiếc kính, không có vết sáng"],
         "answer": 0, "explanation": "Giữa dày, rìa mỏng là thấu kính hội tụ: chùm nắng gần song song gom về một chấm nhỏ tại tiêu điểm."},
        {"type": MC, "question": "Dựng ảnh qua thấu kính hội tụ bằng tia qua quang tâm và tia song song trục chính, hai tia ló loe xa nhau, không cắt nhau sau thấu kính. Vật đang nằm ở đâu?",
         "options": ["Xa hơn 2f kể từ thấu kính", "Đúng tại khoảng cách 2f", "Giữa F và vị trí cách O một đoạn 2f", "Giữa quang tâm O và F"],
         "answer": 3, "explanation": "Khi d < f, tia qua O dốc hơn tia qua F' nên hai tia ló loe ra; phải kéo dài ngược mới gặp nhau, cho ảnh ảo."},
        {"type": MC, "question": "Thấu kính hội tụ có f = 8 cm, vật đặt cách thấu kính 12 cm. Ảnh cách thấu kính:",
         "options": ["4,8 cm", "24 cm", "20 cm", "4 cm"],
         "answer": 1, "explanation": "1/d' = 1/8 − 1/12 = 1/24 nên d' = 24 cm, ảnh thật. Ra 4,8 cm là cộng 1/8 + 1/12 thay vì trừ."},
        {"type": MC, "question": "Đặt ngọn nến cách thấu kính hội tụ (f = 10 cm) một khoảng 6 cm. Dịch tấm màn phía sau thấu kính từ sát kính ra thật xa. Trên màn:",
         "options": ["Có ảnh nến ngược chiều, lớn hơn nến", "Có ảnh nến cùng chiều, lớn hơn nến", "Không lúc nào có ảnh rõ của ngọn nến", "Có ảnh rõ khi màn cách kính đúng 15 cm"],
         "answer": 2, "explanation": "d < f cho ảnh ảo (d' = −15 cm, cùng phía với nến), chỉ nhìn qua kính mới thấy, không hứng được trên màn."},
        {"type": MC, "question": "Thấu kính hội tụ đang cho ảnh rõ của bóng đèn trên màn. Dán giấy đen che nửa dưới thấu kính. Ảnh trên màn:",
         "options": ["Vẫn đủ hình, tối hơn", "Chỉ còn nửa trên", "Chỉ còn nửa dưới", "Mất hẳn, màn tối đen"],
         "answer": 0, "explanation": "Mỗi điểm của vật gửi tia tới khắp mặt kính; nửa còn lại vẫn cho đủ ảnh, chỉ ít ánh sáng hơn nên tối hơn."},
        {"type": MC, "question": "Thấu kính phân kì có tiêu cự 20 cm; vật đặt cách thấu kính 30 cm. Ảnh của vật:",
         "options": ["thật, cách thấu kính 60 cm", "thật, cách thấu kính 12 cm", "ảo, cách thấu kính 60 cm", "ảo, cách thấu kính 12 cm"],
         "answer": 3, "explanation": "Thay f = −20: 1/d' = −1/20 − 1/30 = −1/12, d' = −12 cm: ảnh ảo cách kính 12 cm. Ra 60 cm là quên dấu trừ của f."},
        {"type": MC, "question": "Vật cao 3 cm đặt cách thấu kính hội tụ (f = 10 cm) một khoảng 30 cm. Ảnh cao:",
         "options": ["6 cm", "1,5 cm", "4,5 cm", "1 cm"],
         "answer": 1, "explanation": "1/d' = 1/10 − 1/30 = 1/15, d' = 15 cm; h' = 3·15/30 = 1,5 cm."},
    ],
}
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "KHTN 9", "lesson_title": "Bài 8. Thấu kính"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Đặc điểm thấu kính hội tụ, phân kì và tiêu cự; dựng ảnh của vật qua thấu kính; công thức thấu kính và số phóng đại",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
