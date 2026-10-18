"use client";

/**
 * components/pwa/PushOptInPrompt.tsx — lời mời bật thông báo đẩy (rung + hiện ngoài màn hình khoá), kiểu Duolingo.
 *
 * Quy tắc thiết kế: B2/N1 (một nút chính, nút phụ "Để sau"), D2/D3 (nút >= 44px), M4/C1 (chữ >= 14px), giọng nhẹ.
 * Chỉ học sinh, chỉ khi trình duyệt hỗ trợ và quyền còn ở trạng thái "chưa hỏi"; chỉ xin quyền khi HS BẤM nút.
 * Hiện sau ~25 giây ở trang, không hiện lúc đang làm bài (/kiem-tra/lam). "Để sau" nhớ 14 ngày. iOS chưa cài
 * PWA: không hiện (PwaInstallBanner lo hướng dẫn cài). Không có round-trip Supabase cho tới khi HS bấm "Bật".
 * Cùng bảng/RPC với DailyReminderCard: bật ở đây = bật luôn nhắc luyện 19h + nhận thông báo từ thầy/trợ giảng.
 */

import { useEffect, useState } from "react";
import { useAuthSnapshot } from "@/components/auth/auth-context";
import { DEFAULT_REMIND_HOUR, detectPushEnv, getVapidPublicKey, urlBase64ToBytes } from "@/lib/push-reminder";

const SNOOZE_KEY = "thachlab-push-optin-until";
const SNOOZE_DAYS = 14;

function snoozed(): boolean {
  try {
    return Number(localStorage.getItem(SNOOZE_KEY) ?? 0) > Date.now();
  } catch {
    return false;
  }
}

export default function PushOptInPrompt() {
  const { profile } = useAuthSnapshot();
  const vapid = getVapidPublicKey();
  const [show, setShow] = useState(false);
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState(false);
  const isStudent = profile?.role === "student";

  useEffect(() => {
    if (!isStudent || !vapid || snoozed()) return;
    const ua = navigator.userAgent;
    const env = detectPushEnv({
      hasServiceWorker: "serviceWorker" in navigator,
      hasPushManager: "PushManager" in window,
      hasNotification: "Notification" in window,
      isIos: /iphone|ipad|ipod/i.test(ua),
      isStandalone:
        window.matchMedia("(display-mode: standalone)").matches ||
        (navigator as Navigator & { standalone?: boolean }).standalone === true,
    });
    if (env !== "ready" || Notification.permission !== "default") return;
    const t = window.setTimeout(async () => {
      if (window.location.pathname.startsWith("/kiem-tra/lam")) return;
      const reg = await navigator.serviceWorker.getRegistration().catch(() => undefined);
      if (!reg) return;
      const sub = await reg.pushManager.getSubscription().catch(() => null);
      if (!sub) setShow(true);
    }, 25_000);
    return () => window.clearTimeout(t);
  }, [isStudent, vapid]);

  if (!show || !vapid) return null;

  const later = () => {
    try {
      localStorage.setItem(SNOOZE_KEY, String(Date.now() + SNOOZE_DAYS * 86_400_000));
    } catch {
      // bỏ qua
    }
    setShow(false);
  };

  const enable = async () => {
    setBusy(true);
    try {
      const perm = await Notification.requestPermission();
      if (perm !== "granted") return later();
      const reg = await navigator.serviceWorker.getRegistration();
      if (!reg) return later();
      const sub =
        (await reg.pushManager.getSubscription()) ??
        (await reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: urlBase64ToBytes(vapid) }));
      const json = sub.toJSON();
      const { getSupabase } = await import("@/services/supabase");
      const { error } = await getSupabase().rpc("upsert_my_push_subscription", {
        p_endpoint: sub.endpoint,
        p_p256dh: json.keys?.p256dh ?? "",
        p_auth: json.keys?.auth ?? "",
        p_hour: DEFAULT_REMIND_HOUR,
      });
      if (error) throw error;
      setDone(true);
      window.setTimeout(() => setShow(false), 3500);
    } catch {
      later();
    } finally {
      setBusy(false);
    }
  };

  return (
    <div role="dialog" aria-label="Bật thông báo" className="fixed inset-x-3 bottom-24 z-[90] sm:left-auto sm:right-4 sm:w-96">
      <div className="rounded-2xl border border-blue-400/40 bg-panel p-4 shadow-2xl shadow-black/50">
        {done ? (
          <p className="text-base font-semibold text-ink">Đã bật. Có bài mới hay lời nhắn, điện thoại sẽ rung báo em nhé.</p>
        ) : (
          <>
            <p className="text-base font-semibold text-ink">Bật thông báo để không lỡ bài?</p>
            <p className="mt-1 text-sm leading-relaxed text-muted">
              Có bài mới, lời nhắn của thầy hoặc trợ giảng, điện thoại sẽ rung và hiện ngay trên màn hình, không cần mở web. Tối đa 3 tin mỗi ngày.
            </p>
            <div className="mt-3 flex flex-wrap items-center gap-3">
              <button
                type="button"
                onClick={enable}
                disabled={busy}
                className="min-h-11 rounded-xl bg-blue-600 px-5 text-base font-semibold text-white disabled:opacity-50"
              >
                Bật thông báo
              </button>
              <button type="button" onClick={later} className="min-h-11 px-3 text-base text-muted">
                Để sau
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
