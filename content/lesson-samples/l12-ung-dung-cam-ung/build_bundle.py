"""Đóng gói theory.html + câu tự kiểm tra thành bundle.json.
Chạy từ thư mục này:  python3 build_bundle.py"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent

EXAM = {
    "title": "Luyện tập — Một số ứng dụng của cảm ứng điện từ",
    "duration_minutes": 12,
    "questions": [
        {"type": "multiple_choice",
         "question": "Thay dây thép của đàn guitar điện bằng dây nylon rồi gảy cùng cách. Tín hiệu đưa vào loa thế nào?",
         "options": [
             "Gần như mất, vì dây nylon không bị từ hoá.",
             "To hơn, vì dây nylon nhẹ, rung mạnh hơn.",
             "Như cũ, vì nam châm trong cuộn vẫn còn.",
             "Đảo chiều, vì nylon cách điện."],
         "answer": 0,
         "explanation": "Pickup chỉ có dòng khi từ thông qua cuộn đổi. Dây nylon không nhiễm từ nên từ thông gần như đứng yên."},
        {"type": "multiple_choice",
         "question": "Đặt điện thoại lên một nam châm vĩnh cửu, không có đế sạc. Pin có được nạp không?",
         "options": [
             "Có, nam châm càng mạnh pin càng mau đầy.",
             "Không, vì từ thông của nam châm đứng yên không đổi.",
             "Có, nếu úp đúng mặt có cuộn dây.",
             "Có, vì nam châm hút mặt lưng máy."],
         "answer": 1,
         "explanation": "Suất điện động cảm ứng chỉ có khi từ thông biến thiên. Nam châm đứng yên cho e = 0. Đế sạc phải phát từ trường xoay chiều."},
        {"type": "multiple_choice",
         "question": "Nam châm rơi chậm trong ống đồng, nhanh trong ống nhựa cùng chiều dài. Giải thích đúng là",
         "options": [
             "Đồng hút nam châm nên nam châm bị dính.",
             "Ống đồng nặng hơn nên nam châm rơi chậm.",
             "Dòng Foucault trong thành đồng sinh lực hãm.",
             "Ống nhựa sinh ma sát lớn nên đáng lẽ phải chậm hơn đồng."],
         "answer": 2,
         "explanation": "Đồng không nhiễm từ: nam châm vẫn rơi hết ống. Dòng Foucault trong thành đồng bị từ trường tác dụng lực ngược chiều rơi."},
        {"type": "multiple_choice",
         "question": "Xe đã dừng. Phanh Foucault dùng nam châm một chiều kẹp đĩa kim loại còn hãm xe không?",
         "options": [
             "Còn, vì nam châm vẫn bật.",
             "Không, vì đĩa đứng yên nên từ thông không đổi.",
             "Đảo chiều và đẩy xe chạy tiếp.",
             "Còn, và mạnh hơn lúc xe đang chạy."],
         "answer": 1,
         "explanation": "Hết chuyển động thì hết dòng Foucault, hết lực hãm. Giữ xe lúc đỗ là việc của phanh ma sát."},
        {"type": "multiple_choice",
         "question": "Một vòng Foucault có r = 0,50 Ω, từ thông Φ = 2·10⁻⁴ cos(1,6·10⁵ t) Wb. Công suất toả nhiệt trung bình trên vòng là",
         "options": ["2048 W.", "1024 W.", "0 W.", "32 W."],
         "answer": 1,
         "explanation": "e0 = Φ0·ω = 32 V, E = e0/√2 = 16√2 V, P = E²/r = 512/0,50 = 1024 W. 2048 W là dùng nhầm e0 thay cho E."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 12", "lesson_title": "Bài 15. Một số ứng dụng của cảm ứng điện từ"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Guitar, sạc không dây, dòng Foucault và các ứng dụng",
    "theory_html": (HERE / "theory.html").read_text(encoding="utf-8"),
    "worked_examples": [],
    "exam": EXAM,
    "raster_images": [],
}
(HERE / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", len(bundle["theory_html"]))
