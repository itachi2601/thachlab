// Báo lỗi #141 (24/10/2026): question_bank #7333 đáp án lưu C (nhiệt năng) nhưng đúng là D (nhiệt độ).
// Mặc định dry-run; --apply ghi thật, sao lưu dòng cũ vào scripts/logs/.
import { createClient } from "@supabase/supabase-js";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
for (const l of readFileSync(".env.local", "utf8").split("\n")) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] ??= m[2].trim().replace(/^"|"$/g, ""); }
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
const ID = 7333;
const { data: row, error } = await sb.from("question_bank").select("id,question").eq("id", ID).single();
if (error || !row) throw new Error(error?.message ?? "không thấy dòng");
const q = row.question as any;
if (q.answer !== 2 || !String(q.options?.[3]).startsWith("Nhiệt không thể tự truyền")) { console.log("Dòng đã khác dự kiến, dừng.", q.answer); process.exit(1); }
const next = {
  ...q,
  answer: 3,
  explanation:
    '<p class="text-base leading-relaxed my-2">Nhiệt chỉ truyền tự phát từ vật có <strong class="font-bold">nhiệt độ</strong> cao sang vật có nhiệt độ thấp (không phụ thuộc vật nào có nhiệt năng lớn hơn). Vì vậy nhiệt không thể tự truyền từ vật có nhiệt độ thấp sang vật có nhiệt độ cao hơn.</p><p class="text-base leading-relaxed my-2">Chọn D.</p>',
};
console.log("answer", q.answer, "->", next.answer);
if (!process.argv.includes("--apply")) { console.log("dry-run, thêm --apply để ghi"); process.exit(0); }
mkdirSync("scripts/logs", { recursive: true });
writeFileSync(`scripts/logs/qb-${ID}-truoc-sua-bao-loi-141.json`, JSON.stringify(row, null, 1));
const { error: e2 } = await sb.from("question_bank").update({ question: next }).eq("id", ID);
if (e2) throw new Error(e2.message);
const { data: chk } = await sb.from("question_bank").select("question").eq("id", ID).single();
console.log("đã ghi, answer =", (chk?.question as any).answer);
