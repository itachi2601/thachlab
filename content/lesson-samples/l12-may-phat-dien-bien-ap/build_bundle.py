"""Đóng gói theory.html + 5 câu tự kiểm tra thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_bundle.py
"""
import json

EXAM = {
    "title": "Luyện tập — Máy phát điện xoay chiều. Máy biến áp",
    "duration_minutes": 10,
    "questions": [
        {
            "type": "multiple_choice",
            "question": "Đường dây truyền tải điện đi xa được đẩy lên điện áp rất cao (500 kV) chủ yếu để",
            "options": [
                "sinh thêm điện năng, vì điện áp cao thì năng lượng nhiều hơn.",
                "giảm hao phí toả nhiệt trên dây dẫn.",
                "giữ cho dòng điện trên đường dây không đổi chiều.",
                "tăng tần số dòng điện cho động cơ quay nhanh hơn.",
            ],
            "answer": 1,
            "explanation": "Với cùng công suất P, dòng trên dây là I = P/U. Điện áp càng cao thì dòng càng nhỏ, mà hao phí là ΔP = RI² — nên hao phí giảm rất mạnh. Tăng U lên k lần thì hao phí giảm k² lần. Máy biến áp không sinh thêm điện năng, không đổi tần số, và dòng trên đường dây vẫn là dòng xoay chiều đổi chiều liên tục.",
        },
        {
            "type": "multiple_choice",
            "question": "Rô-to của một máy phát điện xoay chiều có 2 cặp cực, quay 1500 vòng/phút. Tần số dòng điện phát ra là",
            "options": ["25 Hz.", "50 Hz.", "100 Hz.", "3000 Hz."],
            "answer": 1,
            "explanation": "Đổi tốc độ quay ra vòng/s: n = 1500/60 = 25 vòng/s. Rồi f = np = 25 × 2 = 50 Hz. Các phương án sai ứng với ba lỗi hay gặp: quên nhân số cặp cực (25 Hz), nhầm 2 cặp cực thành 4 cực (100 Hz), quên chia 60 (3000 Hz).",
        },
        {
            "type": "multiple_choice",
            "question": "Một máy biến áp lí tưởng có cuộn sơ cấp 500 vòng, cuộn thứ cấp 50 vòng. Nối cuộn sơ cấp với điện áp xoay chiều 220 V. Điện áp hiệu dụng hai đầu cuộn thứ cấp là",
            "options": ["22 V.", "2200 V.", "220 V.", "2,2 V."],
            "answer": 0,
            "explanation": "U2 = U1·N2/N1 = 220 × 50/500 = 22 V. Ít vòng hơn nên điện áp nhỏ hơn — máy hạ áp. Viết ngược tỉ số cho 2200 V; tưởng máy biến áp không đổi điện áp cho 220 V.",
        },
        {
            "type": "multiple_choice",
            "question": "Cùng công suất truyền đi và cùng đường dây, nếu tăng điện áp nơi phát lên 10 lần thì hao phí trên đường dây",
            "options": ["giảm 10 lần.", "giảm 100 lần.", "không đổi.", "tăng 10 lần."],
            "answer": 1,
            "explanation": "I = P/U nên tăng U lên 10 lần thì I giảm 10 lần; hao phí ΔP = RI² tỉ lệ với bình phương dòng điện nên giảm 10² = 100 lần.",
        },
        {
            "type": "multiple_choice",
            "question": "Một máy biến áp lí tưởng tăng điện áp từ 220 V lên 22 kV. Điều nào sau đây đúng?",
            "options": [
                "Công suất hai cuộn bằng nhau, cường độ hiệu dụng giảm 100 lần.",
                "Công suất cuộn thứ cấp lớn hơn 100 lần vì điện áp lớn hơn 100 lần.",
                "Công suất cuộn thứ cấp nhỏ hơn 100 lần vì cường độ giảm 100 lần.",
                "Tần số dòng điện cũng tăng 100 lần.",
            ],
            "answer": 0,
            "explanation": "Máy biến áp chỉ đổi điện áp, công suất giữ nguyên: P1 = P2 nên U tăng bao nhiêu lần thì I giảm bấy nhiêu lần. Nếu công suất cũng tăng thì năng lượng sinh ra từ hư không, vi phạm bảo toàn năng lượng. Tần số không đổi vì máy biến áp không tự tạo ra dao động.",
        },
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 12", "lesson_title": "Bài 14. Máy phát điện xoay chiều. Máy biến áp"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Máy phát điện xoay chiều và máy biến áp",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}

with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("ok", len(bundle["theory_html"]), "bytes theory")
