/**
 * lib/offline-queue.ts — hàng đợi bền cho kết quả luyện tập khi mất mạng (GĐ 2.6 / M3).
 *
 * Thuần logic, không biết Supabase: bộ lưu (localStorage) và hàm gửi được truyền vào nên test được bằng tsx.
 * Quy tắc:
 *  - Chỉ đưa vào hàng đợi khi lỗi là lỗi MẠNG (isNetworkError). Lỗi logic/RLS thì không xếp hàng.
 *  - Mỗi mục có id = clientToken; thêm trùng id thì bỏ qua (không nhân đôi).
 *  - Giới hạn số mục và dung lượng; vượt giới hạn thì từ chối (enqueue trả false) — KHÔNG lặng lẽ xoá mục cũ.
 *  - Xả tuần tự; lỗi mạng -> dừng, giữ nguyên; lỗi logic -> tăng attempts, quá MAX_ATTEMPTS thì bỏ.
 *  - Mọi truy cập storage bọc try/catch.
 */

export const OFFLINE_QUEUE_KEY = "thachlab-offline-queue-v1";
export const OFFLINE_QUEUE_EVENT = "thachlab:offline-queue-changed";
export const MAX_QUEUE_ITEMS = 30;
export const MAX_QUEUE_BYTES = 400_000;
export const MAX_ATTEMPTS = 3;

export interface QueueItem<P = unknown> {
  /** clientToken của phiên — dùng để gửi lại idempotent. */
  id: string;
  studentId: string;
  queuedAt: string;
  attempts: number;
  payload: P;
}

export type SendResult = "ok" | "network" | "logic";

export interface QueueStorage {
  getItem(key: string): string | null;
  setItem(key: string, value: string): void;
}

export function defaultStorage(): QueueStorage | null {
  try {
    if (typeof localStorage === "undefined") return null;
    return localStorage;
  } catch {
    return null;
  }
}

function notify() {
  try {
    if (typeof window !== "undefined") window.dispatchEvent(new Event(OFFLINE_QUEUE_EVENT));
  } catch {
    // bỏ qua
  }
}

export function readQueue<P = unknown>(storage: QueueStorage | null = defaultStorage()): QueueItem<P>[] {
  if (!storage) return [];
  try {
    const raw = storage.getItem(OFFLINE_QUEUE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed.filter(
      (x): x is QueueItem<P> =>
        x && typeof x.id === "string" && typeof x.studentId === "string" && typeof x.attempts === "number",
    );
  } catch {
    return [];
  }
}

function writeQueue(items: QueueItem[], storage: QueueStorage | null): boolean {
  if (!storage) return false;
  try {
    storage.setItem(OFFLINE_QUEUE_KEY, JSON.stringify(items));
    notify();
    return true;
  } catch {
    return false; // hết dung lượng / bị chặn
  }
}

export function pendingCount(studentId?: string, storage: QueueStorage | null = defaultStorage()): number {
  const items = readQueue(storage);
  return studentId ? items.filter((i) => i.studentId === studentId).length : items.length;
}

/** true nếu mục đã nằm trong hàng đợi sau lệnh gọi (kể cả trùng id); false nếu không lưu được. */
export function enqueue<P>(
  item: { id: string; studentId: string; payload: P; queuedAt?: string },
  storage: QueueStorage | null = defaultStorage(),
): boolean {
  const items = readQueue(storage);
  if (items.some((i) => i.id === item.id)) return true;
  if (items.length >= MAX_QUEUE_ITEMS) return false;
  const next = [
    ...items,
    {
      id: item.id,
      studentId: item.studentId,
      queuedAt: item.queuedAt ?? new Date().toISOString(),
      attempts: 0,
      payload: item.payload,
    },
  ];
  if (JSON.stringify(next).length > MAX_QUEUE_BYTES) return false;
  return writeQueue(next, storage);
}

let flushing = false;

/** Xả các mục của một học sinh, tuần tự. Trả số mục đã gửi xong. Không chạy chồng nhau. */
export async function flushQueue<P>(
  studentId: string,
  send: (item: QueueItem<P>) => Promise<SendResult>,
  storage: QueueStorage | null = defaultStorage(),
): Promise<number> {
  if (flushing) return 0;
  flushing = true;
  let sent = 0;
  try {
    const ids = readQueue<P>(storage)
      .filter((i) => i.studentId === studentId)
      .map((i) => i.id);
    for (const id of ids) {
      // đọc lại mỗi vòng: tab khác có thể đã xả mục này
      const item = readQueue<P>(storage).find((i) => i.id === id);
      if (!item) continue;
      let result: SendResult;
      try {
        result = await send(item);
      } catch {
        result = "network";
      }
      if (result === "network") break;
      const fresh = readQueue<P>(storage);
      if (result === "ok") {
        sent += 1;
        writeQueue(
          fresh.filter((i) => i.id !== id),
          storage,
        );
      } else {
        const attempts = item.attempts + 1;
        writeQueue(
          attempts >= MAX_ATTEMPTS
            ? fresh.filter((i) => i.id !== id)
            : fresh.map((i) => (i.id === id ? { ...i, attempts } : i)),
          storage,
        );
      }
    }
  } finally {
    flushing = false;
  }
  return sent;
}

/** Lỗi do mạng/tạm thời (đáng gửi lại), khác lỗi logic/RLS (gửi lại vô ích). */
export function isNetworkError(err: unknown): boolean {
  if (typeof navigator !== "undefined" && navigator.onLine === false) return true;
  if (!err) return false;
  const e = err as { message?: unknown; status?: unknown; name?: unknown };
  const status = typeof e.status === "number" ? e.status : undefined;
  if (status === 0 || status === 502 || status === 503 || status === 504 || status === 408) return true;
  const msg = `${typeof e.message === "string" ? e.message : ""} ${typeof e.name === "string" ? e.name : ""}`;
  return /failed to fetch|networkerror|network request failed|load failed|fetch failed|network error|timed? ?out|econn|enotfound|offline/i.test(
    msg,
  );
}
