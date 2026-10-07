"""Đóng gói theory.html + câu tự kiểm tra thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_bundle.py
"""
import json

Q = lambda q, o, a, e: {"type": "multiple_choice", "question": q, "options": o, "answer": a, "explanation": e}
EXAM = {
    "title": "Luyện tập — Đo cảm ứng từ bằng cân dòng điện",
    "duration_minutes": 10,
    "questions": [
        Q("Trong thí nghiệm cân dòng điện, cân điện tử đo trực tiếp lực nào?",
          ["Lực từ tác dụng lên dây dẫn.", "Phản lực của lực từ tác dụng lên nam châm đặt trên đĩa cân.", "Trọng lực của dây dẫn.", "Lực đẩy của không khí nóng quanh dây."], 1,
          "Dây giữ trên giá riêng, chỉ nam châm nằm trên đĩa cân. Theo định luật III Newton nam châm chịu lực bằng và ngược chiều lực từ lên dây, nên cân đọc phản lực đó."),
        Q("Đang đo với I = 3,0 A thì cân chỉ +1,45 g. Giữ nguyên độ lớn dòng nhưng đảo chiều dòng điện thì số cân là",
          ["0,00 g.", "+1,45 g.", "−1,45 g.", "+2,90 g."], 2,
          "Đảo chiều dòng thì lực từ lên dây và phản lực lên nam châm đều đổi chiều, độ lớn không đổi nên cân chỉ −1,45 g."),
        Q("Chân giá đỡ khung dây tựa lên chính bệ cân. Khi đóng mạch số cân sẽ",
          ["tăng gấp đôi.", "báo lỗi quá tải.", "vẫn chỉ đúng Δm như trước.", "gần như không đổi vì hai lực ngược chiều triệt tiêu trên cân."], 3,
          "Lực lên dây truyền qua giá xuống cân, lực lên nam châm cũng đè xuống cân; hai lực bằng nhau, ngược chiều nên cân không thấy gì."),
        Q("Cạnh khung l = 4,0 cm, I = 2,5 A, cân tăng Δm = 1,20 g (g = 9,81 m/s²). Cảm ứng từ là",
          ["0,12 T.", "0,012 T.", "4,7·10⁻³ T.", "1,2·10² T."], 0,
          "F = Δm·g = 1,20·10⁻³·9,81 ≈ 1,18·10⁻² N; B = F/(I·l) = 1,18·10⁻²/(2,5·0,040) ≈ 0,12 T. Ra 0,012 là quên g; ra 4,7·10⁻³ là quên chia l; ra 1,2·10² là quên đổi gam sang kg."),
        Q("Dây hợp với đường sức góc 60° nhưng vẫn dùng B = Δm·g/(I·l). Giá trị B tính ra so với thật là",
          ["lớn hơn khoảng 13%.", "nhỏ hơn khoảng 50%.", "không đổi.", "nhỏ hơn khoảng 13%."], 3,
          "Lực chỉ bằng sin 60° ≈ 0,87 lần BIl nên B tính ra nhỏ hơn thật khoảng 13%."),
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 12", "lesson_title": "Bài 11. Thực hành đo độ lớn cảm ứng từ"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Đo cảm ứng từ bằng cân dòng điện",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}
with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("ok", len(bundle["theory_html"]), "bytes theory")
