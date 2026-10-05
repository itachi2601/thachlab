/**
 * lib/push-reminder.ts — phần thuần của "Nhắc 1 lần/ngày" (GĐ 2.6 / M4), không đụng DOM khi import.
 * Khoá công khai VAPID đọc từ NEXT_PUBLIC_VAPID_PUBLIC_KEY; thiếu -> tính năng ẩn (không lỗi).
 */

export const REMIND_HOURS = [17, 18, 19, 20, 21] as const;
export const DEFAULT_REMIND_HOUR = 19;

export function getVapidPublicKey(): string | null {
  const k = process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY?.trim();
  return k ? k : null;
}

/** Khoá VAPID base64url -> bytes cho pushManager.subscribe({applicationServerKey}). */
export function urlBase64ToBytes(b64: string): Uint8Array<ArrayBuffer> {
  const pad = "=".repeat((4 - (b64.length % 4)) % 4);
  const raw = atob((b64 + pad).replace(/-/g, "+").replace(/_/g, "/"));
  const out = new Uint8Array(new ArrayBuffer(raw.length));
  for (let i = 0; i < raw.length; i++) out[i] = raw.charCodeAt(i);
  return out;
}

export type PushEnv =
  | "unsupported" // trình duyệt không có Push
  | "ios-needs-install" // iOS: chỉ chạy khi đã thêm vào Màn hình chính
  | "ready";

export function detectPushEnv(w: {
  hasServiceWorker: boolean;
  hasPushManager: boolean;
  hasNotification: boolean;
  isIos: boolean;
  isStandalone: boolean;
}): PushEnv {
  if (w.isIos && !w.isStandalone) return "ios-needs-install";
  if (!w.hasServiceWorker || !w.hasPushManager || !w.hasNotification) return "unsupported";
  return "ready";
}

export function clampHour(h: number): number {
  if (!Number.isFinite(h)) return DEFAULT_REMIND_HOUR;
  return Math.min(22, Math.max(6, Math.round(h)));
}
