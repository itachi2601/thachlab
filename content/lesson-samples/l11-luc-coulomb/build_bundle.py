"""Đóng gói theory.html + 5 câu tự kiểm tra thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_bundle.py
"""
import json

EXAM = {
    "title": "Luyện tập — Lực tương tác giữa hai điện tích",
    "duration_minutes": 10,
    "questions": [
        {"type": "multiple_choice",
         "question": "Thanh thuỷ tinh cọ xát với lụa thì nhiễm điện dương. Nguyên nhân là",
         "options": ["Thanh thuỷ tinh nhận thêm proton từ lụa.", "Thanh thuỷ tinh nhận thêm electron từ lụa.",
                     "Cọ xát tạo ra điện tích dương mới trên thanh.", "Thanh thuỷ tinh mất bớt electron sang lụa."],
         "answer": 3,
         "explanation": "Chỉ electron di chuyển khi cọ xát; thanh mất electron nên thiếu electron, nhiễm điện dương. Proton không rời hạt nhân, và điện tích không tự sinh ra (bảo toàn điện tích)."},
        {"type": "multiple_choice",
         "question": "Hai điện tích q₁ = q₂ = 2 µC đặt cách nhau 3 cm trong không khí. Lực tương tác giữa chúng là",
         "options": ["4·10⁻³ N", "1,2 N", "4·10⁷ N", "40 N"],
         "answer": 3,
         "explanation": "F = 9·10⁹·(2·10⁻⁶)²/(0,03)² = 3,6·10⁻²/9·10⁻⁴ = 40 N. 4·10⁻³ N là quên đổi cm ra m; 1,2 N là quên bình phương r; 4·10⁷ N là đổi µC thành 10⁻³ C."},
        {"type": "multiple_choice",
         "question": "Hai quả cầu giống hệt mang +6 µC và −2 µC, cho chạm nhau rồi đặt lại đúng khoảng cách cũ. So với lúc đầu, hai quả",
         "options": ["vẫn hút nhau, lực giảm 3 lần.", "chuyển sang đẩy nhau, lực giảm 3 lần.",
                     "chuyển sang đẩy nhau, lực tăng 4/3 lần.", "hết tương tác vì đã trung hoà."],
         "answer": 1,
         "explanation": "Sau khi tách mỗi quả có (6 − 2)/2 = +2 µC, cùng dấu nên đẩy nhau. Tích độ lớn từ 12 còn 4 nên lực giảm 3 lần."},
        {"type": "multiple_choice",
         "question": "Cho AB = 8 cm, q₁ = +9 µC tại A, q₂ = +1 µC tại B. Đặt q₀ ở đâu để nó cân bằng?",
         "options": ["Cách A 2 cm, cách B 6 cm.", "Trung điểm AB.", "Cách A 6 cm, cách B 2 cm.", "Ngoài đoạn AB, phía B, cách B 4 cm."],
         "answer": 2,
         "explanation": "Cùng dấu nên q₀ ở giữa A và B, gần điện tích nhỏ hơn: r₁/r₂ = √9 = 3 và r₁ + r₂ = 8 cm, nên r₁ = 6 cm, r₂ = 2 cm."},
        {"type": "multiple_choice",
         "question": "Hai quả cầu nhỏ giống nhau, mỗi quả 0,4 g, treo cùng một điểm bằng hai dây cách điện dài bằng nhau. Tích điện bằng nhau thì khi cân bằng hai dây hợp nhau góc 90° và hai quả cách nhau 6 cm. Lấy g = 10 m/s². Điện tích mỗi quả là",
         "options": ["80 nC", "20 nC", "40 nC", "10 nC"],
         "answer": 2,
         "explanation": "Mỗi dây lệch 45° nên F = P·tan45° = 4·10⁻³ N. |q| = r·√(F/k) = 0,06·√(4·10⁻³/9·10⁹) = 4·10⁻⁸ C = 40 nC. 80 nC là cho q tỉ lệ với khối lượng (quên căn bậc hai)."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 11", "lesson_title": "Bài 16. Lực tương tác giữa hai điện tích"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Nhiễm điện, định luật Coulomb, tổng hợp và cân bằng lực điện",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}

with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("ok")
