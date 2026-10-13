"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { Bell, CheckCheck, MessageSquare, Newspaper } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { useAuth } from "@/components/auth/AuthProvider";
import EmptyState from "@/components/ui/EmptyState";
import { timeAgo } from "@/lib/time-ago";
import { fetchMyClassIds } from "@/services/classes";
import { fetchRecentPostHeads, visibleTo } from "@/services/content";
import { fetchNotifications, markAllRead, markRead } from "@/services/notifications";
import { getSupabase } from "@/services/supabase";

/**
 * Hộp thư: MỘT danh sách gộp thông báo + tin nhắn của thầy + tin tức, mới nhất trước, có lọc theo loại
 * (thầy chốt 13/10/2026; thay cho ba mục rời trong menu, N3, C2). Không thêm RPC: ba truy vấn nhẹ chạy song song,
 * mỗi nguồn lấy tối đa 40 dòng mới nhất rồi trộn ở client.
 */
type Kind = "thong_bao" | "tin_nhan" | "tin_tuc";
type Filter = "tat_ca" | Kind;

interface Item {
  key: string;
  kind: Kind;
  at: string;
  title: string;
  sub: string;
  href?: string;
  /** Tin nhắn không có trang chi tiết: bấm để mở ngay tại chỗ. */
  full?: string;
  notiId?: number;
  unread: boolean;
}

const FILTERS: { key: Filter; label: string }[] = [
  { key: "tat_ca", label: "Tất cả" },
  { key: "thong_bao", label: "Thông báo" },
  { key: "tin_nhan", label: "Tin nhắn" },
  { key: "tin_tuc", label: "Tin tức" },
];

const KIND_META: Record<Kind, { label: string; Icon: typeof Bell; tone: string }> = {
  thong_bao: { label: "Thông báo", Icon: Bell, tone: "bg-warn/10 text-warn" },
  tin_nhan: { label: "Tin nhắn", Icon: MessageSquare, tone: "bg-primary-soft text-primary" },
  tin_tuc: { label: "Tin tức", Icon: Newspaper, tone: "bg-surface-2 text-muted" },
};

const LIMIT = 40;

function Feed() {
  const { session } = useAuth();
  const [items, setItems] = useState<Item[] | null>(null);
  const [filter, setFilter] = useState<Filter>("tat_ca");
  const [open, setOpen] = useState<string | null>(null);

  useEffect(() => {
    if (!session) return;
    let alive = true;
    Promise.all([
      fetchNotifications(LIMIT).catch(() => []),
      Promise.resolve(
        getSupabase()
          .from("messages")
          .select("id, created_at, subject, body, recipient_id, class_name")
          .order("created_at", { ascending: false })
          .limit(LIMIT),
      )
        .then(({ data }) => data ?? [])
        .catch(() => []),
      fetchRecentPostHeads(LIMIT).catch(() => []),
      fetchMyClassIds(session.user.id).catch(() => null),
    ]).then(([notis, msgs, posts, classIds]) => {
      if (!alive) return;
      const out: Item[] = [
        ...notis.map((n): Item => ({
          key: `n${n.id}`,
          kind: "thong_bao",
          at: n.created_at,
          title: n.title,
          sub: n.body,
          href: n.href || undefined,
          notiId: n.id,
          unread: !n.read_at,
        })),
        ...msgs.map((m): Item => ({
          key: `m${m.id}`,
          kind: "tin_nhan",
          at: m.created_at,
          title: m.subject || "(Không có tiêu đề)",
          sub: m.recipient_id ? "Gửi riêng cho em" : m.class_name ? `Lớp ${m.class_name}` : "Toàn trường",
          full: m.body,
          unread: false,
        })),
        ...posts
          .filter((p) => visibleTo(p.classIds, classIds))
          .map((p): Item => ({
            key: `p${p.id}`,
            kind: "tin_tuc",
            at: p.created_at,
            title: p.title,
            sub: "",
            href: `/tin-tuc#post-${p.id}`,
            unread: false,
          })),
      ];
      out.sort((a, b) => b.at.localeCompare(a.at));
      setItems(out);
    });
    return () => {
      alive = false;
    };
  }, [session]);

  const shown = useMemo(() => (items ?? []).filter((i) => filter === "tat_ca" || i.kind === filter), [items, filter]);
  const unread = (items ?? []).filter((i) => i.unread).length;

  async function readAll() {
    await markAllRead().catch(() => undefined);
    setItems((rows) => rows?.map((r) => ({ ...r, unread: false })) ?? null);
  }

  function touch(item: Item) {
    if (item.notiId === undefined || !item.unread) return;
    void markRead([item.notiId]).catch(() => undefined);
    setItems((rows) => rows?.map((r) => (r.key === item.key ? { ...r, unread: false } : r)) ?? null);
  }

  return (
    <div className="mx-auto max-w-2xl">
      <div className="mb-4 flex items-center gap-3">
        <h1 className="font-display text-2xl font-bold text-ink">Hộp thư</h1>
        <span className="text-sm text-muted">{unread > 0 ? `${unread} chưa đọc` : ""}</span>
        {unread > 0 && (
          <button type="button" onClick={readAll} className="ml-auto inline-flex min-h-11 items-center gap-1.5 rounded-xl border border-line px-4 text-sm font-semibold text-ink hover:border-line-strong">
            <CheckCheck size={15} aria-hidden /> Đọc hết
          </button>
        )}
      </div>

      <div role="tablist" aria-label="Lọc hộp thư" className="mb-3 flex gap-1.5 overflow-x-auto">
        {FILTERS.map((f) => (
          <button
            key={f.key}
            role="tab"
            aria-selected={filter === f.key}
            type="button"
            onClick={() => setFilter(f.key)}
            className={`inline-flex min-h-11 shrink-0 items-center rounded-full border px-3.5 text-sm font-semibold ${
              filter === f.key ? "border-primary bg-primary-soft text-primary" : "border-line text-ink hover:border-line-strong"
            }`}
          >
            {f.label}
          </button>
        ))}
      </div>

      {items === null ? (
        <p className="text-muted">Đang tải…</p>
      ) : shown.length === 0 ? (
        <EmptyState title="Chưa có gì ở đây" description="Bài mới, kết quả chấm và tin từ thầy sẽ hiện ở hộp thư này." />
      ) : (
        <ul className="overflow-hidden rounded-2xl border border-line bg-panel">
          {shown.map((item) => {
            const { Icon, tone, label } = KIND_META[item.kind];
            const expanded = open === item.key;
            const body = (
              <>
                <span className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-full ${tone}`} aria-label={label}>
                  <Icon size={17} aria-hidden />
                </span>
                <span className="min-w-0 flex-1 text-left">
                  <span className={`block text-[15px] text-ink ${item.unread ? "font-bold" : "font-medium"}`}>{item.title}</span>
                  {item.sub && <span className="mt-0.5 line-clamp-2 block text-[13px] text-muted">{item.sub}</span>}
                </span>
                <span className="flex shrink-0 flex-col items-end gap-1 text-[12px] text-muted">
                  {timeAgo(item.at)}
                  {item.unread && <span className="h-2.5 w-2.5 rounded-full bg-primary" aria-label="Chưa đọc" />}
                </span>
              </>
            );
            const rowCls = "flex min-h-16 w-full items-start gap-3 px-4 py-3 hover:bg-surface-2";
            return (
              <li key={item.key} className="border-b border-line last:border-0">
                {item.full !== undefined ? (
                  <>
                    <button type="button" aria-expanded={expanded} onClick={() => setOpen(expanded ? null : item.key)} className={rowCls}>
                      {body}
                    </button>
                    {expanded && <p className="whitespace-pre-wrap px-4 pb-4 pl-16 text-sm leading-relaxed text-ink">{item.full}</p>}
                  </>
                ) : item.href ? (
                  <Link href={item.href} onClick={() => touch(item)} className={rowCls}>
                    {body}
                  </Link>
                ) : (
                  <div className={rowCls}>{body}</div>
                )}
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}

export default function HopThuPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen w-full px-4 pb-24 pt-28 sm:px-6">
        <RequireAuth>
          <Feed />
        </RequireAuth>
      </main>
      <Footer variant="app" />
    </>
  );
}
