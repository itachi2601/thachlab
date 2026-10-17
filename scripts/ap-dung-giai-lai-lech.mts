// Áp quyết định của thầy (17/10/2026) cho 394 câu Haiku lệch DB, dựa trên scripts/data/giai-lai/ket-qua2.json (lượt kiểm Sonnet 5.5):
//   db_nghi_sai (Sonnet = Haiku ≠ DB) → ĐỔI đáp án DB theo AI + dùng lời giải Sonnet
//   db_dung     (Sonnet = DB ≠ Haiku) → GIỮ đáp án DB + dùng lời giải Sonnet
//   ba_ben_khac + 8 câu parse lỗi    → ẨN khỏi ngân hàng (archived=true)
// Ghi vào question_bank VÀ mọi bản sao trùng nội dung trong exams.questions. Sao lưu ra scripts/logs/ trước khi ghi.
//   npx tsx scripts/ap-dung-giai-lai-lech.mts            dry-run (chỉ đọc)   |   --apply  ghi thật
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");
const k2: any[] = JSON.parse(fs.readFileSync("scripts/data/giai-lai/ket-qua2.json", "utf8"));
const NOTE = "17/10/2026: giải lại bằng AI";

const dung = k2.filter((x) => x.loai === "db_dung"), sai = k2.filter((x) => x.loai === "db_nghi_sai");
const bo = k2.filter((x) => x.loai === "ba_ben_khac" || x.loi);
const loiHinhThuc = [...dung, ...sai].filter((x) => x.katex_loi > 0 || x.mui_ten_con > 0);
console.log(`đổi đáp án ${sai.length} · giữ đáp án ${dung.length} · ẩn ${bo.length} · trong nhóm ghi có KaTeX lỗi/⇒ sai chỗ: ${loiHinhThuc.length}`);

const ids = k2.map((x) => x.id);
const bank = new Map<number, any>();
for (let i = 0; i < ids.length; i += 200) {
  const { data, error } = await sb.from("question_bank").select("id,question,archived,note").in("id", ids.slice(i, i + 200));
  if (error) throw new Error(error.message);
  data!.forEach((r) => bank.set(r.id, r));
}
const key = (q: any) => JSON.stringify([q.type, q.question, q.options ?? null, (q.statements ?? []).map((s: any) => s.text)]);
function moi(q: any, x: any, doiDapAn: boolean) {
  const n = structuredClone(q);
  n.explanation = x.explanation;
  if (doiDapAn) {
    if (q.type === "multiple_choice") n.answer = "ABCD".indexOf(String(x.sonnet).trim().toUpperCase().charAt(0));
    else if (q.type === "short_answer") n.answer = String(x.sonnet).trim();
    else n.statements = q.statements.map((s: any, i: number) => ({ ...s, answer: !!x.sonnet[i] }));
  }
  return n;
}
const thayThe = new Map<string, any>(); // key nội dung câu → câu mới (cho bản sao trong exams)
const plan: { id: number; truoc: any; sau: any }[] = [];
let boQua = 0;
for (const [list, doi] of [[dung, false], [sai, true]] as const) for (const x of list) {
  const r = bank.get(x.id); if (!r) { boQua++; continue; }
  if (x.katex_loi > 0 || x.mui_ten_con > 0) { boQua++; continue; } // lời giải hỏng định dạng → không ghi, báo riêng
  const sau = moi(r.question, x, doi);
  if (doi && ((x.type === "multiple_choice" && sau.answer < 0) || (x.type === "true_false" && !Array.isArray(x.sonnet)))) { boQua++; continue; }
  plan.push({ id: x.id, truoc: r.question, sau });
  thayThe.set(key(r.question), { sau, doi });
}
console.log(`sẽ ghi ${plan.length} câu vào ngân hàng · bỏ qua ${boQua} (định dạng hỏng/đáp án không hợp lệ)`);

// quét exams
const exams: any[] = [];
for (let o = 0; ; o += 100) {
  const { data, error } = await sb.from("exams").select("id,questions").order("id").range(o, o + 99);
  if (error) throw new Error(error.message);
  exams.push(...data!); if (data!.length < 100) break;
}
let banSao = 0, deDoi = 0; const examMoi = new Map<number, any[]>(); const examGoc = new Map<number, any>();
for (const e of exams) {
  if (!Array.isArray(e.questions)) continue;
  let doi = false;
  const qs = e.questions.map((q: any) => { const t = thayThe.get(key(q)); if (!t) return q; doi = true; banSao++; return { ...q, explanation: t.sau.explanation, ...(q.type === "multiple_choice" || q.type === "short_answer" ? { answer: t.sau.answer } : { statements: t.sau.statements }) }; });
  if (doi) { examMoi.set(e.id, qs); examGoc.set(e.id, e.questions); deDoi++; }
}
console.log(`bản sao trong exams: ${banSao} câu ở ${deDoi} đề`);
if (!APPLY) { console.log("dry-run xong — thêm --apply để ghi"); process.exit(0); }

const bp = `scripts/logs/giai-lai-lech-backup-${Date.now()}.json`;
fs.writeFileSync(bp, JSON.stringify({ bank: [...bank.values()].filter((r) => ids.includes(r.id)), exams: [...examGoc].map(([id, questions]) => ({ id, questions })) }));
console.log("sao lưu:", bp);
let ok = 0, loi = 0;
for (const p of plan) {
  const { error } = await sb.from("question_bank").update({ question: p.sau }).eq("id", p.id);
  if (error) { loi++; console.log("LỖI", p.id, error.message); } else ok++;
}
console.log(`ngân hàng: ghi ${ok}, lỗi ${loi}`);
let okE = 0;
for (const [id, qs] of examMoi) { const { error } = await sb.from("exams").update({ questions: qs }).eq("id", id); if (error) console.log("LỖI đề", id, error.message); else okE++; }
console.log(`exams: ghi ${okE}/${examMoi.size} đề`);
let an = 0;
for (const x of bo) {
  const r = bank.get(x.id); if (!r) continue;
  const { error } = await sb.from("question_bank").update({ archived: true, note: r.note ? `${r.note} · ${NOTE}: bất đồng, ẩn` : `${NOTE}: bất đồng, ẩn` }).eq("id", x.id);
  if (error) console.log("LỖI ẩn", x.id, error.message); else an++;
}
console.log(`đã ẩn ${an}/${bo.length} câu`);
