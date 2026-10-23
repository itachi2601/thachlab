#!/usr/bin/env python3
"""Áp hệ khung có nghĩa (3 khung: 📌 phải nhớ, ⚠️ bẫy, ✍️ tự kiểm tra; còn lại ghi chú) lên theory.src.html của bài cũ.
Dùng: python3 scripts/ap-he-khung.py content/lesson-samples/<bài>/theory.src.html [--dry]
Chỉ thêm lớp / bọc khối Bẫy; không đổi chữ nội dung (trừ bỏ emoji đầu nhãn của hộp có khung). Chạy lại an toàn.
Khối công thức .tl-fx KHÔNG tự động: viết tay (cần bảng chú giải đại lượng)."""
import re, sys, pathlib

p = pathlib.Path(sys.argv[1]); dry = "--dry" in sys.argv
s = p.read_text(encoding="utf8"); orig = s
EMOJI = r"(?:✍️|🎤|🎯|✅|📌|⚠️)\s*"

def box(m):
    cls, rest = m.group(1), m.group(2)
    if re.search(r"\btl-(note|keep|check|trap)\b", cls): return m.group(0)
    lab = re.search(r'<p class="tl-label">(.*?)</p>', rest, re.S)
    t = lab.group(1) if lab else ""
    if "Mang về" in t:
        kind = "tl-keep"
    elif "tl-box--think" in cls and re.search(r"Tự kiểm tra|Trả bài|Điền bước|Thử sức|Thử thách|Biến thể|Luyện", t):
        kind = "tl-check"
    else:
        kind = "tl-note"
    if kind != "tl-note" and lab:
        rest = rest.replace(lab.group(0), '<p class="tl-label">' + re.sub("^" + EMOJI, "", t) + "</p>", 1)
    return f'<div class="{cls} {kind}"{rest}'

# hộp: <div class="tl-box ..."  (giữ nguyên thuộc tính còn lại)
s = re.sub(r'<div class="(tl-box(?: tl-box--\w+)?)"([^>]*>\s*(?:<p class="tl-label">.*?</p>)?)', box, s, flags=re.S)
s = re.sub(r'<details class="tl-details">', '<details class="tl-details tl-more">', s)

# bọc Bẫy: <h4>Bẫy …</h4> … tới trước h3/h4 kế, div.tl-box, details, hoặc hết
if "tl-trap" not in s:
    pat = re.compile(r'(<h4>Bẫy\b.*?</h4>)(.*?)(?=<h3|<h4|<div class="tl-box|<details|\Z)', re.S)
    s = pat.sub(lambda m: '<div class="tl-trap">\n' + m.group(1) + m.group(2).rstrip() + '\n</div>\n\n', s)

print(p, "đổi" if s != orig else "không đổi", {k: s.count(k) for k in ("tl-keep", "tl-check", "tl-note", "tl-trap", "tl-more", "tl-fx")})
if not dry and s != orig: p.write_text(s, encoding="utf8")
