// Đổi tên gốc các đề "máy sinh" (giữa kì / cuối kì / thi thử) sang tên chuẩn — xem lib/exam-title.ts.
//   npx tsx scripts/doi-ten-de-chuan.mts            # chạy thử: in số đề đổi, không ghi
//   npx tsx scripts/doi-ten-de-chuan.mts --apply    # ghi thật, sao lưu tên cũ ra scripts/logs/
// Hoàn tác: npx tsx scripts/doi-ten-de-chuan.mts --restore scripts/logs/<file sao lưu>
// Cần public/data/exam-index.json mới (node scripts/build-content.mjs --only-exam-samples) để biết loại đề và lớp.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { createClient } from "@supabase/supabase-js";
import { isMachineExamTitle, standardExamTitle } from "../lib/exam-title";

const env = Object.fromEntries(
  readFileSync(".env.local", "utf8")
    .split("\n")
    .filter((l) => l.includes("=") && !l.startsWith("#"))
    .map((l) => {
      const i = l.indexOf("=");
      return [l.slice(0, i), l.slice(i + 1).replace(/^["']|["']$/g, "")];
    }),
);
const admin = createClient(env.NEXT_PUBLIC_SUPABASE_URL, env.SUPABASE_SERVICE_ROLE_KEY, { auth: { persistSession: false } });

async function runBatches<T>(items: T[], size: number, fn: (x: T) => Promise<void>) {
  for (let i = 0; i < items.length; i += size) await Promise.all(items.slice(i, i + size).map(fn));
}

const restoreIdx = process.argv.indexOf("--restore");
if (restoreIdx > 0) {
  const backup = JSON.parse(readFileSync(process.argv[restoreIdx + 1], "utf8")) as { id: number; old: string }[];
  await runBatches(backup, 20, async (r) => {
    const { error } = await admin.from("exams").update({ title: r.old }).eq("id", r.id);
    if (error) throw error;
  });
  console.log(`đã khôi phục ${backup.length} tên đề.`);
  process.exit(0);
}

const apply = process.argv.includes("--apply");
const index = JSON.parse(readFileSync("public/data/exam-index.json", "utf8")).exams as {
  id: number; title: string; shelf: "giua-ki" | "cuoi-ki" | "thi-thu"; grade: string;
}[];
const changes = index
  .filter((e) => isMachineExamTitle(e.title))
  .map((e) => ({ id: e.id, old: e.title, next: standardExamTitle(e.title, e.shelf, e.grade) }))
  .filter((c) => c.next !== c.old);
console.log(`${changes.length} đề sẽ đổi tên (trên ${index.length} đề trong mục lục).`);
if (!apply) {
  for (const c of changes.slice(0, 5)) console.log(`  #${c.id}: ${c.old}\n      → ${c.next}`);
  console.log("Chạy lại với --apply để ghi.");
  process.exit(0);
}

mkdirSync("scripts/logs", { recursive: true });
const backupPath = `scripts/logs/doi-ten-de-${new Date().toISOString().slice(0, 10)}.json`;
writeFileSync(backupPath, JSON.stringify(changes.map(({ id, old }) => ({ id, old })), null, 1));
console.log(`đã sao lưu tên cũ: ${backupPath}`);
let done = 0;
await runBatches(changes, 20, async (c) => {
  const { error } = await admin.from("exams").update({ title: c.next }).eq("id", c.id).eq("title", c.old);
  if (error) throw error;
  done++;
});
console.log(`đã đổi ${done}/${changes.length} tên đề.`);
