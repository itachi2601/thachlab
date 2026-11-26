"""Đóng gói theory.html + 7 câu luyện tập thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_bundle.py
"""
import json

EXAM = {
    "title": "Luyện tập — Một số ứng dụng của cảm ứng điện từ",
    "duration_minutes": 10,
    "questions": [
        {
            "type": "multiple_choice",
            "question": "Trong bếp từ, bộ phận nào nóng lên trước tiên?",
            "options": [
                "Mặt kính của bếp, rồi dẫn nhiệt sang đáy nồi.",
                "Đáy nồi, vì dòng điện cảm ứng toả nhiệt ngay trong kim loại.",
                "Đáy nồi, vì bị nam châm hút mạnh rồi cọ xát với mặt kính.",
                "Cuộn dây dưới bếp, rồi chiếu tia hồng ngoại vào nồi.",
            ],
            "answer": 1,
            "explanation": "Bếp từ không có mâm nóng để truyền nhiệt. Cuộn dây dưới mặt kính tạo từ trường biến thiên; từ trường xuyên qua mặt kính cách điện vào đáy nồi gang và sinh dòng điện cảm ứng (dòng Foucault) ngay trong đáy nồi. Chính dòng đó toả nhiệt Joule làm nồi nóng lên, còn mặt kính chỉ ấm lên nhờ nồi truyền lại.",
        },
        {
            "type": "multiple_choice",
            "question": "Một đế sạc không dây có cuộn sơ cấp 200 vòng nối với nguồn xoay chiều 12 V, cuộn thứ cấp 150 vòng. Coi hai cuộn ghép lí tưởng, điện áp trên cuộn thứ cấp là",
            "options": ["9,0 V.", "16 V.", "12 V.", "3 V."],
            "answer": 0,
            "explanation": "Máy biến áp lí tưởng: U2/U1 = N2/N1, suy ra U2 = 12 × 150/200 = 9,0 V. Các phương án sai ứng với ba lỗi hay gặp: đảo tỉ số vòng (16 V), tưởng máy biến áp không đổi điện áp (12 V), và lấy hiệu số vòng (3 V). Thực tế sạc không dây không có lõi sắt chung nên điện áp đo được còn thấp hơn giá trị lí tưởng này.",
        },
        {
            "type": "multiple_choice",
            "question": "Tấm nhôm liền khối dao động giữa hai cực nam châm thì tắt rất nhanh; thay bằng tấm nhôm có rãnh xẻ thì dao động lâu hơn. Vì sao?",
            "options": [
                "Tấm có rãnh xẻ nhẹ hơn nên ít bị lực hãm hơn.",
                "Rãnh cắt các đường dòng Foucault, điện trở mạch dòng tăng nên dòng cảm ứng nhỏ, lực hãm yếu.",
                "Rãnh làm tấm nhôm không còn nằm trong từ trường nữa.",
                "Rãnh làm tấm dẫn điện tốt hơn nên dòng lớn hơn và lực hãm mạnh hơn.",
            ],
            "answer": 1,
            "explanation": "Lực hãm điện từ sinh ra do dòng Foucault khép kín trong tấm, không do khối lượng. Rãnh xẻ cắt các đường dòng khép kín, làm điện trở của mạch dòng tăng; cùng một suất điện động cảm ứng nhưng dòng nhỏ hơn nên lực hãm yếu đi rõ rệt và dao động tắt chậm hơn.",
        },
        {
            "type": "multiple_choice",
            "question": "Trường hợp nào sau đây xuất hiện dòng điện Foucault trong một tấm kim loại?",
            "options": [
                "Tấm nhôm đặt yên trên bàn, sát một nam châm vĩnh cửu đứng yên.",
                "Tấm nhôm rơi qua vùng từ trường mạnh giữa hai cực nam châm.",
                "Tấm nhôm đặt trong lò nướng đang nóng.",
                "Tấm nhôm được nối hai đầu với một viên pin.",
            ],
            "answer": 1,
            "explanation": "Điều kiện là từ thông qua khối phải biến thiên. Tấm nhôm rơi qua từ trường thì từ thông qua nó biến thiên liên tục nên sinh dòng Foucault và lực hãm hướng lên. Từ thông không đổi (A) thì không có dòng cảm ứng; nóng lên trong lò (C) là do truyền nhiệt; nối với pin (D) là dòng do nguồn đẩy qua, không phải dòng cảm ứng.",
        },
        {
            "type": "multiple_choice",
            "question": "Một máy biến áp trong bộ sạc có cuộn sơ cấp 600 vòng nối với điện áp xoay chiều 220 V, cuộn thứ cấp 150 vòng. Coi gần đúng lí tưởng, điện áp ra của cuộn thứ cấp là",
            "options": ["55 V.", "880 V.", "165 V.", "220 V."],
            "answer": 0,
            "explanation": "U2 = U1·N2/N1 = 220 × 150/600 = 220 × 0,25 = 55 V. Cuộn thứ cấp ít vòng hơn nên điện áp ra nhỏ hơn điện áp vào (máy hạ áp). Các phương án sai là ba lỗi hay gặp: đảo tỉ số vòng (880 V), lấy hiệu số vòng (165 V), và tưởng máy biến áp giữ nguyên điện áp (220 V).",
        },
        {
            "type": "true_false",
            "question": "Đế sạc không dây có cuộn sơ cấp 200 vòng nối với nguồn xoay chiều 12 V; cuộn thứ cấp 150 vòng nằm sau lưng điện thoại. Hai cuộn không có lõi sắt chung.",
            "statements": [
                {"text": "Nếu nối cuộn sơ cấp với nguồn điện một chiều 12 V ổn định thì cuộn thứ cấp vẫn có suất điện động cảm ứng.", "answer": False},
                {"text": "Coi hai cuộn ghép lí tưởng thì điện áp hiệu dụng ở cuộn thứ cấp bằng 9,0 V.", "answer": True},
                {"text": "Đặt điện thoại xa đế sạc hơn thì điện áp ở cuộn thứ cấp tăng vì từ thông rò giảm.", "answer": False},
                {"text": "Pin cần nhận 5 400 J với công suất nạp 9 W thì thời gian nạp là 10 phút.", "answer": True},
            ],
            "explanation": "a) Sai: dòng một chiều ổn định thì từ thông qua cuộn thứ cấp không đổi, không có suất điện động cảm ứng.<br>b) Đúng: $U_2 = U_1\\dfrac{N_2}{N_1} = 12 \\cdot \\dfrac{150}{200} = 9{,}0$ V.<br>c) Sai: càng xa thì từ thông rò càng nhiều, điện áp thứ cấp càng giảm.<br>d) Đúng: $t = \\dfrac{A}{P} = \\dfrac{5\\,400}{9} = 600$ s $= 10$ phút.",
        },
        {
            "type": "short_answer",
            "question": "Một bếp từ có công suất 2 000 W đun 1,5 kg nước từ 25 °C lên 75 °C trong 3 phút. Nhiệt dung riêng của nước 4 180 J/(kg·K). Hiệu suất của bếp bằng bao nhiêu phần trăm (làm tròn đến hàng đơn vị)?",
            "answer": "87",
            "explanation": "$H = \\dfrac{mc\\Delta t}{P\\tau} = \\dfrac{1{,}5 \\cdot 4\\,180 \\cdot 50}{2\\,000 \\cdot 180} = \\dfrac{313\\,500}{360\\,000} \\approx 0{,}871$, tức khoảng 87%.",
        },
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 12", "lesson_title": "Bài 15. Một số ứng dụng của cảm ứng điện từ"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Từ trường biến thiên làm nóng nồi, sạc pin và hãm xe",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}

with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("ok", len(bundle["theory_html"]), "bytes theory")
