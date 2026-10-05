#!/usr/bin/env python3
"""Đóng gói bundle.json từ theory.html + exam.json. Chạy sau build_figs.py."""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
theory = (HERE / "theory.html").read_text(encoding="utf8")
exam = json.loads((HERE / "exam.json").read_text(encoding="utf8"))

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 11",
               "lesson_title": "Bài 26. Thực hành: Đo suất điện động và điện trở trong của pin điện hoá"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Thiết kế phương án đo ℰ và r của pin bằng biến trở, vôn kế, ampe kế; xử lý số liệu bằng đồ thị U–I",
    "theory_html": theory,
    "worked_examples": [],
    "exam": exam,
    "raster_images": [],
}

out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"bundle.json: {out.stat().st_size/1024:.1f} KB · {len(exam['questions'])} câu · "
      f"{len(re.findall(r'<figure class=.fig.', theory))} hình")
