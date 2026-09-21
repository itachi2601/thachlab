import { getSupabase } from "@/services/supabase";

// ============================================================
// Thông báo lớp — "việc cần làm hôm nay" + "bài tập về nhà".
// Xem docs/supabase-migration-class-announcements.sql.
// ============================================================

export type AnnouncementKind = "today_task" | "homework";

export interface ClassAnnouncement {
  id: number;
  classId: number;
  kind: AnnouncementKind;
  body: string;
  createdBy: string;
  createdByName: string;
  createdAt: string;
}

interface AnnouncementRow {
  id: number;
  class_id: number;
  kind: AnnouncementKind;
  body: string;
  created_by: string;
  created_at: string;
  profiles: { full_name: string } | { full_name: string }[] | null;
}

const SELECT = "id, class_id, kind, body, created_by, created_at, profiles(full_name)";

function toAnnouncement(row: AnnouncementRow): ClassAnnouncement {
  const author = Array.isArray(row.profiles) ? row.profiles[0] ?? null : row.profiles;
  return {
    id: row.id,
    classId: row.class_id,
    kind: row.kind,
    body: row.body,
    createdBy: row.created_by,
    createdByName: author?.full_name ?? "",
    createdAt: row.created_at,
  };
}

/** Thông báo mới nhất của mỗi loại cho một lớp — dùng ở trang chủ học sinh. */
export async function fetchLatestAnnouncements(classId: number): Promise<Record<AnnouncementKind, ClassAnnouncement | null>> {
  const { data, error } = await getSupabase()
    .from("class_announcements")
    .select(SELECT)
    .eq("class_id", classId)
    .order("created_at", { ascending: false })
    .limit(20);
  if (error) throw error;
  const rows = ((data ?? []) as unknown as AnnouncementRow[]).map(toAnnouncement);
  return {
    today_task: rows.find((r) => r.kind === "today_task") ?? null,
    homework: rows.find((r) => r.kind === "homework") ?? null,
  };
}

/** Vài dòng BTVN gần đây nhất — mục "Bài tập về nhà" hiện danh sách chứ không chỉ 1 dòng. */
export async function fetchRecentAnnouncements(
  classId: number,
  kind: AnnouncementKind,
  limit = 5,
): Promise<ClassAnnouncement[]> {
  const { data, error } = await getSupabase()
    .from("class_announcements")
    .select(SELECT)
    .eq("class_id", classId)
    .eq("kind", kind)
    .order("created_at", { ascending: false })
    .limit(limit);
  if (error) throw error;
  return ((data ?? []) as unknown as AnnouncementRow[]).map(toAnnouncement);
}

export async function postAnnouncement(input: {
  classId: number;
  kind: AnnouncementKind;
  body: string;
  createdBy: string;
}): Promise<void> {
  const { error } = await getSupabase().from("class_announcements").insert({
    class_id: input.classId,
    kind: input.kind,
    body: input.body.trim(),
    created_by: input.createdBy,
  });
  if (error) throw error;
}

export async function deleteAnnouncement(id: number): Promise<void> {
  const { error } = await getSupabase().from("class_announcements").delete().eq("id", id);
  if (error) throw error;
}
