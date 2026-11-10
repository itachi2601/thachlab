#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Thực hành: Đo tốc độ của vật chuyển động",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Cổng quang E nối ổ A, cổng quang F nối ổ B của đồng hồ đo thời gian hiện số. Muốn đo thời gian viên bi đi từ E tới F, chọn MODE nào?",
         "options": ["MODE A", "MODE A ↔ B", "MODE A + B", "MODE T"],
         "answer": 1,
         "explanation": "MODE A ↔ B bắt đầu đếm khi bi chắn cổng nối ổ A và dừng khi bi chắn cổng nối ổ B. MODE A chỉ đếm lúc bi đang che tia của cổng E; A + B cộng hai khoảng che tia; T dùng cho vật dao động."},
        {"type": MC,
         "question": "Thả viên bi lăn trên máng nghiêng qua hai cổng quang E, F cách nhau $s$; đồng hồ ở MODE A ↔ B hiện thời gian $t$. Phát biểu nào sau đây sai?",
         "options": ["Ba số đo thời gian lệch nhau ít hơn nhiều so với bấm đồng hồ bằng tay",
                     "Nam châm điện giúp lần nào bi cũng lăn từ cùng một vị trí",
                     "Dời cổng F ra xa cổng E hơn thì số chỉ của đồng hồ lớn hơn",
                     "Kết quả $s/t$ là tốc độ của viên bi đúng lúc nó đi qua cổng F"],
         "answer": 3,
         "explanation": "$s/t$ là tốc độ trung bình trên cả đoạn EF. Bi lăn nhanh dần nên lúc qua F nó nhanh hơn con số này; muốn biết tốc độ tại F phải đo thời gian bi chắn cổng F rồi lấy $d/t$."},
        {"type": MC,
         "question": "Cần biết viên bi đang lăn nhanh bao nhiêu đúng lúc nó tới chân máng nghiêng. Cách làm nào đúng?",
         "options": ["Hai cổng ở đỉnh và chân máng, MODE A ↔ B, lấy chiều dài máng chia số chỉ",
                     "Một cổng ở chân máng, MODE của ổ nối cổng đó, lấy đường kính bi chia số chỉ",
                     "Một cổng ở chân máng, MODE của ổ nối cổng đó, lấy chiều dài máng chia số chỉ",
                     "Hai cổng ở đỉnh và chân máng, MODE A + B, lấy đường kính bi chia số chỉ"],
         "answer": 1,
         "explanation": "Tốc độ tại một điểm là tốc độ tức thời: đặt một cổng tại điểm đó, đo thời gian bi chắn tia, lấy $d/t$ với $d$ là đường kính bi. Hai cổng với MODE A ↔ B chỉ cho tốc độ trung bình trên cả máng."},
        {"type": MC,
         "question": "Cổng quang đặt hơi cao nên tia sáng chỉ cắt phần trên của viên bi. So với tốc độ thật của bi, kết quả $d/t$ sẽ",
         "options": ["lớn hơn, vì thời gian chắn tia ngắn hơn thời gian bi đi hết đường kính",
                     "nhỏ hơn, vì tia chỉ gặp một phần nhỏ của bi nên đồng hồ đếm chậm lại",
                     "không đổi, vì đường kính $d$ vẫn là con số đã đo bằng thước kẹp",
                     "lúc lớn hơn lúc nhỏ hơn, nên chỉ cần đo nhiều lần rồi lấy trung bình"],
         "answer": 0,
         "explanation": "Tia lệch tâm thì bi chỉ chắn tia trên một dây cung ngắn hơn $d$, nên $t$ nhỏ đi; chia $d$ cho $t$ nhỏ hơn ra tốc độ lớn hơn thật. Độ lệch luôn về một phía nên lấy trung bình không sửa được."},
        {"type": MC,
         "question": "Phép đo (I): $t = 0{,}800\\ \\text{s}$, sai số $0{,}004\\ \\text{s}$. Phép đo (II): $t = 0{,}020\\ \\text{s}$, sai số $0{,}001\\ \\text{s}$. Phép đo nào chính xác hơn?",
         "options": ["(II), vì sai số $0{,}001\\ \\text{s}$ nhỏ hơn sai số $0{,}004\\ \\text{s}$",
                     "Như nhau, vì hai phép đo dùng cùng một đồng hồ hiện số",
                     "(II), vì thời gian đo càng ngắn thì càng ít bị lệch",
                     "(I), vì sai số tỉ đối của (I) nhỏ hơn của (II)"],
         "answer": 3,
         "explanation": "(I): $0{,}004/0{,}800 = 0{,}5\\ \\%$. (II): $0{,}001/0{,}020 = 5\\ \\%$. Phải so sai số với chính giá trị đo; thời gian càng ngắn thì một độ chia của đồng hồ càng chiếm phần lớn."},
        {"type": MC,
         "question": "Một phép đo tốc độ có $\\bar v = 0{,}800\\ \\text{m/s}$, $\\delta s = 0{,}1\\ \\%$ và $\\delta t = 0{,}4\\ \\%$. Kết quả ghi vào báo cáo là",
         "options": ["$v = 0{,}800 \\pm 0{,}5\\ \\text{m/s}$", "$v = 0{,}800 \\pm 0{,}003\\ \\text{m/s}$",
                     "$v = 0{,}800 \\pm 0{,}004\\ \\text{m/s}$", "$v = 0{,}800 \\pm 0{,}0004\\ \\text{m/s}$"],
         "answer": 2,
         "explanation": "$\\delta v = \\delta s + \\delta t = 0{,}5\\ \\%$, nên $\\Delta v = 0{,}800 \\cdot 0{,}005 = 0{,}004\\ \\text{m/s}$. $0{,}5$ là quên nhân với $\\bar v$; $0{,}003$ là lấy hiệu hai sai số tỉ đối; $0{,}0004$ là đổi phần trăm thiếu mười lần."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 6. Thực hành: Đo tốc độ của vật chuyển động"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Đồng hồ đo thời gian hiện số và cổng quang điện; đo tốc độ trung bình (hai cổng, MODE A ↔ B) và tốc độ tức thời (một cổng, d/t) của viên bi trên máng nghiêng; xử lý số liệu, viết kết quả có sai số",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig', theory))} hình")
