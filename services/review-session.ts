// Buổi ôn tập theo chặng — phía thầy/trợ giảng (tạo, điều khiển, bảng điều phối) và phía học sinh (xem chặng của mình).
// Toàn bộ đi qua RPC review_* (migration 20261021120000_on_tap_theo_chang); học sinh không đọc trực tiếp bảng nào.
import { getSupabase } from "@/services/supabase";

export interface ReviewStageDef {
  exam_id: number;
  item_id: number | null;
  title: string;
  minutes: number;
  /** Chặng "ôn dạng": nhãn dạng của từng câu theo thứ tự trong đề (dùng cho thống kê sai theo dạng). */
  dang_by_index?: string[];
}

/** idle = chưa mở · doing = đang làm · failed = đã nộp, chưa đạt ngưỡng · passed = đạt. */
export type StageState = "idle" | "doing" | "failed" | "passed";

export interface StageProgress {
  state: StageState;
  answered: number;
  total: number;
  best_pct: number | null;
  tries: number;
  /** Số giây kể từ lần cuối đáp án được lưu (chỉ khi đang làm). */
  idle_secs: number | null;
}

export interface BoardStudent extends StageProgress {
  id: string;
  name: string;
}

export interface WrongQuestion {
  idx: number;
  total: number;
  wrong: number;
  pct: number;
  dang?: string | null;
  /** Số em ĐANG sai (lượt làm mới nhất của em vẫn sai). Bản máy chủ cũ không có trường này. */
  students_wrong?: number;
}

export interface DangStat {
  label: string;
  total: number;
  wrong: number;
  pct: number;
  students_wrong: number;
  students: number;
}

export interface ReviewBoard {
  now: string;
  session: {
    id: number;
    title: string;
    class_id: number;
    threshold: number;
    status: "ready" | "running" | "finished";
    current_stage: number;
    /** Chặng bảng này đang tính (bản máy chủ cũ không có: coi là chặng hiện tại). */
    viewed_stage?: number;
    stage_started_at: string | null;
    secs_left: number | null;
    stages: ReviewStageDef[];
  };
  students: BoardStudent[];
  wrongest: WrongQuestion[];
  /** Sai theo dạng ở chặng hiện tại (rỗng nếu chặng không phải ôn dạng). */
  by_dang?: DangStat[];
}

export interface ReviewListItem {
  id: number;
  title: string;
  class_id: number;
  class_name: string;
  status: "ready" | "running" | "finished";
  current_stage: number;
  stage_count: number;
  created_at: string;
  /** Bản máy chủ cũ không có: coi là buổi trên lớp. */
  mode?: ReviewMode;
  due_at?: string | null;
}

/** live = ôn trên lớp (đồng hồ chung, thầy mở từng chặng) · self = tự học ở nhà (mở sẵn, có hạn nộp, không đồng hồ). */
export type ReviewMode = "live" | "self";

export interface MyStage extends ReviewStageDef {
  mine: StageProgress | null;
  /** Chế độ tự học nối tiếp: chặng trước chưa đạt (và em nộp chưa đủ 2 lượt) thì chặng này đang khoá. */
  locked?: boolean;
  /** Chế độ tự học: số bạn đã nộp chặng này (ẩn danh). */
  class_submitted?: number;
  class_total?: number;
}

export interface MyReviewState {
  now: string;
  id: number;
  title: string;
  threshold: number;
  status: "ready" | "running" | "finished";
  mode?: ReviewMode;
  due_at?: string | null;
  sequential?: boolean;
  current_stage: number;
  secs_left: number | null;
  stages: MyStage[];
  /** Số liệu chung của lớp ở chặng hiện tại (ẩn danh). */
  class: { submitted: number; total: number } | null;
}

async function rpc<T>(fn: string, args: Record<string, unknown>): Promise<T> {
  const { data, error } = await getSupabase().rpc(fn, args);
  if (error) throw new Error(error.message);
  return data as T;
}

export const createReviewSession = (classId: number, title: string, threshold: number, stages: ReviewStageDef[]) =>
  rpc<number>("review_create", { p_class: classId, p_title: title, p_threshold: threshold, p_stages: stages });

/** Buổi tự học ở nhà: mọi chặng mở sẵn, hạn nộp `dueAt` (ISO), `sequential` = chặng sau chờ chặng trước đạt. */
export const createReviewSelfSession = (
  classId: number,
  title: string,
  threshold: number,
  stages: ReviewStageDef[],
  dueAt: string,
  sequential: boolean,
) =>
  rpc<number>("review_create_self", {
    p_class: classId,
    p_title: title,
    p_threshold: threshold,
    p_stages: stages,
    p_due_at: dueAt,
    p_sequential: sequential,
  });

export interface ReviewMeta {
  mode: ReviewMode;
  due_at: string | null;
  sequential: boolean;
}

/** Chế độ của một buổi ôn (máy chủ chưa chạy migration tự học thì lỗi → coi là buổi trên lớp). */
export const getReviewMeta = (sessionId: number) =>
  rpc<ReviewMeta>("review_session_meta", { p_session: sessionId }).catch(
    (): ReviewMeta => ({ mode: "live", due_at: null, sequential: false }),
  );

export const listReviewSessions = (classId: number | null = null) =>
  rpc<ReviewListItem[]>("review_list", { p_class: classId });

/** stage −1 = về "chưa bắt đầu"; 0..n−1 = mở chặng đó (đặt lại đồng hồ); ≥ n = kết thúc buổi. */
export const setReviewStage = (sessionId: number, stage: number) =>
  rpc<void>("review_set_stage", { p_session: sessionId, p_stage: stage });

export const extendReviewStage = (sessionId: number, seconds: number) =>
  rpc<void>("review_extend", { p_session: sessionId, p_seconds: seconds });

/** `stage` bỏ trống = chặng hiện tại; số khác = xem lại chặng đó. */
export const getReviewBoard = (sessionId: number, stage: number | null = null) =>
  stage === null
    ? rpc<ReviewBoard>("review_board", { p_session: sessionId })
    : rpc<ReviewBoard>("review_board_stage", { p_session: sessionId, p_stage: stage });

/** Một em đang sai một câu (lượt làm mới nhất của em ở câu đó vẫn sai). */
export interface WrongStudentRow {
  student_id: string;
  name: string;
  idx: number;
  dang: string | null;
  earned: number | null;
  max: number | null;
  tries: number;
}

export const getWrongStudents = (sessionId: number, stage: number | null = null) =>
  rpc<WrongStudentRow[]>("review_wrong_students", { p_session: sessionId, p_stage: stage });

/** Buổi ôn đang diễn ra của lớp em (null nếu không có). */
export const getMyReviewState = (sessionId: number | null = null) =>
  rpc<MyReviewState | null>("review_my_state", { p_session: sessionId });

export interface DangPoolItem {
  label: string;
  n: number;
}

export interface BuiltDangExam {
  exam_id: number;
  title: string;
  question_count: number;
  dang: { label: string; n: number }[];
  dang_by_index: string[];
}

/** Số câu đã gán theo dạng của một bài (để biết bài nào đủ câu ôn dạng). */
export const getDangPool = (lessonId: number) => rpc<DangPoolItem[]>("review_dang_pool", { p_lesson: lessonId });

/** Dựng đề ôn dạng cho một bài: mỗi dạng bốc perDang câu đã gán, gán đề cho lớp. */
export const buildDangExam = (classId: number, lessonId: number, perDang: number) =>
  rpc<BuiltDangExam>("review_build_dang_exam", { p_class: classId, p_lesson: lessonId, p_per_dang: perDang });

export function reviewErrorText(e: unknown): string {
  const m = e instanceof Error ? e.message : String(e);
  if (/forbidden/.test(m)) return "Tài khoản này không có quyền với buổi ôn.";
  if (/not_found/.test(m)) return "Không tìm thấy buổi ôn (có thể đã bị xoá).";
  if (/exam_not_found/.test(m)) return "Có đề trong danh sách không còn tồn tại.";
  if (/due_invalid/.test(m)) return "Hạn nộp phải là một thời điểm trong tương lai.";
  if (/stage_invalid/.test(m)) return "Chặng này không có trong buổi ôn.";
  if (/stages_invalid/.test(m)) return "Buổi ôn cần từ 1 đến 12 chặng.";
  if (/no_dang/.test(m)) return "Bài này chưa có câu nào được gán dạng nên chưa dựng được đề ôn dạng.";
  if (/not_authenticated/.test(m)) return "Cần đăng nhập lại.";
  return "Chưa kết nối được, thử lại sau ít giây.";
}

// ---------- Chọn đề cho các chặng ----------

export interface PickerExam {
  examId: number;
  itemId: number | null;
  lessonId: number | null;
  lessonTitle: string;
  title: string;
  questionCount: number;
  published: boolean;
  /** Loại mục chứa đề (ly_thuyet = Kiểm tra nhanh; còn lại = đề bài tập). */
  kind?: string;
}

export interface PickerChapter {
  id: number;
  title: string;
}

/** Chương dùng được cho một lớp (chương gán cho lớp đó, hoặc chương toàn trường). */
export async function fetchPickerChapters(classId: number): Promise<PickerChapter[]> {
  const { data, error } = await getSupabase()
    .from("chapters")
    .select("id, title, sort_order, chapter_classes(class_id)")
    .order("sort_order")
    .order("id");
  if (error) throw new Error(error.message);
  const rows = (data ?? []) as unknown as { id: number; title: string; chapter_classes: { class_id: number }[] | null }[];
  return rows
    .filter((c) => !c.chapter_classes?.length || c.chapter_classes.some((r) => r.class_id === classId))
    .map((c) => ({ id: c.id, title: c.title }));
}

/**
 * Các đề "Kiểm tra nhanh" của một chương: đề gắn vào mục lý thuyết (`ly_thuyet`) của từng bài, theo thứ tự bài.
 * Lấy cả bài chưa công bố vì thầy có thể ôn bằng đề chưa mở cho học sinh; cờ `published` để người chọn thấy.
 */
export const fetchChapterQuickQuizzes = (chapterId: number) => fetchChapterExams(chapterId, ["ly_thuyet"]);

/** Các bài của một chương (để chọn bài ôn dạng bài tập). */
export async function fetchChapterLessons(chapterId: number): Promise<{ id: number; title: string }[]> {
  const { data, error } = await getSupabase()
    .from("lessons")
    .select("id, title")
    .eq("chapter_id", chapterId)
    .order("sort_order")
    .order("id");
  if (error) throw new Error(error.message);
  return (data ?? []) as { id: number; title: string }[];
}

async function fetchChapterExams(chapterId: number, kinds: string[]): Promise<PickerExam[]> {
  const supabase = getSupabase();
  const { data: lessons, error: le } = await supabase
    .from("lessons")
    .select("id, title, sort_order")
    .eq("chapter_id", chapterId)
    .order("sort_order")
    .order("id");
  if (le) throw new Error(le.message);
  const lessonRows = (lessons ?? []) as { id: number; title: string }[];
  if (lessonRows.length === 0) return [];

  const { data: items, error: ie } = await supabase
    .from("lesson_items")
    .select("id, lesson_id, kind, exam_ids")
    .in("kind", kinds)
    .order("sort_order")
    .in("lesson_id", lessonRows.map((l) => l.id));
  if (ie) throw new Error(ie.message);
  const itemRows = (items ?? []) as { id: number; lesson_id: number; kind: string; exam_ids: number[] | null }[];
  const examIds = [...new Set(itemRows.flatMap((i) => i.exam_ids ?? []))];
  if (examIds.length === 0) return [];

  const { data: exams, error: ee } = await supabase
    .from("exams")
    .select("id, title, question_count, published")
    .in("id", examIds);
  if (ee) throw new Error(ee.message);
  const examById = new Map(((exams ?? []) as { id: number; title: string; question_count: number | null; published: boolean }[]).map((e) => [e.id, e]));

  const out: PickerExam[] = [];
  for (const l of lessonRows) {
    for (const it of itemRows.filter((i) => i.lesson_id === l.id)) {
      for (const id of it.exam_ids ?? []) {
        const e = examById.get(id);
        if (!e) continue;
        out.push({
          examId: id,
          itemId: it.id,
          lessonId: l.id,
          lessonTitle: l.title,
          title: e.title,
          questionCount: e.question_count ?? 0,
          published: e.published,
          kind: it.kind,
        });
      }
    }
  }
  return out;
}

/** Thêm một đề bất kỳ theo mã số (không gắn mục bài học). */
export async function fetchPickerExamById(examId: number): Promise<PickerExam | null> {
  const { data } = await getSupabase()
    .from("exams")
    .select("id, title, question_count, published")
    .eq("id", examId)
    .maybeSingle();
  const e = data as { id: number; title: string; question_count: number | null; published: boolean } | null;
  if (!e) return null;
  return { examId: e.id, itemId: null, lessonId: null, lessonTitle: "Đề nhập theo mã", title: e.title, questionCount: e.question_count ?? 0, published: e.published };
}

/** Nội dung ngắn của một câu để chiếu/đọc nhanh trên bảng điều phối. */
export async function fetchQuestionSnippets(examId: number): Promise<string[]> {
  const { data } = await getSupabase().from("exams_staff").select("questions").eq("id", examId).maybeSingle();
  const qs = ((data as { questions?: { question?: string }[] } | null)?.questions ?? []) as { question?: string }[];
  return qs.map((q) =>
    String(q.question ?? "")
      .replace(/<[^>]+>/g, " ")
      .replace(/\$[^$]*\$/g, "…")
      .replace(/\s+/g, " ")
      .trim()
      .slice(0, 90),
  );
}

/** Số phút gợi ý cho một chặng theo số câu (≈ 0,6 phút/câu, trong 5–20). */
export function suggestedMinutes(questionCount: number): number {
  return Math.min(20, Math.max(5, Math.round(questionCount * 0.6) || 10));
}
