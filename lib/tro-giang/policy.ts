import { getSupabase } from '@/services/supabase';
import type { TaSessionRow } from './queries';

export const POLICY_START = '2026-10-01';
export const POLICY_SCORES = [
  ['touches', 'Tiếp xúc trên lớp', 30],
  ['phudao', 'Chất lượng phụ đạo', 25],
  ['homework', 'Kiểm tra bài tập về nhà', 20],
  ['attendance', 'Chuyên cần', 15],
  ['observation', 'Thầy quan sát', 10],
] as const;
export type ScoreKey = typeof POLICY_SCORES[number][0];
export interface SessionPolicy {
  attendance: 'on_time' | 'late' | 'excused_absence' | 'unexcused_absence';
  arrived_early: boolean;
  homework_checked: boolean;
  homework_missing: number;
  walked_tables: boolean;
  reported_students: boolean;
  attention_note: string;
  teaching_minutes: number;
  teaching_note: string;
  prepared: boolean;
  recalled: boolean;
  asked_each: boolean;
  followups: { student: string; lesson: string; difficulty: string }[];
}
export function emptyPolicy(): SessionPolicy {
  return { attendance: 'on_time', arrived_early: false, homework_checked: false, homework_missing: 0, walked_tables: false, reported_students: false, attention_note: '', teaching_minutes: 0, teaching_note: '', prepared: false, recalled: false, asked_each: false, followups: [] };
}
export function tutoringFactor(count: number) { return count < 1 || count > 4 ? null : count <= 2 ? 1.2 : 1.4; }
export interface MonthPolicy extends Record<ScoreKey, number | null> {
  assistant_id: string; month: string; closed_at: string | null; note: string;
  overrides: Partial<Record<ScoreKey, number | null>>;
  total_score: number | null; hourly_rate: number | null; class_factor: number | null;
  class_count: number; tutoring_count: number; pending_count: number;
  class_hours: number; teaching_hours: number; tutoring_hours: number; tutoring_weighted_hours: number; papers: number;
  class_pay: number | null; teaching_pay: number | null; tutoring_pay: number | null; grading_pay: number; total_pay: number | null;
  missing: string[]; trial: boolean;
}
export function policyError(error: unknown): Error {
  const e = error as { code?: string; message?: string };
  if (e.code === 'PGRST202' || e.code === '42P01' || e.code === '42703') return new Error('Quy chế tháng 10 chưa được kích hoạt trên hệ thống. Thầy cần cập nhật dữ liệu trước khi sử dụng.');
  return new Error(e.message || 'Không tải được dữ liệu trợ giảng.');
}
export async function getPolicyMonth(id: string, month: string): Promise<MonthPolicy> {
  const { data, error } = await getSupabase().rpc('ta_monthly_policy', { p_assistant_id: id, p_month: month });
  if (error) throw policyError(error);
  return data as MonthPolicy;
}
export async function savePolicyMonth(id: string, month: string, scores: MonthPolicy['overrides'], rate: number | null, note: string, close: boolean): Promise<MonthPolicy> {
  const { data, error } = await getSupabase().rpc('ta_save_month_review', { p_assistant_id: id, p_month: month, p_scores: scores, p_rate: rate, p_note: note, p_close: close });
  if (error) throw policyError(error);
  return data as MonthPolicy;
}
export async function getPolicySessions(id: string, month: string): Promise<TaSessionRow[]> {
  const end = new Date(`${month}T12:00:00Z`); end.setUTCMonth(end.getUTCMonth() + 1);
  const { data, error } = await getSupabase().from('ta_sessions').select('*').eq('assistant_id', id).gte('work_date', month).lt('work_date', end.toISOString().slice(0, 10)).order('work_date', { ascending: false });
  if (error) throw policyError(error);
  return data as TaSessionRow[];
}
export async function updatePolicySession(id: string, fields: Partial<Pick<TaSessionRow, 'work_date' | 'class_label' | 'start_time' | 'end_time' | 'student_touches' | 'papers_graded' | 'policy' | 'status' | 'note' | 'phudao_students'>>): Promise<void> {
  const { error } = await getSupabase().from('ta_sessions').update(fields).eq('id', id);
  if (error) throw policyError(error);
}
