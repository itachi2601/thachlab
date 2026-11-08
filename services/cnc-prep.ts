import { getSupabase } from "@/services/supabase";
import { fetchCncQuizBanks, type CncQuizQuestion } from "@/services/cnc-exam-bank";

// CNC lớp đảo ngược — quiz "chuẩn bị tối trước" theo buổi (JiTT).
// Câu hỏi: exams.cnc_key = "prep-<buổi>" (đăng ở /quan-tri/cnc-dang-de). Kết quả: bảng cnc_prep_responses
// (migration 20261108120000). Không tính điểm, chỉ để giảng viên biết lớp sai câu nào trước giờ học.
// Bảng buổi theo docs/CNC-FLIPPED-THIET-KE-LAI-2026-11-08.md mục 4.3 (đánh số bài như trên web: lesson-4-turn = Bài 4,
// lesson-4-mill = Bài 5, lesson-5 = Bài 6, lesson-6 = Bài 7).
export const CNC_PREP_SESSIONS = [
  { no: 2, title: "Lập trình tiện (1)", lessonId: "lesson-2", read: "Bài 2 · mục 1–2", anchor: "muc-1" },
  { no: 3, title: "Lập trình tiện (2)", lessonId: "lesson-2", read: "Bài 2 · mục 4–5", anchor: "muc-4" },
  { no: 4, title: "Lập trình phay (1)", lessonId: "lesson-3", read: "Bài 3 · mục 1–2", anchor: "muc-1" },
  { no: 5, title: "Lập trình phay (2)", lessonId: "lesson-3", read: "Bài 3 · mục 4–5", anchor: "muc-4" },
  { no: 6, title: "Vận hành tiện", lessonId: "lesson-4-turn", read: "Bài 4 · mục 8–9", anchor: "muc-8" },
  { no: 7, title: "Vận hành phay", lessonId: "lesson-4-mill", read: "Bài 5 · mục 8–9", anchor: "muc-8" },
  { no: 8, title: "Gia công tiện (1)", lessonId: "lesson-5", read: "Bài 6 · mục 1–2", anchor: "muc-1" },
  { no: 9, title: "Gia công tiện (2)", lessonId: "lesson-5", read: "Bài 6 · mục 4", anchor: "muc-4" },
  { no: 10, title: "Gia công phay (1)", lessonId: "lesson-6", read: "Bài 7 · mục 1", anchor: "muc-1" },
  { no: 11, title: "Gia công phay (2)", lessonId: "lesson-6", read: "Bài 7 · mục 3–4", anchor: "muc-3" },
  { no: 12, title: "Dự án nhóm", lessonId: null, read: "Đề dự án (giảng viên phát)", anchor: null },
] as const;

// Link "mở bài" nhảy thẳng tới mục: neo `muc-N` là id của tiêu đề "N. …" trong body_html (đã ghi 8/11/2026),
// `bai-mau` là mục "V. Bài toán mẫu". CncCourseWorkspace đọc ?bai= rồi cuộn tới #neo.
export const cncLessonHref = (lessonId: string, anchor?: string | null) =>
  `/lop-hoc/cnc/?bai=${lessonId}${anchor ? `#${anchor}` : ""}`;
// Phiếu buổi (cnc_lessons id flip-N), trang /lop-hoc/cnc/buoi/?so=N.
export const cncSessionSheetHref = (no: number) => `/lop-hoc/cnc/buoi/?so=${no}`;

export type CncPrepSession = (typeof CNC_PREP_SESSIONS)[number];
export const CNC_PREP_PASS = 4; // trên 5 câu: "sẵn sàng vào máy"
export const cncPrepKey = (no: number) => `prep-${no}`;

export type CncPrepResponse = {
  id: number;
  course_id: number;
  student_id: string;
  session_no: number;
  answers: (number | null)[];
  score: number;
  total: number;
  chua_ro: string | null;
  created_at: string;
};

const fields = "id, course_id, student_id, session_no, answers, score, total, chua_ro, created_at";

// Một truy vấn cho mọi buổi; buổi chưa đăng câu hỏi thì không có trong kết quả.
export async function fetchCncPrepBanks(): Promise<Record<number, CncQuizQuestion[]>> {
  const banks = await fetchCncQuizBanks(CNC_PREP_SESSIONS.map((s) => cncPrepKey(s.no)));
  const out: Record<number, CncQuizQuestion[]> = {};
  for (const s of CNC_PREP_SESSIONS) {
    const qs = banks[cncPrepKey(s.no)];
    if (qs?.length) out[s.no] = qs;
  }
  return out;
}

export async function submitCncPrep(input: {
  courseId: number;
  sessionNo: number;
  answers: (number | null)[];
  score: number;
  total: number;
  chuaRo: string;
}) {
  const chuaRo = input.chuaRo.trim().slice(0, 500);
  const { error } = await getSupabase()
    .from("cnc_prep_responses")
    .insert({
      course_id: input.courseId,
      session_no: input.sessionNo,
      answers: input.answers,
      score: input.score,
      total: input.total,
      chua_ro: chuaRo || null,
    });
  if (error) throw error;
}

export async function fetchMyCncPrep(courseId: number, studentId: string) {
  const { data, error } = await getSupabase()
    .from("cnc_prep_responses")
    .select(fields)
    .eq("course_id", courseId)
    .eq("student_id", studentId)
    .order("created_at", { ascending: true });
  if (error) throw error;
  return (data ?? []) as CncPrepResponse[];
}

export async function fetchCourseCncPrep(courseId: number, sessionNo: number) {
  const { data, error } = await getSupabase()
    .from("cnc_prep_responses")
    .select(fields)
    .eq("course_id", courseId)
    .eq("session_no", sessionNo)
    .order("created_at", { ascending: true });
  if (error) throw error;
  return (data ?? []) as CncPrepResponse[];
}

export type CncPrepQuestionStat = {
  index: number;
  question: string;
  wrong: number;
  answered: number;
  picks: number[];
  correctIndex: number;
};

// Thống kê theo LƯỢT ĐẦU của mỗi sinh viên (phản ánh việc chuẩn bị ở nhà, không bị lượt làm lại che).
export function summarizeCncPrep(rows: CncPrepResponse[], questions: CncQuizQuestion[]) {
  const first = new Map<string, CncPrepResponse>();
  const best = new Map<string, number>();
  for (const row of rows) {
    if (!first.has(row.student_id)) first.set(row.student_id, row);
    best.set(row.student_id, Math.max(best.get(row.student_id) ?? 0, row.score));
  }
  const firsts = [...first.values()];
  const stats: CncPrepQuestionStat[] = questions.map((q, index) => {
    const picks = q.options.map(() => 0);
    let answered = 0,
      wrong = 0;
    for (const row of firsts) {
      const pick = row.answers[index];
      if (pick === null || pick === undefined) continue;
      answered++;
      if (pick >= 0 && pick < picks.length) picks[pick]++;
      if (pick !== q.correctIndex) wrong++;
    }
    return { index, question: q.question, wrong, answered, picks, correctIndex: q.correctIndex };
  });
  const notes = rows
    .filter((row) => row.chua_ro)
    .map((row) => ({ studentId: row.student_id, text: row.chua_ro as string, at: row.created_at }));
  const avg = firsts.length ? firsts.reduce((sum, row) => sum + row.score / row.total, 0) / firsts.length : 0;
  return { firsts, best, stats, notes, avg };
}
