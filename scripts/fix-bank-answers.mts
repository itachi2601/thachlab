// Sửa đáp án một số câu trong question_bank đã được Claude đối chiếu tay (không phải DeepSeek áp thẳng).
// MẶC ĐỊNH dry-run: chỉ in TRƯỚC/SAU, không ghi. Thêm --apply mới ghi. Luôn sao lưu bản gốc ra scripts/logs/ trước khi ghi.
//
//   npx tsx scripts/fix-bank-answers.mts            # dry-run, xem trước
//   npx tsx scripts/fix-bank-answers.mts --apply    # ghi thật (có sao lưu)
//
// An toàn: với mỗi câu, script KIỂM đáp án hiện tại khớp "oldAnswer" đã ghi dưới đây; lệch (phiên khác đã sửa) → BỎ QUA câu đó.
// Chỉ đổi trường đáp án bên trong JSON `question`, không đụng nội dung đề / content_hash.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
function readEnvLocal(key: string): string | undefined {
  const p = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const line = fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}
const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
const key = process.env.SUPABASE_SERVICE_ROLE_KEY ?? readEnvLocal("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) { console.error("thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY"); process.exit(1); }
const supabase = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });

const APPLY = process.argv.includes("--apply");

type Patch =
  | { id: number; kind: "mc"; old: number; neu: number; reason: string }
  | { id: number; kind: "short"; old: string; neu: string; reason: string }
  | { id: number; kind: "tf"; old: boolean[]; neu: boolean[]; reason: string };

// Đọc danh sách sửa từ scripts/data/bank-answer-fixes.json (mục "fixes"). Mục "_can_xac_nhan" KHÔNG áp (chờ thầy duyệt).
const FIXES_FILE = path.join(scriptDir, "data", "bank-answer-fixes.json");
const PATCHES: Patch[] = (JSON.parse(fs.readFileSync(FIXES_FILE, "utf8")) as { fixes: Patch[] }).fixes;
console.log(`Đọc ${PATCHES.length} câu cần sửa từ ${path.relative(process.cwd(), FIXES_FILE)}.\n`);

const eqArr = (a: unknown[], b: unknown[]) => a.length === b.length && a.every((x, i) => x === b[i]);

const backup: unknown[] = [];
let willWrite = 0;

for (const p of PATCHES) {
  const { data, error } = await supabase.from("question_bank").select("id, question").eq("id", p.id).single();
  if (error || !data) { console.log(`⚠️  id=${p.id}: không đọc được (${error?.message ?? "không có"}) — bỏ qua.`); continue; }
  const q = data.question as Record<string, unknown>;
  backup.push({ id: p.id, question: JSON.parse(JSON.stringify(q)) });

  let okOld = false;
  let before = "";
  let after = "";
  const next = JSON.parse(JSON.stringify(q)) as Record<string, unknown>;

  if (p.kind === "mc") {
    okOld = q.answer === p.old;
    before = String(q.answer); after = String(p.neu);
    next.answer = p.neu;
  } else if (p.kind === "short") {
    okOld = String(q.answer) === p.old;
    before = String(q.answer); after = p.neu;
    next.answer = p.neu;
  } else {
    const st = (q.statements as { answer: boolean }[]) ?? [];
    okOld = Array.isArray(st) && eqArr(st.map((s) => !!s.answer), p.old);
    before = JSON.stringify(st.map((s) => !!s.answer)); after = JSON.stringify(p.neu);
    (next.statements as { answer: boolean }[]) = st.map((s, i) => ({ ...s, answer: p.neu[i] }));
  }

  if (!okOld) {
    console.log(`⚠️  id=${p.id}: đáp án hiện tại (${before}) KHÁC kỳ vọng (${JSON.stringify(p.old)}) — có thể đã sửa nơi khác. BỎ QUA.`);
    continue;
  }
  console.log(`• id=${p.id} [${p.kind}]  ${before}  →  ${after}`);
  console.log(`    ${p.reason}`);
  willWrite += 1;

  if (APPLY) {
    const { error: upErr } = await supabase.from("question_bank").update({ question: next }).eq("id", p.id);
    if (upErr) console.log(`    ✗ GHI LỖI: ${upErr.message}`);
    else console.log(`    ✓ đã ghi.`);
  }
}

const bkFile = path.join(scriptDir, "logs", `fix-bank-backup-${Date.now()}.json`);
fs.mkdirSync(path.dirname(bkFile), { recursive: true });
fs.writeFileSync(bkFile, JSON.stringify(backup, null, 2));
console.log(`\nSao lưu bản gốc ${backup.length} câu → ${path.relative(process.cwd(), bkFile)}`);
console.log(APPLY ? `Đã GHI ${willWrite} câu.` : `DRY-RUN: sẽ ghi ${willWrite} câu. Chạy lại kèm --apply để ghi thật.`);
