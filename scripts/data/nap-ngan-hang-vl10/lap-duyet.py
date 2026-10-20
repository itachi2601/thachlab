#!/usr/bin/env python3
"""Dựng duyet/duyet.html cho các câu chưa khớp (giữa đáp án nguồn và 2 lượt giải độc lập). Không dùng LLM, không đụng DB."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
cau = {q['key']: q for q in json.load(open(f'{H}/cau-bank.json'))}
hk = {o['key']: o for o in json.load(open(f'{H}/ket-qua-haiku.json'))}
sn = {o['key']: o for o in json.load(open(f'{H}/ket-qua.json')) if o['trangThai'] != 'chua-co-ket-qua'}
rows = []
for k, q in cau.items():
    h = hk.get(k, {}); s = sn.get(k)
    if h.get('trangThai') == 'khop' or (s and s['trangThai'] == 'khop'): continue
    lydo = {'LECH': 'Đáp án nguồn lệch với lời giải độc lập', 'khong-co-dap-so-nguon': 'Lời giải gốc không nêu đáp số',
            'chua-co-ket-qua': 'Chưa có kết quả giải'}.get((s or h).get('trangThai'), '?')
    rows.append({'key': k, 'type': q['type'], 'q': q['question'], 'options': q.get('options'), 'statements': q.get('statements'),
                 'nguon': (s or h).get('nguon'), 'haiku': h.get('giai'), 'sonnet': s.get('giai') if s else None,
                 'goc': q['gocLoiGiai'], 'giaiAI': (s or h).get('explanation', ''), 'lydo': lydo, 'ghiChuAI': ((s or h).get('ghi_chu') or '')})
json.dump(rows, open(f'{H}/duyet/items.json', 'w'), ensure_ascii=False, indent=1)
data = json.dumps({'rows': rows}, ensure_ascii=False).replace('<', '\\u003c')
html = '''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Duyệt câu VL10 Chương III</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">
<style>
:root{--bg:#f7f7f5;--card:#fff;--ink:#1d1d1b;--mut:#666;--line:#ddd;--acc:#1a56db;--warn:#fff4cc;--ok:#1a7f37}
@media (prefers-color-scheme:dark){:root{--bg:#161616;--card:#202020;--ink:#eee;--mut:#aaa;--line:#3a3a3a;--acc:#6ea0ff;--warn:#4a3f10;--ok:#4cc16a}}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,sans-serif}
header{position:sticky;top:0;background:var(--card);border-bottom:1px solid var(--line);padding:10px 16px;z-index:5;display:flex;gap:12px;flex-wrap:wrap;align-items:center}
button{font:inherit;padding:8px 14px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);cursor:pointer;min-height:44px}
button.p{background:var(--acc);color:#fff;border-color:var(--acc)}
main{max-width:860px;margin:0 auto;padding:16px}
section{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:0 0 20px}
section.done{border-color:var(--ok)}
h2{margin:0 0 8px;font-size:17px}.mut{color:var(--mut);font-size:14px}
.note{background:var(--warn);padding:8px 12px;border-radius:8px;margin:8px 0}
.opt{padding:4px 0}.tag{display:inline-block;font-size:13px;border-radius:6px;padding:0 6px;margin-left:6px;border:1px solid var(--line)}
.ans{margin:10px 0;padding:8px 12px;border-radius:8px;border:1px solid var(--line);font-size:15px}
label.c{display:block;padding:8px 0;min-height:44px}textarea,input[type=text]{width:100%;box-sizing:border-box;font:inherit;padding:8px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink)}
details{margin-top:8px}summary{cursor:pointer;min-height:32px}
</style></head><body>
<header><strong>Duyệt VL10 Chương III</strong><button class="p" id="pick">Chọn file lưu (phan-hoi.json)</button><button id="dl">Tải JSON về</button><span id="st" class="mut">Chưa chọn file — tạm lưu trong trình duyệt</span><span id="cnt" class="mut"></span></header>
<main id="m"></main>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js"></script>
<script>
const D=__DATA__;const KEY='duyet-vl10-c3';let fh=null,R={};
try{R=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
const L='ABCD',S='abcd';
const fmt=a=>a==null?'—':Array.isArray(a)?a.map((v,i)=>S[i]+':'+(v?'Đ':'S')).join(' '):String(a);
function render(){const m=document.getElementById('m');m.innerHTML='';
D.rows.forEach((r,i)=>{const s=document.createElement('section');const v=R[r.key]||{};if(v.choice)s.className='done';
let body=`<h2>${i+1}/${D.rows.length} · ${r.key} · ${({multiple_choice:'Trắc nghiệm',true_false:'Đúng–Sai',short_answer:'Trả lời ngắn'})[r.type]}</h2><div class="note">${r.lydo}</div><div>${r.q}</div>`;
if(r.options)body+=r.options.map((o,j)=>`<div class="opt"><b>${L[j]}.</b> ${o}</div>`).join('');
if(r.statements)body+=r.statements.map((o,j)=>`<div class="opt"><b>${S[j]})</b> ${o.text}</div>`).join('');
body+=`<div class="ans"><b>Nguồn (file Word):</b> ${fmt(r.nguon)}<br><b>Haiku:</b> ${fmt(r.haiku)} · <b>Sonnet:</b> ${fmt(r.sonnet)}${r.ghiChuAI?'<br><i>Ghi chú AI: '+r.ghiChuAI+'</i>':''}</div>`;
body+=`<details><summary>Lời giải gốc trong Word</summary><div>${(r.goc||'(trống)').replace(/\\n/g,'<br>')}</div></details>`;
body+=`<details><summary>Lời giải của Sonnet/Haiku</summary><div>${r.giaiAI||'(không có)'}</div></details>`;
const ch=[['nguon','Đáp án nguồn đúng'],['ai','Đáp án của Sonnet đúng'],['khac','Đáp án khác (ghi bên dưới)'],['bo','Bỏ câu này']];
body+=ch.map(([c,t])=>`<label class="c"><input type="radio" name="r${i}" value="${c}" ${v.choice===c?'checked':''}> ${t}</label>`).join('');
body+=`<input type="text" placeholder="Đáp án khác / ghi chú (vd: B, hoặc a Đ b S c Đ d S, hoặc 2,5)" value="${(v.note||'').replace(/"/g,'&quot;')}">`;
s.innerHTML=body;m.appendChild(s);
s.querySelectorAll('input[type=radio]').forEach(x=>x.onchange=()=>{(R[r.key]=R[r.key]||{}).choice=x.value;save();s.className='done'});
s.querySelector('input[type=text]').oninput=e=>{(R[r.key]=R[r.key]||{}).note=e.target.value;save()};});
if(window.renderMathInElement)renderMathInElement(m,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false});
document.getElementById('cnt').textContent=Object.values(R).filter(x=>x.choice).length+'/'+D.rows.length+' đã chọn';}
async function save(){try{localStorage.setItem(KEY,JSON.stringify(R))}catch(e){}
document.getElementById('cnt').textContent=Object.values(R).filter(x=>x.choice).length+'/'+D.rows.length+' đã chọn';
if(fh){try{const w=await fh.createWritable();await w.write(JSON.stringify(R,null,1));await w.close();document.getElementById('st').textContent='Đã lưu vào file';}catch(e){document.getElementById('st').textContent='Lỗi ghi file: '+e.message}}}
document.getElementById('pick').onclick=async()=>{if(!window.showSaveFilePicker){alert('Trình duyệt không hỗ trợ — dùng nút Tải JSON về');return}
fh=await showSaveFilePicker({suggestedName:'phan-hoi.json',types:[{description:'JSON',accept:{'application/json':['.json']}}]});save()};
document.getElementById('dl').onclick=()=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(R,null,1)],{type:'application/json'}));a.download='phan-hoi.json';a.click()};
window.addEventListener('load',()=>setTimeout(render,300));
</script></body></html>'''.replace('__DATA__', data)
open(f'{H}/duyet/duyet.html', 'w', encoding='utf8').write(html)
from collections import Counter
print(len(rows), Counter(r['lydo'] for r in rows))
