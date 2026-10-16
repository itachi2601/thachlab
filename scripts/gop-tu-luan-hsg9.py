#!/usr/bin/env python3
"""Gộp khối bài tập tự luận (từ skill soan-bai-tap-tu-luan-hsg, file web-tu-luan.json: {lesson_id: html}) vào
mục `tu_luan.body_html` của scripts/data/bai-tap-mau/<lesson_id>.json. Idempotent: khối nằm giữa hai marker
<!-- <tag>:start --> … <!-- <tag>:end -->, chạy lại thì thay, không nhân đôi. Sau đó đăng bằng publish-bai-tap-mau.mts.
Dùng: python3 scripts/gop-tu-luan-hsg9.py <web-tu-luan.json> <tag> [--dry-run]
"""
import json, re, sys, pathlib
src, tag = sys.argv[1], sys.argv[2]; dry = "--dry-run" in sys.argv
web = json.load(open(src))
for lid, html in web.items():
    p = pathlib.Path(f"scripts/data/bai-tap-mau/{lid}.json"); d = json.load(open(p))
    tl = d.setdefault("tu_luan", {"label": "Bài tập tự luận (xếp từ dễ đến khó)", "body_html": ""})
    block = f"<!-- {tag}:start --><h3>Bài tập Vận dụng – Vận dụng cao (bộ Cơ học)</h3>{html}<!-- {tag}:end -->"
    pat = re.compile(rf"<!-- {re.escape(tag)}:start -->.*?<!-- {re.escape(tag)}:end -->", re.S)
    before = len(tl["body_html"])
    tl["body_html"] = pat.sub(lambda m: block, tl["body_html"]) if pat.search(tl["body_html"]) else tl["body_html"] + block
    print(f"{lid} {d.get('lesson_title','')[:40]}: tu_luan {before} → {len(tl['body_html'])} ký tự ({'thay' if before and pat.search(block) and before != len(tl['body_html']) else 'nối'})")
    if not dry: json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)
print("dry-run, chưa ghi" if dry else "đã ghi JSON")
