#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py  rồi  npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts <bundle.json>
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Điện trở. Định luật Ohm",
    "duration_minutes": 10,
    "questions": [
        {"type": MC, "question": "Đặt hiệu điện thế 6 V vào hai đầu một dây dẫn, ampe kế chỉ 200 mA. Điện trở của dây là",
         "options": ["0,03 Ω", "1 200 Ω", "30 Ω", "1,2 Ω"],
         "answer": 2, "explanation": "Đổi 200 mA = 0,2 A; R = U/I = 6/0,2 = 30 Ω. Ra 0,03 Ω là quên đổi mA ra A; ra 1,2 Ω là nhân U·I."},
        {"type": MC, "question": "Đo U và I của một dây constantan khoảng 20 Ω bằng ampe kế có độ chia 0,01 A. Lần đo có dòng nhỏ nhất (0,08 A) cho U/I lệch xa 20 Ω nhất. Lí do hợp lí nhất là",
         "options": ["Dòng nhỏ nên lệch khi đọc ampe kế chiếm tỉ lệ lớn", "Điện trở của dây giảm khi hiệu điện thế nhỏ", "Vôn kế đã bị mắc nối tiếp với đoạn dây", "Định luật Ohm chỉ đúng khi hiệu điện thế lớn"],
         "answer": 0, "explanation": "Lệch nửa vạch 0,005 A so với 0,08 A là khoảng 6 %, so với 0,30 A chưa tới 2 %. Dây constantan gần như giữ nguyên điện trở."},
        {"type": MC, "question": "Một dây dẫn có điện trở 12 Ω. Cắt lấy đúng một nửa chiều dài của nó. Điện trở của đoạn vừa cắt là",
         "options": ["24 Ω", "12 Ω", "3 Ω", "6 Ω"],
         "answer": 3, "explanation": "Cùng vật liệu, cùng tiết diện, R tỉ lệ với chiều dài: 6 Ω. Ra 3 Ω là kết quả khi gập đôi dây."},
        {"type": MC, "question": "Một điện trở 15 Ω đang mắc vào hiệu điện thế 3 V. Tăng hiệu điện thế lên 6 V. Khi đó",
         "options": ["R tăng lên 30 Ω, I giữ nguyên", "R giảm còn 7,5 Ω, I tăng gấp bốn", "R vẫn 15 Ω, I tăng gấp đôi", "R vẫn 15 Ω, I giữ nguyên"],
         "answer": 2, "explanation": "R do chính dây quyết định, không do U. I đi từ 0,2 A lên 0,4 A."},
        {"type": MC, "question": "Trên đồ thị I theo U của hai dây dẫn, tại U = 3 V dây (1) cho I = 0,3 A, dây (2) cho I = 0,1 A (đường (1) dốc hơn). Dây nào có điện trở lớn hơn?",
         "options": ["Dây (2)", "Dây (1)", "Hai dây bằng nhau", "Chưa đủ dữ kiện để so"],
         "answer": 0, "explanation": "Cùng U mà I nhỏ hơn thì cản nhiều hơn: R₂ = 30 Ω, R₁ = 10 Ω. Trên đồ thị I theo U, đường dốc hơn có R nhỏ hơn."},
        {"type": MC, "question": "Một bạn mắc nhầm vôn kế nối tiếp với bóng đèn rồi đóng khoá. Hiện tượng là",
         "options": ["Đèn sáng bình thường, vôn kế chỉ hiệu điện thế của đèn", "Đèn gần như không sáng, vôn kế chỉ gần bằng của nguồn", "Đèn sáng mạnh hơn, vôn kế cháy do dòng điện quá lớn", "Đèn sáng yếu đi một nửa, vôn kế chỉ đúng số 0"],
         "answer": 1, "explanation": "Vôn kế có điện trở rất lớn: mắc nối tiếp làm dòng gần như bằng 0, gần như cả hiệu điện thế nguồn đặt lên vôn kế."},
        {"type": MC, "question": "Dây constantan (ρ = 0,5·10⁻⁶ Ω·m) dài 4 m, tiết diện 0,5 mm², mắc vào hiệu điện thế 12 V. Cường độ dòng điện qua dây là",
         "options": ["48 A", "0,33 A", "3·10⁶ A", "3 A"],
         "answer": 3, "explanation": "S = 0,5·10⁻⁶ m²; R = ρl/S = 4 Ω; I = U/R = 3 A. Ra 3·10⁶ A là quên đổi mm² ra m²."},
    ],
}
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "KHTN 9", "lesson_title": "Bài 11. Điện trở. Định luật Ohm"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Điện trở và cách đo; định luật Ohm, đồ thị I theo U; điện trở dây dẫn phụ thuộc chiều dài, tiết diện, vật liệu",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
