"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { Bell, CheckCheck, X } from "lucide-react";
import { useAuth } from "@/components/auth/auth-context";
import { timeAgo } from "@/lib/time-ago";
import type { Notification } from "@/services/notifications";

// 2 phút/lần (trước 60s), bỏ qua khi tab ẩn — giảm log Supabase; quay lại tab thì tải ngay.
const POLL_MS = 120_000;

/**
 * Chuông thông báo trên thanh điều hướng: đếm chưa đọc (RPC, rẻ), mở ra thì tải 10 dòng
 * mới nhất. Mọi thông báo do trigger trong DB sinh ra (supabase-migration-thong-bao.sql).
 * Poll mỗi phút + khi quay lại tab — không dùng realtime để khỏi tốn kết nối.
 *
 * NotificationBell nằm trong Navbar (render ở MỌI trang, kể cả trang công khai chưa đăng
 * nhập) nên các hàm gọi supabase (fetchNotifications...) được import ĐỘNG (dynamic
 * import) thay vì import thẳng ở đầu file — nếu import thẳng, mọi trang công khai sẽ
 * phải tải cả @supabase/supabase-js dù component luôn return null khi chưa đăng nhập
 * (session === null, xem dòng "if (!session) return null" bên dưới).
 */
export default function NotificationBell() {
  const { session } = useAuth();
  const [count, setCount] = useState(0);
  const [open, setOpen] = useState(false);
  const [items, setItems] = useState<Notification[] | null>(null);
  const [toast, setToast] = useState<{ title: string; body: string; href: string } | null>(null);
  const ref = useRef<HTMLDivElement>(null);
  const prevCount = useRef<number | null>(null);

  const showToast = useCallback((t: { title: string; body: string; href: string }) => {
    setToast(t);
    try {
      navigator.vibrate?.([200, 100, 200]); // Android; iOS/desktop bỏ qua
    } catch {
      // bỏ qua
    }
  }, []);

  const refreshCount = useCallback(
    (force = false) => {
      if (!session || (!force && document.visibilityState === "hidden")) return;
      import("@/services/notifications").then(({ fetchUnreadCount, fetchNotifications }) =>
        fetchUnreadCount()
          .then((n) => {
            const before = prevCount.current;
            prevCount.current = n;
            setCount(n);
            // Có thông báo mới từ lần đếm trước (không phải lần tải đầu): hiện popup ngay, không đợi mở chuông.
            if (before !== null && n > before) {
              void fetchNotifications(1)
                .then(([latest]) => latest && !latest.read_at && showToast({ title: latest.title, body: latest.body, href: latest.href || "/thong-bao" }))
                .catch(() => undefined);
            }
          })
          .catch(() => undefined),
      );
    },
    [session, showToast],
  );

  // Service worker báo "vừa có push" -> đếm lại ngay (không chờ chu kỳ poll) và hiện popup.
  useEffect(() => {
    if (!session || !("serviceWorker" in navigator)) return;
    const onMsg = (e: MessageEvent) => {
      if (e.data?.type !== "thachlab-push") return;
      showToast({ title: e.data.title || "ThachLab", body: e.data.body || "", href: e.data.url || "/thong-bao" });
      prevCount.current = null; // đã hiện popup từ payload, đừng hiện lần nữa khi đếm lại
      refreshCount(true);
    };
    navigator.serviceWorker.addEventListener("message", onMsg);
    return () => navigator.serviceWorker.removeEventListener("message", onMsg);
  }, [session, refreshCount, showToast]);

  useEffect(() => {
    if (!toast) return;
    const t = window.setTimeout(() => setToast(null), 9000);
    return () => window.clearTimeout(t);
  }, [toast]);

  useEffect(() => {
    if (!session) return;
    refreshCount();
    const timer = window.setInterval(() => refreshCount(), POLL_MS);
    const onFocus = () => refreshCount();
    const onVisible = () => {
      if (document.visibilityState === "visible") refreshCount();
    };
    window.addEventListener("focus", onFocus);
    document.addEventListener("visibilitychange", onVisible);
    return () => {
      window.clearInterval(timer);
      window.removeEventListener("focus", onFocus);
      document.removeEventListener("visibilitychange", onVisible);
    };
  }, [session, refreshCount]);

  useEffect(() => {
    if (!open) return;
    import("@/services/notifications").then(({ fetchNotifications }) =>
      fetchNotifications(10).then(setItems).catch(() => setItems([])),
    );
    function onClickOutside(event: MouseEvent) {
      if (ref.current && !ref.current.contains(event.target as Node)) setOpen(false);
    }
    document.addEventListener("mousedown", onClickOutside);
    return () => document.removeEventListener("mousedown", onClickOutside);
  }, [open]);

  if (!session) return null;

  async function openItem(item: Notification) {
    if (!item.read_at) {
      const { markRead } = await import("@/services/notifications");
      await markRead([item.id]).catch(() => undefined);
      setCount((c) => Math.max(0, c - 1));
    }
    setOpen(false);
  }

  async function readAll() {
    const { markAllRead } = await import("@/services/notifications");
    await markAllRead().catch(() => undefined);
    setCount(0);
    setItems((rows) => rows?.map((r) => ({ ...r, read_at: r.read_at ?? new Date().toISOString() })) ?? null);
  }

  return (
    <div className="relative" ref={ref}>
      {toast && (
        <div role="status" aria-live="polite" className="fixed inset-x-3 top-3 z-[100] sm:left-auto sm:right-4 sm:w-96">
          <div className="flex items-start gap-2 rounded-2xl border border-blue-400/40 bg-panel p-3 shadow-2xl shadow-black/50">
            <Link
              href={toast.href}
              onClick={() => setToast(null)}
              className="flex min-h-11 min-w-0 flex-1 items-start gap-3 rounded-xl px-1"
            >
              <Bell size={20} className="mt-0.5 shrink-0 text-blue-300" />
              <span className="min-w-0">
                <span className="block text-base font-semibold text-ink">{toast.title}</span>
                {toast.body && <span className="mt-0.5 line-clamp-2 block text-sm text-muted">{toast.body}</span>}
              </span>
            </Link>
            <button
              type="button"
              aria-label="Đóng"
              onClick={() => setToast(null)}
              className="inline-flex h-11 w-11 shrink-0 items-center justify-center rounded-full text-muted hover:bg-surface-2"
            >
              <X size={18} />
            </button>
          </div>
        </div>
      )}
      <button
        type="button"
        aria-label={count > 0 ? `${count} thông báo chưa đọc` : "Thông báo"}
        aria-expanded={open}
        onClick={() => setOpen((v) => !v)}
        className="relative inline-flex h-11 w-11 items-center justify-center rounded-full text-ink transition-colors hover:bg-surface-2 hover:text-primary"
      >
        <Bell size={19} />
        {count > 0 && (
          <span className="absolute -right-0.5 -top-0.5 flex h-5 min-w-5 items-center justify-center rounded-full bg-red-500 px-1 text-[12px] font-bold text-white">
            {count > 99 ? "99+" : count}
          </span>
        )}
      </button>

      {open && (
        <div className="fixed inset-x-3 top-16 overflow-hidden rounded-2xl border border-line bg-panel/95 shadow-2xl shadow-black/50 sm:absolute sm:inset-x-auto sm:right-0 sm:top-[calc(100%+8px)] sm:w-[26rem]">
          <div className="flex items-center justify-between border-b border-line px-4 py-3">
            <span className="text-base font-bold text-ink">Thông báo</span>
            {count > 0 && (
              <button type="button" onClick={readAll} className="inline-flex items-center gap-1 text-sm text-blue-300 hover:underline">
                <CheckCheck size={13} /> Đọc hết
              </button>
            )}
          </div>
          <div className="max-h-[60vh] overflow-y-auto">
            {items === null ? (
              <p className="p-4 text-base text-muted">Đang tải…</p>
            ) : items.length === 0 ? (
              <p className="p-4 text-base text-slate-500">Chưa có thông báo nào.</p>
            ) : (
              <ul>
                {items.map((item) => (
                  <li key={item.id} className="border-b border-line last:border-0">
                    <Link
                      href={item.href || "/thong-bao"}
                      onClick={() => void openItem(item)}
                      className={`block px-4 py-3.5 transition-colors hover:bg-surface-2 ${item.read_at ? "" : "bg-blue-500/[.06]"}`}
                    >
                      <span className="flex items-start gap-2.5">
                        {!item.read_at && <span className="mt-2 h-2 w-2 shrink-0 rounded-full bg-blue-400" />}
                        <span className="min-w-0">
                          <span className={`block text-base text-ink ${item.read_at ? "" : "font-semibold"}`}>{item.title}</span>
                          {item.body && <span className="mt-1 line-clamp-2 block text-sm text-muted">{item.body}</span>}
                          <span className="mt-1.5 block text-sm text-slate-500">{timeAgo(item.created_at)}</span>
                        </span>
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            )}
          </div>
          <Link href="/hop-thu" onClick={() => setOpen(false)} className="block border-t border-line px-4 py-3 text-center text-sm font-semibold text-blue-300 hover:bg-surface-2">
            Mở hộp thư
          </Link>
        </div>
      )}
    </div>
  );
}
