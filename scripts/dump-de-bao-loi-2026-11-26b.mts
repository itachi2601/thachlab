// Chỉ ĐỌC: xuất đề 123, 289 (báo lỗi #172, #171 — 26/11/2026).
import { createClient } from "@supabase/supabase-js";
import { readFileSync, writeFileSync } from "node:fs";
for (const l of readFileSync(".env.local", "utf8").split("\n")) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] ??= m[2].trim().replace(/^"|"$/g, ""); }
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
const { data } = await sb.from("exams").select("id,title,questions").in("id", [123, 289]);
for (const e of data ?? []) { writeFileSync(`scripts/logs/bao-loi-1126/de-${e.id}.json`, JSON.stringify(e, null, 1)); console.log("de", e.id); }
