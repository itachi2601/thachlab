"use client";

import { useEffect, useState } from "react";
import { CncVideosAdmin } from "@/components/admin/CncMediaPanels";
import { useToast } from "@/components/ui/Toast";
import { fetchCncLessons, type CncLesson } from "@/services/cnc-lessons";
import {
  createCncLessonVideo,
  deleteCncLessonVideo,
  fetchCncLessonVideos,
  getYouTubeVideoId,
  type CncLessonVideo,
} from "@/services/cnc-lesson-videos";

export default function CncVideoAdmin() {
  const toast = useToast();
  const [lessons, setLessons] = useState<CncLesson[]>([]);
  const [lessonId, setLessonId] = useState<string | null>(null);
  const [videos, setVideos] = useState<CncLessonVideo[]>([]);
  const [loading, setLoading] = useState(true);
  const [ready, setReady] = useState(true);
  const [adding, setAdding] = useState(false);
  const [title, setTitle] = useState("");
  const [url, setUrl] = useState("");

  useEffect(() => {
    fetchCncLessons()
      .then((ls) => {
        setLessons(ls);
        setLessonId((current) => current ?? ls[0]?.id ?? null);
      })
      .catch(() => setLessons([]));
  }, []);

  useEffect(() => {
    if (!lessonId) return;
    let cancelled = false;
    setLoading(true);
    setTitle("");
    setUrl("");
    fetchCncLessonVideos(lessonId)
      .then((v) => {
        if (!cancelled) {
          setVideos(v);
          setReady(true);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setVideos([]);
          setReady(false);
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [lessonId]);

  async function handleAdd() {
    if (!lessonId) return;
    if (!title.trim()) {
      toast("error", "Hãy nhập tên video");
      return;
    }
    if (!getYouTubeVideoId(url)) {
      toast("error", "Liên kết YouTube không hợp lệ");
      return;
    }
    setAdding(true);
    try {
      const video = await createCncLessonVideo({ lessonId, title, youtubeUrl: url, sortOrder: videos.length });
      setVideos((current) => [...current, video]);
      setTitle("");
      setUrl("");
      setReady(true);
      toast("success", "Đã thêm video vào bài học.");
    } catch (error) {
      setReady(false);
      toast("error", `Không thêm được video: ${error instanceof Error ? error.message : error}`);
    } finally {
      setAdding(false);
    }
  }

  async function handleDelete(video: CncLessonVideo) {
    try {
      await deleteCncLessonVideo(video.id);
      setVideos((current) => current.filter((v) => v.id !== video.id));
      toast("success", "Đã xóa video khỏi bài học.");
    } catch (error) {
      toast("error", `Không xóa được video: ${error instanceof Error ? error.message : error}`);
    }
  }

  const activeLesson = lessons.find((l) => l.id === lessonId) ?? null;

  return (
    <div className="space-y-6">
      <header>
        <p className="admin-lead" style={{ marginTop: 0 }}>
          Chọn bài học rồi đăng video YouTube — mỗi bài có thể có nhiều video.
        </p>
      </header>

      <label className="block text-sm text-slate-300">
        Bài học
        <select
          value={lessonId ?? ""}
          onChange={(e) => setLessonId(e.target.value || null)}
          className="mt-1 w-full rounded-xl border border-white/10 bg-panel px-3 py-2 text-white sm:max-w-md"
        >
          {lessons.map((l) => (
            <option key={l.id} value={l.id}>
              {l.title}
            </option>
          ))}
        </select>
      </label>

      {activeLesson && (
        <CncVideosAdmin
          lessonTitle={activeLesson.shortTitle}
          videos={videos}
          loading={loading}
          ready={ready}
          adding={adding}
          title={title}
          url={url}
          onTitleChange={setTitle}
          onUrlChange={setUrl}
          onAdd={handleAdd}
          onDelete={handleDelete}
        />
      )}
      {!activeLesson && lessons.length === 0 && (
        <p className="text-sm text-slate-400">Chưa có bài học nào — thêm bài học trước ở trang Bài học.</p>
      )}
    </div>
  );
}
