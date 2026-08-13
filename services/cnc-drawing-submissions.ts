import { getSupabase } from "@/services/supabase";

export type CncDrawingStatus = "pending" | "approved" | "rejected";

export type CncDrawingSubmission = {
  id: number;
  course_id: number | null;
  created_at: string;
  updated_at: string;
  student_id: string;
  lesson_id: string;
  file_name: string;
  storage_path: string;
  mime_type: string;
  size_bytes: number;
  status: CncDrawingStatus;
  teacher_feedback: string;
  reviewed_by: string | null;
  reviewed_at: string | null;
  profiles?: { full_name: string; class_name: string } | null;
};

const BUCKET = "cnc-drawings";
const SELECT_FIELDS = "id, course_id, created_at, updated_at, student_id, lesson_id, file_name, storage_path, mime_type, size_bytes, status, teacher_feedback, reviewed_by, reviewed_at";

function safeFileName(name: string) {
  const extension = name.includes(".") ? `.${name.split(".").pop()}` : "";
  const stem = name
    .replace(/\.[^.]+$/, "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-zA-Z0-9_-]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .toLowerCase();
  return `${stem || "ban-ve"}${extension.toLowerCase()}`;
}

export async function fetchMyCncDrawingSubmission(lessonId: string, courseId?: number) {
  const supabase = getSupabase();
  const { data: authData } = await supabase.auth.getUser();
  if (!authData.user) return null;
  let query = supabase
    .from("cnc_drawing_submissions")
    .select(SELECT_FIELDS)
    .eq("student_id", authData.user.id)
    .eq("lesson_id", lessonId);
  query = courseId ? query.eq("course_id", courseId) : query.is("course_id", null);
  const { data, error } = await query.maybeSingle();
  if (error) throw error;
  return data as CncDrawingSubmission | null;
}

export async function submitCncDrawing({ lessonId, file, courseId }: { lessonId: string; file: File; courseId?: number }) {
  const supabase = getSupabase();
  const { data: authData, error: authError } = await supabase.auth.getUser();
  if (authError || !authData.user) throw new Error("Hãy đăng nhập bằng tài khoản sinh viên trước khi nộp bản vẽ.");

  const existing = await fetchMyCncDrawingSubmission(lessonId, courseId);
  if (existing?.status === "pending") throw new Error("Bản vẽ đang chờ giảng viên duyệt.");
  if (existing?.status === "approved") throw new Error("Bản vẽ đã được duyệt, không cần nộp lại.");

  const path = `${authData.user.id}/${lessonId}/${Date.now()}-${safeFileName(file.name)}`;
  const { error: uploadError } = await supabase.storage
    .from(BUCKET)
    .upload(path, file, { contentType: file.type || "application/octet-stream", upsert: false });
  if (uploadError) throw uploadError;

  const payload = {
    course_id: courseId ?? null,
    student_id: authData.user.id,
    lesson_id: lessonId,
    file_name: file.name,
    storage_path: path,
    mime_type: file.type || "application/octet-stream",
    size_bytes: file.size,
    status: "pending" as const,
    teacher_feedback: "",
    reviewed_by: null,
    reviewed_at: null,
    updated_at: new Date().toISOString(),
  };

  const query = existing
    ? supabase.from("cnc_drawing_submissions").update(payload).eq("id", existing.id)
    : supabase.from("cnc_drawing_submissions").insert(payload);
  const { data, error } = await query.select(SELECT_FIELDS).single();
  if (error) {
    await supabase.storage.from(BUCKET).remove([path]);
    throw error;
  }
  if (existing?.storage_path) await supabase.storage.from(BUCKET).remove([existing.storage_path]);
  return data as CncDrawingSubmission;
}

export async function fetchAllCncDrawingSubmissions() {
  const { data, error } = await getSupabase()
    .from("cnc_drawing_submissions")
    .select(`${SELECT_FIELDS}, profiles!cnc_drawing_submissions_student_id_fkey(full_name, class_name)`)
    .order("updated_at", { ascending: false });
  if (error) throw error;
  return (data ?? []).map((item) => ({
    ...item,
    profiles: Array.isArray(item.profiles) ? (item.profiles[0] ?? null) : item.profiles,
  })) as CncDrawingSubmission[];
}

export async function createCncDrawingDownloadUrl(storagePath: string) {
  const { data, error } = await getSupabase().storage.from(BUCKET).createSignedUrl(storagePath, 3600);
  if (error) throw error;
  return data.signedUrl;
}

export async function reviewCncDrawingSubmission(id: number, status: "approved" | "rejected", teacherFeedback: string) {
  const supabase = getSupabase();
  const { data: authData, error: authError } = await supabase.auth.getUser();
  if (authError || !authData.user) throw new Error("Phiên đăng nhập quản trị không hợp lệ.");
  const { data, error } = await supabase
    .from("cnc_drawing_submissions")
    .update({
      status,
      teacher_feedback: teacherFeedback.trim(),
      reviewed_by: authData.user.id,
      reviewed_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    })
    .eq("id", id)
    .select(SELECT_FIELDS)
    .single();
  if (error) throw error;
  return data as CncDrawingSubmission;
}
