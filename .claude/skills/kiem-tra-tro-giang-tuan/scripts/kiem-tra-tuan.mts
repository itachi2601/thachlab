// Kiểm tiến trình trợ giảng theo tuần (Thứ Hai–Chủ nhật, giờ VN) từ ta_sessions và soạn thông báo nhắc nhẹ.
// Mặc định DRY-RUN (chỉ đọc). CHẠY TRÊN MAC (cần service role trong .env.local).
//   npx tsx .claude/skills/kiem-tra-tro-giang-tuan/scripts/kiem-tra-tuan.mts [--tuan YYYY-MM-DD] [--yes] [--json]
//   --tuan  một ngày bất kỳ trong tuần cần kiểm (mặc định: hôm nay, giờ VN)
//   --yes   gửi thật: ghi notifications + ta_reminders (mỗi trợ giảng tối đa 1 lần/tuần, chạy lại không gửi trùng)
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const yes = process.argv.includes("--yes");
const asJson = process.argv.includes("--json");
const argTuan = process.argv.includes("--tuan") ? process.argv[process.argv.indexOf("--tuan") + 1] : undefined;

function envLocal(key: string): string | undefined {
  const line = fs.readFileSync(path.join(root, ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}
const sb = createClient(envLocal("NEXT_PUBLIC_SUPABASE_URL")!, envLocal("SUPABASE_SERVICE_ROLE_KEY")!);

// ---------- tuần ----------
const vnToday = new Date(new Date().toLocaleString("en-US", { timeZone: "Asia/Ho_Chi_Minh" }));
const iso = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
function mondayOf(d: Date) { const x = new Date(d); x.setDate(x.getDate() - ((x.getDay() + 6) % 7)); x.setHours(0, 0, 0, 0); return x; }
const base = argTuan ? new Date(`${argTuan}T00:00:00`) : vnToday;
const mon = mondayOf(base);
const sun = new Date(mon); sun.setDate(sun.getDate() + 6);
const weekStart = iso(mon), weekEnd = iso(sun);
const prevWeeks = [1, 2].map((k) => { const d = new Date(mon); d.setDate(d.getDate() - 7 * k); return iso(d); });
const label = `${String(mon.getDate()).padStart(2, "0")}/${String(mon.getMonth() + 1).padStart(2, "0")}–${String(sun.getDate()).padStart(2, "0")}/${String(sun.getMonth() + 1).padStart(2, "0")}`;

// ---------- dữ liệu ----------
type Item = { code: string; text: string };
const { data: assistants, error: ea } = await sb.from("ta_assistants").select("id,user_id,full_name,short_name,started_at").eq("active", true);
if (ea) throw ea;
const { data: sessions, error: es } = await sb.from("ta_sessions")
  .select("id,assistant_id,work_date,session_type,class_label,student_touches,status,reject_reason,policy,phudao_students")
  .gte("work_date", weekStart).lte("work_date", weekEnd);
if (es) throw es;
const { data: links } = await sb.from("ta_assistant_classes").select("assistant_id");
const hasClass = new Set((links ?? []).map((l) => l.assistant_id as string));
const { data: stale } = await sb.from("ta_sessions").select("assistant_id,work_date").eq("status", "rejected").lt("work_date", weekStart);
const { data: needs } = await sb.from("tutoring_needs").select("assigned_to,first_seen_at,status").eq("status", "assigned");

let history: { assistant_id: string; week_start: string; level: number }[] = [];
let tableOk = true;
{
  const { data, error } = await sb.from("ta_reminders").select("assistant_id,week_start,level").in("week_start", [weekStart, ...prevWeeks]);
  if (error) { tableOk = false; console.warn(`! chưa có bảng ta_reminders (${error.message}) — chạy migration 20261011170000 trước khi gửi thật.`); }
  else history = data as typeof history;
}

const TARGET_TOUCH = 12; // quy chế: 12 lượt/buổi
const lessonNote = (v: unknown) => v === false;

// ---------- chấm từng người ----------
const out: any[] = [];
for (const a of assistants ?? []) {
  const mine = (sessions ?? []).filter((s) => s.assistant_id === a.id);
  const lop = mine.filter((s) => s.session_type === "lop" && s.status !== "rejected");
  const pd = mine.filter((s) => s.session_type === "phudao" && s.status !== "rejected");
  const items: Item[] = [];
  const add = (code: string, text: string) => items.push({ code, text });

  if (new Date(`${weekStart}T00:00:00`) < new Date(a.started_at ?? "1970-01-01")) continue; // chưa vào làm
  if (!mine.length && hasClass.has(a.id)) add("chua_ghi_buoi", "Tuần này con chưa ghi buổi nào. Nếu có lên lớp thì ghi bù phiếu buổi; nếu nghỉ thì nhắn thầy biết.");
  const rej = mine.filter((s) => s.status === "rejected").length + (stale ?? []).filter((s) => s.assistant_id === a.id).length;
  if (rej) add("phieu_tra_ve", `Có ${rej} phiếu thầy trả về, con vào sửa lại giúp thầy.`);
  if (lop.length) {
    const avg = lop.reduce((n, s) => n + Math.min(1, (s.student_touches ?? 0) / TARGET_TOUCH), 0) / lop.length;
    if (avg < 0.7) add("it_tiep_xuc", `Số lượt con đến hỏi từng em còn thấp so với mục tiêu ${TARGET_TOUCH} lượt/buổi. Buổi tới con đi vòng thêm các bàn nhé.`);
    const miss = (k: string, t: string) => { const n = lop.filter((s) => lessonNote((s.policy as any)?.[k])).length; if (n) add(k, `${t} (${n}/${lop.length} buổi chưa làm).`); };
    miss("arrived_early", "Con đến sớm trước giờ học để chuẩn bị");
    miss("homework_checked", "Con kiểm tra bài tập về nhà đầu buổi");
    miss("walked_tables", "Con đi vòng các bàn trong giờ làm bài");
    miss("reported_students", "Con báo thầy những em cần chú ý sau buổi");
    const late = lop.filter((s) => ["late", "unexcused_absence"].includes((s.policy as any)?.attendance)).length;
    if (late) add("chuyen_can", `Có ${late} buổi con đi trễ hoặc vắng không báo trước. Có việc gì thì con báo thầy sớm.`);
  }
  if (hasClass.has(a.id) && !pd.length) add("chua_phu_dao", "Tuần này chưa có buổi phụ đạo nào. Các em yếu rất cần con, con sắp xếp một buổi nhé.");
  for (const k of ["prepared", "recalled", "asked_each"] as const) {
    const n = pd.filter((s) => lessonNote((s.policy as any)?.[k])).length;
    if (n) add(`pd_${k}`, ({ prepared: "Con chuẩn bị bài trước khi phụ đạo", recalled: "Con cho em nhắc lại kiến thức cũ trước khi giảng", asked_each: "Con hỏi lại từng em để chắc là em hiểu" } as const)[k] + ` (${n}/${pd.length} buổi chưa làm).`);
  }
  const wait = (needs ?? []).filter((n) => n.assigned_to === a.user_id && Date.now() - +new Date(n.first_seen_at) > 14 * 864e5).length;
  if (wait) add("em_cho_phu_dao", `Có ${wait} em đã được giao cho con từ hơn 2 tuần mà chưa được phụ đạo.`);

  // lịch sử → mức nhắc
  const had = (w: string) => history.some((h) => h.assistant_id === a.id && h.week_start === w);
  const streak = had(prevWeeks[0]) ? (had(prevWeeks[1]) ? 2 : 1) : 0;
  const level = Math.min(3, 1 + streak);
  const already = history.some((h) => h.assistant_id === a.id && h.week_start === weekStart);
  out.push({ assistant_id: a.id, user_id: a.user_id, name: a.short_name || a.full_name, buoi: mine.length, items, level, already });
}

// ---------- soạn lời nhắc (giọng thầy gọi "con", xưng "thầy"; xem references/giong-nhac.md) ----------
function compose(o: any): { title: string; body: string } {
  const lines = o.items.map((i: Item) => `• ${i.text}`);
  const open = o.level === 1
    ? `Con ${o.name} ơi, thầy xem lại tuần ${label}, còn mấy việc thầy nhắc con:`
    : o.level === 2
      ? `Con ${o.name} ơi, tuần ${label} còn mấy việc giống tuần trước, thầy nhắc lại:`
      : `Con ${o.name} ơi, đã 3 tuần liền thầy nhắc những việc này. Thầy muốn gặp con nói chuyện:`;
  const close = o.level === 1
    ? "Mỗi việc nhỏ này đều ảnh hưởng đến các em. Con cố gắng nhé, thầy tin con."
    : o.level === 2
      ? "Thầy hỏi thật: con đang gặp khó ở chỗ nào? Nhắn thầy, mình cùng gỡ. Các em đang trông vào con."
      : "Làm trợ giảng không chỉ vì lương mà vì tương lai của các em. Nếu con thấy chưa đủ thời gian hay tâm sức thì nói thẳng với thầy, mình bàn cách phù hợp nhất.";
  return { title: `Thầy nhắc nhẹ tuần ${label}`, body: [open, ...lines, close].join("\n") };
}

const todo = out.filter((o) => o.items.length && !o.already);
for (const o of todo) Object.assign(o, compose(o));

// ---------- báo cáo ----------
const report = { tuan: weekStart, den: weekEnd, tong: out.length, du_viec: out.filter((o) => !o.items.length).map((o) => o.name), da_nhac_roi: out.filter((o) => o.already).map((o) => o.name), can_nhac: todo };
fs.mkdirSync(path.join(root, "scripts/logs"), { recursive: true });
fs.writeFileSync(path.join(root, `scripts/logs/ta-nhac-${weekStart}.json`), JSON.stringify(report, null, 2));
if (asJson) console.log(JSON.stringify(report, null, 2));
else {
  console.log(`Tuần ${label} (${weekStart}): ${out.length} trợ giảng — ${report.du_viec.length} đủ việc, ${todo.length} cần nhắc, ${report.da_nhac_roi.length} đã nhắc rồi.`);
  if (report.du_viec.length) console.log(`✓ Đủ việc: ${report.du_viec.join(", ")}`);
  for (const o of todo) console.log(`\n--- ${o.name} · ${o.buoi} buổi · mức ${o.level}${o.user_id ? "" : " · THIẾU user_id, không gửi được"}\n${o.title}\n${o.body}`);
}

// ---------- gửi thật ----------
if (!yes) { console.log(`\n○ DRY-RUN — chưa gửi gì. Gửi thật: thêm --yes${argTuan ? ` --tuan ${argTuan}` : ""}`); process.exit(0); }
if (!tableOk) throw new Error("Chưa có bảng ta_reminders — chạy migration trước.");
for (const o of todo) {
  if (!o.user_id) { console.log(`! bỏ qua ${o.name}: chưa gắn tài khoản`); continue; }
  const { data: n, error: en } = await sb.from("notifications").insert({ user_id: o.user_id, kind: "ta_nhac_viec", title: o.title, body: o.body, href: "/tro-giang" }).select("id").single();
  if (en) { console.log(`✗ ${o.name}: ${en.message}`); continue; }
  const { error: er } = await sb.from("ta_reminders").insert({ assistant_id: o.assistant_id, week_start: weekStart, level: o.level, items: o.items, title: o.title, body: o.body, notification_id: n.id });
  if (er) { await sb.from("notifications").delete().eq("id", n.id); console.log(`✗ ${o.name}: ${er.message} (đã hoàn tác thông báo)`); continue; }
  console.log(`→ đã gửi ${o.name}`);
}
