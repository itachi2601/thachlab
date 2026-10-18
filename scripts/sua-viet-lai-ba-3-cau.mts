// Sửa văn 3 lời giải lô ảnh (HS kiểm 18/10/2026): 457310, 1501615, 670214. Sao lưu scripts/logs/. Chỉ question_bank.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const rep: Record<number, [string, string][]> = {
  457310: [['"áp suất" không phải đại lượng tăng lên khi hấp thụ nhiệt trong câu này.', 'chỗ trống (2) cần đại lượng đo độ nóng lạnh, tức nhiệt độ, không phải áp suất.']],
  1501615: [["độ dốc đều thay đổi nên $a$ không đổi là sai.", "độ dốc của chúng thay đổi nên $a$ thay đổi, không phải chuyển động biến đổi đều."]],
  670214: [[", và đây là đẳng quá trình nên cũng không chọn B.", ". B (đẳng áp) cũng không chọn vì đoạn nằm ngang là đẳng nhiệt."]],
};
const { data, error } = await sb.from("question_bank").select("id,question").in("id", Object.keys(rep).map(Number));
if (error) throw new Error(error.message);
fs.writeFileSync(`scripts/logs/sua-viet-lai-ba-3-cau-backup-${Date.now()}.json`, JSON.stringify(data));
for (const r of data!) {
  let e = String(r.question.explanation);
  for (const [a, b] of rep[r.id]) e = e.includes(a) ? e.replace(a, b) : (console.log("KHÔNG KHỚP", r.id, a.slice(0, 30)), e);
  if (e === r.question.explanation) continue;
  const { error: e2 } = await sb.from("question_bank").update({ question: { ...r.question, explanation: e } }).eq("id", r.id);
  console.log(r.id, e2 ? "LỖI " + e2.message : "ok");
}
