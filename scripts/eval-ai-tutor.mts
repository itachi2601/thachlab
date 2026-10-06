// Eval offline cho AI Tutor (docs/AI-TUTOR.md mục 7): lấy N câu học sinh LÀM SAI THẬT, cho từng
// model sinh một GỢI Ý TẦNG 1 kiểu Socratic (không lộ đáp án) với grounding là lời giải + lý thuyết
// của chính bài đó, rồi xuất phiếu chấm mù (nhãn A/B/C đã xáo) để thầy chấm 3 tiêu chí:
// không lộ đáp án · đúng vật lí · trúng chỗ sai. Chi phí/usage thật ghi kèm từng lượt gọi.
//
// CHỈ ĐỌC DB — không ghi gì vào Supabase. Có gọi API trả tiền (trừ --dry-run).
//
//   npx tsx scripts/eval-ai-tutor.mts --dry-run                 # chỉ in prompt mẫu, không gọi API
//   npx tsx scripts/eval-ai-tutor.mts --n 2 --providers deepseek # thử nhỏ
//   npx tsx scripts/eval-ai-tutor.mts --n 30 --providers deepseek,openai,anthropic
//   npx tsx scripts/eval-ai-tutor.mts --n 30 --models deepseek=deepseek-flash,openai=gpt-6-luna,anthropic=claude-sonnet-5-5
//   npx tsx scripts/eval-ai-tutor.mts --seed 7                  # đổi mẫu câu (mặc định seed 1, lặp lại được)
//   npx tsx scripts/eval-ai-tutor.mts --allow-images            # giữ cả câu có hình (mặc định bỏ: model không thấy ảnh)
//
// Kết quả: scripts/logs/eval-ai-tutor-<thời điểm>.json (đầy đủ, có khoá nhãn), -phieu-cham.md (phiếu
// chấm mù cho thầy), -khoa-nhan.md (khoá nhãn A/B/C → model, mở sau khi chấm xong).
//
// Cần .env.local: NEXT_PUBLIC_SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, và key của provider muốn chạy:
// DEEPSEEK_API_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY. Thiếu key provider nào thì bỏ qua provider đó.
//
// Tên model & giá mục theo thời gian — tra trang chính thức trước khi tin (AGENTS.md mục "Gọi AI provider"):
//   api-docs.deepseek.com/quick_start/pricing · platform.claude.com/docs/en/about-claude/pricing ·
//   developers.openai.com/api/docs/pricing

import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { gradeQuestion } from "@/features/exams/types";
import type { ExamQuestion, QuestionResponse } from "@/features/exams/types";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const LETTERS = ["A", "B", "C", "D"];

type Provider = "deepseek" | "openai" | "anthropic";
const ALL_PROVIDERS: Provider[] = ["deepseek", "openai", "anthropic"];
const DEFAULT_MODELS: Record<Provider, string> = {
  deepseek: "deepseek-flash",
  openai: "gpt-6-luna",
  anthropic: "claude-sonnet-5-5",
};

// Giá USD / 1M token, tra 6/10/2026 từ trang chính thức. CHỈ để ước tính — tra lại trước khi tin.
// cacheRead/cacheWrite: giá đọc/ghi cache. DeepSeek: off-peak = nửa giá peak, ghi cache miễn phí.
interface Price { input: number; output: number; cacheRead: number; cacheWrite?: number }
const PRICES: Record<string, Price> = {
  "deepseek-flash": { input: 0.3, output: 1.2, cacheRead: 0.006 }, // peak; off-peak ×0.5
  "deepseek-v4-pro": { input: 1.32, output: 3.96, cacheRead: 0.044 },
  "gpt-6-luna": { input: 0.1, output: 0.5, cacheRead: 0.01 },
  "gpt-5.6-luna": { input: 0.2, output: 1.2, cacheRead: 0.02 },
  "gpt-5.4-nano": { input: 0.2, output: 1.25, cacheRead: 0.02 },
  "claude-haiku-4-5": { input: 1, output: 5, cacheRead: 0.1, cacheWrite: 1.25 },
  "claude-sonnet-5-5": { input: 2, output: 10, cacheRead: 0.2, cacheWrite: 2.5 },
  "claude-opus-5-5": { input: 4, output: 20, cacheRead: 0.2, cacheWrite: 5 },
};

// ── tham số dòng lệnh ──────────────────────────────────────────────────────────
function arg(name: string): string | undefined {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 ? process.argv[i + 1] : undefined;
}
const DRY_RUN = process.argv.includes("--dry-run");
const ALLOW_IMAGES = process.argv.includes("--allow-images");
const N = Number(arg("n") ?? 30);
const SEED = Number(arg("seed") ?? 1);
const PROVIDERS = ((arg("providers") ?? ALL_PROVIDERS.join(",")).split(",").map((s) => s.trim()) as Provider[]).filter((p) =>
  ALL_PROVIDERS.includes(p),
);
const MODELS: Record<Provider, string> = { ...DEFAULT_MODELS };
for (const pair of (arg("models") ?? "").split(",")) {
  const [p, m] = pair.split("=").map((s) => s.trim());
  if (p && m && ALL_PROVIDERS.includes(p as Provider)) MODELS[p as Provider] = m;
}

function readEnvLocal(key: string): string | undefined {
  const p = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const line = fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}
const env = (k: string) => process.env[k] ?? readEnvLocal(k);

function fail(msg: string): never {
  console.error("Lỗi:", msg);
  process.exit(1);
}

// PRNG có seed để lặp lại cùng mẫu câu
function mulberry32(a: number) {
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const rand = mulberry32(SEED);
function shuffle<T>(xs: T[]): T[] {
  const a = [...xs];
  for (let i = a.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function stripHtml(html: string): string {
  return html
    .replace(/<style[\s\S]*?<\/style>|<script[\s\S]*?<\/script>|<svg[\s\S]*?<\/svg>/gi, " ")
    .replace(/<br\s*\/?>|<\/p>|<\/li>|<\/h[1-6]>|<\/tr>/gi, "\n")
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/[ \t]+/g, " ")
    .replace(/\n\s*\n+/g, "\n")
    .trim();
}

// ── dữ liệu ────────────────────────────────────────────────────────────────────
interface WrongRow {
  exam_result_id: number;
  question_index: number;
  exam_id: number;
  student_id: string;
  topic_name: string;
  qtype: string;
  created_at: string;
}

interface Sample {
  exam_id: number;
  exam_title: string;
  question_index: number;
  topic_name: string;
  lesson_id: number | null;
  question: ExamQuestion;
  response: QuestionResponse;
  responseText: string;
  correctText: string;
  theory: string;
}

function questionStem(q: ExamQuestion): string {
  // Đề KHÔNG đánh dấu đáp án đúng — phần đó đưa riêng ở mục grounding.
  const parts = [q.question];
  if (q.type === "multiple_choice") parts.push(q.options.map((o, j) => `${LETTERS[j]}. ${o}`).join("\n"));
  if (q.type === "true_false") parts.push(q.statements.map((s, j) => `${["a", "b", "c", "d"][j]}) ${s.text}`).join("\n"));
  return parts.join("\n");
}

function describeResponse(q: ExamQuestion, r: QuestionResponse): { text: string; answered: boolean } {
  if (q.type === "multiple_choice") {
    if (typeof r !== "number") return { text: "", answered: false };
    return { text: `${LETTERS[r]}. ${q.options[r] ?? ""}`, answered: true };
  }
  if (q.type === "short_answer") {
    const s = typeof r === "string" ? r.trim() : "";
    return { text: s, answered: s !== "" };
  }
  if (q.type === "true_false") {
    if (!Array.isArray(r) || r.every((v) => v === null)) return { text: "", answered: false };
    const t = r.map((v, j) => `${["a", "b", "c", "d"][j]}) ${v === null ? "bỏ trống" : v ? "Đúng" : "Sai"}`).join("; ");
    return { text: t, answered: true };
  }
  return { text: "", answered: false };
}

function describeCorrect(q: ExamQuestion): string {
  if (q.type === "multiple_choice") return `${LETTERS[q.answer]}. ${q.options[q.answer] ?? ""}`;
  if (q.type === "short_answer") return q.answer;
  if (q.type === "true_false") return q.statements.map((s, j) => `${["a", "b", "c", "d"][j]}) ${s.answer ? "Đúng" : "Sai"}`).join("; ");
  return "";
}

async function loadSamples(n: number): Promise<Sample[]> {
  const url = env("NEXT_PUBLIC_SUPABASE_URL");
  const key = env("SUPABASE_SERVICE_ROLE_KEY");
  if (!url || !key) fail("thiếu NEXT_PUBLIC_SUPABASE_URL hoặc SUPABASE_SERVICE_ROLE_KEY trong .env.local");
  const sb = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });

  // Câu làm sai gần đây (trắc nghiệm + trả lời ngắn + đúng/sai), bỏ tự luận
  const { data: wrongRows, error } = await sb
    .from("exam_question_results")
    .select("exam_result_id, question_index, exam_id, student_id, topic_name, qtype, created_at")
    .eq("is_correct", false)
    .in("qtype", ["multiple_choice", "short_answer", "true_false"])
    .order("created_at", { ascending: false })
    .limit(1000); // PostgREST trả tối đa 1000 dòng/lần; 1000 câu sai gần nhất là đủ để rút mẫu
  if (error) fail(`đọc exam_question_results: ${error.message}`);
  const rows = (wrongRows ?? []) as WrongRow[];
  console.log(`Đọc được ${rows.length} dòng làm sai gần nhất.`);

  // Mỗi (đề, câu) chỉ lấy 1 lần; xáo theo seed để mẫu trải nhiều đề/chủ đề
  const seen = new Set<string>();
  const uniq: WrongRow[] = [];
  for (const r of shuffle(rows)) {
    const k = `${r.exam_id}:${r.question_index}`;
    if (seen.has(k)) continue;
    seen.add(k);
    uniq.push(r);
  }

  const examCache = new Map<number, { title: string; questions: ExamQuestion[] } | null>();
  const resultCache = new Map<number, QuestionResponse[] | null>();
  const lessonOfExam = new Map<number, number | null>();
  const theoryOfLesson = new Map<number, string>();

  async function exam(id: number) {
    if (!examCache.has(id)) {
      const { data } = await sb.from("exams").select("title, questions").eq("id", id).maybeSingle();
      examCache.set(id, data ? { title: data.title as string, questions: (data.questions ?? []) as ExamQuestion[] } : null);
    }
    return examCache.get(id) ?? null;
  }
  async function responses(resultId: number) {
    if (!resultCache.has(resultId)) {
      const { data } = await sb.from("exam_results").select("detail").eq("id", resultId).maybeSingle();
      const d = (data?.detail ?? null) as { responses?: QuestionResponse[] } | null;
      resultCache.set(resultId, Array.isArray(d?.responses) ? d!.responses! : null);
    }
    return resultCache.get(resultId) ?? null;
  }
  async function lessonId(examId: number) {
    if (!lessonOfExam.has(examId)) {
      const { data } = await sb.from("lesson_items").select("lesson_id").contains("exam_ids", [examId]).limit(1);
      lessonOfExam.set(examId, data && data[0] ? (data[0].lesson_id as number) : null);
    }
    return lessonOfExam.get(examId) ?? null;
  }
  async function theory(lid: number) {
    if (!theoryOfLesson.has(lid)) {
      const { data } = await sb
        .from("lesson_items")
        .select("summary_html, body_html")
        .eq("lesson_id", lid)
        .eq("kind", "ly_thuyet")
        .limit(1);
      const row = data?.[0] as { summary_html?: string | null; body_html?: string | null } | undefined;
      const txt = stripHtml(row?.summary_html?.trim() || row?.body_html || "");
      theoryOfLesson.set(lid, txt.length > 2500 ? `${txt.slice(0, 2500)}…` : txt);
    }
    return theoryOfLesson.get(lid) ?? "";
  }

  const out: Sample[] = [];
  let skippedNowCorrect = 0;
  let skippedImages = 0;
  for (const r of uniq) {
    if (out.length >= n) break;
    const ex = await exam(r.exam_id);
    const q = ex?.questions[r.question_index];
    if (!ex || !q || q.type === "essay") continue;
    const rs = await responses(r.exam_result_id);
    const resp = rs?.[r.question_index];
    if (resp === undefined) continue;
    const d = describeResponse(q, resp);
    if (!d.answered) continue; // bỏ qua câu bỏ trống — không có "chỗ sai" để gợi ý
    if (!(q.explanation ?? "").trim()) continue; // cần lời giải làm grounding
    // Đề có thể đã được sửa đáp án SAU khi HS làm → dòng is_correct=false nhưng chấm lại theo đề hiện tại
    // lại đúng. Chấm lại để chắc chắn đây là câu sai thật so với đề đang hiển thị.
    const g = gradeQuestion(q, resp);
    if (g.max > 0 && g.earned === g.max) {
      skippedNowCorrect += 1;
      continue;
    }
    if (!ALLOW_IMAGES && /<img\b/i.test(questionStem(q) + (q.explanation ?? ""))) {
      skippedImages += 1;
      continue;
    }
    const lid = await lessonId(r.exam_id);
    out.push({
      exam_id: r.exam_id,
      exam_title: ex.title,
      question_index: r.question_index,
      topic_name: r.topic_name,
      lesson_id: lid,
      question: q,
      response: resp,
      responseText: d.text,
      correctText: describeCorrect(q),
      theory: lid ? await theory(lid) : "",
    });
  }
  if (skippedNowCorrect) console.log(`Bỏ ${skippedNowCorrect} dòng: chấm lại theo đề hiện tại thì ĐÚNG (đề đã sửa đáp án sau khi HS làm?).`);
  if (skippedImages) console.log(`Bỏ ${skippedImages} câu có hình (model không thấy ảnh; giữ lại bằng --allow-images).`);
  return out;
}

// ── prompt ─────────────────────────────────────────────────────────────────────
const SYSTEM_PROMPT = `Bạn là trợ giảng Vật lí THPT trong ứng dụng học tập ThachLab, đang trò chuyện với một học sinh vừa làm sai một câu.
Nhiệm vụ: đưa đúng MỘT gợi ý đầu tiên theo lối Socratic để em tự tìm ra chỗ sai.

Quy tắc bắt buộc:
1. TUYỆT ĐỐI không nói đáp án đúng, không nêu chữ cái phương án đúng, không nêu kết quả số cuối cùng, không nói "đáp án là".
2. Chỉ ra em đang hiểu nhầm hoặc bỏ sót điều gì DỰA TRÊN phương án em đã chọn (vì sao em có thể đã chọn như vậy), rồi đặt 1–2 câu hỏi dẫn dắt để em tự xem lại.
3. Dùng đúng kiến thức trong phần "Lý thuyết của bài" và "Lời giải" được cung cấp; không bịa công thức ngoài đó.
4. Giọng thân thiện, gọi học sinh là "bạn", xưng "mình"; không xưng "thầy/cô". Tiếng Việt, tối đa 120 từ, không dùng markdown, không dùng tiêu đề.
5. Công thức viết dạng văn bản thường (ví dụ v = s/t), không LaTeX.`;

function buildUserPrompt(s: Sample): string {
  const q = s.question;
  return [
    `## Câu hỏi (chủ đề: ${s.topic_name || "chưa gắn"})`,
    questionStem(q),
    "",
    `## Học sinh đã chọn / trả lời`,
    s.responseText,
    "",
    `## Dữ liệu chỉ để bạn hiểu bài — KHÔNG được lặp lại cho học sinh`,
    `Đáp án đúng: ${s.correctText}`,
    `Lời giải: ${stripHtml(q.explanation ?? "")}`,
    s.theory ? `\n## Lý thuyết của bài\n${s.theory}` : "",
    "",
    "Hãy viết gợi ý đầu tiên cho học sinh.",
  ].join("\n");
}

// ── gọi API (REST thuần, không SDK) ────────────────────────────────────────────
interface CallResult {
  provider: Provider;
  model: string;
  text: string;
  input_tokens: number;
  output_tokens: number;
  cache_read_tokens: number;
  cache_write_tokens: number;
  reasoning_tokens: number | null; // null = provider không tách riêng (Anthropic gộp vào output)
  latency_ms: number;
  called_at: string;
  is_peak: boolean | null; // chỉ DeepSeek
  stop_reason: string;
  cost_usd: number | null;
  error?: string;
}

function deepseekIsPeak(d: Date): boolean {
  // Peak: 01:00–04:00 và 06:00–10:00 UTC, thứ Hai–Sáu (chưa trừ lễ Trung Quốc)
  const day = d.getUTCDay();
  const h = d.getUTCHours() + d.getUTCMinutes() / 60;
  if (day === 0 || day === 6) return false;
  return (h >= 1 && h < 4) || (h >= 6 && h < 10);
}

function cost(model: string, r: Omit<CallResult, "cost_usd">): number | null {
  const p = PRICES[model];
  if (!p) return null;
  const k = r.provider === "deepseek" && r.is_peak === false ? 0.5 : 1;
  const uncached = Math.max(0, r.input_tokens - r.cache_read_tokens - r.cache_write_tokens);
  const usd =
    (uncached * p.input + r.cache_read_tokens * p.cacheRead + r.cache_write_tokens * (p.cacheWrite ?? p.input) + r.output_tokens * p.output) /
    1e6;
  return usd * k;
}

async function postJson(url: string, headers: Record<string, string>, body: unknown): Promise<{ ok: boolean; status: number; json: unknown; text: string }> {
  const res = await fetch(url, { method: "POST", headers: { "content-type": "application/json", ...headers }, body: JSON.stringify(body) });
  const text = await res.text();
  let json: unknown = null;
  try {
    json = JSON.parse(text);
  } catch {
    /* giữ text */
  }
  return { ok: res.ok, status: res.status, json, text };
}

async function callProvider(provider: Provider, model: string, apiKey: string, user: string): Promise<CallResult> {
  const t0 = Date.now();
  const calledAt = new Date();
  const base: Omit<CallResult, "cost_usd" | "text" | "stop_reason"> = {
    provider,
    model,
    input_tokens: 0,
    output_tokens: 0,
    cache_read_tokens: 0,
    cache_write_tokens: 0,
    reasoning_tokens: null,
    latency_ms: 0,
    called_at: calledAt.toISOString(),
    is_peak: provider === "deepseek" ? deepseekIsPeak(calledAt) : null,
  };
  try {
    if (provider === "deepseek") {
      // deepseek-flash mặc định BẬT thinking → tắt cho tầng gợi ý (như classify-questions)
      const r = await postJson(
        "https://api.deepseek.com/chat/completions",
        { authorization: `Bearer ${apiKey}` },
        {
          model,
          max_tokens: 800,
          thinking: { type: "disabled" },
          messages: [
            { role: "system", content: SYSTEM_PROMPT },
            { role: "user", content: user },
          ],
        },
      );
      if (!r.ok) throw new Error(`HTTP ${r.status}: ${r.text.slice(0, 300)}`);
      const j = r.json as {
        choices: { message: { content: string }; finish_reason: string }[];
        usage: {
          prompt_tokens: number;
          completion_tokens: number;
          prompt_cache_hit_tokens?: number;
          completion_tokens_details?: { reasoning_tokens?: number };
        };
      };
      const u = j.usage;
      const out = {
        ...base,
        text: j.choices[0]?.message?.content ?? "",
        stop_reason: j.choices[0]?.finish_reason ?? "",
        input_tokens: u.prompt_tokens,
        output_tokens: u.completion_tokens,
        cache_read_tokens: u.prompt_cache_hit_tokens ?? 0,
        reasoning_tokens: u.completion_tokens_details?.reasoning_tokens ?? 0,
        latency_ms: Date.now() - t0,
      };
      return { ...out, cost_usd: cost(model, out) };
    }
    if (provider === "openai") {
      const r = await postJson(
        "https://api.openai.com/v1/chat/completions",
        { authorization: `Bearer ${apiKey}` },
        {
          model,
          max_completion_tokens: 2000, // model có suy luận tính reasoning vào đây
          messages: [
            { role: "system", content: SYSTEM_PROMPT },
            { role: "user", content: user },
          ],
        },
      );
      if (!r.ok) throw new Error(`HTTP ${r.status}: ${r.text.slice(0, 300)}`);
      const j = r.json as {
        choices: { message: { content: string }; finish_reason: string }[];
        usage: {
          prompt_tokens: number;
          completion_tokens: number;
          prompt_tokens_details?: { cached_tokens?: number };
          completion_tokens_details?: { reasoning_tokens?: number };
        };
      };
      const u = j.usage;
      const out = {
        ...base,
        text: j.choices[0]?.message?.content ?? "",
        stop_reason: j.choices[0]?.finish_reason ?? "",
        input_tokens: u.prompt_tokens,
        output_tokens: u.completion_tokens,
        cache_read_tokens: u.prompt_tokens_details?.cached_tokens ?? 0,
        reasoning_tokens: u.completion_tokens_details?.reasoning_tokens ?? 0,
        latency_ms: Date.now() - t0,
      };
      return { ...out, cost_usd: cost(model, out) };
    }
    // anthropic — dòng 5.x: thinking luôn bật (adaptive), hạ bằng effort low; thinking tính vào
    // max_tokens nên để rộng (memory reference_anthropic_api_thinking_max_tokens). Haiku 4.5 không
    // nhận output_config.effort → bỏ qua tham số đó.
    const isHaiku45 = /^claude-haiku-4-5/.test(model);
    const body: Record<string, unknown> = {
      model,
      max_tokens: isHaiku45 ? 1000 : 16000,
      system: [{ type: "text", text: SYSTEM_PROMPT, cache_control: { type: "ephemeral" } }],
      messages: [{ role: "user", content: user }],
    };
    if (!isHaiku45) body.output_config = { effort: "low" };
    const r = await postJson("https://api.anthropic.com/v1/messages", { "x-api-key": apiKey, "anthropic-version": "2023-06-01" }, body);
    if (!r.ok) throw new Error(`HTTP ${r.status}: ${r.text.slice(0, 300)}`);
    const j = r.json as {
      content: { type: string; text?: string }[];
      stop_reason: string;
      usage: { input_tokens: number; output_tokens: number; cache_read_input_tokens?: number; cache_creation_input_tokens?: number };
    };
    const u = j.usage;
    const out = {
      ...base,
      text: j.content.filter((b) => b.type === "text").map((b) => b.text ?? "").join("\n"),
      stop_reason: j.stop_reason,
      // Anthropic: input_tokens là phần KHÔNG cache; cộng lại để cùng nghĩa "tổng prompt" với 2 provider kia
      input_tokens: u.input_tokens + (u.cache_read_input_tokens ?? 0) + (u.cache_creation_input_tokens ?? 0),
      output_tokens: u.output_tokens,
      cache_read_tokens: u.cache_read_input_tokens ?? 0,
      cache_write_tokens: u.cache_creation_input_tokens ?? 0,
      reasoning_tokens: null,
      latency_ms: Date.now() - t0,
    };
    return { ...out, cost_usd: cost(model, out) };
  } catch (e) {
    return { ...base, text: "", stop_reason: "error", latency_ms: Date.now() - t0, cost_usd: null, error: e instanceof Error ? e.message : String(e) };
  }
}

// Nghi lộ đáp án: gợi ý chứa chữ cái phương án đúng dạng "A." / "đáp án A" hay kết quả số/đoạn text đáp án.
function leakSuspect(s: Sample, hint: string): boolean {
  const h = hint.toLowerCase().replace(/\s+/g, " ");
  const q = s.question;
  if (q.type === "multiple_choice") {
    const letter = LETTERS[q.answer];
    if (new RegExp(`(đáp án|phương án|chọn|là)\\s*${letter}\\b`, "i").test(hint)) return true;
    const optText = stripHtml(q.options[q.answer] ?? "").toLowerCase().replace(/\s+/g, " ").trim();
    if (optText.length >= 6 && h.includes(optText)) return true;
  }
  if (q.type === "short_answer") {
    const a = q.answer.trim().replace(".", ",");
    const alt = a.replace(",", ".");
    if (a && (h.includes(a.toLowerCase()) || h.includes(alt.toLowerCase()))) return true;
  }
  return false;
}

// ── xuất phiếu ──────────────────────────────────────────────────────────────────
interface Record_ {
  idx: number;
  sample: Sample;
  hints: { label: string; result: CallResult; leak_suspect: boolean }[];
}

function writeOutputs(records: Record_[], stamp: string) {
  const dir = path.resolve(scriptDir, "logs");
  fs.mkdirSync(dir, { recursive: true });
  const basePath = path.join(dir, `eval-ai-tutor-${stamp}`);

  fs.writeFileSync(`${basePath}.json`, JSON.stringify({ seed: SEED, n: records.length, models: MODELS, providers: PROVIDERS, records }, null, 2));

  const sheet: string[] = [
    `# Phiếu chấm gợi ý AI Tutor — ${stamp} (seed ${SEED}, ${records.length} câu)`,
    "",
    "Chấm từng gợi ý theo 3 tiêu chí, mỗi tiêu chí 0/1: **Không lộ** đáp án · **Đúng VL** (không sai kiến thức) · **Trúng chỗ sai**",
    "(nhắm đúng cái học sinh nhầm, không nói chung chung). Nhãn A/B/C đã xáo theo từng câu; khoá nhãn ở file `-khoa-nhan.md`, mở sau khi chấm.",
    "Cột *Nghi lộ (máy)* là kiểm tự động thô, chỉ để lưu ý — thầy quyết.",
    "",
  ];
  for (const r of records) {
    const s = r.sample;
    sheet.push(`## Câu ${r.idx} — đề #${s.exam_id} «${s.exam_title}», câu ${s.question_index + 1} · ${s.topic_name || "chưa gắn chủ đề"}`);
    sheet.push("");
    sheet.push("```");
    sheet.push(stripHtml(questionStem(s.question)));
    sheet.push("```");
    sheet.push(`- HS chọn: **${stripHtml(s.responseText)}**`);
    sheet.push(`- Đáp án đúng (chỉ thầy thấy): ${stripHtml(s.correctText)}`);
    sheet.push("");
    for (const h of r.hints) {
      sheet.push(`### Gợi ý ${h.label}${h.result.error ? " (LỖI gọi API)" : ""}`);
      sheet.push("");
      sheet.push(h.result.error ? `> ${h.result.error}` : h.result.text.split("\n").map((l) => `> ${l}`).join("\n"));
      sheet.push("");
      sheet.push(`Nghi lộ (máy): ${h.leak_suspect ? "CÓ" : "không"} · ${h.result.output_tokens} token ra · ${(h.result.latency_ms / 1000).toFixed(1)}s`);
      sheet.push("");
      sheet.push("| Không lộ | Đúng VL | Trúng chỗ sai | Ghi chú |");
      sheet.push("|---|---|---|---|");
      sheet.push("|  |  |  |  |");
      sheet.push("");
    }
  }
  fs.writeFileSync(`${basePath}-phieu-cham.md`, sheet.join("\n"));

  const key: string[] = [`# Khoá nhãn — ${stamp}`, "", "| Câu | Nhãn | Provider | Model | Chi phí (USD) |", "|---|---|---|---|---|"];
  for (const r of records) for (const h of r.hints) key.push(`| ${r.idx} | ${h.label} | ${h.result.provider} | ${h.result.model} | ${h.result.cost_usd?.toFixed(5) ?? "?"} |`);
  fs.writeFileSync(`${basePath}-khoa-nhan.md`, key.join("\n"));

  return basePath;
}

function summarize(records: Record_[]) {
  const by = new Map<string, { n: number; err: number; inp: number; out: number; reason: number; cacheRead: number; usd: number; ms: number; leak: number; peak: number }>();
  for (const r of records)
    for (const h of r.hints) {
      const k = `${h.result.provider}/${h.result.model}`;
      const a = by.get(k) ?? { n: 0, err: 0, inp: 0, out: 0, reason: 0, cacheRead: 0, usd: 0, ms: 0, leak: 0, peak: 0 };
      a.n += 1;
      if (h.result.error) a.err += 1;
      a.inp += h.result.input_tokens;
      a.out += h.result.output_tokens;
      a.reason += h.result.reasoning_tokens ?? 0;
      a.cacheRead += h.result.cache_read_tokens;
      a.usd += h.result.cost_usd ?? 0;
      a.ms += h.result.latency_ms;
      if (h.leak_suspect) a.leak += 1;
      if (h.result.is_peak) a.peak += 1;
      by.set(k, a);
    }
  console.log("\nTổng kết usage (chỉ số đo, chưa phải chất lượng — chất lượng do thầy chấm):");
  console.log("| Model | Lượt | Lỗi | TB token vào | TB token ra | TB suy luận | Cache đọc | TB giây | Nghi lộ | Σ USD | USD/1000 lượt | Giờ peak |");
  console.log("|---|---|---|---|---|---|---|---|---|---|---|---|");
  for (const [k, a] of by) {
    const ok = Math.max(1, a.n - a.err);
    console.log(
      `| ${k} | ${a.n} | ${a.err} | ${Math.round(a.inp / ok)} | ${Math.round(a.out / ok)} | ${Math.round(a.reason / ok)} | ${a.cacheRead} | ${(a.ms / a.n / 1000).toFixed(1)} | ${a.leak} | ${a.usd.toFixed(4)} | ${((a.usd / ok) * 1000).toFixed(2)} | ${a.peak}/${a.n} |`,
    );
  }
  console.log("\nGiá dùng để quy đổi là bảng PRICES tra 6/10/2026 trong script — tra lại trang chính thức trước khi trích dẫn.");
}

// ── main ────────────────────────────────────────────────────────────────────────
async function main() {
  const keys: Partial<Record<Provider, string>> = {
    deepseek: env("DEEPSEEK_API_KEY"),
    openai: env("OPENAI_API_KEY"),
    anthropic: env("ANTHROPIC_API_KEY"),
  };
  const active = PROVIDERS.filter((p) => {
    if (!keys[p]) console.log(`Bỏ qua ${p}: thiếu ${p.toUpperCase()}_API_KEY.`);
    return Boolean(keys[p]);
  });
  if (!DRY_RUN && active.length === 0) fail("không có provider nào có key. Thêm DEEPSEEK_API_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY vào .env.local hoặc chạy --dry-run.");

  const samples = await loadSamples(N);
  if (samples.length === 0) fail("không tìm được câu làm sai có đáp án đã chọn + lời giải.");
  console.log(`Chọn được ${samples.length} câu làm sai (seed ${SEED}).`);

  if (DRY_RUN) {
    console.log("\n=== SYSTEM ===\n" + SYSTEM_PROMPT);
    console.log("\n=== USER (câu 1) ===\n" + buildUserPrompt(samples[0]));
    console.log(`\n--dry-run: không gọi API. Sẽ gọi ${active.length} provider × ${samples.length} câu = ${active.length * samples.length} lượt.`);
    return;
  }

  const stamp = new Date().toISOString().slice(0, 16).replace(/[-:T]/g, "").replace(/(\d{8})(\d{4})/, "$1-$2");
  const records: Record_[] = [];
  for (let i = 0; i < samples.length; i += 1) {
    const s = samples[i];
    const user = buildUserPrompt(s);
    process.stdout.write(`Câu ${i + 1}/${samples.length} (đề #${s.exam_id} c${s.question_index + 1})…`);
    const results: CallResult[] = [];
    for (const p of active) {
      const r = await callProvider(p, MODELS[p], keys[p]!, user);
      results.push(r);
      process.stdout.write(r.error ? ` ${p}:LỖI` : ` ${p}:${r.output_tokens}tk`);
    }
    process.stdout.write("\n");
    const labels = shuffle(["A", "B", "C", "D"].slice(0, results.length));
    records.push({
      idx: i + 1,
      sample: s,
      hints: results.map((result, j) => ({ label: labels[j], result, leak_suspect: result.text ? leakSuspect(s, result.text) : false })),
    });
    // ghi dần để không mất nếu dừng giữa chừng
    writeOutputs(records, stamp);
  }
  const basePath = writeOutputs(records, stamp);
  summarize(records);
  console.log(`\nĐã ghi:\n  ${basePath}-phieu-cham.md  (thầy chấm)\n  ${basePath}-khoa-nhan.md   (mở sau khi chấm)\n  ${basePath}.json`);
}

main().catch((e) => fail(e instanceof Error ? e.message : String(e)));
