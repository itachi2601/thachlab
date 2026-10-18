// Sửa tay 4 lời giải viết lại (HS kiểm 18/10/2026): 673791, 1503770, 397781, 1495563. Sao lưu scripts/logs/. Chỉ question_bank.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const P = (t: string) => `<p class="text-base leading-relaxed my-2">${t}</p>`;
const rep: Record<number, (e: string) => string> = {
  673791: (e) => e.replace(/<p[^>]*>Sai vì:.*?<\/p>/s, P("Sai vì: A ($p/V=nRT$), B ($V/T=npR$) và C ($np/V=RT$) đều cho $p$ tăng khi $V$ tăng (ở $T$ không đổi), trái định luật Boyle ($pV$ không đổi nên $p$ giảm khi $V$ tăng).")),
  1503770: (e) => e.replace(/<p[^>]*>Sai vì:.*?<\/p>/s, P("Sai vì: A (1 s) cho quãng ngang $5\\cdot 1=5\\ \\text{m}\\ne 15\\ \\text{m}$; B (2 s) cho $5\\cdot 2=10\\ \\text{m}$; C (4 s) cho $5\\cdot 4=20\\ \\text{m}$; đều không bằng tầm xa 15 m.")),
  397781: (e) => e.replace(/<p[^>]*>Đề hiểu là.*?<\/p>/s, ""),
  1495563: (e) => e.replace("yếu hơn lực hạt nhân cỡ $10^{36}$ lần", "rất yếu so với lực hạt nhân (chênh nhau hàng chục bậc độ lớn)"),
};
const { data, error } = await sb.from("question_bank").select("id,question").in("id", Object.keys(rep).map(Number));
if (error) throw new Error(error.message);
fs.writeFileSync(`scripts/logs/sua-viet-lai-4-cau-backup-${Date.now()}.json`, JSON.stringify(data));
for (const r of data!) {
  const ex2 = rep[r.id](r.question.explanation);
  if (ex2 === r.question.explanation) { console.log("KHÔNG ĐỔI", r.id); continue; }
  const { error: e2 } = await sb.from("question_bank").update({ question: { ...r.question, explanation: ex2 } }).eq("id", r.id);
  console.log(r.id, e2 ? "LỖI " + e2.message : "ok");
}
