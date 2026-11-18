#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) từ theory.html + câu kiểm tra nhanh.
Dùng: python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts <bundle.json>
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Cảm ứng điện từ. Nguyên tắc tạo ra dòng điện xoay chiều",
    "duration_minutes": 10,
    "questions": [
        {"type": MC, "question": "Đặt một thanh nam châm đứng yên trong lòng cuộn dây kín nối điện kế. Kim điện kế",
         "options": ["lệch mạnh và đứng yên ở đó", "lệch qua lại liên tục", "chỉ số 0", "lệch nhiều hơn nếu nam châm mạnh hơn"],
         "answer": 2, "explanation": "Nam châm đứng yên thì số đường sức qua cuộn dây không đổi, không có dòng cảm ứng. Nam châm mạnh hay yếu không quan trọng khi nó đứng yên."},
        {"type": MC, "question": "Điều kiện để xuất hiện dòng điện cảm ứng trong cuộn dây dẫn kín là",
         "options": ["số đường sức từ xuyên qua tiết diện cuộn dây biến thiên", "có nhiều đường sức từ xuyên qua tiết diện cuộn dây", "đặt cuộn dây gần một nam châm mạnh", "cuộn dây được nối với pin"],
         "answer": 0, "explanation": "Cần số đường sức xuyên qua tiết diện cuộn dây kín thay đổi (tăng hoặc giảm). Nhiều đường sức mà không đổi thì không có dòng."},
        {"type": MC, "question": "Cuộn A nối pin qua công tắc, cuộn B đặt sát cuộn A và nối điện kế. Kim điện kế của cuộn B lệch khi nào?",
         "options": ["Chỉ khi công tắc đang giữ đóng", "Trong lúc đóng và trong lúc ngắt công tắc", "Chỉ khi công tắc đang để ngắt", "Không bao giờ, vì hai cuộn không chạm nhau"],
         "answer": 1, "explanation": "Lúc đóng, dòng trong A tăng; lúc ngắt, dòng giảm: số đường sức qua B biến thiên nên có dòng cảm ứng. Giữ đóng thì từ trường không đổi, kim về 0."},
        {"type": MC, "question": "Dòng điện xoay chiều là dòng điện",
         "options": ["có cường độ luôn không đổi", "chỉ chạy theo một chiều nhưng lúc mạnh lúc yếu", "do pin và acquy tạo ra", "luân phiên đổi chiều"],
         "answer": 3, "explanation": "Dòng xoay chiều luân phiên đổi chiều. Pin, acquy tạo dòng một chiều."},
        {"type": MC, "question": "Trong đinamô xe đạp, bộ phận nào là rôto?",
         "options": ["Nam châm", "Cuộn dây", "Bóng đèn", "Dây nối"],
         "answer": 0, "explanation": "Núm đinamô quay theo bánh xe làm nam châm quay (rôto); cuộn dây đứng yên (stato)."},
        {"type": MC, "question": "Rôto của một máy phát là nam châm hai cực, quay 50 vòng mỗi giây. Mỗi giây dòng điện do máy tạo ra đổi chiều bao nhiêu lần?",
         "options": ["25 lần", "50 lần", "100 lần", "200 lần"],
         "answer": 2, "explanation": "Mỗi vòng quay, hai cực lần lượt qua trước cuộn dây nên dòng đổi chiều 2 lần; 50 vòng cho 100 lần."},
    ],
}
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "KHTN 9", "lesson_title": "Bài 14. Cảm ứng điện từ. Nguyên tắc tạo ra dòng điện xoay chiều"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Thí nghiệm Faraday; điều kiện xuất hiện dòng điện cảm ứng; dòng điện xoay chiều; nguyên tắc tạo dòng xoay chiều, máy phát điện (rôto, stato)",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
