#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_figs.py && python3 build_bundle.py   rồi
      npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts content/lesson-samples/l9-lang-kinh-tan-sac/bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Lăng kính",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Tia sáng đang đi trong thuỷ tinh, ló ra không khí ở mặt bên thứ hai của lăng kính. So với pháp tuyến tại điểm ló, tia ló:",
         "options": ["Gần pháp tuyến hơn tia trong thuỷ tinh", "Luôn trùng với pháp tuyến",
                     "Xa pháp tuyến hơn tia trong thuỷ tinh", "Song song với mặt bên thứ hai"],
         "answer": 2,
         "explanation": "Từ thuỷ tinh (chiết quang hơn) ra không khí, góc khúc xạ lớn hơn góc tới nên tia ra xa pháp tuyến. Gần pháp tuyến là chuyện ở mặt thứ nhất (không khí vào thuỷ tinh)."},
        {"type": MC,
         "question": "Đo góc lệch qua lăng kính (số liệu minh hoạ): đỏ trung bình 47,7°, lục 49,3° (chênh khoảng 1,7°); mỗi lần đọc thước sai ±1°, cả ba lần đo lục đều lớn hơn cả ba lần đo đỏ. Kết luận nào hợp lý nhất?",
         "options": ["Lục có vẻ lệch hơn đỏ; nên đo thêm cho chắc", "Lục và đỏ lệch bằng nhau, chênh lệch hoàn toàn do đo sai",
                     "Đỏ lệch nhiều hơn lục một chút", "Bảng không cho biết gì về ba màu"],
         "answer": 0,
         "explanation": "Chênh khoảng 1,7° chỉ nhỉnh hơn sai số một lần đo, nhưng cả ba lần lục đều lớn hơn đỏ: có xu hướng lục lệch hơn, cần đo thêm để chắc."},
        {"type": MC,
         "question": "Cho ánh sáng trắng đi qua một tấm kính lọc màu lục, rồi mới cho qua lăng kính. Trên màn thấy:",
         "options": ["Đủ bảy màu từ đỏ đến tím", "Một vệt trắng, không lệch",
                     "Chỉ một vệt màu lục hẹp", "Bảy màu, trong đó lục đậm nhất"],
         "answer": 2,
         "explanation": "Lăng kính chỉ tách màu có sẵn. Sau tấm lọc chỉ còn ánh sáng lục nên chỉ còn vệt lục, bị lệch về phía đáy."},
        {"type": MC,
         "question": "Lăng kính đặt ngược: cạnh ở dưới, đáy ở trên. Chiếu tia laser đỏ nằm ngang, từ trái sang, vào mặt bên bên trái. Tia ló ra ở mặt bên phải đi:",
         "options": ["Chếch lên trên", "Chếch xuống dưới", "Thẳng, không lệch", "Tách thành bảy màu"],
         "answer": 0,
         "explanation": "Tia ló luôn lệch về phía đáy; đáy đang ở trên nên tia chếch lên. Laser đỏ đơn sắc nên không tách màu."},
        {"type": MC,
         "question": "Ba chùm sáng hẹp màu đỏ, vàng, lam chiếu vào cùng một điểm, cùng góc tới, trên lăng kính đặt đáy ở dưới. Trên màn, thứ tự ba vệt từ trên xuống là:",
         "options": ["Lam, vàng, đỏ", "Vàng, đỏ, lam", "Ba vệt trùng nhau", "Đỏ, vàng, lam"],
         "answer": 3,
         "explanation": "Chiết suất tăng dần đỏ → vàng → lam nên độ lệch về đáy cũng tăng dần: đỏ lệch ít nhất, nằm cao nhất."},
        {"type": MC,
         "question": "Lăng kính vuông tại B, góc chiết quang A = 20°. Chiếu tia đỏ vuông góc mặt AB; tia ló hợp với pháp tuyến của mặt AC góc 30,9°. Góc lệch D của tia đỏ là:",
         "options": ["30,9°", "10,9°", "50,9°", "20°"],
         "answer": 1,
         "explanation": "Tia đi thẳng qua AB, góc tới ở AC bằng A = 20°. D = 30,9° − 20° = 10,9°. 30,9° là góc ló so với pháp tuyến, 20° là góc tới, 50,9° là cộng nhầm."},
    ],
}

# đối chiếu đáp án bundle với tl-ok trong theory.html (bỏ câu dự đoán q1)
quiz = re.findall(r'<div class="tl-quiz">(.*?)<div class="tl-fb', theory, re.S)[1:]
assert len(quiz) == len(exam["questions"]), (len(quiz), len(exam["questions"]))
for q, item in zip(quiz, exam["questions"]):
    kinds = re.findall(r'class="tl-opt (tl-ok|tl-no)"', q)
    assert kinds.index("tl-ok") == item["answer"], item["question"]

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "KHTN 9", "lesson_title": "Bài 7. Lăng kính"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Đường truyền tia sáng qua lăng kính; tán sắc ánh sáng trắng, chiết suất phụ thuộc màu",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
