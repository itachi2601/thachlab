#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho CNCTM 1 – Bài 10 (Gia công ren).
Dùng: python3 build_figs.py && python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
Nguồn ý: giáo trình CNCTM của bộ môn (Chương 10). Phiếu giao việc, ví dụ M10/M12 là ví dụ tự soạn.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Kiểm tra nhanh — Gia công ren",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Bước ren P là:",
         "options": ["Khoảng cách hai đỉnh ren kề nhau, đo song song với trục", "Quãng một mối ren đi được sau một vòng",
                     "Hiệu giữa đường kính ngoài và đường kính trong", "Chiều cao tam giác cơ sở của ren"],
         "answer": 0,
         "explanation": "P đo dọc trục giữa hai đỉnh kề nhau; quãng đi sau một vòng là bước xoắn = k·P."},
        {"type": MC,
         "question": "Ren 2 đầu mối có bước ren P = 4 mm. Bước xoắn bằng:",
         "options": ["2 mm", "4 mm", "8 mm", "16 mm"],
         "answer": 2,
         "explanation": "Bước xoắn = số đầu mối × bước ren = 2 × 4 = 8 mm."},
        {"type": MC,
         "question": "Khi tiện thô ren tam giác, nên tiến dao theo cách nào?",
         "options": ["Hướng kính, hai lưỡi cùng cắt", "Hướng xiên, dao chỉ cắt một bên",
                     "Dọc trục, không ăn sâu", "Tiến tay tuỳ ý"],
         "answer": 1,
         "explanation": "Hướng xiên: một lưỡi cắt, phoi thoát dễ, dao lâu mòn → cắt thô; hướng kính dùng cắt tinh."},
        {"type": MC,
         "question": "Tiện ren thang T32×6 trên máy tiện vạn năng. Dùng dao thế nào?",
         "options": ["Một dao prôfin, ăn sâu bằng tiến ngang", "Bộ 3 hoặc 4 dao (thô, cắt chiều cao, định hình tinh)",
                     "Bàn ren", "Tarô ren thang"],
         "answer": 1,
         "explanation": "Ren thang bước lớn hơn 3 mm cắt bằng bộ 3 hoặc 4 dao; một dao prôfin chỉ cho bước đến 3 mm."},
        {"type": MC,
         "question": "Dụng cụ nào dùng để cắt ren trong lỗ đường kính khoảng 4–30 mm?",
         "options": ["Bàn ren", "Bàn cán ren", "Tarô", "Dao phay đĩa"],
         "answer": 2,
         "explanation": "Tarô chuyên cắt ren trong đường kính nhỏ; bàn ren và bàn cán làm ren ngoài."},
        {"type": MC,
         "question": "Trước khi cắt ren M16 bằng bàn ren, trục nên được tiện tới:",
         "options": ["Ø16,3 mm", "Ø16,0 mm", "Ø15,85 mm", "Ø14,0 mm"],
         "answer": 2,
         "explanation": "Nhỏ hơn d khoảng 0,1–0,2 mm (15,8–15,9) để tránh nở ren."},
        {"type": MC,
         "question": "Ưu điểm chính của cán ren so với tiện ren là:",
         "options": ["Làm được mọi biên dạng, mọi đường kính", "Ren bền hơn nhờ thớ bị nén, năng suất cao",
                     "Không cần máy chuyên dùng", "Chính xác hơn mài ren"],
         "answer": 1,
         "explanation": "Cán ren là biến dạng dẻo: thớ không bị cắt đứt, dễ tự động hoá nên năng suất cao."},
        {"type": MC,
         "question": "Đo đường kính trung bình d₂ của ren ngoài bằng:",
         "options": ["Thước cặp kẹp hai đỉnh ren", "Panme đo ren", "Dưỡng ren", "Calip nút"],
         "answer": 1,
         "explanation": "Panme đo ren (hoặc đồng hồ đo ren) đo d₂; dưỡng kiểm bước và góc; calip nút kiểm ren trong."},
    ],
}


bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Công nghệ chế tạo máy 1", "lesson_title": "Bài 10. Gia công ren"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Thông số ren · tiện ren · tarô, bàn ren · phay, cán, mài ren · kiểm tra ren",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự lý thuyết,", len(exam["questions"]), "câu")

