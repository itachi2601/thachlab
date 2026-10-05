"use client";

/**
 * components/pwa/OfflineSync.tsx — xả hàng đợi kết quả luyện tập + chỉ báo nhỏ (GĐ 2.6 / M3).
 *
 * Quy tắc thiết kế: N1/B2 (không phải điểm nổi bật: nền tối, chữ nhỏ vừa đủ, không màu bão hoà),
 * B4 (không chuyển động, không toast tự hiện), B6 (không thêm thanh: chỉ là viên thuốc nhỏ nổi trên
 * thanh đáy), D2 (nút ≥ 44px), M4 (kèm chữ, không chỉ màu), L6 (chỉ hiện khi offline hoặc còn kết quả chờ,
 * ẩn khi không có gì). Chỉ học sinh. Không round-trip Supabase khi hàng đợi rỗng.
 */

import { useCallback, useEffect, useRef, useState } from "react";
import { useAuth } from "@/components/auth/auth-context";
import { OFFLINE_QUEUE_EVENT, pendingCount } from "@/lib/offline-queue";
import { flushPracticeQueue } from "@/services/lessons";

export default function OfflineSync() {
  const { profile, session } = useAuth();
  const uid = session?.user.id;
  const isStudent = profile?.role === "student";
  const [online, setOnline] = useState(() => typeof navigator === "undefined" || navigator.onLine !== false);
  const [pending, setPending] = useState(0);
  const [busy, setBusy] = useState(false);
  const busyRef = useRef(false);

  const refresh = useCallback(() => setPending(pendingCount(uid)), [uid]);

  const flush = useCallback(async () => {
    if (busyRef.current || pendingCount(uid) === 0) return;
    if (typeof navigator !== "undefined" && navigator.onLine === false) return;
    busyRef.current = true;
    setBusy(true);
    try {
      await flushPracticeQueue();
    } catch {
      // giữ lại, lần sau thử tiếp
    } finally {
      busyRef.current = false;
      setBusy(false);
      refresh();
    }
  }, [uid, refresh]);

  useEffect(() => {
    if (!isStudent) return;
    queueMicrotask(refresh); // đọc hàng đợi (localStorage) sau khi mount
    queueMicrotask(() => void flush()); // mở lại app: xả nếu có
    const onOnline = () => {
      setOnline(true);
      void flush();
    };
    const onOffline = () => setOnline(false);
    const onVisible = () => {
      if (document.visibilityState === "visible") void flush();
    };
    window.addEventListener("online", onOnline);
    window.addEventListener("offline", onOffline);
    window.addEventListener(OFFLINE_QUEUE_EVENT, refresh);
    document.addEventListener("visibilitychange", onVisible);
    return () => {
      window.removeEventListener("online", onOnline);
      window.removeEventListener("offline", onOffline);
      window.removeEventListener(OFFLINE_QUEUE_EVENT, refresh);
      document.removeEventListener("visibilitychange", onVisible);
    };
  }, [isStudent, flush, refresh]);

  if (!isStudent || (online && pending === 0)) return null;

  const text = !online
    ? pending > 0
      ? `Đang offline · ${pending} kết quả chờ gửi`
      : "Đang offline"
    : `${pending} kết quả chờ gửi`;

  return (
    <div
      role="status"
      className="fixed left-3 z-40 flex items-center gap-1 rounded-full border border-white/10 bg-panel/95 pl-3 text-sm text-slate-200 shadow-lg"
      style={{ bottom: "calc(4.75rem + env(safe-area-inset-bottom))" }}
    >
      <span>{text}</span>
      {online && pending > 0 && (
        <button
          type="button"
          onClick={() => void flush()}
          disabled={busy}
          className="min-h-11 rounded-full px-3 text-sm font-semibold text-blue-300 disabled:opacity-60"
        >
          {busy ? "Đang gửi" : "Gửi lại"}
        </button>
      )}
      {!(online && pending > 0) && <span className="pr-3" />}
    </div>
  );
}
