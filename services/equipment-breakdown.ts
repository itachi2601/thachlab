import { getSupabase } from "@/services/supabase";
import { compressImageFile } from "@/services/image-compress";

export type BreakdownStatus = "open" | "in_progress" | "resolved";

export type EquipmentBreakdownReport = {
  id: number;
  course_id: number;
  session_id: number | null;
  machine_code: string;
  description: string;
  broken_photo_path: string;
  resolved_photo_path: string | null;
  broken_at: string;
  status: BreakdownStatus;
  reported_by: string | null;
  resolved_by: string | null;
  resolved_at: string | null;
  resolved_note: string;
  created_at: string;
  profiles?: { full_name: string } | null;
};

const BUCKET = "equipment-breakdown-photos";
const SELECT_FIELDS = "id, course_id, session_id, machine_code, description, broken_photo_path, resolved_photo_path, broken_at, status, reported_by, resolved_by, resolved_at, resolved_note, created_at, profiles!equipment_breakdown_reports_reported_by_fkey(full_name)";

function normalize(row: Record<string, unknown>) {
  return { ...row, profiles: Array.isArray(row.profiles) ? (row.profiles[0] ?? null) : row.profiles } as EquipmentBreakdownReport;
}

export async function fetchEquipmentBreakdownReports(courseId: number) {
  const { data, error } = await getSupabase()
    .from("equipment_breakdown_reports")
    .select(SELECT_FIELDS)
    .eq("course_id", courseId)
    .order("created_at", { ascending: false });
  if (error) throw error;
  return (data ?? []).map(normalize);
}

export type EquipmentBreakdownReportWithCourse = EquipmentBreakdownReport & { course_offerings?: { name: string; class_label: string } | null };

// Lịch sử báo hỏng của 1 máy trên mọi khoá học — dùng cho trang tổng quan tình trạng máy (cấp bộ môn).
export async function fetchEquipmentBreakdownReportsByMachine(machineCode: string) {
  const { data, error } = await getSupabase()
    .from("equipment_breakdown_reports")
    .select(`${SELECT_FIELDS}, course_offerings(name, class_label)`)
    .eq("machine_code", machineCode)
    .order("broken_at", { ascending: false });
  if (error) throw error;
  return (data ?? []).map((row) => {
    const normalized = normalize(row as Record<string, unknown>) as EquipmentBreakdownReportWithCourse;
    const courseRaw = (row as Record<string, unknown>).course_offerings;
    normalized.course_offerings = Array.isArray(courseRaw) ? (courseRaw[0] ?? null) : (courseRaw as EquipmentBreakdownReportWithCourse["course_offerings"]) ?? null;
    return normalized;
  });
}

export async function reportEquipmentBreakdown({ courseId, sessionId, machineCode, description, brokenAt, file }: { courseId: number; sessionId: number | null; machineCode: string; description: string; brokenAt: string; file: File }) {
  const supabase = getSupabase();
  const compressed = await compressImageFile(file);
  const path = `${courseId}/${machineCode}-broken-${Date.now()}-${compressed.name}`;
  const { error: uploadError } = await supabase.storage.from(BUCKET).upload(path, compressed, { contentType: compressed.type || "application/octet-stream", upsert: false });
  if (uploadError) throw uploadError;
  const { data, error } = await supabase.rpc("report_equipment_breakdown", {
    p_course_id: courseId, p_session_id: sessionId, p_machine_code: machineCode, p_description: description.trim(), p_storage_path: path, p_broken_at: brokenAt,
  });
  if (error) {
    await supabase.storage.from(BUCKET).remove([path]);
    throw error;
  }
  return data as number;
}

export async function startEquipmentRepair(id: number) {
  const { error } = await getSupabase().rpc("start_equipment_repair", { p_id: id });
  if (error) throw error;
}

export async function resolveEquipmentBreakdown({ id, courseId, machineCode, note, file }: { id: number; courseId: number; machineCode: string; note: string; file: File }) {
  const supabase = getSupabase();
  const compressed = await compressImageFile(file);
  const path = `${courseId}/${machineCode}-resolved-${Date.now()}-${compressed.name}`;
  const { error: uploadError } = await supabase.storage.from(BUCKET).upload(path, compressed, { contentType: compressed.type || "application/octet-stream", upsert: false });
  if (uploadError) throw uploadError;
  const { error } = await supabase.rpc("resolve_equipment_breakdown", { p_id: id, p_note: note.trim(), p_resolved_photo_path: path });
  if (error) {
    await supabase.storage.from(BUCKET).remove([path]);
    throw error;
  }
}

export async function createEquipmentBreakdownPhotoUrl(storagePath: string) {
  const { data, error } = await getSupabase().storage.from(BUCKET).createSignedUrl(storagePath, 3600);
  if (error) throw error;
  return data.signedUrl;
}
