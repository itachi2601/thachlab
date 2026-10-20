// Cập nhật nội dung 10 chương AVCN từ bundle local — CHỈ hai mục:
//   - ly_thuyet.body_html  (mở bài + bảng Part + tiêu đề ⭐⭐)
//   - bai_tap_mau.questions (đề mẫu 5 Part: bỏ chú thích điểm ở tiêu đề Part + câu trấn an)
// KHÔNG đụng exam/luyen_tap/exam_ids/tiêu đề/thứ tự, không tạo đề mới (giữ kết quả HS đã làm).
//
//   npx tsx scripts/cap-nhat-avcn-noi-dung.mts [--dry-run | --apply]
//
// Mặc định là dry-run: chỉ đọc DB, in thay đổi, không ghi. `--apply` mới ghi.
// Tự sao lưu các dòng sắp ghi ra scripts/logs/ trước khi UPDATE; sau khi ghi, đọc lại và
// đối chiếu: nội dung mới phải khớp bundle, mọi cột/mục khác phải y nguyên.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const fail = (m: string): never => {
  console.error("Lỗi:", m);
  process.exit(1);
};
function env(key: string): string | undefined {
  if (process.env[key]) return process.env[key];
  const p = path.join(root, ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const l = fs.readFileSync(p, "utf8").split("\n").find((x) => x.startsWith(`${key}=`));
  return l ? l.slice(key.length + 1).trim() : undefined;
}

const APPLY = process.argv.includes("--apply");
const DRY = process.argv.includes("--dry-run") || !APPLY;
if (APPLY && process.argv.includes("--dry-run")) fail("chọn một trong --dry-run / --apply");

/** So sánh JSON không phụ thuộc thứ tự khoá (jsonb của Postgres trả khoá đã sắp xếp). */
function canonical(v: unknown): string {
  if (Array.isArray(v)) return `[${v.map(canonical).join(",")}]`;
  if (v && typeof v === "object")
    return `{${Object.keys(v as Record<string, unknown>)
      .sort()
      .map((k) => `${JSON.stringify(k)}:${canonical((v as Record<string, unknown>)[k])}`)
      .join(",")}}`;
  return JSON.stringify(v);
}

/** Các cụm chỉ nói về điểm thi — không được còn trong nội dung HS thấy. */
const CAM = [
  "bao nhiêu điểm trong đề",
  "trên 7 điểm",
  "điểm thành phần",
  "một phần điểm",
  "nửa điểm",
  "· 2,5 đ",
  "· 2 đ",
  "· 1 đ",
];
/** Số + "điểm" (2,5 điểm / 2 điểm / 1 điểm) — không bắt "điểm tập trung", "ưu điểm". */
const SO_DIEM = /\d(?:,\d)?\s*điểm/;

function viPham(text: string): string[] {
  const bad = CAM.filter((x) => text.includes(x));
  if (SO_DIEM.test(text)) bad.push(`số điểm (${text.match(SO_DIEM)?.[0]})`);
  return bad;
}

type Bundle = {
  theory_html: string;
  worked_examples: { label: string; body_html: string }[];
};

type Item = {
  id: number;
  lesson_id: number;
  kind: string;
  title: string;
  subtitle: string;
  body_html: string;
  questions: unknown[];
  exam_ids: number[];
  sort_order: number;
  [k: string]: unknown;
};

const url = env("NEXT_PUBLIC_SUPABASE_URL");
const key = env("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) fail("thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY trong .env.local");
const sb = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });

// 1. Thư mục bài → số chương
const dirs = fs
  .readdirSync(path.join(root, "content", "lesson-samples"))
  .filter((n) => /^avcn-chapter-\d+-/.test(n))
  .map((n) => ({ dir: path.join(root, "content", "lesson-samples", n), n }))
  .map(({ dir }) => {
    const d = JSON.parse(fs.readFileSync(path.join(dir, "data", "bai.json"), "utf8"));
    return { dir, chapter: Number(d.meta.chapter), title: d.meta.title_en };
  })
  .sort((a, b) => a.chapter - b.chapter);
if (dirs.length !== 10 || dirs.some((d, i) => d.chapter !== i + 1)) fail(`không đủ 10 chương AVCN (thấy ${dirs.length})`);

// 2. Chương + bài trên DB (chỉ đọc)
const { data: chapters, error: cErr } = await sb
  .from("chapters")
  .select("id, title, subject_code")
  .eq("subject_code", "avcn");
if (cErr) fail(`đọc chapters: ${cErr.message}`);
const chapterIds = (chapters ?? []).map((c) => c.id as number);
const { data: lessons, error: lErr } = await sb
  .from("lessons")
  .select("id, chapter_id, sort_order, title, published")
  .in("chapter_id", chapterIds)
  .order("sort_order");
if (lErr) fail(`đọc lessons: ${lErr.message}`);
const lessonTheoChuong = new Map<number, { id: number; title: string; published: boolean }>();
for (const l of lessons ?? []) lessonTheoChuong.set(Number(l.sort_order), { id: l.id as number, title: l.title as string, published: !!l.published });
if (lessonTheoChuong.size !== 10) fail(`DB không đủ 10 bài AVCN (thấy ${lessonTheoChuong.size})`);

// 3. Bundle local + đọc mục đang có
const bundles = dirs.map((d) => ({
  ...d,
  bundle: JSON.parse(fs.readFileSync(path.join(d.dir, "bundle.json"), "utf8")) as Bundle,
}));

const ids = dirs.map((d) => lessonTheoChuong.get(d.chapter)!.id);
const { data: items, error: iErr } = await sb
  .from("lesson_items")
  .select("*")
  .in("lesson_id", ids)
  .in("kind", ["ly_thuyet", "bai_tap_mau"])
  .order("lesson_id")
  .order("sort_order");
if (iErr) fail(`đọc lesson_items: ${iErr.message}`);
const itemTheo = new Map<string, Item>();
for (const it of items ?? []) itemTheo.set(`${it.lesson_id}:${it.kind}`, it as Item);

// 4. Kế hoạch thay đổi
type Plan = {
  lessonId: number;
  chapter: number;
  title: string;
  theory?: { item: Item; next: string; badCu: string[]; badMoi: string[] };
  btm?: { item: Item; next: unknown[]; subtitle: string; badCu: string[]; badMoi: string[] };
};
const plans: Plan[] = [];
for (const { chapter, dir, bundle } of bundles) {
  const lesson = lessonTheoChuong.get(chapter)!;
  const plan: Plan = { lessonId: lesson.id, chapter, title: lesson.title };
  const lt = itemTheo.get(`${lesson.id}:ly_thuyet`);
  if (!lt) fail(`bài ${lesson.id} (chương ${chapter}) không có mục ly_thuyet`);
  const nextHtml = bundle.theory_html;
  if (lt.body_html !== nextHtml) {
    const badMoi = viPham(nextHtml);
    if (badMoi.length) fail(`lý thuyết chương ${chapter} vẫn còn cụm điểm: ${badMoi.join(", ")}`);
    plan.theory = { item: lt, next: nextHtml, badCu: viPham(lt.body_html), badMoi };
  }
  const bt = itemTheo.get(`${lesson.id}:bai_tap_mau`);
  if (!bt) fail(`bài ${lesson.id} (chương ${chapter}) không có mục bai_tap_mau`);
  const worked = bundle.worked_examples.filter((w) => w.body_html.trim() !== "");
  const nextJson = JSON.parse(JSON.stringify(worked));
  if (canonical(bt.questions) !== canonical(nextJson)) {
    const badCu = viPham(JSON.stringify(bt.questions));
    const badMoi = viPham(JSON.stringify(nextJson));
    if (badMoi.length) fail(`bài tập mẫu chương ${chapter} vẫn còn cụm điểm: ${badMoi.join(", ")}`);
    plan.btm = { item: bt, next: nextJson as unknown[], subtitle: `${worked.length} dạng bài kèm lời giải`, badCu, badMoi };
  }
  plans.push(plan);
}

for (const p of plans) {
  console.log(`Chương ${p.chapter} · bài ${p.lessonId} — ${p.title}`);
  if (!p.theory && !p.btm) {
    console.log("  = không đổi");
    continue;
  }
  if (p.theory) {
    console.log(`  lý thuyết: ${p.theory.item.body_html.length} → ${p.theory.next.length} ký tự`);
    if (p.theory.badCu.length) console.log(`    đang có: ${p.theory.badCu.join(", ")}`);
  }
  if (p.btm) {
    console.log(
      `  bài tập mẫu: ${(p.btm.item.questions as unknown[]).length} → ${p.btm.next.length} dạng` +
        (p.btm.badCu.length ? ` · đang có: ${p.btm.badCu.join(", ")}` : ""),
    );
  }
}

const soThayDoi = plans.filter((p) => p.theory || p.btm).length;
console.log(`\n${soThayDoi}/${plans.length} bài cần ghi.`);
if (DRY) {
  console.log("[DRY-RUN] chưa ghi gì. Chạy lại với --apply để ghi.");
  process.exit(0);
}
if (soThayDoi === 0) {
  console.log("Không có gì để ghi.");
  process.exit(0);
}

// 5. Sao lưu các dòng sắp ghi
const stamp = new Date().toISOString().replace(/[:.]/g, "-");
const backupDir = path.join(root, "scripts", "logs");
fs.mkdirSync(backupDir, { recursive: true });
const backupFile = path.join(backupDir, `avcn-noi-dung-backup-${stamp}.json`);
fs.writeFileSync(
  backupFile,
  JSON.stringify(
    {
      createdAt: new Date().toISOString(),
      lessons: plans.map((p) => ({
        chapter: p.chapter,
        lesson_id: p.lessonId,
        title: p.title,
        ly_thuyet: p.theory ? p.theory.item : null,
        bai_tap_mau: p.btm ? p.btm.item : null,
      })),
    },
    null,
    2,
  ),
);
console.log(`Đã sao lưu: ${path.relative(root, backupFile)}`);

// 6. Ghi
for (const p of plans) {
  if (p.theory) {
    const r = await sb
      .from("lesson_items")
      .update({ body_html: p.theory.next })
      .eq("id", p.theory.item.id)
      .eq("lesson_id", p.lessonId)
      .eq("kind", "ly_thuyet")
      .select("id");
    if (r.error || r.data?.length !== 1) fail(`ghi lý thuyết bài ${p.lessonId}: ${r.error?.message ?? `ảnh hưởng ${r.data?.length} dòng`}`);
    console.log(`✓ lý thuyết bài ${p.lessonId}`);
  }
  if (p.btm) {
    const r = await sb
      .from("lesson_items")
      .update({ questions: p.btm.next, subtitle: p.btm.subtitle })
      .eq("id", p.btm.item.id)
      .eq("lesson_id", p.lessonId)
      .eq("kind", "bai_tap_mau")
      .select("id");
    if (r.error || r.data?.length !== 1) fail(`ghi bài tập mẫu bài ${p.lessonId}: ${r.error?.message ?? `ảnh hưởng ${r.data?.length} dòng`}`);
    console.log(`✓ bài tập mẫu bài ${p.lessonId}`);
  }
}

// 7. Đọc lại, đối chiếu
const { data: after, error: aErr } = await sb
  .from("lesson_items")
  .select("*")
  .in("lesson_id", ids)
  .in("kind", ["ly_thuyet", "bai_tap_mau"]);
if (aErr) fail(`đọc lại lesson_items: ${aErr.message}`);
const afterTheo = new Map<string, Item>();
for (const it of after ?? []) afterTheo.set(`${it.lesson_id}:${it.kind}`, it as Item);

const problems: string[] = [];
for (const p of plans) {
  for (const kind of ["ly_thuyet", "bai_tap_mau"] as const) {
    const truoc = itemTheo.get(`${p.lessonId}:${kind}`)!;
    const sau = afterTheo.get(`${p.lessonId}:${kind}`);
    if (!sau) {
      problems.push(`bài ${p.lessonId} ${kind}: mục biến mất`);
      continue;
    }
    // Mọi cột khác phải y nguyên
    for (const k of Object.keys(truoc)) {
      if (kind === "ly_thuyet" && k === "body_html") continue;
      if (kind === "bai_tap_mau" && (k === "questions" || k === "subtitle")) continue;
      if (canonical(truoc[k]) !== canonical(sau[k])) problems.push(`bài ${p.lessonId} ${kind}: cột ${k} đổi`);
    }
    const b = bundles.find((x) => x.chapter === p.chapter)!.bundle;
    if (kind === "ly_thuyet" && sau.body_html !== b.theory_html) problems.push(`bài ${p.lessonId}: lý thuyết không khớp bundle`);
    if (kind === "bai_tap_mau") {
      const worked = JSON.parse(JSON.stringify(b.worked_examples.filter((w) => w.body_html.trim() !== "")));
      if (canonical(sau.questions) !== canonical(worked)) problems.push(`bài ${p.lessonId}: bài tập mẫu không khớp bundle`);
    }
    if (viPham(kind === "ly_thuyet" ? sau.body_html : JSON.stringify(sau.questions)).length)
      problems.push(`bài ${p.lessonId} ${kind}: vẫn còn cụm điểm`);
  }
}
// Số mục của mỗi bài không đổi
for (const id of ids) {
  const n1 = (items ?? []).filter((x) => x.lesson_id === id).length;
  const n2 = (after ?? []).filter((x) => x.lesson_id === id).length;
  if (n1 !== n2) problems.push(`bài ${id}: số mục ${n1} → ${n2}`);
}

if (problems.length) {
  console.error("\n✗ Đối chiếu SAU ghi thấy lệch:");
  for (const x of problems) console.error("  - " + x);
  console.error(`Hoàn tác: dùng ${path.relative(root, backupFile)}`);
  process.exit(1);
}
console.log(`\n✓ Đã ghi và đối chiếu xong ${soThayDoi} bài. Mọi cột khác giữ nguyên.`);
console.log("Site tĩnh: chạy `bash scripts/deploy.sh` để bản /data/lessons mới lên web.");
