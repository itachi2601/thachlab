// Chỉ ĐỌC: dò exams chứa câu báo lỗi 26/11/2026 (#171 nút chai, #172 Charles, #176 hai bình van, #174 6,68).
import { createClient } from "@supabase/supabase-js";
import { readFileSync } from "node:fs";
for (const l of readFileSync(".env.local", "utf8").split("\n")) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] ??= m[2].trim().replace(/^"|"$/g, ""); }
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
const needles: Record<string, string> = {
  "171": "nút chai và thành bình thủy tinh",
  "171b": "nung nóng khí trong chai đến",
  "172": "biểu thức nào sau đây không đúng với định luật Charles",
  "176": "thông nhau qua một cái van. Van chỉ mở",
  "174": "6,68",
};
const { data: ids } = await sb.from("exams").select("id").order("id");
for (let i = 0; i < (ids ?? []).length; i += 50) {
  const chunk = ids!.slice(i, i + 50).map((r) => r.id);
  for (let t = 0; t < 3; t++) {
    const { data, error } = await sb.from("exams").select("id,title,questions").in("id", chunk);
    if (error) { await new Promise((r) => setTimeout(r, 2000)); continue; }
    for (const e of data ?? []) ((e.questions as any[]) ?? []).forEach((q, j) => { const s = JSON.stringify(q); for (const [k, n] of Object.entries(needles)) if (s.includes(n)) console.log(k, "exam", e.id, e.title, "idx", j); });
    break;
  }
}
console.log("XONG");
