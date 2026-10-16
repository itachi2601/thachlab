// Sửa nốt các ca độ C mất dấu độ còn sót sau sua-do-c-mat-dau-do.mts (chuỗi cụ thể theo id), sao lưu ra scripts/logs/.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const env = (k: string) => fs.readFileSync(".env.local", "utf8").split("\n").find((l) => l.startsWith(`${k}=`))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const SP: [RegExp, string][] = [[/(\d{2}(?:,\d)?) 0C/g, "$1°C"]];
const FIX: Record<number, [RegExp, string][]> = {
  656431: [[/3270C/, "327°C"], [/16130C/, "1613°C"], [/Bước 00C/, "Bước 0°C"], [/1000C/, "100°C"]],
  656431: [[/3270C/, "327°C"], [/16130C/, "1613°C"], [/Bước 00C/, "Bước 0°C"], [/1000C/, "100°C"]],
};
const { data } = await sb.from("question_bank").select("id, question").in("id", Object.keys(FIX).map(Number));
fs.writeFileSync(`scripts/logs/backup-do-c-le-${Date.now()}.json`, JSON.stringify(data));
for (const r of data!) {
  let js = JSON.stringify(r.question); const before = js;
  for (const [a, b] of FIX[r.id]) js = js.replace(a, b);
  if (js === before) { console.log(r.id, "KHÔNG ĐỔI"); continue; }
  const { error } = await sb.from("question_bank").update({ question: JSON.parse(js) }).eq("id", r.id);
  console.log(r.id, error ? error.message : "ok");
}
