import json, html, sys, os
ROOT = "/Users/MAC/Projects/thachlab"
IDS = [10, 11, 12, 13, 14, 125, 126, 127]
NHAP = len(sys.argv) > 1 and sys.argv[1] == "nhap"
OUT = f"{ROOT}/scripts/data/duyet/quiz-ch3-l12/" + ("xem-nhap.html" if NHAP else "xem.html")
cat = json.load(open(f"{ROOT}/public/data/catalog.json"))
TITLE = {l["id"]: l["title"] for l in cat["lessons"]}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
e = html.escape
L = "ABCD"
parts = []
nav = []
for i in IDS:
    p = (f"{ROOT}/scripts/logs/batch-quiz/sinh/{i}.json" if NHAP else f"{ROOT}/scripts/data/theory-quiz/{i}.json")
    d = json.load(open(p))
    d.setdefault("lesson_title", TITLE[i])
    if NHAP: d["generated_by"] = "BẢN NHÁP CHƯA KIỂM CHÉO (Sonnet)"
    qs = d["questions"]
    rm = d.get("review", {}).get("removed", [])
    nav.append(f'<a href="#b{i}">{e(d["lesson_title"])}</a>')
    parts.append(f'<h2 id="b{i}">{e(d["lesson_title"])}</h2><p class="meta">{len(qs)} câu · loại {len(rm)} câu · sinh bởi {e(str(d.get("generated_by")))} · ngày {d.get("generated_at")}</p>')
    for n, q in enumerate(qs, 1):
        t = q["type"]
        h = f'<div class="q"><div class="tag">Câu {n} · {t} · {q.get("kind")} · {q.get("difficulty")}</div><div class="qt">{e(q["question"])}</div>'
        if t == "multiple_choice":
            h += "<ul>" + "".join(f'<li class="{"ok" if k == q["answer"] else ""}"><b>{L[k]}.</b> {e(o)}</li>' for k, o in enumerate(q["options"])) + "</ul>"
        elif t == "true_false":
            h += "<ul>" + "".join(f'<li class="{"ok" if s["answer"] else "no"}"><b>{"abcd"[k]})</b> {e(s["text"])} <em>→ {"Đúng" if s["answer"] else "Sai"}</em></li>' for k, s in enumerate(q["statements"])) + "</ul>"
        else:
            h += f'<p class="ok2">Đáp án: <b>{e(str(q["answer"]))}</b></p>'
        h += f'<div class="ex">Lời giải: {e(q.get("explanation",""))}</div></div>'
        parts.append(h)
    if rm:
        parts.append('<details><summary>Câu đã bị loại khi kiểm chéo (' + str(len(rm)) + ')</summary>' + "".join(f'<p class="rm">• {e(r["question"])}<br><em>{e(r["reason"])}</em></p>' for r in rm) + "</details>")
page = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Quiz Chương 3 lớp 12 - bản xem</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<style>body{{font:16px/1.55 system-ui;max-width:760px;margin:0 auto;padding:16px;background:#fff;color:#111}}
.q{{border:1px solid #ddd;border-radius:10px;padding:12px;margin:12px 0}}.tag{{font-size:12px;color:#666}}.qt{{font-weight:600;margin:6px 0}}
ul{{list-style:none;padding:0;margin:6px 0}}li{{padding:4px 8px;border-radius:6px}}li.ok{{background:#e6f6e9}}li.no{{background:#fdecec}}
.ex{{background:#f5f5f7;border-radius:8px;padding:8px;font-size:15px;margin-top:6px}}.meta{{color:#666}}nav a{{display:block;padding:2px 0}}
.rm{{color:#a33;font-size:14px}}.ok2{{background:#e6f6e9;padding:4px 8px;border-radius:6px}}</style></head><body>
<h1>Quiz lý thuyết Chương 3 lớp 12 — {"BẢN NHÁP mới, chưa kiểm chéo" if NHAP else "bản đang lưu"}</h1><nav>{''.join(nav)}</nav>{''.join(parts)}
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
<script>renderMathInElement(document.body,{{delimiters:[{{left:"$$",right:"$$",display:true}},{{left:"$",right:"$",display:false}}],throwOnError:false}})</script></body></html>"""
open(OUT, "w").write(page)
print(OUT, len(page))
