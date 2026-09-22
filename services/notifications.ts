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

/** "5 phút trước", "hôm qua"… cho danh sách ngắn. */
export function timeAgo(iso: string): string {
  const diff = (Date.now() - new Date(iso).getTime()) / 1000;
  if (diff < 60) return "vừa xong";
  if (diff < 3600) return `${Math.floor(diff / 60)} phút trước`;
  if (diff < 86400) return `${Math.floor(diff / 3600)} giờ trước`;
  if (diff < 172800) return "hôm qua";
  return new Date(iso).toLocaleDateString("vi-VN");
}
