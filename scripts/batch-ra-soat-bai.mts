// Rà soát HÀNG LOẠT bài lý thuyết bằng Claude qua Message Batches API (giá bằng nửa API thường, credit
// khuyến mãi Anthropic áp dụng được — Claude Code thì không). Mỗi bài là một request: Claude đọc mục
// lý thuyết như "lượt Claude" (bước 1b skill cap-nhat-bai-hoc-theo-gemini, prompt gốc
// .claude/skills/cap-nhat-bai-hoc-theo-gemini/references/PROMPT-CLAUDE-HOC-SINH.md) và trả JSON góp ý.
//
// CHỈ ĐỌC DB (lesson_items.kind='ly_thuyet'), KHÔNG ghi gì vào Supabase. Chỉ ghi file trong
// scripts/logs/batch-ra-soat/ và (nếu bài có thư mục trong content/lesson-samples theo content/gemini/hang-doi.md)
// gemini/nhan/hoc-sinh-trung-binh-claude.json để chế độ /gemini-nhan đọc tiếp.
//
//   npx tsx scripts/batch-ra-soat-bai.mts --du-toan [--lop 12] [--lesson-ids 10,11]   # đếm token, ước giá, KHÔNG gọi tính tiền
//   npx tsx scripts/batch-ra-soat-bai.mts --gui --lesson-ids 10                        # thử 1 bài → in batch id
//   npx tsx scripts/batch-ra-soat-bai.mts --gui --lop 12                               # cả lớp 12
//   npx tsx scripts/batch-ra-soat-bai.mts --gui                                        # mọi bài lý thuyết đã published
//   npx tsx scripts/batch-ra-soat-bai.mts --nhan [batch_id] [--cho]                    # lấy kết quả (mặc định batch mới nhất; --cho = đợi tới khi xong)
//   npx tsx scripts/batch-ra-soat-bai.mts --tong-hop                                   # gộp mọi kết quả đã nhận → BAO-CAO.md
//
// Tuỳ chọn: --model claude-opus-5-5 (mặc định) | claude-sonnet-5-5 · --effort high (mặc định) · --vai trung-binh
//           --limit N (số bài tối đa) · --chua-ra-soat (bỏ bài đã có kết quả)
//
// Cần .env.local: NEXT_PUBLIC_SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, ANTHROPIC_API_KEY.
// Chạy trong tab terminal của thầy (Bash sandbox chặn *.supabase.co). Giá tra 8/10/2026, chỉ để ước tính.

import Anthropic from "@anthropic-ai/sdk";
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const LOG_DIR = path.join(root, "scripts/logs/batch-ra-soat");
const KQ_DIR = path.join(LOG_DIR, "ket-qua");
fs.mkdirSync(KQ_DIR, { recursive: true });

// ── tham số ───────────────────────────────────────────────────────────────────
function arg(name: string): string | undefined {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 && !process.argv[i + 1]?.startsWith("--") ? process.argv[i + 1] : undefined;
}
const flag = (n: string) => process.argv.includes(`--${n}`);
const MODEL = arg("model") ?? "claude-opus-5-5";
const EFFORT = (arg("effort") ?? "high") as "low" | "medium" | "high" | "xhigh" | "max";
const VAI = arg("vai") ?? "trung-binh";

function envVar(key: string): string | undefined {
  if (process.env[key]) return process.env[key];
  const p = path.join(root, ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const line = fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim().replace(/^["']|["']$/g, "") : undefined;
}
function fail(msg: string): never {
  console.error(`✗ ${msg}`);
  process.exit(1);
}

// Giá USD/1M token API thường (batch = ½). Tra platform.claude.com/docs/en/about-claude/pricing trước khi tin.
const PRICE: Record<string, { input: number; output: number; cacheRead: number; cacheWrite: number }> = {
  "claude-opus-5-5": { input: 4, output: 20, cacheRead: 0.2, cacheWrite: 5 },
  "claude-sonnet-5-5": { input: 2, output: 10, cacheRead: 0.2, cacheWrite: 2.5 },
  "claude-haiku-5-5": { input: 0.1, output: 0.5, cacheRead: 0.01, cacheWrite: 0.125 },
};
function costUsd(model: string, u: { input_tokens: number; output_tokens: number; cache_read_input_tokens?: number | null; cache_creation_input_tokens?: number | null }): number | null {
  const p = PRICE[model];
  if (!p) return null;
  const batch = 0.5;
  return (
    ((u.input_tokens * p.input + u.output_tokens * p.output + (u.cache_read_input_tokens ?? 0) * p.cacheRead + (u.cache_creation_input_tokens ?? 0) * p.cacheWrite) / 1e6) * batch
  );
}

// ── prompt (lấy từ file tham chiếu của skill, một nguồn duy nhất) ─────────────
const PROMPT_FILE = ".claude/skills/cap-nhat-bai-hoc-theo-gemini/references/PROMPT-CLAUDE-HOC-SINH.md";
const PROFILE_FILE = ".claude/skills/cap-nhat-bai-hoc-theo-gemini/references/PROMPT-GEMINI-HOC-SINH.md";
function loadPrompt(): string {
  const raw = fs.readFileSync(path.join(root, PROMPT_FILE), "utf8");
  const marker = "## PROMPT (sao chép từ đây)";
  if (!raw.includes(marker)) fail(`không thấy "${marker}" trong ${PROMPT_FILE}`);
  let tpl = raw.split(marker)[1].split("\n## Lưu ý khi đọc kết quả")[0].trim();
  // Định nghĩa 3 hồ sơ nằm ở prompt Gemini — nhúng vào để không phải tham chiếu file ngoài.
  const g = fs.readFileSync(path.join(root, PROFILE_FILE), "utf8");
  const profiles = g.split("\n").filter((l) => /^- `(yeu|trung-binh|kha)`:/.test(l)).join("\n");
  tpl = tpl
    .replace("(xem định nghĩa hồ sơ ở `PROMPT-GEMINI-HOC-SINH.md`)", `(định nghĩa hồ sơ:\n${profiles}\n)`)
    .replace("Chỉ đọc đúng file {ĐƯỜNG DẪN}. Không đọc bất kỳ file nào trong thư mục `gemini/`.", "Nội dung bài nằm trong thẻ <bai_hoc> của tin nhắn.")
    .replaceAll("{LỚP}", "{lớp ghi trong tin nhắn}")
    .replaceAll('"{TÊN BÀI}"', "{tên bài ghi trong tin nhắn}")
    .replaceAll("{VAI}", "{hồ sơ ghi trong tin nhắn}");
  return tpl;
}
const SYSTEM = loadPrompt();

// JSON schema khớp đầu ra trong prompt — structured output để khỏi vỡ JSON.
const LOAI = ["mơ_hồ", "thiếu_ví_dụ", "từ_chưa_giải_thích", "nhảy_bước", "quá_dài", "lặp_ý", "phương_án_nhiễu_khó_hiểu", "nghi_sai_đáp_án", "khác"];
const SCHEMA = {
  type: "object",
  additionalProperties: false,
  required: ["bai", "vai", "nguon", "gop_y", "du_doan_loi_sai"],
  properties: {
    bai: { type: "string" },
    vai: { type: "string" },
    nguon: { type: "string", enum: ["claude"] },
    gop_y: {
      type: "array",
      items: {
        type: "object",
        additionalProperties: false,
        required: ["id", "vi_tri", "trich_nguyen_van", "loai", "muc", "em_hieu_la", "de_xuat"],
        properties: {
          id: { type: "string" },
          vi_tri: { type: "string" },
          trich_nguyen_van: { type: "string" },
          loai: { type: "string", enum: LOAI },
          muc: { type: "string", enum: ["chặn", "khó", "nhỏ"] },
          em_hieu_la: { type: "string" },
          de_xuat: { type: "string" },
        },
      },
    },
    du_doan_loi_sai: {
      type: "array",
      items: {
        type: "object",
        additionalProperties: false,
        required: ["cau", "dap_an_sai_hap_dan", "loi_tu_duy", "bai_da_nhan_manh", "trich_nguyen_van"],
        properties: {
          cau: { type: "string" },
          dap_an_sai_hap_dan: { type: "string" },
          loi_tu_duy: { type: "string" },
          bai_da_nhan_manh: { type: "boolean" },
          trich_nguyen_van: { type: "string" },
        },
      },
    },
  },
};

// ── nội dung bài ──────────────────────────────────────────────────────────────
// Giữ HTML (tên mục, lớp tl-ok lộ đáp án đúng — prompt dựa vào đó), bỏ phần nặng vô nghĩa với model.
function stripHeavy(html: string): string {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, "")
    .replace(/<style[\s\S]*?<\/style>/gi, "")
    .replace(/<svg[\s\S]*?<\/svg>/gi, "[hình vẽ minh hoạ]")
    .replace(/<img[^>]*>/gi, "[ảnh]")
    .replace(/data:[a-z/+-]+;base64,[A-Za-z0-9+/=]+/g, "")
    .replace(/\s(style|data-[\w-]+|aria-[\w-]+|tabindex|role)="[^"]*"/g, "")
    .replace(/<!--[\s\S]*?-->/g, "")
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n");
}

function danhMucYccd(lessonId: number): string {
  const tp = path.join(root, "scripts/data/question-topics.json");
  if (!fs.existsSync(tp)) return "(không có danh mục)";
  const all = JSON.parse(fs.readFileSync(tp, "utf8")) as { id: number; lesson_id: number; name: string; parent_id: number | null }[];
  const mine = all.filter((t) => t.lesson_id === lessonId);
  const leaves = mine.filter((t) => !mine.some((u) => u.parent_id === t.id));
  const list = leaves.length ? leaves : mine;
  return list.length ? list.map((t) => `- ${t.name}`).join("\n") : "(không có danh mục)";
}

interface Bai { lessonId: number; itemId: number; ten: string; lop: string; chuong: string; html: string }

async function layBai(): Promise<Bai[]> {
  const url = envVar("NEXT_PUBLIC_SUPABASE_URL") ?? fail("thiếu NEXT_PUBLIC_SUPABASE_URL");
  const key = envVar("SUPABASE_SERVICE_ROLE_KEY") ?? fail("thiếu SUPABASE_SERVICE_ROLE_KEY");
  const sb = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });

  const [lessons, chapters, cc, classes, items] = await Promise.all([
    sb.from("lessons").select("id,title,chapter_id,published"),
    sb.from("chapters").select("id,title"),
    sb.from("chapter_classes").select("chapter_id,class_id"),
    sb.from("classes").select("id,name"),
    sb.from("lesson_items").select("id,lesson_id,body_html").eq("kind", "ly_thuyet"),
  ]);
  for (const r of [lessons, chapters, cc, classes, items]) if (r.error) fail(`Supabase: ${r.error.message}`);

  const chapterTitle = new Map(chapters.data!.map((c) => [c.id, c.title as string]));
  const className = new Map(classes.data!.map((c) => [c.id, c.name as string]));
  const chapterClass = new Map<number, string>();
  for (const r of cc.data!) if (!chapterClass.has(r.chapter_id)) chapterClass.set(r.chapter_id, className.get(r.class_id) ?? "");
  const lessonById = new Map(lessons.data!.map((l) => [l.id, l]));

  const ids = arg("lesson-ids")?.split(",").map((s) => Number(s.trim()));
  const lopFilter = arg("lop");
  const out: Bai[] = [];
  for (const it of items.data!) {
    const l = lessonById.get(it.lesson_id);
    if (!l || !l.published) continue;
    if (ids && !ids.includes(l.id)) continue;
    const lopName = chapterClass.get(l.chapter_id) ?? "";
    const lop = lopName.match(/\d+/)?.[0] ?? "?";
    if (lopFilter && lop !== lopFilter) continue;
    const html = stripHeavy(it.body_html ?? "");
    if (html.replace(/<[^>]+>/g, "").trim().length < 400) continue; // mục trống/quá ngắn, chưa có bài
    if (flag("chua-ra-soat") && fs.existsSync(path.join(KQ_DIR, `${l.id}.json`))) continue;
    out.push({ lessonId: l.id, itemId: it.id, ten: l.title, lop, chuong: chapterTitle.get(l.chapter_id) ?? "", html });
  }
  out.sort((a, b) => a.lessonId - b.lessonId);
  const limit = Number(arg("limit") ?? 0);
  return limit ? out.slice(0, limit) : out;
}

function userMessage(b: Bai): string {
  return [
    `Lớp: ${b.lop}`,
    `Chương: ${b.chuong}`,
    `Tên bài: ${b.ten}`,
    `Hồ sơ học sinh: ${VAI}`,
    `Danh mục yêu cầu cần đạt của bài (phạm vi kiến thức):\n${danhMucYccd(b.lessonId)}`,
    ``,
    `<bai_hoc>\n${b.html}\n</bai_hoc>`,
  ].join("\n");
}

function params(b: Bai): Anthropic.MessageCreateParamsNonStreaming {
  return {
    model: MODEL,
    max_tokens: 16000,
    system: [{ type: "text", text: SYSTEM, cache_control: { type: "ephemeral" } }],
    messages: [{ role: "user", content: userMessage(b) }],
    output_config: { effort: EFFORT, format: { type: "json_schema", schema: SCHEMA } },
  };
}

// ── ánh xạ lesson_id → thư mục content/lesson-samples (từ hang-doi.md) ─────────
function thuMucCuaBai(): Map<number, string> {
  const m = new Map<number, string>();
  const p = path.join(root, "content/gemini/hang-doi.md");
  if (!fs.existsSync(p)) return m;
  for (const line of fs.readFileSync(p, "utf8").split("\n")) {
    const cells = line.split("|").map((s) => s.trim());
    if (cells.length < 4) continue;
    const id = Number(cells[2]);
    if (Number.isInteger(id) && id > 0 && fs.existsSync(path.join(root, "content/lesson-samples", cells[1]))) m.set(id, cells[1]);
  }
  return m;
}

// ── chế độ ────────────────────────────────────────────────────────────────────
const client = new Anthropic({ apiKey: envVar("ANTHROPIC_API_KEY") ?? fail("thiếu ANTHROPIC_API_KEY trong .env.local") });

async function duToan() {
  const bai = await layBai();
  if (!bai.length) fail("không có bài nào khớp bộ lọc");
  let tongIn = 0;
  const p = PRICE[MODEL];
  console.log(`Model ${MODEL} · effort ${EFFORT} · ${bai.length} bài\n`);
  for (const b of bai) {
    const c = await client.messages.countTokens({ model: MODEL, system: SYSTEM, messages: params(b).messages });
    tongIn += c.input_tokens;
    console.log(`  ${String(b.lessonId).padStart(4)} L${b.lop} ${b.ten.slice(0, 50).padEnd(50)} ${c.input_tokens.toLocaleString()} tok`);
  }
  const uocOut = bai.length * 4000; // ~4k token output/bài (JSON + thinking high) — ước
  if (p) {
    const usd = ((tongIn * p.input + uocOut * p.output) / 1e6) * 0.5;
    console.log(`\nTổng vào ${tongIn.toLocaleString()} tok · ra ước ${uocOut.toLocaleString()} tok → ≈ $${usd.toFixed(2)} (giá batch ½, chưa trừ cache system prompt)`);
  }
}

async function gui() {
  const bai = await layBai();
  if (!bai.length) fail("không có bài nào khớp bộ lọc");
  const requests = bai.map((b) => ({ custom_id: `lesson-${b.lessonId}`, params: params(b) }));
  const batch = await client.messages.batches.create({ requests });
  const manifest = {
    batch_id: batch.id,
    created_at: batch.created_at,
    model: MODEL,
    effort: EFFORT,
    vai: VAI,
    bai: bai.map((b) => ({ lesson_id: b.lessonId, item_id: b.itemId, ten: b.ten, lop: b.lop, chuong: b.chuong })),
  };
  const mp = path.join(LOG_DIR, `${batch.id}.manifest.json`);
  fs.writeFileSync(mp, JSON.stringify(manifest, null, 2));
  console.log(`✓ Đã gửi batch ${batch.id} — ${bai.length} bài, model ${MODEL}, effort ${EFFORT}`);
  console.log(`  manifest: ${path.relative(root, mp)}`);
  console.log(`  lấy kết quả: npx tsx scripts/batch-ra-soat-bai.mts --nhan ${batch.id} --cho`);
}

function manifestMoiNhat(): string | undefined {
  const files = fs.readdirSync(LOG_DIR).filter((f) => f.endsWith(".manifest.json"));
  if (!files.length) return undefined;
  files.sort((a, b) => fs.statSync(path.join(LOG_DIR, b)).mtimeMs - fs.statSync(path.join(LOG_DIR, a)).mtimeMs);
  return files[0].replace(".manifest.json", "");
}

interface KetQua { lesson_id: number; ten: string; lop: string; chuong: string; batch_id: string; model: string; usage: Anthropic.Usage; cost_usd: number | null; data: { gop_y: { muc: string; loai: string }[]; du_doan_loi_sai: { bai_da_nhan_manh: boolean }[] } }

async function nhan() {
  const id = arg("nhan") ?? manifestMoiNhat() ?? fail("chưa có batch nào — chạy --gui trước");
  const mp = path.join(LOG_DIR, `${id}.manifest.json`);
  const manifest = fs.existsSync(mp) ? (JSON.parse(fs.readFileSync(mp, "utf8")) as { model: string; bai: { lesson_id: number; ten: string; lop: string; chuong: string }[] }) : { model: MODEL, bai: [] };
  const meta = new Map(manifest.bai.map((b) => [b.lesson_id, b]));

  let batch = await client.messages.batches.retrieve(id);
  while (batch.processing_status !== "ended") {
    const c = batch.request_counts;
    console.log(`  ${batch.processing_status}: đang xử lý ${c.processing}, xong ${c.succeeded}, lỗi ${c.errored}`);
    if (!flag("cho")) {
      console.log(`Chưa xong. Chạy lại với --cho để đợi, hoặc thử lại sau.`);
      return;
    }
    await new Promise((r) => setTimeout(r, 60_000));
    batch = await client.messages.batches.retrieve(id);
  }

  let tongUsd = 0;
  let nSucc = 0;
  const loi: string[] = [];
  const thuMuc = thuMucCuaBai();
  for await (const r of await client.messages.batches.results(id)) {
    const lessonId = Number(r.custom_id.replace("lesson-", ""));
    const m = meta.get(lessonId) ?? { lesson_id: lessonId, ten: "?", lop: "?", chuong: "" };
    if (r.result.type !== "succeeded") {
      loi.push(`${r.custom_id}: ${r.result.type}${r.result.type === "errored" ? ` — ${JSON.stringify(r.result.error).slice(0, 200)}` : ""}`);
      continue;
    }
    const msg = r.result.message;
    if (msg.stop_reason === "refusal") {
      loi.push(`${r.custom_id}: refusal ${msg.stop_details?.category ?? ""}`);
      continue;
    }
    const text = msg.content.filter((b): b is Anthropic.TextBlock => b.type === "text").map((b) => b.text).join("");
    let data: KetQua["data"];
    try {
      data = JSON.parse(text);
    } catch {
      loi.push(`${r.custom_id}: JSON hỏng (stop_reason ${msg.stop_reason})`);
      fs.writeFileSync(path.join(KQ_DIR, `${lessonId}.raw.txt`), text);
      continue;
    }
    const usd = costUsd(manifest.model, msg.usage);
    tongUsd += usd ?? 0;
    nSucc++;
    const kq: KetQua = { lesson_id: lessonId, ten: m.ten, lop: m.lop, chuong: m.chuong, batch_id: id, model: manifest.model, usage: msg.usage, cost_usd: usd, data };
    fs.writeFileSync(path.join(KQ_DIR, `${lessonId}.json`), JSON.stringify(kq, null, 2));
    // Bài có thư mục nguồn → ghi đúng chỗ chế độ /gemini-nhan đọc (không ghi đè bản đã có).
    const dir = thuMuc.get(lessonId);
    if (dir) {
      const dest = path.join(root, "content/lesson-samples", dir, "gemini/nhan", `hoc-sinh-${VAI}-claude.json`);
      if (!fs.existsSync(dest)) {
        fs.mkdirSync(path.dirname(dest), { recursive: true });
        fs.writeFileSync(dest, JSON.stringify({ ...data, nguon: "claude" }, null, 2));
      }
    }
    const chan = data.gop_y.filter((g) => g.muc === "chặn").length;
    console.log(`  ✓ ${String(lessonId).padStart(4)} L${m.lop} ${m.ten.slice(0, 45).padEnd(45)} góp ý ${String(data.gop_y.length).padStart(2)} (chặn ${chan}) · $${(usd ?? 0).toFixed(3)}`);
  }
  console.log(`\n${nSucc} bài xong · ≈ $${tongUsd.toFixed(2)}${loi.length ? `\nLỗi (${loi.length}):\n  ${loi.join("\n  ")}` : ""}`);
  tongHop();
}

function tongHop() {
  const files = fs.readdirSync(KQ_DIR).filter((f) => /^\d+\.json$/.test(f));
  const all = files.map((f) => JSON.parse(fs.readFileSync(path.join(KQ_DIR, f), "utf8")) as KetQua);
  const score = (k: KetQua) => k.data.gop_y.filter((g) => g.muc === "chặn").length * 10 + k.data.gop_y.filter((g) => g.muc === "khó").length * 3 + k.data.gop_y.length;
  all.sort((a, b) => score(b) - score(a));
  const lines = [
    `# Báo cáo rà soát bài lý thuyết bằng Claude (Batch API)`,
    ``,
    `Cập nhật: ${new Date().toISOString().slice(0, 16).replace("T", " ")} · ${all.length} bài · tổng ≈ $${all.reduce((s, k) => s + (k.cost_usd ?? 0), 0).toFixed(2)}`,
    `Xếp theo mức cần sửa (chặn ×10, khó ×3, mỗi góp ý ×1). Kết quả từng bài: \`scripts/logs/batch-ra-soat/ket-qua/<lesson_id>.json\`.`,
    `Góp ý là GỢI Ý — kiểm từng mục trước khi sửa (skill cap-nhat-bai-hoc-theo-gemini, chế độ 2, bước 2).`,
    ``,
    `| lesson_id | Lớp | Bài | Góp ý | Chặn | Khó | Loại hay gặp | Quiz chưa nhấn bẫy |`,
    `|---|---|---|---|---|---|---|---|`,
  ];
  for (const k of all) {
    const g = k.data.gop_y;
    const loai = Object.entries(g.reduce<Record<string, number>>((m, x) => ((m[x.loai] = (m[x.loai] ?? 0) + 1), m), {}))
      .sort((a, b) => b[1] - a[1])
      .slice(0, 2)
      .map(([l, n]) => `${l} ${n}`)
      .join(", ");
    const quiz = k.data.du_doan_loi_sai.filter((d) => !d.bai_da_nhan_manh).length;
    lines.push(`| ${k.lesson_id} | ${k.lop} | ${k.ten} | ${g.length} | ${g.filter((x) => x.muc === "chặn").length} | ${g.filter((x) => x.muc === "khó").length} | ${loai} | ${quiz}/${k.data.du_doan_loi_sai.length} |`);
  }
  const bp = path.join(LOG_DIR, "BAO-CAO.md");
  fs.writeFileSync(bp, lines.join("\n") + "\n");
  console.log(`→ ${path.relative(root, bp)}`);
}

(async () => {
  if (flag("du-toan")) await duToan();
  else if (flag("gui")) await gui();
  else if (flag("nhan")) await nhan();
  else if (flag("tong-hop")) tongHop();
  else fail("chọn một: --du-toan | --gui | --nhan [batch_id] | --tong-hop");
})().catch((e) => {
  if (e instanceof Anthropic.AuthenticationError) fail("ANTHROPIC_API_KEY sai hoặc hết hạn");
  if (e instanceof Anthropic.APIError) fail(`Anthropic ${e.status}: ${e.message}`);
  fail(e instanceof Error ? e.message : String(e));
});
