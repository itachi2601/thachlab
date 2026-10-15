// Gieo dữ liệu thử cho HS Test 1/2: 1 danh hiệu (mùa đang chạy của lớp 12) + 1 mục phụ đạo (note='TEST-SEED').
// Chạy:  node --env-file=.env.local scripts/gieo-hs-test.mjs        (gieo)
//        node --env-file=.env.local scripts/gieo-hs-test.mjs --xoa  (dọn mọi dòng của 2 HS test)
import { createClient } from "@supabase/supabase-js";

const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY, { auth: { persistSession: false } });
const EMAILS = ["hs.test1@thachlab.local", "hs.test2@thachlab.local"];
const CLASS_ID = 18;
const MARK = "TEST-SEED";

const { data: profs } = await sb.from("profiles").select("id,full_name").in("full_name", ["HS Test 1", "HS Test 2"]);
const ids = (profs ?? []).map((p) => p.id);
if (ids.length !== 2) { console.error("Không thấy đủ 2 HS test — chạy tao-hs-test.mjs trước"); process.exit(1); }
const [hs1] = (profs ?? []).filter((p) => p.full_name === "HS Test 1");
const step = async (label, q) => { const { data, error } = await q; console.log(error ? `! ${label}: ${error.message}` : `ok ${label}`, error ? "" : (data?.length ?? "")); return data; };

if (process.argv.includes("--xoa")) {
  await step("xoá theory reviews", sb.from("tutoring_theory_reviews").delete().in("student_id", ids).select("tutoring_need_id"));
  await step("xoá exit attempts", sb.from("tutoring_exit_attempts").delete().in("student_id", ids).select("id"));
  await step("xoá registrations", sb.from("tutoring_registrations").delete().in("student_id", ids).select("id"));
  await step("xoá needs", sb.from("tutoring_needs").delete().in("student_id", ids).select("id"));
  await step("xoá awards", sb.from("rank_title_awards").delete().in("student_id", ids).select("id"));
  process.exit(0);
}

const { data: season } = await sb.from("rank_seasons").select("id,class_ids").eq("status", "active").contains("class_ids", [CLASS_ID]).order("id", { ascending: false }).limit(1).maybeSingle();
if (!season) { console.error("Không có mùa active cho lớp 12"); process.exit(1); }

// Danh hiệu: lấy 1 danh hiệu chuyên môn đang bật
const { data: title } = await sb.from("rank_titles").select("code,name").eq("enabled", true).eq("kind", "specialist").order("sort").limit(1).maybeSingle();
console.log("Danh hiệu:", title?.name, "| mùa:", season.id);
if (title) await step("gieo award thuc_tinh", sb.from("rank_title_awards").insert({ student_id: hs1.id, title_code: title.code, level: "thuc_tinh", season_id: season.id, evidence: { seed: MARK } }).select("id"));

// Mục phụ đạo: chủ đề "Sự chuyển thể"
const { data: topic } = await sb.from("question_topics").select("id,name").ilike("name", "Sự chuyển thể%").limit(1).maybeSingle();
console.log("Chủ đề phụ đạo:", topic?.name, topic?.id);
if (topic) await step("gieo need", sb.from("tutoring_needs").insert({ student_id: hs1.id, class_id: CLASS_ID, topic_id: topic.id, form: "bai_tap", wrong: 6, total: 10, pct: 40, source: "auto", status: "open", note: MARK }).select("id"));
