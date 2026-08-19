import { getSupabase } from "@/services/supabase";
import { compressImageFile } from "@/services/image-compress";

export type MachineCheckpoint = "start" | "end";
export type EquipmentStatus = "normal" | "maintenance" | "broken";
export type MachineType = "cnc_turn" | "cnc_mill" | "manual_turn" | "manual_mill";

export const MACHINE_TYPE_LABELS: Record<MachineType, string> = {
  cnc_turn: "Máy tiện CNC",
  cnc_mill: "Máy phay CNC",
  manual_turn: "Máy tiện truyền thống",
  manual_mill: "Máy phay truyền thống",
};
const MACHINE_TYPE_ORDER: MachineType[] = ["cnc_turn", "cnc_mill", "manual_turn", "manual_mill"];

export interface Machine {
  code: string;
  label: string;
  machine_type: MachineType;
  is_active: boolean;
}

export async function fetchMachines() {
  const { data, error } = await getSupabase().from("machines")
    .select("code, label, machine_type, is_active")
    .eq("is_active", true).order("machine_type").order("code");
  if (error) throw error;
  return (data ?? []) as Machine[];
}

export function groupMachinesByType(machines: Machine[]) {
  return MACHINE_TYPE_ORDER
    .map((type) => ({ type, label: MACHINE_TYPE_LABELS[type], machines: machines.filter((m) => m.machine_type === type) }))
    .filter((group) => group.machines.length > 0);
}

const BUCKET = "attendance-machine-photos";

export const FIVE_S_CRITERIA = [
  { key: "sang_loc", label: "Sàng lọc", hint: "Bỏ vật không cần" },
  { key: "sap_xep", label: "Sắp xếp", hint: "Dụng cụ đúng chỗ" },
  { key: "sach_se", label: "Sạch sẽ", hint: "Không phoi, dầu" },
  { key: "san_soc", label: "Săn sóc", hint: "Tự kiểm tra định kỳ" },
  { key: "san_sang", label: "Sẵn sàng", hint: "Máy an toàn, dùng ngay được" },
] as const;
export type FiveSKey = (typeof FIVE_S_CRITERIA)[number]["key"];

export const EQUIPMENT_STATUS_META: Record<EquipmentStatus, { label: string; style: string }> = {
  normal: { label: "Bình thường", style: "border-white/10 text-slate-300" },
  maintenance: { label: "Cần bảo trì", style: "border-amber-400/30 bg-amber-500/10 text-amber-200" },
  broken: { label: "Hỏng", style: "border-red-400/30 bg-red-500/10 text-red-200" },
};

export interface AttendanceMachinePhoto {
  id: number; session_id: number; machine_code: string; checkpoint: MachineCheckpoint;
  storage_path: string; note: string; uploaded_by: string | null; created_at: string;
  profiles?: { full_name: string } | null;
}

export interface AttendanceMachineScore {
  session_id: number; machine_code: string;
  sang_loc: boolean; sap_xep: boolean; sach_se: boolean; san_soc: boolean; san_sang: boolean;
  equipment_status: EquipmentStatus; note: string; updated_at: string;
}

export function fiveSScore(score?: AttendanceMachineScore) {
  if (!score) return 0;
  return FIVE_S_CRITERIA.reduce((sum, item) => sum + (score[item.key] ? 2 : 0), 0);
}

export async function selectAttendanceMachine(sessionId: number, machineCode: string) {
  const { error } = await getSupabase().rpc("select_attendance_machine", { p_session_id: sessionId, p_machine_code: machineCode });
  if (error) throw error;
}

export async function isFirstOnMachine(sessionId: number, machineCode: string) {
  const { data, error } = await getSupabase().rpc("is_first_on_machine", { p_session_id: sessionId, p_machine_code: machineCode });
  if (error) throw error;
  return Boolean(data);
}

export async function fetchAttendanceMachinePhotos(sessionId: number) {
  const { data, error } = await getSupabase().from("attendance_machine_photos")
    .select("id, session_id, machine_code, checkpoint, storage_path, note, uploaded_by, created_at, profiles!attendance_machine_photos_uploaded_by_fkey(full_name)")
    .eq("session_id", sessionId);
  if (error) throw error;
  return (data ?? []).map((row) => ({ ...row, profiles: Array.isArray(row.profiles) ? row.profiles[0] ?? null : row.profiles })) as AttendanceMachinePhoto[];
}

export async function submitAttendanceMachinePhoto({ sessionId, machineCode, checkpoint, file, note = "" }: { sessionId: number; machineCode: string; checkpoint: MachineCheckpoint; file: File; note?: string }) {
  const supabase = getSupabase();
  const { data: authData, error: authError } = await supabase.auth.getUser();
  if (authError || !authData.user) throw new Error("Hãy đăng nhập trước khi nộp ảnh.");
  const compressed = await compressImageFile(file);
  const extension = compressed.name.includes(".") ? `.${compressed.name.split(".").pop()}` : "";
  const path = `${sessionId}/${machineCode}-${checkpoint}-${Date.now()}${extension}`;
  const { error: uploadError } = await supabase.storage.from(BUCKET).upload(path, compressed, { contentType: compressed.type || "application/octet-stream", upsert: false });
  if (uploadError) throw uploadError;
  const { error } = await supabase.rpc("submit_attendance_machine_photo", { p_session_id: sessionId, p_machine_code: machineCode, p_checkpoint: checkpoint, p_storage_path: path, p_note: note });
  if (error) {
    await supabase.storage.from(BUCKET).remove([path]);
    throw error;
  }
}

export async function createAttendanceMachinePhotoUrl(storagePath: string) {
  const { data, error } = await getSupabase().storage.from(BUCKET).createSignedUrl(storagePath, 3600);
  if (error) throw error;
  return data.signedUrl;
}

export async function fetchAttendanceMachineScores(sessionId: number) {
  const { data, error } = await getSupabase().from("attendance_machine_scores").select("session_id, machine_code, sang_loc, sap_xep, sach_se, san_soc, san_sang, equipment_status, note, updated_at").eq("session_id", sessionId);
  if (error) throw error;
  return (data ?? []) as AttendanceMachineScore[];
}

export async function updateAttendanceMachineScore(sessionId: number, machineCode: string, patch: Partial<Pick<AttendanceMachineScore, FiveSKey | "equipment_status" | "note">>) {
  const { error } = await getSupabase().from("attendance_machine_scores").upsert({ session_id: sessionId, machine_code: machineCode, updated_at: new Date().toISOString(), ...patch }, { onConflict: "session_id,machine_code" });
  if (error) throw error;
}
