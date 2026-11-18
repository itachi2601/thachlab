#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts <bundle.json>
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Vòng năng lượng trên Trái Đất. Năng lượng hoá thạch",
    "duration_minutes": 10,
    "questions": [
        {"type": MC, "question": "Năng lượng chứa trong than đá lúc đầu đến từ đâu?",
         "options": ["Từ nhà máy nhiệt điện nạp vào than khi đốt", "Từ ánh sáng Mặt Trời, cây cổ đại giữ lại nhờ quang hợp", "Từ sức nóng lòng đất, không liên quan Mặt Trời", "Than tự sinh ra năng lượng, không lấy từ đâu cả"],
         "answer": 1, "explanation": "Than hình thành từ xác cây cổ đại. Khi sống, cây quang hợp biến năng lượng ánh sáng Mặt Trời thành năng lượng hoá học; nhiệt và áp suất lòng đất chỉ biến xác cây thành than."},
        {"type": MC, "question": "Nhà máy điện nào dưới đây dùng nguồn năng lượng không có gốc từ Mặt Trời?",
         "options": ["Thuỷ điện: nước hồ chảy qua tua bin", "Điện gió: gió quay cánh quạt", "Điện địa nhiệt: hơi nóng từ lòng đất", "Nhiệt điện than: đốt than đá"],
         "answer": 2, "explanation": "Nhiệt lòng đất có sẵn bên trong Trái Đất. Nước lên hồ nhờ Mặt Trời làm bay hơi, gió do Mặt Trời làm nóng không đều, than là năng lượng Mặt Trời cây cổ đại cất lại."},
        {"type": MC, "question": "Khi cây xanh quang hợp, năng lượng chuyển hoá thế nào?",
         "options": ["Năng lượng ánh sáng thành năng lượng hoá học", "Năng lượng hoá học thành năng lượng ánh sáng", "Động năng của gió thành năng lượng hoá học", "Năng lượng hoá học thành nhiệt năng"],
         "answer": 0, "explanation": "Lá hấp thụ ánh sáng, tạo chất hữu cơ chứa năng lượng hoá học. Hoá năng thành nhiệt là khi đốt hoặc hô hấp."},
        {"type": MC, "question": "Cùng một loại xăng, giá bán ở vùng xa kho cảng thường cao hơn ở thành phố lớn. Lí do chính là gì?",
         "options": ["Xăng ở vùng xa tốt hơn, cháy được lâu hơn", "Phải tốn thêm chi phí chở xăng tới đó", "Vùng xa ít nắng nên xăng hình thành chậm hơn", "Người vùng xa dùng ít xăng nên xăng đắt"],
         "answer": 1, "explanation": "Giá nhiên liệu phụ thuộc chi phí khai thác và vận chuyển; chở càng xa thì chi phí cộng vào giá càng lớn."},
        {"type": MC, "question": "Vì sao than đá, dầu mỏ được xếp vào năng lượng không tái tạo?",
         "options": ["Vì đốt xong chúng biến mất hoàn toàn, không còn chất gì", "Vì Trái Đất không còn cây cối để tạo than mới", "Vì chúng không có gốc từ năng lượng Mặt Trời", "Vì hình thành mất hàng triệu năm, ta dùng nhanh hơn rất nhiều"],
         "answer": 3, "explanation": "Than, dầu, khí cần hàng triệu năm chôn vùi mới hình thành, trong khi con người dùng hết chỉ trong vài trăm năm. Cây vẫn mọc nhưng không kịp bù."},
        {"type": MC, "question": "Xe máy chạy xăng. Chuỗi nào đúng thứ tự, từ gốc tới bánh xe quay?",
         "options": ["Xăng → Mặt Trời → sinh vật biển cổ → động cơ", "Sinh vật biển cổ → Mặt Trời → dầu mỏ → động cơ", "Mặt Trời → sinh vật biển cổ → dầu mỏ → xăng → động cơ", "Lòng đất nóng → dầu mỏ → xăng → động cơ"],
         "answer": 2, "explanation": "Sinh vật biển cổ sống nhờ quang hợp, xác bị chôn vùi thành dầu mỏ; lọc dầu ra xăng; động cơ đốt xăng: hoá năng → nhiệt → cơ năng. Mặt Trời luôn là khâu đầu."},
    ],
}
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "KHTN 9", "lesson_title": "Bài 16. Vòng năng lượng trên Trái Đất. Năng lượng hoá thạch"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Mặt Trời là nguồn gốc của hầu hết năng lượng; vòng năng lượng (nước, gió, quang hợp); nhiên liệu hoá thạch hình thành, không tái tạo; ưu, nhược điểm, giá và tác động môi trường",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
