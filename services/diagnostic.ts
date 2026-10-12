import { getSupabase } from "./supabase";

/** Một bài trong kết quả kiểm tra đầu vào: đúng `correct`/`total` câu. */
export interface DiagnosticTopicResult {
  topicId: number;
  correct: number;
  total: number;
}

export interface DiagnosticStatus {
  done: boolean;
  createdAt?: string;
  needCount?: number;
  perTopic?: DiagnosticTopicResult[];
}

/** Số bài tối đa mỗi lượt và số câu mỗi bài (thầy chốt 12/10/2026: ~15–18 câu, 5–6 bài). */
export const DIAGNOSTIC_MAX_TOPICS = 6;
export const DIAGNOSTIC_QUESTIONS_PER_TOPIC = 3;
/** Sai từ ngần này câu trong một bài thì dừng bài đó, không bắt làm hết. */
export const DIAGNOSTIC_STOP_AFTER_WRONG = 2;

export async function fetchDiagnostic(studentId: string): Promise<DiagnosticStatus> {
  const { data, error } = await getSupabase().rpc("diagnostic_get", { p_student: studentId });
  if (error) throw new Error(error.message);
  const d = data as { done: boolean; createdAt?: string; needCount?: number; perTopic?: DiagnosticTopicResult[] };
  return d;
}

export async function submitDiagnostic(studentId: string, results: DiagnosticTopicResult[]): Promise<number> {
  const { data, error } = await getSupabase().rpc("diagnostic_submit", { p_student: studentId, p_results: results });
  if (error) throw new Error(error.message);
  return (data as { needCount: number }).needCount;
}

/** Thầy / trợ giảng cho em làm lại. */
export async function resetDiagnostic(studentId: string): Promise<void> {
  const { error } = await getSupabase().rpc("diagnostic_reset", { p_student: studentId });
  if (error) throw new Error(error.message);
}
