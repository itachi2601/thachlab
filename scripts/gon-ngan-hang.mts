// Gộp câu TRÙNG trong ngân hàng bằng cách LƯU TRỮ dòng thừa (không xoá). Mặc định dry-run.
//   (1) supabase db query --linked -f scripts/data/gon-ngan-hang/in-use.sql -o json > scripts/data/gon-ngan-hang/in-use.raw
//   (2) npx tsx scripts/gon-ngan-hang.mts            → in số liệu + ghi scripts/data/gon-ngan-hang/{ke-hoach,can-duyet}.json
//   (3) npx tsx scripts/gon-ngan-hang.mts --apply    → lưu trữ dòng thừa (sao lưu scripts/logs/gon-ngan-hang-backup-*.json)
// Khoá trùng = chữ đề + chữ các phương án/ý (bỏ thẻ HTML, khoảng trắng). Nhóm mà các dòng ĐANG DÙNG trong đề có đáp án khác nhau → can-duyet.json, không tự gộp.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply"), D = "scripts/data/gon-ngan-hang/";
const raw = fs.readFileSync(D + "in-use.raw", "utf8"); const use = new Map<string, Set<number>>(); const pos = new Map<string, string>();
for (const r of JSON.parse(raw.slice(raw.indexOf("{"), raw.lastIndexOf("}") + 1)).rows) { (use.get(r.h) ?? use.set(r.h, new Set()).get(r.h)!).add(r.exam_id); pos.set(r.exam_id + ":" + r.idx, r.h); }
const rows: any[] = [];
for (let f = 0; ; f += 500) { let d: any; for (let t = 0; t < 5; t++) { const r = await sb.from("question_bank").select("id,created_at,content_hash,source_exam_id,source_index,topic_id,topic_name,difficulty_source,grade,difficulty,form,archived,qtype,question").eq("archived", false).order("id").range(f, f + 499);
  if (!r.error) { d = r.data; break; } await new Promise((s) => setTimeout(s, 2000)); } if (!d) throw new Error("timeout"); rows.push(...d); if (d.length < 500) break; }
const pl = (h: any) => String(h ?? "").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim().toLowerCase();
const key = (r: any) => { const q = r.question ?? {}; const o = q.options ?? q.statements ?? q.items ?? [];
  return pl(q.question) + "‖" + (Array.isArray(o) ? o.map((x: any) => pl(typeof x === "string" ? x : x?.text ?? JSON.stringify(x))).join("|") : pl(JSON.stringify(o))); };
const ans = (r: any) => JSON.stringify(r.question?.answer ?? r.question?.correct ?? null);
// (A) PHIÊN BẢN CŨ: dòng không còn dùng trong đề nào, mà đề nguồn ở đúng vị trí đó nay mang một câu khác (đã sửa) giống ≥60% chữ.
const byHash = new Map(rows.map((r) => [r.content_hash, r])); const tok = (x: string) => new Set(x.split(/\W+/).filter((w) => w.length > 1));
const jac = (a: Set<string>, b: Set<string>) => { let i = 0; a.forEach((w) => b.has(w) && i++); return i / (a.size + b.size - i || 1); };
const txt = (q: any) => pl(q?.question) + " " + (Array.isArray(q?.options) ? q.options.map(pl).join(" ") : "");
const cu: { id: number; thay: number }[] = []; const daCu = new Set<number>();
for (const r of rows) { if (use.has(r.content_hash)) continue; const h2 = pos.get(r.source_exam_id + ":" + r.source_index); if (!h2 || h2 === r.content_hash) continue;
  const r2 = byHash.get(h2); if (r2 && jac(tok(txt(r.question)), tok(txt(r2.question))) >= 0.6) { cu.push({ id: r.id, thay: r2.id }); daCu.add(r.id); } }
const rows0 = rows; rows.splice(0, rows.length, ...rows0.filter((r) => !daCu.has(r.id)));
// (B) TRÙNG: cùng chữ đề + phương án.
const g = new Map<string, any[]>(); for (const r of rows) { const k = key(r); if (pl(r.question?.question).length >= 25) (g.get(k) ?? g.set(k, []).get(k)!).push(r); }
const plan: any[] = [], duyet: any[] = []; let thua = 0;
const goc = new Map(rows0.map((r) => [r.id, r]));
for (const a of [...g.values()].filter((a) => a.length > 1)) {
  const dung = a.filter((r) => (use.get(r.content_hash)?.size ?? 0) > 0);
  const dapAn = new Set((dung.length ? dung : a).map(ans));
  if (dapAn.size > 1) { duyet.push({ ids: a.map((r) => r.id), dang_dung: dung.map((r) => r.id), cau: pl(a[0].question.question).slice(0, 120), dap_an: a.map((r) => ({ id: r.id, dap_an: ans(r), de: [...(use.get(r.content_hash) ?? [])].slice(0, 5) })) }); continue; }
  const diem = (r: any) => (use.get(r.content_hash)?.size ?? 0) * 10 + (r.topic_id ? 3 : 0) + (r.difficulty ? 2 : 0) + (r.form ? 1 : 0);
  const keeper = [...a].sort((x, y) => diem(y) - diem(x) || x.id - y.id)[0];
  const bo = a.filter((r) => r.id !== keeper.id); thua += bo.length;
  plan.push({ keeper: keeper.id, archive: bo.map((r) => r.id), dang_dung_bo: bo.filter((r) => (use.get(r.content_hash)?.size ?? 0) > 0).length });
}
plan.push({ keeper: 0, archive: cu.map((c) => c.id), dang_dung_bo: 0, phien_ban_cu: cu });
fs.writeFileSync(D + "ke-hoach.json", JSON.stringify(plan)); fs.writeFileSync(D + "can-duyet.json", JSON.stringify(duyet, null, 1));
console.log(`phiên bản cũ ${cu.length} dòng · dòng chưa lưu trữ còn ${rows.length} · nhóm trùng ${plan.length - 1 + duyet.length} · tự gộp ${plan.length - 1} nhóm (lưu trữ ${thua} dòng, trong đó ${plan.reduce((s: number, p: any) => s + p.dang_dung_bo, 0)} dòng còn khớp một đề) · cần duyệt ${duyet.length} nhóm (${duyet.reduce((s, d) => s + d.ids.length, 0)} dòng)`);
// Chuyển lời giải: dòng giữ lại chưa có lời giải (<80 ký tự) mà dòng bị lưu trữ có (≥80) và cùng đáp án → chép sang.
const chuyen: { id: number; explanation: string }[] = [];
const cap = [...cu.map((c) => [c.thay, c.id]), ...plan.filter((p: any) => p.keeper).flatMap((p: any) => p.archive.map((i: number) => [p.keeper, i]))];
for (const [k, v] of cap) { const rk = goc.get(k)!, rv = goc.get(v)!; if (!rk || !rv) continue;
  if (pl(rk.question.explanation).length < 80 && pl(rv.question.explanation).length >= 80 && ans(rk) === ans(rv) && !chuyen.some((c) => c.id === k)) chuyen.push({ id: k, explanation: rv.question.explanation }); }
// Chuyển nhãn: dòng giữ lại thiếu chủ đề/mức độ/dạng mà dòng bị lưu trữ có → chép sang.
const nhan = new Map<number, any>();
for (const [k, v] of cap) { const rk = goc.get(k)!, rv = goc.get(v)!; if (!rk || !rv) continue; const u: any = nhan.get(k) ?? {};
  if (!rk.topic_id && rv.topic_id && !u.topic_id) { u.topic_id = rv.topic_id; u.topic_name = rv.topic_name; }
  if (!rk.difficulty && rv.difficulty && !u.difficulty) { u.difficulty = rv.difficulty; u.difficulty_source = rv.difficulty_source; }
  if (!rk.form && rv.form && !u.form) u.form = rv.form;
  if (!rk.grade && rv.grade && !u.grade) u.grade = rv.grade;
  if (Object.keys(u).length) nhan.set(k, u); }
console.log(`chuyển nhãn sang dòng giữ lại: ${nhan.size}`);
console.log(`chuyển lời giải sang dòng giữ lại: ${chuyen.length}`);
fs.writeFileSync(D + "chuyen-loi-giai.json", JSON.stringify(chuyen));
if (!APPLY) { console.log("dry-run — thêm --apply để lưu trữ"); process.exit(0); }
for (const [id, u] of nhan) { const { error } = await sb.from("question_bank").update(u).eq("id", id); if (error) throw new Error(error.message); }
const ids = plan.flatMap((p: any) => p.archive);
fs.writeFileSync(`scripts/logs/gon-ngan-hang-backup-${Date.now()}.json`, JSON.stringify({ ids_luu_tru: ids, nhan_truoc: [...nhan.keys()].map((i) => { const r = goc.get(i)!; return { id: i, topic_id: r.topic_id, topic_name: r.topic_name, difficulty: r.difficulty, difficulty_source: r.difficulty_source, form: r.form, grade: r.grade }; }), truoc_khi_chuyen_loi_giai: chuyen.map((c) => ({ id: c.id, question: goc.get(c.id)!.question })) }));
for (const c of chuyen) { const q = { ...goc.get(c.id)!.question, explanation: c.explanation }; const { error } = await sb.from("question_bank").update({ question: q }).eq("id", c.id); if (error) throw new Error(error.message); }
let ok = 0; for (let i = 0; i < ids.length; i += 200) { const { error } = await sb.from("question_bank").update({ archived: true }).in("id", ids.slice(i, i + 200)); if (error) throw new Error(error.message); ok += Math.min(200, ids.length - i); }
console.log("đã lưu trữ", ok);
