#!/usr/bin/env python3
"""Đóng gói bundle.json (schema thachlab.lesson-bundle/v1) từ theory.html + các câu tự kiểm tra trong bài.
Dùng: python3 build_bundle.py   rồi   npx tsx .claude/skills/.../validate_bundle.mts bundle.json
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")

MC = "multiple_choice"
exam = {
    "title": "Kiểm tra nhanh — Điện thế",
    "duration_minutes": 8,
    "questions": [
        {"type": MC,
         "question": "Đặt q₁ = 2 µC tại M thì thế năng là 40 µJ. Bỏ q₁, đặt q₂ = −3 µC vào đúng M. Điện thế tại M và thế năng của q₂ là:",
         "options": ["20 V; −60 µJ", "−20 V; −60 µJ", "20 V; 60 µJ", "−13,3 V; 40 µJ"],
         "answer": 0,
         "explanation": "V_M = W/q₁ = 40/2 = 20 V, là của điểm M nên không đổi khi thay điện tích. W = q₂V_M = (−3)(20) = −60 µJ."},
        {"type": MC,
         "question": "Một electron đi từ M (V_M = 10 V) đến N (V_N = 60 V). Công của lực điện là (e = 1,6·10⁻¹⁹ C):",
         "options": ["−8,0·10⁻¹⁸ J", "+1,12·10⁻¹⁷ J", "−1,12·10⁻¹⁷ J", "+8,0·10⁻¹⁸ J"],
         "answer": 3,
         "explanation": "U_MN = 10 − 60 = −50 V; A = qU_MN = (−1,6·10⁻¹⁹)(−50) = +8,0·10⁻¹⁸ J = 50 eV. Electron tự chạy về chỗ điện thế cao nên lực điện sinh công dương."},
        {"type": MC,
         "question": "Điện trường đều E = 1000 V/m. Đoạn MN = 5 cm hợp với đường sức góc 60°, N lệch về phía chiều đường sức so với M. U_MN bằng:",
         "options": ["50 V", "43,3 V", "25 V", "0 V"],
         "answer": 2,
         "explanation": "d là hình chiếu của MN lên đường sức: d = 5·cos60° = 2,5 cm. U_MN = Ed = 1000·0,025 = 25 V."},
        {"type": MC,
         "question": "Hai bản phẳng song song cách nhau 2 cm, nối nguồn 120 V, mốc điện thế ở bản âm; M cách bản âm 0,5 cm (V_M = 30 V). Electron đi từ M tới bản dương. Công của lực điện:",
         "options": ["−1,44·10⁻¹⁷ J", "+1,44·10⁻¹⁷ J", "+4,8·10⁻¹⁸ J", "+1,92·10⁻¹⁷ J"],
         "answer": 1,
         "explanation": "U = V_M − V_+ = 30 − 120 = −90 V; A = (−1,6·10⁻¹⁹)(−90) = +1,44·10⁻¹⁷ J = 90 eV."},
        {"type": MC,
         "question": "Cùng hai bản trên (cách 2 cm, 120 V) nhưng chọn mốc điện thế ở bản dương. Điện thế tại M (cách bản âm 0,5 cm) và hiệu điện thế giữa bản dương và bản âm là:",
         "options": ["−90 V; 120 V", "30 V; 120 V", "90 V; −120 V", "−90 V; 0 V"],
         "answer": 0,
         "explanation": "E = 6000 V/m; M cách bản dương 1,5 cm nên thấp hơn bản dương 90 V: V_M = −90 V. Hiệu điện thế không phụ thuộc mốc: vẫn 120 V."},
    ],
}

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 11", "chapter_title": "Chương 3: Điện trường", "lesson_title": "Bài 20. Điện thế"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Công của lực điện và thế năng điện; điện thế, hiệu điện thế và liên hệ U = Ed",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
