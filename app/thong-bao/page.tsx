"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Bell, CheckCheck, Trash2 } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { useAuth } from "@/components/auth/AuthProvider";
import EmptyState from "@/components/ui/EmptyState";
import {
  deleteNotification,
  fetchNotifications,
  markAllRead,
  markRead,
  timeAgo,
  type Notification,
} from "@/services/notifications";

function Inbox() {
  const { session } = useAuth();
  const [items, setItems] = useState<Notification[] | null>(null);

  useEffect(() => {
    if (!session) return;
    fetchNotifications(200).then(setItems).catch(() => setItems([]));
  }, [session]);

  async function readAll() {
    await markAllRead().catch(() => undefined);
    setItems((rows) => rows?.map((r) => ({ ...r, read_at: r.read_at ?? new Date().toISOString() })) ?? null);
  }

  async function remove(id: number) {
    await deleteNotification(id).catch(() => undefined);
    setItems((rows) => rows?.filter((r) => r.id !== id) ?? null);
  }

  if (items === null) return <p className="text-slate-400">Đang tải…</p>;
  const unread = items.filter((i) => !i.read_at).length;

  return (
    <>
      <div className="flex flex-wrap items-center gap-3">
        <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-500/15 text-blue-300">
          <Bell size={20} />
        </span>
        <div>
          <h1 className="font-display text-2xl font-bold text-white">Thông báo</h1>
          <p className="text-sm text-slate-400">{unread > 0 ? `${unread} chưa đọc` : "Đã đọc hết"}</p>
        </div>
        {unread > 0 && (
          <button type="button" onClick={readAll} className="ml-auto inline-flex items-center gap-1.5 rounded-xl border border-white/15 px-4 py-2 text-sm font-semibold text-slate-200">
            <CheckCheck size={15} /> Đánh dấu đã đọc hết
          </button>
        )}
      </div>

      {items.length === 0 ? (
        <EmptyState
          className="mt-8"
          title="Chưa có thông báo nào"
          description="Khi có bài mới, kết quả chấm hay tin từ thầy cô, em sẽ thấy ở đây."
        />
      ) : (
        <ul className="mt-6 space-y-2">
          {items.map((item) => (
            <li key={item.id} className={`flex items-start gap-3 rounded-2xl border p-4 ${item.read_at ? "border-white/10 bg-panel" : "border-blue-400/25 bg-blue-500/[.06]"}`}>
              <Link
                href={item.href || "#"}
                onClick={() => {
                  if (!item.read_at) {
                    void markRead([item.id]).catch(() => undefined);
                    setItems((rows) => rows?.map((r) => (r.id === item.id ? { ...r, read_at: new Date().toISOString() } : r)) ?? null);
                  }
                }}
                className="min-w-0 flex-1"
              >
                <span className={`block ${item.read_at ? "text-slate-300" : "font-semibold text-white"}`}>{item.title}</span>
                {item.body && <span className="mt-1 block text-sm text-slate-400">{item.body}</span>}
                <span className="mt-1 block text-xs text-slate-500">{timeAgo(item.created_at)}</span>
              </Link>
              <button type="button" onClick={() => remove(item.id)} title="Xoá" className="rounded-lg border border-white/10 p-1.5 text-slate-500 hover:border-red-500/30 hover:text-red-300">
                <Trash2 size={14} />
              </button>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}

export default function ThongBaoPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-3xl px-6 pb-20 pt-28">
        <RequireAuth>
          <Inbox />
        </RequireAuth>
      </main>
      <Footer />
    </>
  );
}
