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

export interface NewSessionInput {
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
  papers_graded?: number | null;
  video_url?: string | null;
  video_tier?: TaVideoTier | null;
  published_at?: string | null; // ISO timestamptz
  topic_source_id?: string | null;
  note?: string | null;
}

/** Ghi 1 buổi làm việc — status luôn khởi tạo 'submitted' (mặc định ở DB), không cho client set. */
export async function createSession(input: NewSessionInput): Promise<void> {
  const { error } = await getSupabase().from("ta_sessions").insert({
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
    papers_graded: input.papers_graded ?? null,
    video_url: input.video_url ?? null,
    video_tier: input.video_tier ?? null,
    published_at: input.published_at ?? null,
    topic_source_id: input.topic_source_id ?? null,
    note: input.note ?? null,
  });
  if (error) throw error;
}

/** 1 gợi ý đề tài video lấy từ ta_video_topic_suggestions() — xem mục 8.4. */
export interface TaTopicSuggestion {
  session_id: string;
  work_date: string;
  class_label: string | null;
  error_note: string;
}

export async function fetchTopicSuggestion(sessionId: string): Promise<TaTopicSuggestion | null> {
  const { data, error } = await getSupabase().rpc("ta_video_topic_suggestions");
  if (error) throw error;
  const rows = (data ?? []) as TaTopicSuggestion[];
  return rows.find((r) => r.session_id === sessionId) ?? null;
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
  hours: number | null;
  student_touches: number | null;
  papers_graded: number | null;
  status: TaSessionStatus;
  reject_reason: string | null;
}

export async function fetchRecentSessions(assistantId: string, limit = 10): Promise<TaSessionListItem[]> {
  const { data, error } = await getSupabase()
    .from("ta_sessions")
    .select("id, work_date, session_type, class_label, hours, student_touches, papers_graded, status, reject_reason")
    .eq("assistant_id", assistantId)
    .order("work_date", { ascending: false })
    .order("created_at", { ascending: false })
    .limit(limit);
  if (error) throw error;
  return (data ?? []) as TaSessionListItem[];
}
