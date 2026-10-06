// Đăng tin tức Vật lí / học thuật (scripts/data/tin-tuc/*.json, do skill dang-tin-tuc-vat-ly soạn) lên bảng `posts`
// qua RPC create_post_with_targets — hiện ở /tin-tuc. Mặc định là DRY-RUN; thêm --yes mới ghi thật.
// CHẠY TRÊN MAC (cần service role). /tin-tuc đọc Supabase lúc chạy nên KHÔNG cần deploy.
//
//   npx tsx scripts/dang-tin-tuc.mts                    # dry-run mọi file chưa đăng
//   npx tsx scripts/dang-tin-tuc.mts --file 2026-10-06-x.json --yes
//   npx tsx scripts/dang-tin-tuc.mts --yes              # đăng mọi file hợp lệ chưa đăng
//
// File JSON: { title, body_html, source_url, source_name, subject_code?, class_ids?, content_type?, video_url? }

import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const DIR = path.join(root, "scripts", "data", "tin-tuc");

function envLocal(key: string): string | undefined {
  const p = path.join(root, ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const line = fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}
function fail(m: string): never { console.error("Lỗi:", m); process.exit(1); }

const argv = process.argv.slice(2);
const yes = argv.includes("--yes");
const only = argv.includes("--file") ? argv[argv.indexOf("--file") + 1] : null;

interface News {
  title: string; body_html: string; source_url: string; source_name: string;
  subject_code?: string; class_ids?: number[]; content_type?: string; video_url?: string;
  posted_id?: number;
}

function check(n: News): string[] {
  const e: string[] = [];
  if (!n.title || n.title.length > 140) e.push("title trống hoặc > 140 ký tự");
  if (!n.body_html || n.body_html.length < 200) e.push("body_html quá ngắn (<200 ký tự)");
  if (n.body_html.length > 3500) e.push("body_html quá dài (>3500 ký tự) — tin phải ngắn, bài sâu để vào Blog");
  if (!/^https:\/\//.test(n.source_url ?? "")) e.push("source_url phải là https://");
  if (!n.source_name) e.push("thiếu source_name");
  if (n.body_html && !n.body_html.includes(n.source_url)) e.push("body_html phải chứa link nguồn (source_url)");
  if (/\n/.test(n.body_html ?? "")) e.push("body_html có xuống dòng — /tin-tuc dùng pre-wrap nên sẽ thừa dòng trống; viết liền một dòng");
  if (/<script|onerror=|onclick=|javascript:/i.test(n.body_html ?? "")) e.push("body_html có mã script");
  if (/data:image/i.test(n.body_html ?? "")) e.push("không nhúng base64");
  if (n.subject_code && !["vat-ly", "hoa-hoc", "sinh-hoc"].includes(n.subject_code)) e.push("subject_code không hợp lệ");
  if (n.content_type && !["thong_bao", "tai_lieu", "video"].includes(n.content_type)) e.push("content_type không hợp lệ");
  return e;
}

const files = fs.existsSync(DIR) ? fs.readdirSync(DIR).filter((f) => f.endsWith(".json")).sort() : [];
const todo = files.filter((f) => (only ? f === only : true));
if (todo.length === 0) fail("không có file nào trong scripts/data/tin-tuc/");

const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? envLocal("NEXT_PUBLIC_SUPABASE_URL");
const key = process.env.SUPABASE_SERVICE_ROLE_KEY ?? envLocal("SUPABASE_SERVICE_ROLE_KEY");
if (yes && (!url || !key)) fail("thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY");
const sb = url && key ? createClient(url, key) : null;

// Chống đăng trùng: cùng link nguồn hoặc cùng tiêu đề đã có trong posts.
let existing: { title: string; body: string }[] = [];
if (sb) {
  const { data, error } = await sb.from("posts").select("title, body").order("created_at", { ascending: false }).limit(500);
  if (error) fail(`không đọc được posts: ${error.message}`);
  existing = data ?? [];
} else console.log("(dry-run không có khoá DB → bỏ qua kiểm trùng với DB)\n");

let ok = 0, bad = 0, dup = 0;
for (const f of todo) {
  const fp = path.join(DIR, f);
  const n = JSON.parse(fs.readFileSync(fp, "utf8")) as News;
  if (n.posted_id) { console.log(`= ${f}: đã đăng (post ${n.posted_id})`); continue; }
  const errs = check(n);
  if (errs.length) { bad++; console.log(`✗ ${f}\n    - ${errs.join("\n    - ")}`); continue; }
  if (existing.some((p) => p.title.trim() === n.title.trim() || (p.body ?? "").includes(n.source_url))) {
    dup++; console.log(`≈ ${f}: TRÙNG tin đã có trong DB (cùng tiêu đề hoặc link nguồn) — bỏ qua`); continue;
  }
  console.log(`${yes ? "→ đăng" : "○ sẽ đăng"} ${f}: "${n.title}" [${n.subject_code ?? "vat-ly"}, ${(n.class_ids ?? []).length ? "lớp " + n.class_ids!.join(",") : "toàn trường"}] · ${n.body_html.length} ký tự`);
  if (!yes) { ok++; continue; }
  const { data, error } = await sb!.rpc("create_post_with_targets", {
    p_title: n.title, p_body: n.body_html, p_video_url: n.video_url ?? "",
    p_content_type: n.content_type ?? "thong_bao", p_subject_code: n.subject_code ?? "vat-ly",
    p_class_ids: n.class_ids ?? [], p_course_ids: [],
  });
  if (error) { bad++; console.log(`  ✗ RPC lỗi: ${error.message}`); continue; }
  n.posted_id = data as number;
  fs.writeFileSync(fp, JSON.stringify(n, null, 2) + "\n");
  const { data: row } = await sb!.from("posts").select("published").eq("id", data as number).single();
  ok++; console.log(`  ✓ post ${data} — ${row?.published ? "ĐANG HIỆN" : "đang ẨN (bật Hiện ở /quan-tri/bai-dang)"}`);
}
console.log(`\n${yes ? "Đã đăng" : "Hợp lệ"}: ${ok} · lỗi: ${bad} · trùng: ${dup}`);
if (!yes && ok) console.log("Thêm --yes để ghi thật. Hoàn tác: xoá dòng trong /quan-tri/bai-dang (bài đăng chưa hiện nếu published=false).");
process.exit(bad ? 1 : 0);
