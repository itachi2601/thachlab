"use client";

// Bảng điều hành giảng viên CNC theo nhịp lớp đảo ngược: chọn buổi → đọc 3 chặng
// Tối trước (quiz chuẩn bị: chữa câu nào, ai chưa làm) → Trong buổi (điểm danh, chia trạm, ai được cắt thật,
// việc chờ duyệt) → Sau buổi (cổng G1–G5 cả lớp, sinh viên cần kèm).
// Thay tab "Tổng quan" cũ (chỉ số % tiến độ + biểu đồ chất lượng) — số liệu ở đây đều trả lời câu
// "buổi này tôi làm gì với ai". Phần hiển thị thuần là FlipBoardView (dùng lại ở /dev/cnc-bang-buoi).
import { useEffect, useMemo, useState } from "react";
import {
  ArrowRight,
  BookOpen,
  CalendarCheck,
  CheckCircle2,
  ClipboardList,
  FileText,
  Hourglass,
  LockKeyhole,
  MessageCircleQuestion,
  Moon,
  Radio,
  RefreshCw,
  ShieldAlert,
  Target,
  Wrench,
} from "lucide-react";
import type { CncQuizQuestion } from "@/services/cnc-exam-bank";
import { fetchCourseCompetencyPermissions, type CompetencyPermission } from "@/services/cnc-competencies";
import { fetchAttendanceRecordsForSessions, fetchAttendanceSessions } from "@/services/course-attendance";
import {
  CNC_FLIP_LESSONS,
  CNC_FLIP_SESSIONS,
  buildFlipBoard,
  cncFlipLessonLabel,
  inferCncFlipSession,
  type FlipBoard,
  type FlipStudent,
} from "@/services/cnc-flip";
import { cncLessonHref, cncSessionSheetHref, fetchCncPrepBanks, fetchCourseCncPrepAll, type CncPrepResponse } from "@/services/cnc-prep";
import { fetchOpenCncLessons, updateOpenCncLessons } from "@/services/course-lesson-release";
import { CncPrepSessionResults } from "@/components/dashboard/CncPrepResultsPanel";

type DashboardTab = "overview" | "grades" | "competencies" | "attendance";
export type FlipToday = { present: number; late: number; absent: number; open: boolean } | null;

type Loaded = {
  courseId: number;
  permissions: CompetencyPermission[];
  openLessons: string[];
  banks: Record<number, CncQuizQuestion[]>;
  prepRows: CncPrepResponse[];
  sessionDates: string[];
  today: FlipToday;
  savedNo: number | null;
};

const localDate = () => {
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")}`;
};
const storageKey = (courseId: number) => `cnc-flip-buoi-${courseId}`;
function readSavedNo(courseId: number) {
  try {
    const n = Number(window.localStorage.getItem(storageKey(courseId)));
    return CNC_FLIP_SESSIONS.some((item) => item.no === n) ? n : null;
  } catch {
    return null;
  }
}

export default function TeacherFlipBoard({
  courseId,
  students,
  onOpenTab,
  onOpenStudent,
  onOpenLiveExam,
}: {
  courseId: number;
  students: FlipStudent[];
  onOpenTab: (tab: DashboardTab) => void;
  onOpenStudent: (id: string) => void;
  onOpenLiveExam?: () => void;
}) {
  const [data, setData] = useState<Loaded | null>(null);
  const [tick, setTick] = useState(0);
  const [loadedKey, setLoadedKey] = useState("");
  const [picked, setPicked] = useState<{ courseId: number; no: number } | null>(null);
  const [releaseBusy, setReleaseBusy] = useState(false);
  const [releaseError, setReleaseError] = useState("");
  const requestKey = `${courseId}-${tick}`;

  useEffect(() => {
    let cancelled = false;
    const key = `${courseId}-${tick}`;
    const today = localDate();
    // Từng nguồn tự lùi về rỗng: bảng vẫn dùng được khi một migration chưa chạy.
    Promise.all([
      fetchAttendanceSessions(courseId).catch(() => []),
      fetchCourseCompetencyPermissions(courseId).catch(() => []),
      fetchOpenCncLessons(courseId).catch(() => ["lesson-1"]),
      fetchCncPrepBanks().catch(() => ({}) as Record<number, CncQuizQuestion[]>),
      fetchCourseCncPrepAll(courseId).catch(() => []),
    ]).then(async ([sessions, permissions, released, banks, prepRows]) => {
      const todaySessions = sessions.filter((item) => item.session_date === today);
      const todayRows = await fetchAttendanceRecordsForSessions(todaySessions.map((item) => item.id)).catch(() => []);
      if (cancelled) return;
      setData({
        courseId,
        permissions,
        openLessons: released.length ? released : ["lesson-1"],
        banks,
        prepRows,
        sessionDates: sessions.map((item) => item.session_date),
        today: todaySessions.length
          ? {
              present: todayRows.filter((row) => row.status === "present").length,
              late: todayRows.filter((row) => row.status === "late").length,
              absent: todayRows.filter((row) => row.status === "absent").length,
              open: todaySessions.some((item) => item.status === "open"),
            }
          : null,
        savedNo: readSavedNo(courseId),
      });
      setLoadedKey(key);
    });
    return () => {
      cancelled = true;
    };
  }, [courseId, tick]);

  const ready = data?.courseId === courseId ? data : null;
  const sessionNo =
    (picked?.courseId === courseId ? picked.no : null) ??
    ready?.savedNo ??
    (ready ? inferCncFlipSession(ready.sessionDates, localDate()) : 1);

  const board = useMemo(
    () =>
      buildFlipBoard({
        students,
        permissions: ready?.permissions ?? [],
        openLessons: ready?.openLessons ?? ["lesson-1"],
        banks: ready?.banks ?? {},
        prepRows: ready?.prepRows ?? [],
        sessionNo,
      }),
    [students, ready, sessionNo],
  );

  if (!ready) return <div className="min-h-[24rem] animate-pulse rounded-2xl bg-surface-2" aria-hidden />;

  const toggleLesson = async (lessonId: string) => {
    const next = ready.openLessons.includes(lessonId) ? ready.openLessons.filter((id) => id !== lessonId) : [...ready.openLessons, lessonId];
    setReleaseBusy(true);
    setReleaseError("");
    try {
      await updateOpenCncLessons(courseId, next);
      setData((current) => (current ? { ...current, openLessons: next } : current));
    } catch {
      setReleaseError("Chưa lưu được phạm vi bài mở. Thử lại sau ít phút.");
    } finally {
      setReleaseBusy(false);
    }
  };

  return (
    <FlipBoardView
      board={board}
      students={students}
      taughtCount={new Set(ready.sessionDates.filter((date) => date <= localDate())).size}
      today={ready.today}
      openLessons={ready.openLessons}
      releaseBusy={releaseBusy}
      releaseError={releaseError}
      loading={loadedKey !== requestKey}
      onPickSession={(no) => {
        setPicked({ courseId, no });
        try {
          window.localStorage.setItem(storageKey(courseId), String(no));
        } catch {
          /* chế độ riêng tư: chỉ không nhớ buổi */
        }
      }}
      onToggleLesson={toggleLesson}
      onReload={() => setTick((n) => n + 1)}
      onOpenTab={onOpenTab}
      onOpenStudent={onOpenStudent}
      onOpenLiveExam={onOpenLiveExam}
    />
  );
}

const letter = (index: number) => String.fromCharCode(65 + index);

export function FlipBoardView({
  board,
  students,
  taughtCount,
  today,
  openLessons,
  releaseBusy,
  releaseError,
  loading,
  onPickSession,
  onToggleLesson,
  onReload,
  onOpenTab,
  onOpenStudent,
  onOpenLiveExam,
}: {
  board: FlipBoard;
  students: FlipStudent[];
  taughtCount: number;
  today: FlipToday;
  openLessons: string[];
  releaseBusy: boolean;
  releaseError: string;
  loading: boolean;
  onPickSession: (no: number) => void;
  onToggleLesson: (lessonId: string) => void;
  onReload: () => void;
  onOpenTab: (tab: DashboardTab) => void;
  onOpenStudent: (id: string) => void;
  onOpenLiveExam?: () => void;
}) {
  const { session, prep } = board;
  const total = students.length;
  const lessonOpen = !session.lessonId || openLessons.includes(session.lessonId);
  const done = prep.ready.length + prep.weak.length;
  const focusGate = board.gates.find((item) => item.gate.id === session.gate);
  const startAtWinnc = [...prep.weak, ...prep.none];

  return (
    <div className={`space-y-4 ${loading ? "opacity-70" : ""}`}>
      {/* Chọn buổi: lộ đủ 12 buổi, không cuộn ngang */}
      <section className="rounded-2xl border border-line bg-panel p-4 sm:p-5">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h3 className="font-display text-lg font-bold text-ink">12 buổi lớp đảo ngược</h3>
          <div className="flex items-center gap-3">
            <span className="text-xs text-muted">Đã dạy {Math.min(taughtCount, 12)}/12 buổi</span>
            <button
              type="button"
              onClick={onReload}
              className="inline-flex min-h-[40px] items-center gap-1.5 rounded-xl border border-line px-3 text-xs font-semibold text-muted hover:text-primary"
            >
              <RefreshCw size={14} aria-hidden /> Tải lại
            </button>
          </div>
        </div>
        <ol className="mt-3 grid grid-cols-6 gap-1.5 lg:grid-cols-12">
          {CNC_FLIP_SESSIONS.map((item) => {
            const active = item.no === session.no;
            const prepCount = board.prepDone[item.no];
            return (
              <li key={item.no}>
                <button
                  type="button"
                  onClick={() => onPickSession(item.no)}
                  aria-current={active ? "step" : undefined}
                  title={`Buổi ${item.no} · ${item.title}`}
                  className={`flex min-h-[52px] w-full flex-col items-center justify-center rounded-xl border px-1 py-1.5 text-center transition ${
                    active
                      ? "border-primary bg-primary text-white"
                      : item.no <= taughtCount
                        ? "border-line bg-surface-2 text-ink hover:border-primary"
                        : "border-line text-muted hover:border-primary"
                  }`}
                >
                  <strong className="text-sm leading-tight">
                    {item.no}
                    {item.gateCheck && <span className="ml-0.5 text-[11px] font-semibold">·{item.gate}</span>}
                  </strong>
                  <small className={`text-[11px] leading-tight ${active ? "text-white/85" : "text-muted"}`}>
                    {prepCount === undefined ? (item.hasPrep ? "chưa đăng" : "—") : `${prepCount}/${total}`}
                  </small>
                </button>
              </li>
            );
          })}
        </ol>
        <p className="mt-2 text-xs text-muted">Số nhỏ dưới mỗi buổi: sinh viên đã làm câu chuẩn bị. Buổi có nhãn G là buổi chốt cổng năng lực.</p>

        <div className="mt-4 flex flex-wrap items-start justify-between gap-3 border-t border-line pt-4">
          <div className="min-w-0">
            <p className="text-xs font-bold uppercase tracking-wide text-primary">Buổi {session.no}</p>
            <h4 className="font-display text-xl font-bold text-ink">{session.title}</h4>
            <p className="mt-1 text-sm text-muted">
              {cncFlipLessonLabel(session.lessonId)} · hướng tới cổng {session.gate}
              {session.gateCheck ? " (chốt cuối buổi)" : ""}
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <a href={cncSessionSheetHref(session.no)} target="_blank" rel="noreferrer" className={linkBtn}>
              <FileText size={15} aria-hidden /> Phiếu buổi
            </a>
            {session.lessonId && (
              <a href={cncLessonHref(session.lessonId, session.anchor)} target="_blank" rel="noreferrer" className={linkBtn}>
                <BookOpen size={15} aria-hidden /> Mở bài
              </a>
            )}
            {session.lessonId &&
              (lessonOpen ? (
                <span className="inline-flex min-h-[40px] items-center gap-1.5 rounded-xl bg-ok/10 px-3 text-xs font-bold text-ok">
                  <CheckCircle2 size={15} aria-hidden /> Bài đã mở cho lớp
                </span>
              ) : (
                <button
                  type="button"
                  disabled={releaseBusy}
                  onClick={() => session.lessonId && onToggleLesson(session.lessonId)}
                  className="inline-flex min-h-[40px] items-center gap-1.5 rounded-xl bg-primary px-3 text-xs font-bold text-white disabled:opacity-50"
                >
                  <LockKeyhole size={15} aria-hidden /> Mở bài này cho lớp
                </button>
              ))}
          </div>
        </div>
        {releaseError && <p className="mt-3 rounded-xl bg-danger/10 p-3 text-xs text-danger">{releaseError}</p>}
      </section>

      <div className="grid gap-4 xl:grid-cols-[1.25fr_1fr_1fr]">
        {/* 1 — TỐI TRƯỚC */}
        <Phase step={1} icon={<Moon size={17} aria-hidden />} title="Tối trước" hint={session.read ? `Sinh viên đọc ${session.read} (≤ 20 phút) + 5 câu` : "Buổi này không có gói đọc trước"}>
          {!session.hasPrep ? (
            <Empty>Buổi 1 giảng viên dạy trực tiếp nội quy, máy, điểm chuẩn. Không có câu chuẩn bị.</Empty>
          ) : !prep.available ? (
            <Empty>
              Chưa đăng câu chuẩn bị cho buổi {session.no}.{" "}
              <a href="/quan-tri/cnc-dang-de" className="font-semibold text-primary underline">
                Đăng 5 câu vào ngân hàng “Chuẩn bị buổi {session.no}”
              </a>
            </Empty>
          ) : (
            <>
              <div className="grid grid-cols-3 gap-2 text-center">
                <Stat value={`${done}/${total}`} label="đã làm" />
                <Stat value={done ? `${Math.round(prep.avg * 100)}%` : "—"} label="đúng lượt đầu" />
                <Stat value={String(prep.ready.length)} label={`đạt ${prep.pass}/${prep.questions.length}`} />
              </div>

              <div>
                <h5 className={subhead}>
                  <Target size={15} aria-hidden /> Chữa đầu giờ (15 phút)
                </h5>
                {prep.ranked.length === 0 ? (
                  <p className="mt-2 text-sm text-muted">Chưa có lượt làm nào. Nhắc lớp làm trước giờ học.</p>
                ) : prep.ranked[0].wrong === 0 ? (
                  <p className="mt-2 text-sm text-ok">Lớp không sai câu nào ở lượt đầu. Vào thẳng phần dạy trên máy.</p>
                ) : (
                  <ol className="mt-2 space-y-2">
                    {prep.ranked
                      .filter((stat) => stat.wrong > 0)
                      .slice(0, 2)
                      .map((stat) => {
                        const question = prep.questions[stat.index];
                        const topWrong = stat.picks
                          .map((n, i) => ({ n, i }))
                          .filter((pick) => pick.i !== stat.correctIndex && pick.n > 0)
                          .sort((a, b) => b.n - a.n)[0];
                        return (
                          <li key={stat.index} className="rounded-xl border border-line bg-surface-2 p-3">
                            <div className="flex items-start justify-between gap-3">
                              <p className="text-sm text-ink">
                                <strong>Câu {stat.index + 1}.</strong> {stat.question}
                              </p>
                              <span className="shrink-0 rounded-full bg-danger/10 px-2 py-0.5 text-xs font-bold text-danger">
                                sai {stat.wrong}/{stat.answered}
                              </span>
                            </div>
                            {question && (
                              <p className="mt-1.5 text-xs text-muted">
                                Đúng: <strong className="text-ink">{letter(stat.correctIndex)}. {question.options[stat.correctIndex]}</strong>
                                {topWrong && (
                                  <>
                                    <br />
                                    Nhầm nhiều nhất ({topWrong.n} em): {letter(topWrong.i)}. {question.options[topWrong.i]}
                                  </>
                                )}
                              </p>
                            )}
                          </li>
                        );
                      })}
                  </ol>
                )}
              </div>

              <div>
                <h5 className={subhead}>
                  <MessageCircleQuestion size={15} aria-hidden /> Chỗ em chưa rõ ({prep.notes.length})
                </h5>
                {prep.notes.length ? (
                  <ul className="mt-2 max-h-56 space-y-2 overflow-y-auto">
                    {prep.notes.map((note, index) => (
                      <li key={`${note.studentId}-${index}`} className="rounded-xl border border-line p-3 text-sm text-ink">
                        <span className="text-xs font-semibold text-muted">{note.name}</span>
                        <p className="mt-0.5 whitespace-pre-line">{note.text}</p>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="mt-2 text-sm text-muted">Chưa có câu hỏi nào gửi lên.</p>
                )}
              </div>

              {prep.none.length > 0 && (
                <div>
                  <h5 className={subhead}>Chưa làm ({prep.none.length})</h5>
                  <NameChips items={prep.none} onOpen={onOpenStudent} />
                </div>
              )}

              <details className="rounded-xl border border-line">
                <summary className="flex min-h-[44px] cursor-pointer items-center px-3 text-sm font-semibold text-primary">Xem đủ {prep.questions.length} câu và phương án lớp chọn</summary>
                <div className="px-3 pb-3">
                  <CncPrepSessionResults questions={prep.questions} rows={prep.rows} students={students} />
                </div>
              </details>
            </>
          )}
        </Phase>

        {/* 2 — TRONG BUỔI */}
        <Phase step={2} icon={<Wrench size={17} aria-hidden />} title="Trong buổi" hint="300 phút: chữa 15′ · dạy trên máy ≤ 90′ · hai trạm đổi lượt">
          <button type="button" onClick={() => onOpenTab("attendance")} className={rowBtn}>
            <span className="flex items-center gap-3">
              <CalendarCheck size={18} className="shrink-0 text-primary" aria-hidden />
              <span>
                <strong className="block text-sm text-ink">Điểm danh + gán máy</strong>
                <small className="text-xs text-muted">
                  {today
                    ? `Hôm nay: ${today.present + today.late}/${total} có mặt${today.late ? ` (${today.late} muộn)` : ""}${today.absent ? ` · ${today.absent} vắng` : ""}${today.open ? " · ca đang mở" : ""}`
                    : "Hôm nay chưa mở ca điểm danh"}
                </small>
              </span>
            </span>
            <ArrowRight size={16} className="shrink-0 text-muted" aria-hidden />
          </button>

          <div className="grid grid-cols-2 gap-2">
            <Station title="Trạm máy thật" task={session.machine} />
            <Station title="Trạm WinNC" task={session.winnc} />
          </div>

          {prep.available && (
            <div>
              <h5 className={subhead}>Gợi ý lượt đầu</h5>
              <p className="mt-1 text-xs text-muted">Em đã chuẩn bị vào máy thật trước; em chưa đạt ngồi WinNC, đọc lại gói rồi đổi trạm.</p>
              <div className="mt-2 space-y-2">
                <Group tone="ok" label={`Máy thật trước · ${prep.ready.length} em`} items={prep.ready} onOpen={onOpenStudent} empty="Chưa em nào đạt câu chuẩn bị." />
                <Group
                  tone="warn"
                  label={`WinNC trước · ${startAtWinnc.length} em`}
                  items={startAtWinnc.map((item) => ({ ...item, name: "best" in item ? `${item.name} (${item.best}/${prep.questions.length})` : item.name }))}
                  onOpen={onOpenStudent}
                  empty="Cả lớp đã đạt câu chuẩn bị."
                />
              </div>
            </div>
          )}

          {session.cutNeeds.length > 0 && (
            <div className={`rounded-xl border p-3 ${board.cutBlocked.length ? "border-danger/40 bg-danger/5" : "border-ok/30 bg-ok/5"}`}>
              <h5 className={`flex items-center gap-1.5 text-sm font-bold ${board.cutBlocked.length ? "text-danger" : "text-ok"}`}>
                <ShieldAlert size={15} aria-hidden />
                {board.cutBlocked.length ? `Chưa được cắt thật · ${board.cutBlocked.length} em` : "Cả lớp đủ quyền cắt thật"}
              </h5>
              {board.cutBlocked.length > 0 && (
                <ul className="mt-2 max-h-48 space-y-1 overflow-y-auto">
                  {board.cutBlocked.map((item) => (
                    <li key={item.id}>
                      <button type="button" onClick={() => onOpenStudent(item.id)} className="min-h-[36px] w-full rounded-lg px-2 text-left text-sm text-ink hover:bg-surface-2">
                        <strong>{item.name}</strong> <span className="text-xs text-muted">thiếu {item.missing.join(", ")}</span>
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}

          <button type="button" onClick={() => onOpenTab("competencies")} className={rowBtn}>
            <span className="flex items-center gap-3">
              <Hourglass size={18} className={`shrink-0 ${board.waiting.length ? "text-warn" : "text-muted"}`} aria-hidden />
              <span>
                <strong className="block text-sm text-ink">Chờ thầy duyệt tại xưởng · {board.waiting.length} em</strong>
                <small className="text-xs text-muted">
                  {board.waiting.length
                    ? board.waiting
                        .slice(0, 4)
                        .map((item) => item.name)
                        .join(", ") + (board.waiting.length > 4 ? "…" : "")
                    : "Chấm checklist, rubric, cấp quyền đứng máy"}
                </small>
              </span>
            </span>
            <ArrowRight size={16} className="shrink-0 text-muted" aria-hidden />
          </button>

          {onOpenLiveExam && (
            <button type="button" onClick={onOpenLiveExam} className={rowBtn}>
              <span className="flex items-center gap-3">
                <Radio size={18} className="shrink-0 text-primary" aria-hidden />
                <span>
                  <strong className="block text-sm text-ink">Phòng thi trực tiếp</strong>
                  <small className="text-xs text-muted">Bảng xếp hạng bài vận hành máy phay, chiếu toàn màn hình</small>
                </span>
              </span>
              <ArrowRight size={16} className="shrink-0 text-muted" aria-hidden />
            </button>
          )}
        </Phase>

        {/* 3 — SAU BUỔI */}
        <Phase step={3} icon={<ClipboardList size={17} aria-hidden />} title="Sau buổi" hint="Lớp qua cổng nào, ai cần kèm trước buổi kế">
          <div>
            <h5 className={subhead}>Năm cổng năng lực</h5>
            <ul className="mt-2 space-y-2">
              {board.gates.map(({ gate, byStatus }) => {
                const passed = byStatus.dat.length;
                const waiting = byStatus.cho_duyet.length;
                const doing = byStatus.dang_lam.length;
                const focus = gate.id === session.gate;
                return (
                  <li key={gate.id} className={`rounded-xl border p-2.5 ${focus ? "border-primary bg-primary-soft" : "border-line"}`}>
                    <div className="flex items-baseline justify-between gap-2">
                      <span className="text-sm text-ink">
                        <strong>{gate.id}</strong> {gate.title}
                      </span>
                      <span className="shrink-0 text-xs font-bold tabular-nums text-ink">
                        {passed}/{total} đạt
                      </span>
                    </div>
                    <div className="mt-1.5 flex h-2 overflow-hidden rounded-full bg-surface-2" aria-hidden>
                      <i className="block bg-ok" style={{ width: `${total ? (passed / total) * 100 : 0}%` }} />
                      <i className="block bg-warn" style={{ width: `${total ? (waiting / total) * 100 : 0}%` }} />
                      <i className="block bg-primary/40" style={{ width: `${total ? (doing / total) * 100 : 0}%` }} />
                    </div>
                    {(waiting > 0 || doing > 0) && (
                      <p className="mt-1 text-xs text-muted">
                        {[waiting ? `${waiting} chờ duyệt` : "", doing ? `${doing} đang làm` : ""].filter(Boolean).join(" · ")}
                      </p>
                    )}
                  </li>
                );
              })}
            </ul>
            {focusGate && session.gateCheck && (
              <p className="mt-2 text-xs text-muted">
                Cuối buổi {session.no} chốt {focusGate.gate.id}: còn {total - focusGate.byStatus.dat.length} em chưa đạt.
              </p>
            )}
          </div>

          <div>
            <h5 className={subhead}>Cần kèm trước buổi kế ({board.behind.length})</h5>
            {board.behind.length ? (
              <ul className="mt-2 max-h-72 space-y-1.5 overflow-y-auto">
                {board.behind.map((item) => (
                  <li key={item.id}>
                    <button type="button" onClick={() => onOpenStudent(item.id)} className="flex min-h-[44px] w-full items-center justify-between gap-2 rounded-xl border border-line p-2.5 text-left hover:border-primary">
                      <span>
                        <strong className="block text-sm text-ink">{item.name}</strong>
                        <small className="text-xs text-muted">{item.reasons.join(" · ")}</small>
                      </span>
                      <ArrowRight size={15} className="shrink-0 text-muted" aria-hidden />
                    </button>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="mt-2 text-sm text-muted">Chưa em nào chậm cổng đã chốt hay bỏ chuẩn bị từ 2 buổi.</p>
            )}
          </div>

          <button type="button" onClick={() => onOpenTab("grades")} className={rowBtn}>
            <span className="text-sm font-semibold text-ink">Bảng điểm quá trình</span>
            <ArrowRight size={16} className="shrink-0 text-muted" aria-hidden />
          </button>
        </Phase>
      </div>

      <details className="rounded-2xl border border-line bg-panel">
        <summary className="flex min-h-[48px] cursor-pointer items-center justify-between gap-3 px-4 text-sm font-bold text-ink sm:px-5">
          <span>Phạm vi bài đang mở cho lớp</span>
          <span className="rounded-full bg-surface-2 px-2.5 py-1 text-xs text-muted">
            {CNC_FLIP_LESSONS.filter((item) => openLessons.includes(item.id)).length}/{CNC_FLIP_LESSONS.length} bài
          </span>
        </summary>
        <div className="grid gap-2 px-4 pb-4 sm:grid-cols-2 sm:px-5 xl:grid-cols-4">
          {CNC_FLIP_LESSONS.map((lesson) => {
            const opened = openLessons.includes(lesson.id);
            return (
              <button
                key={lesson.id}
                type="button"
                disabled={releaseBusy}
                aria-pressed={opened}
                onClick={() => onToggleLesson(lesson.id)}
                className={`flex min-h-[44px] items-center justify-between gap-2 rounded-xl border px-3 text-left text-sm font-semibold disabled:opacity-50 ${opened ? "border-primary bg-primary-soft text-ink" : "border-line text-muted"}`}
              >
                <span>
                  Bài {lesson.no} · {lesson.name}
                </span>
                {opened ? <CheckCircle2 size={16} className="shrink-0 text-ok" aria-hidden /> : <LockKeyhole size={15} className="shrink-0" aria-hidden />}
              </button>
            );
          })}
        </div>
      </details>
    </div>
  );
}

const linkBtn = "inline-flex min-h-[40px] items-center gap-1.5 rounded-xl border border-line px-3 text-xs font-bold text-ink hover:border-primary hover:text-primary";
const rowBtn = "flex min-h-[52px] w-full items-center justify-between gap-3 rounded-xl border border-line p-3 text-left hover:border-primary";
const subhead = "flex items-center gap-1.5 text-sm font-bold text-ink";

function Phase({ step, icon, title, hint, children }: { step: number; icon: React.ReactNode; title: string; hint: string; children: React.ReactNode }) {
  return (
    <section className="rounded-2xl border border-line bg-panel p-4 sm:p-5">
      <header className="flex items-start gap-3 border-b border-line pb-3">
        <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-primary text-sm font-bold text-white">{step}</span>
        <div>
          <h4 className="flex items-center gap-1.5 font-display text-base font-bold text-ink">
            {icon} {title}
          </h4>
          <p className="text-xs text-muted">{hint}</p>
        </div>
      </header>
      <div className="mt-4 space-y-4">{children}</div>
    </section>
  );
}

function Stat({ value, label }: { value: string; label: string }) {
  return (
    <div className="rounded-xl border border-line bg-surface-2 p-2.5">
      <strong className="block text-xl tabular-nums text-ink">{value}</strong>
      <small className="text-xs text-muted">{label}</small>
    </div>
  );
}

function Station({ title, task }: { title: string; task: string }) {
  return (
    <div className="rounded-xl border border-line bg-surface-2 p-3">
      <strong className="block text-xs font-bold uppercase tracking-wide text-muted">{title}</strong>
      <p className="mt-1 text-sm text-ink">{task}</p>
    </div>
  );
}

function Empty({ children }: { children: React.ReactNode }) {
  return <p className="rounded-xl border border-dashed border-line p-4 text-sm text-muted">{children}</p>;
}

function NameChips({ items, onOpen }: { items: { id: string; name: string }[]; onOpen: (id: string) => void }) {
  return (
    <div className="mt-2 flex flex-wrap gap-1.5">
      {items.map((item) => (
        <button key={item.id} type="button" onClick={() => onOpen(item.id)} className="min-h-[36px] rounded-lg border border-line px-2.5 text-xs font-semibold text-ink hover:border-primary">
          {item.name}
        </button>
      ))}
    </div>
  );
}

function Group({ tone, label, items, onOpen, empty }: { tone: "ok" | "warn"; label: string; items: { id: string; name: string }[]; onOpen: (id: string) => void; empty: string }) {
  return (
    <details className="rounded-xl border border-line" open={tone === "warn"}>
      <summary className={`flex min-h-[44px] cursor-pointer items-center px-3 text-sm font-bold ${tone === "ok" ? "text-ok" : "text-warn"}`}>{label}</summary>
      <div className="px-3 pb-3">{items.length ? <NameChips items={items} onOpen={onOpen} /> : <p className="text-sm text-muted">{empty}</p>}</div>
    </details>
  );
}
