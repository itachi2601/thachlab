// Chỉ ĐỌC: mục bai_tap_mau của L10 bài 68–79 đã có chưa, bao nhiêu dạng, sửa lần cuối khi nào.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const envText = fs.readFileSync(path.join(root, ".env.local"), "utf8").split("\n");
const env = (k: string) => envText.find((l) => l.startsWith(k + "="))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!);

const ids = [68, 69, 70, 71, 72, 73, 74, 76, 77, 78, 79];
const { data, error } = await sb.from("lesson_items").select("*").in("lesson_id", ids).eq("kind", "bai_tap_mau");
if (error) throw error;
for (const id of ids) {
  const rows = (data ?? []).filter((r: any) => r.lesson_id === id);
  if (!rows.length) { console.log(id, "CHƯA có mục bai_tap_mau"); continue; }
  for (const r of rows as any[]) {
    const q = Array.isArray(r.questions) ? r.questions : [];
    const buoc = q.filter((x: any) => JSON.stringify(x).includes("buoc")).length;
    console.log(id, "item", r.id, "|", q.length, "dạng, có buoc:", buoc, "|", r.subtitle ?? "", "|", r.published_at ? "đã đăng" : "nháp");
  }
}
