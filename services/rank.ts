// Hệ thống rank (RP theo mùa + danh hiệu) — mọi tính toán nằm trong Postgres
// (docs/supabase-migration-rank-system.sql); ở đây chỉ gọi RPC và đọc bảng cấu hình.

import type { ExamQuestion } from "@/features/exams/types";
import type {
  ClassRankBoard,
  ClassRankGroups,
  FixQuizResult,
  FixQuizStart,
  FixableTopic,
  RankLedgerEntry,
  RankSeasonSummary,
  RankStatus,
  RankTitle,
  TierCode,
  TitleLevel,
} from "@/features/rank/types";
import { getSupabase } from "@/services/supabase";
import { isStudentPreview, unlockBoard, unlockSeasons, unlockStatus, unlockTitles } from "@/features/rank/preview";

// ============================================================
// Học sinh / phụ huynh / giáo viên xem
// ============================================================
export async function fetchMyRankStatus(): Promise<RankStatus | null> {
  const { data, error } = await getSupabase().rpc("rank_my_status");
  if (error) throw error;
  const status = (data as RankStatus | null) ?? null;
  // Admin đang "Xem như học sinh" → mở khoá hết (Vô Song, 45 danh hiệu, chuỗi ngày…), xem features/rank/preview.ts.
  return isStudentPreview() ? unlockStatus(status) : status;
}

export async function fetchRankStatusOf(studentId: string): Promise<RankStatus | null> {
  const { data, error } = await getSupabase().rpc("rank_status_of", { p_student: studentId });
  if (error) throw error;
  return (data as RankStatus | null) ?? null;
}

export async function fetchMyTitles(): Promise<RankTitle[]> {
  const { data, error } = await getSupabase().rpc("rank_my_titles");
  if (error) throw error;
  const titles = (data as RankTitle[] | null) ?? [];
  return isStudentPreview() ? unlockTitles(titles) : titles;
}

export async function fetchTitlesOf(studentId: string): Promise<RankTitle[]> {
  const { data, error } = await getSupabase().rpc("rank_titles_of", { p_student: studentId });
  if (error) throw error;
  return (data as RankTitle[] | null) ?? [];
}

export async function fetchLedgerOf(studentId: string, seasonId: number | null = null, limit = 50): Promise<RankLedgerEntry[]> {
  const { data, error } = await getSupabase().rpc("rank_ledger_of", {
    p_student: studentId,
    p_season: seasonId,
    p_limit: limit,
  });
  if (error) throw error;
  return (data as RankLedgerEntry[] | null) ?? [];
}

export async function fetchSeasonsOf(studentId: string): Promise<RankSeasonSummary[]> {
  const { data, error } = await getSupabase().rpc("rank_seasons_of", { p_student: studentId });
  if (error) throw error;
  const seasons = (data as RankSeasonSummary[] | null) ?? [];
  return isStudentPreview() ? unlockSeasons(seasons) : seasons;
}

export async function setDisplayTitle(code: string | null, level: TitleLevel | null): Promise<void> {
  const { error } = await getSupabase().rpc("rank_set_display_title", { p_code: code, p_level: level });
  if (error) throw error;
}

export async function fetchClassRankGroups(classId: number): Promise<ClassRankGroups | null> {
  const { data, error } = await getSupabase().rpc("rank_class_groups", { p_class_id: classId });
  if (error) throw error;
  return (data as ClassRankGroups | null) ?? null;
}

export async function fetchClassRankBoard(classId: number): Promise<ClassRankBoard | null> {
  const sb = getSupabase();
  const { data, error } = await sb.rpc("rank_class_board", { p_class_id: classId });
  if (error) throw error;
  const board = (data as ClassRankBoard | null) ?? null;
  if (!isStudentPreview()) return board;
  const { data: u } = await sb.auth.getUser();
  const { data: p } = u?.user
    ? await sb.from("profiles").select("full_name, avatar_url").eq("id", u.user.id).maybeSingle()
    : { data: null };
  return unlockBoard(board, p?.full_name ?? "Em", p?.avatar_url ?? null);
}

// ============================================================
// Sửa sai để nhận RP
// ============================================================
export async function startFixQuiz(resultId: number, topicId: number): Promise<FixQuizStart> {
  const { data, error } = await getSupabase().rpc("rank_fix_quiz_start", {
    p_exam_result_id: resultId,
    p_topic_id: topicId,
  });
  if (error) throw new Error(error.message);
  const d = data as {
    attempt_id: number;
    topic_name: string;
    total: number;
    attempts_left: number;
    pass_pct: number;
    questions: ExamQuestion[];
  };
  return {
    attemptId: d.attempt_id,
    topicName: d.topic_name,
    total: d.total,
    attemptsLeft: d.attempts_left,
    passPct: d.pass_pct,
    questions: d.questions ?? [],
  };
}

export async function submitFixQuiz(attemptId: number, correct: number): Promise<FixQuizResult> {
  const { data, error } = await getSupabase().rpc("rank_fix_quiz_submit", {
    p_attempt_id: attemptId,
    p_correct: correct,
  });
  if (error) throw new Error(error.message);
  const d = data as { pct: number; passed: boolean; rp_delta: number; fixed_topics: number; wrong_topics: number };
  return { pct: d.pct, passed: d.passed, rpDelta: d.rp_delta, fixedTopics: d.fixed_topics, wrongTopics: d.wrong_topics };
}

/** Các chủ đề (tầng bài) em làm sai trong một bài — kèm số lượt sửa sai đã dùng. */
interface TopicRef {
  id: number;
  parent_id: number | null;
  name: string;
}
type TopicEmbed = (TopicRef & { parent?: TopicRef | TopicRef[] | null }) | (TopicRef & { parent?: TopicRef | TopicRef[] | null })[] | null;

function firstOf<T>(v: T | T[] | null | undefined): T | undefined {
  return Array.isArray(v) ? v[0] : (v ?? undefined);
}

export async function fetchFixableTopics(resultId: number): Promise<FixableTopic[]> {
  const supabase = getSupabase();
  // Chủ đề + chủ đề cha nhúng thẳng vào từng câu (FK topic_id → question_topics, parent_id tự tham chiếu)
  // và bảng lượt sửa sai chạy song song: 1 tầng thay vì 4 tầng nối tiếp.
  const [{ data: rows, error }, { data: attempts }] = await Promise.all([
    supabase
      .from("exam_question_results")
      .select("topic_id, is_correct, topic:topic_id(id, parent_id, name, parent:parent_id(id, parent_id, name))")
      .eq("exam_result_id", resultId),
    supabase.from("rank_fix_attempts").select("topic_id, status, passed").eq("exam_result_id", resultId),
  ]);
  if (error) throw error;
  const ids = Array.from(new Set((rows ?? []).map((r) => r.topic_id as number | null).filter((x): x is number => x !== null)));
  if (ids.length === 0) return [];

  const byId = new Map<number, TopicRef>();
  for (const r of rows ?? []) {
    const t = firstOf(r.topic as unknown as TopicEmbed);
    if (!t) continue;
    byId.set(t.id, { id: t.id, parent_id: t.parent_id, name: t.name });
    const parent = firstOf(t.parent);
    if (parent && !byId.has(parent.id)) byId.set(parent.id, { id: parent.id, parent_id: parent.parent_id, name: parent.name });
  }

  const agg = new Map<number, { wrong: number; total: number }>();
  for (const r of rows ?? []) {
    const t = byId.get(r.topic_id as number);
    if (!t) continue;
    const lessonId = t.parent_id ?? t.id;
    const cur = agg.get(lessonId) ?? { wrong: 0, total: 0 };
    cur.total += 1;
    if (!r.is_correct) cur.wrong += 1;
    agg.set(lessonId, cur);
  }

  const done = new Map<number, { count: number; passed: boolean }>();
  for (const a of attempts ?? []) {
    const cur = done.get(a.topic_id as number) ?? { count: 0, passed: false };
    if (a.status === "done") cur.count += 1;
    if (a.passed) cur.passed = true;
    done.set(a.topic_id as number, cur);
  }

  return Array.from(agg.entries())
    .filter(([, v]) => v.wrong > 0)
    .map(([topicId, v]) => ({
      topicId,
      name: byId.get(topicId)?.name ?? `Chủ đề #${topicId}`,
      wrong: v.wrong,
      total: v.total,
      attemptsDone: done.get(topicId)?.count ?? 0,
      passed: done.get(topicId)?.passed ?? false,
    }))
    .sort((a, b) => b.wrong - a.wrong || a.name.localeCompare(b.name, "vi"));
}

export interface ResultRpContext {
  seasonId: number;
  seasonName: string;
  sourceEnabled: boolean;
  maxRp: number;
  fixMaxRp: number;
  practiceRp: number;
  fixRp: number;
}

/**
 * RP đã nhận từ một bài làm (bài luyện tập + sửa sai) trong mùa hiện tại; null = chưa mở mùa.
 * `status`: trạng thái rank đã tải sẵn (fetchMyRankStatus) — truyền vào để khỏi gọi RPC lại; bỏ trống thì tự tải.
 */
export async function fetchResultRpContext(
  resultId: number,
  examId: number,
  status?: RankStatus | null,
): Promise<ResultRpContext | null> {
  if (status === undefined) status = await fetchMyRankStatus();
  if (!status?.season) return null;
  const supabase = getSupabase();
  const [{ data: src }, { data: awards }, { data: season }] = await Promise.all([
    supabase.from("rank_sources").select("max_rp, enabled").eq("season_id", status.season.id).eq("source_kind", "exam").eq("source_id", examId).maybeSingle(),
    supabase
      .from("rank_rp_awards")
      .select("source_kind, source_ref, awarded")
      .eq("season_id", status.season.id)
      .in("source_ref", [`exam:${examId}`, `exam_result:${resultId}`]),
    supabase.from("rank_seasons").select("config").eq("id", status.season.id).maybeSingle(),
  ]);
  const cfg = (season?.config ?? {}) as Record<string, number | string>;
  let practiceRp = 0;
  let fixRp = 0;
  for (const a of awards ?? []) {
    if (a.source_kind === "practice") practiceRp = a.awarded as number;
    if (a.source_kind === "fix") fixRp = a.awarded as number;
  }
  return {
    seasonId: status.season.id,
    seasonName: status.season.name,
    sourceEnabled: !!src?.enabled,
    maxRp: (src?.max_rp as number | undefined) ?? 0,
    fixMaxRp: Number(cfg.fix_max_rp ?? 10),
    practiceRp,
    fixRp,
  };
}

// ============================================================
// Giáo viên — cấu hình
// ============================================================
export interface RankSeason {
  id: number;
  name: string;
  starts_on: string;
  ends_on: string;
  class_ids: number[];
  status: "draft" | "active" | "closed";
  config: Record<string, number>;
  boss_exam_id: number | null;
  boss_pass_score: number | null;
  closed_at: string | null;
  created_at: string;
}

const SEASON_COLS = "id, name, starts_on, ends_on, class_ids, status, config, boss_exam_id, boss_pass_score, closed_at, created_at";

export async function fetchSeasons(): Promise<RankSeason[]> {
  const { data, error } = await getSupabase().from("rank_seasons").select(SEASON_COLS).order("starts_on", { ascending: false });
  if (error) throw error;
  return (data ?? []) as RankSeason[];
}

export async function createSeason(input: { name: string; startsOn: string; endsOn: string; classIds: number[]; activate: boolean }): Promise<number> {
  const { data, error } = await getSupabase().rpc("rank_create_season", {
    p_name: input.name,
    p_starts: input.startsOn,
    p_ends: input.endsOn,
    p_class_ids: input.classIds,
    p_activate: input.activate,
  });
  if (error) throw new Error(error.message);
  return data as number;
}

export async function updateSeason(id: number, patch: Partial<Omit<RankSeason, "id" | "created_at">>): Promise<void> {
  const { error } = await getSupabase().from("rank_seasons").update(patch).eq("id", id);
  if (error) throw new Error(error.message);
}

export interface RankTierRow {
  season_id: number;
  code: TierCode;
  sort: number;
  name: string;
  min_rp: number;
  has_divisions: boolean;
  required_title_count: number;
  required_title_level: TitleLevel | null;
  challenge_exam_id: number | null;
  challenge_pass_score: number | null;
}

export async function fetchTiers(seasonId: number): Promise<RankTierRow[]> {
  const { data, error } = await getSupabase()
    .from("rank_tiers")
    .select("season_id, code, sort, name, min_rp, has_divisions, required_title_count, required_title_level, challenge_exam_id, challenge_pass_score")
    .eq("season_id", seasonId)
    .order("sort");
  if (error) throw error;
  return (data ?? []) as RankTierRow[];
}

export async function updateTier(seasonId: number, code: TierCode, patch: Partial<RankTierRow>): Promise<void> {
  const { error } = await getSupabase().from("rank_tiers").update(patch).eq("season_id", seasonId).eq("code", code);
  if (error) throw new Error(error.message);
}

export interface RankSourceRow {
  season_id: number;
  source_kind: "practice_item" | "exam";
  source_id: number;
  max_rp: number;
  enabled: boolean;
}

export async function fetchSources(seasonId: number): Promise<RankSourceRow[]> {
  const { data, error } = await getSupabase()
    .from("rank_sources")
    .select("season_id, source_kind, source_id, max_rp, enabled")
    .eq("season_id", seasonId);
  if (error) throw error;
  return (data ?? []) as RankSourceRow[];
}

export async function upsertSources(rows: RankSourceRow[]): Promise<void> {
  if (rows.length === 0) return;
  const { error } = await getSupabase().from("rank_sources").upsert(rows, { onConflict: "season_id,source_kind,source_id" });
  if (error) throw new Error(error.message);
}

export interface SourceCandidate {
  kind: "practice_item" | "exam";
  id: number;
  title: string;
  itemKind: "luyen_tap" | "bai_tap_ve_nha" | "kiem_tra";
  lessonId: number;
  lessonTitle: string;
  chapterId: number;
  chapterTitle: string;
  /** rỗng = toàn trường */
  classIds: number[];
}

/** Mọi mục luyện tập / BTVN / kiểm tra trong các bài học — để giáo viên chọn bài tính RP. */
export async function fetchSourceCandidates(): Promise<SourceCandidate[]> {
  const supabase = getSupabase();
  const [{ data: items }, { data: lessons }, { data: chapters }, { data: chapterClasses }] = await Promise.all([
    supabase.from("lesson_items").select("id, lesson_id, kind, title, exam_ids").in("kind", ["luyen_tap", "bai_tap_ve_nha", "kiem_tra"]).order("sort_order"),
    supabase.from("lessons").select("id, chapter_id, title, sort_order"),
    supabase.from("chapters").select("id, title, sort_order"),
    supabase.from("chapter_classes").select("chapter_id, class_id"),
  ]);
  const lessonById = new Map((lessons ?? []).map((l) => [l.id as number, l as { id: number; chapter_id: number; title: string; sort_order: number }]));
  const chapterById = new Map((chapters ?? []).map((c) => [c.id as number, c as { id: number; title: string; sort_order: number }]));
  const classesByChapter = new Map<number, number[]>();
  for (const cc of chapterClasses ?? []) {
    const list = classesByChapter.get(cc.chapter_id as number) ?? [];
    list.push(cc.class_id as number);
    classesByChapter.set(cc.chapter_id as number, list);
  }
  const examIds = new Set<number>();
  for (const it of items ?? []) for (const e of (it.exam_ids as number[] | null) ?? []) examIds.add(e);
  const examTitle = new Map<number, string>();
  if (examIds.size) {
    const { data: exams } = await supabase.from("exams").select("id, title").in("id", Array.from(examIds));
    for (const e of exams ?? []) examTitle.set(e.id as number, e.title as string);
  }

  const out: SourceCandidate[] = [];
  for (const it of items ?? []) {
    const lesson = lessonById.get(it.lesson_id as number);
    if (!lesson) continue;
    const chapter = chapterById.get(lesson.chapter_id);
    if (!chapter) continue;
    const base = {
      itemKind: it.kind as SourceCandidate["itemKind"],
      lessonId: lesson.id,
      lessonTitle: lesson.title,
      chapterId: chapter.id,
      chapterTitle: chapter.title,
      classIds: classesByChapter.get(chapter.id) ?? [],
    };
    if (it.kind === "luyen_tap") {
      out.push({ kind: "practice_item", id: it.id as number, title: (it.title as string) || "Luyện tập", ...base });
    } else {
      for (const e of (it.exam_ids as number[] | null) ?? []) {
        out.push({ kind: "exam", id: e, title: examTitle.get(e) ?? `Đề #${e}`, ...base });
      }
    }
  }
  out.sort((a, b) => {
    const ca = chapterById.get(a.chapterId)!.sort_order - chapterById.get(b.chapterId)!.sort_order;
    if (ca) return ca;
    const la = lessonById.get(a.lessonId)!.sort_order - lessonById.get(b.lessonId)!.sort_order;
    return la || a.title.localeCompare(b.title, "vi");
  });
  return out;
}

export interface RankTitleRow {
  code: string;
  group_code: string;
  kind: "specialist" | "collection" | "achievement";
  name: string;
  description: string;
  sort: number;
  min_questions: number;
  awaken_accuracy: number;
  master_accuracy: number;
  legend_challenge_exam_id: number | null;
  legend_accuracy: number;
  requires: Record<string, unknown>;
  enabled: boolean;
}

export async function fetchTitleRows(): Promise<RankTitleRow[]> {
  const { data, error } = await getSupabase()
    .from("rank_titles")
    .select(
      "code, group_code, kind, name, description, sort, min_questions, awaken_accuracy, master_accuracy, legend_challenge_exam_id, legend_accuracy, requires, enabled",
    )
    .order("sort");
  if (error) throw error;
  return (data ?? []) as RankTitleRow[];
}

export async function updateTitleRow(code: string, patch: Partial<RankTitleRow>): Promise<void> {
  const { error } = await getSupabase().from("rank_titles").update(patch).eq("code", code);
  if (error) throw new Error(error.message);
}

export async function fetchTitleTopicMap(): Promise<Map<string, number[]>> {
  const { data, error } = await getSupabase().from("rank_title_topics").select("title_code, topic_id");
  if (error) throw error;
  const map = new Map<string, number[]>();
  for (const r of data ?? []) {
    const list = map.get(r.title_code as string) ?? [];
    list.push(r.topic_id as number);
    map.set(r.title_code as string, list);
  }
  return map;
}

export async function setTitleTopics(code: string, topicIds: number[]): Promise<void> {
  const supabase = getSupabase();
  const del = await supabase.from("rank_title_topics").delete().eq("title_code", code);
  if (del.error) throw new Error(del.error.message);
  if (topicIds.length === 0) return;
  const ins = await supabase.from("rank_title_topics").insert(topicIds.map((topic_id) => ({ title_code: code, topic_id })));
  if (ins.error) throw new Error(ins.error.message);
}

export interface SeasonOverviewRow {
  student_id: string;
  full_name: string;
  class_names: string | null;
  rp: number;
  tier_code: TierCode;
  tier_sort: number;
  division: number | null;
  titles_count: number;
  last_award_at: string | null;
  /** Tên bậc đủ RP nhưng đang kẹt điều kiện, null = không kẹt. */
  pending_gate: string | null;
}

export async function fetchSeasonOverview(seasonId: number): Promise<SeasonOverviewRow[]> {
  const { data, error } = await getSupabase().rpc("rank_season_overview", { p_season: seasonId });
  if (error) throw error;
  return (data as SeasonOverviewRow[] | null) ?? [];
}

export async function adjustRp(seasonId: number, studentId: string, delta: number, reason: string): Promise<void> {
  const { error } = await getSupabase().rpc("rank_adjust_rp", {
    p_season: seasonId,
    p_student: studentId,
    p_delta: delta,
    p_reason: reason,
  });
  if (error) throw new Error(error.message);
}

export async function closeSeason(seasonId: number): Promise<number> {
  const { data, error } = await getSupabase().rpc("rank_close_season", { p_season: seasonId });
  if (error) throw new Error(error.message);
  return (data as number) ?? 0;
}

export async function recomputeSeason(seasonId: number): Promise<number> {
  const { data, error } = await getSupabase().rpc("rank_recompute_season", { p_season: seasonId });
  if (error) throw new Error(error.message);
  return (data as number) ?? 0;
}

export async function recomputeStudent(seasonId: number, studentId: string): Promise<void> {
  const { error } = await getSupabase().rpc("rank_recompute_student", { p_season: seasonId, p_student: studentId });
  if (error) throw new Error(error.message);
}

// ---------- Lộ trình bậc (học sinh xem trước toàn bộ huy hiệu + điều kiện) ----------
export interface TierLadderStep extends RankTierRow {
  /** Ngưỡng RP của bậc kế trên; null = bậc cao nhất. */
  next_min: number | null;
  challenge_title: string | null;
}

/** Toàn bộ bậc của một mùa kèm tên đề thử thách — policy "anyone reads rank_tiers" cho phép học sinh đọc. */
export async function fetchTierLadder(seasonId: number): Promise<TierLadderStep[]> {
  const tiers = await fetchTiers(seasonId);
  const examIds = tiers.map((t) => t.challenge_exam_id).filter((id): id is number => id !== null);
  const titles = new Map<number, string>();
  if (examIds.length > 0) {
    const { data } = await getSupabase().from("exams").select("id, title").in("id", examIds);
    for (const e of data ?? []) titles.set(e.id as number, e.title as string);
  }
  return tiers.map((t, i) => ({
    ...t,
    next_min: tiers[i + 1]?.min_rp ?? null,
    challenge_title: t.challenge_exam_id !== null ? (titles.get(t.challenge_exam_id) ?? null) : null,
  }));
}
