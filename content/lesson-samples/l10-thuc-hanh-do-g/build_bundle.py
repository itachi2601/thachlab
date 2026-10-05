#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Thực hành: Đo gia tốc rơi tự do",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Thả bi từ s = 0,300 m; đồng hồ ghi t = 0,247 s. Gia tốc rơi tự do tính được là:",
         "options": ["2,43 m/s²", "4,92 m/s²", "0,0366 m/s²", "9,83 m/s²"],
         "answer": 3,
         "explanation": "g = 2s/t² = 2·0,300/0,247² ≈ 9,83 m/s². 2,43 là 2s/t (chia t thay vì t²); 4,92 là s/t² (quên nhân 2); 0,0366 là 2st² (nhân thay vì chia)."},
        {"type": MC,
         "question": "Trong phép đo có Δs/s = 0,2 % và 2Δt/t̄ ≈ 1,4 %, câu nào đúng?",
         "options": ["Sai số chủ yếu do thời gian; nên thả cao hơn và đo nhiều lần hơn",
                     "Sai số chủ yếu do độ cao; nên dùng thước chia tới 0,1 mm",
                     "Hai phần như nhau vì cùng có mặt trong công thức",
                     "Không còn sai số vì đã lấy trung bình 5 lần"],
         "answer": 0,
         "explanation": "Thời gian chiếm 1,4 % so với 0,2 % của độ cao, vì Δt có hệ số 2 và t̄ chỉ cỡ 0,3 s. Thả cao hơn làm t̄ lớn hơn nên Δt/t̄ nhỏ đi. Lấy trung bình chỉ giảm phần ngẫu nhiên, sai số dụng cụ vẫn còn."},
        {"type": MC,
         "question": "Bi thật sự rơi 0,500 m trong t = 0,319 s (đo đúng). Nhóm đo s từ mặt nam châm nên ghi 0,510 m. Gia tốc nhóm tính ra:",
         "options": ["Nhỏ hơn 9,83 m/s², vì s ghi dài hơn thì bi rơi chậm hơn",
                     "Vẫn bằng 9,83 m/s², vì g chỉ phụ thuộc thời gian",
                     "Lớn hơn: 2·0,510/0,319² ≈ 10,02 m/s², lệch khoảng +2 %",
                     "Lớn hơn, nhưng lấy trung bình nhiều lần sẽ bù lại"],
         "answer": 2,
         "explanation": "g = 2s/t² tỉ lệ với s: s lớn hơn 2 % thì g lớn hơn 2 % (10,02 so với 9,83). Lệch cùng một phía ở mọi lần nên lấy trung bình không bù được."},
        {"type": MC,
         "question": "Nam châm còn từ dư nên bi luôn rời muộn khoảng 0,002 s ở mọi lần thả. Nhóm đo 100 lần rồi lấy trung bình. Điều nào đúng?",
         "options": ["Dao động giữa các lần giảm, nhưng t̄ vẫn lớn hơn thật cỡ 0,002 s, nên g vẫn nhỏ hơn thật",
                     "Cả sai số ngẫu nhiên lẫn hệ thống đều giảm về 0",
                     "Độ trễ 0,002 s mất đi vì lần nhanh lần chậm bù nhau",
                     "g lớn hơn thật vì t đọc lớn hơn"],
         "answer": 0,
         "explanation": "Độ trễ cùng phía mọi lần là sai số hệ thống; trung bình chỉ trị sai số ngẫu nhiên. t đọc lớn hơn thật nên g = 2s/t² nhỏ hơn thật."},
        {"type": MC,
         "question": "Ba nhóm báo cáo (m/s²): nhóm 1: 9,68 ± 0,13; nhóm 2: 9,50 ± 0,05; nhóm 3: 10,20 ± 0,30. Kết quả của nhóm nào phù hợp với 9,8?",
         "options": ["Nhóm 2, vì sai số nhỏ nhất",
                     "Nhóm 1, vì khoảng từ 9,55 đến 9,81 chứa 9,8",
                     "Nhóm 3, vì khoảng ± 0,30 rộng nhất nên chắc chắn chứa 9,8",
                     "Không nhóm nào, vì không nhóm nào đo đúng 9,8"],
         "answer": 1,
         "explanation": "9,68 − 0,13 = 9,55 và 9,68 + 0,13 = 9,81: khoảng chứa 9,8. Nhóm 2 (9,45–9,55) chụm lại nhưng lệch, dấu hiệu sai số hệ thống; nhóm 3 (9,90–10,50) không chứa 9,8."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 11. Thực hành: Đo gia tốc rơi tự do"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Phương án đo g bằng cổng quang; xử lí số liệu, sai số tuyệt đối và tương đối; đồ thị s–t²; sai số ngẫu nhiên và hệ thống",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
