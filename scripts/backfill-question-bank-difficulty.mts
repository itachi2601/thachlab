// Gợi ý mức độ (Dễ/Trung bình/Khó) bằng AI cho các câu trong ngân hàng câu hỏi đang
// difficulty = '' (chưa gắn) — sau khi docs/supabase-migration-question-bank-difficulty.sql
// VÀ supabase/migrations/20260925150000_difficulty_source.sql đã chạy (nếu chưa chạy, cập
// nhật ở đây sẽ không đồng bộ ngược về đề gốc / lỗi cột difficulty_source không tồn tại).
//
// Ghi thẳng vào question_bank.difficulty + difficulty_source = 'ai' (không qua duyệt riêng)
// — trigger sẽ tự đồng bộ ngược vào exams.questions của mọi đề đang chứa đúng câu đó (kèm
// key difficultySource). Chạy lại an toàn: chỉ xử lý các câu còn difficulty = '', không đụng
// câu đã có mức độ (kể cả do thầy tự gắn tay).
//
// LƯU Ý: script này KHÔNG có chế độ dry-run — mỗi lần chạy ghi thẳng vào DB thật ngay (tốn
// lượt gọi Anthropic API + tiền). Muốn thử trước, truyền [số câu tối đa] nhỏ (vd 20) rồi tự
// xem lại vài dòng trong /quan-tri/ngan-hang-cau-hoi trước khi chạy không giới hạn.
//
//   npx tsx scripts/backfill-question-bank-difficulty.mts [số câu tối đa]
//
// Cần .env.local có NEXT_PUBLIC_SUPABASE_URL, và hỏi SUPABASE_SERVICE_ROLE_KEY +
// ANTHROPIC_API_KEY nếu chưa có trong env/.env.local.

import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";
import { questionTextForAi } from "@/services/exam-question-text";
import type { ExamQuestion } from "@/features/exams/types";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const BATCH_SIZE = 40;
const MODEL = "claude-haiku-4-5";
const DIFFICULTIES = ["de", "trung-binh", "kho"] as const;
type Difficulty = (typeof DIFFICULTIES)[number];

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

interface BankRow {
  id: number;
  question: ExamQuestion;
}

function buildPrompt(items: { i: number; text: string }[]): string {
  const list = items.map((it) => `--- Câu (index=${it.i}) ---\n${it.text}`).join("\n\n");
  return (
    `Đánh giá độ khó với học sinh THPT trung bình cho từng câu hỏi Vật lý dưới đây, chọn đúng 1 ` +
    `trong 3 mức: "de" (nhận biết/áp dụng công thức trực tiếp, 1 bước tính), "trung-binh" (cần 2-3 ` +
    `bước biến đổi hoặc kết hợp 2 khái niệm), "kho" (nhiều bước, đồ thị/tình huống phức tạp, hoặc dễ ` +
    `nhầm lẫn).\n\n${list}`
  );
}

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

async function classifyBatch(apiKey: string, items: { i: number; text: string }[]): Promise<Map<number, Difficulty>> {
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
          max_tokens: 4096,
          system:
            "Bạn là trợ lý đánh giá độ khó câu hỏi trắc nghiệm Vật lý THPT. Chỉ trả về DUY NHẤT một JSON " +
            'hợp lệ đúng dạng {"results":[{"index":0,"difficulty":"de"}]}, không kèm lời giải thích, ' +
            "không bọc trong markdown code fence.",
          messages: [{ role: "user", content: buildPrompt(items) }],
        }),
      }),
    "Gọi AI",
  );
  if (!res.ok) throw new Error(`Anthropic API lỗi ${res.status}: ${await res.text()}`);
  const data = (await res.json()) as { content?: { type: string; text?: string }[] };
  const textBlock = data.content?.find((b) => b.type === "text");
  const raw = textBlock?.text ?? "";
  const start = raw.indexOf("{");
  const end = raw.lastIndexOf("}");
  if (start < 0 || end < 0) throw new Error("AI không trả về JSON hợp lệ.");
  const parsed = JSON.parse(raw.slice(start, end + 1)) as { results?: unknown };
  const rows = Array.isArray(parsed.results) ? parsed.results : [];
  const validIdx = new Set(items.map((it) => it.i));
  const out = new Map<number, Difficulty>();
  for (const row of rows) {
    if (!row || typeof row !== "object") continue;
    const r = row as Record<string, unknown>;
    const index = Number(r.index);
    if (!validIdx.has(index)) continue;
    if (typeof r.difficulty === "string" && (DIFFICULTIES as readonly string[]).includes(r.difficulty)) {
      out.set(index, r.difficulty as Difficulty);
    }
  }
  return out;
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

  // PostgREST/supabase-js giới hạn mặc định 1000 dòng/lần đọc — lặp lại việc đọc "1000 câu còn
  // trống kế tiếp" cho tới khi hết hoặc chạm `limit` (nếu có), vì câu đã ghi xong không còn khớp
  // difficulty = '' nên mỗi lần đọc lại tự nhiên lấy đúng phần chưa xử lý, không cần offset.
  const PAGE_SIZE = 1000;
  let done = 0;
  let batchNo = 0;
  // Câu ghi lỗi vẫn còn difficulty = '' nên sẽ nổi lại ở lần đọc trang kế tiếp — nhớ id đã thử
  // hỏng trong lượt chạy này để không lặp vô hạn trên đúng những câu không xử lý được.
  const failedIds = new Set<number>();
  for (;;) {
    if (limit && done + failedIds.size >= limit) break;

    const { data, error } = await supabase
      .from("question_bank")
      .select("id, question")
      .eq("difficulty", "")
      .eq("archived", false)
      .order("id")
      .limit(PAGE_SIZE);
    if (error) fail(`đọc question_bank lỗi: ${error.message}`);
    const allRows = (data ?? []) as BankRow[];
    if (batchNo === 0) console.log(`Còn ít nhất ${allRows.length}${allRows.length === PAGE_SIZE ? "+" : ""} câu chưa gắn mức độ.`);
    const rows = allRows.filter((r) => !failedIds.has(r.id)).slice(0, limit ? limit - done - failedIds.size : undefined);
    if (rows.length === 0) break;

    for (let start = 0; start < rows.length; start += BATCH_SIZE) {
      const batch = rows.slice(start, start + BATCH_SIZE);
      const items = batch.map((r, i) => ({ i, text: questionTextForAi(r.question) }));
      batchNo += 1;
      console.log(`\nLô ${batchNo}: ${batch.length} câu…`);
      let results: Map<number, Difficulty>;
      try {
        results = await classifyBatch(anthropicKey, items);
      } catch (e) {
        console.error("  Lỗi gọi AI:", e instanceof Error ? e.message : String(e));
        batch.forEach((r) => failedIds.add(r.id));
        continue;
      }
      for (let i = 0; i < batch.length; i += 1) {
        const difficulty = results.get(i);
        if (!difficulty) {
          failedIds.add(batch[i].id);
          continue;
        }
        try {
          await withRetry(async () => {
            const { error: updErr } = await supabase
              .from("question_bank")
              .update({ difficulty, difficulty_source: "ai" })
              .eq("id", batch[i].id);
            if (updErr) throw new Error(updErr.message);
          }, `Ghi câu #${batch[i].id}`);
        } catch (e) {
          console.error(`  Lỗi ghi câu #${batch[i].id}:`, e instanceof Error ? e.message : String(e));
          failedIds.add(batch[i].id);
          continue;
        }
        done += 1;
      }
      console.log(`  ✓ đã ghi luỹ kế ${done}, bỏ qua luỹ kế ${failedIds.size}.`);
    }
  }
  console.log(
    `\nHoàn tất: ${done} câu đã gắn mức độ, ${failedIds.size} câu bỏ qua (AI không chắc hoặc lỗi — gắn tay ở /quan-tri/ngan-hang-cau-hoi).`,
  );
}

main().catch((err) => fail(err instanceof Error ? err.message : String(err)));
