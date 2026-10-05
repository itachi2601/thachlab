#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Tính sai số trong phép đo. Ghi kết quả đo",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Đo thời gian 10 dao động của con lắc đơn 5 lần được t̄ = 20,07 s; độ lệch từng lần 0,12; 0,22; 0,07; 0,13; 0,16 s; đồng hồ số có sai số dụng cụ 0,01 s. Sai số tuyệt đối Δt của phép đo là:",
         "options": ["0,15 s", "0,14 s", "0,70 s", "0,22 s"],
         "answer": 0,
         "explanation": "Trung bình các độ lệch = 0,70/5 = 0,14 s, cộng sai số dụng cụ 0,01 s được Δt = 0,15 s. 0,14 là quên sai số dụng cụ; 0,70 là quên chia cho 5; 0,22 là độ lệch lớn nhất, không phải trung bình."},
        {"type": MC,
         "question": "Đo cạnh hình lập phương được δa = 0,5 %. Sai số tỉ đối của thể tích V = a³ là:",
         "options": ["0,5 %", "1,0 %", "0,17 %", "1,5 %"],
         "answer": 3,
         "explanation": "a xuất hiện 3 lần trong V = a·a·a nên δV = 3·0,5 % = 1,5 %. 0,5 % quên số mũ; 1,0 % nhân với 2; 0,17 % chia cho 3 thay vì nhân."},
        {"type": MC,
         "question": "Đo chiều dài bàn nhiều lần được l̄ = 1,5273 m và Δl = 0,004 m. Cách ghi đúng là:",
         "options": ["l = (1,5273 ± 0,004) m", "l = (1,53 ± 0,004) m", "l = (1,527 ± 0,004) m", "l = 1,527 m"],
         "answer": 2,
         "explanation": "Δl dừng ở chữ số thập phân thứ 3 nên l̄ cũng lấy 3 chữ số thập phân: 1,527. Ghi 1,5273 thừa chữ số; 1,53 làm tròn quá tay; thiếu sai số thì không phải một khoảng giá trị."},
        {"type": MC,
         "question": "Cân điện tử chưa chỉnh về số 0, luôn chỉ thừa 0,3 g. Cân một vật 5 lần rồi lấy trung bình. Kết luận đúng là:",
         "options": ["Trung bình vẫn thừa khoảng 0,3 g; đo thêm không sửa được",
                     "Hết sai số, vì đã lấy trung bình",
                     "Độ lệch còn khoảng 0,06 g, vì chia cho 5",
                     "Đo thêm 100 lần thì độ lệch triệt tiêu"],
         "answer": 0,
         "explanation": "Đây là sai số hệ thống: lệch cùng một phía 0,3 g ở cả 5 lần nên trung bình cũng lệch 0,3 g. Lấy trung bình chỉ làm giảm sai số ngẫu nhiên; muốn sửa phải chỉnh cân về số 0."},
        {"type": MC,
         "question": "Thước thép vạch 1 mm (sai số dụng cụ 0,5 mm) đo tấm nhôm (250,0 ± 0,5) mm và chốt (12,0 ± 0,5) mm. Phép đo nào chính xác hơn, vì sao?",
         "options": ["Chốt, vì vật nhỏ nên ít sai số",
                     "Như nhau, vì cùng Δ = 0,5 mm",
                     "Chốt, vì δ ≈ 0,2 % nhỏ hơn tấm",
                     "Tấm, vì δ ≈ 0,2 % nhỏ hơn δ ≈ 4,2 % của chốt"],
         "answer": 3,
         "explanation": "Tấm: 0,5/250 ≈ 0,2 %. Chốt: 0,5/12 ≈ 4,2 %. Cùng sai số tuyệt đối thì vật nhỏ có sai số tỉ đối lớn hơn; so độ chính xác phải so δ, không so Δ."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 3. Thực hành tính sai số trong phép đo. Ghi kết quả đo"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Đơn vị SI, thứ nguyên; sai số hệ thống và ngẫu nhiên; sai số tuyệt đối, tỉ đối; phép đo gián tiếp; ghi kết quả và chữ số có nghĩa",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
