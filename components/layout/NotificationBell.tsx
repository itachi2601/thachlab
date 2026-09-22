"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { Bell, CheckCheck } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import {
  fetchNotifications,
  fetchUnreadCount,
  markAllRead,
  markRead,
  timeAgo,
  type Notification,
} from "@/services/notifications";

const POLL_MS = 60_000;

/**
 * Chuông thông báo trên thanh điều hướng: đếm chưa đọc (RPC, rẻ), mở ra thì tải 10 dòng
 * mới nhất. Mọi thông báo do trigger trong DB sinh ra (supabase-migration-thong-bao.sql).
 * Poll mỗi phút + khi quay lại tab — không dùng realtime để khỏi tốn kết nối.
 */
export default function NotificationBell() {
  const { session } = useAuth();
  const [count, setCount] = useState(0);
  const [open, setOpen] = useState(false);
  const [items, setItems] = useState<Notification[] | null>(null);
  const ref = useRef<HTMLDivElement>(null);

  const refreshCount = useCallback(() => {
    if (!session) return;
    fetchUnreadCount().then(setCount).catch(() => undefined);
  }, [session]);

  useEffect(() => {
    if (!session) return;
    refreshCount();
    const timer = window.setInterval(refreshCount, POLL_MS);
    const onFocus = () => refreshCount();
    window.addEventListener("focus", onFocus);
    return () => {
      window.clearInterval(timer);
      window.removeEventListener("focus", onFocus);
    };
  }, [session, refreshCount]);

  useEffect(() => {
    if (!open) return;
    fetchNotifications(10).then(setItems).catch(() => setItems([]));
    function onClickOutside(event: MouseEvent) {
      if (ref.current && !ref.current.contains(event.target as Node)) setOpen(false);
    }
    document.addEventListener("mousedown", onClickOutside);
    return () => document.removeEventListener("mousedown", onClickOutside);
  }, [open]);

  if (!session) return null;

  async function openItem(item: Notification) {
    if (!item.read_at) {
      await markRead([item.id]).catch(() => undefined);
      setCount((c) => Math.max(0, c - 1));
    }
    setOpen(false);
  }

  async function readAll() {
    await markAllRead().catch(() => undefined);
    setCount(0);
    setItems((rows) => rows?.map((r) => ({ ...r, read_at: r.read_at ?? new Date().toISOString() })) ?? null);
  }

  return (
    <div className="relative" ref={ref}>
      <button
        type="button"
        aria-label={count > 0 ? `${count} thông báo chưa đọc` : "Thông báo"}
        aria-expanded={open}
        onClick={() => setOpen((v) => !v)}
        className="relative inline-flex h-10 w-10 items-center justify-center rounded-full text-slate-300 transition-colors hover:bg-white/[0.07] hover:text-white"
      >
        <Bell size={19} />
        {count > 0 && (
          <span className="absolute -right-0.5 -top-0.5 flex h-5 min-w-5 items-center justify-center rounded-full bg-red-500 px-1 text-[10px] font-bold text-white">
            {count > 99 ? "99+" : count}
          </span>
        )}
      </button>

      {open && (
        <div className="absolute right-0 top-[calc(100%+8px)] w-80 overflow-hidden rounded-2xl border border-white/10 bg-[#0B1220]/[0.98] shadow-2xl shadow-black/50 sm:w-96">
          <div className="flex items-center justify-between border-b border-white/10 px-4 py-2.5">
            <span className="text-sm font-bold text-white">Thông báo</span>
            {count > 0 && (
              <button type="button" onClick={readAll} className="inline-flex items-center gap-1 text-xs text-blue-300 hover:underline">
                <CheckCheck size={13} /> Đọc hết
              </button>
            )}
          </div>
          <div className="max-h-[60vh] overflow-y-auto">
            {items === null ? (
              <p className="p-4 text-sm text-slate-400">Đang tải…</p>
            ) : items.length === 0 ? (
              <p className="p-4 text-sm text-slate-500">Chưa có thông báo nào.</p>
            ) : (
              <ul>
                {items.map((item) => (
                  <li key={item.id} className="border-b border-white/5 last:border-0">
                    <Link
                      href={item.href || "/thong-bao"}
                      onClick={() => void openItem(item)}
                      className={`block px-4 py-3 transition-colors hover:bg-white/[0.05] ${item.read_at ? "" : "bg-blue-500/[.06]"}`}
                    >
                      <span className="flex items-start gap-2">
                        {!item.read_at && <span className="mt-1.5 h-2 w-2 shrink-0 rounded-full bg-blue-400" />}
                        <span className="min-w-0">
                          <span className={`block text-sm ${item.read_at ? "text-slate-300" : "font-semibold text-white"}`}>{item.title}</span>
                          {item.body && <span className="mt-0.5 line-clamp-2 block text-xs text-slate-400">{item.body}</span>}
                          <span className="mt-1 block text-[11px] text-slate-500">{timeAgo(item.created_at)}</span>
                        </span>
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            )}
          </div>
          <Link href="/thong-bao" onClick={() => setOpen(false)} className="block border-t border-white/10 px-4 py-2.5 text-center text-xs font-semibold text-blue-300 hover:bg-white/[0.05]">
            Xem tất cả
          </Link>
        </div>
      )}
    </div>
  );
}
