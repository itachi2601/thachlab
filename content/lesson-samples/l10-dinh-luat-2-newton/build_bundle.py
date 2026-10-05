#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Định luật 2 Newton",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Một xe 0,50 kg được kéo bằng lực 0,20 N (bỏ qua ma sát). Nếu lực kéo tăng lên 0,60 N thì gia tốc của xe:",
         "options": ["Không đổi, vì vẫn là chiếc xe cũ", "Giảm còn một phần ba",
                     "Tăng thêm 0,40 m/s², thành 0,80 m/s²", "Tăng gấp ba, thành 1,2 m/s²"],
         "answer": 3,
         "explanation": "Khối lượng không đổi thì a tỉ lệ thuận với F: lực gấp ba, gia tốc gấp ba, a = 0,60/0,50 = 1,2 m/s². Chọn 0,80 m/s² là gán độ tăng của lực cho gia tốc mà quên chia cho m."},
        {"type": MC,
         "question": "Cùng một lực đẩy, xe chở hàng có tổng khối lượng gấp 3 xe rỗng. Gia tốc của xe chở hàng bằng:",
         "options": ["Một phần ba gia tốc xe rỗng", "Gấp ba gia tốc xe rỗng",
                     "Bằng gia tốc xe rỗng, vì cùng lực", "Một phần chín gia tốc xe rỗng"],
         "answer": 0,
         "explanation": "a = F/m: m gấp 3 thì a còn 1/3. Gia tốc tỉ lệ nghịch bậc một với khối lượng, không phải bình phương."},
        {"type": MC,
         "question": "Kéo một thùng 20 kg trên sàn bằng lực nằm ngang 100 N, lực ma sát là 60 N. Gia tốc của thùng là:",
         "options": ["5 m/s²", "8 m/s²", "2 m/s²", "3 m/s²"],
         "answer": 2,
         "explanation": "F trong định luật 2 Newton là hợp lực: 100 − 60 = 40 N, a = 40/20 = 2 m/s². Ra 5 m/s² là quên ma sát."},
        {"type": MC,
         "question": "Xe đang chạy về hướng bắc thì tài xế đạp phanh. Trong lúc phanh, gia tốc của xe hướng về:",
         "options": ["Hướng bắc, cùng chiều chuyển động", "Không có hướng, vì gia tốc bằng không khi xe còn chạy",
                     "Hướng xuống mặt đường", "Hướng nam, ngược chiều vận tốc"],
         "answer": 3,
         "explanation": "Gia tốc cùng hướng hợp lực. Lực hãm hướng nam nên gia tốc hướng nam; vận tốc vẫn hướng bắc nhưng giảm dần."},
        {"type": MC,
         "question": "Xe đồ chơi khối lượng 200 g chịu hợp lực 0,5 N. Gia tốc của xe là:",
         "options": ["0,0025 m/s²", "2,5 m/s²", "0,4 m/s²", "100 m/s²"],
         "answer": 1,
         "explanation": "Đổi 200 g = 0,2 kg; a = 0,5/0,2 = 2,5 m/s². Ra 0,0025 là để nguyên đơn vị gam."},
        {"type": MC,
         "question": "Ô tô 1000 kg đang chạy 20 m/s thì phanh, dừng lại sau 40 m. Lực hãm (coi không đổi) là:",
         "options": ["5000 N, ngược chiều chuyển động", "10 000 N, ngược chiều chuyển động",
                     "500 N, ngược chiều chuyển động", "5000 N, cùng chiều chuyển động"],
         "answer": 0,
         "explanation": "v² − v0² = 2as nên a = (0 − 400)/(2·40) = −5 m/s²; F = m·|a| = 5000 N, hướng ngược chuyển động. Ra 10 000 N là quên số 2 trong 2as."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 10", "lesson_title": "Bài 15. Định luật 2 Newton"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Gia tốc tỉ lệ thuận với hợp lực, tỉ lệ nghịch với khối lượng; khối lượng là mức quán tính; bài toán động lực học",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
