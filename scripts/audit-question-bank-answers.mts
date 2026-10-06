// Kiểm lại đáp án ngân hàng câu hỏi bằng DeepSeek — CHỈ ĐỌC, KHÔNG GHI gì vào DB.
//
// Cách làm: model giải MÙ từng câu (không thấy đáp án/lời giải đang lưu), rồi so với đáp án trong
// question_bank. Lượt 1 dùng deepseek-flash; lượt 2 (--stage 2) giải lại các câu lệch bằng
// deepseek-v4-pro. Kết quả ra scripts/logs/audit-bank-*.json (+ .csv) để thầy duyệt; việc sửa
// đáp án là script riêng, chạy sau khi duyệt.
//
//   npx tsx scripts/audit-question-bank-answers.mts --grade 12 --limit 200            # lượt 1, mẫu ngẫu nhiên
//   npx tsx scripts/audit-question-bank-answers.mts --stage 2 --in scripts/logs/audit-bank-XXXX.json
//   Tuỳ chọn: --conc 30 (số cuộc gọi song song) · --seed 1 · --resume <file.json> · --ignore-peak
//
// Giá DeepSeek tính nửa tiền ngoài giờ cao điểm (01–04 & 06–10 giờ UTC, T2–T6 = 08–11 & 13–17 giờ VN),
// nên mặc định script tự ngủ khi vào giờ cao điểm; --ignore-peak để chạy bất chấp.
//
// Bỏ qua (không tốn API): câu tự luận, câu có ảnh/SVG trong đề hoặc phương án (model không đọc được).
// Cần .env.local có NEXT_PUBLIC_SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, DEEPSEEK_API_KEY.

import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import type { ExamQuestion } from "@/features/exams/types";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const LOG_DIR = path.join(scriptDir, "logs");
const LETTERS = ["A", "B", "C", "D"];

// Giá USD / 1M token ngoài giờ cao điểm (api-docs.deepseek.com/quick_start/pricing, 6/10/2026). Cao điểm ×2.
const PRICE = {
  "deepseek-flash": { in: 0.15, out: 0.6 },
  "deepseek-v4-pro": { in: 0.66, out: 1.98 },
} as const;
type Model = keyof typeof PRICE;

function readEnvLocal(key: string): string | undefined {
  const p = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const line = fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}
function fail(msg: string): never {
  console.error("Lỗi:", msg);
  process.exit(1);
}
const sleep = (ms: number) => new Promise<void>((r) => setTimeout(r, ms));

function arg(name: string): string | undefined {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 ? process.argv[i + 1] : undefined;
}
const flag = (name: string) => process.argv.includes(`--${name}`);

// ---------- Giờ cao điểm ----------
function isPeak(d = new Date()): boolean {
  const dow = d.getUTCDay(); // 0 CN … 6 T7
  if (dow === 0 || dow === 6) return false;
  const h = d.getUTCHours();
  return (h >= 1 && h < 4) || (h >= 6 && h < 10);
}
async function waitOffPeak(ignore: boolean) {
  if (ignore) return;
  let told = false;
  while (isPeak()) {
    if (!told) {
      console.log(`  ⏸ đang giờ cao điểm DeepSeek (giá gấp đôi) — tạm dừng, kiểm lại mỗi 5 phút… (${new Date().toISOString()})`);
      told = true;
    }
    await sleep(5 * 60_000);
  }
  if (told) console.log("  ▶ hết cao điểm, chạy tiếp.");
}

// ---------- Chuẩn hoá nội dung gửi model ----------
function htmlToText(html: string): string {
  return html
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<\/(p|div|li|tr|h\d)>/gi, "\n")
    .replace(/<[^>]+>/g, "")
    .replace(/&nbsp;/g, " ")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"')
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}
const hasMedia = (s: string) => /<(img|svg|canvas|video|iframe)\b/i.test(s);

interface Prepared {
  text: string; // đề + phương án, KHÔNG có đáp án/lời giải
  expected: unknown; // đáp án đang lưu
}

/** Trả null + lý do nếu không kiểm được bằng văn bản. */
function prepare(q: ExamQuestion): Prepared | { skip: string } {
  if (q.type === "essay") return { skip: "tu_luan" };
  if (q.type === "multiple_choice") {
    if (!Array.isArray(q.options) || q.options.length !== 4 || typeof q.answer !== "number") return { skip: "du_lieu_loi" };
    if (hasMedia(q.question) || q.options.some(hasMedia)) return { skip: "co_anh" };
    const text =
      `${htmlToText(q.question)}\n` + q.options.map((o, i) => `${LETTERS[i]}. ${htmlToText(o)}`).join("\n");
    return { text, expected: q.answer };
  }
  if (q.type === "true_false") {
    if (!Array.isArray(q.statements) || q.statements.length !== 4) return { skip: "du_lieu_loi" };
    if (hasMedia(q.question) || q.statements.some((s) => hasMedia(s.text))) return { skip: "co_anh" };
    const text =
      `${htmlToText(q.question)}\n` + q.statements.map((s, i) => `${"abcd"[i]}) ${htmlToText(s.text)}`).join("\n");
    return { text, expected: q.statements.map((s) => !!s.answer) };
  }
  if (q.type === "short_answer") {
    if (hasMedia(q.question)) return { skip: "co_anh" };
    if (typeof q.answer !== "string" || !q.answer.trim()) return { skip: "du_lieu_loi" };
    return { text: htmlToText(q.question), expected: q.answer };
  }
  return { skip: "du_lieu_loi" };
}

const SYSTEM =
  "Bạn là giáo viên Vật lí THPT Việt Nam, giải câu hỏi chính xác. Đề dùng LaTeX trong $...$. Hãy tự giải cẩn thận từ đầu " +
  "(đổi đơn vị, làm tròn đúng yêu cầu đề). Nếu đề thiếu dữ kiện/hình vẽ nên không thể giải chắc chắn, đặt \"answer\": null. " +
  "Chỉ trả về MỘT JSON hợp lệ, không văn bản khác.";

function userPrompt(type: ExamQuestion["type"], text: string): string {
  const fmt =
    type === "multiple_choice"
      ? 'Chọn đúng 1 phương án. Trả: {"answer":"A","reason":"≤40 từ"} (answer là A, B, C hoặc D).'
      : type === "true_false"
        ? 'Với từng ý a,b,c,d xác định Đúng/Sai. Trả: {"answer":[true,false,true,true],"reason":"≤60 từ"} (đúng 4 phần tử boolean theo thứ tự a,b,c,d).'
        : 'Trả lời bằng MỘT số, dùng dấu phẩy thập phân kiểu Việt Nam (vd "-1,5"), tối đa 4 ký tự, làm tròn đúng theo đề. Trả: {"answer":"12,5","reason":"≤40 từ"}.';
  return `${text}\n\n${fmt}`;
}

// ---------- Gọi DeepSeek ----------
interface Usage {
  prompt: number;
  completion: number;
}
interface Solved {
  answer: unknown; // null nếu model không chắc
  reason: string;
  usage: Usage;
}

async function solve(apiKey: string, model: Model, type: ExamQuestion["type"], text: string): Promise<Solved> {
  let lastErr: unknown;
  for (let attempt = 1; attempt <= 3; attempt += 1) {
    try {
      const res = await fetch("https://api.deepseek.com/chat/completions", {
        method: "POST",
        headers: { "content-type": "application/json", authorization: `Bearer ${apiKey}` },
        body: JSON.stringify({
          model,
          max_tokens: 16000, // gồm cả phần suy luận
          response_format: { type: "json_object" },
          messages: [
            { role: "system", content: SYSTEM },
            { role: "user", content: userPrompt(type, text) },
          ],
        }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}: ${(await res.text()).slice(0, 200)}`);
      const data = (await res.json()) as {
        choices?: { message?: { content?: string } }[];
        usage?: { prompt_tokens?: number; completion_tokens?: number };
      };
      const usage = { prompt: data.usage?.prompt_tokens ?? 0, completion: data.usage?.completion_tokens ?? 0 };
      const raw = data.choices?.[0]?.message?.content ?? "";
      const a = raw.indexOf("{");
      const b = raw.lastIndexOf("}");
      if (a < 0 || b < 0) throw new Error("content rỗng/không có JSON");
      const parsed = JSON.parse(raw.slice(a, b + 1)) as { answer?: unknown; reason?: unknown };
      return { answer: parsed.answer ?? null, reason: String(parsed.reason ?? "").slice(0, 400), usage };
    } catch (e) {
      lastErr = e;
      if (attempt < 3) await sleep(2000 * attempt);
    }
  }
  throw lastErr;
}

// ---------- So đáp án ----------
function normNum(s: string): number | null {
  const n = Number(s.trim().replace(/\s/g, "").replace(",", "."));
  return Number.isFinite(n) ? n : null;
}
type Verdict = "khop" | "lech" | "khong_chac" | "loi_api";

function compare(q: ExamQuestion, expected: unknown, got: unknown): Verdict {
  if (got === null || got === undefined) return "khong_chac";
  if (q.type === "multiple_choice") {
    const idx = LETTERS.indexOf(String(got).trim().toUpperCase().slice(0, 1));
    return idx < 0 ? "khong_chac" : idx === expected ? "khop" : "lech";
  }
  if (q.type === "true_false") {
    if (!Array.isArray(got) || got.length !== 4 || got.some((x) => typeof x !== "boolean")) return "khong_chac";
    return (expected as boolean[]).every((v, i) => v === got[i]) ? "khop" : "lech";
  }
  const e = normNum(String(expected));
  const g = normNum(String(got));
  if (e === null || g === null) return String(expected).trim() === String(got).trim() ? "khop" : "lech";
  // sai số tương đối 1% (đề làm tròn nên không đòi khớp từng chữ số)
  return Math.abs(e - g) <= Math.max(1e-9, Math.abs(e) * 0.01) ? "khop" : "lech";
}

// ---------- Báo cáo ----------
interface Item {
  id: number;
  grade: string;
  type: string;
  topic: string;
  stored: unknown;
  s1?: { model: Model; answer: unknown; reason: string; verdict: Verdict; prompt: number; completion: number };
  s2?: { model: Model; answer: unknown; reason: string; verdict: Verdict; prompt: number; completion: number };
  skip?: string;
  /** nghi_sai = cả 2 model cùng lệch và trùng nhau; flash_nham = pro khớp DB; can_xem = còn lại */
  final?: "khop" | "nghi_sai" | "flash_nham" | "can_xem" | "bo_qua" | "chua_xong";
}
interface Report {
  startedAt: string;
  args: Record<string, string | number | boolean>;
  items: Item[];
}

function settle(it: Item) {
  if (it.skip) return (it.final = "bo_qua");
  if (!it.s1) return (it.final = "chua_xong");
  if (it.s1.verdict === "khop") return (it.final = "khop");
  if (!it.s2) return (it.final = "chua_xong");
  if (it.s2.verdict === "khop") return (it.final = "flash_nham");
  if (it.s2.verdict === "lech" && JSON.stringify(it.s2.answer) === JSON.stringify(it.s1.answer)) return (it.final = "nghi_sai");
  return (it.final = "can_xem");
}

function cost(items: Item[]) {
  let usd = 0;
  let tin = 0;
  let tout = 0;
  for (const it of items)
    for (const s of [it.s1, it.s2]) {
      if (!s) continue;
      usd += (s.prompt * PRICE[s.model].in + s.completion * PRICE[s.model].out) / 1e6;
      tin += s.prompt;
      tout += s.completion;
    }
  return { usd, tin, tout };
}

function save(file: string, rep: Report) {
  fs.writeFileSync(file, JSON.stringify(rep, null, 1));
  const csv = ["id,lop,dang,chu_de,db,flash,pro,ket_luan,ly_do_pro_hoac_flash"]
    .concat(
      rep.items.map((it) =>
        [
          it.id, it.grade, it.type, JSON.stringify(it.topic ?? ""), JSON.stringify(it.stored ?? ""),
          JSON.stringify(it.s1?.answer ?? ""), JSON.stringify(it.s2?.answer ?? ""), it.final ?? "",
          JSON.stringify((it.s2?.reason || it.s1?.reason || it.skip) ?? ""),
        ].join(","),
      ),
    )
    .join("\n");
  fs.writeFileSync(file.replace(/\.json$/, ".csv"), csv);
}

function summary(items: Item[]) {
  const c: Record<string, number> = {};
  for (const it of items) c[it.final ?? "?"] = (c[it.final ?? "?"] ?? 0) + 1;
  const k = cost(items);
  console.log("\nTổng kết:", c);
  console.log(
    `Token: ${k.tin} vào / ${k.tout} ra · chi phí ≈ $${k.usd.toFixed(3)} (giá giờ thấp điểm${isPeak() ? " — hiện đang cao điểm, thực tế ×2" : ""}).`,
  );
}

async function pool<T>(list: T[], conc: number, fn: (x: T, n: number) => Promise<void>) {
  let next = 0;
  await Promise.all(
    Array.from({ length: conc }, async () => {
      for (;;) {
        const i = next++;
        if (i >= list.length) return;
        await fn(list[i], i);
      }
    }),
  );
}

function mulberry32(a: number) {
  return () => {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// ---------- main ----------
async function main() {
  const stage = Number(arg("stage") ?? 1);
  const conc = Number(arg("conc") ?? 30);
  const ignorePeak = flag("ignore-peak");
  const deepseekKey = process.env.DEEPSEEK_API_KEY ?? readEnvLocal("DEEPSEEK_API_KEY");
  if (!deepseekKey) fail("thiếu DEEPSEEK_API_KEY");
  fs.mkdirSync(LOG_DIR, { recursive: true });

  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
  const serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY ?? readEnvLocal("SUPABASE_SERVICE_ROLE_KEY");
  if (!supabaseUrl || !serviceKey) fail("thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY");
  const supabase = createClient(supabaseUrl, serviceKey, { auth: { autoRefreshToken: false, persistSession: false } });

  async function fetchQuestions(ids: number[]) {
    const out = new Map<number, ExamQuestion>();
    for (let i = 0; i < ids.length; i += 200) {
      const { data, error } = await supabase.from("question_bank").select("id, question").in("id", ids.slice(i, i + 200));
      if (error) fail(`đọc question_bank lỗi: ${error.message}`);
      for (const r of data ?? []) out.set(r.id as number, r.question as ExamQuestion);
    }
    return out;
  }

  let rep: Report;
  let file: string;

  if (stage === 1) {
    const resume = arg("resume");
    if (resume) {
      file = path.resolve(resume);
      rep = JSON.parse(fs.readFileSync(file, "utf8")) as Report;
      console.log(`Chạy tiếp ${file}: ${rep.items.filter((i) => !i.s1 && !i.skip).length} câu chưa xong.`);
    } else {
      const grade = arg("grade");
      const limit = arg("limit") ? Number(arg("limit")) : undefined;
      const seed = Number(arg("seed") ?? 1);
      const all: { id: number; grade: string; topic_name: string; question: ExamQuestion }[] = [];
      for (let from = 0; ; from += 1000) {
        let q = supabase.from("question_bank").select("id, grade, topic_name, question").eq("archived", false).order("id");
        if (grade) q = q.eq("grade", grade);
        const { data, error } = await q.range(from, from + 999);
        if (error) fail(`đọc question_bank lỗi: ${error.message}`);
        all.push(...(data as typeof all));
        if ((data?.length ?? 0) < 1000) break;
      }
      console.log(`Đọc ${all.length} câu${grade ? ` lớp ${grade}` : ""} (chưa lưu trữ).`);
      // Chỉ lấy mẫu trong số câu kiểm được bằng văn bản, trộn theo seed để mẫu trải đều các dạng/chủ đề.
      const rnd = mulberry32(seed);
      const shuffled = all.map((r) => ({ r, k: rnd() })).sort((a, b) => a.k - b.k).map((x) => x.r);
      const items: Item[] = [];
      const skipCount: Record<string, number> = {};
      for (const r of shuffled) {
        const p = prepare(r.question);
        if ("skip" in p) {
          skipCount[p.skip] = (skipCount[p.skip] ?? 0) + 1;
          continue;
        }
        if (limit && items.length >= limit) continue;
        items.push({ id: r.id, grade: r.grade, type: r.question.type, topic: r.topic_name ?? "", stored: p.expected });
      }
      console.log(`Kiểm được ${items.length} câu bằng văn bản; bỏ qua (không tốn API):`, skipCount);
      rep = { startedAt: new Date().toISOString(), args: { grade: grade ?? "", limit: limit ?? 0, seed, conc }, items };
      file = path.join(LOG_DIR, `audit-bank-${new Date().toISOString().replace(/[:.]/g, "-")}.json`);
    }

    const todo = rep.items.filter((i) => !i.s1 && !i.skip);
    const qmap = await fetchQuestions(todo.map((i) => i.id));
    let done = 0;
    await pool(todo, conc, async (it) => {
      await waitOffPeak(ignorePeak);
      const q = qmap.get(it.id);
      if (!q) { it.skip = "khong_doc_duoc"; return; }
      const p = prepare(q);
      if ("skip" in p) { it.skip = p.skip; return; }
      try {
        const r = await solve(deepseekKey, "deepseek-flash", q.type, p.text);
        it.s1 = { model: "deepseek-flash", answer: r.answer, reason: r.reason, verdict: compare(q, p.expected, r.answer), prompt: r.usage.prompt, completion: r.usage.completion };
      } catch (e) {
        it.s1 = { model: "deepseek-flash", answer: null, reason: String(e instanceof Error ? e.message : e).slice(0, 200), verdict: "loi_api", prompt: 0, completion: 0 };
      }
      done += 1;
      if (done % 20 === 0) {
        rep.items.forEach(settle);
        save(file, rep);
        console.log(`  ${done}/${todo.length} · ≈ $${cost(rep.items).usd.toFixed(3)}`);
      }
    });
  } else {
    const inFile = arg("in");
    if (!inFile) fail("--stage 2 cần --in <file audit lượt 1>");
    file = path.resolve(inFile);
    rep = JSON.parse(fs.readFileSync(file, "utf8")) as Report;
    // Câu lệch hoặc model không chắc ở lượt 1 (loại lỗi API: chạy lại lượt 1 bằng --resume trước).
    const todo = rep.items.filter((i) => i.s1 && (i.s1.verdict === "lech" || i.s1.verdict === "khong_chac") && !i.s2);
    console.log(`Lượt 2 (deepseek-v4-pro): ${todo.length} câu.`);
    const qmap = await fetchQuestions(todo.map((i) => i.id));
    let done = 0;
    await pool(todo, Math.min(conc, 20), async (it) => {
      await waitOffPeak(ignorePeak);
      const q = qmap.get(it.id);
      const p = q ? prepare(q) : { skip: "x" };
      if (!q || "skip" in p) return;
      try {
        const r = await solve(deepseekKey, "deepseek-v4-pro", q.type, p.text);
        it.s2 = { model: "deepseek-v4-pro", answer: r.answer, reason: r.reason, verdict: compare(q, p.expected, r.answer), prompt: r.usage.prompt, completion: r.usage.completion };
      } catch (e) {
        it.s2 = { model: "deepseek-v4-pro", answer: null, reason: String(e instanceof Error ? e.message : e).slice(0, 200), verdict: "loi_api", prompt: 0, completion: 0 };
      }
      done += 1;
      if (done % 10 === 0) { rep.items.forEach(settle); save(file, rep); console.log(`  ${done}/${todo.length}`); }
    });
  }

  rep.items.forEach(settle);
  save(file, rep);
  summary(rep.items);
  console.log(`\nBáo cáo: ${file}\n         ${file.replace(/\.json$/, ".csv")}`);
}

main().catch((e) => fail(e instanceof Error ? e.message : String(e)));
