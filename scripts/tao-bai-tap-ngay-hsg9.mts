// Tạo bộ "Bài tập mỗi ngày" Cơ học cho lớp HSG Vật lí 9 (class 19) từ content/hsg9/bai-tap-ngay-co-hoc/ngay-N.json.
// Mỗi ngày = 1 đề tự chấm (published=false tới 6:00 sáng ngày đó) + 1 chặng của buổi ôn tự học (review_sessions mode='self').
// Chặng mở theo giờ nhờ migration 20261028100000 (pg_cron gọi review_open_due_stages: bật đề + chuông cho cả lớp).
// Mặc định DRY-RUN. CHẠY TRÊN MAC sau khi migration đã chạy.
//   npx tsx scripts/tao-bai-tap-ngay-hsg9.mts          # xem trước
//   npx tsx scripts/tao-bai-tap-ngay-hsg9.mts --yes    # tạo thật
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import { validateBundle, bundleToRows, type LessonBundle } from "@/services/lesson-import";

const CLASS_ID = 19;
const DIR = "content/hsg9/bai-tap-ngay-co-hoc/";
const TITLE = "Bài tập mỗi ngày: Chuyển động, đồ thị, lực";
// Giờ mở từng ngày (ICT, +07:00). Ngày 1 mở ngay khi tạo.
const OPEN = ["now", "2026-10-30T06:00:00+07:00", "2026-11-01T06:00:00+07:00", "2026-11-02T06:00:00+07:00", "2026-11-03T06:00:00+07:00"];
const DUE = "2026-11-04T06:00:00+07:00";
const yes = process.argv.includes("--yes");

const env = Object.fromEntries(
  fs.readFileSync(".env.local", "utf8").split("\n").filter((l) => l.includes("=")).map((l) => [l.slice(0, l.indexOf("=")), l.slice(l.indexOf("=") + 1).trim()]),
);
const sb = createClient(env.NEXT_PUBLIC_SUPABASE_URL, env.SUPABASE_SERVICE_ROLE_KEY);

const days = OPEN.map((_, i) => JSON.parse(fs.readFileSync(`${DIR}ngay-${i + 1}.json`, "utf8")));
const built = days.map((d, i) => {
  const bundle: LessonBundle = {
    schema: "thachlab.lesson-bundle/v1",
    theory_html: "",
    worked_examples: [],
    exam: {
      title: `Ngày ${i + 1} · ${d.chu_de}`,
      topic: d.chu_de,
      difficulty: "kho",
      duration_minutes: 45,
      subject_code: "hsg-vat-ly",
      questions: d.questions,
    },
  };
  const chk = validateBundle(bundle);
  if (!chk.ok) throw new Error(`Ngày ${i + 1}: ${chk.errors.join("; ")}`);
  return { bundle, rows: bundleToRows(bundle, 0), warnings: chk.warnings };
});
for (const [i, b] of built.entries()) console.log(`Ngày ${i + 1}: ${b.rows.exam.title} · ${b.bundle.exam.questions.length} câu · mở ${OPEN[i]}`);
if (!yes) { console.log("DRY-RUN: thêm --yes để tạo."); process.exit(0); }

const { data: dup } = await sb.from("review_sessions").select("id").eq("class_id", CLASS_ID).eq("title", TITLE);
if (dup?.length) throw new Error(`đã có buổi #${dup[0].id}, không tạo lại`);

const stages: Record<string, unknown>[] = [];
for (const [i, b] of built.entries()) {
  const first = OPEN[i] === "now";
  const { data: ex, error } = await sb.from("exams").insert({ ...b.rows.exam, published: first }).select("id").single();
  if (error || !ex) throw new Error(`tạo đề ngày ${i + 1}: ${error?.message}`);
  await sb.from("exam_classes").insert({ exam_id: ex.id, class_id: CLASS_ID });
  stages.push({
    exam_id: ex.id, item_id: null, title: `Ngày ${i + 1} · ${days[i].chu_de}`, minutes: 45,
    brief: `4 bài · 30–45 phút · ${days[i].chu_de}`,
    ...(first ? { opened: true } : { open_at: new Date(OPEN[i]).toISOString() }),
  });
  console.log(`  ✓ ngày ${i + 1}: đề #${ex.id}`);
}
const { data: ses, error: e2 } = await sb.from("review_sessions").insert({
  class_id: CLASS_ID, title: TITLE, threshold: 1, stages, mode: "self", due_at: new Date(DUE).toISOString(), sequential: false,
  current_stage: stages.length - 1, stage_started_at: new Date().toISOString(), status: "running",
}).select("id").single();
if (e2 || !ses) throw new Error(`tạo buổi: ${e2?.message}`);
console.log(`✓ buổi tự học #${ses.id}`);

// Chuông cho cả lớp: bộ bài + ngày 1 mở ngay. Các ngày sau do pg_cron gửi lúc 6:00.
const { data: stu } = await sb.from("user_classes").select("user_id, profiles!inner(role)").eq("class_id", CLASS_ID).eq("status", "active");
const ids = (stu ?? []).filter((r: any) => r.profiles?.role === "student").map((r: any) => r.user_id as string);
for (const uid of ids) {
  const { error } = await sb.rpc("notify_user", {
    p_user: uid, p_kind: "review_self_new", p_title: "Bài tập mỗi ngày: Chuyển động, đồ thị, lực",
    p_body: "5 ngày, mỗi ngày 4 bài (30–45 phút). Ngày 1 đã mở. Vào làm và xem bạn nào đã nộp.", p_href: "/lop-hoc/on-tap/",
  });
  if (error) { console.log("notify_user lỗi:", error.message, "(kiểm tên tham số)"); break; }
}
console.log(`✓ chuông ${ids.length} em`);
