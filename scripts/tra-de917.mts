import { createClient } from "@supabase/supabase-js";
import { readFileSync, writeFileSync } from "node:fs";
for (const l of readFileSync(".env.local", "utf8").split("\n")) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] ??= m[2].trim().replace(/^"|"$/g, ""); }
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
const { data } = await sb.from("exams").select("questions").eq("id", 917).single();
const t = (x: any) => String(x ?? "").replace(/<img[^>]*>/g, "[HINH]").replace(/<[^>]+>/g, " ").slice(0, 500);
writeFileSync("/private/tmp/claude-501/-Users-MAC-Projects-thachlab/fdb9ffa7-aead-4851-a4c0-cb91cc4afe32/scratchpad/bl/917-text.txt", (data!.questions as any[]).map((q, i) => "Q" + (i + 1) + ": " + t(q.question) + "\n  opts: " + (q.options ?? []).map(t).join(" | ").slice(0, 300)).join("\n"));
