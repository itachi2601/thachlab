"""Đóng gói theory.html + 5 câu tự kiểm tra thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_bundle.py
"""
import json

EXAM = {
    "title": "Luyện tập — Một số ứng dụng của cảm ứng điện từ",
    "duration_minutes": 10,
    "questions": [
        {
            "type": "multiple_choice",
            "question": "Thay dây thép của đàn guitar điện bằng dây nylon, gảy cùng cách. Tín hiệu đưa vào loa sẽ",
            "options": [
                "gần như mất, vì dây nylon không bị nam châm từ hoá nên từ thông qua cuộn gần như không đổi.",
                "to hơn, vì dây nylon nhẹ nên rung mạnh hơn.",
                "như cũ, vì nam châm trong cuộn vẫn còn.",
                "đổi thành dòng một chiều ổn định.",
            ],
            "answer": 0,
            "explanation": "Pickup chỉ cho tín hiệu khi từ thông qua cuộn biến thiên. Dây thép bị từ hoá và rung nên làm từ thông đổi; dây nylon không nhiễm từ nên từ thông gần như đứng yên. Nam châm nằm yên trong cuộn tự nó không tạo dòng.",
        },
        {
            "type": "multiple_choice",
            "question": "Thả cùng một nam châm vào ống nhựa và ống đồng dựng thẳng. Nam châm rơi chậm hơn trong ống đồng vì",
            "options": [
                "dòng Foucault trong thành đồng sinh lực từ hãm nam châm.",
                "đồng hút nam châm nên nam châm bị dính vào thành ống.",
                "ống đồng nặng hơn nên kéo nam châm lại.",
                "đồng cản không khí nhiều hơn nhựa.",
            ],
            "answer": 0,
            "explanation": "Nam châm chuyển động làm từ thông qua thành đồng biến thiên, sinh dòng Foucault; theo định luật Lenz, lực từ của dòng đó chống lại chuyển động. Đồng không nhiễm từ nên không hút nam châm; nhựa không dẫn điện nên không có dòng đó.",
        },
        {
            "type": "multiple_choice",
            "question": "Đặt điện thoại lên một nam châm vĩnh cửu rất mạnh, không có đế sạc. Pin có được nạp không?",
            "options": [
                "Có, nam châm càng mạnh pin càng mau đầy.",
                "Không, vì từ thông của nam châm đứng yên không đổi nên suất điện động bằng không.",
                "Có, nếu úp đúng mặt có cuộn dây.",
                "Có, nhưng chậm hơn khi dùng đế sạc.",
            ],
            "answer": 1,
            "explanation": "Suất điện động cảm ứng e = −ΔΦ/Δt. Nam châm vĩnh cửu nằm yên cho ΔΦ = 0 nên e = 0. Lực hút và suất điện động là hai việc khác nhau; đế sạc phải phát từ trường biến thiên (dòng xoay chiều).",
        },
        {
            "type": "multiple_choice",
            "question": "Nồi nào sôi được trên bếp từ thông thường?",
            "options": [
                "Nồi nhôm trơn, đáy dày.",
                "Nồi thuỷ tinh.",
                "Nồi gang, nam châm dính được vào đáy.",
                "Nồi đồng.",
            ],
            "answer": 2,
            "explanation": "Đáy gang nhiễm từ gom được từ thông nên sinh dòng Foucault lớn, nóng nhanh ngay trong đáy nồi. Nhôm và đồng không gom từ thông nên suất điện động cảm ứng nhỏ, bếp thường ngắt; thuỷ tinh không dẫn điện nên không có dòng Foucault.",
        },
        {
            "type": "multiple_choice",
            "question": "Coi dòng Foucault trong đáy nồi như một vòng dây có điện trở 0,50 Ω, từ thông Φ = 2·10⁻⁴ cos(1,6·10⁵ t) Wb. Công suất toả nhiệt trung bình trên vòng là",
            "options": ["2048 W.", "0 W.", "32 W.", "1024 W."],
            "answer": 3,
            "explanation": "e = −Φ′ có biên độ e₀ = Φ₀ω = 2·10⁻⁴ · 1,6·10⁵ = 32 V. Hiệu dụng E = e₀/√2 = 16√2 V, nên P = E²/r = 512/0,50 = 1024 W. Ra 2048 W là dùng biên độ thay cho hiệu dụng; ra 0 W là lấy trung bình của suất điện động có dấu; 32 là số vôn của e₀.",
        },
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 12", "lesson_title": "Bài 15. Một số ứng dụng của cảm ứng điện từ"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Guitar điện, sạc không dây và dòng điện Foucault",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}

with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("ok", len(bundle["theory_html"]), "bytes theory")
