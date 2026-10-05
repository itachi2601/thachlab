// Gắn nhãn Chủ đề (yêu cầu cần đạt) + Dạng (lý thuyết/bài tập) cho các câu trong
// question_bank đang topic_name = '' — cùng việc mà nút "AI gắn nhãn" ở trang
// /quan-tri/ngan-hang-cau-hoi làm, nhưng chạy hàng loạt và không cần phiên đăng nhập.
//
// CÁCH LÀM: mỗi lượt gọi DeepSeek một lô tối đa 40 câu, CHỈ trong cùng một khối lớp (danh mục
// YCCĐ gửi kèm là danh mục của đúng khối đó — giống hệt danh mục mà trang ngân hàng đưa cho AI),
// và kiểm tra lại phía script: nhãn trả về phải khớp NGUYÊN VĂN một tên trong danh mục, form phải
// là 'ly_thuyet' | 'bai_tap'. Câu nào AI không trả nhãn hợp lệ thì BỎ QUA, không đoán bừa.
//
// KHÔNG cần script tự đồng bộ sang đề gốc: ghi topic_name vào question_bank là trigger DB
// (trg_bank_touch + trg_bank_tags_to_exams, migration 20260925150000_difficulty_source.sql) tự
// tra topic_id theo tên, tự điền lại grade/subject_code theo danh mục, và tự vá `topic`/`form`
// vào mọi hàng exams.questions có cùng content_hash. Vì vậy script chỉ UPDATE đúng 2 cột.
//
// Câu trong ngân hàng KHÔNG có grade (hiện 141 câu, phần lớn từ đề "Kiểm tra hiểu bài" soạn
// trước khi gắn khối) không suy ra được danh mục YCCĐ nào → mặc định BỎ QUA; muốn xử lý thì gắn
// khối cho chúng ở trang ngân hàng (nút sửa khối) rồi chạy lại.
//
//   npx tsx scripts/backfill-question-bank-topics.mts --dry-run        # chỉ in + ghi log, KHÔNG ghi DB
//   npx tsx scripts/backfill-question-bank-topics.mts 40               # thử 40 câu rồi xem lại trên web
//   npx tsx scripts/backfill-question-bank-topics.mts                  # chạy hết phần còn thiếu
//   npx tsx scripts/backfill-question-bank-topics.mts --grade=12       # chỉ một khối
//   npx tsx scripts/backfill-question-bank-topics.mts --undo scripts/logs/backfill-bank-topics-<...>.json
//
// Mỗi lượt chạy đều ghi log JSON (đề xuất/đã ghi từng câu) vào scripts/logs/ — dùng để rà lại
// bằng mắt, và để hoàn tác bằng --undo (chỉ hoàn tác câu mà nhãn hiện tại vẫn đúng như lúc ghi,
// không đè lên câu thầy đã sửa tay sau đó).
//
// Cần .env.local có NEXT_PUBLIC_SUPABASE_URL + DEEPSEEK_API_KEY, và
// SUPABASE_SERVICE_ROLE_KEY (hỏi nếu thiếu). Script chỉ chạm các câu đang TRỐNG nhãn nên chạy
// lại nhiều lần vẫn an toàn.

import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";
import { questionTextForAi } from "@/services/exam-question-text";
import type { ExamQuestion } from "@/features/exams/types";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const LOG_DIR = path.resolve(scriptDir, "logs");
const BATCH_SIZE = 40;
const MODEL = "deepseek-flash";
const API_URL = "https://api.deepseek.com/chat/completions";
const FORMS = ["ly_thuyet", "bai_tap"] as const;
type Form = (typeof FORMS)[number];

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
    rlAny._writeToOutput = (chunk) =>
      (rl as unknown as { output: NodeJS.WritableStream }).output.write(rlAny.stdoutMuted ? "*" : chunk);
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

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/** Thử lại tối đa 2 lần khi mạng chập chờn — lỗi HTTP thật (401/400…) thì báo luôn. */
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

interface BankRow {
  id: number;
  grade: string;
  subject_code: string | null;
  form: string | null;
  question: ExamQuestion;
  source_exam_id: number | null;
}

interface Catalog {
  /** Tên YCCĐ theo đúng thứ tự trang ngân hàng đưa cho AI: mỗi chủ đề tầng bài rồi các YCCĐ con. */
  names: string[];
  set: Set<string>;
}

/** Danh mục YCCĐ của từng khối — giống cách trang ngân hàng dựng aiCandidateNames. */
async function loadCatalogs(supabase: SupabaseClient): Promise<Map<string, Catalog>> {
  const { data, error } = await supabase
    .from("question_topics")
    .select("id, grade, parent_id, name, sort_order")
    .order("sort_order")
    .order("name");
  if (error) fail(`đọc question_topics lỗi: ${error.message}`);
  const rows = (data ?? []) as { id: number; grade: string; parent_id: number | null; name: string; sort_order: number }[];
  const byGrade = new Map<string, typeof rows>();
  for (const r of rows) {
    const arr = byGrade.get(r.grade) ?? [];
    arr.push(r);
    byGrade.set(r.grade, arr);
  }
  const out = new Map<string, Catalog>();
  for (const [grade, list] of byGrade) {
    const parents = list.filter((t) => t.parent_id === null);
    const names: string[] = [];
    for (const p of parents) {
      names.push(p.name);
      for (const c of list.filter((t) => t.parent_id === p.id)) names.push(c.name);
    }
    // Chủ đề con mồ côi (thiếu cha) vẫn phải có trong danh mục, tránh bỏ sót.
    for (const t of list) if (!names.includes(t.name)) names.push(t.name);
    out.set(grade, { names, set: new Set(names) });
  }
  return out;
}

function buildPrompt(items: { i: number; text: string; source?: string }[], topics: string[]): string {
  const topicList = topics.map((t, i) => `${i + 1}. ${t}`).join("\n");
  const itemList = items
    .map((it) => {
      const src = it.source ? `(Nguồn: ${it.source})\n` : "";
      return `--- Câu (index=${it.i}) ---\n${src}${it.text}`;
    })
    .join("\n\n");
  return (
    `Danh mục yêu cầu cần đạt (chỉ được chọn NGUYÊN VĂN một mục trong danh sách này cho mỗi câu, ` +
    `không tự đặt tên mới, không sửa chính tả):\n${topicList}\n\n` +
    `Phân loại từng câu hỏi Vật lý THPT dưới đây: chọn đúng 1 yêu cầu cần đạt phù hợp nhất trong ` +
    `danh mục trên, và xác định "form" là "ly_thuyet" (câu hỏi lý thuyết/khái niệm/định nghĩa, ` +
    `không cần tính toán) hoặc "bai_tap" (câu có số liệu/công thức/tính toán để ra đáp số). ` +
    `Dòng "(Nguồn: ...)" là tên đề gốc, chỉ để tham khảo thêm — vẫn phải chọn theo nội dung câu.` +
    `\n\n${itemList}`
  );
}

async function classifyBatch(
  apiKey: string,
  topics: string[],
  items: { i: number; text: string; source?: string }[],
): Promise<Map<number, { topic: string; form?: Form }>> {
  const res = await withRetry(
    () =>
      fetch(API_URL, {
        method: "POST",
        headers: { "content-type": "application/json", authorization: `Bearer ${apiKey}` },
        body: JSON.stringify({
          model: MODEL,
          max_tokens: 8192,
          temperature: 0,
          // Việc này chỉ là phân loại JSON ngắn — thinking chỉ tốn token/thời gian.
          thinking: { type: "disabled" },
          response_format: { type: "json_object" },
          messages: [
            {
              role: "system",
              content:
                "Bạn là trợ lý phân loại câu hỏi trắc nghiệm Vật lý THPT theo yêu cầu cần đạt (YCCĐ). " +
                "Chỉ trả về DUY NHẤT một JSON hợp lệ đúng dạng " +
                '{"results":[{"index":0,"topic":"...","form":"ly_thuyet"}]}, ' +
                "không kèm lời giải thích, không bọc trong markdown code fence.",
            },
            { role: "user", content: buildPrompt(items, topics) },
          ],
        }),
      }),
    "Gọi AI",
  );
  if (!res.ok) throw new Error(`DeepSeek API lỗi ${res.status}: ${(await res.text()).slice(0, 300)}`);
  const data = (await res.json()) as { choices?: { message?: { content?: string | null } }[] };
  const raw = data.choices?.[0]?.message?.content ?? "";
  const start = raw.indexOf("{");
  const end = raw.lastIndexOf("}");
  if (start < 0 || end < 0) throw new Error("AI không trả về JSON hợp lệ.");
  const parsed = JSON.parse(raw.slice(start, end + 1)) as { results?: unknown };
  const validIdx = new Set(items.map((it) => it.i));
  const out = new Map<number, { topic: string; form?: Form }>();
  for (const row of Array.isArray(parsed.results) ? parsed.results : []) {
    if (!row || typeof row !== "object") continue;
    const r = row as Record<string, unknown>;
    const index = Number(r.index);
    if (!validIdx.has(index)) continue;
    if (typeof r.topic !== "string" || !r.topic.trim()) continue;
    const form =
      typeof r.form === "string" && (FORMS as readonly string[]).includes(r.form) ? (r.form as Form) : undefined;
    out.set(index, { topic: r.topic.trim(), form });
  }
  return out;
}

interface LogItem {
  id: number;
  before: { topic_name: string; form: string };
  after: { topic_name: string; form: string };
}

async function undo(logPath: string): Promise<void> {
  if (!fs.existsSync(logPath)) fail(`không thấy file log: ${logPath}`);
  const log = JSON.parse(fs.readFileSync(logPath, "utf8")) as { items?: LogItem[] };
  const items = log.items ?? [];
  if (items.length === 0) fail("file log không có câu nào để hoàn tác.");

  const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
  if (!url) fail("không đọc được NEXT_PUBLIC_SUPABASE_URL từ .env.local");
  const serviceKey =
    process.env.SUPABASE_SERVICE_ROLE_KEY ??
    readEnvLocal("SUPABASE_SERVICE_ROLE_KEY") ??
    (await askHidden("Dán SUPABASE_SERVICE_ROLE_KEY (Settings → API → service_role): "));
  if (!serviceKey) fail("thiếu SUPABASE_SERVICE_ROLE_KEY");
  const supabase = createClient(url, serviceKey, { auth: { autoRefreshToken: false, persistSession: false } });

  console.log(`Hoàn tác ${items.length} câu theo ${path.basename(logPath)} …`);
  let restored = 0;
  let kept = 0;
  for (const it of items) {
    // Chỉ hoàn tác khi nhãn hiện tại VẪN đúng như lúc script ghi (không đè lên sửa tay sau đó).
    const { data, error } = await supabase
      .from("question_bank")
      .update({ topic_name: it.before.topic_name, form: it.before.form })
      .eq("id", it.id)
      .eq("topic_name", it.after.topic_name)
      .select("id");
    if (error) {
      console.error(`  câu #${it.id} lỗi: ${error.message}`);
      continue;
    }
    if ((data ?? []).length > 0) restored += 1;
    else kept += 1;
  }
  console.log(`Xong: hoàn tác ${restored} câu, giữ nguyên ${kept} câu (nhãn đã khác — có người sửa tay).`);
}

async function main() {
  const argv = process.argv.slice(2);
  const undoIdx = argv.indexOf("--undo");
  if (undoIdx >= 0) {
    const logPath = argv[undoIdx + 1];
    if (!logPath) fail("--undo cần đường dẫn file log.");
    return undo(logPath);
  }

  const dryRun = argv.includes("--dry-run");
  const gradeFilter = argv.find((a) => a.startsWith("--grade="))?.slice("--grade=".length);
  const limitArg = argv.find((a) => /^\d+$/.test(a));
  const limit = limitArg ? Number(limitArg) : undefined;

  const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
  if (!url) fail("không đọc được NEXT_PUBLIC_SUPABASE_URL từ .env.local");
  const serviceKey =
    process.env.SUPABASE_SERVICE_ROLE_KEY ??
    readEnvLocal("SUPABASE_SERVICE_ROLE_KEY") ??
    (await askHidden("Dán SUPABASE_SERVICE_ROLE_KEY (Settings → API → service_role): "));
  if (!serviceKey) fail("thiếu SUPABASE_SERVICE_ROLE_KEY");
  const deepseekKey =
    process.env.DEEPSEEK_API_KEY ?? readEnvLocal("DEEPSEEK_API_KEY") ?? (await askHidden("Dán DEEPSEEK_API_KEY: "));
  if (!deepseekKey) fail("thiếu DEEPSEEK_API_KEY");

  const supabase = createClient(url, serviceKey, { auth: { autoRefreshToken: false, persistSession: false } });
  const catalogs = await loadCatalogs(supabase);
  console.log(
    `Danh mục YCCĐ: ${[...catalogs].map(([g, c]) => `lớp ${g}=${c.names.length} mục`).join(", ")}` +
      (dryRun ? "  [DRY-RUN: không ghi DB]" : ""),
  );

  // Tên đề gốc để làm gợi ý cho AI (đề "Luyện tập – Bài 28. Động lượng" giúp chọn đúng YCCĐ).
  const examTitle = new Map<number, string>();
  async function examLabel(examId: number): Promise<string | undefined> {
    if (examTitle.has(examId)) return examTitle.get(examId);
    const { data } = await supabase.from("exams").select("title, topic").eq("id", examId).maybeSingle();
    const row = data as { title?: string; topic?: string } | null;
    const label = [row?.title, row?.topic].filter(Boolean).join(" — ") || undefined;
    examTitle.set(examId, label ?? "");
    return label;
  }

  const PAGE_SIZE = 1000;
  let skippedNoAnswer = 0;
  let skippedNoGrade = 0;
  let attempted = 0;
  let batchNo = 0;
  const failedIds = new Set<number>();
  const logItems: LogItem[] = [];
  const touchedGrades = new Set<string>();
  // Câu đã đưa vào một lô nào đó trong lượt chạy này (hoặc cố tình bỏ qua). Bắt buộc phải nhớ:
  // câu AI không trả nhãn hợp lệ vẫn còn topic_name = '' trong DB nên sẽ được đọc lại ở trang
  // sau — không nhớ thì chạy vô hạn (nhất là --dry-run, không ghi gì để chúng biến mất).
  const seen = new Set<number>();

  for (;;) {
    let query = supabase
      .from("question_bank")
      .select("id, grade, subject_code, form, question, source_exam_id")
      .eq("archived", false)
      .eq("topic_name", "")
      .order("id")
      .limit(PAGE_SIZE);
    if (gradeFilter) query = query.eq("grade", gradeFilter);
    const { data, error } = await query;
    if (error) fail(`đọc question_bank lỗi: ${error.message}`);

    const rows: BankRow[] = [];
    for (const r of (data ?? []) as BankRow[]) {
      if (seen.has(r.id)) continue;
      if (limit && attempted >= limit) break;
      seen.add(r.id);
      if (!r.grade || !catalogs.has(r.grade)) {
        skippedNoGrade += 1; // câu không có khối: không biết danh mục YCCĐ nào để chọn
        continue;
      }
      rows.push(r);
      attempted += 1;
    }
    if (rows.length === 0) break;

    // Gộp theo khối lớp: mỗi lượt gọi AI chỉ được dùng danh mục của đúng một khối.
    const byGrade = new Map<string, BankRow[]>();
    for (const r of rows) {
      const arr = byGrade.get(r.grade) ?? [];
      arr.push(r);
      byGrade.set(r.grade, arr);
    }

    for (const [grade, gradeRows] of byGrade) {
      const catalog = catalogs.get(grade)!;
      touchedGrades.add(grade);
      for (let start = 0; start < gradeRows.length; start += BATCH_SIZE) {
        const batch = gradeRows.slice(start, start + BATCH_SIZE);
        const items = await Promise.all(
          batch.map(async (r, i) => ({
            i,
            text: questionTextForAi(r.question),
            source: r.source_exam_id !== null ? await examLabel(r.source_exam_id) : undefined,
          })),
        );
        batchNo += 1;
        console.log(`\nLô ${batchNo} (lớp ${grade}): ${batch.length} câu…`);
        let results: Map<number, { topic: string; form?: Form }>;
        try {
          results = await classifyBatch(deepseekKey, catalog.names, items);
        } catch (e) {
          console.error("  Lỗi gọi AI:", e instanceof Error ? e.message : String(e));
          batch.forEach((r) => failedIds.add(r.id));
          continue;
        }

        for (let i = 0; i < batch.length; i += 1) {
          const r = batch[i];
          const res = results.get(i);
          // Nhãn phải khớp nguyên văn danh mục của khối — AI bịa tên là bỏ, không ghi.
          if (!res || !catalog.set.has(res.topic)) {
            skippedNoAnswer += 1;
            continue;
          }
          const before = { topic_name: "", form: r.form ?? "" };
          const after = { topic_name: res.topic, form: !before.form && res.form ? res.form : before.form };
          if (dryRun) {
            logItems.push({ id: r.id, before, after });
            continue;
          }
          try {
            await withRetry(async () => {
              const payload: Record<string, unknown> = { topic_name: after.topic_name };
              if (after.form) payload.form = after.form;
              // Ràng buộc topic_name = '' để không đè lên câu vừa được gắn tay ở phiên khác.
              const { error: updErr } = await supabase.from("question_bank").update(payload).eq("id", r.id).eq("topic_name", "");
              if (updErr) throw new Error(updErr.message);
            }, `Ghi câu #${r.id}`);
          } catch (e) {
            console.error(`  Lỗi ghi câu #${r.id}:`, e instanceof Error ? e.message : String(e));
            failedIds.add(r.id);
            continue;
          }
          logItems.push({ id: r.id, before, after });
        }
        console.log(`  ✓ ${dryRun ? "đề xuất" : "đã ghi"} luỹ kế ${logItems.length}, bỏ qua ${skippedNoAnswer}.`);
        await sleep(300);
      }
    }
  }

  fs.mkdirSync(LOG_DIR, { recursive: true });
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const logPath = path.join(LOG_DIR, `backfill-bank-topics-${stamp}${dryRun ? "-dryrun" : ""}.json`);
  fs.writeFileSync(
    logPath,
    JSON.stringify(
      {
        startedAt: new Date().toISOString(),
        mode: dryRun ? "dry-run" : "apply",
        model: MODEL,
        grades: [...touchedGrades].sort(),
        items: logItems,
      },
      null,
      2,
    ),
  );

  console.log(
    `\nHoàn tất: ${logItems.length} câu ${dryRun ? "đề xuất (CHƯA ghi DB)" : "đã gắn nhãn"}, ` +
      `${skippedNoAnswer} câu AI không trả nhãn hợp lệ (bỏ qua — gắn tay trên web), ` +
      `${skippedNoGrade} câu thiếu khối (bỏ qua), ${failedIds.size} câu lỗi gọi/ghi.`,
  );
  console.log(`Log: ${path.relative(path.resolve(scriptDir, ".."), logPath)}`);
  if (dryRun) {
    console.log("Rà lại log rồi chạy lại KHÔNG có --dry-run để ghi thật.");
  } else {
    console.log(
      `Trigger DB đã tự vá nhãn vào exams.questions. Hoàn tác nếu cần:\n  npx tsx scripts/backfill-question-bank-topics.mts --undo ${path.relative(path.resolve(scriptDir, ".."), logPath)}`,
    );
  }
}

main().catch((err) => fail(err instanceof Error ? err.message : String(err)));
