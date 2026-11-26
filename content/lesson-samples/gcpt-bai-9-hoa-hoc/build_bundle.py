#!/usr/bin/env python3
"""Đóng gói bundle.json (thachlab.lesson-bundle/v1) cho GCPT – Bài 9.
Dùng: python3 build_figs.py && python3 build_bundle.py  rồi
      npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts bundle.json
Quiz tự kiểm trong bài → exam (≤4 câu); hai câu tự luận mẫu → worked_examples (tab Bài mẫu).
"""
import html
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
CLASS = "Các phương pháp gia công phi truyền thống"
LESSON = "Bài 9. Gia công hoá học và quang hoá (CHM, PCM)"
THEORY_SUB = "Nguyên lý mặt nạ + ăn mòn · quy trình PCM · ăn lẹm · số liệu, an toàn · chọn công nghệ"
EXAM_TITLE = "Kiểm tra nhanh — CHM và PCM"
theory = (HERE / "theory.html").read_text(encoding="utf8")


def strip(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s))).strip()


def parse_worked():
    out = []
    for m in re.finditer(r'<div class="tl-box tl-box--think tl-check">\s*<p class="tl-label">(Câu \d[^<]*)</p>(.*?)\n</div>', theory, re.S):
        label, body = m.group(1), m.group(2)
        body = body.replace('<details class="tl-details tl-more">', '<details class="tl-details" open>')
        out.append({"label": label.split("(")[0].strip() + " · " + ("giải thích" if "giải thích" in label else "chọn công nghệ"),
                    "body_html": body.strip()})
    return out


exam_qs = []
# lấy mọi .tl-quiz theo thứ tự xuất hiện
for m in re.finditer(r'<p>((?:(?!</p>).)*?)</p>\s*<div class="tl-quiz">(.*?)</div>\s*</div>\s*</div>', theory, re.S):
    question = strip(m.group(1))
    body = m.group(2)
    opts, ans = [], None
    for i, o in enumerate(re.finditer(r'<label [^>]*class="tl-opt (tl-ok|tl-no)">(.*?)</label>', body, re.S)):
        opts.append(re.sub(r"^[A-D]\.\s*", "", strip(o.group(2))))
        if o.group(1) == "tl-ok":
            ans = i
    fb = re.search(r'tl-fb--ok"><p>(.*?)</p>', body, re.S)
    exam_qs.append({"type": "multiple_choice", "question": question, "options": opts, "answer": ans,
                    "explanation": strip(fb.group(1)) if fb else ""})

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": CLASS, "lesson_title": LESSON},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": THEORY_SUB,
    "theory_html": theory,
    "worked_examples": parse_worked(),
    "exam": {"title": EXAM_TITLE, "duration_minutes": 8, "questions": exam_qs},
    "raster_images": [],
}
out = HERE / "bundle.json"
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("đã ghi", out, len(theory), "ký tự,", len(exam_qs), "câu quiz,", len(bundle["worked_examples"]), "bài mẫu")
