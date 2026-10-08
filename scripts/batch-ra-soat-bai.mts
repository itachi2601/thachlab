// Rà soát HÀNG LOẠT bài lý thuyết bằng Claude qua Message Batches API (giá bằng nửa API thường, credit
// khuyến mãi Anthropic áp dụng được — Claude Code thì không). Mỗi bài là một request. Hai chế độ:
//   --che-do hoc-sinh   (mặc định) Claude đọc mục lý thuyết như "lượt Claude" (bước 1b skill
//                       cap-nhat-bai-hoc-theo-gemini, prompt .../references/PROMPT-CLAUDE-HOC-SINH.md) → JSON góp ý.
//   --che-do bai-tap-mau Claude đề xuất BẢN NHÁP đúng 4 dạng bài tập mẫu bắc cầu 4 cấp bám nội dung lý thuyết
//                       + danh mục YCCĐ (prompt .claude/skills/soan-bai-tap-mau/references/PROMPT-GEMINI-BAI-TAP-MAU.md),
//                       tự chạy kiem-ban-nhap-gemini.py để kiểm số học/phạm vi. Bản nháp KHÔNG đăng nguyên văn —
//                       Claude viết lại theo skill soan-bai-tap-mau (chế độ 2B của skill Gemini).
//
// CHỈ ĐỌC DB (lesson_items.kind='ly_thuyet'), KHÔNG ghi gì vào Supabase. Chỉ ghi file trong
// scripts/logs/batch-ra-soat/ và (nếu bài có thư mục trong content/lesson-samples theo content/gemini/hang-doi.md)
// gemini/nhan/hoc-sinh-trung-binh-claude.json hoặc gemini/nhan/bai-tap-mau.json để chế độ /gemini-nhan đọc tiếp
// (không ghi đè bản đã có).
//
//   npx tsx scripts/batch-ra-soat-bai.mts --du-toan [--lop 12] [--lesson-ids 10,11]   # đếm token, ước giá, KHÔNG gọi tính tiền
//   npx tsx scripts/batch-ra-soat-bai.mts --gui --lesson-ids 10                        # thử 1 bài → in batch id
//   npx tsx scripts/batch-ra-soat-bai.mts --gui --lop 12                               # cả lớp 12
//   npx tsx scripts/batch-ra-soat-bai.mts --gui                                        # mọi bài lý thuyết đã published
//   npx tsx scripts/batch-ra-soat-bai.mts --nhan [batch_id] [--cho]                    # lấy kết quả (mặc định batch mới nhất; --cho = đợi tới khi xong)
//   npx tsx scripts/batch-ra-soat-bai.mts --tong-hop                                   # gộp mọi kết quả đã nhận → BAO-CAO*.md
//   npx tsx scripts/batch-ra-soat-bai.mts --che-do bai-tap-mau --gui --lesson-ids 10   # nháp 4 dạng bài tập mẫu cho bài 10
//   npx tsx scripts/batch-ra-soat-bai.mts --che-do sua-ly-thuyet --gui --lesson-ids 10 # Claude tự chốt góp ý (gemini/nhan/hoc-sinh-*.json)
//        và trả cả theory.src.html đã sửa → --nhan ghi nguồn (sao lưu), build, lint, cập nhật so-quyet-dinh + hang-doi (8/10/2026)
//
// Tuỳ chọn: --model claude-opus-5-5 (mặc định) | claude-sonnet-5-5 · --effort high (mặc định) · --vai trung-binh
//           --limit N (số bài tối đa) · --chua-ra-soat (bỏ bài đã có kết quả)
//
// Cần .env.local: NEXT_PUBLIC_SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, ANTHROPIC_API_KEY
//   (+ ANTHROPIC_WORKSPACE_ID=wrkspc_... nếu key cấp tổ chức, API báo "not scoped to a workspace").
// Chạy trong tab terminal của thầy (Bash sandbox chặn *.supabase.co). Giá tra 8/10/2026, chỉ để ước tính.

import Anthropic from "@anthropic-ai/sdk";
import { createClient } from "@supabase/supabase-js";
import { spawnSync } from "node:child_process";
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
type CheDo = "hoc-sinh" | "bai-tap-mau" | "sua-ly-thuyet";
const CHE_DO = (arg("che-do") ?? "hoc-sinh") as CheDo;
if (!["hoc-sinh", "bai-tap-mau", "sua-ly-thuyet"].includes(CHE_DO)) fail("--che-do phải là hoc-sinh | bai-tap-mau | sua-ly-thuyet");
const prefixCua = (c: string) => (c === "bai-tap-mau" ? "btm-" : c === "sua-ly-thuyet" ? "sua-" : "lesson-");
const suffixCua = (c: string) => (c === "bai-tap-mau" ? ".bai-tap-mau.json" : c === "sua-ly-thuyet" ? ".sua.json" : ".json");
const PREFIX = prefixCua(CHE_DO);
const SUFFIX = suffixCua(CHE_DO);

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
const BTM_PROMPT_FILE = ".claude/skills/soan-bai-tap-mau/references/PROMPT-GEMINI-BAI-TAP-MAU.md";
function loadPromptBtm(): string {
  const raw = fs.readFileSync(path.join(root, BTM_PROMPT_FILE), "utf8");
  const marker = "## PROMPT (sao chép từ đây)";
  if (!raw.includes(marker)) fail(`không thấy "${marker}" trong ${BTM_PROMPT_FILE}`);
  return raw
    .split(marker)[1]
    .split("\n---\n")[0]
    .trim()
    .replace('cho bài "{TÊN BÀI}" (lớp {LỚP}), bám đúng ký hiệu và kiến thức trong bài lý thuyết đính kèm', "cho bài nêu trong tin nhắn (tên bài, lớp), bám đúng ký hiệu và kiến thức trong bài lý thuyết nằm trong thẻ <bai_hoc> của tin nhắn")
    .replace("{YCCĐ}", "  (danh mục nằm trong tin nhắn, mục \"Danh mục yêu cầu cần đạt\")")
    .replaceAll('"{TÊN BÀI}"', "\"{tên bài ghi trong tin nhắn}\"");
}
const SUA_PROMPT_FILE = ".claude/skills/cap-nhat-bai-hoc-theo-gemini/references/PROMPT-CLAUDE-SUA-LY-THUYET.md";
function loadPromptSua(): string {
  const raw = fs.readFileSync(path.join(root, SUA_PROMPT_FILE), "utf8");
  const marker = "## PROMPT (sao chép từ đây)";
  if (!raw.includes(marker)) fail(`không thấy "${marker}" trong ${SUA_PROMPT_FILE}`);
  return raw.split(marker)[1].split("\n## Lưu ý khi đọc kết quả")[0].trim();
}
const SYSTEM = CHE_DO === "bai-tap-mau" ? loadPromptBtm() : CHE_DO === "sua-ly-thuyet" ? loadPromptSua() : loadPrompt();

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

const S = { type: "string" };
const ARR_S = { type: "array", items: S };
const obj = (props: Record<string, unknown>) => ({ type: "object", additionalProperties: false, required: Object.keys(props), properties: props });
const SCHEMA_BTM = obj({
  lesson_title: S,
  dang_bai: {
    type: "array",
    items: obj({
      label: S,
      cap_do: { type: "integer" },
      ten_cap_do: S,
      nhan_thuc: { type: "string", enum: ["nhận biết", "thông hiểu", "vận dụng", "vận dụng cao"] },
      cau_noi: S,
      yccd_de_xuat: S,
      de_bai: S,
      dieu_kien_ap_dung: S,
      phan_tich: { type: "array", items: obj({ trich_de: S, du_lieu: S, kien_thuc: S }) },
      can_tim: obj({ ky_hieu: S, cong_thuc: S }),
      kien_thuc_goi_lai: ARR_S,
      cac_buoc: { type: "array", items: obj({ tieu_de: S, cong_thuc_chu: S, the_so: S, ket_qua: S, kiem_tra: S }) },
      dap_so: { type: "array", items: obj({ y: S, gia_tri: { type: "number" }, don_vi: S }) },
      kiem_tinh: { type: "array", items: obj({ mo_ta: S, bieu_thuc: S, ky_vong: { type: "number" }, sai_so_tuong_doi: { type: "number" } }) },
      nhan_dang: S,
      bay_thuong_gap: ARR_S,
      dieu_ban_khong_chac: ARR_S,
      mo_phong_goi_y: S,
    }),
  },
});

const SCHEMA_SUA = obj({
  html: S,
  quyet_dinh: { type: "array", items: obj({ id: S, quyet_dinh: { type: "string", enum: ["chap_nhan", "tu_choi", "da_sua_truoc"] }, ghi_chu: S }) },
  doi_noi_dung: ARR_S,
  so_tu_them: { type: "integer" },
});
const SCHEMA_CUA = (c: string) => (c === "bai-tap-mau" ? SCHEMA_BTM : c === "sua-ly-thuyet" ? SCHEMA_SUA : SCHEMA);

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

interface Bai {
  lessonId: number; itemId: number; ten: string; lop: string; chuong: string; html: string; nguon: "repo" | "db";
  // chỉ sua-ly-thuyet: thư mục bài, theory.src.html nguyên văn, JSON góp ý các lượt, sổ quyết định vòng trước
  dir?: string; src?: string; gopY?: string; quyetDinhCu?: string;
}

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

  const thuMucNguon = thuMucCuaBai();
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
    // Bài có thư mục nguồn trong repo (content/gemini/hang-doi.md) → đọc theory.html ở repo, vì repo có thể
    // đã sửa mà chưa đăng; DB chỉ là nguồn khi không có thư mục. Góp ý phải khớp bản sắp đăng (8/10/2026).
    const dirRepo = thuMucNguon.get(l.id);
    const repoHtml = dirRepo ? path.join(root, "content/lesson-samples", dirRepo, "theory.html") : undefined;
    const nguon = repoHtml && fs.existsSync(repoHtml) ? "repo" : "db";
    const html = stripHeavy(nguon === "repo" ? fs.readFileSync(repoHtml!, "utf8") : (it.body_html ?? ""));
    if (html.replace(/<[^>]+>/g, "").trim().length < 400) continue; // mục trống/quá ngắn, chưa có bài
    if (flag("chua-ra-soat") && fs.existsSync(path.join(KQ_DIR, `${l.id}${SUFFIX}`))) continue;
    const b: Bai = { lessonId: l.id, itemId: it.id, ten: l.title, lop, chuong: chapterTitle.get(l.chapter_id) ?? "", html, nguon };
    if (CHE_DO === "sua-ly-thuyet") {
      // Cần đủ bộ: thư mục nguồn + theory.src.html + ít nhất một JSON góp ý trong gemini/nhan/.
      if (!dirRepo) { console.warn(`  bỏ ${l.id} ${l.title}: không có thư mục trong hang-doi.md`); continue; }
      const dirAbs = path.join(root, "content/lesson-samples", dirRepo);
      const srcP = path.join(dirAbs, "theory.src.html");
      const nhanDir = path.join(dirAbs, "gemini/nhan");
      const gopFiles = fs.existsSync(nhanDir) ? fs.readdirSync(nhanDir).filter((f) => /^hoc-sinh-.*\.json$/.test(f)).sort() : [];
      if (!fs.existsSync(srcP) || !gopFiles.length) { console.warn(`  bỏ ${l.id} ${l.title}: thiếu theory.src.html hoặc gemini/nhan/hoc-sinh-*.json`); continue; }
      const qdP = path.join(dirAbs, "gemini/da-xu-ly/so-quyet-dinh.json");
      b.dir = dirRepo;
      b.src = fs.readFileSync(srcP, "utf8");
      b.gopY = gopFiles.map((f) => `// ${f}\n${fs.readFileSync(path.join(nhanDir, f), "utf8")}`).join("\n\n");
      b.quyetDinhCu = fs.existsSync(qdP) ? fs.readFileSync(qdP, "utf8").slice(0, 8000) : "";
    }
    out.push(b);
  }
  out.sort((a, b) => a.lessonId - b.lessonId);
  const limit = Number(arg("limit") ?? 0);
  return limit ? out.slice(0, limit) : out;
}

function userMessageSua(b: Bai): string {
  return [
    `Lớp: ${b.lop}`,
    `Chương: ${b.chuong}`,
    `Bài: ${b.ten}`,
    ``,
    `<bai_hoc>`, b.src ?? "", `</bai_hoc>`,
    ``,
    `<gop_y>`, b.gopY ?? "", `</gop_y>`,
    ``,
    `<quyet_dinh_cu>`, b.quyetDinhCu || "(chưa có vòng trước)", `</quyet_dinh_cu>`,
  ].join("\n");
}

function userMessage(b: Bai): string {
  if (CHE_DO === "sua-ly-thuyet") return userMessageSua(b);
  return [
    `Lớp: ${b.lop}`,
    `Chương: ${b.chuong}`,
    `Tên bài: ${b.ten}`,
    ...(CHE_DO === "hoc-sinh" ? [`Hồ sơ học sinh: ${VAI}`] : []),
    `Danh mục yêu cầu cần đạt của bài (phạm vi kiến thức):\n${danhMucYccd(b.lessonId)}`,
    ``,
    `<bai_hoc>\n${b.html}\n</bai_hoc>`,
  ].join("\n");
}

function params(b: Bai): Anthropic.MessageCreateParamsNonStreaming {
  return {
    model: MODEL,
    // Suy nghĩ (effort high) tính chung vào trần này; 16000 từng cắt JSON bài 10 ở góp ý 19 (8/10/2026).
    max_tokens: CHE_DO === "bai-tap-mau" ? 48000 : CHE_DO === "sua-ly-thuyet" ? 64000 : 32000, // sua: trả cả file HTML (~15k) + suy nghĩ
    system: [{ type: "text", text: SYSTEM, cache_control: { type: "ephemeral" } }],
    messages: [{ role: "user", content: userMessage(b) }],
    output_config: { effort: EFFORT, format: { type: "json_schema", schema: SCHEMA_CUA(CHE_DO) } },
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
const WORKSPACE_ID = envVar("ANTHROPIC_WORKSPACE_ID");
const client = new Anthropic({
  apiKey: envVar("ANTHROPIC_API_KEY") ?? fail("thiếu ANTHROPIC_API_KEY trong .env.local"),
  // Key cấp tổ chức (không gắn workspace) bắt buộc kèm header này; key gắn workspace thì bỏ trống.
  ...(WORKSPACE_ID ? { defaultHeaders: { "anthropic-workspace-id": WORKSPACE_ID } } : {}),
});

async function duToan() {
  const bai = await layBai();
  if (!bai.length) fail("không có bài nào khớp bộ lọc");
  let tongIn = 0;
  const p = PRICE[MODEL];
  console.log(`Chế độ ${CHE_DO} · model ${MODEL} · effort ${EFFORT} · ${bai.length} bài\n`);
  for (const b of bai) {
    const c = await client.messages.countTokens({ model: MODEL, system: SYSTEM, messages: params(b).messages });
    tongIn += c.input_tokens;
    console.log(`  ${String(b.lessonId).padStart(4)} L${b.lop} ${b.ten.slice(0, 50).padEnd(50)} ${c.input_tokens.toLocaleString()} tok · ${b.nguon}`);
  }
  const uocOut = bai.length * (CHE_DO === "bai-tap-mau" ? 24000 : CHE_DO === "sua-ly-thuyet" ? 26000 : 14000); // token ra/bài (JSON + thinking high) — đo thật bài 10: 14,5k (8/10/2026)
  if (p) {
    const usd = ((tongIn * p.input + uocOut * p.output) / 1e6) * 0.5;
    console.log(`\nTổng vào ${tongIn.toLocaleString()} tok · ra ước ${uocOut.toLocaleString()} tok → ≈ $${usd.toFixed(2)} (giá batch ½, chưa trừ cache system prompt)`);
  }
}

async function gui() {
  const bai = await layBai();
  if (!bai.length) fail("không có bài nào khớp bộ lọc");
  const requests = bai.map((b) => ({ custom_id: `${PREFIX}${b.lessonId}`, params: params(b) }));
  const batch = await client.messages.batches.create({ requests });
  const manifest = {
    batch_id: batch.id,
    created_at: batch.created_at,
    che_do: CHE_DO,
    model: MODEL,
    effort: EFFORT,
    vai: VAI,
    bai: bai.map((b) => ({ lesson_id: b.lessonId, item_id: b.itemId, ten: b.ten, lop: b.lop, chuong: b.chuong })),
  };
  const mp = path.join(LOG_DIR, `${batch.id}.manifest.json`);
  fs.writeFileSync(mp, JSON.stringify(manifest, null, 2));
  console.log(`✓ Đã gửi batch ${batch.id} — chế độ ${CHE_DO}, ${bai.length} bài, model ${MODEL}, effort ${EFFORT}`);
  console.log(`  manifest: ${path.relative(root, mp)}`);
  console.log(`  lấy kết quả: npx tsx scripts/batch-ra-soat-bai.mts --nhan ${batch.id} --cho`);
  console.log(`  thử 1 bài trước: ${bai.length === 1 ? "đang làm" : "nên --gui --lesson-ids <id> trước khi chạy cả kho"}`);
}

function manifestMoiNhat(): string | undefined {
  const files = fs.readdirSync(LOG_DIR).filter((f) => f.endsWith(".manifest.json"));
  if (!files.length) return undefined;
  files.sort((a, b) => fs.statSync(path.join(LOG_DIR, b)).mtimeMs - fs.statSync(path.join(LOG_DIR, a)).mtimeMs);
  return files[0].replace(".manifest.json", "");
}

interface KetQuaHS { gop_y: { muc: string; loai: string }[]; du_doan_loi_sai: { bai_da_nhan_manh: boolean }[] }
interface KetQuaBTM { lesson_title: string; dang_bai: { label: string; cap_do: number; yccd_de_xuat: string; dieu_ban_khong_chac: string[] }[] }
interface KetQuaSua { html: string; quyet_dinh: { id: string; quyet_dinh: string; ghi_chu: string }[]; doi_noi_dung: string[]; so_tu_them: number }
interface KetQua<T = KetQuaHS | KetQuaBTM | KetQuaSua> {
  lesson_id: number; ten: string; lop: string; chuong: string; batch_id: string; che_do: string; model: string;
  usage: Anthropic.Usage; cost_usd: number | null; data: T;
  kiem?: { ok: boolean; loi: number; canh_bao: number; log: string }; // chỉ bai-tap-mau: kết quả kiem-ban-nhap-gemini.py
  sua?: KetQuaXuLySua; // chỉ sua-ly-thuyet
}

interface KetQuaXuLySua { ok: boolean; trang_thai: "da-sua" | "loi-lint" | "loi-cau-truc" | "khong-thu-muc"; loi: string[]; ghi_vao?: string; sao_luu?: string; lint: Record<string, string> }

// Ghi HTML đã sửa vào theory.src.html (sao lưu bản cũ), build hình + bundle, chạy lint; không ghi DB.
function xuLySua(lessonId: number, dir: string | undefined, data: KetQuaSua, ten: string): KetQuaXuLySua {
  const r: KetQuaXuLySua = { ok: false, trang_thai: "khong-thu-muc", loi: [], lint: {} };
  if (!dir) { r.loi.push("không có thư mục bài"); return r; }
  const dirAbs = path.join(root, "content/lesson-samples", dir);
  const srcP = path.join(dirAbs, "theory.src.html");
  const cu = fs.readFileSync(srcP, "utf8");
  const moi = data.html;
  // Kiểm cấu trúc: số mốc hình, số mục, số quiz phải y nguyên.
  const dem = (h: string, re: RegExp) => (h.match(re) ?? []).length;
  const kiem: [string, RegExp][] = [["mốc <!--FIGn-->", /<!--FIG\d+-->/g], ["<h3>", /<h3[\s>]/g], ["tl-quiz", /class="[^"]*\btl-quiz\b/g], ["tl-ok", /\btl-ok\b/g]];
  for (const [t, re] of kiem) if (dem(cu, re) !== dem(moi, re)) r.loi.push(`${t}: cũ ${dem(cu, re)} ≠ mới ${dem(moi, re)}`);
  if (moi.length < cu.length * 0.7) r.loi.push(`HTML mới ngắn bất thường (${moi.length} so với ${cu.length} ký tự)`);
  if (r.loi.length) { r.trang_thai = "loi-cau-truc"; fs.writeFileSync(path.join(KQ_DIR, `${lessonId}.sua.html`), moi); return r; }
  // Sao lưu rồi ghi.
  const daXuLy = path.join(dirAbs, "gemini/da-xu-ly");
  fs.mkdirSync(daXuLy, { recursive: true });
  const moc = new Date().toISOString().slice(0, 16).replace(/[-:T]/g, "");
  const saoLuu = path.join(daXuLy, `theory.src.${moc}.html`);
  fs.copyFileSync(srcP, saoLuu);
  fs.writeFileSync(srcP, moi);
  r.sao_luu = path.relative(root, saoLuu);
  r.ghi_vao = path.relative(root, srcP);
  // Build + lint.
  const chay = (cmd: string, args: string[], cwd = root) => { const x = spawnSync(cmd, args, { cwd, encoding: "utf8" }); return { ok: x.status === 0, log: ((x.stdout ?? "") + (x.stderr ?? "")).trim() }; };
  const SK = ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts";
  const theoryP = path.join(dirAbs, "theory.html");
  const buoc: [string, () => { ok: boolean; log: string }][] = [
    ["build_figs", () => (fs.existsSync(path.join(dirAbs, "build_figs.py")) ? chay("python3", ["build_figs.py"], dirAbs) : { ok: true, log: "(không có build_figs.py)" })],
    ["build_bundle", () => (fs.existsSync(path.join(dirAbs, "build_bundle.py")) ? chay("python3", ["build_bundle.py"], dirAbs) : { ok: true, log: "(không có build_bundle.py)" })],
    ["lint_theory", () => chay("python3", [`${SK}/lint_theory.py`, theoryP])],
    ["lint_do_dai", () => chay("python3", [`${SK}/lint_do_dai.py`, theoryP])],
    ["check_quizzes", () => chay("python3", [`${SK}/check_quizzes.py`, theoryP])],
  ];
  let lintOk = true;
  for (const [t, f] of buoc) {
    const x = f();
    r.lint[t] = x.log.slice(-1500);
    if (!x.ok) { lintOk = false; r.loi.push(`${t} lỗi`); }
  }
  r.ok = lintOk;
  r.trang_thai = lintOk ? "da-sua" : "loi-lint";
  // Sổ quyết định: nối thêm một vòng, không viết lại vòng cũ.
  const qdP = path.join(daXuLy, "so-quyet-dinh.json");
  let qd: Record<string, unknown> = {};
  try { qd = fs.existsSync(qdP) ? JSON.parse(fs.readFileSync(qdP, "utf8")) : {}; } catch { qd = { ghi_chu_json_cu_hong: true }; }
  const vongCu = Number(qd.vong ?? 0);
  qd.bai ??= dir;
  qd.vong = vongCu + 1;
  const vongKey = `vong${qd.vong}_sua_api`;
  qd[vongKey] = { ngay: new Date().toISOString().slice(0, 10), model: MODEL, quyet_dinh: data.quyet_dinh, doi_noi_dung: data.doi_noi_dung, so_tu_them: data.so_tu_them, trang_thai: r.trang_thai, loi: r.loi, sao_luu: r.sao_luu };
  fs.writeFileSync(qdP, JSON.stringify(qd, null, 2));
  // hang-doi.md: cập nhật cột trạng thái + ghi chú của đúng dòng.
  const hdP = path.join(root, "content/gemini/hang-doi.md");
  if (fs.existsSync(hdP)) {
    const lines = fs.readFileSync(hdP, "utf8").split("\n").map((l) => {
      const c = l.split("|").map((x) => x.trim());
      if (c.length < 5 || c[1] !== dir) return l;
      const nhan = data.quyet_dinh.filter((x) => x.quyet_dinh === "chap_nhan").length;
      return `| ${c[1]} | ${c[2]} | ${r.trang_thai} | ${ten}: API sửa ${nhan}/${data.quyet_dinh.length} góp ý ${qd.vong ? `(vòng ${qd.vong})` : ""}${lintOk ? ", lint sạch, chờ đăng" : ", LỖI lint — sửa tay"} |`;
    });
    fs.writeFileSync(hdP, lines.join("\n"));
  }
  return r;
}

// Chạy kiểm máy của skill soan-bai-tap-mau lên bản nháp vừa nhận (số học, trích đề, YCCĐ, từ cấm).
function kiemBanNhap(file: string, lessonId: number): KetQua["kiem"] {
  const script = path.join(root, ".claude/skills/soan-bai-tap-mau/scripts/kiem-ban-nhap-gemini.py");
  if (!fs.existsSync(script)) return undefined;
  const r = spawnSync("python3", [script, file, "--lesson-id", String(lessonId)], { cwd: root, encoding: "utf8" });
  const log = (r.stdout ?? "") + (r.stderr ?? "");
  const tong = log.match(/Tổng:\s*(\d+)\s*lỗi,\s*(\d+)\s*cảnh báo/);
  return {
    ok: r.status === 0,
    loi: tong ? Number(tong[1]) : (log.match(/✗/g) ?? []).length,
    canh_bao: tong ? Number(tong[2]) : (log.match(/^\s*!/gm) ?? []).length,
    log,
  };
}

async function nhan() {
  const id = arg("nhan") ?? manifestMoiNhat() ?? fail("chưa có batch nào — chạy --gui trước");
  const mp = path.join(LOG_DIR, `${id}.manifest.json`);
  const manifest = fs.existsSync(mp)
    ? (JSON.parse(fs.readFileSync(mp, "utf8")) as { model: string; che_do?: string; vai?: string; bai: { lesson_id: number; ten: string; lop: string; chuong: string }[] })
    : { model: MODEL, che_do: CHE_DO, vai: VAI, bai: [] };
  const cheDo = manifest.che_do ?? "hoc-sinh";
  const prefix = prefixCua(cheDo);
  const suffix = suffixCua(cheDo);
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
    const lessonId = Number(r.custom_id.replace(prefix, ""));
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
      fs.writeFileSync(path.join(KQ_DIR, `${lessonId}${suffix}.raw.txt`), text);
      continue;
    }
    const usd = costUsd(manifest.model, msg.usage);
    tongUsd += usd ?? 0;
    nSucc++;
    const kq: KetQua = { lesson_id: lessonId, ten: m.ten, lop: m.lop, chuong: m.chuong, batch_id: id, che_do: cheDo, model: manifest.model, usage: msg.usage, cost_usd: usd, data };
    const kqPath = path.join(KQ_DIR, `${lessonId}${suffix}`);
    // Bài có thư mục nguồn → ghi đúng chỗ chế độ /gemini-nhan đọc (không ghi đè bản đã có).
    const dir = thuMuc.get(lessonId);
    const destName = cheDo === "bai-tap-mau" ? "bai-tap-mau.json" : `hoc-sinh-${manifest.vai ?? VAI}-claude.json`;
    const dest = dir && cheDo !== "sua-ly-thuyet" ? path.join(root, "content/lesson-samples", dir, "gemini/nhan", destName) : undefined;
    let daGhiNhan = false;
    if (dest) {
      fs.mkdirSync(path.dirname(dest), { recursive: true });
      if (fs.existsSync(dest)) { // bản cũ dời sang da-xu-ly/ kèm mốc giờ, không mất
        const cu = path.join(root, "content/lesson-samples", dir!, "da-xu-ly", `${path.basename(dest, ".json")}.${new Date().toISOString().slice(0, 16).replace(/[-:T]/g, "")}.json`);
        fs.mkdirSync(path.dirname(cu), { recursive: true });
        fs.renameSync(dest, cu);
      }
      fs.writeFileSync(dest, JSON.stringify(cheDo === "bai-tap-mau" ? data : { ...data, nguon: "claude" }, null, 2));
      daGhiNhan = true;
    }
    if (cheDo === "sua-ly-thuyet") {
      const r = xuLySua(lessonId, dir, data as KetQuaSua, m.ten);
      kq.sua = r;
      fs.writeFileSync(kqPath, JSON.stringify({ ...kq, data: { ...(data as KetQuaSua), html: `(đã ghi vào ${r.ghi_vao ?? "—"})` } }, null, 2));
      const qd = (data as KetQuaSua).quyet_dinh;
      console.log(`  ${r.ok ? "✓" : "✗"} ${String(lessonId).padStart(4)} L${m.lop} ${m.ten.slice(0, 45).padEnd(45)} nhận ${qd.filter((x) => x.quyet_dinh === "chap_nhan").length}/${qd.length} · ${r.trang_thai} · $${(usd ?? 0).toFixed(3)}`);
      if (!r.ok) console.log(`      ${r.loi.join(" | ").slice(0, 300)}`);
    } else if (cheDo === "bai-tap-mau") {
      // Bản nháp thuần (đúng định dạng kiem-ban-nhap-gemini.py đọc) để riêng, kiểm máy ngay.
      const nhapPath = path.join(KQ_DIR, `${lessonId}.bai-tap-mau.nhap.json`);
      fs.writeFileSync(nhapPath, JSON.stringify(data, null, 2));
      kq.kiem = kiemBanNhap(nhapPath, lessonId);
      fs.writeFileSync(kqPath, JSON.stringify(kq, null, 2));
      const d = (data as KetQuaBTM).dang_bai;
      const k = kq.kiem;
      console.log(`  ${k?.ok ? "✓" : "✗"} ${String(lessonId).padStart(4)} L${m.lop} ${m.ten.slice(0, 45).padEnd(45)} ${d.length} dạng · kiểm ${k ? `${k.loi} lỗi, ${k.canh_bao} cảnh báo` : "bỏ qua"} · $${(usd ?? 0).toFixed(3)}${daGhiNhan ? " → gemini/nhan" : ""}`);
    } else {
      fs.writeFileSync(kqPath, JSON.stringify(kq, null, 2));
      const hs = data as KetQuaHS;
      const chan = hs.gop_y.filter((g) => g.muc === "chặn").length;
      console.log(`  ✓ ${String(lessonId).padStart(4)} L${m.lop} ${m.ten.slice(0, 45).padEnd(45)} góp ý ${String(hs.gop_y.length).padStart(2)} (chặn ${chan}) · $${(usd ?? 0).toFixed(3)}${daGhiNhan ? " → gemini/nhan" : ""}`);
    }
  }
  console.log(`\n${nSucc} bài xong · ≈ $${tongUsd.toFixed(2)}${loi.length ? `\nLỗi (${loi.length}):\n  ${loi.join("\n  ")}` : ""}`);
  tongHop();
}

const now = () => new Date().toISOString().slice(0, 16).replace("T", " ");
function docKetQua<T>(re: RegExp): KetQua<T>[] {
  return fs.readdirSync(KQ_DIR).filter((f) => re.test(f)).map((f) => JSON.parse(fs.readFileSync(path.join(KQ_DIR, f), "utf8")) as KetQua<T>);
}

function tongHop() {
  tongHopHocSinh();
  tongHopBaiTapMau();
  tongHopSua();
}

function tongHopSua() {
  const all = docKetQua<KetQuaSua>(/^\d+\.sua\.json$/);
  if (!all.length) return;
  all.sort((a, b) => Number(a.sua?.ok ?? false) - Number(b.sua?.ok ?? false) || a.lesson_id - b.lesson_id); // lỗi lên đầu
  const lines = [
    `# Báo cáo sửa lý thuyết bằng Claude (Batch API, chế độ sua-ly-thuyet)`,
    ``,
    `Cập nhật: ${now()} · ${all.length} bài · tổng ≈ $${all.reduce((s, k) => s + (k.cost_usd ?? 0), 0).toFixed(2)}`,
    `Bài \`da-sua\`: theory.src.html đã ghi (bản cũ ở gemini/da-xu-ly/theory.src.<mốc>.html), theory.html + bundle.json đã build, lint sạch → đăng bằng \`bash scripts/cap-nhat-ly-thuyet.sh content/lesson-samples/<bài>/theory.html <id> --yes\`.`,
    `Bài \`loi-lint\`: đã ghi nguồn nhưng lint báo lỗi → Claude Code sửa tay phần lỗi (xem \`ket-qua/<id>.sua.json\` → sua.lint). Bài \`loi-cau-truc\`: KHÔNG ghi, HTML trả về ở \`ket-qua/<id>.sua.html\`.`,
    ``,
    `| lesson_id | Lớp | Bài | Trạng thái | Nhận/tổng | Đổi nội dung | Lỗi |`,
    `|---|---|---|---|---|---|---|`,
  ];
  for (const k of all) {
    const qd = k.data.quyet_dinh ?? [];
    lines.push(`| ${k.lesson_id} | ${k.lop} | ${k.ten} | ${k.sua?.trang_thai ?? "—"} | ${qd.filter((x) => x.quyet_dinh === "chap_nhan").length}/${qd.length} | ${(k.data.doi_noi_dung ?? []).length} | ${(k.sua?.loi ?? []).join("; ").slice(0, 120)} |`);
  }
  const bp = path.join(LOG_DIR, "BAO-CAO-SUA.md");
  fs.writeFileSync(bp, lines.join("\n") + "\n");
  console.log(`→ ${path.relative(root, bp)}`);
}

function tongHopHocSinh() {
  const all = docKetQua<KetQuaHS>(/^\d+\.json$/);
  if (!all.length) return;
  const score = (k: KetQua<KetQuaHS>) => k.data.gop_y.filter((g) => g.muc === "chặn").length * 10 + k.data.gop_y.filter((g) => g.muc === "khó").length * 3 + k.data.gop_y.length;
  all.sort((a, b) => score(b) - score(a));
  const lines = [
    `# Báo cáo rà soát bài lý thuyết bằng Claude (Batch API)`,
    ``,
    `Cập nhật: ${now()} · ${all.length} bài · tổng ≈ $${all.reduce((s, k) => s + (k.cost_usd ?? 0), 0).toFixed(2)}`,
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

function tongHopBaiTapMau() {
  const all = docKetQua<KetQuaBTM>(/^\d+\.bai-tap-mau\.json$/);
  if (!all.length) return;
  // Bản sạch (kiểm máy không lỗi) lên đầu — đó là bài đáng viết lại trước.
  all.sort((a, b) => Number(b.kiem?.ok ?? false) - Number(a.kiem?.ok ?? false) || (a.kiem?.loi ?? 99) - (b.kiem?.loi ?? 99) || a.lesson_id - b.lesson_id);
  const lines = [
    `# Báo cáo bản nháp bài tập mẫu do Claude đề xuất (Batch API)`,
    ``,
    `Cập nhật: ${now()} · ${all.length} bài · tổng ≈ $${all.reduce((s, k) => s + (k.cost_usd ?? 0), 0).toFixed(2)}`,
    `Bản nháp: \`scripts/logs/batch-ra-soat/ket-qua/<lesson_id>.bai-tap-mau.nhap.json\` (đúng định dạng \`kiem-ban-nhap-gemini.py\`), log kiểm trong \`<lesson_id>.bai-tap-mau.json\` → \`kiem.log\`.`,
    `KHÔNG đăng nguyên văn: viết lại theo skill soan-bai-tap-mau (chế độ 2B của cap-nhat-bai-hoc-theo-gemini) — kiểm số liệu, phong cách AI-TUTOR 9, mô phỏng, kiểm chéo kiem-code, thầy duyệt.`,
    `Bài có thư mục nguồn đã được chép sẵn vào \`gemini/nhan/bai-tap-mau.json\` (nếu chưa có).`,
    ``,
    `| lesson_id | Lớp | Bài | Dạng | Kiểm máy | Lỗi | Cảnh báo | Không chắc | Dạng đề xuất |`,
    `|---|---|---|---|---|---|---|---|---|`,
  ];
  for (const k of all) {
    const d = k.data.dang_bai;
    const khongChac = d.reduce((s, x) => s + (x.dieu_ban_khong_chac?.length ?? 0), 0);
    const ten = d.map((x) => x.label.replace(/^Dạng \d+\s*[·:-]?\s*/, "")).join(" · ");
    lines.push(`| ${k.lesson_id} | ${k.lop} | ${k.ten} | ${d.length} | ${k.kiem ? (k.kiem.ok ? "✓" : "✗") : "—"} | ${k.kiem?.loi ?? "—"} | ${k.kiem?.canh_bao ?? "—"} | ${khongChac} | ${ten} |`);
  }
  const bp = path.join(LOG_DIR, "BAO-CAO-BAI-TAP-MAU.md");
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
