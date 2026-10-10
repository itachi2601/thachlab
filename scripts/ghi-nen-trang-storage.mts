// Ghi đè ảnh nền-trắng (scripts/data/gemini-hinh/nen-trang/<id>/anh-N.png) lên ĐÚNG đường dẫn Storage cũ của ảnh trong câu
// ngân hàng (bucket lesson-media) — URL không đổi nên KHÔNG đụng question_bank/exams, mọi đề đang dùng tự đẹp lên.
// Ảnh gốc đã nằm ở scripts/data/gemini-hinh/cau/<id>/ → hoàn tác bằng --khoi-phuc.
//   npx tsx scripts/ghi-nen-trang-storage.mts 610079,618296            # dry-run
//   npx tsx scripts/ghi-nen-trang-storage.mts 610079,618296 --ghi      # ghi thật
//   npx tsx scripts/ghi-nen-trang-storage.mts 610079,618296 --ghi --khoi-phuc   # trả ảnh gốc
// Chạy trên Mac qua tab terminal (cần SUPABASE_SERVICE_ROLE_KEY trong env/.env.local).
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(scriptDir, "data", "gemini-hinh");
const ids = (process.argv[2] ?? "").split(",").map(Number).filter(Boolean);
const ghi = process.argv.includes("--ghi");
const khoiPhuc = process.argv.includes("--khoi-phuc");
function readEnvLocal(key: string): string | undefined {
  const p = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const line = fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}
if (!ids.length) { console.error("cần danh sách id"); process.exit(1); }
const rows: { id: number; srcs: string[] }[] = JSON.parse(fs.readFileSync(path.join(scriptDir, "data", "kiem-ke-anh-ngan-hang", "rows.json"), "utf8"));
const jobs: { id: number; storagePath: string; file: string; type: string }[] = [];
for (const id of ids) {
  const r = rows.find((x) => x.id === id);
  if (!r) { console.error(`#${id}: không có trong rows.json`); continue; }
  r.srcs.forEach((src, i) => {
    const m = src.match(/\/storage\/v1\/object\/public\/lesson-media\/(.+)$/);
    if (!m) { console.error(`#${id} ảnh ${i + 1}: không phải Storage lesson-media — bỏ qua`); return; }
    const goc = fs.readdirSync(path.join(root, "cau", String(id))).find((f) => f.startsWith(`anh-${i + 1}.`));
    const file = khoiPhuc ? path.join(root, "cau", String(id), goc ?? "") : path.join(root, "nen-trang", String(id), `anh-${i + 1}.png`);
    if (!fs.existsSync(file) || (khoiPhuc && !goc)) { console.error(`#${id} ảnh ${i + 1}: thiếu file ${file}`); return; }
    jobs.push({ id, storagePath: m[1], file, type: file.endsWith(".png") ? "image/png" : "image/jpeg" });
  });
}
console.log(`${khoiPhuc ? "KHÔI PHỤC ảnh gốc" : "GHI ảnh nền trắng"}: ${jobs.length} ảnh`);
for (const j of jobs) console.log(`  #${j.id} ← ${path.relative(root, j.file)} → lesson-media/${j.storagePath}`);
if (!ghi) { console.log("DRY-RUN. Thêm --ghi để ghi thật."); process.exit(0); }
const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
const key = process.env.SUPABASE_SERVICE_ROLE_KEY ?? readEnvLocal("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) { console.error("thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY"); process.exit(1); }
const supabase = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });
let ok = 0;
for (const j of jobs) {
  const { error } = await supabase.storage.from("lesson-media").upload(j.storagePath, fs.readFileSync(j.file), { upsert: true, contentType: j.type, cacheControl: "300" });
  if (error) console.error(`#${j.id} ${j.storagePath}: LỖI ${error.message}`); else { ok++; console.log(`#${j.id} ✓ ${j.storagePath}`); }
}
console.log(`xong ${ok}/${jobs.length}`);
