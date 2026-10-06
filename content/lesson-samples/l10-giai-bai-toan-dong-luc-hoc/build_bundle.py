#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Cách giải bài toán động lực học",
    "duration_minutes": 10,
    "questions": [
        {"type": MC,
         "question": "Kéo thùng sách 20 kg bằng lực 100 N, dây xiên lên 30° so với sàn, hệ số ma sát trượt 0,2, g = 10 m/s². Lực ma sát trượt là:",
         "options": ["40 N", "30 N", "50 N", "17,3 N"],
         "answer": 1,
         "explanation": "N = mg − F·sin30° = 200 − 50 = 150 N; F_ms = 0,2·150 = 30 N. 40 N là coi N = mg; 50 N là cộng F·sinα; 17,3 N là lấy F·cosα làm áp lực."},
        {"type": MC,
         "question": "Hộp trượt xuống dốc nghiêng 30°, hệ số ma sát trượt 0,2, g = 10 m/s². Gia tốc của hộp xấp xỉ:",
         "options": ["5,0 m/s²", "3,0 m/s²", "6,7 m/s²", "3,3 m/s²"],
         "answer": 3,
         "explanation": "a = g(sinα − μcosα) = 10(0,5 − 0,2·0,866) ≈ 3,3 m/s². 5,0 là quên ma sát; 3,0 là tính ma sát bằng μmg; 6,7 là cộng ma sát thay vì trừ."},
        {"type": MC,
         "question": "Khối m1 trên bàn nối dây qua ròng rọc ở mép bàn với vật treo m2. Chọn chiều dương đi theo dây (m1 sang phải, m2 xuống). Phương trình định luật II đúng cho vật treo m2 là:",
         "options": ["P2 − T = m2·a", "T − P2 = m2·a", "P2 = m2·a", "P2 − T = (m1 + m2)·a"],
         "answer": 0,
         "explanation": "Với m2, chiều dương hướng xuống: P2 cùng chiều dương, lực căng T ngược chiều. Lấy chiều dương của m2 hướng lên mà vẫn dùng chung a với m1 là sai dấu; muốn dùng trục riêng thì phải đổi dấu a."},
        {"type": MC,
         "question": "Đẩy hộp trượt lên một con dốc rồi buông tay. Lúc hộp còn đang trượt lên, các lực tác dụng lên hộp là:",
         "options": ["Trọng lực, phản lực, lực đẩy của tay và ma sát", "Trọng lực, phản lực, \"lực đà\" lên dốc và ma sát",
                     "Trọng lực, phản lực và ma sát hướng xuống dốc", "Trọng lực, phản lực và ma sát hướng lên dốc"],
         "answer": 2,
         "explanation": "Tay đã rời hộp nên hết lực đẩy; \"lực đà\" là quán tính, không do vật nào gây ra. Hộp đi lên nên ma sát trượt hướng xuống dốc."},
        {"type": MC,
         "question": "Hộp trượt xuống một tấm ván. Nâng ván từ 20° lên 40° (hộp vẫn trượt). Áp lực N và ma sát trượt thay đổi thế nào?",
         "options": ["Không đổi, vì N = mg", "Cả hai cùng giảm", "N giảm, ma sát tăng", "Cả hai cùng tăng"],
         "answer": 1,
         "explanation": "N = mg·cosα giảm khi α tăng; ma sát trượt μN giảm theo. N = mg chỉ đúng trên mặt ngang không có lực xiên."},
        {"type": MC,
         "question": "Viên đá trượt lên một con dốc phủ băng nghiêng góc α (bỏ ma sát), dừng lại rồi trượt xuống. Chọn chiều dương hướng lên dốc. Gia tốc của viên đá:",
         "options": ["Lúc lên −g·sinα, lúc xuống +g·sinα", "Lúc lên +g·sinα, lúc xuống −g·sinα",
                     "Bằng 0 ở điểm cao nhất, lúc khác −g·sinα", "Luôn bằng −g·sinα"],
         "answer": 3,
         "explanation": "Lực dọc dốc duy nhất là P·sinα, luôn hướng xuống; chiều dương giữ nguyên nên a = −g·sinα suốt, kể cả ở điểm cao nhất (v = 0 nhưng lực vẫn còn)."},
        {"type": MC,
         "question": "Đẩy ngang một tủ quần áo 50 kg bằng lực 120 N, tủ không nhúc nhích. Hệ số ma sát nghỉ 0,4, g = 10 m/s². Lực ma sát của sàn lên tủ là:",
         "options": ["120 N", "200 N", "0 N", "80 N"],
         "answer": 0,
         "explanation": "Tủ đứng yên nên a = 0: F − F_ms = 0, F_ms = 120 N (ma sát nghỉ). μN = 200 N chỉ là mức lớn nhất ma sát nghỉ đạt được."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10",
               "lesson_title": "Bài 20. Một số ví dụ về cách giải các bài toán thuộc phần động lực học"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Quy trình 4 bước Vẽ · Kể lực · Viết ΣF = ma · Chiếu và giải, áp cho mặt ngang có ma sát, mặt phẳng nghiêng, hai vật nối dây",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

# kiểm: đáp án trong exam khớp đáp án tl-ok trong bài (quiz 2..8)
oks = re.findall(r'id="tl65-q(\d)([a-d])"><label[^>]*class="tl-opt tl-ok"', theory)
ok_map = {int(q): "abcd".index(c) for q, c in oks}
for i, q in enumerate(exam["questions"], start=2):
    assert ok_map[i] == q["answer"], (i, ok_map[i], q["answer"])
letters = [ok_map[k] for k in sorted(ok_map)]
assert all(letters.count(k) == 2 for k in range(4)), letters   # rải đều A–D

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình · đáp án đúng {''.join('ABCD'[k] for k in letters)}")
