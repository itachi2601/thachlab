// Tải lý thuyết của bài KHOÁ từ DB về scripts/data/.lesson-cache/<id>.json (cùng dạng public/data/lessons/<id>.json)
// vì build-content chỉ xuất bài xem thử. CHỈ ĐỌC DB (service role), không ghi gì. Chạy trên Mac.
//   npx tsx .claude/skills/soan-quiz-ly-thuyet/scripts/fetch-lessons.mts 83 84 85 [--force]
import { createClient } from "@supabase/supabase-js";
import { execSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { LESSON_CACHE_DIR, ROOT, lessonFile } from "./lib";

function envFiles(): string[] {
  const out = [path.join(ROOT, ".env.local")];
  try { // worktree: .env.local nằm ở thư mục chính
    const common = execSync("git rev-parse --path-format=absolute --git-common-dir", { cwd: ROOT, encoding: "utf8" }).trim();
    out.push(path.join(path.dirname(common), ".env.local"));
  } catch { /* không phải repo git */ }
  return out;
}
export function readEnvLocal(key: string): string | undefined {
  if (process.env[key]) return process.env[key];
  for (const p of envFiles()) {
    if (!fs.existsSync(p)) continue;
    const line = fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
    if (line) return line.slice(key.length + 1).trim().replace(/^["']|["']$/g, "");
  }
  return undefined;
}

/** Đảm bảo mỗi bài có file lesson (public/data hoặc cache); thiếu thì tải từ DB. */
export async function ensureLessons(ids: number[], force = false): Promise<void> {
  const need = ids.filter((id) => force || !lessonFile(id));
  if (!need.length) return;
  const url = readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
  const key = readEnvLocal("SUPABASE_SERVICE_ROLE_KEY");
  if (!url || !key) throw new Error("thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY (.env.local) để tải bài khoá từ DB");
  const sb = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });
  fs.mkdirSync(LESSON_CACHE_DIR, { recursive: true });
  for (const id of need) {
    const { data: lesson, error } = await sb.from("lessons").select("id, title, chapter_id, sort_order, published, lesson_kind").eq("id", id).single();
    if (error || !lesson) throw new Error(`đọc lessons #${id}: ${error?.message ?? "không thấy"}`);
    const { data: items, error: e2 } = await sb.from("lesson_items").select("id, kind, title, body_html, summary_html, exam_ids").eq("lesson_id", id).eq("kind", "ly_thuyet");
    if (e2) throw new Error(`đọc lesson_items bài ${id}: ${e2.message}`);
    fs.writeFileSync(path.join(LESSON_CACHE_DIR, `${id}.json`), JSON.stringify({ lesson, items }));
    console.log(`  đã tải bài ${id} (${(lesson as { title: string }).title}) · ${(items ?? []).length} mục lý thuyết → .lesson-cache`);
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  const ids = args.filter((a) => /^\d+$/.test(a)).map(Number);
  if (!ids.length) { console.error("cần ít nhất một lesson_id"); process.exit(1); }
  await ensureLessons(ids, args.includes("--force"));
}
