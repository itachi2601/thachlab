"use client";

import { useEffect, useMemo, useState } from "react";
import { Copy, Search } from "lucide-react";
import { fetchCttcStudentIds, removeStudentFromClass, type ClassStudent } from "@/services/classes";
import { useToast } from "@/components/ui/Toast";
import { fetchClassExamResults, type ClassExamResult } from "@/services/class-results";
import { fetchAttendanceRecordsForSessions, fetchAttendanceSessions, type ThptAttendanceSession } from "@/services/class-attendance";
import type { LearningHistoryEntry } from "@/services/progress";
import { fetchStudentLearningHistoryFast } from "@/services/student-profile";
import ParentLinkCard from "@/components/dashboard/ParentLinkCard";
import StudentAccountCard from "@/components/dashboard/StudentAccountCard";
import ParentDigestCard from "@/components/dashboard/ParentDigestCard";
import DiagnosticAdmin from "@/components/dashboard/DiagnosticAdmin";
import ChapterMasteryRadar from "@/components/results/ChapterMasteryRadar";
import { buildCourseRadar, fetchClassQuestionActivity, fetchCurriculumMeta } from "@/services/class-insights";
import type { ChapterLessonMastery } from "@/services/mastery";
import PasswordResetCard from "@/components/dashboard/PasswordResetCard";
import StudentContactCard from "@/components/dashboard/StudentContactCard";

type ProfileTab = "hoc" | "lien-lac" | "quan-ly";
type LogView = "hoat-dong" | "diem" | "diem-danh";

function daysAgo(iso: string, nowMs: number): string {
  const d = Math.floor((nowMs - Date.parse(iso)) / 86400e3);
  return d <= 0 ? "Hôm nay" : `${d} ngày trước`;
}

const ACTIVITY_LABEL: Record<LearningHistoryEntry["activity"], string> = {
  theory: "Lý thuyết",
  practice: "Luyện tập",
  exam: "Đề kiểm tra",
};

const STATUS_LABEL: Record<string, string> = { present: "Có mặt", late: "Đi trễ", excused: "Vắng có phép", absent: "Vắng không phép" };

export default function TeacherThptStudentProfile({
  classId,
  students,
  selectedId,
  onSelect,
  onRemoved,
  adminTools = false,
}: {
  classId: number;
  students: ClassStudent[];
  selectedId: string | null;
  onSelect: (id: string) => void;
  onRemoved?: () => void;
  /** Công cụ tài khoản (mật khẩu, phụ huynh, chẩn đoán, gỡ khỏi lớp): chỉ ở /quan-tri/hoc-sinh, dashboard giáo viên không hiện. */
  adminTools?: boolean;
}) {
  const [search, setSearch] = useState("");
  const [results, setResults] = useState<ClassExamResult[]>([]);
  const [sessions, setSessions] = useState<ThptAttendanceSession[]>([]);
  const [attendanceByStudent, setAttendanceByStudent] = useState<Map<string, Map<number, string>>>(new Map());
  const [cttcIds, setCttcIds] = useState<Set<string>>(new Set());
  const [removing, setRemoving] = useState(false);
  const [history, setHistory] = useState<LearningHistoryEntry[]>([]);
  const [radar, setRadar] = useState<{ id: string; current: ChapterLessonMastery[]; prev: ChapterLessonMastery[] } | null>(null);
  // Tab/bộ lọc nhớ theo từng học sinh: đổi em thì tự về Học tập, không cần effect.
  const [view, setView] = useState<{ id: string | null; tab: ProfileTab; log: LogView }>({ id: null, tab: "hoc", log: "hoat-dong" });
  const cur = view.id === selectedId ? view : { id: selectedId, tab: "hoc" as ProfileTab, log: "hoat-dong" as LogView };
  const tab = cur.tab;
  const log = cur.log;
  const setTab = (t: ProfileTab) => setView({ ...cur, tab: t });
  const setLog = (l: LogView) => setView({ ...cur, log: l });
  const toast = useToast();

  const studentIds = useMemo(() => students.map((item) => item.id), [students]);

  useEffect(() => {
    fetchClassExamResults(studentIds).then(setResults).catch(() => setResults([]));
  }, [studentIds]);

  useEffect(() => {
    fetchCttcStudentIds(studentIds).then(setCttcIds).catch(() => setCttcIds(new Set()));
  }, [studentIds]);

  useEffect(() => {
    void (async () => {
      if (!selectedId) {
        setHistory([]);
        return;
      }
      try {
        setHistory(await fetchStudentLearningHistoryFast(selectedId));
      } catch {
        setHistory([]);
      }
    })();
  }, [selectedId]);

  useEffect(() => {
    let cancelled = false;
    fetchAttendanceSessions(classId)
      .then(async (rows) => {
        const records = await fetchAttendanceRecordsForSessions(rows.map((session) => session.id)).catch(() => []);
        if (cancelled) return;
        setSessions(rows);
        const map = new Map<string, Map<number, string>>();
        records.forEach((record) => {
          const inner = map.get(record.student_id) ?? new Map<number, string>();
          inner.set(record.session_id, record.status);
          map.set(record.student_id, inner);
        });
        setAttendanceByStudent(map);
      })
      .catch(() => undefined);
    return () => { cancelled = true; };
  }, [classId]);

  async function handleRemove() {
    if (!selected) return;
    if (!window.confirm(`Gỡ "${selected.full_name}" khỏi lớp này? Học sinh sẽ mất quyền xem nội dung/đề của lớp.`)) return;
    setRemoving(true);
    try {
      await removeStudentFromClass(selected.id, classId);
      onRemoved?.();
    } catch (error) {
      window.alert(error instanceof Error ? error.message : "Không gỡ được học sinh khỏi lớp.");
    } finally {
      setRemoving(false);
    }
  }

  const [nowMs] = useState(() => Date.now());
  const [onlyNew, setOnlyNew] = useState(false);
  const isNew = (s: { joined_at?: string | null }) => !!s.joined_at && nowMs - Date.parse(s.joined_at) < 21 * 86400e3;
  const newCount = students.filter(isNew).length;
  const visibleStudents = students
    .filter((item) => item.full_name.toLocaleLowerCase("vi-VN").includes(search.trim().toLocaleLowerCase("vi-VN")))
    .filter((item) => !onlyNew || isNew(item));
  useEffect(() => {
    if (!selectedId) return;
    let cancelled = false;
    void (async () => {
      try {
        const [rows, meta] = await Promise.all([fetchClassQuestionActivity([selectedId]), fetchCurriculumMeta()]);
        if (cancelled) return;
        setRadar({
          id: selectedId,
          current: buildCourseRadar(rows, meta),
          prev: buildCourseRadar(rows, meta, new Date(Date.now() - 30 * 86400e3)),
        });
      } catch {
        if (!cancelled) setRadar(null);
      }
    })();
    return () => { cancelled = true; };
  }, [selectedId]);
  const radarData = useMemo(
    () => (radar && radar.id === selectedId ? { current: radar.current, prev: radar.prev.some((i) => i.pct !== null) ? radar.prev : null } : null),
    [radar, selectedId],
  );

  const selected = students.find((item) => item.id === selectedId) ?? null;
  const selectedResults = results.filter((row) => row.student_id === selectedId).sort((a, b) => Date.parse(b.created_at) - Date.parse(a.created_at));
  const selectedAttendance = selectedId ? attendanceByStudent.get(selectedId) ?? new Map<number, string>() : new Map<number, string>();

  const presentCount = sessions.filter((x) => ["present", "late"].includes(selectedAttendance.get(x.id) ?? "")).length;
  const absentSessions = sessions.filter((x) => ["absent", "excused"].includes(selectedAttendance.get(x.id) ?? ""));
  const absentCount = absentSessions.length;

  const recentScores = selectedResults.slice(0, 5).map((r) => Number(r.score)).filter((n) => Number.isFinite(n));
  const avgRecent = recentScores.length ? recentScores.reduce((a, b) => a + b, 0) / recentScores.length : null;
  const lastActive = history.reduce<string | null>((m, e) => (!m || Date.parse(e.at) > Date.parse(m) ? e.at : m), null);
  const weakest = radarData?.current.filter((x) => x.isLatest !== false && x.pct !== null && x.answeredCount > 0).sort((a, b) => (a.pct ?? 0) - (b.pct ?? 0))[0] ?? null;

  return (
    <div className="grid gap-4 lg:grid-cols-[280px_1fr]">
      <aside className="rounded-2xl border border-white/10 bg-panel p-3">
        <div className="mb-3 flex items-center gap-2 rounded-xl border border-white/10 bg-panel-deep px-3 py-2">
          <Search size={15} className="text-slate-500" />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Tìm học sinh…"
            className="w-full bg-transparent text-sm text-white placeholder:text-slate-500 focus:outline-none"
          />
        </div>
        {newCount > 0 && (
          <button
            type="button"
            onClick={() => setOnlyNew((v) => !v)}
            className={`mb-3 w-full rounded-xl px-3 py-2 text-left text-sm font-bold ${onlyNew ? "bg-emerald-600 text-white" : "bg-emerald-500/15 text-emerald-300"}`}
          >
            {onlyNew ? "Đang lọc: " : ""}Mới vào 3 tuần qua · {newCount} em
          </button>
        )}
        <div className="max-h-[60vh] space-y-1 overflow-y-auto">
          {visibleStudents.map((student) => (
            <button
              key={student.id}
              onClick={() => onSelect(student.id)}
              className={`block w-full rounded-xl px-3 py-2.5 text-left text-sm ${
                selectedId === student.id ? "bg-blue-600 text-white" : "text-slate-300 hover:bg-white/5"
              }`}
            >
              <strong className="block">
                {student.full_name}
                {isNew(student) && (
                  <span className="ml-1.5 rounded-full bg-emerald-500/20 px-1.5 py-0.5 text-[12px] font-bold text-emerald-300">
                    Mới
                  </span>
                )}
                {cttcIds.has(student.id) && (
                  <span className="ml-1.5 rounded-full bg-amber-500/20 px-1.5 py-0.5 text-[12px] font-bold text-amber-300">
                    CTTC
                  </span>
                )}
              </strong>
              <small className="opacity-70">
                {student.class_name || "Chưa cập nhật lớp"}
                {isNew(student) && student.joined_at ? ` · vào ${new Date(student.joined_at).toLocaleDateString("vi-VN")}` : ""}
              </small>
            </button>
          ))}
          {!visibleStudents.length && <p className="p-3 text-center text-sm text-slate-500">Không tìm thấy học sinh.</p>}
        </div>
      </aside>

      {!selected ? (
        <div className="grid min-h-72 place-items-center rounded-2xl border border-dashed border-white/10 text-sm text-slate-500">
          Chọn một học sinh để xem hồ sơ.
        </div>
      ) : (
        <div className="space-y-4">
          <section className="rounded-2xl border border-white/10 bg-panel p-5">
            <div className="flex flex-wrap items-center gap-2">
              <h3 className="font-display text-xl font-bold text-white">{selected.full_name}</h3>
              {isNew(selected) && <span className="rounded-full bg-emerald-500/20 px-2 py-0.5 text-[12px] font-bold text-emerald-300">Mới</span>}
              {cttcIds.has(selected.id) && <span className="rounded-full bg-amber-500/20 px-2 py-0.5 text-[12px] font-bold text-amber-300">CTTC</span>}
            </div>
            <p className="mt-1 text-sm text-slate-400">
              Lớp {selected.class_name || "chưa cập nhật"}
              {selected.joined_at ? ` · vào lớp ${new Date(selected.joined_at).toLocaleDateString("vi-VN")}` : ""}
            </p>
            <dl className="mt-3 grid grid-cols-2 gap-2 sm:grid-cols-4">
              {[
                ["Điểm đề gần đây", avgRecent === null ? "—" : avgRecent.toLocaleString("vi-VN", { maximumFractionDigits: 1 })],
                ["Có mặt", sessions.length ? `${presentCount}/${sessions.length}` : "—"],
                ["Yếu nhất", weakest ? `${weakest.lessonTitle} · ${Math.round(weakest.pct ?? 0)}%` : "—"],
                ["Hoạt động gần nhất", lastActive ? daysAgo(lastActive, nowMs) : "Chưa có"],
              ].map(([label, value]) => (
                <div key={label} className="min-w-0 rounded-xl bg-white/[.04] px-3 py-2">
                  <dt className="text-[12px] font-bold uppercase tracking-wide text-slate-500">{label}</dt>
                  <dd className="mt-0.5 truncate text-sm font-bold text-white" title={value}>{value}</dd>
                </div>
              ))}
            </dl>
          </section>

          <nav className="flex gap-1 overflow-x-auto rounded-2xl border border-white/10 bg-panel p-1" aria-label="Mục hồ sơ">
            {([["hoc", "Học tập"], ["lien-lac", "Liên lạc gia đình"], ...(adminTools ? [["quan-ly", "Quản lý"]] : [])] as [ProfileTab, string][]).map(([id, label]) => (
              <button
                key={id}
                type="button"
                onClick={() => setTab(id)}
                aria-current={tab === id ? "page" : undefined}
                className={`min-h-11 shrink-0 flex-1 rounded-xl px-4 text-sm font-bold ${tab === id ? "bg-blue-600 text-white" : "text-slate-300 hover:bg-white/5"}`}
              >
                {label}
              </button>
            ))}
          </nav>

          {tab === "hoc" && (
            <>
              {adminTools && <DiagnosticAdmin key={`diag-${selected.id}`} studentId={selected.id} studentName={selected.full_name} classId={classId} />}
              {radarData && <ChapterMasteryRadar key={`radar-${selected.id}`} studentId={selected.id} courseData={radarData} />}

              <section className="rounded-2xl border border-white/10 bg-panel p-5">
                <div className="flex flex-wrap items-center gap-2">
                  <h4 className="mr-auto font-display text-lg font-bold text-white">Lịch sử</h4>
                  {([["hoat-dong", "Hoạt động"], ["diem", "Điểm đề"], ["diem-danh", "Điểm danh"]] as [LogView, string][]).map(([id, label]) => (
                    <button
                      key={id}
                      type="button"
                      onClick={() => setLog(id)}
                      className={`min-h-9 rounded-full px-3 text-xs font-bold ${log === id ? "bg-white text-slate-900" : "border border-white/15 text-slate-300"}`}
                    >
                      {label}
                    </button>
                  ))}
                </div>

                {log === "hoat-dong" && (history.length ? (
                  <div className="mt-3 max-h-80 space-y-2 overflow-y-auto">
                    {history.map((entry, i) => (
                      <div key={i} className="rounded-xl bg-white/[.02] p-3 text-sm">
                        <span className="mr-2 rounded-full border border-white/10 px-2 py-0.5 text-[12px] font-bold uppercase text-slate-400">{ACTIVITY_LABEL[entry.activity]}</span>
                        <strong className="text-white">{entry.title}</strong>
                        <small className="mt-1 block text-slate-500">{entry.detail} · {new Date(entry.at).toLocaleString("vi-VN")}</small>
                      </div>
                    ))}
                  </div>
                ) : <p className="mt-3 text-sm text-slate-500">Chưa có hoạt động học tập nào được ghi nhận.</p>)}

                {log === "diem" && (selectedResults.length ? (
                  <div className="mt-3 max-h-80 space-y-2 overflow-y-auto pr-1">
                    {selectedResults.map((row) => (
                      <div key={row.id} className="flex items-center justify-between gap-3 rounded-xl bg-white/[.02] p-3">
                        <div className="min-w-0">
                          <strong className="text-sm text-white">{row.exams?.title ?? `Đề #${row.exam_id}`}</strong>
                          <small className="mt-1 block text-slate-500">{new Date(row.created_at).toLocaleString("vi-VN")}</small>
                        </div>
                        <span className="font-mono text-lg font-bold text-white">{Number(row.score).toLocaleString("vi-VN")}</span>
                      </div>
                    ))}
                  </div>
                ) : <p className="mt-3 text-sm text-slate-500">Chưa làm bài kiểm tra nào.</p>)}

                {log === "diem-danh" && (sessions.length ? (
                  <div className="mt-3">
                    <p className="text-sm text-slate-300">Có mặt {presentCount}/{sessions.length} buổi{absentCount > 0 && <> · vắng {absentCount}</>}</p>
                    {absentSessions.length > 0 && (
                      <ul className="mt-2 space-y-1 text-sm text-slate-400">
                        {absentSessions.map((session) => (
                          <li key={session.id}>{STATUS_LABEL[selectedAttendance.get(session.id) ?? ""]} · {session.title} · {new Date(session.starts_at).toLocaleDateString("vi-VN")}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                ) : <p className="mt-3 text-sm text-slate-500">Lớp chưa có buổi điểm danh nào.</p>)}
              </section>
            </>
          )}

          {tab === "lien-lac" && (
            <>
              <StudentContactCard key={`contact-${selected.id}`} studentId={selected.id} />
              {adminTools && (
                <>
                  <ParentLinkCard key={selected.id} studentId={selected.id} studentName={selected.full_name} />
                  <ParentDigestCard key={`digest-${selected.id}`} studentId={selected.id} studentName={selected.full_name} />
                </>
              )}
            </>
          )}

          {tab === "quan-ly" && adminTools && (
            <>
              <StudentAccountCard key={`acc-${selected.id}`} studentId={selected.id} />
              {selected.student_code && (
                <button
                  type="button"
                  onClick={async () => {
                    try {
                      await navigator.clipboard.writeText(selected.student_code ?? "");
                      toast("success", "Đã chép tài khoản đăng nhập.");
                    } catch {
                      toast("error", "Trình duyệt không cho chép tự động — bôi đen rồi chép tay nhé.");
                    }
                  }}
                  className="inline-flex min-h-11 items-center gap-1.5 rounded-xl border border-white/10 px-4 text-sm font-semibold text-slate-300 hover:text-white"
                >
                  Chép tài khoản đăng nhập: <span className="font-mono text-white">{selected.student_code}</span> <Copy size={14} />
                </button>
              )}
              <PasswordResetCard key={`pw-${selected.id}`} studentId={selected.id} studentName={selected.full_name} />
              <section className="rounded-2xl border border-red-500/25 bg-red-500/[.04] p-5">
                <h4 className="font-display text-lg font-bold text-red-200">Khu vực nguy hiểm</h4>
                {cttcIds.has(selected.id) && (
                  <p className="mt-2 text-xs text-amber-200">
                    Em này cũng có tài khoản CTTC (CNC/tiện phay) — có thể đã bị gán nhầm vào lớp THPT này.
                  </p>
                )}
                <button
                  type="button"
                  onClick={handleRemove}
                  disabled={removing}
                  className="mt-3 min-h-11 rounded-xl border border-red-500/40 px-4 text-sm font-bold text-red-300 hover:bg-red-500/10 disabled:opacity-50"
                >
                  {removing ? "Đang gỡ…" : "Xóa khỏi lớp"}
                </button>
              </section>
            </>
          )}
        </div>
      )}
    </div>
  );
}
