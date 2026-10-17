// Đọc <thư-mục>/phan-hoi.json từ trang scripts/lap-duyet-lop-de.mts rồi gán lớp cho đề:
//   action = "<class_id>" → chèn exam_classes (sao lưu danh sách chèn ra scripts/logs/)
//   "toan_truong" → không đổi;  "an" → published=false (sao lưu);  chưa chọn → báo còn treo
//   npx tsx scripts/ap-dung-duyet-lop-de.mts scripts/data/duyet/<tên-đợt> [--dry]
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const d = path.dirname(fileURLToPath(import.meta.url));
const env = (k: string) => fs.readFileSync(path.resolve(d, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const dir = path.resolve(process.argv[2] ?? ""), DRY = process.argv.includes("--dry");
const items: { id: number }[] = JSON.parse(fs.readFileSync(path.join(dir, "items.json"), "utf8"));
const fb = JSON.parse(fs.readFileSync(path.join(dir, "phan-hoi.json"), "utf8")).items as Record<string, { action?: string; note?: string }>;
const { data: cls } = await sb.from("classes").select("id, name");
const classIds = new Set((cls ?? []).map((c) => c.id));
const gan: { exam_id: number; class_id: number }[] = [], an: number[] = [], treo: number[] = [], giu: number[] = [];
for (const it of items) {
  const a = fb[it.id]?.action;
  if (!a) treo.push(it.id);
  else if (a === "toan_truong") giu.push(it.id);
  else if (a === "an") an.push(it.id);
  else if (classIds.has(Number(a))) gan.push({ exam_id: it.id, class_id: Number(a) });
  else treo.push(it.id);
}
console.log(`Gán lớp: ${gan.length} · Ẩn: ${an.length} · Giữ toàn trường: ${giu.length} · Chưa chọn: ${treo.length}${treo.length ? " → " + treo.join(", ") : ""}`);
for (const g of gan) console.log(`  #${g.exam_id} → lớp ${cls?.find((c) => c.id === g.class_id)?.name}${fb[g.exam_id]?.note ? "   ghi chú: " + fb[g.exam_id].note : ""}`);
if (DRY) process.exit(0);
const stamp = new Date().toISOString().replace(/[:.]/g, "-");
const bak = path.resolve(d, "logs", `ap-dung-duyet-lop-de-${stamp}.json`);
fs.mkdirSync(path.dirname(bak), { recursive: true });
fs.writeFileSync(bak, JSON.stringify({ gan, an }, null, 1));
if (gan.length) {
  // Bỏ cặp đã có (đề có thể đã được gán bởi đợt khác trong lúc chờ duyệt).
  const { data: have } = await sb.from("exam_classes").select("exam_id, class_id").in("exam_id", gan.map((g) => g.exam_id));
  const key = new Set((have ?? []).map((h) => `${h.exam_id}:${h.class_id}`));
  const rows = gan.filter((g) => !key.has(`${g.exam_id}:${g.class_id}`));
  const { error } = await sb.from("exam_classes").insert(rows);
  if (error) { console.error("Lỗi chèn exam_classes:", error.message); process.exit(1); }
  console.log(`Đã chèn ${rows.length} dòng exam_classes (${gan.length - rows.length} dòng đã có sẵn).`);
}
if (an.length) {
  const { error } = await sb.from("exams").update({ published: false }).in("id", an);
  if (error) { console.error("Lỗi ẩn đề:", error.message); process.exit(1); }
  console.log(`Đã ẩn ${an.length} đề.`);
}
console.log("Sao lưu:", bak);
