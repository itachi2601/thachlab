"""Đóng gói theory.html + 5 câu tự kiểm tra thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_bundle.py
"""
import json

EXAM = {
    "title": "Luyện tập — Thang nhiệt độ",
    "duration_minutes": 10,
    "questions": [
        {
            "type": "multiple_choice",
            "question": "Nhiệt độ của một vật cho biết điều gì khi vật tiếp xúc với vật khác?",
            "options": [
                "Trạng thái cân bằng nhiệt và chiều truyền nhiệt năng giữa các vật.",
                "Khối lượng của vật.",
                "Thể tích của vật.",
                "Số phân tử có trong vật.",
            ],
            "answer": 0,
            "explanation": "Nhiệt độ cho biết trạng thái cân bằng nhiệt của các vật tiếp xúc nhau và chiều truyền nhiệt năng: nhiệt năng truyền từ vật có nhiệt độ cao hơn sang vật có nhiệt độ thấp hơn.",
        },
        {
            "type": "multiple_choice",
            "question": "Hai mốc quy ước của thang nhiệt độ Celsius là",
            "options": [
                "nhiệt độ nước đá đang tan là 0 °C và nhiệt độ nước đá đông đặc là 100 °C.",
                "nhiệt độ nước đá đang tan là 0 °C và nhiệt độ hơi nước đang sôi là 100 °C.",
                "nhiệt độ thấp nhất là 0 °C và nhiệt độ cao nhất là 100 °C.",
                "nhiệt độ nước đá đang tan là 32 °C và nhiệt độ hơi nước đang sôi là 212 °C.",
            ],
            "answer": 1,
            "explanation": "Thang Celsius lấy nhiệt độ nóng chảy của nước đá tinh khiết là 0 °C và nhiệt độ sôi của nước tinh khiết ở áp suất tiêu chuẩn là 100 °C; khoảng giữa chia thành 100 khoảng bằng nhau. 32 °F và 212 °F là hai mốc của thang Fahrenheit.",
        },
        {
            "type": "multiple_choice",
            "question": "Điều nào sau đây đúng khi nói về 0 K?",
            "options": [
                "0 K là nhiệt độ nước đá đang tan, tức 0 °C.",
                "0 K là nhiệt độ thấp nhất mà vật có thể có, tức −273,15 °C.",
                "0 K là nhiệt độ thấp nhất mà vật có thể có, tức 0 °C.",
                "0 K là nhiệt độ sôi của nước ở áp suất tiêu chuẩn.",
            ],
            "answer": 1,
            "explanation": "Độ không tuyệt đối 0 K ứng với −273,15 °C. Nước đá đang tan ở 0 °C, tức 273,15 K — hai thang lệch nhau đúng ở chỗ gốc.",
        },
        {
            "type": "multiple_choice",
            "question": "Nhiệt độ phòng là 25 °C. Trên thang Fahrenheit, nhiệt độ đó là",
            "options": ["25 °F.", "57 °F.", "77 °F.", "298 °F."],
            "answer": 2,
            "explanation": "t(°F) = 1,8·t(°C) + 32 = 1,8 × 25 + 32 = 77 °F. Các phương án sai ứng với ba lỗi hay gặp: giữ nguyên con số, quên nhân 1,8, hoặc cộng 273 của thang Kelvin.",
        },
        {
            "type": "multiple_choice",
            "question": "Một chi tiết thép nguội từ 200 °C xuống 30 °C. Độ giảm nhiệt độ đó là",
            "options": [
                "170 °C, tức 170 K và 306 °F.",
                "170 °C, tức 443 K và 306 °F.",
                "170 °C, tức 170 K và 170 °F.",
                "170 °C, tức 306 K và 170 °F.",
            ],
            "answer": 0,
            "explanation": "Khoảng chênh trên thang Kelvin bằng khoảng chênh trên thang Celsius (1 K = 1 °C) nên ΔT = 170 K; trên thang Fahrenheit phải nhân 1,8: Δt(°F) = 1,8 × 170 = 306 °F. Không cộng 273 vào một khoảng chênh — 273 chỉ dùng khi đổi một giá trị nhiệt độ.",
        },
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 12", "lesson_title": "Bài 2. Thang nhiệt độ"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Ba thang đo, một nhiệt độ",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}

with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("ok", len(bundle["theory_html"]), "bytes theory")
