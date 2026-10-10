// Ghi question_bank.lint_flags bằng lib/question-lint.ts (một nguồn quy tắc, không regex trong SQL).
// CHỈ ghi cột lint_flags — không đụng archived, không đụng exams. Chỉ lưu cờ mức "loi", bỏ qua câu có lint_ignored.
//   npx tsx scripts/cap-nhat-lint-flags.mts --dry-run [N]   # xem thử N dòng đổi (mặc định 20), KHÔNG ghi
//   npx tsx scripts/cap-nhat-lint-flags.mts --ghi            # ghi thật; log JSON {id,before,after} ở scripts/logs/
//   npx tsx scripts/cap-nhat-lint-flags.mts --undo scripts/logs/<log>.json
// Cần migration 20261011120000_question_bank_lint_flags đã chạy.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { activeLintFlags, blockingFlags, flagCodes } from "../lib/question-lint";

const dir = path.dirname(fileURLToPath(import.meta.url));
const envTxt = fs.readFileSync(path.resolve(dir, "..", ".env.local"), "utf8").split("\n");
const env = (k: string) => envTxt.find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim()!;
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const argv = process.argv.slice(2);
const same = (a: string[], b: string[]) => a.length === b.length && a.every((x, i) => x === b[i]);

async function writeAll(rows: { id: number; flags: string[] }[], concurrency = 10) {
  let i = 0, done = 0;
  await Promise.all(Array.from({ length: concurrency }, async () => {
    while (i < rows.length) {
      const r = rows[i++];
      const { error } = await sb.from("question_bank").update({ lint_flags: r.flags }).eq("id", r.id);
      if (error) { console.error(`id ${r.id}:`, error.message); process.exit(1); }
      if (++done % 200 === 0) console.log(`  …${done}/${rows.length}`);
    }
  }));
}

const undoIdx = argv.indexOf("--undo");
if (undoIdx >= 0) {
  const log = JSON.parse(fs.readFileSync(argv[undoIdx + 1], "utf8")) as { id: number; before: string[] }[];
  await writeAll(log.map((l) => ({ id: l.id, flags: l.before })));
  console.log(`Đã hoàn tác ${log.length} dòng.`);
  process.exit(0);
}

const write = argv.includes("--ghi");
const dIdx = argv.indexOf("--dry-run");
const showN = dIdx >= 0 && /^\d+$/.test(argv[dIdx + 1] ?? "") ? Number(argv[dIdx + 1]) : 20;

const changes: { id: number; before: string[]; after: string[] }[] = [];
const byCode: Record<string, number> = {};
let from = 0, total = 0;
for (;;) {
  const { data, error } = await sb.from("question_bank").select("id, qtype, question, lint_flags").eq("archived", false).order("id").range(from, from + 999);
  if (error) { console.error(error.message); process.exit(1); }
  if (!data?.length) break;
  for (const r of data) {
    total++;
    const after = flagCodes(blockingFlags(activeLintFlags(r.question, r.qtype)));
    const before = [...((r.lint_flags as string[]) ?? [])].sort();
    for (const c of after) byCode[c] = (byCode[c] ?? 0) + 1;
    if (!same(before, after)) changes.push({ id: r.id, before, after });
  }
  from += 1000;
}
console.log(`Quét ${total} câu · ${changes.length} dòng cần đổi lint_flags`, byCode);

if (!write) {
  for (const c of changes.slice(0, showN)) console.log(c.id, JSON.stringify(c.before), "→", JSON.stringify(c.after));
  console.log("(dry-run: chưa ghi gì. Thêm --ghi để ghi thật.)");
  process.exit(0);
}
const logFile = path.join(dir, "logs", `lint-flags-${Date.now()}.json`);
fs.writeFileSync(logFile, JSON.stringify(changes, null, 1));
console.log("Log hoàn tác:", path.relative(process.cwd(), logFile));
await writeAll(changes.map((c) => ({ id: c.id, flags: c.after })));
console.log(`Đã ghi ${changes.length} dòng. Hoàn tác: --undo ${path.relative(process.cwd(), logFile)}`);
