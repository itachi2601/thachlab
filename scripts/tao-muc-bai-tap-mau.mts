// Tạo mục lesson_items kind='bai_tap_mau' (questions rỗng) cho bài chưa có, sao theo hình dạng mục của bài mẫu.
// Chỉ INSERT một dòng cho mỗi bài, không đụng mục khác. Bài đã có mục thì bỏ qua.
//   npx tsx scripts/tao-muc-bai-tap-mau.mts --lesson 30 --mau 158
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const argv = process.argv.slice(2);
const arg = (k: string) => Number(argv[argv.indexOf(k) + 1]);
const lessonId = arg("--lesson"), mauId = arg("--mau");
const fail = (m: string): never => { console.error("Lỗi:", m); process.exit(1); };
const env = (k: string) => {
  const p = path.join(root, ".env.local");
  const l = fs.existsSync(p) ? fs.readFileSync(p, "utf8").split("\n").find((x) => x.startsWith(k + "=")) : undefined;
  return process.env[k] ?? l?.slice(k.length + 1).trim();
};
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false, autoRefreshToken: false } });
const have = await sb.from("lesson_items").select("id").eq("lesson_id", lessonId).eq("kind", "bai_tap_mau");
if (have.error) fail(have.error.message);
if (have.data!.length) { console.log(`Bài ${lessonId} đã có mục bai_tap_mau (id ${have.data![0].id}) — bỏ qua.`); process.exit(0); }
const mau = await sb.from("lesson_items").select("*").eq("id", mauId).eq("kind", "bai_tap_mau").single();
if (mau.error) fail(mau.error.message);
const { id: _id, created_at: _c, updated_at: _u, ...rest } = mau.data as Record<string, unknown>;
const row = { ...rest, lesson_id: lessonId, questions: [], exam_ids: [], subtitle: "0 dạng bài kèm lời giải" };
const ins = await sb.from("lesson_items").insert(row).select("id");
if (ins.error) fail(ins.error.message);
console.log(`✓ Đã tạo mục bai_tap_mau id ${ins.data![0].id} cho bài ${lessonId} (sao hình dạng từ mục ${mauId}). Hoàn tác: xoá dòng lesson_items id ${ins.data![0].id}.`);
