import { getSupabase } from "@/services/supabase";

export interface AdminTodayTask {
  id: number;
  classId: number;
  className: string;
  body: string;
  createdAt: string;
}

export interface AdminTodayNotice {
  id: number;
  title: string;
  body: string;
  href: string;
  createdAt: string;
}

export interface AdminTodayBoard {
  tasks: AdminTodayTask[];
  notices: AdminTodayNotice[];
  pendingJoins: number;
  newBugs: number;
  /** Mọi truy vấn đều lỗi — bảng hiện một dòng, không để trống im lặng. */
  failed: boolean;
}

interface TaskRow {
  id: number;
  body: string;
  class_id: number;
  created_at: string;
  classes: { name: string } | { name: string }[] | null;
}

function classNameOf(row: TaskRow): string {
  const embedded = Array.isArray(row.classes) ? row.classes[0] : row.classes;
  const name = embedded?.name?.trim() || "Lớp";
  return /^\d+$/.test(name) ? `Lớp ${name}` : name;
}

/** Việc admin thấy trên trang chủ: thông báo "cần làm hôm nay" mới nhất mỗi lớp, cộng việc đang chờ. */
export async function fetchAdminTodayBoard(): Promise<AdminTodayBoard> {
  const supabase = getSupabase();
  const [tasksRes, noticesRes, joinsRes, bugsRes] = await Promise.all([
    supabase
      .from("class_announcements")
      .select("id, body, class_id, created_at, classes(name)")
      .eq("kind", "today_task")
      .order("created_at", { ascending: false })
      .limit(40),
    supabase
      .from("notifications")
      .select("id, title, body, href, created_at")
      .is("read_at", null)
      .order("created_at", { ascending: false })
      .limit(5),
    supabase.from("user_classes").select("user_id", { count: "exact", head: true }).eq("status", "pending"),
    supabase.from("bug_reports").select("id", { count: "exact", head: true }).eq("status", "moi"),
  ]);

  const seen = new Set<number>();
  const tasks: AdminTodayTask[] = [];
  if (!tasksRes.error) {
    for (const row of (tasksRes.data ?? []) as TaskRow[]) {
      if (seen.has(row.class_id)) continue;
      seen.add(row.class_id);
      tasks.push({
        id: row.id,
        classId: row.class_id,
        className: classNameOf(row),
        body: row.body,
        createdAt: row.created_at,
      });
      if (tasks.length >= 6) break;
    }
  }

  const notices: AdminTodayNotice[] = noticesRes.error
    ? []
    : ((noticesRes.data ?? []) as { id: number; title: string; body: string; href: string | null; created_at: string }[]).map(
        (row) => ({
          id: row.id,
          title: row.title,
          body: row.body ?? "",
          href: row.href?.startsWith("/") ? row.href : "/thong-bao",
          createdAt: row.created_at,
        }),
      );

  return {
    tasks,
    notices,
    pendingJoins: joinsRes.error ? 0 : joinsRes.count ?? 0,
    newBugs: bugsRes.error ? 0 : bugsRes.count ?? 0,
    failed: Boolean(tasksRes.error && noticesRes.error && joinsRes.error && bugsRes.error),
  };
}
