#!/usr/bin/env python3
"""Kiểm cấu trúc theory.html của bài lý thuyết tương tác. Dùng: lint_theory.py <theory.html>"""
import re, sys
h = open(sys.argv[1], encoding="utf8").read()
err, warn = [], []
if re.search(r"<script\b|<style\b", h, re.I): err.append("có <script>/<style> (bị validate chặn)")
if re.search(r"\son\w+\s*=", h, re.I): err.append("có thuộc tính on*=")
if re.search(r"\\\[|\\\]|\\textbf\{|\\includegraphics", h): err.append("còn sót LaTeX thô")
if h.count("$") % 2: err.append("số dấu $ lẻ")
if re.search(r"<p\b[^>]*>\s*[-•●▪]\s", h): err.append('<p> mở bằng "-"/"•" (bị đổi thành bullet)')
if re.search(r"\.{4,}", h): warn.append('có chuỗi "...." (bị xoá khi hiển thị)')
for t in ("details", "div", "figure", "table", "svg", "ul", "p"):
    o = len(re.findall(rf"<{t}\b", h)); c = len(re.findall(rf"</{t}>", h))
    if o != c: err.append(f"<{t}> mở {o} ≠ đóng {c}")
if not re.search(r"<h3\b", h): err.append("không có <h3> mốc I., II.… (Ôn ngay không cuộn được)")
ids = re.findall(r'\bid="([^"]+)"', h)
dup = {i for i in ids if ids.count(i) > 1}
if dup: err.append(f"id trùng: {sorted(dup)}")
if "<img" in h: warn.append("có <img> — ảnh phải .webp ≤150 KB, qua Storage")
for i, qz in enumerate(re.split(r'(?=<div class="tl-quiz")', h)[1:], 1):
    seg = qz.split("</div>\n</div>")[0] if "</div>\n</div>" in qz else qz
    # Chỉ <label> mới là phương án; link phụ (vd. nút "Mở bộ Flashcard" dùng lại class tl-opt tl-ok)
    # không được tính là đáp án thứ hai — báo giả này từng chặn đăng 7 chương AVCN (20/10/2026).
    ok = len(re.findall(r'<label[^>]*class="tl-opt tl-ok"', seg))
    no = len(re.findall(r'<label[^>]*class="tl-opt tl-no"', seg))
    if ok != 1: err.append(f"quiz #{i}: có {ok} đáp án tl-ok (cần đúng 1)")
    if no < 1: err.append(f"quiz #{i}: không có đáp án tl-no")
    ins = re.findall(r'<input type="radio" name="([^"]+)" id="([^"]+)">\s*<label for="([^"]+)"', seg)
    if any(a[1] != a[2] for a in ins): err.append(f"quiz #{i}: for/id không khớp")
    if len({a[0] for a in ins}) > 1: err.append(f"quiz #{i}: nhiều name trong một quiz")
    if "tl-fb--ok" not in seg or "tl-fb--no" not in seg: err.append(f"quiz #{i}: thiếu .tl-fb--ok/--no")
if not re.search(r"Trả bài", h): warn.append('thiếu mục "Trả bài" trước bài tập')
if "tl-box--exp" not in h: warn.append("chưa có thí nghiệm/ví dụ (.tl-box--exp)")
# Mỗi ý một dòng (thầy chốt 7/10/2026): không ghép nhiều ý bằng " · " trong <li>/<p> (trừ <svg>, bảng)
_txt = re.sub(r"<svg.*?</svg>|<table.*?</table>", "", h, flags=re.S)
for m in re.finditer(r"<(?:li|p)[^>]*>([^<]*(?:<(?!/?(?:li|p)\b)[^>]*>[^<]*)*?)</(?:li|p)>", _txt, flags=re.S):
    if m.group(1).count(" · ") >= 1 and "🔑" in m.group(1) or m.group(1).count(" · ") >= 2:
        warn.append("ghép nhiều ý bằng \" · \" (mỗi ý một dòng): " + re.sub(r"<[^>]+>|\s+", " ", m.group(1)).strip()[:70])
# 🔑 chỉ một ý, ngắn
for m in re.finditer(r"🔑([^<]*(?:<(?!/p)[^>]*>[^<]*)*)</p>", h):
    if len(re.sub(r"<[^>]+>|\$[^$]*\$", "", m.group(1)).split()) > 14:
        warn.append("dòng 🔑 quá dài (>14 chữ): " + re.sub(r"<[^>]+>", "", m.group(1)).strip()[:60])
if "tl-table--data" not in h: warn.append("chưa có bảng Câu trong đề / Dữ liệu / Kiến thức (.tl-table--data)")
fig = len(re.findall(r'<figure class="fig"', h))
print(f"{len(h)/1024:.1f} KB · {fig} hình · {len(re.findall('tl-quiz', h))} quiz · {len(re.findall('<details', h))} details")
for w in warn: print("⚠", w)
for e in err: print("✗", e)
sys.exit(1 if err else 0)
