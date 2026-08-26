"use client";

import { useCallback, useEffect, useState } from "react";
import LaTexEditor from "@/components/admin/LaTexEditor";
import { useToast } from "@/components/ui/Toast";
import type { SchoolClass } from "@/features/exams/types";
import {
  SECTION_META,
  SECTION_ORDER,
  type Chapter,
  type Lesson,
  type LessonItem,
  type LessonItemKind,
} from "@/features/lessons/types";
import {
  displayClassesByGrade,
  expandClassIdsByGrade,
  fetchClasses,
  setItemClasses,
} from "@/services/classes";
import { fetchChapters, fetchLessonItems, fetchLessons } from "@/services/lessons";
import { getSupabase } from "@/services/supabase";

const inputCls =
  "rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";
const chipBtn =
  "rounded-lg bg-white/5 px-2 py-1 text-xs text-slate-300 hover:bg-white/15";

interface ExamOption {
  id: number;
  title: string;
}

// ---------- Form thêm/sửa 1 mục trong bài học ----------
function ItemForm({
  lessonId,
  item,
  exams,
  nextSort,
  onSaved,
  onCancel,
}: {
  lessonId: number;
  item: LessonItem | null;
  exams: ExamOption[];
  nextSort: number;
  onSaved: () => void;
  onCancel: () => void;
}) {
  const toast = useToast();
  const [kind, setKind] = useState<LessonItemKind>(item?.kind ?? "ly_thuyet");
  const [title, setTitle] = useState(item?.title ?? "");
  const [subtitle, setSubtitle] = useState(item?.subtitle ?? "");
  const [videoUrl, setVideoUrl] = useState(item?.video_url ?? "");
  const [pdfUrl, setPdfUrl] = useState(item?.pdf_url ?? "");
  const [bodyHtml, setBodyHtml] = useState(item?.body_html ?? "");
  const [examId, setExamId] = useState<string>(item?.exam_id ? String(item.exam_id) : "");
  const [busy, setBusy] = useState(false);

  const isExamKind = kind === "luyen_tap_de" || kind === "kiem_tra";
  const isVideoKind = kind === "video";

  async function save() {
    if (!title.trim()) {
      toast("error", "Mục cần có tiêu đề.");
      return;
    }
    setBusy(true);
    const payload = {
      lesson_id: lessonId,
      kind,
      title: title.trim(),
      subtitle: subtitle.trim(),
      body_html: isExamKind || isVideoKind ? "" : bodyHtml,
      video_url: isVideoKind ? videoUrl.trim() : "",
      pdf_url: isExamKind ? "" : pdfUrl.trim(),
      exam_id: isExamKind && examId ? Number(examId) : null,
      sort_order: item?.sort_order ?? nextSort,
    };
    const supabase = getSupabase();
    const { error } = item
      ? await supabase.from("lesson_items").update(payload).eq("id", item.id)
      : await supabase.from("lesson_items").insert(payload);
    setBusy(false);
    if (error) {
      toast("error", error.message);
      return;
    }
    toast("success", item ? "Đã cập nhật mục." : "Đã thêm mục.");
    onSaved();
  }

  return (
    <div className="space-y-3 rounded-2xl border border-primary/40 bg-[#0B1020] p-5">
      <div className="flex flex-wrap items-center gap-3">
        <select
          value={kind}
          onChange={(e) => setKind(e.target.value as LessonItemKind)}
          className={`${inputCls} bg-[#0B1020]`}
        >
          {SECTION_ORDER.map((k) => (
            <option key={k} value={k}>
              {SECTION_META[k].icon} {SECTION_META[k].label}
            </option>
          ))}
        </select>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Tiêu đề mục, vd Lý thuyết trọng tâm"
          className={`${inputCls} min-w-60 flex-1`}
        />
        <input
          value={subtitle}
          onChange={(e) => setSubtitle(e.target.value)}
          placeholder="Phụ đề (không bắt buộc)"
          className={`${inputCls} min-w-40 flex-1`}
        />
      </div>

      {isVideoKind && (
        <input
          value={videoUrl}
          onChange={(e) => setVideoUrl(e.target.value)}
          placeholder="Link YouTube, vd https://youtu.be/…"
          className={`${inputCls} w-full`}
        />
      )}
      {!isExamKind && (
        <input
          value={pdfUrl}
          onChange={(e) => setPdfUrl(e.target.value)}
          placeholder="Link PDF (không bắt buộc)"
          className={`${inputCls} w-full`}
        />
      )}
      {!isExamKind && !isVideoKind && (
        <LaTexEditor
          value={bodyHtml}
          onChange={(html) => setBodyHtml(html)}
          placeholder="Nội dung (viết LaTeX hoặc HTML)"
        />
      )}
      {isExamKind && (
        <select
          value={examId}
          onChange={(e) => setExamId(e.target.value)}
          className={`${inputCls} w-full bg-[#0B1020]`}
        >
          <option value="">— Chọn đề đã soạn (tab Đề kiểm tra) —</option>
          {exams.map((e) => (
            <option key={e.id} value={e.id}>
              #{e.id} · {e.title}
            </option>
          ))}
        </select>
      )}

      <div className="flex gap-2">
        <button
          onClick={save}
          disabled={busy}
          className="rounded-full bg-[#2563EB] px-5 py-2 text-sm font-semibold text-white hover:bg-primary-dark disabled:opacity-50"
        >
          {item ? "Lưu mục" : "+ Thêm mục"}
        </button>
        <button
          onClick={onCancel}
          className="rounded-full border border-white/15 px-5 py-2 text-sm text-slate-300 hover:border-white/30"
        >
          Hủy
        </button>
      </div>
    </div>
  );
}

// ---------- Quản lý mục của 1 bài học ----------
function LessonItemsEditor({ lesson, onBack }: { lesson: Lesson; onBack: () => void }) {
  const toast = useToast();
  const [items, setItems] = useState<LessonItem[]>([]);
  const [exams, setExams] = useState<ExamOption[]>([]);
  const [editing, setEditing] = useState<LessonItem | null>(null);
  const [adding, setAdding] = useState(false);

  const reload = useCallback(() => {
    fetchLessonItems(lesson.id).then(setItems);
  }, [lesson.id]);
  useEffect(reload, [reload]);

  useEffect(() => {
    getSupabase()
      .from("exams")
      .select("id, title")
      .order("created_at", { ascending: false })
      .then(({ data }) => setExams((data as ExamOption[]) ?? []));
  }, []);

  async function move(idx: number, dir: -1 | 1) {
    const other = idx + dir;
    if (other < 0 || other >= items.length) return;
    const a = items[idx];
    const b = items[other];
    const supabase = getSupabase();
    await supabase.from("lesson_items").update({ sort_order: b.sort_order }).eq("id", a.id);
    await supabase.from("lesson_items").update({ sort_order: a.sort_order }).eq("id", b.id);
    reload();
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-3">
        <button onClick={onBack} className={chipBtn}>
          ← Quay lại
        </button>
        <h3 className="font-display font-semibold text-white">{lesson.title}</h3>
        {!adding && !editing && (
          <button
            onClick={() => setAdding(true)}
            className="ml-auto rounded-full bg-[#2563EB] px-5 py-2 text-sm font-semibold text-white hover:bg-primary-dark"
          >
            + Thêm mục
          </button>
        )}
      </div>

      {(adding || editing) && (
        <ItemForm
          lessonId={lesson.id}
          item={editing}
          exams={exams}
          nextSort={items.length + 1}
          onSaved={() => {
            setAdding(false);
            setEditing(null);
            reload();
          }}
          onCancel={() => {
            setAdding(false);
            setEditing(null);
          }}
        />
      )}

      <div className="space-y-2">
        {items.map((it, idx) => {
          const meta = SECTION_META[it.kind];
          return (
            <div
              key={it.id}
              className="flex flex-wrap items-center gap-3 rounded-2xl border border-white/10 bg-[#0B1020] px-4 py-3"
            >
              <span title={meta.label}>{meta.icon}</span>
              <span className="min-w-0 flex-1">
                <span className="block truncate text-sm font-medium text-white">
                  {it.title}
                </span>
                <span className="text-xs" style={{ color: meta.color }}>
                  {meta.label}
                  {it.exam_id && ` · đề #${it.exam_id}`}
                  {it.video_url && " · video"}
                  {it.pdf_url && " · PDF"}
                </span>
              </span>
              <span className="flex items-center gap-1">
                <button onClick={() => move(idx, -1)} title="Lên" className={chipBtn}>
                  ↑
                </button>
                <button onClick={() => move(idx, 1)} title="Xuống" className={chipBtn}>
                  ↓
                </button>
                <button
                  onClick={() => {
                    setAdding(false);
                    setEditing(it);
                  }}
                  className="rounded-full border border-white/15 px-3 py-1 text-xs text-slate-300 hover:border-white/30"
                >
                  Sửa
                </button>
                <button
                  onClick={async () => {
                    if (!confirm(`Xóa mục "${it.title}"?`)) return;
                    await getSupabase().from("lesson_items").delete().eq("id", it.id);
                    toast("success", "Đã xóa mục.");
                    reload();
                  }}
                  className="rounded-full border border-red-500/30 px-3 py-1 text-xs text-red-300 hover:border-red-500/60"
                >
                  Xóa
                </button>
              </span>
            </div>
          );
        })}
        {items.length === 0 && !adding && (
          <p className="text-sm text-slate-400">
            Chưa có mục nào — bấm “+ Thêm mục” để soạn lý thuyết, video, đề…
          </p>
        )}
      </div>
    </div>
  );
}

// ---------- Quản lý bài học của 1 chương ----------
function ChapterLessonsEditor({
  chapter,
  schoolClass,
  onBack,
}: {
  chapter: Chapter;
  schoolClass: SchoolClass | null;
  onBack: () => void;
}) {
  const toast = useToast();
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [openLesson, setOpenLesson] = useState<Lesson | null>(null);
  const [title, setTitle] = useState("");

  const reload = useCallback(() => {
    fetchLessons(true).then((ls) =>
      setLessons(ls.filter((l) => l.chapter_id === chapter.id)),
    );
  }, [chapter.id]);
  useEffect(reload, [reload]);

  if (openLesson)
    return <LessonItemsEditor lesson={openLesson} onBack={() => setOpenLesson(null)} />;

  async function addLesson(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim()) return;
    const { error } = await getSupabase().from("lessons").insert({
      chapter_id: chapter.id,
      title: title.trim(),
      sort_order: lessons.length + 1,
    });
    if (error) {
      toast("error", error.message);
      return;
    }
    toast("success", "Đã thêm bài học.");
    setTitle("");
    reload();
  }

  async function move(idx: number, dir: -1 | 1) {
    const other = idx + dir;
    if (other < 0 || other >= lessons.length) return;
    const a = lessons[idx];
    const b = lessons[other];
    const supabase = getSupabase();
    await supabase.from("lessons").update({ sort_order: b.sort_order }).eq("id", a.id);
    await supabase.from("lessons").update({ sort_order: a.sort_order }).eq("id", b.id);
    reload();
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-3">
        <button onClick={onBack} className={chipBtn}>
          ← Chọn chương khác
        </button>
        <div className="min-w-0">
          <p className="text-xs font-semibold uppercase tracking-wide text-[#60A5FA]">
            {schoolClass ? `Lớp ${schoolClass.name}` : "Toàn trường"}
          </p>
          <h3 className="truncate font-display font-semibold text-white">
            {chapter.title}
          </h3>
        </div>
      </div>

      <form onSubmit={addLesson} className="flex flex-wrap gap-3">
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Tên bài học, vd Giá trị lượng giác của góc lượng giác"
          className={`${inputCls} min-w-72 flex-1`}
        />
        <button
          type="submit"
          className="rounded-full bg-[#2563EB] px-5 py-2 text-sm font-semibold text-white hover:bg-primary-dark"
        >
          + Thêm bài
        </button>
      </form>

      <div className="space-y-2">
        {lessons.map((l, idx) => (
          <div
            key={l.id}
            className={`flex flex-wrap items-center gap-3 rounded-2xl border border-white/10 bg-[#0B1020] px-4 py-3 ${
              l.published ? "" : "opacity-50"
            }`}
          >
            <button
              onClick={() => setOpenLesson(l)}
              className="min-w-0 flex-1 text-left"
            >
              <span className="block truncate font-medium text-white hover:text-primary">
                {l.title}
              </span>
              <span className="text-xs text-slate-500">{l.itemCount} mục</span>
            </button>
            <span className="flex items-center gap-1">
              <button onClick={() => move(idx, -1)} title="Lên" className={chipBtn}>
                ↑
              </button>
              <button onClick={() => move(idx, 1)} title="Xuống" className={chipBtn}>
                ↓
              </button>
              <button
                onClick={async () => {
                  await getSupabase()
                    .from("lessons")
                    .update({ published: !l.published })
                    .eq("id", l.id);
                  reload();
                }}
                className="rounded-full border border-white/15 px-3 py-1 text-xs text-slate-300 hover:border-white/30"
              >
                {l.published ? "Ẩn" : "Hiện"}
              </button>
              <button
                onClick={() => setOpenLesson(l)}
                className="rounded-full border border-white/15 px-3 py-1 text-xs text-slate-300 hover:border-white/30"
              >
                Soạn mục
              </button>
              <button
                onClick={async () => {
                  if (!confirm(`Xóa bài "${l.title}" và toàn bộ mục bên trong?`)) return;
                  await getSupabase().from("lessons").delete().eq("id", l.id);
                  toast("success", "Đã xóa bài học.");
                  reload();
                }}
                className="rounded-full border border-red-500/30 px-3 py-1 text-xs text-red-300 hover:border-red-500/60"
              >
                Xóa
              </button>
            </span>
          </div>
        ))}
        {lessons.length === 0 && (
          <p className="text-sm text-slate-400">Chưa có bài học nào trong chương.</p>
        )}
      </div>
    </div>
  );
}

// ---------- Cấp cao nhất: danh sách chương ----------
export default function LessonsAdmin() {
  const toast = useToast();
  const [classes, setClasses] = useState<SchoolClass[]>([]);
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [openChapter, setOpenChapter] = useState<Chapter | null>(null);
  const [title, setTitle] = useState("");
  const [selectedClassId, setSelectedClassId] = useState<number | null>(null);

  const reload = useCallback(() => {
    fetchChapters().then(setChapters);
  }, []);
  useEffect(reload, [reload]);

  useEffect(() => {
    fetchClasses().then((items) => {
      setClasses(items);
      setSelectedClassId((current) => current ?? items[0]?.id ?? null);
    });
  }, []);

  const selectedClass =
    classes.find((schoolClass) => schoolClass.id === selectedClassId) ?? null;
  const displayClasses = displayClassesByGrade(classes);
  const visibleClassIds =
    selectedClassId === null ? [] : (expandClassIdsByGrade([selectedClassId], classes) ?? []);
  const classChapters =
    selectedClassId === null
      ? []
      : chapters.filter(
          (chapter) =>
            chapter.classIds.length === 0 ||
            chapter.classIds.some((classId) => visibleClassIds.includes(classId)),
        );

  if (openChapter)
    return (
      <ChapterLessonsEditor
        chapter={openChapter}
        schoolClass={selectedClass}
        onBack={() => setOpenChapter(null)}
      />
    );

  async function addChapter(e: React.FormEvent) {
    e.preventDefault();
    if (!selectedClassId) {
      toast("error", "Hãy chọn lớp trước khi thêm chương.");
      return;
    }
    if (!title.trim()) return;
    const { data, error } = await getSupabase()
      .from("chapters")
      .insert({ title: title.trim(), sort_order: classChapters.length + 1 })
      .select("id")
      .single();
    if (error || !data) {
      toast("error", error?.message ?? "Không tạo được chương.");
      return;
    }
    await setItemClasses("chapter_classes", "chapter_id", data.id, [selectedClassId]);
    toast("success", "Đã thêm chương.");
    setTitle("");
    reload();
  }

  async function move(idx: number, dir: -1 | 1) {
    const other = idx + dir;
    if (other < 0 || other >= classChapters.length) return;
    const a = classChapters[idx];
    const b = classChapters[other];
    const supabase = getSupabase();
    await supabase.from("chapters").update({ sort_order: b.sort_order }).eq("id", a.id);
    await supabase.from("chapters").update({ sort_order: a.sort_order }).eq("id", b.id);
    reload();
  }

  return (
    <div className="space-y-6">
      <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        <p className="mb-3 text-sm font-medium text-slate-300">
          1. Chọn lớp
        </p>
        <div className="flex flex-wrap gap-2">
          {displayClasses.map((schoolClass) => {
            const active = schoolClass.id === selectedClassId;
            return (
              <button
                key={schoolClass.id}
                type="button"
                onClick={() => {
                  setSelectedClassId(schoolClass.id);
                  setOpenChapter(null);
                }}
                style={
                  active
                    ? { backgroundColor: schoolClass.color, borderColor: schoolClass.color }
                    : undefined
                }
                className={`rounded-full border px-4 py-2 text-sm font-semibold transition-colors ${
                  active
                    ? "text-white"
                    : "border-white/10 text-slate-400 hover:border-white/30 hover:text-slate-200"
                }`}
              >
                {schoolClass.icon && `${schoolClass.icon} `}
                {schoolClass.name}
              </button>
            );
          })}
          {displayClasses.length === 0 && (
            <span className="text-sm text-slate-500">
              Chưa có lớp — thêm lớp ở mục Lớp học trước.
            </span>
          )}
        </div>
      </section>

      <form
        onSubmit={addChapter}
        className="space-y-4 rounded-2xl border border-white/10 bg-[#0B1020] p-5"
      >
        <div>
          <p className="text-sm font-medium text-slate-300">
            2. Thêm chương cho {selectedClass ? `lớp ${selectedClass.name}` : "lớp đã chọn"}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            Chương mới sẽ chỉ hiện trong lớp đang chọn, sau đó admin vào chương để thêm bài học.
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Tên chương, vd Chương 1: Hàm số lượng giác…"
            className={`${inputCls} min-w-72 flex-1`}
            disabled={!selectedClassId}
          />
          <button
            type="submit"
            disabled={!selectedClassId}
            className="rounded-full bg-[#2563EB] px-5 py-2 text-sm font-semibold text-white hover:bg-primary-dark"
          >
            + Thêm chương
          </button>
        </div>
      </form>

      <div className="space-y-2">
        <div>
          <p className="text-sm font-medium text-slate-300">
            3. Chọn chương để đăng bài học
          </p>
          {selectedClass && (
            <p className="mt-1 text-xs text-slate-500">
              Đang xem chương của lớp {selectedClass.name}.
            </p>
          )}
        </div>
        {classChapters.map((ch, idx) => (
          <div
            key={ch.id}
            className="flex flex-wrap items-center gap-3 rounded-2xl border border-white/10 bg-[#0B1020] px-4 py-3"
          >
            <button
              onClick={() => setOpenChapter(ch)}
              className="min-w-0 flex-1 text-left"
            >
              <span className="block truncate font-medium text-white hover:text-primary">
                {ch.title}
              </span>
              <span className="text-xs text-slate-500">
                {ch.classIds.length === 0
                  ? "Toàn trường — chưa gán lớp"
                  : classes
                      .filter((c) => ch.classIds.includes(c.id))
                      .map((c) => c.name)
                      .join(", ")}
              </span>
            </button>
            <span className="flex items-center gap-1">
              {selectedClassId !== null && (
                <button
                  onClick={async () => {
                    const has = ch.classIds.includes(selectedClassId);
                    const nextIds = has
                      ? ch.classIds.filter((id) => id !== selectedClassId)
                      : [...ch.classIds, selectedClassId];
                    await setItemClasses("chapter_classes", "chapter_id", ch.id, nextIds);
                    reload();
                  }}
                  title={
                    ch.classIds.includes(selectedClassId)
                      ? `Bỏ khỏi lớp ${selectedClass?.name}`
                      : `Gán vào lớp ${selectedClass?.name}`
                  }
                  className={`rounded-full border px-3 py-1 text-xs font-semibold ${
                    ch.classIds.includes(selectedClassId)
                      ? "border-emerald-400/40 bg-emerald-500/10 text-emerald-200"
                      : "border-white/15 text-slate-300 hover:border-white/30"
                  }`}
                >
                  {ch.classIds.includes(selectedClassId)
                    ? `✓ ${selectedClass?.name}`
                    : `+ ${selectedClass?.name}`}
                </button>
              )}
              <button onClick={() => move(idx, -1)} title="Lên" className={chipBtn}>
                ↑
              </button>
              <button onClick={() => move(idx, 1)} title="Xuống" className={chipBtn}>
                ↓
              </button>
              <button
                onClick={() => setOpenChapter(ch)}
                className="rounded-full border border-white/15 px-3 py-1 text-xs text-slate-300 hover:border-white/30"
              >
                Soạn bài
              </button>
              <button
                onClick={async () => {
                  if (!confirm(`Xóa chương "${ch.title}" và toàn bộ bài học bên trong?`))
                    return;
                  await getSupabase().from("chapters").delete().eq("id", ch.id);
                  toast("success", "Đã xóa chương.");
                  reload();
                }}
                className="rounded-full border border-red-500/30 px-3 py-1 text-xs text-red-300 hover:border-red-500/60"
              >
                Xóa
              </button>
            </span>
          </div>
        ))}
        {selectedClassId && classChapters.length === 0 && (
          <p className="text-sm text-slate-400">
            Lớp này chưa có chương nào — thêm chương đầu tiên ở trên.
          </p>
        )}
      </div>
    </div>
  );
}
