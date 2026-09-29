/**
 * Rà lại đề/bài học đã đăng để tìm nội dung bị dính liền: nhiều dòng "Bước n:",
 * "- ", "a)", "1)"... nằm chung một khối văn bản mà không có <br> ngăn cách —
 * đúng bug vừa sửa trong exam-latex-parser.ts / latex-converter.ts.
 *
 * Chỉ ĐỌC, không sửa gì trên Supabase — in ra danh sách để rà tay/quyết định.
 */
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";

function readEnvLocal(name: string): string | undefined {
  const envPath = path.resolve(import.meta.dirname, "..", ".env.local");
  if (!fs.existsSync(envPath)) return undefined;
  const line = fs
    .readFileSync(envPath, "utf8")
    .split("\n")
    .find((l) => l.startsWith(`${name}=`));
  return line?.slice(name.length + 1).trim();
}

const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
const key = process.env.SUPABASE_SERVICE_ROLE_KEY ?? readEnvLocal("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) throw new Error("Thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY trong .env.local");
const supabase = createClient(url, key);

// Thu hẹp có chủ đích: chỉ bắt đúng chữ "Bước n" lặp lại — khớp sát lời than phiền gốc
// ("các bước thí nghiệm"). Không bắt "(1)... (2)..." hay "a)... b)..." vì phần lớn lời
// giải Đúng/Sai vốn được soạn liền mạch một đoạn theo đúng chủ ý (xuat_thachlab.py),
// bắt rộng hơn sẽ ra hàng trăm false-positive không phải bug.
const STEP_LINE_RE = /(?:^|[.\s>])Bước\s*\d+\s*[:.)]/gi;

/** Đếm mốc "Bước n" trong một đoạn KHÔNG bị <br> ngăn cách — >=2 mốc trong cùng 1 đoạn là dấu hiệu dính liền. */
function maxMarkersInOneSegment(text: string): number {
  if (!text) return 0;
  const segments = text.split(/<br\s*\/?>|<\/p>|<p[^>]*>/i);
  let max = 0;
  for (const seg of segments) {
    const hits = seg.match(STEP_LINE_RE);
    if (hits && hits.length > max) max = hits.length;
  }
  return max;
}

function fieldsOf(q: any): { field: string; text: string }[] {
  const out: { field: string; text: string }[] = [];
  if (typeof q.question === "string") out.push({ field: "question", text: q.question });
  if (typeof q.explanation === "string") out.push({ field: "explanation", text: q.explanation });
  if (Array.isArray(q.options))
    q.options.forEach((o: string, i: number) => out.push({ field: `options[${i}]`, text: o }));
  if (Array.isArray(q.statements))
    q.statements.forEach((s: any, i: number) => out.push({ field: `statements[${i}]`, text: s?.text ?? "" }));
  return out;
}

async function auditExams() {
  console.log("\n=== ĐỀ (exams.questions) ===");
  const { data, error } = await supabase.from("exams").select("id, title, questions");
  if (error) throw error;
  let hit = 0;
  for (const exam of data ?? []) {
    const questions = (exam.questions as any[]) ?? [];
    questions.forEach((q, qi) => {
      for (const { field, text } of fieldsOf(q)) {
        const n = maxMarkersInOneSegment(text);
        if (n >= 2) {
          hit += 1;
          console.log(`- exam #${exam.id} "${exam.title}" · câu ${qi + 1} · ${field} · ${n} mốc dính liền`);
          console.log(`    ${text.slice(0, 160).replace(/\s+/g, " ")}${text.length > 160 ? "…" : ""}`);
        }
      }
    });
  }
  console.log(`Tổng: ${hit} chỗ nghi dính liền trong đề.`);
}

async function auditLessons() {
  console.log("\n=== BÀI HỌC (lesson_items.body_html, kind=ly_thuyet) ===");
  const { data, error } = await supabase
    .from("lesson_items")
    .select("id, lesson_id, title, body_html")
    .eq("kind", "ly_thuyet");
  if (error) throw error;
  let hit = 0;
  for (const item of data ?? []) {
    const n = maxMarkersInOneSegment(item.body_html ?? "");
    if (n >= 2) {
      hit += 1;
      console.log(`- lesson_item #${item.id} (lesson ${item.lesson_id}) "${item.title}" · ${n} mốc dính liền`);
    }
  }
  console.log(`Tổng: ${hit} mục lý thuyết nghi dính liền.`);
}

async function main() {
  await auditExams();
  await auditLessons();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
