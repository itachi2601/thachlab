// Áp kết quả Opus sửa câu "đề hư" (scripts/data/giai-lai/de-hu/kq-NN.json, sinh từ xuat-de-hu-opus.mts) vào ngân hàng VÀ bản sao trong exams.questions.
//   npx tsx scripts/ap-dung-de-hu-opus.mts --offline   chỉ kiểm máy
//   npx tsx scripts/ap-dung-de-hu-opus.mts             dry-run có đối chiếu DB
//   npx tsx scripts/ap-dung-de-hu-opus.mts --apply     sinh scripts/data/giai-lai/de-hu/sql/chunk-NN.sql (mỗi chunk một giao dịch: tắt trigger exams→ngân hàng,
//   cập nhật ngân hàng + MỌI bản sao đề, đặt lại content_hash) và sao lưu bản gốc; chạy file bằng: supabase db query --linked -f <file>
import fs from "node:fs";
import { plain, katexLoi, dbAnswer, tachMuiTen, loiMuiTen, hasImg } from "./lib/giai-lai-chung.mts";
const APPLY = process.argv.includes("--apply"), OFF = process.argv.includes("--offline");
const DIR = "scripts/data/giai-lai/de-hu/";
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
  const { data, error } = await sb.from("question_bank").select("id,archived,note,content_hash,question").in("id", ids.slice(i, i + 200));
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
import { execSync } from "node:child_process";
execSync("supabase db query --linked -f scripts/data/gon-ngan-hang/in-use.sql -o json > scripts/data/gon-ngan-hang/in-use.raw 2>/dev/null", { shell: "/bin/bash" });
const raw = fs.readFileSync("scripts/data/gon-ngan-hang/in-use.raw", "utf8"); const byHash = new Map<string, { exam: number; idx: number }[]>();
for (const r of JSON.parse(raw.slice(raw.indexOf("{"), raw.lastIndexOf("}") + 1)).rows) (byHash.get(r.h) ?? byHash.set(r.h, []).get(r.h)!).push({ exam: r.exam_id, idx: r.idx });
const exCache = new Map<number, any[]>(); const exOf = async (id: number) => { if (!exCache.has(id)) { const { data, error } = await sb.from("exams").select("questions").eq("id", id).single(); if (error) throw error; exCache.set(id, data!.questions); } return exCache.get(id)!; };
const items: any[] = [], an: any[] = [], bk: any[] = [];
for (const v of viec) {
  const r = cur.get(v.id);
  if (v.patch.archived) { an.push({ id: v.id, note: v.patch.note }); bk.push({ id: v.id, archived: r.archived, note: r.note }); continue; }
  const ex: any[] = [];
  for (const u of byHash.get(r.content_hash ?? "") ?? []) { const el = (await exOf(u.exam))[u.idx]; if (el) ex.push({ exam: u.exam, idx: u.idx, el: { ...el, ...v.patch.question } }); }
  items.push({ id: v.id, nq: v.patch.question, note: v.patch.note, ex }); bk.push({ id: v.id, question: r.question, note: r.note, ex: ex.map((e) => ({ exam: e.exam, idx: e.idx, el_cu: undefined })) });
}
const SQ = DIR + "sql/"; fs.mkdirSync(SQ, { recursive: true });
fs.writeFileSync(DIR + `backup-ap-dung-${Date.now()}.json`, JSON.stringify(bk));
const tag = (p: string) => { let t = "j"; while (p.includes("$" + t + "$")) t += "x"; return "$" + t + "$"; };
for (let i = 0, n = 1; i < items.length; i += 100, n++) { const p = JSON.stringify(items.slice(i, i + 100)); const t = tag(p);
  fs.writeFileSync(SQ + `chunk-${String(n).padStart(2, "0")}.sql`, `begin;\nalter table public.exams disable trigger trg_exams_sync_bank;\ndo $do$ declare r jsonb; e jsonb; h text; begin\n  for r in select * from jsonb_array_elements(${t}${p}${t}::jsonb) loop\n    h := public.question_content_hash(r->'nq');\n    if exists (select 1 from public.question_bank where content_hash = h and id <> (r->>'id')::bigint) then raise notice 'TRUNG %', r->>'id'; continue; end if;\n    update public.question_bank set question = r->'nq', content_hash = h, note = coalesce(r->>'note', note), lint_flags = '{}', updated_at = now() where id = (r->>'id')::bigint;\n    for e in select * from jsonb_array_elements(r->'ex') loop\n      update public.exams set questions = jsonb_set(questions, array[e->>'idx'], e->'el') where id = (e->>'exam')::bigint;\n    end loop;\n  end loop;\nend $do$;\nalter table public.exams enable trigger trg_exams_sync_bank;\ncommit;\n`); }
if (an.length) fs.writeFileSync(SQ + "an.sql", "begin;\n" + an.map((x) => `update public.question_bank set archived = true, note = ${"$q$" + x.note + "$q$"} where id = ${x.id};`).join("\n") + "\ncommit;\n");
console.log(`đã sinh ${Math.ceil(items.length / 100)} chunk (${items.length} câu, ${items.reduce((s, x) => s + x.ex.length, 0)} bản sao đề) + an.sql (${an.length} câu ẩn) trong ${SQ}`);
