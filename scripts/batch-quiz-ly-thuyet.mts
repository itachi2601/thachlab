// Soạn HÀNG LOẠT bộ "Kiểm tra nhanh" lý thuyết (20 câu/bài) bằng Claude qua Message Batches API (nửa giá, dùng credit API).
// Thay cho bước B + C của skill soan-quiz-ly-thuyet khi thầy bảo "giao cho API". Không đọc/ghi Supabase:
// nguồn là public/data/lessons/<id>.json, đầu ra là scripts/data/theory-quiz/<id>.json (rồi đăng bằng publish-theory-quiz.mts).
//
//   npx tsx scripts/batch-quiz-ly-thuyet.mts --du-toan --lesson-ids 27,129,130          # đếm token, ước giá, KHÔNG gửi
//   npx tsx scripts/batch-quiz-ly-thuyet.mts --buoc sinh --gui --lesson-ids 129          # thử 1 bài → in batch id
//   npx tsx scripts/batch-quiz-ly-thuyet.mts --buoc sinh --nhan [--cho]                  # lấy bản nháp → logs/batch-quiz/sinh/<id>.json
//   npx tsx scripts/batch-quiz-ly-thuyet.mts --buoc kiem --gui                           # kiểm chéo ĐỘC LẬP các bản nháp đã nhận
//   npx tsx scripts/batch-quiz-ly-thuyet.mts --buoc kiem --nhan [--cho]                  # loại câu sai → validate → ghi scripts/data/theory-quiz/
//   npx tsx scripts/batch-quiz-ly-thuyet.mts --buoc ghichu --gui --lesson-ids …          # thêm distractorNotes (vì sao phương án sai) vào bộ ĐÃ có, giữ nguyên câu
//   npx tsx scripts/batch-quiz-ly-thuyet.mts --buoc ghichu --nhan [--cho]                # gộp ghi chú → validate → ghi đè scripts/data/theory-quiz/ (bản trước: logs/batch-quiz/ban-truoc-ghichu/)
//
// Tuỳ chọn: --model (sinh: claude-sonnet-5-5, kiem: claude-opus-5-5) · --effort (medium/high) · --lesson-ids a,b,c
// Cần .env.local: ANTHROPIC_API_KEY (+ ANTHROPIC_WORKSPACE_ID nếu key cấp tổ chức). Chạy trong tab terminal.

import Anthropic from "@anthropic-ai/sdk";
import fs from "node:fs";
import path from "node:path";
import { getLessonInfo, loadTopics, QUIZ_DIR, ROOT, validateQuiz } from "../.claude/skills/soan-quiz-ly-thuyet/scripts/lib";

const REF = path.join(ROOT, ".claude/skills/soan-quiz-ly-thuyet/references");
const LOG = path.join(ROOT, "scripts/logs/batch-quiz");
const argv = process.argv.slice(2);
const arg = (n: string) => (argv.includes(`--${n}`) ? argv[argv.indexOf(`--${n}`) + 1] : undefined);
const flag = (n: string) => argv.includes(`--${n}`);
const BUOC = (arg("buoc") ?? "sinh") as "sinh" | "kiem" | "ghichu";
if (!["sinh", "kiem", "ghichu"].includes(BUOC)) fail("--buoc phải là sinh, kiem hoặc ghichu");
const MODEL = arg("model") ?? (BUOC === "sinh" ? "claude-sonnet-5-5" : "claude-opus-5-5");
const EFFORT = (arg("effort") ?? (BUOC === "sinh" ? "medium" : "high")) as "low" | "medium" | "high";
const IDS = (arg("lesson-ids") ?? "").split(",").map((s) => Number(s.trim())).filter((n) => Number.isInteger(n) && n > 0);

function fail(m: string): never { console.error(`✗ ${m}`); process.exit(1); }
function env(key: string): string | undefined {
  if (process.env[key]) return process.env[key];
  const p = path.join(ROOT, ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const l = fs.readFileSync(p, "utf8").split("\n").find((x) => x.startsWith(`${key}=`));
  return l ? l.slice(key.length + 1).trim().replace(/^["']|["']$/g, "") : undefined;
}
const mk = (d: string) => { const p = path.join(LOG, d); fs.mkdirSync(p, { recursive: true }); return p; };
const SINH_DIR = mk("sinh"), KIEM_DIR = mk("kiem"), LAMLAI_DIR = mk("can-lam-lai"), GHICHU_DIR = mk("ghichu"), TRUOC_DIR = mk("ban-truoc-ghichu");
const BATCHES = path.join(LOG, "batches.json");
type BatchRec = { id: string; buoc: string; model: string; lessons: number[]; at: string };
const readBatches = (): BatchRec[] => (fs.existsSync(BATCHES) ? JSON.parse(fs.readFileSync(BATCHES, "utf8")) : []);

// ── đầu vào bài ───────────────────────────────────────────────────────────────
interface Bai { id: number; title: string; itemId: number; sections: { index: number; heading: string }[]; html: string; multi: boolean }
function loadBai(id: number): Bai {
  const info = getLessonInfo(id);
  if (info.items.length === 0) fail(`bài ${id}: không có mục ly_thuyet`);
  const it = info.items[0];
  const data = JSON.parse(fs.readFileSync(path.join(ROOT, "public/data/lessons", `${id}.json`), "utf8"));
  const raw = data.items.find((x: { id: number }) => x.id === it.itemId);
  return { id, title: info.title, itemId: it.itemId, sections: it.sections.map((s) => ({ index: s.index, heading: s.heading })), html: `${raw.summary_html ?? ""}\n${raw.body_html ?? ""}`, multi: info.items.length > 1 };
}
const secList = (b: Bai) => (b.sections.length ? b.sections.map((s) => `  đoạn ${s.index}: ${s.heading}`).join("\n") : "  (không có đoạn → bỏ trường theorySection)");

// ── prompt ────────────────────────────────────────────────────────────────────
const FORMAT = `
ĐỊNH DẠNG ĐẦU RA — chỉ in MỘT đối tượng JSON, không văn bản ngoài, không rào \`\`\`:
{"questions":[ ... 20 câu ... ]}
Mỗi câu có đủ: "type", "kind", "topic", "form":"ly_thuyet", "difficulty" ("de" hoặc "trung-binh"), "difficultySource":"ai", "theorySection" (số nguyên theo danh sách đoạn được cho; bỏ nếu bài không có đoạn), "question", "explanation", và:
- multiple_choice: "options": [4 chuỗi khác nhau], "answer": 0..3
- "distractorNotes" (bắt buộc với multiple_choice và true_false): mỗi giá trị MỘT câu ≤ 25 từ nêu đúng lỗi tư duy khiến học sinh chọn như vậy là sai, không vai "thầy", không nhắc tên phương án khác. multiple_choice: khoá là nhãn "A"|"B"|"C"|"D" của đúng 3 phương án SAI (không có khoá cho phương án đúng). true_false: khoá "0".."3" cho cả 4 ý — viết lý do vì sao chọn ngược lại với đáp án của ý đó là sai (ý đúng: vì sao không thể coi là sai; ý sai: vì sao không thể coi là đúng).
- true_false: "statements": [{"text":"…","answer":true|false} × đúng 4], ít nhất 1 ý sai
"topic": nếu được cho danh sách yêu cầu cần đạt thì chọn đúng tên sát nội dung câu; không có thì dùng đúng tên bài.
Cơ cấu cố định: 14 multiple_choice, 6 true_false, KHÔNG có short_answer; 10 câu kind kiến thức (dinh_nghia|dinh_luat|hien_tuong|dieu_kien) + 10 câu kind công thức (cong_thuc|don_vi|tinh_nhanh|bien_doi). Bài ít công thức thì bù bằng câu kiến thức nhưng vẫn đủ 20 câu.
Công thức LaTeX trong $…$, cân dấu $; dùng \\\\lt, \\\\gt thay cho < >. Trong JSON, mỗi dấu \\ của LaTeX phải viết thành \\\\.`;
const BO = fs.readFileSync(path.join(REF, "phong-cach-de-bo-gd.md"), "utf8");
const SYS_SINH = `${fs.readFileSync(path.join(REF, "prompt-sinh-cau.md"), "utf8")}\n${BO}\n(Học sinh có thể là THCS hoặc THPT tuỳ bài; bám đúng mức của bài.)\n${FORMAT}`;
const SYS_KIEM = `${fs.readFileSync(path.join(REF, "prompt-kiem-cheo.md"), "utf8")}\n${BO}
Áp dụng thêm "Quy tắc loại câu ngoài chương trình" ở trên: câu hỏi kiến thức không thuộc chương trình Vật lí 12 hoặc chỉ lấy từ phần đọc thêm/em có biết → verdict "nghi_ngo" kèm reason bắt đầu bằng "NGOÀI CHƯƠNG TRÌNH".
ĐỊNH DẠNG ĐẦU RA — chỉ in MỘT đối tượng JSON: {"results":[{"i":1,"verdict":"dung|sai|nghi_ngo","reason":"…","section_ok":true,"section_should_be":null}, … mỗi câu một phần tử]}
Kiểm cả "distractorNotes": ghi chú nào sai về vật lí, nói đúng phương án đúng là sai, nhắc tên phương án khác, hoặc thiếu so với quy định → verdict "nghi_ngo" kèm reason bắt đầu bằng "GHI CHÚ".
Nội dung bài và các câu được đưa ngay trong tin nhắn (không cần đọc file). Với câu tính toán, tự tính lại độc lập.`;

const SYS_GHICHU = `Bạn là giáo viên vật lí THPT. Đầu vào: nội dung bài lý thuyết và bộ câu hỏi ĐÃ chốt (đáp án và lời giải đúng). Việc duy nhất: viết "distractorNotes" cho từng câu, KHÔNG sửa câu, đáp án hay lời giải.
Quy tắc: mỗi ghi chú MỘT câu, ≤ 25 từ, nêu đúng lỗi tư duy khiến học sinh chọn như vậy là sai (nhầm chiều, nhầm đại lượng, áp quy tắc sai điều kiện, đảo tỉ lệ…), bám nội dung bài, không vai "thầy", không nhắc tên phương án khác (thứ tự có thể bị xáo), không nhắc "đáp án đúng là X".
- multiple_choice: khoá là nhãn "A"|"B"|"C"|"D" của đúng 3 phương án SAI (nhãn theo thứ tự options: 0=A,1=B,2=C,3=D); không có khoá cho phương án đúng.
- true_false: khoá "0".."3" cho cả 4 ý; viết lý do vì sao chọn NGƯỢC với đáp án của ý đó là sai (ý đúng: vì sao không thể coi là sai; ý sai: vì sao không thể coi là đúng).
Công thức LaTeX trong $…$, cân dấu $. Trong JSON mỗi dấu \\ của LaTeX viết thành \\\\.
Nếu thấy đáp án của câu nào có vẻ SAI so với bài, đừng viết ghi chú cho câu đó mà ghi vào "nghi_van".
ĐỊNH DẠNG: chỉ in MỘT đối tượng JSON: {"notes":[{"i":1,"distractorNotes":{...}}, … mỗi câu trắc nghiệm / đúng–sai một phần tử, i tính từ 1 theo thứ tự câu được đưa], "nghi_van":[{"i":3,"reason":"…"}]}`;

function userSinh(b: Bai, topics: string[] | undefined): string {
  return [`Bài ${b.id}: ${b.title}`, `item_id: ${b.itemId}`, `Danh sách đoạn:\n${secList(b)}`,
    topics?.length ? `Yêu cầu cần đạt của bài (chọn làm "topic"):\n${topics.map((t) => `- ${t}`).join("\n")}` : `Không có danh sách yêu cầu cần đạt → "topic" = "${b.title}".`,
    `<body_html>\n${b.html}\n</body_html>`].join("\n\n");
}
function userKiem(b: Bai, qs: unknown[]): string {
  return [`Bài ${b.id}: ${b.title}`, `Danh sách đoạn:\n${secList(b)}`, `<body_html>\n${b.html}\n</body_html>`,
    `<cac_cau>\n${qs.map((q, i) => `#${i + 1} ${JSON.stringify(q)}`).join("\n")}\n</cac_cau>`].join("\n\n");
}

// ── API ───────────────────────────────────────────────────────────────────────
const client = new Anthropic({
  apiKey: env("ANTHROPIC_API_KEY") ?? fail("thiếu ANTHROPIC_API_KEY trong .env.local"),
  ...(env("ANTHROPIC_WORKSPACE_ID") ? { defaultHeaders: { "anthropic-workspace-id": env("ANTHROPIC_WORKSPACE_ID")! } } : {}),
});
const prefix = (buoc: string) => `quiz-${buoc}-`;
function paramsOf(b: Bai, draft?: unknown[]): Anthropic.MessageCreateParamsNonStreaming {
  const topics = loadTopics()?.get(b.id);
  return {
    model: MODEL,
    max_tokens: 32000,
    system: [{ type: "text", text: BUOC === "sinh" ? SYS_SINH : BUOC === "ghichu" ? SYS_GHICHU : SYS_KIEM, cache_control: { type: "ephemeral" } }],
    messages: [{ role: "user", content: BUOC === "sinh" ? userSinh(b, topics) : userKiem(b, draft!) }],
    output_config: { effort: EFFORT },
  };
}
const draftOf = (id: number) => {
  const p = BUOC === "ghichu" ? path.join(QUIZ_DIR, `${id}.json`) : path.join(SINH_DIR, `${id}.json`);
  return fs.existsSync(p) ? (JSON.parse(fs.readFileSync(p, "utf8")).questions as unknown[]) : null;
};
const textOf = (m: Anthropic.Message) => m.content.filter((c): c is Anthropic.TextBlock => c.type === "text").map((c) => c.text).join("");
// Model hay thêm "Tổng kết…" hoặc rào ``` quanh JSON → cắt từ { đầu tới } cuối.
function parseJson(t: string): any { const a = t.indexOf("{"), z = t.lastIndexOf("}"); return JSON.parse(a >= 0 && z > a ? t.slice(a, z + 1) : t); }

async function gui(dryRun: boolean) {
  if (IDS.length === 0) fail("cần --lesson-ids a,b,c");
  const reqs: { custom_id: string; params: Anthropic.MessageCreateParamsNonStreaming }[] = [];
  const lessons: number[] = [];
  for (const id of IDS) {
    const b = loadBai(id);
    if (b.multi) console.warn(`  ! bài ${id}: nhiều mục lý thuyết, chỉ dùng mục đầu (itemId ${b.itemId})`);
    let draft: unknown[] | undefined;
    if (BUOC !== "sinh") { draft = draftOf(id) ?? undefined; if (!draft) { console.warn(`  ! bài ${id}: chưa có bản nháp (chạy --buoc sinh --nhan trước), bỏ qua`); continue; } }
    reqs.push({ custom_id: `${prefix(BUOC)}${id}`, params: paramsOf(b, draft) });
    lessons.push(id);
  }
  console.log(`Bước ${BUOC} · model ${MODEL} · effort ${EFFORT} · ${reqs.length} bài`);
  if (dryRun) {
    let tok = 0;
    for (const r of reqs) { const c = await client.messages.countTokens({ model: r.params.model, system: r.params.system, messages: r.params.messages }); tok += c.input_tokens; console.log(`  ${r.custom_id}: ${c.input_tokens} token vào`); }
    console.log(`Tổng ${tok} token vào (+ ~${reqs.length * (BUOC === "sinh" ? 14000 : 8000)} token ra ước tính). KHÔNG gửi gì.`);
    return;
  }
  if (reqs.length === 0) fail("không có request nào để gửi");
  const batch = await client.messages.batches.create({ requests: reqs });
  fs.writeFileSync(BATCHES, JSON.stringify([...readBatches(), { id: batch.id, buoc: BUOC, model: MODEL, lessons, at: new Date().toISOString() }], null, 1));
  console.log(`✓ Đã gửi batch ${batch.id} (${reqs.length} bài). Lấy kết quả: --buoc ${BUOC} --nhan --cho`);
}

async function nhan() {
  const recs = readBatches().filter((r) => r.buoc === BUOC);
  const rec = arg("nhan") && !arg("nhan")!.startsWith("--") ? recs.find((r) => r.id === arg("nhan")) : recs[recs.length - 1];
  if (!rec) fail(`chưa có batch bước ${BUOC}`);
  let batch = await client.messages.batches.retrieve(rec.id);
  while (batch.processing_status !== "ended") {
    const c = batch.request_counts;
    console.log(`  ${batch.processing_status}: đang xử lý ${c.processing}, xong ${c.succeeded}, lỗi ${c.errored}`);
    if (!flag("cho")) return console.log("Chưa xong — thêm --cho để đợi.");
    await new Promise((r) => setTimeout(r, 60_000));
    batch = await client.messages.batches.retrieve(rec.id);
  }
  const loi: string[] = [];
  const ok: number[] = [];
  const got = new Map<number, any>();
  for await (const r of await client.messages.batches.results(rec.id)) {
    const id = Number(r.custom_id.replace(prefix(BUOC), ""));
    if (r.result.type !== "succeeded") { loi.push(`${id}: ${r.result.type}`); continue; }
    const m = r.result.message;
    if (m.stop_reason === "max_tokens" || m.stop_reason === "refusal") { loi.push(`${id}: ${m.stop_reason}`); continue; }
    try { got.set(id, parseJson(textOf(m))); } catch { loi.push(`${id}: JSON hỏng`); fs.writeFileSync(path.join(LOG, `${id}.${BUOC}.raw.txt`), textOf(m)); }
  }
  if (BUOC === "ghichu") {
    const xong: string[] = [], redo: string[] = [];
    for (const [id, d] of got) {
      fs.writeFileSync(path.join(GHICHU_DIR, `${id}.json`), JSON.stringify(d, null, 1));
      const file = path.join(QUIZ_DIR, `${id}.json`);
      const quiz = JSON.parse(fs.readFileSync(file, "utf8"));
      const byI = new Map<number, any>((Array.isArray(d.notes) ? d.notes : []).map((x: any) => [x.i, x.distractorNotes]));
      const nghi = new Set<number>((Array.isArray(d.nghi_van) ? d.nghi_van : []).map((x: any) => x.i));
      quiz.questions.forEach((q: any, idx: number) => { const n = byI.get(idx + 1); if (n && typeof n === "object") q.distractorNotes = n; });
      const { errors, warnings } = validateQuiz(quiz, { topics: loadTopics() });
      const thieu = warnings.filter((w) => w.includes("distractorNotes")).length;
      if (errors.length) { fs.writeFileSync(path.join(LAMLAI_DIR, `${id}.ghichu.json`), JSON.stringify(quiz, null, 1)); redo.push(`${id}: ${errors.slice(0, 3).join("; ")}`); continue; }
      fs.copyFileSync(file, path.join(TRUOC_DIR, `${id}.json`));
      fs.writeFileSync(file, JSON.stringify(quiz, null, 1) + "\n");
      xong.push(`${id} (${quiz.questions.length} câu${thieu ? `, ${thieu} câu thiếu ghi chú` : ""}${nghi.size ? `, nghi vấn đáp án: câu ${[...nghi].join(",")}` : ""})`);
    }
    console.log(`✓ Đã gộp ghi chú: ${xong.length} bài\n  ${xong.join("\n  ")}`);
    if (redo.length) console.log(`✗ Cần xem tay (bản ở logs/batch-quiz/can-lam-lai/):\n  ${redo.join("\n  ")}`);
  } else if (BUOC === "sinh") {
    for (const [id, d] of got) {
      if (!Array.isArray(d.questions)) { loi.push(`${id}: thiếu questions`); continue; }
      fs.writeFileSync(path.join(SINH_DIR, `${id}.json`), JSON.stringify(d, null, 1)); ok.push(id);
    }
    console.log(`✓ Nháp: ${ok.length} bài [${ok.join(",")}]. Tiếp: --buoc kiem --gui --lesson-ids ${ok.join(",")}`);
  } else {
    const reviewed: string[] = [], redo: string[] = [];
    for (const [id, d] of got) {
      const draft = draftOf(id)!;
      const b = loadBai(id);
      const res: any[] = Array.isArray(d.results) ? d.results : [];
      fs.writeFileSync(path.join(KIEM_DIR, `${id}.json`), JSON.stringify(d, null, 1));
      const verdict = new Map<number, any>(res.map((x) => [x.i, x]));
      const kept: any[] = [], removed: { question: string; reason: string }[] = [];
      draft.forEach((q: any, idx) => {
        const v = verdict.get(idx + 1);
        if (!v || v.verdict !== "dung") { removed.push({ question: String(q.question).slice(0, 200), reason: v ? `${v.verdict}: ${v.reason}` : "không có phán quyết" }); return; }
        if (b.sections.length) {
          if (v.section_ok === false && Number.isInteger(v.section_should_be) && v.section_should_be >= 0 && v.section_should_be < b.sections.length) q.theorySection = v.section_should_be;
          else if (v.section_ok === false) delete q.theorySection;
        }
        kept.push(q);
      });
      const KN = ["dinh_nghia", "dinh_luat", "hien_tuong", "dieu_kien"];
      const kien = kept.filter((q) => KN.includes(q.kind)).length;
      const out = { lesson_id: id, lesson_title: b.title, item_id: b.itemId, generated_at: new Date().toISOString().slice(0, 10), generated_by: `batch-api ${rec.model}`,
        quiz_min_correct: Math.ceil(kept.length * 0.75), review: { checked: true, counts: { kien_thuc: kien, cong_thuc: kept.length - kien }, removed }, questions: kept };
      const { errors, warnings } = validateQuiz(out, { topics: loadTopics() });
      if (errors.length) { fs.writeFileSync(path.join(LAMLAI_DIR, `${id}.json`), JSON.stringify(out, null, 1)); redo.push(`${id}: ${errors.slice(0, 3).join("; ")}`); continue; }
      fs.writeFileSync(path.join(QUIZ_DIR, `${id}.json`), JSON.stringify(out, null, 1) + "\n");
      reviewed.push(`${id} (${kept.length} câu, loại ${removed.length}${warnings.length ? `, ${warnings.length} cảnh báo` : ""})`);
    }
    console.log(`✓ Ghi vào scripts/data/theory-quiz/: ${reviewed.length} bài\n  ${reviewed.join("\n  ")}`);
    if (redo.length) console.log(`✗ Cần làm lại / xem tay (bản nháp ở scripts/logs/batch-quiz/can-lam-lai/):\n  ${redo.join("\n  ")}`);
  }
  const u = batch.request_counts;
  console.log(`Batch ${rec.id}: ${u.succeeded} thành công, ${u.errored} lỗi, ${u.expired} hết hạn.`);
  if (loi.length) console.log(`✗ Lỗi:\n  ${loi.join("\n  ")}`);
}

if (flag("du-toan")) await gui(true);
else if (flag("gui")) await gui(false);
else if (flag("nhan")) await nhan();
else fail("cần --du-toan | --gui | --nhan");
