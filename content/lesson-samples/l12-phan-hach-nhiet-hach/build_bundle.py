"""Đóng gói theory.html + 7 câu luyện tập thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_bundle.py
"""
import json

EXAM = {
    "title": "Luyện tập — Phản ứng phân hạch, phản ứng nhiệt hạch và ứng dụng",
    "duration_minutes": 10,
    "questions": [
        {
            "type": "multiple_choice",
            "question": "Trong phản ứng phân hạch $^{235}_{92}\\text{U} + {}^{1}_{0}\\text{n} \\to {}^{144}_{56}\\text{Ba} + {}^{89}_{36}\\text{Kr} + x\\,{}^{1}_{0}\\text{n}$, giá trị của $x$ là",
            "options": ["x = 1.", "x = 2.", "x = 3.", "x = 4."],
            "answer": 2,
            "explanation": "Bảo toàn số nuclôn: 235 + 1 = 144 + 89 + x, suy ra x = 3. Kiểm tra điện tích: 92 + 0 = 56 + 36 + 0, khớp.",
        },
        {
            "type": "multiple_choice",
            "question": "Phân hạch U-235 toả năng lượng vì",
            "options": [
                "nơtron bị hấp thụ và toàn bộ khối lượng của nó biến thành nhiệt.",
                "tổng khối lượng nghỉ của các mảnh vỡ nhỏ hơn khối lượng nghỉ ban đầu.",
                "hai hạt nhân urani kết hợp thành một hạt nhân nặng hơn.",
                "êlectron trong nguyên tử urani chuyển mức và phát ra ánh sáng.",
            ],
            "answer": 1,
            "explanation": "Năng lượng lấy từ phần khối lượng nghỉ hụt đi của cả phản ứng: W = (m_trước − m_sau)c². Hai mảnh vỡ bền hơn hạt nhân urani nên năng lượng liên kết riêng tăng và tổng khối lượng nghỉ giảm. Chuyển mức êlectron chỉ cho năng lượng cỡ vài êlectron vôn.",
        },
        {
            "type": "multiple_choice",
            "question": "Một lò phản ứng đang có hệ số nhân nơtron k = 1,002. Phản ứng dây chuyền trong lò sẽ",
            "options": [
                "tắt dần, vì k còn nhỏ hơn 2.",
                "số nơtron tăng dần theo từng thế hệ, vì k > 1.",
                "đứng yên không đổi, vì k xấp xỉ 1.",
                "dừng ngay, vì k khác đúng 1.",
            ],
            "answer": 1,
            "explanation": "k = 1,002 > 1 nên mỗi thế hệ có nhiều nơtron hơn thế hệ trước một chút — số nơtron tăng dần. Mốc so sánh của k là 1, không phải 2; muốn công suất không đổi phải giữ đúng k = 1 bằng thanh điều khiển.",
        },
        {
            "type": "multiple_choice",
            "question": "Điều kiện để phản ứng nhiệt hạch xảy ra là",
            "options": [
                "nhiệt độ cỡ 10⁸–10⁹ K, mật độ hạt nhân đủ lớn và duy trì đủ lâu.",
                "có nơtron chậm bắn vào hạt nhân nhẹ.",
                "nhiệt độ phòng và áp suất thấp để hạt nhân dễ tiến lại gần nhau.",
                "chỉ cần đặt hai hạt nhân nhẹ sát nhau là đủ.",
            ],
            "answer": 0,
            "explanation": "Ba điều kiện phải đủ cùng lúc: nhiệt độ rất cao để thắng lực đẩy Cu-lông, mật độ lớn để va chạm đủ nhiều, thời gian giam đủ dài để năng lượng thu về lớn hơn năng lượng bỏ ra. Nơtron chậm là cách mồi phân hạch, không phải nhiệt hạch.",
        },
        {
            "type": "multiple_choice",
            "question": "U-235 phân hạch toả trung bình 200 MeV. Số phân hạch cần thiết để toả ra năng lượng 1 J là",
            "options": ["3,1·10¹⁰.", "3,1·10¹³.", "1,25·10¹⁰.", "5,0·10¹²."],
            "answer": 0,
            "explanation": "1 MeV = 1,6·10⁻¹³ J nên 200 MeV = 3,2·10⁻¹¹ J. Số phân hạch cần: 1 ÷ 3,2·10⁻¹¹ ≈ 3,1·10¹⁰ hạt.",
        },
        {
            "type": "true_false",
            "question": "Xét phản ứng nhiệt hạch ${}^{2}_{1}\\text{H} + {}^{3}_{1}\\text{H} \\to {}^{4}_{2}\\text{He} + {}^{1}_{0}\\text{n}$, toả năng lượng khoảng $17{,}6\\ \\text{MeV}$. Một phân hạch U-235 toả trung bình $200\\ \\text{MeV}$.",
            "statements": [
                {"text": "Tổng khối lượng nghỉ của các hạt sau phản ứng nhỏ hơn tổng khối lượng nghỉ của các hạt trước phản ứng.", "answer": True},
                {"text": "Giống phân hạch U-235, phản ứng này được mồi bằng cách bắn neutron chậm vào hạt nhân ${}^{2}_{1}\\text{H}$.", "answer": False},
                {"text": "Năng lượng toả ra của một phản ứng này lớn hơn năng lượng toả ra của một phân hạch U-235.", "answer": False},
                {"text": "Lõi Mặt trời chỉ cỡ $1{,}5\\cdot10^{7}\\ \\text{K}$ nhưng nhiệt hạch vẫn xảy ra nhờ mật độ rất lớn và lực hấp dẫn giam khối khí rất lâu.", "answer": True},
            ],
            "explanation": "a) Đúng: phản ứng toả năng lượng nên khối lượng nghỉ giảm, $W = (m_{\\text{trước}} - m_{\\text{sau}})c^2 \\gt 0$.<br>b) Sai: neutron chậm là cách mồi phân hạch; nhiệt hạch cần nhiệt độ $10^8$–$10^9$ K, mật độ lớn, đủ lâu để thắng lực đẩy Cu-lông.<br>c) Sai: $17{,}6\\ \\text{MeV} \\lt 200\\ \\text{MeV}$.<br>d) Đúng: thiếu nhiệt độ thì mật độ lõi cực lớn và thời gian giam hàng tỉ năm bù lại.",
        },
        {
            "type": "short_answer",
            "question": "Cho khối lượng hạt nhân: $m_{\\text{D}} = 2{,}0136\\ \\text{u}$, $m_{\\text{T}} = 3{,}0155\\ \\text{u}$, $m_{\\text{He}} = 4{,}0015\\ \\text{u}$, $m_{\\text{n}} = 1{,}0087\\ \\text{u}$; $1\\ \\text{u}\\cdot c^2 = 931{,}5\\ \\text{MeV}$. Năng lượng toả ra của phản ứng ${}^{2}_{1}\\text{H} + {}^{3}_{1}\\text{H} \\to {}^{4}_{2}\\text{He} + {}^{1}_{0}\\text{n}$ bằng bao nhiêu MeV (làm tròn đến hàng phần mười)?",
            "answer": "17,6",
            "explanation": "$\\Delta m = (2{,}0136 + 3{,}0155) - (4{,}0015 + 1{,}0087) = 5{,}0291 - 5{,}0102 = 0{,}0189\\ \\text{u}$.<br>$W = 0{,}0189 \\cdot 931{,}5 \\approx 17{,}6\\ \\text{MeV}$.",
        },
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {
        "class_name": "Vật lí 12",
        "lesson_title": "Bài 16. Phản ứng phân hạch, phản ứng nhiệt hạch và ứng dụng",
    },
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Phân hạch, dây chuyền, lò phản ứng và nhiệt hạch",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}

with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("ok", len(bundle["theory_html"]), "bytes theory")
