"""Nhét theory.html vào bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_bundle.py
"""
import json

b = json.load(open("bundle.json", encoding="utf8"))
b["theory_html"] = open("theory.html", encoding="utf8").read()
json.dump(b, open("bundle.json", "w", encoding="utf8"), ensure_ascii=False, indent=2)
print("ok", len(b["theory_html"]), "bytes theory")
