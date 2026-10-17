import { getSupabase } from "@/services/supabase";

// DT-01: sự kiện học tập nối tiếp (open/leave/submit) → RPC log_learning_events.
// Gom hàng đợi trong bộ nhớ, gửi 1 RPC mỗi 60 giây hoặc khi ẩn tab; KHÔNG gửi lúc tải trang nên không thêm
// round-trip cho /lop-hoc/bai. Lỗi mạng thì bỏ lô (sự kiện phân tích, không đáng làm phiền HS).

export type LearningEventKind = "open" | "leave" | "submit";

interface PendingEvent {
  lessonId: number;
  itemId?: number;
  kind: LearningEventKind;
  durationS?: number;
  at: string;
}

const FLUSH_MS = 60_000;
const MAX_QUEUE = 50; // trùng trần mỗi lần gọi của RPC

let queue: PendingEvent[] = [];
let timer: number | null = null;
let listening = false;

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
