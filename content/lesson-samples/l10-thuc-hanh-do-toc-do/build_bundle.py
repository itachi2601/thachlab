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
         "question": "Vì sao đồng hồ hiện số nối cổng quang cho thời gian ít sai số hơn bấm tay?",
         "options": ["Thời điểm bắt đầu và kết thúc do tia sáng bị chắn quyết định, không có độ trễ của người bấm",
                     "Vì xe chạy chậm hơn khi qua cổng quang",
                     "Vì d/t luôn đúng bằng tốc độ tức thời tại cổng",
                     "Vì đồng hồ hiện số hoàn toàn không có sai số"],
         "answer": 0,
         "explanation": "Tia sáng bị chắn thì đồng hồ chạy, hết chắn thì dừng, không cần tay người. d/t vẫn là tốc độ trung bình trên bề rộng tấm chắn, và đồng hồ chỉ chia tới 0,001 s nên vẫn có sai số."},
        {"type": MC,
         "question": "Nhóm em bấm tay, mỗi lần bấm lệch cỡ 0,1 s. Cách nào giảm sai số tương đối hợp lí nhất?",
         "options": ["Dùng đồng hồ bấm giây đắt hơn, vẫn bấm tay",
                     "Chỉ bấm một lần, nhưng bấm thật dứt khoát",
                     "Rút ngắn đường chạy để dễ nhìn xe hơn",
                     "Kéo dài đường chạy (cùng tốc độ), đo nhiều lần rồi lấy trung bình"],
         "answer": 3,
         "explanation": "Đường dài gấp đôi thì t dài gấp đôi, độ lệch bấm vẫn cỡ 0,1 s nên δt giảm một nửa; đo nhiều lần cho thêm trung bình và ước lượng sai số. Đồng hồ đắt không sửa được phản xạ; một lần bấm không ước được sai số; đường ngắn làm δt tăng."},
        {"type": MC,
         "question": "Xe đang chạy nhanh dần qua cổng quang. Muốn d/t sát tốc độ tức thời tại cổng hơn, nên làm gì?",
         "options": ["Dùng tấm chắn rộng hơn để t dài, đo cho chính xác",
                     "Không cần làm gì, d/t luôn là tốc độ tức thời",
                     "Dùng tấm chắn hẹp hơn, miễn t còn dài hơn nhiều bước chia của đồng hồ",
                     "Đo thêm một lần với cùng tấm chắn rồi lấy trung bình"],
         "answer": 2,
         "explanation": "d/t là tốc độ trung bình trên bề rộng tấm chắn; tấm chắn hẹp thì khoảng thời gian ngắn, tốc độ đổi ít. Hẹp quá thì đồng hồ làm tròn mạnh. Lấy trung bình nhiều lần không sửa được độ lệch do d rộng."},
        {"type": MC,
         "question": "Phép đo (I): 100 m, sai số 0,5 m. Phép đo (II): 0,50 m, sai số 0,5 cm. Phép đo nào chính xác hơn?",
         "options": ["(II), vì 0,5 cm nhỏ hơn 0,5 m",
                     "(I), vì sai số tương đối của (I) nhỏ hơn của (II)",
                     "Như nhau, vì cùng ghi \"0,5\"",
                     "Không so sánh được vì hai đơn vị khác nhau"],
         "answer": 1,
         "explanation": "(I): 0,5/100 = 0,5 %. (II): 0,5/50 = 1 % (đổi 0,50 m = 50 cm). Sai số tương đối không có đơn vị nên so sánh được; phải so với giá trị đo."},
        {"type": MC,
         "question": "Tấm chắn rộng 3,0 cm che cổng quang trong 0,060 s. Tốc độ của xe là:",
         "options": ["50 m/s", "2,0 m/s", "0,0018 m/s", "0,50 m/s"],
         "answer": 3,
         "explanation": "v = 0,030 m / 0,060 s = 0,50 m/s (đổi 3,0 cm = 0,030 m). 50 là quên đổi cm ra m; 2,0 là chia ngược t : d (d đã đổi ra m); 0,0018 là nhân d·t thay vì chia."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 6. Thực hành: Đo tốc độ của vật chuyển động"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Đo tốc độ bằng thước và đồng hồ, cổng quang, video; sai số tuyệt đối và tương đối; chọn tấm chắn; so sánh ưu, nhược các phương án",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig', theory))} hình")
