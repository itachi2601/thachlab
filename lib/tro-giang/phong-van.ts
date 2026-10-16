import { getSupabase } from "@/services/supabase";

/** Nhóm em được phỏng vấn — khớp check constraint `ta_interviews.grp`. */
export const INTERVIEW_GROUPS = [
  { value: "chua_mo", label: "Đang mở khoá, chưa mở bài tự kiểm tra" },
  { value: "bo_truot", label: "Đã mở bài tự kiểm tra, bỏ giữa chừng / trượt" },
  { value: "da_thoat", label: "Đã thoát bằng bài tự kiểm tra (≥80%)" },
  { value: "khac", label: "Khác" },
] as const;

export type InterviewGroup = (typeof INTERVIEW_GROUPS)[number]["value"];

/** 11 câu của docs/PHIEU-PHONG-VAN-PHU-DAO-2026-10-16.md — sửa phiếu thì sửa cả ở đây. `only` = chỉ hỏi nhóm đó. */
export const INTERVIEW_QUESTIONS: { id: string; text: string; only?: InterviewGroup[] }[] = [
  { id: "q1", text: "Lần gần nhất em thấy chủ đề bị gắn \"đang mở khoá\" trên web, em nghĩ gì, cảm thấy gì? (nhớ lại tình huống cụ thể)" },
  { id: "q2", text: "Em hiểu \"đang mở khoá\" nghĩa là gì? Em nghĩ web muốn em làm gì tiếp theo?" },
  { id: "q3", text: "Sau đó em làm gì? (làm gì / không làm gì / đi hỏi ai)" },
  { id: "q4", text: "Em có biết có bài tự kiểm tra 20 câu để thoát không? Biết từ đâu? Em thấy nó ở chỗ nào?" },
  { id: "q5", text: "Điều gì khiến em chưa bấm vào? Nếu nói thật lòng thì lý do chính là gì?", only: ["chua_mo"] },
  { id: "q6", text: "Lúc bỏ / trượt em đang ở câu nào, đang nghĩ gì? Ngay sau đó em làm gì?", only: ["bo_truot"] },
  { id: "q7", text: "Điều gì khiến em làm đến cùng? Lúc thoát em thấy gì?", only: ["da_thoat"] },
  { id: "q8", text: "Nếu phải ôn trước khi làm bài tự kiểm tra, em muốn ôn bằng cách nào? Em đọc lại lý thuyết chỗ nào, bằng gì?" },
  { id: "q9", text: "20 câu một lượt: dài, vừa hay ngắn? Làm lúc nào trong ngày, ở đâu, bằng điện thoại hay máy tính?" },
  { id: "q10", text: "Em có ngại bạn hoặc thầy cô thấy mình trong danh sách này không? Cái gì khiến em dễ chịu hơn?" },
];

export interface InterviewRow {
  id: string;
  code: string;
  grp: InterviewGroup;
  answers: Record<string, string>;
  barrier: string | null;
  wish: string | null;
  by: string;
  updated_at: string;
}

export async function saveInterview(input: {
  code: string;
  grp: InterviewGroup;
  answers: Record<string, string>;
  barrier: string;
  wish: string;
}): Promise<void> {
  const { error } = await getSupabase().rpc("ta_interview_save", {
    p_code: input.code,
    p_grp: input.grp,
    p_answers: input.answers,
    p_barrier: input.barrier,
    p_wish: input.wish,
  });
  if (error) throw error;
}

export async function listInterviews(): Promise<InterviewRow[]> {
  const { data, error } = await getSupabase().rpc("ta_interview_list");
  if (error) throw error;
  return (data ?? []) as InterviewRow[];
}
