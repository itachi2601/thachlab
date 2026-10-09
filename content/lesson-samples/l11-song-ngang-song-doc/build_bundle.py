#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Sóng ngang, sóng dọc, sự truyền năng lượng",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Loa đầu sân trường phát nhạc, âm truyền theo phương nằm ngang tới tai em. Lớp không khí sát tai em dao động thế nào?",
         "options": ["Qua lại theo phương nằm ngang, dọc phương truyền âm",
                     "Lên xuống theo phương thẳng đứng, vuông góc phương truyền",
                     "Chạy một mạch từ loa tới tai em rồi dừng lại ở đó",
                     "Đứng yên hoàn toàn; chỉ có màng loa là dao động"],
         "answer": 0,
         "explanation": "Sóng âm trong không khí là sóng dọc: lớp khí bị nén – dãn, dao động qua lại dọc phương truyền."},
        {"type": MC,
         "question": "Đặt một điện thoại đang đổ chuông, màn hình sáng, vào bình kín rồi hút dần không khí ra. Em thấy gì?",
         "options": ["Tiếng chuông to dần vì không còn không khí cản lại",
                     "Tiếng chuông giữ nguyên vì vỏ bình rắn vẫn truyền âm",
                     "Cả tiếng chuông lẫn ánh sáng màn hình cùng tắt dần",
                     "Tiếng chuông nhỏ dần; màn hình vẫn sáng như cũ"],
         "answer": 3,
         "explanation": "Sóng âm là sóng cơ, cần phần tử môi trường: ít không khí thì tiếng nhỏ dần. Ánh sáng là sóng điện từ, truyền được trong chân không."},
        {"type": MC,
         "question": "Vẩy dây nhảy cùng nhịp (cùng tần số), lần sau biên độ gấp đôi lần trước. Năng lượng sóng truyền qua mỗi giây gấp mấy lần?",
         "options": ["2 lần", "4 lần", "Không đổi, vì cùng tần số", "√2 lần"],
         "answer": 1,
         "explanation": "Năng lượng sóng tỉ lệ A²: 2² = 4 lần."},
        {"type": MC,
         "question": "Dây dài treo thẳng đứng từ trần. Em lắc đầu dưới qua lại theo phương nằm ngang; sóng chạy dọc dây lên trần. Sóng trên dây là:",
         "options": ["Sóng dọc, vì sóng truyền theo phương thẳng đứng",
                     "Sóng ngang, vì dao động vuông góc phương truyền",
                     "Sóng dọc, vì sợi dây được treo dọc theo tường",
                     "Không phải sóng, vì dây không được căng nằm ngang"],
         "answer": 1,
         "explanation": "Tên gọi so phương dao động với phương truyền: dao động nằm ngang, truyền thẳng đứng, vuông góc nhau nên là sóng ngang."},
        {"type": MC,
         "question": "Sóng âm trong không khí (v = 340 m/s) có vùng nén cách vùng dãn gần nhất 0,2 m. Tần số âm là:",
         "options": ["1700 Hz", "425 Hz", "850 Hz", "68 Hz"],
         "answer": 2,
         "explanation": "Nén – dãn gần nhất cách λ/2 nên λ = 0,4 m; f = v/λ = 340/0,4 = 850 Hz."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 11", "lesson_title": "Bài 9. Sóng ngang, sóng dọc, sự truyền năng lượng của sóng cơ"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Sóng ngang · sóng dọc · vùng nén – dãn · môi trường truyền sóng · năng lượng và cường độ sóng",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
