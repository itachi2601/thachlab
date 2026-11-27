#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho CNCTM 2 – Bài 16 (Công nghệ gia công chi tiết dạng bạc).
Dùng: python3 build_figs.py && python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
Nguồn ý: giáo trình CNCTM 2 của bộ môn (Chương 16, "Công nghệ gia công chi tiết bạc và dạng bạc").
Bài toán mẫu và số liệu trong câu hỏi là ví dụ tự soạn; dung sai IT tra theo TCVN 2244 / ISO 286.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"

exam = {
    "title": "Kiểm tra nhanh — Gia công chi tiết dạng bạc",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Yêu cầu kỹ thuật quan trọng nhất của chi tiết dạng bạc là:",
         "options": ["Độ nhám mặt ngoài và độ cứng",
                     "Độ đồng tâm mặt ngoài – lỗ và độ vuông góc mặt đầu – tâm lỗ",
                     "Chiều dài bạc và khối lượng", "Số lỗ tra dầu và rãnh dầu"],
         "answer": 1,
         "explanation": "Giáo trình nêu hai yêu cầu chính: độ đồng tâm giữa mặt trụ ngoài và mặt trong, độ vuông góc của mặt đầu so với đường tâm lỗ."},
        {"type": MC,
         "question": "Bạc thép có đường kính lỗ Ø12. Phôi thường dùng là:",
         "options": ["Phôi cán ống", "Phôi đúc có lỗ sẵn", "Thép thanh hoặc phôi đúc đặc", "Kim loại tấm cuốn lại"],
         "answer": 2,
         "explanation": "Lỗ nhỏ hơn 20 mm: thép thanh định hình, thép cán nóng hoặc phôi đúc đặc (không có lỗ sẵn)."},
        {"type": MC,
         "question": "Lỗ bạc Ø40, cấp chính xác 7. Dung sai đường kính lỗ là:",
         "options": ["0,016 mm", "0,025 mm", "0,039 mm", "0,030 mm"],
         "answer": 1,
         "explanation": "Ø40 thuộc khoảng 30 ÷ 50 mm, IT7 = 25 µm = 0,025 mm (0,016 là IT6, 0,039 là IT8, 0,030 là IT7 của khoảng 50 ÷ 80 mm)."},
        {"type": MC,
         "question": "Phương án gia công mọi mặt chính của bạc trong một lần gá thường dùng khi:",
         "options": ["Phôi đúc từng chiếc, sản lượng lớn",
                     "Phôi thanh hoặc phôi ống, cắt đứt ở bước cuối; đơn chiếc, loạt nhỏ",
                     "Bạc đã nhiệt luyện", "Bạc rất dài, L/D lớn hơn 5"],
         "answer": 1,
         "explanation": "Một lần gá hợp với phôi thanh, phôi ống mà cắt đứt làm cuối cùng. Phôi đúc phải đúc thêm vấu nên tốn vật liệu."},
        {"type": MC,
         "question": "Ở lần gá thứ hai của phương án hai lần gá, chuẩn tinh để gia công mặt ngoài là:",
         "options": ["Mặt ngoài thô và một mặt đầu", "Lỗ và mặt đầu vừa gia công",
                     "Hai mặt đầu", "Lỗ dầu và rãnh then"],
         "answer": 1,
         "explanation": "Lần gá thứ hai lấy mặt đầu và lỗ vừa gia công làm chuẩn tinh, thường qua trục gá đàn hồi."},
        {"type": MC,
         "question": "Định vị bạc vào lỗ bằng trục gá đàn hồi gá trên hai mũi tâm (chống tâm) để tiện mặt ngoài. Sai số gá đặt:",
         "options": ["Bằng 0", "Bằng khe hở lỗ – trục gá", "Bằng dung sai lỗ", "Bằng nửa dung sai mặt ngoài"],
         "answer": 0,
         "explanation": "Trục gá đàn hồi khử khe hở (thông lệ); theo giáo trình, chống tâm thì sai số gá đặt không có, gá trên mâm cặp thì rất bé."},
        {"type": MC,
         "question": "Thứ tự đúng trong đường lối công nghệ gia công bạc là:",
         "options": ["Nhiệt luyện → mặt chính → lỗ phụ → tinh",
                     "Mặt chính → lỗ phụ → rãnh → nhiệt luyện → tinh → kiểm tra",
                     "Lỗ phụ → mặt chính → nhiệt luyện → rãnh",
                     "Mặt chính → tinh → nhiệt luyện → lỗ phụ"],
         "answer": 1,
         "explanation": "Gia công mặt chính, khoan lỗ phụ, gia công rãnh, nhiệt luyện, gia công tinh, đánh bóng, kiểm tra."},
        {"type": MC,
         "question": "Kiểm tra độ đồng tâm giữa mặt ngoài và lỗ bạc thường dùng:",
         "options": ["Thước cặp đo hai đầu bạc", "Bạc lồng trên trục tâm, đồng hồ so chạm mặt ngoài, quay bạc",
                     "Thước vuông áp vào mặt đầu", "Mẫu so độ nhám"],
         "answer": 1,
         "explanation": "Dùng đồng hồ so và đồ gá kiểm tra (trục tâm) giống sơ đồ kiểm trục bậc. Thước vuông dùng kiểm độ vuông góc mặt đầu."},
    ],
}

# Rải vị trí đáp án đúng (không dồn một chữ cái): đưa đáp án đúng câu i về vị trí VI_TRI[i].
VI_TRI = [1, 2, 3, 0, 3, 0, 2, 1]
for q, k in zip(exam["questions"], VI_TRI):
    dung = q["options"].pop(q["answer"])
    q["options"].insert(k, dung)
    q["answer"] = k

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Công nghệ chế tạo máy 2", "lesson_title": "Bài 16. Công nghệ gia công chi tiết dạng bạc"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Yêu cầu đồng tâm, vuông góc · phôi theo lỗ · ba phương án chuẩn · thứ tự nguyên công · kiểm tra",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự lý thuyết,", len(exam["questions"]), "câu")
