import { getSupabase } from "@/services/supabase";
import type { ClassExamResult } from "@/services/class-results";
import type { ChapterLessonMastery, MasteryLevel as RadarLevel } from "@/services/mastery";

/**
 * Số liệu cho dashboard giáo viên (bản đồ thành thạo, nhóm theo chủ đề, cảnh báo sớm).
 * Tính ở client từ bảng kết quả từng câu — quy tắc nhãn giống docs/mastery-rules.md
 * (10 lượt gần nhất, sum(earned)/sum(max), <4 lượt = chưa đủ dữ liệu).
 */

export type MasteryLevel = "none" | "weak" | "mid" | "strong";

export const LEVEL_META: Record<MasteryLevel, { icon: string; label: string; cls: string }> = {
  strong: { icon: "✅", label: "Nắm vững", cls: "bg-emerald-500/15 text-emerald-300" },
  mid: { icon: "🟡", label: "Cần luyện thêm", cls: "bg-amber-500/15 text-amber-300" },
  weak: { icon: "🔴", label: "Chưa đạt", cls: "bg-red-500/15 text-red-300" },
  none: { icon: "⚪", label: "Chưa đủ dữ liệu", cls: "bg-slate-500/20 text-slate-400" },
};

const LEVEL_ORDER: Record<MasteryLevel, number> = { weak: 0, mid: 1, strong: 2, none: 3 };

export interface QuestionActivityRow {
  student_id: string;
  topic_id: number;
  earned: number;
  max: number;
  created_at: string;
}

const PAGE = 1000;

async function fetchAllRows(table: "exam_question_results" | "practice_question_results", studentIds: string[]) {
  const out: QuestionActivityRow[] = [];
  // Chia học sinh thành nhóm nhỏ để mỗi truy vấn không quá lớn, rồi phân trang.
  for (let i = 0; i < studentIds.length; i += 40) {
    const chunk = studentIds.slice(i, i + 40);
    for (let from = 0; ; from += PAGE) {
      const { data, error } = await getSupabase()
        .from(table)
        .select("student_id, topic_id, earned, max, created_at")
        .in("student_id", chunk)
        .not("topic_id", "is", null)
        .order("created_at", { ascending: false })
        .range(from, from + PAGE - 1);
      if (error) throw error;
      const rows = (data ?? []) as { student_id: string; topic_id: number; earned: number | string; max: number | string; created_at: string }[];
      for (const r of rows) out.push({ ...r, earned: Number(r.earned), max: Number(r.max) });
      if (rows.length < PAGE) break;
    }
  }
  return out;
}

/** Mọi dòng làm bài từng câu (làm đề + luyện tập) của các học sinh, đã gộp hai bảng. */
export async function fetchClassQuestionActivity(studentIds: string[]): Promise<QuestionActivityRow[]> {
  if (studentIds.length === 0) return [];
  const [a, b] = await Promise.all([
    fetchAllRows("exam_question_results", studentIds),
    fetchAllRows("practice_question_results", studentIds).catch(() => [] as QuestionActivityRow[]),
  ]);
  return [...a, ...b];
}

export interface TopicMeta {
  id: number;
  name: string;
  parentId: number | null;
  lessonId: number | null;
  sortOrder: number;
}
export interface LessonMeta {
  id: number;
  title: string;
  chapterId: number;
  sortOrder: number;
  published: boolean;
}
export interface ChapterMeta {
  id: number;
  title: string;
  sortOrder: number;
  subjectCode: string | null;
  /** Lớp mà chương được gắn (chapter_classes) — để gom "cả khoá" đúng lớp. */
  classIds: number[];
}
export interface CurriculumMeta {
  topics: Map<number, TopicMeta>;
  lessons: Map<number, LessonMeta>;
  chapters: Map<number, ChapterMeta>;
}

export async function fetchCurriculumMeta(): Promise<CurriculumMeta> {
  const supabase = getSupabase();
  const [t, l, c, cc] = await Promise.all([
    supabase.from("question_topics").select("id, name, parent_id, lesson_id, sort_order"),
    supabase.from("lessons").select("id, title, chapter_id, sort_order, published"),
    supabase.from("chapters").select("id, title, sort_order, subject_code"),
    supabase.from("chapter_classes").select("chapter_id, class_id"),
  ]);
  const topics = new Map<number, TopicMeta>();
  for (const r of (t.data ?? []) as { id: number; name: string; parent_id: number | null; lesson_id: number | null; sort_order: number }[]) {
    topics.set(r.id, { id: r.id, name: r.name, parentId: r.parent_id, lessonId: r.lesson_id, sortOrder: r.sort_order });
  }
  const lessons = new Map<number, LessonMeta>();
  for (const r of (l.data ?? []) as { id: number; title: string; chapter_id: number; sort_order: number; published: boolean }[]) {
    lessons.set(r.id, { id: r.id, title: r.title, chapterId: r.chapter_id, sortOrder: r.sort_order, published: r.published });
  }
  const classIdsOf = new Map<number, number[]>();
  for (const r of (cc.data ?? []) as { chapter_id: number; class_id: number }[]) {
    const list = classIdsOf.get(r.chapter_id);
    if (list) list.push(r.class_id);
    else classIdsOf.set(r.chapter_id, [r.class_id]);
  }
  const chapters = new Map<number, ChapterMeta>();
  for (const r of (c.data ?? []) as { id: number; title: string; sort_order: number; subject_code: string | null }[]) {
    chapters.set(r.id, { id: r.id, title: r.title, sortOrder: r.sort_order, subjectCode: r.subject_code, classIds: classIdsOf.get(r.id) ?? [] });
  }
  return { topics, lessons, chapters };
}

export function levelOf(count: number, rate: number): MasteryLevel {
  if (count < 4) return "none";
  if (rate >= 0.8) return "strong";
  if (rate >= 0.5) return "mid";
  return "weak";
}

export interface TopicCell {
  topicId: number;
  count: number;
  rate: number;
  level: MasteryLevel;
}

export interface MasteryMap {
  /** studentId -> topicId -> ô thành thạo */
  byStudentTopic: Map<string, Map<number, TopicCell>>;
  /** studentId -> lessonId -> mức thấp nhất trong các nhóm đã đủ dữ liệu */
  byStudentLesson: Map<string, Map<number, MasteryLevel>>;
  /** lessonId -> chủ đề (topicId) có dữ liệu của lớp */
  topicsOfLesson: Map<number, number[]>;
  lastActivity: Map<string, string>;
}

export function buildMasteryMap(rows: QuestionActivityRow[], meta: CurriculumMeta): MasteryMap {
  const grouped = new Map<string, QuestionActivityRow[]>(); // `${student}|${topic}`
  const lastActivity = new Map<string, string>();
  for (const r of rows) {
    const k = `${r.student_id}|${r.topic_id}`;
    const list = grouped.get(k);
    if (list) list.push(r);
    else grouped.set(k, [r]);
    const cur = lastActivity.get(r.student_id);
    if (!cur || r.created_at > cur) lastActivity.set(r.student_id, r.created_at);
  }
  const byStudentTopic = new Map<string, Map<number, TopicCell>>();
  const byStudentLesson = new Map<string, Map<number, MasteryLevel>>();
  const topicsOfLesson = new Map<number, Set<number>>();

  for (const [k, list] of grouped) {
    const [studentId, topicIdStr] = k.split("|");
    const topicId = Number(topicIdStr);
    const recent = list.sort((a, b) => (a.created_at < b.created_at ? 1 : -1)).slice(0, 10);
    const earned = recent.reduce((s, r) => s + r.earned, 0);
    const max = recent.reduce((s, r) => s + r.max, 0);
    const rate = max > 0 ? earned / max : 0;
    const cell: TopicCell = { topicId, count: recent.length, rate, level: levelOf(recent.length, rate) };
    const st = byStudentTopic.get(studentId) ?? new Map<number, TopicCell>();
    st.set(topicId, cell);
    byStudentTopic.set(studentId, st);

    const lessonId = meta.topics.get(topicId)?.lessonId;
    if (lessonId == null) continue;
    const tl = topicsOfLesson.get(lessonId) ?? new Set<number>();
    tl.add(topicId);
    topicsOfLesson.set(lessonId, tl);
    if (cell.level === "none") {
      const sl = byStudentLesson.get(studentId) ?? new Map<number, MasteryLevel>();
      if (!sl.has(lessonId)) sl.set(lessonId, "none");
      byStudentLesson.set(studentId, sl);
      continue;
    }
    const sl = byStudentLesson.get(studentId) ?? new Map<number, MasteryLevel>();
    const prev = sl.get(lessonId);
    if (!prev || prev === "none" || LEVEL_ORDER[cell.level] < LEVEL_ORDER[prev]) sl.set(lessonId, cell.level);
    byStudentLesson.set(studentId, sl);
  }
  return {
    byStudentTopic,
    byStudentLesson,
    topicsOfLesson: new Map([...topicsOfLesson].map(([k, v]) => [k, [...v]])),
    lastActivity,
  };
}

export interface PairGroup {
  weak: string[];
  helper: string | null;
}

/** Chia nhóm 3–4 em: mỗi nhóm một em vững kèm các em yếu cùng chủ đề. */
export function suggestGroups(weakIds: string[], strongIds: string[]): PairGroup[] {
  if (weakIds.length === 0) return [];
  const size = 3;
  const groups: PairGroup[] = [];
  for (let i = 0; i < weakIds.length; i += size) {
    groups.push({ weak: weakIds.slice(i, i + size), helper: strongIds[groups.length % Math.max(strongIds.length, 1)] ?? null });
  }
  return groups;
}

// ---------------------------------------------------------------------------
// Cảnh báo sớm (tín hiệu hành vi, trước khi thành "cần phụ đạo")
// ---------------------------------------------------------------------------
export type EarlySignalKind = "inactive" | "score_drop" | "rushed" | "never_started";

export interface EarlySignal {
  studentId: string;
  kind: EarlySignalKind;
  text: string;
}

export const EARLY_THRESHOLDS = {
  inactiveDays: 10,
  dropMin: 1.5,
  rushedRatio: 0.35,
  rushedMaxScore: 5,
};

const DAY = 86400000;

export function computeEarlySignals(
  studentIds: string[],
  results: ClassExamResult[],
  lastActivity: Map<string, string>,
  now = Date.now(),
): EarlySignal[] {
  const out: EarlySignal[] = [];
  const byStudent = new Map<string, ClassExamResult[]>();
  const durationsByExam = new Map<number, number[]>();
  for (const r of results) {
    const l = byStudent.get(r.student_id) ?? [];
    l.push(r);
    byStudent.set(r.student_id, l);
    if (r.duration_seconds > 0) {
      const d = durationsByExam.get(r.exam_id) ?? [];
      d.push(r.duration_seconds);
      durationsByExam.set(r.exam_id, d);
    }
  }
  const median = (a: number[]) => {
    const s = [...a].sort((x, y) => x - y);
    return s[Math.floor(s.length / 2)];
  };
  // Chỉ báo "lâu không hoạt động" khi cả lớp còn hoạt động gần đây — tránh báo hàng loạt lúc nghỉ hè/nghỉ lễ.
  const classRecent = [...lastActivity.values()].some((t) => now - new Date(t).getTime() < EARLY_THRESHOLDS.inactiveDays * DAY);

  for (const id of studentIds) {
    const own = (byStudent.get(id) ?? []).slice().sort((a, b) => (a.created_at < b.created_at ? -1 : 1));
    const last = lastActivity.get(id);
    const lastExam = own.length ? own[own.length - 1].created_at : undefined;
    const latest = [last, lastExam].filter(Boolean).sort().pop();

    if (!latest) {
      if (classRecent) out.push({ studentId: id, kind: "never_started", text: "Chưa làm câu nào trên hệ thống" });
    } else if (classRecent) {
      const days = Math.floor((now - new Date(latest).getTime()) / DAY);
      if (days >= EARLY_THRESHOLDS.inactiveDays) out.push({ studentId: id, kind: "inactive", text: `${days} ngày chưa hoạt động` });
    }

    if (own.length >= 3) {
      const [a, b, c] = own.slice(-3).map((r) => Number(r.score));
      if (a > b && b > c && a - c >= EARLY_THRESHOLDS.dropMin) {
        out.push({ studentId: id, kind: "score_drop", text: `Điểm giảm 3 lần liên tiếp: ${a} → ${b} → ${c}` });
      }
    }

    const lastR = own[own.length - 1];
    if (lastR && lastR.duration_seconds > 0) {
      const d = durationsByExam.get(lastR.exam_id) ?? [];
      if (d.length >= 5 && Number(lastR.score) < EARLY_THRESHOLDS.rushedMaxScore && lastR.duration_seconds < median(d) * EARLY_THRESHOLDS.rushedRatio) {
        out.push({
          studentId: id,
          kind: "rushed",
          text: `Làm "${lastR.exams?.title ?? "đề"}" rất nhanh (${Math.round(lastR.duration_seconds / 60)}′) nhưng chỉ ${lastR.score} điểm`,
        });
      }
    }
  }
  return out;
}

// ---------------------------------------------------------------------------
// Dữ liệu cho biểu đồ mạng nhện (ChapterMasteryRadar) của MỘT học sinh, nhìn từ phía giáo viên.
// Cùng công thức RPC get_my_chapter_mastery_pct (chỉ đọc theo auth.uid() nên giáo viên không dùng được):
// chương = chương của lượt làm gần nhất (tới mốc `before`), pct bài = Σearned/Σmax của ≤10 lượt/nhóm,
// nhãn bài = nhãn thấp nhất trong các nhóm đủ dữ liệu.
// ---------------------------------------------------------------------------
export function buildChapterRadar(rows: QuestionActivityRow[], meta: CurriculumMeta, before?: Date): ChapterLessonMastery[] {
  const cutoff = before ? before.toISOString() : null;
  const usable = rows.filter((r) => !cutoff || r.created_at <= cutoff).sort((a, b) => (a.created_at < b.created_at ? 1 : -1));
  let chapterId: number | undefined;
  for (const r of usable) {
    const lid = meta.topics.get(r.topic_id)?.lessonId;
    const ch = lid != null ? meta.lessons.get(lid)?.chapterId : undefined;
    if (ch != null) { chapterId = ch; break; }
  }
  if (chapterId == null) return [];
  const chapter = meta.chapters.get(chapterId);
  const byTopic = new Map<number, QuestionActivityRow[]>();
  for (const r of usable) {
    const l = byTopic.get(r.topic_id) ?? [];
    if (l.length < 10) l.push(r);
    byTopic.set(r.topic_id, l);
  }
  const lessons = [...meta.lessons.values()].filter((l) => l.chapterId === chapterId && l.published).sort((a, b) => a.sortOrder - b.sortOrder);
  return lessons.map((lesson) => {
    let n = 0, se = 0, sm = 0, minRank: number | null = null;
    for (const t of meta.topics.values()) {
      if (t.lessonId !== lesson.id) continue;
      const list = byTopic.get(t.id) ?? [];
      const e = list.reduce((a, r) => a + r.earned, 0);
      const m = list.reduce((a, r) => a + r.max, 0);
      n += list.length; se += e; sm += m;
      if (list.length >= 4 && m > 0) {
        const rank = e / m >= 0.8 ? 2 : e / m >= 0.5 ? 1 : 0;
        minRank = minRank === null ? rank : Math.min(minRank, rank);
      }
    }
    const level: RadarLevel = minRank === null ? "insufficient" : minRank === 0 ? "weak" : minRank === 1 ? "practicing" : "mastered";
    return {
      chapterId: chapterId!,
      chapterTitle: chapter?.title ?? "",
      lessonId: lesson.id,
      lessonTitle: lesson.title,
      sortOrder: lesson.sortOrder,
      answeredCount: n,
      pct: sm === 0 ? null : Math.round((se / sm) * 100),
      level,
    };
  });
}

/**
 * Như buildChapterRadar nhưng trả MỌI bài đã công bố của khoá (các chương cùng môn, chung lớp với chương
 * em làm gần nhất) kèm earned/max và chapterSort để radar chuyển được Theo chương / Cả khoá. Cùng công thức
 * RPC get_my_course_mastery_pct (giáo viên không gọi được vì RPC đọc theo auth.uid()).
 */
export function buildCourseRadar(rows: QuestionActivityRow[], meta: CurriculumMeta, before?: Date): ChapterLessonMastery[] {
  const cutoff = before ? before.toISOString() : null;
  const usable = rows.filter((r) => !cutoff || r.created_at <= cutoff).sort((a, b) => (a.created_at < b.created_at ? 1 : -1));
  let latestId: number | undefined;
  for (const r of usable) {
    const lid = meta.topics.get(r.topic_id)?.lessonId;
    const ch = lid != null ? meta.lessons.get(lid)?.chapterId : undefined;
    if (ch != null) { latestId = ch; break; }
  }
  if (latestId == null) return [];
  const latest = meta.chapters.get(latestId);
  const courseIds = new Set<number>([latestId]);
  for (const c of meta.chapters.values()) {
    if (c.subjectCode === (latest?.subjectCode ?? null) && c.classIds.some((id) => latest?.classIds.includes(id))) courseIds.add(c.id);
  }
  const byTopic = new Map<number, QuestionActivityRow[]>();
  for (const r of usable) {
    const l = byTopic.get(r.topic_id) ?? [];
    if (l.length < 10) l.push(r);
    byTopic.set(r.topic_id, l);
  }
  const lessons = [...meta.lessons.values()]
    .filter((l) => courseIds.has(l.chapterId) && l.published)
    .sort((a, b) => (meta.chapters.get(a.chapterId)?.sortOrder ?? 0) - (meta.chapters.get(b.chapterId)?.sortOrder ?? 0) || a.chapterId - b.chapterId || a.sortOrder - b.sortOrder);
  return lessons.map((lesson) => {
    let n = 0, se = 0, sm = 0, minRank: number | null = null;
    for (const t of meta.topics.values()) {
      if (t.lessonId !== lesson.id) continue;
      const list = byTopic.get(t.id) ?? [];
      const e = list.reduce((a, r) => a + r.earned, 0);
      const m = list.reduce((a, r) => a + r.max, 0);
      n += list.length; se += e; sm += m;
      if (list.length >= 4 && m > 0) {
        const rank = e / m >= 0.8 ? 2 : e / m >= 0.5 ? 1 : 0;
        minRank = minRank === null ? rank : Math.min(minRank, rank);
      }
    }
    const level: RadarLevel = minRank === null ? "insufficient" : minRank === 0 ? "weak" : minRank === 1 ? "practicing" : "mastered";
    const chapter = meta.chapters.get(lesson.chapterId);
    return {
      chapterId: lesson.chapterId,
      chapterTitle: chapter?.title ?? "",
      lessonId: lesson.id,
      lessonTitle: lesson.title,
      sortOrder: lesson.sortOrder,
      answeredCount: n,
      pct: sm === 0 ? null : Math.round((se / sm) * 100),
      level,
      chapterSort: chapter?.sortOrder ?? 0,
      subjectCode: chapter?.subjectCode ?? null,
      isLatest: lesson.chapterId === latestId,
      earned: se,
      max: sm,
    };
  });
}
