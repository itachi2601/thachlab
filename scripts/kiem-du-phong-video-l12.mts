import { createClient } from "@supabase/supabase-js";
import { readFileSync } from "node:fs";
for (const l of readFileSync(".env.local", "utf8").split("\n")) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] ??= m[2].trim().replace(/^"|"$/g, ""); }
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
const { data } = await sb.from("lesson_items").select("id,lesson_id,body_html").in("id", [8, 171, 173, 175]);
for (const r of data ?? []) { const h = String(r.body_html); console.log(r.lesson_id, "iframe", (h.match(/<iframe/g) ?? []).length, "du-phong", (h.match(/Nếu không xem được video/g) ?? []).length, "sau-iframe", (h.match(/<\/iframe><\/div>\s*<p><strong>Nếu không xem/g) ?? []).length); }
