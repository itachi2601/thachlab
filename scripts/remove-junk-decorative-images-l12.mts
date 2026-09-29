// Xoá ảnh trang trí vô nghĩa (mockup "thanh tiêu đề cửa sổ trình duyệt" màu cam/xanh navy —
// vốn là ảnh minh hoạ style tiêu đề trong file Word gốc của GV, không phải hình vật lý) khỏi
// body_html của 6 mục lý thuyết Lớp 12 chương Từ trường + Điện từ (lesson_id 11,13,14,125,126,127).
// Nhận diện bằng cách so khớp MD5 nội dung ảnh đã tải lên Supabase Storage với 9 hash đã xác
// nhận bằng mắt (xem output/*/media/d0N.png tương ứng) — KHÔNG đoán theo tên file (vd d01.png ở
// bai14-may-bien-ap lại là ảnh thật, không phải trang trí).
//
//   npx tsx scripts/remove-junk-decorative-images-l12.mts            # dry-run
//   npx tsx scripts/remove-junk-decorative-images-l12.mts --write    # ghi thật (tự backup)

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

// 17 URL đã xác nhận đúng là ảnh trang trí (đối chiếu MD5 với 9 file gốc đã xem bằng mắt).
const JUNK_URLS = [
  "https://fxnqgmfqdbvnjawgnsfi.supabase.co/storage/v1/object/public/lesson-media/11/1790352876656-d01.png",
  "https://fxnqgmfqdbvnjawgnsfi.supabase.co/storage/v1/object/public/lesson-media/11/1790352878072-d02.png",
  "https://fxnqgmfqdbvnjawgnsfi.supabase.co/storage/v1/object/public/lesson-media/125/1790353303576-d01.png",
  "https://fxnqgmfqdbvnjawgnsfi.supabase.co/storage/v1/object/public/lesson-media/125/1790353312830-d02.png",
  "https://fxnqgmfqdbvnjawgnsfi.supabase.co/storage/v1/object/public/lesson-media/125/1790353439033-d01.png",
  "https://fxnqgmfqdbvnjawgnsfi.supabase.co/storage/v1/object/public/lesson-media/126/1790353596249-d01.png",
  "https://fxnqgmfqdbvnjawgnsfi.supabase.co/storage/v1/object/public/lesson-media/126/1790353597336-d02.png",
  "https://fxnqgmfqdbvnjawgnsfi.supabase.co/storage/v1/object/public/lesson-media/126/1790353598950-d03.png",
  "https://fxnqgmfqdbvnjawgnsfi.supabase.co/storage/v1/object/public/lesson-media/127/1790353642018-d01.png",
  "https://fxnqgmfqdbvnjawgnsfi.supabase.co/storage/v1/object/public/lesson-media/127/1790353642411-d02.png",
  "https://fxnqgmfqdbvnjawgnsfi.supabase.co/storage/v1/object/public/lesson-media/127/1790353655853-d03.png",
  "https://fxnqgmfqdbvnjawgnsfi.supabase.co/storage/v1/object/public/lesson-media/13/1790353042899-d01.png",
  "https://fxnqgmfqdbvnjawgnsfi.supabase.co/storage/v1/object/public/lesson-media/13/1790353043496-d02.png",
  "https://fxnqgmfqdbvnjawgnsfi.supabase.co/storage/v1/object/public/lesson-media/13/1790353054188-d03.png",
  "https://fxnqgmfqdbvnjawgnsfi.supabase.co/storage/v1/object/public/lesson-media/13/1790353237468-d01.png",
  "https://fxnqgmfqdbvnjawgnsfi.supabase.co/storage/v1/object/public/lesson-media/14/1790353278357-d01.png",
  "https://fxnqgmfqdbvnjawgnsfi.supabase.co/storage/v1/object/public/lesson-media/14/1790353285395-d01.png",
];

const THEORY_ITEM_IDS = [52, 66, 141, 143, 145, 183];

function escapeRe(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function removeJunkImages(html: string): { html: string; removed: number } {
  let removed = 0;
  let out = html;
  for (const url of JUNK_URLS) {
    if (!out.includes(url)) continue;
    // Ưu tiên xoá cả <p> nếu ảnh này là NỘI DUNG DUY NHẤT của đoạn đó (không có chữ nào khác).
    const wholeParaRe = new RegExp(`<p[^>]*>\\s*<img[^>]*src="${escapeRe(url)}"[^>]*>\\s*</p>`, "g");
    const before = out;
    out = out.replace(wholeParaRe, "");
    if (out !== before) {
      removed++;
      continue;
    }
    // Nếu ảnh nằm chung đoạn với chữ khác — chỉ xoá riêng thẻ <img>, giữ nguyên phần chữ.
    const imgOnlyRe = new RegExp(`<img[^>]*src="${escapeRe(url)}"[^>]*>`, "g");
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

  const backup: Record<string, unknown> = {};
  let totalRemoved = 0;

  for (const id of THEORY_ITEM_IDS) {
    const { data: row, error } = await readClient.from("lesson_items").select("id, kind, body_html").eq("id", id).single();
    if (error) throw new Error(`đọc #${id}: ${error.message}`);
    if (!row || row.kind !== "ly_thuyet") throw new Error(`#${id} không phải ly_thuyet — dừng.`);
    const { html: newHtml, removed } = removeJunkImages(row.body_html ?? "");
    totalRemoved += removed;
    console.log(`#${id}: xoá ${removed} ảnh trang trí  (${(row.body_html ?? "").length} → ${newHtml.length} ký tự)`);
    if (!write) continue;
    backup[`theory_${id}`] = { id, body_html: row.body_html };
    const { error: updErr } = await writeClient!.from("lesson_items").update({ body_html: newHtml }).eq("id", id);
    if (updErr) throw new Error(`update #${id}: ${updErr.message}`);
  }

  console.log(`\nTổng: xoá ${totalRemoved}/${JUNK_URLS.length} ảnh trang trí.`);
  if (write) {
    fs.mkdirSync(LOG_DIR, { recursive: true });
    const p = path.join(LOG_DIR, `remove-junk-images-backup-${Date.now()}.json`);
    fs.writeFileSync(p, JSON.stringify(backup, null, 2), "utf8");
    console.log(`Đã backup vào ${path.relative(process.cwd(), p)}.`);
    console.log(`Nhớ chạy: node scripts/build-content.mjs`);
  } else {
    console.log("[dry-run] chưa ghi gì. Chạy lại kèm --write để ghi thật.");
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
