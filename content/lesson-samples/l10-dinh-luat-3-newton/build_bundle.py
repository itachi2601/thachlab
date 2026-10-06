#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Định luật III Newton",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Em đi giày trượt, hai tay đẩy mạnh vào thành sân gắn chặt với mặt đất. Em sẽ chuyển động thế nào?",
         "options": ["Đứng yên, vì thành sân không nhúc nhích", "Trượt tiến về phía thành sân",
                     "Trượt lùi ra xa thành sân", "Trượt sang bên, dọc theo thành sân"],
         "answer": 2,
         "explanation": "Em đẩy thành thì thành đẩy lại em, cùng độ lớn, ngược chiều (định luật III). Giày trượt gần như không ma sát nên em lùi ra xa."},
        {"type": MC,
         "question": "Chiếc đèn treo vào trần bằng một sợi dây, đang đứng yên. Hai lực nào là cặp lực – phản lực?",
         "options": ["Trọng lực lên đèn và lực dây kéo đèn", "Trọng lực lên đèn và lực đèn kéo dây",
                     "Lực dây kéo đèn và lực trần kéo dây", "Lực dây kéo đèn và lực đèn kéo dây"],
         "answer": 3,
         "explanation": "Cặp lực – phản lực là A tác dụng lên B và B tác dụng lại A, đặt lên hai vật khác nhau: dây kéo đèn và đèn kéo dây. Trọng lực và lực dây cùng đặt lên đèn nên là hai lực cân bằng."},
        {"type": MC,
         "question": "Con muỗi đâm vào kính chắn gió của ô tô đang chạy nhanh. Lực của muỗi lên kính so với lực của kính lên muỗi:",
         "options": ["Nhỏ hơn rất nhiều, vì muỗi rất nhẹ", "Bằng nhau về độ lớn",
                     "Lớn hơn, vì ô tô đang chạy nhanh", "Bằng không, vì kính chẳng bị làm sao"],
         "answer": 1,
         "explanation": "Lực và phản lực luôn bằng nhau về độ lớn. Muỗi nát vì nó nhẹ nên gia tốc cực lớn (a = F/m)."},
        {"type": MC,
         "question": "Một phi hành gia lơ lửng đứng yên ngoài không gian rồi ném cái búa về phía trước. Phi hành gia sẽ:",
         "options": ["Vẫn đứng yên, vì không có gì để tựa vào", "Trôi về phía trước theo cái búa",
                     "Trôi lùi về phía sau", "Trôi lên phía trên"],
         "answer": 2,
         "explanation": "Người đẩy búa về trước thì búa đẩy lại người về sau; không có ma sát nên người trôi lùi."},
        {"type": MC,
         "question": "Hai bạn 50 kg và 70 kg đứng trên giày trượt, đẩy nhau trong cùng một khoảng thời gian rồi buông tay. Sau đó:",
         "options": ["Bạn 50 kg có tốc độ lớn hơn", "Bạn 70 kg có tốc độ lớn hơn, vì bị đẩy mạnh hơn",
                     "Hai bạn cùng tốc độ, vì lực bằng nhau", "Bạn 70 kg đứng yên, vì nặng hơn"],
         "answer": 0,
         "explanation": "Lực bằng nhau, thời gian bằng nhau nhưng a = F/m nên bạn nhẹ có gia tốc lớn hơn, tốc độ v = at lớn hơn."},
        {"type": MC,
         "question": "Hai xe đẩy trên bàn nhẵn, ép lò xo giữa chúng rồi thả ra. Xe 1 nặng 1 kg có gia tốc 4 m/s². Xe 2 nặng 2 kg có gia tốc:",
         "options": ["0,5 m/s²", "2 m/s²", "4 m/s²", "8 m/s²"],
         "answer": 1,
         "explanation": "Lò xo đẩy hai xe bằng lực bằng nhau nên m1·a1 = m2·a2, suy ra a2 = 1·4/2 = 2 m/s²."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 16. Định luật 3 Newton"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Phát biểu định luật 3 Newton; Cặp lực và phản lực; Vận dụng trong một số tình huống thực tế",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
