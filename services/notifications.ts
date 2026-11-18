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

// Chuông (NotificationBell) và thanh tab dưới (MobileTabBar) cùng hỏi lúc mở trang → dùng chung một lượt
// RPC trong 3 giây; sau khi đánh dấu đã đọc/xoá thì bỏ bản nhớ để lượt hỏi kế tiếp lấy số mới.
const UNREAD_SHARE_MS = 3000;
let unreadShared: { at: number; value: Promise<number> } | null = null;

export function fetchUnreadCount(): Promise<number> {
  if (unreadShared && Date.now() - unreadShared.at < UNREAD_SHARE_MS) return unreadShared.value;
  const value = (async () => {
    const { data, error } = await getSupabase().rpc("unread_notification_count");
    if (error) return 0;
    return Number(data ?? 0);
  })();
  unreadShared = { at: Date.now(), value };
  return value;
}

export async function markRead(ids: number[]): Promise<void> {
  if (ids.length === 0) return;
  unreadShared = null;
  const { error } = await getSupabase()
    .from("notifications")
    .update({ read_at: new Date().toISOString() })
    .in("id", ids)
    .is("read_at", null);
  if (error) throw error;
}

export async function markAllRead(): Promise<void> {
  unreadShared = null;
  const { error } = await getSupabase()
    .from("notifications")
    .update({ read_at: new Date().toISOString() })
    .is("read_at", null);
  if (error) throw error;
}

export async function deleteNotification(id: number): Promise<void> {
  unreadShared = null;
  const { error } = await getSupabase().from("notifications").delete().eq("id", id);
  if (error) throw error;
}

// timeAgo chuyển sang lib/time-ago.ts (hàm thuần, không đụng supabase) — re-export ở đây
// để app/thong-bao/page.tsx (đang import từ đây) không phải sửa gì.
export { timeAgo } from "@/lib/time-ago";
