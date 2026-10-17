// Sửa đáp án + nhãn (1),(2)… cho câu "số phát biểu đúng" trong question_bank.
// Mặc định DRY-RUN (chỉ in). Thêm --apply để ghi. Trước khi ghi luôn sao lưu các dòng cũ ra scripts/logs/.
//   npx tsx scripts/sua-phat-bieu-ngan-hang.mts            # dry-run
//   npx tsx scripts/sua-phat-bieu-ngan-hang.mts --apply    # ghi thật
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

// Đáp án đã đối chiếu: index 0-based trong options (đã kiểm: answer là chỉ số 0-based).
// Chỉ đổi answer; stem (nếu cần) đổi bằng hàm fixStem.
// Gắn nhãn (n) cho các đoạn ngăn bởi <br> (đoạn 0 là câu dẫn), bỏ qua đoạn cuối nếu là câu kết.
const labelBr = (s: string, from: number, to: number) =>
  s.split("<br>").map((p, i) => (i >= from && i <= to ? `(${i}) ${p.trim()}` : p)).join("<br>");

const PATCHES: Record<number, { answer?: number; fixStem?: (s: string) => string }> = {
  7342: { answer: 3 },   // 4 phát biểu đúng: (1),(4),(5),(6) → option "4." (index 3)
  // Đáp án giữ nguyên (đã đối chiếu: đúng (1),(2),(4) → "3." index 1); chỉ thêm nhãn.
  456682: { fixStem: (s) => s
    .replace("− Từ điểm ba, giữ nguyên nhiệt độ và tăng", "<br>(1) Từ điểm ba, giữ nguyên nhiệt độ và tăng")
    .replace("− Từ điểm ba, giữ nguyên áp suất và tăng", "<br>(2) Từ điểm ba, giữ nguyên áp suất và tăng")
    .replace("− Điểm ba của nước", "<br>(3) Điểm ba của nước")
    .replace("− Từ điểm ba, giữ nguyên áp suất và giảm", "<br>(4) Từ điểm ba, giữ nguyên áp suất và giảm") },
  633134: { fixStem: (s) => labelBr(s, 1, 5) },  // đáp án (3),(4),(5) = option index 2, giữ nguyên
  683263: { fixStem: (s) => labelBr(s, 1, 4) },  // 4/4 đúng → "4." index 0, giữ nguyên
  681767: { answer: 1, fixStem: (s) => s
    .replace(/\b1\.\s*(?=Một vật)/, "(1) ").replace(/\b2\.\s*(?=Quán tính)/, "(2) ")
    .replace(/\b3\.\s*(?=Khối lượng)/, "(3) ").replace(/\b4\.\s*(?=Lực và phản lực)/, "(4) ") },
};

const ids = Object.keys(PATCHES).map(Number);
const { data, error } = await supabase.from("question_bank").select("id, question").in("id", ids);
if (error) { console.error(error.message); process.exit(1); }

const backup = data ?? [];
const bkFile = path.join(scriptDir, "logs", `sao-luu-phat-bieu-${Date.now()}.json`);
fs.writeFileSync(bkFile, JSON.stringify(backup, null, 2));
console.log(`Sao lưu ${backup.length} dòng → ${path.relative(process.cwd(), bkFile)}`);

for (const row of backup) {
  const p = PATCHES[row.id];
  const q = { ...row.question };
  const before = { answer: q.answer };
  if (p.answer !== undefined) q.answer = p.answer;
  if (p.fixStem) q.question = p.fixStem(q.question);
  console.log(`#${row.id}: answer ${before.answer} → ${q.answer}${p.fixStem ? " (+ stem)" : ""}`);
  if (p.fixStem) console.log(`   stem mới: ${q.question.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").slice(0, 400)}`);
  if (APPLY) {
    const { error: e } = await supabase.from("question_bank").update({ question: q }).eq("id", row.id);
    if (e) { console.error(`#${row.id} lỗi: ${e.message}`); process.exit(1); }
  }
}
console.log(APPLY ? "ĐÃ GHI." : "DRY-RUN — chưa ghi. Thêm --apply để ghi.");
