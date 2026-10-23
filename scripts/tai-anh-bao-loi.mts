import { createClient } from "@supabase/supabase-js";
import { writeFileSync } from "node:fs";
import { readFileSync } from "node:fs";
for (const l of readFileSync(".env.local", "utf8").split("\n")) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] ??= m[2].trim().replace(/^"|"$/g, ""); }
const out = process.argv[2];
import { mkdirSync } from "node:fs"; mkdirSync(out, { recursive: true });
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
const { data } = await sb.from("bug_reports").select("id,screenshot_path").in("id", (process.argv[3] ?? "108,109,110,111,113,114").split(",").map(Number));
for (const r of data ?? []) {
  const { data: f, error } = await sb.storage.from("bug-report-screenshots").download(r.screenshot_path);
  if (error || !f) { console.log("fail", r.id, error?.message); continue; }
  writeFileSync(`${out}/${r.id}.jpg`, Buffer.from(await f.arrayBuffer()));
  console.log("ok", r.id);
}
