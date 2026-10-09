#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Thực hành: Tổng hợp lực",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Treo vật nặng 2,0 N bằng hai dây giống hệt nhau, đối xứng, góc giữa hai dây là α. Tăng α từ 60° lên 120°, lực căng của mỗi dây thay đổi thế nào?",
         "options": ["Không đổi, vì trọng lượng của vật vẫn là 2,0 N",
                     "Giảm đi, vì dây xoạc ra thì mỗi dây chỉ gánh nhẹ hơn",
                     "Tăng lên, vì hai lực nghiêng vẫn phải đỡ 2,0 N",
                     "Bằng một nửa trọng lượng vật, vì hai dây giống hệt nhau"],
         "answer": 2,
         "explanation": "Mỗi lực căng nghiêng nên chỉ một phần của nó hướng lên; dây càng xoạc, phần hướng lên càng nhỏ nên lực căng phải lớn hơn mới đỡ đủ 2,0 N. 2,0 N là lực tổng hợp của hai dây, không phải của từng dây; một nửa trọng lượng chỉ đúng khi α = 0°."},
        {"type": MC,
         "question": "F1 = 1,2 N, F2 = 1,6 N, hai dây vuông góc. Lực kế thứ ba (treo vật) chỉ gần nhất:",
         "options": ["2,0 N", "2,8 N", "0,4 N", "1,4 N"],
         "answer": 0,
         "explanation": "F = sqrt(1,2² + 1,6²) = 2,0 N; nút O đứng yên nên lực kế 3 chỉ đúng độ lớn này. 2,8 là cộng hai độ lớn (chỉ khi cùng chiều), 0,4 là hiệu (chỉ khi ngược chiều), 1,4 là trung bình."},
        {"type": MC,
         "question": "Nhóm khác: F1 = 1,0 N, F2 = 1,0 N, hai dây vuông góc, F3 = 1,9 N. Mỗi lực kế sai 0,1 N, tỉ lệ xích 1 cm ứng với 0,5 N. Kết luận nào đúng?",
         "options": ["Hợp quy tắc, vì F3 gần với F1 + F2 = 2,0 N",
                     "Quy tắc hình bình hành sai, vì δ > Δ",
                     "Hợp quy tắc, vì mỗi lực kế chỉ sai 0,1 N",
                     "Chưa hợp, vì δ = 0,5 N vượt Δ"],
         "answer": 3,
         "explanation": "Cạnh 2,0 cm, chéo 2,8 cm nên F vẽ = 1,40 N; δ = |1,40 − 1,9| = 0,50 N > Δ = 0,30 N. Cần kiểm số 0, góc, phương dây rồi đo lại; một lần δ > Δ chưa bác bỏ được quy tắc."},
        {"type": MC,
         "question": "Lực kế 1 và 2 chưa chỉnh 0: khi chưa móc gì, mỗi cái chỉ +0,1 N. Lực kế 3 đã chỉnh đúng. Nhóm dựng hình bình hành từ số đọc F1, F2. So với F3 thật, F vẽ sẽ:",
         "options": ["Bằng nhau, vì hai số lệch bù trừ cho nhau",
                     "Nhỏ hơn, vì lực kế thừa số 0 làm lực kéo yếu đi",
                     "Không so được, vì ba lực kế phải lệch giống nhau hoàn toàn",
                     "Lớn hơn, vì cả hai số đọc đều dư thêm"],
         "answer": 3,
         "explanation": "Cả hai số đọc đều dư 0,1 N nên hình bình hành vẽ từ chúng to hơn thật, trong khi F3 đúng. Hai lệch cùng dấu nên cộng dồn; số 0 lệch làm số đọc lớn lên chứ không làm lực yếu đi; vẫn so được sau khi trừ số lệch."},
        {"type": MC,
         "question": "F1 = 2,0 N, F2 = 3,0 N, góc giữa hai dây ở nút O là α = 120°. Lực tổng hợp có độ lớn gần nhất:",
         "options": ["5,0 N", "2,6 N", "4,4 N", "3,6 N"],
         "answer": 1,
         "explanation": "F² = 2,0² + 3,0² + 2·2,0·3,0·cos 120° = 13 − 6 = 7 nên F ≈ 2,6 N. 5,0 là cộng độ lớn (α = 0°), 4,4 dùng 60° (nhầm góc bù), 3,6 dùng 90°."},
        {"type": MC,
         "question": "Nút O đứng yên, vật nặng kéo lực kế 3 xuống. Lực tổng hợp F của F1 và F2 có đặc điểm nào?",
         "options": ["Hướng xuống, độ lớn bằng F3, vì cùng chiều với vật",
                     "Hướng lên, nhỏ hơn F3, vì mỗi dây chỉ gánh một phần",
                     "Hướng lên, độ lớn bằng F3, vì nút O đứng yên",
                     "Hướng lên, lớn hơn F3, vì phải nâng cả vật lẫn nút"],
         "answer": 2,
         "explanation": "Nút O đứng yên nên F + F3 = 0: F cùng độ lớn với F3 và ngược chiều, tức hướng lên. Không có phần gánh bớt hay gánh thêm."},
        {"type": MC,
         "question": "Cùng thí nghiệm lần 2: giữ F1 = F2 = 2,0 N nhưng mở rộng góc từ α = 60° lên 90°. Số chỉ F3 của lực kế thứ ba thay đổi thế nào?",
         "options": ["Tăng, vì hai lực kéo ra hai bên mạnh hơn",
                     "Giảm, vì hai lực bớt cùng hướng hơn",
                     "Không đổi, vì F1 và F2 không đổi",
                     "Giảm về 0, vì hai lực vuông góc triệt tiêu nhau"],
         "answer": 1,
         "explanation": "F = 2·2,0·cos(α/2): α = 60° cho 3,46 N, α = 90° cho 2,83 N. Hai lực hướng ra hai phía thì phần cộng vào nhau ít hơn; tổng hợp phụ thuộc cả góc; lực chỉ triệt tiêu khi ngược chiều và bằng nhau."},
        {"type": MC,
         "question": "Thanh nhẹ AB có hai lực kế ở hai đầu, vật P = 3,0 N treo cách A 20 cm. Dời vật về phía A (giảm d_A), F_A và F_B thay đổi thế nào?",
         "options": ["F_A tăng, F_B giảm, tổng vẫn bằng P",
                     "F_A giảm, F_B tăng, tổng vẫn bằng P, vì lực kế gần vật chỉ nhẹ đi",
                     "Cả hai không đổi, vì P không đổi",
                     "F_A tăng, F_B giảm, tổng nhỏ hơn P"],
         "answer": 0,
         "explanation": "F_A = P·d_B/AB tăng khi d_B tăng, F_B giảm, còn F_A + F_B = P; ví dụ d_A = 10 cm cho F_A = 2,5 N, F_B = 0,5 N. Đầu gần vật gánh nhiều hơn chứ không nhẹ đi; cách chia cho hai đầu đổi theo vị trí; hai lực kế luôn gánh đủ P."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 22. Thực hành: Tổng hợp lực"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Tổng hợp hai lực đồng quy bằng ba lực kế và hình bình hành; so lực vẽ với lực cân bằng đo được, độ lệch, sai số; hai lực song song",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
