// Dựng trang HTML duyệt các câu "đề mơ hồ" mà Sonnet không cho ghi thẳng (hỏi / ẩn / đổi đáp án / lời giải cần sửa).
//   npx tsx scripts/lap-duyet-mo-ho.mts   đọc scripts/data/giai-lai/mo-ho/{lo,kq}-NN.json (+ kq-08b.json đè kq-08) → mo-ho/duyet/duyet.html
// Thầy bấm "Chọn file lưu" một lần (Chrome), chọn từng câu, file phan-hoi.json tự lưu cùng thư mục.
import fs from "node:fs";
const DIR = "scripts/data/giai-lai/mo-ho/";
const ls = fs.readdirSync(DIR);
const src = new Map<number, any>();
for (const f of ls.filter((f) => /^lo-\d+\.json$/.test(f))) for (const x of JSON.parse(fs.readFileSync(DIR + f, "utf8"))) src.set(x.id, x);
const kq = new Map<number, any>();
for (const f of ls.filter((f) => /^kq-\d+\.json$/.test(f))) for (const x of JSON.parse(fs.readFileSync(DIR + f, "utf8"))) kq.set(x.id, x);
if (ls.includes("kq-08b.json")) for (const x of JSON.parse(fs.readFileSync(DIR + "kq-08b.json", "utf8"))) kq.set(x.id, x);
const ORDER: Record<string, number> = { doi: 0, hoi: 1, an: 2, sua: 3 };
// "doi" mà đáp án đề nghị trùng dap_an_db = lô xuất lúc đáp án ngân hàng đang bị trigger ghi đè (đã khôi phục) → coi như "ghi"
const trungDb = (k: any) => k.kl === "doi" && String(k.dap_an_dung ?? "").replace(/\s/g, "").charAt(0).toUpperCase() === String(src.get(k.id)?.dap_an_db ?? "").charAt(0).toUpperCase();
const rows = [...kq.values()].filter((k) => !trungDb(k) && (k.kl !== "ghi" || k.sua)).map((k) => {
  const s = src.get(k.id);
  return { id: k.id, lop: s.lop, chu_de: s.chu_de, q: s.cau_hoi, db: s.dap_an_db, loai: k.kl === "ghi" ? "sua" : k.kl, tuGiai: k.tu_giai, dung: k.dap_an_dung ?? "", sua: k.sua ?? "", lyDo: k.ly_do ?? "",
    ghiHaiku: s.ghi_chu_haiku ?? "", exMoi: s.loi_giai_moi ?? "" };
}).sort((a, b) => (ORDER[a.loai] ?? 9) - (ORDER[b.loai] ?? 9) || a.id - b.id);
const json = JSON.stringify({ batch: "mo-ho", rows }).replace(/</g, "\\u003c");
const html = `<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Duyệt câu đề mơ hồ</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">
<style>:root{--bg:#f7f7f5;--card:#fff;--ink:#1d1d1b;--mut:#666;--line:#ddd;--acc:#1a56db;--ok:#1a7f37;--bad:#c62828;--warn:#fff4cc}
@media (prefers-color-scheme:dark){:root{--bg:#161616;--card:#202020;--ink:#eee;--mut:#aaa;--line:#3a3a3a;--acc:#6ea0ff;--ok:#4cc26a;--bad:#ff7b72;--warn:#4a3f10}}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,sans-serif}
header{position:sticky;top:0;background:var(--card);border-bottom:1px solid var(--line);padding:10px 16px;z-index:5;display:flex;gap:10px;flex-wrap:wrap;align-items:center}
button,select{font:inherit;padding:8px 14px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);cursor:pointer;min-height:44px}button.p{background:var(--acc);color:#fff;border-color:var(--acc)}
main{max-width:1000px;margin:0 auto;padding:16px}section{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:0 0 20px}
h2{margin:0 0 8px;font-size:18px}.mut{color:var(--mut);font-size:14px}.chip{display:inline-block;padding:2px 10px;border-radius:99px;font-size:13px;border:1px solid var(--line);margin:2px 6px 2px 0}
.note{background:var(--warn);padding:6px 12px;border-radius:8px;margin:6px 0;font-size:14px}.box{border:1px solid var(--line);border-radius:8px;padding:8px 12px;margin:8px 0}.box h3{margin:0 0 4px;font-size:14px;color:var(--mut)}
label.o{display:block;padding:8px 4px;min-height:44px;box-sizing:border-box}textarea{width:100%;box-sizing:border-box;min-height:60px;font:inherit;padding:8px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink)}
ul.op{margin:4px 0;padding-left:20px}#st{font-size:14px}.ok{color:var(--ok)}.bad{color:var(--bad)}details summary{cursor:pointer;color:var(--acc)}</style></head><body>
<header><strong>Duyệt câu đề mơ hồ</strong><select id="f"><option value="">Tất cả</option><option value="doi">Đổi đáp án</option><option value="hoi">Cần thầy quyết</option><option value="an">Nên ẩn</option><option value="sua">Lời giải cần sửa</option></select>
<button class="p" id="pick">Chọn file lưu (phan-hoi.json)</button><button id="dl">Tải JSON</button><span id="st" class="mut"></span></header><main id="m"></main>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script><script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js"></script>
<script>
const D=${json};const KEY="duyet-"+D.batch;let fh=null,state={};try{state=JSON.parse(localStorage.getItem(KEY)||"{}")}catch(e){}
const esc=s=>String(s??"").replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
const LOAI={doi:["Sonnet: đáp án DB sai","bad"],hoi:["Sonnet không chắc, cần thầy quyết","bad"],an:["Sonnet đề nghị ẩn câu","bad"],sua:["Ghi được nếu sửa lời giải","ok"]};
const ACT=[["ghi","Ghi lời giải mới như hiện tại"],["doi_dap_an","Đổi đáp án DB theo Sonnet + ghi lời giải mới"],["an","Ẩn câu khỏi ngân hàng"],["sua_tay","Tôi sẽ sửa tay / yêu cầu sửa (ghi ở ô dưới)"],["giu","Không đổi gì"]];
const fmt=a=>a==null?"—":Array.isArray(a)?a.map((v,i)=>"abcd"[i]+") "+(v?"Đ":"S")).join(" · "):String(a);
function stem(q){let h="<div>"+(q.question||"")+"</div>";if(q.options)h+='<ul class="op">'+q.options.map((o,i)=>"<li>"+"ABCD"[i]+". "+o+"</li>").join("")+"</ul>";
 if(q.statements)h+='<ul class="op">'+q.statements.map((s,i)=>"<li>"+"abcd"[i]+") "+s.text+"</li>").join("")+"</ul>";return h}
const m=document.getElementById("m");
function draw(){const f=document.getElementById("f").value;m.innerHTML=D.rows.filter(r=>!f||r.loai===f).map(r=>{const s=state[r.id]||{};const [lt,lc]=LOAI[r.loai]||["?",""];
 return '<section data-id="'+r.id+'"><h2>#'+r.id+' <span class="mut">lớp '+esc(r.lop)+' · '+esc(r.chu_de)+'</span></h2><span class="chip '+lc+'">'+lt+'</span>'+stem(r.q)
 +'<p><span class="chip">DB: <b>'+esc(fmt(r.db))+'</b></span><span class="chip">Sonnet tự giải: <b>'+esc(fmt(r.tuGiai))+'</b></span>'+(r.dung?'<span class="chip bad">Đáp án đúng theo Sonnet: <b>'+esc(fmt(r.dung))+'</b></span>':"")+"</p>"
 +'<div class="note">Sonnet: '+esc(r.lyDo)+"</div>"+(r.sua?'<div class="note">Cần sửa lời giải: '+esc(r.sua)+"</div>":"")+(r.ghiHaiku?'<div class="note">Haiku: '+esc(r.ghiHaiku)+"</div>":"")
 +'<details><summary>Lời giải mới (Haiku)</summary><div class="box">'+(r.exMoi||"—")+'</div></details>'
 +'<div>'+ACT.map(([v,t])=>'<label class="o"><input type="radio" name="a'+r.id+'" value="'+v+'"'+(s.action===v?" checked":"")+"> "+t+"</label>").join("")+'<textarea placeholder="Ghi chú / yêu cầu sửa (nếu có)">'+esc(s.note||"")+"</textarea></div></section>"}).join("");
 const g=()=>window.renderMathInElement?renderMathInElement(document.body,{delimiters:[{left:"$$",right:"$$",display:true},{left:"$",right:"$",display:false}],throwOnError:false}):setTimeout(g,200);g();upd()}
const st=document.getElementById("st");function upd(){st.textContent="Đã chọn "+Object.values(state).filter(x=>x.action).length+"/"+D.rows.length}
function out(){return JSON.stringify({batch:D.batch,savedAt:new Date().toISOString(),items:state},null,2)}
async function save(){try{localStorage.setItem(KEY,JSON.stringify(state))}catch(e){}upd();if(!fh)return;try{const w=await fh.createWritable();await w.write(out());await w.close();st.className="ok";st.textContent+=" · lưu "+new Date().toLocaleTimeString("vi")+" → "+fh.name}catch(e){st.className="bad";st.textContent="Lưu lỗi: "+e.message}}
m.addEventListener("input",e=>{const sec=e.target.closest("section");if(!sec)return;const id=sec.dataset.id;const o=state[id]||(state[id]={});if(e.target.type==="radio")o.action=e.target.value;else o.note=e.target.value;save()});
document.getElementById("f").onchange=draw;
document.getElementById("pick").onclick=async()=>{if(!window.showSaveFilePicker){alert("Dùng Chrome/Edge để tự lưu, hoặc bấm Tải JSON.");return}try{fh=await showSaveFilePicker({suggestedName:"phan-hoi.json",types:[{description:"JSON",accept:{"application/json":[".json"]}}]});await save()}catch(e){}};
document.getElementById("dl").onclick=()=>{const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([out()],{type:"application/json"}));a.download="phan-hoi.json";a.click()};
addEventListener("load",draw);
</script></body></html>`;
fs.mkdirSync(DIR + "duyet", { recursive: true });
fs.writeFileSync(DIR + "duyet/duyet.html", html);
const c = (l: string) => rows.filter((r) => r.loai === l).length;
console.log(`Đã ghi ${DIR}duyet/duyet.html · ${rows.length} câu (đổi ${c("doi")}, hỏi ${c("hoi")}, ẩn ${c("an")}, sửa ${c("sua")}) · ghi thẳng: ${kq.size - rows.length}`);
