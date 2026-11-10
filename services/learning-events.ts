import { getSupabase } from "@/services/supabase";

// DT-01: sự kiện học tập nối tiếp (open/leave/submit) → RPC log_learning_events.
// Gom hàng đợi trong bộ nhớ, gửi 1 RPC mỗi 60 giây hoặc khi ẩn tab; KHÔNG gửi lúc tải trang nên không thêm
// round-trip cho /lop-hoc/bai. Lỗi mạng thì bỏ lô (sự kiện phân tích, không đáng làm phiền HS).

export type LearningEventKind = "open" | "leave" | "submit";

interface PendingEvent {
  lessonId?: number;
  itemId?: number;
  kind: LearningEventKind | "read_depth" | "clip_choice";
  tnId?: string;
  choice?: number | null;
  correct?: boolean | null;
  durationS?: number;
  h3Max?: number;
  h3Total?: number;
  quizDone?: number;
  quizTotal?: number;
  at: string;
}

const FLUSH_MS = 60_000;
const MAX_QUEUE = 50; // trùng trần mỗi lần gọi của RPC

let queue: PendingEvent[] = [];
let timer: number | null = null;
let listening = false;

export function flushLearningEvents() {
  flush();
}

function flush() {
  if (timer !== null) {
    window.clearTimeout(timer);
    timer = null;
  }
  if (queue.length === 0) return;
  const batch = queue.slice(0, MAX_QUEUE);
  queue = queue.slice(MAX_QUEUE);
  void Promise.resolve(getSupabase().rpc("log_learning_events", { p_events: batch })).catch(() => undefined);
  if (queue.length > 0) flush();
}

function ensureListening() {
  if (listening || typeof document === "undefined") return;
  listening = true;
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "hidden") flush();
  });
  window.addEventListener("pagehide", flush);
}

export function logLearningEvent(input: { lessonId: number; itemId?: number; kind: LearningEventKind; durationS?: number }) {
  if (typeof window === "undefined") return;
  ensureListening();
  queue.push({
    lessonId: input.lessonId,
    itemId: input.itemId,
    kind: input.kind,
    durationS: input.durationS === undefined ? undefined : Math.max(0, Math.min(3600, Math.round(input.durationS))),
    at: new Date().toISOString(),
  });
  if (queue.length >= MAX_QUEUE) flush();
  else if (timer === null) timer = window.setTimeout(flush, FLUSH_MS);
}

/**
 * Độ sâu đọc một mục lý thuyết (migration 20261018150000_read_depth_quiz): mốc <h3> sâu nhất đã cuộn tới
 * và số câu .tl-quiz đã bấm. Máy chủ giữ MAX theo (HS, mục, ngày) nên gửi lặp mỗi lần ẩn tab không sai số.
 */
export function logReadDepth(input: { itemId: number; h3Max: number; h3Total: number; quizDone: number; quizTotal: number }) {
  if (typeof window === "undefined") return;
  const clamp = (n: number) => Math.max(0, Math.min(200, Math.round(n)));
  const h3Total = clamp(input.h3Total);
  const quizTotal = clamp(input.quizTotal);
  if (h3Total === 0 && quizTotal === 0) return;
  ensureListening();
  queue.push({
    kind: "read_depth",
    itemId: input.itemId,
    h3Total,
    h3Max: Math.min(clamp(input.h3Max), h3Total),
    quizTotal,
    quizDone: Math.min(clamp(input.quizDone), quizTotal),
    at: new Date().toISOString(),
  });
  // Gọi lúc rời mục/ẩn tab: gửi ngay (không chờ hẹn giờ 60 giây kẻo tab đóng mất lô); microtask để N mục cùng ẩn tab đi chung một lô.
  queueMicrotask(flush);
}

/**
 * Lựa chọn ở điểm dừng Dự đoán của khung video thí nghiệm (migration clip_choice). Không chấm điểm, không RP:
 * chỉ để thầy xem tỉ lệ chọn A–D của từng clip. `choice` null = bấm "Chưa muốn đoán, xem luôn".
 * Đi chung lô 60 giây với open/leave nên không thêm round-trip.
 */
export function logClipChoice(input: { lessonId: number; tnId: string; choice: number | null; correct: boolean | null }) {
  if (typeof window === "undefined") return;
  ensureListening();
  queue.push({
    kind: "clip_choice",
    lessonId: input.lessonId,
    tnId: input.tnId.slice(0, 60),
    choice: input.choice,
    correct: input.correct,
    at: new Date().toISOString(),
  });
  if (queue.length >= MAX_QUEUE) flush();
  else if (timer === null) timer = window.setTimeout(flush, FLUSH_MS);
}
