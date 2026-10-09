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
for i, qz in enumerate(re.split(r'(?=<div class="tl-quiz">)', h)[1:], 1):
    seg = qz.split("</div>\n</div>")[0] if "</div>\n</div>" in qz else qz
    ok = seg.count('class="tl-opt tl-ok"'); no = seg.count('class="tl-opt tl-no"')
    if ok != 1: err.append(f"quiz #{i}: có {ok} đáp án tl-ok (cần đúng 1)")
    if no < 1: err.append(f"quiz #{i}: không có đáp án tl-no")
    ins = re.findall(r'<input type="radio" name="([^"]+)" id="([^"]+)">\s*<label for="([^"]+)"', seg)
    if any(a[1] != a[2] for a in ins): err.append(f"quiz #{i}: for/id không khớp")
    if len({a[0] for a in ins}) > 1: err.append(f"quiz #{i}: nhiều name trong một quiz")
    if "tl-fb--ok" not in seg or "tl-fb--no" not in seg: err.append(f"quiz #{i}: thiếu .tl-fb--ok/--no")
# Phản hồi quiz không được đẩy học sinh rời màn hình ("đọc mục II.2 rồi quay lại", "xem lại bước 3 của lời giải"):
# lúc đó học sinh đang nhìn đúng câu hỏi, nên chỉ trỏ tới thứ còn nằm trên màn hình (dòng 🔑 phía trên, đề, phương án).
_V = r"(?:[Đđ]ọc|[Xx]em|[Mm]ở|[Ll]àm|[Ôô]n|[Nn]hìn)(?: lại)?(?: tiếp)?"
_L = (r"(?:mục|bước|Hình \d|Bẫy \d|bảng|lời giải|bài toán mẫu|bài mẫu|phần thử sức|phần điền bước|phần luyện|"
      r"quy tắc|hệ thức|gạch đầu dòng|ba gạch|hàng đầu|đoạn cong|dòng \")")
RE_ROI_MAN_HINH = re.compile(r"quay lại|[Đđ]ọc tiếp tới|(?:hãy )?" + _V + r"\s+(?:tới\s+)?" + _L
                             + r"|\((?:xem|ở) [^)]*\)|— xem (?:mục|Bẫy|Hình|bước)")
for m in re.finditer(r'<div class="tl-fb tl-fb--(?:no|ok)">(.*?)</div>', h, re.S):
    for sen in re.split(r"(?<=[.!?])\s+", re.sub(r"<[^>]+>", "", m.group(1)).strip()):
        if RE_ROI_MAN_HINH.search(sen) and not re.search(r"ngay trên|phía trên|ngay dưới", sen):
            err.append(f"phản hồi quiz đẩy học sinh rời màn hình: «{sen[:80]}» — trỏ tới dòng 🔑 phía trên / đề / phương án thay vì mục khác")
if not re.search(r"Trả bài", h): warn.append('thiếu mục "Trả bài" trước bài tập')
if "tl-box--exp" not in h: warn.append("chưa có thí nghiệm/ví dụ (.tl-box--exp)")
if "tl-table--data" not in h: warn.append("chưa có bảng Câu trong đề / Dữ liệu / Kiến thức (.tl-table--data)")
fig = len(re.findall(r'<figure class="fig"', h))
print(f"{len(h)/1024:.1f} KB · {fig} hình · {len(re.findall('tl-quiz', h))} quiz · {len(re.findall('<details', h))} details")
for w in warn: print("⚠", w)
for e in err: print("✗", e)
sys.exit(1 if err else 0)
