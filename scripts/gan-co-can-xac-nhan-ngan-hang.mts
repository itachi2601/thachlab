// Gắn cờ `canXacNhanDapAn` vào question_bank.lint_flags cho các câu trong mục "_can_xac_nhan" của scripts/data/bank-answer-fixes.json
// (127 câu Claude nghi sai đáp án, CHỜ thầy duyệt). Câu có lint_flags khác rỗng bị lesson_practice_pool/check_bank_practice_answer loại
// khỏi kho Luyện tập và khỏi bộ lọc "Chỉ câu sạch" → học sinh không gặp câu có thể sai đáp án trong lúc chờ duyệt.
// CHỈ ghi cột lint_flags (thêm mã, giữ cờ có sẵn); không đụng question/archived. Không đổi đáp án.
//
//   npx tsx scripts/gan-co-can-xac-nhan-ngan-hang.mts                  # dry-run (mặc định): in từng câu, KHÔNG ghi
//   npx tsx scripts/gan-co-can-xac-nhan-ngan-hang.mts --ghi            # ghi thật (có log hoàn tác)
//   npx tsx scripts/gan-co-can-xac-nhan-ngan-hang.mts --undo <log.json>  # hoàn tác theo log
//
// Câu bị bỏ qua: không đọc được; đã archived; đáp án hiện tại KHÁC "old" trong file (đã có phiên khác sửa — không còn là ca nghi ngờ).
// scripts/cap-nhat-lint-flags.mts giữ nguyên mã này (MANUAL_FLAG_CODES trong lib/question-lint.ts).
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const FLAG = "canXacNhanDapAn";
const dir = path.dirname(fileURLToPath(import.meta.url));
const envTxt = fs.readFileSync(path.resolve(dir, "..", ".env.local"), "utf8").split("\n");
const env = (k: string) => envTxt.find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim() ?? "";
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const argv = process.argv.slice(2);
const WRITE = argv.includes("--ghi");

type Row = { id: number; before: string[]; after: string[] };
async function writeAll(rows: Row[]) {
  for (const r of rows) {
    const { error } = await sb.from("question_bank").update({ lint_flags: r.after }).eq("id", r.id);
    if (error) { console.error(`id ${r.id}:`, error.message); process.exit(1); }
  }
}

const undoIdx = argv.indexOf("--undo");
if (undoIdx >= 0) {
  const log = JSON.parse(fs.readFileSync(argv[undoIdx + 1], "utf8")) as Row[];
  await writeAll(log.map((l) => ({ id: l.id, before: l.after, after: l.before })));
  console.log(`Đã hoàn tác ${log.length} dòng.`);
  process.exit(0);
}

type Cand = { id: number; kind: "mc" | "short" | "tf"; old: number | string | boolean[]; nghi: unknown; reason: string };
const cands = (JSON.parse(fs.readFileSync(path.join(dir, "data", "bank-answer-fixes.json"), "utf8")) as { _can_xac_nhan: Cand[] })._can_xac_nhan;

const ids = cands.map((c) => c.id);
const { data, error } = await sb.from("question_bank").select("id, archived, question, lint_flags").in("id", ids);
if (error) { console.error(error.message); process.exit(1); }
const byId = new Map((data ?? []).map((r) => [r.id as number, r]));

const changes: Row[] = [];
const skipped: Record<string, number[]> = { khongDoc: [], archived: [], daSua: [], daCoCo: [] };
for (const c of cands) {
  const r = byId.get(c.id);
  if (!r) { skipped.khongDoc.push(c.id); continue; }
  if (r.archived) { skipped.archived.push(c.id); continue; }
  const q = r.question as Record<string, unknown>;
  let cur: unknown;
  if (c.kind === "mc") cur = q.answer;
  else if (c.kind === "short") cur = String(q.answer);
  else cur = ((q.statements as { answer: boolean }[]) ?? []).map((s) => !!s.answer);
  if (JSON.stringify(cur) !== JSON.stringify(c.old)) { skipped.daSua.push(c.id); continue; }
  const before = [...((r.lint_flags as string[]) ?? [])].sort();
  if (before.includes(FLAG)) { skipped.daCoCo.push(c.id); continue; }
  changes.push({ id: c.id, before, after: [...before, FLAG].sort() });
}

console.log(`Đọc ${cands.length} câu _can_xac_nhan · sẽ gắn cờ ${changes.length} câu`);
for (const [k, v] of Object.entries(skipped)) if (v.length) console.log(`  bỏ qua (${k}): ${v.length} — ${v.slice(0, 15).join(", ")}${v.length > 15 ? "…" : ""}`);
const withOther = changes.filter((c) => c.before.length > 0).length;
console.log(`  trong đó ${withOther} câu đã có cờ lint khác (giữ nguyên, chỉ thêm ${FLAG})`);
for (const c of changes.slice(0, 8)) console.log(`  ${c.id}: ${JSON.stringify(c.before)} → ${JSON.stringify(c.after)}`);

if (!WRITE) {
  console.log("(dry-run: chưa ghi gì. Thêm --ghi để ghi thật.)");
  process.exit(0);
}
const logFile = path.join(dir, "logs", `can-xac-nhan-${Date.now()}.json`);
fs.mkdirSync(path.dirname(logFile), { recursive: true });
fs.writeFileSync(logFile, JSON.stringify(changes, null, 1));
await writeAll(changes);
console.log(`Đã ghi ${changes.length} dòng. Hoàn tác: --undo ${path.relative(process.cwd(), logFile)}`);
