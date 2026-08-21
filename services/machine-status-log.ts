import { getSupabase } from "@/services/supabase";
import type { MachineStatus } from "@/services/attendance-machine";

export interface MachineStatusLogEntry {
  id: number;
  machine_code: string;
  status: MachineStatus;
  note: string;
  created_by: string | null;
  updated_by: string | null;
  created_at: string;
  updated_at: string;
  profiles?: { full_name: string } | null;
}

const SELECT_FIELDS = "id, machine_code, status, note, created_by, updated_by, created_at, updated_at, profiles!machine_status_log_created_by_fkey(full_name)";

function normalize(row: Record<string, unknown>) {
  return { ...row, profiles: Array.isArray(row.profiles) ? (row.profiles[0] ?? null) : row.profiles } as MachineStatusLogEntry;
}

export async function fetchMachineStatusLog(machineCode: string) {
  const { data, error } = await getSupabase().from("machine_status_log")
    .select(SELECT_FIELDS).eq("machine_code", machineCode).order("created_at", { ascending: false });
  if (error) throw error;
  return (data ?? []).map(normalize);
}

export async function addMachineStatusLog(machineCode: string, status: MachineStatus, note: string) {
  const { error } = await getSupabase().rpc("add_machine_status_log", { p_machine_code: machineCode, p_status: status, p_note: note.trim() });
  if (error) throw error;
}

export async function updateMachineStatusLog(id: number, status: MachineStatus, note: string, createdAt?: string) {
  const { error } = await getSupabase().rpc("update_machine_status_log", {
    p_id: id, p_status: status, p_note: note.trim(), p_created_at: createdAt ?? null,
  });
  if (error) throw error;
}
