#!/usr/bin/env python3
"""Đóng gói bundle.json từ theory.html. Chạy sau build_figs.py."""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Tắt dần, cưỡng bức, cộng hưởng",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Con lắc thả trong dầu nhớt rất đặc, ma sát quá lớn. Điều nào đúng?",
         "options": [
             "Vật có thể về vị trí cân bằng rồi dừng, không kịp dao động qua lại",
             "Vật vẫn dao động điều hoà, chỉ chu kì dài hơn",
             "Năng lượng giảm nhưng biên độ giữ nguyên",
             "Li độ không đổi ngay từ lúc thả"],
         "answer": 0,
         "explanation": "Ma sát quá lớn thì vật không kịp dao động qua lại. Năng lượng thành nhiệt trên đoạn đường về vị trí cân bằng."},
        {"type": MC,
         "question": "Quét lực cưỡng bức, f0 = 2,0 Hz, sai số đọc biên độ ±0,2 cm. Bảng A: 1,0 Hz → 2,7 cm; 1,5 Hz → 4,2 cm; 2,0 Hz → 6,0 cm; 2,5 Hz → 4,2 cm; 3,0 Hz → 2,7 cm. Kết luận đúng?",
         "options": [
             "Biên độ lớn nhất ở f = 1,0 Hz vì lực mới bắt đầu tác dụng",
             "Đỉnh ở f = 2,0 Hz; chênh 1,8 cm lớn hơn sai số 0,2 cm nên không nhầm đỉnh",
             "1,5 Hz và 2,5 Hz khác nhau rõ, vì một bên đang tăng, một bên đang giảm",
             "Tần số vật luôn bằng 2,0 Hz dù lực có tần số khác"],
         "answer": 1,
         "explanation": "A lớn nhất tại 2,0 Hz, trùng f0. Hiệu 6,0 − 4,2 = 1,8 cm lớn hơn sai số 0,2 cm. Hai hàng 4,2 cm lệch nhau 0. Lúc ổn định, tần số vật bằng tần số lực."},
        {"type": MC,
         "question": "Học sinh nói nhún xích đu đúng nhịp chính là dao động cưỡng bức vì có ngoại lực. Chỗ cần sửa là gì?",
         "options": [
             "Xích đu không có ngoại lực, nên không thể là duy trì",
             "Cưỡng bức không bao giờ có ngoại lực",
             "Nhún chỉ bù một phần mỗi nhịp; lực cưỡng bức thì liên tục, vật lấy tần số của lực",
             "Hai loại giống hệt nhau về chu kì"],
         "answer": 2,
         "explanation": "Cả hai đều có ngoại lực. Duy trì chỉ bù một phần chu kì và giữ chu kì riêng. Cưỡng bức tác dụng liên tục, chu kì bằng chu kì lực."},
        {"type": MC,
         "question": "Bệ máy có f0 = 10 Hz. Động cơ gây lực rất mạnh nhưng f = 25 Hz. Biên độ ổn định thế nào?",
         "options": [
             "Không cực đại: cộng hưởng cần f = f0, không phải chỉ cần lực mạnh",
             "Cực đại, vì lực mạnh thì luôn cộng hưởng",
             "Biên độ bằng không, vì f khác f0 thì vật không dao động",
             "Vật dao động với f = 10 Hz vì đó là tần số riêng"],
         "answer": 0,
         "explanation": "Cộng hưởng khi f = f0. Lệch 15 Hz thì A không cực đại. Vật vẫn dao động với tần số của lực, tức 25 Hz."},
        {"type": MC,
         "question": "Bệ có f0 = 12 Hz. Động cơ chạy ổn định ở f = 18 Hz. Tần số dao động của bệ là:",
         "options": [
             "12 Hz, vì hệ chỉ dao động ở tần số riêng",
             "18 Hz, vì lúc ổn định tần số vật bằng tần số lực",
             "30 Hz, bằng tổng hai tần số",
             "6 Hz, bằng hiệu hai tần số"],
         "answer": 1,
         "explanation": "Khi dao động cưỡng bức đã ổn định, tần số vật bằng tần số lực. 18 Hz không trùng f0 nên không cộng hưởng, nhưng tần số vẫn là 18 Hz."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 11", "lesson_title": "Bài 6. Dao động tắt dần. Dao động cưỡng bức. Hiện tượng cộng hưởng"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "So sánh dao động tắt dần – duy trì – cưỡng bức và hiện tượng cộng hưởng",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
