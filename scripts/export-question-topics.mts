// Xuất question_topics (id, lesson_id, name, parent_id) ra scripts/data/question-topics.json để skill
// soan-quiz-ly-thuyet biết tên YCCĐ của từng bài khi gắn `topic`. CHẠY TRÊN MAC (cần service role).
//   npx tsx scripts/export-question-topics.mts
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
function readEnvLocal(key: string): string | undefined {
  const p = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const line = fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}
function askHidden(q: string): Promise<string> {
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    const a = rl as unknown as { _writeToOutput: (c: string) => void; stdoutMuted: boolean };
    a._writeToOutput = (c) => (rl as unknown as { output: NodeJS.WritableStream }).output.write(a.stdoutMuted ? "*" : c);
    a.stdoutMuted = false;
    rl.question(q, (v) => { rl.close(); process.stdout.write("\n"); resolve(v.trim()); });
    a.stdoutMuted = true;
  });
}
function fail(m: string): never { console.error("Lỗi:", m); process.exit(1); }

const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
if (!url) fail("không đọc được NEXT_PUBLIC_SUPABASE_URL");
const key = process.env.SUPABASE_SERVICE_ROLE_KEY ?? readEnvLocal("SUPABASE_SERVICE_ROLE_KEY") ?? (await askHidden("Dán SUPABASE_SERVICE_ROLE_KEY: "));
if (!key) fail("thiếu SUPABASE_SERVICE_ROLE_KEY");
const supabase = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });

const { data, error } = await supabase.from("question_topics").select("id, lesson_id, name, parent_id").order("lesson_id").order("id");
if (error) fail(error.message);
const out = path.join(scriptDir, "data", "question-topics.json");
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, JSON.stringify(data, null, 1) + "\n");
console.log(`✓ ${data.length} chủ đề → ${path.relative(process.cwd(), out)}`);
