// Sửa nốt vài ca độ C lẻ (theo id) sau sua-do-c-dang-con-lai.mts, sao lưu ra scripts/logs/.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const env = (k: string) => fs.readFileSync(".env.local", "utf8").split("\n").find((l) => l.startsWith(`${k}=`))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const FIX: Record<number, [RegExp, string][]> = {
  7727: [[/100 \^\{0\}C/g, "100^\\\\circ C"]],
  570414: [[/(\d\d) 0 C/g, "$1°C"]],
  401746: [[/ở 20 C/g, "ở 20°C"]],
  458578: [[/bằng 60 C/g, "bằng 60°C"]],
  458582: [[/độ 20 C/g, "độ 20°C"]],
};
const { data } = await sb.from("question_bank").select("id, question").in("id", Object.keys(FIX).map(Number));
fs.writeFileSync(`scripts/logs/backup-do-c-le2-${Date.now()}.json`, JSON.stringify(data));
for (const r of data!) {
  let js = JSON.stringify(r.question); const before = js;
  for (const [a, b] of FIX[r.id]) js = js.replace(a, b);
  if (js === before) { console.log(r.id, "KHÔNG ĐỔI"); continue; }
  const { error } = await sb.from("question_bank").update({ question: JSON.parse(js) }).eq("id", r.id);
  console.log(r.id, error ? error.message : "ok");
}
