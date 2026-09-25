// Lớp đọc học liệu công khai từ file tĩnh cùng origin (public/data/, sinh bởi
// scripts/build-content.mjs lúc build) — CHỈ dành cho trang học sinh. Trang giáo
// viên / quản trị vẫn gọi thẳng fetchLessons/fetchClasses/... để luôn thấy dữ liệu mới nhất.
//
// Cách hoạt động ("tĩnh trước, tươi sau"):
//   1. Trả về ngay dữ liệu trong file tĩnh (1 request cùng origin, host cache 10 phút).
//   2. Song song gọi 1 truy vấn Supabase nhẹ (không có body_html) để đối chiếu; nếu
//      dữ liệu trên DB đã khác → tải bản đầy đủ từ Supabase và báo qua onUpdate.
//   3. File tĩnh thiếu / 404 / hỏng → gọi Supabase như cũ, kết quả y hệt.
// Các bảng chưa có cột updated_at nên đối chiếu bằng metadata (tên, mô tả, mục, đề gắn);
// riêng nội dung lý thuyết sửa tại chỗ chỉ cập nhật sau khi build lại (xem README).
import type { SchoolClass } from "@/features/exams/types";
import {
  normalizeLessonItemKind,
  normalizeLessonKind,
  type Chapter,
  type Lesson,
  type LessonItem,
} from "@/features/lessons/types";
import { fetchClasses } from "@/services/classes";
import {
  fetchChapters,
  fetchLessons,
  fetchLessonWithItems,
  fetchLessonItems,
  type LessonWithItemRefs,
} from "@/services/lessons";
import { getSupabase } from "@/services/supabase";

const DATA_BASE = "/data";

interface StaticCatalog {
  generatedAt: string;
  classes: SchoolClass[];
  chapters: Chapter[];
  lessons: LessonWithItemRefs[];
}

type StaticItem = LessonItem & { questions_count?: number };

interface StaticLesson {
  generatedAt: string;
  lesson: Lesson;
  chapterTitle: string;
  items: StaticItem[];
}

export interface LessonBundle {
  lesson: Lesson;
  chapterTitle: string;
  items: LessonItem[];
}

async function fetchStaticJson<T>(path: string): Promise<T | null> {
  if (typeof window === "undefined") return null;
  try {
    const res = await fetch(`${DATA_BASE}${path}`, { cache: "default" });
    if (!res.ok) return null;
    const type = res.headers.get("content-type") ?? "";
    if (!type.includes("json")) return null;
    return (await res.json()) as T;
  } catch {
    return null;
  }
}

// ---------- Catalog: lớp → chương → bài ----------

let catalogPromise: Promise<StaticCatalog | null> | null = null;

function loadCatalog(): Promise<StaticCatalog | null> {
  if (!catalogPromise) {
    catalogPromise = fetchStaticJson<StaticCatalog>("/catalog.json").then((cat) => {
      if (!cat || !Array.isArray(cat.classes) || !Array.isArray(cat.chapters) || !Array.isArray(cat.lessons)) {
        return null;
      }
      return {
        ...cat,
        lessons: cat.lessons.map((l) => ({
          ...l,
          lesson_kind: normalizeLessonKind(l.lesson_kind),
          itemRefs: l.itemRefs ?? [],
          itemCount: l.itemRefs?.length ?? 0,
        })),
      };
    });
  }
  return catalogPromise;
}

interface FreshCatalog {
  classes: SchoolClass[];
  chapters: Chapter[];
  lessons: LessonWithItemRefs[];
}

let revalidatePromise: Promise<FreshCatalog | null> | null = null;

/** Khoá so sánh danh sách bài — đúng những cột fetchLessons chọn (không có gì để bỏ bớt: mô tả cả site ~8 KB). */
function lessonsKey(lessons: LessonWithItemRefs[]): string {
  return JSON.stringify(
    lessons.map((l) => [
      l.id,
      l.chapter_id,
      l.title,
      l.sort_order,
      l.published,
      l.lesson_kind,
      l.description,
      // lesson_items lồng trong fetchLessons không có thứ tự cố định → sắp theo id trước khi so.
      [...l.itemRefs].sort((a, b) => a.id - b.id).map((r) => [r.id, r.exam_ids]),
    ]),
  );
}

/**
 * Đối chiếu catalog tĩnh với DB — chạy 1 lần cho mỗi lượt tải trang (nhiều nơi gọi dùng chung).
 * Trả về bản mới nếu danh sách bài đã khác, null nếu vẫn khớp (hoặc không kiểm tra được).
 * Chương/lớp đổi mà bài không đổi thì chỉ cập nhật sau khi build lại (hiếm: vài lần/năm).
 */
function revalidateCatalog(cat: StaticCatalog): Promise<FreshCatalog | null> {
  if (!revalidatePromise) {
    revalidatePromise = (async () => {
      try {
        const lessons = await fetchLessons();
        if (lessonsKey(lessons) === lessonsKey(cat.lessons)) return null;
        const [classes, chapters] = await Promise.all([fetchClasses(), fetchChapters()]);
        return { classes, chapters, lessons };
      } catch {
        return null;
      }
    })();
  }
  return revalidatePromise;
}

/** Như fetchClasses() nhưng ưu tiên file tĩnh; onUpdate được gọi nếu DB đã khác bản tĩnh. */
export async function fetchClassesStatic(onUpdate?: (fresh: SchoolClass[]) => void): Promise<SchoolClass[]> {
  const cat = await loadCatalog();
  if (!cat) return fetchClasses();
  if (onUpdate) void revalidateCatalog(cat).then((fresh) => fresh && onUpdate(fresh.classes));
  return cat.classes;
}

/** Như fetchChapters() nhưng ưu tiên file tĩnh. */
export async function fetchChaptersStatic(onUpdate?: (fresh: Chapter[]) => void): Promise<Chapter[]> {
  const cat = await loadCatalog();
  if (!cat) return fetchChapters();
  if (onUpdate) void revalidateCatalog(cat).then((fresh) => fresh && onUpdate(fresh.chapters));
  return cat.chapters;
}

/** Như fetchLessons() (chỉ bài đã công bố) nhưng ưu tiên file tĩnh. */
export async function fetchLessonsStatic(
  onUpdate?: (fresh: LessonWithItemRefs[]) => void,
): Promise<LessonWithItemRefs[]> {
  const cat = await loadCatalog();
  if (!cat) return fetchLessons();
  if (onUpdate) void revalidateCatalog(cat).then((fresh) => fresh && onUpdate(fresh.lessons));
  return cat.lessons;
}

// ---------- Một bài học + các mục ----------

// Cột metadata mục (không body_html) — cùng thứ tự lùi V3 → V2 → V1 như services/lessons.ts.
const META_V1 = "id, lesson_id, kind, title, subtitle, video_url, pdf_url, exam_ids, sort_order";
const META_V2 = `${META_V1}, due_at`;
const META_V3 = `${META_V2}, required, quiz_min_correct, practice_pass_score`;

function normalizeItem(raw: Record<string, unknown>): StaticItem {
  return {
    ...raw,
    kind: normalizeLessonItemKind(raw.kind),
    subtitle: raw.subtitle ?? "",
    body_html: raw.body_html ?? "",
    video_url: raw.video_url ?? "",
    pdf_url: raw.pdf_url ?? "",
    questions: raw.questions ?? [],
    exam_ids: raw.exam_ids ?? [],
    due_at: (raw.due_at as string | null) ?? null,
    required: (raw.required as boolean | undefined) ?? true,
    quiz_min_correct: (raw.quiz_min_correct as number | null | undefined) ?? null,
    practice_pass_score: (raw.practice_pass_score as number | null | undefined) ?? null,
  } as unknown as StaticItem;
}

/** Khoá so sánh bài + mục, bỏ body_html/questions (chỉ đếm số câu bài tập mẫu). */
function lessonKey(lesson: Lesson, chapterTitle: string, items: StaticItem[]): string {
  return JSON.stringify([
    lesson.id,
    lesson.chapter_id,
    lesson.title,
    lesson.sort_order,
    lesson.published,
    lesson.lesson_kind,
    lesson.description,
    chapterTitle,
    items.map((it) => [
      it.id,
      it.kind,
      it.title,
      it.subtitle,
      it.video_url,
      it.pdf_url,
      it.exam_ids,
      it.sort_order,
      it.due_at,
      it.required,
      it.quiz_min_correct,
      it.practice_pass_score,
      it.questions_count ?? it.questions.length,
    ]),
  ]);
}

const lessonPromises = new Map<number, Promise<StaticLesson | null>>();

function loadStaticLesson(id: number): Promise<StaticLesson | null> {
  let p = lessonPromises.get(id);
  if (!p) {
    p = fetchStaticJson<StaticLesson>(`/lessons/${id}.json`).then((file) => {
      if (!file || !file.lesson || file.lesson.id !== id || !Array.isArray(file.items)) return null;
      return {
        ...file,
        lesson: { ...file.lesson, lesson_kind: normalizeLessonKind(file.lesson.lesson_kind), itemCount: file.items.length },
        items: file.items.map((it) => normalizeItem(it as unknown as Record<string, unknown>)),
      };
    });
    lessonPromises.set(id, p);
  }
  return p;
}

/**
 * Truy vấn nhẹ: bài + tên chương + metadata mục (không body_html) kèm `questions` của
 * bài tập mẫu (lời giải — không nằm trong file tĩnh, nhưng hiện cho mọi người như trước).
 * Trả về undefined khi truy vấn lỗi (DB thiếu cột…), null khi bài không còn xem được.
 */
async function fetchLessonMeta(
  id: number,
): Promise<{ lesson: Lesson; chapterTitle: string; items: StaticItem[] } | null | undefined> {
  for (const columns of [META_V3, META_V2, META_V1]) {
    const res = await getSupabase()
      .from("lessons")
      .select(
        `id, chapter_id, title, sort_order, published, lesson_kind, description, chapters(title), lesson_items(${columns}, questions)`,
      )
      .eq("id", id)
      .order("sort_order", { referencedTable: "lesson_items" })
      .order("id", { referencedTable: "lesson_items" })
      .maybeSingle();
    if (res.error) continue;
    const data = res.data as
      | (Record<string, unknown> & { chapters?: { title: string } | null; lesson_items?: Record<string, unknown>[] })
      | null;
    if (!data) return null;
    return {
      lesson: {
        id: data.id,
        chapter_id: data.chapter_id,
        title: data.title,
        sort_order: data.sort_order,
        published: data.published,
        lesson_kind: normalizeLessonKind(data.lesson_kind),
        itemCount: data.lesson_items?.length ?? 0,
        description: (data.description as string) ?? "",
      } as unknown as Lesson,
      chapterTitle: (data.chapters as unknown as { title: string } | null)?.title ?? "",
      items: (data.lesson_items ?? []).map(normalizeItem),
    };
  }
  return undefined;
}

function stripCount(items: StaticItem[]): LessonItem[] {
  return items.map((it) => {
    const { questions_count: _omit, ...rest } = it;
    void _omit;
    return rest as LessonItem;
  });
}

const revalidatedLessons = new Map<number, Promise<LessonBundle | null | undefined>>();

/**
 * Đối chiếu 1 bài với DB (1 lần/bài/lượt tải trang). Trả về:
 *  - undefined: vẫn khớp và không có gì cần bổ sung;
 *  - LessonBundle: bản cần hiển thị (bài tĩnh + lời giải bài tập mẫu, hoặc bản đầy đủ từ DB khi đã khác);
 *  - null: bài không còn xem được (đã gỡ công bố / xoá).
 */
function revalidateLesson(id: number, file: StaticLesson): Promise<LessonBundle | null | undefined> {
  let p = revalidatedLessons.get(id);
  if (!p) {
    p = (async () => {
      try {
        const meta = await fetchLessonMeta(id);
        if (meta === undefined) return undefined; // không đối chiếu được → giữ bản tĩnh
        if (meta === null) return null;
        if (lessonKey(meta.lesson, meta.chapterTitle, meta.items) !== lessonKey(file.lesson, file.chapterTitle, file.items)) {
          return fetchLessonWithItems(id); // đã khác → lấy trọn bản mới (có body_html)
        }
        const questionsById = new Map(meta.items.map((it) => [it.id, it.questions]));
        if (![...questionsById.values()].some((q) => q.length > 0)) return undefined;
        return {
          lesson: file.lesson,
          chapterTitle: file.chapterTitle,
          items: stripCount(file.items).map((it) => ({ ...it, questions: questionsById.get(it.id) ?? [] })),
        };
      } catch {
        return undefined;
      }
    })();
    revalidatedLessons.set(id, p);
  }
  return p;
}

/**
 * Như fetchLessonWithItems(id) nhưng ưu tiên file tĩnh. onUpdate nhận bản cần thay
 * (lời giải bài tập mẫu tải thêm, hoặc bản mới khi DB đã khác) hoặc null nếu bài không còn.
 */
export async function fetchLessonWithItemsStatic(
  id: number,
  onUpdate?: (fresh: LessonBundle | null) => void,
): Promise<LessonBundle | null> {
  const file = await loadStaticLesson(id);
  if (!file) return fetchLessonWithItems(id);
  if (onUpdate) void revalidateLesson(id, file).then((fresh) => fresh !== undefined && onUpdate(fresh));
  return { lesson: file.lesson, chapterTitle: file.chapterTitle, items: stripCount(file.items) };
}

/** Như fetchLessonItems(lessonId) nhưng ưu tiên file tĩnh; onUpdate nhận danh sách mục mới khi cần thay. */
export async function fetchLessonItemsStatic(
  lessonId: number,
  onUpdate?: (fresh: LessonItem[]) => void,
): Promise<LessonItem[]> {
  const file = await loadStaticLesson(lessonId);
  if (!file) return fetchLessonItems(lessonId);
  if (onUpdate) {
    void revalidateLesson(lessonId, file).then((fresh) => {
      if (fresh === undefined) return;
      onUpdate(fresh ? fresh.items : []);
    });
  }
  return stripCount(file.items);
}
