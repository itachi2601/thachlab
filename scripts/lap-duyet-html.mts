// Dựng trang HTML để thầy duyệt tay các câu ngân hàng nghi lỗi: xem câu (KaTeX), chọn Sửa theo đề xuất / Sửa theo ý thầy / Bỏ / Giữ,
// ghi yêu cầu sửa; trang TỰ LƯU ra file JSON (Chrome/Edge: bấm "Chọn file lưu" một lần, sau đó mỗi thay đổi ghi thẳng vào file).
//   npx tsx scripts/lap-duyet-html.mts scripts/data/duyet/<tên-đợt>      # đọc <thư-mục>/items.json → ghi <thư-mục>/duyet.html
// items.json: [{ id, ghiChu, deXuat? }]. Thầy lưu kết quả thành <thư-mục>/phan-hoi.json; Claude đọc rồi chạy
//   npx tsx scripts/ap-dung-duyet.mts <thư-mục>      # "Bỏ" → ẩn câu (archived=true, có sao lưu); "Sửa" → in ra để Claude sửa
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const d = path.dirname(fileURLToPath(import.meta.url));
const env = (k: string) => fs.readFileSync(path.resolve(d, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const dir = path.resolve(process.argv[2] ?? "");
const items: { id: number; ghiChu: string; deXuat?: string }[] = JSON.parse(fs.readFileSync(path.join(dir, "items.json"), "utf8"));
const { data, error } = await sb.from("question_bank").select("id, grade, qtype, question").in("id", items.map((i) => i.id));
if (error) { console.error(error.message); process.exit(1); }
const rows = items.map((it) => ({ ...it, grade: data!.find((r) => r.id === it.id)?.grade, qtype: data!.find((r) => r.id === it.id)?.qtype, q: data!.find((r) => r.id === it.id)?.question }));
const batch = path.basename(dir);
const json = JSON.stringify({ batch, rows }).replace(/</g, "\\u003c");
const html = `<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Duyệt câu hỏi ${batch}</title>
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
h2{margin:0 0 8px;font-size:18px}.mut{color:var(--mut);font-size:14px}
.note{background:var(--warn);padding:8px 12px;border-radius:8px;margin:8px 0}
.q img{max-width:100%}.blk{border-top:1px dashed var(--line);margin-top:10px;padding-top:8px}
label.opt{display:block;padding:8px 0;min-height:44px}textarea{width:100%;box-sizing:border-box;min-height:80px;font:inherit;padding:8px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink)}
#st{font-size:14px}.ok{color:#1a7f37}.bad{color:#c62828}
</style></head><body>
<header><strong>Duyệt ${batch}</strong><button class="p" id="pick">Chọn file lưu (phan-hoi.json)</button><button id="dl">Tải JSON về</button><span id="st" class="mut">Chưa chọn file — tạm lưu trong trình duyệt.</span></header>
<main id="m"></main>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js"></script>
<script>
const D=${json};
const KEY="duyet-"+D.batch;let fh=null,state={};
try{state=JSON.parse(localStorage.getItem(KEY)||"{}")}catch(e){}
const esc=s=>String(s??"").replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
const ACT=[["de_xuat","Sửa theo đề xuất của Claude"],["y_thay","Sửa theo ý thầy (ghi bên dưới)"],["bo","Bỏ câu này (ẩn khỏi ngân hàng)"],["giu","Giữ nguyên — không có lỗi"]];
function blocks(q){let h='<div class="q">'+(q.question||"")+'</div>';
 if(Array.isArray(q.options))h+='<div class="blk">'+q.options.map((o,i)=>'<div>'+"ABCD"[i]+'. '+(typeof o==="string"?o:(o.text??JSON.stringify(o)))+'</div>').join("")+'</div>';
 if(Array.isArray(q.statements))h+='<div class="blk">'+q.statements.map((s,i)=>'<div>'+"abcd"[i]+') '+s.text+' <b>['+(s.answer?"Đúng":"Sai")+']</b></div>').join("")+'</div>';
 if(q.answer!==undefined&&!Array.isArray(q.statements))h+='<div class="blk"><b>Đáp án:</b> '+esc(JSON.stringify(q.answer))+'</div>';
 if(q.explanation)h+='<div class="blk"><b>Lời giải:</b><br>'+q.explanation+'</div>';return h}
document.getElementById("m").innerHTML=D.rows.map(r=>{const s=state[r.id]||{};return '<section data-id="'+r.id+'"><h2>#'+r.id+' <span class="mut">lớp '+esc(r.grade)+' · '+esc(r.qtype)+'</span></h2>'
 +'<div class="note"><b>Nghi ngờ:</b> '+esc(r.ghiChu)+(r.deXuat?'<br><b>Đề xuất:</b> '+esc(r.deXuat):'')+'</div>'+blocks(r.q||{})
 +'<div class="blk">'+ACT.map(([v,t])=>'<label class="opt"><input type="radio" name="a'+r.id+'" value="'+v+'"'+(s.action===v?" checked":"")+'> '+t+'</label>').join("")
 +'<textarea placeholder="Yêu cầu sửa / ghi chú cho Claude (ví dụ: V₁ = 10.10^-3 m³, đổi cả phần đề lẫn đáp án)">'+esc(s.note||"")+'</textarea></div></section>'}).join("");
function out(){return JSON.stringify({batch:D.batch,savedAt:new Date().toISOString(),items:Object.fromEntries(Object.entries(state).map(([k,v])=>[k,v]))},null,2)}
const st=document.getElementById("st");
async function save(){try{localStorage.setItem(KEY,JSON.stringify(state))}catch(e){}
 if(!fh){return}try{const w=await fh.createWritable();await w.write(out());await w.close();st.className="ok";st.textContent="Đã lưu "+new Date().toLocaleTimeString("vi")+" → "+fh.name}catch(e){st.className="bad";st.textContent="Lưu lỗi: "+e.message}}
document.getElementById("m").addEventListener("input",e=>{const sec=e.target.closest("section");if(!sec)return;const id=sec.dataset.id;const o=state[id]||(state[id]={});
 if(e.target.type==="radio")o.action=e.target.value;else o.note=e.target.value;save()});
document.getElementById("pick").onclick=async()=>{if(!window.showSaveFilePicker){alert("Trình duyệt này không hỗ trợ tự lưu — dùng Chrome/Edge, hoặc bấm Tải JSON về.");return}
 try{fh=await showSaveFilePicker({suggestedName:"phan-hoi.json",types:[{description:"JSON",accept:{"application/json":[".json"]}}]});await save()}catch(e){}};
document.getElementById("dl").onclick=()=>{const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([out()],{type:"application/json"}));a.download="phan-hoi.json";a.click()};
addEventListener("load",()=>renderMathInElement(document.body,{delimiters:[{left:"$$",right:"$$",display:true},{left:"$",right:"$",display:false}],throwOnError:false}));
</script></body></html>`;
fs.writeFileSync(path.join(dir, "duyet.html"), html);
console.log("Đã ghi", path.join(dir, "duyet.html"), "·", rows.length, "câu");
