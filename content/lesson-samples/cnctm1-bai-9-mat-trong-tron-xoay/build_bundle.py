#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho CNCTM 1 – Bài 9 Gia công mặt tròn xoay trong.
Dùng: python3 build_figs.py && python3 build_bundle.py  rồi
      npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
Nguồn ý: giáo trình CNCTM của bộ môn (Chương 9). Ví dụ lỗ khoan Ø20 lay rộng, bạc gang Ø40, lỗ Ø12, lỗ Ø150 là ví dụ tự soạn.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Kiểm tra nhanh — Gia công mặt tròn xoay trong",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Vì sao gia công lỗ thường khó hơn gia công mặt ngoài cùng đường kính?",
         "options": ["Vì lỗ luôn cần cấp chính xác cao hơn",
                     "Vì dao nhỏ, kém cứng vững; khó quan sát, khó đo; phoi và nhiệt khó thoát",
                     "Vì không có máy chuyên gia công lỗ", "Vì phôi có lỗ luôn mềm hơn"],
         "answer": 1,
         "explanation": "Dao nằm trong lỗ nên bị giới hạn kích thước, kém cứng vững; lại khó thoát phoi, khó đo."},
        {"type": MC,
         "question": "Khoan lỗ bằng mũi Ø20 nhưng lỗ đo được lớn hơn 20 mm. Nguyên nhân thường gặp là gì?",
         "options": ["Hai lưỡi cắt mài không đều, mũi khoan quay lệch tâm", "Phôi nguội đi sau khi khoan",
                     "Tốc độ quay quá thấp", "Dùng dung dịch trơn nguội"],
         "answer": 0,
         "explanation": "Lưỡi dài hơn cắt xa tâm hơn làm lỗ lay rộng."},
        {"type": MC,
         "question": "Khoan 200 lỗ giống nhau, cần lỗ không xiên. Biện pháp hợp nhất?",
         "options": ["Tăng lượng chạy dao", "Dùng mũi khoan dài hơn",
                     "Dùng đồ gá có bạc dẫn hướng mũi khoan", "Doa lại cho thẳng"],
         "answer": 2,
         "explanation": "Bạc dẫn giữ mũi khoan đúng vị trí, đúng hướng. Doa đi theo lỗ cũ nên không làm lỗ thẳng lại."},
        {"type": MC,
         "question": "Phương pháp nào KHÔNG sửa được sai lệch vị trí (đường tâm xiên, lệch) của lỗ có sẵn?",
         "options": ["Khoét", "Tiện lỗ", "Mài lỗ", "Doa"],
         "answer": 3,
         "explanation": "Dao doa cắt lớp mỏng, thường lắp tùy động nên đi theo tâm lỗ có sẵn."},
        {"type": MC,
         "question": "Lỗ then hoa thông suốt, sản xuất hàng chục nghìn chiếc. Nên gia công bằng gì?",
         "options": ["Tiện lỗ", "Chuốt", "Mài khôn", "Khoan rồi doa"],
         "answer": 1,
         "explanation": "Chuốt hợp lỗ thông, tiết diện không đổi (kể cả then hoa), sản lượng lớn."},
        {"type": MC,
         "question": "Khi mài khôn, nếu độ vượt của thỏi đá ra khỏi hai đầu lỗ quá lớn thì lỗ bị gì?",
         "options": ["Hai đầu lỗ tóp lại", "Lỗ bị xiên", "Không ảnh hưởng", "Hai đầu lỗ loe ra"],
         "answer": 3,
         "explanation": "Hai đầu bị đá mài lâu hơn nên loe; độ vượt quá nhỏ thì hai đầu tóp."},
        {"type": MC,
         "question": "Bạc gang có lỗ đúc sẵn Ø40, cần cấp 8, Ra 1,6, đồng tâm mặt ngoài, hàng loạt vừa. Trình tự hợp lý?",
         "options": ["Khoét thô → khoét tinh (cùng lần gá với mặt ngoài) → doa bán tinh", "Khoan → doa tinh",
                     "Chuốt một lượt", "Doa tinh ngay trên lỗ đúc"],
         "answer": 0,
         "explanation": "Lỗ đúc sẵn không khoan; khoét sửa đường tâm; doa bán tinh đạt cấp 8–7, Ra 1,6."},
        {"type": MC,
         "question": "Lỗ bắt bulông trên phôi đặc chỉ cần cấp 13, Rz 30 µm. Cách nào ít công nhất mà vẫn đạt yêu cầu?",
         "options": ["Khoan rồi doa tinh", "Khoét rồi mài lỗ", "Chỉ khoan", "Tiện tinh mỏng"],
         "answer": 2,
         "explanation": "Khoan đạt cấp 14–12, Rz 40–20; cấp 13, Rz 30 nằm trong khoảng đó."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Công nghệ chế tạo máy 1", "lesson_title": "Bài 9. Gia công mặt tròn xoay trong"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Khoan · khoét, doa · tiện lỗ · chuốt · mài lỗ, mài khôn · trình tự gia công lỗ",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự lý thuyết,", len(exam["questions"]), "câu")
