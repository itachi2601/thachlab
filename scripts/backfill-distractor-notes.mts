// Sinh "ghi chú phương án nhiễu" (distractorNotes) bằng AI cho câu trắc nghiệm trong ngân hàng câu hỏi — để chế độ
// Luyện tập "Từng câu" nói được VÌ SAO phương án em chọn sai (nhầm công thức, quên đổi đơn vị, đổi dấu…).
// Việc B của docs/BAN-GIAO-RANK-THI-THANG-HANG-2026-10-03.md.
//
// Điều kiện: migration supabase/migrations/20261003120000_distractor_notes.sql ĐÃ chạy (hàm bank_set_distractor_notes
// và question_content_hash bỏ distractorNotes). Chưa chạy thì script dừng ngay ở lần ghi đầu tiên.
//
// Ghi qua RPC bank_set_distractor_notes: vào question_bank.question VÀ vào mọi exams.questions có cùng câu (Luyện tập
// đọc câu từ exams.questions, không đọc ngân hàng). content_hash không đổi nên không sinh dòng ngân hàng trùng.
//
// Phạm vi ưu tiên: grade 11/12, qtype multiple_choice, chủ đề (và chủ đề con) của 8 danh hiệu có ≥20 câu Trung bình
// (chua_te_song, bac_thay_mach_dien, vu_cong_lech_pha, bac_thay_nhip_dao_dong, nguoi_truyen_nang_luong,
// phap_su_dien_truong, ke_danh_thuc_dong_dien, ke_tich_tru_loi_dinh). Câu đã có ghi chú thì bỏ qua → chạy lại an toàn.
//
// LƯU Ý: GHI THẬT NGAY vào DB (tốn lượt gọi Anthropic API). Thử trước với số nhỏ rồi xem trong Luyện tập "Từng câu":
//
//   npx tsx scripts/backfill-distractor-notes.mts 20            # thử 20 câu
//   npx tsx scripts/backfill-distractor-notes.mts 20 --dry-run  # chỉ in ghi chú, không ghi DB
//   npx tsx scripts/backfill-distractor-notes.mts               # chạy hết phạm vi ưu tiên
//
// Chạy trên Mac (cần SUPABASE_SERVICE_ROLE_KEY + ANTHROPIC_API_KEY trong env/.env.local, thiếu thì hỏi).

import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";
import { questionTextForAi } from "@/services/exam-question-text";
import type { ExamQuestion } from "@/features/exams/types";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const BATCH_SIZE = 8;
const MODEL = "claude-sonnet-5-5";
const MAX_WORDS = 30; // trần cứng; prompt nhắm 10–18 từ (công thức $…$ cũng tính là từ)
const LETTERS = ["A", "B", "C", "D"] as const;
const PRIORITY_TITLES = [
  "chua_te_song",
  "bac_thay_mach_dien",
  "vu_cong_lech_pha",
  "bac_thay_nhip_dao_dong",
  "nguoi_truyen_nang_luong",
  "phap_su_dien_truong",
  "ke_danh_thuc_dong_dien",
  "ke_tich_tru_loi_dinh",
];

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

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

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
  question: ExamQuestion;
}

const SYSTEM =
  "Bạn viết ghi chú chẩn đoán lỗi cho câu trắc nghiệm Vật lí THPT, hiện ngay sau khi người học chọn sai (kiểu Duolingo). " +
  "Với MỖI phương án SAI, viết đúng 1 câu ngắn 10–18 từ (tiếng Việt) nêu LỖI TƯ DUY dẫn tới phương án đó: nhầm công thức " +
  "hoặc đại lượng, quên đổi đơn vị, đổi dấu hoặc chiều, lẫn hai khái niệm, bỏ sót một bước… Nói lỗi, không nói " +
  '"phương án này sai". Dạng viết: mở đầu bằng động từ hoặc danh từ chỉ lỗi, KHÔNG mở đầu bằng "Em", không có chủ ngữ ' +
  '"em/bạn/học sinh" (ví dụ: "Nhầm $\\omega$ với $f$: quên chia cho $2\\pi$." · "Lẫn khoảng cách ngược pha ' +
  '$\\lambda/2$ với $\\lambda/4$." · "Đổi 20 cm sang mét còn thiếu."). Với câu hỏi "chọn phát biểu SAI/KHÔNG đúng", ' +
  'các phương án nhiễu là phát biểu đúng → viết "Phát biểu này đúng: <lý do ngắn>." TUYỆT ĐỐI không dùng vai ' +
  '"thầy/cô", không chữ "thầy". Công thức viết trong $…$ (KaTeX); trong công thức dùng \\lt, \\gt thay cho < và >. ' +
  "Không nhắc lại đáp án đúng, không tiết lộ số liệu cuối. Chỉ trả về DUY NHẤT một JSON hợp lệ dạng " +
  '{"results":[{"index":0,"notes":{"A":"…","C":"…","D":"…"}}]} — khoá là nhãn phương án SAI (A–D), không bọc ' +
  "trong markdown code fence, không lời giải thích thêm. Trong chuỗi JSON, mỗi dấu gạch chéo ngược của LaTeX phải " +
  'nhân đôi ("\\\\lambda", "\\\\frac").';

function buildPrompt(items: { i: number; text: string; wrong: string[] }[]): string {
  return items
    .map((it) => `--- Câu (index=${it.i}) — cần ghi chú cho các phương án sai: ${it.wrong.join(", ")} ---\n${it.text}`)
    .join("\n\n");
}

function countWords(s: string): number {
  return s.trim().split(/\s+/).filter(Boolean).length;
}

/** Giữ ghi chú hợp lệ: đúng khoá phương án sai, ≤ MAX_WORDS từ, không có chữ "thầy". Đủ hết phương án sai mới nhận. */
function cleanNotes(raw: unknown, wrong: string[]): { notes: Record<string, string> } | { reason: string } {
  if (!raw || typeof raw !== "object") return { reason: "không có notes" };
  const src = raw as Record<string, unknown>;
  const out: Record<string, string> = {};
  for (const k of wrong) {
    const v = typeof src[k] === "string" ? (src[k] as string).trim() : "";
    if (!v) return { reason: `thiếu phương án ${k}` };
    if (countWords(v) > MAX_WORDS) return { reason: `${k} dài ${countWords(v)} từ (> ${MAX_WORDS})` };
    if (/thầy/i.test(v)) return { reason: `${k} có chữ "thầy"` };
    if (/^\s*em\b/i.test(v)) return { reason: `${k} mở đầu bằng "Em"` };
    out[k] = v;
  }
  return { notes: out };
}

/** AI đôi khi quên nhân đôi dấu \ của LaTeX trong chuỗi JSON ("\lambda" là escape không hợp lệ → JSON.parse hỏng cả lô).
 *  Ghi chú không có xuống dòng/tab thật, nên mọi \ đơn không đứng trước " đều coi là dấu \ của công thức → nhân đôi. */
function repairJson(s: string): string {
  const P = "\u0000";
  return s.replace(/\\\\/g, P).replace(/\\(?!")/g, "\\\\").replace(new RegExp(P, "g"), "\\\\");
}

function parseResults(raw: string): unknown[] {
  const start = raw.indexOf("{");
  const end = raw.lastIndexOf("}");
  if (start < 0 || end < 0) throw new Error("AI không trả về JSON hợp lệ.");
  const slice = raw.slice(start, end + 1);
  let parsed: { results?: unknown };
  try {
    parsed = JSON.parse(slice) as { results?: unknown };
  } catch {
    parsed = JSON.parse(repairJson(slice)) as { results?: unknown }; // ném lỗi tiếp nếu vẫn hỏng
  }
  return Array.isArray(parsed.results) ? parsed.results : [];
}

async function generateBatch(apiKey: string, items: { i: number; text: string; wrong: string[] }[]): Promise<Map<number, Record<string, string>>> {
  let rows: unknown[] = [];
  for (let attempt = 1; ; attempt += 1) {
    try {
      rows = parseResults(await callAi(apiKey, items));
      break;
    } catch (e) {
      if (attempt >= 2) throw e;
      console.log(`  ↻ JSON hỏng (${e instanceof Error ? e.message : String(e)}), gọi AI lại lần 2…`);
    }
  }
  const byIndex = new Map(items.map((it) => [it.i, it]));
  const out = new Map<number, Record<string, string>>();
  const seen = new Set<number>();
  for (const row of rows) {
    if (!row || typeof row !== "object") continue;
    const r = row as Record<string, unknown>;
    const item = byIndex.get(Number(r.index));
    if (!item) continue;
    seen.add(item.i);
    const res = cleanNotes(r.notes, item.wrong);
    if ("notes" in res) out.set(item.i, res.notes);
    else console.log(`  ✗ index ${item.i}: ${res.reason}`);
  }
  for (const it of items) if (!seen.has(it.i)) console.log(`  ✗ index ${it.i}: AI không trả về câu này`);
  return out;
}

async function callAi(apiKey: string, items: { i: number; text: string; wrong: string[] }[]): Promise<string> {
  const res = await withRetry(
    () =>
      fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "content-type": "application/json", "x-api-key": apiKey, "anthropic-version": "2023-06-01" },
        body: JSON.stringify({ model: MODEL, max_tokens: 4096, system: SYSTEM, messages: [{ role: "user", content: buildPrompt(items) }] }),
      }),
    "Gọi AI",
  );
  if (!res.ok) throw new Error(`Anthropic API lỗi ${res.status}: ${await res.text()}`);
  const data = (await res.json()) as { content?: { type: string; text?: string }[] };
  return data.content?.find((b) => b.type === "text")?.text ?? "";
}

async function main() {
  const args = process.argv.slice(2);
  const dry = args.includes("--dry-run");
  const limitArg = args.find((a) => /^\d+$/.test(a));
  const limit = limitArg ? Number(limitArg) : undefined;

  const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
  if (!url) fail("không đọc được NEXT_PUBLIC_SUPABASE_URL từ .env.local");
  const serviceKey =
    process.env.SUPABASE_SERVICE_ROLE_KEY ??
    readEnvLocal("SUPABASE_SERVICE_ROLE_KEY") ??
    (await askHidden("Dán SUPABASE_SERVICE_ROLE_KEY (Settings → API → service_role): "));
  if (!serviceKey) fail("thiếu SUPABASE_SERVICE_ROLE_KEY");
  const anthropicKey = process.env.ANTHROPIC_API_KEY ?? readEnvLocal("ANTHROPIC_API_KEY") ?? (await askHidden("Dán ANTHROPIC_API_KEY: "));
  if (!anthropicKey) fail("thiếu ANTHROPIC_API_KEY");

  const supabase = createClient(url, serviceKey, { auth: { autoRefreshToken: false, persistSession: false } });

  // Chủ đề của 8 danh hiệu ưu tiên + chủ đề con của chúng.
  const { data: tt, error: ttErr } = await supabase.from("rank_title_topics").select("topic_id").in("title_code", PRIORITY_TITLES);
  if (ttErr) fail(`đọc rank_title_topics lỗi: ${ttErr.message}`);
  const baseIds = [...new Set((tt ?? []).map((r) => r.topic_id as number))];
  if (baseIds.length === 0) fail("không có chủ đề nào của các danh hiệu ưu tiên");
  const { data: kids, error: kidErr } = await supabase.from("question_topics").select("id").in("parent_id", baseIds);
  if (kidErr) fail(`đọc question_topics lỗi: ${kidErr.message}`);
  const topicIds = [...new Set([...baseIds, ...(kids ?? []).map((r) => r.id as number)])];
  console.log(`Phạm vi: ${topicIds.length} chủ đề của ${PRIORITY_TITLES.length} danh hiệu ưu tiên, lớp 11/12.${dry ? " (--dry-run: không ghi DB)" : ""}`);

  const PAGE_SIZE = 500;
  let cursor = 0;
  let done = 0;
  let batchNo = 0;
  const failedIds = new Set<number>();
  for (;;) {
    if (limit && done + failedIds.size >= limit) break;
    const { data, error } = await supabase
      .from("question_bank")
      .select("id, question")
      .eq("archived", false)
      .eq("qtype", "multiple_choice")
      .in("grade", ["11", "12"])
      .in("topic_id", topicIds)
      .gt("id", cursor)
      .order("id")
      .limit(PAGE_SIZE);
    if (error) fail(`đọc question_bank lỗi: ${error.message}`);
    const page = (data ?? []) as BankRow[];
    if (page.length === 0) break;
    cursor = page[page.length - 1].id;
    const todo = page
      .filter((r) => r.question.type === "multiple_choice" && Array.isArray(r.question.options) && r.question.options.length === 4 && !r.question.distractorNotes)
      .slice(0, limit ? limit - done - failedIds.size : undefined);

    for (let start = 0; start < todo.length; start += BATCH_SIZE) {
      const batch = todo.slice(start, start + BATCH_SIZE);
      const items = batch.map((r, i) => {
        const q = r.question as Extract<ExamQuestion, { type: "multiple_choice" }>;
        return { i, text: questionTextForAi(q), wrong: LETTERS.filter((_, k) => k !== q.answer) as string[] };
      });
      batchNo += 1;
      console.log(`\nLô ${batchNo}: ${batch.length} câu…`);
      let results: Map<number, Record<string, string>>;
      try {
        results = await generateBatch(anthropicKey, items);
      } catch (e) {
        console.error("  Lỗi gọi AI:", e instanceof Error ? e.message : String(e));
        batch.forEach((r) => failedIds.add(r.id));
        continue;
      }
      for (let i = 0; i < batch.length; i += 1) {
        const notes = results.get(i);
        if (!notes) {
          failedIds.add(batch[i].id);
          continue;
        }
        if (dry) {
          console.log(`  #${batch[i].id}`, JSON.stringify(notes, null, 0));
          done += 1;
          continue;
        }
        try {
          await withRetry(async () => {
            const { error: rpcErr } = await supabase.rpc("bank_set_distractor_notes", { p_bank_id: batch[i].id, p_notes: notes });
            if (rpcErr) throw new Error(rpcErr.message);
          }, `Ghi câu #${batch[i].id}`);
        } catch (e) {
          console.error(`  Lỗi ghi câu #${batch[i].id}:`, e instanceof Error ? e.message : String(e));
          failedIds.add(batch[i].id);
          continue;
        }
        done += 1;
      }
      console.log(`  ✓ luỹ kế ${done} câu${dry ? " (chưa ghi)" : " đã ghi"}, bỏ qua ${failedIds.size}.`);
    }
  }
  console.log(`\nHoàn tất: ${done} câu có ghi chú phương án nhiễu, ${failedIds.size} câu bỏ qua (AI trả sai định dạng/quá dài hoặc lỗi ghi).`);
}

main().catch((err) => fail(err instanceof Error ? err.message : String(err)));
