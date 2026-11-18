#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts <bundle.json>
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Dụng cụ đo và thuyết trình một vấn đề khoa học",
    "duration_minutes": 10,
    "questions": [
        {"type": MC, "question": "Đưa nam châm vào rồi rút ra khỏi cuộn dây. Muốn thấy dòng điện cảm ứng đổi chiều, nối hai đầu cuộn dây với dụng cụ nào?",
         "options": ["Điện kế", "Joulemeter", "Biến áp nguồn", "Lăng kính"],
         "answer": 0, "explanation": "Điện kế phát hiện dòng rất nhỏ, vạch 0 ở giữa nên kim lệch sang hai phía khi dòng đổi chiều. Joulemeter đo điện năng, biến áp nguồn là nguồn cấp điện, lăng kính là dụng cụ quang."},
        {"type": MC, "question": "Lỡ mắc ampe kế song song với bóng đèn rồi đóng khoá. Điều gì xảy ra?",
         "options": ["Đèn sáng bình thường, ampe kế chỉ đúng dòng qua đèn", "Đèn sáng bình thường, ampe kế chỉ 0", "Đèn sáng hơn vì có thêm một nhánh", "Dòng dồn qua ampe kế rất lớn, đèn gần như tắt"],
         "answer": 3, "explanation": "Ampe kế có điện trở rất nhỏ; mắc song song với đèn là gần như nối tắt nguồn, dòng rất lớn đi qua ampe kế, có thể làm hỏng dụng cụ hoặc đứt cầu chì."},
        {"type": MC, "question": "Chưa biết dòng trong mạch cỡ bao nhiêu. Đồng hồ có thang 20 mA, 200 mA, 10 A. Cách nào vừa an toàn, vừa đọc chính xác?",
         "options": ["Đo thử ở 10 A, rồi hạ xuống thang nhỏ nhất vẫn lớn hơn số đo", "Đo ngay ở 20 mA cho nhiều chữ số", "Giữ thang 10 A suốt buổi cho chắc", "Đo ở 200 mA vì nằm giữa"],
         "answer": 0, "explanation": "Thang lớn dò cỡ số đo mà không sợ quá tải; biết cỡ rồi hạ thang để có thêm chữ số. Đo ngay ở thang nhỏ dễ quá thang, giữ thang 10 A thì kết quả thô."},
        {"type": MC, "question": "Đồng hồ đa năng có thang dòng 20 mA, 200 mA, 10 A và thang hiệu điện thế 2 V, 20 V, 200 V. Dòng qua đèn LED khoảng 15 mA, nguồn 3 V. Chọn thang chính xác nhất mà không quá thang.",
         "options": ["20 mA và 2 V", "20 mA và 20 V", "200 mA và 20 V", "10 A và 200 V"],
         "answer": 1, "explanation": "15 mA nhỏ hơn 20 mA nên thang 20 mA; 3 V lớn hơn 2 V nên phải dùng thang 20 V."},
        {"type": MC, "question": "Em cần thông tin \"sạc điện thoại qua đêm có làm chai pin không\". Nguồn nào nên làm chỗ dựa chính?",
         "options": ["Video có nhiều lượt xem nhất", "Bình luận của một người tự nhận là kĩ sư", "Hướng dẫn của hãng điện thoại, đối chiếu thêm bài của một trường đại học", "Bài không ghi tác giả, ngày đăng nhưng được chia sẻ nhiều"],
         "answer": 2, "explanation": "Nguồn đáng tin có tổ chức chịu trách nhiệm, có ngày đăng và được đối chiếu với một nguồn độc lập. Lượt xem, lượt chia sẻ hay lời tự nhận không làm thông tin đúng hơn."},
        {"type": MC, "question": "Trong bài thuyết trình \"Có nên sạc điện thoại qua đêm?\", lời khuyên \"rút sạc khi pin đầy\" nên đặt ở đâu?",
         "options": ["Phần mở đầu, để gây chú ý", "Giữa thân bài, trước khi đưa số liệu", "Slide cuối cùng ghi tên nguồn tham khảo", "Phần kết luận, sau khi đã trình bày bằng chứng"],
         "answer": 3, "explanation": "Đề xuất, kiến nghị rút ra từ bằng chứng nên đặt ở phần kết luận, sau khi thân bài đã trình bày số liệu."},
    ],
}
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "KHTN 9", "lesson_title": "Bài 1. Giới thiệu một số dụng cụ và hoá chất. Thuyết trình một vấn đề khoa học"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Dụng cụ đo và thiết bị Vật lí KHTN 9; mắc ampe kế, vôn kế, chọn thang đo; an toàn điện, laser, hoá chất; các bước báo cáo và thuyết trình",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
