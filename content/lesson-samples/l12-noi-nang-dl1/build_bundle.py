"""Đóng gói theory.html + 6 câu tự kiểm tra thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_bundle.py
"""
import json

EXAM = {
    "title": "Luyện tập — Nội năng và định luật I",
    "duration_minutes": 10,
    "questions": [
        {
            "type": "multiple_choice",
            "question": "Nội năng của một vật là",
            "options": [
                "tổng động năng và thế năng của các phân tử cấu tạo nên vật.",
                "nhiệt lượng mà vật nhận được trong quá trình truyền nhiệt.",
                "động năng của vật khi vật chuyển động.",
                "tổng công mà vật sinh ra và nhiệt lượng vật toả ra.",
            ],
            "answer": 0,
            "explanation": "Nội năng là tổng động năng và thế năng của các phân tử cấu tạo nên vật, kí hiệu U, đơn vị jun (J). Nhiệt lượng và công chỉ là phần năng lượng truyền đi, không phải nội năng.",
        },
        {
            "type": "multiple_choice",
            "question": "Hai ấm nước cùng ở 60 °C: ấm A chứa 0,2 kg, ấm B chứa 2 kg. Kết luận nào đúng?",
            "options": [
                "Hai ấm có nội năng bằng nhau vì cùng nhiệt độ.",
                "Ấm B có nội năng lớn hơn vì có nhiều phân tử hơn.",
                "Ấm A có nội năng lớn hơn vì phân tử chuyển động nhanh hơn.",
                "Không so sánh được nội năng của hai ấm khác khối lượng.",
            ],
            "answer": 1,
            "explanation": "Cùng nhiệt độ nghĩa là mỗi phân tử có cùng mức động năng trung bình. Nội năng là tổng của mọi phân tử, nên ấm B nhiều nước gấp 10 lần thì nội năng lớn hơn khoảng 10 lần.",
        },
        {
            "type": "multiple_choice",
            "question": "Cách nào sau đây làm biến đổi nội năng của vật bằng hình thức truyền nhiệt?",
            "options": [
                "Xoa hai bàn tay vào nhau cho nóng lên.",
                "Nén khí trong bơm xe đạp làm khí nóng lên.",
                "Hơ ống nghiệm trên ngọn lửa đèn cồn.",
                "Chà một miếng kim loại xuống sàn nhà.",
            ],
            "answer": 2,
            "explanation": "Hơ ống nghiệm trên lửa: khí trong ống và ngọn lửa chênh nhiệt độ, không có lực nào làm dịch chuyển nên đây là truyền nhiệt. Ba trường hợp còn lại đều có lực làm vật dịch chuyển — thực hiện công.",
        },
        {
            "type": "multiple_choice",
            "question": "Cần bao nhiêu nhiệt lượng để đun 2 kg nước từ 25 °C lên 100 °C? Lấy c = 4200 J/(kg·K).",
            "options": ["210 000 J.", "630 000 J.", "840 000 J.", "8 400 J."],
            "answer": 1,
            "explanation": "Q = mcΔt = 4200 × 2 × (100 − 25) = 630 000 J. Δt là độ tăng nhiệt độ, phải lấy 100 − 25 = 75 K, không lấy 25 hay 100.",
        },
        {
            "type": "multiple_choice",
            "question": "Người ta truyền cho khối khí trong xilanh nhiệt lượng 100 J; khí giãn nở sinh công 60 J. Độ biến thiên nội năng của khối khí là",
            "options": ["+160 J.", "+40 J.", "−40 J.", "+60 J."],
            "answer": 1,
            "explanation": "Khí nhận nhiệt nên Q = +100 J; khí sinh công nên A = −60 J. Vậy ΔU = A + Q = −60 + 100 = +40 J: nội năng tăng. Lỗi ra +160 J là quên đổi dấu công.",
        },
        {
            "type": "multiple_choice",
            "question": "Một lượng khí bị nén, nhận công 90 J, đồng thời toả ra môi trường 30 J. Độ biến thiên nội năng của khí là",
            "options": ["+120 J.", "+60 J.", "−60 J.", "−120 J."],
            "answer": 1,
            "explanation": "Nhận công: A = +90 J. Toả nhiệt: Q = −30 J. ΔU = 90 − 30 = +60 J — nội năng tăng, khí nóng lên.",
        },
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 12", "lesson_title": "Bài 3. Nội năng. Định luật 1 của nhiệt động lực học"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Nội năng và định luật I nhiệt động lực học",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}

with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("ok", len(bundle["theory_html"]), "bytes theory")
