// Xử lý câu trùng (lưu trữ, không xoá) + dọn rác đề 1237787 trong question_bank.
// Mặc định DRY-RUN. --apply để ghi. Sao lưu toàn bộ dòng cũ ra scripts/logs/ trước khi ghi.
//   npx tsx scripts/sua-trung-ngan-hang.mts            # dry-run
//   npx tsx scripts/sua-trung-ngan-hang.mts --apply    # ghi thật
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

// Bản trùng → lưu trữ (archived=true), giữ bản gốc còn hiển thị.
// (Đợt 1 đã chạy xong: 633923, 454505, 672808 đã lưu trữ — để trống khi chạy đợt sau.)
const ARCHIVE: Record<number, { keep: number }> = {};
// Rác hiển thị "A. B. C. D." trong stem (đáp án giữ nguyên, chờ thầy xác nhận).
const CLEAN: Record<number, (s: string) => string> = {
  // Xoá "A. B. C. D." (dù có thẻ HTML/nbsp xen giữa) và số 3 rơi lại ở cuối câu dẫn.
  1237787: (s) => s
    .replace(/A\.(?:\s|&nbsp;|<[^>]*>)*B\.(?:\s|&nbsp;|<[^>]*>)*C\.(?:\s|&nbsp;|<[^>]*>)*D\./g, "")
    .replace(/([?.])((?:\s|&nbsp;|<[^>]*>)*)\d(?:\s|&nbsp;|<[^>]*>)*$/, "$1$2")
    .replace(/\s{2,}/g, " ").trim()
    // Đổi nhãn 1. 2. 3. 4. thành (1)…(4) cho khớp quy ước đề.
    .replace(/\b1\.\s*(?=Tia X mang)/, "(1) ").replace(/\b2\.\s*(?=Tính chất)/, "(2) ")
    .replace(/\b3\.\s*(?=Do tia X)/, "(3) ").replace(/\b4\.\s*(?=Trong y học)/, "(4) "),
};

const ids = [...Object.keys(ARCHIVE), ...Object.keys(CLEAN)].map(Number);
const { data, error } = await supabase.from("question_bank").select("id, archived, note, question").in("id", ids);
if (error) { console.error(error.message); process.exit(1); }
const rows = data ?? [];
const bkFile = path.join(scriptDir, "logs", `sao-luu-trung-${Date.now()}.json`);
fs.writeFileSync(bkFile, JSON.stringify(rows, null, 2));
console.log(`Sao lưu ${rows.length} dòng → ${path.relative(process.cwd(), bkFile)}`);

for (const row of rows) {
  if (ARCHIVE[row.id]) {
    const note = `Trùng với #${ARCHIVE[row.id].keep} — lưu trữ 16/10/2026`;
    console.log(`#${row.id}: archived ${row.archived} → true | ${note}`);
    if (APPLY) {
      const { error: e } = await supabase.from("question_bank").update({ archived: true, note }).eq("id", row.id);
      if (e) { console.error(`#${row.id} lỗi: ${e.message}`); process.exit(1); }
    }
  }
  if (CLEAN[row.id]) {
    const q = { ...row.question, question: CLEAN[row.id](row.question.question) };
    const tail = q.question.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").slice(-120);
    console.log(`#${row.id}: stem dọn rác | đuôi mới: ${tail}`);
    if (APPLY) {
      const { error: e } = await supabase.from("question_bank").update({ question: q }).eq("id", row.id);
      if (e) { console.error(`#${row.id} lỗi: ${e.message}`); process.exit(1); }
    }
  }
}
console.log(APPLY ? "ĐÃ GHI." : "DRY-RUN — chưa ghi. Thêm --apply để ghi.");
