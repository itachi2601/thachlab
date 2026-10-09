// Đọc nguyên văn một số câu trong question_bank để người/agent kiểm tay — CHỈ ĐỌC, KHÔNG GHI.
//   npx tsx scripts/dump-bank-questions.mts 440002 463366 671619 ...
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

const ids = process.argv.slice(2).map(Number).filter(Boolean);
if (!ids.length) { console.error("Truyền danh sách id."); process.exit(1); }

const { data, error } = await supabase
  .from("question_bank")
  .select("id, grade, topic_name, question")
  .in("id", ids);
if (error) { console.error(error.message); process.exit(1); }

const out = (data ?? []).sort((a, b) => ids.indexOf(a.id) - ids.indexOf(b.id));
const outFile = path.join(scriptDir, "logs", `dump-bank-${Date.now()}.json`);
fs.writeFileSync(outFile, JSON.stringify(out, null, 2));
console.log(`Đã ghi ${out.length} câu → ${path.relative(process.cwd(), outFile)}`);
