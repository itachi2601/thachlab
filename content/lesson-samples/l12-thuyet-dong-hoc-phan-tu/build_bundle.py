"""Đóng gói theory.html + 5 câu tự kiểm tra thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_bundle.py
"""
import json

EXAM = {
    "title": "Luyện tập — Thuyết động học phân tử chất khí",
    "duration_minutes": 10,
    "questions": [
        {
            "type": "multiple_choice",
            "question": "Đặt một hộp kính kín chứa khói hương trên bàn, không có gió. Các hạt khói trong hộp chuyển động hỗn loạn vì",
            "options": [
                "hạt khói tự bò như một con vật tí hon.",
                "ánh sáng chiếu vào hộp đã đẩy các hạt khói đi.",
                "trong hộp kín luôn có một dòng khí nhẹ thổi qua.",
                "các phân tử khí va đập vào hạt khói từ mọi phía, lúc mạnh lúc yếu, không cân bằng nhau.",
            ],
            "answer": 3,
            "explanation": "Hạt khói to hơn phân tử khí hàng nghìn lần nên không tự chuyển động được. Nó bị các phân tử khí va đập từ mọi phía; số va đập hai phía không bao giờ cân bằng tuyệt đối nên hạt bị đẩy lệch liên tục — đó là chuyển động Brown, bằng chứng gián tiếp cho chuyển động hỗn loạn không ngừng của phân tử.",
        },
        {
            "type": "multiple_choice",
            "question": "Điều nào đúng khi nói về lực tương tác giữa các phân tử khí?",
            "options": [
                "Giữa các phân tử khí không có lực nào.",
                "Có cả lực hút và lực đẩy, nhưng rất yếu vì khoảng cách giữa các phân tử lớn.",
                "Chỉ có lực hút rất mạnh, mạnh hơn cả ở thể rắn.",
                "Lực đẩy mạnh đến mức các phân tử không bao giờ lại gần nhau.",
            ],
            "answer": 1,
            "explanation": "Giữa các phân tử khí có cả lực hút lẫn lực đẩy (gọi chung là lực liên kết), nhưng khoảng cách giữa chúng lớn gấp nhiều lần kích thước nên lực này rất yếu — yếu hơn hẳn thể lỏng và thể rắn. Vì thế khí dễ nén và dễ chiếm hết thể tích bình chứa.",
        },
        {
            "type": "multiple_choice",
            "question": "Câu nào mô tả đúng mô hình khí lí tưởng?",
            "options": [
                "Phân tử đứng yên, chỉ chuyển động khi bị nén.",
                "Phân tử hút nhau rất mạnh nên dính thành cụm.",
                "Phân tử là chất điểm; giữa hai va chạm đi thẳng đều; va chạm hoàn toàn đàn hồi.",
                "Kích thước phân tử tính đúng như thực tế, chỉ bỏ qua khối lượng.",
            ],
            "answer": 2,
            "explanation": "Mô hình khí lí tưởng gồm bốn nội dung: bỏ qua kích thước phân tử (coi là chất điểm), bỏ qua lực tương tác khi chưa va chạm, giữa hai va chạm phân tử chuyển động thẳng đều, và va chạm với nhau hoặc với thành bình là va chạm hoàn toàn đàn hồi. Khí thực ở nhiệt độ và áp suất bình thường gần đúng như khí lí tưởng.",
        },
        {
            "type": "multiple_choice",
            "question": "Hai bình giống nhau, cùng ở điều kiện tiêu chuẩn: bình A chứa 1 mol N₂, bình B chứa 1 mol CO₂. Kết luận nào đúng?",
            "options": [
                "Hai bình cùng thể tích khí, khối lượng khí khác nhau.",
                "Hai bình cùng khối lượng khí, thể tích khác nhau.",
                "Bình N₂ có thể tích lớn hơn vì phân tử N₂ nhẹ hơn.",
                "Hai bình cùng thể tích và cùng khối lượng khí.",
            ],
            "answer": 0,
            "explanation": "Ở điều kiện tiêu chuẩn, thể tích mol của mọi chất khí đều bằng 22,4 lít, nên cùng 1 mol thì cùng thể tích. Khối lượng lại bằng n·M, mà khối lượng mol khác nhau: N₂ là 28 g/mol còn CO₂ là 44 g/mol, nên bình CO₂ nặng hơn.",
        },
        {
            "type": "multiple_choice",
            "question": "Một bình chứa 2 mol khí helium (He, M = 4 g/mol) ở điều kiện tiêu chuẩn. Khối lượng và thể tích của lượng khí đó là",
            "options": ["8 g và 2 lít.", "4 g và 44,8 lít.", "8 g và 22,4 lít.", "8 g và 44,8 lít."],
            "answer": 3,
            "explanation": "Khối lượng m = n·M = 2 × 4 = 8 g. Thể tích ở đktc V = n × 22,4 = 2 × 22,4 = 44,8 lít. Ba phương án sai ứng với ba kiểu lẫn: lấy số mol 2 làm số lít, dùng khối lượng mol của 1 mol mà quên nhân với n, và quên nhân 22,4 với n.",
        },
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 12", "lesson_title": "Bài 5. Thuyết động học phân tử chất khí"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Phân tử chuyển động không ngừng — mol và số Avogadro",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}

with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("ok", len(bundle["theory_html"]), "bytes theory", len(EXAM["questions"]), "câu luyện tập")
