"use client";

import { useEffect, useMemo, useState } from "react";
import { AlertTriangle, Check, Loader2, Search } from "lucide-react";
import { fetchClassStudents, type ClassStudent } from "@/services/classes";
import {
  fetchOutcomeGaps,
  fetchQuestionTopics,
  lessonTopics,
  outcomeGapsByNeed,
  type OutcomeGap,
  type QuestionTopic,
} from "@/services/analytics";
import {
  ACTIVE_NEED_STATUSES,
  fetchNeedsForStudents,
  needLabel,
  type TutoringNeed,
} from "@/services/tutoring";

export interface PickedStudent {
  id: string;
  name: string;
}

const MAX_STUDENTS = 4;

const DEMO_ROSTER: ClassStudent[] = [
  { id: "demo-1", full_name: "Nguyễn Văn A (mẫu)", class_name: "12" },
  { id: "demo-2", full_name: "Trần Thị B (mẫu)", class_name: "12" },
];

/**
 * Phiếu phụ đạo: chọn em từ danh sách lớp (không gõ tên nữa — em phải có tài khoản
 * thì mới nối được với phần em đang hổng), rồi tick đúng chủ đề đã dạy trong buổi.
 * Tick xong, mục "cần phụ đạo" của em chuyển sang "đã phụ đạo"; bài kiểm tra sau em
 * làm đúng lại thì hệ thống tự đóng thành "đã khắc phục".
 */
export default function PhudaoPlanner({
  classId,
  grade,
  students,
  onChange,
  coverage,
  onCoverageChange,
  demo,
  badge,
}: {
  classId: number | null;
  grade: string | null;
  students: PickedStudent[];
  onChange: (students: PickedStudent[]) => void;
  /** studentId -> danh sách topicId đã dạy trong buổi này */
  coverage: Record<string, number[]>;
  onCoverageChange: (next: Record<string, number[]>) => void;
  demo: boolean;
  badge?: string;
}) {
  // Giữ kèm classId để lúc đổi lớp là danh sách cũ biến mất ngay, không phải chờ tải xong.
  const [loaded, setLoaded] = useState<{
    classId: number | null;
    list: ClassStudent[];
    error: string | null;
  } | null>(demo ? { classId: null, list: DEMO_ROSTER, error: null } : null);
  const [needs, setNeeds] = useState<TutoringNeed[]>([]);
  const [topics, setTopics] = useState<QuestionTopic[]>([]);
  const [outcomes, setOutcomes] = useState<OutcomeGap[]>([]);
  const [query, setQuery] = useState("");

  const roster = demo ? DEMO_ROSTER : loaded && loaded.classId === classId ? loaded.list : null;
  const error = loaded && loaded.classId === classId ? loaded.error : null;

  useEffect(() => {
    if (demo || !classId) return;
    let alive = true;
    fetchClassStudents(classId)
      .then((list) => alive && setLoaded({ classId, list, error: null }))
      .catch(
        () =>
          alive &&
          setLoaded({
            classId,
            list: [],
            error: "Chưa đọc được danh sách lớp. Nhờ thầy gán lớp này cho bạn ở trang Nhân sự.",
          }),
      );
    return () => {
      alive = false;
    };
  }, [classId, demo]);

  useEffect(() => {
    if (demo || !roster || roster.length === 0) return;
    fetchNeedsForStudents(roster.map((s) => s.id), ACTIVE_NEED_STATUSES)
      .then(setNeeds)
      .catch(() => setNeeds([]));
    fetchOutcomeGaps(roster.map((s) => s.id))
      .then(setOutcomes)
      .catch(() => setOutcomes([]));
  }, [roster, demo]);

  useEffect(() => {
    if (demo || !grade) return;
    fetchQuestionTopics(grade).then(setTopics).catch(() => setTopics([]));
  }, [grade, demo]);

  // Trong mỗi phần đang hổng, em sai đúng yêu cầu cần đạt nào — dạy cho trúng.
  const outcomesByNeed = useMemo(() => outcomeGapsByNeed(outcomes), [outcomes]);

  const needsByStudent = useMemo(() => {
    const map = new Map<string, TutoringNeed[]>();
    for (const need of needs) {
      const list = map.get(need.studentId) ?? [];
      list.push(need);
      map.set(need.studentId, list);
    }
    return map;
  }, [needs]);

  const pickedIds = new Set(students.map((s) => s.id));

  const candidates = useMemo(() => {
    const list = (roster ?? []).filter((s) => !pickedIds.has(s.id));
    const q = query.trim().toLowerCase();
    const filtered = q ? list.filter((s) => s.full_name.toLowerCase().includes(q)) : list;
    // Em đang hổng nhiều phần nhất đứng trước — đó mới là em cần gọi đi phụ đạo.
    return filtered.sort((a, b) => {
      const gap = (needsByStudent.get(b.id)?.length ?? 0) - (needsByStudent.get(a.id)?.length ?? 0);
      return gap !== 0 ? gap : a.full_name.localeCompare(b.full_name, "vi");
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [roster, query, needsByStudent, students]);

  function pick(student: ClassStudent) {
    if (students.length >= MAX_STUDENTS) return;
    onChange([...students, { id: student.id, name: student.full_name }]);
  }

  function drop(id: string) {
    onChange(students.filter((s) => s.id !== id));
    const next = { ...coverage };
    delete next[id];
    onCoverageChange(next);
  }

  function toggleTopic(studentId: string, topicId: number) {
    const current = coverage[studentId] ?? [];
    const next = current.includes(topicId)
      ? current.filter((id) => id !== topicId)
      : [...current, topicId];
    onCoverageChange({ ...coverage, [studentId]: next });
  }

  return (
    <div>
      <div className="mb-2 flex items-center justify-between">
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Các em được phụ đạo</p>
        {badge && <span className="text-xs font-bold text-amber-300">{badge}</span>}
      </div>

      {!classId && !demo ? (
        <p className="rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-400">
          Chọn lớp ở trên trước, rồi chọn em trong danh sách lớp.
        </p>
      ) : (
        <>
          {/* Em đã chọn + phần cần phụ đạo của từng em */}
          <div className="space-y-3">
            {students.map((student) => {
              const list = needsByStudent.get(student.id) ?? [];
              const ticked = coverage[student.id] ?? [];
              // Buổi phụ đạo ghi theo tầng bài (khớp khoá của mục cần phụ đạo), không
              // liệt kê từng yêu cầu cần đạt cho khỏi rối.
              const extraTopics = lessonTopics(topics).filter(
                (t) => !list.some((n) => n.topicId === t.id),
              );
              return (
                <div key={student.id} className="rounded-2xl border border-white/10 bg-white/5 p-3">
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <p className="font-semibold text-white">{student.name}</p>
                      <p className="text-xs text-slate-400">
                        {list.length > 0
                          ? `${list.length} phần đang hổng — tick phần em vừa được dạy`
                          : "Chưa có phần nào hệ thống ghi là hổng"}
                      </p>
                    </div>
                    <button
                      type="button"
                      onClick={() => drop(student.id)}
                      className="rounded-full border border-white/15 px-2.5 py-1 text-xs text-slate-300"
                    >
                      Bỏ
                    </button>
                  </div>

                  {list.length > 0 && (
                    <div className="mt-3 flex flex-wrap gap-2">
                      {list.map((need) => {
                        const on = ticked.includes(need.topicId);
                        return (
                          <button
                            key={need.id}
                            type="button"
                            onClick={() => toggleTopic(student.id, need.topicId)}
                            className={`inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-xs font-semibold transition-colors ${
                              on
                                ? "border-emerald-400/50 bg-emerald-500/15 text-emerald-200"
                                : "border-red-400/40 bg-red-500/10 text-red-200"
                            }`}
                          >
                            {on ? <Check size={13} /> : <AlertTriangle size={13} />}
                            {needLabel(need)}
                            <span className="font-normal opacity-70">
                              sai {need.wrong}/{need.total}
                            </span>
                          </button>
                        );
                      })}
                    </div>
                  )}
                  {list.length > 0 && (
                    <>
                      {list.map((need) => {
                        const detail =
                          outcomesByNeed.get(`${need.studentId}|${need.topicId}|${need.form}`) ?? [];
                        if (detail.length === 0) return null;
                        return (
                          <p key={`d-${need.id}`} className="mt-1.5 text-xs text-slate-400">
                            <span className="text-slate-500">{needLabel(need)}:</span>{" "}
                            {detail
                              .slice(0, 4)
                              .map((o) => `${o.topicName} (sai ${o.wrong}/${o.total})`)
                              .join(" · ")}
                          </p>
                        );
                      })}
                    </>
                  )}

                  {extraTopics.length > 0 && (
                    <label className="mt-3 block text-xs text-slate-400">
                      Dạy thêm phần khác
                      <select
                        value=""
                        onChange={(e) => {
                          const id = Number(e.target.value);
                          if (id) toggleTopic(student.id, id);
                        }}
                        className="mt-1 w-full rounded-xl border border-white/10 bg-panel px-3 py-2 text-sm text-white"
                      >
                        <option value="">Chọn chủ đề…</option>
                        {extraTopics.map((topic) => (
                          <option key={topic.id} value={topic.id}>
                            {ticked.includes(topic.id) ? "✓ " : ""}
                            {topic.name}
                          </option>
                        ))}
                      </select>
                    </label>
                  )}

                  {/* Chủ đề dạy thêm đã tick nhưng không nằm trong danh sách hổng */}
                  {ticked.filter((id) => !list.some((n) => n.topicId === id)).length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-2">
                      {ticked
                        .filter((id) => !list.some((n) => n.topicId === id))
                        .map((id) => (
                          <button
                            key={id}
                            type="button"
                            onClick={() => toggleTopic(student.id, id)}
                            className="inline-flex items-center gap-1.5 rounded-full border border-emerald-400/50 bg-emerald-500/15 px-3 py-1.5 text-xs font-semibold text-emerald-200"
                          >
                            <Check size={13} />
                            {topics.find((t) => t.id === id)?.name ?? `Chủ đề #${id}`}
                          </button>
                        ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Chọn thêm em */}
          {students.length < MAX_STUDENTS && (
            <div className="mt-3 rounded-2xl border border-white/10 bg-white/5 p-3">
              <div className="flex items-center gap-2 rounded-xl border border-white/10 bg-panel px-3 py-2">
                <Search size={14} className="text-slate-500" />
                <input
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Tìm tên em trong lớp…"
                  className="w-full bg-transparent text-sm text-white placeholder:text-slate-500 focus:outline-none"
                />
              </div>
              {roster === null ? (
                <p className="mt-3 flex items-center gap-2 text-sm text-slate-400">
                  <Loader2 size={14} className="animate-spin" /> Đang tải danh sách lớp…
                </p>
              ) : error ? (
                <p className="mt-3 text-sm text-amber-300">{error}</p>
              ) : candidates.length === 0 ? (
                <p className="mt-3 text-sm text-slate-400">
                  {roster.length === 0
                    ? "Lớp này chưa có em nào đăng ký tài khoản."
                    : "Không tìm thấy em nào khớp."}
                </p>
              ) : (
                <div className="mt-3 max-h-56 space-y-1.5 overflow-y-auto">
                  {candidates.map((student) => {
                    const count = needsByStudent.get(student.id)?.length ?? 0;
                    return (
                      <button
                        key={student.id}
                        type="button"
                        onClick={() => pick(student)}
                        className="flex w-full items-center justify-between gap-2 rounded-xl border border-white/10 px-3 py-2 text-left text-sm text-white hover:border-white/30"
                      >
                        <span>{student.full_name}</span>
                        {count > 0 && (
                          <span className="shrink-0 rounded-full bg-red-500/15 px-2 py-0.5 text-xs font-bold text-red-200">
                            {count} phần hổng
                          </span>
                        )}
                      </button>
                    );
                  })}
                </div>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
}
