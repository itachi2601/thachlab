import type { SchoolClass } from "@/features/exams/types";
import { getSupabase } from "@/services/supabase";

// Phân công giảng viên theo khối lớp THPT — song song với services/course-instructors.ts (CTTC).

export interface ClassInstructor {
  class_id: number;
  instructor_id: string;
  assigned_at: string;
  profiles: { id: string; full_name: string; class_name: string } | null;
}

export async function fetchClassInstructors(classId: number) {
  const { data, error } = await getSupabase().from("class_instructors")
    .select("class_id, instructor_id, assigned_at, profiles!class_instructors_instructor_id_fkey(id, full_name, class_name)")
    .eq("class_id", classId);
  if (error) throw error;
  return (data ?? []).map((row) => ({ ...row, profiles: Array.isArray(row.profiles) ? row.profiles[0] ?? null : row.profiles })) as ClassInstructor[];
}

export async function assignClassInstructor(classId: number, instructorId: string) {
  const supabase = getSupabase();
  const { data: auth } = await supabase.auth.getUser();
  const { error } = await supabase.from("class_instructors").upsert(
    { class_id: classId, instructor_id: instructorId, assigned_by: auth.user?.id ?? null },
    { onConflict: "class_id,instructor_id" },
  );
  if (error) throw error;
}

export async function unassignClassInstructor(classId: number, instructorId: string) {
  const { error } = await getSupabase().from("class_instructors").delete().eq("class_id", classId).eq("instructor_id", instructorId);
  if (error) throw error;
}

/** Khối lớp mà 1 giảng viên đang được phân công dạy — dùng cho dashboard giáo viên THPT. */
export async function fetchInstructorClasses(instructorId: string) {
  const { data, error } = await getSupabase().from("class_instructors")
    .select("classes(id, name, slug, color, icon, sort_order, active)")
    .eq("instructor_id", instructorId);
  if (error) throw error;
  return (data ?? [])
    .map((row) => (Array.isArray(row.classes) ? row.classes[0] ?? null : row.classes))
    .filter((schoolClass): schoolClass is SchoolClass => Boolean(schoolClass))
    .sort((a, b) => a.sort_order - b.sort_order);
}
