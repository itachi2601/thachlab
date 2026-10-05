#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Làm quen với Vật lí",
    "duration_minutes": 6,
    "questions": [
        {"type": MC,
         "question": "Ấm nước sắp sôi: nắp ấm rung, hơi nước bay ra, phân tử nước chuyển động nhanh hơn. Phần nào thuộc phạm vi nghiên cứu của vật lí?",
         "options": ["Chỉ nắp ấm rung, vì ta nhìn thấy nó",
                     "Chỉ chuyển động của phân tử, vì đó mới là gốc",
                     "Cả hai, và mối liên hệ giữa chúng",
                     "Không phần nào, đây là việc của hoá học"],
         "answer": 2,
         "explanation": "Vật lí nghiên cứu vận động và năng lượng ở mọi cấp độ: từ phân tử chuyển động nhiệt tới nắp ấm rung, và cách cái này gây ra cái kia. Nước hoá hơi vẫn là nước, không có chất mới."},
        {"type": MC,
         "question": "Cặp nào phân loại đúng?",
         "options": ["Phân tử nước: vi mô; chiếc ấm nước: vĩ mô",
                     "Hạt cát: vi mô, vì rất nhỏ",
                     "Vũ trụ: ngoài phạm vi vật lí, vì quá lớn",
                     "Nguyên tử: vĩ mô, vì cũng là vật chất"],
         "answer": 0,
         "explanation": "Phân tử không thấy bằng mắt thường nên là vi mô; chiếc ấm thấy rõ nên là vĩ mô. Hạt cát vẫn nhìn thấy bằng mắt (vĩ mô); vũ trụ nằm trong đối tượng của vật lí."},
        {"type": MC,
         "question": "Lan thấy quyển sách rơi nhanh hơn tờ giấy và nói: \"Chắc do không khí cản tờ giấy nhiều hơn.\" Câu nói này thuộc bước nào của quy trình nghiên cứu?",
         "options": ["Quan sát, suy luận", "Hình thành giả thuyết", "Kiểm tra giả thuyết", "Rút ra kết luận"],
         "answer": 1,
         "explanation": "Đây là một dự đoán có thể kiểm tra mà chưa kiểm tra: đó là giả thuyết. \"Sách rơi nhanh hơn\" mới là quan sát; chưa có thí nghiệm nào nên chưa thể kết luận."},
        {"type": MC,
         "question": "Lí thuyết dự đoán máy CNC chạy dao hết 30 s, máy thật chạy hết 33 s. Kết luận hợp lí nhất?",
         "options": ["Máy hỏng nên phải bỏ kết quả đo",
                     "Lí thuyết sai hoàn toàn nên bỏ phép tính",
                     "Phép đo sai vì lí thuyết đã tính chắc chắn",
                     "Mô hình thiếu yếu tố; sửa rồi đo lại"],
         "answer": 3,
         "explanation": "Phép tính chỉ đúng với điều đã đưa vào mô hình (chạy đều). Chênh 3 s gợi ý yếu tố bị bỏ sót: máy giảm tốc ở 4 góc, mỗi góc khoảng 0,75 s. Lí thuyết và thực nghiệm bổ sung nhau."},
        {"type": MC,
         "question": "Nhóm giả thuyết: gắn thêm quả nặng thì xe đồ chơi chạy nhanh hơn. Đo xong, xe nặng hơn lại chậm hơn. Điều nào đúng?",
         "options": ["Giả thuyết bị bác bỏ; nhóm nên đặt giả thuyết mới",
                     "Thí nghiệm hỏng, làm lại tới khi xe nặng chạy nhanh hơn",
                     "Giả thuyết vẫn đúng, chỉ cần ghi số liệu theo dự đoán",
                     "Không rút ra được gì, vì giả thuyết sai"],
         "answer": 0,
         "explanation": "Kết quả trái dự đoán cho biết thêm điều mới (có thể xe nặng hơn chịu ma sát lớn hơn). Chỉnh kết quả cho hợp ý muốn không phải là khoa học; không khớp thì điều chỉnh hoặc bác bỏ giả thuyết."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 1. Làm quen với Vật lí"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Đối tượng và mục tiêu của vật lí; ảnh hưởng tới đời sống, kĩ thuật; phương pháp thực nghiệm, lí thuyết; quy trình 5 bước",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
