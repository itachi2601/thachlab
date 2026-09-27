// Sinh "Tóm tắt ý chính cần thuộc" bằng AI cho các mục lý thuyết (lesson_items.kind =
// 'ly_thuyet') đang summary_html = '' — sau khi
// supabase/migrations/20260927120000_lesson_item_summary.sql đã chạy (chưa chạy thì cột
// không tồn tại, script báo lỗi ngay ở bước đọc).
//
// Ghi thẳng vào lesson_items.summary_html (không qua duyệt riêng). Chạy lại an toàn: chỉ
// xử lý các mục còn summary_html = '', không đụng mục đã có tóm tắt (kể cả do thầy tự sửa
// tay qua REST sau này).
//
// LƯU Ý: script này KHÔNG có chế độ dry-run — mỗi lần chạy ghi thẳng vào DB thật ngay (tốn
// lượt gọi Anthropic API + tiền). Muốn thử trước, truyền [số bài tối đa] nhỏ (vd 5) rồi tự
// xem lại trên trang /lop-hoc/bai (khối "📌 Tóm tắt ý chính cần thuộc" dưới tiêu đề mục lý
// thuyết) trước khi chạy không giới hạn — nhớ site export tĩnh, phải
// `bash scripts/deploy.sh` lại thì tóm tắt mới lên web thật.
//
//   npx tsx scripts/backfill-lesson-summary.mts [số bài tối đa]
//
// Cần .env.local có NEXT_PUBLIC_SUPABASE_URL, và hỏi SUPABASE_SERVICE_ROLE_KEY +
// ANTHROPIC_API_KEY nếu chưa có trong env/.env.local.

import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const MODEL = "claude-haiku-4-5";

function readEnvLocal(key: string): string | undefined {
  const envPath = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(envPath)) return undefined;
  const line = fs
    .readFileSync(envPath, "utf8")
    .split("\n")
    .find((l) => l.startsWith(`${key}=`));
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

interface ItemRow {
  id: number;
  title: string;
  body_html: string;
}

const SYSTEM_PROMPT =
  "Bạn là trợ lý soạn tóm tắt ôn thi Vật lý THPT. Đọc bài lý thuyết (HTML) rồi trích ra " +
  "PHẦN CẦN THUỘC LÒNG — định nghĩa cốt lõi, công thức, đơn vị, hằng số, điều kiện áp dụng — " +
  "bỏ hết phần diễn giải/ví dụ/dẫn dắt. Trả về DUY NHẤT một khối HTML dạng " +
  '"<ul><li>…</li><li>…</li></ul>", 5–10 gạch đầu dòng, mỗi dòng ngắn gọn 1 ý. Giữ NGUYÊN cú ' +
  "pháp công thức kiểu Azota đã có trong bài ($...$ cho công thức trong dòng, $$...$$ cho công " +
  "thức riêng dòng) — không đổi sang cú pháp khác, không thêm \\( \\) hay markdown. Không kèm " +
  "lời giải thích, không bọc trong markdown code fence, không thêm tiêu đề.";

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/** Thử lại tối đa 2 lần khi mạng chập chờn ("fetch failed") — lỗi HTTP thật (401/400…) thì báo luôn. */
async function withRetry<T>(fn: () => Promise<T>, label: string): Promise<T> {
  let lastErr: unknown;
  for (let attempt = 1; attempt <= 3; attempt += 1) {
    try {
      return await fn();
    } catch (e) {
      lastErr = e;
      if (attempt < 3) {
        console.error(`  ${label} lỗi (lần ${attempt}): ${e instanceof Error ? e.message : String(e)} — thử lại…`);
        await sleep(1500 * attempt);
      }
    }
  }
  throw lastErr;
}

async function summarizeOne(apiKey: string, bodyHtml: string): Promise<string> {
  const res = await withRetry(
    () =>
      fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "content-type": "application/json",
          "x-api-key": apiKey,
          "anthropic-version": "2023-06-01",
        },
        body: JSON.stringify({
          model: MODEL,
          max_tokens: 1024,
          system: SYSTEM_PROMPT,
          messages: [{ role: "user", content: bodyHtml }],
        }),
      }),
    "Gọi AI",
  );
  if (!res.ok) throw new Error(`Anthropic API lỗi ${res.status}: ${await res.text()}`);
  const data = (await res.json()) as { content?: { type: string; text?: string }[] };
  const textBlock = data.content?.find((b) => b.type === "text");
  let html = (textBlock?.text ?? "").trim();
  // Phòng khi model vẫn bọc code fence dù đã dặn — bóc ra cho chắc.
  html = html.replace(/^```(?:html)?\s*/i, "").replace(/```\s*$/, "").trim();
  if (!/^<ul/i.test(html)) throw new Error("AI không trả về đúng khối <ul> như yêu cầu.");
  return html;
}

async function main() {
  const limit = process.argv[2] ? Number(process.argv[2]) : undefined;

  const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
  if (!url) fail("không đọc được NEXT_PUBLIC_SUPABASE_URL từ .env.local");
  const serviceKey =
    process.env.SUPABASE_SERVICE_ROLE_KEY ??
    readEnvLocal("SUPABASE_SERVICE_ROLE_KEY") ??
    (await askHidden("Dán SUPABASE_SERVICE_ROLE_KEY (Settings → API → service_role): "));
  if (!serviceKey) fail("thiếu SUPABASE_SERVICE_ROLE_KEY");
  const anthropicKey =
    process.env.ANTHROPIC_API_KEY ??
    readEnvLocal("ANTHROPIC_API_KEY") ??
    (await askHidden("Dán ANTHROPIC_API_KEY: "));
  if (!anthropicKey) fail("thiếu ANTHROPIC_API_KEY");

  const supabase = createClient(url, serviceKey, { auth: { autoRefreshToken: false, persistSession: false } });

  let done = 0;
  const failedIds = new Set<number>();
  for (;;) {
    if (limit && done + failedIds.size >= limit) break;

    const { data, error } = await supabase
      .from("lesson_items")
      .select("id, title, body_html")
      .eq("kind", "ly_thuyet")
      .eq("summary_html", "")
      .neq("body_html", "")
      .order("id")
      .limit(50);
    if (error) fail(`đọc lesson_items lỗi: ${error.message} (đã chạy migration summary_html chưa?)`);
    const allRows = (data ?? []) as ItemRow[];
    if (done === 0 && failedIds.size === 0) console.log(`Còn ít nhất ${allRows.length}${allRows.length === 50 ? "+" : ""} mục lý thuyết chưa có tóm tắt.`);
    const rows = allRows.filter((r) => !failedIds.has(r.id)).slice(0, limit ? limit - done - failedIds.size : undefined);
    if (rows.length === 0) break;

    for (const row of rows) {
      console.log(`\n#${row.id} — ${row.title}…`);
      let summary: string;
      try {
        summary = await summarizeOne(anthropicKey, row.body_html);
      } catch (e) {
        console.error("  Lỗi gọi AI:", e instanceof Error ? e.message : String(e));
        failedIds.add(row.id);
        continue;
      }
      try {
        await withRetry(async () => {
          const { error: updErr } = await supabase
            .from("lesson_items")
            .update({ summary_html: summary })
            .eq("id", row.id);
          if (updErr) throw new Error(updErr.message);
        }, `Ghi mục #${row.id}`);
      } catch (e) {
        console.error(`  Lỗi ghi mục #${row.id}:`, e instanceof Error ? e.message : String(e));
        failedIds.add(row.id);
        continue;
      }
      done += 1;
      console.log(`  ✓ đã ghi luỹ kế ${done}, bỏ qua luỹ kế ${failedIds.size}.`);
    }
  }
  console.log(
    `\nHoàn tất: ${done} mục đã có tóm tắt, ${failedIds.size} mục bỏ qua (AI lỗi — xem log ở trên, sửa tay qua REST nếu cần).`,
  );
}

main().catch((err) => fail(err instanceof Error ? err.message : String(err)));
