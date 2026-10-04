"""Đóng gói theory.html + 5 câu tự kiểm tra thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_bundle.py
"""
import json

EXAM = {
    "title": "Luyện tập — Hiện tượng phóng xạ",
    "duration_minutes": 10,
    "questions": [
        {
            "type": "multiple_choice",
            "question": "Điều gì quyết định hạt nhân nào của một mẫu phóng xạ sẽ phân rã ở giây tiếp theo?",
            "options": [
                "Nhiệt độ: chỗ nóng hơn phân rã trước.",
                "Vị trí: hạt nhân gần bề mặt phân rã trước.",
                "Không gì cả — đó là chuyện ngẫu nhiên của từng hạt nhân.",
                "Khối lượng mẫu: nặng thì phân rã đều hơn.",
            ],
            "answer": 2,
            "explanation": "Phóng xạ có tính ngẫu nhiên: chỉ biết được xác suất phân rã của từng hạt nhân trong một khoảng thời gian, không biết hạt nào phân rã lúc nào. Nhiệt độ, áp suất, vị trí và khối lượng mẫu đều không quyết định điều đó.",
        },
        {
            "type": "multiple_choice",
            "question": "Vì sao tia anpha lệch về bản âm còn tia beta trừ lệch về bản dương trong cùng một điện trường đều?",
            "options": [
                "Vì tia anpha nặng hơn nên rơi xuống.",
                "Vì hạt anpha mang điện dương còn electron mang điện âm.",
                "Vì tia anpha phát ra từ bản âm.",
                "Vì tia anpha bị hấp thụ rồi đổi chiều.",
            ],
            "answer": 1,
            "explanation": "Chiều lệch do điện tích quyết định: hạt anpha là hạt nhân heli mang +2e nên bị đẩy về bản âm; electron mang −e nên bị đẩy về bản dương. Tia gamma không mang điện nên bay thẳng, không lệch.",
        },
        {
            "type": "multiple_choice",
            "question": "Một mẫu poloni có chu kì bán rã 138 ngày. Sau 414 ngày, bao nhiêu phần trăm số hạt nhân ban đầu còn lại?",
            "options": ["12,5%.", "87,5%.", "25%.", "50%."],
            "answer": 0,
            "explanation": "t/T = 414/138 = 3, tức đúng 3 chu kì bán rã, nên còn lại 1/2^3 = 1/8 = 12,5%. Con số 87,5% là phần đã phân rã, không phải phần còn lại.",
        },
        {
            "type": "multiple_choice",
            "question": "Một nguồn phóng xạ có độ phóng xạ 3,7.10^10 Bq. Con số đó bằng",
            "options": ["1 Ci.", "3,7.10^10 Ci.", "0,37 Ci.", "1 phân rã mỗi giây."],
            "answer": 0,
            "explanation": "Theo định nghĩa 1 Ci = 3,7.10^10 Bq, nên 3,7.10^10 Bq chính là 1 Ci. Curi là đơn vị lớn hơn becơren nên số đo bằng curi phải nhỏ hơn số đo bằng becơren.",
        },
        {
            "type": "multiple_choice",
            "question": "Vì sao carbon-14 (chu kì bán rã 5730 năm) chỉ định tuổi được tới khoảng vài chục nghìn năm?",
            "options": [
                "Vì sau khoảng 10 chu kì, lượng carbon-14 còn lại quá ít để đo.",
                "Vì carbon-14 có chu kì bán rã quá dài.",
                "Vì tia beta trừ của nó không thoát ra khỏi mẫu gỗ.",
                "Vì carbon trong mẫu bay hơi dần.",
            ],
            "answer": 0,
            "explanation": "Sau khoảng 10 chu kì bán rã (≈57 000 năm) chỉ còn dưới 0,1% lượng carbon-14 ban đầu; số đếm chìm vào phông nền nên không đo được nữa. Chu kì bán rã 5730 năm là ngắn, không phải dài.",
        },
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 12", "lesson_title": "Bài 17. Hiện tượng phóng xạ"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Phóng xạ, chu kì bán rã và độ phóng xạ",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}

with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("ok", len(bundle["theory_html"]), "bytes theory")
