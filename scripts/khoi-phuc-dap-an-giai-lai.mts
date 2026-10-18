// ⚠ ĐÃ DÙNG XONG 18/10/2026 — mốc "trước" trong ket-qua.json đã cũ, câu nào còn khác mốc là do sửa có chủ ý. KHÔNG chạy --apply nữa; cần trả câu lẻ về sao lưu thì dùng scripts/khoi-phuc-tu-sao-luu-ids.mts.
// Khôi phục đáp án ngân hàng bị ghi đè nhầm khi ap-dung-giai-lai-khop.mts cập nhật exams.questions (17/10/2026 ~16:30–… UTC):
// trigger đồng bộ exams → question_bank đã chép đáp án CŨ trong bản sao đề đè lên đáp án ngân hàng của mọi câu nằm trong đề được ghi.
// Mốc "trước" = trường db trong scripts/data/giai-lai/ket-qua.json (đáp án ngân hàng trước khi chạy). Chỉ sửa câu có updated_at >= TU và đáp án khác mốc.
//   npx tsx scripts/khoi-phuc-dap-an-giai-lai.mts           dry-run (ghi scripts/data/giai-lai/khoi-phuc-ds.json)
//   npx tsx scripts/khoi-phuc-dap-an-giai-lai.mts --apply   ghi thật, sao lưu scripts/logs/khoi-phuc-dap-an-backup-*.json
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import { dbAnswer } from "./lib/giai-lai-chung.mts";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");
const TU = "2026-10-17T16:00:00Z";
// nhóm "DB nghi sai" đã đổi đáp án có chủ ý theo AI (ap-dung-giai-lai-lech): đích = đáp án Sonnet, KHÔNG so với mốc cũ ở vòng 1
const k2: any[] = JSON.parse(fs.readFileSync("scripts/data/giai-lai/ket-qua2.json", "utf8")).filter((x: any) => x.loai === "db_nghi_sai" && x.sonnet != null);
const idK2 = new Set(k2.map((x) => x.id));
const k: any[] = JSON.parse(fs.readFileSync("scripts/data/giai-lai/ket-qua.json", "utf8")).filter((x: any) => x.db !== undefined && !idK2.has(x.id));
const cur = new Map<number, any>();
for (let i = 0; i < k.length; i += 200) {
  const { data, error } = await sb.from("question_bank").select("id,updated_at,question").in("id", k.slice(i, i + 200).map((x) => x.id));
  if (error) throw new Error(error.message);
  data!.forEach((r) => cur.set(r.id, r));
}
const eq = (a: any, b: any) => JSON.stringify(a) === JSON.stringify(b);
const saiRaw: { id: number; type: string; truoc: any; nay: any }[] = [];
for (const x of k) {
  const r = cur.get(x.id); if (!r || r.updated_at < TU) continue;
  const nay = dbAnswer(r.question);
  if (!eq(nay, x.db)) saiRaw.push({ id: x.id, type: r.question.type, truoc: x.db, nay });
}
// nếu trigger chép ngược nhóm DB-nghi-sai về cũ thì đưa về đích Sonnet
const cur2 = new Map<number, any>();
for (let i = 0; i < k2.length; i += 200) {
  const { data, error } = await sb.from("question_bank").select("id,updated_at,archived,question").in("id", k2.slice(i, i + 200).map((x) => x.id));
  if (error) throw new Error(error.message);
  data!.forEach((r) => cur2.set(r.id, r));
}
let lechQuayVe = 0;
for (const x of k2) {
  const r = cur2.get(x.id); if (!r || r.archived) continue;
  const nay = dbAnswer(r.question);
  if (!eq(nay, x.sonnet) && !(r.question.type === "multiple_choice" && String(x.sonnet).charAt(0) === nay)) { lechQuayVe++; cur.set(x.id, r); saiRaw.push({ id: x.id, type: r.question.type, truoc: r.question.type === "multiple_choice" ? String(x.sonnet).charAt(0) : x.sonnet, nay }); }
}
// câu kiểu dữ liệu lẫn lộn (short_answer mang đáp án ĐĐSS / mảng) — không tự khôi phục, để thầy xem tay
const BO = new Set([680966, 680967, 683068, 1225216, 384253, 425260]);
const sai = saiRaw.filter((s) => !BO.has(s.id));
const dem: Record<string, number> = {}; sai.forEach((s) => (dem[s.type] = (dem[s.type] ?? 0) + 1));
console.log(`cần khôi phục ${sai.length} câu`, dem, `· trong đó nhóm DB-nghi-sai (đã đổi có chủ ý) nay lệch đích: ${lechQuayVe}`);
fs.writeFileSync("scripts/data/giai-lai/khoi-phuc-ds.json", JSON.stringify(sai));
if (!APPLY) { console.log("dry-run xong — thêm --apply để ghi"); process.exit(0); }
const bp = `scripts/logs/khoi-phuc-dap-an-backup-${Date.now()}.json`;
fs.writeFileSync(bp, JSON.stringify(sai.map((s) => ({ id: s.id, question: cur.get(s.id).question }))));
console.log("sao lưu:", bp);
let ok = 0, loi = 0;
for (const s of sai) {
  const q = structuredClone(cur.get(s.id).question);
  if (q.type === "multiple_choice") q.answer = "ABCD".indexOf(s.truoc);
  else if (q.type === "short_answer") q.answer = s.truoc;
  else (q.statements ?? []).forEach((st: any, i: number) => (st.answer = !!s.truoc[i]));
  const { error } = await sb.from("question_bank").update({ question: q }).eq("id", s.id);
  if (error) { loi++; console.log("LỖI", s.id, error.message); } else ok++;
}
console.log(`đã khôi phục ${ok}, lỗi ${loi}`);
