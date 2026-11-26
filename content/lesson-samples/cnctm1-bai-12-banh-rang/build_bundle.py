#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho CNCTM 1 – Bài 12 (Gia công bánh răng).
Dùng: python3 build_figs.py && python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
Nguồn ý: giáo trình CNCTM của bộ môn (Chương 12). Số đọc đồng hồ so và bài toán mẫu là ví dụ tự soạn.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Kiểm tra nhanh — Gia công bánh răng",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Mặt lỗ của bánh răng thường cần gia công đạt cấp chính xác:",
         "options": ["11 ÷ 10", "9 ÷ 8", "7 ÷ 6", "3 ÷ 2"],
         "answer": 2,
         "explanation": "Mặt lỗ bánh răng và cổ trục của trục răng cần đạt cấp 7 ÷ 6."},
        {"type": MC,
         "question": "Phay bánh răng bằng dao phay mô-đun trên máy phay vạn năng, sau mỗi rãnh phải:",
         "options": ["Đổi dao", "Phân độ một góc 360°/Z", "Tôi răng vừa cắt", "Đảo chiều quay dao"],
         "answer": 1,
         "explanation": "Phương pháp định hình cắt từng rãnh, phân độ 360°/Z bằng đầu phân độ để sang rãnh kế."},
        {"type": MC,
         "question": "Bộ 8 dao phay mô-đun: bánh răng Z = 45 dùng dao số mấy?",
         "options": ["Số 4", "Số 5", "Số 6", "Số 7"],
         "answer": 2,
         "explanation": "Dao số 6 dùng cho Z = 35 ÷ 54."},
        {"type": MC,
         "question": "Ưu điểm cơ bản của dao phay lăn so với dao phay mô-đun là:",
         "options": ["Dao rẻ, dễ chế tạo", "Một dao cắt đúng prôfin cho mọi số răng cùng mô-đun và góc ăn khớp",
                     "Làm được bánh răng bậc sát vai", "Không cần máy chuyên dùng"],
         "answer": 1,
         "explanation": "Phay lăn là bao hình, dao ăn khớp đúng với bánh răng thân khai có bất kỳ số răng nào cùng m, góc ăn khớp."},
        {"type": MC,
         "question": "Phay lăn bánh răng Z = 36 bằng dao một đầu mối. Tỉ số n_dao / n_phôi bằng:",
         "options": ["1/36", "1", "18", "36"],
         "answer": 3,
         "explanation": "n_d / n_ph = Z_ph / K_d = 36 / 1 = 36."},
        {"type": MC,
         "question": "Bánh răng bậc có vành răng sát vai, nên cắt răng bằng:",
         "options": ["Phay lăn", "Xọc răng bằng dao dạng bánh răng", "Cà răng", "Mài răng từ phôi trơn"],
         "answer": 1,
         "explanation": "Phay lăn cần khoảng thoát dao lớn nên không làm được bánh răng bậc; xọc răng làm được."},
        {"type": MC,
         "question": "Cà răng là phương pháp gia công tinh dùng cho:",
         "options": ["Bánh răng đã tôi cứng", "Bánh răng không qua nhiệt luyện, lượng dư lớn nhất 0,15 mm",
                     "Phôi chưa cắt răng", "Bánh vít"],
         "answer": 1,
         "explanation": "Cà răng dùng cho bánh răng không nhiệt luyện, dư lớn nhất 0,15 mm; răng đã tôi thì mài."},
        {"type": MC,
         "question": "Cán răng có đặc điểm:",
         "options": ["Năng suất thấp hơn phay lăn", "Năng suất gấp 15 ÷ 20 lần cắt răng, hao kim loại chỉ 3 ÷ 4%",
                     "Chỉ cán nóng với mọi mô-đun", "Làm yếu răng vì cắt đứt thớ"],
         "answer": 1,
         "explanation": "Cán răng năng suất cao gấp 15 ÷ 20 lần, hao 3 ÷ 4% khối lượng phôi, tăng tuổi bền; m < 1 cán nguội."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Công nghệ chế tạo máy 1", "lesson_title": "Bài 12. Gia công bánh răng"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Yêu cầu kỹ thuật · dao phay mô-đun · phay lăn, xọc, cán răng · cà, mài răng · kiểm tra",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự lý thuyết,", len(exam["questions"]), "câu")

