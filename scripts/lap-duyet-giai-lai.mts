// Dựng trang HTML duyệt các câu mà Haiku lệch đáp án DB, kèm kết luận của Sonnet 5.5 (lượt kiểm thứ hai).
//   npx tsx scripts/lap-duyet-giai-lai.mts      đọc scripts/data/giai-lai/ket-qua.json + ket-qua2.json → scripts/data/giai-lai/duyet-lech/duyet.html
// Trang tự lưu ra file (Chrome/Edge: bấm "Chọn file lưu" một lần), thầy lưu thành phan-hoi.json cùng thư mục.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const DIR = "scripts/data/giai-lai/";
const k1 = new Map((JSON.parse(fs.readFileSync(DIR + "ket-qua.json", "utf8")) as any[]).map((x) => [x.id, x]));
const k2: any[] = JSON.parse(fs.readFileSync(DIR + "ket-qua2.json", "utf8"));
const ids = k2.map((x) => x.id);
const qs = new Map<number, any>();
for (let i = 0; i < ids.length; i += 200) {
  const { data, error } = await sb.from("question_bank").select("id,grade,topic_name,question").in("id", ids.slice(i, i + 200));
  if (error) throw new Error(error.message);
  data!.forEach((r) => qs.set(r.id, r));
}
const ORDER: Record<string, number> = { db_nghi_sai: 0, ba_ben_khac: 1, db_dung: 2 };
const rows = k2.map((s) => {
  const h = k1.get(s.id), q = qs.get(s.id);
  return { id: s.id, grade: q?.grade, topic: q?.topic_name, q: q?.question, loai: s.loai ?? "loi", loi: s.loi, db: s.db, haiku: s.haiku ?? h?.answer, sonnet: s.sonnet,
    ghiHaiku: h?.ghi_chu ?? "", ghiSonnet: s.ghi_chu ?? "", exHaiku: h?.explanation ?? "", exSonnet: s.explanation ?? "", katex: s.katex_loi ?? 0 };
}).sort((a, b) => (ORDER[a.loai] ?? 9) - (ORDER[b.loai] ?? 9) || a.id - b.id);
const json = JSON.stringify({ batch: "giai-lai-lech", rows }).replace(/</g, "\\u003c");
const html = `<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Duyệt câu lệch đáp án</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">
<style>:root{--bg:#f7f7f5;--card:#fff;--ink:#1d1d1b;--mut:#666;--line:#ddd;--acc:#1a56db;--ok:#1a7f37;--bad:#c62828;--warn:#fff4cc}
@media (prefers-color-scheme:dark){:root{--bg:#161616;--card:#202020;--ink:#eee;--mut:#aaa;--line:#3a3a3a;--acc:#6ea0ff;--ok:#4cc26a;--bad:#ff7b72;--warn:#4a3f10}}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,sans-serif}
header{position:sticky;top:0;background:var(--card);border-bottom:1px solid var(--line);padding:10px 16px;z-index:5;display:flex;gap:10px;flex-wrap:wrap;align-items:center}
button,select{font:inherit;padding:8px 14px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);cursor:pointer;min-height:44px}button.p{background:var(--acc);color:#fff;border-color:var(--acc)}
main{max-width:1000px;margin:0 auto;padding:16px}section{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:0 0 20px}
h2{margin:0 0 8px;font-size:18px}.mut{color:var(--mut);font-size:14px}.chip{display:inline-block;padding:2px 10px;border-radius:99px;font-size:13px;border:1px solid var(--line);margin:2px 6px 2px 0}
.note{background:var(--warn);padding:6px 12px;border-radius:8px;margin:6px 0;font-size:14px}.cols{display:grid;grid-template-columns:1fr 1fr;gap:14px}@media(max-width:700px){.cols{grid-template-columns:1fr}}
.box{border:1px solid var(--line);border-radius:8px;padding:8px 12px}.box h3{margin:0 0 4px;font-size:14px;color:var(--mut)}label.o{display:block;padding:8px 4px;min-height:44px;box-sizing:border-box}
textarea{width:100%;box-sizing:border-box;min-height:60px;font:inherit;padding:8px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink)}ul.op{margin:4px 0;padding-left:20px}#st{font-size:14px}.ok{color:var(--ok)}.bad{color:var(--bad)}</style></head><body>
<header><strong>Duyệt câu lệch đáp án</strong><select id="f"><option value="">Tất cả</option><option value="db_nghi_sai">DB nghi sai</option><option value="ba_ben_khac">Ba bên khác nhau</option><option value="db_dung">DB đúng</option></select>
<button class="p" id="pick">Chọn file lưu (phan-hoi.json)</button><button id="dl">Tải JSON</button><span id="st" class="mut"></span></header><main id="m"></main>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script><script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js"></script>
<script>
const D=${json};const KEY="duyet-"+D.batch;let fh=null,state={};try{state=JSON.parse(localStorage.getItem(KEY)||"{}")}catch(e){}
const esc=s=>String(s??"").replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
const LOAI={db_nghi_sai:["DB nghi sai: Sonnet trùng Haiku, lệch DB","bad"],ba_ben_khac:["Ba bên khác nhau (đề mơ hồ?)","bad"],db_dung:["DB đúng: Sonnet trùng DB, Haiku sai","ok"]};
const ACT=[["giu_dap_an","Giữ đáp án DB, dùng lời giải mới (Sonnet)"],["doi_dap_an","Đổi đáp án DB theo model + dùng lời giải mới"],["bo","Bỏ câu (ẩn khỏi ngân hàng)"],["giu","Không đổi gì"]];
const fmt=(t,a)=>a==null?"—":Array.isArray(a)?a.map((v,i)=>"abcd"[i]+") "+(v?"Đ":"S")).join(" · "):String(a);
function stem(q){let h="<div>"+(q.question||"")+"</div>";if(q.options)h+='<ul class="op">'+q.options.map((o,i)=>"<li>"+"ABCD"[i]+". "+o+"</li>").join("")+"</ul>";
 if(q.statements)h+='<ul class="op">'+q.statements.map((s,i)=>"<li>"+"abcd"[i]+") "+s.text+"</li>").join("")+"</ul>";return h}
const m=document.getElementById("m");
function draw(){const f=document.getElementById("f").value;m.innerHTML=D.rows.filter(r=>!f||r.loai===f).map(r=>{const s=state[r.id]||{};const [lt,lc]=LOAI[r.loai]||["Lỗi gọi",""];const q=r.q||{};
 return '<section data-id="'+r.id+'"><h2>#'+r.id+' <span class="mut">lớp '+esc(r.grade)+' · '+esc(r.topic)+'</span></h2><span class="chip '+lc+'">'+lt+'</span>'+stem(q)
 +'<p><span class="chip">DB: <b>'+esc(fmt(q.type,r.db))+'</b></span><span class="chip">Haiku: <b>'+esc(fmt(q.type,r.haiku))+'</b></span><span class="chip">Sonnet: <b>'+esc(fmt(q.type,r.sonnet))+'</b></span>'+(r.katex?'<span class="chip bad">KaTeX lỗi '+r.katex+'</span>':"")+"</p>"
 +(r.ghiHaiku?'<div class="note">Haiku: '+esc(r.ghiHaiku)+"</div>":"")+(r.ghiSonnet?'<div class="note">Sonnet: '+esc(r.ghiSonnet)+"</div>":"")
 +'<div class="cols"><div class="box"><h3>LỜI GIẢI SONNET 5.5</h3>'+(r.exSonnet||"—")+'</div><div class="box"><h3>LỜI GIẢI HAIKU 5.5</h3>'+(r.exHaiku||"—")+'</div></div>'
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
fs.mkdirSync(DIR + "duyet-lech", { recursive: true });
fs.writeFileSync(DIR + "duyet-lech/duyet.html", html);
const c = (l: string) => rows.filter((r) => r.loai === l).length;
console.log(`Đã ghi ${DIR}duyet-lech/duyet.html · ${rows.length} câu (DB nghi sai ${c("db_nghi_sai")}, ba bên khác ${c("ba_ben_khac")}, DB đúng ${c("db_dung")})`);
