import { getSupabase } from "./supabase";

/** Độ chắc em tự chọn sau mỗi câu (thầy chốt 14/10/2026: 3 mức). */
export type DiagnosticConfidence = "chac" | "hoi" | "doan";

export const CONFIDENCE_LABEL: Record<DiagnosticConfidence, string> = {
  chac: "Em chắc",
  hoi: "Hơi chắc",
  doan: "Em đoán",
};

/**
 * Nhóm của một bài, DB tính (không tin client):
 * vung = đúng và chắc · chua_vung = đúng nhưng đoán/hơi chắc, hoặc sai 1 câu ·
 * hieu_sai = sai mà chắc (ảo tưởng hiểu) · chua_biet = sai ≥2 câu và đều không chắc.
 */
export type DiagnosticLevel = "vung" | "chua_vung" | "hieu_sai" | "chua_biet";

export const LEVEL_LABEL: Record<DiagnosticLevel, string> = {
  vung: "Đã vững",
  chua_vung: "Cần ôn thêm",
  hieu_sai: "Hiểu chưa đúng",
  chua_biet: "Chưa biết",
};

/** Một bài trong kết quả kiểm tra đầu vào: đúng `correct`/`total` câu. */
export interface DiagnosticTopicResult {
  topicId: number;
  correct: number;
  total: number;
  /** Vị trí trong danh sách bài lớp đã học: 0 = bài gần nhất, càng lớn càng cũ (nền tảng). */
  seq?: number;
  /** Bài lùi về để dò tiền đề (2 câu dễ), không nằm trong 6 bài chính. */
  probe?: boolean;
  /** Từng câu: đúng/sai + độ chắc, để DB tính nhóm. */
  answers?: { ok: boolean; conf: DiagnosticConfidence }[];
  /** Do DB điền khi trả về; phụ huynh không nhận các trường này. */
  level?: DiagnosticLevel;
  sureWrong?: number;
  shakyRight?: number;
}

export interface DiagnosticStatus {
  done: boolean;
  createdAt?: string;
  needCount?: number;
  perTopic?: DiagnosticTopicResult[];
}

export interface DiagnosticSubmitResult {
  needCount: number;
  perTopic: DiagnosticTopicResult[];
}

/** Số bài chính mỗi lượt và số câu mỗi bài (thầy chốt 12/10/2026: ~15–18 câu, 5–6 bài). */
export const DIAGNOSTIC_MAX_TOPICS = 6;
/** Số bài dự trữ phía sau (cũ hơn) để dò tiền đề khi bài chính hổng. */
export const DIAGNOSTIC_RESERVE_TOPICS = 3;
/** Tối đa bài dò tiền đề mỗi lượt, mỗi bài 2 câu dễ. */
export const DIAGNOSTIC_MAX_PROBES = 3;
export const DIAGNOSTIC_PROBE_QUESTIONS = 2;
export const DIAGNOSTIC_QUESTIONS_PER_TOPIC = 3;
/** Sai từ ngần này câu trong một bài thì dừng bài đó, không bắt làm hết. */
export const DIAGNOSTIC_STOP_AFTER_WRONG = 2;

export async function fetchDiagnostic(studentId: string): Promise<DiagnosticStatus> {
  const { data, error } = await getSupabase().rpc("diagnostic_get", { p_student: studentId });
  if (error) throw new Error(error.message);
  const d = data as { done: boolean; createdAt?: string; needCount?: number; perTopic?: DiagnosticTopicResult[] };
  return d;
}

/** Bản đồ cả lớp một lần (thầy/trợ giảng). Em chưa làm thì không có trong kết quả. */
export async function fetchDiagnosticMaps(studentIds: string[]): Promise<Map<string, DiagnosticTopicResult[]>> {
  if (studentIds.length === 0) return new Map();
  const { data, error } = await getSupabase().rpc("diagnostic_maps", { p_students: studentIds });
  if (error) throw new Error(error.message);
  const rows = (data ?? []) as { student_id: string; per_topic: DiagnosticTopicResult[] }[];
  return new Map(rows.map((r) => [r.student_id, r.per_topic ?? []]));
}

export async function submitDiagnostic(
  studentId: string,
  results: DiagnosticTopicResult[],
): Promise<DiagnosticSubmitResult> {
  const { data, error } = await getSupabase().rpc("diagnostic_submit", { p_student: studentId, p_results: results });
  if (error) throw new Error(error.message);
  const d = data as { needCount: number; perTopic?: DiagnosticTopicResult[] };
  return { needCount: d.needCount, perTopic: d.perTopic ?? [] };
}

/** Thầy / trợ giảng cho em làm lại. */
export async function resetDiagnostic(studentId: string): Promise<void> {
  const { error } = await getSupabase().rpc("diagnostic_reset", { p_student: studentId });
  if (error) throw new Error(error.message);
}

/** Bài tính vào kết quả "cần dạy" (khớp DB: hieu_sai / chua_biet mở mục phụ đạo). */
export function isGapLevel(level: DiagnosticLevel | undefined): boolean {
  return level === "hieu_sai" || level === "chua_biet";
}

/** Bài hổng hay là bài thật sự cần dạy trước khi học tiếp. Bản cũ không có level thì suy từ số câu. */
export function levelOf(r: DiagnosticTopicResult): DiagnosticLevel {
  if (r.level) return r.level;
  const wrong = r.total - r.correct;
  if (r.total >= 2 && wrong >= 2 && (wrong * 100) / r.total >= 60) return "chua_biet";
  return wrong >= 1 ? "chua_vung" : "vung";
}

export interface StartMap {
  /** Đã vững: trợ giảng bỏ qua, chỉ ôn nhanh vài phút cho em vui. */
  skip: DiagnosticTopicResult[];
  /** Thứ tự dạy: hiểu chưa đúng trước (cần gỡ), rồi chưa biết, rồi cần ôn; cùng nhóm thì bài cũ (nền tảng) trước. */
  order: DiagnosticTopicResult[];
}

const LEVEL_PRIORITY: Record<DiagnosticLevel, number> = { hieu_sai: 0, chua_biet: 1, chua_vung: 2, vung: 3 };

/** Từ kết quả kiểm tra đầu vào dựng "bản đồ xuất phát": bỏ qua gì, bắt đầu từ đâu, rồi đi tiếp thế nào. */
export function buildStartMap(rows: DiagnosticTopicResult[]): StartMap {
  const skip = rows.filter((r) => levelOf(r) === "vung");
  const order = rows
    .filter((r) => levelOf(r) !== "vung")
    .sort(
      (a, b) =>
        LEVEL_PRIORITY[levelOf(a)] - LEVEL_PRIORITY[levelOf(b)] || (b.seq ?? 0) - (a.seq ?? 0) || a.topicId - b.topicId,
    );
  return { skip, order };
}

export interface HandoffOptions {
  assistants: { id: string; name: string }[];
  current: { id: string; name: string; since: string } | null;
}

/** Trợ giảng chọn được cho em (đã gán lớp của em) + người đang phụ trách. Chỉ thầy phụ trách lớp / admin gọi được. */
export async function fetchHandoffOptions(studentId: string): Promise<HandoffOptions> {
  const { data, error } = await getSupabase().rpc("ta_handoff_options", { p_student: studentId });
  if (error) throw new Error(error.message);
  return data as HandoffOptions;
}

export interface HandoffResult {
  assistant: string;
  assignedNeeds: number;
  invited: boolean;
}

/** Giao em cho trợ giảng; có `courseId` và em chưa làm kiểm tra đầu vào thì mời em làm luôn. */
export async function assignHandoff(
  studentId: string,
  assistantId: string,
  courseId: number | null,
): Promise<HandoffResult> {
  const { data, error } = await getSupabase().rpc("ta_handoff_assign", {
    p_student: studentId,
    p_assistant: assistantId,
    p_course: courseId,
  });
  if (error) throw new Error(error.message);
  return data as HandoffResult;
}

export async function clearHandoff(studentId: string): Promise<void> {
  const { error } = await getSupabase().rpc("ta_handoff_clear", { p_student: studentId });
  if (error) throw new Error(error.message);
}
