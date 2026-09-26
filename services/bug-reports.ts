import { getSupabase } from "@/services/supabase";
import { compressImageFile } from "@/services/image-compress";
// Types + nhãn chuyển sang lib/bug-report-labels.ts (thuần, không đụng supabase) —
// re-export ở đây để các file đang import từ "@/services/bug-reports" không phải sửa gì.
export {
  BUG_CATEGORY_LABELS,
  BUG_STATUS_LABELS,
  type BugCategory,
  type BugStatus,
} from "@/lib/bug-report-labels";
import type { BugCategory, BugStatus } from "@/lib/bug-report-labels";

export interface BugReport {
  id: number;
  created_at: string;
  updated_at: string;
  user_id: string | null;
  reporter_name: string;
  reporter_email: string;
  page_url: string;
  category: BugCategory;
  description: string;
  screenshot_path: string | null;
  status: BugStatus;
  admin_note: string;
  profiles?: { full_name: string } | null;
}

const BUCKET = "bug-report-screenshots";
const SELECT_FIELDS =
  "id, created_at, updated_at, user_id, reporter_name, reporter_email, page_url, category, description, screenshot_path, status, admin_note, profiles(full_name)";

function normalize(row: Record<string, unknown>) {
  return { ...row, profiles: Array.isArray(row.profiles) ? (row.profiles[0] ?? null) : row.profiles } as BugReport;
}

export async function submitBugReport({
  description,
  category,
  pageUrl,
  userId,
  reporterName,
  reporterEmail,
  file,
}: {
  description: string;
  category: BugCategory;
  pageUrl: string;
  userId?: string | null;
  reporterName?: string;
  reporterEmail?: string;
  file?: File | null;
}) {
  const supabase = getSupabase();
  let screenshotPath: string | null = null;
  if (file) {
    const compressed = await compressImageFile(file);
    const safeName = compressed.name.replace(/[^a-zA-Z0-9.\-_]/g, "_");
    screenshotPath = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}-${safeName}`;
    const { error: uploadError } = await supabase.storage
      .from(BUCKET)
      .upload(screenshotPath, compressed, { contentType: compressed.type || "application/octet-stream", upsert: false });
    if (uploadError) throw uploadError;
  }
  const { error } = await supabase.from("bug_reports").insert({
    user_id: userId ?? null,
    reporter_name: reporterName?.trim() ?? "",
    reporter_email: reporterEmail?.trim() ?? "",
    page_url: pageUrl,
    category,
    description: description.trim(),
    screenshot_path: screenshotPath,
  });
  if (error) {
    if (screenshotPath) await supabase.storage.from(BUCKET).remove([screenshotPath]);
    throw error;
  }
}

export async function fetchBugReports(status?: BugStatus) {
  let query = getSupabase().from("bug_reports").select(SELECT_FIELDS).order("created_at", { ascending: false });
  if (status) query = query.eq("status", status);
  const { data, error } = await query;
  if (error) throw error;
  return (data ?? []).map((row) => normalize(row as Record<string, unknown>));
}

export async function fetchMyBugReports(userId: string) {
  const { data, error } = await getSupabase()
    .from("bug_reports")
    .select(SELECT_FIELDS)
    .eq("user_id", userId)
    .order("created_at", { ascending: false });
  if (error) throw error;
  return (data ?? []).map((row) => normalize(row as Record<string, unknown>));
}

export async function updateBugReportStatus(id: number, status: BugStatus, adminNote: string) {
  const { error } = await getSupabase()
    .from("bug_reports")
    .update({ status, admin_note: adminNote.trim(), updated_at: new Date().toISOString() })
    .eq("id", id);
  if (error) throw error;
}

export async function createBugReportScreenshotUrl(storagePath: string) {
  const { data, error } = await getSupabase().storage.from(BUCKET).createSignedUrl(storagePath, 3600);
  if (error) throw error;
  return data.signedUrl;
}

export async function deleteBugReport(id: number, screenshotPath: string | null) {
  const supabase = getSupabase();
  const { error } = await supabase.from("bug_reports").delete().eq("id", id);
  if (error) throw error;
  if (screenshotPath) await supabase.storage.from(BUCKET).remove([screenshotPath]);
}
