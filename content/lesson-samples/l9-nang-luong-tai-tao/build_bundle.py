#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts <bundle.json>
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Một số dạng năng lượng tái tạo",
    "duration_minutes": 10,
    "questions": [
        {"type": MC, "question": "Nguồn nào dưới đây không phải năng lượng tái tạo?",
         "options": ["Gió thổi qua cánh đồng ven biển", "Khí thiên nhiên khai thác ngoài khơi", "Rơm rạ còn lại sau mùa gặt", "Nước sông chảy từ trên núi xuống"],
         "answer": 1, "explanation": "Khí thiên nhiên là nhiên liệu hoá thạch, hình thành qua hàng triệu năm, dùng hết là cạn. Gió, rơm rạ (sinh khối), nước sông được tự nhiên bù lại nhanh."},
        {"type": MC, "question": "Tua-bin gió mô hình nối với điện trở 10 Ω. Gió 2 m/s cho U trung bình 0,60 V; gió 4 m/s cho 1,80 V. Công suất điện trên điện trở tăng khoảng bao nhiêu lần?",
         "options": ["2 lần", "3 lần", "9 lần", "4 lần"],
         "answer": 2, "explanation": "U gấp 3 lần; P = U²/R nên P gấp 3² = 9 lần (0,036 W lên 0,324 W). Ra 3 là quên bình phương, ra 2 là lấy theo tốc độ gió."},
        {"type": MC, "question": "Một vùng đã có nhiều điện mặt trời. Vì sao lưới điện vẫn cần thêm nguồn phát ổn định như thuỷ điện?",
         "options": ["Điện mặt trời không phát ban đêm, giảm khi trời mây", "Điện mặt trời thải nhiều khí hơn thuỷ điện khi phát", "Tấm pin chỉ chạy được vào mùa hè", "Điện từ pin mặt trời không dùng được trong nhà"],
         "answer": 0, "explanation": "Pin quang điện chỉ cho điện khi có ánh sáng. Buổi tối nhu cầu cao mà pin không phát, nên cần nguồn bù như thuỷ điện (giữ nước ban ngày, xả buổi tối)."},
        {"type": MC, "question": "Câu nào đúng về năng lượng tái tạo và môi trường?",
         "options": ["Điện gió không đốt nhiên liệu nên không ảnh hưởng gì tới sinh vật", "Thuỷ điện chỉ dùng nước nên không làm thay đổi hệ sinh thái sông", "Hầu như không thải khí khi chạy, nhưng lúc xây và lúc bỏ vẫn gây hại", "Tấm pin mặt trời hết hạn có thể bỏ chung với rác sinh hoạt"],
         "answer": 2, "explanation": "Tua-bin gió gây ồn, va phải chim; đập thuỷ điện ngập rừng, chặn cá; tấm pin hỏng là rác thải điện tử phải xử lí riêng. 'Sạch' chỉ đúng lúc đang phát điện."},
        {"type": MC, "question": "Nguồn nào dưới đây không có gốc từ năng lượng Mặt Trời?",
         "options": ["Năng lượng gió", "Thuỷ điện trên sông", "Năng lượng sinh khối từ trấu", "Năng lượng địa nhiệt"],
         "answer": 3, "explanation": "Địa nhiệt là nhiệt từ lòng Trái Đất. Gió do Mặt Trời nung mặt đất không đều; nước hồ thuỷ điện do Mặt Trời làm bốc hơi rồi mưa trên núi; lúa quang hợp nhờ ánh sáng."},
        {"type": MC, "question": "Mái trường lắp 20 tấm pin, mỗi tấm 500 W khi nắng đủ. Mỗi ngày tương đương 4 giờ nắng đủ. Điện năng hệ pin tạo ra mỗi ngày là",
         "options": ["10 kWh", "40 kWh", "40 000 kWh", "2 kWh"],
         "answer": 1, "explanation": "P = 20 · 0,5 kW = 10 kW; A = P·t = 10 · 4 = 40 kWh. 10 là công suất chưa nhân giờ; 40 000 là quên đổi W ra kW; 2 là chỉ một tấm."},
    ],
}
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "KHTN 9", "lesson_title": "Bài 17. Một số dạng năng lượng tái tạo"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Năng lượng tái tạo là gì; mặt trời, gió, nước, sinh khối, địa nhiệt; chuỗi chuyển hoá năng lượng; ưu và nhược điểm; ước lượng điện từ pin mặt trời",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
