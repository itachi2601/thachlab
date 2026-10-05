// Kiểm LOẠT: file `content/lesson-samples/*/theory.html` có khớp mục Lý thuyết đang có trong DB không
// (bỏ qua khối video)? Dùng TRƯỚC khi bồi dặp video vào loạt bài đã đăng: bài nào file khác DB thì
// `--chi-video` sẽ chặn (đúng ý đồ) — cần xem tay trước khi đăng.
//
//   npx tsx scripts/so-file-voi-db.mts [--bai <slug|lesson_id>] [--chi-tiet] [--json]
//
// CHỈ ĐỌC: 1 truy vấn `lesson_items` (kind='ly_thuyet'), không ghi DB, không tạo file sao lưu.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { choKhacDauTien, chuanHoaNgoaiVideo, demKhoiVideo } from "./lib/video-html";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
function env(key: string): string | undefined {
  if (process.env[key]) return process.env[key];
  const p = path.join(root, ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const l = fs.readFileSync(p, "utf8").split("\n").find((x) => x.startsWith(`${key}=`));
  return l ? l.slice(key.length + 1).trim() : undefined;
}

const argv = process.argv.slice(2);
const JSON_OUT = argv.includes("--json");
const chiTiet = argv.includes("--chi-tiet"); // in cả đoạn khác nhau (mặc định chỉ in dòng tóm tắt)
const bi = argv.indexOf("--bai");
const only = bi >= 0 ? argv[bi + 1] : undefined;

const url = env("NEXT_PUBLIC_SUPABASE_URL");
const key = env("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) {
  console.error("thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY (cần chạy trên Mac)");
  process.exit(1);
}
const sb = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });

// slug → lesson_id, suy từ kho thí nghiệm (nguồn duy nhất nối thư mục bài với lesson_id)
const idTheoSlug = new Map<string, number>();
for (const name of fs.readdirSync(path.join(root, "content", "thi-nghiem"))) {
  if (!/^tn-.*\.json$/.test(name)) continue;
  const d = JSON.parse(fs.readFileSync(path.join(root, "content", "thi-nghiem", name), "utf8"));
  const m = /lesson-samples\/([^/]+)\//.exec(d.nguon_trong_bai ?? "");
  if (m && typeof d.lesson_id !== "undefined") idTheoSlug.set(m[1], d.lesson_id);
}

// 1 truy vấn duy nhất
const { data, error } = await sb.from("lesson_items").select("lesson_id, body_html").eq("kind", "ly_thuyet");
if (error) {
  console.error("Lỗi đọc DB:", error.message);
  process.exit(1);
}
const dbTheoLesson = new Map<number, string>();
for (const r of (data ?? []) as { lesson_id: number; body_html: string | null }[]) {
  dbTheoLesson.set(Number(r.lesson_id), r.body_html ?? "");
}

const goc = path.join(root, "content", "lesson-samples");
const khac: string[] = [];
const khop: string[] = [];
const khongCoDb: string[] = [];
for (const slug of fs.readdirSync(goc).sort()) {
  const f = path.join(goc, slug, "theory.html");
  if (!fs.existsSync(f)) continue;
  const lessonId = idTheoSlug.get(slug);
  if (!lessonId) continue;
  if (only && slug !== only && String(lessonId) !== only) continue;
  const fileHtml = fs.readFileSync(f, "utf8");
  const dbHtml = dbTheoLesson.get(lessonId);
  if (dbHtml === undefined) {
    khongCoDb.push(`${slug} (lesson ${lessonId}): DB không có mục Lý thuyết`);
    continue;
  }
  const a = chuanHoaNgoaiVideo(dbHtml);
  const b = chuanHoaNgoaiVideo(fileHtml);
  if (a === b) {
    khop.push(`${slug} (lesson ${lessonId}) — video: file ${demKhoiVideo(fileHtml)} · DB ${demKhoiVideo(dbHtml)}`);
  } else {
    const dong = `${slug} (lesson ${lessonId}) — khác ${Math.abs(a.length - b.length)} ký tự`;
    khac.push(chiTiet ? `${dong}\n${choKhacDauTien(a, b)}` : dong);
  }
}

if (JSON_OUT) {
  console.log(JSON.stringify({ khop: khop.length, khac: khac.length, khongCoDb: khongCoDb.length, chiTiet: { khac, khongCoDb } }, null, 1));
} else {
  console.log(`── KHỚP (file = DB, chỉ có thể khác khối video): ${khop.length} bài ──`);
  for (const k of khop) console.log(`✓ ${k}`);
  if (khongCoDb.length) {
    console.log(`\n── DB KHÔNG CÓ mục Lý thuyết: ${khongCoDb.length} ──`);
    for (const k of khongCoDb) console.log(`? ${k}`);
  }
  if (khac.length) {
    console.log(`\n── KHÁC NGOÀI KHỐI VIDEO: ${khac.length} bài (đừng đăng bằng --chi-video khi chưa xem) ──`);
    for (const k of khac) console.log(`✗ ${k}`);
  } else {
    console.log("\nKhông bài nào khác ngoài khối video.");
  }
}
process.exitCode = khac.length > 0 ? 1 : 0;
