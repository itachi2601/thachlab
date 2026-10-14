/**
 * Đọc ghi chú của giáo viên lúc dạy (bảng teacher_lesson_notes) và in gọn theo BÀI → MỤC.
 * Chạy trên Mac: npx tsx .claude/skills/xem-ghi-chu-lop/scripts/doc-ghi-chu.mts [--status moi|da_xem|da_xu_ly|all]
 *   Mặc định lấy ghi chú chưa xử lý (moi + da_xem).
 *   --danh-dau da_xem|da_xu_ly --ids 1,2,3 [--ghi "đã làm gì"]   đổi trạng thái (chỉ cột status/resolution)
 * Đọc bằng service_role (bỏ qua RLS) — ghi chú là việc riêng của thầy, không đưa ra ngoài phiên Claude.
 */
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..", "..", "..", "..");
function env(name: string) {
  if (process.env[name]) return process.env[name];
  const p = path.join(root, ".env.local");
  if (!fs.existsSync(p)) return undefined;
  return fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${name}=`))?.slice(name.length + 1).trim();
}
const url = env("NEXT_PUBLIC_SUPABASE_URL"), key = env("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) throw new Error("Thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY");
const sb = createClient(url, key);

const args = process.argv.slice(2);
const arg = (name: string) => (args.includes(name) ? args[args.indexOf(name) + 1] : undefined);

const mark = arg("--danh-dau");
if (mark) {
  if (!["da_xem", "da_xu_ly"].includes(mark)) throw new Error("--danh-dau chỉ nhận da_xem | da_xu_ly");
  const ids = (arg("--ids") ?? "").split(",").map(Number).filter(Number.isInteger);
  if (!ids.length) throw new Error("Thiếu --ids 1,2,3");
  const patch: Record<string, string> = { status: mark, updated_at: new Date().toISOString() };
  if (arg("--ghi")) patch.resolution = arg("--ghi")!;
  const { error, count } = await sb.from("teacher_lesson_notes").update(patch, { count: "exact" }).in("id", ids);
  if (error) throw error;
  console.log(`Đã đánh dấu ${count} ghi chú → ${mark}`);
  process.exit(0);
}

const status = arg("--status") ?? "open";
let q = sb
  .from("teacher_lesson_notes")
  .select("id,created_at,lesson_id,item_id,page_key,page_heading,tag,body,status,resolution,lessons(title)")
  .order("lesson_id").order("created_at");
if (status === "open") q = q.in("status", ["moi", "da_xem"]);
else if (status !== "all") q = q.eq("status", status);
const { data, error } = await q;
if (error) throw error;

const TAG: Record<string, string> = {
  hs_hieu_sai: "HS hiểu sai", thieu_hinh: "Thiếu hình/mô phỏng", vi_du: "Ví dụ chưa hay",
  dai_nhanh: "Dài/quá nhanh", loi: "Lỗi", y_tuong: "Ý tưởng",
};
type Row = NonNullable<typeof data>[number];
const lessonTitle = (r: Row) => {
  const l = (r as { lessons?: { title: string } | { title: string }[] | null }).lessons;
  return (Array.isArray(l) ? l[0]?.title : l?.title) ?? "?";
};
const byLesson = new Map<number, Row[]>();
for (const r of data ?? []) byLesson.set(r.lesson_id, [...(byLesson.get(r.lesson_id) ?? []), r]);

console.log(`# Ghi chú lớp (status=${status}): ${data?.length ?? 0} ghi chú, ${byLesson.size} bài\n`);
for (const [lessonId, list] of byLesson) {
  console.log(`## Bài ${lessonId} — ${lessonTitle(list[0])} (${list.length})`);
  for (const r of list) {
    console.log(`- #${r.id} ${r.created_at.slice(0, 10)} [${TAG[r.tag] ?? r.tag}] ${r.page_heading ? `@ ${r.page_heading}` : ""}\n  ${r.body.replace(/\s+/g, " ")}`);
  }
  console.log();
}
const out = path.join(root, "scripts", "logs", `ghi-chu-lop-${new Date().toISOString().slice(0, 10)}.json`);
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, JSON.stringify(data, null, 2));
console.log(`(đã ghi ${path.relative(root, out)})`);
