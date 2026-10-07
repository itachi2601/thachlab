#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_figs.py && python3 build_bundle.py
rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts content/lesson-samples/l9-phan-xa-toan-phan/bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Phản xạ toàn phần",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Chiếu một tia laser từ trong nước chếch lên mặt nước, rồi tăng dần góc tới. Tia sáng đi ra không khí sẽ thế nào?",
         "options": ["Luôn ló ra, chỉ lệch ngày càng xa pháp tuyến", "Tới một góc nào đó thì không ló ra nữa",
                     "Luôn ló ra, lệch dần về gần pháp tuyến", "Ló ra càng lúc càng sáng hơn"],
         "answer": 1,
         "explanation": "Từ nước ra không khí, góc khúc xạ lớn hơn góc tới nên chạm 90° trước; tăng góc tới nữa thì không còn tia ló, ánh sáng phản xạ toàn phần."},
        {"type": MC,
         "question": "Một khối nhựa trong có góc tới hạn 40° (ánh sáng đi từ nhựa ra không khí). Chiếu tia sáng trong nhựa tới mặt phân cách với góc tới 25°. Em thấy:",
         "options": ["Cả tia khúc xạ lẫn tia phản xạ", "Chỉ tia phản xạ, sáng như tia tới",
                     "Chỉ tia khúc xạ, không có phản xạ", "Không thấy tia nào ló ra khỏi nhựa"],
         "answer": 0,
         "explanation": "25° < 40° nên chưa phản xạ toàn phần: có tia khúc xạ ló ra, và mặt phân cách vẫn phản xạ một phần nên có tia phản xạ mờ."},
        {"type": MC,
         "question": "Ánh sáng đi từ thủy tinh (n = 1,5) sang nước (n = 1,33). Góc tới hạn gần nhất với giá trị nào?",
         "options": ["41,8°", "27,5°", "48,8°", "62,5°"],
         "answer": 3,
         "explanation": "sin i_th = 1,33/1,5 ≈ 0,887 nên i_th ≈ 62,5°. 41,8° là coi môi trường sau là không khí; 48,8° là nước ra không khí; 27,5° là góc với mặt phân cách."},
        {"type": MC,
         "question": "Không được gập sợi quang thành góc quá gắt, nếu không tín hiệu sẽ yếu hẳn. Lý do đúng nhất là:",
         "options": ["Ánh sáng đi chậm lại ở chỗ bị gập", "Chiết suất của lõi tăng ở chỗ bị gập",
                     "Góc tới nhỏ đi, ánh sáng lọt ra vỏ", "Ánh sáng bị phản xạ ngược về đầu"],
         "answer": 2,
         "explanation": "Chỗ gập gắt làm góc tới tại thành sợi tụt dưới góc tới hạn, không còn phản xạ toàn phần, một phần ánh sáng khúc xạ ra vỏ."},
        {"type": MC,
         "question": "Đứng trên bờ, chiếu đèn pin xuống mặt hồ, xiên rất sát mặt nước (góc tới 85°). Ánh sáng có bị phản xạ toàn phần không?",
         "options": ["Không, vì ánh sáng đi từ không khí vào nước", "Có, vì góc tới đã lớn hơn 48,8°",
                     "Có, nhưng chỉ khi mặt hồ phẳng lặng như gương", "Không, vì nước hấp thụ hết ánh sáng"],
         "answer": 0,
         "explanation": "Đi từ không khí vào nước (chiết quang kém sang chiết quang hơn) thì luôn có tia khúc xạ; 48,8° chỉ là góc tới hạn của chiều từ nước ra."},
        {"type": MC,
         "question": "Trong khối thủy tinh (góc tới hạn khoảng 42° khi ra không khí), tia sáng hợp với mặt phân cách thủy tinh – không khí góc 30°. Có phản xạ toàn phần không?",
         "options": ["Không, vì 30° nhỏ hơn 42°", "Có, vì góc tới là 60°",
                     "Không, vì 30° + 42° < 90°", "Có, vì thủy tinh luôn phản xạ toàn phần"],
         "answer": 1,
         "explanation": "Góc tới đo từ pháp tuyến: i = 90° − 30° = 60° > 42°, ánh sáng đi từ thủy tinh ra không khí nên phản xạ toàn phần."},
        {"type": MC,
         "question": "Lợi ích chính của lăng kính phản xạ toàn phần so với gương phẳng tráng bạc trong ống nhòm là:",
         "options": ["Ảnh to hơn, vì lăng kính phóng đại", "Dùng được với mọi góc tới, vì không cần điều kiện",
                     "Ảnh nhiều màu hơn, vì lăng kính tách màu", "Ảnh sáng hơn, vì gần như không mất ánh sáng"],
         "answer": 3,
         "explanation": "Phản xạ toàn phần trả lại gần như toàn bộ ánh sáng, còn lớp bạc của gương luôn hấp thụ một phần."},
        {"type": MC,
         "question": "Đèn dưới đáy bể bơi (nước n = 1,33). Một tia tới mặt nước với góc tới 50°. Tia đó:",
         "options": ["Ló ra với góc khúc xạ 50°", "Ló ra, đi sát mặt nước (r = 90°)",
                     "Bị phản xạ toàn phần vào nước", "Ló ra với góc khúc xạ nhỏ hơn 50°"],
         "answer": 2,
         "explanation": "Góc tới hạn ≈ 48,8° < 50°; thử 1,33·sin 50° ≈ 1,02 > 1 nên không có tia ló, ánh sáng phản xạ toàn phần."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "KHTN 9", "lesson_title": "Bài 6. Phản xạ toàn phần"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Hiện tượng phản xạ toàn phần; hai điều kiện; góc tới hạn sin i_th = n2/n1; cáp quang",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

# đáp án trong bundle phải khớp tl-ok trong theory.html (theo thứ tự quiz)
quiz_ok = []
for qz in re.findall(r'<div class="tl-quiz">(.*?)<div class="tl-fb', theory, re.S):
    labels = re.findall(r'class="tl-opt (tl-ok|tl-no)"', qz)
    quiz_ok.append(labels.index("tl-ok"))
assert quiz_ok == [q["answer"] for q in exam["questions"]], (quiz_ok, [q["answer"] for q in exam["questions"]])

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình · đáp án {quiz_ok}")
