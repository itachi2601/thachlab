#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""soat_nhan.py — soát nhãn phân loại trong một ĐỀ VĂN BẢN kiểu Azota (de.txt) trước
khi dán vào /quan-tri/dang-de.

    python3 soat_nhan.py de.txt --grade 12

Mỗi câu ("Câu n.") phải có đủ hai dòng:
    Chủ đề: <tên yêu cầu cần đạt, đúng như danh mục question_topics của khối>
    Dạng: lý thuyết | bài tập
Script tải danh mục khối (REST anon-key, đọc .env.local của repo — dùng lại
`fetch_topics` của build_bundle.py) rồi báo: câu thiếu nhãn, tên chủ đề không có trong
danh mục (kèm tên gần nhất), chủ đề còn ở mức cả bài. Có ✗ thì sửa de.txt rồi chạy lại.
Cờ --fix: tự chuẩn hoá hoa/thường + khoảng trắng của tên theo danh mục, ghi đè de.txt.
"""
import argparse
import difflib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_bundle import fetch_topics, topic_key, clean_topic  # noqa: E402

RE_CAU = re.compile(r"^\s*(?:\*\s*)?Câu\s*(\d+)\s*[.:)]", re.I)
RE_TOPIC = re.compile(r"^\s*(Chủ\s*đề|YCCĐ|Yêu\s*cầu\s*cần\s*đạt|Năng\s*lực)\s*[:：]\s*(.*?)\s*$", re.I)
RE_FORM = re.compile(r"^\s*(Dạng|Loại)\s*[:：]\s*(.*?)\s*$", re.I)
FORMS = {"lý thuyết", "lí thuyết", "lt", "bài tập", "bt"}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("text")
    ap.add_argument("--grade", required=True)
    ap.add_argument("--fix", action="store_true")
    a = ap.parse_args()

    lines = open(a.text, encoding="utf-8").read().split("\n")
    rows, err = fetch_topics(a.grade)
    if err:
        sys.exit("không tải được danh mục: " + err)
    canon = {topic_key(r["name"]): clean_topic(r["name"]) for r in rows}
    coarse = {topic_key(r["name"]) for r in rows if r.get("parent_id") is None}

    q, topics, forms = 0, {}, {}
    errors, warns = [], []
    for i, line in enumerate(lines):
        if RE_CAU.match(line):
            q += 1
            continue
        if q == 0:
            continue
        m = RE_TOPIC.match(line)
        if m:
            name = clean_topic(m.group(2))
            topics[q] = name
            k = topic_key(name)
            if k in canon:
                if a.fix and name != canon[k]:
                    lines[i] = "Chủ đề: " + canon[k]
                if k in coarse:
                    warns.append('câu %d: "%s" là tên BÀI — nên chọn yêu cầu cần đạt trong bài' % (q, name))
            else:
                near = difflib.get_close_matches(k, list(canon), n=2, cutoff=0.5)
                errors.append('câu %d: "%s" không có trong danh mục khối %s%s' % (
                    q, name, a.grade, " — gần nhất: " + " | ".join(canon[n] for n in near) if near else ""))
            continue
        m = RE_FORM.match(line)
        if m:
            v = m.group(2).strip().lower()
            forms[q] = v
            if v not in FORMS:
                errors.append('câu %d: "Dạng: %s" — chỉ nhận lý thuyết | bài tập' % (q, m.group(2)))

    thieu_t = [n for n in range(1, q + 1) if not topics.get(n)]
    thieu_f = [n for n in range(1, q + 1) if not forms.get(n)]
    if thieu_t:
        errors.append("thiếu dòng Chủ đề: câu " + ", ".join(map(str, thieu_t)))
    if thieu_f:
        errors.append("thiếu dòng Dạng: câu " + ", ".join(map(str, thieu_f)))

    for w in warns:
        print("⚠ " + w)
    for e in errors:
        print("✗ " + e)
    if a.fix:
        open(a.text, "w", encoding="utf-8").write("\n".join(lines))
    print("Nhãn: %d/%d câu đủ · %d chủ đề%s" % (
        q - len(set(thieu_t) | set(thieu_f)), q, len(set(topics.values())),
        " · %d cảnh báo" % len(warns) if warns else ""))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
