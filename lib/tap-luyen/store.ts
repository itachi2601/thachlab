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
  /** cần migration 20261119120000 — null/thiếu nếu chưa đo hoặc cột chưa có */
  neck_cm?: number | null;
  wrist_cm?: number | null;
  note?: string | null;
};

// Khoá localStorage theo tài khoản: máy dùng chung (phòng máy, máy ở nhà) không lẫn buổi tập của người khác,
// và hàng chờ của người trước không bị gửi lên dưới tài khoản người sau.
let uid = "";
const K = (name: string) => `tapluyen:${uid ? `${uid}:` : ""}${name}`;
const K_DRAFT = "draft", K_QUEUE = "queue", K_CACHE = "cache", K_MCACHE = "mcache";

/** Gọi trước mọi hàm lưu/đọc. `adoptLegacy`: chuyển dữ liệu khoá cũ (chưa theo tài khoản, chỉ giáo viên dùng trước 19/11/2026) về tài khoản này. */
export function setTapLuyenUser(id: string, adoptLegacy: boolean) {
  if (uid === id) return;
  uid = id;
  try {
    for (const n of [K_DRAFT, K_QUEUE, K_CACHE, K_MCACHE]) {
      const old = localStorage.getItem(`tapluyen:${n}`);
      if (old == null) continue;
      if (adoptLegacy && localStorage.getItem(K(n)) == null) localStorage.setItem(K(n), old);
      if (adoptLegacy) localStorage.removeItem(`tapluyen:${n}`);
    }
  } catch {
    /* chế độ ẩn danh */
  }
}

function lsGet<T>(k: string, fb: T): T {
  if (!uid) return fb;
  try {
    const v = localStorage.getItem(K(k));
    return v ? (JSON.parse(v) as T) : fb;
  } catch {
    return fb;
  }
}
function lsSet(k: string, v: unknown) {
  if (!uid) return;
  try {
    if (v == null) localStorage.removeItem(K(k));
    else localStorage.setItem(K(k), JSON.stringify(v));
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
    const base = "measured_on,height_cm,weight_kg,chest_cm,waist_cm,hip_cm,shoulder_cm,arm_cm,note";
    const q = (cols: string) => getSupabase().from("body_measurements").select(cols).order("measured_on", { ascending: true });
    let res = await q(`${base},neck_cm,wrist_cm`);
    if (res.error) res = await q(base); // chưa chạy migration thêm cổ/cổ tay → vẫn đọc được số đo cũ
    const { data, error } = res;
    if (error) throw error;
    const list = ((data ?? []) as unknown as Record<string, unknown>[]).map((r) => {
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
  // Chưa chạy migration neck/wrist thì gửi cột lạ sẽ lỗi cả lần lưu → chỉ gửi hai cột này khi có giá trị.
  const { neck_cm, wrist_cm, ...rest } = m;
  const row = { ...rest, ...(neck_cm != null ? { neck_cm } : {}), ...(wrist_cm != null ? { wrist_cm } : {}) };
  const { error } = await getSupabase().from("body_measurements").upsert(row, { onConflict: "user_id,measured_on" });
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

/** Buổi trong tuần (thứ Hai 0h giờ máy) và buổi nên tập tiếp: ưu tiên `focus`, rồi buổi đầu danh sách (A / 1), rồi buổi lâu chưa tập. */
export function weekPlan(list: Workout[], keys: string[], focus?: string | null) {
  const mon = new Date();
  mon.setHours(0, 0, 0, 0);
  mon.setDate(mon.getDate() - ((mon.getDay() + 6) % 7));
  const thisWeek = list.filter((w) => new Date(w.started_at) >= mon);
  const done = new Set(thisWeek.map((w) => w.routine_key));
  const lastOf = (k: string) => list.find((w) => w.routine_key === k);
  const left = keys.filter((k) => !done.has(k));
  const next =
    (focus && !done.has(focus) ? focus : null) ??
    (left.includes(keys[0]) ? keys[0] : [...left].sort((a, b) => (lastOf(a)?.started_at ?? "").localeCompare(lastOf(b)?.started_at ?? ""))[0]) ??
    null;
  return { count: thisWeek.length, done, next, lastOf };
}

/** Bài không tạ: số lần (hoặc số giây) tốt nhất trong các hiệp làm việc của mỗi buổi. */
export function bestCountHistory(list: Workout[], exId: string) {
  const pts: { date: string; v: number }[] = [];
  for (const w of [...list].reverse()) {
    const e = w.exercises.find((x) => x.id === exId);
    if (!e) continue;
    const best = Math.max(0, ...e.sets.filter((s) => s.done && s.kind === "n").map((s) => s.sec ?? s.reps ?? 0));
    if (best) pts.push({ date: w.started_at.slice(0, 10), v: best });
  }
  return pts;
}
