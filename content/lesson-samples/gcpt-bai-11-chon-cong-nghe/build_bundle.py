#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho GCPT – Bài 11. Chạy: python3 build_figs.py && python3 build_bundle.py
Ý lấy từ kiến thức chung về gia công phi truyền thống; chi tiết mẫu là ví dụ tự soạn. Số liệu chỉ ở mức tham khảo."""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {"title": "Kiểm tra nhanh — Chọn công nghệ gia công", "duration_minutes": 8, "questions": [
    {"type": MC, "question": "Tấm khuôn dập thép đã tôi, lỗ biên dạng xuyên suốt, góc nhọn, một chiếc. Công nghệ hợp nhất?",
     "options": ["Phay cao tốc", "Cắt dây (WEDM)", "Cắt laser", "Cắt plasma"], "answer": 1,
     "explanation": "Thép tôi dẫn điện nên phóng điện cắt được; dây mảnh cắt được góc trong nhỏ, độ chính xác cao. Phay mòn dao và bo góc; laser, plasma thô và có vùng ảnh hưởng nhiệt."},
    {"type": MC, "question": "Composite nền nhựa dày 8 mm. Nhóm công nghệ nào bị loại ngay ở bước vật liệu?",
     "options": ["EDM và WEDM", "Tia nước hạt mài", "Phay bằng dao phù hợp", "Không loại được"], "answer": 0,
     "explanation": "Composite nền nhựa không dẫn điện nên loại nhóm phóng điện (EDM, WEDM) và ECM."},
    {"type": MC, "question": "Phát biểu nào đúng?",
     "options": ["Laser cắt được mọi vật liệu", "Tấm thép 30 mm dung sai ±0,05 mm nên chọn plasma",
                 "Cấm vùng ảnh hưởng nhiệt thì loại laser và plasma, giữ tia nước", "Chi tiết một chiếc nên làm điện cực ECM riêng"], "answer": 2,
     "explanation": "Ràng buộc nhiệt loại nhóm nhiệt; tia nước không sinh nhiệt đáng kể. Các phát biểu còn lại sai về vật liệu, dung sai hoặc số lượng."},
    {"type": MC, "question": "Thép cacbon 2 mm, 5.000 chi tiết, dung sai ±0,1 mm, cho phép nhiệt. Chọn gì?",
     "options": ["Tia nước", "Plasma", "WEDM", "Laser"], "answer": 3,
     "explanation": "Tấm mỏng, số lượng lớn, đạt dung sai và cho phép nhiệt nên laser nhanh hơn tia nước; WEDM quá chậm; plasma thô."},
]}
bundle = {"schema": "thachlab.lesson-bundle/v1",
          "target": {"class_name": "Các phương pháp gia công phi truyền thống", "lesson_title": "Bài 11. Chọn công nghệ gia công cho chi tiết"},
          "theory_title": "Lý thuyết trọng tâm",
          "theory_subtitle": "Quy trình 5 bước · ma trận so sánh · 5 chi tiết mẫu · tự luận mẫu",
          "theory_html": theory, "worked_examples": [], "exam": exam, "raster_images": []}
(HERE / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi bundle.json", len(exam["questions"]), "câu")
