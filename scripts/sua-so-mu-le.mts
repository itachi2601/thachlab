// Sửa tay 5 chỗ số mũ mất ^ mà script hàng loạt bỏ sót (hệ số n/Ν Hy Lạp, trong $…$ không khoảng trắng). Sao lưu ra scripts/logs/.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const d = path.dirname(fileURLToPath(import.meta.url));
const env = (k: string) => fs.readFileSync(path.resolve(d, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const FIX: [number, RegExp, string][] = [
  [570416, /n\.105 Pa/g, "n.10<sup>5</sup> Pa"],
  [590943, /3\.108m\/s/g, "3.10^{8}m/s"],
  [607408, /4\.102 Ν/g, "4.10<sup>2</sup> Ν"],
  [673780, /D = 6\.102 kg/g, "D = 6.10<sup>2</sup> kg"],
  [1178258, /5\.10-2 \$\\mu C/g, "5.10<sup>−2</sup> $\\mu C"],
];
const backup: any[] = [];
for (const [id, re, rep] of FIX) {
  const { data } = await sb.from("question_bank").select("id, question").eq("id", id).single();
  const js = JSON.stringify(data!.question);
  const n = (js.match(re) ?? []).length;
  console.log(id, "khớp", n);
  if (n < 1) continue;
  backup.push({ id, question: data!.question });
  const { error } = await sb.from("question_bank").update({ question: JSON.parse(js.replace(re, rep.replace(/\\/g, "\\\\"))) }).eq("id", id);
  if (error) { console.error(id, error.message); process.exit(1); }
}
fs.writeFileSync(path.join(d, "logs", `backup-so-mu-le-${Date.now()}.json`), JSON.stringify(backup));
