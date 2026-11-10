# Dựng xem-thu.html: đề (từ l10-dong-luc-hoc.json) | hình (svg/<id>.svg). Chạy từ gốc repo.
import json,re,os
b='scripts/data/hinh-cau-hoi/'
d={r['id']:r for r in json.load(open(b+'l10-dong-luc-hoc.json'))}
ids=[int(f[:-4]) for f in sorted(os.listdir(b+'svg'),key=lambda f:int(f[:-4])) if f.endswith('.svg')]
strip=lambda x:re.sub(r'<img[^>]*class="eq"[^>]*>','',str(x))
def txt(o): return o if isinstance(o,str) else o.get('text','')
cards=''
for i in ids:
    q=d[i]['question']; svg=open(b+f'svg/{i}.svg').read()
    opts=''.join(f'<li>{strip(txt(o))}</li>' for o in (q.get('options') or q.get('statements') or []))
    cards+=f'<section><div class="fig">{svg}</div><div class="q"><small>#{i} · {d[i]["topic_name"]}</small><p>{strip(q["question"])}</p><ol type="{"A" if q.get("options") else "a"}">{opts}</ol></div></section>'
open(b+'xem-thu.html','w').write(f'''<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Xem thử hình L10</title>
<style>body{{font:16px/1.6 system-ui;max-width:980px;margin:0 auto;padding:16px;color:#1e293b;background:#fff}}section{{display:grid;grid-template-columns:minmax(0,1fr);gap:12px;border-bottom:1px solid #e2e8f0;padding:16px 0}}
@media(min-width:760px){{section{{grid-template-columns:minmax(0,1fr) minmax(0,420px)}}.fig{{order:2}}}}.fig svg{{width:100%;height:auto;max-width:440px}}small{{color:#64748b}}</style>
<h1>Thí điểm hình minh hoạ — L10 Động lực học</h1>{cards}''')
print(len(ids),'câu')
