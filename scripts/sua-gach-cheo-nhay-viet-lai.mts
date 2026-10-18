// Bỏ dấu \" thừa (gạch chéo ngược trước nháy) trong lời giải đã ghi ở đợt viết lại 1 (viet-lai). Chỉ question_bank, có sao lưu.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const ids: number[] = [];
for (const f of fs.readdirSync("scripts/data/giai-lai/viet-lai").filter((f) => /^kq-\d+\.json$/.test(f))) for (const x of JSON.parse(fs.readFileSync("scripts/data/giai-lai/viet-lai/" + f, "utf8"))) if (x.explanation.includes('\\"')) ids.push(x.id);
const { data, error } = await sb.from("question_bank").select("id,question").in("id", ids);
if (error) throw new Error(error.message);
const dirty = data!.filter((r) => String(r.question.explanation ?? "").includes('\\"'));
fs.writeFileSync(`scripts/logs/sua-gach-cheo-backup-${Date.now()}.json`, JSON.stringify(dirty));
for (const r of dirty) { const { error: e } = await sb.from("question_bank").update({ question: { ...r.question, explanation: r.question.explanation.replaceAll('\\"', '"') } }).eq("id", r.id); console.log(r.id, e ? "LỖI " + e.message : "ok"); }
console.log("cần sửa", dirty.length, "/", ids.length);
