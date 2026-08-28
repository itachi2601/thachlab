"use client";

import { useCallback, useEffect, useState } from "react";
import ClassPicker from "@/components/admin/ClassPicker";
import CoursePicker from "@/components/admin/CoursePicker";
import {
  createPostWithTargets,
  updatePostWithTargets,
  type PostContentType,
} from "@/services/content";
import { fetchClasses } from "@/services/classes";
import { fetchAllCourseOfferings, type CourseOfferingWithSubject } from "@/services/course-enrollments";
import { getSupabase } from "@/services/supabase";
import { useToast } from "@/components/ui/Toast";
import { ACADEMIC_SUBJECTS, academicSubject } from "@/services/academic-subjects";
import type { SchoolClass } from "@/features/exams/types";

interface Post {
  id: number;
  created_at: string;
  title: string;
  body: string;
  video_url: string;
  published: boolean;
  subject_code: string;
  content_type: PostContentType;
  classIds: number[];
  courseIds: number[];
}

interface ClassRef {
  class_id: number;
}
interface CourseRef {
  course_id: number;
}

const CONTENT_TYPES: { value: PostContentType; label: string }[] = [
  { value: "thong_bao", label: "Thông báo" },
  { value: "tai_lieu", label: "Tài liệu" },
  { value: "video", label: "Video" },
];

const inputCls =
  "w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";

function errorMessage(error: unknown, fallback: string) {
  if (error instanceof Error) return error.message;
  if (error && typeof error === "object" && "message" in error && typeof error.message === "string") {
    return error.message;
  }
  return fallback;
}

const emptyForm = {
  title: "",
  videoUrl: "",
  body: "",
  classIds: [] as number[],
  courseIds: [] as number[],
  subjectCode: "vat-ly",
  contentType: "thong_bao" as PostContentType,
};

export default function PostsAdmin() {
  const toast = useToast();
  const [posts, setPosts] = useState<Post[]>([]);
  const [classes, setClasses] = useState<SchoolClass[]>([]);
  const [courses, setCourses] = useState<CourseOfferingWithSubject[]>([]);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const reload = useCallback(async () => {
    const { data, error } = await getSupabase()
      .from("posts")
      .select(
        "id, created_at, title, body, video_url, published, subject_code, content_type, post_classes(class_id), post_courses(course_id)",
      )
      .order("created_at", { ascending: false });
    if (error) {
      toast("error", errorMessage(error, "Chưa tải được danh sách bài đăng."));
      return;
    }
    setPosts(
      (data ?? []).map((p) => ({
        ...p,
        content_type: (p.content_type as PostContentType) ?? "thong_bao",
        classIds: ((p.post_classes as ClassRef[]) ?? []).map((c) => c.class_id),
        courseIds: ((p.post_courses as CourseRef[]) ?? []).map((c) => c.course_id),
      })) as Post[],
    );
  }, [toast]);

  useEffect(() => {
    const timer = window.setTimeout(() => void reload(), 0);
    fetchClasses().then(setClasses);
    fetchAllCourseOfferings().then(setCourses).catch(() => setCourses([]));
    return () => clearTimeout(timer);
  }, [reload]);

  function startEdit(p: Post) {
    setEditingId(p.id);
    setForm({
      title: p.title,
      videoUrl: p.video_url,
      body: p.body,
      classIds: p.classIds,
      courseIds: p.courseIds,
      subjectCode: p.subject_code,
      contentType: p.content_type,
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function cancelEdit() {
    setEditingId(null);
    setForm(emptyForm);
  }

  async function submitPost(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError("");
    const targets = {
      title: form.title.trim(),
      body: form.body.trim(),
      videoUrl: form.videoUrl.trim(),
      contentType: form.contentType,
      subjectCode: form.subjectCode,
      classIds: form.classIds,
      courseIds: form.courseIds,
    };
    try {
      if (editingId !== null) {
        await updatePostWithTargets(editingId, targets);
        toast("success", "Đã cập nhật bài đăng.");
      } else {
        await createPostWithTargets(targets);
        toast("success", "Đã đăng thông báo/học liệu.");
      }
      cancelEdit();
      await reload();
    } catch (err) {
      setError(errorMessage(err, "Không đăng được bài — vui lòng thử lại."));
    } finally {
      setBusy(false);
    }
  }

  async function togglePublished(p: Post) {
    const { error } = await getSupabase()
      .from("posts")
      .update({ published: !p.published })
      .eq("id", p.id);
    if (error) {
      toast("error", errorMessage(error, "Chưa đổi được trạng thái bài đăng."));
      return;
    }
    await reload();
  }

  async function deletePost(p: Post) {
    if (!confirm(`Xóa bài "${p.title}"?`)) return;
    const { error } = await getSupabase().from("posts").delete().eq("id", p.id);
    if (error) {
      toast("error", errorMessage(error, "Chưa xóa được bài đăng."));
      return;
    }
    if (editingId === p.id) cancelEdit();
    toast("success", "Đã xóa bài đăng.");
    await reload();
  }

  function classNames(ids: number[]) {
    return ids
      .map((id) => classes.find((c) => c.id === id)?.name)
      .filter(Boolean)
      .join(", ");
  }

  function courseNames(ids: number[]) {
    return ids
      .map((id) => courses.find((c) => c.id === id)?.name)
      .filter(Boolean)
      .join(", ");
  }

  return (
    <div className="space-y-8">
      <form
        onSubmit={submitPost}
        className="space-y-4 rounded-2xl border border-white/10 bg-[#0B1020] p-6"
      >
        <div className="flex items-center justify-between">
          <h2 className="font-display text-lg font-semibold text-white">
            {editingId !== null ? "Sửa bài đăng" : "Đăng thông báo hoặc học liệu"}
          </h2>
          {editingId !== null && (
            <button
              type="button"
              onClick={cancelEdit}
              className="text-xs font-medium text-slate-400 hover:text-slate-200"
            >
              Hủy sửa
            </button>
          )}
        </div>
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="block">
            <span className="mb-2 block text-sm font-medium text-slate-300">Môn học</span>
            <select
              value={form.subjectCode}
              onChange={(e) => setForm((f) => ({ ...f, subjectCode: e.target.value }))}
              className={`${inputCls} bg-[#0B1020]`}
            >
              {ACADEMIC_SUBJECTS.map((subject) => (
                <option key={subject.code} value={subject.code}>
                  {subject.icon} {subject.label}
                </option>
              ))}
            </select>
          </label>
          <label className="block">
            <span className="mb-2 block text-sm font-medium text-slate-300">Loại nội dung</span>
            <select
              value={form.contentType}
              onChange={(e) =>
                setForm((f) => ({ ...f, contentType: e.target.value as PostContentType }))
              }
              className={`${inputCls} bg-[#0B1020]`}
            >
              {CONTENT_TYPES.map((t) => (
                <option key={t.value} value={t.value}>
                  {t.label}
                </option>
              ))}
            </select>
          </label>
        </div>
        <input
          required
          value={form.title}
          onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
          placeholder="Tiêu đề bài học"
          className={inputCls}
        />
        <input
          value={form.videoUrl}
          onChange={(e) => setForm((f) => ({ ...f, videoUrl: e.target.value }))}
          placeholder="Link YouTube (không bắt buộc)"
          className={inputCls}
        />
        <textarea
          value={form.body}
          onChange={(e) => setForm((f) => ({ ...f, body: e.target.value }))}
          placeholder="Nội dung / mô tả (không bắt buộc)"
          rows={4}
          className={inputCls}
        />
        <ClassPicker
          selected={form.classIds}
          onChange={(classIds) => setForm((f) => ({ ...f, classIds }))}
        />
        <CoursePicker
          selected={form.courseIds}
          onChange={(courseIds) => setForm((f) => ({ ...f, courseIds }))}
        />
        {error && <p className="text-sm text-red-400">{error}</p>}
        <button
          type="submit"
          disabled={busy}
          className="rounded-full bg-[#2563EB] px-5 py-2.5 text-sm font-semibold text-white hover:bg-primary-dark disabled:opacity-50"
        >
          {busy ? "Đang lưu…" : editingId !== null ? "Lưu thay đổi" : "Đăng bài"}
        </button>
      </form>

      <div className="space-y-3">
        {posts.map((p) => (
          <div
            key={p.id}
            className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-white/10 bg-[#0B1020] px-5 py-4"
          >
            <div className="min-w-0">
              <p className="font-medium text-white">{p.title}</p>
              <p className="text-xs text-slate-500">
                {new Date(p.created_at).toLocaleString("vi-VN")}
                {` · ${academicSubject(p.subject_code).label}`}
                {` · ${CONTENT_TYPES.find((t) => t.value === p.content_type)?.label ?? p.content_type}`}
                {p.video_url && " · có video"}
                {!p.published && " · đang ẩn"}
              </p>
              {(p.classIds.length > 0 || p.courseIds.length > 0) && (
                <p className="mt-1 text-xs text-slate-400">
                  {p.classIds.length > 0 && `Lớp: ${classNames(p.classIds)}`}
                  {p.classIds.length > 0 && p.courseIds.length > 0 && " · "}
                  {p.courseIds.length > 0 && `Khóa: ${courseNames(p.courseIds)}`}
                </p>
              )}
              {p.classIds.length === 0 && p.courseIds.length === 0 && (
                <p className="mt-1 text-xs text-slate-500">Toàn trường</p>
              )}
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => startEdit(p)}
                className="rounded-full border border-white/15 px-3 py-1.5 text-xs font-medium text-slate-300 hover:border-white/30"
              >
                Sửa
              </button>
              <button
                onClick={() => togglePublished(p)}
                className="rounded-full border border-white/15 px-3 py-1.5 text-xs font-medium text-slate-300 hover:border-white/30"
              >
                {p.published ? "Ẩn" : "Hiện"}
              </button>
              <button
                onClick={() => deletePost(p)}
                className="rounded-full border border-red-500/30 px-3 py-1.5 text-xs font-medium text-red-300 hover:border-red-500/60"
              >
                Xóa
              </button>
            </div>
          </div>
        ))}
        {posts.length === 0 && (
          <p className="text-sm text-slate-400">Chưa có bài đăng nào.</p>
        )}
      </div>
    </div>
  );
}
