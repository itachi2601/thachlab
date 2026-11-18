#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts <bundle.json>
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Tác dụng của dòng điện xoay chiều",
    "duration_minutes": 10,
    "questions": [
        {"type": MC, "question": "Nhóm nào chỉ gồm thiết bị dùng chủ yếu tác dụng nhiệt của dòng điện?",
         "options": ["Bàn là, ấm siêu tốc, máy sưởi", "Bàn là, quạt điện, đèn LED", "Chuông điện, ấm siêu tốc, loa", "Nồi cơm điện, quạt trần, bút thử điện"],
         "answer": 0, "explanation": "Bàn là, ấm siêu tốc, máy sưởi đều cần nóng. Quạt, chuông, loa dùng tác dụng từ; đèn LED, bút thử điện dùng tác dụng phát sáng."},
        {"type": MC, "question": "Một nam châm điện nối với nguồn xoay chiều. Kim nam châm đặt cạnh một đầu nam châm điện sẽ",
         "options": ["lệch hẳn về một phía rồi đứng yên", "đứng yên vì dòng xoay chiều không có tác dụng từ", "quay tròn liên tục nhiều vòng", "rung tại chỗ, bị hút rồi bị đẩy liên tục"],
         "answer": 3, "explanation": "Dòng điện đổi chiều thì cực từ của nam châm điện đổi theo, kim nam châm lúc bị hút lúc bị đẩy nên rung tại chỗ. Lệch hẳn một phía là trường hợp nguồn một chiều."},
        {"type": MC, "question": "Thấy bạn bị điện giật, tay còn dính vào dây điện hở. Việc làm đầu tiên là gì?",
         "options": ["Nắm tay bạn kéo ra thật nhanh", "Dội nước vào bạn cho tỉnh", "Ngắt aptomat hoặc rút phích để cắt điện", "Gọi to để bạn tự buông dây ra"],
         "answer": 2, "explanation": "Phải cắt điện trước. Chạm vào bạn là bị giật theo; nước dẫn điện; dòng điện làm cơ co giật nên bạn không tự buông tay được."},
        {"type": MC, "question": "Dòng điện trong nhà bằng 0 tới 100 lần mỗi giây. Vì sao em không thấy đèn chớp tắt?",
         "options": ["Vì đúng lúc đó dòng điện chạy ngược chiều, vẫn đủ mạnh", "Vì mỗi lần dòng yếu đi quá ngắn, mắt không kịp nhận ra", "Vì đèn trong nhà chỉ sáng nhờ pin dự phòng", "Vì cường độ dòng xoay chiều không thay đổi"],
         "answer": 1, "explanation": "Mỗi lần dòng yếu đi chỉ vài phần nghìn giây: dây tóc không kịp nguội, mắt không tách được 100 lần mỗi giây. Đúng lúc đổi chiều dòng điện bằng 0."},
        {"type": MC, "question": "Mắc ampe kế một chiều (chốt +, −) nối tiếp đèn 6 V – 3 W vào nguồn xoay chiều 6 V. Đèn sáng bình thường. Kim ampe kế sẽ",
         "options": ["chỉ 0,50 A như ampe kế xoay chiều", "lệch hẳn sang trái, quá vạch 0", "chỉ 0,25 A, bằng một nửa", "gần như đứng ở vạch 0"],
         "answer": 3, "explanation": "Lực làm kim quay đổi chiều 100 lần mỗi giây, kim không kịp quay theo nên đứng ở vạch 0. Đo dòng xoay chiều phải dùng ampe kế ghi AC hoặc ~."},
        {"type": MC, "question": "Nhãn máy sấy tóc ghi 220 V~ 1 200 W. Mỗi ngày dùng 15 phút, trong 30 ngày máy tiêu thụ điện năng là",
         "options": ["9 kWh", "540 kWh", "0,3 kWh", "9 000 kWh"],
         "answer": 0, "explanation": "t = 0,25 h · 30 = 7,5 h; A = 1,2 kW · 7,5 h = 9 kWh. Ra 540 là chưa đổi phút ra giờ, 0,3 là quên nhân 30 ngày, 9 000 là chưa đổi W ra kW."},
    ],
}
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "KHTN 9", "lesson_title": "Bài 15. Tác dụng của dòng điện xoay chiều"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Tác dụng nhiệt, phát sáng, từ, sinh lí của dòng điện xoay chiều; an toàn điện 220 V; dụng cụ đo xoay chiều (AC, ~)",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
