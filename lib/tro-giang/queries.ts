import type { SessionPolicy } from "./policy";
import { getSupabase } from "@/services/supabase";

export type TaTier = "B1" | "B2" | "B3";
export type TaSessionType = "lop" | "phudao" | "chambai" | "hanhchinh" | "video";
export type TaSessionStatus = "submitted" | "approved" | "rejected";
export type TaVideoTier = "don_gian" | "dung_ky";

export interface TaAssistant {
  id: string;
  user_id: string;
  full_name: string;
  short_name: string;
  tier: TaTier;
  retained_rate: number | null;
  active: boolean;
  started_at: string;
}

export interface TaSessionRow {
  policy?: SessionPolicy;
  id: string;
  assistant_id: string;
  work_date: string;
  session_type: TaSessionType;
  class_label: string | null;
  start_time: string | null;
  end_time: string | null;
  hours: number | null;
  student_touches: number | null;
  touch_names: string[];
  error_note: string | null;
  error_note_at: string | null;
  homework_given: string | null;
  student_recap_ok: boolean | null;
  /** Danh sách em được phụ đạo trong buổi — số em quyết định hệ số quy đổi giờ. */
  phudao_students: string[];
  papers_graded: number | null;
  video_url: string | null;
  video_tier: TaVideoTier | null;
  published_at: string | null;
  topic_source_id: string | null;
  note: string | null;
  status: TaSessionStatus;
  reject_reason: string | null;
  created_at: string;
  approved_at: string | null;
}

/** Hồ sơ trợ giảng của người đang đăng nhập, null nếu tài khoản này chưa được đăng ký làm trợ giảng. */
export async function getMyAssistant(userId: string): Promise<TaAssistant | null> {
  const { data, error } = await getSupabase()
    .from("ta_assistants")
    .select("id, user_id, full_name, short_name, tier, retained_rate, active, started_at")
    .eq("user_id", userId)
    .maybeSingle();
  if (error) throw error;
  return data as TaAssistant | null;
}

export interface TaAssistantClass {
  class_id: number;
  name: string;
}

/** Các lớp trợ giảng được phân công — nguồn cho ô chọn lớp ở form ghi buổi. */
export async function fetchMyAssistantClasses(assistantId: string): Promise<TaAssistantClass[]> {
  const { data, error } = await getSupabase()
    .from("ta_assistant_classes")
    .select("class_id, classes(name)")
    .eq("assistant_id", assistantId);
  if (error) throw error;
  return (data ?? [])
    .map((row) => {
      const { class_id, classes } = row as {
        class_id: number;
        classes: { name: string } | { name: string }[] | null;
      };
      const joined = Array.isArray(classes) ? classes[0] : classes;
      return { class_id, name: joined?.name ?? `Lớp #${class_id}` };
    })
    .sort((a, b) => a.name.localeCompare(b.name, "vi"));
}

export interface NewSessionInput {
  policy?: SessionPolicy;
  assistant_id: string;
  work_date: string; // yyyy-mm-dd
  session_type: TaSessionType;
  class_label?: string | null;
  start_time?: string | null; // HH:mm
  end_time?: string | null; // HH:mm
  student_touches?: number | null;
  touch_names?: string[];
  error_note?: string | null;
  homework_given?: string | null;
  student_recap_ok?: boolean | null;
  phudao_students?: string[];
  /** Khớp thứ tự với phudao_students — buổi phụ đạo từ 01/10/2026 bắt buộc có. */
  phudao_student_ids?: string[];
  class_id?: number | null;
  papers_graded?: number | null;
  video_url?: string | null;
  video_tier?: TaVideoTier | null;
  published_at?: string | null; // ISO timestamptz
  topic_source_id?: string | null;
  note?: string | null;
}

/**
 * Ghi 1 buổi làm việc — status luôn khởi tạo 'submitted' (mặc định ở DB), không cho client set.
 * Trả về id của buổi để ghi tiếp chủ đề đã phụ đạo (tutoring_session_topics).
 */
export async function createSession(input: NewSessionInput): Promise<string> {
  const { data, error } = await getSupabase().from("ta_sessions").insert({
    ...(input.policy ? { policy: input.policy } : {}),
    assistant_id: input.assistant_id,
    work_date: input.work_date,
    session_type: input.session_type,
    class_label: input.class_label ?? null,
    start_time: input.start_time ?? null,
    end_time: input.end_time ?? null,
    student_touches: input.student_touches ?? null,
    touch_names: input.touch_names ?? [],
    error_note: input.error_note ?? null,
    homework_given: input.homework_given ?? null,
    student_recap_ok: input.student_recap_ok ?? null,
    phudao_students: input.phudao_students ?? [],
    phudao_student_ids: input.phudao_student_ids ?? [],
    class_id: input.class_id ?? null,
    papers_graded: input.papers_graded ?? null,
    video_url: input.video_url ?? null,
    video_tier: input.video_tier ?? null,
    published_at: input.published_at ?? null,
    topic_source_id: input.topic_source_id ?? null,
    note: input.note ?? null,
  }).select("id").single();
  if (error) throw error;
  return (data as { id: string }).id;
}

/** 1 gợi ý đề tài video lấy từ ta_video_topic_suggestions() — xem mục 8.4. */
export interface TaTopicSuggestion {
  session_id: string;
  work_date: string;
  class_label: string | null;
  error_note: string;
}

/** Lỗi lớp trong p_days ngày gần nhất của chính mình mà chưa bạn nào làm video. */
export async function fetchTopicSuggestions(days = 14): Promise<TaTopicSuggestion[]> {
  const { data, error } = await getSupabase().rpc("ta_video_topic_suggestions", { p_days: days });
  if (error) throw error;
  return (data ?? []) as TaTopicSuggestion[];
}

export async function fetchTopicSuggestion(sessionId: string): Promise<TaTopicSuggestion | null> {
  const rows = await fetchTopicSuggestions();
  return rows.find((r) => r.session_id === sessionId) ?? null;
}

export interface TaVideoRates {
  effective_from: string;
  price_don_gian: number;
  price_dung_ky: number;
  view_threshold_1: number;
  view_bonus_1: number;
  view_threshold_2: number;
  view_bonus_2: number;
  lead_bonus: number;
  monthly_budget_cap: number;
}

/** Bảng giá đang hiệu lực tại tháng chỉ định — dùng để hiện mốc thưởng, không viết cứng số. */
export async function fetchVideoRates(month: string): Promise<TaVideoRates | null> {
  const { data, error } = await getSupabase()
    .from("ta_video_rates")
    .select(
      "effective_from, price_don_gian, price_dung_ky, view_threshold_1, view_bonus_1, view_threshold_2, view_bonus_2, lead_bonus, monthly_budget_cap",
    )
    .lte("effective_from", month)
    .order("effective_from", { ascending: false })
    .limit(1)
    .maybeSingle();
  if (error) throw error;
  return (data ?? null) as TaVideoRates | null;
}

/** 1 hàng trả về từ ta_monthly_score() — nguồn tính điểm/lương duy nhất, xem mục 4 của đề bài. */
export interface TaMonthlyScore {
  assistant_id: string;
  month: string;
  lop_sessions: number;
  phudao_sessions: number;
  avg_touches: number;
  touches_score: number;
  ontime_error_notes: number;
  error_note_rate: number;
  error_note_score: number;
  complete_phudao: number;
  phudao_complete_rate: number;
  phudao_score: number;
  flag_count: number;
  focus_score: number;
  total_score: number;
  bonus_per_hour: number;
  converted_hours: number;
  papers_graded: number;
  base_pay: number;
  bonus_pay: number;
  grading_pay: number;
  total_pay: number;
}

/** month: ngày 1 của tháng cần tính, dạng yyyy-mm-dd. */
export async function getMonthlyScore(assistantId: string, month: string): Promise<TaMonthlyScore> {
  const { data, error } = await getSupabase().rpc("ta_monthly_score", {
    p_assistant_id: assistantId,
    p_month: month,
  });
  if (error) throw error;
  const rows = (data ?? []) as TaMonthlyScore[];
  return rows[0];
}

/** Giờ tích lũy trọn đời (lop+phudao đã duyệt) — dùng để xét lên bậc. */
export async function getAccruedHours(assistantId: string): Promise<number> {
  const { data, error } = await getSupabase().rpc("ta_accrued_hours", {
    p_assistant_id: assistantId,
  });
  if (error) throw error;
  return (data ?? 0) as number;
}

export interface TaSessionListItem {
  id: string;
  work_date: string;
  session_type: TaSessionType;
  class_label: string | null;
  phudao_students: string[];
  hours: number | null;
  student_touches: number | null;
  papers_graded: number | null;
  status: TaSessionStatus;
  reject_reason: string | null;
}

export async function fetchRecentSessions(assistantId: string, limit = 10): Promise<TaSessionListItem[]> {
  const { data, error } = await getSupabase()
    .from("ta_sessions")
    .select("id, work_date, session_type, class_label, phudao_students, hours, student_touches, papers_graded, status, reject_reason")
    .eq("assistant_id", assistantId)
    .order("work_date", { ascending: false })
    .order("created_at", { ascending: false })
    .limit(limit);
  if (error) throw error;
  return (data ?? []) as TaSessionListItem[];
}

// ============================================================
// Khu quản trị (giáo viên) — mọi hàm dưới đây chỉ chạy được với tài khoản role='admin',
// RLS và các hàm SECURITY DEFINER tự chặn phía DB.
// ============================================================

export async function fetchAssistants(): Promise<TaAssistant[]> {
  const { data, error } = await getSupabase()
    .from("ta_assistants")
    .select("id, user_id, full_name, short_name, tier, retained_rate, active, started_at")
    .order("short_name");
  if (error) throw error;
  return (data ?? []) as TaAssistant[];
}

export interface TaPendingSession extends TaSessionListItem {
  policy?: SessionPolicy;
  assistant_id: string;
  assistant_name: string;
  touch_names: string[];
  error_note: string | null;
  homework_given: string | null;
  student_recap_ok: boolean | null;
  phudao_students: string[];
  video_url: string | null;
  video_tier: TaVideoTier | null;
  note: string | null;
}

/** Hàng chờ duyệt của toàn đội, mới nhất trước. */
export async function fetchPendingSessions(): Promise<TaPendingSession[]> {
  const { data, error } = await getSupabase()
    .from("ta_sessions")
    .select(
      "*, ta_assistants(short_name)",
    )
    .eq("status", "submitted")
    .order("work_date", { ascending: false });
  if (error) throw error;
  return (data ?? []).map((row) => {
    const { ta_assistants: joined, ...rest } = row as Record<string, unknown> & {
      ta_assistants: { short_name: string } | { short_name: string }[] | null;
    };
    const assistant = Array.isArray(joined) ? joined[0] : joined;
    return { ...rest, assistant_name: assistant?.short_name ?? "—" } as TaPendingSession;
  });
}

export async function approveSessions(ids: string[]): Promise<void> {
  if (ids.length === 0) return;
  const { error } = await getSupabase()
    .from("ta_sessions")
    .update({ status: "approved", approved_at: new Date().toISOString(), reject_reason: null })
    .in("id", ids);
  if (error) throw error;
}

export async function rejectSession(id: string, reason: string): Promise<void> {
  const { error } = await getSupabase()
    .from("ta_sessions")
    .update({ status: "rejected", reject_reason: reason })
    .eq("id", id);
  if (error) throw error;
}

/**
 * Trung bình lượt chạm trên các buổi 'lop' ĐÃ DUYỆT của từng trợ giảng — dùng để đánh dấu
 * buổi có số chạm bất thường cao so với chính bạn đó (đối chiếu ngẫu nhiên, không phải nghi ngờ).
 */
export async function fetchTouchBaselines(): Promise<Map<string, number>> {
  const { data, error } = await getSupabase()
    .from("ta_sessions")
    .select("assistant_id, student_touches")
    .eq("session_type", "lop")
    .eq("status", "approved")
    .not("student_touches", "is", null);
  if (error) throw error;
  const sums = new Map<string, { total: number; count: number }>();
  for (const row of (data ?? []) as { assistant_id: string; student_touches: number }[]) {
    const cur = sums.get(row.assistant_id) ?? { total: 0, count: 0 };
    cur.total += row.student_touches;
    cur.count += 1;
    sums.set(row.assistant_id, cur);
  }
  return new Map([...sums].map(([id, { total, count }]) => [id, total / count]));
}

export async function createFlag(assistantId: string, note: string, flagDate: string): Promise<void> {
  const { error } = await getSupabase()
    .from("ta_flags")
    .insert({ assistant_id: assistantId, note: note || null, flag_date: flagDate });
  if (error) throw error;
}

export interface TaTeamMonthlyHours {
  month: string;
  converted_hours: number;
  session_count: number;
}

export async function fetchTeamMonthlyHours(months = 12): Promise<TaTeamMonthlyHours[]> {
  const { data, error } = await getSupabase().rpc("ta_team_monthly_hours", { p_months: months });
  if (error) throw error;
  return (data ?? []) as TaTeamMonthlyHours[];
}

export async function fetchCourseTotalHours(): Promise<number> {
  const { data, error } = await getSupabase().rpc("ta_course_total_hours");
  if (error) throw error;
  return (data ?? 0) as number;
}

export async function fetchHoursCap(): Promise<number> {
  const { data, error } = await getSupabase()
    .from("ta_settings")
    .select("course_hours_cap")
    .eq("id", true)
    .maybeSingle();
  if (error) throw error;
  return (data?.course_hours_cap ?? 1000) as number;
}

export async function updateHoursCap(cap: number): Promise<void> {
  const { error } = await getSupabase()
    .from("ta_settings")
    .update({ course_hours_cap: cap, updated_at: new Date().toISOString() })
    .eq("id", true);
  if (error) throw error;
}

// ---------- Mảng video (mục 8) ----------

export interface TaVideoLedgerRow {
  session_id: string;
  assistant_id: string;
  work_date: string;
  video_tier: TaVideoTier | null;
  video_url: string | null;
  published_at: string | null;
  status: TaSessionStatus;
  reject_reason: string | null;
  topic_source_id: string | null;
  latest_checked_at: string | null;
  latest_views: number;
  latest_saves: number;
  latest_comments: number;
  view_bonus: number;
  production_pay: number;
  lead_count: number;
  lead_bonus: number;
  total_pay: number;
}

/** assistantId = null → toàn đội (chỉ giáo viên gọi được). */
export async function fetchVideoLedger(assistantId: string | null = null): Promise<TaVideoLedgerRow[]> {
  const { data, error } = await getSupabase().rpc("ta_video_ledger", { p_assistant_id: assistantId });
  if (error) throw error;
  return (data ?? []) as TaVideoLedgerRow[];
}

/** Ghi số liệu tuần cho 1 video — trùng (video, ngày) thì ghi đè. */
export async function upsertVideoStats(input: {
  session_id: string;
  checked_at: string;
  views: number;
  saves: number;
  comments: number;
}): Promise<void> {
  const { error } = await getSupabase()
    .from("ta_video_stats")
    .upsert(input, { onConflict: "session_id,checked_at" });
  if (error) throw error;
}

export async function createLead(input: {
  student_name: string;
  source: string;
  attributed_session_id: string | null;
  registered_at: string;
}): Promise<void> {
  const { error } = await getSupabase().from("ta_leads").insert(input);
  if (error) throw error;
}

export interface TaVideoAdminSummary {
  month: string;
  videos_published: number;
  total_views: number;
  total_saves: number;
  total_comments: number;
  leads_count: number;
  production_spend: number;
  view_bonus_spend: number;
  lead_bonus_spend: number;
  total_spend: number;
  budget_cap: number;
  over_budget: boolean;
  cost_per_lead: number | null;
}

export async function fetchVideoAdminSummary(month: string): Promise<TaVideoAdminSummary> {
  const { data, error } = await getSupabase().rpc("ta_video_admin_summary", { p_month: month });
  if (error) throw error;
  return ((data ?? []) as TaVideoAdminSummary[])[0];
}

export interface TaTopicExploitation {
  eligible_count: number;
  used_count: number;
  rate: number;
}

export async function fetchTopicExploitationRate(days = 14): Promise<TaTopicExploitation> {
  const { data, error } = await getSupabase().rpc("ta_topic_exploitation_rate", { p_days: days });
  if (error) throw error;
  return ((data ?? []) as TaTopicExploitation[])[0];
}
