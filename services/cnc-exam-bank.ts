import { getSupabase } from "@/services/supabase";
import type { Exam, MultipleChoiceQuestion } from "@/features/exams/types";

// Ngân hàng câu hỏi trắc nghiệm CNC — lưu trong bảng exams (cnc_key duy nhất mỗi ngân hàng,
// published luôn false nên không lộ ra trang /kiem-tra công khai). "lesson-4-turn"/"lesson-4-mill"
// và "gate" chưa được gắn vào bài học nào trong CncCourseWorkspace (nội dung cũ, giữ lại phòng
// khi cần dùng lại), các ngân hàng còn lại đang được học sinh làm trực tiếp.
export const CNC_QUIZ_BANKS = [
  { key: "lesson-1", label: "Quiz cuối Bài 1 — Giới thiệu máy tiện/phay CNC" },
  { key: "lesson-2", label: "Quiz nhận biết lệnh — Bài 2 (Tiện)" },
  { key: "lesson-3", label: "Quiz nhận biết lệnh — Bài 3 (Phay)" },
  { key: "turn-translate", label: "Dịch lệnh G-code — Tiện" },
  { key: "mill-translate", label: "Dịch lệnh G-code — Phay" },
  { key: "operation-turn", label: "Kiểm tra vận hành máy tiện" },
  { key: "operation-mill", label: "Kiểm tra vận hành máy phay" },
  { key: "tool-setup-turn", label: "Kiểm tra cài đặt dao tiện" },
  { key: "tool-setup-mill", label: "Kiểm tra cài đặt dao phay" },
  { key: "gate", label: "Quiz chốt chặn an toàn (chưa gắn vào bài học)" },
  { key: "lesson-4-turn", label: "Quiz Bài 4 — Tiện (chưa gắn vào bài học)" },
  { key: "lesson-4-mill", label: "Quiz Bài 4 — Phay (chưa gắn vào bài học)" },
  // Quiz chuẩn bị tối trước (lớp đảo ngược), 5 câu/buổi — services/cnc-prep.ts.
  { key: "prep-2", label: "Chuẩn bị buổi 2 — Lập trình tiện (1)" },
  { key: "prep-3", label: "Chuẩn bị buổi 3 — Lập trình tiện (2)" },
  { key: "prep-4", label: "Chuẩn bị buổi 4 — Lập trình phay (1)" },
  { key: "prep-5", label: "Chuẩn bị buổi 5 — Lập trình phay (2)" },
  { key: "prep-6", label: "Chuẩn bị buổi 6 — Vận hành tiện" },
  { key: "prep-7", label: "Chuẩn bị buổi 7 — Vận hành phay" },
  { key: "prep-8", label: "Chuẩn bị buổi 8 — Gia công tiện (1)" },
  { key: "prep-9", label: "Chuẩn bị buổi 9 — Gia công tiện (2)" },
  { key: "prep-10", label: "Chuẩn bị buổi 10 — Gia công phay (1)" },
  { key: "prep-11", label: "Chuẩn bị buổi 11 — Gia công phay (2)" },
  { key: "prep-12", label: "Chuẩn bị buổi 12 — Dự án nhóm" },
] as const;

export type CncQuizBankKey = (typeof CNC_QUIZ_BANKS)[number]["key"];

export interface CncQuizQuestion {
  id: string;
  question: string;
  options: string[];
  correctIndex: number;
  explanation: string;
}

function toQuizQuestions(key: string, questions: MultipleChoiceQuestion[]): CncQuizQuestion[] {
  // Các màn hình quiz CNC hiện chấm tự động câu trắc nghiệm. Những dạng còn lại
  // vẫn được lưu nguyên vẹn trong ngân hàng để giáo viên biên soạn và chấm riêng.
  return questions.filter((q) => q.type === "multiple_choice").map((q, index) => ({
    id: `${key}-${index}`,
    question: q.question,
    options: q.options,
    correctIndex: q.answer,
    explanation: q.explanation,
  }));
}

// Nạp nhiều ngân hàng cùng lúc (1 query) — dùng khi mở trang bài học CNC.
export async function fetchCncQuizBanks(keys: string[]): Promise<Record<string, CncQuizQuestion[]>> {
  if (!keys.length) return {};
  const { data, error } = await getSupabase().from("exams").select("cnc_key, questions").in("cnc_key", keys);
  if (error) throw error;
  const result: Record<string, CncQuizQuestion[]> = {};
  for (const row of data ?? []) {
    if (!row.cnc_key) continue;
    result[row.cnc_key] = toQuizQuestions(row.cnc_key, (row.questions ?? []) as MultipleChoiceQuestion[]);
  }
  return result;
}

export interface CncExamBankMeta {
  key: string;
  label: string;
  examId: number | null;
  questionCount: number;
}

// Dùng ở trang quản trị LMS CNC để liệt kê tình trạng từng ngân hàng câu hỏi.
export async function fetchCncExamBankMeta(): Promise<CncExamBankMeta[]> {
  const { data, error } = await getSupabase().from("exams_staff").select("id, cnc_key, questions").not("cnc_key", "is", null);
  if (error) throw error;
  const byKey = new Map((data ?? []).map((row) => [row.cnc_key as string, row]));
  return CNC_QUIZ_BANKS.map(({ key, label }) => {
    const row = byKey.get(key);
    return {
      key,
      label,
      examId: row?.id ?? null,
      questionCount: row ? ((row.questions as unknown[] | null)?.length ?? 0) : 0,
    };
  });
}

// Dùng khi mở "Xem/sửa" 1 ngân hàng trong ExamEditor.
export async function fetchCncExamRow(key: string): Promise<Exam | null> {
  const { data, error } = await getSupabase()
    .from("exams_staff")
    .select("id, title, duration_minutes, published, questions, topic, difficulty, created_at, cnc_key")
    .eq("cnc_key", key)
    .maybeSingle();
  if (error) throw error;
  return data as Exam | null;
}
