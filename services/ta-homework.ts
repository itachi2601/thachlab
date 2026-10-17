import { getSupabase } from "@/services/supabase";

// ============================================================
// BTVN giao riêng từng em / nhóm trên web (trợ giảng giao, học sinh làm trên tài khoản của mình).
// Hàm RPC: supabase/migrations/20261017180000_ta_giao_btvn_rieng.sql
// "Đã làm" = có bài nộp (exam_results) sau lúc giao — không có cờ tay.
// ============================================================

export interface ExamOption {
  id: number;
  title: string;
}

export interface PendingHomework {
  id: number;
  examId: number;
  examTitle: string;
  dueAt: string | null;
  note: string;
  assignedAt: string;
  assignerName: string;
}

export interface HomeworkOverviewRow {
  id: number;
  studentId: string;
  studentName: string;
  examId: number;
  examTitle: string;
  dueAt: string | null;
  assignedAt: string;
  done: boolean;
  bestScore: number | null;
  late: boolean;
}

export async function assignHomework(input: {
  classId: number;
  studentIds: string[];
  examId: number;
  dueAt: string | null;
  note: string;
}): Promise<number> {
  const { data, error } = await getSupabase().rpc("ta_homework_assign", {
    p_class_id: input.classId,
    p_student_ids: input.studentIds,
    p_exam_id: input.examId,
    p_due_at: input.dueAt,
    p_note: input.note,
  });
  if (error) throw new Error(error.message);
  return Number(data ?? 0);
}

export async function fetchMyPendingHomework(): Promise<PendingHomework[]> {
  const { data, error } = await getSupabase().rpc("my_pending_homework");
  if (error) throw new Error(error.message);
  return ((data ?? []) as {
    id: number;
    exam_id: number;
    exam_title: string;
    due_at: string | null;
    note: string;
    assigned_at: string;
    assigner_name: string;
  }[]).map((r) => ({
    id: r.id,
    examId: r.exam_id,
    examTitle: r.exam_title,
    dueAt: r.due_at,
    note: r.note,
    assignedAt: r.assigned_at,
    assignerName: r.assigner_name,
  }));
}

export async function fetchHomeworkOverview(classId: number, days = 21): Promise<HomeworkOverviewRow[]> {
  const { data, error } = await getSupabase().rpc("ta_homework_overview", { p_class_id: classId, p_days: days });
  if (error) throw new Error(error.message);
  return ((data ?? []) as {
    id: number;
    student_id: string;
    student_name: string;
    exam_id: number;
    exam_title: string;
    due_at: string | null;
    assigned_at: string;
    done: boolean;
    best_score: number | null;
    late: boolean;
  }[]).map((r) => ({
    id: r.id,
    studentId: r.student_id,
    studentName: r.student_name,
    examId: r.exam_id,
    examTitle: r.exam_title,
    dueAt: r.due_at,
    assignedAt: r.assigned_at,
    done: r.done,
    bestScore: r.best_score === null ? null : Number(r.best_score),
    late: r.late,
  }));
}

/** Tìm đề theo từ khoá (tên đề hoặc chủ đề) để giao BTVN. */
export async function searchExams(keywords: string[], limit = 8): Promise<ExamOption[]> {
  const terms = keywords.map((k) => k.replace(/[%,()]/g, " ").trim()).filter(Boolean);
  if (terms.length === 0) return [];
  const filter = terms.flatMap((t) => [`title.ilike.%${t}%`, `topic.ilike.%${t}%`]).join(",");
  const { data } = await getSupabase()
    .from("exams")
    .select("id, title")
    .eq("published", true)
    .or(filter)
    .order("id", { ascending: false })
    .limit(limit);
  return (data as ExamOption[]) ?? [];
}
