// Áp phản hồi thầy duyệt đợt so-mu-2026-10-16 (scripts/data/duyet/so-mu-2026-10-16/phan-hoi.json): sửa chuỗi cụ thể, sao lưu bản gốc ra scripts/logs/.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const env = (k: string) => fs.readFileSync(".env.local", "utf8").split("\n").find((l) => l.startsWith(`${k}=`))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const FIX: Record<number, [string, string][]> = {
  1475529: [["10.103 m3", "10.10<sup>−3</sup> m<sup>3</sup>"], ["30.103 m3", "30.10<sup>−3</sup> m<sup>3</sup>"]],
  1178258: [["q = 5.10-2  $\\mu C.$", "q = 5.10<sup>−2</sup>  $\\mu C.$"]],
  398354: [["x.102%.V", "x.1,02.V"]],
  642757: [["105 pa", "10<sup>5</sup> Pa"], ["10^5.103%", "10^5.1,03"]],
  656420: [["770C", "77°C"], ["270C", "27°C"], ["370C", "37°C"], ["170C", "17°C"], ["V_1.101%", "V_1.1,01"], ["27^0C", "27^\\circ C"], ["t^0C", "t^\\circ C"]],
  571235: [["$p_0$ = 105 Pa", "$p_0 = 10^5$ Pa"]],
  669975: [["= 270C", "= 27°C"], ["t = -500C", "t = −50°C"], ["V = 6.102 m<sup>3</sup>", "V = 6.10<sup>2</sup> m<sup>3</sup>"]],
};
const ids = Object.keys(FIX).map(Number);
const { data } = await sb.from("question_bank").select("id, question").in("id", ids);
fs.writeFileSync(`scripts/logs/backup-duyet-so-mu-${Date.now()}.json`, JSON.stringify(data));
for (const r of data!) {
  let js = JSON.stringify(r.question);
  for (const [a, b] of FIX[r.id]) {
    const ea = JSON.stringify(a).slice(1, -1), eb = JSON.stringify(b).slice(1, -1);
    if (!js.includes(ea)) { console.log(r.id, "KHÔNG KHỚP:", a); continue; }
    js = js.split(ea).join(eb);
  }
  const { error } = await sb.from("question_bank").update({ question: JSON.parse(js) }).eq("id", r.id);
  console.log(r.id, error ? error.message : "ok");
}
