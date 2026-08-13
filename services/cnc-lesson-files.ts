import { getSupabase } from "@/services/supabase";

export type CncLessonFileKind = "powerpoint" | "material";

export type CncLessonFile = {
  id: number;
  lesson_id: string;
  kind: CncLessonFileKind;
  title: string;
  file_name: string;
  file_url: string;
  storage_path: string;
  mime_type: string;
  size_bytes: number;
  created_at: string;
};

const BUCKET = "cnc-lessons";

function safeFileName(name: string) {
  const extension = name.includes(".") ? `.${name.split(".").pop()}` : "";
  const stem = name
    .replace(/\.[^.]+$/, "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-zA-Z0-9_-]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .toLowerCase();
  return `${stem || "tai-lieu"}${extension.toLowerCase()}`;
}

export async function fetchCncLessonFiles(lessonId?: string) {
  let query = getSupabase()
    .from("cnc_lesson_files")
    .select("id, lesson_id, kind, title, file_name, file_url, storage_path, mime_type, size_bytes, created_at")
    .order("created_at", { ascending: false });
  if (lessonId) query = query.eq("lesson_id", lessonId);
  const { data, error } = await query;
  if (error) throw error;
  return (data ?? []) as CncLessonFile[];
}

export async function uploadCncLessonFile({
  lessonId,
  kind,
  title,
  file,
}: {
  lessonId: string;
  kind: CncLessonFileKind;
  title: string;
  file: File;
}) {
  const supabase = getSupabase();
  const path = `${lessonId}/${kind}/${Date.now()}-${safeFileName(file.name)}`;
  const { error: uploadError } = await supabase.storage
    .from(BUCKET)
    .upload(path, file, { contentType: file.type || undefined, upsert: false });
  if (uploadError) throw uploadError;

  const { data: publicData } = supabase.storage.from(BUCKET).getPublicUrl(path);
  const { data, error } = await supabase
    .from("cnc_lesson_files")
    .insert({
      lesson_id: lessonId,
      kind,
      title: title.trim() || file.name,
      file_name: file.name,
      file_url: publicData.publicUrl,
      storage_path: path,
      mime_type: file.type || "application/octet-stream",
      size_bytes: file.size,
    })
    .select("id, lesson_id, kind, title, file_name, file_url, storage_path, mime_type, size_bytes, created_at")
    .single();

  if (error) {
    await supabase.storage.from(BUCKET).remove([path]);
    throw error;
  }
  return data as CncLessonFile;
}

export async function deleteCncLessonFile(file: CncLessonFile) {
  const supabase = getSupabase();
  const { error } = await supabase.from("cnc_lesson_files").delete().eq("id", file.id);
  if (error) throw error;
  const { error: storageError } = await supabase.storage
    .from(BUCKET)
    .remove([file.storage_path]);
  if (storageError) throw storageError;
}

export function formatFileSize(bytes: number) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}
