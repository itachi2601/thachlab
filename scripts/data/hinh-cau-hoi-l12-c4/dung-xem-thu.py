# Dựng xem-thu.html: đề (từ l12-hat-nhan.json) | hình (svg/<id>.svg). Chạy: python3 dung-xem-thu.py
import json,re,os
b=os.path.dirname(os.path.abspath(__file__))+'/'
d={r['id']:r for r in json.load(open(b+'l12-hat-nhan.json'))}
ids=sorted(int(f[:-4]) for f in os.listdir(b+'svg') if f.endswith('.svg'))
strip=lambda x:re.sub(r'<img[^>]*class="eq"[^>]*>','',str(x))
def txt(o): return o if isinstance(o,str) else o.get('text','')
cards=''
for i in ids:
    q=d[i]['question']; svg=open(b+f'svg/{i}.svg').read()
    opts=''.join(f'<li>{strip(txt(o))}</li>' for o in (q.get('options') or q.get('statements') or []))
    cards+=f'<section><div class="fig">{svg}</div><div class="q"><small>#{i} · {d[i]["topic_name"]}</small><p>{strip(q["question"])}</p><ol type="{"A" if q.get("options") else "a"}">{opts}</ol></div></section>'
open(b+'xem-thu.html','w').write(f'''<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Xem thử hình L12 C4</title>
<link rel=stylesheet href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css"><script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script><script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body,{{delimiters:[{{left:'$',right:'$',display:false}}]}})"></script>
<style>:root{{color-scheme:light dark}}body{{font:16px/1.6 system-ui;max-width:980px;margin:0 auto;padding:16px;color:#1e293b;background:#fff}}@media(prefers-color-scheme:dark){{body{{color:#e2e8f0;background:#0f172a}}}}section{{display:grid;grid-template-columns:minmax(0,1fr);gap:12px;border-bottom:1px solid #94a3b833;padding:16px 0}}
@media(min-width:760px){{section{{grid-template-columns:minmax(0,1fr) minmax(0,420px)}}.fig{{order:2}}}}.fig svg{{width:100%;height:auto;max-width:440px}}small{{color:#64748b}}</style>
<h1>Hình minh hoạ — L12 Chương 4 Vật lí hạt nhân</h1>{cards}''')
print(len(ids),'câu')
