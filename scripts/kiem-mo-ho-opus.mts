// Kiểm lại sau ap-dung-mo-ho-opus.mts --apply: đọc question_bank, so với kq Opus (đề + đáp án + lời giải; câu "an" phải archived).
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import { tachMuiTen } from "./lib/giai-lai-chung.mts";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const DIR = "scripts/data/giai-lai/mo-ho/opus/";
const GIU: number[] = JSON.parse(fs.readFileSync(DIR + "giu-lai.json", "utf8"));
const kq = fs.readdirSync(DIR).filter((f) => /^kq-\d+\.json$/.test(f)).flatMap((f) => JSON.parse(fs.readFileSync(DIR + f, "utf8")) as any[]).filter((k) => k.kl !== "hoi" && !GIU.includes(k.id));
const { data, error } = await sb.from("question_bank").select("id,archived,question").in("id", kq.map((k) => k.id));
if (error) throw new Error(error.message);
const m = new Map(data!.map((r) => [r.id, r]));
const lamSach = (h: string) => h.replace(/(?<!\\)\$(.+?)(?<!\\)\$/gs, (_m, t: string) => "$" + t.replace(/</g, "\\lt ").replace(/>/g, "\\gt ") + "$");
const sai: string[] = [];
for (const k of kq) {
  const r = m.get(k.id); if (!r) { sai.push(`${k.id} không thấy`); continue; }
  if (k.kl === "an") { if (!r.archived) sai.push(`${k.id} chưa ẩn`); continue; }
  const n = { ...k.cau_hoi_moi, explanation: tachMuiTen(lamSach(String(k.cau_hoi_moi.explanation))) };
  if (JSON.stringify(r.question) !== JSON.stringify(n)) sai.push(`${k.id} khác kq`);
}
console.log(`kiểm ${kq.length} câu, lệch ${sai.length}`, sai.slice(0, 20));
