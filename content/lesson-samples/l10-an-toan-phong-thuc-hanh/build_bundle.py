#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Các quy tắc an toàn trong phòng thực hành Vật lí",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Mạch đã lắp gần xong, bộ nguồn đang bật, còn một đầu dây chưa nối vào bóng đèn. Việc đầu tiên cần làm trước khi cầm đầu dây đó là:",
         "options": ["Nối ngay cho kịp giờ, vì dây có vỏ nhựa nên chạm vào là an toàn",
                     "Tắt công tắc nguồn, rồi mới nối dây",
                     "Đeo găng cao su rồi nối luôn khi nguồn còn bật",
                     "Nối bằng một tay, tay kia giấu ra sau lưng"],
         "answer": 1,
         "explanation": "Quy tắc đầu tiên của điện: tắt công tắc nguồn trước khi cầm hoặc tháo thiết bị điện. Vỏ nhựa chỉ bọc thân dây; găng cao su hay mẹo một tay không thay được việc ngắt nguồn."},
        {"type": MC,
         "question": "Một dụng cụ ghi 6 V, DC. Bộ nguồn có Input 220 V ~ và Output 3–12 V DC. Nối dụng cụ vào đâu là đúng?",
         "options": ["Đầu ra xoay chiều AC 6 V (nếu bộ nguồn có)",
                     "Output DC, núm ở vạch 12 V cho dụng cụ hoạt động mạnh hơn",
                     "Input 220 V ~, vì đó là chỗ có điện",
                     "Output DC, núm ở vạch 6 V"],
         "answer": 3,
         "explanation": "Cần đúng loại dòng (DC), đúng chỗ (Output) và đúng số vôn (6 V). AC sai loại dòng; vạch 12 V gấp đôi định mức; Input là chỗ bộ nguồn nhận điện từ ổ cắm, không nối dụng cụ vào đó."},
        {"type": MC,
         "question": "Lọ cồn có hai kí hiệu: chất dễ cháy và cấm lửa. Trên bàn đang đốt đèn cồn và có bộ nguồn, nên đặt lọ cồn ở đâu?",
         "options": ["Đậy kín nắp, để xa đèn cồn đang cháy và xa thiết bị điện",
                     "Sát đèn cồn, để rót thêm cho tiện",
                     "Cạnh ổ cắm, để nếu đổ thì chảy xuống sàn",
                     "Trên bộ nguồn cho đỡ chật bàn"],
         "answer": 0,
         "explanation": "Chất dễ cháy phải xa lửa và xa thiết bị điện; đậy nắp để hơi cồn không lan ra. Các chỗ còn lại đặt cồn gần lửa hoặc gần điện."},
        {"type": MC,
         "question": "Một thiết bị ghi Input 110 V ~. Em thấy phích cắm vừa khít ổ 220 V của phòng thực hành. Nhận định đúng là:",
         "options": ["An toàn, vì phích cắm vừa khít",
                     "Chỉ hỏng nếu để cắm lâu",
                     "An toàn nếu bật công tắc thật nhanh rồi tắt",
                     "Không được cắm: 220 V gấp đôi định mức 110 V, dễ cháy hỏng; phải hỏi giáo viên"],
         "answer": 3,
         "explanation": "Chỉ cắm khi hiệu điện thế nguồn tương ứng với dụng cụ. Hình dạng phích chỉ cho biết cắm được, số vôn trên nhãn mới cho biết dùng được; quá áp có thể làm hỏng ngay lần bật đầu."},
        {"type": MC,
         "question": "Dây nguồn của bộ nguồn bị tróc vỏ, hở lõi đồng. Việc đúng là:",
         "options": ["Quấn tạm băng dính rồi dùng tiếp cho kịp giờ",
                     "Tắt công tắc, không dùng nữa và báo giáo viên để đổi dụng cụ khác",
                     "Tự cắt phần hở rồi nối lại cho gọn",
                     "Chỉ cầm vào phần vỏ còn lành khi dùng"],
         "answer": 1,
         "explanation": "Phải kiểm tra dụng cụ trước khi dùng; dây hở là dụng cụ hỏng. Không sửa tạm, không tự sửa, đổi dụng cụ khác theo hướng dẫn của giáo viên."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 2. Các quy tắc an toàn trong phòng thực hành Vật lí"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Kí hiệu trên thiết bị, kí hiệu cảnh báo; 10 quy tắc an toàn khi thực hành; xử lí tình huống ở bàn thực hành",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
