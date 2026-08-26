import { getSupabase } from "@/services/supabase";

export type EnrollmentStatus = "pending" | "active" | "rejected" | "suspended" | "completed" | "left";
export type EnrollmentMode = "approval" | "automatic" | "closed";

export interface CourseOffering {
  id: number; name: string; class_label: string; school_year: string; join_code: string;
  enrollment_mode: EnrollmentMode; status: "draft" | "active" | "completed" | "archived";
  starts_at: string | null; ends_at: string | null;
}

export interface EnrollmentRow {
  course_id: number; student_id: string; status: EnrollmentStatus; enrolled_at: string;
  profiles: { id: string; full_name: string; class_name: string } | null;
}

export async function fetchCncCourses(subjectCode: string = "cnc") {
  const { data, error } = await getSupabase().from("course_offerings")
    .select("id, name, class_label, school_year, join_code, enrollment_mode, status, starts_at, ends_at, subjects!inner(code)")
    .eq("subjects.code", subjectCode).order("school_year", { ascending: false });
  if (error) throw error;
  return (data ?? []) as unknown as CourseOffering[];
}

export async function createCncCourse(input: Pick<CourseOffering, "name" | "class_label" | "school_year" | "enrollment_mode">, subjectCode: string = "cnc", joinPrefix: string = "CNC") {
  const supabase = getSupabase();
  const [{ data: subject, error: subjectError }, { data: auth }] = await Promise.all([
    supabase.from("subjects").select("id").eq("code", subjectCode).single(), supabase.auth.getUser(),
  ]);
  if (subjectError) throw subjectError;
  const joinCode = `${joinPrefix}-${crypto.randomUUID().replaceAll("-", "").slice(0, 6).toUpperCase()}`;
  const { error } = await supabase.from("course_offerings").insert({
    subject_id: subject.id, created_by: auth.user?.id ?? null, ...input, join_code: joinCode, status: "active",
  });
  if (error) throw error;
}

export async function fetchCourseEnrollments(courseId: number) {
  const { data, error } = await getSupabase().from("course_enrollments")
    .select("course_id, student_id, status, enrolled_at, profiles!course_enrollments_student_id_fkey(id, full_name, class_name)")
    .eq("course_id", courseId).order("enrolled_at");
  if (error) throw error;
  return (data ?? []).map((row) => ({ ...row, profiles: Array.isArray(row.profiles) ? row.profiles[0] ?? null : row.profiles })) as EnrollmentRow[];
}

export async function reviewEnrollment(courseId: number, studentId: string, status: "active" | "rejected" | "suspended" | "left") {
  const supabase = getSupabase();
  const { data: auth } = await supabase.auth.getUser();
  const { error } = await supabase.from("course_enrollments").update({
    status, approved_by: auth.user?.id ?? null, approved_at: status === "active" ? new Date().toISOString() : null,
  }).eq("course_id", courseId).eq("student_id", studentId);
  if (error) throw error;
}

export async function requestEnrollment(joinCode: string) {
  const { data, error } = await getSupabase().rpc("request_course_enrollment", { p_join_code: joinCode.trim() });
  if (error) throw error;
  return data as { course_id: number; course_name: string; subject_code: string; school_year: string; status: EnrollmentStatus };
}

export async function fetchMyActiveCncCourse(userId: string, subjectCode: string = "cnc") {
  const { data, error } = await getSupabase().from("course_enrollments")
    .select("status, course_offerings!inner(id, name, class_label, school_year, status, subjects!inner(code))")
    .eq("student_id", userId).eq("course_offerings.subjects.code", subjectCode)
    .in("status", ["pending", "active", "suspended"]).order("enrolled_at", { ascending: false });
  if (error) throw error;
  const row = data?.[0];
  if (!row) return null;
  const course = Array.isArray(row.course_offerings) ? row.course_offerings[0] : row.course_offerings;
  return { status: row.status as EnrollmentStatus, course: course as unknown as { id: number; name: string; class_label: string; school_year: string } };
}

export async function fetchMyEnrollment(userId: string) {
  const { data, error } = await getSupabase().from("course_enrollments")
    .select("status, course_offerings!inner(id, name, class_label, school_year, status, subjects!inner(code, name))")
    .eq("student_id", userId)
    .in("status", ["pending", "active", "suspended"]).order("enrolled_at", { ascending: false });
  if (error) throw error;
  const row = data?.[0];
  if (!row) return null;
  const course = Array.isArray(row.course_offerings) ? row.course_offerings[0] : row.course_offerings;
  const subject = Array.isArray(course.subjects) ? course.subjects[0] : course.subjects;
  return {
    status: row.status as EnrollmentStatus,
    subjectCode: subject.code as string,
    subjectName: subject.name as string,
    course: course as unknown as { id: number; name: string; class_label: string; school_year: string; status: string },
  };
}

export async function fetchMyCncEnrollments(userId: string, subjectCode: string = "cnc") {
  const { data, error } = await getSupabase().from("course_enrollments")
    .select("status, enrolled_at, course_offerings!inner(id, name, class_label, school_year, status, subjects!inner(code))")
    .eq("student_id", userId)
    .eq("course_offerings.subjects.code", subjectCode)
    .in("status", ["pending", "active", "suspended"])
    .order("enrolled_at", { ascending: false });
  if (error) throw error;
  return (data ?? []).map((row) => ({
    status: row.status as EnrollmentStatus,
    enrolled_at: row.enrolled_at as string,
    course: (Array.isArray(row.course_offerings) ? row.course_offerings[0] : row.course_offerings) as unknown as {
      id: number; name: string; class_label: string; school_year: string; status: string;
    },
  }));
}
