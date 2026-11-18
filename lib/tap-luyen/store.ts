// Lưu buổi tập + số đo. Buổi đang tập giữ ở localStorage (tải lại trang không mất);
// bấm Kết thúc → ghi Supabase; lỗi mạng/chưa chạy migration → vào hàng chờ, lần mở sau tự gửi lại.
import { getSupabase } from "@/services/supabase";

export type SetKind = "w" | "n"; // khởi động | làm việc
export type LoggedSet = { kind: SetKind; kg: number | null; reps: number | null; sec: number | null; done: boolean };
export type LoggedExercise = { id: string; name: string; note?: string; rest: number; lo?: number; hi?: number; sets: LoggedSet[] };
export type Workout = {
  client_id: string;
  routine_key: string | null;
  title: string;
  started_at: string;
  ended_at: string;
  exercises: LoggedExercise[];
  note?: string | null;
};
export type Measurement = {
  measured_on: string;
  height_cm: number | null;
  weight_kg: number | null;
  chest_cm: number | null;
  waist_cm: number | null;
  hip_cm: number | null;
  shoulder_cm: number | null;
  arm_cm: number | null;
  note?: string | null;
};

const K_DRAFT = "tapluyen:draft";
const K_QUEUE = "tapluyen:queue";
const K_CACHE = "tapluyen:cache";
const K_MCACHE = "tapluyen:mcache";

function lsGet<T>(k: string, fb: T): T {
  try {
    const v = localStorage.getItem(k);
    return v ? (JSON.parse(v) as T) : fb;
  } catch {
    return fb;
  }
}
function lsSet(k: string, v: unknown) {
  try {
    if (v == null) localStorage.removeItem(k);
    else localStorage.setItem(k, JSON.stringify(v));
  } catch {
    /* bộ nhớ đầy / chế độ ẩn danh */
  }
}

export type Draft = Omit<Workout, "ended_at">;
export const loadDraft = () => lsGet<Draft | null>(K_DRAFT, null);
export const saveDraft = (d: Draft | null) => lsSet(K_DRAFT, d);

export const newId = () =>
  typeof crypto !== "undefined" && "randomUUID" in crypto ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(36).slice(2)}`;

const queue = () => lsGet<Workout[]>(K_QUEUE, []);
export const pendingCount = () => queue().length;

async function upsertWorkout(w: Workout) {
  const { error } = await getSupabase().from("workout_logs").upsert(w, { onConflict: "user_id,client_id" });
  if (error) throw error;
}

/** Ghi buổi tập; trả về true nếu đã lên máy chủ, false nếu đang nằm hàng chờ. */
export async function saveWorkout(w: Workout): Promise<boolean> {
  const cache = lsGet<Workout[]>(K_CACHE, []).filter((x) => x.client_id !== w.client_id);
  lsSet(K_CACHE, [w, ...cache].slice(0, 200));
  try {
    await upsertWorkout(w);
    return true;
  } catch {
    lsSet(K_QUEUE, [...queue().filter((x) => x.client_id !== w.client_id), w]);
    return false;
  }
}

export async function flushQueue(): Promise<number> {
  const q = queue();
  const left: Workout[] = [];
  for (const w of q) {
    try {
      await upsertWorkout(w);
    } catch {
      left.push(w);
    }
  }
  lsSet(K_QUEUE, left);
  return q.length - left.length;
}

export async function fetchWorkouts(): Promise<{ list: Workout[]; offline: boolean }> {
  const local = [...queue(), ...lsGet<Workout[]>(K_CACHE, [])];
  try {
    const { data, error } = await getSupabase()
      .from("workout_logs")
      .select("client_id,routine_key,title,started_at,ended_at,exercises,note")
      .order("started_at", { ascending: false })
      .limit(300);
    if (error) throw error;
    const server = (data ?? []) as Workout[];
    const ids = new Set(server.map((w) => w.client_id));
    const merged = [...queue().filter((w) => !ids.has(w.client_id)), ...server];
    lsSet(K_CACHE, server.slice(0, 200));
    return { list: sortWorkouts(merged), offline: false };
  } catch {
    const seen = new Set<string>();
    return { list: sortWorkouts(local.filter((w) => !seen.has(w.client_id) && seen.add(w.client_id))), offline: true };
  }
}
const sortWorkouts = (l: Workout[]) => [...l].sort((a, b) => b.started_at.localeCompare(a.started_at));

export async function deleteWorkout(clientId: string) {
  lsSet(K_CACHE, lsGet<Workout[]>(K_CACHE, []).filter((x) => x.client_id !== clientId));
  lsSet(K_QUEUE, queue().filter((x) => x.client_id !== clientId));
  const { error } = await getSupabase().from("workout_logs").delete().eq("client_id", clientId);
  if (error) throw error;
}

export async function fetchMeasurements(): Promise<{ list: Measurement[]; offline: boolean }> {
  try {
    const { data, error } = await getSupabase()
      .from("body_measurements")
      .select("measured_on,height_cm,weight_kg,chest_cm,waist_cm,hip_cm,shoulder_cm,arm_cm,note")
      .order("measured_on", { ascending: true });
    if (error) throw error;
    const list = (data ?? []).map((r) => {
      const o = { ...r } as Record<string, unknown>;
      for (const k of Object.keys(o)) if (k.endsWith("_cm") || k.endsWith("_kg")) o[k] = o[k] == null ? null : Number(o[k]);
      return o as Measurement;
    });
    lsSet(K_MCACHE, list);
    return { list, offline: false };
  } catch {
    return { list: lsGet<Measurement[]>(K_MCACHE, []), offline: true };
  }
}

export async function saveMeasurement(m: Measurement) {
  const { error } = await getSupabase().from("body_measurements").upsert(m, { onConflict: "user_id,measured_on" });
  if (error) throw error;
}
export async function deleteMeasurement(date: string) {
  const { error } = await getSupabase().from("body_measurements").delete().eq("measured_on", date);
  if (error) throw error;
}

// ---- tính toán ----
/** 1RM ước lượng (Epley), chỉ hiệp làm việc đã tick. */
export const e1rm = (kg: number, reps: number) => (reps <= 1 ? kg : kg * (1 + reps / 30));
export function workoutStats(w: { exercises: LoggedExercise[] }) {
  let volume = 0,
    sets = 0;
  for (const e of w.exercises)
    for (const s of e.sets)
      if (s.done && s.kind === "n") {
        sets++;
        if (s.kg && s.reps) volume += s.kg * s.reps;
      }
  return { volume, sets };
}
/** Hiệp làm việc lần gần nhất của bài `exId` (để hiện cột "Lần trước"). */
export function lastSetsOf(list: Workout[], exId: string, before?: string): LoggedSet[] {
  for (const w of list) {
    if (before && w.started_at >= before) continue;
    const e = w.exercises.find((x) => x.id === exId);
    const done = e?.sets.filter((s) => s.done);
    if (done?.length) return done;
  }
  return [];
}
export function bestE1rmHistory(list: Workout[], exId: string) {
  const pts: { date: string; v: number; top: string }[] = [];
  for (const w of [...list].reverse()) {
    const e = w.exercises.find((x) => x.id === exId);
    if (!e) continue;
    let best = 0,
      top = "";
    for (const s of e.sets)
      if (s.done && s.kind === "n" && s.kg && s.reps) {
        const v = e1rm(s.kg, s.reps);
        if (v > best) {
          best = v;
          top = `${fmtKg(s.kg)} kg × ${s.reps}`;
        }
      }
    if (best) pts.push({ date: w.started_at.slice(0, 10), v: Math.round(best * 10) / 10, top });
  }
  return pts;
}
export const fmtKg = (n: number) => String(Math.round(n * 100) / 100).replace(".", ",");
