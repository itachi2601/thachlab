// Gom câu ngân hàng có BẢNG DỮ LIỆU bị dồn thành một dòng chữ (không có TAB, không có <table>) và dựng trang duyệt
// scripts/data/bang-ngan-hang/duyet.html (cùng kiểu so-sanh.html của hình): bên trái đề hiện tại, bên phải bảng đề xuất
// (sửa được), chọn Dùng / Sửa / Bỏ, rồi "Xuất quyết định" → dán vào quyet-dinh.json. CHỈ ĐỌC, không ghi DB.
//   npx tsx scripts/lap-duyet-bang-ngan-hang.mts
// Hai dạng còn lại (dòng có TAB, \begin{tabular}) đã được lib/question-table.ts dựng bảng lúc hiển thị — chỉ đếm.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const out = path.join(dir, "data", "bang-ngan-hang");
const env = (k: string) => process.env[k] ?? fs.readFileSync(path.resolve(dir, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });

const rows: any[] = [];
for (let from = 0; ; from += 1000) {
  const { data, error } = await sb.from("question_bank").select("id, grade, topic_name, question").eq("archived", false).order("id").range(from, from + 999);
  if (error) { console.error(error.message); process.exit(1); }
  if (!data?.length) break;
  rows.push(...data);
}

// token: giữ $…$ nguyên khối
const tokenize = (s: string) => s.match(/\$[^$]*\$|\S+/g) ?? [];
const NUMTOK = /^(?:[-−–]?\d+(?:[.,]\d+)?(?:∘C|°C|\^?0C|%)?|\$\s*[-−–]?\s*\d+(?:[.,]\d+)?\s*(?:\^?\{?\\?circ\}?\s*C?|[A-Za-z]{0,2})\s*\$|\$?\(?\^?\{?\\circ\}?\s*C\)?\$?)$/;
const isNum = (t: string) => NUMTOK.test(t);
const KEY = /bảng|số liệu|như sau|ghi lại|kết quả đo|cho ở/i;

type Cand = { id: number; grade: string; topic: string; before: string; span: string; after: string; rows: string[][]; kind: string };
const cands: Cand[] = [];
let nTab = 0, nTabular = 0, nTable = 0;
for (const r of rows) {
  const q: string = r.question?.question ?? "";
  if (/<table/i.test(q)) { nTable++; continue; }
  if (/\\begin\{tabular\}/.test(q)) { nTabular++; continue; }
  if (q.includes("\t")) { nTab++; continue; }
  const plain = q.replace(/<(?!br\s*\/?>)[^>]+>/gi, "");
  if (/<br\s*\/?>/i.test(plain) && plain.split(/<br\s*\/?>/i).some((l) => l.trim() && tokenize(l).filter(isNum).length >= 4 && tokenize(l).length <= 24)) {
    // mỗi dòng <br> là một hàng nhưng ô cách bằng dấu cách — vẫn thuộc nhóm cần duyệt
  }
  const toks = tokenize(plain.replace(/<br\s*\/?>/gi, " ⏎ "));
  // tìm cụm số liên tiếp dài nhất (cho phép ⏎ xen giữa)
  let best: [number, number] | null = null;
  for (let i = 0; i < toks.length; ) {
    if (!isNum(toks[i])) { i++; continue; }
    let j = i, cnt = 0;
    while (j < toks.length && (isNum(toks[j]) || toks[j] === "⏎" || (toks[j].length <= 3 && /^[^\d\s$]+$/.test(toks[j]) && j + 1 < toks.length && isNum(toks[j + 1])))) { if (isNum(toks[j])) cnt++; j++; }
    if (cnt >= 3 && (!best || cnt > best[1] - best[0])) best = [i, j];
    i = j + 1;
  }
  if (!best) continue;
  const numCnt = toks.slice(best[0], best[1]).filter(isNum).length;
  const hasKey = KEY.test(plain);
  if (!(numCnt >= 5 || (numCnt >= 3 && hasKey))) continue;
  // lùi lấy tối đa 4 token nhãn trước cụm số (dừng ở dấu câu kết thúc / ⏎)
  let s = best[0]; let back = 0;
  while (s > 0 && back < 5 && !/[.:?!]$/.test(toks[s - 1]) && toks[s - 1] !== "⏎") { s--; back++; }
  // rút bớt: bỏ các từ dẫn quá dài về trước nếu có "bảng"
  const bangIdx = toks.slice(s, best[0]).findIndex((t) => /^bảng/i.test(t));
  if (bangIdx > 0) s += bangIdx + 1;
  // gom hàng: tách tại chỗ chuyển từ cụm số → nhãn chữ (≥1 token chữ) rồi lại số
  const seg = toks.slice(s, best[1]);
  const rowsOut: string[][] = [];
  let cur: string[] = [];
  let label: string[] = [];
  let seenNum = false;
  const flush = () => { if (cur.length) rowsOut.push(cur); cur = []; };
  for (const t of seg) {
    if (t === "⏎") { flush(); label = []; seenNum = false; continue; }
    if (isNum(t)) { if (!cur.length && label.length) { cur.push(label.join(" ")); label = []; } if (!cur.length) cur.push(""); cur.push(t); seenNum = true; }
    else {
      if (seenNum) { flush(); seenNum = false; label = []; }
      label.push(t);
    }
  }
  if (label.length && !cur.length) rowsOut.push([label.join(" ")]); else flush();
  // Dạng "t (s) x (cm) O 20 10 … " : K nhãn đứng liền trước, dãy số chung → chia đều K hàng.
  const firstNum = seg.findIndex((t) => isNum(t) || /^[OoΟ]$/.test(t));
  const labs: string[] = [];
  for (const t of seg.slice(0, Math.max(firstNum, 0))) { if (/^\(|^\$?\(/.test(t) && labs.length) labs[labs.length - 1] += " " + t; else labs.push(t); }
  const vals = seg.slice(Math.max(firstNum, 0)).filter((t) => t !== "⏎");
  if (labs.length >= 2 && vals.length % labs.length === 0 && vals.every((t) => isNum(t) || /^[OoΟ]$/.test(t))) {
    const per = vals.length / labs.length;
    rowsOut.length = 0;
    labs.forEach((l, k) => rowsOut.push([l, ...vals.slice(k * per, (k + 1) * per).map((t) => (/^[OoΟ]$/.test(t) ? "0" : t))]));
  }
  const spanText = seg.join(" ").replace(/ ⏎ /g, " ");
  const bi = plain.replace(/<br\s*\/?>/gi, " ").indexOf(spanText);
  const flat = plain.replace(/<br\s*\/?>/gi, " ");
  cands.push({
    id: r.id, grade: r.grade, topic: r.topic_name ?? "",
    before: bi >= 0 ? flat.slice(0, bi) : flat, span: spanText, after: bi >= 0 ? flat.slice(bi + spanText.length) : "",
    rows: rowsOut.filter((x) => x.length > 1), kind: hasKey ? "co-tu-khoa" : "chi-co-so",
  });
}
fs.mkdirSync(out, { recursive: true });
fs.writeFileSync(path.join(out, "ung-vien.json"), JSON.stringify(cands, null, 1));
console.log(`Bảng đã là <table>: ${nTable} · tabular thô (tự dựng lúc hiển thị): ${nTabular} · có TAB (tự dựng lúc hiển thị): ${nTab} · dồn dòng cần duyệt: ${cands.length}`);

const payload = JSON.stringify(cands).replace(/</g, "\\u003c");
fs.writeFileSync(path.join(out, "duyet.html"), `<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Duyệt bảng dữ liệu ngân hàng</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
<style>body{font-family:system-ui;margin:10px;color:#111;max-width:1100px}#tong{position:sticky;top:0;background:#fff;padding:8px;border-bottom:1px solid #ddd;z-index:5}
.c{border:1px solid #ddd;border-radius:8px;padding:10px;margin:10px 0;display:grid;grid-template-columns:1fr 1fr;gap:12px}.c.d{border-color:#16a34a;background:#f0fdf4}.c.s{border-color:#2563eb;background:#eff6ff}.c.b{border-color:#9ca3af;background:#f3f4f6;opacity:.7}
.t{font-size:.95em;line-height:1.5}.t mark{background:#fde68a}small{color:#666}textarea{width:100%;box-sizing:border-box;font-family:monospace;min-height:90px}
table{border-collapse:collapse;margin:6px 0}th,td{border:1px solid #64748b;padding:5px 12px;text-align:center}th{background:#e2e8f0}.nut label{margin-right:12px}@media(max-width:700px){.c{grid-template-columns:1fr}}</style>
<div id="tong"><b id="dem"></b> · <button onclick="xuat()">Xuất quyết định (JSON)</button> <span id="kq"></span><br><small>Trái: đề hiện tại (vùng vàng = chỗ máy nghĩ là bảng). Phải: ô nhập mỗi dòng một hàng, ô cách nhau bằng TAB (hoặc "|") và bảng xem trước. Đúng → Dùng; sửa ô rồi chọn Dùng; không phải bảng → Bỏ.</small></div><div id="ds"></div>
<script>
const D=${payload};const Q={};
function dung(t){return t.split(/\\n/).map(l=>l.trim()).filter(Boolean).map(l=>l.includes('\\t')?l.split('\\t'):l.split('|').map(x=>x.trim()))}
function bang(t){const r=dung(t);return '<table>'+r.map((c,i)=>'<tr>'+c.map(x=>i==0?'<th>'+x+'</th>':'<td>'+x+'</td>').join('')+'</tr>').join('')+'</table>'}
function ve(i){const c=D[i],q=Q[i];const el=document.getElementById('c'+i);el.className='c '+(q.quyet=='dung'?'d':q.quyet=='sua'?'s':q.quyet=='bo'?'b':'');document.getElementById('p'+i).innerHTML=bang(q.bang);renderMathInElement(document.getElementById('p'+i),{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false});dem()}
function dem(){const n=Object.values(Q);document.getElementById('dem').textContent=D.length+' câu · dùng '+n.filter(x=>x.quyet=='dung').length+' · sửa '+n.filter(x=>x.quyet=='sua').length+' · bỏ '+n.filter(x=>x.quyet=='bo').length+' · chưa duyệt '+n.filter(x=>!x.quyet).length}
const ds=document.getElementById('ds');
D.forEach((c,i)=>{Q[i]={id:c.id,quyet:'',bang:c.rows.map(r=>r.join('\\t')).join('\\n')};
 const e=document.createElement('div');e.id='c'+i;e.innerHTML='<div class="t"><small>#'+c.id+' · L'+c.grade+' · '+c.topic+'</small><br>'+c.before+'<mark>'+c.span+'</mark>'+c.after+'</div><div><textarea id="t'+i+'"></textarea><div class="nut"><label><input type=radio name=r'+i+' value=dung>Dùng</label><label><input type=radio name=r'+i+' value=sua>Sửa (đã chỉnh)</label><label><input type=radio name=r'+i+' value=bo>Bỏ</label></div><div id="p'+i+'"></div></div>';
 ds.appendChild(e);const ta=document.getElementById('t'+i);ta.value=Q[i].bang;
 ta.oninput=()=>{Q[i].bang=ta.value;ve(i)};e.querySelectorAll('input[type=radio]').forEach(r=>r.onchange=()=>{Q[i].quyet=r.value;ve(i)});
 const t=e.querySelector('.t');renderMathInElement(t,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false});ve(i)});
function xuat(){const o={};Object.values(Q).filter(x=>x.quyet).forEach(x=>o[x.id]={quyet:x.quyet,bang:x.bang});const s=JSON.stringify(o,null,1);navigator.clipboard&&navigator.clipboard.writeText(s);document.getElementById('kq').textContent='Đã chép '+Object.keys(o).length+' quyết định vào clipboard — dán vào scripts/data/bang-ngan-hang/quyet-dinh.json';}
</script></html>`);
console.log("→ scripts/data/bang-ngan-hang/duyet.html");
