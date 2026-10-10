// Dạng dữ liệu trả về từ các RPC quiz_* (xem supabase/migrations/20261006150000_quiz_live.sql).

export type QuizPhase = "lobby" | "question" | "reveal" | "finished";

export interface QuizTopEntry {
  id: number;
  nickname: string;
  score: number;
}

/** quiz_state — góc nhìn của học sinh. */
export type PlayerState =
  | { phase: "gone" | "kicked" }
  | {
      phase: QuizPhase;
      title: string;
      index: number;
      total: number;
      time_limit: number;
      seconds_left: number;
      players: number;
      nickname: string;
      score: number;
      rank: number;
      question?: string;
      options?: string[];
      my_choice?: number | null;
      my_points?: number;
      my_correct?: boolean;
      answer?: number;
      explanation?: string;
      top?: QuizTopEntry[];
    };

/** quiz_host_state — màn hình điều khiển/chiếu. */
export interface HostState {
  pin: string;
  phase: QuizPhase;
  title: string;
  index: number;
  total: number;
  time_limit: number;
  seconds_left: number;
  players: { id: number; nickname: string; answered: boolean }[];
  question?: string;
  options?: string[];
  counts?: number[];
  answer?: number;
  explanation?: string;
  top?: QuizTopEntry[];
}

export const QUIZ_ERRORS: Record<string, string> = {
  room_not_found: "Không thấy phòng với mã này — kiểm lại mã PIN trên màn hình.",
  nickname_taken: "Biệt danh này đã có người dùng, chọn tên khác nhé.",
  nickname_invalid: "Biệt danh dài 1–20 ký tự.",
  not_open: "Câu này đã đóng.",
  time_up: "Hết giờ rồi.",
  kicked: "Bạn đã bị mời ra khỏi phòng.",
  forbidden: "Tài khoản này không có quyền điều khiển phòng.",
  set_empty: "Bộ câu chưa có câu nào.",
  pin_busy: "Chưa tạo được mã PIN, thử lại.",
};

/** Lấy mã lỗi quiz_* từ thông báo của PostgREST/Supabase ("…: room_not_found"). */
export function quizErrorText(e: unknown): string {
  const msg = e instanceof Error ? e.message : String(e);
  for (const k of Object.keys(QUIZ_ERRORS)) if (msg.includes(k)) return QUIZ_ERRORS[k];
  return msg;
}
