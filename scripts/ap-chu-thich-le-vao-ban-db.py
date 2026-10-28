#!/usr/bin/env python3
"""Áp content/lesson-samples/_margin_fig.margin_figs lên bản lý thuyết ĐANG CÓ trong DB (đã xuất bằng xuat-ly-thuyet-db.mts).
Dùng: python3 scripts/ap-chu-thich-le-vao-ban-db.py <vào.html> <ra.html>   (in số hình còn sót nguồn trong figcaption)"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "content/lesson-samples"))
from _margin_fig import margin_figs

src, dst = map(pathlib.Path, sys.argv[1:3])
h = src.read_text(encoding="utf8")
n = margin_figs(h)
dst.write_text(n, encoding="utf8")
left = len(re.findall(r"<figcaption>(?:(?!</figcaption>).)*OpenStax", n, re.S))
print(f"{src.name}: {'đổi' if n != h else 'không đổi'}, còn sót {left}")
