#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho GCPT – Bài 5 Gia công bằng laser (LBM).
Dùng: python3 build_figs.py && python3 build_bundle.py  rồi
      npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
Chưa có id bài (migration lớp gcpt chờ chạy); khi có: upload-lesson.mts … --lesson <id>.
Ví dụ 3 kW / 0,2 mm / 3 m/phút là ví dụ tự soạn.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Tự kiểm tra nhanh — Gia công bằng laser (LBM)",
    "duration_minutes": 5,
    "questions": [
        {"type": MC,
         "question": "Vì sao chùm laser làm nóng chảy kim loại dù ánh sáng không có khối lượng?",
         "options": ["Ánh sáng đẩy cơ học rất mạnh", "Hội tụ thành điểm rất nhỏ nên cường độ cực lớn, kim loại hấp thụ nhiệt",
                     "Ánh sáng hoà tan kim loại", "Laser tạo tia lửa điện"],
         "answer": 1,
         "explanation": "Cơ chế là nhiệt: I = P/(πd²/4), d nhỏ thì I lớn."},
        {"type": MC,
         "question": "Cắt tấm inox cần cạnh sáng để hàn ngay. Khí trợ hợp lý nhất là:",
         "options": ["Ôxy", "Nitơ áp suất cao", "Không cần khí", "Hiđrô"],
         "answer": 1,
         "explanation": "Nitơ chỉ thổi kim loại lỏng đi, không phản ứng nên cạnh sáng, không ôxit."},
        {"type": MC,
         "question": "Giữ nguyên công suất, đường kính điểm hội tụ giảm một nửa. Cường độ chùm:",
         "options": ["Gấp đôi", "Gấp bốn", "Giảm một nửa", "Không đổi"],
         "answer": 1,
         "explanation": "I tỷ lệ với 1/d²: d nhỏ một nửa thì I gấp 4 lần."},
        {"type": MC,
         "question": "P = 2 kW, v = 3 m/phút. Năng lượng đường E = P/v là:",
         "options": ["40 J/mm", "20 J/mm", "667 J/mm", "6 J/mm"],
         "answer": 0,
         "explanation": "3 m/phút = 50 mm/s; E = 2000/50 = 40 J/mm."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Các phương pháp gia công phi truyền thống", "lesson_title": "Bài 5. Gia công bằng laser (LBM)"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "CO₂, fiber, Nd:YAG · khí trợ · cường độ và năng lượng đường · HAZ · an toàn laser",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự lý thuyết,", len(exam["questions"]), "câu")
