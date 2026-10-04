#!/usr/bin/env node
// Sinh bản tĩnh của học liệu công khai vào public/data/ để trang học sinh
// (/lop-hoc, /lop-hoc/bai, trang chủ HS) đọc từ cùng origin thay vì gọi Supabase
// (~100–150 ms mỗi round-trip lúc còn ở Sydney; nay Singapore) trước khi có nội dung. Chạy tự động trước
// mỗi lần build (prebuild trong package.json) — SAU KHI ĐĂNG/SỬA BÀI PHẢI BUILD LẠI.
//
//   public/data/manifest.json        — generatedAt + số lượng (rỗng nếu không lấy được dữ liệu)
//   public/data/catalog.json         — lớp → chương → bài (kèm mô tả/YCCĐ) + tham chiếu mục (id, exam_ids)
//   public/data/lessons/<id>.json    — 1 bài: lesson + tên chương + các mục; chỉ mục lý thuyết/video
//                                      có body_html; mục khác chỉ metadata (KHÔNG questions, KHÔNG đề)
//   public/data/home-stats.json      — số chương/bài/mục toàn site + theo từng lớp, cho trang chủ
//                                      (đọc LÚC BUILD trong app/(public)/page.tsx — không gọi Supabase khi tải).
//                                      Kèm 3 số thật của cả site: students (profiles.role='student'),
//                                      attempts (exam_results — mỗi dòng là một bài đã chấm),
//                                      questions (question_bank chưa archive). Ba bảng này khoá RLS với
//                                      anon nên chỉ đếm được khi có SUPABASE_SERVICE_ROLE_KEY; thiếu khoá
//                                      thì để null (trang chủ tự ẩn số), KHÔNG ghi 0 vì 0 là số sai.
//
// Chỉ dùng ANON key (đúng RLS của khách chưa đăng nhập) — file tĩnh không bao giờ
// chứa thứ mà người chưa đăng nhập không xem được. Đề thi (exams.questions, có đáp án)
// và lời giải bài tập mẫu (lesson_items.questions) TUYỆT ĐỐI không đưa vào đây.
//
// Không làm fail build: thiếu env / Supabase lỗi → in cảnh báo, giữ file cũ nếu có,
// không có thì ghi manifest rỗng; client tự lùi về gọi Supabase như cũ.
import { existsSync, mkdirSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const OUT_DIR = join(ROOT, "public", "data");
const LESSONS_DIR = join(OUT_DIR, "lessons");
const ENV_FILE = join(ROOT, ".env.local");

// Cột của lesson_items theo từng đợt migration — giống ITEM_COLUMNS_V3/V2/V1 ở services/lessons.ts.
const ITEM_META_V1 = "id, lesson_id, kind, title, subtitle, video_url, pdf_url, exam_ids, sort_order";
const ITEM_META_V2 = `${ITEM_META_V1}, due_at`;
const ITEM_META_V3 = `${ITEM_META_V2}, required, quiz_min_correct, practice_pass_score`;
// published_at là migration mới (nháp → đăng chính thức từng mục, cột
// docs/supabase-migration-lesson-item-draft-publish.sql) — mục null (chưa từng đăng)
// TUYỆT ĐỐI không được vào file tĩnh, dù trang admin có thể vẫn đang sửa dở.
const ITEM_META_V4 = `${ITEM_META_V3}, published_at`;
// summary_html là migration mới nhất ("Tóm tắt ý chính cần thuộc",
// supabase/migrations/20260927120000_lesson_item_summary.sql) — cùng nhóm với
// body_html (chỉ mục ly_thuyet/video mới cần), nhưng cần lùi phiên bản riêng vì
// có thể migration đó chưa chạy dù published_at đã có từ trước.
const ITEM_META_V5 = `${ITEM_META_V4}, summary_html`;
// Loại mục được đưa body_html vào file tĩnh (không có lời giải/đáp án).
const BODY_KINDS = new Set(["ly_thuyet", "video"]);

function warn(msg) {
  console.warn(`[build-content] ⚠ ${msg}`);
}

function loadEnv() {
  if (existsSync(ENV_FILE)) {
    try {
      process.loadEnvFile(ENV_FILE);
    } catch (e) {
      warn(`không đọc được .env.local: ${e.message}`);
    }
  }
  return {
    url: process.env.NEXT_PUBLIC_SUPABASE_URL,
    anonKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
    serviceKey: process.env.SUPABASE_SERVICE_ROLE_KEY,
  };
}

function writeJson(path, value) {
  writeFileSync(path, JSON.stringify(value));
}

function hasOldData() {
  return existsSync(join(OUT_DIR, "catalog.json"));
}

/** Không lấy được dữ liệu: giữ bản cũ nếu có, không thì ghi manifest rỗng. */
function bail(reason) {
  warn(reason);
  mkdirSync(OUT_DIR, { recursive: true });
  if (hasOldData()) {
    warn("giữ nguyên public/data/ của lần build trước.");
    return;
  }
  writeJson(join(OUT_DIR, "manifest.json"), { generatedAt: null, lessons: 0, error: reason });
  warn("ghi manifest rỗng — trang học sinh sẽ gọi Supabase như cũ.");
}

/** Lấy hết dòng của 1 truy vấn, mỗi trang 1000 dòng (giới hạn mặc định của PostgREST). */
async function fetchAll(makeQuery) {
  const PAGE = 1000;
  const rows = [];
  for (let from = 0; ; from += PAGE) {
    const { data, error } = await makeQuery().range(from, from + PAGE - 1);
    if (error) throw error;
    rows.push(...(data ?? []));
    if (!data || data.length < PAGE) return rows;
  }
}

/**
 * Đếm số liệu thật của cả site cho dải tổng trang chủ (build-time, KHÔNG phải request lúc tải trang).
 *
 * profiles / exam_results / question_bank đều chỉ cho authenticated đọc (xem
 * supabase/migrations/20260925140000_perf_rls.sql) nên anon key luôn đếm ra 0 → phải dùng
 * service role. Không có khoá (máy khác, CI không cấu hình) → trả null cho từng số, trang chủ
 * tự ẩn; TUYỆT ĐỐI không ghi 0 thay cho "không biết" vì 0 cũng là một con số trông như thật.
 */
async function fetchSiteCounts(url, serviceKey) {
  const counts = { students: null, attempts: null, questions: null };
  if (!serviceKey) {
    warn(
      "thiếu SUPABASE_SERVICE_ROLE_KEY — home-stats.json để trống students/attempts/questions " +
        "(RLS chặn anon đọc profiles/exam_results/question_bank).",
    );
    return counts;
  }
  const { createClient } = await import("@supabase/supabase-js");
  const admin = createClient(url, serviceKey, { auth: { persistSession: false } });
  const targets = [
    ["students", "profiles", (q) => q.eq("role", "student")],
    ["attempts", "exam_results", null],
    ["questions", "question_bank", (q) => q.eq("archived", false)],
  ];
  for (const [field, table, refine] of targets) {
    try {
      let query = admin.from(table).select("*", { count: "exact", head: true });
      if (refine) query = refine(query);
      const { count, error } = await query;
      if (error) throw error;
      counts[field] = typeof count === "number" ? count : null;
    } catch (e) {
      warn(`không đếm được ${table}: ${e?.message ?? e} — để trống trường ${field}.`);
    }
  }
  return counts;
}

/**
 * Số liệu cho trang chủ (mục "Em đang học ở đâu?" + dải tổng): mỗi lớp đếm chương gắn với lớp
 * (chapter_classes), bài đã công bố trong các chương đó và mục đã đăng trong các bài đó.
 * Một chương gắn nhiều lớp được đếm cho từng lớp (tổng toàn site vẫn đếm mỗi chương 1 lần).
 */
/**
 * Lớp học thêm đang mở đăng ký + lịch tuần, cho dải "Dành cho phụ huynh" ở trang chủ.
 * RLS cho anon đọc khoá is_public + active (xem docs/KHOA-HOC.md), nên dùng được anon key.
 * Đọc LÚC BUILD (giống số liệu bên dưới) — trang chủ không gọi Supabase khi tải (quy tắc
 * "không thêm round-trip cho /"). Lịch đổi theo học kì, mỗi lần deploy là mới. Lỗi → null,
 * trang chủ tự hiện câu "chưa có lịch", không fail build.
 */
async function fetchPublicCourses(supabase) {
  try {
    const { data, error } = await supabase
      .from("thpt_courses")
      .select(
        "id, class_id, name, school_year, starts_at, is_public, status, classes(name), thpt_course_schedules(weekday, start_time, end_time, location)",
      )
      .eq("is_public", true)
      .eq("status", "active")
      .order("class_id")
      .order("id");
    if (error) throw error;
    return (data ?? []).map((row) => {
      const cls = Array.isArray(row.classes) ? row.classes[0] : row.classes;
      return {
        id: row.id,
        name: row.name,
        className: cls?.name ?? "",
        schoolYear: row.school_year ?? "",
        startsAt: row.starts_at ?? null,
        schedules: (row.thpt_course_schedules ?? [])
          .map((x) => ({
            weekday: x.weekday,
            start: String(x.start_time).slice(0, 5),
            end: String(x.end_time).slice(0, 5),
            location: x.location ?? "",
          }))
          .sort((a, b) => a.weekday - b.weekday || a.start.localeCompare(b.start)),
      };
    });
  } catch (e) {
    warn(`không đọc được thpt_courses: ${e?.message ?? e} — home-stats.json để trống courses.`);
    return null;
  }
}

function buildHomeStats(generatedAt, classes, chapters, lessons, itemsByLesson, counts, courses) {
  const lessonsByChapter = new Map();
  for (const l of lessons) {
    const list = lessonsByChapter.get(l.chapter_id) ?? [];
    list.push(l);
    lessonsByChapter.set(l.chapter_id, list);
  }
  const itemCount = (lessonId) => (itemsByLesson.get(lessonId) ?? []).length;
  const perClass = classes.map((c) => {
    const ownChapters = chapters.filter((ch) => ch.classIds.includes(c.id));
    const ownLessons = ownChapters.flatMap((ch) => lessonsByChapter.get(ch.id) ?? []);
    return {
      id: c.id,
      slug: c.slug,
      name: c.name,
      color: c.color,
      icon: c.icon,
      chapters: ownChapters.length,
      lessons: ownLessons.length,
      items: ownLessons.reduce((sum, l) => sum + itemCount(l.id), 0),
    };
  });
  return {
    generatedAt,
    totals: {
      classes: classes.length,
      chapters: chapters.length,
      lessons: lessons.length,
      items: lessons.reduce((sum, l) => sum + itemCount(l.id), 0),
      ...counts,
    },
    classes: perClass,
    courses,
  };
}

async function main() {
  const started = Date.now();
  const { url, anonKey, serviceKey } = loadEnv();
  if (!url || !anonKey) return bail("thiếu NEXT_PUBLIC_SUPABASE_URL / NEXT_PUBLIC_SUPABASE_ANON_KEY.");

  const { createClient } = await import("@supabase/supabase-js");
  const supabase = createClient(url, anonKey, { auth: { persistSession: false } });

  let classes, chapters, lessonRows, itemRows, itemColumns;
  try {
    // ---- classes (như fetchClasses) ----
    const cls = await supabase
      .from("classes")
      .select("id, name, slug, color, icon, sort_order, active")
      .eq("active", true)
      .order("sort_order")
      .order("name");
    if (cls.error) throw cls.error;
    classes = cls.data ?? [];

    // ---- chapters (như fetchChapters) ----
    const chs = await supabase
      .from("chapters")
      .select("id, title, sort_order, subject_code, chapter_classes(class_id)")
      .order("sort_order")
      .order("id");
    if (chs.error) throw chs.error;
    chapters = (chs.data ?? []).map((c) => ({
      id: c.id,
      title: c.title,
      sort_order: c.sort_order,
      classIds: (c.chapter_classes ?? []).map((r) => r.class_id),
      subjectCode: c.subject_code ?? "vat-ly",
    }));

    // ---- lessons đã công bố (như fetchLessons(false), tự lùi khi thiếu cột lesson_kind) ----
    const lessonSelect = (withKind) =>
      supabase
        .from("lessons")
        .select(
          withKind
            ? "id, chapter_id, title, sort_order, published, lesson_kind, description"
            : "id, chapter_id, title, sort_order, published",
        )
        .eq("published", true)
        .order("sort_order")
        .order("id");
    try {
      lessonRows = await fetchAll(() => lessonSelect(true));
    } catch {
      lessonRows = await fetchAll(() => lessonSelect(false));
    }

    // ---- lesson_items của các bài đó (metadata + body_html + questions chỉ để đếm) ----
    const lessonIds = lessonRows.map((l) => l.id);
    const itemSelect = (columns) => () =>
      supabase
        .from("lesson_items")
        .select(`${columns}, body_html, questions`)
        .in("lesson_id", lessonIds)
        .order("lesson_id")
        .order("sort_order")
        .order("id");
    itemRows = null;
    for (const columns of [ITEM_META_V5, ITEM_META_V4, ITEM_META_V3, ITEM_META_V2, ITEM_META_V1]) {
      try {
        itemRows = lessonIds.length ? await fetchAll(itemSelect(columns)) : [];
        itemColumns = columns;
        break;
      } catch {
        /* thiếu cột migration mới → thử danh sách cột cũ hơn */
      }
    }
    if (!itemRows) throw new Error("không đọc được lesson_items với bất kỳ danh sách cột nào");
    // Chưa chạy migration published_at → coi như mọi mục đã đăng (giữ hành vi cũ).
    // Đã có cột thì lọc thẳng mục published_at = null (chưa đăng) khỏi file tĩnh.
    if (itemColumns === ITEM_META_V4 || itemColumns === ITEM_META_V5) {
      itemRows = itemRows.filter((r) => r.published_at !== null);
    }
  } catch (e) {
    return bail(`không lấy được dữ liệu từ Supabase: ${e?.message ?? e}`);
  }

  const generatedAt = new Date().toISOString();
  const chapterTitle = new Map(chapters.map((c) => [c.id, c.title]));
  const itemsByLesson = new Map();
  let strippedBodies = 0;
  for (const raw of itemRows) {
    const { body_html, summary_html, questions, ...meta } = raw;
    const keepBody = BODY_KINDS.has(raw.kind);
    if (!keepBody && (body_html ?? "").trim()) strippedBodies += 1;
    const item = {
      ...meta,
      subtitle: meta.subtitle ?? "",
      video_url: meta.video_url ?? "",
      pdf_url: meta.pdf_url ?? "",
      exam_ids: meta.exam_ids ?? [],
      body_html: keepBody ? body_html ?? "" : "",
      summary_html: keepBody ? summary_html ?? "" : "",
      // Lời giải bài tập mẫu (questions) không vào file tĩnh — chỉ ghi số lượng để
      // client biết cần tải thêm từ Supabase.
      questions: [],
      questions_count: Array.isArray(questions) ? questions.length : 0,
    };
    const list = itemsByLesson.get(raw.lesson_id) ?? [];
    list.push(item);
    itemsByLesson.set(raw.lesson_id, list);
  }
  if (strippedBodies) {
    warn(
      `${strippedBodies} mục không phải lý thuyết/video có body_html — đã bỏ khỏi file tĩnh, ` +
        "trang HS sẽ hiện thiếu phần đó cho tới khi bổ sung BODY_KINDS trong scripts/build-content.mjs.",
    );
  }

  const lessons = lessonRows.map((l) => ({
    id: l.id,
    chapter_id: l.chapter_id,
    title: l.title,
    sort_order: l.sort_order,
    published: l.published,
    lesson_kind: l.lesson_kind ?? "bai_hoc",
    description: l.description ?? "",
  }));

  const catalog = {
    generatedAt,
    classes,
    chapters,
    lessons: lessons.map((l) => ({
      ...l,
      itemCount: (itemsByLesson.get(l.id) ?? []).length,
      itemRefs: (itemsByLesson.get(l.id) ?? []).map((it) => ({ id: it.id, exam_ids: it.exam_ids })),
    })),
  };

  // Ghi ra đĩa: dữ liệu đã đủ trong bộ nhớ nên xoá thư mục lessons cũ rồi ghi lại
  // (bài đã gỡ công bố không còn file; catalog ghi sau cùng).
  rmSync(LESSONS_DIR, { recursive: true, force: true });
  mkdirSync(LESSONS_DIR, { recursive: true });
  let bytes = 0;
  for (const l of lessons) {
    const file = {
      generatedAt,
      lesson: l,
      chapterTitle: chapterTitle.get(l.chapter_id) ?? "",
      items: itemsByLesson.get(l.id) ?? [],
    };
    const json = JSON.stringify(file);
    bytes += json.length;
    writeFileSync(join(LESSONS_DIR, `${l.id}.json`), json);
  }
  writeJson(join(OUT_DIR, "catalog.json"), catalog);
  const counts = await fetchSiteCounts(url, serviceKey);
  const courses = await fetchPublicCourses(supabase);
  writeJson(
    join(OUT_DIR, "home-stats.json"),
    buildHomeStats(generatedAt, classes, chapters, lessons, itemsByLesson, counts, courses),
  );
  writeJson(join(OUT_DIR, "manifest.json"), {
    generatedAt,
    itemColumns,
    classes: classes.length,
    chapters: chapters.length,
    lessons: lessons.length,
    items: itemRows.length,
  });

  const files = readdirSync(LESSONS_DIR).length + 2;
  const countsText = Object.entries(counts)
    .map(([key, value]) => `${key}=${value ?? "?"}`)
    .join(" · ");
  console.log(
    `[build-content] ✓ ${classes.length} lớp · ${chapters.length} chương · ${lessons.length} bài · ` +
      `${itemRows.length} mục → ${files} file, ${(bytes / 1024).toFixed(0)} KB bài học, ` +
      `${((Date.now() - started) / 1000).toFixed(1)} s · ${countsText}`,
  );
}

main().catch((e) => bail(`lỗi không mong đợi: ${e?.message ?? e}`));
