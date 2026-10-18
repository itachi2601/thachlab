// Áp kết quả Opus soát lại 214 câu "đề mơ hồ" (scripts/data/giai-lai/mo-ho/opus/kq-NN.json, sinh từ xuat-mo-ho-opus.mts) vào question_bank. KHÔNG đụng exams.
//   npx tsx scripts/ap-dung-mo-ho-opus.mts --offline   chỉ kiểm máy file kq (không cần mạng) → opus/kiem-may.json
//   npx tsx scripts/ap-dung-mo-ho-opus.mts             dry-run có đối chiếu DB
//   npx tsx scripts/ap-dung-mo-ho-opus.mts --apply     ghi thật, sao lưu scripts/logs/mo-ho-opus-backup-*.json
// kl: ghi (chỉ đổi explanation) | sua_de (đổi đề/phương án/đáp án + lời giải) | doi_dap_an | an (archived=true) | hoi (không ghi, in ra opus/hoi-thay.json).
// Bỏ qua câu mà đáp án DB đã khác lúc xuất lô (có người sửa sau), câu đã ẩn, hoặc kq không qua kiểm máy.
import fs from "node:fs";
import { plain, katexLoi, dbAnswer, tachMuiTen, loiMuiTen, hasImg } from "./lib/giai-lai-chung.mts";
const APPLY = process.argv.includes("--apply"), OFF = process.argv.includes("--offline");
const DIR = "scripts/data/giai-lai/mo-ho/opus/";
const ls = fs.readdirSync(DIR), rd = (f: string) => JSON.parse(fs.readFileSync(DIR + f, "utf8")) as any[];
const src = new Map<number, any>(), kq = new Map<number, any>();
for (const f of ls.filter((f) => /^lo-\d+\.json$/.test(f))) rd(f).forEach((x) => src.set(x.id, x));
for (const f of ls.filter((f) => /^kq-\d+\.json$/.test(f))) rd(f).forEach((x) => kq.set(x.id, x));
const eq = (a: any, b: any) => JSON.stringify(a) === JSON.stringify(b);
const lamSach = (h: string) => h.replace(/(?<!\\)\$(.+?)(?<!\\)\$/gs, (_m, t: string) => "$" + t.replace(/</g, "\\lt ").replace(/>/g, "\\gt ") + "$");
const chuDe = (q: any) => [q.question, ...(q.options ?? []), ...(q.statements ?? []).map((s: any) => s.text)].join(" ");

const thieu = [...src.keys()].filter((id) => !kq.has(id));
const loiKiem: string[] = []; const sach = new Map<number, any>(); const dem: Record<string, number> = {};
for (const [id, k] of kq) {
  const s = src.get(id); if (!s) { loiKiem.push(`${id}: không có trong lô`); continue; }
  dem[k.kl] = (dem[k.kl] ?? 0) + 1;
  if (!["ghi", "sua_de", "doi_dap_an", "an", "hoi"].includes(k.kl)) { loiKiem.push(`${id}: kl lạ "${k.kl}"`); continue; }
  if (!String(k.ly_do ?? "").trim()) loiKiem.push(`${id}: thiếu ly_do`);
  if (k.kl === "an" || k.kl === "hoi") { sach.set(id, null); continue; }
  const o = s.cau_hoi, n = structuredClone(k.cau_hoi_moi);
  if (!n || typeof n !== "object") { loiKiem.push(`${id}: thiếu cau_hoi_moi`); continue; }
  const e: string[] = [];
  if (n.type !== o.type) e.push("đổi type");
  for (const key of Object.keys(o)) if (!(key in n)) e.push(`mất khoá ${key}`);
  n.explanation = tachMuiTen(lamSach(String(n.explanation ?? "")));
  if (plain(n.explanation).length < 40) e.push("lời giải quá ngắn");
  if (katexLoi(n.explanation) > 0) e.push(`KaTeX lời giải lỗi ${katexLoi(n.explanation)}`);
  if (loiMuiTen(n.explanation) > 0) e.push("⇒ sai chỗ");
  if (katexLoi(chuDe(n)) > 0) e.push("KaTeX đề lỗi");
  if (hasImg(n) && !hasImg(o)) e.push("thêm ảnh");
  if (n.type === "multiple_choice" && !(Number.isInteger(n.answer) && n.answer >= 0 && n.answer <= 3 && n.options?.length === 4)) e.push("answer/options trắc nghiệm sai dạng");
  if (n.type === "true_false" && !(n.statements?.length === 4 && n.statements.every((x: any) => typeof x.answer === "boolean"))) e.push("statements đúng–sai sai dạng");
  if (n.type === "short_answer" && !String(n.answer ?? "").trim()) e.push("thiếu đáp số");
  const giongCu = eq({ ...n, explanation: "" }, { ...o, explanation: "" });
  if (k.kl === "ghi" && !giongCu) e.push("kl=ghi nhưng đổi ngoài explanation");
  if (k.kl !== "ghi" && giongCu) e.push(`kl=${k.kl} nhưng không đổi gì ngoài lời giải`);
  if (k.kl === "doi_dap_an" && eq(dbAnswer(n), dbAnswer(o))) e.push("doi_dap_an nhưng đáp án như cũ");
  if (e.length) { loiKiem.push(`${id}: ${e.join("; ")}`); continue; }
  sach.set(id, n);
}
fs.writeFileSync(DIR + "kiem-may.json", JSON.stringify({ dem, thieu, loiKiem }, null, 1));
console.log(`kq ${kq.size}/${src.size} câu · theo kl`, dem, `\nthiếu ${thieu.length} · lỗi kiểm máy ${loiKiem.length}${loiKiem.length ? ":\n  " + loiKiem.join("\n  ") : ""}`);
fs.writeFileSync(DIR + "hoi-thay.json", JSON.stringify([...kq.values()].filter((k) => k.kl === "hoi").map((k) => ({ id: k.id, ly_do: k.ly_do, cau_hoi: src.get(k.id)?.cau_hoi })), null, 1));
if (OFF) process.exit(0);

const { createClient } = await import("@supabase/supabase-js");
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
// giu-lai.json: id dò lần 2 (kiem-code) chưa cho qua hoặc có số liệu tự dựng → chờ thầy duyệt, không ghi
const GIU: number[] = fs.existsSync(DIR + "giu-lai.json") ? JSON.parse(fs.readFileSync(DIR + "giu-lai.json", "utf8")) : [];
const ids = [...sach.keys()].filter((id) => kq.get(id).kl !== "hoi" && !GIU.includes(id));
console.log(`giữ lại chờ thầy: ${GIU.length}`);
const cur = new Map<number, any>();
for (let i = 0; i < ids.length; i += 200) {
  const { data, error } = await sb.from("question_bank").select("id,archived,note,question").in("id", ids.slice(i, i + 200));
  if (error) throw new Error(error.message);
  data!.forEach((r) => cur.set(r.id, r));
}
const viec: { id: number; patch: any }[] = []; const bo: string[] = []; const doiSoVoiDb: string[] = [];
for (const id of ids) {
  const r = cur.get(id), k = kq.get(id), s = src.get(id);
  if (!r) { bo.push(`${id}: không thấy`); continue; }
  if (r.archived) { bo.push(`${id}: đã ẩn`); continue; }
  const dbNay = dbAnswer(r.question); // lô xuất lúc cau_hoi.answer và dap_an_db có thể lệch (sự cố trigger) → nhận một trong hai
  if (!eq(dbNay, dbAnswer(s.cau_hoi)) && !eq(dbNay, s.dap_an_db)) { bo.push(`${id}: đáp án DB đã khác lúc xuất lô`); continue; }
  if (k.kl === "an") { viec.push({ id, patch: { archived: true, note: `18/10/2026: soát câu mơ hồ (Opus) — ẩn: ${k.ly_do}` + (r.note ? " | " + r.note : "") } }); continue; }
  const note = k.kl === "ghi" ? r.note : `18/10/2026: Opus ${k.kl === "sua_de" ? "sửa đề" : "đổi đáp án"}: ${k.thay_doi ?? k.ly_do}` + (r.note ? " | " + r.note : "");
  if (k.kl === "ghi" && !eq(dbNay, dbAnswer(sach.get(id)))) { bo.push(`${id}: kl=ghi nhưng đáp án DB hiện tại khác đáp án trong kq`); continue; }
  if (!eq(dbNay, dbAnswer(sach.get(id)))) doiSoVoiDb.push(`${id} (${k.kl}): ${JSON.stringify(dbNay)} → ${JSON.stringify(dbAnswer(sach.get(id)))}`);
  viec.push({ id, patch: { question: sach.get(id), note } });
}
const c = (l: string) => viec.filter((v) => kq.get(v.id).kl === l).length;
console.log(`sẽ ghi: lời giải ${c("ghi")} · sửa đề ${c("sua_de")} · đổi đáp án ${c("doi_dap_an")} · ẩn ${c("an")} · bỏ qua ${bo.length}${bo.length ? ":\n  " + bo.join("\n  ") : ""}`);
console.log(`đáp án khác DB hiện tại: ${doiSoVoiDb.length}\n  ` + doiSoVoiDb.join("\n  "));
if (!APPLY) { console.log("dry-run xong — thêm --apply để ghi"); process.exit(0); }
const bp = `scripts/logs/mo-ho-opus-backup-${Date.now()}.json`;
fs.writeFileSync(bp, JSON.stringify(viec.map((v) => ({ id: v.id, archived: cur.get(v.id).archived, note: cur.get(v.id).note, question: cur.get(v.id).question })))); console.log("sao lưu:", bp);
let ok = 0, loi = 0;
for (const v of viec) {
  const { error } = await sb.from("question_bank").update(v.patch).eq("id", v.id);
  if (error) { loi++; console.log("LỖI", v.id, error.message); } else ok++;
}
console.log(`đã ghi ${ok}, lỗi ${loi}`);
