"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { BookOpen, Check, RefreshCw, Users } from "lucide-react";
import type { ClassStudent } from "@/services/classes";
import { useAuth } from "@/components/auth/AuthProvider";
import { useToast } from "@/components/ui/Toast";
import { fetchOutcomeGaps, outcomeGapsByNeed, type OutcomeGap } from "@/services/analytics";
import {
  ACTIVE_NEED_STATUSES,
  NEED_STATUS_LABEL,
  fetchCoverageForStudents,
  fetchNeedsForStudents,
  needLabel,
  refreshClassNeeds,
  updateNeed,
  type NeedStatus,
  type TutoringCoverage,
  type TutoringNeed,
} from "@/services/tutoring";

const STATUS_TONE: Record<NeedStatus, string> = {
  open: "border-red-500/40 bg-red-500/10 text-red-200",
  assigned: "border-amber-500/40 bg-amber-500/10 text-amber-200",
  tutored: "border-blue-500/40 bg-blue-500/10 text-blue-200",
  cleared: "border-emerald-500/40 bg-emerald-500/10 text-emerald-200",
  dismissed: "border-white/15 bg-white/5 text-slate-400",
};

function shortDate(iso: string | null) {
  if (!iso) return "";
  return new Date(iso).toLocaleDateString("vi-VN", { day: "2-digit", month: "2-digit" });
}

/**
 * Tab "Phụ đạo" của giáo viên: mỗi em đang hổng phần nào, phần nào đã được trợ giảng
 * dạy (ngày nào, ai dạy), phần nào em đã làm đúng lại. Số liệu sinh tự động từ
 * kết quả từng câu — xem docs/supabase-migration-tutoring-needs.sql.
 */
export default function TeacherThptTutoring({
  classId,
  students,
}: {
  classId: number;
  students: ClassStudent[];
}) {
  const { profile } = useAuth();
  const toast = useToast();
  const [needs, setNeeds] = useState<TutoringNeed[] | null>(null);
  const [coverage, setCoverage] = useState<TutoringCoverage[]>([]);
  const [outcomes, setOutcomes] = useState<OutcomeGap[]>([]);
  const [filter, setFilter] = useState<"active" | "all">("active");
  const [busy, setBusy] = useState(false);

  const studentIds = useMemo(() => students.map((s) => s.id), [students]);
  const nameById = useMemo(() => new Map(students.map((s) => [s.id, s.full_name])), [students]);

  const load = useCallback(() => {
    // studentIds rỗng thì hai hàm dưới tự trả về [] — đừng setState thẳng trong effect.
    fetchNeedsForStudents(studentIds, filter === "active" ? ACTIVE_NEED_STATUSES : [])
      .then(setNeeds)
      .catch(() => setNeeds([]));
    fetchCoverageForStudents(studentIds).then(setCoverage).catch(() => setCoverage([]));
    fetchOutcomeGaps(studentIds).then(setOutcomes).catch(() => setOutcomes([]));
  }, [studentIds, filter]);
  useEffect(load, [load]);

  // Em còn sai đúng yêu cầu cần đạt nào trong phần đó — để buổi phụ đạo dạy trúng chỗ.
  const outcomesByNeed = useMemo(() => outcomeGapsByNeed(outcomes), [outcomes]);

  // Lịch sử đã dạy, tra theo "em + chủ đề".
  const taughtByKey = useMemo(() => {
    const map = new Map<string, TutoringCoverage>();
    for (const item of coverage) {
      const key = `${item.studentId}|${item.topicId}`;
      if (!map.has(key)) map.set(key, item); // coverage đã sắp mới nhất trước
    }
    return map;
  }, [coverage]);

  const byStudent = useMemo(() => {
    const map = new Map<string, TutoringNeed[]>();
    for (const need of needs ?? []) {
      const list = map.get(need.studentId) ?? [];
      list.push(need);
      map.set(need.studentId, list);
    }
    return [...map.entries()]
      .map(([id, list]) => ({ id, name: nameById.get(id) ?? "(không rõ)", list }))
      .sort((a, b) => {
        const open = (x: TutoringNeed[]) => x.filter((n) => n.status === "open").length;
        return open(b.list) - open(a.list) || a.name.localeCompare(b.name, "vi");
      });
  }, [needs, nameById]);

  // Phần cả lớp yếu nhất — để thầy xếp một buổi phụ đạo chung thay vì gọi từng em.
  const hotTopics = useMemo(() => {
    const map = new Map<string, { label: string; students: number }>();
    for (const need of needs ?? []) {
      if (!ACTIVE_NEED_STATUSES.includes(need.status)) continue;
      const key = needLabel(need);
      const entry = map.get(key) ?? { label: key, students: 0 };
      entry.students += 1;
      map.set(key, entry);
    }
    return [...map.values()].sort((a, b) => b.students - a.students).slice(0, 5);
  }, [needs]);

  const counts = useMemo(() => {
    const list = needs ?? [];
    return {
      open: list.filter((n) => n.status === "open").length,
      tutored: list.filter((n) => n.status === "tutored").length,
      cleared: list.filter((n) => n.status === "cleared").length,
      students: new Set(list.filter((n) => ACTIVE_NEED_STATUSES.includes(n.status)).map((n) => n.studentId)).size,
    };
  }, [needs]);

  async function rebuild() {
    setBusy(true);
    try {
      const n = await refreshClassNeeds(classId);
      toast("success", `Đã rà lại ${n} em theo kết quả bài kiểm tra gần nhất.`);
      load();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa rà lại được.");
    } finally {
      setBusy(false);
    }
  }

  async function setStatus(need: TutoringNeed, status: NeedStatus) {
    try {
      await updateNeed(need.id, { status, assignedTo: status === "assigned" ? profile?.id ?? null : need.assignedTo });
      load();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa cập nhật được.");
    }
  }

  return (
    <div className="space-y-5">
      <section className="rounded-3xl border border-white/10 bg-[#0B1020] p-6">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <h2 className="font-display text-xl font-bold text-white">Phụ đạo theo chủ đề</h2>
            <p className="mt-1 text-sm text-slate-400">
              Sinh tự động từ 2 bài gần nhất của mỗi em: sai từ một nửa số câu của một phần
              (tối thiểu 3 câu) thì phần đó vào danh sách cần phụ đạo. Trợ giảng tick phần đã
              dạy khi ghi buổi; em làm đúng lại ở bài sau thì mục tự đóng.
            </p>
          </div>
          <button
            type="button"
            onClick={rebuild}
            disabled={busy}
            className="inline-flex items-center gap-2 rounded-full border border-white/15 px-4 py-2 text-sm font-semibold text-slate-200 disabled:opacity-40"
          >
            <RefreshCw size={14} className={busy ? "animate-spin" : ""} /> Rà lại cả lớp
          </button>
        </div>

        <div className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-4">
          <Metric label="Em cần phụ đạo" value={counts.students} tone="text-red-300" />
          <Metric label="Phần chưa ai nhận" value={counts.open} tone="text-amber-300" />
          <Metric label="Phần đã dạy" value={counts.tutored} tone="text-blue-300" />
          <Metric label="Phần đã khắc phục" value={counts.cleared} tone="text-emerald-300" />
        </div>
      </section>

      {hotTopics.length > 0 && (
        <section className="rounded-3xl border border-white/10 bg-[#0B1020] p-6">
          <h3 className="flex items-center gap-2 font-semibold text-white">
            <BookOpen size={16} className="text-sky-300" /> Nên phụ đạo chung phần nào
          </h3>
          <div className="mt-3 flex flex-wrap gap-2">
            {hotTopics.map((topic) => (
              <span
                key={topic.label}
                className="inline-flex items-center gap-2 rounded-full border border-sky-400/40 bg-sky-500/10 px-3 py-1.5 text-sm text-sky-100"
              >
                {topic.label}
                <span className="inline-flex items-center gap-1 text-xs font-bold text-sky-300">
                  <Users size={12} />
                  {topic.students}
                </span>
              </span>
            ))}
          </div>
        </section>
      )}

      <div className="flex gap-2">
        {(["active", "all"] as const).map((id) => (
          <button
            key={id}
            type="button"
            onClick={() => setFilter(id)}
            className={`rounded-full border px-4 py-2 text-sm font-semibold ${
              filter === id ? "border-blue-400/50 bg-blue-500/15 text-blue-200" : "border-white/10 text-slate-400"
            }`}
          >
            {id === "active" ? "Còn phải làm" : "Tất cả"}
          </button>
        ))}
      </div>

      {needs === null ? (
        <p className="text-sm text-slate-400">Đang tải…</p>
      ) : byStudent.length === 0 ? (
        <p className="rounded-2xl border border-dashed border-white/10 p-10 text-center text-sm text-slate-500">
          Chưa có mục phụ đạo nào. Đề phải được gắn chủ đề cho từng câu thì hệ thống mới
          chỉ ra được em hổng phần nào — gắn ở trang Quản trị → Chủ đề, rồi bấm “Rà lại cả lớp”.
        </p>
      ) : (
        <div className="space-y-3">
          {byStudent.map((student) => (
            <article key={student.id} className="rounded-2xl border border-white/10 bg-[#0B1020] p-4">
              <h3 className="font-semibold text-white">{student.name}</h3>
              <div className="mt-3 space-y-2">
                {student.list.map((need) => {
                  const taught = taughtByKey.get(`${need.studentId}|${need.topicId}`);
                  const detail =
                    outcomesByNeed.get(`${need.studentId}|${need.topicId}|${need.form}`) ?? [];
                  return (
                    <div
                      key={need.id}
                      className="rounded-xl border border-white/10 px-3 py-2"
                    >
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="text-sm text-white">{needLabel(need)}</span>
                      <span className="text-xs text-slate-500">
                        sai {need.wrong}/{need.total}
                      </span>
                      <span className={`rounded-full border px-2.5 py-0.5 text-xs font-bold ${STATUS_TONE[need.status]}`}>
                        {NEED_STATUS_LABEL[need.status]}
                      </span>
                      {taught && (
                        <span className="inline-flex items-center gap-1 text-xs text-blue-300">
                          <Check size={12} />
                          {shortDate(taught.workDate ?? taught.createdAt)}
                          {taught.assistantName ? ` · ${taught.assistantName}` : ""}
                        </span>
                      )}
                      {need.note && <span className="text-xs text-slate-500">— {need.note}</span>}
                      <span className="ml-auto flex gap-1.5">
                        {need.status !== "cleared" && (
                          <button
                            type="button"
                            onClick={() => setStatus(need, "cleared")}
                            className="rounded-full border border-emerald-400/40 px-2.5 py-1 text-xs font-semibold text-emerald-200"
                          >
                            Đã ổn
                          </button>
                        )}
                        {need.status !== "dismissed" && (
                          <button
                            type="button"
                            onClick={() => setStatus(need, "dismissed")}
                            className="rounded-full border border-white/15 px-2.5 py-1 text-xs font-semibold text-slate-300"
                          >
                            Bỏ qua
                          </button>
                        )}
                      </span>
                    </div>
                      {detail.length > 0 && (
                        <p className="mt-1.5 text-xs text-slate-400">
                          Hổng:{" "}
                          {detail
                            .slice(0, 4)
                            .map((o) => `${o.topicName} (${o.wrong}/${o.total})`)
                            .join(" · ")}
                        </p>
                      )}
                    </div>
                  );
                })}
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}

function Metric({ label, value, tone }: { label: string; value: number; tone: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">{label}</p>
      <p className={`mt-1 font-mono text-2xl font-bold tabular-nums ${tone}`}>{value}</p>
    </div>
  );
}
