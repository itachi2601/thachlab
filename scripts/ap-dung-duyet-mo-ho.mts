// Áp dụng phản hồi của thầy trên trang duyệt câu mơ hồ (scripts/data/giai-lai/mo-ho/duyet/duyet.html → phan-hoi.json) vào question_bank. KHÔNG đụng exams.
//   npx tsx scripts/ap-dung-duyet-mo-ho.mts [đường-dẫn/phan-hoi.json]            dry-run (mặc định đọc scripts/data/giai-lai/mo-ho/duyet/phan-hoi.json)
//   npx tsx scripts/ap-dung-duyet-mo-ho.mts [đường-dẫn/phan-hoi.json] --apply    ghi thật, sao lưu scripts/logs/duyet-mo-ho-backup-*.json
// Hành động: ghi = ghi lời giải mới | doi_dap_an = đổi đáp án theo Sonnet (KHÔNG ghi lời giải cũ vì viết cho đáp án khác, câu vào danh sách cần lời giải mới)
//            an = archived=true | sua_tay, giu = không đổi (sua_tay in ghi chú của thầy ra file để xử lý riêng).
// Bỏ qua câu có đáp án trong DB đã khác lúc soát (có người sửa), hoặc đã có lời giải ≥80 ký tự khi ghi.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import { plain, katexLoi, dbAnswer } from "./lib/giai-lai-chung.mts";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");
const DIR = "scripts/data/giai-lai/mo-ho/";
const file = process.argv.slice(2).find((a) => !a.startsWith("--")) ?? DIR + "duyet/phan-hoi.json";
const ph: Record<string, { action?: string; note?: string }> = JSON.parse(fs.readFileSync(file, "utf8")).items ?? {};
const ls = fs.readdirSync(DIR), rd = (f: string) => JSON.parse(fs.readFileSync(DIR + f, "utf8")) as any[];
const src = new Map<number, any>(), kq = new Map<number, any>();
for (const f of ls.filter((f) => /^lo-\d+\.json$/.test(f))) rd(f).forEach((x) => src.set(x.id, x));
for (const f of ls.filter((f) => /^kq-\d+\.json$/.test(f))) rd(f).forEach((x) => kq.set(x.id, x));
if (ls.includes("kq-08b.json")) rd("kq-08b.json").forEach((x) => kq.set(x.id, x));
const lamSach = (h: string) => h.replace(/(?<!\\)\$(.+?)(?<!\\)\$/gs, (_m, t: string) => "$" + t.replace(/</g, "\\lt ").replace(/>/g, "\\gt ") + "$");
const eq = (a: any, b: any) => JSON.stringify(a) === JSON.stringify(b);
const parseDung = (type: string, d: any): any => {
  const s = String(d ?? "").trim(); if (!s) return null;
  if (type === "multiple_choice") return /^[A-D]/i.test(s) ? s.charAt(0).toUpperCase() : null;
  if (type === "true_false") { const m = [...s.matchAll(/([a-d])\s*[:=]\s*(Đ|S|đ|s|true|false)/gi)]; if (m.length !== 4) return null; return m.sort((a, b) => a[1].localeCompare(b[1])).map((x) => /^(Đ|true)$/i.test(x[2])); }
  return s;
};
const ids = Object.keys(ph).map(Number).filter((id) => ph[id]?.action && kq.has(id));
const cur = new Map<number, any>();
for (let i = 0; i < ids.length; i += 200) {
  const { data, error } = await sb.from("question_bank").select("id,archived,note,question").in("id", ids.slice(i, i + 200));
  if (error) throw new Error(error.message);
  data!.forEach((r) => cur.set(r.id, r));
}
type Viec = { id: number; loai: "ghi" | "doi" | "an"; sau: any; archived?: boolean; note?: string };
const viec: Viec[] = []; const bo: string[] = []; const cuaThay: any[] = []; const canLoiGiai: number[] = [];
const dem: Record<string, number> = {};
for (const id of ids) {
  const a = ph[id].action!; dem[a] = (dem[a] ?? 0) + 1;
  const r = cur.get(id), s = src.get(id), k = kq.get(id);
  if (!r) { bo.push(`${id}: không thấy`); continue; }
  if (a === "giu") continue;
  if (a === "sua_tay") { cuaThay.push({ id, yeuCau: ph[id].note ?? "", sonnet: k.ly_do, sua: k.sua ?? "" }); continue; }
  if (r.archived) { bo.push(`${id}: đã ẩn`); continue; }
  const q = r.question, dbNay = dbAnswer(q), dbLuc = s.dap_an_db;
  if (!eq(dbNay, dbLuc) && !(q.type === "multiple_choice" && dbNay === dbLuc)) { bo.push(`${id}: đáp án DB đã khác lúc soát`); continue; }
  if (a === "an") { viec.push({ id, loai: "an", sau: q, archived: true, note: `18/10/2026: soát câu mơ hồ (Sonnet + thầy duyệt) — ẩn${ph[id].note ? ": " + ph[id].note : ""}` + (r.note ? " | " + r.note : "") }); continue; }
  if (a === "ghi") {
    if (plain(q.explanation).length >= 80) { bo.push(`${id}: đã có lời giải`); continue; }
    const ex = lamSach(String(s.loi_giai_moi ?? "")); if (plain(ex).length < 40 || katexLoi(ex) > 0) { bo.push(`${id}: lời giải mới rỗng/KaTeX lỗi`); continue; }
    viec.push({ id, loai: "ghi", sau: { ...q, explanation: ex } }); continue;
  }
  if (a === "doi_dap_an") {
    const dung = parseDung(q.type, k.dap_an_dung); if (dung == null) { bo.push(`${id}: Sonnet không nêu đáp án đúng đọc được ("${k.dap_an_dung ?? ""}")`); continue; }
    const n = structuredClone(q);
    if (q.type === "multiple_choice") n.answer = "ABCD".indexOf(dung); else if (q.type === "short_answer") n.answer = dung; else (n.statements ?? []).forEach((st: any, i: number) => (st.answer = !!dung[i]));
    viec.push({ id, loai: "doi", sau: n }); canLoiGiai.push(id); continue;
  }
  bo.push(`${id}: hành động lạ "${a}"`);
}
const c = (l: string) => viec.filter((v) => v.loai === l).length;
console.log(`phản hồi ${Object.keys(ph).length} câu · theo hành động`, dem, `\nsẽ ghi lời giải ${c("ghi")} · đổi đáp án ${c("doi")} · ẩn ${c("an")} · bỏ qua ${bo.length}${bo.length ? ":\n  " + bo.join("\n  ") : ""}`);
fs.writeFileSync(DIR + "duyet/viec-con-lai.json", JSON.stringify({ suaTay: cuaThay, canLoiGiaiMoi: canLoiGiai, boQua: bo }, null, 1));
console.log(`việc thầy để tự sửa ${cuaThay.length}, đổi đáp án cần lời giải mới ${canLoiGiai.length} → ${DIR}duyet/viec-con-lai.json`);
if (!APPLY) { console.log("dry-run xong — thêm --apply để ghi"); process.exit(0); }
const bp = `scripts/logs/duyet-mo-ho-backup-${Date.now()}.json`;
fs.writeFileSync(bp, JSON.stringify(viec.map((v) => ({ id: v.id, archived: cur.get(v.id).archived, note: cur.get(v.id).note, question: cur.get(v.id).question })))); console.log("sao lưu:", bp);
let ok = 0, loi = 0;
for (const v of viec) {
  const patch: any = { question: v.sau }; if (v.archived) { patch.archived = true; patch.note = v.note; }
  const { error } = await sb.from("question_bank").update(patch).eq("id", v.id);
  if (error) { loi++; console.log("LỖI", v.id, error.message); } else ok++;
}
console.log(`đã ghi ${ok}, lỗi ${loi}`);
