// Đọc <thư-mục>/phan-hoi.json do thầy lưu từ trang duyệt (scripts/lap-duyet-html.mts), rồi:
//   "bo"  → ẩn câu (archived=true), sao lưu bản gốc ra scripts/logs/;  thêm --dry để chỉ liệt kê
//   "de_xuat" / "y_thay" → KHÔNG tự ghi: in ra để Claude sửa theo đề xuất / ý thầy rồi quét lại
//   "giu" → bỏ qua;  chưa chọn → báo còn treo
//   npx tsx scripts/ap-dung-duyet.mts scripts/data/duyet/<tên-đợt> [--dry]
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const d = path.dirname(fileURLToPath(import.meta.url));
const env = (k: string) => fs.readFileSync(path.resolve(d, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const dir = path.resolve(process.argv[2] ?? ""), DRY = process.argv.includes("--dry");
const items: { id: number; deXuat?: string }[] = JSON.parse(fs.readFileSync(path.join(dir, "items.json"), "utf8"));
const fb = JSON.parse(fs.readFileSync(path.join(dir, "phan-hoi.json"), "utf8")).items as Record<string, { action?: string; note?: string }>;
const bo: number[] = [], sua: string[] = [], treo: number[] = [];
for (const it of items) {
  const f = fb[it.id];
  if (!f?.action) treo.push(it.id);
  else if (f.action === "bo") bo.push(it.id);
  else if (f.action === "de_xuat") sua.push(`#${it.id} SỬA THEO ĐỀ XUẤT: ${it.deXuat || "(không có đề xuất)"}${f.note ? " · ghi chú: " + f.note : ""}`);
  else if (f.action === "y_thay") sua.push(`#${it.id} SỬA THEO Ý THẦY: ${f.note || "(thầy chưa ghi gì)"}`);
}
if (bo.length && !DRY) {
  const { data } = await sb.from("question_bank").select("id, archived").in("id", bo);
  fs.writeFileSync(path.join(d, "logs", `backup-duyet-bo-${Date.now()}.json`), JSON.stringify(data));
  const { error } = await sb.from("question_bank").update({ archived: true }).in("id", bo);
  if (error) { console.error(error.message); process.exit(1); }
}
console.log(`${DRY ? "DRY · " : ""}Bỏ (ẩn): ${bo.join(", ") || "—"}\nGiữ nguyên: ${items.filter((i) => fb[i.id]?.action === "giu").map((i) => i.id).join(", ") || "—"}\nChờ Claude sửa:\n${sua.join("\n") || "—"}\nChưa quyết: ${treo.join(", ") || "—"}`);
