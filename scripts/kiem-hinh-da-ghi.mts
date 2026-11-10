// Kiểm (CHỈ ĐỌC): mỗi id trong quyet-dinh.json phải có đúng 1 <svg trong đề ngân hàng. Dùng: npx tsx scripts/kiem-hinh-da-ghi.mts hinh-cau-hoi
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const dir = path.dirname(fileURLToPath(import.meta.url));
const env = (k: string) => process.env[k] ?? [path.resolve(dir, "..", ".env.local"), "/Users/MAC/Projects/thachlab/.env.local"].filter(fs.existsSync).map((p) => fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${k}=`))).find(Boolean)?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const ids = Object.keys(JSON.parse(fs.readFileSync(path.join(dir, "data", process.argv[2], "quyet-dinh.json"), "utf8"))).filter((k) => /^\d+$/.test(k)).map(Number);
const { data, error } = await sb.from("question_bank").select("id, question").in("id", ids);
if (error) { console.error(error.message); process.exit(1); }
const n = (s: string) => (s.match(/<svg[\s>]/gi) ?? []).length;
const bad = (data ?? []).filter((r) => n(String((r.question as { question?: string }).question ?? "")) !== 1);
console.log(`${data?.length}/${ids.length} câu; sai số hình: ${bad.length}`, bad.map((r) => `${r.id}:${n(String((r.question as { question?: string }).question))}`).join(" "));
