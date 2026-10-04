"""Đóng gói theory.html + 5 câu tự kiểm tra thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_bundle.py
"""
import json

EXAM = {
    "title": "Luyện tập — An toàn phóng xạ",
    "duration_minutes": 10,
    "questions": [
        {
            "type": "multiple_choice",
            "question": "Hai kỹ thuật viên cùng đứng cách nguồn phóng xạ 2 m; người A vào trong 5 phút, người B vào trong 20 phút. Vì sao người B nhận liều lớn hơn?",
            "options": [
                "Vì thời gian chiếu xạ dài hơn — cùng khoảng cách, liều tỉ lệ thuận với thời gian.",
                "Vì đứng lâu thì khả năng đâm xuyên của tia mạnh dần lên.",
                "Vì nguồn phóng xạ mạnh dần trong lúc chiếu.",
                "Không ai nhận nhiều hơn, vì hai người đứng cùng khoảng cách.",
            ],
            "answer": 0,
            "explanation": "Cùng khoảng cách thì liều nhận được tỉ lệ thuận với thời gian phơi nhiễm: B ở trong 20 phút nên nhận gấp 4 lần A. Khả năng đâm xuyên và độ mạnh của nguồn là tính chất của nguồn và loại tia, không đổi theo thời gian đứng gần.",
        },
        {
            "type": "multiple_choice",
            "question": "Một mẫu mô phơi nhiễm tia alpha, nhận liều hấp thụ D = 0,05 Gy. Liều tương đương của mẫu mô đó là",
            "options": [
                "0,05 Sv.",
                "1 Sv.",
                "0,05 Gy — vì Gy và Sv là một.",
                "0,0025 Sv.",
            ],
            "answer": 1,
            "explanation": "H = w_R·D = 20 × 0,05 = 1 Sv, vì hạt alpha có hệ số chất lượng w_R = 20. Phương án 0,05 Sv là quên hệ số chất lượng; 0,05 Gy là gộp hai đơn vị (Gy đo năng lượng mô hấp thụ, Sv đo mức nguy hiểm); 0,0025 Sv là chia cho 20 thay vì nhân.",
        },
        {
            "type": "multiple_choice",
            "question": "Máy đo cho suất liều 120 µSv/h tại khoảng cách 2 m. Muốn liều nhận được không quá 20 µSv thì ở khoảng cách 4 m được đứng tối đa bao lâu?",
            "options": ["40 phút.", "10 phút.", "20 phút.", "2 giờ 40 phút."],
            "answer": 0,
            "explanation": "Ở 4 m, khoảng cách gấp đôi so với 2 m nên suất liều giảm 4 lần: 120/4 = 30 µSv/h. Thời gian tối đa t = 20 µSv ÷ 30 µSv/h = 2/3 h = 40 phút. 10 phút là quên đổi khoảng cách; 20 phút là dùng 1/r thay vì 1/r²; 2 giờ 40 phút là chia cho 4² = 16.",
        },
        {
            "type": "multiple_choice",
            "question": "Điểm khác nhau cơ bản giữa chẩn đoán hình ảnh phóng xạ và xạ trị ung thư là",
            "options": [
                "Chẩn đoán dùng đồng vị phóng xạ, xạ trị thì không.",
                "Chẩn đoán đưa nguồn vào trong, xạ trị chiếu từ ngoài.",
                "Chẩn đoán liều thấp để ghi hình, xạ trị liều cao để diệt tế bào.",
                "Chẩn đoán không gây liều, chỉ xạ trị gây liều.",
            ],
            "answer": 2,
            "explanation": "Cả hai đều dùng bức xạ, khác nhau ở mục đích và mức liều: chẩn đoán cần liều thấp nhất còn đủ ghi hình, xạ trị cần liều cao đủ diệt tế bào ung thư. Xạ trị cũng dùng đồng vị phóng xạ (dược chất uống, tiêm) và chẩn đoán cũng gây liều, chỉ là liều thấp.",
        },
        {
            "type": "multiple_choice",
            "question": "Cách làm nào KHÔNG phù hợp với chất thải phóng xạ mức cao?",
            "options": [
                "Thuỷ tinh hoá, bọc thép rồi chôn sâu trong tầng địa chất.",
                "Lưu trong bể nước để chắn tia nhiều năm.",
                "Pha loãng với nước rồi xả ra sông.",
                "Phân loại theo chu kì bán rã trước khi lưu giữ.",
            ],
            "answer": 2,
            "explanation": "Pha loãng chỉ làm nồng độ thấp đi trong chốc lát, chất phóng xạ vẫn vào nước, vào sinh vật rồi tích tụ theo chuỗi thức ăn. Nguyên tắc đúng là cô lập và cô đặc: giảm thể tích, cố định trong khối bền, cách li trong bể nước hoặc tầng địa chất ổn định, và phân loại theo chu kì bán rã trước.",
        },
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 12", "lesson_title": "Bài 18. An toàn phóng xạ"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Liều chiếu xạ và nguyên tắc an toàn",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}

with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("ok", len(bundle["theory_html"]), "bytes theory")
