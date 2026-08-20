import { getSupabase } from "@/services/supabase";
import { compressImageFile } from "@/services/image-compress";

export type MachineCheckpoint = "start" | "end";
export type MachineType = "cnc_turn" | "cnc_mill" | "manual_turn" | "manual_mill" | "auxiliary";
export type MachineStatus = "ok" | "broken";

export const MACHINE_TYPE_LABELS: Record<MachineType, string> = {
  cnc_turn: "Máy tiện CNC",
  cnc_mill: "Máy phay CNC",
  manual_turn: "Máy tiện truyền thống",
  manual_mill: "Máy phay truyền thống",
  auxiliary: "Thiết bị khác",
};
const MACHINE_TYPE_ORDER: MachineType[] = ["cnc_turn", "cnc_mill", "manual_turn", "manual_mill", "auxiliary"];

export interface Machine {
  code: string;
  label: string;
  machine_type: MachineType;
  workshop: string;
  status: MachineStatus;
  note: string;
  is_active: boolean;
}

const MACHINE_FIELDS = "code, label, machine_type, workshop, status, note, is_active";

export async function fetchMachines() {
  const { data, error } = await getSupabase().from("machines")
    .select(MACHINE_FIELDS)
    .eq("is_active", true).order("machine_type").order("code");
  if (error) throw error;
  return (data ?? []) as Machine[];
}

export async function fetchAllMachines() {
  const { data, error } = await getSupabase().from("machines")
    .select(MACHINE_FIELDS)
    .order("workshop").order("machine_type").order("code");
  if (error) throw error;
  return (data ?? []) as Machine[];
}

export function groupMachinesByType(machines: Machine[]) {
  return MACHINE_TYPE_ORDER
    .map((type) => ({ type, label: MACHINE_TYPE_LABELS[type], machines: machines.filter((m) => m.machine_type === type) }))
    .filter((group) => group.machines.length > 0);
}

export function groupMachinesByWorkshop(machines: Machine[]) {
  const workshops = [...new Set(machines.map((m) => m.workshop))].sort();
  return workshops.map((workshop) => ({ workshop, machines: machines.filter((m) => m.workshop === workshop) }));
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

export interface AttendanceMachinePhoto {
  id: number; session_id: number; machine_code: string; checkpoint: MachineCheckpoint;
  storage_path: string; note: string; uploaded_by: string | null; created_at: string;
  profiles?: { full_name: string } | null;
}

export interface AttendanceMachineScore {
  session_id: number; machine_code: string;
  sang_loc: boolean; sap_xep: boolean; sach_se: boolean; san_soc: boolean; san_sang: boolean;
  note: string; updated_at: string;
}

export function fiveSScore(score?: AttendanceMachineScore) {
  if (!score) return 0;
  return FIVE_S_CRITERIA.reduce((sum, item) => sum + (score[item.key] ? 2 : 0), 0);
}

export async function selectAttendanceMachine(sessionId: number, machineCode: string) {
  const { error } = await getSupabase().rpc("select_attendance_machine", { p_session_id: sessionId, p_machine_code: machineCode });
  if (error) throw error;
}

export async function isPhotoDutyMachine(sessionId: number, machineCode: string) {
  const { data, error } = await getSupabase().rpc("is_photo_duty_machine", { p_session_id: sessionId, p_machine_code: machineCode });
  if (error) throw error;
  return Boolean(data);
}

export async function isPhotoDutyWorkshop(sessionId: number) {
  const { data, error } = await getSupabase().rpc("is_photo_duty_workshop", { p_session_id: sessionId });
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
  const { data, error } = await getSupabase().from("attendance_machine_scores").select("session_id, machine_code, sang_loc, sap_xep, sach_se, san_soc, san_sang, note, updated_at").eq("session_id", sessionId);
  if (error) throw error;
  return (data ?? []) as AttendanceMachineScore[];
}

export async function updateAttendanceMachineScore(sessionId: number, machineCode: string, patch: Partial<Pick<AttendanceMachineScore, FiveSKey | "note">>) {
  const { error } = await getSupabase().from("attendance_machine_scores").upsert({ session_id: sessionId, machine_code: machineCode, updated_at: new Date().toISOString(), ...patch }, { onConflict: "session_id,machine_code" });
  if (error) throw error;
}
