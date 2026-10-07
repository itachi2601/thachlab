#!/usr/bin/env python3
"""Xem thử một bài tập mẫu bằng Chrome headless: dựng trang với CSS thật (globals.css) + KaTeX, mở sẵn mọi nút
(Phân tích đề / Lời giải), bấm "Chạy mô phỏng" rồi chụp ở khung CUỐI (virtual time 15 s).
Dùng:  python3 .claude/skills/soan-bai-tap-mau/scripts/xem-thu.py scripts/data/bai-tap-mau/<id>.json <thư-mục-ra> [--rong 500] [--dang 1,3]
Sinh: <ra>/dang-<n>.png (cả dạng: đề + mô phỏng ở khung cuối + phân tích + lời giải). Chrome macOS ép cửa sổ ≥ 500px nên mặc định 500."""
import json, os, subprocess, sys
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
src, out = sys.argv[1], sys.argv[2]
width = int(sys.argv[sys.argv.index("--rong") + 1]) if "--rong" in sys.argv else 500
only = set(map(int, sys.argv[sys.argv.index("--dang") + 1].split(","))) if "--dang" in sys.argv else None
os.makedirs(out, exist_ok=True)
d = json.load(open(src))
g = open(os.path.join(root, "app/globals.css"), encoding="utf8").read()
css = g[g.index("/* Hình vẽ SVG nội tuyến"):g.index("/* ---------- Nội dung bài viết blog")] + g[g.index("/* Bài lý thuyết tương tác"):]
katex = os.path.join(root, "node_modules/katex/dist")
chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
for i, q in enumerate(d["dang_bai"] + ([d["tu_luan"]] if d.get("tu_luan") else []), 1):
    if only and i not in only: continue
    body = f'<h3>{q["label"]}</h3>' + (q.get("problem_html") or q.get("body_html", "")) + (f'<h4>Phân tích đề</h4>{q["analysis_html"]}' if q.get("analysis_html") else "") + (f'<h4>Lời giải</h4>{q["solution_html"]}' if q.get("solution_html") else "")
    html = (f'<!doctype html><meta charset=utf8><link rel=stylesheet href="file://{katex}/katex.min.css"><style>body{{background:#0f172a;color:#e2e8f0;font:16px/1.7 sans-serif;max-width:720px;margin:auto;padding:12px}}{css}</style>'
            f'<span class="exam-content">{body}</span><script src="file://{katex}/katex.min.js"></script><script src="file://{katex}/contrib/auto-render.min.js"></script>'
            '<script>renderMathInElement(document.body,{delimiters:[{left:"$$",right:"$$",display:true},{left:"$",right:"$",display:false}]});'
            'document.querySelectorAll("button[data-bt-run]").forEach(b=>b.closest("figure").querySelectorAll("animate,animateTransform").forEach(a=>a.beginElement()))</script>')
    p = os.path.join(out, f"dang-{i}.html"); open(p, "w", encoding="utf8").write(html)
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={width},3600", "--virtual-time-budget=15000",
                    f"--screenshot={os.path.join(out, f'dang-{i}.png')}", f"file://{p}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
    print("dang", i, "→", os.path.join(out, f"dang-{i}.png"))
