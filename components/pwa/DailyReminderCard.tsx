"use client";

/**
 * components/pwa/DailyReminderCard.tsx — bật/tắt "Nhắc luyện 1 lần mỗi ngày" (GĐ 2.6 / M4), ở /tai-khoan.
 *
 * Quy tắc thiết kế: B2/N1 (một nút chính), D2/D3 (nút >= 44px), M4/C1 (chữ >= 14px), giọng nhẹ — không dọa
 * mất chuỗi. Chỉ học sinh. Chỉ xin quyền thông báo khi HS BẤM nút (không popup tự bật). iOS chưa cài PWA ->
 * chỉ hướng dẫn, không xin quyền. Thiếu NEXT_PUBLIC_VAPID_PUBLIC_KEY -> không render gì.
 * Component này chỉ nạp lazy (next/dynamic ssr:false + LazyErrorBoundary ở app/tai-khoan/page.tsx);
 * chỉ gọi Supabase khi HS đang mở /tai-khoan (không thêm round-trip ở trang chủ/bài/làm đề).
 */

import { useCallback, useEffect, useState } from "react";
import { useAuth } from "@/components/auth/auth-context";
import { getSupabase } from "@/services/supabase";
import {
  DEFAULT_REMIND_HOUR,
  REMIND_HOURS,
  clampHour,
  detectPushEnv,
  getVapidPublicKey,
  urlBase64ToBytes,
  type PushEnv,
} from "@/lib/push-reminder";

type Phase = "loading" | "off" | "on" | "denied" | "ios-needs-install" | "unsupported" | "no-sw";

function readEnv(): PushEnv {
  const ua = navigator.userAgent;
  return detectPushEnv({
    hasServiceWorker: "serviceWorker" in navigator,
    hasPushManager: "PushManager" in window,
    hasNotification: "Notification" in window,
    isIos: /iphone|ipad|ipod/i.test(ua),
    isStandalone:
      window.matchMedia("(display-mode: standalone)").matches ||
      (navigator as Navigator & { standalone?: boolean }).standalone === true,
  });
}

export default function DailyReminderCard() {
  const { profile } = useAuth();
  const vapid = getVapidPublicKey();
  const [phase, setPhase] = useState<Phase>("loading");
  const [hour, setHour] = useState<number>(DEFAULT_REMIND_HOUR);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");
  const isStudent = profile?.role === "student";

  const refresh = useCallback(async () => {
    const env = readEnv();
    if (env !== "ready") return setPhase(env);
    if (Notification.permission === "denied") return setPhase("denied");
    const reg = await navigator.serviceWorker.getRegistration().catch(() => undefined);
    if (!reg) return setPhase("no-sw");
    const sub = await reg.pushManager.getSubscription().catch(() => null);
    if (!sub) return setPhase("off");
    const { data } = await getSupabase()
      .from("push_subscriptions")
      .select("remind_hour, enabled")
      .eq("endpoint", sub.endpoint)
      .maybeSingle();
    if (data?.enabled) {
      setHour(clampHour(data.remind_hour));
      setPhase("on");
    } else {
      setPhase("off");
    }
  }, []);

  useEffect(() => {
    if (!isStudent || !vapid) return;
    void Promise.resolve().then(refresh);
  }, [isStudent, vapid, refresh]);

  if (!isStudent || !vapid) return null;

  const enable = async () => {
    setBusy(true);
    setMsg("");
    try {
      const perm = await Notification.requestPermission(); // chỉ chạy sau khi HS bấm nút
      if (perm !== "granted") {
        setPhase(perm === "denied" ? "denied" : "off");
        return;
      }
      const reg = await navigator.serviceWorker.getRegistration();
      if (!reg) return setPhase("no-sw");
      const sub =
        (await reg.pushManager.getSubscription()) ??
        (await reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: urlBase64ToBytes(vapid) }));
      const json = sub.toJSON();
      const { error } = await getSupabase().rpc("upsert_my_push_subscription", {
        p_endpoint: sub.endpoint,
        p_p256dh: json.keys?.p256dh ?? "",
        p_auth: json.keys?.auth ?? "",
        p_hour: hour,
      });
      if (error) throw error;
      setPhase("on");
    } catch {
      setMsg("Chưa bật được nhắc. Em thử lại sau nhé.");
    } finally {
      setBusy(false);
    }
  };

  const disable = async () => {
    setBusy(true);
    setMsg("");
    try {
      const reg = await navigator.serviceWorker.getRegistration();
      const sub = await reg?.pushManager.getSubscription();
      if (sub) {
        await getSupabase().from("push_subscriptions").delete().eq("endpoint", sub.endpoint);
        await sub.unsubscribe().catch(() => false);
      }
      setPhase("off");
    } catch {
      setMsg("Chưa tắt được nhắc. Em thử lại sau nhé.");
    } finally {
      setBusy(false);
    }
  };

  const changeHour = async (h: number) => {
    setHour(h);
    setMsg("");
    try {
      const reg = await navigator.serviceWorker.getRegistration();
      const sub = await reg?.pushManager.getSubscription();
      if (sub) {
        const { error } = await getSupabase().from("push_subscriptions").update({ remind_hour: h }).eq("endpoint", sub.endpoint);
        if (error) throw error;
      }
    } catch {
      setMsg("Chưa lưu được giờ nhắc. Em thử lại sau nhé.");
    }
  };

  const hint =
    phase === "ios-needs-install"
      ? "Để nhận nhắc trên iPhone, em thêm ThachLab vào Màn hình chính trước (nút Chia sẻ trên Safari → “Thêm vào Màn hình chính”), rồi mở ThachLab từ biểu tượng đó."
      : phase === "denied"
        ? "Thông báo đang bị chặn. Em bật lại trong phần cài đặt của trình duyệt cho trang này nếu muốn nhận nhắc."
        : phase === "unsupported"
          ? "Trình duyệt này chưa hỗ trợ nhắc. Em thử bằng Chrome trên điện thoại."
          : phase === "no-sw"
            ? "Mở lại trang này sau vài giây rồi thử lại."
            : null;

  return (
    <section className="mt-6 rounded-3xl border border-white/10 bg-panel p-6" aria-label="Nhắc luyện mỗi ngày">
      <h2 className="font-display text-lg font-bold text-white">Nhắc luyện 5 phút mỗi ngày</h2>
      <p className="mt-1 text-sm leading-relaxed text-slate-300">
        Mỗi ngày một tin duy nhất, vào giờ em chọn, chỉ khi hôm nay em chưa luyện.
      </p>

      {hint && <p className="mt-3 text-sm leading-relaxed text-slate-300">{hint}</p>}

      {phase === "off" && (
        <div className="mt-4 flex flex-wrap items-center gap-3">
          <label className="flex items-center gap-2 text-sm text-slate-200">
            Giờ nhắc
            <select
              value={hour}
              onChange={(e) => setHour(Number(e.target.value))}
              className="min-h-11 rounded-xl border border-white/15 bg-white/5 px-3 text-base text-white"
            >
              {REMIND_HOURS.map((h) => (
                <option key={h} value={h} className="text-black">
                  {h}:00
                </option>
              ))}
            </select>
          </label>
          <button
            type="button"
            onClick={enable}
            disabled={busy}
            className="min-h-11 rounded-xl bg-blue-600 px-5 text-base font-semibold text-white disabled:opacity-50"
          >
            Bật nhắc
          </button>
        </div>
      )}

      {phase === "on" && (
        <div className="mt-4 flex flex-wrap items-center gap-3">
          <label className="flex items-center gap-2 text-sm text-slate-200">
            Giờ nhắc
            <select
              value={hour}
              onChange={(e) => void changeHour(Number(e.target.value))}
              className="min-h-11 rounded-xl border border-white/15 bg-white/5 px-3 text-base text-white"
            >
              {REMIND_HOURS.map((h) => (
                <option key={h} value={h} className="text-black">
                  {h}:00
                </option>
              ))}
            </select>
          </label>
          <button
            type="button"
            onClick={disable}
            disabled={busy}
            className="min-h-11 rounded-xl border border-white/15 px-5 text-base text-slate-200 disabled:opacity-50"
          >
            Tắt nhắc
          </button>
        </div>
      )}

      {msg && (
        <p role="status" className="mt-3 text-sm text-amber-200">
          {msg}
        </p>
      )}
    </section>
  );
}
