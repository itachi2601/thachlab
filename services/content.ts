import type { Difficulty } from "@/features/exams/types";
import { getSupabase } from "@/services/supabase";

export interface ExamMeta {
  id: number;
  title: string;
  duration_minutes: number;
  question_count: number;
  topic: string;
  difficulty: Difficulty;
  created_at: string;
  classIds: number[];
  subjectCode: string;
}

export type PostContentType = "thong_bao" | "tai_lieu" | "video";

export interface PostMeta {
  id: number;
  created_at: string;
  title: string;
  body: string;
  video_url: string;
  content_type: PostContentType;
  classIds: number[];
  courseIds: number[];
  subjectCode: string;
}

interface ClassRef {
  class_id: number;
}

interface CourseRef {
  course_id: number;
}

export async function fetchPublishedExams(): Promise<ExamMeta[]> {
  const { data } = await getSupabase()
    .from("exams")
    .select(
      "id, title, duration_minutes, question_count, topic, difficulty, created_at, subject_code, exam_classes(class_id)",
    )
    .eq("published", true)
    .order("created_at", { ascending: false });
  return (data ?? []).map((e) => ({
    ...e,
    classIds: ((e.exam_classes as ClassRef[]) ?? []).map((c) => c.class_id),
    subjectCode: e.subject_code ?? "vat-ly",
  })) as ExamMeta[];
}

export async function fetchPublishedPosts(): Promise<PostMeta[]> {
  const { data } = await getSupabase()
    .from("posts")
    .select(
      "id, created_at, title, body, video_url, content_type, subject_code, post_classes(class_id), post_courses(course_id)",
    )
    .eq("published", true)
    .order("created_at", { ascending: false });
  return (data ?? []).map((p) => ({
    ...p,
    content_type: (p.content_type as PostContentType) ?? "thong_bao",
    classIds: ((p.post_classes as ClassRef[]) ?? []).map((c) => c.class_id),
    courseIds: ((p.post_courses as CourseRef[]) ?? []).map((c) => c.course_id),
    subjectCode: p.subject_code ?? "vat-ly",
  })) as PostMeta[];
}

/** Nội dung không gán lớp = toàn trường; có gán = phải trùng lớp người xem. */
export function visibleTo(itemClassIds: number[], myClassIds: number[] | null) {
  if (itemClassIds.length === 0) return true;
  if (myClassIds === null) return true; // admin / chưa lọc
  return itemClassIds.some((id) => myClassIds.includes(id));
}

/**
 * Bài đăng cho học viên CTTC theo khóa học. Bài chỉ gán lớp THPT (không gán
 * khóa nào) không được coi là "toàn trường" ở đây — tránh rò bài THPT sang
 * feed CNC/CTTC. Chỉ bài không gán cả lớp lẫn khóa mới là toàn trường thật sự.
 */
export function visibleToCourse(
  itemCourseIds: number[],
  itemClassIds: number[],
  myCourseId: number | null,
) {
  if (myCourseId !== null && itemCourseIds.includes(myCourseId)) return true;
  return itemCourseIds.length === 0 && itemClassIds.length === 0;
}

interface PostTargetsInput {
  title: string;
  body: string;
  videoUrl: string;
  contentType: PostContentType;
  subjectCode: string;
  classIds: number[];
  courseIds: number[];
}

export async function createPostWithTargets(input: PostTargetsInput): Promise<number> {
  const { data, error } = await getSupabase().rpc("create_post_with_targets", {
    p_title: input.title,
    p_body: input.body,
    p_video_url: input.videoUrl,
    p_content_type: input.contentType,
    p_subject_code: input.subjectCode,
    p_class_ids: input.classIds,
    p_course_ids: input.courseIds,
  });
  if (error) throw error;
  return data as number;
}

export async function updatePostWithTargets(
  postId: number,
  input: PostTargetsInput,
): Promise<void> {
  const { error } = await getSupabase().rpc("update_post_with_targets", {
    p_post_id: postId,
    p_title: input.title,
    p_body: input.body,
    p_video_url: input.videoUrl,
    p_content_type: input.contentType,
    p_subject_code: input.subjectCode,
    p_class_ids: input.classIds,
    p_course_ids: input.courseIds,
  });
  if (error) throw error;
}
