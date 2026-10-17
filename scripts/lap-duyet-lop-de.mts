// Dựng trang HTML để thầy chọn LỚP cho các đề đã đăng chưa gán exam_classes (script gan-lop-de-chua-gan.mts không suy được).
//   npx tsx scripts/lap-duyet-lop-de.mts scripts/data/duyet/<tên-đợt>   # đọc <thư-mục>/items.json → ghi <thư-mục>/duyet.html
// items.json: [{ id, title, ghiChu, deXuat? }] (deXuat = class_id đề xuất). Thầy lưu kết quả thành <thư-mục>/phan-hoi.json
// (Chrome/Edge: "Chọn file lưu" một lần, mỗi thay đổi tự ghi), rồi Claude chạy scripts/ap-dung-duyet-lop-de.mts <thư-mục>.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const d = path.dirname(fileURLToPath(import.meta.url));
const env = (k: string) => fs.readFileSync(path.resolve(d, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const dir = path.resolve(process.argv[2] ?? "");
const items: { id: number; ghiChu: string; deXuat?: string }[] = JSON.parse(fs.readFileSync(path.join(dir, "items.json"), "utf8"));
const [{ data: ex, error }, { data: cls }] = await Promise.all([
  sb.from("exams").select("id, title, question_count, duration_minutes, created_at, subject_code, questions").in("id", items.map((i) => i.id)),
  sb.from("classes").select("id, name").order("id"),
]);
if (error) { console.error(error.message); process.exit(1); }
const rows = items.map((it) => {
  const e = ex!.find((r) => r.id === it.id);
  const qs = Array.isArray(e?.questions) ? (e!.questions as { question?: string; options?: unknown[] }[]).slice(0, 2) : [];
  return { ...it, title: e?.title, n: e?.question_count, phut: e?.duration_minutes, ngay: e?.created_at?.slice(0, 10), mon: e?.subject_code, qs: qs.map((q) => ({ question: q.question, options: q.options })) };
});
const batch = path.basename(dir);
const json = JSON.stringify({ batch, rows, classes: cls ?? [] }).replace(/</g, "\\u003c");
const html = `<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Gán lớp cho đề ${batch}</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">
<style>
:root{--bg:#f7f7f5;--card:#fff;--ink:#1d1d1b;--mut:#666;--line:#ddd;--acc:#1a56db;--warn:#fff4cc}
@media (prefers-color-scheme:dark){:root{--bg:#161616;--card:#202020;--ink:#eee;--mut:#aaa;--line:#3a3a3a;--acc:#6ea0ff;--warn:#4a3f10}}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,sans-serif}
header{position:sticky;top:0;background:var(--card);border-bottom:1px solid var(--line);padding:10px 16px;z-index:5;display:flex;gap:12px;flex-wrap:wrap;align-items:center}
button{font:inherit;padding:8px 14px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);cursor:pointer;min-height:44px}
button.p{background:var(--acc);color:#fff;border-color:var(--acc)}
main{max-width:860px;margin:0 auto;padding:16px}
section{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:0 0 20px}
h2{margin:0 0 4px;font-size:18px}.mut{color:var(--mut);font-size:14px}
.note{background:var(--warn);padding:8px 12px;border-radius:8px;margin:8px 0}
.q{border-top:1px dashed var(--line);margin-top:10px;padding-top:8px;font-size:15px}.q img{max-width:100%}
.opts{display:flex;flex-wrap:wrap;gap:6px 14px;margin-top:10px}label.opt{display:inline-flex;align-items:center;gap:6px;min-height:44px;padding:0 6px}
textarea{width:100%;box-sizing:border-box;min-height:44px;font:inherit;padding:8px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink);margin-top:6px}
#st{font-size:14px}.ok{color:#1a7f37}.bad{color:#c62828}details{margin-top:6px}summary{cursor:pointer;color:var(--acc)}
</style></head><body>
<header><strong>Gán lớp · ${batch}</strong><button class="p" id="pick">Chọn file lưu (phan-hoi.json)</button><button id="dl">Tải JSON về</button><button id="all12">Chọn đề xuất cho tất cả</button><span id="st" class="mut">Chưa chọn file — tạm lưu trong trình duyệt.</span></header>
<main id="m"></main>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js"></script>
<script>
const D=${json};
const KEY="duyet-"+D.batch;let fh=null,state={};
try{state=JSON.parse(localStorage.getItem(KEY)||"{}")}catch(e){}
const esc=s=>String(s??"").replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
const ACT=[...D.classes.map(c=>[String(c.id),"Lớp "+c.name]),["toan_truong","Để toàn trường (mọi lớp thấy)"],["an","Ẩn đề (published=false)"]];
function qs(list){return (list||[]).map((q,i)=>'<div class="q"><b>Câu '+(i+1)+'.</b> '+(q.question||"")+(Array.isArray(q.options)?'<div>'+q.options.map((o,j)=>'<div>'+"ABCD"[j]+'. '+(typeof o==="string"?o:(o&&o.text)||JSON.stringify(o))+'</div>').join("")+'</div>':'')+'</div>').join("")}
document.getElementById("m").innerHTML=D.rows.map(r=>{const s=state[r.id]||{};return '<section data-id="'+r.id+'"><h2>#'+r.id+' · '+esc(r.title)+'</h2><div class="mut">'+esc(r.n)+' câu · '+esc(r.phut)+' phút · đăng '+esc(r.ngay)+' · '+esc(r.mon)+'</div>'
 +'<div class="note">'+esc(r.ghiChu)+(r.deXuat?'<br><b>Đề xuất:</b> '+esc((ACT.find(a=>a[0]===r.deXuat)||[])[1]||r.deXuat):'')+'</div>'
 +'<details><summary>Xem 2 câu đầu</summary>'+qs(r.qs)+'</details>'
 +'<div class="opts">'+ACT.map(([v,t])=>'<label class="opt"><input type="radio" name="a'+r.id+'" value="'+v+'"'+(s.action===v?" checked":"")+'> '+t+'</label>').join("")+'</div>'
 +'<textarea placeholder="Ghi chú cho Claude (nếu cần)">'+esc(s.note||"")+'</textarea></section>'}).join("");
function out(){return JSON.stringify({batch:D.batch,savedAt:new Date().toISOString(),items:state},null,2)}
const st=document.getElementById("st");
async function save(){try{localStorage.setItem(KEY,JSON.stringify(state))}catch(e){}
 if(!fh){return}try{const w=await fh.createWritable();await w.write(out());await w.close();st.className="ok";st.textContent="Đã lưu "+new Date().toLocaleTimeString("vi")+" → "+fh.name}catch(e){st.className="bad";st.textContent="Lưu lỗi: "+e.message}}
document.getElementById("m").addEventListener("input",e=>{const sec=e.target.closest("section");if(!sec)return;const id=sec.dataset.id;const o=state[id]||(state[id]={});
 if(e.target.type==="radio")o.action=e.target.value;else o.note=e.target.value;save()});
document.getElementById("all12").onclick=()=>{for(const r of D.rows){if(!r.deXuat)continue;(state[r.id]||(state[r.id]={})).action=r.deXuat;const el=document.querySelector('section[data-id="'+r.id+'"] input[value="'+r.deXuat+'"]');if(el)el.checked=true}save()};
document.getElementById("pick").onclick=async()=>{if(!window.showSaveFilePicker){alert("Trình duyệt này không hỗ trợ tự lưu — dùng Chrome/Edge, hoặc bấm Tải JSON về.");return}
 try{fh=await showSaveFilePicker({suggestedName:"phan-hoi.json",types:[{description:"JSON",accept:{"application/json":[".json"]}}]});await save()}catch(e){}};
document.getElementById("dl").onclick=()=>{const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([out()],{type:"application/json"}));a.download="phan-hoi.json";a.click()};
addEventListener("load",()=>renderMathInElement(document.body,{delimiters:[{left:"$$",right:"$$",display:true},{left:"$",right:"$",display:false}],throwOnError:false}));
</script></body></html>`;
fs.writeFileSync(path.join(dir, "duyet.html"), html);
console.log("Đã ghi", path.join(dir, "duyet.html"), "·", rows.length, "đề");
