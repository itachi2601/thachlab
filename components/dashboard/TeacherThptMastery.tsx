"use client";

import { useEffect, useMemo, useState } from "react";
import { Copy, Users } from "lucide-react";
import type { ClassStudent } from "@/services/classes";
import {
  LEVEL_META,
  buildMasteryMap,
  fetchClassQuestionActivity,
  fetchCurriculumMeta,
  suggestGroups,
  type CurriculumMeta,
  type MasteryLevel,
  type QuestionActivityRow,
} from "@/services/class-insights";
import { useToast } from "@/components/ui/Toast";

/**
 * Bản đồ thành thạo của lớp theo bài/YCCĐ + gợi ý nhóm (N1: một cái nhìn, màu kèm biểu tượng).
 * Quy tắc nhãn: docs/mastery-rules.md.
 */
export default function TeacherThptMastery({
  students,
  onOpenStudent,
  onOpenTab,
}: {
  students: ClassStudent[];
  onOpenStudent: (id: string) => void;
  onOpenTab: (tab: "alerts") => void;
}) {
  const toast = useToast();
  const studentIds = useMemo(() => students.map((s) => s.id), [students]);
  const [rows, setRows] = useState<QuestionActivityRow[] | null>(null);
  const [meta, setMeta] = useState<CurriculumMeta | null>(null);
  const [error, setError] = useState("");
  const [chapterId, setChapterId] = useState<number | null>(null);
  const [lessonId, setLessonId] = useState<number | null>(null);

  useEffect(() => {
    let cancelled = false;
    Promise.all([fetchClassQuestionActivity(studentIds), fetchCurriculumMeta()])
      .then(([r, m]) => {
        if (cancelled) return;
        setRows(r);
        setMeta(m);
        setError("");
      })
      .catch((e: unknown) => {
        if (!cancelled) setError(e instanceof Error ? e.message : "Không tải được dữ liệu thành thạo.");
      });
    return () => { cancelled = true; };
  }, [studentIds]);

  const map = useMemo(() => (rows && meta ? buildMasteryMap(rows, meta) : null), [rows, meta]);
  const nameOf = useMemo(() => new Map(students.map((s) => [s.id, s.full_name])), [students]);

  // Các bài có dữ liệu của lớp, gom theo chương.
  const lessonsWithData = useMemo(() => {
    if (!map || !meta) return [];
    return [...map.topicsOfLesson.keys()]
      .map((id) => meta.lessons.get(id))
      .filter((l): l is NonNullable<typeof l> => Boolean(l))
      .sort((a, b) => {
        const ca = meta.chapters.get(a.chapterId)?.sortOrder ?? 0;
        const cb = meta.chapters.get(b.chapterId)?.sortOrder ?? 0;
        return ca - cb || a.sortOrder - b.sortOrder;
      });
  }, [map, meta]);

  const chapters = useMemo(() => {
    if (!meta) return [];
    const ids = [...new Set(lessonsWithData.map((l) => l.chapterId))];
    return ids.map((id) => meta.chapters.get(id)).filter((c): c is NonNullable<typeof c> => Boolean(c)).sort((a, b) => a.sortOrder - b.sortOrder);
  }, [lessonsWithData, meta]);

  // Chương mặc định = chương có hoạt động gần nhất của lớp.
  const defaultChapter = useMemo(() => {
    if (!rows || !meta) return null;
    let best: { t: string; ch: number } | null = null;
    for (const r of rows) {
      const lid = meta.topics.get(r.topic_id)?.lessonId;
      const ch = lid != null ? meta.lessons.get(lid)?.chapterId : undefined;
      if (ch != null && (!best || r.created_at > best.t)) best = { t: r.created_at, ch };
    }
    return best?.ch ?? chapters[0]?.id ?? null;
  }, [rows, meta, chapters]);

  const activeChapter = chapterId ?? defaultChapter;
  const shownLessons = lessonsWithData.filter((l) => l.chapterId === activeChapter);

  const countsByLesson = (lid: number) => {
    const c: Record<MasteryLevel, string[]> = { weak: [], mid: [], strong: [], none: [] };
    for (const s of students) c[map?.byStudentLesson.get(s.id)?.get(lid) ?? "none"].push(s.id);
    return c;
  };

  // "Nên nhóm trước": bài có nhiều em chưa vững nhất (chỉ tính em đủ dữ liệu).
  const priority = useMemo(() => {
    if (!map) return [];
    return lessonsWithData
      .map((l) => {
        const c = countsByLesson(l.id);
        return { lesson: l, weak: c.weak.length, mid: c.mid.length };
      })
      .filter((x) => x.weak + x.mid >= 2)
      .sort((a, b) => b.weak * 2 + b.mid - (a.weak * 2 + a.mid))
      .slice(0, 4);
    // countsByLesson đọc map + students; không cần liệt kê
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [map, lessonsWithData, students]);

  if (error) return <p className="rounded-2xl border border-red-500/30 p-5 text-sm text-red-300">{error}</p>;
  if (!rows || !meta || !map) return <p className="text-sm text-slate-400">Đang tính mức thành thạo…</p>;
  if (lessonsWithData.length === 0) {
    return (
      <p className="rounded-2xl border border-dashed border-white/10 p-8 text-center text-sm text-slate-500">
        Lớp chưa có câu nào gắn yêu cầu cần đạt. Khi học sinh làm đề/luyện tập có nhãn Chủ đề, bản đồ sẽ hiện ở đây.
      </p>
    );
  }

  const selected = lessonId ?? priority[0]?.lesson.id ?? shownLessons[0]?.id ?? null;

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-center gap-3">
        <select
          aria-label="Chọn chương"
          value={activeChapter ?? ""}
          onChange={(e) => { setChapterId(Number(e.target.value)); setLessonId(null); }}
          className="min-w-60 max-w-full rounded-xl border border-white/10 bg-panel px-3 py-2 text-sm text-white"
        >
          {chapters.map((c) => <option key={c.id} value={c.id}>{c.title}</option>)}
        </select>
        <ul className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-slate-400">
          {(["strong", "mid", "weak", "none"] as MasteryLevel[]).map((k) => (
            <li key={k}>{LEVEL_META[k].icon} {LEVEL_META[k].label}</li>
          ))}
        </ul>
      </div>

      {priority.length > 0 && (
        <section className="rounded-2xl border border-amber-400/20 bg-amber-500/[.05] p-4">
          <h3 className="mb-2 font-display text-base font-bold text-white">Nên nhóm lại trước</h3>
          <ul className="space-y-2">
            {priority.map(({ lesson, weak, mid }) => (
              <li key={lesson.id}>
                <button
                  type="button"
                  onClick={() => { setChapterId(lesson.chapterId); setLessonId(lesson.id); }}
                  className={`flex w-full items-center justify-between gap-3 rounded-xl px-4 py-3 text-left text-sm ${selected === lesson.id ? "bg-white/10" : "bg-white/[.04] hover:bg-white/10"} text-slate-200`}
                >
                  <span className="min-w-0 truncate">{lesson.title}</span>
                  <span className="shrink-0 text-xs text-slate-400">🔴 {weak} · 🟡 {mid}</span>
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}

      <div className="overflow-x-auto rounded-2xl border border-white/10">
        <table className="w-full text-sm">
          <thead className="bg-white/5 text-xs text-slate-400">
            <tr>
              <th className="sticky left-0 z-10 min-w-36 bg-panel px-3 py-2 text-left font-medium">Học sinh</th>
              {shownLessons.map((l) => (
                <th key={l.id} className="min-w-24 px-2 py-2 text-center font-medium">
                  <button
                    type="button"
                    onClick={() => setLessonId(l.id)}
                    className={`w-full rounded-lg px-1 py-1 leading-snug ${selected === l.id ? "bg-blue-600 text-white" : "hover:bg-white/10"}`}
                    title={l.title}
                  >
                    <span className="line-clamp-3 block">{l.title}</span>
                  </button>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {students.map((s) => (
              <tr key={s.id}>
                <td className="sticky left-0 bg-panel px-3 py-2">
                  <button type="button" onClick={() => onOpenStudent(s.id)} className="text-left text-white hover:underline">{s.full_name}</button>
                </td>
                {shownLessons.map((l) => {
                  const lv = map.byStudentLesson.get(s.id)?.get(l.id) ?? "none";
                  return (
                    <td key={l.id} className="px-2 py-2 text-center" title={`${s.full_name} · ${l.title}: ${LEVEL_META[lv].label}`}>
                      <span className={`inline-block min-w-9 rounded-md px-2 py-1 ${LEVEL_META[lv].cls}`}>{LEVEL_META[lv].icon}</span>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selected != null && meta.lessons.get(selected) && (
        <GroupPanel
          lessonTitle={meta.lessons.get(selected)!.title}
          topicIds={map.topicsOfLesson.get(selected) ?? []}
          meta={meta}
          students={students}
          nameOf={nameOf}
          cells={map.byStudentTopic}
          lessonLevels={countsByLesson(selected)}
          onCopy={(text) => {
            void navigator.clipboard?.writeText(text).then(() => toast("success", "Đã chép danh sách nhóm."), () => toast("error", "Không chép được."));
          }}
          onOpenTab={onOpenTab}
        />
      )}
    </div>
  );
}

function GroupPanel({
  lessonTitle,
  topicIds,
  meta,
  students,
  nameOf,
  cells,
  lessonLevels,
  onCopy,
  onOpenTab,
}: {
  lessonTitle: string;
  topicIds: number[];
  meta: CurriculumMeta;
  students: ClassStudent[];
  nameOf: Map<string, string>;
  cells: ReturnType<typeof buildMasteryMap>["byStudentTopic"];
  lessonLevels: Record<MasteryLevel, string[]>;
  onCopy: (text: string) => void;
  onOpenTab: (tab: "alerts") => void;
}) {
  const needHelp = [...lessonLevels.weak, ...lessonLevels.mid];
  const groups = suggestGroups(needHelp, lessonLevels.strong);
  const n = (id: string) => nameOf.get(id) ?? "—";

  // Từng YCCĐ: ai chưa đạt (chỉ tính em đủ dữ liệu).
  const perTopic = topicIds
    .map((tid) => {
      const weak = students
        .filter((s) => {
          const lv = cells.get(s.id)?.get(tid)?.level;
          return lv === "weak" || lv === "mid";
        })
        .map((s) => s.id);
      return { tid, name: meta.topics.get(tid)?.name ?? `#${tid}`, isLesson: meta.topics.get(tid)?.parentId == null, weak };
    })
    .filter((t) => t.weak.length > 0)
    .sort((a, b) => b.weak.length - a.weak.length);

  const text = [
    `Nhóm ôn: ${lessonTitle}`,
    ...groups.map((g, i) => `Nhóm ${i + 1}: ${g.weak.map(n).join(", ")}${g.helper ? ` — kèm: ${n(g.helper)}` : ""}`),
  ].join("\n");

  return (
    <section className="space-y-4 rounded-2xl border border-white/10 bg-panel p-5">
      <div className="flex flex-wrap items-center gap-3">
        <Users size={18} className="text-blue-300" />
        <h3 className="min-w-0 flex-1 font-display text-base font-bold text-white">{lessonTitle}</h3>
        <span className="text-xs text-slate-400">
          ✅ {lessonLevels.strong.length} · 🟡 {lessonLevels.mid.length} · 🔴 {lessonLevels.weak.length} · ⚪ {lessonLevels.none.length}
        </span>
      </div>

      {needHelp.length === 0 ? (
        <p className="text-sm text-emerald-300">Chưa có em nào cần ôn lại bài này (trong số em đủ dữ liệu).</p>
      ) : (
        <>
          <div>
            <p className="mb-2 text-xs font-bold uppercase tracking-wide text-slate-400">Chưa vững theo từng yêu cầu</p>
            <ul className="space-y-2">
              {perTopic.slice(0, 6).map((t) => (
                <li key={t.tid} className="rounded-xl bg-white/[.04] px-4 py-3 text-sm">
                  <p className="font-semibold text-slate-100">{t.weak.length} em · {t.isLesson ? "Câu tổng hợp của bài" : t.name}</p>
                  <p className="mt-1 text-xs leading-relaxed text-slate-400">{t.weak.map(n).join(", ")}</p>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <p className="mb-2 text-xs font-bold uppercase tracking-wide text-slate-400">Gợi ý chia nhóm (em vững kèm em chưa vững)</p>
            <ul className="space-y-2">
              {groups.map((g, i) => (
                <li key={i} className="rounded-xl bg-white/[.04] px-4 py-3 text-sm text-slate-200">
                  <p><b>Nhóm {i + 1}:</b> {g.weak.map(n).join(", ")}</p>
                  <p className="text-xs text-slate-400">{g.helper ? `Kèm: ${n(g.helper)}` : "Chưa có em nào nắm vững để kèm — giáo viên dạy lại nhóm này"}</p>
                </li>
              ))}
            </ul>
          </div>
          <div className="flex flex-wrap gap-2">
            <button type="button" onClick={() => onCopy(text)} className="inline-flex items-center gap-2 rounded-full bg-primary px-4 py-2 text-sm font-semibold text-white hover:bg-primary-dark">
              <Copy size={14} /> Chép danh sách nhóm
            </button>
            <button type="button" onClick={() => onOpenTab("alerts")} className="rounded-full border border-white/15 px-4 py-2 text-sm text-slate-200 hover:bg-white/10">
              Mở phụ đạo
            </button>
          </div>
        </>
      )}
    </section>
  );
}
