# Từ cau.json sinh: (1) scripts/sql/soan-cau-dang-thieu-ly-thuyet.sql  (2) duyet.html (trang thầy duyệt, KaTeX)
#   python3 scripts/data/soan-cau-dang-thieu/tao-sql-va-trang.py [--bo stt,stt,...]
import json, os, sys, html
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, "..", "..", ".."))
rows = json.load(open(os.path.join(here, "cau.json")))
bo = set()
if "--bo" in sys.argv: bo = {int(x) for x in sys.argv[sys.argv.index("--bo") + 1].split(",") if x}
rows = [r for r in rows if r["stt"] not in bo]
NOTE = "soan-dang-thieu-ly-thuyet-20261105"
SRC = "claude-2026-11-05-soan-dang-thieu"

vals = []
for r in rows:
    qj = json.dumps(r["q"], ensure_ascii=False)
    assert "$q$" not in qj and "$l$" not in r["dang_label"]
    vals.append(f"  ($q${qj}$q$::jsonb, {r['topic_id']}, $l${r['topic_name']}$l$, {r['lesson_id']}, $l${r['dang_label']}$l$)")
sql = f"""-- Câu mới soạn cho {len({r['key'] for r in rows})} dạng LÝ THUYẾT/HIỆN TƯỢNG có dưới 3 câu chắc (docs/dang-thieu-cau.md), {len(rows)} câu.
-- Nguồn: scripts/data/soan-cau-dang-thieu/cau.py (soạn trong phiên 05/11/2026, kiem-code soát độc lập, thầy duyệt qua duyet.html).
-- CHẠY SAU KHI THẦY DUYỆT, sau 22h. Ghi: question_bank (note = '{NOTE}', archived = false) + question_dang (source = '{SRC}', unsure = false).
-- Câu trùng content_hash với câu đã có thì bỏ qua (không gán dạng cho câu cũ).
-- Rollback (không có bảng nào khác tham chiếu câu mới ngay sau khi nạp):
--   begin; delete from public.question_dang where source = '{SRC}';
--          delete from public.question_bank where note = '{NOTE}'; commit;
begin;
create temp table _v (q jsonb, tid bigint, tname text, lid bigint, label text) on commit drop;
insert into _v values
{",\n".join(vals)};

create temp table _moi on commit drop as
with ins as (
  insert into public.question_bank (subject_code, grade, topic_id, topic_name, form, qtype, difficulty, difficulty_source, question, content_hash, archived, note)
  select 'vat-ly', (select t.grade from public.question_topics t where t.id = v.tid), v.tid, v.tname, 'bai_tap', v.q->>'type', v.q->>'difficulty', 'ai',
         v.q, public.question_content_hash(v.q), false, '{NOTE}'
  from _v v
  where not exists (select 1 from public.question_bank b where b.content_hash = public.question_content_hash(v.q))
  returning id, content_hash
)
select ins.id, v.lid, v.label from ins join _v v on public.question_content_hash(v.q) = ins.content_hash;

insert into public.question_dang (question_id, lesson_id, dang_label, unsure, source)
select id, lid, label, false, '{SRC}' from _moi
on conflict (question_id, lesson_id) do nothing;

-- Kiểm: số câu mới / số gán dạng (kỳ vọng {len(rows)} / {len(rows)}); câu thiếu grade (topic không có lớp) phải = 0
select (select count(*) from public.question_bank where note = '{NOTE}') as cau_moi,
       (select count(*) from public.question_dang where source = '{SRC}') as gan_dang,
       (select count(*) from public.question_bank where note = '{NOTE}' and grade is null) as thieu_grade;
commit;
"""
open(os.path.join(root, "scripts", "sql", "soan-cau-dang-thieu-ly-thuyet.sql"), "w").write(sql)

# ---------- trang duyệt ----------
by = {}
for r in rows: by.setdefault(r["key"], []).append(r)
def card(r):
    q = r["q"]; h = f'<article id="c{r["stt"]}"><div class="meta">#{r["stt"]} · {"Trắc nghiệm" if q["type"]=="multiple_choice" else "Đúng/Sai"} · {q["difficulty"]}</div>'
    h += f'<div class="q">{q["question"]}</div>'
    if q["type"] == "multiple_choice":
        h += '<ol class="opt">' + "".join(f'<li class="{"ok" if i==q["answer"] else ""}"><b>{"ABCD"[i]}.</b> {o}</li>' for i, o in enumerate(q["options"])) + "</ol>"
    else:
        h += '<ol class="opt">' + "".join(f'<li><b>{"abcd"[i]})</b> {s["text"]} <span class="tag {"d" if s["answer"] else "s"}">{"Đúng" if s["answer"] else "Sai"}</span></li>' for i, s in enumerate(q["statements"])) + "</ol>"
    h += f'<details><summary>Lời giải</summary>{q["explanation"]}</details>'
    h += f'<div class="act" data-stt="{r["stt"]}"><label><input type="radio" name="a{r["stt"]}" value="ok"> Đăng</label><label><input type="radio" name="a{r["stt"]}" value="sua"> Sửa</label><label><input type="radio" name="a{r["stt"]}" value="bo"> Bỏ</label><textarea placeholder="Ghi chú cho Claude (nếu Sửa/Bỏ)"></textarea></div></article>'
    return h
sections = "".join(f'<section><h2>{html.escape(v[0]["dang_label"])}</h2><p class="sub">Bài {v[0]["lesson_id"]} · {html.escape(v[0]["topic_name"])} · {len(v)} câu mới</p>{"".join(card(r) for r in v)}</section>' for v in by.values())
page = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Duyệt câu dạng thiếu</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">
<style>
:root{{--bg:#f7f7f5;--card:#fff;--ink:#1d1d1b;--mut:#666;--line:#ddd;--acc:#1a56db;--ok:#e6f4ea;--okb:#1a7f37;--bad:#c62828}}
@media (prefers-color-scheme:dark){{:root{{--bg:#161616;--card:#202020;--ink:#eee;--mut:#aaa;--line:#3a3a3a;--acc:#6ea0ff;--ok:#16301d;--okb:#5cc879;--bad:#ff7b7b}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,sans-serif}}
header{{position:sticky;top:0;z-index:5;background:var(--card);border-bottom:1px solid var(--line);padding:10px 16px;display:flex;gap:10px;flex-wrap:wrap;align-items:center}}
main{{max-width:820px;margin:0 auto;padding:16px}}h1{{font-size:18px;margin:0}}h2{{font-size:17px;margin:24px 0 2px}}.sub,.meta{{color:var(--mut);font-size:14px}}
article{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:10px 0}}
.opt{{list-style:none;padding:0;margin:8px 0}}.opt li{{padding:4px 8px;border-radius:6px}}.opt li.ok{{background:var(--ok);outline:1px solid var(--okb)}}
.tag{{font-size:13px;font-weight:600;padding:1px 6px;border-radius:5px;margin-left:4px}}.tag.d{{color:var(--okb)}}.tag.s{{color:var(--bad)}}
details{{border-top:1px dashed var(--line);padding-top:6px}}summary{{cursor:pointer;color:var(--acc);min-height:32px}}
.act{{display:flex;gap:14px;flex-wrap:wrap;align-items:center;margin-top:8px}}.act label{{min-height:44px;display:flex;align-items:center;gap:4px}}
textarea{{flex:1 1 100%;min-height:44px;font:inherit;padding:6px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink);box-sizing:border-box}}
button{{font:inherit;min-height:44px;padding:6px 14px;border-radius:8px;border:1px solid var(--acc);background:var(--acc);color:#fff;cursor:pointer}}
</style></head><body>
<header><h1>Duyệt {len(rows)} câu · {len(by)} dạng lý thuyết</h1><span class="sub" id="st"></span><button id="dl">Tải phan-hoi.json</button></header>
<main><p class="sub">Đáp án đúng tô xanh; lời giải bấm để mở. Mặc định câu không chọn gì = Đăng. Chọn Sửa/Bỏ kèm ghi chú rồi bấm “Tải phan-hoi.json” và gửi file cho Claude. Tự lưu trong trình duyệt.</p>{sections}</main>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js"></script>
<script>
const K="duyet-soan-dang-thieu";let S={{}};try{{S=JSON.parse(localStorage.getItem(K)||"{{}}")}}catch(e){{}}
const st=document.getElementById("st");
function upd(){{const n=Object.values(S).filter(v=>v.a&&v.a!=="ok").length;st.textContent=n?n+" câu Sửa/Bỏ":"";try{{localStorage.setItem(K,JSON.stringify(S))}}catch(e){{}}}}
document.querySelectorAll(".act").forEach(el=>{{const id=el.dataset.stt,s=S[id]||{{}};const ta=el.querySelector("textarea");ta.value=s.n||"";
 el.querySelectorAll("input").forEach(i=>{{if(i.value===s.a)i.checked=true;i.onchange=()=>{{S[id]={{...(S[id]||{{}}),a:i.value}};upd()}}}});
 ta.oninput=()=>{{S[id]={{...(S[id]||{{}}),n:ta.value}};upd()}}}});upd();
document.getElementById("dl").onclick=()=>{{const b=new Blob([JSON.stringify({{batch:"soan-dang-thieu-ly-thuyet",savedAt:new Date().toISOString(),items:S}},null,2)],{{type:"application/json"}});
 const a=document.createElement("a");a.href=URL.createObjectURL(b);a.download="phan-hoi.json";a.click()}};
document.addEventListener("DOMContentLoaded",()=>renderMathInElement(document.body,{{delimiters:[{{left:"$$",right:"$$",display:true}},{{left:"$",right:"$",display:false}}],throwOnError:false}}));
</script></body></html>"""
open(os.path.join(here, "duyet.html"), "w").write(page)
print(f"SQL + trang duyệt: {len(rows)} câu, {len(by)} dạng" + (f" (bỏ {sorted(bo)})" if bo else ""))
