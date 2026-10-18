// Dọn cảnh báo giả trong student_alerts (đánh dấu "Bỏ qua" = dismissed, KHÔNG xoá).
//   npx tsx scripts/don-canh-bao-gia.mts --dry-run   # (mặc định) in số đếm theo nguyên nhân, ghi báo cáo scripts/logs/
//   npx tsx scripts/don-canh-bao-gia.mts --apply     # sao lưu dòng sẽ đổi ra scripts/logs/, rồi đánh dấu dismissed
//   npx tsx scripts/don-canh-bao-gia.mts --undo <file-backup>   # trả status cũ
// Cảnh báo giả (chỉ xét status='open'):
//   tai_khoan_khong_phai_hs  — người nhận không phải role student (admin/giáo viên/trợ giảng)
//   tai_khoan_thu            — profiles.is_test, hoặc (khi chưa chạy migration) email hs.test% / tên có test|anonymus
//   chua_toi_han             — missed_assessment mà KHÔNG đề nào quá hạn / đủ >=50% lớp nộp (luật mới), hoặc em đã nộp hết
// Chạy SAU migration 20261018170000 để có cột is_test/due_at; chưa có thì script tự dùng luật dự phòng và báo rõ.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const env = (k: string) => fs.readFileSync(path.resolve(scriptDir, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");
const undoIdx = process.argv.indexOf("--undo");
const logs = path.join(scriptDir, "logs");
fs.mkdirSync(logs, { recursive: true });
const stamp = new Date().toISOString().replace(/[:.]/g, "-");

async function pageAll<T>(q: (from: number, to: number) => PromiseLike<{ data: T[] | null; error: any }>): Promise<T[]> {
  const out: T[] = [];
  for (let from = 0; ; from += 1000) {
    const { data, error } = await q(from, from + 999);
    if (error) throw error;
    out.push(...(data ?? []));
    if (!data || data.length < 1000) break;
  }
  return out;
}

if (undoIdx >= 0) {
  const rows = JSON.parse(fs.readFileSync(process.argv[undoIdx + 1], "utf8")) as { id: number; status: string; handled_note: string | null }[];
  for (const r of rows) {
    const { error } = await sb.from("student_alerts").update({ status: r.status, handled_note: r.handled_note ?? "" }).eq("id", r.id);
    if (error) throw error;
  }
  console.log(`Đã trả lại ${rows.length} cảnh báo.`);
  process.exit(0);
}

type Alert = { id: number; student_id: string; class_id: number | null; kind: string; status: string; reason: string; handled_note: string | null; assessment_ids: number[] | null };
const alerts = await pageAll<Alert>((a, b) =>
  sb.from("student_alerts").select("id,student_id,class_id,kind,status,reason,handled_note,assessment_ids").eq("status", "open").range(a, b));

// hồ sơ người nhận
const studentIds = [...new Set(alerts.map((a) => a.student_id))];
let hasIsTest = true;
const probe = await sb.from("profiles").select("is_test").limit(1);
if (probe.error) hasIsTest = false;
const profCols = "id,full_name,role" + (hasIsTest ? ",is_test" : "");
const profs = new Map<string, any>();
for (let i = 0; i < studentIds.length; i += 200) {
  const { data, error } = await sb.from("profiles").select(profCols).in("id", studentIds.slice(i, i + 200));
  if (error) throw error;
  for (const p of data ?? []) profs.set((p as any).id, p);
}
const emails = new Map<string, string>();
for (let page = 1; ; page++) {
  const { data, error } = await sb.auth.admin.listUsers({ page, perPage: 1000 });
  if (error) throw error;
  for (const u of data.users) emails.set(u.id, u.email ?? "");
  if (data.users.length < 1000) break;
}
const isTest = (id: string) => {
  const p = profs.get(id);
  if (hasIsTest) return !!p?.is_test;
  return /^hs\.test.*@thachlab\.local$/.test(emails.get(id) ?? "") || /\b(test|anonymus)\b/i.test(p?.full_name ?? "");
};

// luật mới cho missed_assessment
let hasDue = true;
if ((await sb.from("class_assessments").select("due_at").limit(1)).error) hasDue = false;
const asm = await pageAll<any>((a, b) => sb.from("class_assessments").select("id,class_id,exam_id" + (hasDue ? ",due_at" : "")).range(a, b));
const asmById = new Map(asm.map((x: any) => [x.id, x]));
const members = await pageAll<{ class_id: number; user_id: string }>((a, b) => sb.from("user_classes").select("class_id,user_id").eq("status", "active").range(a, b));
const memberProfs = new Map<string, any>();
const allMemberIds = [...new Set(members.map((m) => m.user_id))];
for (let i = 0; i < allMemberIds.length; i += 200) {
  const { data } = await sb.from("profiles").select(profCols).in("id", allMemberIds.slice(i, i + 200));
  for (const p of data ?? []) memberProfs.set((p as any).id, p);
}
const isRealStudent = (id: string) => {
  const p = memberProfs.get(id) ?? profs.get(id);
  if (!p || p.role !== "student") return false;
  return hasIsTest ? !p.is_test : !(/^hs\.test.*@thachlab\.local$/.test(emails.get(id) ?? "") || /\b(test|anonymus)\b/i.test(p.full_name ?? ""));
};
const results = await pageAll<{ student_id: string; exam_id: number }>((a, b) => sb.from("exam_results").select("student_id,exam_id").in("exam_id", [...new Set(asm.map((x: any) => x.exam_id))]).range(a, b));
const doneBy = new Map<number, Set<string>>();
for (const r of results) (doneBy.get(r.exam_id) ?? doneBy.set(r.exam_id, new Set()).get(r.exam_id)!).add(r.student_id);
const realByClass = new Map<number, string[]>();
for (const m of members) if (isRealStudent(m.user_id)) (realByClass.get(m.class_id) ?? realByClass.set(m.class_id, []).get(m.class_id)!).push(m.user_id);
const now = Date.now();
function assessmentDue(a: any): boolean {
  if (a.due_at) return new Date(a.due_at).getTime() < now;
  const real = realByClass.get(a.class_id) ?? [];
  if (!real.length) return false;
  const done = real.filter((id) => doneBy.get(a.exam_id)?.has(id)).length;
  return done / real.length >= 0.5;
}

const counts = new Map<string, number>();
const toDismiss: { alert: Alert; cause: string }[] = [];
for (const a of alerts) {
  let cause: string | null = null;
  const p = profs.get(a.student_id);
  if (p && p.role !== "student") cause = "tai_khoan_khong_phai_hs";
  else if (isTest(a.student_id)) cause = "tai_khoan_thu";
  else if (a.kind === "missed_assessment") {
    const missing = (a.assessment_ids ?? []).map((id) => asmById.get(id)).filter(Boolean)
      .filter((x: any) => !doneBy.get(x.exam_id)?.has(a.student_id));
    if (!missing.some(assessmentDue)) cause = "chua_toi_han";
  }
  if (cause) { toDismiss.push({ alert: a, cause }); counts.set(cause, (counts.get(cause) ?? 0) + 1); }
}

console.log(`Cột is_test: ${hasIsTest ? "có" : "CHƯA (dùng luật dự phòng email/tên)"} · cột due_at: ${hasDue ? "có" : "CHƯA (chỉ dùng luật >=50% lớp nộp)"}`);
console.log(`Cảnh báo đang mở: ${alerts.length}`);
const byKind = new Map<string, number>();
for (const a of alerts) byKind.set(a.kind, (byKind.get(a.kind) ?? 0) + 1);
console.log("  theo loại:", Object.fromEntries(byKind));
console.log("Cảnh báo giả theo nguyên nhân:", Object.fromEntries(counts), `→ tổng ${toDismiss.length}, giữ ${alerts.length - toDismiss.length}`);
const sample = toDismiss.filter((x) => x.cause !== "chua_toi_han").slice(0, 8).map((x) => `${profs.get(x.alert.student_id)?.full_name} (${x.cause})`);
if (sample.length) console.log("Mẫu tài khoản bị loại:", sample.join("; "));

const report = path.join(logs, `don-canh-bao-gia-${stamp}.${APPLY ? "backup" : "dryrun"}.json`);
const backupRows = toDismiss.map((x) => ({ id: x.alert.id, status: x.alert.status, handled_note: x.alert.handled_note, cause: x.cause, student: profs.get(x.alert.student_id)?.full_name }));
fs.writeFileSync(report, JSON.stringify(backupRows, null, 1));
console.log(`Ghi ${APPLY ? "sao lưu" : "báo cáo"}: ${report}`);

if (!APPLY) { console.log("DRY-RUN: chưa ghi gì. Thêm --apply để đánh dấu Bỏ qua."); process.exit(0); }
let n = 0;
for (const { alert, cause } of toDismiss) {
  const { error } = await sb.from("student_alerts").update({ status: "dismissed", handled_note: `dọn tự động: ${cause}`, updated_at: new Date().toISOString() }).eq("id", alert.id).eq("status", "open");
  if (error) throw error;
  n++;
}
console.log(`Đã đánh dấu Bỏ qua ${n} cảnh báo. Hoàn tác: npx tsx scripts/don-canh-bao-gia.mts --undo ${report}`);
