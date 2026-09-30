// Xuất question_topics (id, lesson_id, name, parent_id) ra scripts/data/question-topics.json để skill
// soan-quiz-ly-thuyet biết tên YCCĐ của từng bài khi gắn `topic`. CHỈ ĐỌC. Chạy trên Mac (cần service role):
//   npx tsx scripts/export-question-topics.mts
// Cloud bị chặn Supabase và không có key — skill vẫn chạy được khi file này chưa có (topic = lesson.title).
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));

function readEnvLocal(key: string): string | undefined {
  const envPath = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(envPath)) return undefined;
  const line = fs.readFileSync(envPath, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}

function askHidden(query: string): Promise<string> {
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    const rlAny = rl as unknown as { _writeToOutput: (chunk: string) => void; stdoutMuted: boolean };
    rlAny._writeToOutput = (chunk) => (rl as unknown as { output: NodeJS.WritableStream }).output.write(rlAny.stdoutMuted ? "*" : chunk);
    rlAny.stdoutMuted = false;
    rl.question(query, (answer) => {
      rl.close();
      process.stdout.write("\n");
      resolve(answer.trim());
    });
    rlAny.stdoutMuted = true;
  });
}

function fail(msg: string): never {
  console.error("Lỗi:", msg);
  process.exit(1);
}

async function main() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
  if (!url) fail("không đọc được NEXT_PUBLIC_SUPABASE_URL từ .env.local");
  const key =
    process.env.SUPABASE_SERVICE_ROLE_KEY ??
    readEnvLocal("SUPABASE_SERVICE_ROLE_KEY") ??
    (await askHidden("Dán SUPABASE_SERVICE_ROLE_KEY (Settings → API → service_role): "));
  if (!key) fail("thiếu SUPABASE_SERVICE_ROLE_KEY");
  const supabase = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });

  const rows: { id: number; lesson_id: number | null; name: string; parent_id: number | null }[] = [];
  for (let from = 0; ; from += 1000) {
    const { data, error } = await supabase
      .from("question_topics")
      .select("id, lesson_id, name, parent_id")
      .order("id")
      .range(from, from + 999);
    if (error) fail(error.message);
    rows.push(...(data ?? []));
    if (!data || data.length < 1000) break;
  }
  const out = path.join(scriptDir, "data", "question-topics.json");
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, JSON.stringify({ exported_at: new Date().toISOString(), topics: rows }, null, 1) + "\n");
  console.log(`✓ ${rows.length} chủ đề → ${path.relative(process.cwd(), out)}`);
}

main().catch((e) => fail(e instanceof Error ? e.message : String(e)));
