// Lưu trữ tài khoản HS bị bỏ (em không đăng nhập lại được nên đã có tài khoản mới) — KHÔNG xoá gì.
//   npx tsx scripts/luu-tru-tai-khoan-bo.mts <tai-khoan-bo-*.json>                 # dry-run: in danh sách sẽ lưu trữ
//   npx tsx scripts/luu-tru-tai-khoan-bo.mts <file.json> --apply [--bo-id=<uuid>,…]  # sao lưu rồi ghi
//   npx tsx scripts/luu-tru-tai-khoan-bo.mts --undo <scripts/logs/luu-tru-backup-*.json>
// Lưu trữ = user_classes.status 'active' -> 'archived' (mọi danh sách/sweep chỉ xét 'active' nên tự loại em ra),
// và đóng cảnh báo đang mở của tài khoản đó. Dữ liệu học (điểm, bài làm) giữ nguyên, hoàn tác bằng --undo.
// Chỉ lấy ca chắc: tài khoản mới đã từng đăng nhập, tài khoản cũ không đăng nhập sau khi tài khoản mới được tạo.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const env = (k: string) => fs.readFileSync(path.resolve(scriptDir, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const args = process.argv.slice(2);
const APPLY = args.includes("--apply");
const stamp = new Date().toISOString().replace(/[:.]/g, "-");

const undoAt = args.indexOf("--undo");
if (undoAt >= 0) {
  const b = JSON.parse(fs.readFileSync(args[undoAt + 1], "utf8"));
  for (const r of b.user_classes) {
    const { error } = await sb.from("user_classes").update({ status: r.status }).eq("user_id", r.user_id).eq("class_id", r.class_id);
    if (error) throw error;
  }
  for (const a of b.alerts) {
    const { error } = await sb.from("student_alerts").update({ status: a.status, handled_note: a.handled_note ?? "" }).eq("id", a.id);
    if (error) throw error;
  }
  console.log(`Đã trả ${b.user_classes.length} dòng lớp và ${b.alerts.length} cảnh báo.`);
  process.exit(0);
}

const file = args.find((a) => a.endsWith(".json"))!;
const skip = new Set((args.find((a) => a.startsWith("--bo-id="))?.slice(8) ?? "").split(",").filter(Boolean));
const { abandoned } = JSON.parse(fs.readFileSync(file, "utf8")) as { abandoned: any[] };
const sure = abandoned.filter((o) => o.newer_last_sign_in && (!o.last_sign_in || o.last_sign_in < o.newer_created) && !skip.has(o.id));
console.log(`Ca chắc: ${sure.length}/${abandoned.length} (bỏ ${abandoned.length - sure.length} ca tài khoản cũ còn dùng hoặc tài khoản mới chưa đăng nhập).`);

const ids = sure.map((o) => o.id);
const { data: ucs, error: e1 } = await sb.from("user_classes").select("user_id,class_id,status").in("user_id", ids).eq("status", "active");
if (e1) throw e1;
const { data: als, error: e2 } = await sb.from("student_alerts").select("id,status,handled_note").in("student_id", ids).eq("status", "open");
if (e2) throw e2;
const nameOf = new Map(sure.map((o) => [o.id, `${o.name} <${o.email}>`]));
for (const o of sure) console.log(`- ${nameOf.get(o.id)} → giữ ${o.newer_email}`);
console.log(`Dòng lớp sẽ lưu trữ: ${ucs!.length} · cảnh báo mở sẽ đóng: ${als!.length}`);

if (!APPLY) { console.log("Dry-run. Thêm --apply để ghi."); process.exit(0); }

const backup = path.join(scriptDir, "logs", `luu-tru-backup-${stamp}.json`);
fs.writeFileSync(backup, JSON.stringify({ user_classes: ucs, alerts: als }, null, 2));
for (const r of ucs!) {
  const { error } = await sb.from("user_classes").update({ status: "archived" }).eq("user_id", r.user_id).eq("class_id", r.class_id);
  if (error) { console.error("Lỗi (có thể do CHECK status):", error.message); process.exit(1); }
}
if (als!.length) {
  const { error } = await sb.from("student_alerts").update({ status: "resolved", handled_note: "tự đóng: tài khoản cũ đã lưu trữ (em dùng tài khoản mới)" }).in("id", als!.map((a) => a.id));
  if (error) throw error;
}
console.log(`Đã ghi. Sao lưu: ${backup}\nHoàn tác: npx tsx scripts/luu-tru-tai-khoan-bo.mts --undo ${backup}`);
