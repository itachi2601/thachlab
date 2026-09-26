import { getSupabase } from "./supabase";

export interface Notification {
  id: number;
  kind: string;
  title: string;
  body: string;
  href: string;
  created_at: string;
  read_at: string | null;
}

const SELECT = "id, kind, title, body, href, created_at, read_at";

/** Thông báo của chính mình, mới nhất trước. RLS chỉ trả dòng user_id = auth.uid(). */
export async function fetchNotifications(limit = 50): Promise<Notification[]> {
  const { data, error } = await getSupabase()
    .from("notifications")
    .select(SELECT)
    .order("created_at", { ascending: false })
    .limit(limit);
  if (error) throw error;
  return (data ?? []) as Notification[];
}

export async function fetchUnreadCount(): Promise<number> {
  const { data, error } = await getSupabase().rpc("unread_notification_count");
  if (error) return 0;
  return Number(data ?? 0);
}

export async function markRead(ids: number[]): Promise<void> {
  if (ids.length === 0) return;
  const { error } = await getSupabase()
    .from("notifications")
    .update({ read_at: new Date().toISOString() })
    .in("id", ids)
    .is("read_at", null);
  if (error) throw error;
}

export async function markAllRead(): Promise<void> {
  const { error } = await getSupabase()
    .from("notifications")
    .update({ read_at: new Date().toISOString() })
    .is("read_at", null);
  if (error) throw error;
}

export async function deleteNotification(id: number): Promise<void> {
  const { error } = await getSupabase().from("notifications").delete().eq("id", id);
  if (error) throw error;
}

// timeAgo chuyển sang lib/time-ago.ts (hàm thuần, không đụng supabase) — re-export ở đây
// để app/thong-bao/page.tsx (đang import từ đây) không phải sửa gì.
export { timeAgo } from "@/lib/time-ago";
