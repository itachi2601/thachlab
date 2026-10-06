#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Định luật bảo toàn động lượng",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "An (50 kg) trượt 4 m/s trên băng, ôm chầm lấy Bình (50 kg) đang đứng yên. Bỏ qua ma sát. Ngay sau cú ôm, hai bạn cùng lướt với tốc độ:",
         "options": ["4 m/s, An kéo Bình theo đúng tốc độ cũ", "2 m/s", "0, ôm nhau thì đứng lại",
                     "Khoảng 2,8 m/s, để động năng giữ nguyên"],
         "answer": 1,
         "explanation": "Động lượng trước: 50·4 = 200 kg·m/s. Sau: 100·v = 200 ⇒ v = 2 m/s. Động năng không được giữ (va chạm mềm), thứ giữ nguyên là động lượng."},
        {"type": MC,
         "question": "Hệ nào dưới đây coi được là hệ kín trong thời gian xét?",
         "options": ["Quả táo đang rơi tự do (hệ chỉ gồm quả táo)", "Người và xe đạp đang phanh trên đường nhựa",
                     "Thuyền buồm đang được gió đẩy ra khơi", "Hai xe va chạm trên ray đệm khí nằm ngang"],
         "answer": 3,
         "explanation": "Trên ray đệm khí, trọng lực cân bằng lực đỡ, ma sát gần bằng 0; lực giữa hai xe là nội lực. Trọng lực (táo), ma sát (xe đạp), gió (thuyền) là ngoại lực không cân bằng."},
        {"type": MC,
         "question": "Bi cái lăn 2 m/s va thẳng vào bi đỏ cùng khối lượng đang đứng yên. Coi va chạm là đàn hồi. Kết quả nào thoả cả bảo toàn động lượng lẫn động năng?",
         "options": ["Bi cái dừng, bi đỏ đi tiếp 2 m/s", "Hai bi cùng đi 1 m/s theo chiều cũ",
                     "Bi cái bật lùi 2 m/s, bi đỏ đi 2 m/s", "Bi cái đi tiếp 2 m/s, bi đỏ đi 2 m/s"],
         "answer": 0,
         "explanation": "Hai vật bằng khối lượng va chạm đàn hồi trực diện thì đổi vận tốc: động lượng 2m và động năng ½m·4 đều giữ nguyên. Hai bi cùng đi 1 m/s là va chạm mềm (mất nửa động năng)."},
        {"type": MC,
         "question": "Súng 4 kg đặt tự do, bắn viên đạn 20 g bay ngang với vận tốc 500 m/s. Súng giật với vận tốc:",
         "options": ["25 m/s, ngược chiều đạn", "2,5 m/s, cùng chiều đạn", "2,5 m/s, ngược chiều đạn",
                     "0, súng nặng hơn nhiều nên không giật"],
         "answer": 2,
         "explanation": "V = −(0,02·500)/4 = −2,5 m/s: dấu trừ nghĩa là ngược chiều đạn. Ra 25 m/s là đổi nhầm 20 g = 0,2 kg."},
        {"type": MC,
         "question": "Người 50 kg đứng trên xe goòng 100 kg đang chạy 2 m/s trên ray ngang. Người nhảy khỏi xe về phía sau với vận tốc 1 m/s so với đất. Bỏ qua ma sát. Ngay sau đó xe chạy với tốc độ:",
         "options": ["2,5 m/s", "3,5 m/s", "3,0 m/s", "2,0 m/s"],
         "answer": 1,
         "explanation": "Chiều dương theo xe: 150·2 = 100·V + 50·(−1) ⇒ V = 3,5 m/s. Ra 2,5 m/s là thế +1 cho người (quên dấu)."},
        {"type": MC,
         "question": "Viên đạn bay ngang cắm vào bao cát treo đứng yên và nằm lại trong đó. Trong lúc va chạm, với hệ đạn + bao cát:",
         "options": ["Động lượng và động năng đều bảo toàn", "Động năng bảo toàn, động lượng giảm",
                     "Động lượng và động năng đều giảm", "Động lượng bảo toàn, động năng giảm"],
         "answer": 3,
         "explanation": "Đạn nằm lại trong bao là va chạm mềm: va chạm rất nhanh nên hệ coi là kín, động lượng bảo toàn; phần lớn động năng thành nhiệt và biến dạng."},
        {"type": MC,
         "question": "Viên bi thép lăn trên bàn, va vào cục đất nặn đứng yên, dính lại rồi cả hai trượt chậm dần, dừng sau 30 cm. Dùng được bảo toàn động lượng cho hệ bi + đất nặn ở giai đoạn nào?",
         "options": ["Từ ngay trước đến ngay sau va chạm", "Từ lúc va chạm đến lúc dừng hẳn",
                     "Không giai đoạn nào, vì bàn có ma sát", "Chỉ dùng được khi mặt bàn nhẵn tuyệt đối"],
         "answer": 0,
         "explanation": "Trong khoảnh khắc va chạm, ma sát rất nhỏ so với nội lực nên bỏ qua được. Trên quãng trượt 30 cm, ma sát tác dụng lâu và đưa động lượng về 0."},
        {"type": MC,
         "question": "Xe 1 nặng 1 kg chạy 4 m/s va vào xe 2 nặng 3 kg đang chạy 2 m/s ngược chiều. Hai xe móc dính vào nhau. Ngay sau va chạm, hai xe:",
         "options": ["Chạy 2,5 m/s theo chiều xe 1", "Chạy 0,5 m/s theo chiều xe 1",
                     "Chạy 0,5 m/s theo chiều xe 2", "Chạy 2,0 m/s theo chiều xe 2"],
         "answer": 2,
         "explanation": "Chiều dương theo xe 1: v = (1·4 + 3·(−2))/4 = −0,5 m/s, tức theo chiều xe 2. Ra 2,5 m/s là quên dấu của v₂."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 29. Định luật bảo toàn động lượng"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Hệ kín; định luật bảo toàn động lượng; va chạm mềm, va chạm đàn hồi; chuyển động bằng phản lực; dấu của vận tốc",
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
