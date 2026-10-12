#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts <bundle.json>
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Cơ năng",
    "duration_minutes": 10,
    "questions": [
        {"type": MC, "question": "Một flycam 0,5 kg bay ngang ở độ cao 8 m với vận tốc 6 m/s. Gốc thế năng ở mặt đất. Cơ năng của flycam là",
         "options": ["40 J", "58 J", "13 J", "49 J"],
         "answer": 3, "explanation": "Wt = 10mh = 10·0,5·8 = 40 J; Wđ = ½mv² = ½·0,5·36 = 9 J; W = 49 J. Ra 58 J là quên ½, ra 13 J là quên số 10 trong Wt."},
        {"type": MC, "question": "Một vận động viên bật lên khỏi ván nhảy cầu, lên tới điểm cao nhất rồi rơi xuống nước. Thế năng chuyển hoá thành động năng trong giai đoạn nào?",
         "options": ["Từ lúc rời ván đến điểm cao nhất", "Từ điểm cao nhất đến lúc chạm nước", "Cả hai giai đoạn trên", "Không giai đoạn nào, vì năng lượng không đổi dạng"],
         "answer": 1, "explanation": "Từ điểm cao nhất xuống, người thấp dần và nhanh dần: thế năng giảm, động năng tăng. Lúc đi lên thì ngược lại."},
        {"type": MC, "question": "Thả khối trượt 0,20 kg trên máng đệm khí nghiêng từ độ cao h = 0,10; 0,20; 0,30; 0,40 m. Thế năng lúc thả 10mh = 0,200; 0,400; 0,600; 0,800 J, còn động năng đo ở chân dốc ½mv² = 0,193; 0,384; 0,576; 0,767 J. Lí do hợp lí nhất khiến ½mv² luôn nhỏ hơn 10mh một chút là",
         "options": ["Khối trượt nhẹ đi một chút khi chạy nhanh", "Ở chân dốc thế năng bằng 0 nên cơ năng mất bớt",
                     "Còn lực cản nhỏ, một phần cơ năng thành nhiệt", "Công thức ½mv² chỉ đúng khi vật chạy chậm"],
         "answer": 2, "explanation": "Lực cản rất nhỏ nhưng không bằng 0; phần chênh vài phần trăm là phần cơ năng đã thành nhiệt."},
        {"type": MC, "question": "Ném một quả bóng thẳng đứng lên, bỏ qua sức cản. Gốc thế năng ở mặt đất. Khi bóng ở điểm cao nhất,",
         "options": ["động năng bằng 0, cơ năng bằng thế năng", "cơ năng bằng 0, vì bóng dừng lại", "thế năng bằng 0, vì bóng đổi chiều", "cơ năng lớn hơn lúc vừa ném"],
         "answer": 0, "explanation": "Ở điểm cao nhất v = 0 nên Wđ = 0; bóng ở trên cao nên Wt lớn nhất và W = Wt, không bằng 0."},
        {"type": MC, "question": "Thả quả bóng cao su xuống sàn cứng, mỗi lần nảy bóng lên thấp hơn lần trước. Câu nào đúng?",
         "options": ["Năng lượng của bóng mất đi, trái định luật bảo toàn năng lượng", "Cơ năng của bóng vẫn bảo toàn qua mỗi lần nảy",
                     "Động năng của bóng tăng dần sau mỗi lần nảy", "Cơ năng giảm, phần giảm thành nhiệt năng"],
         "answer": 3, "explanation": "Mỗi lần va sàn, một phần cơ năng thành nhiệt năng và âm thanh. Cơ năng giảm nhưng năng lượng toàn phần vẫn bảo toàn."},
        {"type": MC, "question": "Một quả cam 0,2 kg trên cành cao 3 m so với mặt đất. Mặt bàn dưới gốc cây cao 1 m. Thế năng của quả cam khi chọn gốc thế năng ở mặt bàn là",
         "options": ["4 J", "6 J", "2 J", "8 J"],
         "answer": 0, "explanation": "Độ cao so với mặt bàn h = 3 − 1 = 2 m; Wt = 10·0,2·2 = 4 J. Ra 6 J là tính độ cao từ mặt đất."},
        {"type": MC, "question": "Thả rơi một vật 0,5 kg không vận tốc đầu từ độ cao 5 m, bỏ qua sức cản. Vận tốc của vật lúc chạm đất là",
         "options": ["100 m/s", "7,07 m/s", "10 m/s", "3,16 m/s"],
         "answer": 2, "explanation": "W = Wt = 10·0,5·5 = 25 J; chạm đất ½·0,5·v² = 25 nên v² = 100, v = 10 m/s. Ra 100 là chưa lấy căn."},
    ],
}
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "KHTN 9", "lesson_title": "Bài 3. Cơ năng"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Cơ năng W = Wđ + Wt; động năng và thế năng chuyển hoá qua lại (con lắc, vật rơi); bảo toàn cơ năng khi không có lực cản",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
