#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Lực cản và lực nâng",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Vận động viên trượt băng tốc độ cúi gập người, mặc đồ bó sát, đội mũ thuôn dài. Mục đích chính là:",
         "options": ["Tăng trọng lượng ép xuống mặt băng", "Giảm ma sát giữa lưỡi giày và mặt băng",
                     "Giảm lực cản của không khí nhờ hình dạng thuôn, ít hứng gió", "Tăng lực đẩy Archimedes của không khí để người nhẹ đi"],
         "answer": 2,
         "explanation": "Lực cản của chất lưu phụ thuộc hình dạng và tốc độ. Tư thế cúi, đồ bó, mũ thuôn làm giảm lực cản của không khí; trọng lượng, ma sát của lưỡi giày và lực đẩy của không khí gần như không đổi."},
        {"type": MC,
         "question": "Thép có khối lượng riêng gấp gần 8 lần nước, vậy mà tàu thép vẫn nổi. Lí do đúng là:",
         "options": ["Thép đóng tàu là loại nhẹ hơn nước", "Khi tàu nổi yên, lực đẩy Archimedes lớn hơn trọng lượng tàu",
                     "Không khí nâng phần thân tàu nằm trên mặt nước", "Thân tàu rỗng chiếm chỗ rất nhiều nước; khi nổi yên, lực đẩy bằng trọng lượng tàu"],
         "answer": 3,
         "explanation": "F_A tính theo thể tích nước bị chiếm chỗ. Thân rỗng chiếm chỗ nhiều nước nên chỉ cần chìm một phần là F_A = P. Khi nổi yên hai lực bằng nhau, không phải F_A lớn hơn."},
        {"type": MC,
         "question": "Người nhảy dù đã mở dù, đang rơi đều 5 m/s (bỏ qua lực đẩy Archimedes của không khí). Nhận xét đúng:",
         "options": ["Lực cản bằng trọng lượng người và dù; hợp lực bằng 0", "Không còn lực nào tác dụng lên người và dù",
                     "Lực cản lớn hơn trọng lượng, nên người không nhanh thêm được", "Lực cản nhỏ hơn trọng lượng, vì người vẫn đang đi xuống"],
         "answer": 0,
         "explanation": "Vận tốc không đổi thì gia tốc bằng 0, hợp lực bằng 0: lực cản đúng bằng trọng lượng. Trọng lực vẫn còn; lực cản lớn hơn thì người chậm dần, nhỏ hơn thì nhanh dần."},
        {"type": MC,
         "question": "Khối gỗ thể tích 2,0 dm³ nổi trên nước, phần chìm 1,2 dm³. Lấy ρ nước = 1000 kg/m³, g = 10 m/s². Lực đẩy Archimedes là:",
         "options": ["20 N", "12 000 N", "8 N", "12 N"],
         "answer": 3,
         "explanation": "Chỉ phần chìm chiếm chỗ nước: F_A = 1000 · 10 · 1,2·10⁻³ = 12 N. Ra 20 N là lấy thể tích cả khối; 12 000 N là quên đổi dm³ ra m³; 8 N là lấy phần nổi."},
        {"type": MC,
         "question": "Quả nặng chìm hẳn trong bể được hạ từ độ sâu 20 cm xuống 60 cm (chưa chạm đáy). Lực đẩy Archimedes lên nó:",
         "options": ["Tăng gấp 3, vì sâu gấp 3", "Không đổi", "Giảm, vì nước phía trên đè nặng hơn", "Tăng thêm một lượng bằng áp suất khí quyển"],
         "answer": 1,
         "explanation": "Lực đẩy do chênh lệch áp suất giữa mặt dưới và mặt trên, Δp = ρgΔh, không đổi khi hạ sâu; F_A = ρgV không chứa độ sâu h."},
        {"type": MC,
         "question": "Khối nhôm treo vào lực kế chỉ 5,4 N ngoài không khí (ρ nhôm = 2700 kg/m³, ρ nước = 1000 kg/m³, g = 10 m/s²). Nhúng một nửa thể tích vào nước, lực kế chỉ:",
         "options": ["3,4 N", "1,0 N", "4,4 N", "5,4 N"],
         "answer": 2,
         "explanation": "V = 0,54/2700 = 2·10⁻⁴ m³; phần chìm 10⁻⁴ m³ nên F_A = 1 N; T = 5,4 − 1 = 4,4 N. Ra 3,4 N là lấy V cả vật."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 19. Lực cản và lực nâng"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Lực cản của chất lưu, ba giai đoạn rơi và tốc độ giới hạn; lực đẩy Archimedes, chênh lệch áp suất; nổi, lơ lửng, chìm",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
