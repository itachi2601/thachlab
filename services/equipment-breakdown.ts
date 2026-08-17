import { getSupabase } from "@/services/supabase";
import { compressImageFile } from "@/services/image-compress";

export type EquipmentBreakdownReport = {
  id: number;
  course_id: number;
  session_id: number | null;
  machine_code: string;
  description: string;
  storage_path: string;
  status: "open" | "resolved";
  reported_by: string | null;
  resolved_by: string | null;
  resolved_at: string | null;
  resolved_note: string;
  created_at: string;
  profiles?: { full_name: string } | null;
};

const BUCKET = "equipment-breakdown-photos";
const SELECT_FIELDS = "id, course_id, session_id, machine_code, description, storage_path, status, reported_by, resolved_by, resolved_at, resolved_note, created_at, profiles!equipment_breakdown_reports_reported_by_fkey(full_name)";

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

export async function reportEquipmentBreakdown({ courseId, sessionId, machineCode, description, file }: { courseId: number; sessionId: number | null; machineCode: string; description: string; file: File }) {
  const supabase = getSupabase();
  const compressed = await compressImageFile(file);
  const path = `${courseId}/${machineCode}-${Date.now()}-${compressed.name}`;
  const { error: uploadError } = await supabase.storage.from(BUCKET).upload(path, compressed, { contentType: compressed.type || "application/octet-stream", upsert: false });
  if (uploadError) throw uploadError;
  const { data, error } = await supabase.rpc("report_equipment_breakdown", {
    p_course_id: courseId, p_session_id: sessionId, p_machine_code: machineCode, p_description: description.trim(), p_storage_path: path,
  });
  if (error) {
    await supabase.storage.from(BUCKET).remove([path]);
    throw error;
  }
  return data as number;
}

export async function resolveEquipmentBreakdown(id: number, note: string) {
  const { error } = await getSupabase().rpc("resolve_equipment_breakdown", { p_id: id, p_note: note.trim() });
  if (error) throw error;
}

export async function createEquipmentBreakdownPhotoUrl(storagePath: string) {
  const { data, error } = await getSupabase().storage.from(BUCKET).createSignedUrl(storagePath, 3600);
  if (error) throw error;
  return data.signedUrl;
}
