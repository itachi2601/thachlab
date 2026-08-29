"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { ArrowLeft, ArrowRight, BookOpen, Download, ExternalLink, FileQuestion, FileText, Settings2, Video } from "lucide-react";
import {
  CNC_COURSE_ITEMS,
  CNC_PROGRESS,
  CNC_SETUP_CHECKLIST,
  type CncCourseItem,
} from "@/services/cnc-lms";
import {
  fetchCncExamBankMeta,
  fetchCncExamRow,
  type CncExamBankMeta,
} from "@/services/cnc-exam-bank";
import type { Exam } from "@/features/exams/types";
import ImportExam from "@/components/admin/ImportExam";
import ExamEditor from "@/components/admin/ExamEditor";
import { useToast } from "@/components/ui/Toast";
import {
  deleteCncLessonFile,
  fetchCncLessonFiles,
  formatFileSize,
  uploadCncLessonFile,
  type CncLessonFile,
  type CncLessonFileKind,
} from "@/services/cnc-lesson-files";
import {
  createCncLessonVideo,
  deleteCncLessonVideo,
  fetchCncLessonVideos,
  getYouTubeThumbnailUrl,
  getYouTubeVideoId,
  type CncLessonVideo,
} from "@/services/cnc-lesson-videos";
type EditableCncItem = {
  id: string;
  title: string;
  shortTitle: string;
  duration: string;
  emphasis?: string;
  topics: string[];
  resources: string[];
  activities: string[];
  flipped?: boolean;
  assignment?: {
    title: string;
    requirement: string;
    accept: string;
  };
};

function normalizeItem(item: CncCourseItem): EditableCncItem {
  return {
    id: item.id,
    title: item.title,
    shortTitle: item.shortTitle,
    duration: item.duration,
    emphasis: "emphasis" in item ? item.emphasis : "",
    topics: "topics" in item ? [...(item.topics ?? [])] : [],
    resources: "resources" in item ? [...(item.resources ?? [])] : [],
    activities: [...item.activities],
    flipped: "flipped" in item ? item.flipped : false,
    assignment:
      "assignment" in item && item.assignment
        ? { ...item.assignment }
        : undefined,
  };
}

function linesToList(value: string) {
  return value
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
}

function listToLines(value: string[]) {
  return value.join("\n");
}

export default function CncLmsAdmin({ initialLessonId }: { initialLessonId?: string }) {
  const toast = useToast();
  const [items, setItems] = useState<EditableCncItem[]>(
    CNC_COURSE_ITEMS.map(normalizeItem),
  );
  const activeId = items.some((item) => item.id === initialLessonId)
    ? initialLessonId!
    : items[0]?.id ?? "intro";
  const [checklist, setChecklist] = useState([...CNC_SETUP_CHECKLIST]);
  const [bankMeta, setBankMeta] = useState<CncExamBankMeta[]>([]);
  const [importBank, setImportBank] = useState<{ key: string; label: string } | null>(null);
  const [editingBank, setEditingBank] = useState<{ key: string; label: string } | null>(null);
  const [editingExam, setEditingExam] = useState<Exam | null>(null);
  const loadBankMeta = () => void fetchCncExamBankMeta().then(setBankMeta).catch(() => undefined);
  useEffect(() => { loadBankMeta(); }, []);
  async function openBankEditor(bank: { key: string; label: string }) {
    const row = await fetchCncExamRow(bank.key).catch(() => null);
    setEditingBank(bank);
    setEditingExam(row);
  }
  const [turningQuizScore, setTurningQuizScore] = useState(
    CNC_PROGRESS.turningQuizScore,
  );
  const [millingQuizScore, setMillingQuizScore] = useState(
    CNC_PROGRESS.millingQuizScore,
  );
  const [turningOperationPassed, setTurningOperationPassed] = useState(
    CNC_PROGRESS.turningOperationPassed,
  );
  const [millingOperationPassed, setMillingOperationPassed] = useState(
    CNC_PROGRESS.millingOperationPassed,
  );
  const [lessonFiles, setLessonFiles] = useState<CncLessonFile[]>([]);
  const [filesLoading, setFilesLoading] = useState(true);
  const [uploadingKind, setUploadingKind] = useState<CncLessonFileKind | null>(null);
  const [fileStorageReady, setFileStorageReady] = useState(true);
  const [lessonVideos, setLessonVideos] = useState<CncLessonVideo[]>([]);
  const [videosLoading, setVideosLoading] = useState(true);
  const [videosReady, setVideosReady] = useState(true);
  const [addingVideo, setAddingVideo] = useState(false);
  const [videoTitle, setVideoTitle] = useState("");
  const [videoUrl, setVideoUrl] = useState("");

  const activeItem = items.find((item) => item.id === activeId) ?? items[0];
  const activeIndex = items.findIndex((item) => item.id === activeId);
  const previousItem = activeIndex > 0 ? items[activeIndex - 1] : null;
  const nextItem = activeIndex >= 0 && activeIndex < items.length - 1 ? items[activeIndex + 1] : null;
  const operationLessonsUnlocked = turningQuizScore >= 80 && millingQuizScore >= 80;

  const lockPreview = useMemo(
    () =>
      items.map((item) => {
        if (item.id === "lesson-4-turn" || item.id === "lesson-4-mill") {
          return {
            id: item.id,
            title: item.shortTitle,
            locked: !operationLessonsUnlocked,
            reason: "Quiz Bài 2 và Bài 3 cần đạt từ 80%.",
          };
        }
        if (item.id === "lesson-5") {
          return {
            id: item.id,
            title: item.shortTitle,
            locked: !turningOperationPassed,
            reason: "Cần đạt bài Vận hành và cài đặt máy tiện CNC.",
          };
        }
        if (item.id === "lesson-6") {
          return {
            id: item.id,
            title: item.shortTitle,
            locked: !millingOperationPassed,
            reason: "Cần đạt bài Vận hành và cài đặt máy phay CNC.",
          };
        }
        return { id: item.id, title: item.shortTitle, locked: false, reason: "" };
      }),
    [items, operationLessonsUnlocked, turningOperationPassed, millingOperationPassed],
  );

  useEffect(() => {
    let cancelled = false;
    setFilesLoading(true);
    fetchCncLessonFiles(activeId)
      .then((files) => {
        if (!cancelled) {
          setLessonFiles(files);
          setFileStorageReady(true);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setLessonFiles([]);
          setFileStorageReady(false);
        }
      })
      .finally(() => {
        if (!cancelled) setFilesLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [activeId]);

  useEffect(() => {
    let cancelled = false;
    setVideosLoading(true);
    setVideoTitle("");
    setVideoUrl("");
    fetchCncLessonVideos(activeId)
      .then((videos) => {
        if (!cancelled) {
          setLessonVideos(videos);
          setVideosReady(true);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setLessonVideos([]);
          setVideosReady(false);
        }
      })
      .finally(() => {
        if (!cancelled) setVideosLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [activeId]);

  async function handleLessonFile(
    kind: CncLessonFileKind,
    file: File | undefined,
  ) {
    if (!file) return;
    const isPowerPoint = /\.(ppt|pptx)$/i.test(file.name);
    if (kind === "powerpoint" && !isPowerPoint) {
      toast("error", "Bài giảng phải là tệp .ppt hoặc .pptx");
      return;
    }
    if (file.size > 50 * 1024 * 1024) {
      toast("error", "Tệp vượt quá giới hạn 50 MB");
      return;
    }
    setUploadingKind(kind);
    try {
      const uploaded = await uploadCncLessonFile({
        lessonId: activeItem.id,
        kind,
        title: file.name.replace(/\.[^.]+$/, ""),
        file,
      });
      setLessonFiles((current) => [uploaded, ...current]);
      setFileStorageReady(true);
      toast(
        "success",
        kind === "powerpoint"
          ? "Đã đưa PowerPoint vào nội dung bài học."
          : "Đã thêm tệp vào mục Tài liệu.",
      );
    } catch (error) {
      setFileStorageReady(false);
      toast("error", `Không tải được tệp: ${error instanceof Error ? error.message : error}`);
    } finally {
      setUploadingKind(null);
    }
  }

  async function handleDeleteLessonFile(file: CncLessonFile) {
    try {
      await deleteCncLessonFile(file);
      setLessonFiles((current) => current.filter((item) => item.id !== file.id));
      toast("success", "Đã xóa tệp khỏi bài học.");
    } catch (error) {
      toast("error", `Không xóa được tệp: ${error instanceof Error ? error.message : error}`);
    }
  }

  async function handleAddVideo() {
    if (!videoTitle.trim()) {
      toast("error", "Hãy nhập tên video");
      return;
    }
    if (!getYouTubeVideoId(videoUrl)) {
      toast("error", "Liên kết YouTube không hợp lệ");
      return;
    }

    setAddingVideo(true);
    try {
      const video = await createCncLessonVideo({
        lessonId: activeItem.id,
        title: videoTitle,
        youtubeUrl: videoUrl,
        sortOrder: lessonVideos.length,
      });
      setLessonVideos((current) => [...current, video]);
      setVideoTitle("");
      setVideoUrl("");
      setVideosReady(true);
      toast("success", "Đã thêm video vào bài học.");
    } catch (error) {
      setVideosReady(false);
      toast("error", `Không thêm được video: ${error instanceof Error ? error.message : error}`);
    } finally {
      setAddingVideo(false);
    }
  }

  async function handleDeleteVideo(video: CncLessonVideo) {
    try {
      await deleteCncLessonVideo(video.id);
      setLessonVideos((current) => current.filter((item) => item.id !== video.id));
      toast("success", "Đã xóa video khỏi bài học.");
    } catch (error) {
      toast("error", `Không xóa được video: ${error instanceof Error ? error.message : error}`);
    }
  }

  function updateActive(patch: Partial<EditableCncItem>) {
    setItems((current) =>
      current.map((item) =>
        item.id === activeItem.id ? { ...item, ...patch } : item,
      ),
    );
  }

  function updateAssignment(patch: Partial<NonNullable<EditableCncItem["assignment"]>>) {
    updateActive({
      assignment: {
        title: activeItem.assignment?.title ?? "",
        requirement: activeItem.assignment?.requirement ?? "",
        accept: activeItem.assignment?.accept ?? "",
        ...patch,
      },
    });
  }

  function exportConfig() {
    const payload = {
      progressRules: {
        operationLessons: "Mở khi Quiz Bài 2 và Bài 3 đều >= 80%",
        turningProduction: "Mở khi đạt bài Vận hành và cài đặt máy tiện CNC",
        millingProduction: "Mở khi đạt bài Vận hành và cài đặt máy phay CNC",
      },
      previewProgress: {
        turningQuizScore,
        millingQuizScore,
        turningOperationPassed,
        millingOperationPassed,
      },
      setupChecklist: checklist,
      courseItems: items,
    };
    const blob = new Blob([JSON.stringify(payload, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "cnc-lms-config.json";
    link.click();
    URL.revokeObjectURL(url);
  }

  if (importBank) {
    return <ImportExam cncBank={importBank} onDone={() => { setImportBank(null); loadBankMeta(); }} />;
  }
  if (editingBank) {
    return <ExamEditor exam={editingExam} cncBank={editingBank} onDone={() => { setEditingBank(null); setEditingExam(null); loadBankMeta(); }} />;
  }

  if (!activeItem) {
    return <p className="text-sm text-slate-400">Chưa có nội dung LMS CNC.</p>;
  }

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-3xl border border-blue-400/20 bg-[radial-gradient(circle_at_90%_0%,rgba(37,99,235,.2),transparent_38%),#0B1020] p-6">
        <div className="mb-5 flex flex-wrap items-center justify-between gap-3 border-b border-white/10 pb-4">
          <Link href="/quan-tri/lms-cnc" className="inline-flex items-center gap-2 text-sm font-bold text-blue-300 hover:text-blue-200"><ArrowLeft size={17}/> Danh sách bài học</Link>
          <Link href={activeItem.id === "intro" ? "/lop-hoc/cnc" : `/lop-hoc/cnc/${activeItem.id}`} target="_blank" className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs font-bold text-slate-200 hover:bg-white/10">Xem trang học <ExternalLink size={14}/></Link>
        </div>
        <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <span className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-blue-300"><Settings2 size={14}/> {activeItem.id === "intro" ? "Giới thiệu học phần" : `Bài ${activeIndex}`}</span>
            <h1 className="mt-2 max-w-3xl font-display text-2xl font-bold text-white sm:text-3xl">{activeItem.title}</h1>
            <p className="mt-2 text-sm text-slate-400">{activeItem.duration} · Trang soạn riêng của bài học</p>
          </div>
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              onClick={() => toast("success", "Đã lưu bản nháp LMS CNC trên giao diện.")}
              className="rounded-full bg-[#2563EB] px-5 py-2 text-sm font-semibold text-white hover:bg-primary-dark"
            >
              Lưu thay đổi
            </button>
            <button
              type="button"
              onClick={exportConfig}
              className="rounded-full border border-white/15 px-5 py-2 text-sm font-semibold text-slate-200 hover:border-white/30"
            >
              <Download size={14}/> Xuất JSON
            </button>
          </div>
        </div>
        <div className="mt-6 grid grid-cols-2 gap-2 border-t border-white/10 pt-4 sm:grid-cols-4">
          <Anchor href="#thong-tin" icon={<BookOpen size={15}/>} label="Thông tin"/>
          <Anchor href="#hoc-lieu" icon={<FileText size={15}/>} label="Học liệu"/>
          <Anchor href="#video" icon={<Video size={15}/>} label="Video"/>
          <Anchor href="#cau-hoi" icon={<FileQuestion size={15}/>} label="Câu hỏi"/>
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-3">
        <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
          <h3 className="font-display font-semibold text-white">Rule khóa</h3>
          <div className="mt-4 grid gap-3">
            <label className="text-sm text-slate-300">
              Điểm Quiz Bài 2
              <input
                type="number"
                min={0}
                max={100}
                value={turningQuizScore}
                onChange={(event) => setTurningQuizScore(Number(event.target.value))}
                className="mt-1 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-white"
              />
            </label>
            <label className="text-sm text-slate-300">
              Điểm Quiz Bài 3
              <input
                type="number"
                min={0}
                max={100}
                value={millingQuizScore}
                onChange={(event) => setMillingQuizScore(Number(event.target.value))}
                className="mt-1 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-white"
              />
            </label>
            <label className="flex items-center gap-3 rounded-xl bg-white/5 px-3 py-2 text-sm text-slate-300">
              <input
                type="checkbox"
                checked={turningOperationPassed}
                onChange={(event) =>
                  setTurningOperationPassed(event.target.checked)
                }
              />
              Đã đạt vận hành và cài đặt máy tiện
            </label>
            <label className="flex items-center gap-3 rounded-xl bg-white/5 px-3 py-2 text-sm text-slate-300">
              <input
                type="checkbox"
                checked={millingOperationPassed}
                onChange={(event) =>
                  setMillingOperationPassed(event.target.checked)
                }
              />
              Đã đạt vận hành và cài đặt máy phay
            </label>
          </div>
        </div>

        <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-5 lg:col-span-2">
          <h3 className="font-display font-semibold text-white">Xem trước khóa/mở</h3>
          <div className="mt-4 grid gap-2 sm:grid-cols-2">
            {lockPreview.map((item) => (
              <div
                key={item.id}
                className="rounded-xl border border-white/10 bg-white/5 px-4 py-3"
              >
                <div className="flex items-center justify-between gap-3">
                  <span className="text-sm font-semibold text-white">{item.title}</span>
                  <span
                    className={`rounded-full px-2 py-0.5 text-xs font-bold ${
                      item.locked
                        ? "bg-amber-500/15 text-amber-200"
                        : "bg-emerald-500/15 text-emerald-200"
                    }`}
                  >
                    {item.locked ? "Khóa" : "Mở"}
                  </span>
                </div>
                {item.locked && (
                  <p className="mt-2 text-xs leading-5 text-slate-400">{item.reason}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="thong-tin" className="scroll-mt-28">
        <div className="space-y-5 rounded-3xl border border-white/10 bg-[#0B1020] p-5 sm:p-6">
          <div className="border-b border-white/10 pb-4"><p className="text-xs font-bold uppercase tracking-wider text-blue-300">Nội dung bài học</p><h2 className="mt-1 font-display text-xl font-semibold text-white">Thông tin và tài nguyên</h2><p className="mt-1 text-xs text-slate-500">Các thay đổi tại đây chỉ áp dụng cho {activeItem.shortTitle}.</p></div>
          <div id="hoc-lieu" className="scroll-mt-28">
          <CncFilesAdmin
            lessonTitle={activeItem.shortTitle}
            files={lessonFiles}
            loading={filesLoading}
            uploadingKind={uploadingKind}
            storageReady={fileStorageReady}
            onUpload={handleLessonFile}
            onDelete={handleDeleteLessonFile}
          />
          </div>

          <div id="video" className="scroll-mt-28">
          <CncVideosAdmin
            lessonTitle={activeItem.shortTitle}
            videos={lessonVideos}
            loading={videosLoading}
            ready={videosReady}
            adding={addingVideo}
            title={videoTitle}
            url={videoUrl}
            onTitleChange={setVideoTitle}
            onUrlChange={setVideoUrl}
            onAdd={handleAddVideo}
            onDelete={handleDeleteVideo}
          />
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <label className="text-sm text-slate-300">
              Tên hiển thị trong sidebar
              <input
                value={activeItem.shortTitle}
                onChange={(event) => updateActive({ shortTitle: event.target.value })}
                className="mt-1 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-white"
              />
            </label>
            <label className="text-sm text-slate-300">
              Thời lượng / nhãn
              <input
                value={activeItem.duration}
                onChange={(event) => updateActive({ duration: event.target.value })}
                className="mt-1 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-white"
              />
            </label>
          </div>

          <label className="block text-sm text-slate-300">
            Tiêu đề bài học
            <input
              value={activeItem.title}
              onChange={(event) => updateActive({ title: event.target.value })}
              className="mt-1 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-white"
            />
          </label>

          <label className="block text-sm text-slate-300">
            Ghi chú trọng tâm
            <input
              value={activeItem.emphasis ?? ""}
              onChange={(event) => updateActive({ emphasis: event.target.value })}
              placeholder="Ví dụ: Trọng tâm cài đặt dao, phôi"
              className="mt-1 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-white placeholder:text-slate-500"
            />
          </label>

          <div className="grid gap-4 lg:grid-cols-3">
            <label className="block text-sm text-slate-300">
              Đề mục
              <textarea
                value={listToLines(activeItem.topics)}
                onChange={(event) =>
                  updateActive({ topics: linesToList(event.target.value) })
                }
                rows={9}
                className="mt-1 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-white"
              />
            </label>
            <label className="block text-sm text-slate-300">
              Tài nguyên
              <textarea
                value={listToLines(activeItem.resources)}
                onChange={(event) =>
                  updateActive({ resources: linesToList(event.target.value) })
                }
                rows={9}
                className="mt-1 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-white"
              />
            </label>
            <label className="block text-sm text-slate-300">
              Hoạt động
              <textarea
                value={listToLines(activeItem.activities)}
                onChange={(event) =>
                  updateActive({ activities: linesToList(event.target.value) })
                }
                rows={9}
                className="mt-1 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-white"
              />
            </label>
          </div>

          <div className="grid gap-4 lg:grid-cols-2">
            <div className="rounded-xl border border-white/10 bg-white/5 p-4">
              <label className="flex items-center gap-3 text-sm text-slate-300">
                <input
                  type="checkbox"
                  checked={Boolean(activeItem.flipped)}
                  onChange={(event) => updateActive({ flipped: event.target.checked })}
                />
                Có khu lớp học đảo ngược
              </label>
              <label className="mt-4 block text-sm text-slate-300">
                Checklist bài vận hành
                <textarea
                  value={listToLines(checklist)}
                  onChange={(event) => setChecklist(linesToList(event.target.value))}
                  rows={8}
                  className="mt-1 w-full rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2 text-white"
                />
              </label>
            </div>

            <div className="rounded-xl border border-white/10 bg-white/5 p-4">
              <label className="flex items-center gap-3 text-sm text-slate-300">
                <input
                  type="checkbox"
                  checked={Boolean(activeItem.assignment)}
                  onChange={(event) =>
                    updateActive({
                      assignment: event.target.checked
                        ? {
                            title: "Nộp bài",
                            requirement: "Mô tả yêu cầu nộp bài.",
                            accept: ".NC",
                          }
                        : undefined,
                    })
                  }
                />
                Có khu vực nộp bài
              </label>
              {activeItem.assignment && (
                <div className="mt-4 space-y-3">
                  <input
                    value={activeItem.assignment.title}
                    onChange={(event) => updateAssignment({ title: event.target.value })}
                    placeholder="Tên bài nộp"
                    className="w-full rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2 text-white placeholder:text-slate-500"
                  />
                  <textarea
                    value={activeItem.assignment.requirement}
                    onChange={(event) =>
                      updateAssignment({ requirement: event.target.value })
                    }
                    placeholder="Yêu cầu nộp bài"
                    rows={4}
                    className="w-full rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2 text-white placeholder:text-slate-500"
                  />
                  <input
                    value={activeItem.assignment.accept}
                    onChange={(event) => updateAssignment({ accept: event.target.value })}
                    placeholder=".NC, ảnh mô phỏng 3D"
                    className="w-full rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2 text-white placeholder:text-slate-500"
                  />
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        <div id="cau-hoi" className="scroll-mt-28" />
        <h3 className="font-display text-lg font-semibold text-white">
          Ngân hàng câu hỏi CNC
        </h3>
        <p className="mt-2 text-sm leading-6 text-slate-400">
          Câu hỏi trắc nghiệm của từng bài — bấm &quot;Cập nhật qua LaTeX&quot; để dán file
          LaTeX thay cả ngân hàng (xem hướng dẫn định dạng ngay trong đó), hoặc bấm &quot;Xem/sửa&quot;
          để sửa nhanh từng câu.
        </p>
        <div className="mt-4 space-y-2">
          {bankMeta.map((bank) => (
            <div key={bank.key} className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-white/10 bg-white/5 p-3">
              <div>
                <strong className="text-sm text-white">{bank.label}</strong>
                <p className="mt-0.5 text-xs text-slate-500">{bank.questionCount} câu{!bank.examId && " · chưa có dữ liệu"}</p>
              </div>
              <div className="flex shrink-0 gap-2">
                <button
                  type="button"
                  onClick={() => setImportBank({ key: bank.key, label: bank.label })}
                  className="rounded-lg border border-orange-400/30 bg-orange-500/10 px-3 py-1.5 text-xs font-bold text-orange-200 hover:bg-orange-500/20"
                >
                  Cập nhật qua LaTeX
                </button>
                <button
                  type="button"
                  onClick={() => void openBankEditor({ key: bank.key, label: bank.label })}
                  className="rounded-lg border border-blue-400/25 bg-blue-500/10 px-3 py-1.5 text-xs font-bold text-blue-200 hover:bg-blue-500/20"
                >
                  {bank.examId ? "Nhập / sửa câu hỏi" : "+ Tạo câu hỏi"}
                </button>
              </div>
            </div>
          ))}
          {!bankMeta.length && (
            <p className="text-sm text-slate-500">Đang tải danh sách ngân hàng câu hỏi…</p>
          )}
        </div>
      </section>

      <nav className="grid gap-3 sm:grid-cols-2" aria-label="Chuyển bài học quản trị">
        {previousItem ? <Link href={`/quan-tri/lms-cnc/${previousItem.id}`} className="group rounded-2xl border border-white/10 bg-[#0B1020] p-4 hover:border-blue-400/40"><span className="inline-flex items-center gap-2 text-xs font-bold text-slate-500"><ArrowLeft size={15}/> Bài trước</span><strong className="mt-2 block text-sm text-white group-hover:text-blue-200">{previousItem.shortTitle}</strong></Link> : <span/>}
        {nextItem && <Link href={`/quan-tri/lms-cnc/${nextItem.id}`} className="group rounded-2xl border border-white/10 bg-[#0B1020] p-4 text-right hover:border-blue-400/40"><span className="inline-flex items-center gap-2 text-xs font-bold text-slate-500">Bài tiếp theo <ArrowRight size={15}/></span><strong className="mt-2 block text-sm text-white group-hover:text-blue-200">{nextItem.shortTitle}</strong></Link>}
      </nav>
    </div>
  );
}

function Anchor({href,icon,label}:{href:string;icon:React.ReactNode;label:string}){return <a href={href} className="inline-flex items-center justify-center gap-2 rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-xs font-bold text-slate-300 hover:border-blue-400/30 hover:text-blue-200">{icon}{label}</a>}

function CncVideosAdmin({
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
          <h3 className="mt-1 font-display text-lg font-bold text-white">
            YouTube · {lessonTitle}
          </h3>
          <p className="mt-1 text-xs leading-5 text-slate-400">
            Có thể thêm nhiều video. Mỗi video sẽ xuất hiện trong mục Video bài giảng của bài đang chọn.
          </p>
        </div>
        <span className="w-fit rounded-full bg-red-500/10 px-3 py-1 text-xs font-semibold text-red-200">
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
            className="rounded-xl bg-red-600 px-4 py-2 text-sm font-bold text-white hover:bg-red-500 disabled:cursor-not-allowed disabled:opacity-50"
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
          <p className="rounded-xl border border-dashed border-white/10 px-4 py-5 text-center text-xs text-slate-500 md:col-span-2">
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

function CncFilesAdmin({
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
          <h3 className="mt-1 font-display text-lg font-bold text-white">
            {lessonTitle}
          </h3>
          <p className="mt-1 text-xs leading-5 text-slate-400">
            PowerPoint xuất hiện ở Nội dung bài học; các tệp khác xuất hiện trong mục Tài liệu.
          </p>
        </div>
        <span className="w-fit rounded-full bg-white/5 px-3 py-1 text-xs font-semibold text-slate-300">
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
    <div className="rounded-xl border border-white/10 bg-[#080D1A] p-4">
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
