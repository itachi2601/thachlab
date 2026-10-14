// Lưu trữ (archived=true) các câu ngân hàng có ảnh TRỐNG hoặc KHÔNG MỞ ĐƯỢC — đọc từ anh-le-trang.json do kiem-anh-le-trang.mts --bank sinh ra.
//   npx tsx scripts/luu-tru-cau-anh-trong-hong.mts          # dry-run: chỉ liệt kê
//   npx tsx scripts/luu-tru-cau-anh-trong-hong.mts --apply   # ghi; sao lưu trạng thái cũ (archived, note) ra scripts/logs/
// Không xoá dòng nào; đề đã tạo từ các câu này không bị đụng (chúng giữ bản sao riêng).
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const dir = path.dirname(fileURLToPath(import.meta.url));
function env(k: string) { const l = fs.readFileSync(path.resolve(dir, "..", ".env.local"), "utf8").split("\n").find((x) => x.startsWith(k + "=")); return l?.slice(k.length + 1).trim(); }
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL ?? env("NEXT_PUBLIC_SUPABASE_URL")!, process.env.SUPABASE_SERVICE_ROLE_KEY ?? env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const rep = JSON.parse(fs.readFileSync(path.join(dir, "data", "kiem-ke-anh-ngan-hang", "anh-le-trang.json"), "utf8")) as { hits: { id: number; frac: number; label: string }[]; errs: { id?: number; src: string; loi: string }[] };
const blank = rep.hits.filter((h) => h.label === "ngân hàng" && h.frac < 0.002).map((h) => h.id);
const broken = rep.errs.filter((e) => e.id).map((e) => e.id!);
const ids = [...new Set([...blank, ...broken])];
console.log(`ảnh trống: ${blank.length} câu; ảnh không mở được: ${new Set(broken).size} câu; tổng ${ids.length} câu`, ids);
if (!ids.length) process.exit(0);
const { data, error } = await sb.from("question_bank").select("id, archived, note").in("id", ids);
if (error) { console.error(error.message); process.exit(1); }
console.log(`${data!.filter((r) => !r.archived).length} câu đang hiện, ${data!.filter((r) => r.archived).length} đã lưu trữ sẵn`);
if (!process.argv.includes("--apply")) { console.log("DRY-RUN, chưa ghi. Thêm --apply để lưu trữ."); process.exit(0); }
fs.mkdirSync(path.join(dir, "logs"), { recursive: true });
const bk = path.join(dir, "logs", `luu-tru-anh-trong-hong-${new Date().toISOString().replace(/[:.]/g, "-")}.backup.json`);
fs.writeFileSync(bk, JSON.stringify(data));
for (const r of data!.filter((x) => !x.archived)) {
  const note = [r.note, "ảnh trống/không mở được, lưu trữ 14/10/2026"].filter(Boolean).join(" | ");
  const u = await sb.from("question_bank").update({ archived: true, note }).eq("id", r.id);
  if (u.error) console.error(r.id, u.error.message);
}
console.log("xong. Sao lưu:", bk, "\nHoàn tác: đặt lại archived/note theo file này.");
