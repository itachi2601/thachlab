import { createClient } from "@supabase/supabase-js";
import { readFileSync } from "node:fs";
for (const l of readFileSync(".env.local", "utf8").split("\n")) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] ??= m[2].trim().replace(/^"|"$/g, ""); }
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
const { data } = await sb.from("lessons").select("id,title,chapter_id,published").or("title.ilike.%chuyển thể%,title.ilike.%thang nhiệt%,title.ilike.%nội năng%,title.ilike.%thực hành%nhiệt%,title.ilike.%đo nhiệt dung%");
for (const r of data ?? []) console.log(r.id, "|", r.title, "| ch", r.chapter_id, "|", r.published);
