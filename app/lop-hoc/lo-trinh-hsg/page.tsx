"use client";

import Link from "next/link";
import { useEffect, useMemo, useState, useSyncExternalStore } from "react";
import { ArrowLeft } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { useAuth } from "@/components/auth/AuthProvider";
import TeacherViewBanner from "@/components/auth/TeacherViewBanner";
import { useTeacherView } from "@/components/auth/useTeacherView";
import { supabaseConfigured } from "@/services/supabase";
import { fetchLessonsStatic } from "@/services/static-content";
import { fetchMyProgressMarks, summarizeLessonProgress, type LessonWithItemRefs, type MyProgressMarks } from "@/services/lessons";
import { HSG_HREF } from "@/services/academic-subjects";
import {
  HSG9_EXAM_DATE,
  HSG9_EXAM_LABEL,
  HSG9_SESSIONS,
  daysBetween,
  ddmm,
  loadTicks,
  reviewDue,
  saveTicks,
  todayTaskIndex,
  todayVn,
  upcomingSession,
  type Hsg9Session,
} from "@/features/hsg9/lo-trinh";
import { SessionLessons, TaskList, type LessonProgressMap } from "@/components/lop-hoc/Hsg9Parts";

/**
 * Nguồn ngoài (URL, localStorage) đọc qua useSyncExternalStore thay vì setState trong effect.
 * Dấu tick là ghi chép riêng trên máy nên giữ trong một store nhỏ ở phạm vi module.
 */
const EMPTY_TICKS: Record<string, boolean> = {};
let ticksStore: { key: string; value: Record<string, boolean> } | null = null;
const ticksListeners = new Set<() => void>();

function subscribeTicks(listener: () => void): () => void {
  ticksListeners.add(listener);
  return () => {
    ticksListeners.delete(listener);
  };
}

function readTicksSnapshot(key: string): Record<string, boolean> {
  if (!ticksStore || ticksStore.key !== key) ticksStore = { key, value: loadTicks(key) };
  return ticksStore.value;
}

function commitTicks(key: string, value: Record<string, boolean>) {
  ticksStore = { key, value };
  saveTicks(key, value);
  for (const listener of ticksListeners) listener();
}

const subscribeNoop = () => () => {};

/** Ngày xem lộ trình: ?ngay=yyyy-mm-dd nếu hợp lệ, ngược lại là hôm nay (giờ VN). */
function readTodaySnapshot(): string {
  const ngay = new URLSearchParams(window.location.search).get("ngay");
  return ngay && /^\d{4}-\d{2}-\d{2}$/.test(ngay) ? ngay : todayVn();
}

/**
 * Lộ trình 18 buổi thứ Bảy của khoá HSG Vật lí 9 cho học sinh.
 * Thứ tự theo việc cần làm (G3, N1): tuần này → ôn lại → các buổi sắp tới; buổi đã qua thu gọn.
 * Không điểm thưởng/xếp hạng (L3): tiến độ bài lấy từ dấu đã học của chính em, dấu tick là ghi chép riêng.
 */
export default function LoTrinhHsgPage() {
  const { session } = useAuth();
  const { isTeacherView } = useTeacherView();
  const userId = session?.user.id ?? null;
  // ?ngay=yyyy-mm-dd: xem trước lộ trình như vào ngày đó (thầy soát, hoặc em xem tuần sau).
  const today = useSyncExternalStore<string | null>(subscribeNoop, readTodaySnapshot, () => null);
  const ticksKey = userId && !isTeacherView ? userId : null;
  const ticks = useSyncExternalStore<Record<string, boolean>>(
    subscribeTicks,
    () => (ticksKey ? readTicksSnapshot(ticksKey) : EMPTY_TICKS),
    () => EMPTY_TICKS,
  );
  const [lessons, setLessons] = useState<LessonWithItemRefs[] | null>(null);
  const [marks, setMarks] = useState<MyProgressMarks | null>(null);

  useEffect(() => {
    if (supabaseConfigured) fetchLessonsStatic(setLessons).then(setLessons).catch(() => setLessons([]));
  }, []);

  useEffect(() => {
    if (!userId || !supabaseConfigured || isTeacherView) return;
    let cancelled = false;
    fetchMyProgressMarks(userId)
      .then((result) => {
        if (!cancelled) setMarks(result);
      })
      .catch(() => {
        if (!cancelled) setMarks(null);
      });
    return () => {
      cancelled = true;
    };
  }, [userId, isTeacherView]);

  const progress: LessonProgressMap | null = useMemo(
    () => (isTeacherView || !lessons || !marks ? null : summarizeLessonProgress(lessons, marks)),
    [isTeacherView, lessons, marks],
  );

  const toggle = userId && !isTeacherView
    ? (id: string) => {
        commitTicks(userId, { ...ticks, [id]: !ticks[id] });
      }
    : null;

  const current = today ? upcomingSession(today) : null;
  const past = today ? HSG9_SESSIONS.filter((s) => s.date < today) : [];
  const later = current ? HSG9_SESSIONS.filter((s) => s.date > current.date) : [];
  const review = today ? reviewDue(today) : [];
  const daysToExam = today ? daysBetween(today, HSG9_EXAM_DATE) : 0;

  return (
    <>
      <Navbar />
      <main className="min-h-screen w-full bg-bg">
        <div className="mx-auto w-full max-w-2xl px-4 pb-20 pt-24 sm:px-6">
          <TeacherViewBanner />
          <Link href={HSG_HREF} className="lesson-link inline-flex min-h-11 items-center gap-1 text-sm">
            <ArrowLeft className="h-4 w-4" aria-hidden /> Khoá HSG Vật lí 9
          </Link>
          <h1 className="mt-2 text-2xl font-bold text-ink">Lộ trình 18 buổi thứ Bảy</h1>
          <p className="mt-1 text-sm text-muted">
            Thi cấp thành phố {HSG9_EXAM_LABEL}
            {daysToExam > 0 && ` · còn ${Math.ceil(daysToExam / 7)} tuần`}. Lý thuyết và bài tập mẫu em tự học ở nhà
            khoảng 1 giờ mỗi ngày; thứ Bảy trên lớp chỉ làm bài khó.
          </p>

          {!today ? null : current ? (
            <section className="mt-6 rounded-2xl border border-line bg-panel p-4" aria-labelledby="tuan-nay">
              <p className="text-xs font-semibold uppercase tracking-wide text-muted">
                Tuần này · buổi {current.buoi} · thứ Bảy {ddmm(current.date)}
              </p>
              <h2 id="tuan-nay" className="mt-1 text-lg font-semibold text-ink">
                {current.chuDe}
              </h2>
              {current.kiemTra && <p className="mt-0.5 text-sm text-warn">{current.kiemTra}</p>}

              {current.tuHoc.length > 0 && (
                <div className="mt-3">
                  <TaskList
                    session={current}
                    ticks={ticks}
                    onToggle={toggle}
                    todayIndex={todayTaskIndex(current, today)}
                  />
                </div>
              )}
              {current.btvn && (
                <p className="mt-3 rounded-lg bg-bg p-3 text-sm text-ink">
                  <span className="font-semibold">Bài tập về nhà: </span>
                  {current.btvn}
                </p>
              )}
              <div className="mt-3">
                <SessionLessons session={current} lessons={lessons} progress={progress} />
              </div>
              <p className="mt-2 text-xs text-muted">
                {userId
                  ? "Dấu tick là ghi chép riêng của em, lưu trên máy này. Tiến độ bài (số mục) tự cập nhật khi em học trên web."
                  : "Đăng nhập để đánh dấu việc đã làm và xem tiến độ bài."}{" "}
                Sau 22 giờ thì nghỉ, việc còn lại làm bù ngày hôm sau.
              </p>
            </section>
          ) : (
            <p className="mt-6 text-sm text-muted">Khoá đã kết thúc. Chúc các em thi tốt!</p>
          )}

          {review.length > 0 && (
            <section className="mt-4 rounded-2xl border border-line bg-panel p-4" aria-labelledby="on-lai">
              <h2 id="on-lai" className="text-base font-semibold text-ink">
                Ôn lại tuần này
              </h2>
              <p className="mt-1 text-sm text-muted">
                Học cách đây khoảng 4 tuần. Làm lại 3 bài em từng sai, gập lời giải trước khi làm — nhớ lâu hơn đọc lại.
              </p>
              {review.map((s) => (
                <div key={s.buoi} className="mt-2">
                  <SessionLessons session={s} lessons={lessons} progress={progress} />
                </div>
              ))}
            </section>
          )}

          {later.length > 0 && (
            <section className="mt-6" aria-labelledby="sap-toi">
              <h2 id="sap-toi" className="text-base font-semibold text-ink">
                Các buổi sắp tới
              </h2>
              <ol className="mt-2 space-y-2">
                {later.map((s) => (
                  <SessionRow key={s.buoi} s={s} lessons={lessons} progress={progress} ticks={ticks} onToggle={null} />
                ))}
                <li className="rounded-xl border border-line bg-panel px-4 py-3 text-sm">
                  <span className="font-semibold text-ink">Thứ Tư 24/02 · Thi cấp thành phố</span>
                  <span className="block text-muted">Tự luận 120 phút.</span>
                </li>
              </ol>
            </section>
          )}

          {past.length > 0 && (
            <details className="mt-6">
              <summary className="flex min-h-11 cursor-pointer items-center text-base font-semibold text-ink">
                Đã qua ({past.length} buổi)
              </summary>
              <ol className="mt-2 space-y-2">
                {past.map((s) => (
                  <SessionRow key={s.buoi} s={s} lessons={lessons} progress={progress} ticks={ticks} onToggle={toggle} />
                ))}
              </ol>
            </details>
          )}

          <details className="mt-4">
            <summary className="flex min-h-11 cursor-pointer items-center text-base font-semibold text-ink">
              Một buổi thứ Bảy 3 giờ gồm gì
            </summary>
            <ul className="mt-2 space-y-1 text-sm text-ink">
              <li>0:00–0:30: đề mini 3 câu làm giấy (2 câu bài cũ, 1 câu bài tuần này), chấm chéo.</li>
              <li>0:30–1:00: chữa đề mini, ghi sổ lỗi.</li>
              <li>1:00–2:15: chuyên đề mới, 3–4 bài khó; em giải trước rồi mới chữa.</li>
              <li>2:15–2:50: một bài tự luận kiểu đề thật, hoặc bài thí nghiệm – xử lý số liệu.</li>
              <li>2:50–3:00: chốt từ khoá, nhận việc tuần sau trên web.</li>
            </ul>
            <p className="mt-2 text-sm text-muted">Buổi có kiểm tra: bài 60 phút và chữa 30 phút thay cho đề mini.</p>
          </details>
        </div>
      </main>
      <Footer variant="app" />
    </>
  );
}

function SessionRow({
  s,
  lessons,
  progress,
  ticks,
  onToggle,
}: {
  s: Hsg9Session;
  lessons: LessonWithItemRefs[] | null;
  progress: LessonProgressMap | null;
  ticks: Record<string, boolean>;
  /** Buổi đã qua vẫn đánh dấu được (làm bù); buổi sắp tới chỉ xem trước. */
  onToggle: ((id: string) => void) | null;
}) {
  const hasDetail = s.tuHoc.length > 0 || s.lessons.length > 0;
  const head = (
    <span className="min-w-0">
      <span className="block text-xs text-muted">
        Buổi {s.buoi} · thứ Bảy {ddmm(s.date)}
        {s.kiemTra && <span className="text-warn"> · {s.kiemTra}</span>}
      </span>
      <span className="block text-sm font-medium text-ink">{s.chuDe}</span>
    </span>
  );
  if (!hasDetail) return <li className="rounded-xl border border-line bg-panel px-4 py-3">{head}</li>;
  return (
    <li className="rounded-xl border border-line bg-panel">
      <details>
        <summary className="flex min-h-11 cursor-pointer items-center px-4 py-3">{head}</summary>
        <div className="space-y-2 px-4 pb-3">
          {s.tuHoc.length > 0 && <TaskList session={s} ticks={ticks} onToggle={onToggle} />}
          <SessionLessons session={s} lessons={lessons} progress={progress} />
        </div>
      </details>
    </li>
  );
}
