import { getSupabase } from "@/services/supabase";

export type CncLessonVideo = {
  id: number;
  lesson_id: string;
  title: string;
  youtube_url: string;
  youtube_id: string;
  sort_order: number;
  created_at: string;
};

export function getYouTubeVideoId(value: string) {
  const input = value.trim();
  if (/^[\w-]{11}$/.test(input)) return input;

  try {
    const url = new URL(input);
    const host = url.hostname.replace(/^www\./, "");
    if (host === "youtu.be") return url.pathname.split("/").filter(Boolean)[0] ?? null;
    if (host === "youtube.com" || host === "m.youtube.com") {
      if (url.pathname === "/watch") return url.searchParams.get("v");
      const parts = url.pathname.split("/").filter(Boolean);
      if (["embed", "shorts", "live"].includes(parts[0])) return parts[1] ?? null;
    }
  } catch {
    return null;
  }

  return null;
}

export function getYouTubeEmbedUrl(videoId: string) {
  return `https://www.youtube-nocookie.com/embed/${videoId}`;
}

export function getYouTubeThumbnailUrl(videoId: string) {
  return `https://i.ytimg.com/vi/${videoId}/hqdefault.jpg`;
}

const VIDEO_FIELDS =
  "id, lesson_id, title, youtube_url, youtube_id, sort_order, created_at";

export async function fetchCncLessonVideos(lessonId?: string) {
  let query = getSupabase()
    .from("cnc_lesson_videos")
    .select(VIDEO_FIELDS)
    .order("sort_order", { ascending: true })
    .order("created_at", { ascending: true });
  if (lessonId) query = query.eq("lesson_id", lessonId);
  const { data, error } = await query;
  if (error) throw error;
  return (data ?? []) as CncLessonVideo[];
}

export async function createCncLessonVideo({
  lessonId,
  title,
  youtubeUrl,
  sortOrder,
}: {
  lessonId: string;
  title: string;
  youtubeUrl: string;
  sortOrder: number;
}) {
  const youtubeId = getYouTubeVideoId(youtubeUrl);
  if (!youtubeId || youtubeId.length !== 11) {
    throw new Error("Liên kết YouTube không hợp lệ");
  }

  const normalizedUrl = `https://www.youtube.com/watch?v=${youtubeId}`;
  const { data, error } = await getSupabase()
    .from("cnc_lesson_videos")
    .insert({
      lesson_id: lessonId,
      title: title.trim() || "Video bài giảng",
      youtube_url: normalizedUrl,
      youtube_id: youtubeId,
      sort_order: sortOrder,
    })
    .select(VIDEO_FIELDS)
    .single();
  if (error) throw error;
  return data as CncLessonVideo;
}

export async function deleteCncLessonVideo(videoId: number) {
  const { error } = await getSupabase()
    .from("cnc_lesson_videos")
    .delete()
    .eq("id", videoId);
  if (error) throw error;
}
