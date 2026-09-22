"use client";

import {
  type CncLessonFile,
  type CncLessonFileKind,
  formatFileSize,
} from "@/services/cnc-lesson-files";
import { getYouTubeThumbnailUrl, getYouTubeVideoId, type CncLessonVideo } from "@/services/cnc-lesson-videos";

export function CncVideosAdmin({
  lessonTitle,
  videos,
  loading,
  ready,
  adding,
  title,
  url,
  onTitleChange,
  onUrlChange,
  onAdd,
  onDelete,
}: {
  lessonTitle: string;
  videos: CncLessonVideo[];
  loading: boolean;
  ready: boolean;
  adding: boolean;
  title: string;
  url: string;
  onTitleChange: (value: string) => void;
  onUrlChange: (value: string) => void;
  onAdd: () => void;
  onDelete: (video: CncLessonVideo) => void;
}) {
  const previewId = getYouTubeVideoId(url);

  return (
    <section className="rounded-2xl border border-red-500/25 bg-red-500/5 p-5">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-xs font-bold tracking-wide text-red-300 uppercase">
            Video bài giảng
          </p>
          <h3 className="mt-1 admin-h2">
            YouTube · {lessonTitle}
          </h3>
          <p className="mt-1 text-xs leading-5 text-slate-400">
            Có thể thêm nhiều video. Mỗi video sẽ xuất hiện trong mục Video bài giảng của bài đang chọn.
          </p>
        </div>
        <span className="admin-badge admin-badge--danger w-fit">
          {videos.length} video
        </span>
      </div>

      {!ready && !loading && (
        <div className="mt-4 rounded-xl border border-amber-500/30 bg-amber-500/10 px-4 py-3 text-xs leading-5 text-amber-200">
          Bảng video CNC chưa sẵn sàng. Hãy chạy lại migration
          <strong> supabase-migration-cnc-files.sql</strong> trong Supabase.
        </div>
      )}

      <div className="mt-5 grid gap-4 lg:grid-cols-[1fr_220px]">
        <div className="space-y-3">
          <label className="block text-sm text-slate-300">
            Tên video
            <input
              value={title}
              onChange={(event) => onTitleChange(event.target.value)}
              placeholder="Ví dụ: Cấu tạo máy tiện CNC"
              className="mt-1 w-full rounded-xl border border-white/10 bg-[#080D1A] px-3 py-2 text-white placeholder:text-slate-500"
            />
          </label>
          <label className="block text-sm text-slate-300">
            Liên kết YouTube
            <input
              value={url}
              onChange={(event) => onUrlChange(event.target.value)}
              placeholder="https://www.youtube.com/watch?v=..."
              className="mt-1 w-full rounded-xl border border-white/10 bg-[#080D1A] px-3 py-2 text-white placeholder:text-slate-500"
            />
          </label>
          <button
            type="button"
            disabled={adding || !title.trim() || !previewId}
            onClick={onAdd}
            className="admin-btn admin-btn--danger"
          >
            {adding ? "Đang thêm video…" : "+ Thêm video vào bài học"}
          </button>
        </div>

        <div className="overflow-hidden rounded-xl border border-white/10 bg-[#080D1A]">
          {previewId ? (
            <img
              src={getYouTubeThumbnailUrl(previewId)}
              alt="Xem trước video YouTube"
              className="aspect-video h-full w-full object-cover"
            />
          ) : (
            <div className="flex aspect-video items-center justify-center px-5 text-center text-xs text-slate-500">
              Dán liên kết YouTube để xem trước ảnh video.
            </div>
          )}
        </div>
      </div>

      <div className="mt-5 grid gap-3 md:grid-cols-2">
        {loading ? (
          <p className="text-xs text-slate-400">Đang tải danh sách video…</p>
        ) : videos.length === 0 ? (
          <p className="admin-empty md:col-span-2">
            Bài học này chưa có video YouTube.
          </p>
        ) : videos.map((video, index) => (
          <div key={video.id} className="flex gap-3 rounded-xl border border-white/10 bg-[#080D1A] p-3">
            <img
              src={getYouTubeThumbnailUrl(video.youtube_id)}
              alt=""
              className="h-16 w-28 rounded-lg object-cover"
            />
            <div className="min-w-0 flex-1">
              <span className="text-[10px] font-bold text-red-300">VIDEO {index + 1}</span>
              <a href={video.youtube_url} target="_blank" rel="noreferrer" className="mt-0.5 block truncate text-sm font-semibold text-white hover:text-red-300">
                {video.title}
              </a>
              <button type="button" onClick={() => onDelete(video)} className="mt-2 text-[10px] font-bold text-red-300 hover:text-red-200">
                Xóa video
              </button>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export function CncFilesAdmin({
  lessonTitle,
  files,
  loading,
  uploadingKind,
  storageReady,
  onUpload,
  onDelete,
}: {
  lessonTitle: string;
  files: CncLessonFile[];
  loading: boolean;
  uploadingKind: CncLessonFileKind | null;
  storageReady: boolean;
  onUpload: (kind: CncLessonFileKind, file: File | undefined) => void;
  onDelete: (file: CncLessonFile) => void;
}) {
  const powerPoints = files.filter((file) => file.kind === "powerpoint");
  const materials = files.filter((file) => file.kind === "material");

  return (
    <section className="rounded-2xl border border-primary/30 bg-primary/10 p-5">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-xs font-bold tracking-wide text-[#93C5FD] uppercase">
            Tệp của bài học
          </p>
          <h3 className="mt-1 admin-h2">
            {lessonTitle}
          </h3>
          <p className="mt-1 text-xs leading-5 text-slate-400">
            PowerPoint xuất hiện ở Nội dung bài học; các tệp khác xuất hiện trong mục Tài liệu.
          </p>
        </div>
        <span className="admin-badge w-fit">
          Tối đa 50 MB/tệp
        </span>
      </div>

      {!storageReady && !loading && (
        <div className="mt-4 rounded-xl border border-amber-500/30 bg-amber-500/10 px-4 py-3 text-xs leading-5 text-amber-200">
          Kho tệp CNC chưa sẵn sàng. Hãy chạy migration
          <strong> supabase-migration-cnc-files.sql</strong> trong Supabase trước khi tải tệp.
        </div>
      )}

      <div className="mt-5 grid gap-4 md:grid-cols-2">
        <FileUploadPanel
          icon="PPT"
          title="PowerPoint bài giảng"
          description="Chấp nhận .ppt và .pptx"
          accept=".ppt,.pptx,application/vnd.ms-powerpoint,application/vnd.openxmlformats-officedocument.presentationml.presentation"
          busy={uploadingKind === "powerpoint"}
          files={powerPoints}
          onFile={(file) => onUpload("powerpoint", file)}
          onDelete={onDelete}
        />
        <FileUploadPanel
          icon="FILE"
          title="Tài liệu bài học"
          description="PDF, Word, Excel, ZIP, NC và tệp văn bản"
          accept=".pdf,.doc,.docx,.xls,.xlsx,.zip,.rar,.nc,.txt"
          busy={uploadingKind === "material"}
          files={materials}
          onFile={(file) => onUpload("material", file)}
          onDelete={onDelete}
        />
      </div>
    </section>
  );
}

function FileUploadPanel({
  icon,
  title,
  description,
  accept,
  busy,
  files,
  onFile,
  onDelete,
}: {
  icon: string;
  title: string;
  description: string;
  accept: string;
  busy: boolean;
  files: CncLessonFile[];
  onFile: (file: File | undefined) => void;
  onDelete: (file: CncLessonFile) => void;
}) {
  return (
    <div className="admin-card">
      <div className="flex items-center gap-3">
        <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-[#2563EB]/15 text-xs font-black text-[#93C5FD]">
          {icon}
        </span>
        <div>
          <h4 className="text-sm font-bold text-white">{title}</h4>
          <p className="mt-0.5 text-xs text-slate-500">{description}</p>
        </div>
      </div>

      <label className={`mt-4 flex cursor-pointer items-center justify-center rounded-xl border border-dashed border-white/20 bg-white/5 px-4 py-4 text-center text-xs font-semibold text-slate-300 hover:border-primary/60 hover:bg-primary/10 ${busy ? "pointer-events-none opacity-60" : ""}`}>
        {busy ? "Đang tải tệp lên…" : "+ Chọn tệp để tải lên"}
        <input
          type="file"
          accept={accept}
          disabled={busy}
          onChange={(event) => {
            onFile(event.target.files?.[0]);
            event.currentTarget.value = "";
          }}
          className="sr-only"
        />
      </label>

      <div className="mt-4 space-y-2">
        {files.length === 0 ? (
          <p className="rounded-lg bg-white/5 px-3 py-3 text-center text-xs text-slate-500">
            Chưa có tệp nào.
          </p>
        ) : (
          files.map((file) => (
            <div key={file.id} className="flex items-center gap-3 rounded-lg border border-white/10 bg-white/5 px-3 py-2">
              <div className="min-w-0 flex-1">
                <a
                  href={file.file_url}
                  target="_blank"
                  rel="noreferrer"
                  className="block truncate text-xs font-semibold text-white hover:text-[#60A5FA]"
                >
                  {file.title}
                </a>
                <p className="mt-0.5 truncate text-[10px] text-slate-500">
                  {file.file_name} · {formatFileSize(file.size_bytes)}
                </p>
              </div>
              <button
                type="button"
                onClick={() => onDelete(file)}
                className="rounded-lg px-2 py-1 text-[10px] font-bold text-red-300 hover:bg-red-500/10"
              >
                Xóa
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
