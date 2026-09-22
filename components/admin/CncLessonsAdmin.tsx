"use client";

import { useCallback, useEffect, useState } from "react";
import LaTexEditor from "@/components/admin/LaTexEditor";
import { CncFilesAdmin } from "@/components/admin/CncMediaPanels";
import { useToast } from "@/components/ui/Toast";
import {
  CNC_PROGRESS,
  CNC_SETUP_CHECKLIST,
} from "@/services/cnc-lms";
import {
  createCncLesson,
  deleteCncLesson,
  fetchCncLessons,
  suggestCncLessonId,
  updateCncLesson,
  type CncLesson,
} from "@/services/cnc-lessons";
import {
  deleteCncLessonFile,
  fetchCncLessonFiles,
  uploadCncLessonFile,
  type CncLessonFile,
  type CncLessonFileKind,
} from "@/services/cnc-lesson-files";

const inputCls =
  "w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";
const chipBtn = "admin-chip";

function linesToList(value: string) {
  return value.split("\n").map((line) => line.trim()).filter(Boolean);
}
function listToLines(value: string[]) {
  return value.join("\n");
}

// ---------- Panel chung: checklist bài vận hành + xem trước điều kiện mở bài ----------
// Đây vẫn là công cụ xem trước cục bộ (không lưu DB) — logic mở/khóa thật nằm trong
// CncCourseWorkspace.tsx và services/cnc-progress.ts, không đổi khi thầy chỉnh ở đây.
function CncRulesPreview() {
  const [checklist, setChecklist] = useState([...CNC_SETUP_CHECKLIST]);
  const [turningQuizScore, setTurningQuizScore] = useState(CNC_PROGRESS.turningQuizScore);
  const [millingQuizScore, setMillingQuizScore] = useState(CNC_PROGRESS.millingQuizScore);
  const [turningOperationPassed, setTurningOperationPassed] = useState(CNC_PROGRESS.turningOperationPassed);
  const [millingOperationPassed, setMillingOperationPassed] = useState(CNC_PROGRESS.millingOperationPassed);
  const operationLessonsUnlocked = turningQuizScore >= 80 && millingQuizScore >= 80;

  const lockPreview = [
    { id: "lesson-4-turn/mill", title: "Bài 4/5 — Vận hành tiện/phay", locked: !operationLessonsUnlocked, reason: "Quiz Bài 2 và Bài 3 cần đạt từ 80%." },
    { id: "lesson-5", title: "Bài 6 — Gia công tiện", locked: !turningOperationPassed, reason: "Cần đạt bài Vận hành và cài đặt máy tiện CNC." },
    { id: "lesson-6", title: "Bài 7 — Gia công phay", locked: !millingOperationPassed, reason: "Cần đạt bài Vận hành và cài đặt máy phay CNC." },
  ];

  return (
    <section className="grid gap-4 lg:grid-cols-3">
      <div className="admin-card">
        <h3 className="admin-h2">Điều kiện mở bài (xem trước)</h3>
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
            <input type="checkbox" checked={turningOperationPassed} onChange={(event) => setTurningOperationPassed(event.target.checked)} />
            Đã đạt vận hành và cài đặt máy tiện
          </label>
          <label className="flex items-center gap-3 rounded-xl bg-white/5 px-3 py-2 text-sm text-slate-300">
            <input type="checkbox" checked={millingOperationPassed} onChange={(event) => setMillingOperationPassed(event.target.checked)} />
            Đã đạt vận hành và cài đặt máy phay
          </label>
        </div>
      </div>

      <div className="admin-card lg:col-span-2">
        <h3 className="admin-h2">Xem trước khóa/mở</h3>
        <div className="mt-4 grid gap-2 sm:grid-cols-2">
          {lockPreview.map((item) => (
            <div key={item.id} className="rounded-xl border border-white/10 bg-white/5 px-4 py-3">
              <div className="flex items-center justify-between gap-3">
                <span className="text-sm font-semibold text-white">{item.title}</span>
                <span className={`rounded-full px-2 py-0.5 text-xs font-bold ${item.locked ? "bg-amber-500/15 text-amber-200" : "bg-emerald-500/15 text-emerald-200"}`}>
                  {item.locked ? "Khóa" : "Mở"}
                </span>
              </div>
              {item.locked && <p className="mt-2 text-xs leading-5 text-slate-400">{item.reason}</p>}
            </div>
          ))}
        </div>
        <label className="mt-4 block text-sm text-slate-300">
          Checklist bài vận hành
          <textarea
            value={listToLines(checklist)}
            onChange={(event) => setChecklist(linesToList(event.target.value))}
            rows={6}
            className="mt-1 w-full rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2 text-white"
          />
        </label>
      </div>
    </section>
  );
}

// ---------- Soạn 1 bài học ----------
function LessonEditor({ lesson, onSaved, onBack }: { lesson: CncLesson; onSaved: () => void; onBack: () => void }) {
  const toast = useToast();
  const [title, setTitle] = useState(lesson.title);
  const [shortTitle, setShortTitle] = useState(lesson.shortTitle);
  const [durationLabel, setDurationLabel] = useState(lesson.duration);
  const [emphasis, setEmphasis] = useState(lesson.emphasis ?? "");
  const [bodyHtml, setBodyHtml] = useState(lesson.bodyHtml);
  const [resources, setResources] = useState(listToLines(lesson.resources));
  const [busy, setBusy] = useState(false);

  const [files, setFiles] = useState<CncLessonFile[]>([]);
  const [filesLoading, setFilesLoading] = useState(true);
  const [uploadingKind, setUploadingKind] = useState<CncLessonFileKind | null>(null);
  const [storageReady, setStorageReady] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setFilesLoading(true);
    fetchCncLessonFiles(lesson.id)
      .then((f) => {
        if (!cancelled) {
          setFiles(f);
          setStorageReady(true);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setFiles([]);
          setStorageReady(false);
        }
      })
      .finally(() => {
        if (!cancelled) setFilesLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [lesson.id]);

  async function handleUpload(kind: CncLessonFileKind, file: File | undefined) {
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
      const uploaded = await uploadCncLessonFile({ lessonId: lesson.id, kind, title: file.name.replace(/\.[^.]+$/, ""), file });
      setFiles((current) => [uploaded, ...current]);
      setStorageReady(true);
      toast("success", kind === "powerpoint" ? "Đã đưa PowerPoint vào nội dung bài học." : "Đã thêm tệp vào mục Tài liệu.");
    } catch (error) {
      setStorageReady(false);
      toast("error", `Không tải được tệp: ${error instanceof Error ? error.message : error}`);
    } finally {
      setUploadingKind(null);
    }
  }

  async function handleDeleteFile(file: CncLessonFile) {
    try {
      await deleteCncLessonFile(file);
      setFiles((current) => current.filter((f) => f.id !== file.id));
      toast("success", "Đã xóa tệp khỏi bài học.");
    } catch (error) {
      toast("error", `Không xóa được tệp: ${error instanceof Error ? error.message : error}`);
    }
  }

  async function save() {
    if (!title.trim() || !shortTitle.trim()) {
      toast("error", "Bài học cần có tiêu đề và tên hiển thị sidebar.");
      return;
    }
    setBusy(true);
    try {
      await updateCncLesson(lesson.id, {
        title: title.trim(),
        shortTitle: shortTitle.trim(),
        duration: durationLabel.trim(),
        emphasis: emphasis.trim() || null,
        bodyHtml,
        resources: linesToList(resources),
      });
      toast("success", "Đã lưu bài học.");
      onSaved();
    } catch (error) {
      toast("error", error instanceof Error ? error.message : String(error));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-center gap-3">
        <button onClick={onBack} className={chipBtn}>
          ← Danh sách bài học
        </button>
        <h3 className="admin-h2">{lesson.title}</h3>
      </div>

      <div className="admin-card space-y-4">
        <div className="grid gap-4 md:grid-cols-2">
          <label className="text-sm text-slate-300">
            Tên hiển thị trong sidebar
            <input value={shortTitle} onChange={(e) => setShortTitle(e.target.value)} className={`${inputCls} mt-1`} />
          </label>
          <label className="text-sm text-slate-300">
            Thời lượng / nhãn
            <input value={durationLabel} onChange={(e) => setDurationLabel(e.target.value)} className={`${inputCls} mt-1`} />
          </label>
        </div>

        <label className="block text-sm text-slate-300">
          Tiêu đề bài học
          <input value={title} onChange={(e) => setTitle(e.target.value)} className={`${inputCls} mt-1`} />
        </label>

        <label className="block text-sm text-slate-300">
          Ghi chú trọng tâm
          <input
            value={emphasis}
            onChange={(e) => setEmphasis(e.target.value)}
            placeholder="Ví dụ: Trọng tâm cài đặt dao, phôi"
            className={`${inputCls} mt-1`}
          />
        </label>

        <label className="block text-sm text-slate-300">
          Nội dung bài học
          <LaTexEditor value={bodyHtml} onChange={setBodyHtml} placeholder="Nội dung (viết LaTeX hoặc HTML)" />
        </label>

        <label className="block text-sm text-slate-300">
          Tài nguyên (mỗi dòng một mục)
          <textarea value={resources} onChange={(e) => setResources(e.target.value)} rows={4} className={`${inputCls} mt-1`} />
        </label>

        <div className="flex gap-2">
          <button onClick={save} disabled={busy} className="admin-btn admin-btn--primary disabled:opacity-50">
            {busy ? "Đang lưu…" : "Lưu bài học"}
          </button>
        </div>
      </div>

      <CncFilesAdmin
        lessonTitle={shortTitle}
        files={files}
        loading={filesLoading}
        uploadingKind={uploadingKind}
        storageReady={storageReady}
        onUpload={handleUpload}
        onDelete={handleDeleteFile}
      />
    </div>
  );
}

// ---------- Danh sách bài học ----------
export default function CncLessonsAdmin() {
  const toast = useToast();
  const [lessons, setLessons] = useState<CncLesson[]>([]);
  const [openLesson, setOpenLesson] = useState<CncLesson | null>(null);
  const [newTitle, setNewTitle] = useState("");

  const reload = useCallback(() => {
    fetchCncLessons().then(setLessons).catch(() => setLessons([]));
  }, []);
  useEffect(reload, [reload]);

  if (openLesson) {
    return (
      <LessonEditor
        lesson={openLesson}
        onBack={() => {
          setOpenLesson(null);
          reload();
        }}
        onSaved={reload}
      />
    );
  }

  async function addLesson(e: React.FormEvent) {
    e.preventDefault();
    if (!newTitle.trim()) return;
    const id = suggestCncLessonId(newTitle, lessons.map((l) => l.id));
    try {
      const created = await createCncLesson({
        id,
        title: newTitle.trim(),
        shortTitle: newTitle.trim(),
        duration: "",
        emphasis: null,
        bodyHtml: "",
        resources: [],
        sortOrder: lessons.length,
      });
      toast("success", "Đã thêm bài học.");
      setNewTitle("");
      reload();
      setOpenLesson(created);
    } catch (error) {
      toast("error", error instanceof Error ? error.message : String(error));
    }
  }

  async function move(idx: number, dir: -1 | 1) {
    const other = idx + dir;
    if (other < 0 || other >= lessons.length) return;
    const a = lessons[idx];
    const b = lessons[other];
    await Promise.all([
      updateCncLesson(a.id, { sortOrder: b.sortOrder }),
      updateCncLesson(b.id, { sortOrder: a.sortOrder }),
    ]);
    reload();
  }

  return (
    <div className="space-y-6">
      <header>
        <p className="admin-lead" style={{ marginTop: 0 }}>
          Soạn nội dung bài học CNC — giống hệt cách đăng bài học Vật lý, không cần sửa code.
        </p>
      </header>

      <CncRulesPreview />

      <form onSubmit={addLesson} className="admin-card flex flex-wrap gap-3">
        <input
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          placeholder="Tên bài học mới, vd Bài 8: Gia công CNC nâng cao"
          className={`${inputCls} min-w-72 flex-1`}
        />
        <button type="submit" className="admin-btn admin-btn--primary">
          + Thêm bài học
        </button>
      </form>

      <div className="space-y-2">
        {lessons.map((l, idx) => (
          <div key={l.id} className="admin-card admin-card--row">
            <button onClick={() => setOpenLesson(l)} className="min-w-0 flex-1 text-left">
              <span className="block truncate font-medium text-white hover:text-primary">{l.title}</span>
              <span className="text-xs text-slate-500">{l.duration}</span>
            </button>
            <span className="flex items-center gap-1">
              <button onClick={() => move(idx, -1)} title="Lên" className={chipBtn}>↑</button>
              <button onClick={() => move(idx, 1)} title="Xuống" className={chipBtn}>↓</button>
              <button onClick={() => setOpenLesson(l)} className="admin-chip">Soạn</button>
              <button
                onClick={async () => {
                  if (!confirm(`Xóa bài "${l.title}"?`)) return;
                  try {
                    await deleteCncLesson(l.id);
                    toast("success", "Đã xóa bài học.");
                    reload();
                  } catch (error) {
                    toast("error", error instanceof Error ? error.message : String(error));
                  }
                }}
                className="admin-chip admin-chip--danger"
              >
                Xóa
              </button>
            </span>
          </div>
        ))}
        {lessons.length === 0 && <p className="text-sm text-slate-400">Chưa có bài học nào — thêm bài đầu tiên ở trên.</p>}
      </div>
    </div>
  );
}
