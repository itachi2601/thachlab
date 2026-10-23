// Báo lỗi #137: đề 753 câu 6 ý c thiếu "ở cùng nhiệt độ". Giữ answer=true. Dry-run mặc định, --apply để ghi (exams + bản sao trong question_bank). Sao lưu trước khi ghi.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const apply = process.argv.includes("--apply");
const OLD = "Cùng một chất, khối lượng càng lớn thì nội năng càng lớn.";
const NEW = "Cùng một chất, ở cùng nhiệt độ, khối lượng càng lớn thì nội năng càng lớn.";
const sua = (q: any) => { const n = structuredClone(q); const s = n.statements?.find((x: any) => x.text === OLD); if (s) s.text = NEW; return n; };
const { data: e } = await sb.from("exams").select("id,questions").eq("id", 753).single();
const idx = e!.questions.findIndex((q: any) => q.statements?.some((s: any) => s.text === OLD));
if (idx < 0) throw new Error("không thấy câu (đã sửa rồi?)");
const { data: bank } = await sb.from("question_bank").select("id,question").filter("question->statements", "cs", JSON.stringify([{ text: OLD }]));
console.log("đề 753 idx", idx, "| bản sao ngân hàng:", bank?.map((b) => b.id));
if (!apply) { console.log("DRY-RUN, thêm --apply để ghi"); process.exit(0); }
const bp = `scripts/logs/sua-de753-cau6-backup-${Date.now()}.json`;
fs.writeFileSync(bp, JSON.stringify({ exam: e, bank })); console.log("sao lưu:", bp);
const qs = structuredClone(e!.questions); qs[idx] = sua(qs[idx]);
console.log("exams", (await sb.from("exams").update({ questions: qs }).eq("id", 753)).error?.message ?? "ok");
for (const b of bank ?? []) console.log("bank", b.id, (await sb.from("question_bank").update({ question: sua(b.question) }).eq("id", b.id)).error?.message ?? "ok");
const { data: c } = await sb.from("exams").select("questions").eq("id", 753).single();
console.log("sau:", c!.questions[idx].statements[2].text, "| answer", c!.questions[idx].statements[2].answer);
