#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho GCPT – Bài 4 Gia công điện hoá (ECM).
Dùng: python3 build_figs.py && python3 build_bundle.py  rồi
      npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
Chưa có id bài (migration lớp gcpt chờ chạy); khi có: upload-lesson.mts … --lesson <id>.
Ví dụ hốc 2 cm² / 200 A là ví dụ tự soạn; hằng số Faraday, A, ρ của sắt là số chuẩn.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Tự kiểm tra nhanh — Gia công điện hoá (ECM)",
    "duration_minutes": 5,
    "questions": [
        {"type": MC,
         "question": "Trong ECM, phôi nối với cực nào và điều gì xảy ra ở đó?",
         "options": ["Cực âm, sinh khí hiđrô", "Cực dương, kim loại tan thành ion",
                     "Cực dương, phôi nóng chảy bởi tia lửa", "Cực âm, kim loại bám thêm vào phôi"],
         "answer": 1,
         "explanation": "Phôi là cực dương (anode): kim loại mất electron thành ion tan vào dung dịch. Dụng cụ là cực âm."},
        {"type": MC,
         "question": "Vì sao dụng cụ ECM hầu như không mòn?",
         "options": ["Làm bằng vật liệu cứng nhất", "Không chạm phôi và là cực âm, chỉ sinh khí",
                     "Quay chậm", "Được tôi cứng"],
         "answer": 1,
         "explanation": "Dụng cụ không chạm phôi, không là cực dương nên không bị hoà tan; ở đó chỉ có bọt khí H₂."},
        {"type": MC,
         "question": "Giữ nguyên diện tích gia công, tăng dòng gấp đôi. Tốc độ tiến dụng cụ (cùng η) thay đổi thế nào?",
         "options": ["Không đổi", "Gấp đôi", "Giảm một nửa", "Gấp bốn"],
         "answer": 1,
         "explanation": "v = ηAJ/(zFρ), tỷ lệ bậc một với mật độ dòng J."},
        {"type": MC,
         "question": "Phát biểu nào về ECM là SAI?",
         "options": ["Không có vùng ảnh hưởng nhiệt", "Gia công được gốm và nhựa",
                     "Tốc độ bóc không phụ thuộc độ cứng phôi", "Cần dụng cụ thiết kế riêng"],
         "answer": 1,
         "explanation": "Gốm, nhựa không dẫn điện nên không thể làm cực dương."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Các phương pháp gia công phi truyền thống", "lesson_title": "Bài 4. Gia công điện hoá (ECM)"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Nguyên lý anode – cathode · định luật Faraday · khe hở · chọn / không chọn ECM",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự lý thuyết,", len(exam["questions"]), "câu")
