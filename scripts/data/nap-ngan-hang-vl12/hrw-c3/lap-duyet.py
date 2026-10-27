# Dựng bản duyệt HTML (không cần DB) từ cau-final.json + gan-nhan.json → docs/ra-soat/cau-hoi-hrw-c3.html
# Chạy: python3 scripts/data/nap-ngan-hang-vl12/hrw-c3/lap-duyet.py
import json, os, html
D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(D, "..", "..", "..", ".."))
Q = json.load(open(os.path.join(D, "cau-final.json")))
N = json.load(open(os.path.join(D, "gan-nhan.json")))
LESSON = {10: "Bài 9. Khái niệm từ trường", 11: "Bài 10. Lực từ. Cảm ứng từ", 12: "Bài 11. Thực hành đo độ lớn cảm ứng từ",
          13: "Bài 12. Hiện tượng cảm ứng điện từ", 14: "Bài 13. Đại cương về dòng điện xoay chiều",
          125: "Bài 14. Máy phát điện xoay chiều. Máy biến áp", 126: "Bài 15. Một số ứng dụng của cảm ứng điện từ",
          127: "Bài 16. Điện từ trường. Mô hình sóng điện từ"}
TYPE = {"multiple_choice": "Trắc nghiệm", "true_false": "Đúng – sai", "short_answer": "Trả lời ngắn"}
DIFF = {"de": "Dễ", "tb": "Trung bình", "kho": "Khó"}
parts = []
for q in Q:
    n = N[q["key"]]
    body = [q["question"]]
    if q["type"] == "multiple_choice":
        body.append("".join(f'<p class="opt{" ok" if i == q["answer"] else ""}"><b>{"ABCD"[i]}.</b> {o}</p>' for i, o in enumerate(q["options"])))
    elif q["type"] == "true_false":
        body.append("".join(f'<p class="opt"><b>{"abcd"[i]})</b> {s["text"]} <span class="{"ok" if s["answer"] else "bad"}">— {"Đúng" if s["answer"] else "Sai"}</span></p>' for i, s in enumerate(q["statements"])))
    else:
        body.append(f'<p class="opt"><b>Đáp án:</b> <span class="ok">{html.escape(str(q["answer"]))}</span></p>')
    parts.append(f'''<section id="{q["key"]}"><h2>Câu {q["num"]} <span class="mut">· {TYPE[q["type"]]} · {DIFF[n["difficulty"]]}</span></h2>
<p class="mut">{LESSON[q["lesson_id"]]} · Chủ đề: <b>{html.escape(n["topic"])}</b> · <i>{html.escape(q["nguon"])}</i> · <code>{q["key"]}</code></p>
<div class="q">{"".join(body)}</div>
<details><summary>Lời giải</summary><div class="blk">{q["explanation"]}</div></details></section>''')
page = f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Duyệt 20 câu Chương 3 Từ trường phỏng theo HRW</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">
<style>
:root{{--bg:#f7f7f5;--card:#fff;--ink:#1d1d1b;--mut:#666;--line:#ddd;--ok:#1a7f37;--bad:#c62828}}
@media (prefers-color-scheme:dark){{:root{{--bg:#161616;--card:#202020;--ink:#eee;--mut:#aaa;--line:#3a3a3a;--ok:#4caf50;--bad:#ef5350}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,sans-serif}}
main{{max-width:860px;margin:0 auto;padding:16px}}
section{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:0 0 20px}}
h1{{font-size:20px;margin:8px 0 16px}}h2{{margin:0 0 6px;font-size:18px}}.mut{{color:var(--mut);font-size:14px}}
.opt{{margin:4px 0;padding-left:8px}}.opt.ok{{background:rgba(26,127,55,.12);border-radius:6px}}
.ok{{color:var(--ok);font-weight:600}}.bad{{color:var(--bad);font-weight:600}}
.blk{{border-top:1px dashed var(--line);margin-top:8px;padding-top:8px}}summary{{cursor:pointer;margin-top:8px;color:var(--mut)}}
code{{font-size:13px}}
</style></head><body><main>
<h1>Duyệt 20 câu Chương 3 Từ trường — phỏng theo HRW 12e (27/10/2026)</h1>
<p class="mut">6 trắc nghiệm · 8 đúng–sai · 6 trả lời ngắn · 6 dễ / 10 TB / 4 khó · phủ 8 bài (bài 9–16). Chưa ghi DB. Phương án tô xanh là đáp án.</p>
{"".join(parts)}
</main>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js" onload="renderMathInElement(document.body,{{delimiters:[{{left:'$',right:'$',display:false}}],throwOnError:false}})"></script>
</body></html>'''
out = os.path.join(ROOT, "docs", "ra-soat", "cau-hoi-hrw-c3.html")
open(out, "w").write(page)
print(out, len(page))
