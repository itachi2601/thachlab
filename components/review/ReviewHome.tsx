"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ArrowDown, ArrowUp, Plus, X } from "lucide-react";
import Button from "@/components/ui/Button";
import { useToast } from "@/components/ui/Toast";
import type { SchoolClass } from "@/features/exams/types";
import { fetchClasses } from "@/services/classes";
import {
  createReviewSession,
  fetchChapterExerciseExams,
  fetchChapterQuickQuizzes,
  fetchPickerChapters,
  fetchPickerExamById,
  listReviewSessions,
  reviewErrorText,
  suggestedMinutes,
  type PickerChapter,
  type PickerExam,
  type ReviewListItem,
} from "@/services/review-session";
import { reviewConsolePath } from "@/lib/review-link";

interface PickedStage {
  pick: PickerExam;
  minutes: number;
}

const STATUS_TEXT: Record<ReviewListItem["status"], string> = {
  ready: "Chưa bắt đầu",
  running: "Đang diễn ra",
  finished: "Đã kết thúc",
};

/** Danh sách buổi ôn gần đây + form tạo buổi mới (chọn lớp → chương → các đề "Kiểm tra nhanh" làm chặng). */
export default function ReviewHome() {
  const toast = useToast();
  const router = useRouter();
  const [sessions, setSessions] = useState<ReviewListItem[] | null>(null);
  const [classes, setClasses] = useState<SchoolClass[]>([]);
  const [classId, setClassId] = useState<number | null>(null);
  const [chapters, setChapters] = useState<PickerChapter[]>([]);
  const [chapterId, setChapterId] = useState<number | null>(null);
  const [options, setOptions] = useState<PickerExam[] | null>(null);
  const [exercises, setExercises] = useState<PickerExam[] | null>(null);
  const [stages, setStages] = useState<PickedStage[]>([]);
  const [title, setTitle] = useState("");
  const [threshold, setThreshold] = useState(80);
  const [manualId, setManualId] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    let off = false;
    listReviewSessions(null)
      .then((r) => !off && setSessions(r))
      .catch(() => !off && setSessions([]));
    fetchClasses()
      .then((c) => !off && setClasses(c as SchoolClass[]))
      .catch(() => undefined);
    return () => {
      off = true;
    };
  }, []);

  useEffect(() => {
    if (!classId) return;
    let off = false;
    fetchPickerChapters(classId)
      .then((c) => {
        if (off) return;
        setChapters(c);
        setChapterId(null);
        setOptions(null);
        setExercises(null);
      })
      .catch(() => !off && setChapters([]));
    return () => {
      off = true;
    };
  }, [classId]);

  const loadChapter = useCallback(
    async (id: number) => {
      setChapterId(id);
      setOptions(null);
      setExercises(null);
      try {
        const [quick, ex] = await Promise.all([fetchChapterQuickQuizzes(id), fetchChapterExerciseExams(id)]);
        setOptions(quick);
        setExercises(ex);
        const ch = chapters.find((c) => c.id === id);
        setTitle((t) => t || (ch ? `Ôn tập · ${ch.title}` : ""));
      } catch {
        setOptions([]);
        setExercises([]);
        toast("error", "Không tải được danh sách đề của chương này.");
      }
    },
    [chapters, toast],
  );

  const chosen = useMemo(() => new Set(stages.map((s) => s.pick.examId)), [stages]);

  function toggle(p: PickerExam) {
    setStages((cur) =>
      chosen.has(p.examId)
        ? cur.filter((s) => s.pick.examId !== p.examId)
        : [...cur, { pick: p, minutes: suggestedMinutes(p.questionCount) }],
    );
  }

  function move(i: number, d: -1 | 1) {
    setStages((cur) => {
      const j = i + d;
      if (j < 0 || j >= cur.length) return cur;
      const next = [...cur];
      [next[i], next[j]] = [next[j], next[i]];
      return next;
    });
  }

  async function addManual() {
    const id = Number(manualId.replace(/\D/g, ""));
    if (!id) return;
    if (chosen.has(id)) {
      toast("info", "Đề này đã có trong danh sách chặng.");
      return;
    }
    const p = await fetchPickerExamById(id);
    if (!p) {
      toast("error", `Không tìm thấy đề số ${id}.`);
      return;
    }
    setStages((cur) => [...cur, { pick: p, minutes: suggestedMinutes(p.questionCount) }]);
    setManualId("");
  }

  async function create() {
    if (!classId || stages.length === 0 || busy) return;
    setBusy(true);
    try {
      const id = await createReviewSession(
        classId,
        title.trim() || "Buổi ôn tập",
        threshold,
        stages.map((s) => ({ exam_id: s.pick.examId, item_id: s.pick.itemId, title: s.pick.title.replace(/^Kiểm tra nhanh\s*[—-]\s*/i, ""), minutes: s.minutes })),
      );
      router.push(reviewConsolePath(id));
    } catch (e) {
      toast("error", reviewErrorText(e));
      setBusy(false);
    }
  }

  const unpublished = stages.filter((s) => !s.pick.published).length;

  return (
    <div className="space-y-8">
      <header>
        <h1 className="font-display text-2xl font-bold text-ink">Ôn tập theo chặng</h1>
        <p className="mt-1 text-sm text-muted">
          Cả lớp ôn cùng nhịp: mỗi chặng là một đề (Kiểm tra nhanh để ôn lý thuyết, đề bài tập để ôn các dạng), có đồng hồ chung. Giáo viên và trợ giảng thấy
          từng em chưa mở, đang làm hay đã đạt; học sinh chỉ thấy tiến độ của mình và số liệu chung của lớp.
        </p>
      </header>

      <section aria-labelledby="gan-day" className="space-y-3">
        <h2 id="gan-day" className="text-lg font-bold text-ink">Buổi ôn gần đây</h2>
        {sessions === null ? (
          <p className="text-sm text-muted">Đang tải…</p>
        ) : sessions.length === 0 ? (
          <p className="text-sm text-muted">Chưa có buổi ôn nào. Tạo buổi đầu tiên ở bên dưới.</p>
        ) : (
          <ul className="space-y-2">
            {sessions.map((s) => (
              <li key={s.id}>
                <Link
                  href={reviewConsolePath(s.id)}
                  className="flex min-h-11 flex-wrap items-center gap-x-3 gap-y-1 rounded-2xl border border-line bg-panel px-4 py-3 hover:bg-surface-2"
                >
                  <span className="min-w-0 flex-1 font-semibold text-ink">{s.title}</span>
                  <span className="text-sm text-muted">Lớp {s.class_name} · {s.stage_count} chặng</span>
                  <span className="text-sm font-semibold text-primary">
                    {STATUS_TEXT[s.status]}
                    {s.status === "running" ? ` · chặng ${s.current_stage + 1}` : ""}
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section aria-labelledby="tao-moi" className="space-y-4 rounded-2xl border border-line bg-panel p-4 sm:p-5">
        <h2 id="tao-moi" className="text-lg font-bold text-ink">Tạo buổi ôn mới</h2>

        <div className="grid gap-3 sm:grid-cols-2">
          <label className="block text-sm font-semibold text-ink">
            Lớp
            <select
              value={classId ?? ""}
              onChange={(e) => setClassId(Number(e.target.value) || null)}
              className="mt-1 block min-h-11 w-full rounded-xl border border-line-strong bg-panel px-3 text-base text-ink"
            >
              <option value="">— chọn lớp —</option>
              {classes.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </label>
          <label className="block text-sm font-semibold text-ink">
            Chương
            <select
              value={chapterId ?? ""}
              onChange={(e) => e.target.value && void loadChapter(Number(e.target.value))}
              disabled={!classId}
              className="mt-1 block min-h-11 w-full rounded-xl border border-line-strong bg-panel px-3 text-base text-ink disabled:opacity-50"
            >
              <option value="">— chọn chương —</option>
              {chapters.map((c) => (
                <option key={c.id} value={c.id}>{c.title}</option>
              ))}
            </select>
          </label>
        </div>

        {chapterId && (
          <>
            <ExamPicker
              heading="Ôn lý thuyết — đề Kiểm tra nhanh của chương"
              empty="Chương này chưa có Kiểm tra nhanh gắn vào bài. Có thể nhập mã đề ở dưới."
              list={options}
              chosen={chosen}
              toggle={toggle}
            />
            <ExamPicker
              heading="Ôn các dạng bài tập — đề bài tập của chương"
              empty="Chương này chưa có đề bài tập gắn vào bài. Có thể nhập mã đề ở dưới."
              list={exercises}
              chosen={chosen}
              toggle={toggle}
            />
          </>
        )}

        <div className="flex flex-wrap items-end gap-2">
          <label className="block text-sm font-semibold text-ink">
            Thêm đề theo mã số
            <input
              inputMode="numeric"
              value={manualId}
              onChange={(e) => setManualId(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && void addManual()}
              placeholder="vd 770"
              className="mt-1 block min-h-11 w-36 rounded-xl border border-line-strong bg-panel px-3 text-base text-ink"
            />
          </label>
          <Button variant="outline" onClick={() => void addManual()}>
            <Plus size={16} /> Thêm
          </Button>
        </div>

        {stages.length > 0 && (
          <div>
            <p className="mb-2 text-sm font-semibold text-ink">Các chặng theo thứ tự ({stages.length})</p>
            <ol className="space-y-2">
              {stages.map((s, i) => (
                <li key={s.pick.examId} className="flex flex-wrap items-center gap-2 rounded-xl border border-line px-3 py-2">
                  <span className="w-16 shrink-0 text-sm font-bold text-primary">Chặng {i + 1}</span>
                  <span className="min-w-0 flex-1 basis-40 text-sm text-ink">{s.pick.lessonId ? s.pick.lessonTitle : s.pick.title}</span>
                  <label className="flex items-center gap-1.5 text-sm text-muted">
                    <input
                      type="number"
                      min={1}
                      max={60}
                      value={s.minutes}
                      onChange={(e) => {
                        const v = Math.min(60, Math.max(1, Number(e.target.value) || 1));
                        setStages((cur) => cur.map((x, k) => (k === i ? { ...x, minutes: v } : x)));
                      }}
                      className="min-h-11 w-16 rounded-xl border border-line-strong bg-panel px-2 text-center text-base text-ink"
                      aria-label={`Số phút chặng ${i + 1}`}
                    />
                    phút
                  </label>
                  <span className="flex gap-1">
                    <button type="button" aria-label="Lên" onClick={() => move(i, -1)} className="grid size-11 place-items-center rounded-xl hover:bg-surface-2"><ArrowUp size={16} /></button>
                    <button type="button" aria-label="Xuống" onClick={() => move(i, 1)} className="grid size-11 place-items-center rounded-xl hover:bg-surface-2"><ArrowDown size={16} /></button>
                    <button type="button" aria-label="Bỏ chặng" onClick={() => setStages((cur) => cur.filter((_, k) => k !== i))} className="grid size-11 place-items-center rounded-xl hover:bg-surface-2"><X size={16} /></button>
                  </span>
                </li>
              ))}
            </ol>
            {unpublished > 0 && (
              <p className="mt-2 text-sm text-warn">
                ⚠ {unpublished} đề đang ẩn: học sinh sẽ không mở được. Bật Hiện cho đề (hoặc bỏ chặng) trước khi bắt đầu.
              </p>
            )}
          </div>
        )}

        <div className="grid gap-3 sm:grid-cols-2">
          <label className="block text-sm font-semibold text-ink">
            Tên buổi ôn
            <input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              maxLength={120}
              className="mt-1 block min-h-11 w-full rounded-xl border border-line-strong bg-panel px-3 text-base text-ink"
            />
          </label>
          <label className="block text-sm font-semibold text-ink">
            Ngưỡng đạt mỗi chặng (%)
            <input
              type="number"
              min={1}
              max={100}
              value={threshold}
              onChange={(e) => setThreshold(Math.min(100, Math.max(1, Number(e.target.value) || 80)))}
              className="mt-1 block min-h-11 w-28 rounded-xl border border-line-strong bg-panel px-3 text-base text-ink"
            />
          </label>
        </div>

        <Button onClick={() => void create()} disabled={!classId || stages.length === 0 || busy}>
          {busy ? "Đang tạo…" : "Tạo buổi ôn"}
        </Button>
      </section>
    </div>
  );
}

const KIND_TEXT: Record<string, string> = { bai_tap_ve_nha: "Bài tập về nhà", kiem_tra: "Kiểm tra" };

function ExamPicker({
  heading,
  empty,
  list,
  chosen,
  toggle,
}: {
  heading: string;
  empty: string;
  list: PickerExam[] | null;
  chosen: Set<number>;
  toggle: (p: PickerExam) => void;
}) {
  return (
    <div>
      <p className="mb-2 text-sm font-semibold text-ink">{heading} — chọn các đề làm chặng</p>
      {list === null ? (
        <p className="text-sm text-muted">Đang tải…</p>
      ) : list.length === 0 ? (
        <p className="text-sm text-muted">{empty}</p>
      ) : (
        <ul className="space-y-1.5">
          {list.map((o) => (
            <li key={o.examId}>
              <label className="flex min-h-11 cursor-pointer items-start gap-3 rounded-xl border border-line px-3 py-2 hover:bg-surface-2">
                <input type="checkbox" checked={chosen.has(o.examId)} onChange={() => toggle(o)} className="mt-1 size-5 shrink-0" />
                <span className="min-w-0 flex-1 text-sm text-ink">
                  <span className="font-semibold">{o.lessonTitle}</span>
                  <span className="block text-muted">
                    {o.kind && KIND_TEXT[o.kind] ? `${KIND_TEXT[o.kind]} · ` : ""}
                    {o.questionCount} câu · đề số {o.examId}
                    {!o.published && <span className="ml-2 font-semibold text-warn">⚠ đề đang ẩn</span>}
                  </span>
                </span>
              </label>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
