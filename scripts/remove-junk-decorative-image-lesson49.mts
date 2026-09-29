// Xoá 4 ảnh trang trí vô nghĩa (mockup thanh tiêu đề cửa sổ, không phải hình vật lý) khỏi
// lesson_items#90 (lesson_id=49, "Độ dịch chuyển, quãng đường đi được" — Lớp 10) — phát hiện khi
// thầy yêu cầu rà lại toàn bộ Lớp 10+11 sau đợt sửa Lớp 12 Từ trường/Điện từ. Ảnh phục vụ qua
// đường dẫn local public/lessons/do-dich-chuyen-quang-duong-di-duoc/media/d0N.png (không phải
// Supabase Storage), khớp đúng cùng loại mockup đã xác nhận ở
// scripts/remove-junk-decorative-images-l12.mts (d01/d02/d04 khớp hash cũ, d03 là biến thể mới
// cùng kiểu, đã xem bằng mắt xác nhận).
//
//   npx tsx scripts/remove-junk-decorative-image-lesson49.mts            # dry-run
//   npx tsx scripts/remove-junk-decorative-image-lesson49.mts --write    # ghi thật (tự backup)

import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const LOG_DIR = path.resolve(scriptDir, "logs");

function readEnvLocal(key: string): string | undefined {
  const envPath = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(envPath)) return undefined;
  const line = fs.readFileSync(envPath, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}

const ITEM_ID = 90;
const JUNK_FILES = ["d01.png", "d02.png", "d03.png", "d04.png"];

function removeJunk(html: string): { html: string; removed: number } {
  let out = html;
  let removed = 0;
  for (const fname of JUNK_FILES) {
    const escFname = fname.replace(/\./g, "\\.");
    const wholeParaRe = new RegExp(`<p[^>]*>\\s*<img[^>]*src="[^"]*${escFname}"[^>]*>\\s*</p>`, "g");
    const before = out;
    out = out.replace(wholeParaRe, "");
    if (out !== before) { removed++; continue; }
    const imgOnlyRe = new RegExp(`<img[^>]*src="[^"]*${escFname}"[^>]*>`, "g");
    const before2 = out;
    out = out.replace(imgOnlyRe, "");
    if (out !== before2) removed++;
  }
  return { html: out, removed };
}

async function main() {
  const write = process.argv.includes("--write");
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
  if (!url) throw new Error("thiếu NEXT_PUBLIC_SUPABASE_URL");
  const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_ANON_KEY");
  if (!anonKey) throw new Error("thiếu NEXT_PUBLIC_SUPABASE_ANON_KEY");
  const serviceKey = write ? (process.env.SUPABASE_SERVICE_ROLE_KEY ?? readEnvLocal("SUPABASE_SERVICE_ROLE_KEY")) : undefined;
  if (write && !serviceKey) throw new Error("thiếu SUPABASE_SERVICE_ROLE_KEY (bắt buộc khi --write)");

  const readClient = createClient(url, serviceKey ?? anonKey, { auth: { autoRefreshToken: false, persistSession: false } });
  const writeClient = write ? createClient(url, serviceKey!, { auth: { autoRefreshToken: false, persistSession: false } }) : null;

  const { data: row, error } = await readClient.from("lesson_items").select("id, lesson_id, body_html").eq("id", ITEM_ID).single();
  if (error) throw new Error(`đọc #${ITEM_ID}: ${error.message}`);
  if (!row || row.lesson_id !== 49) throw new Error(`#${ITEM_ID} không khớp lesson_id=49 — dừng.`);

  const { html: newHtml, removed } = removeJunk(row.body_html ?? "");
  console.log(`#${ITEM_ID}: xoá ${removed}/4 ảnh trang trí  (${(row.body_html ?? "").length} → ${newHtml.length} ký tự)`);

  if (!write) {
    console.log("[dry-run] chưa ghi gì.");
    return;
  }
  fs.mkdirSync(LOG_DIR, { recursive: true });
  const p = path.join(LOG_DIR, `remove-junk-image-lesson49-backup-${Date.now()}.json`);
  fs.writeFileSync(p, JSON.stringify({ id: ITEM_ID, body_html: row.body_html }, null, 2), "utf8");
  const { error: updErr } = await writeClient!.from("lesson_items").update({ body_html: newHtml }).eq("id", ITEM_ID);
  if (updErr) throw new Error(`update #${ITEM_ID}: ${updErr.message}`);
  console.log(`Đã ghi + backup vào ${path.relative(process.cwd(), p)}. Nhớ chạy: node scripts/build-content.mjs`);
}

main().catch((e) => { console.error(e); process.exit(1); });
