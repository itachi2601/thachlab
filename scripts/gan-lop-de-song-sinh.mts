// Gán lớp cho đề published chưa có exam_classes mà gan-lop-de-chua-gan.mts không suy được (22/11/2026).
// Quy tắc: (1) đề "sinh đôi" cùng tiêu đề đã có lớp → lấy lớp của nó; (2) tiêu đề Chuyên đề/HSG/CNC/AVCN → nhóm tương ứng; còn lại để trống, in ra.
//   npx tsx scripts/gan-lop-de-song-sinh.mts           # dry-run, ghi bảng ra scripts/logs/
//   npx tsx scripts/gan-lop-de-song-sinh.mts --apply   # chèn exam_classes + file undo
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const envTxt = fs.readFileSync(path.resolve(dir, "..", ".env.local"), "utf8");
const env = (k: string) => envTxt.split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");

async function all<T>(build: (a: number, b: number) => PromiseLike<{ data: T[] | null; error: any }>): Promise<T[]> {
  const out: T[] = [];
  for (let f = 0; ; f += 1000) {
    const { data, error } = await build(f, f + 999);
    if (error) throw new Error(error.message);
    out.push(...(data ?? []));
    if (!data || data.length < 1000) return out;
  }
}
const exams = await all<any>((a, b) => sb.from("exams").select("id,title,subject_code,published").order("id").range(a, b));
const ec = await all<any>((a, b) => sb.from("exam_classes").select("exam_id,class_id").order("exam_id").range(a, b));
const classesOf = new Map<number, number[]>();
for (const r of ec) (classesOf.get(r.exam_id) ?? classesOf.set(r.exam_id, []).get(r.exam_id)!).push(r.class_id);
const todo = exams.filter((e) => e.published && !classesOf.has(e.id));
const byTitle = new Map<string, any[]>();
for (const e of exams) (byTitle.get(e.title.trim()) ?? byTitle.set(e.title.trim(), []).get(e.title.trim())!).push(e);

const plan: { exam_id: number; class_id: number; why: string; title: string }[] = [];
const left: any[] = [];
for (const e of todo) {
  const twins = (byTitle.get(e.title.trim()) ?? []).filter((x) => x.id !== e.id && classesOf.has(x.id));
  const cls = new Set<number>(twins.flatMap((t) => classesOf.get(t.id)!));
  if (cls.size) { for (const c of cls) plan.push({ exam_id: e.id, class_id: c, why: `sinh đôi #${twins.map((t) => t.id).join(",")}`, title: e.title }); continue; }
  const bySubject = e.subject_code === "hsg-vat-ly" ? 19 : e.subject_code === "avcn" ? 20 : e.id === 1352 ? 16 : null;
  if (bySubject) { plan.push({ exam_id: e.id, class_id: bySubject, why: "môn/bài", title: e.title }); continue; }
  left.push(e);
}
console.log(`chưa gán ${todo.length}; gán theo sinh đôi ${new Set(plan.map((p) => p.exam_id)).size}; còn lại ${left.length}`);
for (const e of left) console.log(`  CÒN #${e.id} [${e.subject_code}] ${e.title}`);
fs.writeFileSync(path.resolve(dir, "logs", `gan-lop-song-sinh-${APPLY ? "ap-dung" : "dry"}-${Date.now()}.json`), JSON.stringify({ inserted: plan.map(({ exam_id, class_id }) => ({ exam_id, class_id })), plan, left }, null, 1));
if (APPLY) {
  const { error } = await sb.from("exam_classes").insert(plan.map(({ exam_id, class_id }) => ({ exam_id, class_id })));
  if (error) { console.error(error.message); process.exit(1); }
  console.log(`Đã chèn ${plan.length} dòng`);
}
