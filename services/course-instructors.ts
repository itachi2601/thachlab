import { getSupabase } from "@/services/supabase";

export interface AssignableProfile {
  id: string;
  full_name: string;
  class_name: string;
  student_code: string | null;
  role: "student" | "admin" | "instructor";
  admin_area: "thpt" | "cttc" | null;
}

export async function searchProfiles(query: string) {
  const supabase = getSupabase();
  let request = supabase.from("profiles").select("id, full_name, class_name, student_code, role, admin_area").order("full_name").limit(20);
  const trimmed = query.trim();
  if (trimmed) request = request.or(`full_name.ilike.%${trimmed}%,class_name.ilike.%${trimmed}%,student_code.ilike.%${trimmed}%`);
  const { data, error } = await request;
  if (error) throw error;
  return (data ?? []) as AssignableProfile[];
}

export async function setInstructorRole(profileId: string, isInstructor: boolean) {
  const { error } = await getSupabase().from("profiles").update({
    role: isInstructor ? "instructor" : "student",
    // Thu hồi vai trò giảng viên thì cũng thu hồi luôn quyền vào khu vực quản trị.
    ...(isInstructor ? {} : { admin_area: null }),
  }).eq("id", profileId);
  if (error) throw error;
}

/** Phân công (hoặc thu hồi, area = null) khu vực quản trị mà 1 giảng viên được vào /quan-tri. */
export async function setInstructorAdminArea(profileId: string, area: "thpt" | "cttc" | null) {
  const { error } = await getSupabase().from("profiles").update({ admin_area: area }).eq("id", profileId);
  if (error) throw error;
}

export async function fetchInstructorRoster() {
  const { data, error } = await getSupabase().from("profiles").select("id, full_name, class_name").eq("role", "instructor").order("full_name");
  if (error) throw error;
  return (data ?? []) as { id: string; full_name: string; class_name: string }[];
}

export interface CourseInstructor {
  course_id: number;
  instructor_id: string;
  assigned_at: string;
  profiles: { id: string; full_name: string; class_name: string } | null;
}

export async function fetchCourseInstructors(courseId: number) {
  const { data, error } = await getSupabase().from("course_instructors")
    .select("course_id, instructor_id, assigned_at, profiles!course_instructors_instructor_id_fkey(id, full_name, class_name)")
    .eq("course_id", courseId);
  if (error) throw error;
  return (data ?? []).map((row) => ({ ...row, profiles: Array.isArray(row.profiles) ? row.profiles[0] ?? null : row.profiles })) as CourseInstructor[];
}

export async function assignInstructor(courseId: number, instructorId: string) {
  const supabase = getSupabase();
  const { data: auth } = await supabase.auth.getUser();
  const { error } = await supabase.from("course_instructors").upsert(
    { course_id: courseId, instructor_id: instructorId, assigned_by: auth.user?.id ?? null },
    { onConflict: "course_id,instructor_id" },
  );
  if (error) throw error;
}

export async function unassignInstructor(courseId: number, instructorId: string) {
  const { error } = await getSupabase().from("course_instructors").delete().eq("course_id", courseId).eq("instructor_id", instructorId);
  if (error) throw error;
}
