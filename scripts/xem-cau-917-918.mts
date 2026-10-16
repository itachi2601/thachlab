import { createClient } from "@supabase/supabase-js";
import { readFileSync } from "node:fs";
for (const l of readFileSync(".env.local", "utf8").split("\n")) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] ??= m[2].trim().replace(/^"|"$/g, ""); }
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
for (const [id, i] of [[917, 2], [918, 10]] as const) {
  const { data } = await sb.from("exams").select("questions").eq("id", id).single();
  console.log("== exam", id, "q", i + 1, JSON.stringify((data!.questions as any[])[i]));
}
