#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/.../validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Mô tả sóng",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Một chiếc lá nhỏ rơi xuống mặt hồ yên. Sóng từ một chiếc thuyền máy lan tới chỗ chiếc lá. Chiếc lá sẽ:",
         "options": ["Trôi ra xa theo chiều sóng truyền",
                     "Nhấp nhô tại chỗ, gần như không dịch chuyển theo sóng",
                     "Đứng yên tuyệt đối vì lá rất nhẹ",
                     "Bị sóng kéo chìm xuống đáy hồ"],
         "answer": 1,
         "explanation": "Sóng truyền pha và năng lượng, không truyền vật chất. Chiếc lá dao động tại chỗ quanh vị trí cân bằng của nó."},
        {"type": MC,
         "question": "Một sóng cơ có chu kì T = 0,4 s lan truyền với tốc độ v = 2,5 m/s. Bước sóng là:",
         "options": ["0,16 m", "1 m", "6,25 m", "0,4 m"],
         "answer": 1,
         "explanation": "λ = vT = 2,5 × 0,4 = 1 m. Chú ý không dùng v/T."},
        {"type": MC,
         "question": "Một sóng cơ truyền với tốc độ v = 40 cm/s và tần số f = 20 Hz. Điểm M cách nguồn O đoạn 5 cm. Dao động của M so với O là:",
         "options": ["Cùng pha", "Ngược pha", "Vuông pha", "Không xác định được vì thiếu biên độ"],
         "answer": 1,
         "explanation": "λ = v/f = 2 cm; d/λ = 2,5 = 2 + 1/2 nên M ngược pha với O. Độ lệch pha không phụ thuộc biên độ."},
        {"type": MC,
         "question": "Sóng có A = 2 cm, f = 50 Hz, tốc độ truyền sóng v = 2 m/s. Phát biểu nào đúng?",
         "options": ["Tốc độ dao động cực đại bằng tốc độ truyền sóng vì cùng ký hiệu v",
                     "Tốc độ dao động cực đại là ωA = 2π.50.0,02 ≈ 6,28 m/s, là đại lượng khác với v = 2 m/s",
                     "Tốc độ dao động cực đại luôn nhỏ hơn tốc độ truyền sóng",
                     "Hai đại lượng này chỉ khác nhau về đơn vị đo"],
         "answer": 1,
         "explanation": "v do môi trường quyết định, v_max = ωA do nguồn quyết định (A và f); không có quy luật cái nào lớn hơn."},
        {"type": MC,
         "question": "Một sóng truyền trên dây từ trái sang phải. Tại một thời điểm, dây có dạng hình sin và điểm P nằm ở sườn bên phải của một đỉnh sóng (phía trước theo chiều truyền). Ngay sau đó P sẽ:",
         "options": ["Đi lên", "Đi xuống", "Đứng yên vì đang ở sườn dốc", "Chạy sang phải cùng với đỉnh sóng"],
         "answer": 0,
         "explanation": "Sóng truyền sang phải thì đỉnh sóng dịch sang phải, điểm nằm trước đỉnh bị nâng lên: sườn trước đi lên, sườn sau đi xuống."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 11", "lesson_title": "Mô tả sóng"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Bước sóng · chu kì · tần số · tốc độ truyền sóng · phương trình sóng và đồ thị sóng",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
