#!/usr/bin/env python3
"""Tìm clip YouTube ứng viên cho bài lý thuyết: mỗi từ khoá in 5 kết quả đầu
(id | tiêu đề | kênh), id nào oEmbed báo lỗi thì ghi "không nhúng được".
Chỉ đọc, không ghi gì. Chưa xem nội dung clip → thầy vẫn phải soát V1–V7.

  python3 scripts/tim-clip-youtube.py "slinky longitudinal wave" "speed of sound resonance tube"
"""
import re, sys, json, urllib.request, urllib.parse

UA = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en"}
for q in sys.argv[1:]:
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(q)
    html = urllib.request.urlopen(urllib.request.Request(url, headers=UA)).read().decode()
    ids = []
    for m in re.finditer(r'"videoId":"([\w-]{11})"', html):
        if m.group(1) not in ids:
            ids.append(m.group(1))
    print("##", q)
    for i in ids[:5]:
        try:
            o = json.load(urllib.request.urlopen(
                "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=%s&format=json" % i))
            print(i, "|", o["title"], "|", o["author_name"])
        except Exception:
            print(i, "| (không nhúng được / oEmbed lỗi)")
