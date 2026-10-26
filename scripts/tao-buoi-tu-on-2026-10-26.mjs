// Tạo các buổi "Tự ôn ở nhà" (review_sessions mode='self') cho L10 Ch.1+2, L11 Ch.1, L12 Ch.1+2
// và đăng một thông báo lớp (class_announcements kind='homework' → trigger sinh chuông cho em + phụ huynh).
// Mặc định DRY-RUN; thêm --yes để ghi thật. Chạy lại an toàn: buổi/thông báo đã có thì bỏ qua.
//   node scripts/tao-buoi-tu-on-2026-10-26.mjs [--yes]
import fs from "node:fs";

const yes = process.argv.includes("--yes");
const env = Object.fromEntries(
  fs.readFileSync(new URL("../.env.local", import.meta.url), "utf8")
    .split("\n").filter((l) => l.includes("=") && !l.startsWith("#"))
    .map((l) => [l.slice(0, l.indexOf("=")), l.slice(l.indexOf("=") + 1).trim().replace(/^"|"$/g, "")]),
);
const U = env.NEXT_PUBLIC_SUPABASE_URL, K = env.SUPABASE_SERVICE_ROLE_KEY;
const H = { apikey: K, Authorization: `Bearer ${K}`, "Content-Type": "application/json" };
const get = async (p) => { const r = await fetch(`${U}/rest/v1/${p}`, { headers: H }); if (!r.ok) throw new Error(`${p}: ${await r.text()}`); return r.json(); };
const post = async (t, row) => { const r = await fetch(`${U}/rest/v1/${t}`, { method: "POST", headers: { ...H, Prefer: "return=representation" }, body: JSON.stringify(row) }); if (!r.ok) throw new Error(`${t}: ${await r.text()}`); return (await r.json())[0]; };

const DUE = "2026-11-01T21:00:00+07:00";
const DUE_TEXT = "21:00 Chủ nhật 1/11";
const THRESHOLD = 80;
// lớp → [{ chapter id, nhãn }]
const PLAN = [
  { classId: 16, mon: "Vật lí 10", chapters: [{ id: 10, nhan: "Chương 1: Mở đầu" }, { id: 11, nhan: "Chương 2: Động học" }] },
  { classId: 17, mon: "Vật lí 11", chapters: [{ id: 6, nhan: "Chương 1: Dao động" }] },
  { classId: 18, mon: "Vật lí 12", chapters: [{ id: 2, nhan: "Chương 1: Vật lí nhiệt" }, { id: 3, nhan: "Chương 2: Khí lí tưởng" }] },
];

const [admin] = await get("profiles?select=id&role=eq.admin&order=created_at&limit=1");
if (!admin) throw new Error("không tìm thấy admin làm created_by");

for (const cls of PLAN) {
  const made = [];
  for (const ch of cls.chapters) {
    const lessons = await get(`lessons?select=id,title&chapter_id=eq.${ch.id}&order=sort_order,id`);
    const items = await get(`lesson_items?select=id,lesson_id,exam_ids&kind=eq.ly_thuyet&lesson_id=in.(${lessons.map((l) => l.id).join(",")})&order=sort_order`);
    const examIds = [...new Set(items.flatMap((i) => i.exam_ids ?? []))];
    const exams = new Map((await get(`exams?select=id,title,question_count,published&id=in.(${examIds.join(",")})`)).map((e) => [e.id, e]));
    const stages = [];
    for (const l of lessons) {
      for (const it of items.filter((i) => i.lesson_id === l.id)) {
        for (const id of it.exam_ids ?? []) {
          const e = exams.get(id);
          if (!e || !e.published) { console.log(`  ! bỏ đề ${id} (chưa công bố hoặc không có)`); continue; }
          stages.push({ exam_id: id, item_id: it.id, title: l.title, minutes: Math.max(5, Math.round(e.question_count * 0.6)) });
        }
      }
    }
    const title = `Tự ôn ở nhà — ${ch.nhan}`;
    console.log(`\n[${cls.mon}] ${title}: ${stages.length} chặng, ngưỡng ${THRESHOLD}%, hạn ${DUE_TEXT}`);
    stages.forEach((s, i) => console.log(`   ${i + 1}. ${s.title} (đề ${s.exam_id})`));
    if (stages.length < 1 || stages.length > 12) throw new Error("số chặng ngoài 1..12");
    made.push({ ch, n: stages.length });
    const dup = await get(`review_sessions?select=id&class_id=eq.${cls.classId}&title=eq.${encodeURIComponent(title)}`);
    if (dup.length) { console.log(`   (đã có buổi #${dup[0].id}, bỏ qua)`); continue; }
    if (!yes) continue;
    const row = await post("review_sessions", {
      class_id: cls.classId, created_by: admin.id, title, threshold: THRESHOLD, stages, mode: "self",
      due_at: DUE, sequential: true, current_stage: stages.length - 1, stage_started_at: new Date().toISOString(), status: "running",
    });
    console.log(`   ✓ tạo buổi #${row.id}`);
  }

  const dong = made.map((m) => `${m.ch.nhan} (${m.n} chặng)`).join("; ");
  const body = `Tự ôn ở nhà · ${cls.mon}: ${dong} đã mở sẵn. Vào Lớp học, bấm thẻ Ôn tập ở đầu trang, làm lần lượt từng chặng. Mỗi chặng là một đề ngắn, đạt ${THRESHOLD}% thì mở chặng kế. Không tính giờ, em làm dần từng ngày cũng được. Hạn: ${DUE_TEXT}.`;
  const sent = await get(`class_announcements?select=id&class_id=eq.${cls.classId}&kind=eq.homework&body=like.${encodeURIComponent("Tự ôn ở nhà ·")}*`);
  console.log(`\nThông báo lớp ${cls.classId}:\n  ${body}`);
  if (sent.length) { console.log(`  (đã gửi #${sent[0].id}, bỏ qua)`); continue; }
  if (!yes) continue;
  const a = await post("class_announcements", { class_id: cls.classId, kind: "homework", body, created_by: admin.id });
  console.log(`  ✓ đã gửi thông báo #${a.id}`);
}
console.log(yes ? "\nXONG." : "\nDRY-RUN: thêm --yes để tạo thật.");
