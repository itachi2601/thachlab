"""Đóng gói theory.html + 5 câu tự kiểm tra thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_bundle.py
"""
import json

EXAM = {
    "title": "Luyện tập — Khái niệm từ trường",
    "duration_minutes": 10,
    "questions": [
        {
            "type": "multiple_choice",
            "question": "Hai dây dẫn thẳng, dài, song song, có dòng điện chạy cùng chiều. Kết luận nào đúng?",
            "options": [
                "Hai dây hút nhau, vì giữa chúng có tương tác từ.",
                "Hai dây đẩy nhau, vì hai dòng điện cùng chiều thì cùng cực.",
                "Không hút cũng không đẩy, vì hai dây không phải nam châm.",
                "Hai dây đẩy nhau, vì mỗi dây là một nam châm thẳng.",
            ],
            "answer": 0,
            "explanation": "Dòng điện có từ tính: mỗi dây tạo ra từ trường tác dụng lực lên dây kia. Hai dòng điện cùng chiều hút nhau, ngược chiều đẩy nhau. Chỉ nam châm mới có cực N, S nên phương án nói về \"cùng cực\" của dòng điện là sai.",
        },
        {
            "type": "multiple_choice",
            "question": "Hướng của từ trường tại một điểm được quy ước là",
            "options": [
                "hướng từ đông sang tây.",
                "hướng nam – bắc của kim nam châm nhỏ nằm cân bằng tại điểm đó.",
                "hướng từ vật nặng sang vật nhẹ đặt gần đó.",
                "hướng chuyển động của các hạt mang điện đặt tại điểm đó.",
            ],
            "answer": 1,
            "explanation": "Từ trường định hướng cho kim nam châm nhỏ: lấy chiều từ cực nam sang cực bắc của kim lúc kim đã nằm cân bằng tại điểm đó làm chiều của từ trường tại điểm ấy.",
        },
        {
            "type": "multiple_choice",
            "question": "Điều nào sau đây KHÔNG phải là tính chất của đường sức từ?",
            "options": [
                "Qua mỗi điểm trong không gian chỉ vẽ được một đường sức.",
                "Chỗ đường sức mau thì từ trường mạnh hơn chỗ đường sức thưa.",
                "Đường sức từ là đường cong hở, bắt đầu ở cực bắc và kết thúc ở cực nam.",
                "Chiều của đường sức từ là chiều của từ trường tại mỗi điểm.",
            ],
            "answer": 2,
            "explanation": "Đường sức từ là đường cong kín: ra khỏi cực bắc ở bên ngoài nam châm, đi vào cực nam, rồi đi tiếp bên trong nam châm từ nam sang bắc. Vì vậy nó không có điểm đầu và điểm cuối. Ba tính chất còn lại đều đúng.",
        },
        {
            "type": "multiple_choice",
            "question": "Trên một hình vẽ đường sức từ, vùng A có đường sức mau hơn hẳn vùng B. Kết luận nào đúng?",
            "options": [
                "Từ trường ở vùng A mạnh hơn ở vùng B.",
                "Từ trường ở vùng A yếu hơn ở vùng B, vì chỗ đó chật.",
                "Đường sức mau hay thưa không liên quan đến độ mạnh của từ trường.",
                "Hai vùng có từ trường bằng nhau vì cùng một nam châm.",
            ],
            "answer": 0,
            "explanation": "Theo quy ước vẽ, mật độ đường sức biểu diễn độ lớn của cảm ứng từ: đường sức mau ở chỗ từ trường mạnh, thưa ở chỗ yếu. Số liệu đo bằng cảm biến ở gần và xa cực nam châm cũng cho thấy đúng như vậy.",
        },
        {
            "type": "multiple_choice",
            "question": "Một la bàn nằm ngang đặt trong vùng có thành phần nằm ngang của từ trường Trái Đất là 30 µT hướng bắc. Một dây dẫn tạo thêm tại đó từ trường 40 µT hướng đông. Kim la bàn lệch khỏi hướng bắc một góc gần nhất với giá trị nào?",
            "options": ["$37^\\circ$", "$53^\\circ$", "$90^\\circ$", "$0^\\circ$"],
            "answer": 1,
            "explanation": "Hai từ trường thành phần vuông góc nhau nên cảm ứng từ tổng hợp có độ lớn $\\sqrt{30^2 + 40^2} = 50$ µT và $\\tan\\alpha = 40/30 \\approx 1{,}33$, suy ra $\\alpha \\approx 53^\\circ$. Kết quả $37^\\circ$ là góc còn lại của tam giác vuông, dễ lấy nhầm.",
        },
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 12", "lesson_title": "Bài 9. Khái niệm từ trường"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Tương tác từ, từ trường và đường sức từ",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}

with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("ok", len(bundle["theory_html"]), "bytes theory")
