"""Đóng gói theory.html + 5 câu tự kiểm tra thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_bundle.py
"""
import json

EXAM = {
    "title": "Luyện tập — Năng lượng liên kết hạt nhân",
    "duration_minutes": 10,
    "questions": [
        {
            "type": "multiple_choice",
            "question": "Điều nào sau đây đúng khi nói về lực hạt nhân?",
            "options": [
                "Là lực hút tĩnh điện giữa prôtôn và êlectron trong nguyên tử.",
                "Là lực đẩy giữa các nuclôn, chống lại lực hút tĩnh điện.",
                "Là lực hút giữa các nuclôn, tác dụng trong phạm vi cỡ 10⁻¹⁵ m.",
                "Chỉ tác dụng giữa hai prôtôn, không tác dụng với nơtrôn.",
            ],
            "answer": 2,
            "explanation": "Lực hạt nhân là lực hút giữa các nuclôn, không phụ thuộc điện tích (cặp p–p, p–n, n–n đều hút nhau như nhau) và có bán kính tác dụng rất ngắn, cỡ 10⁻¹⁵ m — đúng bằng kích thước hạt nhân. Lực này không phải lực tĩnh điện và không phải lực hấp dẫn, nhưng mạnh hơn hẳn lực đẩy tĩnh điện giữa các prôtôn nên hạt nhân vẫn đứng vững.",
        },
        {
            "type": "multiple_choice",
            "question": "Khối lượng của một hạt nhân giảm đi $0{,}030377\\ \\text{u}$ khi nó được tạo thành từ các nuclôn rời. Năng lượng giải phóng tương ứng là",
            "options": [
                "$28{,}3\\ \\text{MeV}$.",
                "$0{,}030377\\ \\text{MeV}$ vì khối lượng tính theo u thì năng lượng tính theo MeV.",
                "$3 \\cdot 10^8\\ \\text{MeV}$ vì phải nhân với tốc độ ánh sáng.",
                "$9 \\cdot 10^{16}\\ \\text{MeV}$ vì phải nhân với $c^2$.",
            ],
            "answer": 0,
            "explanation": "E = Δm·c², và với Δm tính theo u thì hệ số đổi 931,5 MeV/u đã bao sẵn c²: E = 0,030377 × 931,5 = 28,3 MeV. Không nhân thêm c hay c² lần nữa, và đơn vị u không phải MeV.",
        },
        {
            "type": "multiple_choice",
            "question": "Một hạt nhân có năng lượng liên kết $492\\ \\text{MeV}$ và số khối $A = 56$. Năng lượng liên kết riêng của nó là",
            "options": [
                "$492\\ \\text{MeV}$ cho mỗi nuclôn.",
                "$2{,}76 \\cdot 10^4\\ \\text{MeV}$ cho mỗi nuclôn.",
                "$18{,}9\\ \\text{MeV}$ cho mỗi nuclôn.",
                "$8{,}79\\ \\text{MeV}$ cho mỗi nuclôn.",
            ],
            "answer": 3,
            "explanation": "Năng lượng liên kết riêng là năng lượng tính cho MỘT nuclôn: E_lkr = E_lk/A = 492/56 = 8,79 MeV. Phương án A là chưa chia; B là làm phép nhân 492 × 56; C là chia cho 26 prôtôn thay vì chia cho cả 56 nuclôn.",
        },
        {
            "type": "multiple_choice",
            "question": "Urani-235 có năng lượng liên kết $1783{,}9\\ \\text{MeV}$, sắt-56 có $492{,}3\\ \\text{MeV}$. So sánh nào sau đây đúng?",
            "options": [
                "Urani bền hơn vì năng lượng liên kết lớn hơn gần 4 lần.",
                "Sắt bền hơn vì năng lượng liên kết riêng lớn hơn.",
                "Sắt bền hơn vì khối lượng hạt nhân nhỏ hơn nên dễ giữ hơn.",
                "Không so sánh được vì hai hạt nhân khác số khối.",
            ],
            "answer": 1,
            "explanation": "Phải chia năng lượng liên kết cho số nuclôn rồi mới so độ bền: urani 1783,9/235 = 7,59 MeV, sắt 492,3/56 = 8,79 MeV mỗi nuclôn. Năng lượng liên kết thô lớn hơn không có nghĩa là bền hơn, vì nó tăng theo số nuclôn. Đây cũng là lí do urani có thể phân hạch toả năng lượng.",
        },
        {
            "type": "multiple_choice",
            "question": "Phản ứng $^{2}_{1}\\text{H} + {}^{3}_{1}\\text{H} \\to {}^{4}_{2}\\text{He} + {}^{1}_{0}\\text{n}$ có khối lượng giảm đi $0{,}018883\\ \\text{u}$ (tổng khối lượng sau nhỏ hơn tổng khối lượng trước). Năng lượng toả ra khi một phản ứng xảy ra là",
            "options": [
                "$17{,}6\\ \\text{MeV}$ cho mỗi nuclôn tham gia.",
                "$3{,}52\\ \\text{MeV}$ cho một phản ứng.",
                "$17{,}6\\ \\text{MeV}$ cho một phản ứng.",
                "$0{,}018883\\ \\text{MeV}$ cho một phản ứng.",
            ],
            "answer": 2,
            "explanation": "E = Δm·c² = 0,018883 × 931,5 = 17,6 MeV cho một phản ứng. Có 5 nuclôn tham gia nên nếu tính cho mỗi nuclôn thì được khoảng 3,5 MeV, nhưng đề hỏi cho một phản ứng. Phương án D bỏ luôn hệ số 931,5 nên ra đúng con số khối lượng.",
        },
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 12", "lesson_title": "Bài 15. Năng lượng liên kết hạt nhân"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Độ hụt khối, năng lượng liên kết và độ bền vững hạt nhân",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}

with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("ok", len(bundle["theory_html"]), "bytes theory")
